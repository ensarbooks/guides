# Terraform Guide: EC2-based Elasticsearch Cluster with ELB

This guide walks through provisioning an **Amazon EC2-based Elasticsearch cluster** behind an **Elastic Load Balancer (ELB)** using Terraform. It covers an advanced setup with multiple configuration options (environment-specific settings, Elasticsearch version selection, secure credentials, etc.). We’ll use a modular project structure and Terraform best practices to ensure the cluster is scalable and maintainable. Each section below corresponds to a key aspect of the implementation, with code snippets and explanations.

## 1. File Structure & Organization

Organizing Terraform code properly makes it easier to manage and reuse. We will use the standard Terraform project layout:

- **Main configuration files**:

  - `main.tf` – the primary entry point where resources are defined (or where modules are called) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,for%20variables%20and%20outputs%2C%20respectively)).
  - `variables.tf` – all input variable definitions (with types, defaults, and descriptions) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,for%20variables%20and%20outputs%2C%20respectively)).
  - `outputs.tf` – all output values exported by the configuration ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,for%20variables%20and%20outputs%2C%20respectively)).
  - (Optionally, a `versions.tf` for required provider/Terraform versions.)

- **Modules directory**:
  - `modules/` – contains reusable child modules for components like the Elasticsearch cluster, ELB, etc. Each module follows the same file structure (`main.tf`, `variables.tf`, `outputs.tf`) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,their%20own%20IAM%20policy%20choices)). Modules help encapsulate resources (for example, you might have a module for the EC2 cluster and another for the load balancer) to keep the root configuration simple and DRY ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=1)).

For instance, a module could be created for the **Elasticsearch cluster** (defining EC2 instances, Auto Scaling Group, security groups, etc.) and another for the **ELB**. The root `main.tf` would then instantiate these modules with the appropriate variables. Using modules in this way allows advanced users to swap or reuse components easily ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=1)).

**Project Structure Example:**

```
terraform-elasticsearch/
├── main.tf          # Root module: calls child modules or defines resources
├── variables.tf     # Input variable definitions for root module
├── outputs.tf       # Output definitions for root module
├── modules/
│   ├── ec2_cluster/
│   │    ├── main.tf        # EC2 instances + ASG
│   │    ├── variables.tf   # Variables for cluster module (e.g., AMI ID, instance type)
│   │    └── outputs.tf     # Outputs from cluster module (e.g., instance IDs)
│   └── elb/
│        ├── main.tf        # ELB resource and related settings
│        ├── variables.tf   # Variables for ELB module (e.g., subnet IDs, SGs)
│        └── outputs.tf     # Outputs from ELB module (e.g., ELB DNS)
└── env/
    ├── dev.tfvars    # (Optional) TF variables file for Dev environment
    ├── staging.tfvars
    └── prod.tfvars
```

Each Terraform file has a clear purpose. Keeping variables and outputs separate makes the configuration cleaner and auto-generates documentation for inputs/outputs ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,69%20for%20more%20details)). The modules directory can contain nested modules if needed to further split complex behavior (for example, separate sub-modules for IAM policies, if those get complex) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,their%20own%20IAM%20policy%20choices)).

## 2. Environment & Version Configuration

We want our Terraform code to deploy the cluster to different environments (Development, Integration, Staging, Production) with potentially different settings, and to support multiple Elasticsearch versions (2.4.5 vs 8.0.0). We achieve this with input **variables** and conditional logic.

**Environment Variable**: Define a variable to specify the deployment environment. This can control naming conventions, number of instances, and other env-specific tweaks. We’ll also enforce allowed values using Terraform's validation rule:

```hcl
variable "environment" {
  description = "Deployment environment (Development, Integration, Staging, Production)"
  type        = string
  validation {
    condition     = contains(["Development","Integration","Staging","Production"], var.environment)
    error_message = "Environment must be one of Development, Integration, Staging, Production."
  }
}
```

This variable ensures the user specifies a valid environment name, preventing typos ([Terraform - How to restrict an input variable to a list of possible choices - Stack Overflow](https://stackoverflow.com/questions/57190035/terraform-how-to-restrict-an-input-variable-to-a-list-of-possible-choices#:~:text=variable%20,%3D%20string)). In practice, you might use a shorter enum (like "dev", "intg", "stage", "prod") for convenience, but the concept is the same. The chosen `environment` can be used in resource names or tags to distinguish resources in different environments (e.g., an EC2 name prefix or an S3 bucket name could include the environment).

**Elasticsearch Version Variable**: We also define a variable for the Elasticsearch version:

```hcl
variable "elasticsearch_version" {
  description = "Elasticsearch major version (e.g., 2.4.5 or 8.0.0)"
  type        = string
  validation {
    condition     = contains(["2.4.5", "8.0.0"], var.elasticsearch_version)
    error_message = "Supported versions are 2.4.5 or 8.0.0."
  }
}
```

This allows us to adjust resources based on the version. For example, we might use different AMIs or user-data scripts for ES 2.x vs 8.x. By restricting the values, we ensure only supported versions are deployed.

**Using the Environment Variable**: The environment variable can be used to parameterize the configuration so that _the only differences between environments are the values of variables_, not the structure of resources ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=You%20do%20not%20want%20different,the%20only%20thing%20that%20changes)). For instance, we could set lower instance counts or smaller instance types for Development, and larger ones for Production. These values can be supplied via separate `.tfvars` files or Terraform Cloud workspace variables for each environment. This approach guarantees that Dev, Staging, Prod all use the same Terraform code (infrastructure-as-code), with only the inputs differing, so what you test in Dev is what you later run in Prod (just scaled appropriately) ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=You%20do%20not%20want%20different,the%20only%20thing%20that%20changes)).

**Example**: If using Terraform Cloud or workspaces, you might have a workspace per environment (a common strategy is one workspace per env per configuration) to keep state separate ([Automating Multi-Environment Deployments with Terraform Cloud ...](https://medium.com/hashicorp-engineering/automating-multi-environment-deployments-with-terraform-cloud-workspaces-6d9c7dcd2321#:~:text=Automating%20Multi,and%20permissions%20should%20match)). Each workspace can override the `environment` variable (and others) accordingly. If using CLI, you might structure different directories or simply use `-var-file=env/dev.tfvars` for each environment. Both approaches are viable; just ensure each environment’s state is separate and locked (more on state management in section 10).

## 3. Instance & Cluster Configuration

Next, we configure the EC2 instances that will form the Elasticsearch cluster, using an **Auto Scaling Group (ASG)** for high availability and scalability. Key parameters (instance type, disk size, cluster size) will be configurable via variables.

**EC2 Instance Type & AMI**: Define a variable for the instance type (e.g., `t3.medium`, `m5.large` depending on needed memory/CPU) and choose an appropriate Amazon Machine Image (AMI). The AMI could be an official Linux distribution or a custom image pre-baked with Elasticsearch. For demonstration, we might use Amazon Linux 2 or Ubuntu and install Elasticsearch via user data. The AMI ID can be looked up by Terraform data sources (filtered by OS and region). If ES 2.4.5 requires an older OS (Java 8) and ES 8.0.0 can run on a newer OS (Java 11+), we could map versions to different AMIs.

Example variable definitions:

```hcl
variable "instance_type" {
  description = "EC2 instance type for Elasticsearch nodes"
  type        = string
  default     = "t3.medium"
}
variable "instance_count" {
  description = "Number of ES data nodes (desired capacity of ASG)"
  type        = number
  default     = 3
}
variable "root_volume_size" {
  description = "Size (GB) of the root EBS volume for each instance"
  type        = number
  default     = 50
}
```

_(We will configure the root volume in detail in section 7.)_

**Auto Scaling Group Setup**: We use an ASG to maintain the desired number of instances and spread them across multiple Availability Zones for resilience. We’ll create either an `aws_autoscaling_group` with a Launch Configuration or Launch Template. A Launch Template is more modern and flexible (and supports new features), so we'll illustrate using `aws_launch_template` plus ASG.

- **Launch Template**: Specifies the instance configuration (AMI, instance type, key pair, security groups, user data, etc.). We include a block to set the root volume size and enable encryption:
  ```hcl
  resource "aws_launch_template" "es_nodes" {
    name_prefix   = "${var.environment}-es-${var.elasticsearch_version}-"
    image_id      = data.aws_ami.linux_es.id   # looked up AMI appropriate for the ES version
    instance_type = var.instance_type
    key_name      = var.key_name               # SSH key for access (passed in as variable)
    security_group_names = []                  # (We will attach SGs via ASG or use network_interfaces)
    user_data     = base64encode(templatefile("user_data_es.sh", {
                      es_version = var.elasticsearch_version,
                      cluster_name = "${var.environment}-es-cluster"
                   }))
    block_device_mappings {
      device_name = "/dev/xvda"
      ebs {
        volume_size           = var.root_volume_size
        encrypted             = true
        delete_on_termination = true
      }
    }
    # (additional settings like IAM instance profile will be added in Security section)
  }
  ```
  In the above:
  - We set `device_name = "/dev/xvda"` (commonly the root volume device name for Amazon Linux) and configure an EBS block with `volume_size` and `encrypted = true` to ensure the root disk is of desired size and encrypted ([terraform: Set root device size using launch template](https://pet2cattle.com/2022/06/launch-template-root-device#:~:text=resource%20,demo_launch_tpl)).
  - The `user_data` is populated from an external shell script (`user_data_es.sh`) using `templatefile` for clarity. This script will handle installing and configuring Elasticsearch on the instance at boot.
- **Auto Scaling Group**: Now we define the ASG to use this launch template:

  ```hcl
  resource "aws_autoscaling_group" "es_cluster" {
    name                      = "${var.environment}-es-cluster"
    vpc_zone_identifier       = var.private_subnet_ids  # Subnets to launch instances in (private subnets across AZs)
    max_size                  = var.instance_count
    min_size                  = var.instance_count
    desired_capacity          = var.instance_count
    launch_template {
      id      = aws_launch_template.es_nodes.id
      version = "$Latest"
    }
    health_check_type         = "EC2"
    health_check_grace_period = 300
    tag {
      key                 = "Name"
      value               = "${var.environment}-es-node"
      propagate_at_launch = true
    }
  }
  ```

  Here we fix `min_size` = `max_size` = `desired_capacity` for a static cluster size (no autoscaling by load, just using ASG for resilience). We spread instances in the provided subnets (which should span multiple AZs). All instances get a Name tag including the environment.

  The ASG ensures the specified number of instances is running. If an instance is terminated (e.g., due to failure), the ASG will launch a replacement automatically. In a multi-AZ setup, this gives high availability.

  _Note:_ We use `health_check_type = "EC2"` for basic EC2 status checks. In a more advanced setup, you might integrate with ELB health checks or custom scripts.

**User Data Script**: The user data is a crucial piece – it bootstraps Elasticsearch on the EC2 instances. Terraform will pass this script to AWS, and EC2 cloud-init will run it on instance launch. Typical steps in `user_data_es.sh` might include:

- Installing Java (OpenJDK).
- Downloading and installing Elasticsearch (if not using a pre-baked AMI). For ES 2.4.5, this could mean installing from a package or tarball; for ES 8.0.0, similarly.
- Writing the Elasticsearch configuration file (`elasticsearch.yml`) with appropriate cluster settings:
  - Set the cluster name (e.g., `cluster.name: "${var.environment}-es-cluster"`).
  - Set node roles (master-eligible, data, etc. depending on your design; for simplicity, assume all nodes are master+data).
  - Configure discovery: For ES 7.x and above, use `cluster.initial_master_nodes` on the first boot for forming a cluster, and possibly use AWS EC2 discovery (via the AWS plugin or by listing private IPs). For ES 2.x, use `discovery.zen.ping.unicast.hosts` if needed.
  - Set network host to local interfaces, etc.
- If Elasticsearch security features are enabled (like in 8.0.0, security is on by default), the user-data might also set up the built-in `elastic` user password (see **Security** section for how to handle this securely).
- Start the service (enable it to start on boot).

For example, a snippet of user data for ES 2.4.5 on Amazon Linux might look like:

```bash
#!/bin/bash
# Install Java 8
yum install -y java-1.8.0-openjdk
# Download and install Elasticsearch 2.4.5
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-2.4.5.rpm
rpm -ivh elasticsearch-2.4.5.rpm
# Configure Elasticsearch
echo "cluster.name: ${var.environment}-es-cluster" >> /etc/elasticsearch/elasticsearch.yml
echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml        # Listen on all interfaces
echo "discovery.zen.ping.unicast.hosts: []" >> /etc/elasticsearch/elasticsearch.yml  # (Using EC2 discovery plugin or none for single-node)
# Start Elasticsearch
service elasticsearch start
```

For ES 8.0.0, it would be similar but with installing a newer version (and possibly setting `cluster.initial_master_nodes` if this is the first boot of the cluster).

The main point is that **user data provides the init commands for the instances**. When the ASG launches a new EC2, it references the Launch Template which contains these `user_data` instructions ([amazon web services - Define: Terraform - AWS - aws_instance - user_data - Stack Overflow](https://stackoverflow.com/questions/54527189/define-terraform-aws-aws-instance-user-data#:~:text=So%20in%20general%2C%20after%20you,desired%20capacity)). This ensures every Elasticsearch node is automatically configured and joins the cluster on boot without manual intervention.

**IAM Instance Profile**: We will attach an IAM role to the EC2 instances (via an instance profile) to grant them permissions for certain actions (for example, reading from S3 for snapshots or reading secure parameters from SSM, as discussed later). The IAM role and profile configuration will be covered in **Security & Access** below.

At this stage, we have an ASG-defined cluster of EC2 instances running Elasticsearch, but we need to set up the Load Balancer to access them and configure networking/security.

## 4. Load Balancer Setup

We will use an **internal Elastic Load Balancer (ELB)** to distribute traffic to the Elasticsearch nodes. This ELB will listen on the necessary ports and forward traffic to the instances. The ports we need:

- **9200 (HTTP)** – for Elasticsearch REST API calls.
- **9300 (TCP)** – for cluster communication (transport protocol). Typically, clients don't need this, but if we have dedicated client nodes or cross-cluster traffic, exposing 9300 via LB might be useful. (Elasticsearch nodes normally discover each other via unicast or other means, so an LB for 9300 is optional. We include it for completeness or for external client use.)
- **443 (HTTPS)** – if we want to allow secure HTTPS access to the cluster from, say, a VPN or proxy. We will terminate SSL at the ELB using an ACM certificate.

We'll create an `aws_elb` resource (classic ELB) with these listeners. Key settings for the ELB:

- Make it **internal** (not internet-facing) since Elasticsearch should not be publicly accessible. Setting `internal = true` achieves this ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true)).
- Enable **cross-zone load balancing** so that traffic is evenly distributed across instances in different AZs ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true)). This prevents imbalance if one AZ has fewer nodes.
- Configure **listeners** for the ports/protocols mentioned.
- Set up a **health check** targeting the Elasticsearch service on port 9200.
- Attach the appropriate **security group** to the ELB (allowing inbound on 9200/9300/443 from the clients and outbound to instances).

**ELB Resource Example:**

```hcl
resource "aws_elb" "es_elb" {
  name               = "${var.environment}-es"            # ELB name
  internal           = true                               # Internal LB (not public) ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true))
  subnets            = var.elb_subnet_ids                 # Private subnets for the ELB (e.g., two subnets in different AZs)
  security_groups    = [aws_security_group.elb.id]        # ELB security group (to be defined in Security section)
  cross_zone_load_balancing = true                        # Distribute traffic across AZs ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true))
  idle_timeout        = 60

  listener {
    lb_port           = 9200
    lb_protocol       = "http"
    instance_port     = 9200
    instance_protocol = "http"
  }
  listener {
    lb_port           = 9300
    lb_protocol       = "tcp"
    instance_port     = 9300
    instance_protocol = "tcp"
  }
  listener {
    lb_port           = 443
    lb_protocol       = "https"
    instance_port     = 9200
    instance_protocol = "http"
    ssl_certificate_id = var.acm_certificate_arn  # ACM certificate for the domain (passed in as a variable)
  }

  health_check {
    target              = "HTTP:9200/"   # Check HTTP on port 9200 root path ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=health_check%20))
    interval            = 10
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "${var.environment}-es-elb"
  }
}
```

In this configuration:

- We define three listeners:
  - HTTP on 9200 -> forward to instance port 9200 ([elasticsearch-ecs/terraform/elasticsearch/main.tf at master · firstlookmedia/elasticsearch-ecs · GitHub](https://github.com/firstlookmedia/elasticsearch-ecs/blob/master/terraform/elasticsearch/main.tf#:~:text=listener%20)).
  - TCP on 9300 -> forward to 9300 ([elasticsearch-ecs/terraform/elasticsearch/main.tf at master · firstlookmedia/elasticsearch-ecs · GitHub](https://github.com/firstlookmedia/elasticsearch-ecs/blob/master/terraform/elasticsearch/main.tf#:~:text=listener%20)).
  - HTTPS on 443 -> forward to 9200 (the ELB will handle SSL termination using the provided `ssl_certificate_id`).
- The `ssl_certificate_id` should be the ARN of an ACM certificate for the domain name you plan to use to access Elasticsearch (if any). If you don't need external HTTPS access, you can omit the 443 listener.
- The health check is hitting `HTTP:9200/` (the root of Elasticsearch, which should return a 200 OK if the node is up). This way, the ELB knows which nodes are healthy and only routes traffic to healthy instances ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=health_check%20)). We set relatively quick interval and thresholds for faster detection of down nodes.

By setting `internal = true`, this ELB will get a DNS name that is resolvable only within the VPC. It will not have a public IP. Clients within your network (application servers, etc.) can use this ELB to communicate with Elasticsearch. Cross-zone load balancing being true ensures if we have, say, 2 nodes in AZ A and 1 node in AZ B, an even load of requests goes to AZ B’s single node as well ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true)).

**Note on using ALB/NLB**: We chose a classic ELB for simplicity and because it supports both TCP and HTTP listeners on one LB. Alternatively, one could use an **NLB** for 9300 (TCP) and an **ALB** for 9200/443 (HTTP/HTTPS), but that adds complexity and multiple DNS endpoints. The classic ELB suffices for this use-case and allows all needed ports on one endpoint.

After applying Terraform, you will have an ELB DNS name (e.g., `internal-dev-es-123456789.us-west-2.elb.amazonaws.com`). We will output this name for convenience. You might also associate it with a friendly CNAME record (optional, via Route53) for easier access (the example in the code above shows how a Route53 record was created for an ELB ([elasticsearch-ecs/terraform/elasticsearch/main.tf at master · firstlookmedia/elasticsearch-ecs · GitHub](https://github.com/firstlookmedia/elasticsearch-ecs/blob/master/terraform/elasticsearch/main.tf#:~:text=resource%20%22aws_route53_record%22%20%22elasticsearch)), though we can also output and use the DNS directly).

## 5. Security & Access

Security is critical for a datastore like Elasticsearch. We will address it on multiple fronts: network access via security groups and load balancer, IAM roles for the EC2 instances, secure handling of the Elasticsearch credentials, and placement in private subnets.

**VPC Network and Subnets**: All resources (EC2 instances and ELB) should reside in a secure VPC. The instances will be in **private subnets** (no direct internet access) and the ELB in an internal subnet. Ensure the subnets provided to the ASG and ELB are not public. If the cluster needs internet for updates, use a NAT gateway or similar. By keeping ES nodes in private subnets, we prevent external access by default.

**Security Groups**: We will use multiple security groups (SGs) to segregate access:

- **Elasticsearch Instances SG**: Allows inbound traffic from the ELB on the necessary ports, and allows intra-cluster communication among instances.
- **ELB SG**: Allows inbound from permitted clients and outbound to instances.

For example:

```hcl
resource "aws_security_group" "es_nodes" {
  name        = "${var.environment}-es-nodes"
  vpc_id      = var.vpc_id
  description = "Security group for ES cluster instances"

  # Ingress rules for ES ports (from ELB SG and self for cluster comm)
  ingress {
    from_port   = 9200
    to_port     = 9200
    protocol    = "tcp"
    security_groups = [aws_security_group.elb.id]  # allow 9200 from ELB
  }
  ingress {
    from_port   = 9300
    to_port     = 9300
    protocol    = "tcp"
    security_groups = [aws_security_group.elb.id, aws_security_group.es_nodes.id]
    # allow 9300 from ELB (if needed) and from itself (cluster nodes talking to each other)
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_allowed_cidrs  # allow SSH from admin IPs (if needed for maintenance)
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # allow instances to initiate any outbound (e.g., to S3 or OS updates)
  }
}
resource "aws_security_group" "elb" {
  name        = "${var.environment}-es-elb"
  vpc_id      = var.vpc_id
  description = "Security group for ES ELB"

  ingress {
    from_port   = 9200
    to_port     = 9200
    protocol    = "tcp"
    cidr_blocks = var.allow_cidr_blocks  # IP ranges allowed to query ES (e.g., app network or VPN CIDR)
  }
  ingress {
    from_port   = 9300
    to_port     = 9300
    protocol    = "tcp"
    cidr_blocks = var.allow_cidr_blocks  # likely same as above if needed
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allow_cidr_blocks
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

In the above SG setup:

- The **ELB SG** (`aws_security_group.elb`) allows incoming traffic on 9200, 9300, 443 from whatever sources you deem appropriate (could be your application servers’ SGs or IP ranges for your offices, etc.). This effectively acts as the entry point to the cluster.
- The **ES Nodes SG** (`aws_security_group.es_nodes`) only trusts the ELB and itself:
  - 9200/tcp from ELB SG (meaning only the ELB can hit the node REST API).
  - 9300/tcp from ELB SG (if the LB is used for transport) and from its own SG (this allows node-to-node communication between ES instances – each instance has the same SG, so this rule lets them talk to each other on 9300).
  - SSH (22) optionally from an admin IP for maintenance.
  - All outbound traffic is allowed from nodes (to reach out for updates, license checks, or S3 for snapshot repository, etc.).
- We attach `aws_security_group.es_nodes.id` to the EC2 Launch Template (or via the ASG). The ELB already has `security_groups = [aws_security_group.elb.id]`.

This configuration ensures that no client can talk directly to ES nodes except via the ELB (which acts as a gatekeeper). Also, it isolates cluster traffic.

**IAM Role for EC2**: Create an IAM role that the EC2 instances will assume. Attach policies needed for:

- Reading/writing to S3 (for snapshot repositories or bootstrap scripts).
- Reading secure parameters from SSM Parameter Store or Secrets Manager (for retrieving credentials or config).
- Sending logs to CloudWatch Logs (if you install a CloudWatch agent or use the default CloudWatch logging for AWS Linux).

Example:

```hcl
resource "aws_iam_role" "es_instance_role" {
  name = "${var.environment}-es-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json  # trust relationship for EC2
}
resource "aws_iam_instance_profile" "es_instance_profile" {
  name = "${var.environment}-es-profile"
  role = aws_iam_role.es_instance_role.name
}
# Attach policies (AWS managed or custom)
resource "aws_iam_role_policy_attachment" "es_ssm" {
  role       = aws_iam_role.es_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"  # example: allows SSM agent and parameter store access
}
resource "aws_iam_role_policy_attachment" "es_s3" {
  role       = aws_iam_role.es_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"        # if needed for snapshots
}
```

Attach the instance profile to the Launch Template (`iam_instance_profile = aws_iam_instance_profile.es_instance_profile.name`). This way, any actions the user-data script or running ES process needs (like accessing S3 or SSM) can be authorized by AWS without embedding AWS keys.

**Securely Handling Elasticsearch Password**: For ES 8.x, security is enabled by default and Elasticsearch will require a password for the `elastic` superuser. We **do not** want to hardcode this password in Terraform code or user-data. Instead, we can generate and store it securely:

- Use Terraform’s `random_password` resource to generate a strong password for the Elastic user.
- Store this password in AWS Systems Manager Parameter Store as a SecureString, or in AWS Secrets Manager, so that it’s encrypted at rest and not exposed directly in Terraform outputs/state.
- The EC2 user-data can then fetch this password from the secure store at startup (because our EC2 IAM role has access to read that parameter/secret). For example, user-data could include an AWS CLI call or use SSM parameter retrieval to get the password and insert it into the ES keystore or use the API to set the built-in user password.

For instance:

```hcl
resource "random_password" "elastic_pwd" {
  length  = 16
  special = true
}

resource "aws_ssm_parameter" "elastic_pwd_param" {
  name  = "/${var.environment}/es/elastic-password"
  type  = "SecureString"
  value = random_password.elastic_pwd.result
  tags = {
    Environment = var.environment
    Service     = "Elasticsearch"
  }
}
```

This will generate a random 16-character password and store it in SSM Parameter Store under a path that includes the environment. The password will be encrypted with AWS managed KMS (or you can specify a KMS key). Terraform state will have the plaintext value of `random_password.elastic_pwd` unless you mark it sensitive, but because we store it in SSM and use that for retrieval, we can avoid ever printing it. (Make sure to protect your state file, see Best Practices section.)

On instance startup, a snippet in user-data could do:

```bash
# Retrieve the Elastic password from SSM Parameter Store
TOKEN="$(curl -s 169.254.169.254/latest/meta-data/iam/security-credentials/${IAM_ROLE_NAME} | jq -r .Token)"  # if using IMDS v2
AWS_REGION="${var.aws_region}"
ELASTIC_PWD=$(aws ssm get-parameter --name "/${var.environment}/es/elastic-password" --with-decryption --region "$AWS_REGION" --output text --query Parameter.Value)
# Use the password, e.g., set it for the built-in elastic user
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -p "$ELASTIC_PWD" --batch
```

(This assumes the AWS CLI is installed or we use SSM agent. Alternatively, one could pass the password as user-data input in a more secure way using instance metadata or retrieve from Secrets Manager.)

The takeaway is: **handle credentials via secure services, not in plain text**. In our Terraform, we generate and store it securely. An operator can retrieve it from SSM when needed. We also mark the Terraform variable or output for this password as `sensitive = true` to avoid it showing in CLI output by accident.

By doing this, we **avoid static secrets in the user-data script**, fulfilling a common requirement to not bake passwords into AMIs or scripts ([How to automatically create a new Elasticsearch cluster (via Terraform and user-data scripts)? - Elasticsearch - Discuss the Elastic Stack](https://discuss.elastic.co/t/how-to-automatically-create-a-new-elasticsearch-cluster-via-terraform-and-user-data-scripts/312619#:~:text=How%20to%20automatically%20,data%20script)). Instead, the secret is pulled at runtime under IAM control.

_(For ES 2.4.5, security (X-Pack) might not be enabled by default, so password handling may not apply. But for consistency, you might still secure it if you install X-Pack or Shield on 2.4.5.)_

**Key Pair for SSH**: We included `var.key_name` in the Launch Template. This refers to an existing AWS Key Pair. Create or use an existing key pair and pass its name via Terraform (e.g., `-var="key_name=mykey"`). This allows SSH access to the instances for debugging. Only users with the private key can SSH in (and our SG only allows SSH from certain IPs). For production, limit SSH and consider using SSM Session Manager (in which case you’d attach the AmazonSSMManagedInstanceCore policy to the IAM role as shown, and you might not even need a key pair).

Now our instances will have:

- Controlled network access (only through ELB).
- Proper IAM permissions (no need for embedding AWS credentials).
- Secure password management for the Elastic user.

## 6. Resource Provisioning Logic (Version-based Conditionals)

We want Terraform to be smart about provisioning resources depending on the Elasticsearch version chosen. The cluster setup for ES 2.4.5 might differ from ES 8.0.0. We can use conditional resource counts or `for_each` to handle this.

One approach is to define **two sets of resources** (launch templates, ASGs, etc.): one for ES 2.4.5 and one for ES 8.0.0, and use the `count` meta-argument to enable the correct set based on the version variable. For example:

```hcl
resource "aws_launch_template" "es_v2" {
  count         = var.elasticsearch_version == "2.4.5" ? 1 : 0  # only create if version is 2.4.5
  name_prefix   = "${var.environment}-es24-"
  image_id      = data.aws_ami.amzn2_java8.id    # assume this AMI has Java 8 for ES2
  instance_type = var.instance_type
  # ... other settings and user_data tailored for ES 2.4.5 ...
}
resource "aws_autoscaling_group" "es_v2" {
  count                = var.elasticsearch_version == "2.4.5" ? 1 : 0
  desired_capacity     = var.instance_count
  min_size             = var.instance_count
  max_size             = var.instance_count
  launch_template      = aws_launch_template.es_v2[0].id
  vpc_zone_identifier  = var.private_subnet_ids
  depends_on           = [aws_launch_template.es_v2]  # ensure LT is created first
  # ... (other config like tags, health_check_type) ...
}

resource "aws_launch_template" "es_v8" {
  count         = var.elasticsearch_version == "8.0.0" ? 1 : 0
  name_prefix   = "${var.environment}-es8-"
  image_id      = data.aws_ami.ubuntu_java11.id   # assume an AMI with Java 11+ for ES8
  instance_type = var.instance_type
  # ... user_data for ES 8.0.0 ...
}
resource "aws_autoscaling_group" "es_v8" {
  count                = var.elasticsearch_version == "8.0.0" ? 1 : 0
  desired_capacity     = var.instance_count
  min_size             = var.instance_count
  max_size             = var.instance_count
  launch_template      = aws_launch_template.es_v8[0].id
  vpc_zone_identifier  = var.private_subnet_ids
  depends_on           = [aws_launch_template.es_v8]
}
```

Here, only one of those ASGs (and its launch template) will actually be created, because the `count` is 0 for the other. This is a common Terraform pattern to **conditionally create resources using a ternary** condition in the `count` argument ([amazon web services - Error aws_alb_target_group has "count" set, its attributes must be accessed on specific instances - Stack Overflow](https://stackoverflow.com/questions/62433708/error-aws-alb-target-group-has-count-set-its-attributes-must-be-accessed-on-s#:~:text=I%20understand,stated%20in%20my%20previous%20comment)). Each resource’s address becomes indexed (`aws_autoscaling_group.es_v2[0]`) so we reference index `[0]` since either it exists as 1 element or not at all.

Within each launch template’s `user_data`, you can use a different script file or commands appropriate to that version (e.g., install different ES version). You might also use different default `instance_type` or `root_volume_size` based on version, though that's usually not necessary.

Another approach is using `for_each` with a map of versions to config. For example, define a map variable that includes only the desired version as a key:

```hcl
locals {
  deploy_versions = { "${var.elasticsearch_version}" = true }
}
resource "aws_launch_template" "es" {
  for_each      = local.deploy_versions
  # each.key will be "2.4.5" or "8.0.0"
  name_prefix   = "${var.environment}-es-${each.key}-"
  image_id      = lookup(var.ami_map, each.key)
  instance_type = var.instance_type
  # ... other settings ...
}
```

This way, `aws_launch_template.es` will have one instance in its state with key "2.4.5" or "8.0.0". The config could look up an AMI or user-data specific to the key. This approach is useful if you potentially wanted to deploy _both_ versions concurrently (e.g., in different clusters) by setting the variable to a list, but in our case we only want one at a time, so the `count` method is simpler.

Since we only want one cluster at a time, the first method (explicit resources with count) is straightforward. It also makes it clear in code what differences exist for each ES version. For example, maybe ES 2.4.5 cluster uses a smaller instance by default and doesn’t mount EFS, whereas ES 8.0.0 might use EFS for some purpose. You can codify those differences in the respective resource blocks.

**Auto Scaling Group differences**: In our case, both versions’ ASGs are similar (just pointing to different launch configs). If you needed to e.g. run a larger cluster for the newer version by default, you could also make `instance_count` vary by version (using a conditional or lookup). For example:

```hcl
variable "default_instance_count_v2" { default = 3 }
variable "default_instance_count_v8" { default = 3 }
# ...
resource "aws_autoscaling_group" "es_v8" {
  count            = var.elasticsearch_version == "8.0.0" ? 1 : 0
  desired_capacity = var.instance_count != 0 ? var.instance_count : var.default_instance_count_v8
  # ...
}
```

Where if `instance_count` is explicitly set we use it, otherwise a default per version.

Terraform’s flexibility with conditionals allows you to avoid duplicating entire configurations for each scenario, instead toggling pieces on/off. By using these conditionals, **the same Terraform codebase can deploy either an ES 2.4.5 cluster or an ES 8.0.0 cluster** depending on input, without manual reconfiguration.

_(If you needed to run both clusters at the same time (perhaps for migration), you could set `elasticsearch_version` to both values in a list and adjust for_each logic to deploy two ASGs. But assuming one at a time for simplicity.)_

## 7. Data & Storage Configuration

Elasticsearch performance and durability depend on how storage is configured. We address two aspects:

- The **root volume** (and any instance store or EBS volumes for data).
- An **Elastic File System (EFS)** for shared persistent storage (optional but mentioned in requirements).

**Root Volume Size & Encryption**: In section 3, we configured the root volume via the launch template’s `block_device_mappings`. We used `volume_size = var.root_volume_size` (e.g., 50 GB by default) and `encrypted = true` to encrypt the volume ([terraform: Set root device size using launch template](https://pet2cattle.com/2022/06/launch-template-root-device#:~:text=resource%20,demo_launch_tpl)). Encryption uses AWS-managed keys by default to protect data at rest. Many organizations require all EBS volumes to be encrypted, and Terraform makes it easy to enforce that. We also set `delete_on_termination = true` so that when an instance is terminated, its volume is cleaned up (since this is not a stateful cluster node, and we will rely on either cluster replication or EFS for persistence).

If additional data volumes were needed (for instance, a dedicated EBS volume for Elasticsearch data separate from the root), we could add more `ebs_block_device` in a launch configuration or more entries in `block_device_mappings` for a launch template. For simplicity, we assume the root volume holds the data (common in smaller clusters). Make sure the volume size is sufficient for your data needs in each environment (perhaps use larger volumes in Prod via a variable override).

**Elastic File System (EFS) for Persistent Storage**: We include an AWS EFS to provide network-mounted storage that all cluster nodes can access. This could be used for storing snapshots, or potentially as the data directory for Elasticsearch (though ES usually expects low-latency local storage; EFS could be used in development or for shared data between nodes, but be cautious about performance). In some cases, EFS might be used to persist data through instance replacements (at the cost of performance).

To set up EFS via Terraform:

- Create the EFS file system resource.
- Create mount targets for the EFS in each subnet/AZ where your EC2 instances run.
- Configure security group rules for NFS (port 2049).

For example:

```hcl
resource "aws_efs_file_system" "es_data" {
  creation_token   = "${var.environment}-es-efs"
  performance_mode = "generalPurpose"
  encrypted        = true
  tags = {
    Name        = "${var.environment}-es-data"
    Environment = var.environment
  }
}
resource "aws_security_group" "efs" {
  name        = "${var.environment}-efs-sg"
  description = "SG for EFS mount"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    security_groups = [aws_security_group.es_nodes.id]  # allow NFS from ES instances
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_efs_mount_target" "a" {
  for_each       = toset(var.private_subnet_ids)
  file_system_id = aws_efs_file_system.es_data.id
  subnet_id      = each.key
  security_groups = [aws_security_group.efs.id]
}
```

We attach an EFS security group that permits NFS (TCP 2049) from the ES Nodes SG ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=1)). We create a mount target in each subnet where an ES instance could reside (using the subnets list via for_each).

Now, the EC2 instances can mount the file system. We need to modify the user-data script to mount the EFS on boot:

- Install the NFS client (Amazon Linux AMI has amazon-efs-utils or needs nfs-utils, Ubuntu uses nfs-common) ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=2,the%20following%20script)).
- Create a mount directory (e.g., `/mnt/efs`).
- Mount the EFS using the EFS DNS name.

For example, in user-data:

```bash
# Install NFS client
yum install -y amazon-efs-utils  # or nfs-utils / apt-get install nfs-common on Ubuntu
# Create mount point
mkdir -p /mnt/efs
# Mount EFS (using DNS: file-system-id.efs.<region>.amazonaws.com)
mount -t nfs4 -o nfsvers=4.1 ${aws_efs_file_system.es_data.id}.efs.${var.aws_region}.amazonaws.com:/ /mnt/efs
```

This uses the EFS DNS naming convention to mount the file system ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=1,System%20using%20the%20following%20script)). If the security groups and mount targets are correctly set, the mount will succeed. We might also add an entry to `/etc/fstab` via user-data for persistence across reboots.

If we intend to use EFS for Elasticsearch data, we would configure `path.data: /mnt/efs` in `elasticsearch.yml` (instead of the default `/var/lib/elasticsearch`). This way, the data directory is on the NFS share. All nodes mounting the same share would technically see the same data files – which is **not a typical Elasticsearch setup** (normally each node has independent storage and ES handles replication). Use caution: sharing the live data directory across nodes can corrupt the cluster, so this is not recommended unless you know what you are doing. A safer use of EFS is to store daily snapshots or backups of indices.

Another use-case: if you expect to replace the entire cluster (e.g., during an upgrade) and want to retain data, you could snapshot to EFS or even shut down ES and copy the data directory to EFS, then have the new cluster read from it. However, again, this is advanced and not standard practice. Usually, one relies on Elasticsearch’s internal replication for persistence (so if one node dies, data is on another).

In summary, we included EFS because it was requested. It provides a persistent, network-accessible storage that outlives any single EC2. In our Terraform code, it's set up with proper security and ready to mount. The actual usage of it (for snapshots or for data) is up to your specific needs. Make sure to **allow NFS port 2049** in both the EFS’s SG and the instances’ SG as configured ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=1)), and then mounting is straightforward.

## 8. Monitoring & Management

To run this cluster in production, you’ll want monitoring and an upgrade strategy. We will incorporate:

- Installation of **Zabbix Agent** and **GBS Agents** on the instances for monitoring.
- A **rolling update** approach for changes (to avoid downtime when Terraform updates the ASG or launch template).

**Installing Monitoring Agents via Terraform**: We have two options to install additional software on our EC2 instances:

- Bake them into a custom AMI (not covered here).
- Use user-data or Terraform **provisioners** to install after launch.

We already utilize user-data for Elasticsearch. We can extend the user-data script to also install the Zabbix agent and any “GBS” agent (assuming GBS is another monitoring or logging agent specific to the environment). For example, user-data could `yum install -y zabbix-agent` and then configure its server IP and start it.

Alternatively, Terraform’s remote-exec provisioner can run commands on the instances after creation. Using a `null_resource` with `remote-exec` allows running scripts via SSH:

```hcl
resource "null_resource" "install_agents" {
  # Use triggers to re-run if instances change
  triggers = {
    cluster_id = aws_autoscaling_group.es_cluster.id
  }
  connection {
    type        = "ssh"
    host        = aws_autoscaling_group.es_cluster.instances[0].private_ip  # or use a proper lookup of instances' IPs
    user        = "ec2-user"  # username for the AMI (ec2-user for Amazon Linux, ubuntu for Ubuntu, etc.)
    private_key = file("~/.ssh/id_rsa")  # your SSH key for the key_pair used
  }
  provisioner "remote-exec" {
    inline = [
      "sudo yum install -y zabbix-agent",
      "sudo systemctl enable zabbix-agent && sudo systemctl start zabbix-agent",
      "sudo yum install -y gbs-agent",            # hypothetical package
      "sudo systemctl enable gbs-agent && sudo systemctl start gbs-agent"
    ]
  }
}
```

In this example, the `null_resource.install_agents` will execute after the ASG is created. We use a trigger (`cluster_id`) tied to the ASG, so if the ASG (or its instances) is replaced, this resource knows to run again. The remote connection uses SSH (make sure your key and security group allow this, as set up in Security & Access). The `remote-exec` then runs installation commands on the first instance. If you need to run on all instances, you might iterate or use a script that targets all instance IPs.

Using Terraform provisioners like this can be useful, but note:

- Terraform will consider the provisioner successful if the commands exit 0. If one instance out of 3 fails to install, Terraform might not detect it easily with this simple setup.
- Another approach: use a configuration management tool (Ansible, Chef, etc.) triggered outside Terraform, or as part of user-data (which runs on every instance individually).

Because we are writing a Terraform-centric guide, the above `null_resource` with `remote-exec` is one way to do it. It demonstrates how Terraform can perform post-creation tasks on remote machines ([Terraform Null Resource - What It is & How to Use It](https://spacelift.io/blog/terraform-null-resource#:~:text=,host%22)). In practice, installing monitoring agents via user-data may be simpler: you can include the commands in the same `user_data_es.sh` so that every instance installs them on boot (this ensures even new instances launched later by ASG will have the agents, without needing Terraform to run again).

For example, add to user-data:

```bash
# Install Zabbix Agent
yum install -y https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-agent.rpm
sed -i "s/Server=127.0.0.1/Server=<ZABBIX_SERVER_IP>/" /etc/zabbix/zabbix_agentd.conf
systemctl enable zabbix-agent && systemctl start zabbix-agent

# Install GBS Agent (assuming it's a downloadable binary or package)
# (commands to install and start GBS agent)
```

This ensures agents are up on every node. The method you choose (remote-exec vs user-data) can depend on your workflow. **Terraform best practice** is to use provisioners only as a last resort (since they introduce potential for partial failures). Where possible, user-data or pre-baked images are more predictable. For our advanced scenario, we showed the `null_resource` method as an example of how to run remote commands via Terraform if needed ([Terraform Null Resource - What It is & How to Use It](https://spacelift.io/blog/terraform-null-resource#:~:text=,host%22)).

**Rolling Updates with Zero Downtime**: When we update certain aspects of the cluster (like AMI ID for a new ES version, or changing instance type), Terraform will create a new launch template/config. By default, an Auto Scaling Group will not replace running instances just because the launch template changed. We need a strategy to replace instances gradually so the cluster updates without downtime.

There are a few tactics:

- **Terraform Lifecycle Hooks**: Using `create_before_destroy` on the launch configuration or ASG. We set `lifecycle { create_before_destroy = true }` on the launch configuration resource ([Manage AWS Auto Scaling Groups | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/aws/aws-asg#:~:text=traffic%20to%20all%20endpoints)), which ensures that when Terraform needs to make a new launch config (due to a change), it will create the new one _before_ destroying the old. The ASG resource will then be updated to point to the new launch config. However, simply changing the launch config for an ASG does not terminate instances; they will gradually replace on next scale events. You might have to explicitly cycle instances (e.g., detach and reattach instances, or do `terraform taint` on the ASG to force recreation of instances). Another way is to change the ASG's `desired_capacity` temporarily to trigger new instances.
- **Maximize uptime approach**: A common approach is a **blue-green or canary deployment**. You can stand up a second ASG (with the new config) alongside the old one, behind the same ELB (or a new ELB, then cut over). Because our Terraform already supports two ASGs (v2 and v8) via conditional logic, one could theoretically deploy a new cluster alongside the old by setting both to count=1 (if code is tweaked accordingly). Then you could migrate data or cut traffic over. This is complex with Elasticsearch due to data migration, but doable (snapshot and restore, or cross-cluster replication between old and new versions, etc).

- **ASG Rolling Update**: AWS Auto Scaling has features like adjusting `MaxSize` above current to launch new instances, then terminating old. You can do this manually: for example, if you want to upgrade the instance type, you could increment `desired_capacity` by 1 (with new launch config in place), wait for a new instance to come up and join cluster, then decrement by 1 to terminate an old instance. Repeat until all are replaced. This process can be orchestrated via scripts or even Terraform with careful apply steps (not purely automatic though).

Given our focus, we will use the Terraform lifecycle to avoid destroying resources before replacements are ready:

```hcl
resource "aws_launch_configuration" "es" {
  # ... (if using launch configuration instead of template)
  lifecycle {
    create_before_destroy = true
  }
}
```

HashiCorp documentation confirms that with `create_before_destroy`, Terraform will create the new launch config first and update the ASG to use it, **to avoid any service interruption** ([Manage AWS Auto Scaling Groups | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/aws/aws-asg#:~:text=traffic%20to%20all%20endpoints)). We used launch templates in our config, and launch templates are inherently versioned – we can achieve a similar effect by not specifying a fixed version (using `$Latest` so new version is used automatically). If using `aws_launch_template`, one strategy is to leave the `name` the same and rely on versioning, or use a new name each time with create_before_destroy (Terraform AWS provider added support for managing LT replacement with `create_before_destroy` on the resource as well).

**Lifecycle on ASG**: By default, Terraform will try to update the ASG in-place (which is fine for certain changes). If an in-place update is not possible, it will replace the ASG, which would tear down the instances by default. To prevent downtime, you might also put `create_before_destroy = true` on the ASG. However, AWS ASG has a limitation: you can’t have two ASGs with the same name, so Terraform would have to create new ASG with a different name (since we didn't specify name, Terraform can generate a new one with a different unique ID). That new ASG would launch new instances (which wouldn't immediately be in the old ELB unless we add them). This gets complicated, so it might be better to allow ASG to update in place, or manage the rolling externally as described.

In summary:

- Use `create_before_destroy` on immutable resources like Launch Configurations ([Manage AWS Auto Scaling Groups | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/aws/aws-asg#:~:text=traffic%20to%20all%20endpoints)) so that new ones come up before old are gone.
- Consider temporarily increasing ASG size or using blue-green technique for truly zero downtime if needed.
- Always plan and test the Terraform changes in a lower environment to see how it behaves (Terraform plan will show if it’s replacing or updating).

**Zabbix/Monitoring**: Ensure your Zabbix server is configured to monitor the new instances (update host IPs, etc., or use auto-registration if possible). The Zabbix agent will provide metrics on CPU, memory, etc. For Elasticsearch-specific monitoring, you might use X-Pack Monitoring, but since Zabbix integration was mentioned, you can use Zabbix templates for Elasticsearch ([Elasticsearch monitoring and integration with Zabbix](https://www.zabbix.com/integrations/elasticsearch#:~:text=Elasticsearch%20monitoring%20and%20integration%20with,both%20standalone%20and%20cluster%20instances)).

**GBS Agents**: Without specific info, assume they are some custom monitoring or log shipping agents. They should be installed and configured similarly to Zabbix. Ensure they have network connectivity to their collectors (open any necessary ports in security groups).

Finally, consider using Terraform to also set up CloudWatch alarms or event notifications (not requested, but as best practice, monitor EC2 metrics, EFS usage, etc., and alert on issues).

## 9. Outputs

We will define output values so that after `terraform apply`, we get important information like the load balancer endpoint. This makes it easy for users or automation pipelines to grab the connection info.

Relevant outputs to include:

- **Elasticsearch ELB DNS Name** – the internal URL to use for connecting to the cluster.
- Perhaps the **Elasticsearch cluster security group ID** (if someone needs to whitelist it elsewhere).
- If we generated an **Elastic password**, we might output it (but as sensitive).
- Possibly **EFS ID or mount point** (for reference).

Mainly, as requested, we output the ELB DNS:

```hcl
output "es_elb_dns" {
  description = "DNS name of the Elasticsearch load balancer"
  value       = aws_elb.es_elb.dns_name
}
```

If using count or for_each on the ELB, adjust the reference accordingly (e.g., `aws_elb.es_elb[0].dns_name`). In our single ELB case, it’s straightforward. For example, the Pelias Terraform script outputs the ELB DNS as a list (because they had `count` on it) ([terraform-elasticsearch/outputs.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/outputs.tf#:~:text=output%20)).

We can also output the Auto Scaling Group name or ARN, number of instances, etc., but those are less frequently needed. The ELB DNS is key because clients (like Kibana or application servers) will use it to connect (e.g., `http://internal-dev-es-xxxxx.elb.amazonaws.com:9200`). If using a friendly CNAME, you might output that as well.

Make sure to mark sensitive outputs as `sensitive = true` (for example, if outputting the `elastic` user password or any other secret). In our config, we actually avoided outputting the password and instead rely on retrieving from SSM when needed, which is more secure.

## 10. Best Practices & Deployment Tips

Finally, let's summarize some best practices that were applied (and some additional ones) when provisioning this kind of infrastructure with Terraform:

- **State Management**: Use a **remote backend** for Terraform state. Do not store state locally or in source control. For example, use an AWS S3 backend with DynamoDB table for state locking ([Setup Terraform S3 Backend With DynamoDB Locking (Guide)](https://devopscube.com/setup-terraform-remote-state-s3-dynamodb/#:~:text=match%20at%20L122%20We%20need,%28race%20conditions)), or use Terraform Cloud’s integrated backend. Remote state enables team collaboration and locking ensures no two runs conflict (preventing race conditions in provisioning) ([Setup Terraform S3 Backend With DynamoDB Locking (Guide)](https://devopscube.com/setup-terraform-remote-state-s3-dynamodb/#:~:text=match%20at%20L122%20We%20need,%28race%20conditions)). A DynamoDB state lock will prevent concurrent `terraform apply` from corrupting the state ([Setup Terraform S3 Backend With DynamoDB Locking (Guide)](https://devopscube.com/setup-terraform-remote-state-s3-dynamodb/#:~:text=Here%20is%20how%20DynamoDB%20state,locking%20works)). If using Terraform Cloud, it automatically handles state storage and locking for you.

- **Separate State per Environment**: Each environment (Dev, Staging, Prod) should have its own state file (or Terraform Cloud workspace). This prevents changes in one env from affecting another and keeps resources isolated. For example, if using S3 backend, have a unique `key` for each env (like `terraform-state-prod.tfstate`). If using Terraform Cloud, use workspaces (one per env) ([Automating Multi-Environment Deployments with Terraform Cloud ...](https://medium.com/hashicorp-engineering/automating-multi-environment-deployments-with-terraform-cloud-workspaces-6d9c7dcd2321#:~:text=Automating%20Multi,and%20permissions%20should%20match)). This way, you can deploy environments independently.

- **Consistent Configuration**: Use the same Terraform configuration for all environments by leveraging variables for differences ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=You%20do%20not%20want%20different,the%20only%20thing%20that%20changes)). This ensures dev/staging/prod are in sync with only scale or minor config differences. If there are major differences, consider using modules and composition (e.g., maybe Prod has a larger multi-cluster setup, in which case you could compose modules differently as needed) ([Best Practice for Reusing with many environments - Terraform - HashiCorp Discuss](https://discuss.hashicorp.com/t/best-practice-for-reusing-with-many-environments/2704#:~:text=,level%20infrastructure%20%E2%80%9Ccomponents%E2%80%9D%20in%20Terraform)).

- **Terraform Cloud/Enterprise**: If possible, use Terraform Cloud or Enterprise for running plans and applies. This gives a nice interface, team access control, and the ability to integrate with VCS for run triggers. Workspaces in Terraform Cloud can be linked to VCS branches for each environment, or you can use one workspace and multiple `.tfvars` with CLI-driven workflow. HashiCorp recommends one workspace per env per configuration for clarity and matching permission scopes ([Automating Multi-Environment Deployments with Terraform Cloud ...](https://medium.com/hashicorp-engineering/automating-multi-environment-deployments-with-terraform-cloud-workspaces-6d9c7dcd2321#:~:text=Automating%20Multi,and%20permissions%20should%20match)).

- **Use of Modules**: We structured the code with reusability in mind. Keep modules generic and loosely coupled. For example, a module to create an ASG of ES nodes could accept parameters to adjust instance count, type, and user-data script. Another module for ELB can be reused for other services too if designed generally. Encapsulating resource sets into modules makes your code easier to manage as it grows. It also allows testing modules in isolation (there are terraform module test frameworks) and using registries. In our guide, we mentioned splitting complex parts into nested modules (like separate sub-module for IAM policies if needed) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,their%20own%20IAM%20policy%20choices)). This kind of separation follows the single-responsibility principle for infrastructure code.

- **Documentation and Comments**: Document the variables and outputs with descriptions (we did so in variables). This is important as Terraform will auto-generate documentation for your module if you publish it. Also, leaving comments in the `main.tf` explaining why certain decisions were made (e.g., why a certain port is open, or why a resource has a lifecycle rule) can help future maintainers.

- **Plan and Review**: Always run `terraform plan` before apply, especially for production. In a team setting, use code reviews for Terraform changes. This helps catch mistakes like an unintended destroy of resources. Use Terraform Cloud’s plan output or pull request integrations to review changes.

- **Lifecycle and Prevent Destroy**: For critical resources like data stores, you might want to set `lifecycle { prevent_destroy = true }` to avoid accidental deletion. For example, the EFS or even the entire ASG could be marked prevent_destroy so that one has to manually confirm or taint to destroy it. This is a safeguard.

- **Terraform State Security**: The state file can contain sensitive data (like our random password). Encrypt the state at rest (S3 backend can encrypt with SSE, and if using Terraform Cloud, it is encrypted by default). Limit access to state only to infrastructure admins. We saw an example where the state was in an encrypted S3 bucket when storing secrets ([Using common Terraform to create SSM parameters for applications deployed to multiple accounts : r/Terraform](https://www.reddit.com/r/Terraform/comments/b3huqv/using_common_terraform_to_create_ssm_parameters/#:~:text=I%20randomly%20generate%20a%20password,the%20path%2C%20it%20stays%20there)). That’s a good practice.

- **Tagging**: Tag all resources with environment, project, and owner information. We included some tags (Name, Environment) in examples. Consistent tagging helps with cost allocation and management.

- **Testing**: Test the user-data scripts thoroughly (you can launch a single EC2 with the user-data in a dev account to verify it installs ES correctly). Also test the Terraform apply and destroy in a non-prod environment to ensure all dependencies are handled (for example, ensure that Terraform destroys the ELB last, after instances, to avoid it hanging onto instances; typically it does this automatically because the ASG will be destroyed which in turn deregisters instances, etc.).

- **Scaling and Performance**: If this cluster is for production, consider using multiple node types (dedicated master nodes, data nodes, ingest nodes). Terraform can be extended to create multiple ASGs for different roles. For brevity, we treated all as data nodes. Similarly, adjust the health check grace period and maybe use ELB health checks for ASG (`health_check_type = "ELB"`) if you want the ASG to use LB health. Also, tune ASG cooldown, etc., if using scaling policies.

- **Upgrading ES**: Going from 2.4.5 to 8.0.0 is a **huge** version leap (several major versions). In reality, you’d likely spin up a new cluster and reindex or restore snapshots. Our Terraform can create either, but migrating the data is another process. Always backup data (snapshots) before upgrading. You could automate snapshots via a scheduled Lambda or use Curator; Terraform could provision an S3 bucket for snapshots and an IAM policy to allow ES to write to it.

- **Terraform Code Maintenance**: Use a formatting and linting tool (like `terraform fmt` and `terraform validate`). Possibly store common values (like AMI IDs per region) in a Terraform map variable or use the AWS SSM public parameters to fetch AMI IDs by name (data source approach).

- **Terraform Versioning**: Keep the Terraform version and provider versions pinned in `versions.tf` to ensure consistency across deployments. For example:
  ```hcl
  terraform {
    required_version = ">= 1.3.0"
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 4.50"  # or latest known stable
      }
      random = {
        source = "hashicorp/random"
        version = "~> 3.0"
      }
    }
  }
  ```
  This ensures everyone uses compatible versions.

By following this guide, you have a robust Terraform configuration for an EC2-based Elasticsearch cluster with an ELB. It is parametrized for different environments and ES versions, uses secure practices for secrets, and is organized for maintainability. Remember that running Elasticsearch on EC2 (self-managed) requires ongoing care (monitoring, patching, scaling) which Terraform sets the stage for, but operational excellence will come from how you monitor and manage the cluster day-to-day. Good luck with your deployment!

**References:**

- HashiCorp Docs – Standard Terraform module structure ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,for%20variables%20and%20outputs%2C%20respectively)) ([Standard Module Structure | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/modules/develop/structure#:~:text=,their%20own%20IAM%20policy%20choices))
- HashiCorp Docs – Input variable validation (example of allowed values list) ([Terraform - How to restrict an input variable to a list of possible choices - Stack Overflow](https://stackoverflow.com/questions/57190035/terraform-how-to-restrict-an-input-variable-to-a-list-of-possible-choices#:~:text=variable%20,%3D%20string))
- Terraform best practices discussion – Using variables to differentiate environments, not separate code ([amazon web services - How to organize Terraform modules for multiple environments? - Stack Overflow](https://stackoverflow.com/questions/66024950/how-to-organize-terraform-modules-for-multiple-environments#:~:text=You%20do%20not%20want%20different,the%20only%20thing%20that%20changes))
- AWS Classic ELB Terraform config – Internal ELB with cross-zone LB and health checks ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=cross_zone_load_balancing%20%3D%20true)) ([terraform-elasticsearch/elb.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/elb.tf#:~:text=health_check%20))
- AWS Classic ELB listeners example – HTTP on 9200 and TCP on 9300 ([elasticsearch-ecs/terraform/elasticsearch/main.tf at master · firstlookmedia/elasticsearch-ecs · GitHub](https://github.com/firstlookmedia/elasticsearch-ecs/blob/master/terraform/elasticsearch/main.tf#:~:text=listener%20)) ([elasticsearch-ecs/terraform/elasticsearch/main.tf at master · firstlookmedia/elasticsearch-ecs · GitHub](https://github.com/firstlookmedia/elasticsearch-ecs/blob/master/terraform/elasticsearch/main.tf#:~:text=listener%20))
- Terraform discussion – Conditional resource creation with count (ternary example) ([amazon web services - Error aws_alb_target_group has "count" set, its attributes must be accessed on specific instances - Stack Overflow](https://stackoverflow.com/questions/62433708/error-aws-alb-target-group-has-count-set-its-attributes-must-be-accessed-on-s#:~:text=I%20understand,stated%20in%20my%20previous%20comment))
- Launch template root volume configuration (encryption and size) ([terraform: Set root device size using launch template](https://pet2cattle.com/2022/06/launch-template-root-device#:~:text=resource%20,demo_launch_tpl))
- AWS EFS setup and mounting (NFS security groups, mount command) ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=1)) ([Mount Up! A Step-by-Step Guide to Creating and Using Amazon EFS on Ubuntu - DEV Community](https://dev.to/techgirlkaydee/mount-up-a-step-by-step-guide-to-creating-and-using-amazon-efs-on-ubuntu-2i86#:~:text=1,System%20using%20the%20following%20script))
- Terraform null_resource with remote-exec (running commands on remote host) ([Terraform Null Resource - What It is & How to Use It](https://spacelift.io/blog/terraform-null-resource#:~:text=,host%22))
- HashiCorp Learn – Launch config create_before_destroy for zero-downtime updates ([Manage AWS Auto Scaling Groups | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/aws/aws-asg#:~:text=traffic%20to%20all%20endpoints))
- Reddit discussion – Generating password and storing in SSM (state in encrypted S3) ([Using common Terraform to create SSM parameters for applications deployed to multiple accounts : r/Terraform](https://www.reddit.com/r/Terraform/comments/b3huqv/using_common_terraform_to_create_ssm_parameters/#:~:text=I%20randomly%20generate%20a%20password,the%20path%2C%20it%20stays%20there))
- Terraform output example – ELB DNS name output ([terraform-elasticsearch/outputs.tf at master · pelias/terraform-elasticsearch · GitHub](https://github.com/pelias/terraform-elasticsearch/blob/master/outputs.tf#:~:text=output%20))
- AWS re:Post – Explanation of Terraform remote state and locking with DynamoDB ([Setup Terraform S3 Backend With DynamoDB Locking (Guide)](https://devopscube.com/setup-terraform-remote-state-s3-dynamodb/#:~:text=match%20at%20L122%20We%20need,%28race%20conditions))
