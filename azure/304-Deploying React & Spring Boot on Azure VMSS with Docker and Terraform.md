# Deploying React & Spring Boot on Azure VMSS with Docker and Terraform

## 1. Prerequisites

Before starting, ensure you have the following tools, accounts, and knowledge ready:

- **Azure Subscription & Account** – An active Azure account with a subscription. If you don’t have one, create a free Azure account ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=For%20this%20tutorial%2C%20you%20will,need)). You should have permissions to create resources (VMSS, networking, etc.).
- **Azure CLI** – Install the Azure CLI and log in (`az login`) to manage Azure resources from your machine ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=,CLI%20installed%20and%20authenticated%20locally)). This is useful for testing and managing infrastructure.
- **Terraform CLI (v1.4+)** – Install Terraform to define and provision Azure infrastructure as code ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=For%20this%20tutorial%2C%20you%20will,need)). Familiarity with basic Terraform workflow (init, plan, apply) is assumed.
- **Docker** – Install Docker to build container images for the React frontend and Spring Boot backend. Ensure Docker is running and you can push images to a registry.
- **Node.js and Build Tools** – Have Node.js (and npm/yarn) installed to build the React app. You’ll use it to compile the React app into a production bundle.
- **Java & Build Tools** – Install JDK (e.g., OpenJDK 17+) and a build tool (Maven or Gradle) to build the Spring Boot application into an executable JAR. This is needed if you aren’t using Docker multi-stage to build the JAR inside the image.
- **Azure Container Registry (ACR)** – Create an Azure Container Registry to store your Docker images (or be prepared to create one via Terraform/CLI). The ACR will be used by VMSS instances to pull the React and Spring Boot container images.
- **CI/CD Platform** – Access to a CI/CD service for automation. This guide will mention GitHub Actions and Azure DevOps Pipelines. You should have a GitHub account ([Deploy container instance by GitHub Actions - Azure Container Instances | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action#:~:text=%2A%20GitHub%20account%20,the%20deployment%2C%20which%20is%20used)) or an Azure DevOps organization ([Create a service connection and build and publish Docker images to Azure Container Registry - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/publish-to-acr?view=azure-devops#:~:text=Prerequisites)) set up for creating pipelines.
- **SSH Key (for VM access)** – Generate an SSH key pair for Linux (e.g., using `ssh-keygen`). The public key will be configured on the VMSS instances for admin access. This is needed if you want to SSH for troubleshooting.
- **Basic Knowledge** – Advanced developers should be comfortable with React, Spring Boot, Docker, and Azure concepts. An understanding of virtual networks, load balancers, and Linux server configuration is helpful. You should also be familiar with YAML (for CI/CD pipeline definitions) and JSON/HCL (for Terraform configurations).

**Note:** Ensure all local tools (Terraform, Azure CLI, Docker, Node, Maven) are logged in or configured as needed. For example, run `az account show` to confirm Azure CLI is authenticated to your subscription, and `docker login` to verify Docker can push to the target registry. This preparation avoids permission issues during automation.

## 2. Architecture Overview

Before diving into code, let's outline the high-level architecture of the deployment. The goal is to host a React frontend and a Spring Boot backend on Azure using Virtual Machine Scale Sets (VMSS), Docker containers, and Terraform-provisioned infrastructure. Below is an overview of how the components interact:

- **Azure Virtual Network & Subnets:** All resources reside in an Azure Virtual Network (VNet) with appropriate subnets. For example, you might have a subnet for the VM Scale Set and another for a database or other services (if any). In a simple setup, one subnet can host the VMSS instances and an Azure Load Balancer ([Azure Virtual Machines baseline architecture - Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/virtual-machines/baseline#:~:text=Azure%20Virtual%20Machines%20baseline%20architecture,and%20one%20for%20back%20end)).
- **Azure VM Scale Set (VMSS):** The VMSS is a group of identical virtual machines that can scale out/in. Each VM instance will run both the React app and the Spring Boot app in Docker containers. The VMSS ensures high availability and scalability by adding or removing VM instances based on load. Azure VM Scale Sets can automatically distribute traffic across instances using a load balancer ([Reliability in Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-virtual-machine-scale-sets#:~:text=With%20Azure%20Virtual%20Machine%20Scale,VM%20instance%20that%20you%20create)).
- **Docker Containers (React & Spring Boot):** On each VMSS instance (which is an Ubuntu Linux VM by default), Docker will run two containers:
  - _Frontend container:_ An Nginx server serving the compiled React app (static files). It listens on port 80 (HTTP) on the VM.
  - _Backend container:_ The Spring Boot application (packaged as a JAR and run with Java) listening on a port (e.g., 8080) inside the container. This will be accessible via an internal port on the VM. We will configure Nginx (or the Azure load balancer) to route API calls to this backend.
- **Azure Load Balancer:** An Azure Load Balancer (L4) will distribute incoming traffic across the VMSS instances. The load balancer will have a public front-end IP. In a simple configuration, it listens on port 80 (and 443 for HTTPS) and forwards requests to port 80 on the VM instances (which is served by the Nginx/React container) ([Azure Load Balancer](https://docs.swimlane.com/turbine_installer/embedded-cluster-install/infrastructure-examples/azure-load-balancer.htm#:~:text=Azure%20Load%20Balancer%20This%20topic,Architecture%20Diagram%20Load%20Balancer)). The React app in the browser will call the Spring Boot API via the same load balancer address (e.g., using relative `/api` paths or a known domain), and Nginx on the VM will proxy those calls to the Spring Boot container.
- **Azure Container Registry (ACR):** ACR stores the Docker images for both the React and Spring Boot applications. VMSS instances will pull the latest image from ACR during provisioning (using Docker). The registry can be secured so that only our Azure VMs (with proper credentials or identities) can pull images.
- **Terraform Infrastructure as Code:** Terraform scripts will automate the provisioning of all Azure resources – Resource Group, VNet, Subnets, Network Security Groups (firewall rules), Load Balancer (with backend pool and health probes), VM Scale Set (with a Linux base image and custom startup script to install Docker and run containers), and autoscale settings. Terraform ensures the infrastructure is consistent and reproducible across environments.
- **Networking & Security:** The VMSS instances will be in a subnet with controlled network access. A Network Security Group (NSG) will allow incoming traffic only on necessary ports (80/443 for web, and 22 for SSH if needed) and perhaps restrict other access. The Spring Boot container might not be exposed directly to the internet – it could be accessed only via the Nginx frontend or internally. The architecture can be adjusted to separate front-end and back-end onto different VMSS and use an internal load balancer for the backend, but for simplicity, this guide describes both running on the same VMSS instances ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=Good%20day,running%20on%20them%3F%20And%20if)).
- **Key Vault (Optional for Secrets):** Azure Key Vault can be used to store sensitive configuration, such as database credentials or API keys. In this architecture, if the Spring Boot app needs secrets, we can give the VMSS a Managed Identity and allow it to fetch those from Key Vault at runtime. This avoids putting secrets in code or in Terraform scripts.
- **Diagram:** _Conceptually, the flow is:_

  **User** (browser) ⟶ **Azure Load Balancer (VMSS Frontend IP)** ⟶ **VMSS Instance (Linux VM)** ⟶ **Nginx Container (serves React & proxies API)** ⟶ **Spring Boot Container (handles API requests)**.

  When load increases, **Auto-scaling** triggers the VMSS to launch additional VM instances (each with the same two containers), and the Load Balancer automatically includes them in traffic distribution. When load decreases, VMSS can scale in (terminate instances). All instances are identical by design (immutable infrastructure). This ensures high availability and scalability.

- **High-Level Interactions:**
  1. **User Access:** The user accesses the React application via a public IP or domain pointing to the Azure Load Balancer. The React app (HTML/JS/CSS) is delivered from the Nginx container on a VMSS instance.
  2. **Frontend to Backend Calls:** When the React app makes API calls (e.g., to fetch data), these calls go to the same load balancer (e.g., `https://myapp.example.com/api/...`). The load balancer forwards the request to one of the VMSS instances. On that VM, Nginx proxies the request to the Spring Boot container (e.g., forward `/api/*` to `http://localhost:8080/api/*`).
  3. **Backend Response:** The Spring Boot container processes the request (possibly interacting with a database or other services if applicable) and returns a response. Nginx then sends this response back to the user via the load balancer.
  4. **Scaling:** Azure Monitor watches metrics (CPU, RAM, etc.) on the VMSS. If CPU usage is high (for example), an autoscale rule triggers addition of a new VM instance ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=name%20%3D%20,)). Terraform will have set up these autoscaling rules. The new VM pulls the latest container images from ACR, joins the load balancer’s back-end pool, and starts serving traffic. Conversely, if usage drops, VMSS can remove instances (while ensuring a minimum count).
  5. **CI/CD Pipeline:** When developers push new code, the CI/CD pipeline builds new Docker images and pushes to ACR. We then trigger a rolling update of the VMSS (via Terraform or Azure CLI) to deploy the new image version (or use blue-green deployment strategy, described later).

This architecture provides a balance between control and simplicity. We use VMSS (IaaS) rather than a fully managed PaaS (like Azure App Service or Azure Spring Apps) to illustrate full control – from OS to container runtime – which suits advanced scenarios. The trade-off is that we manage more ourselves (Docker installation, OS updates, etc.), so we will implement automation and best practices to handle these.

## 3. Infrastructure as Code (IaC) with Terraform

Terraform will be used to provision and configure all Azure infrastructure for this deployment. Using IaC ensures that the environment can be recreated or modified in a controlled way, which is essential for advanced deployment scenarios. We will break down the Terraform setup into components:

### 3.1 Terraform Configuration for Azure Resources

**Terraform Project Structure:** Organize your Terraform files for clarity. For example, you might have: `providers.tf` (for Azure provider settings), `main.tf` (to call modules or include resource definitions), `network.tf` (VNet, Subnet, NSG, Load Balancer), `vmss.tf` (the VM Scale Set and associated compute resources), `outputs.tf` (to output important info like load balancer IP). This separation is logical as seen in a HashiCorp example ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=,for%20the%20scale%20set%20with)), where files are split by purpose (network, compute, etc.).

**Azure Provider:** Start by defining the Azure provider in Terraform, including the required version and features. For example:

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.64"  # use a recent version
    }
  }
}

provider "azurerm" {
  features {}  # enable AzureRM features
}
```

You should also ensure Azure authentication for Terraform. If running locally, `az login` (via Azure CLI) or setting `ARM_CLIENT_ID`, etc., for a service principal works. Terraform can reuse Azure CLI creds by default.

**Resource Group:** Define an Azure Resource Group to contain all resources:

```hcl
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name   # e.g., "rg-myapp-prod"
  location = var.azure_region          # e.g., "East US"
}
```

Variables like `resource_group_name` and `azure_region` can be defined in a `variables.tf` or passed in via a Terraform tfvars file or CI pipeline.

### 3.2 Networking and Load Balancing with Terraform

A secure network is crucial. We will use Terraform to set up a virtual network, subnet, security group, and an Internet-facing load balancer:

- **Virtual Network & Subnet:** Create an Azure Virtual Network and a Subnet for the VM scale set instances. For example:

  ```hcl
  resource "azurerm_virtual_network" "vnet" {
    name                = "myapp-vnet"
    address_space       = ["10.0.0.0/16"]
    location            = azurerm_resource_group.rg.location
    resource_group_name = azurerm_resource_group.rg.name
  }

  resource "azurerm_subnet" "subnet" {
    name                 = "vmss-subnet"
    resource_group_name  = azurerm_resource_group.rg.name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes     = ["10.0.1.0/24"]
  }
  ```

  This defines a VNet with IP range 10.0.0.0/16 and a subnet 10.0.1.0/24 for our VMSS.

- **Network Security Group (NSG):** Define an NSG to allow web and SSH traffic and deny other unwanted access. For example:

  ```hcl
  resource "azurerm_network_security_group" "vmss_nsg" {
    name                = "vmss-nsg"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location

    security_rule {
      name                       = "Allow-HTTP"
      priority                   = 100
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "80"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
    security_rule {
      name                       = "Allow-HTTPS"
      priority                   = 110
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "443"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
    security_rule {
      name                       = "Allow-SSH"
      priority                   = 120
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_prefix         = "*"
      destination_port_range     = "22"
      source_address_prefix      = "*"       # Consider restricting to your IP for security
      destination_address_prefix = "*"
    }
    # ... (default deny rules are implicit at lower priority)
  }
  ```

  Attach the NSG to the VMSS subnet:

  ```hcl
  resource "azurerm_subnet_network_security_group_association" "subnet_nsg_assoc" {
    subnet_id                 = azurerm_subnet.subnet.id
    network_security_group_id = azurerm_network_security_group.vmss_nsg.id
  }
  ```

- **Public Load Balancer:** Create a public IP and a Load Balancer to distribute traffic to the VMSS:

  ```hcl
  resource "azurerm_public_ip" "lb_ip" {
    name                = "vmss-lb-ip"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    allocation_method   = "Static"
    sku                 = "Standard"
  }

  resource "azurerm_lb" "lb" {
    name                = "vmss-lb"
    location            = azurerm_resource_group.rg.location
    resource_group_name = azurerm_resource_group.rg.name
    sku                 = "Standard"
    frontend_ip_configuration {
      name                 = "PublicFrontEnd"
      public_ip_address_id = azurerm_public_ip.lb_ip.id
    }
  }
  ```

  Next, define a **Backend Address Pool** and **Health Probe** for the LB:

  ```hcl
  resource "azurerm_lb_backend_address_pool" "lb_pool" {
    name                = "vmss-backend-pool"
    loadbalancer_id     = azurerm_lb.lb.id
    resource_group_name = azurerm_resource_group.rg.name
  }

  resource "azurerm_lb_probe" "lb_probe" {
    name                = "http-probe"
    resource_group_name = azurerm_resource_group.rg.name
    loadbalancer_id     = azurerm_lb.lb.id
    protocol            = "Tcp"
    port                = 80
    interval_in_seconds = 15
    number_of_probes    = 4
  }
  ```

  This probe will periodically check port 80 on the VMs (Nginx) to see if the instance is healthy.

  Then, create a **Load Balancer Rule** to forward traffic:

  ```hcl
  resource "azurerm_lb_rule" "lb_rule_web" {
    name                           = "http-rule"
    resource_group_name            = azurerm_resource_group.rg.name
    loadbalancer_id                = azurerm_lb.lb.id
    protocol                       = "Tcp"
    frontend_port                  = 80
    backend_port                   = 80
    frontend_ip_configuration_name = azurerm_lb.lb.frontend_ip_configuration[0].name
    backend_address_pool_id        = azurerm_lb_backend_address_pool.lb_pool.id
    probe_id                       = azurerm_lb_probe.lb_probe.id
  }
  ```

  This rule ties everything together: any HTTP request coming to the LB's public IP on port 80 gets distributed to one of the VMSS VM's on port 80 (where Nginx is listening). We would create a similar rule for HTTPS (443) if we plan to terminate SSL on the VM (or we might terminate SSL at the LB using an Application Gateway – discussed in Security/TLS section).

**Attach Load Balancer to VMSS:** We will configure the VM Scale Set to use this load balancer's backend pool and probe when we define the VMSS resource.

### 3.3 Provisioning the VM Scale Set (VMSS) with Terraform

The VM Scale Set resource definition is the core of our deployment. We will use a Linux VMSS and cloud-init (custom data) to install Docker and run containers on each instance. Key points in the VMSS Terraform configuration:

- **VMSS Resource**: Use the `azurerm_linux_virtual_machine_scale_set` resource (or the newer `azurerm_linux_virtual_machine_scale_set` if using AzureRM 3.x). For example:

  ```hcl
  resource "azurerm_linux_virtual_machine_scale_set" "app_vmss" {
    name                = "vmss-myapp"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    sku                 = "Standard_B2s"               # VM size (choose based on load)
    instances           = 2                            # start with 2 instances
    admin_username      = "azureuser"
    admin_ssh_key {
      username   = "azureuser"
      public_key = file("~/.ssh/id_rsa.pub")           # path to your SSH public key
    }

    source_image_reference {
      publisher = "Canonical"
      offer     = "UbuntuServer"
      sku       = "18.04-LTS"
      version   = "latest"
    }
    upgrade_mode = "Automatic"  # enable rolling upgrades automatically when model changes
  ```

  The above sets up a scale set named "vmss-myapp" with 2 instances of Ubuntu 18.04, size B2s (2 vCPU, 4 GB RAM). It also configures the admin user and SSH key for access. We set `upgrade_mode = "Automatic"` so that if we update the VMSS model (for example, new custom data or config via Terraform), Azure will automatically perform a rolling update of VMs ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=If%20the%20extensions%20associated%20with,updated%2C%20are%20existing%20VMs%20affected)).

- **Bootstrapping with Custom Data (Cloud-Init)**: We need each VM to automatically install Docker and run our containers on startup. We can achieve this with **cloud-init** by supplying a custom script via the `custom_data` or `user_data` property. Terraform allows specifying a script which will be passed to the Azure VM instance. In our case, we'll use a Bash script to install Docker and start the containers. We base this script on Azure guidance ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=Your%20script%20should%20incorporate%20the,following%20commands)) ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=docker%20login%20%3Cyour,password)):

  ```bash
  #cloud-config
  runcmd:
    - sudo apt-get update
    - sudo apt-get install -y docker.io
    - sudo systemctl start docker
    - sudo systemctl enable docker
    - sudo docker login <MY_ACR>.azurecr.io -u <ACR_USERNAME> -p <ACR_PASSWORD>
    - sudo docker pull <MY_ACR>.azurecr.io/my-react-app:latest
    - sudo docker pull <MY_ACR>.azurecr.io/my-springboot-app:latest
    - sudo docker run -d --restart always -p 80:80 --name web <MY_ACR>.azurecr.io/my-react-app:latest
    - sudo docker run -d --restart always -p 8080:8080 --name api <MY_ACR>.azurecr.io/my-springboot-app:latest
  ```

  A few notes on this script: It updates apt, installs Docker, and ensures Docker starts on boot ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=apt)). Then it logs into ACR (substitute your ACR login server, and credentials – we will address securing these in the Security section; ideally you use a managed identity instead of plaintext password). It pulls the latest images for the React and Spring Boot apps. Finally, it runs the containers:

  - React container is run on port 80 of the host (`-p 80:80`) so that it serves HTTP traffic directly. We name it "web".
  - Spring Boot container is run on port 8080 of the host (`-p 8080:8080`) and named "api".
    Both use `--restart always` to ensure they restart if the VM reboots or if the container crashes.

  We will embed this script into Terraform. One approach is to put the shell script in a separate file (e.g., `cloud-init.yaml` or `init-script.sh`) and then use Terraform's `file()` function and `base64encode()` to pass it as custom data. Example:

  ```hcl
  resource "azurerm_linux_virtual_machine_scale_set" "app_vmss" {
    # ... (as above)
    custom_data = base64encode(file("${path.module}/cloud-init.yaml"))
    # ...
    os_disk {
      caching              = "ReadWrite"
      storage_account_type = "Standard_LRS"
    }
    # Networking config to attach to VNet:
    network_interface {
      name    = "vmss-nic"
      primary = true

      ip_configuration {
        name      = "vmss-ipconfig"
        subnet_id = azurerm_subnet.subnet.id
        load_balancer_backend_address_pools_ids = [azurerm_lb_backend_address_pool.lb_pool.id]
        primary   = true
      }
    }
  }
  ```

  The `custom_data` field takes a base64-encoded string of the script (cloud-init will execute it on boot). We attach the VMSS NIC to our subnet and the load balancer’s backend pool ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=How%20do%20I%20do%20a,same%20subscription%20and%20same%20region)). This means all VM instances automatically register with the LB.

  **Important:** In the script above, placeholders like `<ACR_USERNAME>` and `<ACR_PASSWORD>` should be replaced securely. You can pass these via Terraform variables (from a secure source) or, better, use a **Managed Identity** for the VMSS with the `AcrPull` role on your ACR. Using a managed identity means you can use Azure CLI on the VM to get an ACR token, or enable the [ACR authentication with managed identity](https://learn.microsoft.com/azure/container-registry/container-registry-authentication-managed-identity). To keep things simple, this guide uses a direct login in the script, but **in production it is recommended to avoid plain credentials** (see Security section for Key Vault usage).

- **Autoscaling Configuration:** With Terraform, you can define an `azurerm_monitor_autoscale_setting` resource to automate scale in/out. For instance:

  ```hcl
  resource "azurerm_monitor_autoscale_setting" "autoscale" {
    name                = "vmss-autoscale"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    target_resource_id  = azurerm_linux_virtual_machine_scale_set.app_vmss.id

    profile {
      name = "autoscale-profile"
      capacity {
        minimum = 2
        default = 2
        maximum = 10
      }
      rule {
        metric_trigger {
          metric_name        = "Percentage CPU"
          metric_resource_id = azurerm_linux_virtual_machine_scale_set.app_vmss.id
          time_grain         = "PT1M"
          statistic          = "Average"
          time_window        = "PT5M"
          time_aggregation   = "Average"
          operator           = "GreaterThan"
          threshold          = 75
        }
        scale_action {
          direction = "Increase"
          type      = "ChangeCount"
          value     = 2
          cooldown  = "PT5M"
        }
      }
      rule {
        metric_trigger {
          metric_name        = "Percentage CPU"
          metric_resource_id = azurerm_linux_virtual_machine_scale_set.app_vmss.id
          time_grain         = "PT1M"
          statistic          = "Average"
          time_window        = "PT5M"
          time_aggregation   = "Average"
          operator           = "LessThan"
          threshold          = 30
        }
        scale_action {
          direction = "Decrease"
          type      = "ChangeCount"
          value     = 1
          cooldown  = "PT10M"
        }
      }
    }
  }
  ```

  In this example, the scale set will have a minimum of 2 instances and can grow to 10. One rule says: if average CPU > 75% for 5 minutes, add 2 instances ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=name%20%3D%20,)). The other says: if average CPU < 30% for 5 minutes, remove 1 instance (down to min 2). The `cooldown` periods prevent thrashing. You can adjust these thresholds and instance counts based on your app's behavior. Azure will use the VMSS's built-in metrics (like CPU) for these rules. The autoscale setting is associated with our VMSS by `target_resource_id`.

- **Outputs:** After applying Terraform, you’d want to output useful information, e.g., the public IP of the load balancer to access the app. For example, in `outputs.tf`:
  ```hcl
  output "lb_ip_address" {
    value = azurerm_public_ip.lb_ip.ip_address
  }
  ```
  Terraform will then display the IP (or you can create a DNS name for it via Azure DNS or Front Door).

**Terraform Apply:** Once you have these configurations, run `terraform init`, `terraform plan`, and `terraform apply`. Terraform will provision the VNet, NSG, LB, VMSS, etc. After a few minutes, you should have the infrastructure up: the VMSS instances will execute the cloud-init script on boot. You can verify on Azure Portal or using Azure CLI (`az vmss list-instances`) that instances are running. The load balancer’s IP (from output) should respond to HTTP requests – you can test it in a browser (you should see the React app) and test the API (perhaps via the browser console or a tool like curl) to ensure the Spring Boot service is reachable (e.g., `http://<LB_IP>/api/hello` returns expected JSON).

### 3.4 Terraform Modules and Automation

For maintainability, consider using or creating Terraform modules:

- **Using Existing Modules:** The Terraform community and Azure team provide modules for common patterns. For example, the Azure Terraform modules for network and VMSS can simplify configuration. The module `Azure/terraform-azurerm-vmss-cloudinit` on GitHub is specifically designed to deploy a VM Scale Set with a cloud-init script ([GitHub - Azure/terraform-azurerm-vmss-cloudinit: Terraform AzureRM module registry to create a VM Scaleset initialized via cloud-init scripts](https://github.com/Azure/terraform-azurerm-vmss-cloudinit#:~:text=This%20Terraform%20module%20deploys%20a,the%20VM%20scale%20set%20deployed)). It expects you to supply network and LB configurations (which we did above) and handles VMSS creation with your custom cloud-init. Using such a module can reduce code duplication. Similarly, there are modules for Azure network (vnet and subnets) and load balancer. Modules can be called in your `main.tf` with appropriate variables. For instance:

  ```hcl
  module "network" {
    source              = "Azure/network/azurerm"
    resource_group_name = azurerm_resource_group.rg.name
    # ... (other vnet settings)
  }

  module "vmss" {
    source              = "Azure/vmss-cloudinit/azurerm"
    resource_group_name = azurerm_resource_group.rg.name
    vm_os_simple        = "UbuntuServer"
    instances           = 2
    vm_size             = "Standard_B2s"
    admin_username      = "azureuser"
    authentication_type = "SSH"
    admin_ssh_key = <<EOF
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD...
  EOF
    custom_data = file("${path.module}/cloud-init.yaml")
    subnet_id   = module.network.subnet_id
    backend_address_pool_id = azurerm_lb_backend_address_pool.lb_pool.id
    # ... (other variables like application name, etc.)
  }
  ```

  This is just an illustrative snippet; the actual module variable names may differ. The idea is that the module encapsulates the VMSS creation logic, while you supply parameters (VM size, image, SSH keys, custom data script, network attachments). The module then returns outputs like the VMSS resource ID, etc., which you can use to configure autoscaling or other resources.

- **Creating Custom Modules:** If you have multiple environments (dev, staging, prod) or plan to reuse this setup, consider structuring your Terraform as reusable modules. For example, create a module for “docker-vmss-app” which takes inputs (app name, image names, etc.) and provisions the whole stack (maybe including LB). Then each environment’s configuration can call this module with different parameters (like scaling limits or instance counts). This promotes consistency across environments and easier changes. A Terraform root module can orchestrate multiple modules (for example, a module for network shared by other components, a module for the app VMSS, etc.).

- **Remote State:** Since this is an advanced guide, remember to store your Terraform state securely (e.g., in Azure Storage backend or Terraform Cloud) if working in a team or for production. This avoids state loss and allows CI pipelines to run terraform commands safely.

Terraform will significantly automate the infrastructure provisioning. With this in place, the next steps involve creating and deploying the application containers themselves.

## 4. Containerization of React and Spring Boot Apps

Containerizing the applications ensures that they run the same way on any environment (your local machine, Azure VMSS, etc.) and encapsulates all dependencies. We will create Docker images for both the React frontend and the Spring Boot backend. We will also apply best practices like multi-stage builds for optimization and secure handling of environment variables.

### 4.1 Dockerizing the React Frontend

The React application is a single-page app (SPA) that, in production, can be served as static files. We can use **multi-stage Docker builds** to create a lightweight image for the React app:

**Dockerfile for React (Multi-stage build with Nginx):**

```dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
# Copy a custom nginx.conf if you need to configure proxies
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

In this Dockerfile:

- We use a Node.js 18 Alpine image to install dependencies and build the app (`npm run build` produces a production-ready static bundle in `build/` directory) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Build%20Stage%20FROM%20node%3A18,RUN%20npm%20run%20build)).
- In the second stage, we use a small Nginx Alpine image. We copy the build artifacts from the first stage into Nginx's web root (`/usr/share/nginx/html`). We then instruct Nginx to run in the foreground (the default command). Port 80 is exposed for HTTP traffic ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Production%20Stage%20FROM%20nginx%3Astable,g%22%2C%20%22daemon%20off)).
- The resulting image contains only Nginx and the static files – Node and the source code do not exist in the final image, reducing size and attack surface. This multi-stage build minimizes the image size by ~80% compared to a dev image ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Production%20Dockerfile%20with%20multi,build)).
- (Optional) If the React app needs to proxy API calls to the backend, you can include a custom `nginx.conf` in the image that defines a proxy pass. For example, configure Nginx to forward requests from `/api/*` to `http://localhost:8080/api/*` (the Spring Boot container). Ensure the Docker network or host allows this communication (in our VMSS, both containers share the host network so `localhost:8080` on the VM will reach the Spring Boot container since we published port 8080 to the host).

**Building the React Image:** You can build and test the image locally:

```bash
docker build -t myacr.azurecr.io/my-react-app:latest .
docker run -p 80:80 myacr.azurecr.io/my-react-app:latest
```

Then visit http://localhost (or appropriate IP) to verify the app loads. This image will be pushed to Azure Container Registry via CI/CD.

### 4.2 Dockerizing the Spring Boot Backend

We will containerize the Spring Boot application (which is a Java app). There are a few ways to do this. We’ll show a Dockerfile approach, again using multi-stage build to optimize the final image size:

**Dockerfile for Spring Boot (Multi-stage):**

```dockerfile
# Stage 1: Build the JAR
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Run the Spring Boot app
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
# Use a non-root user for security
RUN adduser --disabled-password --gecos '' springuser && chown -R springuser /app
USER springuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

Explanation:

- **Stage 1 (Builder):** We use a Maven image with JDK 17 to compile the application. We copy the Maven `pom.xml` and `src` code and run `mvn package` to produce the fat JAR. (If you use Gradle, a similar approach with a Gradle image can be used.)
- **Stage 2 (Runtime):** We use an official OpenJDK runtime-only image (Eclipse Temurin JRE 17 on Alpine or Ubuntu Jammy). This image is much smaller as it only has the JRE (no compiler). We copy the JAR built in the previous stage into this image. We create a non-root user `springuser` and run the app under that user for better security (so the process isn’t running as root inside the container) ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=FROM%20openjdk%3A8,jar%22%2C%22%2Fapp.jar)). We expose port 8080 and set the entrypoint to run the JAR with Java.

This multi-stage build avoids needing to pre-build the JAR outside and ensures our final container has only the necessary runtime and the JAR ([9 Tips for Containerizing Your Spring Boot Code | Docker](https://www.docker.com/blog/9-tips-for-containerizing-your-spring-boot-code/#:~:text=FROM%20eclipse,jar%26amp%3Bquot%3B%2C%20%26amp%3Bquot%3B%2Fapp.jar%26amp%3Bquot)) ([9 Tips for Containerizing Your Spring Boot Code | Docker](https://www.docker.com/blog/9-tips-for-containerizing-your-spring-boot-code/#:~:text=One%20key%20drawback%20of%20our,to%20be%20a%20better%20way)). The image will be smaller and more secure (since it doesn't include Maven, source code, or the JDK). As the Docker official docs note, separating build and runtime stages significantly reduces image size and attack surface ([Multi-stage builds | Docker Docs
](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/#:~:text=previous%20stage)) ([Multi-stage builds | Docker Docs
](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/#:~:text=,for%20starting%20your%20application)).

**Building the Spring Boot Image:**

```bash
docker build -t myacr.azurecr.io/my-springboot-app:latest .
docker run -p 8080:8080 myacr.azurecr.io/my-springboot-app:latest
```

Test that it starts properly. You might want to add `HEALTHCHECK` in the Dockerfile or rely on the Azure LB probe to know if the app is up. When running locally, you can curl `http://localhost:8080/actuator/health` (if Actuator is on) or an endpoint to see if it responds.

**Externalized Configuration:** Spring Boot typically reads config from `application.properties` or environment variables. In containers, you’ll likely supply config via environment variables (e.g., `SPRING_DATASOURCE_URL`, etc.). You can define these in your Docker run command or Docker Compose. For our purposes, any required env vars (like backend URLs, database creds) will be injected via the VMSS startup script or a config file mounted. Ensure that sensitive values are not baked into the image and can be overridden.

### 4.3 Managing Environment Variables Securely

Both React and Spring Boot apps might need environment-specific configurations:

- The React app might need to know the base URL of the API (if not using relative paths). Often, you can build that into the React bundle via an environment variable at build time (e.g., `REACT_APP_API_URL`). If you need runtime configuration, you’d have to fetch config via an API or inject a config file; SPAs are usually built with the needed config.
- The Spring Boot app might need database credentials, API keys, etc., as environment variables (or mounted secrets).

**Security Best Practice:** _Avoid putting secrets in Dockerfiles or images._ Do **not** hard-code passwords or keys in the Dockerfile. Instead, use environment variables at runtime or Docker secrets. The Docker documentation advises caution: _"Be cautious about including sensitive data in environment variables. Consider using Secrets for managing sensitive information."_ ([Best practices | Docker Docs
](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/#:~:text=)). In our context, using Azure Key Vault or Azure DevOps pipeline secrets to inject values is recommended.

For local development, you might use a `.env` file (which you do **not** commit to source control) and Docker Compose to load it. For the Azure VMSS, we can supply environment variables in the startup script or use Azure Key Vault + Managed Identities to fetch them at runtime (discussed in Security section).

**Example:** To pass a database URL and credential to Spring Boot container, you could modify the docker run command:

```bash
sudo docker run -d --restart always -p 8080:8080 --name api \
  -e SPRING_DATASOURCE_URL=${DB_URL} \
  -e SPRING_DATASOURCE_USERNAME=${DB_USER} \
  -e SPRING_DATASOURCE_PASSWORD=${DB_PASS} \
  myacr.azurecr.io/my-springboot-app:latest
```

In Terraform, you could embed those `-e` options in the cloud-init script, pulling the values from Key Vault or Terraform variables (ensuring they are not exposed in logs). If using Key Vault, a strategy is: VMSS managed identity → Key Vault to fetch secret → inject into an env file or directly run the docker command with the secret value.

We’ll revisit secret management, but the key point is to **manage environment variables securely and inject them at runtime, not build time, for secrets**.

### 4.4 Verifying Container Behavior

It’s good practice to test your containers thoroughly **before** deploying:

- Run the two containers together to ensure they can communicate. You can use Docker Compose for a quick local test, with a simple `docker-compose.yml` that starts both and links them via a network.
- Example `docker-compose.yml` (for local test only):

  ```yaml
  version: "3"
  services:
    api:
      image: myacr.azurecr.io/my-springboot-app:latest
      ports:
        - "8080:8080"
    web:
      image: myacr.azurecr.io/my-react-app:latest
      ports:
        - "80:80"
      depends_on:
        - api
      environment:
        - REACT_APP_API_URL=http://localhost:8080 # if your React app uses this
  ```

  This ensures that if the React app is trying to call `localhost:8080`, it will reach the Spring Boot service.

- Check that the React app successfully calls the API and that the API is serving the expected data.

Once images are working, they should be pushed to ACR so that the VMSS (in Azure) can pull them. That push will be done through our CI/CD pipeline.

## 5. CI/CD Integration

With our code containerized, we want an automated way to build and deploy these containers and update our infrastructure. CI/CD will help in continuously integrating changes and deploying them to Azure. We’ll cover two approaches: **GitHub Actions** and **Azure DevOps Pipelines**, since both are common. The goal of the pipeline will be to:

- Build the React and Spring Boot Docker images (perhaps in parallel).
- Run tests (if any) during the build.
- Push the images to Azure Container Registry (ACR).
- Apply Terraform changes (if using GitOps to update infrastructure) or trigger a VMSS rolling upgrade.

### 5.1 Automating Builds and Push with GitHub Actions

**GitHub Actions** can be used to build and push Docker images to ACR whenever code is pushed to your repository (for example, on a push to the `main` or a release branch). You'll need to create an ACR credentials secret in your GitHub repo (or use Azure login action with OpenID Connect for passwordless auth).

A sample GitHub Actions workflow (`.github/workflows/build-and-deploy.yml`):

```yaml
name: CI-CD Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Azure Cloud auth
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          enable-AzPSSession: false

      - name: Azure Container Registry Login
        uses: azure/docker-login@v1
        with:
          login-server: myappacr.azurecr.io
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build and Push React Image
        uses: docker/build-push-action@v4
        with:
          context: ./react-app
          file: ./react-app/Dockerfile
          push: true
          tags: myappacr.azurecr.io/my-react-app:latest

      - name: Build and Push Spring Boot Image
        uses: docker/build-push-action@v4
        with:
          context: ./springboot-app
          file: ./springboot-app/Dockerfile
          push: true
          tags: myappacr.azurecr.io/my-springboot-app:latest
```

Explanation:

- We trigger on push to main (you might have different triggers or manual triggers for deployment).
- The job checks out the repository code.
- `azure/login@v1` uses a service principal (stored in `AZURE_CREDENTIALS` secret) to authenticate to Azure ([Deploy container instance by GitHub Actions - Azure - Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action#:~:text=...%20uses%3A%20azure%2Fdocker,password)). This could be replaced by OIDC federation to Azure if desired (eliminating the need for storing credentials).
- `azure/docker-login@v1` logs into ACR using the admin credentials or a service principal with ACR permissions ([Push a Docker image to Azure Container Registry using a GitHub ...](https://stuartmccoll.github.io/posts/2022-06-11-github-action-to-azure-container-registry/#:~:text=Push%20a%20Docker%20image%20to,server%3A%20%24%7B%7B%20secrets.ACR_REGISTRY_NAME%20%7D%7D.azurecr.io)). We provide the ACR server, username, and password from secrets. After this, the `docker` CLI is authenticated with ACR.
- We use Docker Buildx action (`docker/build-push-action@v4`) to build and push images in one step. We specify the Dockerfile path and tag with the ACR repository name. This action will build the image and push it to ACR because `push: true` is set. We do this for both frontend and backend. These steps run in parallel by default (since no dependency specified), but you can also run them sequentially if needed.

After this job, our images in ACR are updated. Now, we need to deploy the new images to our VMSS. If we have Terraform scripts in the repo, we could automate Terraform apply as well (ensuring the new image tag is used, if using version tags). However, since we used the `latest` tag in this example, our VMSS instances, when recreated or newly scaled, would pull the updated latest image. But running containers won't update automatically just because a new image is in ACR – we need to trigger a redeployment for the running VMs.

**Deploying to VMSS via Rolling Update:** One approach is to use the Azure CLI or Terraform to update the VMSS model (e.g., change a dummy property or update custom_data) which will cause Azure to roll the upgrade (because `upgrade_mode` is Automatic). Alternatively, use the Azure CLI `az vmss update-instances` or `az vmss rolling-upgrade` commands to redeploy. A simpler method is to treat the VMSS as immutable and create a new VMSS (blue-green) – but that's more complex and often unnecessary for containers.

For automation, consider adding a step in GitHub Actions to run Terraform (if the new image tag/version is managed via Terraform variables) or using Azure CLI:

```yaml
- name: Trigger VMSS Rolling Update
  run: az vmss restart --resource-group <RG> --name vmss-myapp --instance-ids "*"
```

This would restart all instances in the scale set, causing them to pull the latest image on startup (since our docker run in cloud-init used `--restart=always`, a reboot will restart the containers, and if `latest` tag was updated and no image cache policy is set, Docker will still use the cached image unless we enforce pull). We might instead do `docker pull` periodically or use version tags.

A more controlled way: incorporate the image version/tag as an input to the VMSS via Terraform. For example, store the image tag in an Azure DevOps variable group or Terraform Cloud variable, update it each deployment and run Terraform apply to set a new custom_data (script) that uses that tag. This way, Azure VMSS sees a model change and rolls out new VMs with the new image.

Due to complexity, many teams opt for Azure Kubernetes Service (AKS) for easier rolling updates of containers. But it’s doable with VMSS: either via script or re-imaging.

For brevity, assume using `latest` and a manual VMSS roll update.

### 5.2 Automating with Azure DevOps Pipelines

If using **Azure DevOps**, you’d create a similar pipeline. Azure DevOps offers tasks like **Docker@2** to build and push images, and integrates with Azure subscriptions and service connections.

A snippet of an Azure DevOps pipeline (YAML):

```yaml
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

variables:
  ACR_NAME: "myappacr"
  IMAGE_TAG: "latest"

steps:
  - task: AzureCLI@2
    inputs:
      azureSubscription: "MyAzureServiceConnection"
      scriptType: "bash"
      scriptLocation: "inlineScript"
      inlineScript: |
        az acr login --name $(ACR_NAME)

  - task: Docker@2
    displayName: Build and publish frontend image
    inputs:
      command: buildAndPush
      repository: $(ACR_NAME).azurecr.io/my-react-app
      dockerfile: react-app/Dockerfile
      tags: $(IMAGE_TAG)
      containerRegistry: "MyACRServiceConnection" # A service connection for ACR

  - task: Docker@2
    displayName: Build and publish backend image
    inputs:
      command: buildAndPush
      repository: $(ACR_NAME).azurecr.io/my-springboot-app
      dockerfile: springboot-app/Dockerfile
      tags: $(IMAGE_TAG)
      containerRegistry: "MyACRServiceConnection"
```

Here:

- We use an Azure service connection for ACR (or Azure subscription). Azure DevOps can also use the ACR's admin account or a service principal.
- The `Docker@2` tasks with `buildAndPush` will do similar to above: build the images and push to ACR in one step ([Create a service connection and build and publish Docker images to Azure Container Registry - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/publish-to-acr?view=azure-devops#:~:text=,%24%28tag)).
- We could add another step using an Azure CLI task or an Azure PowerShell task to initiate a VMSS rolling upgrade or update. For example:

  ```yaml
  - task: AzureCLI@2
    inputs:
      azureSubscription: "MyAzureServiceConnection"
      scriptType: bash
      scriptLocation: inlineScript
      inlineScript: |
        az vmss rolling-upgrade start --resource-group <RG> --name vmss-myapp
  ```

  This triggers the VMSS to start a rolling upgrade of all instances to the latest model. If nothing in the model changed, this might not do anything unless automatic OS image upgrade is configured. A sure way is `az vmss update-instances --instance-ids *` as mentioned, to force restart.

- We could also have Terraform in Azure DevOps. For instance, use tasks: `TerraformInstaller` to install Terraform, then `bash: terraform apply -auto-approve -var image_tag=$(Build.BuildId)` (assuming you use the pipeline build ID as an image tag to uniquely identify images). This would update the VMSS custom data or extension to use the new image tag. The Terraform Azure DevOps provider might need environment service principal credentials.

**CI/CD Considerations:**

- **Multi-stage pipelines:** You might separate CI (build/test) and CD (deploy). For instance, build the images in one pipeline, and trigger a release pipeline to deploy to the VMSS (perhaps after manual approval for prod).
- **Secrets:** Store ACR creds, Azure creds, etc., in the platform’s secure secret store (GitHub Secrets, Azure DevOps Library secure files/variables). Never store plain secrets in the repo.
- **Testing:** Include steps to run unit tests or integration tests. For example, after building the Spring Boot image, run a container with `mvn test` (or use Maven in pipeline outside Docker) to ensure nothing is broken.
- **Notifications:** Set up Slack/Teams/email notifications on pipeline failures or successes as needed.

At this point, a successful pipeline run means new images are in ACR and our infrastructure knows about them. The final piece is ensuring the Azure VMSS picks up the changes (either via rolling restart or scale-in/out events).

## 6. Deployment on Azure VMSS

Now that everything is built and in Azure, let's ensure the VMSS is configured to actually run the Docker containers and handle updates:

### 6.1 Configuring VMSS to Pull and Run Containers

As described in section 3, we used a custom script (cloud-init) in VMSS to install Docker and run the containers at instance startup ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=Your%20script%20should%20incorporate%20the,following%20commands)) ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=docker%20login%20%3Cyour,password)). Here are additional pointers to ensure this works smoothly in practice:

- **Docker Installation**: We installed Docker using `apt-get`. Azure Ubuntu images may not come with Docker pre-installed, so this step is necessary. The script uses `docker.io` from Ubuntu repos, which is fine for starters. For more control, you could install a specific Docker Engine version (or use the **Azure Docker VM Extension**). Microsoft provides a Docker VM extension that can be added to VMSS to handle Docker installation – however, using the extension might not be straightforward to trigger container runs. Our approach is self-contained via script.

- **ACR Authentication**: In the script we used `docker login -u -p`. This means the credentials are in the custom data (base64 encoded in the VMSS model). This is not ideal from a security standpoint (credentials could be decoded by someone with access to VMSS model). A better approach:

  - **Managed Identity**: Enable a system-assigned managed identity on the VMSS (`identity { type = "SystemAssigned" }` in Terraform). Then, in the script, instead of `docker login`, use Azure CLI to get an ACR access token. For example:
    ```bash
    az login --identity
    acr_password=$(az acr login --name <MY_ACR> --expose-token --output tsv --query accessToken)
    docker login <MY_ACR>.azurecr.io -u 00000000-0000-0000-0000-000000000000 -p $acr_password
    ```
    The above uses the managed identity to get an access token for ACR. (The username `000...000` is a placeholder when using token-based login). This avoids hard-coding credentials. Ensure the managed identity has the **AcrPull** role on the ACR.
  - Alternatively, use Azure Key Vault: store the ACR credentials in Key Vault, and in the script use `curl` or `az keyvault secret show --id ...` (with managed identity auth) to retrieve them. This is also secure and auditable.

- **Docker Run**: We run containers with `--restart always`, which means if the Docker daemon or container restarts, they will be relaunched. This covers VM reboots. In VMSS, if an instance is shut down or reimaged, on boot, cloud-init runs again which might attempt to run duplicate containers. However, because we name the containers, if a container with that name exists, Docker run will fail. To be safe, the script could check if a container is already running before running (or use `docker run --rm` with appropriate handling). A simple approach:

  ```bash
  docker ps -a | grep -q "web" || docker run -d --restart always -p 80:80 --name web ...
  ```

  This ensures we don't duplicate on re-run of script. In practice, Azure reimaging a VM might not re-run custom data unless it's a full re-provision, but extension behavior should be considered ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=Are%20extensions%20run%20again%20when,healed%20or%20reimaged)) (if VM is simply rebooted, the cloud-init doesn't re-run, if fully reimaged, it does).

- **VMSS Instance Custom Script Extension**: Another method is to use the **Custom Script Extension** on VMSS to run a script post-provision. We effectively did that via cloud-init. But note, if you ever need to update the script or run commands on existing VMs, you might use the Custom Script Extension resource in Terraform. For example, an extension could be used to deploy updated configuration without recreating VMs.

At this stage, when a VMSS instance starts (either initially or new ones from scale-out), it will execute the cloud-init commands and pull the latest images. If you always use the `:latest` tag, ensure that the VM does indeed pull the newest version (Docker will cache the image after first pull. If you update the image in ACR with the same tag, a new VM might still pull the cached old image if it was baked into the VM image or already pulled. In our case, each VM is fresh so it pulls from ACR. But if an instance reboots, `--restart always` would just restart the container with the same image, not fetch new. So **to deploy updates, you likely need to update the VMSS (causing recreate of VMs or container restart)**).

**Rolling Updates of Containers on VMSS:** Since we chose `upgrade_mode = Automatic` for VMSS, whenever the model (configuration) changes, Azure will roll out changes to all instances gradually. This is useful. To leverage it for deploying a new app version:

- Option 1: Change something inconsequential in the custom data (like an environment variable value or a comment) and run `terraform apply`. Azure VMSS will detect model changes and start a rolling upgrade of VMs (deleting/updating one fault domain at a time, etc.). Each VM re-runs the startup script on re-provision, thereby pulling the new image. This gives zero-downtime if at least one VM stays up while others upgrade.
- Option 2: Use `az vmss rolling-upgrade` commands as mentioned to explicitly start an upgrade with a new image reference (this may require using image versioning or updating custom script extension).
- Option 3: Blue-green with VMSS (detailed in next sub-section).

Azure VMSS can perform automatic OS image upgrades as well (e.g., patch the base image), but that’s separate from our app updates. We mainly care about our containers.

### 6.2 Implementing Auto-Scaling Policies

We configured autoscaling in Terraform. Ensure it’s working:

- The Azure portal (Scale Set -> Instances or Autoscale settings) will show the current number of instances and any scale actions taken. You can simulate high CPU to see if it scales out (e.g., run a CPU-intensive command in one of the containers or use Azure Monitor's "Run test alert rule").
- Make sure to attach the VMSS to the autoscale profile (we did via `target_resource_id`). Azure Monitor will now evaluate the rules. For example, when CPU > 75%, it will add instances up to max ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=name%20%3D%20,)).
- You might also consider custom metrics for scaling (like queue length, request count, etc.), but that requires pushing custom metrics to Azure Monitor from the app. For now, CPU is a simple heuristic.

Auto-scaling will keep your deployment cost-effective and performant: under low load, maybe you only have 2 VMs, under heavy load, you scale up to 5 or 10.

**Testing Autoscale:** You could deploy a load test (using JMeter, Locust, etc.) that simulates traffic to see if new VM instances appear and serve traffic. Remember to configure the load balancer’s health probe properly so it only sends traffic to fully started containers (the `azurerm_lb_probe` on port 80 with a timeout ensures a new VM isn’t considered healthy until Nginx is up).

Also note, scaling _in_ (reducing VMs) will terminate VMs arbitrarily (it attempts to keep balance across fault domains). Ensure your app can handle that (stateless containers are fine – as long as no user session is tied to a specific instance, which in our case, sessions would be client-side or using a shared database).

### 6.3 Rolling Updates and Blue-Green Deployment Strategies

**Rolling Update (In-Place):** We touched on rolling updates using VMSS’s automatic upgrade. This means you can gradually replace the instances with new ones running updated code. Azure will take a few VMs at a time offline, update them, bring them back, then proceed to the next batch, which ensures the service stays up ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=in%20the%20same%20subscription%20and,between%20staging%20and%20production%20slots)). You can configure the upgrade policy (like max batch size, etc., through Azure CLI or Portal; Terraform doesn’t expose fine-grained rolling parameters easily, but Automatic mode uses defaults). Monitor the process via Azure Portal – you’ll see instance status changing to Upgrading.

**Blue-Green Deployment:** In a blue-green model, you maintain two environments: Blue (current live) and Green (new version). For VMSS, a way to do this is:

- Create a second VMSS (Green) with the new version of the app (perhaps using the same Terraform module but with a different name and pointing to the new image tag).
- Attach this new VMSS to the load balancer **using a different backend pool and front-end** (or easier: if using an Application Gateway or Traffic Manager, you can direct traffic to one or the other). Azure Load Balancer itself doesn’t easily do URL switching between two separate VMSS; you could swap the backend pool, but that’s manual. A method mentioned in Azure docs is to swap public IPs of two load balancers ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=How%20do%20I%20do%20a,same%20subscription%20and%20same%20region)) – essentially swapping Blue and Green environments' IPs, but that can cause a short downtime as IPs detach/attach.
- A more seamless method is to use Azure Traffic Manager (DNS-based) or Azure Front Door to route traffic to either Blue or Green deployment. For example, initially all traffic goes to Blue’s LB IP. Once Green is ready, you switch Traffic Manager to Green’s IP. This approach can give near-zero downtime cutover and easy rollback (switch back to Blue if needed) ([Blue-Green deployments using Azure Traffic Manager](https://azure.microsoft.com/en-us/blog/blue-green-deployments-using-azure-traffic-manager/#:~:text=Blue,the%20new%20version%20being%20deployed)) ([Azure Traffic Manager and blue/green deployments - Stack Overflow](https://stackoverflow.com/questions/78732777/azure-traffic-manager-and-blue-green-deployments#:~:text=Azure%20Traffic%20Manager%20and%20blue%2Fgreen,If%20you%20want%20to)).
- Azure suggests using Application Gateway with two backend pools as a faster option to swap, as it can switch routing rules quickly ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=in%20the%20same%20subscription%20and,between%20staging%20and%20production%20slots)). You could register Blue VMSS in pool1 and Green VMSS in pool2 on an Application Gateway (layer 7 load balancer) and then change the rule to direct traffic to the new pool.

However, implementing full blue-green doubles resource usage during deployment. For advanced production scenarios with strict uptime requirements, it is worth it. For many cases, a rolling update on VMSS (which already ensures some instances are always serving) is sufficient.

**Zero-Downtime Consideration:** Ensure that the Spring Boot app can start up fully and pass health checks before it’s put in rotation. Nginx serving static files starts quickly, but the Spring Boot app might take some seconds to initialize. If using Application Gateway or a custom health endpoint, ensure it checks the Spring Boot container too (for example, Nginx could return healthy only when it can reach the backend). Without an Application Gateway, our Azure LB health probe only checks port 80 (Nginx). We might improve it: Nginx could be configured to return unhealthy if backend is down. This can be done by tweaking the nginx health check endpoint or using a custom script. Alternatively, probe port 8080 directly on each VM (provided security allows) to know if Spring Boot is up – but then you’d need to open 8080 in NSG which we might not want externally. For simplicity, assume if Nginx is up, it's serving a maintenance page or something until backend is live.

**Cleanup:** If Blue-Green was used, after switching, you could tear down the old VMSS to save cost, or keep it idle (scaled to zero, which VMSS can’t exactly go to 0 unless it's a flexible orchestration mode – minimum is 1 for uniform, but you could deploy in flex mode for that capability).

In summary, for a straightforward approach, use rolling upgrades (update the VMSS in place). For an extra-safe deployment, consider blue-green with an Application Gateway or DNS switch. Azure's own suggestion: swapping public IPs between two VMSS is possible but may have some delay as resources deallocate/reallocate ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=in%20the%20same%20subscription%20and,between%20staging%20and%20production%20slots)).

## 7. Security Best Practices

Security is critical in production deployments. We will discuss how to secure various aspects of this architecture: the VMSS VM instances, container security, secrets management, and network security including TLS.

### 7.1 Securing VMSS Instances and OS

- **Minimal OS Surface**: Our VMSS uses the latest Ubuntu LTS image. This is a widely used, security-updated image. Ensure to keep the base image updated (Azure can auto-patch OS or you manually update the image version in Terraform periodically). Azure VMSS supports automatic OS image upgrades which can be enabled to keep VMs updated with the latest OS patches.
- **OS Hardening**: Since we have full VM access, apply Linux best practices:

  - Disable password authentication (we did via SSH key only). Azure by default did not set a password for the user (`disable_password_authentication = true` in Terraform) ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=os_profile%20,%7D)).
  - Use the principle of least privilege on the VM: only our Docker containers should be running. Do not install unnecessary packages. The `docker.io` install will bring some dependencies, but you might also want to install monitoring or security agents (discussed later) – still, avoid a full desktop or any UI packages.
  - Ensure the firewall (NSG) only allows needed ports. In our NSG, we allowed 22 for SSH from anywhere which is not ideal – restrict it to your IP or use Azure Bastion for VM access to avoid opening SSH to internet. Or remove SSH access entirely in production and rely on automation + monitoring (no direct VM login).
  - Enable **Azure Security Center (Defender for Cloud)** on the subscription. It will monitor the VMSS instances for baseline deviations and known vulnerabilities. It can alert if, say, Docker engine is unupdated or if there are brute-force attempts on SSH.
  - Use **Managed Identity** for any Azure resource access (like ACR, Key Vault) so you don't need credentials on the VM. This leverages Azure AD tokens and is more secure than secrets.
  - The containers should also run as non-root (we configured Spring Boot to use a `springuser` in the Dockerfile, and the Nginx default user is non-root in Alpine). Running as non-root in containers mitigates certain escalation risks ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=Running%20applications%20with%20user%20privileges,root%20user)).
  - Consider enabling Azure VMSS encryption for disks if the VMs might handle sensitive data. Azure VMs have OS disk encryption options.

- **Patching Docker and System**: Keep Docker up to date. The installed version from Ubuntu repos might be behind. You could install the official Docker CE. Regularly update your custom image script if needed to patch vulnerabilities. This is where using Azure VM extensions for Docker or using Azure Container Services might ease the maintenance – but with manual VMSS, you take on that responsibility.

### 7.2 Network Security and Access Control

- **Network Segmentation**: The VMSS is in a subnet. If you have other tiers (like database in another subnet or Azure service), use Network Security Groups or service endpoints so that the VMSS can only talk to what it needs. The Azure baseline recommends segmenting front-end and back-end in different subnets and applying NSGs accordingly ([Azure Virtual Machines baseline architecture - Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/virtual-machines/baseline#:~:text=Azure%20Virtual%20Machines%20baseline%20architecture,and%20one%20for%20back%20end)). In our case, if the Spring Boot needed database access, we could have a locked-down NSG that only allows the VMSS subnet to reach the database subnet on the DB port.
- **NSG Rules**: We configured NSG to allow ports 80, 443, 22. Ensure **no other ports are open**. For instance, our Spring Boot on 8080 should not be directly accessible from internet – and indeed our NSG doesn't allow 8080 from outside (and LB doesn’t forward it either). So only Nginx (80/443) is exposed. Verify NSG effective rules on Azure: it should show inbound open for 80,443 (any) and 22 (hopefully limited source). You might also add an outbound rule to restrict egress if needed (by default Azure allows outbound to internet; you could restrict VMs from calling out except to specific endpoints like ACR, if you want to tighten security further).
- **Load Balancer / Public IP**: Use Standard SKU LB and IP (we did). Standard LBs are secure by default (they closed ports unless configured). Basic LBs open all ports of attached VMs by default, so it's good we use Standard. Also consider using an **Application Gateway** or **Azure Front Door** in front for added security (WAF capabilities, SSL offload, etc.).
- **HTTPS (TLS)**: Serving the React app and API over HTTPS is a must in production. There are a couple of ways:

  - Terminate TLS at the VM: This means installing an SSL certificate on Nginx in each VM. You would open port 443 in NSG and load balancer. Nginx would serve HTTPS. You can use a wildcard certificate or a certificate from Key Vault. Azure Key Vault can integrate with VMSS via extensions to auto-install certificates. For example, the VM extension for KeyVault certificates can place a cert as a file on the VM or in Windows cert store. In Linux, you might have to script retrieval of cert from Key Vault and configure Nginx. This can be automated but is some effort. Alternatively, use a managed service:
  - **Application Gateway**: Put an Azure Application Gateway in front of the VMSS (the VMSS would be on a _backend pool_ of the App Gateway). App Gateway can have a WAF and handle SSL (you upload the certificate to it). It can do path-based routing too (e.g., /api to one pool, / to another, if you split front/back). In our unified VMSS scenario, you might still use App Gateway just for SSL and WAF. Clients hit App Gateway (HTTPS), App Gateway communicates with VMSS on HTTP (could also be HTTPS if you installed internal certs). This offloads the cert management to App Gateway. Note this introduces additional cost and slight latency, but gives enterprise-grade security and routing features.
  - **Azure Front Door**: Another option for global routing and CDN features. Front Door can terminate HTTPS and forward to an App Gateway or directly to VMs (with required setup). Probably overkill here.

  For simplicity, you might decide to manage TLS on Nginx. If so, use something like Let's Encrypt for certificates or have your org’s certificate. Keep the cert updated (you can automate Let's Encrypt via a cron job in the container or use Azure Automation). Also, configure secure SSL settings on Nginx (disable old TLS versions, etc.).

  **TLS version**: Ensure TLS 1.2 (or 1.3) is used. Azure front-end services usually enforce that. If using your own Nginx, configure it accordingly (Azure Security Center might flag if TLS1.0/1.1 is enabled).

- **Private vs Public**: If this app is internal only (not for internet users), you can avoid a public IP altogether. Use an internal load balancer and perhaps access the app via VPN or Azure Application Proxy. But assuming it's internet-facing, above steps stand.

### 7.3 Container and Application Security

- **Least Privilege for Containers**: We already set the Spring Boot process to non-root in the Dockerfile ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=Example%202)). Also avoid running Nginx as root (by default, Nginx in Alpine might use `nginx` user). Ensure the Docker daemon on the VM is restricted (it runs as root on Linux; be mindful that giving someone docker access is root access on the machine).
- **Image Scanning**: Use ACR’s built-in integration with Microsoft Defender for Cloud to scan images for vulnerabilities when pushed. This can alert you to CVEs in Nginx, Node, Java, etc. Fix high-severity issues by rebuilding images with updated base images regularly.
- **Dependency Management**: Keep your React and Spring Boot dependencies up to date to patch security issues in libraries.
- **API Security**: Implement authentication/authorization on your Spring Boot API if it's not a public open API. Use HTTPS (as discussed) to protect data in transit. Perhaps integrate Azure AD or another IdP if appropriate.
- **Secrets Management**: Use Azure Key Vault for any sensitive configuration. For example, if Spring Boot connects to a database, store the connection string in Key Vault. Then fetch it at container startup. Azure Key Vault is recommended for managing secrets rather than env vars in plaintext ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=Azure%20Key%20Vault%20for%20credentials,or%20secrets)). With Managed Identity, the VMSS can access Key Vault without any secret. We touched on this for ACR, same applies to any secret:
  - You could use an init container or a script that pulls secrets and writes to a volume that the Spring Boot app reads.
  - Or use environment variables that are set at launch by querying Key Vault (one could integrate this into the cloud-init script or run a lightweight tool like **Azure Key Vault to Kubernetes/env** type of solution if not using full AKS – since we are on raw VMs, a simple script is fine).
  - Do **not** commit secrets to Git or Terraform code. Use mechanisms such as Terraform variables (marked sensitive) or Azure DevOps variable groups (secret variables).
- **Managed Identity usage**: We gave an example of using it for ACR. Similarly, if Spring Boot needs to call an Azure service (like an Azure Storage or Cosmos DB), use Managed Identity to fetch credentials or to authenticate directly (Azure SDKs support MSI authentication). This avoids putting keys in config. Azure VMSS supports system-assigned and user-assigned identities, which can be configured in Terraform.

- **Audit Logging**: Enable Azure VMSS diagnostics logs. Azure can collect activity logs (e.g., scaling events, etc.). For security, monitor these:

  - When did scaling occur (was it expected or was it some abnormal event)?
  - If someone attempts an unauthorized SSH login, it would show in Linux auth logs – having those in Log Analytics (with alerts for failures) could be beneficial.

- **Container Isolation**: By default, all containers on a VM share the kernel. If a container is compromised, it could attempt to affect the host or other container. This is why keeping OS and Docker updated is important. If higher isolation is needed, one could explore Azure Kubernetes Service which can use gVisor or Firecracker via Kata containers for isolation – out of scope here, but worth noting if this was a multi-tenant environment requiring strong isolation.

- **Secure Boot & VM integrity**: Azure offers Trusted Launch VMSS (with vTPM, Secure Boot) which defends against rootkit/bootkits. If this is a high-security scenario, consider enabling those features in VMSS (requires compatible image). It ensures the VM boots with a verified OS kernel and helps protect secrets even if the host OS is compromised (vTPM can shield keys). Microsoft security baseline suggests enabling these where possible ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=match%20at%20L764%20the%20VM,Azure%20Policy%20initiatives%2C%20and%20configuring)) ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=,monitoring)).

To summarize: **store secrets in Key Vault (not in code)** ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=Azure%20Key%20Vault%20for%20credentials,or%20secrets)), use managed identities for Azure resource access, restrict network access (NSGs, no open ports other than needed), enforce TLS, run containers as non-root, and keep everything patched. These steps drastically reduce the attack surface and risk of breach.

### 7.4 Security Checklist

Before moving on, here's a quick checklist of security items:

- [x] **Secrets in Key Vault** – e.g., DB passwords, JWT signing keys are not in source code or VM, they are fetched securely at runtime ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=Azure%20Key%20Vault%20for%20credentials,or%20secrets)).
- [x] **Managed Identity** – VMSS identity used for ACR pulls and any Azure access (no hard-coded SP credentials).
- [x] **NSG** – Only ports 80/443 (HTTP/HTTPS) and necessary management ports open, and optionally restrict source IPs for management.
- [x] **Patches** – OS is updated (automatic or manual), Docker is updated, app dependencies updated.
- [x] **HTTPS** – Implemented TLS for front-end. Non-HTTPS disabled.
- [x] **Container** – Non-root user, minimal packages, images scanned for vulns.
- [x] **Monitoring** – Set up alerts for suspicious activities (next section).
- [x] **Backup** – if any data (like user uploads) stored on VM disks (generally not, containers are stateless here). Ensure any stateful data is in a secure external service.

By following the above, the deployment should meet a high security standard for production.

## 8. Monitoring and Logging

Deploying applications is not complete without robust monitoring and logging. We need to monitor the health and performance of both the infrastructure (VMs, OS, network) and the applications (Spring Boot and even the React front-end behavior to an extent). Azure provides several services to achieve this:

### 8.1 Infrastructure Monitoring with Azure Monitor

**Azure Monitor** collects metrics for VMSS such as CPU usage, memory (if Azure Monitor agent installed), disk I/O, network, etc. We already use Azure Monitor metrics for autoscaling (CPU). We can also create **alerts** on these metrics:

- For example, an alert if CPU is above 90% for 10 minutes (maybe our scale-out didn't happen or is insufficient).
- Alert if memory usage is too high or if disk space is low (disk space on VMs can fill up, especially with Docker images; monitor `/var/lib/docker` usage).
- VM availability: Azure emits metrics if instances are unhealthy. We can alert if, say, more than 1 VM in VMSS is down or in error state.

To get memory and detailed host metrics, you should install the Azure Monitor **Log Analytics Agent** (also known as Azure Monitor agent or formerly OMS agent) on the VMs. There is a newer Azure Monitoring Agent that can be deployed to VMSS via extension and configured to send data to a Log Analytics Workspace. You could deploy this via Terraform extension or through Azure Portal (it's an option in VMSS settings). Once the agent is there, you gain insights like memory % available, etc., and can query logs.

- **Log Analytics Workspace**: Create one and configure data collection. Useful logs to collect:
  - Syslog (to capture system logs, auth logs).
  - Docker daemon logs.
  - We might ingest the application logs too (if they output to syslog or a file).

### 8.2 Application Insights for Application Monitoring

**Azure Application Insights** is a component of Azure Monitor specifically for application telemetry (requests, exceptions, traces, dependencies). We should use it for the Spring Boot application:

- Microsoft provides an Application Insights Java SDK and an **Agent** that can auto-instrument the app without code changes ([Monitor performance on Azure VMs - Azure Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/azure-vm-vmss-apps#:~:text=Note)). With Spring Boot, you can either manually add the Application Insights starter dependency, or use the agent which is easier in our container scenario.
- To use the agent in our Docker container, we can do the following:

  - Download the Application Insights Java 3.x Agent JAR (e.g., `applicationinsights-agent-3.4.5.jar`) and include it in the image or mount it. Our Dockerfile can copy it as shown in Microsoft’s example ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=If%20you%27re%20using%20the%20exec,jar%22%60%20parameter%2C%20for%20example)) ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=FROM%20)).
  - Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable to the connection string of your App Insights resource ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=COPY%20agent%2Fapplicationinsights)).
  - Adjust the entrypoint to include the `-javaagent:/path/to/agent.jar`. We could modify our Spring Boot Dockerfile final stage:
    ```dockerfile
    COPY --from=build /app/target/*.jar app.jar
    COPY applicationinsights-agent-3.7.0.jar applicationinsights-agent.jar
    ENV APPLICATIONINSIGHTS_CONNECTION_STRING="<your AI connection string>"
    ENTRYPOINT ["java", "-javaagent:/app/applicationinsights-agent.jar", "-jar", "/app/app.jar"]
    ```
    This will start the JVM with the AI agent. The agent will auto-collect HTTP requests, SQL DB calls (if JDBC used), etc., and send to Azure ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=If%20you%27re%20using%20the%20exec,jar%22%60%20parameter%2C%20for%20example)).
  - Alternatively, use the App Insights VM Extension. There is an extension that can be applied to VMSS which will attempt to instrument Java apps. But in a container, it might not detect the process. The recommended way for containers is to include the agent in the container or use OpenTelemetry. Microsoft documentation notes that the VM extension autoinstrumentation is mainly for IIS, .NET etc., and for Java in containers, you should manually attach the agent ([Monitor performance on Azure VMs - Azure Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/azure-vm-vmss-apps#:~:text=Note)).

- **Application Insights for React**: You can also use Application Insights in the React front-end by adding the JavaScript SDK. This can track page views, user metrics, and caught front-end exceptions. It's as simple as including the AI JavaScript snippet with your instrumentation key in your React app (perhaps behind an environment flag). This is optional but gives a full end-to-end view.

Once App Insights is set up:

- You get **request metrics** (like how many requests per second, response durations for the Spring Boot API).
- **Dependency metrics** (if Spring Boot calls an external service or DB, it logs the call times).
- **Application Logs**: You can use App Insights to capture logs. If you use `Logger` in Spring Boot, you can configure an App Insights appender or rely on agent's capture of `System.out` and certain frameworks. The AI agent 3.x can automatically collect logs from popular frameworks (Logback, etc.) and send to AI as trace telemetry ([Monitor performance on Azure VMs - Azure Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/azure-vm-vmss-apps#:~:text=Note)).
- **Custom metrics/traces**: You can also instrument code to send custom events (like business events).
- **Alerts**: App Insights allows alerts on application metrics. E.g., alert if failed request rate > X%, or specific exception occurrences.

**Connecting Logs and Metrics**: Azure Monitor **can correlate VM metrics with App metrics**. For instance, if CPU is high and at same time requests are high or exceptions spiked, you can see that.

### 8.3 Logging from Docker Containers

By default, Docker containers log to `stdout` and `stderr`. In our VM setup:

- Nginx logs will go to its own files inside container (unless configured to log to stdout).
- Spring Boot (if using console logging) will log to stdout, which Docker captures.

We have a few ways to aggregate these logs:

1. **Azure Monitor Container Logs**: Azure has Container Insights but primarily for AKS. For VMs, if we install the Azure Monitor agent and configure it to collect Docker container logs, it is possible. The Linux agent can be configured (via `/etc/azuremonitoragent/config.yaml` or similar if using new AMA) to collect logs from specific docker container stdout. There was an older approach with fluentd and the OMS agent to gather Docker logs ([How to get Docker Container Logs into Log Analytics Workspace - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/153026/how-to-get-docker-container-logs-into-log-analytic#:~:text=I%20am%20trying%20to%20get,console%20logs)) ([How to get Docker Container Logs into Log Analytics Workspace - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/153026/how-to-get-docker-container-logs-into-log-analytic#:~:text=I%20think%20following%20document%20might,monitor%2Finsights%2Fcontainers)), but it required some config (and only worked with the older Log Analytics agent). If we want to keep it simpler, we might not do this.
2. **Application Insights**: If the Spring Boot logs are captured by AI, that covers those. For Nginx access logs, one approach: configure Nginx to log to stdout (for example, in nginx.conf: `access_log /dev/stdout main; error_log /dev/stderr;`). This way, Nginx logs go to container stdout. Then the Azure monitoring agent (if set to capture docker stdout) or a custom script could read them.
3. **Custom Logging**: We could run a sidecar container or a cron job on VM that `docker logs` each container and ships it somewhere (not very elegant).
4. **Third-party**: Use ELK stack or Azure Log Analytics agent with custom fluentd config to capture `/var/lib/docker/containers/*/*-json.log` files (these files contain stdout logs in JSON). There are community guides on configuring fluentd to pick those up ([How to get Docker Container Logs into Log Analytics Workspace - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/153026/how-to-get-docker-container-logs-into-log-analytic#:~:text=I%20am%20trying%20to%20get,console%20logs)).

An easier method: **Use Application Insights for everything**:

- For Nginx, we could forgo trying to get those logs if not critical, or send Nginx logs to a custom telemetry (like have a script tailing nginx log and sending to AI as trace).
- For Spring Boot, rely on AI.
- The React app doesn’t produce server logs (just static files served).

**Azure Monitor Alerts & Dashboards**:

- Set up alerts for HTTP 500 error rates or exceptions in App Insights.
- Alert if VMSS instance count is at max (meaning you might need to increase capacity).
- Use Azure Dashboard to combine metrics: e.g., a chart for CPU usage, a chart for request rate, etc. This helps in capacity planning and troubleshooting.
- Enable **Azure Monitor for VMs (Insight)** on the scale set: it can analyze VM performance and map processes. It might not fully work on scale set via portal (it tries though). The VM Insights can show you top processes by CPU etc., which can be useful (though we know our main process is likely Java when under load).

### 8.4 Health and Diagnostics

- **Health Probes**: We set an HTTP probe on port 80. Ensure your Nginx returns a 200 on the probe path. By default, it will for `/` if the React index.html is there. If Spring Boot is down, Nginx will still return some page (maybe 502 or a custom error). The LB may not detect that as unhealthy unless we program Nginx to return unhealthy in such case. Something to consider if strong health checking is needed.
- **Application Health**: Spring Boot Actuator can expose health at `/actuator/health`. You could set up an Azure App Insights availability test (ping test) hitting an endpoint periodically from outside to verify the app is up globally.

- **Log Retention**: Decide how long to retain logs/metrics in Azure (default 90 days for Log Analytics, 90 days for AI). Adjust if needed, but be mindful of cost.

- **Tracing**: If distributed tracing is needed (not much here since one service), AI can correlate front-end and back-end via correlation headers if you instrument both.

In summary, leverage Azure Monitor and Application Insights to get a full picture:
Azure Monitor for VM metrics and container logs, Application Insights for application-level telemetry (requests, dependencies, custom events) ([Monitor performance on Azure VMs - Azure Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/azure-vm-vmss-apps#:~:text=Note)). This dual approach covers both infrastructure and app, which is important for advanced monitoring.

## 9. Troubleshooting and Performance Optimization

Even with the best planning, issues can arise. Let’s discuss common problems and how to troubleshoot them, as well as ways to optimize performance and cost:

### 9.1 Common Deployment and Runtime Issues

- **Terraform Errors**: If `terraform apply` fails, check the error message. Common issues:

  - Authentication issues (ensure Azure creds are correct).
  - Quota issues (e.g., if your region doesn’t have enough vCPU quota for the VM size, you might see a failure).
  - Misconfigured dependencies (Terraform may try to create a resource before another – use `depends_on` if needed, though in our config, explicit references handle ordering).
  - VMSS Deployment errors: If the custom data script has invalid syntax, the VMSS will still deploy but the script inside may fail. You won't see that in Terraform output. To troubleshoot, go to Azure Portal -> the VM scale set -> Instances -> pick an instance -> Boot Diagnostics (screenshot of console) or Serial Console. The Serial Console can show cloud-init output and errors ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=docker%20containers,the%20docker%20images%20are%20uploaded)). E.g., one user found that Docker wasn’t installed because the script had a typo, by checking the VM serial log ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=happen%20is%20that%20I%20have,using%20Container%20Registry%2C%20since%20that)).
  - Extension issues: if using VM extensions, those can error – check VMSS instance extension statuses in Azure.

- **VMSS Instances not coming up**: If after deployment, instances are off or unhealthy:

  - Check the **Boot Diagnostics** screenshot for kernel panics or OS errors.
  - Ensure the VM size is available in the chosen region/zone.
  - Check VMSS **model** and **instance** view via Azure CLI:
    ```bash
    az vmss list-instances -g <rg> -n vmss-myapp -o table
    az vmss get-instance-view -g <rg> -n vmss-myapp --instance-id 1 -o json
    ```
    The instance-view can show extension provisioning results, boot status, etc.
  - If the VM is up but Docker containers are not running, SSH into the VM (if accessible) or use `az vmss run-command invoke` to run a quick command like `docker ps`. If Docker isn’t installed, then our script failed early – again check logs.

- **Docker Pull failures**: If the VM cannot pull from ACR:

  - Perhaps the login failed. Check `/var/log/cloud-init.log` on the VM for errors. Maybe the credentials were wrong or the VM’s managed identity lacked permissions. You can try to manually docker login on the VM.
  - Networking: ensure the VM has internet or at least access to ACR’s endpoint. If your VNet is restricted (no internet), you might need a service endpoint or private link to ACR.
  - DNS: VM must resolve `<myacr>.azurecr.io`. By default, Azure provides DNS. If using custom DNS, make sure it can resolve Azure endpoints.

- **Containers not starting**: If images pulled but `docker run` failed:

  - Possibly a port conflict (maybe something already on 80? Unlikely on fresh VM). Or docker run command had a typo. Use `docker ps -a` to see exited containers and `docker logs <name>` to see error output.
  - Spring Boot might have failed to start due to an exception (misconfiguration). Check its logs via `docker logs api`.
  - Nginx container might fail if config is bad. Check `docker logs web`.
  - Ensure the container processes don't require interactive TTY or anything (we used `-d` to run detached).

- **Load Balancer not serving**: If you hit the LB IP and get no response or error:

  - Check that at least one VM instance is healthy. In Azure Portal, under LB -> Backend Pools -> you can see number of healthy vs unhealthy.
  - If all unhealthy, the probe likely failing. Try accessing the site via the VM's IP directly (if you allowed that for testing) or use `curl http://localhost` within the VM to see if Nginx responds.
  - Possibly the NSG is blocking LB probe (shouldn't, as it's source is Azure infrastructure). If you used Standard LB, note that the NSG must allow the probe traffic as well (Standard LB originates from a VM with an Azure IP). In our NSG, we allowed all sources on 80, so it's fine.
  - If using Application Gateway, ensure backend HTTP settings match (host name, etc.).
  - Check that the VMSS is associated with the LB's backend pool (our Terraform did that via `ip_configuration` reference).
  - Use `az network lb show ... --query backendAddressPools[0].backendIPConfigurations` to see if it lists VM NICs.

- **Autoscale not triggering**: If you expect scale out but it doesn't happen:

  - Check Azure Monitor logs for the autoscale evaluation (Azure Portal has an activity log for autoscale actions and reasons).
  - Perhaps the metric isn't crossing the threshold or not reporting. Ensure the VM has the Azure diagnostics extension or at least default metrics (CPU should be there by default).
  - It could be that in Terraform, autoscale was not applied due to some bug. Verify the autoscale setting exists in Azure (Portal: Monitor -> Autoscale settings).
  - There might be a minimum interval (autoscale checks every few minutes).
  - Test by pushing a load that definitely exceeds threshold for longer than time_window.

- **Terraform and CI**:
  - If using Terraform in CI, watch out for state file handling and concurrency. Use a remote state to avoid conflicts.
  - If multiple team members run terraform, they should not clobber each other’s changes.

### 9.2 Debugging Tips

- **Log everything**: Use the VM extension RunCommand to run debug commands on all VMs. For instance:
  ```bash
  az vmss run-command invoke -g <rg> -n vmss-myapp --command-id RunShellScript --instance-id "*" --scripts "docker ps; docker logs api"
  ```
  This can fetch the running containers and logs from each instance in one go.
- **Use Application Insights**: It will show exceptions stack traces if Spring Boot throws any. This is immensely helpful for debugging application-level issues that may not show on infrastructure logs.
- **Local replication**: If something fails on Azure, try to replicate locally with Docker Compose or similar to see if it's environment-specific.
- **Azure Support and Community**: If you face a weird Azure error, search for it. Azure VMSS has some known pitfalls (like the need for outbound NAT for internet access on standard LB if no instance-level public IP – but with standard LB, it creates a default outbound rule so internet should work).

### 9.3 Performance Optimization

Finally, once things are running, consider optimizations:

- **Optimize VM Size**: Monitor the CPU and memory usage. If the instances are mostly idle or not using full resources, you might use smaller VM sizes to save cost (or reduce the number of instances). Conversely, if under heavy load you're maxing out CPU and memory, a larger VM might handle more load per instance, reducing the count of instances needed. There’s a balance – many small VMs vs fewer large VMs. Azure pricing can guide you which is more cost-effective for the performance.
- **Scaling Metrics**: Perhaps CPU isn’t the best indicator. If your app is I/O bound or memory bound, you might scale on memory usage or queue length (if the system has a job queue). Azure Monitor can autoscale on custom metrics too. For example, you could push a custom metric “requests_per_second” from App Insights into Azure Monitor and scale on that if CPU doesn’t correlate well.
- **Optimize Docker layers**: Use caching in Docker builds to reduce build time. Use multi-stage (we did). Also, consider using a caching proxy or Azure Cache for Redis if the app benefits from caching frequently used data instead of recomputing or querying DB repeatedly.
- **CDN for Static Content**: Offload React static files to a CDN (Azure CDN, or Front Door caching). This way, requests for JS/CSS go to CDN edge, reducing load on VMSS for static content. You can still deploy the React app to VMSS, but put a CDN in front of the LB for the `/*.{js,css,png}` files. Azure CDN can pull from the VMSS (if public) or you might move React hosting to Azure Blob static websites or Azure Front Door. This can drastically improve global performance for static assets and reduce VM bandwidth costs.
- **Database connections**: If Spring Boot connects to a database, ensure connection pooling is tuned to avoid exhaustion, especially as VMs scale out (many instances times many connections each = lots of connections). Possibly use a cloud DB that can scale or a read-replica setup if needed.
- **JVM tuning**: If very high throughput, consider tuning the JVM (heap sizes, garbage collector) for Spring Boot. The default might be fine for most moderate loads, but large heaps might need specific GC (G1 vs others).
- **Remove Unused Services**: If you enabled Application Insights agent, monitor its overhead. Typically minimal, but if you find overhead, you can fine-tune what it collects. Similarly, if you have other agents (security or monitoring), ensure they are not consuming too much CPU.
- **Cost Optimization**:
  - Use Azure **Reserved Instances** or **Savings Plans** for VMs if this is a long-running production (can save up to ~50% by committing to 1-year/3-year).
  - Use **Spot VMs** for non-production or if you can tolerate random evictions (likely not for prod API).
  - **Scale-in aggressively** during off hours if traffic drops at night – maybe schedule scaling rules (Autoscale allows schedule-based profiles, e.g., at night min=1, during day min=3).
  - Evaluate if you need all components: For example, if React is mostly static, hosting it on Azure Blob Storage static website + CDN might be far cheaper than running VMs for it. The Spring Boot could then be the only thing on VMSS (and you could even then use Azure App Service for Spring Boot possibly – though here we stick to VMSS).

### 9.4 Disaster Recovery and Redundancy (Performance angle)

While we'll discuss DR in the next section, note that running in multiple regions can also improve performance for users (they connect to nearest). That’s a complex setup (active-active multi-region). But keep in mind if global low-latency is needed, an architecture using multi-region deployment with Azure Front Door directing traffic could be an optimization.

By continuously profiling and load testing your application, you can identify bottlenecks (CPU vs memory vs network). Use Azure’s **Performance Diagnostics** or App Insights Profiler (if available for Java) to capture traces under load to see where time is spent.

In summary, troubleshooting involves checking logs at all levels (VM, container, app) and using Azure’s diagnostic tools, while performance tuning involves right-sizing resources, efficient scaling, and offloading work (cache/static content) where possible.

## 10. Final Review and Production Deployment

Let's recap and finalize what needs to be done before considering the system production-ready, and discuss strategies for resilience and disaster recovery in production.

### 10.1 Pre-Production Best Practices Checklist

Before going live, go through this checklist:

- **Infrastructure**:

  - All Terraform configurations are in version control and reflect the intended state (no out-of-band Azure changes that Terraform doesn't know about).
  - Terraform state is secured (e.g., stored in Azure Storage with access controls) and not left in local machines.
  - The Azure Resource Group contains only the resources needed. Remove any test resources or defaults that are not required (to minimize attack surface and cost).
  - Tags are applied to resources (env, app name, owner) for manageability.
  - Load balancer health probe and load balancing rules are verified in staging environment with high load to ensure they behave as expected.
  - Autoscale thresholds are tuned based on load testing results (so it scales out in time before overload, and scales in when truly under-used).
  - The VMSS upgrade policy is set appropriately (Automatic for ease, or Manual if you prefer to control when upgrades happen).
  - If using Availability Zones, ensure VMSS is zone-distributed (we used `zones = ["1"]` in example for single zone; for HA, use multiple zones if region supports, e.g., `zones = ["1","2","3"]` to spread VMs ([Reliability in Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-virtual-machine-scale-sets#:~:text=,autoscales%20only%20within%20that%20zone))). Update Terraform accordingly for zone redundancy.

- **Security**:

  - NSG rules reviewed – only expected ports open. No wide-open management ports or unnecessary outbound access.
  - SSL certificate installed and HTTPS serving tested. Non-HTTPS access either redirected or disabled.
  - Web application firewall (WAF) in place if this is a high-risk internet-facing app (either via Azure Application Gateway WAF or Azure Front Door WAF). At least have Azure DDoS Basic (which is default) or consider DDoS Standard protection if needed.
  - All secrets (ACR creds, DB creds, etc.) are coming from secure sources (Key Vault or Managed Identity). For any that had to be in the cloud-init script (if you didn't implement Key Vault), rotate those credentials regularly and plan to eliminate them.
  - VMSS Managed Identity has only necessary RBAC roles (e.g., AcrPull, maybe KeyVault Reader). Remove any excess permissions.
  - Test an attack scenario: e.g., run a vulnerability scanner (like Qualys or open-source) against your VM/IP to see if any obvious holes (many organizations do a pen-test or use Azure Defender which can simulate attacks).
  - Ensure container images in ACR are scanned (enable Defender for ACR).

- **Reliability & Monitoring**:

  - Set up Azure Monitor alerts: e.g., alert on high CPU for 30m (could indicate runaway process), alert on low instance count but high load (scale might be stuck), alert on any container crash loops.
  - Setup Application Insights alerts: e.g., alert if Server Exceptions > X in Y minutes, or if response time suddenly spikes.
  - Create a dashboard that shows key metrics (CPU, memory, instance count, request rate, error rate) for quick status checks.
  - Verify logging is capturing needed info. Do a test where you force an error in Spring Boot (maybe throw a test exception) and ensure it appears in App Insights logs and any log storage.
  - If using third-party logging or APM (like Dynatrace, Datadog), ensure their agents are installed and reporting.

- **Performance & Load**:

  - Perform a load test close to expected peak load (and a bit beyond) in a staging environment. Measure the auto-scale response time, the application throughput, and see if any 5xx errors occur.
  - Based on load test, adjust the number of instances (default/min) to handle baseline traffic and the autoscale rules to respond quickly enough.
  - Check that response times under load are within acceptable range (if not, consider scaling out earlier or optimizing code).
  - Test static file delivery (maybe use a CDN in front as mentioned).

- **Deployment Process**:

  - Document the deployment process for new versions. Is it just a git push (CI/CD takes over)? Or do you need to run Terraform manually? Make sure it's clear to the team.
  - If manual intervention is needed for production (like approving a release or pressing a button to swap Blue/Green), ensure responsible parties know how to do it.
  - Use a staging slot or environment that is as similar to production as possible to test any infrastructure changes (like Terraform module updates or major version upgrades) before applying to prod.

- **Roll-back Plan**:
  - Have a strategy if a deployment goes wrong:
    - If using rolling upgrade: know how to stop it or roll back (in VMSS, you might have to redeploy the old image tag or if using App Gateway, divert traffic back to old pool).
    - Keep the previous container images tagged (don't delete the "last known good" image, maybe tag it as `stable` or with a version).
    - In worst case, you can redeploy the whole infra from Terraform using an older commit. Because it's all IaC, in theory, one could spin up a parallel environment quickly from code.
  - Database changes (if any) need backward compatibility to allow quick rollback of app.

### 10.2 Disaster Recovery Strategies

Disaster Recovery (DR) is about handling regional outages or major failures. Azure VMSS is region-specific ([Reliability in Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-virtual-machine-scale-sets#:~:text=Virtual%20Machine%20Scale%20Sets%20can,region%20failover)), and as noted, Azure Site Recovery doesn’t support VMSS (for uniform orchestration) ([Azure VM Scale set cross regional DR - AZURE - KodeKloud - DevOps Learning Community](https://kodekloud.com/community/t/azure-vm-scale-set-cross-regional-dr/261714#:~:text=You%20can%20configure%20disaster%20recovery,doesn%E2%80%99t%20support%20VM%20scale%20sets)). So we need to design our own DR:

- **Multi-Region Deployment**: The primary strategy is to deploy the whole stack in a secondary Azure region. You can use the same Terraform scripts, just parameterize the region and resource names. For example, have `var.azure_region = "EastUS2"` for secondary. This will create a duplicate environment. Use a different resource group and maybe suffix resources with “-dr” or similar. The React and Spring Boot images can be the same (you might use ACR's geo-replication to have images available in multiple regions quickly, or push to two ACRs).
- **Data considerations**: If your Spring Boot uses a database, you need a cross-region replicated database (like Azure SQL with geo-replication, or Cosmos DB which is multi-region by design, or a primary-secondary replication set). Ensure the DR site can access a recent copy of data. Usually, one region is primary for writes, the DR is secondary read-only until failover.
- **DNS/Traffic Manager**: Use Azure Traffic Manager (DNS-based routing) or Azure Front Door to route users to the primary region. In case of failure, switch to secondary. Traffic Manager can detect endpoint failure (via health probe) and automatically fail over DNS to the secondary region’s IP ([Blue-Green deployments using Azure Traffic Manager](https://azure.microsoft.com/en-us/blog/blue-green-deployments-using-azure-traffic-manager/#:~:text=Blue,the%20new%20version%20being%20deployed)). This can take DNS TTL time to propagate (could be 1-5 minutes). Azure Front Door can also do active-passive failover with faster global failover, and it will also handle the SSL and custom domain so you don't need separate certs per region.
- **Cold vs Warm Standby**: You could keep the DR environment scaled down to minimum (maybe 1 instance) to save cost, or even deallocated (scale set capacity 0 isn’t possible with uniform VMSS; min 1, unless using flexible orchestration where you _could_ have 0). A workaround is to not create the VMSS until needed (but that means slower startup). Better to keep 1 VM running in DR to handle minimal load and be warmed up. That instance can also apply updates simultaneously so that DR always runs the same version.
- **Synchronization**: Use CI/CD to deploy to both regions (maybe sequentially: first primary, then secondary once primary is confirmed good, or vice versa for caution).
- **Testing DR**: Regularly perform a DR drill: simulate primary down by disabling the primary endpoint in Traffic Manager and see if all services work from secondary. This test ensures your Spring Boot app in secondary can connect to the database (which might have failed over if using something like Cosmos which does auto-failover, or if using SQL, you might need to initiate a failover).
- **Site Recovery**: As noted, ASR doesn't support VMSS Uniform, but apparently VMSS Flex is partially supported (not scaling, but availability scenario) ([Azure VM Scale set cross regional DR - AZURE - KodeKloud - DevOps Learning Community](https://kodekloud.com/community/t/azure-vm-scale-set-cross-regional-dr/261714#:~:text=Faisal,3)). However, since we can redeploy with Terraform, ASR isn't necessary. Our stateless compute can be re-created from images quickly.
- **Backup**: For any stateful components (maybe you have user-uploaded files on an Azure Files share or something), ensure those are geo-redundant or backed up. Our setup is stateless (assuming all uploaded data goes to a storage service, not local disk).
- **Downtime expectations**: Document the RTO (recovery time objective) and RPO (recovery point objective) you can achieve. If DR is manual (someone runs terraform in DR region), maybe RTO is a few hours. If using Traffic Manager auto-failover, RTO could be minutes. RPO depends on data replication (e.g., if DB is syncing with 5 min lag, you might lose 5 min of data on failover).

- **DR Environment Parity**: The secondary environment should be as identical as possible to primary to avoid surprises. Use the same VM SKU, scale settings (perhaps scaled down normally). Keep images in sync.

- **Costs**: Running two environments doubles costs. If budget is a concern, you might run a scaled-down DR (one instance, small DB) and accept a slight degradation in performance if failover happens until you scale it up.

**Final note**: Some teams choose not to do multi-region for smaller apps and instead rely on Azure's regional reliability (which is generally high) plus nightly backups to restore in worst case. But advanced, mission-critical apps should have DR.

### 10.3 Final Thoughts

At this stage, we've set up a fully automated pipeline from code to Azure infrastructure. We used Terraform to provision reproducible infrastructure, Docker to containerize applications, and Azure VM Scale Sets to host them with auto-scaling. We've integrated CI/CD for continuous deployment and put in place robust monitoring, logging, and security measures.

Before going live, it's wise to run a **pilot or beta** with some real traffic (if possible) to observe system behavior, then iterate on any tuning. Once satisfied:

- Document how to deploy new changes, how to access logs, how to perform emergency operations.
- Train the operations team (if separate) on using Terraform and understanding the VMSS model.
- Have on-call procedures for alerts (who gets paged if an alert triggers at 2am?).

When everything is green-lit, you can confidently point the production DNS (e.g., `myapp.com`) to the Azure load balancer or Front Door and launch 🚀.

This comprehensive setup should serve an advanced team well by providing scalability, resilience, and maintainability. By adhering to the guide above, you ensure that **DevOps best practices** are followed: Infrastructure as Code, Immutable infrastructure (containers & VMSS instances that can be replaced easily), Continuous Deployment, and thorough monitoring and security hardening.

---

**References:**

- Azure VM Scale Sets overvie ([Reliability in Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-virtual-machine-scale-sets#:~:text=With%20Azure%20Virtual%20Machine%20Scale,VM%20instance%20that%20you%20create))】 and autoscaling capabilitie ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=name%20%3D%20,))】.
- Guidance on running Docker on VMSS (custom script and considerations ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=Your%20script%20should%20incorporate%20the,following%20commands)) ([Docker Containers on Azure VMSS - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2157273/docker-containers-on-azure-vmss#:~:text=docker%20login%20%3Cyour,password))】.
- Multi-stage Docker build examples for React and Ngin ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Build%20Stage%20FROM%20node%3A18,RUN%20npm%20run%20build)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Production%20Stage%20FROM%20nginx%3Astable,g%22%2C%20%22daemon%20off))】.
- Docker best practices for secrets and non-root user ([Best practices | Docker Docs
  ](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/#:~:text=)) ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=Running%20applications%20with%20user%20privileges,root%20user))】.
- GitHub Actions and Azure DevOps pipeline examples for building/pushing to AC ([Push a Docker image to Azure Container Registry using a GitHub ...](https://stuartmccoll.github.io/posts/2022-06-11-github-action-to-azure-container-registry/#:~:text=Push%20a%20Docker%20image%20to,server%3A%20%24%7B%7B%20secrets.ACR_REGISTRY_NAME%20%7D%7D.azurecr.io)) ([Create a service connection and build and publish Docker images to Azure Container Registry - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/publish-to-acr?view=azure-devops#:~:text=,%24%28tag))】.
- Azure Security Baseline recommending Key Vault for secret ([Azure security baseline for Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/virtual-machine-scale-sets-security-baseline#:~:text=Azure%20Key%20Vault%20for%20credentials,or%20secrets))】.
- Application Insights Java agent usage for monitoring Spring Boo ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=If%20you%27re%20using%20the%20exec,jar%22%60%20parameter%2C%20for%20example)) ([Application Insights with containers - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-get-started-supplemental#:~:text=COPY%20agent%2Fapplicationinsights))】.
- Azure VMSS Blue-Green deployment (VIP swap) discussio ([FAQ for Azure Virtual Machine Scale Sets - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#:~:text=in%20the%20same%20subscription%20and,between%20staging%20and%20production%20slots))】.
- Azure Site Recovery support matrix for VMSS (note on lack of support ([Azure VM Scale set cross regional DR - AZURE - KodeKloud - DevOps Learning Community](https://kodekloud.com/community/t/azure-vm-scale-set-cross-regional-dr/261714#:~:text=You%20can%20configure%20disaster%20recovery,doesn%E2%80%99t%20support%20VM%20scale%20sets))】.
