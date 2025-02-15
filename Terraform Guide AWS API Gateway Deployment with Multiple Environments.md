# Terraform Guide: AWS API Gateway Deployment with Multiple Environments

This guide provides a **step-by-step Terraform configuration** for deploying an **AWS API Gateway (EnsarAPI)** with a multi-environment setup. It covers advanced topics like environment-specific settings, internal load balancing with a VPC Link integration, custom domain names with SSL, and best practices for structuring Terraform code and state. The target audience is experienced Terraform users looking to implement a robust API Gateway deployment for **Development (dev)**, **Integration (int)**, **Staging (stg)**, and **Production (prd)** environments, potentially serving multiple business units. Each section below breaks down the tasks and configurations required.

## 1. Environment Setup

In a multi-environment architecture, we want isolated configurations for each environment (dev, int, stg, prd) while reusing common patterns. Terraform supports this through **workspaces**, **input variables**, or simply separate directories/configurations per environment. The goal is to avoid hard-coding values and ensure differences (like region or DNS zone) are abstracted.

### 1.1 Organizing Environments

It’s a best practice to **isolate each environment’s state and configuration**. This can be achieved by using separate Terraform state files or workspaces for dev, int, stg, prd ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)). A common pattern is to maintain **separate directories** for each environment, each serving as the root module for that environment ([Simplifying Terraform Multiple Environments: A Step-by-Step Approach | Zeet.co](https://zeet.co/blog/terraform-multiple-environments#:~:text=When%20using%20separate%20directories%20for,its%20variables%20and%20provider%20configurations)). For example:

```
terraform/
├── modules/                # Reusable modules
│   ├── api_gateway/        # Module for API Gateway and integrations
│   ├── network/            # Module for VPC, subnets, NLB, etc.
│   └── ...
└── environments/
    ├── dev/
    │   ├── main.tf         # Calls modules with dev-specific variables
    │   ├── variables.tf    # Variables for dev environment
    │   └── terraform.tfvars# (optional) values for dev
    ├── stg/
    │   └── ...             # Similar structure for staging
    ├── prd/
    │   └── ...             # Production config
    └── int/
        └── ...             # Integration config
```

Each environment directory has its own Terraform configuration which calls the reusable modules with environment-specific inputs. This provides **complete isolation** for environments and easier management of settings like region or account IDs ([Simplifying Terraform Multiple Environments: A Step-by-Step Approach | Zeet.co](https://zeet.co/blog/terraform-multiple-environments#:~:text=Benefits%20of%20Separate%20Directories%20for,Each%20Environment)). The trade-off is some duplication of config files across environments, but that is mitigated by using modules for the common code.

### 1.2 Environment-Specific Configuration

For each environment, define specific values such as AWS region, environment name, and DNS zone. These can be defined as Terraform variables:

```hcl
# variables.tf (common or module input variables)
variable "environment" {
  description = "Deployment environment (dev, int, stg, prd)"
  type        = string
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
}

variable "dns_zone_name" {
  description = "DNS zone domain name for custom domains in this environment"
  type        = string
}
```

In each environment’s configuration (e.g., `environments/dev/terraform.tfvars`), set the values:

```hcl
# environments/dev/terraform.tfvars
environment  = "dev"
aws_region   = "us-east-1"              # example region for dev
dns_zone_name = "dev.example.com"       # DNS zone or domain for dev environment
```

Repeat similarly for `int`, `stg`, `prd` with their respective values (production might use `prod.example.com`, etc.). Using distinct DNS zones or subdomains per environment helps avoid naming collisions and clearly delineates environments.

**Tips:**

- You might use a naming convention throughout Terraform resources that incorporates the environment. For example, tags and resource names could include the env suffix (e.g., `Name = "EnsarAPI-${var.environment}"`). This ensures resources are easily identifiable by environment.
- Keep provider configurations flexible. If each environment uses a different AWS account or region, you can specify the provider’s region per environment. For example:

  ```hcl
  provider "aws" {
    region = var.aws_region
  }
  ```

- Optionally, use Terraform workspaces for environments if you prefer a single configuration. However, using separate directories (or Terraform Cloud workspaces) is often clearer and provides stronger isolation ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)) ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)).

By the end of this step, you should have the baseline structure to deploy to multiple environments with environment-specific variables in place.

## 2. Network Configuration

Next, set up the network components required for the internal microservices that the API Gateway will integrate with. We will create an **internal Network Load Balancer (NLB)** to route API Gateway requests to backend services. The NLB will span multiple Availability Zones for high availability and use **cross-zone load balancing** to evenly distribute traffic across zones.

### 2.1 VPC and Subnets

This guide assumes an existing VPC is in place for your environments (perhaps one per environment or a shared VPC segmented by env). If not, you would first create a VPC and subnets via Terraform (not detailed here). For our purposes, ensure you have at least **two private subnets** in distinct Availability Zones for the NLB's targets. These subnets will host the microservice tasks/instances (for example, ECS tasks or EC2 instances running your backend services).

We will attach the NLB to these two subnets to achieve multi-AZ resilience. For example:

```hcl
# Data source to get subnet IDs by tags or names (assuming subnets are tagged by environment and type)
data "aws_subnet_ids" "private_subnets" {
  vpc_id = var.vpc_id
  # Filter for private subnets for this env, e.g., using tags
  tags = {
    Environment = var.environment
    Tier        = "Private"
  }
}
```

This data source filters subnets in the VPC by tags (adjust filtering to your setup). It will output a list of private subnet IDs for use in the NLB.

### 2.2 Internal NLB with Cross-Zone Load Balancing

Create the Network Load Balancer resource using Terraform’s `aws_lb`. We want an **internal NLB** (not internet-facing) because API Gateway will call it from within AWS via a VPC Link. By setting the NLB as internal, it will have a private IP and not be publicly reachable ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=A%20load%20balancer%20doesn%E2%80%99t%20always,live%20in%20a%20private%20subnet)). We also enable cross-zone load balancing to improve distribution:

```hcl
resource "aws_lb" "ensar_nlb" {
  name               = "${var.environment}-ensar-nlb"
  load_balancer_type = "network"
  internal           = true                        # Make the LB internal (private)  ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=A%20load%20balancer%20doesn%E2%80%99t%20always,live%20in%20a%20private%20subnet))
  subnets            = data.aws_subnet_ids.private_subnets.ids

  enable_cross_zone_load_balancing = true          # Enable cross-AZ load balancing  ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=type%2C%20so%20you%E2%80%99ve%20got%20to,read%20the%20documentation%20carefully))
  tags = {
    Name        = "${var.environment}-Ensar-NLB"
    Environment = var.environment
    Application = "EnsarAPI"
  }
}
```

A few notes on this configuration:

- `internal = true` ensures the NLB is not publicly accessible and can live in the private subnets ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=A%20load%20balancer%20doesn%E2%80%99t%20always,live%20in%20a%20private%20subnet)).
- `enable_cross_zone_load_balancing = true` allows the NLB to distribute traffic evenly across availability zones, which **helps prevent downtime** if one AZ has issues ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=type%2C%20so%20you%E2%80%99ve%20got%20to,read%20the%20documentation%20carefully)). (Be aware that cross-zone traffic might incur additional cost, but it improves resiliency.)
- We attach environment and application tags for clarity.

### 2.3 Target Groups for Microservices

For each backend microservice that the API Gateway needs to call, define a target group on the NLB. Each **AWS API Gateway integration (via VPC Link)** will send requests to one of these target groups. With an NLB, target groups are typically configured for either instance IDs, IP addresses, or AWS Lambda as targets. In our case, we assume ECS or EC2, so we'll use instance or IP mode as appropriate. We’ll also define health checks for targets.

Suppose we have two microservices corresponding to different API functions (for example, one for **Import/Export** operations and one for **Checkout/Checkin** operations). We'll create two target groups:

```hcl
# Example target group for Import/Export service
resource "aws_lb_target_group" "import_service_tg" {
  name        = "${var.environment}-tg-import"
  port        = 80                   # The port your import service listens on
  protocol    = "HTTP"
  target_type = "ip"                 # or "instance", depending on your deployment
  vpc_id      = var.vpc_id

  health_check {
    path                = "/health"  # Assuming the service has a health endpoint
    protocol            = "HTTP"
    healthy_threshold   = 3
    unhealthy_threshold = 2
    interval            = 30
    timeout             = 5
  }

  tags = {
    Environment = var.environment
    Service     = "ImportExport"
  }
}

# Target group for Checkout service
resource "aws_lb_target_group" "checkout_service_tg" {
  name        = "${var.environment}-tg-checkout"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path = "/health"
    protocol = "HTTP"
  }

  tags = {
    Environment = var.environment
    Service     = "Checkout"
  }
}
```

Repeat similar `aws_lb_target_group` resources for any additional microservices. In our scenario with endpoints like Import (async and sync), Export (including OAS3 export), and Checkout/Cancel/Checkin, you might have a few target groups:

- One for import/export operations,
- One for checkout/checkin operations,
- (If “Import Async” and “Import Async Status” are handled by a different service or component, that could be another target group, or they might be part of the import service.)

The exact mapping of endpoints to target groups can vary. You could use a single target group for multiple related endpoints if one microservice handles them, or separate target groups per endpoint if they are distinct services. The configuration above is just an example grouping by functionality.

### 2.4 NLB Listeners and Port Mapping

An NLB listener binds a frontend port to a backend target group. Since our API Gateway will invoke the NLB on specific ports (one per microservice), we set up listeners accordingly. For example, use port **80** for the Import/Export service and **81** for the Checkout service (just an example port; you could use any distinct port numbers that your services will use):

```hcl
# Listener for Import service on port 80
resource "aws_lb_listener" "import_listener" {
  load_balancer_arn = aws_lb.ensar_nlb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.import_service_tg.arn
  }
}

# Listener for Checkout service on port 81
resource "aws_lb_listener" "checkout_listener" {
  load_balancer_arn = aws_lb.ensar_nlb.arn
  port              = 81
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.checkout_service_tg.arn
  }
}
```

We have now configured an **internal NLB** that listens on two ports (80 and 81 in this example). Traffic coming to the NLB on port 80 will go to the Import service’s target group, and traffic on port 81 will go to the Checkout service’s target group. You can add as many listeners as needed for additional microservices (e.g., a listener on 82 for another service, etc.). According to AWS, you only need **one NLB (and one VPC Link)** per VPC even if multiple services are integrated – by using multiple listeners you can route to different services ([Set up a Network Load Balancer for API Gateway private integrations - Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-nlb-for-vpclink-using-console.html#:~:text=For%20each%20VPC%20you%20have,API%20with%20a%20private%20integration)).

**Summary**: At this stage, we have the network load balancer (`aws_lb`) spanning two subnets (two AZs), with cross-zone load balancing enabled, and target groups + listeners configured for each backend service. The NLB is internal-only, meaning it’s accessible only within the VPC (which is what we want for API Gateway's private integration).

## 3. API Gateway Configuration

With the network ready, we configure the **AWS API Gateway** (REST API) that will expose the endpoints. We’ll create a single REST API called **EnsarAPI** that will be parameterized per environment and capable of serving multiple business units. The API Gateway will use **request validation** to ensure incoming requests meet the defined schema (body and parameters) before reaching our backend.

### 3.1 Defining the REST API

Terraform provides the `aws_api_gateway_rest_api` resource to define an API. We can define EnsarAPI with a meaningful name including environment and perhaps business unit context if needed. For example:

```hcl
resource "aws_api_gateway_rest_api" "ensar" {
  name        = "EnsarAPI-${var.environment}"   # e.g., "EnsarAPI-dev", "EnsarAPI-stg"
  description = "Ensar API Gateway for ${var.environment} environment"

  endpoint_configuration {
    types = ["REGIONAL"]  # Use a regional API endpoint; we'll attach custom domain
  }

  tags = {
    Environment = var.environment
    Application = "EnsarAPI"
  }
}
```

Here we use a **Regional** API endpoint, which keeps the traffic within the region (as opposed to EDGE optimized). Since we plan to attach a custom domain and our clients are likely in the same region or using an internal approach, Regional is appropriate. (If needed, Edge optimized could be used for global CDN caching, but then ACM certs must be in us-east-1. We'll stick to Regional per environment for simplicity.)

The API is now defined but has no resources (paths) or methods yet. We included tags for environment and application.

### 3.2 Request Validation Setup

API Gateway can validate incoming requests to ensure the body payload and parameters meet our expectations **before** invoking the backend. In Terraform, an `aws_api_gateway_request_validator` resource enables this for a given API. We want to validate **both the request body and request parameters (query strings and headers)**, so we'll configure accordingly:

```hcl
resource "aws_api_gateway_request_validator" "ensar_validator" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  name        = "validate-body-and-params"
  validate_request_body       = true
  validate_request_parameters = true
}
```

This creates a request validator named "validate-body-and-params" for EnsarAPI which will check both body and parameters ([AWS API Gateway Request Validator - Examples and best practices | Shisho Dojo](https://shisho.dev/dojo/providers/aws/API_Gateway/aws-api-gateway-request-validator/#:~:text=resource%20,true%20validate_request_parameters%20%3D%20true)). We will later attach this validator to methods to enforce validation.

For body validation to be meaningful, you typically define **API Gateway Models** (JSON schema definitions for the request body). This is an advanced topic; if you provide a model and content type for the request, API Gateway will validate the JSON body against that schema. For brevity, we won't define full models for each endpoint here, but note that it’s possible to use `aws_api_gateway_model` resources to define JSON Schema for, say, an Import request payload, and then link it to the method’s request setup. Without a model, enabling `validate_request_body = true` will only check that a body is present (and well-formed JSON if content-type is JSON) but not the internal structure.

### 3.3 Secure IAM Roles for API Gateway (Logging)

As a best practice, enable **CloudWatch Logs** for your API Gateway and ensure it has permission to publish logs. AWS API Gateway uses an internal CloudWatch Logs role (an IAM role) for logging. Terraform’s `aws_api_gateway_account` resource can specify this role. We'll create an IAM role with a policy for CloudWatch Logs and assign it:

```hcl
resource "aws_iam_role" "apigateway_cloudwatch_role" {
  name = "apigateway-${var.environment}-cw-role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": { "Service": "apigateway.amazonaws.com" },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

# Attach AWS managed policy for APIGW to write CloudWatch Logs
resource "aws_iam_role_policy_attachment" "apigw_logs" {
  role       = aws_iam_role.apigateway_cloudwatch_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

# Configure API Gateway account to use this role for logging
resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.apigateway_cloudwatch_role.arn
}
```

The above ensures API Gateway can assume the role and the role has the managed policy to publish logs to CloudWatch. The `aws_api_gateway_account` resource applies at the account level (one per AWS account) and will affect all API Gateways in that account, granting them the ability to send logs. (If this is already set up in your account, Terraform might manage it or skip if unchanged.)

**Why this matters**: By providing `cloudwatch_role_arn`, we allow API Gateway to log request metrics and full requests/responses as configured. The role only permits necessary actions (as per the managed policy) ([Understanding the Terraform Resources that Create an AWS API Gateway REST API – QloudX](https://www.qloudx.com/understanding-the-terraform-resources-that-create-an-aws-api-gateway-rest-api/#:~:text=it%20only%20supports%20one%20argument%3A,role%20to%20allow%20CloudWatch%20access)), aligning with the principle of least privilege. This is part of **secure IAM configurations** – we explicitly control and limit what the API Gateway service can do (only log writing in this case).

### 3.4 Structuring for Multiple Business Units (BU)

The EnsarAPI is intended to support multiple business units. There are a couple of ways to structure this:

- **Single API, multiple domains**: Use one API deployment per environment, but assign multiple custom domain names (one per business unit) that point to the same API. We will cover custom domains later, but note that you can map different domains (e.g., `finance-api.dev.example.com`, `hr-api.dev.example.com`) to the same API Gateway stage. Each BU gets its own hostname, but they hit the same API infrastructure.
- **Separate API per BU**: Alternatively, deploy separate instances of the API for each BU (perhaps in separate Terraform workspaces or by passing a `business_unit` variable to the module). This increases isolation, at the cost of duplicate infrastructure.

We’ll demonstrate the first approach (one API per env, multiple domains for BUs) in the custom domain section. For now, the API resource itself (`aws_api_gateway_rest_api.ensar`) is common and can serve all BUs logically.

If needed, incorporate a variable for business unit in naming. For example, if combining environment and BU in one deployment, the API name might be `EnsarAPI-${var.business_unit}-${var.environment}` to differentiate (e.g., `EnsarAPI-finance-dev`). In our guide, we assume one environment’s Terraform can deploy for all BUs or you run separate Terraform for each BU, whichever fits your org’s process.

With the core API created and validation enabled, we can proceed to defining the specific endpoints.

## 4. API Gateway Endpoints and Methods

We will create the resources (paths) and methods in API Gateway corresponding to the required endpoints. All listed endpoints are HTTP **POST** methods, each with a distinct path, and they may require certain query parameters or headers.

The endpoints to set up (all POST):

- **/import** – Import resource (likely synchronous import)
- **/importAsync** – Initiate an asynchronous import
- **/importAsyncStatus** – Check status of an async import
- **/export** – Export resource
- **/oas3Export** – Export in OpenAPI (OAS3) format
- **/checkout** – Mark an item as checked out
- **/cancelCheckout** – Cancel a checkout
- **/checkin** – Check an item back in

We'll create each of these as a child resource of the API root and tie a POST method to them.

### 4.1 Defining Resources (Paths)

Terraform `aws_api_gateway_resource` is used to define each path segment under the API. The root resource ("/") always exists (you can get its ID via the REST API resource). We will add resources for each endpoint:

```hcl
# Get the root resource ("/") ID of the API
data "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  path        = "/"
}

# Define each API resource path
resource "aws_api_gateway_resource" "import" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "import"
}

resource "aws_api_gateway_resource" "import_async" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "importAsync"
}

resource "aws_api_gateway_resource" "import_async_status" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "importAsyncStatus"
}

# ... similarly for export, oas3Export, checkout, cancelCheckout, checkin:
resource "aws_api_gateway_resource" "export" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "export"
}
resource "aws_api_gateway_resource" "oas3_export" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "oas3Export"
}
resource "aws_api_gateway_resource" "checkout" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "checkout"
}
resource "aws_api_gateway_resource" "cancel_checkout" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "cancelCheckout"
}
resource "aws_api_gateway_resource" "checkin" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = "checkin"
}
```

This sets up all the required path resources. Now the API has the endpoints defined, but no methods attached yet.

**Note:** We used individual resources for clarity. In practice, you could generate these in a loop (e.g., using a `for_each` with a set of path names) to reduce repetitive code, since all these resources share a similar structure. For example:

```hcl
locals {
  paths = ["import", "importAsync", "importAsyncStatus", "export", "oas3Export", "checkout", "cancelCheckout", "checkin"]
}

resource "aws_api_gateway_resource" "endpoints" {
  for_each   = toset(local.paths)
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  parent_id   = data.aws_api_gateway_resource.root.id
  path_part   = each.key
}
```

And then reference them via `aws_api_gateway_resource.endpoints["import"].id`, etc. But for simplicity, we wrote them out above.

### 4.2 Attaching Methods (POST) with Validation

For each resource path, we need to define an `aws_api_gateway_method` for the POST verb. This will specify that it **accepts POST requests**, whether it requires API keys or authorization (not in scope here, we'll assume open or internal usage), and crucially, we will attach our request validator to it and require certain parameters if needed.

We will also prepare to integrate each method with our backend (that part will be in section 5). For now, let's focus on method setup:

Example for the `/import` POST method:

```hcl
resource "aws_api_gateway_method" "post_import" {
  rest_api_id   = aws_api_gateway_rest_api.ensar.id
  resource_id   = aws_api_gateway_resource.import.id
  http_method   = "POST"
  authorization = "NONE"  # Assuming no auth for now (could be AWS_IAM, CUSTOM, etc. as needed)

  request_validator_id = aws_api_gateway_request_validator.ensar_validator.id

  # Example of requiring a query parameter and a header
  request_parameters = {
    "method.request.querystring.type" : true,   # require 'type' query param
    "method.request.header.X-Request-ID" : true # require a custom header
  }
}
```

This defines that for hitting the **POST /import** endpoint:

- No authorization is required (adjust if needed, e.g., you might use an IAM authorizer or Cognito authorizer in real deployments).
- The `request_validator_id` is set, so this method will invoke the validator we created, ensuring body and parameters are checked.
- In `request_parameters`, we declare that a query string parameter `type` is required (`"method.request.querystring.type": true`) and a header `X-Request-ID` is required (`"method.request.header.X-Request-ID": true`). This is just an example. You would list whichever parameters your API expects and mark them true to make them required. If a required parameter is missing in a request, API Gateway will automatically reject the call with a 400 Bad Request before reaching integration.

We should add similar `aws_api_gateway_method` resources for each of the endpoints. They will all be quite similar since all are POST and likely use the same validator. The differences will be in required params if any:

- For asynchronous operations (`importAsync` and `importAsyncStatus`), maybe they require an ID or token as query param to track the job.
- For `checkout` and `cancelCheckout`, possibly an item ID parameter.
- For `export` and `oas3Export`, maybe a format query or something.

Document what parameters are expected for each and enforce accordingly.

For brevity, let's assume each method requires an `X-Request-ID` header for traceability, and maybe some share a common query param, or none. We will set at least one required param in the example to illustrate the mechanism.

Example for another endpoint `/checkout`:

```hcl
resource "aws_api_gateway_method" "post_checkout" {
  rest_api_id   = aws_api_gateway_rest_api.ensar.id
  resource_id   = aws_api_gateway_resource.checkout.id
  http_method   = "POST"
  authorization = "NONE"
  request_validator_id = aws_api_gateway_request_validator.ensar_validator.id

  request_parameters = {
    "method.request.header.X-Request-ID" : true
  }
}
```

This requires the X-Request-ID header but no specific query param (you could add e.g. require `itemId` in query if needed).

Repeat for each endpoint resource (post_importAsync, post_importAsyncStatus, post_export, post_oas3Export, post_cancelCheckout, post_checkin), each referencing the corresponding `aws_api_gateway_resource`. They all use the same `aws_api_gateway_request_validator.ensar_validator`.

At this point, we have API Gateway aware of the resources and methods, and it will validate requests as configured. What remains is to integrate these methods with the backend (our NLB target groups) so that real processing occurs.

## 5. Integration with Microservices

In this step, we connect each API Gateway method to the appropriate backend microservice via the NLB. AWS API Gateway (v1 REST API) supports integration types like HTTP (with VPC Link), Lambda, or AWS services. We will use the **VPC Link HTTP integration** to forward requests to our NLB’s target groups.

**VPC Link** acts as a bridge between API Gateway and our VPC network. We’ll configure one shortly (in section 6), but first, let’s set up the integration resources assuming the VPC Link and NLB are ready.

### 5.1 Configuring Method Integrations

Terraform uses `aws_api_gateway_integration` to define how an API Gateway method connects to the backend. For an HTTP integration through a VPC Link, we need:

- `connection_type` set to `VPC_LINK`
- `connection_id` pointing to our VPC Link ID
- `uri` set to the **Network Load Balancer’s DNS name** (including protocol and port)
- `integration_http_method` – for HTTP/HTTP_PROXY integrations, this is typically the same as the method (POST) or can be "ANY" for proxy.
- `type` – we have a choice of `"HTTP_PROXY"` (direct proxy) or `"HTTP"` (custom integration where you could do mapping templates). **HTTP_PROXY** is simpler and passes the request through as-is to the backend URL. We will use `HTTP_PROXY` for a straightforward proxy setup, which is common for microservice integration.

Let’s integrate the `/import` POST method to the Import service target. Suppose our NLB’s DNS is `internal-ensar-nlb-abc123.us-east-1.elb.amazonaws.com` (Terraform can output this via `aws_lb.ensar_nlb.dns_name`). The Import service is behind listener port 80 on the NLB. So the URI will be `http://internal-ensar-nlb-abc123.us-east-1.elb.amazonaws.com:80/import`. (The path `/import` can be included or not in the URI; since this is a proxy integration, API Gateway will append any path to the base URI. If our entire service is dedicated to this path, we could just use the base domain and port, but it's fine to include the specific resource path as well.)

Example integration:

```hcl
resource "aws_api_gateway_integration" "import_integration" {
  rest_api_id             = aws_api_gateway_rest_api.ensar.id
  resource_id             = aws_api_gateway_resource.import.id
  http_method             = aws_api_gateway_method.post_import.http_method  # "POST"
  integration_http_method = "POST"
  type                    = "HTTP_PROXY"
  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.ensar_link.id

  uri = "${aws_lb.ensar_nlb.dns_name}:80/import"

  # Note: If any request parameters need to be passed through differently or body mapping, we could use request_parameters or request_templates here. In a basic proxy, not needed.
}
```

Key points in this integration:

- `connection_type = "VPC_LINK"` and `connection_id` references the VPC Link we will create (placeholder here as `ensar_link`).
- `uri` uses the NLB DNS name. According to AWS, when using VPC Link, the URI should be the **Network Load Balancer DNS name** with the protocol and port ([amazon web services - API Gateway integration to an elastic beanstalk app with a VPC_LINK fails with AWS ARN for integration must contain path or action - Stack Overflow](https://stackoverflow.com/questions/76412105/api-gateway-integration-to-an-elastic-beanstalk-app-with-a-vpc-link-fails-with-a#:~:text=As%20per%20the%20CloudFormation%20documentation%2C,argument)). We include `:80/import` to direct to the correct listener and path. The scheme is `http://` since it's internal. If your NLB was configured with TLS and the targets expect HTTPS, you’d use `https://` and ensure the NLB listener is TLS.
- `type = "HTTP_PROXY"` means API Gateway will _proxy_ the request directly to the given URI (with minimal request/response transformations). This is suitable since our backend expects the same request and returns a response that we can relay.
- We set `integration_http_method = "POST"` to match the method. (For proxy integrations, API Gateway doesn't really need this to differ; it's mainly for the HTTP integration type, but we keep it consistent.)

We need to create similar `aws_api_gateway_integration` resources for each method:

- `importAsync_integration` pointing to NLB DNS on, say, port 80 as well (if the same service handles both import and importAsync, they might use the same listener. If they are different services, maybe importAsync goes to a different port/listener).
- `importAsyncStatus_integration` – likely goes to the same service handling async jobs, or could be an entirely different one that tracks statuses. For demonstration, assume it's the same as importAsync service.
- `export_integration` – maybe the same service as import (if one service does both import and export). If not, it could be another listener, say port 80 on the same service or a separate instance. We'll assume it's the same service for now for simplicity.
- `oas3Export_integration` – likely same as export service.
- `checkout_integration` – this would use the checkout service target, which we set on port 81. So its URI would be `${aws_lb.ensar_nlb.dns_name}:81/checkout`.
- `cancelCheckout_integration` – same port 81, maybe path `/cancelCheckout`.
- `checkin_integration` – same port 81, path `/checkin`.

To illustrate another integration, e.g. for checkout:

```hcl
resource "aws_api_gateway_integration" "checkout_integration" {
  rest_api_id             = aws_api_gateway_rest_api.ensar.id
  resource_id             = aws_api_gateway_resource.checkout.id
  http_method             = aws_api_gateway_method.post_checkout.http_method
  integration_http_method = "POST"
  type                    = "HTTP_PROXY"
  connection_type         = "VPC_LINK"
  connection_id           = aws_api_gateway_vpc_link.ensar_link.id

  uri = "${aws_lb.ensar_nlb.dns_name}:81/checkout"
}
```

And similarly, `cancelCheckout_integration` with `${aws_lb.ensar_nlb.dns_name}:81/cancelCheckout`, and `checkin_integration` with `${aws_lb.ensar_nlb.dns_name}:81/checkin`.

Ensure the port in the URI matches the listener port for the respective target group on the NLB. This setup aligns with the AWS guidance that each service on the NLB is distinguished by port, and you use one VPC Link for all ([Set up a Network Load Balancer for API Gateway private integrations - Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-nlb-for-vpclink-using-console.html#:~:text=For%20each%20VPC%20you%20have,API%20with%20a%20private%20integration)).

**Important**: The integration `uri` must be a valid address. We use Terraform interpolation for `aws_lb.ensar_nlb.dns_name` which is the NLB’s DNS. Alternatively, you could use the NLB’s ARN in combination with stage variables, but directly using the DNS is straightforward as per AWS documentation ([amazon web services - API Gateway integration to an elastic beanstalk app with a VPC_LINK fails with AWS ARN for integration must contain path or action - Stack Overflow](https://stackoverflow.com/questions/76412105/api-gateway-integration-to-an-elastic-beanstalk-app-with-a-vpc-link-fails-with-a#:~:text=As%20per%20the%20CloudFormation%20documentation%2C,argument)). Also note that for VPC Link integrations, **the `type` should be "HTTP_PROXY"**, as API Gateway requires when integrating with an HTTP endpoint via VPC Link ([amazon web services - API Gateway integration to an elastic beanstalk app with a VPC_LINK fails with AWS ARN for integration must contain path or action - Stack Overflow](https://stackoverflow.com/questions/76412105/api-gateway-integration-to-an-elastic-beanstalk-app-with-a-vpc-link-fails-with-a#:~:text=EDIT%3A%20As%20per%20the%20comments%2C,HTTP_PROXY)).

### 5.2 Integration Request/Response Config (Optional)

Since we chose `HTTP_PROXY`, API Gateway will automatically map the request and responses between the client and the backend. We don’t have to define explicit `aws_api_gateway_integration_response` or `aws_api_gateway_method_response` in this mode for the default 200 flow – by default, it will propagate the backend’s HTTP status code and body to the client. If we wanted to handle different responses or add mapping (for example, catch a backend 500 and map it to a different message), we would use those resources. For an advanced user guide, you might consider:

- Defining at least a generic 200 response and perhaps a 400 for validation errors and 500 for server errors.
- For each method, an `aws_api_gateway_method_response` with status code 200 (and maybe others) and an `aws_api_gateway_integration_response` that maps the backend response to these codes.

However, given our focus and the fact that proxy integration largely auto-handles this, we will not define them explicitly. The API will return whatever the microservice returns. (Just ensure your microservices return appropriate HTTP codes and CORS headers if needed.)

At this point, each API method knows where to send requests in the VPC. Now let's set up the VPC Link resource itself that makes this connectivity possible.

## 6. VPC Link

A **VPC Link** in API Gateway is an object that encapsulates the connection between API Gateway and your VPC resources (in this case, our NLB). When you create a VPC Link, AWS provisions and manages elastic network interfaces in your VPC to facilitate communications. You only need to create it once per network setup, and then multiple API Gateway integrations can use the same link.

### 6.1 Creating the VPC Link in Terraform

Terraform uses `aws_api_gateway_vpc_link` for this. We will create one VPC Link for EnsarAPI in each environment:

```hcl
resource "aws_api_gateway_vpc_link" "ensar_link" {
  name        = "${var.environment}-EnsarVPCLink"
  target_arns = [aws_lb.ensar_nlb.arn]

  tags = {
    Environment = var.environment
    Application = "EnsarAPI"
  }
}
```

**Explanation:**

- `target_arns` accepts a list of ARNs of the Network Load Balancers to integrate with. We provide our `aws_lb.ensar_nlb.arn`. (At least one is required. If you had multiple NLBs for some reason, you could list them, but in our design one NLB is enough.)
- The VPC Link will be used by our integrations (which we already referenced via `connection_id` earlier).

**Important**: The creation of a VPC Link can take some time (a few minutes) because AWS is setting up network interfaces and links. Terraform will wait until it's ready. All our `aws_api_gateway_integration` resources should depend on the VPC link being created (Terraform will handle this ordering since we referenced the VPC link ID in those resources, or we can add explicit `depends_on` if needed).

Once this resource is applied, API Gateway will have a VPC Link named like "dev-EnsarVPCLink" (for dev environment) associated with the NLB.

**Permissions Note**: In most cases, no additional user action is required for API Gateway to create the VPC Link as long as the NLB is in the same account and VPC. If the API Gateway was in a different account, you would need to ensure PrivateLink permissions and acceptor setups. Here, we assume same account. The AWS docs mention that the NLB and API must be in the same account for simplicity ([Set up a Network Load Balancer for API Gateway private integrations - Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-nlb-for-vpclink-using-console.html#:~:text=The%20Network%20Load%20Balancer%20and,by%20the%20same%20AWS%20account)), which we are following.

Now our API Gateway methods (`aws_api_gateway_integration` resources) have a valid `connection_id` to use.

After adding the VPC Link, our integration URIs become active paths. For example, API Gateway will now know how to route requests for `/checkout` through `ensar_link` into the NLB ARN we gave, on the specified port.

### 6.2 Testing the Integration (Briefly)

Although this is a Terraform guide, after deploying, a quick test in dev environment might be:

- Call the **execute-api** endpoint for dev (or custom domain once set) for the import path and see if the request reaches the service (assuming the service is up and registered in the target group).
- Use CloudWatch logs for API Gateway (if enabled) or the service logs to verify connectivity.

The heavy lifting is done. Now we focus on exposing the API to clients via a friendly domain and securing it with SSL.

## 7. SSL Certificate and Custom Domain

To make the API user-friendly and segregated by environment and business unit, we will set up **custom domain names** for each environment (and possibly per business unit). We'll also obtain SSL/TLS certificates for these domains using AWS Certificate Manager (ACM). This allows clients to use URLs like `https://api.dev.example.com/v1/import` instead of the generic `execute-api` URL.

### 7.1 Provisioning SSL Certificates (ACM)

AWS Certificate Manager (ACM) is the preferred way to handle SSL certs for API Gateway. You can request a public certificate (if you own the domain) or import an existing certificate. Terraform has `aws_acm_certificate` for requesting certificates (with validation steps), but detailing that is out of scope. We assume you have certificates created for your domains:

- For example, a certificate covering `*.dev.example.com` for dev environment, `*.stg.example.com` for staging, etc. Alternatively, one could use names like `dev-api.example.com` specifically.

If you were to use Terraform, it would look like:

```hcl
resource "aws_acm_certificate" "dev_cert" {
  domain_name       = "*.dev.example.com"
  validation_method = "DNS"
  # ... Route53 validation records, etc.
}
```

But for brevity, let's assume the certificate ARNs are known or created outside of this script. We will reference them as variables or data sources. For instance:

```hcl
variable "acm_certificate_arn" {
  description = "ACM certificate ARN for the custom domain in this environment"
  type        = string
}
```

And in `terraform.tfvars` for each env, provide the appropriate ACM ARN.

### 7.2 Creating Custom Domain Names in API Gateway

With ACM cert in hand, we create an `aws_api_gateway_domain_name` resource. This binds a hostname to API Gateway and associates the SSL certificate. We will do this for each needed domain.

If supporting multiple business units, you might have multiple domain names pointing to the same API. You can accomplish that by creating multiple `aws_api_gateway_domain_name` resources (one per domain).

For example, let's say in **dev** environment we have two BUs: finance and hr. We want:

- `finance-api.dev.example.com`
- `hr-api.dev.example.com`

Both will map to the dev EnsarAPI. We will create two domain name resources in dev. In staging/prod, similarly.

Example Terraform using a loop for BUs:

```hcl
variable "business_units" {
  type    = list(string)
  default = ["finance", "hr"]  # example BUs
}

resource "aws_api_gateway_domain_name" "custom_domain" {
  for_each        = toset(var.business_units)
  domain_name     = "${each.key}-api.${var.environment}.example.com"
  certificate_arn = var.acm_certificate_arn
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  tags = {
    Environment = var.environment
    BusinessUnit = each.key
  }
}
```

This will create, for environment=dev:

- finance-api.dev.example.com
- hr-api.dev.example.com

(using the same ACM certificate if it covers both, e.g., a wildcard `*.dev.example.com` would cover both subdomains).

If each BU has a completely separate domain or certificate, adjust accordingly (e.g., use a map of BU to cert ARNs).

### 7.3 Base Path Mapping for Versioning

Now we map these domain names to our API Gateway stage. We also want to include versioning in the URL path. The question specifically suggests using **base path mapping** for version (e.g., `/v1`). This means that when users hit `https://finance-api.dev.example.com/v1/...`, API Gateway will route it to a specific stage of our API.

We haven’t created the deployment and stage yet (that’s in the next section), but we know we will have a stage (let's call it "v1" as the version identifier). Alternatively, you might name the stage "dev" and use base path "v1". It can be done either way:

- **Option A**: Stage names correspond to environments (dev, stg, prod) and base path corresponds to API version (v1, v2, etc). In custom domain mapping, you'd map base path "v1" of `finance-api.dev.example.com` to stage "dev" of the API.
- **Option B**: Stage names correspond to versions (v1, v2) and you deploy separate API per env. Then each custom domain uses base path either empty or something else.

To keep things straightforward, let’s choose **Option A**: environment as stage name, version as base path. However, since we decided earlier to deploy separate API per environment, we could also just use stage name "v1" (since only one stage is needed per env at a time). In that case, base path could be empty or also "v1". But the prompt explicitly suggests base path for versioning, so we'll use it.

We will create the base path mapping now (Terraform `aws_api_gateway_base_path_mapping`):

```hcl
# Ensure to create deployment and stage before this (we'll cover in next section).
resource "aws_api_gateway_base_path_mapping" "v1_mapping" {
  for_each    = toset(var.business_units)
  domain_name = aws_api_gateway_domain_name.custom_domain[each.key].domain_name
  stage_name  = aws_api_gateway_stage.ensar_stage.stage_name  # e.g. "v1" or "dev"
  rest_api_id = aws_api_gateway_rest_api.ensar.id

  base_path   = "v1"
}
```

This will map the base path "v1" of each custom domain to our API stage. If `stage_name` is "v1", then effectively the URL becomes `domain.com/v1` -> stage "v1". If instead we had stage "dev" and base_path "v1", then `domain.com/v1` -> stage "dev".

Let’s assume we create stage name = "v1" for simplicity (since it's version 1 of the API). In a multi-stage single-API scenario, you might have had stage "dev" but since we separated envs, we can use version as stage.

So:

- `aws_api_gateway_stage.ensar_stage.stage_name` will be "v1" (we will define that in next section).
- The base_path is "v1", matching the version.

After this mapping, any request to `finance-api.dev.example.com/v1/anything` will be routed to EnsarAPI’s **v1 stage**. Because we attached the certificate for that domain and did the mapping, API Gateway knows how to handle the custom hostname. We must also create appropriate DNS records to point the custom domain to API Gateway.

### 7.4 DNS Configuration

To use the custom domain, you need a DNS CNAME (or ALIAS if using Route 53) record that points your custom domain to the CloudFront distribution domain name that API Gateway provides for the custom domain. In a Regional API, the custom domain is actually served via an underlying CloudFront distribution in the region.

When you create `aws_api_gateway_domain_name`, Terraform will be able to output the `cloudfront_domain_name` or `regional_domain_name` depending on type. For Regional, it’s a regional domain. You then create a DNS record to map your domain.

If using Route 53 and if your DNS zone `dev.example.com` is managed in the same Terraform, you can add:

```hcl
resource "aws_route53_record" "api_dev_finance" {
  zone_id = data.aws_route53_zone.dev_zone.id  # a data source fetching the zone "dev.example.com"
  name    = "finance-api"  # finance-api.dev.example.com
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.custom_domain["finance"].cloudfront_domain_name
    zone_id                = aws_api_gateway_domain_name.custom_domain["finance"].cloudfront_zone_id
    evaluate_target_health = false
  }
}
```

Repeat for hr-api etc. (AWS API Gateway custom domains support Route53 alias which maps the CloudFront distribution directly.)

We won't delve deeper as it's standard DNS setup. Just ensure this is done so that your custom domains resolve to the API Gateway.

Now, with the custom domains in place, users (or internal clients) can use environment-specific and BU-specific URLs, and communication will be over HTTPS with valid certificates.

## 8. Deployment and Versioning

At this stage, our API Gateway configuration (resources, methods, integrations, domain mappings) is defined in Terraform. However, API Gateway will not serve traffic until we create a **Deployment** and a **Stage**. A deployment captures the current state of the API configuration and is essentially a versioned snapshot that can be invoked via a stage.

### 8.1 Creating an API Deployment

Terraform resource `aws_api_gateway_deployment` triggers the creation of a deployment. We typically want Terraform to create a new deployment when there are changes to the API configuration (like new methods). One way is to use the `triggers` argument with a hash of the current config, or simply recreate on each Terraform apply (which isn't ideal for production unless controlled). For an advanced setup, you might compute an MD5 of your OpenAPI spec or some representative string of the API resources, and use that to trigger deployment updates.

For simplicity, we'll create a deployment that depends on all methods:

```hcl
resource "aws_api_gateway_deployment" "ensar_dep" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  stage_name  = null  # We will create a separate Stage resource, so set to null or omit.

  # Use triggers to force new deployment on changes to methods/resources
  triggers = {
    redeploy = sha1(join(",", [
      aws_api_gateway_method.post_import.id,
      aws_api_gateway_method.post_import_async.id,
      aws_api_gateway_method.post_import_async_status.id,
      aws_api_gateway_method.post_export.id,
      aws_api_gateway_method.post_oas3_export.id,
      aws_api_gateway_method.post_checkout.id,
      aws_api_gateway_method.post_cancel_checkout.id,
      aws_api_gateway_method.post_checkin.id
    ]))
  }
}
```

By listing all method IDs in a trigger, any change that alters a method (and thus its ID or count) will change the hash and cause Terraform to replace the deployment, effectively creating a new deployment in API Gateway.

Alternatively, some prefer to manually deploy by running a separate Terraform step or script when needed. But the above automates it.

### 8.2 Defining the Stage

Now define a Stage for this deployment. We can either let the `aws_api_gateway_deployment` above create a stage by giving it a `stage_name`, or use a separate `aws_api_gateway_stage` resource. Using a separate resource allows more control (like stage-level settings, logging, tracing). We choose to explicitly define the stage.

We will use stage name "v1" to represent the version 1 of the API. (If we were doing multi-env in one API, we might use env names, but since each env is separate, "v1" is fine.)

```hcl
resource "aws_api_gateway_stage" "ensar_stage" {
  rest_api_id = aws_api_gateway_rest_api.ensar.id
  deployment_id = aws_api_gateway_deployment.ensar_dep.id
  stage_name   = "v1"

  description  = "Version 1 of EnsarAPI in ${var.environment}"
  variables = {
    # (Optional) stage variables if needed for your integrations
    # e.g. you could set a variable that microservices use, but not needed in our setup
  }

  access_log_settings {
    destination_arn = var.api_gw_access_log_arn # If you have a CloudWatch Log Group or Kinesis Firehose for logs
    format = "$contextRequestId$contextResourcePath..."  # Log format if needed
  }

  tags = {
    Environment = var.environment
    Version     = "v1"
  }
}
```

Important bits:

- `deployment_id` ties this stage to the deployment we created.
- `stage_name = "v1"` sets the URL base path segment for this stage (the invoke URL will contain /v1).
- We included an example `access_log_settings` block. To use it, you'd need a CloudWatch Log Group ARN or a Firehose stream ARN. If not configuring access logs at this time, you can omit it. But enabling access logs with a detailed format is very useful in production for monitoring. (If using access logs to CloudWatch, ensure the API Gateway account CloudWatch role is set, as we did.)
- Tags include environment and version.

Now our API Gateway has a deployed stage. This stage corresponds to the version of the API (v1). If in the future you build v2 of the API, you can create a new deployment and a new stage "v2" (and map it under the custom domain perhaps as /v2).

Because we already set up base path mapping in section 7 to "v1", it will direct to this stage.

### 8.3 (Optional) Stage Settings and Canary

For completeness, note that `aws_api_gateway_stage` allows many configurations:

- Logging level, data trace, throttling rates, etc.
- Canary deployments (a feature to do percentage-based traffic shifting between two deployments on the same stage, e.g., for testing new changes).
- X-Ray tracing.

If needed, you can enable X-Ray: `xray_tracing_enabled = true` on the stage, which helps with distributed tracing across API Gateway and backend (requires X-Ray to be set up).

We won't go deeper, but advanced users can tweak these settings as required by their use case.

At this point, our API is fully deployed. The **invoke URL** for this API (without custom domain) would be:

```
https://${aws_api_gateway_rest_api.ensar.id}.execute-api.${var.aws_region}.amazonaws.com/v1
```

If everything is set up, calling that URL with the appropriate path (e.g., `/import`) should route through the VPC Link to the service.

## 9. Outputs

It’s helpful to output key information from this Terraform deployment so that developers or integrated systems know the endpoints. We will output:

- The **API Gateway invoke URL** (the default AWS endpoint).
- The **Custom Domain URL** for each business unit.
- The **Stage invoke URL** (which might be same as the API Gateway URL above, since stage is included).
- Possibly the VPC Link ID or NLB DNS if needed for debugging (optional).

Here’s how we can define outputs:

```hcl
output "api_gateway_invoke_url" {
  description = "Default invoke URL for the API Gateway (execute-api domain)"
  value       = "https://${aws_api_gateway_rest_api.ensar.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.ensar_stage.stage_name}"
}

output "custom_domain_urls" {
  description = "Custom domain base URLs per business unit for this environment"
  value = { for bu, domain in aws_api_gateway_domain_name.custom_domain :
    bu => "https://${domain.domain_name}/v1" }
}

output "api_stage_arn" {
  description = "ARN of the API Gateway stage"
  value       = aws_api_gateway_stage.ensar_stage.arn
}
```

The `api_gateway_invoke_url` gives something like `https://abcde12345.execute-api.us-east-1.amazonaws.com/v1`. The `custom_domain_urls` will produce a map, e.g., for dev:

```
custom_domain_urls = {
  finance = "https://finance-api.dev.example.com/v1"
  hr      = "https://hr-api.dev.example.com/v1"
}
```

These are the base URLs; append the endpoint path (e.g., `/import`) to call specific functions.

We also output the stage ARN, which can be useful for any cross-stack references or for monitoring setups (you might use it to allow API Gateway to write logs, etc., but we already did via role).

You could also output the `aws_lb.ensar_nlb.dns_name` and `aws_api_gateway_vpc_link.ensar_link.id` if interested. For example:

```hcl
output "nlb_dns_name" {
  value = aws_lb.ensar_nlb.dns_name
}
output "vpc_link_id" {
  value = aws_api_gateway_vpc_link.ensar_link.id
}
```

But those are more internal. The main concern is to expose the endpoints.

Now, after `terraform apply`, you will see in the outputs the URLs and share them with developers or configure your client applications to call the appropriate URL per environment.

## 10. Tags and Resource Management

Throughout the configurations, we've added tags to many resources. Tagging is crucial for organizing and managing AWS resources. We included tags such as **Environment**, **Application**, **Service**, **BusinessUnit**, etc., to make it easy to filter and identify resources in the AWS console and for cost allocation.

Make sure to tag **all applicable resources**:

- VPC, Subnets (with environment, maybe).
- Security groups (if any were used).
- NLB and Target Groups (we did, with environment and service).
- API Gateway resources: Unfortunately, not all API Gateway sub-resources support tagging (the REST API itself and Stage do support tags, which we added).
- VPC Link supports tags (we added).
- IAM roles and CloudWatch log groups if created should be tagged (Terraform IAM resources support tags).
- ACM certificates can be tagged too (for tracking which environment they're for).

A consistent tagging strategy helps in cost tracking and maintenance. For example, AWS recommends categorizing resources by purpose, team, environment, etc. **Implementing a consistent tagging strategy** makes it easier to filter/search resources and monitor cost and usage ([Best Practices for Tagging AWS Resources - Best Practices for Tagging AWS Resources](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html#:~:text=on%20that%20resource,and%20manage%20your%20AWS%20environment)). If your organization has specific required tags (like `Project` or cost center), include those as well in the `tags` map.

**Cost Allocation**: Tagging each environment’s resources with an `Environment` key (`Environment=dev` etc.) allows cost explorer to break down costs by environment. Similarly, tagging by `BusinessUnit` if resources are shared among BUs ensures you can attribute costs properly ([Cost allocation tags - Best Practices for Tagging AWS Resources](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/cost-allocation-tags.html#:~:text=Resources%20docs,entity%20from%20appropriately%20tagged%20resources)).

Double-check that all critical resources have tags:

- The load balancer (we set Name and Environment).
- Target groups (we set Environment and Service).
- API Gateway (we set environment on the Rest API, Stage, and VPC Link).
- Domain names (tagged with environment and BU).
- Any S3 buckets or state resources you create for this infrastructure (if any).

It's easy to forget, for example, if you create CloudWatch Log Groups for API access logs manually, tag them too via Terraform.

---

Up to here, we've completed the main 10 sections. Next, we'll cover some additional best practices and recommendations that were requested, including Terraform module structure, CI/CD pipeline integration, and state management.

## 11. Modularizing Terraform Configuration

For a complex deployment like this, using **Terraform modules** is highly recommended. We hinted at module usage in the environment setup. To recap and detail:

- **Network Module**: Create a module (e.g., `modules/network`) that encapsulates VPC Link infrastructure – the subnets, NLB, target groups, and maybe even the VPC if needed. This module would take inputs like vpc_id, environment name, and details of services (maybe a list of service names and ports to dynamically create target groups and listeners). It would output the NLB ARN, NLB DNS name, and maybe target group ARNs if needed. In our design, network config is relatively static (two target groups, known ports). You could still parameterize the count of services or port numbers per environment if they differ.
- **API Gateway Module**: Another module could handle all API Gateway resources: rest API, resources, methods, integrations, deployment, stage, and even custom domains. This module might take inputs like environment, list of endpoints to create, business units (for domains), and target group associations (e.g., a mapping of endpoint -> target group port or ARN). It could output the URLs and any other metadata. The complexity here is higher due to many interconnected resources, but it's manageable with careful variable design and `for_each` usage.
- **Main or Environment Module**: Alternatively, one could create a top-level module that combines both network and API gateway and use it per environment (maybe even per BU). For example, a module that takes env and BU and stands up the NLB and API for that combination. However, that might duplicate NLB per BU which we decided not to do (we used one NLB for all BUs in env). So it's cleaner to have one env at a time.

Using modules ensures **reusability** and reduces errors. Common logic is written once. It aligns with best practice of _dividing your configuration by business function and environment_ ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)). For instance, network setup is one function, API gateway is another. Each can be a module used by multiple environments to avoid code duplication.

**Example Module Usage**:
Suppose we wrote modules as `network` and `apigateway`. In each environment folder, our `main.tf` might look like:

```hcl
module "network" {
  source          = "../../modules/network"
  environment     = var.environment
  vpc_id          = var.vpc_id
  # perhaps define services list and ports
  services = [
    { name = "import-service", port = 80 },
    { name = "checkout-service", port = 81 }
  ]
  # This module will create NLB, TGs, listeners, and a VPC Link
}

module "api_gateway" {
  source                 = "../../modules/apigateway"
  environment            = var.environment
  rest_api_name          = "EnsarAPI-${var.environment}"
  resource_paths         = ["import", "importAsync", "importAsyncStatus", "export", "oas3Export", "checkout", "cancelCheckout", "checkin"]
  request_validator_body = true
  request_validator_params = true
  vpc_link_id            = module.network.vpc_link_id
  nlb_dns_name           = module.network.nlb_dns_name
  service_port_map       = {                      # mapping endpoints to NLB ports
    import               = 80,
    importAsync          = 80,
    importAsyncStatus    = 80,
    export               = 80,
    oas3Export           = 80,
    checkout             = 81,
    cancelCheckout       = 81,
    checkin              = 81
  }
  business_units         = var.business_units    # e.g., ["finance","hr"]
  certificate_arn        = var.acm_certificate_arn
  api_version            = "v1"
}
```

In this hypothetical usage:

- `module.network` returns outputs like `vpc_link_id`, `nlb_dns_name`, etc. It encapsulates the network details, so the API module doesn't worry about how NLB is set up, just uses its DNS and VPC Link ID.
- `module.api_gateway` takes the list of paths and a map assigning each path to a port (so it knows how to set the integration URI for each). It creates all API Gateway related resources and also sets up the domains and base path mappings.
- The modules themselves would contain the resources similar to what we wrote earlier, parameterized by variables.

While implementing modules is some effort, it pays off as you scale (e.g., adding a new environment is very easy—just create a new environment tfvars and call the modules, no need to copy-paste the whole code).

Terraform registry also has pre-built modules (for example, for API Gateway or VPC Link), but in advanced scenarios like this with many custom details, writing your own is fine.

## 12. CI/CD Pipeline for Terraform

Managing this Terraform configuration in a CI/CD pipeline ensures consistent and safe deployments across environments. Here are some recommendations:

- **Version Control**: Store your Terraform code in a git repository. Use branches to represent changes that go through environments (for example, a common flow is to have `dev` branch for development environment, `staging` branch for staging, `main` or `prod` branch for production). This way, you can merge changes upward through envs.

- **Workspaces or Separate Pipelines**: You could use Terraform Cloud or Terraform Enterprise with multiple workspaces (one per environment) listening to the respective branch ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=baller_chemist)). For instance, push to dev branch triggers Terraform plan/apply on dev workspace (against dev environment config/state). After testing, merging to staging branch triggers apply on stg, and so on. This approach was noted by community as effective ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=baller_chemist)).

- **Automated Plan and Manual Approval**: For production, it's wise to have a manual approval step. The CI pipeline can run `terraform plan` and output it for review. An engineer can then approve an `apply`. This prevents accidental changes going straight to prod.

- **State Backend Setup**: Ensure the pipeline is configured with the correct backend (we discuss state management in next section). If using AWS S3 for state, the IAM credentials in the pipeline must allow access to the S3 bucket and DynamoDB (for locking).

- **Use of Terraform Cloud**: Terraform Cloud can simplify CI/CD by handling remote runs and state. You can connect it to VCS and it will auto-trigger plans on changes. It also has a nice run UI for approvals.

- **Secrets Management**: Do not hardcode secrets (like AWS credentials) in the pipeline config. Use a secure store (like GitHub Actions secrets, Jenkins credentials store, etc.). For Terraform Cloud, you can set environment variables for AWS access keys or use an assumed role.

- **Linting and Formatting**: Integrate `terraform fmt -check` and `terraform validate` in the pipeline to catch syntax or style issues early. Optionally, use `tflint` or `checkov` for static analysis of Terraform code for best practices and security.

- **Parallelism**: If each environment is a separate pipeline job, they can run in parallel for plan. But you might want sequential promotion (don’t apply to stg until dev is applied and validated). This depends on your release strategy.

**Example Pipeline Steps (Pseudo code)**:

1. **Plan (Dev)**: On push to dev branch:
   - `terraform workspace select dev` (if using workspaces) or change directory to `environments/dev`.
   - `terraform init` (with backend config).
   - `terraform plan -out=tfplan.bin`.
   - Save plan artifact or proceed to apply if auto.
2. **Apply (Dev)**: If plan is approved or auto for dev:
   - `terraform apply tfplan.bin`.
3. After dev deployment, perhaps run tests (e.g., API integration tests).
4. When ready to promote, merge dev branch to stg branch, which triggers the pipeline for staging similarly.

If using separate directories and no workspaces, you can just have pipeline jobs that `cd environments/dev && terraform ...` etc., or maintain separate config in the pipeline for each environment.

The key is consistency: treat infrastructure changes similar to code, promoting through environments.

## 13. Terraform State Management Best Practices

Managing Terraform state is crucial in a team and multi-env setting. Here are best practices relevant to our scenario:

- **Use a Remote Backend**: Do not store `terraform.tfstate` locally or in git. Use a remote backend like AWS S3 (with DynamoDB for locking) or Terraform Cloud/Enterprise. This ensures state is persisted reliably and locked to prevent concurrent modifications.

- **Separate State per Environment**: As mentioned, each environment should have its own state file ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)). This way, changes in dev only affect dev’s state. If using S3 backend, you can use a different key for each env. For example:
  ```hcl
  backend "s3" {
    bucket = "my-tf-state-bucket"
    key    = "ensar-api/dev/terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt = true
  }
  ```
  and similarly "ensar-api/stg/terraform.tfstate" for staging, etc. The DynamoDB table can be common for locks (it uses the key to differentiate locks) ([Backend Type: s3 | Terraform - HashiCorp Developer](https://developer.hashicorp.com/terraform/language/backend/s3#:~:text=Backend%20Type%3A%20s3%20,the%20bucket%20and%20key%20variables)).
- **State Security**: Enable encryption on the S3 bucket (as shown with `encrypt = true`). Also enable bucket versioning to recover from accidental deletions. Limit access to the state bucket using IAM policies—only the CI service or trusted admins should read/write state, because state may contain sensitive info (resource IDs, even secrets if any were output) ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=I%20am%20not%20an%20expert%2C,it%20can%20contain%20sensitive%20data)).

- **State Locking**: With DynamoDB or the backend’s native locking, ensure it's in place so two people don't apply at the same time on the same env. Terraform will wait if it finds a lock (DynamoDB prevents the "lost update" scenario).

- **Terraform State for Shared Resources**: If some infrastructure is shared (like the VPC or a Route53 zone), consider separating those into their own Terraform state. For example, your Route53 zones could be managed in a separate Terraform project that creates the zones and maybe some global records. The API infrastructure then only creates records in those zones (which can be done if you have the zone IDs). Or use data sources to fetch shared resource IDs. This decoupling prevents unintentional changes to shared infra when modifying the API stack.

- **Backups**: Have a process to backup the state (if using S3, versioning is a form of backup). Terraform Cloud automatically versions state. You can also use Terraform’s `state pull` to get a local copy if needed for manual inspection.

- **Team Workflow**: If multiple team members work on infra, using a remote backend ensures everyone uses the same state. Avoid running `terraform apply` from a developer’s machine using an outdated state file. Instead, always pull the latest state (Terraform does on init/refresh if remote).

- **State Access Control**: If using Terraform Cloud, take advantage of workspaces and teams to restrict who can apply to production vs dev. Similarly, with S3, use bucket IAM policies (maybe separate buckets per env with stricter access on prod’s bucket).

By following these practices, you maintain the integrity of your infrastructure state across environments and reduce the risk of mistakes.

## 14. Architecture Diagram and Topology Explanation

_(Since embedding images is not possible here, we'll describe the architecture with text. Advanced readers can visualize or sketch the described topology.)_

Each environment (dev, int, stg, prd) follows the same architecture pattern, with isolated resources:

- **Clients** (could be web apps, services, or developers testing) make HTTPS requests to the **Custom Domain** of API Gateway for that environment (e.g., `finance-api.stg.example.com`).
- The request goes to **API Gateway (EnsarAPI)** which has a stage for the API version (e.g., v1). The custom domain and base path mapping ensure the request is routed to the correct API stage.
- API Gateway first **validates the request** (query params and JSON body) according to the configured validator and models. If the request is malformed or missing required data, API Gateway immediately returns a 400 Bad Request error without invoking downstream.
- If validation passes, API Gateway, via the configured **VPC Link**, forwards the request internally to the **Network Load Balancer** in the VPC.
- The **VPC Link** is essentially a private tunnel: API Gateway calls the NLB’s internal address. The NLB receives the request on a specific listener (port) depending on which endpoint was called (as our integration URIs included the port).
- The **Network Load Balancer (internal)** then uses its listener configuration to pass the request to the corresponding **Target Group** of the microservice. Each target group has one or more instances or containers (like ECS tasks or EC2 instances) in the private subnets handling the business logic for that endpoint.
- The microservice processes the request (e.g., performs an import, or a checkout operation) and returns a response.
- The response travels back through the NLB (which just forwards it), through the VPC Link, to API Gateway. API Gateway then returns the response to the client. Because we used `HTTP_PROXY`, by default the status code and body from the microservice are relayed as-is.
- All this happens securely within AWS – the API Gateway is the only component exposed publicly (and it’s using HTTPS with our custom domain certificate). The NLB and microservices are not directly accessible from the internet.
- We also have CloudWatch logging enabled on API Gateway (and the microservices should also log to CloudWatch or a monitoring system), so operationally we can trace requests or errors.

Here's a simplified view in text form:

```
Client -> HTTPS (api.<env>.example.com) -> [ API Gateway (EnsarAPI - env, Stage v1) ]
             |--> (Request Validation, Routing)
             |--> VPC Link -> [ Internal NLB (cross-zone) ]
                           |--> Listener 80 -> Target Group (Import/Export Service) -> EC2/ECS instances
                           |--> Listener 81 -> Target Group (Checkout Service)    -> EC2/ECS instances
                           `... (additional target groups for other services if applicable)
```

Each environment would have its own instance of the above (with possibly different DNS names and physically separate NLBs, target instances, etc., likely in its own AWS account or at least its own VPC).

Multiple business units: In the above, if multiple BUs share the same environment’s API Gateway, the difference is just the **hostname** used:

- e.g., Finance uses `finance-api.dev.example.com/v1/...` and HR uses `hr-api.dev.example.com/v1/...`. Both point to the same API Gateway (dev EnsarAPI stage v1). The Gateway doesn't inherently know the difference except the domain name, but that could be used for logging or throttling distinctions if needed. We simply set up both domains to map to the same stage. This way, BUs can have segregated URLs, and if needed we could issue separate API keys or usage plans in API Gateway per domain (beyond our scope here).

The internal architecture (NLB and services) could also be separated per BU, but our current design assumes shared services. If BUs had completely separate backends, one might instead deploy separate API Gateways or at least separate NLBs per BU to avoid overlapping. The given requirements imply a unified gateway though, so we went with that.

**Scaling considerations**:

- The NLB can handle a lot of traffic and is automatically scaling. It can route to however many targets. We enabled cross-zone to maximize usage of targets in all AZs.
- API Gateway has its own scaling (it can handle thousands of requests per second), but you might need to request limit increases if expecting very high throughput.
- Each microservice behind can scale via Auto Scaling or ECS Service scaling as needed, independent of API Gateway.
- One VPC Link per env is sufficient even as you add more microservices (just add more listeners & target groups), which simplifies expansion.

## 15. Best Practices Recap

To conclude this guide, let's recap some best practices covered (and a few additional ones) in context:

- **Infrastructure as Code**: Keep all the configuration in Terraform (as we did). This allows reviewing changes and ensures consistency across environments.
- **Least Privilege IAM**: The IAM role we created for API Gateway logging had only the permission it needed (to write CloudWatch Logs) ([Understanding the Terraform Resources that Create an AWS API Gateway REST API – QloudX](https://www.qloudx.com/understanding-the-terraform-resources-that-create-an-aws-api-gateway-rest-api/#:~:text=it%20only%20supports%20one%20argument%3A,role%20to%20allow%20CloudWatch%20access)). Similarly, ensure the AWS credentials used by Terraform have just enough permissions to create these resources (e.g., an IAM policy for Terraform that allows managing API Gateway, NLB, ACM, etc., but not more).
- **Parameterize Everything**: We used variables for environment names, regions, etc., which makes the code flexible. This prevents hard-coded values that would need changing for each environment.
- **Modular Design**: Structure Terraform code with reusability in mind (using modules and separate states for environment isolation) ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)). This also enables team collaboration where one team could manage network module updates while another manages the API module.
- **Validation and Testing**: Use Terraform’s plan output in a pipeline to catch unintended changes. Also, after deployment, test each endpoint in dev to ensure integration is correct (e.g., does `/importAsync` return expected result or at least reach the service?). Automated integration tests for the API can be part of your pipeline.
- **Monitor and Log**: We set up basic logging for API Gateway. Consider adding CloudWatch Alarms on API Gateway metrics (such as 5XX error count, latency) to catch issues. Also monitor NLB target health and microservice logs. X-Ray tracing can be enabled to trace requests through API Gateway and into the services, which is valuable in debugging performance issues.
- **Terraform State Management**: Use remote state with locking to avoid team conflicts. We provided an S3/Dynamo approach which is very common and reliable.
- **Keep Terraform DRY**: Avoid duplication by using loops (for_each) as we did in some examples for BUs and endpoints. This not only reduces code, but ensures consistency. For instance, generating 8 almost-identical methods via a loop means if you need to add one header requirement to all, it's one code change in the loop instead of editing 8 blocks.
- **Tag Resources**: Tags help with ops and cost. We stressed this but it’s worth repeating: implement a tagging policy and use Terraform to enforce it (you can even write policies or use terraform validate to ensure each resource has certain tags).
- **Plan for Version 2**: The setup with base path mapping means if you need to deploy a v2 of the API that maybe has different endpoints or improvements, you can deploy a new stage "v2" using a new deployment (possibly from a new Terraform workspace or by extending this one) and map `/v2` on the domain. This allows both v1 and v2 to run concurrently (perhaps v1 eventually deprecated). Our Terraform can accommodate this by allowing multiple stages or duplicating the setup for a new version. Design your Terraform to either allow adding a `api_version = "v2"` to deploy a new stage or use a separate deployment config for v2.

By following this guide, you can achieve a robust, multi-environment API Gateway deployment that is easier to manage, scalable, and secure. Each environment is reproducible from code, reducing manual errors. The use of multiple stages and custom domains provides clear separation between development/testing and production usage, while still using a consistent architecture.

**References:**

- AWS API Gateway VPC Link with NLB (AWS Docs): one NLB and VPC Link can support multiple services via different listeners ([Set up a Network Load Balancer for API Gateway private integrations - Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-nlb-for-vpclink-using-console.html#:~:text=For%20each%20VPC%20you%20have,API%20with%20a%20private%20integration)).
- Enabling cross-zone load balancing for NLB to improve resilience ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=type%2C%20so%20you%E2%80%99ve%20got%20to,read%20the%20documentation%20carefully)).
- Setting the NLB as internal-only for use with VPC endpoints or private integrations ([Provisioning a Network Load Balancer with Terraform | Mario Fernandez](https://hceris.com/provisioning-a-network-load-balancer-with-terraform/#:~:text=A%20load%20balancer%20doesn%E2%80%99t%20always,live%20in%20a%20private%20subnet)).
- Terraform API Gateway request validator example (enforcing body and params) ([AWS API Gateway Request Validator - Examples and best practices | Shisho Dojo](https://shisho.dev/dojo/providers/aws/API_Gateway/aws-api-gateway-request-validator/#:~:text=resource%20,true%20validate_request_parameters%20%3D%20true)).
- VPC Link integration: use NLB DNS name in integration URI and set type to HTTP_PROXY ([amazon web services - API Gateway integration to an elastic beanstalk app with a VPC_LINK fails with AWS ARN for integration must contain path or action - Stack Overflow](https://stackoverflow.com/questions/76412105/api-gateway-integration-to-an-elastic-beanstalk-app-with-a-vpc-link-fails-with-a#:~:text=As%20per%20the%20CloudFormation%20documentation%2C,argument)) ([amazon web services - API Gateway integration to an elastic beanstalk app with a VPC_LINK fails with AWS ARN for integration must contain path or action - Stack Overflow](https://stackoverflow.com/questions/76412105/api-gateway-integration-to-an-elastic-beanstalk-app-with-a-vpc-link-fails-with-a#:~:text=EDIT%3A%20As%20per%20the%20comments%2C,HTTP_PROXY)).
- API Gateway custom domain and base path mapping: domain resource defines domain, base path mapping connects it to stage ([Understanding the Terraform Resources that Create an AWS API Gateway REST API – QloudX](https://www.qloudx.com/understanding-the-terraform-resources-that-create-an-aws-api-gateway-rest-api/#:~:text=The%20next%20two%20resources%20together,custom%20domain%20for%20your%20API)) ([Understanding the Terraform Resources that Create an AWS API Gateway REST API – QloudX](https://www.qloudx.com/understanding-the-terraform-resources-that-create-an-aws-api-gateway-rest-api/#:~:text=%2A%20%60aws_api_gateway_base_path_mapping%60%20maps%20a%20sub,a%20stage%20of%20your%20API)).
- State management: separate state files per environment and secure the state storage (encryption, least access) ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)).
- Terraform code organization: use separate modules per component and separate state per env (avoid code duplication) ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=%E2%80%A2)) ([Simplifying Terraform Multiple Environments: A Step-by-Step Approach | Zeet.co](https://zeet.co/blog/terraform-multiple-environments#:~:text=When%20using%20separate%20directories%20for,its%20variables%20and%20provider%20configurations)).
- CI/CD workflow: use VCS branches and Terraform workspaces per environment for smooth promotion of infra changes ([Best Practices for S3 Remote State and DynamoDB : r/Terraform](https://www.reddit.com/r/Terraform/comments/mdzbdh/best_practices_for_s3_remote_state_and_dynamodb/#:~:text=baller_chemist)).
- Tagging strategy: consistent tagging helps in resource management and cost tracking ([Best Practices for Tagging AWS Resources - Best Practices for Tagging AWS Resources](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html#:~:text=on%20that%20resource,and%20manage%20your%20AWS%20environment)).
