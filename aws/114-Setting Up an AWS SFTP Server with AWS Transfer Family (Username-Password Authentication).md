# Setting Up an AWS SFTP Server with AWS Transfer Family (Username-Password Authentication)

This guide provides a **step-by-step walkthrough** for experienced developers to set up a Secure File Transfer Protocol (SFTP) server on AWS using **AWS Transfer Family** with **username-password authentication**. We will cover the infrastructure as code setup with **Terraform**, building a **Spring Boot REST API** for file transfers, important **security considerations**, and how to **deploy and test** the solution.

**Overview:** AWS Transfer Family SFTP is a fully managed service that uses Amazon S3 as the underlying storage for file transfers ([Setup SFTP on AWS with Username and Password in 15 minutes | CodeRise Technologies - Your Cloud Partner for Digital Success](https://coderise.io/sftp-on-aws-with-username-and-password/#:~:text=In%20this%20blog%2C%20we%20will,reliable%2C%20scalable%20and%20durable%20solution)). By default, AWS Transfer SFTP uses SSH key authentication, but we will enable **password-based authentication** by integrating AWS Secrets Manager as a custom identity provider ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=AWS%20Transfer%20Family%20provides%20a,provider%20setup%20via%20API%20Gateway)). Terraform will provision the Transfer Family server, S3 bucket, IAM roles, and related resources. On the application side, a Spring Boot API will allow uploading and downloading files (stored in S3 via the SFTP server), secured with Spring Security. We will also implement best practices for securing credentials and monitoring the system via CloudWatch.

Let's dive into the detailed steps:

## 1. Terraform Setup for AWS Transfer Family SFTP

In this section, we use Terraform to define all necessary AWS resources for the SFTP server. This includes creating the Transfer Family server, an S3 bucket for storage, IAM roles and policies for access and logging, and the custom authentication setup to allow username/password logins. We assume you have Terraform installed and AWS credentials configured.

### 1.1 Creating the S3 Bucket and IAM Roles

**Step 1: Create an S3 bucket** that will serve as the backend storage for the SFTP server. All files uploaded via SFTP will be stored in this bucket. Make sure to keep the bucket private (no public access) and enable default encryption if required (for example, using an AWS KMS key). In Terraform, you can define the bucket as follows:

```hcl
resource "aws_s3_bucket" "sftp_bucket" {
  bucket = "my-sftp-bucket-name"
  acl    = "private"
  tags = {
    Name = "SFTPBucket"
  }
}
```

Optionally, configure a bucket policy or Block Public Access settings to ensure the data is not publicly accessible. Also consider enabling versioning if you need to keep historical versions of files.

**Step 2: Define an IAM role for S3 access** that the SFTP server will assume on behalf of SFTP users. This role will limit what the SFTP users can do in the S3 bucket. For example, the role might allow listing the bucket and full access to a specific folder (prefix) within the bucket. The role’s trust policy must trust the Transfer Family service principal (`transfer.amazonaws.com`) so that the service can assume the role ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=statement%20)). The permissions policy should allow necessary S3 actions (e.g., ListBucket on the bucket, GetObject/PutObject on relevant key prefixes). For example, in Terraform:

```hcl
# Trust policy allowing AWS Transfer to assume this role
data "aws_iam_policy_document" "transfer_s3_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["transfer.amazonaws.com"]
    }
    effect = "Allow"
  }
}

resource "aws_iam_role" "sftp_s3_access_role" {
  name               = "TransferS3AccessRole"
  assume_role_policy = data.aws_iam_policy_document.transfer_s3_trust.json
}

# Permissions policy for S3 access (restrict to the bucket/prefix)
data "aws_iam_policy_document" "sftp_s3_permissions" {
  statement {
    sid     = "ListBucket"
    actions = ["s3:ListBucket", "s3:GetBucketLocation"]
    resources = ["arn:aws:s3:::${aws_s3_bucket.sftp_bucket.id}"]
  }
  statement {
    sid     = "UserAccess"
    actions = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:GetObjectVersion"]
    resources = ["arn:aws:s3:::${aws_s3_bucket.sftp_bucket.id}/*"]  # allow these actions in the bucket's objects
  }
}

resource "aws_iam_policy" "sftp_s3_policy" {
  name   = "Transfer-S3-Access-Policy"
  policy = data.aws_iam_policy_document.sftp_s3_permissions.json
}

resource "aws_iam_role_policy_attachment" "sftp_s3_policy_attach" {
  role       = aws_iam_role.sftp_s3_access_role.name
  policy_arn = aws_iam_policy.sftp_s3_policy.arn
}
```

In the above, we create `sftp_s3_access_role` and attach a policy allowing list access to the bucket and read/write/delete access to objects under that bucket ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=actions%20%3D%20)) ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=resources%20%3D%20%5B)). You can tailor the resource ARNs if you want to restrict to specific folder paths (prefixes) within the bucket (using session policies or IAM conditions). For example, ensure the policy uses the proper path with a slash (`arn:aws:s3:::my-bucket/myfolder/*`) to avoid unintended access ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Use%20slashes%20in%20session%20policies,to%20limit%20access)) ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=session%20policy%20is%20missing%20a,makes%20it)).

**Step 3: Define an IAM role for CloudWatch logging (optional but recommended).** AWS Transfer Family can push SFTP user activity logs to Amazon CloudWatch if a logging role is configured. Create a role with trust policy for `transfer.amazonaws.com` (same as above) and attach a policy that allows CloudWatch Logs operations. For instance, the policy should allow actions like `logs:CreateLogGroup`, `logs:CreateLogStream`, and `logs:PutLogEvents` on the log group for your Transfer server ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=actions%20%3D%20)) ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=)). Example:

```hcl
resource "aws_iam_role" "sftp_logging_role" {
  name               = "TransferLoggingRole"
  assume_role_policy = data.aws_iam_policy_document.transfer_s3_trust.json  # reusing trust doc with transfer.amazonaws.com
}

resource "aws_iam_policy" "sftp_cloudwatch_policy" {
  name   = "Transfer-CloudWatch-Logs-Policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "logs:CreateLogGroup", "logs:CreateLogStream",
        "logs:DescribeLogStreams", "logs:PutLogEvents"
      ],
      Resource = "arn:aws:logs:*:*:log-group:/aws/transfer/*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "sftp_logs_policy_attach" {
  role       = aws_iam_role.sftp_logging_role.name
  policy_arn = aws_iam_policy.sftp_cloudwatch_policy.arn
}
```

This ensures the Transfer server can create log streams and write logs to CloudWatch under `/aws/transfer/...`. Later, we'll configure the Transfer server to use this logging role.

### 1.2 Defining the AWS Transfer Family Server with Username-Password Auth

**Step 4: Define the AWS Transfer Family SFTP server** in Terraform. This is the core resource that represents the SFTP service. We will specify that it uses **custom authentication** via API Gateway (to enable password logins), and that it uses the S3 bucket as its storage. Key settings include:

- `identity_provider_type = "API_GATEWAY"` – This tells AWS that we will provide an API Gateway endpoint for authentication of users.
- `url` – The invoke URL of the API Gateway that will handle user authentication.
- `invocation_role` – An IAM role that the Transfer service will assume to invoke our API.
- `logging_role` – The IAM role for CloudWatch logging (from step 3).
- `protocols = ["SFTP"]` – Protocols to enable (SFTP in our case; you could also include FTPS/FTP if needed).
- `endpoint_type` – Choose `"PUBLIC"` for an internet-facing endpoint or `"VPC"` for a VPC-hosted endpoint. In this guide, we assume a public endpoint for simplicity (so external SFTP clients can connect), but you can use VPC for internal networks and attach a Security Group for fine-grained access control.

First, **create the invocation role** for the custom identity provider. This role allows the Transfer server to call the API Gateway. Its trust policy is again `transfer.amazonaws.com`. The permissions policy must allow invoking our specific API Gateway endpoint. For example, if our API Gateway REST API has an ID `abcdef1234` and we use an endpoint resource path like `/servers/{serverId}/users/{username}/config` (as per the AWS example), we grant `execute-api:Invoke` on the appropriate ARN. In Terraform, after defining the API (in Step 5), you might do:

```hcl
# Invocation role for Transfer to call API Gateway
resource "aws_iam_role" "sftp_invocation_role" {
  name               = "TransferInvokeAPIRole"
  assume_role_policy = data.aws_iam_policy_document.transfer_s3_trust.json
}

# Policy to allow invoking the API Gateway endpoint
data "aws_iam_policy_document" "sftp_invoke_api_policy_doc" {
  statement {
    actions   = ["execute-api:Invoke"]
    resources = ["arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.sftp_auth_api.id}/*/GET/*"]
    effect    = "Allow"
  }
}
resource "aws_iam_policy" "sftp_invoke_api_policy" {
  name   = "Transfer-Invoke-API-Policy"
  policy = data.aws_iam_policy_document.sftp_invoke_api_policy_doc.json
}
resource "aws_iam_role_policy_attachment" "sftp_invoke_api_attach" {
  role       = aws_iam_role.sftp_invocation_role.name
  policy_arn = aws_iam_policy.sftp_invoke_api_policy.arn
}
```

In the above, we allow the `Invoke` action on any resource (`GET` method) of our API Gateway REST API ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=statement%20)). (Adjust the resource ARN to match your API's ID and stage). We also include any needed `apigateway:GET` permissions if required to query the API (some setups include that, as seen in examples). Now we have the IAM role ARN for invocation.

Next, define the **Transfer Family server resource**:

```hcl
resource "aws_transfer_server" "sftp_server" {
  identity_provider_type = "API_GATEWAY"
  invocation_role        = aws_iam_role.sftp_invocation_role.arn
  url                    = aws_api_gateway_deployment.sftp_auth_deployment.invoke_url   # full invoke URL of API (e.g., https://<api-id>.execute-api.<region>.amazonaws.com/<stage>)
  logging_role           = aws_iam_role.sftp_logging_role.arn  # CloudWatch logs role
  protocols              = ["SFTP"]
  endpoint_type          = "PUBLIC"  # or "VPC" if internal
  # endpoint_details if endpoint_type is VPC (subnet_ids, VPC ID, etc.), plus an Elastic IP for internet access if needed.
  tags = {
    Name = "MySFTPServer"
  }
}
```

When Terraform applies this, it will create an AWS Transfer Family server. **Important:** Take note of the **Server ID** output (the resource ID starting with `s-...`). We will need this for setting up user credentials in Secrets Manager. You can output it in Terraform or find it in AWS console. If using a VPC endpoint, also configure a Security Group to allow SFTP (port 22) access from your clients' IP ranges.

At this point, we have an SFTP server that knows it should consult an API Gateway to authenticate users. However, we haven't created that API Gateway or the backing Lambda function yet. That's next.

### 1.3 Implementing the Custom Identity Provider (API Gateway + Lambda)

To enable **username-password authentication**, we integrate AWS Secrets Manager (for storing user creds) with AWS Transfer via a **Lambda function** exposed through **API Gateway**. When a user attempts to log in, the Transfer service will call the API Gateway endpoint (using the invocation role) with the username and password. The Lambda will validate the credentials against Secrets Manager and return an authentication decision along with the IAM role to use for that user.

**Step 5: Create an AWS Secrets Manager secret for each SFTP user.** Each user will have a secret in the format `aws/transfer/<ServerID>/<Username>`, as required by AWS Transfer’s custom identity provider ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=4,id%2Fusername)). The secret should contain at least the keys **`Password`** and **`Role`**, and optionally home directory or SSH keys. For example, you might create a secret named `aws/transfer/s-1234567890abcdef/user1` with the following key-value pairs:

- **Password:** `User1S3cur3Pass!` (the user's password in plaintext or optionally encrypted by Secrets Manager; Transfer will retrieve it)
- **Role:** `arn:aws:iam::123456789012:role/TransferS3AccessRole` (the ARN of the IAM role created in Step 2, or a specific role for this user)

Optionally, you can add:

- **HomeDirectory:** `/my-sftp-bucket/home/user1` to specify a fixed home directory (prefix in S3) for this user, or use **HomeDirectoryDetails** for logical directory mappings.
- **PublicKey:** an SSH public key if you want to allow key-based auth in addition to password for this user.
- **Policy/ScopeDownPolicy:** session policy JSON to further restrict this user's access (not in the Secrets Manager secret by default, but can be returned by Lambda if needed).
- **AcceptedIpNetwork:** e.g. `203.0.113.0/24` to restrict login to a specific IP range (the Lambda can enforce this).

In Terraform, you could create these secrets using `aws_secretsmanager_secret` and `aws_secretsmanager_secret_version` resources. For example (for one user):

```hcl
resource "aws_secretsmanager_secret" "sftp_user1" {
  name = "aws/transfer/${aws_transfer_server.sftp_server.id}/user1"
}

resource "aws_secretsmanager_secret_version" "sftp_user1_version" {
  secret_id = aws_secretsmanager_secret.sftp_user1.id
  secret_string = jsonencode({
    Password = "User1S3cur3Pass!",
    Role     = aws_iam_role.sftp_s3_access_role.arn
  })
}
```

**Step 6: Create the Lambda function** that will act as the custom authentication logic. AWS provides [sample code and CloudFormation templates](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/) for this. The Lambda's responsibility:

- Parse the incoming request from API Gateway (which will include username, password, server ID, protocol, etc. as parameters).
- Fetch the secret `aws/transfer/serverId/username` from Secrets Manager.
- Compare the provided password with the stored password. For SFTP logins, use the `Password` field; for FTP, use `FTPPassword` if present ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=The%20Lambda%20function%20implements%20this,logic)).
- If the password matches, return a JSON response with status and the user's role and optionally home directory. If it fails, return an error to indicate authentication failure.
- If an SSH key auth is attempted (no password provided), the Lambda can return the stored public keys for that user (so Transfer can validate the SSH key).

The Lambda can be written in Python, Node.js, etc. The AWS blog's sample uses Python. You can deploy the Lambda via Terraform as well:

```hcl
resource "aws_lambda_function" "sftp_custom_auth" {
  function_name = "TransferCustomAuthFunction"
  role          = aws_iam_role.sftp_lambda_role.arn  # define this role with Secrets Manager read access and basic Lambda execution
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = "${path.module}/function.zip"      # assume you've packaged the code
  timeout       = 10
}
```

The Lambda’s IAM role (not shown above) needs permission to read Secrets Manager secrets (`secretsmanager:GetSecretValue` for the relevant secret ARN prefix) and to write CloudWatch logs. We created a snippet of that role earlier (with AWSLambdaBasicExecutionRole and a custom policy for Secrets Manager access) ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=Allow%20Lambda%20to%20upload%20logs,to%20CloudWatch)) ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=resource%20)).

**Step 7: Set up API Gateway** to trigger the Lambda. We create a REST API with a resource path matching Transfer Family’s expected format: `/servers/{serverId}/users/{user}/config`. The method (GET) will integrate with Lambda. API Gateway will pass through query parameters and headers to Lambda as needed. Key integration points:

- **Method:** GET (as required by Transfer).
- **Path:** `/servers/{serverId}/users/{username}/config`.
- **Mapping Template:** Map the incoming request to Lambda input, including the username, serverId, protocol, source IP, and password. According to AWS, Transfer will call the API with query strings `username`, `serverId`, `protocol`, `sourceIp` and an HTTP Authorization header carrying the password (or a custom header). In the AWS sample, they pass the password via a header and map it to Lambda input ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=%2Fservers%2FserverId%2Fusers%2Fusername%2Fconfig)).
- **Lambda Integration:** Lambda Proxy integration can be used, or a custom integration with a mapping template. The AWS sample uses a custom integration and mapping template to supply the parameters.

Using Terraform, you can define the REST API, resource, method, integration, and deployment. For brevity, here's a high-level outline (pseudocode style):

```hcl
resource "aws_api_gateway_rest_api" "sftp_auth_api" {
  name = "SFTPAuthAPI"
}

resource "aws_api_gateway_resource" "sftp_auth_resource" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  parent_id   = aws_api_gateway_rest_api.sftp_auth_api.root_resource_id
  path_part   = "servers"
}

# Child resource for serverId
resource "aws_api_gateway_resource" "sftp_auth_server" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  parent_id   = aws_api_gateway_resource.sftp_auth_resource.id
  path_part   = "{serverId}"
}
# Child resource for users
resource "aws_api_gateway_resource" "sftp_auth_users" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  parent_id   = aws_api_gateway_resource.sftp_auth_server.id
  path_part   = "users"
}
# Child resource for username config
resource "aws_api_gateway_resource" "sftp_auth_user_config" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  parent_id   = aws_api_gateway_resource.sftp_auth_users.id
  path_part   = "{username}"
}

# Finally, the config resource path
resource "aws_api_gateway_resource" "sftp_auth_config" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  parent_id   = aws_api_gateway_resource.sftp_auth_user_config.id
  path_part   = "config"
}

# Method and integration on /servers/{serverId}/users/{username}/config
resource "aws_api_gateway_method" "sftp_auth_method" {
  rest_api_id   = aws_api_gateway_rest_api.sftp_auth_api.id
  resource_id   = aws_api_gateway_resource.sftp_auth_config.id
  http_method   = "GET"
  authorization = "NONE"
  request_parameters = {  # pass through params
    "method.request.querystring.username" = true,
    "method.request.querystring.serverId" = true,
    "method.request.querystring.protocol" = true,
    "method.request.querystring.sourceIp" = true
  }
  request_models = {}  # no body model
}

resource "aws_api_gateway_integration" "sftp_auth_integration" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  resource_id = aws_api_gateway_resource.sftp_auth_config.id
  http_method = aws_api_gateway_method.sftp_auth_method.http_method
  type        = "AWS_PROXY"  # using Lambda Proxy integration for simplicity
  integration_http_method = "POST"
  uri         = aws_lambda_function.sftp_custom_auth.invoke_arn
}
# (If not using proxy integration, you'd specify mapping templates here instead)

# Give API Gateway permission to invoke Lambda
resource "aws_lambda_permission" "allow_apigw_invoke" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sftp_custom_auth.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.sftp_auth_api.execution_arn}/*"
}

# Deploy the API
resource "aws_api_gateway_deployment" "sftp_auth_deployment" {
  rest_api_id = aws_api_gateway_rest_api.sftp_auth_api.id
  stage_name  = "prod"
  depends_on  = [aws_api_gateway_integration.sftp_auth_integration]
}
```

After deploying, you'll have an invoke URL like `https://<api-id>.execute-api.<region>.amazonaws.com/prod/servers/{serverId}/users/{username}/config`. This is the URL you provided in the `aws_transfer_server` resource. Now the pieces connect: when an SFTP client tries to authenticate, Transfer Family will call this API, Lambda will verify the password against Secrets Manager, and if successful, the Transfer service will allow login and restrict the user to the S3 bucket with the IAM role returned.

**Note:** The AWS blog provides a ready-to-use AWS CloudFormation/SAM template that creates the API Gateway and Lambda (which we essentially recreated in Terraform) ([Setup SFTP on AWS with Username and Password in 15 minutes | CodeRise Technologies - Your Cloud Partner for Digital Success](https://coderise.io/sftp-on-aws-with-username-and-password/#:~:text=Step,functions%20and%20required%20IAM%20roles)). You can refer to that for more detail or use it as a reference implementation. The secrets in Secrets Manager are the source of truth for user credentials ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=4,id%2Fusername)), and using Secrets Manager ensures the passwords are stored securely (encrypted at rest and not hard-coded in code).

### 1.4 Configuring Networking and Security Groups

Depending on the `endpoint_type` of your Transfer server, networking will differ:

- **Public Endpoint:** AWS manages the internet-facing endpoint for SFTP. No VPC required. You cannot directly attach a Security Group to a public endpoint; instead, use AWS Transfer's built-in controls like allowed IP lists (you can enforce client IP restrictions via the custom Lambda using the `AcceptedIpNetwork` parameter ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=Key%20%E2%80%93%20AcceptedIpNetwork%20Example%20Value,IP%20address%20for%20the%20client))). Ensure your SFTP clients connect to the server endpoint (which will be `<server-id>.server.transfer.<region>.amazonaws.com` by default) on port 22.

- **VPC Endpoint:** If you chose `endpoint_type = "VPC"`, the server will reside in your VPC. You must specify `endpoint_details` with at least one subnet. AWS will create an elastic network interface in that subnet. You should also allocate an Elastic IP and attach it (so external users can reach it) as shown in the example Terraform snippet ([terraform-aws-sftp-server/transfer-family.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/transfer-family.tf#:~:text=endpoint_details%20)) ([terraform-aws-sftp-server/transfer-family.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/transfer-family.tf#:~:text=protocols%20%3D%20%5B)). You can then attach a **Security Group** to control access. For instance, allow inbound TCP 22 from your office IP range or partners' IPs, etc., and perhaps restrict outbound as needed (though outbound to S3 and Secrets Manager must be allowed). This approach gives you more control over network access, at the cost of managing VPC resources.

Regardless of endpoint type, consider using AWS WAF on the API Gateway endpoint (if using custom auth) to only allow traffic from AWS Transfer and perhaps your admin sources ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Amazon%20API%20Gateway,instance%20to%20allow%20access%20for)). According to AWS, you can configure WAF rules to allow only AWS Transfer's CIDR ranges or specific IPs to reach the API, enhancing security for the password-check endpoint.

Finally, double-check that all IAM roles have least privilege and that sensitive values (like user passwords) are **never exposed in plaintext** in logs or outputs. With the Terraform setup complete, you can proceed to deploy it (we will cover deployment in section 4). Next, let's develop the Spring Boot API that will interface with this SFTP/S3 backend.

## 2. Spring Boot API Development for File Uploads/Downloads

In this section, we create a Spring Boot application that provides RESTful endpoints to upload and download files from the SFTP server's storage (the S3 bucket). This API will serve as an alternative interface to the files for applications that prefer HTTPS/REST over SFTP. We will use the AWS SDK for Java to interact with AWS services (in particular, Amazon S3) and implement secure authentication for the API itself.

### 2.1 Project Setup and Dependencies

**Step 1: Initialize a Spring Boot project** (using start.spring.io or your build tool) with the following dependencies:

- **Spring Web** (for building REST controllers).
- **Spring Security** (for securing the API endpoints).
- **AWS SDK for Java** (specifically the S3 component). You can use AWS SDK v1 or v2; here we'll assume v1 (which includes the `AmazonS3` client), but v2 (with the S3AsyncClient or S3Client) is also an option.
- (Optional) Spring Boot Actuator for monitoring, Lombok for boilerplate reduction, etc.

Add the AWS SDK dependency. For example, in Maven:

```xml
<dependency>
  <groupId>com.amazonaws</groupId>
  <artifactId>aws-java-sdk-s3</artifactId>
  <version>1.12.600</version> <!-- use latest version -->
</dependency>
```

For AWS SDK v2, the dependency is `software.amazon.awssdk:s3`.

Also configure your AWS credentials for the application. In development, you might use environment variables or the default credential chain. In production, you might use an IAM role if deployed on AWS (e.g., EC2 or ECS). Make sure the credentials used by the app have permissions to access the S3 bucket (at least the same as SFTP users, or broader if needed). One approach is to give the Spring Boot app its own IAM user or role with full access to the S3 bucket.

### 2.2 Implementing File Upload and Download Endpoints

**Step 2: Create a service to interact with S3.** For example, an `S3FileService` that wraps the AWS SDK calls. You can configure an `AmazonS3` bean using Spring (with access key, secret, region). For instance:

```java
@Configuration
public class AwsConfig {
    @Value("${aws.accessKey}") String accessKey;
    @Value("${aws.secretKey}") String secretKey;
    @Value("${aws.region}")    String region;

    @Bean
    public AmazonS3 amazonS3() {
        // Use DefaultAWSCredentialsProviderChain or static creds
        BasicAWSCredentials creds = new BasicAWSCredentials(accessKey, secretKey);
        return AmazonS3ClientBuilder.standard()
                    .withRegion(region)
                    .withCredentials(new AWSStaticCredentialsProvider(creds))
                    .build();
    }
}
```

Alternatively, if running on AWS with an instance profile, the SDK will pick up credentials automatically (you can omit explicit keys).

Now, create a service for file operations:

```java
@Service
public class S3FileService {
    @Autowired
    private AmazonS3 amazonS3;
    @Value("${aws.s3.bucketName}")
    private String bucketName;

    public void uploadFile(String key, InputStream fileStream) {
        // Upload file to S3 under the given key
        amazonS3.putObject(bucketName, key, fileStream, new ObjectMetadata());
    }

    public S3Object downloadFile(String key) {
        // Retrieve file from S3
        return amazonS3.getObject(bucketName, key);
    }
}
```

The `uploadFile` method above uses `amazonS3.putObject` with an `InputStream` (and an empty metadata for simplicity). This effectively streams the file into S3. The AWS Java SDK handles the low-level details. (In AWS SDK v2, you would use `s3Client.putObject(PutObjectRequest, RequestBody)` similarly.) ([A Guide to Upload Files to Amazon S3 Bucket Using Spring Boot](https://www.cloudthat.com/resources/blog/a-guide-to-upload-files-to-amazon-s3-bucket-using-spring-boot#:~:text=%40Service%20public%20class%20S3FileUploadService%20,))

**Step 3: Create REST controller endpoints** for upload and download. For example:

```java
@RestController
@RequestMapping("/files")
public class FileTransferController {

    @Autowired
    private S3FileService fileService;

    // Upload endpoint
    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        String filename = file.getOriginalFilename();
        try (InputStream in = file.getInputStream()) {
            fileService.uploadFile(filename, in);
            return ResponseEntity.ok("File uploaded: " + filename);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                 .body("Error uploading file");
        }
    }

    // Download endpoint
    @GetMapping("/download/{filename}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String filename) {
        try {
            S3Object s3Object = fileService.downloadFile(filename);
            S3ObjectInputStream s3is = s3Object.getObjectContent();
            byte[] content = s3is.readAllBytes();
            s3is.close();
            // Return file as Resource
            ByteArrayResource resource = new ByteArrayResource(content);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
                    .contentLength(content.length)
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .body(resource);
        } catch (AmazonServiceException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
}
```

In the upload endpoint, we accept a multipart file upload and stream it directly to S3 via our service. In the download endpoint, we stream the S3 object content back to the client. We set `Content-Disposition` so the browser can download it as a file. For large files, you might want to stream directly to the HTTP response rather than load into memory; for brevity, we used `readAllBytes()` here.

**Note:** The key used in S3 is the filename in this example, but in a real scenario you might include user-specific prefixes or a directory structure. You should ensure that the Spring Boot application writes to the same S3 bucket (and prefix) that the SFTP server is configured to use (e.g., the user’s home directory). Since our S3 IAM role for SFTP already limits users to certain prefixes, our API (running with its own creds) could potentially bypass that. Keep security in mind (more on that in Security Considerations).

### 2.3 Securing the API Endpoints

**Step 4: Implement authentication/authorization for the REST API.** You don't want anyone on the internet to hit your file upload/download API without authorization, since that could expose or allow modification of sensitive files. There are multiple ways to secure a Spring Boot API:

- Use Spring Security with an in-memory or database-backed user store (simple for demonstration).
- Use JWTs (JSON Web Tokens) issued by an auth server (good for stateless auth in production).
- Use AWS Cognito or another OAuth2 identity provider for integration.
- Use simple HTTP Basic Auth over HTTPS for internal or testing purposes.

For simplicity, we'll illustrate using Spring Security with HTTP Basic authentication (username/password for API access), which is easy to set up. In a production scenario, you'd likely use a more robust method (like OAuth2/JWT or API keys ([Using Spring Boot for OAuth2 and JWT REST Protection - Toptal](https://www.toptal.com/spring/spring-boot-oauth2-jwt-rest-protection#:~:text=Using%20Spring%20Boot%20for%20OAuth2,every%20language%20and%20on))).

Add a security configuration class, e.g.:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        // Define a user for demonstration. In real usage, use PasswordEncoder and external storage.
        auth.inMemoryAuthentication()
            .withUser("apiuser").password("{noop}apipassword") // {noop} means no password encoding
            .roles("USER");
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()  // disable CSRF for simplicity
            .authorizeRequests()
            .antMatchers("/files/**").authenticated()  // require auth on our endpoints
            .and()
            .httpBasic();  // use Basic auth
    }
}
```

This configuration requires that any request to `/files/*` must be authenticated with valid credentials (in this case, a single hardcoded user). The credentials (`apiuser/apipassword`) would be provided by the client via the `Authorization: Basic ...` header (over HTTPS). In practice, you would store users in a database or integrate with an existing user directory. You could also choose to secure with tokens: for example, have a login endpoint that issues a JWT which clients must present on subsequent calls. The specifics depend on your needs.

With Spring Security in place, the API now requires a valid login, preventing unauthorized access. Make sure to configure SSL (HTTPS) in production to protect credentials in transit if not already handled by a reverse proxy or load balancer.

### 2.4 Using AWS SDK for Java to Interact with SFTP (S3)

We have essentially used the AWS SDK for Java (Amazon S3 client) to perform file operations. There's no direct AWS SDK method to push files via SFTP protocol; instead, we interact with the underlying storage (S3) directly in our Java code. This is efficient and avoids the overhead of the SFTP protocol for API use cases.

However, for completeness:

- If you needed to programmatically interact with the SFTP server over SFTP (not just S3), you could use a third-party SFTP client library in Java (like **JSch** or **Apache Mina SSHD**) and point it to the server endpoint. You would use the SFTP user credentials (username and password or key) to log in. This might be useful for integration tests or if some part of your system specifically requires SFTP connections.
- The AWS SDK **does** allow managing the Transfer Family server itself (e.g., creating users when using service-managed identity, or starting/stopping the server), but for file transfers, the AWS Transfer Family simply acts as a bridge to S3.

In our case, the combination of AWS Transfer Family + S3 + Spring Boot API covers both traditional SFTP clients and modern RESTful access.

## 3. Security Considerations

Security is paramount when building an SFTP service and exposing file transfer APIs. This section outlines best practices and considerations to keep the system secure:

**3.1 Securing the SFTP Server (AWS Transfer Family):**

- **Use the latest security policies:** AWS Transfer Family allows specifying a security policy (cipher suite, protocols). Use the most restrictive policy that still meets your client compatibility needs, to protect against known vulnerabilities ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=discovered%20vulnerabilities)) ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=to%20worry%20about%20the%20Terrapin,to%20the%20latest%20security%20policy)). Regularly review AWS announcements for updates to security policies.

- **Endpoint access:** If possible, deploy the SFTP server as a VPC endpoint and limit access with security groups. Only allow trusted IP ranges to connect on port 22. If using a public endpoint, consider AWS Global Accelerator or restrict access via the client-side address check. Our solution can enforce an **IP allowlist per user** using the `AcceptedIpNetwork` in Secrets Manager and logic in the auth Lambda (e.g., compare the incoming `sourceIp` parameter and reject if not allowed).

- **WAF for API Gateway:** As mentioned, when using a custom identity provider via API Gateway, protect that endpoint. You can attach AWS WAF to the API Gateway to allow only specific IPs or CIDR ranges. AWS recommends allowing only AWS Transfer's IP addresses (since technically the calls to the auth API come from the Transfer service, not from end-users directly) and perhaps your administrative IPs ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Amazon%20API%20Gateway,instance%20to%20allow%20access%20for)). This prevents attackers from trying to brute-force passwords via the API Gateway endpoint.

- **Secrets Manager encryption and rotation:** Store user passwords in AWS Secrets Manager which encrypts them at rest. Control access to these secrets strictly (only the Lambda's role should be able to read them). Enable automatic rotation if appropriate – you could rotate passwords periodically by generating new ones and updating the Secret (though note that if you rotate, you must inform the user of the new password out-of-band). Rotation could be implemented with a Lambda rotation function. Since AWS Transfer doesn't natively know about password changes until the next login attempt (it reads from Secrets Manager in real-time), rotation is feasible without downtime.

- **Audit and logging:** Enable CloudTrail for AWS Transfer Family and Secrets Manager. This will log actions like when the Transfer server was created, when users authenticate (the custom auth invocation might show up as Lambda invocation logs), and when secrets were accessed. CloudTrail can help detect any unexpected access.

**3.2 Managing User Credentials Securely:**

- **Never store plaintext passwords** in code or version control. In our Terraform, we used a plain string for the secret for demonstration. In practice, use Terraform variables or pipeline integration to inject secrets (or create the Secrets Manager entry manually and reference it). Ensure the Secrets Manager secret is encrypted with a KMS CMK if you have strict requirements (Secrets Manager uses a default AWS managed key by default).

- **Limit Secrets Manager access:** The Lambda role has `secretsmanager:GetSecretValue` for the specific path (e.g., `arn:aws:secretsmanager:region:account:secret:aws/transfer/serverid/*`) ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=)). Do not wildcard to all secrets in your account. This limits the blast radius if the Lambda role is somehow compromised.

- **IAM least privilege:** The IAM roles we created (S3 access role, logging role, invocation role, Lambda role) should have only the needed permissions. For example, the S3 access role’s policy restricts access to one bucket (and even specific prefixes) ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Use%20slashes%20in%20session%20policies,to%20limit%20access)). The invocation role only allows invoking a specific API, not any API Gateway in the account ([terraform-aws-sftp-server/iam.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/iam.tf#:~:text=statement%20)). This principle of least privilege reduces risk.

- **User isolation:** AWS Transfer, when using IAM roles for each user, provides a strong isolation between users by using different role credentials for S3 access. Even if two SFTP users know each other’s usernames, they cannot access each other’s files unless they somehow obtain the other’s password (which is why strong passwords and possibly 2FA on SFTP (by requiring key + password) is beneficial). If a stricter isolation is needed, ensure each user’s IAM role policy is scoped to their own folder and consider adding a session policy when the role is assumed to double-enforce the path (the blog “Six tips” describes using session policies with HomeDirectory to ensure no escaping the home directory ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Use%20slashes%20in%20session%20policies,to%20limit%20access)) ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=%60arn%3Aaws%3As3%3A%3A%3A%24DailyReports%2F,DailyReports))).

- **Password policy:** Enforce a strong password policy for SFTP users. Since AWS Transfer (with custom auth) will accept whatever secret is stored, it's up to you to ensure the passwords you put in Secrets Manager are strong enough. If users set their own passwords through some interface, add validation for length, complexity, etc. You might also implement account lockout or throttling in the auth Lambda (not trivial since Lambda is stateless, but you could log failed attempts and temporarily deny access if too many failures from the same source IP or for the same user).

**3.3 Monitoring and Logging:**

- **CloudWatch Logs:** We attached a CloudWatch logging role to the Transfer server. Go to CloudWatch Logs and you should see a log group like `/aws/transfer/<server-id>`. This will contain logs of user activity: file uploads, downloads, deletions, etc., along with timestamps and user names. Monitor these logs for any suspicious activity (you can set up CloudWatch Log Insights queries or alerts for certain patterns, e.g., numerous failed logins might appear via the Lambda logs rather than these logs).

- **CloudWatch metrics:** AWS Transfer publishes some metrics, and S3 publishes many metrics (e.g., bytes transferred). You can use CloudWatch to track number of connections, files transferred, or errors. Set up alarms if needed (for example, alert if there’s a sudden spike in failed login attempts or if the data transfer volume deviates from normal, which could indicate abuse).

- **Application logs:** For the Spring Boot API, enable logging (and if running on AWS, push logs to CloudWatch or another monitoring system). This lets you audit usage of the API (which user called what, etc.). If using Spring Security with basic auth or tokens, make sure to log authentication attempts (but not passwords) and any potential security-relevant events.

- **Testing and scanning:** Regularly run security scans. For the infrastructure, AWS Config rules or third-party tools can check that your SFTP is configured securely (for example, AWS Config has a rule to check if Transfer logging is enabled). For the application, use dependency scanning and penetration testing to ensure the API is not exposing anything unintentionally.

By following these security practices, you'll ensure that the SFTP service and the complementary API are robust against common threats.

## 4. Deployment and Testing

Finally, after configuration and development, we deploy the Terraform-managed infrastructure and test both SFTP access and the Spring Boot API to verify everything works as expected.

### 4.1 Deploying the Terraform Configuration

**Step 1: Apply Terraform** – Run `terraform init` (to ensure providers are installed) and then `terraform apply` on the configuration from Section 1. Terraform will create the resources in your AWS account:

- S3 bucket
- IAM roles/policies
- Secrets Manager entries
- Lambda function
- API Gateway
- Transfer Family server

This could take a few minutes (especially API Gateway deployment). Once complete, Terraform will output (if configured) the SFTP server ID and maybe the server endpoint URL. If not, you can fetch the server endpoint from the AWS Console or CLI. It will look like `s-xxxxxxxx.transfer.amazonaws.com` (if public) or an EIP address if VPC with EIP.

**Step 2: DNS setup (optional)** – If you want a custom hostname for your SFTP server, you can create a CNAME in Route 53 (or other DNS) pointing to the Transfer server's endpoint URL ([Setup SFTP on AWS with Username and Password in 15 minutes | CodeRise Technologies - Your Cloud Partner for Digital Success](https://coderise.io/sftp-on-aws-with-username-and-password/#:~:text=required%20IAM%20roles)). This can be useful for user-friendliness (e.g., `sftp.mycompany.com`). Ensure to update any clients to use that host and the port (22).

**Step 3: Verify AWS resources** – Check in the AWS console:

- In AWS Transfer Family, you should see the SFTP server in **Online** state. It will have an endpoint, identity provider set to **API Gateway**, and the logging role attached.
- In API Gateway, the endpoint should exist and be deployed to a stage (we used `prod` in Terraform).
- In Lambda, the function for auth should be present. You can even test it manually by simulating an event (providing sample `username`, `password`, etc., in the payload) to ensure it returns the expected output (allow or deny).
- In Secrets Manager, ensure the user secrets are in place (the naming format must match exactly what the Lambda expects: e.g., `aws/transfer/s-1234567890abcdef/user1`). The secret should have the **key** "Password" and the correct value.

### 4.2 Running and Testing the Spring Boot API

**Step 4: Run the Spring Boot application** – If testing locally, just start the application (e.g., `mvn spring-boot:run`). Ensure you provided the necessary AWS credentials (perhaps via `application.properties` or environment) and the `bucketName`. The app should start up on port 8080 (by default).

**Step 5: Test file upload via API** – Use a tool like curl or Postman to test the REST API:

- **Upload Test:**
  ```bash
  curl -u apiuser:apipassword -X POST \
       -F file=@example.txt \
       http://localhost:8080/files/upload
  ```
  This uses basic auth (`-u apiuser:apipassword`) and posts a file. The response should be a 200 OK with message "File uploaded: example.txt". Check the S3 bucket via AWS Console or CLI to see if `example.txt` object is now present in the bucket.
- **Download Test:**
  ```bash
  curl -u apiuser:apipassword -X GET \
       -o downloaded.txt \
       http://localhost:8080/files/download/example.txt
  ```
  This should retrieve the file and save it locally as `downloaded.txt`. Verify its contents match the original file. If you get a 401 Unauthorized, verify the credentials or security config.

Test edge cases: uploading a file with the same name (should overwrite unless versioning is on), downloading a non-existent file (should get a 404 as coded), etc.

### 4.3 Testing SFTP File Transfers

**Step 6: Test SFTP login and file transfer** – Now test the actual SFTP server:

- Use an SFTP client (for example, the command-line `sftp` or tools like FileZilla or WinSCP). Connect to the SFTP server using the hostname from the AWS console (or your custom domain). Use the SFTP username and password that you configured in Secrets Manager (e.g., "user1" and "User1S3cur3Pass!").
- You should be able to establish an SFTP connection. If connection fails, check that the server is in **Online** state and that your network can reach it (for VPC endpoints, you might need to be in that VPC or have a VPN).
- Once connected, try uploading a file via SFTP (most clients allow drag-and-drop or use the `put` command in command-line SFTP). Then check that the file appears in the S3 bucket (it should, within the user's home directory if one was set, otherwise at the root of the bucket).
- Similarly, test downloading a file that was uploaded via the API earlier. The user should see it in their directory and be able to download (`get` command).

If the SFTP client lists an empty directory or cannot see the file uploaded via API, consider the home directory mapping: possibly the SFTP user is restricted to a certain prefix (HomeDirectory). For example, if the API put the file at bucket root and the user's home is `/bucket/home/user1`, the user won't see files outside `/home/user1`. Ensure consistency between how the API places files and the SFTP user's accessible path.

**Step 7: Monitor logs and troubleshoot** – During these tests, watch the CloudWatch logs:

- The **Lambda log** (for auth) will show an invocation each time you attempted a login. If a login failed, it might show the reason (e.g., "password mismatch" or secret not found). This is the first place to check if your SFTP login isn't working. Common issues include the secret name not matching (case sensitive) or the Transfer server using a different server ID than expected (if you recreated the server, the ID changes, and you need to update secret names).
- The **Transfer server log** (CloudWatch Logs for `/aws/transfer/...`) will show SFTP file operations. Check if your upload via SFTP was logged, and if any permission errors are there.
- The Spring Boot app log (console or its logging system) will show the API calls. Ensure no errors there when accessing S3. If the app had insufficient AWS permissions, you'd see errors when calling S3 (which you can fix by adjusting the IAM policy or credentials used by the app).

### 4.4 Debugging Common Issues

Here are some common issues and how to address them:

- **SFTP user cannot authenticate (password)**: Double-check the Secrets Manager entry. The secret name and the keys inside must be exact. For example, if your username is "User1" but you named the secret "user1", the lookup will fail. The Lambda is likely using the username case-sensitively. Also, ensure the `Password` in the secret matches what you are typing. Remember that if you updated a secret value, the Lambda might be caching it (depending on implementation). The AWS sample Lambda does a fresh Secrets Manager lookup each time, so that should reflect changes immediately.

- **SFTP user cannot see or access files**: This usually is an IAM role or Home Directory issue. If you set a `HomeDirectory` for the user (either via secret or if using service-managed user), the user will be restricted to that path. Ensure the IAM role’s policy covers that path. For example, if HomeDirectory is `/mybucket/home/user1`, the IAM policy should allow access to `mybucket/home/user1/*` (and list on `mybucket/home/user1/` as well as possibly list on the bucket or parent prefixes). If the policy is too restrictive or too broad, issues arise. Use the AWS Security Blog tip to include the trailing slash in resource ARNs to avoid confusion ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=session%20policy%20is%20missing%20a,makes%20it)).

- **Permissions error on upload/download via SFTP**: If the SFTP client says "permission denied" when uploading, it indicates the IAM role did not permit a putObject to that key. The CloudWatch logs would show an access denied. Modify the IAM policy for the S3 access role accordingly. Also ensure the S3 bucket policy (if any) isn’t blocking it. (If no bucket policy, IAM alone governs access, which is fine.)

- **Terraform re-ordering issues**: When running `terraform apply`, you might hit an ordering issue where the Transfer server creation tries to call the API Gateway before it's fully ready. In such cases, adding explicit dependencies in Terraform (or using `depends_on` in the transfer_server resource for the API Gateway deployment) can help. Another issue is the circular dependency of server ID and secret creation. If Terraform tries to create the secret before the server, you wouldn't know the server ID. One solution is to apply in two phases: first create the server (with service-managed auth temporarily), grab the ID, then create secrets and switch to API Gateway auth. This complication is a Terraform nuance. For simplicity, some might choose to use the AWS SAM template out-of-band and not manage secrets in TF, instead inputting them manually. As an advanced Terraform user, you could use the Transfer server resource with `identity_provider_type = SERVICE_MANAGED` initially to get the ID, create secrets, then update to API_GATEWAY in a second run. Use caution and maybe test in a lower environment.

- **Spring Boot upload API returns 500**: Check the logs for an exception. Possibly the AWS credentials used by the app do not have access to the S3 bucket (access denied from AWS). Ensure the IAM user/role for the app has rights. Another possibility is a network issue if running outside AWS and using a VPC endpoint without a public route to S3 – but since S3 is public, that’s unlikely to affect a local dev test. If using an AWS VPC endpoint for S3, ensure your app can connect to S3 (maybe needing VPC configuration).

- **Download API returns 404 for existing file**: This means the S3 `getObject` threw an exception (we map to 404). If the file definitely exists in the bucket, check that the key name matches. Remember that S3 is case-sensitive in key names and that the prefix matters. Also, if the S3 file was uploaded via SFTP into a home directory, the key might include that path. Our simple API put it to the root (or whatever path given). So there could be a mismatch in where files are being placed. Align the paths or adjust your S3FileService to use subdirectories as needed.

Once everything is configured correctly, you should have a fully functioning AWS-hosted SFTP server with password authentication and a parallel Spring Boot REST API for file transfer. Users can choose to connect via SFTP using their username/password (which is validated against Secrets Manager), or use your web API with appropriate credentials.

## Conclusion

We have created a secure and flexible file transfer setup using AWS Transfer Family (SFTP) and a Spring Boot API. Using **Terraform**, we automated the provisioning of AWS resources: S3 for storage, Transfer Family for SFTP, IAM roles for fine-grained permissions, Secrets Manager for user passwords, API Gateway and Lambda for custom authentication. On the application side, we leveraged **AWS SDK for Java** within a Spring Boot app to interact with the S3 bucket (which is the same storage behind the SFTP server), providing REST endpoints for file upload/download. Throughout the process, we applied security best practices like least privilege IAM roles, encrypted secret storage, network restrictions, and logging/monitoring with CloudWatch.

By following this guide, an advanced developer should be able to implement a production-ready SFTP solution that integrates with modern applications and adheres to security and compliance requirements. Happy transferring!

**References:**

- AWS Storage Blog – _Enable password authentication for AWS Transfer Family using AWS Secrets Manager_ ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=AWS%20Transfer%20Family%20provides%20a,provider%20setup%20via%20API%20Gateway)) ([Enable password authentication for AWS Transfer Family using AWS Secrets Manager (updated) | AWS Storage Blog](https://aws.amazon.com/blogs/storage/enable-password-authentication-for-aws-transfer-family-using-aws-secrets-manager-updated/#:~:text=AWS%20Lambda%20function)) – Describes the approach of using a custom identity provider with Secrets Manager to allow password logins for SFTP.
- CodeRise Tech Blog – _Setup SFTP on AWS with Username and Password_ ([Setup SFTP on AWS with Username and Password in 15 minutes | CodeRise Technologies - Your Cloud Partner for Digital Success](https://coderise.io/sftp-on-aws-with-username-and-password/#:~:text=In%20this%20blog%2C%20we%20will,reliable%2C%20scalable%20and%20durable%20solution)) ([Setup SFTP on AWS with Username and Password in 15 minutes | CodeRise Technologies - Your Cloud Partner for Digital Success](https://coderise.io/sftp-on-aws-with-username-and-password/#:~:text=Step,functions%20and%20required%20IAM%20roles)) – Provides a high-level overview and mentions the use of AWS Secrets Manager and a CloudFormation template for quickly setting up SFTP with password auth.
- AWS Security Blog – _Six tips to improve the security of your AWS Transfer Family server_ ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=Amazon%20API%20Gateway,instance%20to%20allow%20access%20for)) ([Six tips to improve the security of your AWS Transfer Family server | AWS Security Blog](https://aws.amazon.com/blogs/security/six-tips-to-improve-the-security-of-your-aws-transfer-family-server/#:~:text=session%20policy%20is%20missing%20a,makes%20it)) – Recommends best practices like using WAF on the identity provider API and careful IAM policy scoping (use of "/" in S3 ARNs).
- Terraform AWS Provider Documentation – _aws_transfer_server resource_ – Details on configuring Transfer Family in Terraform (identity_provider_type, invocation_role, etc.) ([terraform-aws-sftp-server/transfer-family.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/transfer-family.tf#:~:text=protocols%20%3D%20%5B)) ([terraform-aws-sftp-server/transfer-family.tf at master · zicodeng/terraform-aws-sftp-server · GitHub](https://github.com/zicodeng/terraform-aws-sftp-server/blob/master/transfer-family.tf#:~:text=endpoint_details%20)).
- AWS SDK for Java Documentation – _Amazon S3 SDK examples_ – Demonstrates usage of the AmazonS3 client to upload and download objects in Java ([A Guide to Upload Files to Amazon S3 Bucket Using Spring Boot](https://www.cloudthat.com/resources/blog/a-guide-to-upload-files-to-amazon-s3-bucket-using-spring-boot#:~:text=%40Service%20public%20class%20S3FileUploadService%20,)).
- Spring Security Reference – Guides on securing REST APIs with Spring Security (for implementing Basic auth or JWT as needed) ([Using Spring Boot for OAuth2 and JWT REST Protection - Toptal](https://www.toptal.com/spring/spring-boot-oauth2-jwt-rest-protection#:~:text=Using%20Spring%20Boot%20for%20OAuth2,every%20language%20and%20on)).
