# Deploying React and .NET Core Docker Applications on Azure VMSS with Terraform

## 1. Introduction & Prerequisites

This guide provides a comprehensive, step-by-step walkthrough for **advanced developers** on deploying a React frontend and a .NET Core backend as Docker containers on **Azure Virtual Machine Scale Sets (VMSS)** using **Terraform**. We will cover everything from infrastructure provisioning to application containerization, deployment, scaling, monitoring, and best practices. By the end, you will have a deep understanding of how to set up a robust, scalable environment on Azure VMSS for containerized applications, using Infrastructure as Code (IaC) principles.

### Overview of Azure VMSS, Docker, and Terraform

**Azure Virtual Machine Scale Sets (VMSS)** allow you to create and manage a group of identical, load-balanced VMs. VMSS can automatically scale the number of VM instances based on demand or a defined schedule ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Azure%20virtual%20machine%20scale%20sets,more%20information%2C%20see%20%206)). This makes them ideal for applications that require elasticity and high availability. VMSS ensures that each VM (or **instance**) in the scale set is configured the same way, which is perfect for deploying container runtime environments consistently.

**Docker** is a containerization platform that packages applications and their dependencies into portable containers. Containers ensure that the React frontend and .NET Core API run in isolated, consistent environments across development, testing, and production. By containerizing these apps, you can run them on any machine with Docker, and achieve consistency from "dev" to "prod" ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Unlike)). In production, containers are typically orchestrated by platforms like Kubernetes, but VMSS offers a lightweight alternative for certain use cases where a full container orchestrator might not be necessary ([You can’t always have Kubernetes: running containers in Azure VM Scale Sets - Elton’s Blog](https://blog.sixeyed.com/you-cant-always-have-kubernetes-running-containers-in-azure-vm-scale-sets/#:~:text=Rule%20number%201%20for%20running,platform%20like%20Azure%20Container%20Instances)) ([You can’t always have Kubernetes: running containers in Azure VM Scale Sets - Elton’s Blog](https://blog.sixeyed.com/you-cant-always-have-kubernetes-running-containers-in-azure-vm-scale-sets/#:~:text=So%20far%2C%20so%20Kubernetes,IP%20address%20for%20each%20node)).

**Terraform** is an open-source Infrastructure as Code tool that allows you to define cloud resources in configuration files using HashiCorp Configuration Language (HCL). Terraform enables you to **define, preview, and deploy** infrastructure changes in a controlled manner ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Terraform%20enables%20the%20definition%2C%20preview%2C,plan%20to%20deploy%20the%20infrastructure)). With Terraform, you can describe Azure resources (like VM scale sets, virtual networks, etc.) in code, version them, and deploy reproducibly. This guide uses Terraform to provision Azure infrastructure (VMSS, networking, security groups, etc.), ensuring that the environment is codified and can be recreated or scaled reliably.

### Azure Account and Resource Setup

Before diving in, ensure you have the following **prerequisites** in place:

- **Azure Subscription**: You will need an active Azure subscription with sufficient permissions to create resources. If you don't have one, create a free account ([Create an Azure virtual machine scale set from a Packer custom image by using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-using-packer-hcl#:~:text=,free%20account%20before%20you%20begin)). All Azure resources (VMSS, VMs, networks, etc.) will be provisioned into this subscription. We will often reference a resource group where these resources will reside.

- **Resource Group**: Decide on a resource group name (e.g., `rg-vmss-demo`) and Azure region (e.g., `eastus` or `westus2`). The resource group organizes all related resources for this deployment. You can create it beforehand using Azure CLI or let Terraform create it.

- **Azure VMSS and Networking**: Familiarize yourself with the basics of VMSS and Azure networking. VMSS requires a virtual network and subnet to deploy VMs. We'll also use an Azure Load Balancer or Application Gateway to distribute traffic to VM instances, and possibly a jumpbox VM for admin access (especially if we secure VMSS instances in a private subnet). We will configure these with Terraform later.

- **Azure Container Registry (ACR)**: An Azure Container Registry will store our Docker images for the React and .NET applications. Ensure you have permissions to create an ACR instance or have an existing one. Using a private registry like ACR ensures your images are stored close to the deployment and can be accessed securely. We will push the Docker images to ACR as part of the CI/CD pipeline.

### Development Environment Prerequisites

On your development machine (or wherever you will run Terraform and build containers), install the following tools:

- **Azure CLI**: Install the Azure Command-Line Interface (CLI) and authenticate it with your Azure account. Azure CLI will be used for certain tasks like logging in, testing connectivity, or manually verifying resources. It can also be used in scripts to, for example, authenticate a VM to ACR using managed identities. Ensure the Azure CLI is up-to-date (`az --version` to check).

- **Terraform**: Install Terraform (v1.4+ recommended). Confirm it's installed by running `terraform version`. Terraform will provision Azure resources; it's recommended to configure it for your shell or use Azure Cloud Shell which has Terraform pre-installed ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=,11)). We will configure Terraform to use the Azure provider and set up backend state storage (to safely store the state file remotely).

- **Docker**: Install Docker Engine (or Docker Desktop if on Windows/Mac). Verify `docker --version` works. Docker is needed to build container images and test them locally. We will use Docker to containerize both the frontend and backend applications.

- **Kubernetes (optional)**: While not required for this guide (since we are focusing on VM Scale Sets, not Kubernetes), having **kubectl** or a local Kubernetes cluster (like kind or minikube) is optional. Advanced readers may use it to test container images on a Kubernetes cluster, but it is **not** needed for deploying to VMSS. We will ignore Kubernetes-specific instructions for this guide, as our focus is on Azure VMSS directly.

- **Node.js and .NET SDK**: To build the applications, install the latest LTS versions of Node.js (for React) and .NET SDK (for the .NET Core API). Although our Docker builds can also handle building the code, having these tools locally is useful for running and testing the apps before containerizing. For example:

  - Node.js 18+ (with npm or yarn) for creating and building the React app.
  - .NET 7 SDK (or .NET 6 LTS, or .NET 8 if available) for creating the Web API and running it locally.

- **Git**: A version control system (like Git) is assumed, as we will be discussing CI/CD pipelines (GitHub Actions or Azure DevOps). Our Terraform code and application code will ideally be in a git repository. Ensure Git is installed and you have a remote repository (GitHub or Azure DevOps project) set up for your code.

Once you have all tools installed, verify each one from the terminal:

```bash
# Azure CLI login
az login

# Terraform version check
terraform version

# Docker version check
docker version

# Node.js and npm version check
node -v && npm -v

# .NET SDK version check
dotnet --info
```

Make sure Azure CLI is logged in to the correct subscription (use `az account show` and `az account set -s <your-subscription-id>` if needed). Also, if using Azure DevOps or GitHub, ensure you have created or identified a project/repository for storing your IaC and app code.

### Setting Up Required Azure Resources

Before writing Terraform code, let's outline the Azure architecture we aim to create:

- **Virtual Network and Subnet**: A VNet to contain our VM scale set. The scale set instances (Ubuntu Linux VMs in this guide) will be launched in a dedicated subnet. For isolation, only the necessary ports will be allowed.

- **Network Security Group (NSG)**: To enforce network traffic rules. We'll use NSGs to allow inbound traffic on required ports (e.g., HTTP 80 and HTTPS 443 for the React app, maybe API port if directly exposed, or 22 for SSH on a restricted basis) and block other access. Security best practice is to minimize open ports: possibly we won't open SSH to the VMSS instances directly, using a jumpbox or Azure Bastion instead. Outbound internet access is needed for the VMs to pull images from ACR (or we attach a NAT gateway for controlled egress).

- **Load Balancer or Application Gateway**: With multiple VM instances, we'll use an Azure Load Balancer to distribute incoming traffic to the VMSS. The LB will have a public IP address and a rule for port 80/443 to forward to the VMSS instances. Optionally, an **Azure Application Gateway** could be used instead for layer-7 routing and TLS termination. In this guide, we'll illustrate using a basic Load Balancer for simplicity, but note that for production web workloads with TLS, Application Gateway or Azure Front Door is recommended to handle SSL certificates and more intelligent routing.

- **Azure Container Registry (ACR)**: If not already created, we'll provision an ACR to store Docker images for the frontend and backend. ACR will be in the same Azure region for performance. We will push our built images here, and configure the VMSS VMs to **pull from ACR** securely. We will leverage Azure Managed Identities so that the VMSS can authenticate to ACR without plaintext credentials ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Use%20the%20az%20role%20assignment,permissions%2C%20assign%20the%20AcrPush%20role)).

- **Virtual Machine Scale Set (VMSS)**: The VMSS itself, configured to use a VM image that has Docker installed (via custom image or cloud-init). Each VMSS instance will run the Docker containers for our applications. We'll configure the VMSS with an instance size (e.g., Standard_D2s_v3 or similar), a certain number of instances (initially maybe 1 or 2), and set up auto-scaling rules. We'll also attach the VMSS to the Load Balancer's backend pool so that new instances automatically register for load balancing.

- **Log Analytics Workspace**: For monitoring, we will set up a Log Analytics workspace. We will install the Azure Monitor agent on the VMSS instances (via extension) to collect logs and metrics, enabling **Azure Monitor VM Insights** for the scale set ([Integrate Virtual Machine Scale Sets with Azure Monitor and VMInsights using Terraform · Thorsten Hans' blog](https://www.thorsten-hans.com/integrate-virtual-machine-scale-sets-azure-monitor-vminsights-terraform/#:~:text=article%2C%20we%E2%80%99ll%20focus%20on%20VMSS%2C,and%20the%20Log%20Analytics%20stuff)) ([Integrate Virtual Machine Scale Sets with Azure Monitor and VMInsights using Terraform · Thorsten Hans' blog](https://www.thorsten-hans.com/integrate-virtual-machine-scale-sets-azure-monitor-vminsights-terraform/#:~:text=,extension)). This allows us to track performance (CPU, memory) and container logs if configured.

- **Jumpbox VM (optional)**: For management, we might deploy a small jumpbox VM (Linux or Windows) in the same VNet, which has a public IP for SSH/RDP. This machine can be used to SSH into the private VMSS instances if needed for debugging. In Terraform, we'll see an example of deploying such a VM (the Azure quickstart uses a "jumpbox" for SSH access to VMs in a private subnet ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=resource%20,tags)) ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=resource%20,Standard_DS1_v2))).

Now that we've set the stage, let's proceed to defining and provisioning this infrastructure using Terraform.

## 2. Infrastructure Setup with Terraform

In this chapter, we will build the Azure infrastructure using Terraform. This includes writing Terraform configuration files to define the VM scale set, networking components, security, and any supporting services. We will emphasize modular and reusable code design, and how to manage Terraform state safely.

**Key aspects we will cover:**

- Writing Terraform configurations for VMSS, including VM image selection (base image or custom image).
- Setting up networking (Virtual Network, Subnet, Load Balancer, NSG).
- Using Terraform **modules** or logical file separation for better organization.
- Remote state management to safely store Terraform state (e.g., in Azure Storage with locking ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=4))).
- Running Terraform commands to deploy the infrastructure.

Let's break down the Terraform setup into steps and components.

### Defining the Azure VM Scale Set in Terraform

Start by creating a directory for your Terraform configuration (e.g., `azure-vmss-terraform`). Inside, we'll have files like `main.tf`, `variables.tf`, `outputs.tf`, and separate files for resources (for clarity). We can also create subfolders for modules if needed.

**Provider Configuration**: In `main.tf`, configure the Azure provider and optionally the backend for state:

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"          # Replace with your state RG
    storage_account_name = "tfstateaccount"      # Your storage account for state
    container_name       = "tfstate"
    key                  = "vmss-demo.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}  # enable AzureRM features
}
```

In the above, we specify the Azure provider and also configure a backend pointing to an Azure Storage account (`tfstateaccount`) and container (`tfstate`) where the state file will live. Storing state in Azure Blob Storage enables state locking and prevents concurrent modifications ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=4)). **Note:** You must create the storage account and container beforehand (this can be done via Azure CLI or a one-time Terraform apply), and set the environment variable `ARM_ACCESS_KEY` to the storage key (or use managed identity for Terraform). This remote state ensures that if multiple team members or CI pipelines run Terraform, they use a shared state with locking to avoid conflicts.

**Resource Group and Key Variables**: Define variables for reuse, such as location and names, in `variables.tf`. For example:

```hcl
variable "location" {
  description = "Azure region for all resources"
  default     = "eastus"
}
variable "resource_group_name" {
  description = "Name of the resource group to create"
  default     = "rg-vmss-demo"
}
variable "vmss_name" {
  description = "Name of the Virtual Machine Scale Set"
  default     = "vmss-app"
}
# ... (other variables like VM size, admin username, etc.)
```

Then, create the resource group and network in Terraform:

```hcl
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}
```

**Virtual Network and Subnet**: We define a VNet and a Subnet for the VMSS:

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "vnet-vmss-demo"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
}
resource "azurerm_subnet" "vmss" {
  name                 = "subnet-vmss"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}
```

We use a **private address space** for the VNet (10.0.0.0/16 in this example) and allocate a /24 subnet for VMSS instances. You can adjust the IP ranges based on your organization's network plan or if integration with on-prem networks is needed (in advanced cases, consider using a VPN or ExpressRoute gateway, but not covered here).

**Network Security Group**: Next, create an NSG for the subnet or directly for the VMSS NICs. Here we attach it to the subnet (so it applies to all VMs in that subnet):

```hcl
resource "azurerm_network_security_group" "vmss" {
  name                = "nsg-vmss-demo"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "HTTP-Allow"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["80"]
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "HTTPS-Allow"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["443"]
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  # (Additional rules: e.g., allow SSH from specific IP, or allow internal backend API port if needed)
}
resource "azurerm_subnet_network_security_group_association" "vmss" {
  subnet_id                 = azurerm_subnet.vmss.id
  network_security_group_id = azurerm_network_security_group.vmss.id
}
```

This NSG has rules to allow HTTP (80) and HTTPS (443) from any source. In production, you might restrict source_address_prefix to known ranges (or use Azure Front Door/App Gateway as the only source). We could also add a rule for SSH (22) limited to your IP for debugging/maintenance, though if using a jumpbox or Azure Bastion, direct SSH to VMSS may not be needed. All other ports not explicitly allowed are implicitly denied by Azure at priority 65500.

**Load Balancer**: For the VMSS to receive traffic, we'll set up an Azure Load Balancer with a public IP:

```hcl
resource "azurerm_public_ip" "lb" {
  name                = "pip-vmss-demo"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "vmss" {
  name                = "lb-vmss-demo"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicFE"
    public_ip_address_id = azurerm_public_ip.lb.id
  }
}
resource "azurerm_lb_backend_address_pool" "bepool" {
  name                = "lb-backend-pool"
  resource_group_name = azurerm_resource_group.main.name
  loadbalancer_id     = azurerm_lb.vmss.id
}
resource "azurerm_lb_probe" "http_probe" {
  name                = "http-probe"
  resource_group_name = azurerm_resource_group.main.name
  loadbalancer_id     = azurerm_lb.vmss.id
  protocol            = "Http"
  port                = 80
  request_path        = "/"      # root path for probe (adjust if needed)
  interval_in_seconds = 15
  number_of_probes    = 3
}
resource "azurerm_lb_rule" "http_rule" {
  name                           = "http-rule"
  resource_group_name            = azurerm_resource_group.main.name
  loadbalancer_id                = azurerm_lb.vmss.id
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = azurerm_lb.frontend_ip_configuration[0].name
  backend_address_pool_id        = azurerm_lb_backend_address_pool.bepool.id
  probe_id                       = azurerm_lb_probe.http_probe.id
}
```

This creates a standard Load Balancer with a static public IP. It configures a health probe on port 80 (HTTP) and a rule forwarding traffic on port 80 to the backend pool (where VMSS instances will be). We could add a similar rule for 443 if we plan to handle TLS on the VMs (but if terminating TLS at the LB, we'd need an Application Gateway instead; standard LB at L4 cannot do TLS offload, so likely the VM or container handles TLS). For simplicity, we'll proceed with port 80 and assume either the React app is served on 80 or that TLS termination is handled elsewhere.

**Virtual Machine Scale Set Resource**: Now the main piece – define the VMSS in Terraform. We will use the `azurerm_virtual_machine_scale_set` resource. Key properties include VM instance SKU (size), capacity, admin credentials, OS image, and importantly, we will supply a custom cloud-init script or custom image to ensure Docker and our app containers run on startup.

Let's consider two approaches for VM image:

- Use a base image (like Ubuntu LTS) and supply a **cloud-init script (custom_data)** to install Docker and run containers at boot.
- Use a **custom image** (baked with Packer) that already has Docker (and possibly our container images preloaded or at least Docker installed and a startup script).

We'll illustrate using a base Ubuntu image with cloud-init (as it's straightforward), and discuss custom image in the next section.

```hcl
resource "azurerm_virtual_machine_scale_set" "app" {
  name                = var.vmss_name
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  zones               = [1, 2, 3]  # Use availability zones for resiliency if region supports it
  sku {
    name     = "Standard_DS1_v2"   # VM size (1 vCPU, 3.5GB RAM for example)
    tier     = "Standard"
    capacity = 2                  # start with 2 instances
  }
  upgrade_policy {
    mode = "Manual"               # Manual upgrade so we control deployments (could use Automatic)
  }

  admin_username                  = "azureuser"
  admin_password                  = random_password.vmss_admin.result   # if using password auth (or use SSH keys)
  disable_password_authentication = false

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name_prefix = "vmss-instance"
    custom_data          = filebase64("cloud-init.txt")
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }

  network_profile {
    name    = "vmss-network-profile"
    primary = true
    ip_configuration {
      name                                   = "ipconfig"
      subnet_id                              = azurerm_subnet.vmss.id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.bepool.id]
      primary                                = true
    }
  }

  health_probe_id = azurerm_lb_probe.http_probe.id

  tags = {
    Environment = "Demo"
    Application = "ReactDotNetApp"
  }
}
```

A lot is happening here:

- `zones` spreads instances across AZs 1, 2, 3 for high availability (optional; only in regions with AZ support and using Uniform VMSS).
- `sku` defines the VM size and initial count (2 instances). Choose a VM size that can comfortably run Docker and your containers (Standard_DS1_v2 is small; for more load, DS2_v2 or DS3_v2 might be better).
- `upgrade_policy.mode` is "Manual", meaning if we update the model (e.g., new custom_data or image), Azure won't automatically reboot all VMs; we will manually apply upgrades. This gives us control to coordinate deployments (Automatic could also be used to automatically roll out changes, but manual is safer for controlled deployment).
- `admin_username` and `admin_password` (or `admin_ssh_key`). Here for demo we use a random password generated via a `random_password` resource (not shown, but Terraform can generate a random password and we output it or store securely). In real scenarios, use SSH keys for Linux VMs or Azure AD login, and avoid passwords.
- `source_image_reference` picks Ubuntu 18.04 LTS (as example; could use 20.04 or 22.04 LTS depending on support and compatibility with Docker).
- The **custom_data** field under `os_profile` is where we provide a base64-encoded cloud-init script (`cloud-init.txt` file in the same directory). This script runs on VM boot to install Docker and start our containers. We'll detail this script soon.
- The network profile attaches the VMSS NICs to our subnet and the Load Balancer backend pool. Each VM instance will get an IP in the subnet and register with the LB. We set `primary = true` as there's one NIC per VM.
- `health_probe_id` links the VMSS to the LB’s health probe for instance health monitoring. Azure will use this to determine if VM instances are healthy (if a VM fails the probe, LB stops sending traffic).
- Tags are optional but good practice for resource management.

Now, let's create the `cloud-init.txt` that the VMSS will use (since we referenced it in custom_data). This is a crucial piece: it will configure the VM on startup. We'll use it to install Docker and run our containers. Create a file `cloud-init.txt` with the following content:

<details>
<summary><strong>cloud-init.txt (User Data Script)</strong></summary>

```yaml
#cloud-config
package_upgrade: true
packages:
  - docker.io
  - azure-cli
runcmd:
  # Login to Azure using managed identity and login to ACR
  - [bash, -c, "az login --identity"]
  - [bash, -c, "az acr login --name <YOUR_ACR_NAME>"]
  # Pull and run the Docker images
  - [bash, -c, "docker pull <YOUR_ACR_NAME>.azurecr.io/react-app:latest"]
  - [bash, -c, "docker pull <YOUR_ACR_NAME>.azurecr.io/dotnet-api:latest"]
  - [
      bash,
      -c,
      "docker run -d --restart always -p 80:80 <YOUR_ACR_NAME>.azurecr.io/react-app:latest",
    ]
  - [
      bash,
      -c,
      "docker run -d --restart always -p 5000:5000 <YOUR_ACR_NAME>.azurecr.io/dotnet-api:latest",
    ]
```

</details>

Let's break down this cloud-init:

- It is in cloud-config format (YAML). We update apt packages and install `docker.io` (Docker Engine) and Azure CLI (`azure-cli` package) on the VM. Installing Docker at boot ensures the VM can run containers. This approach means provisioning will take a bit longer (since apt has to download these on each new instance). In a later section, we will discuss using Packer to bake these in a custom image for speed.
- In `runcmd`, we have commands to:
  1. Use Azure CLI to login with the VM's **managed identity** (`az login --identity`). This command fetches an Azure AD token for the VM's system-assigned identity, allowing subsequent CLI commands to run under that identity.
  2. Then `az acr login --name <Registry>` logs into our Azure Container Registry. Because we gave the VM's identity the "AcrPull" role on the registry, this command will succeed without needing a username/password ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Then%2C%20authenticate%20to%20the%20registry,command%20and%20docker%20commands%20with)). After this, the Docker daemon on the VM can pull images from ACR seamlessly, as the token is cached by Azure CLI for Docker use.
  3. Pull the two images: one for the React app and one for the .NET API. We assume these are tagged as `react-app:latest` and `dotnet-api:latest` in our ACR. (Later, in CI/CD, we'll push these images.)
  4. Run the containers:
     - The React container is run detached (`-d`), always restart, mapping host port 80 to container port 80. (If our React container is an Nginx serving on 80, this serves the web content).
     - The .NET API container is run similarly on port 5000. _Note:_ Exposing 5000 on VM might not be necessary if the React app calls the API through the same host (since both run on same VM, one could call `localhost:5000`). However, because our LB is only forwarding port 80, the API wouldn't be accessible externally through the LB unless we add another LB rule for 5000. In a real deployment, you'd likely have the React app call the API via an internal endpoint or through the same domain (with the API proxied). For simplicity, let's assume the React app makes API calls via relative path or something and maybe we configure Nginx to proxy to the API, or they are separate services accessible via different ports. We can refine this later.
     - The `--restart always` ensures the containers restart if they crash or if the VM reboots.

With this cloud-init, any new VM instance in the scale set should automatically come up, install Docker, login to ACR, and start the two containers. This means scaling out will automatically run the needed workloads on each new VM. The approach uses Azure CLI on the VM, which is a bit heavy; an alternative is to use Docker's ability to login with a service principal or a lightweight script to get a token. But using Azure CLI is straightforward and works for our scenario.

**Important**: Replace `<YOUR_ACR_NAME>` with the name of your Azure Container Registry. Ensure that the VMSS has a **system-assigned managed identity** and that identity has **AcrPull** role on the ACR. We haven't yet added the identity in the Terraform VMSS resource. We should add:

```hcl
identity {
  type = "SystemAssigned"
}
```

inside the `azurerm_virtual_machine_scale_set` resource. This gives each VM an identity in Azure AD. Then, separately, we must create a role assignment:

```hcl
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_virtual_machine_scale_set.app.identity[0].principal_id
}
```

We will define the ACR resource in Terraform soon; once we do, this role assignment grants the VMSS's identity permission to pull from the registry ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Use%20the%20az%20role%20assignment,permissions%2C%20assign%20the%20AcrPush%20role)).

Before that, let's define the **Azure Container Registry** in Terraform:

```hcl
resource "azurerm_container_registry" "acr" {
  name                     = "acrvmssdemo"  # must be globally unique in Azure
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.location
  sku                      = "Basic"        # Basic, Standard, Premium available
  admin_enabled            = false          # We will use managed identity, no admin user
  georeplication_locations = []             # (optional replication regions)
}
```

We disable the admin user (which provides a username/password for the registry) to enforce use of Azure AD authentication. With admin_enabled=false, the only way to push/pull is via Azure AD tokens (which our pipeline and VM will use).

Now our Terraform config includes:

- Resource Group
- VNet/Subnet
- NSG + association
- Public IP, Load Balancer (with frontend, backend pool, probe, rule)
- VMSS (with custom_data, identity)
- ACR
- Role assignment for VMSS identity on ACR.

We should also consider outputting some useful information in `outputs.tf`, for instance:

```hcl
output "lb_public_ip" {
  description = "Public IP of the load balancer"
  value       = azurerm_public_ip.lb.ip_address
}
output "vmss_instances" {
  description = "VMSS instance count and IDs"
  value       = azurerm_virtual_machine_scale_set.app.instances
}
```

(The `instances` attribute gives details about each instance, or we can output the VMSS name or resource IDs for reference.)

At this point, our Terraform code is ready. The next steps:

1. Run `terraform init` to install the Azure provider and initialize backend ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Run%20terraform%20init%20to%20initialize,to%20manage%20your%20Azure%20resources)).
2. Run `terraform plan` to review the resources that will be created ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Run%20terraform%20plan%20to%20create,an%20execution%20plan)).
3. Run `terraform apply` to create the infrastructure ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Run%20terraform%20apply%20to%20apply,plan%20to%20your%20cloud%20infrastructure)). Terraform will provision all the Azure resources in the correct order, thanks to implicit dependencies (e.g., VMSS depends on subnet, LB, etc, which depends on IP, which depends on RG).
4. After apply, Terraform will output the Load Balancer's public IP. You can test it (though at this stage, our VMSS might not have the application running yet if we haven't pushed images to ACR. If the images don't exist, the docker run will fail on the VM, but we can push them next in the guide).
5. Use `az vmss list-instances` or Azure Portal to verify the VMSS instances are up, and perhaps SSH into one (via jumpbox or using `az vmss ssh` extension) to verify Docker is running.

We have successfully defined our core infrastructure. Next, we will focus on the applications themselves: building the React and .NET apps into Docker images and making them available for the VMSS to pull.

### Using Terraform Modules for Reusability

Before moving on, a note on Terraform code organization: In our configuration, we've kept everything in a few files for clarity. However, as projects grow, it's wise to use modules to encapsulate and reuse components. For example, you might create:

- A Terraform module for "networking" that sets up the VNet, subnets, NSG, and maybe the load balancer.
- A module for "vmss_app" that sets up the VMSS and related pieces (maybe taking inputs like the image ID or custom data script, number of instances, etc.).
- A module for "acr" if you reuse registry setup logic.

Using modules promotes reusability and cleaner structure. For instance, HashiCorp's reference tutorial separates network and compute into different files like `network.tf` and `compute.tf` for clarity ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=,for%20the%20scale%20set%20with)). You could further convert those into child modules.

If writing your own modules, organize them in a `modules/` directory. For example, a `modules/vmss` could have its own `main.tf` (with VMSS resource), `variables.tf` (for inputs like vmss_name, image_id, etc.), and `outputs.tf`. Then your root configuration would instantiate it:

```hcl
module "app_vmss" {
  source              = "./modules/vmss"
  vmss_name           = var.vmss_name
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.vmss.id
  lb_backend_pool_id  = azurerm_lb_backend_address_pool.bepool.id
  image_id            = var.custom_image_id  # if using custom image
  acr_name            = azurerm_container_registry.acr.name
  acr_id              = azurerm_container_registry.acr.id
  admin_username      = "azureuser"
  admin_ssh_key       = file("~/.ssh/id_rsa.pub")  # just an example
  instance_count      = 2
  vm_size             = "Standard_DS2_v2"
  ...
}
```

Inside the module, you'd reference those variables to create the VMSS and perhaps the role assignment. This way, if you needed to deploy another scale set (say for another environment or another app), you could reuse the module easily.

Additionally, consider using official or community Terraform modules. For Azure, there are modules published that handle common patterns (e.g., network setup or VMSS creation). For instance, the Azure Terraform provider documentation provides examples and some community modules (like `terraform-azurerm-vmss` on GitHub). If using a well-maintained module, you can reduce code and focus on inputs/outputs.

However, be cautious and ensure you understand the module's behavior, as abstraction can sometimes obscure important details needed for debugging.

### Managing Terraform State and Backend

We configured an Azure backend for Terraform state to ensure reliability and team collaboration. A few best practices for state:

- **Remote State in Azure Storage**: Storing state in Azure Blob Storage keeps it secure and centralized. Azure Storage automatically locks the state file during Terraform operations ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=4)), preventing concurrent applies that could corrupt state. Data in Azure Storage is encrypted at rest by default, adding security.

- **State Access Controls**: Restrict access to the storage account/container where state is kept. Ideally, use a separate resource group or storage account just for state with tightly controlled access (only CI service principal and key team members). Do not expose the state container publicly. Following best practices, the state container should have public access disabled and perhaps use a private endpoint if strict network controls are required.

- **Backend Configuration**: We put the backend config directly in Terraform. Alternatively, you can supply backend config via CLI or partial config and environment variables, which avoids hardcoding secrets (we recommended using `ARM_ACCESS_KEY` env var for the storage key ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=,access_key%3A%20The%20storage%20access%20key)) ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=Key%20points%3A)) so that it isn't in code). If using Terraform Cloud or Enterprise, you could use that as a backend instead, which offers its own state management and locking.

- **State Locking and Unlocking**: Terraform will lock state when you run apply. In Azure backend, if a process crashes and a lock remains, you might need to manually remove the lock via Azure Portal (the lock is an Azure blob lease). This is rare, but good to know for troubleshooting.

- **Sensitive Data**: Never commit the `*.tfstate` file to source control. The backend configuration we used prevents a local state file from being created (once initialized). If you ever run Terraform locally without backend (say, for quick test), be mindful of secrets in state (like passwords). Our config included an admin password for VMSS (via random_password). That would reside in state. Storing state remotely with controlled access mitigates exposure.

- **Terraform Cloud/Enterprise**: As an alternative to Azure storage, Terraform Cloud can be used to store state and run plans. In that case, you wouldn't need to manage storage accounts, but you would need to set up an Azure service principal for Terraform Cloud to use. This can integrate with CI pipelines nicely as well.

Having the backend configured, each team member or pipeline just needs the backend block and appropriate environment variables to access it. This way, everyone works off the same state.

In summary, our infrastructure is now defined in Terraform configuration files. We can build and adjust it using Terraform commands. In the next sections, we will focus on the application side: building Docker images for our React and .NET applications, pushing them to ACR, and then tying everything together with continuous deployment and scaling configurations.

## 3. Building & Containerizing Applications

With the Azure infrastructure in place (or at least defined), the next step is to build our applications and containerize them with Docker. We have two applications:

- A **React** frontend application.
- A **.NET Core** (ASP.NET Core) backend API.

We'll walk through creating simple versions of these apps, writing Dockerfiles for each, and testing them locally using Docker Compose. By containerizing both, we ensure they run consistently on any host (our local machine, or the Azure VMs). This also simplifies deployment to VMSS since the VM instances just need Docker to run our pre-built images.

### Creating a React Frontend Application

For the purpose of this guide, we'll create a sample React application. You can create one using **Create React App** or any preferred React setup. For example, using Create React App:

```bash
npx create-react-app my-app-frontend
```

This will generate a React project in the `my-app-frontend` directory. Inside, you can create a simple component that, say, fetches data from our .NET API and displays it, or just displays "Hello World" for now. Since the focus is deployment, we won't delve deep into React coding. Ensure the app runs with `npm start` locally first.

Now, let's write a **Dockerfile** to containerize this React app. We will use a multi-stage Docker build to optimize the image size and serve the app using Nginx (for production).

Create a file `Dockerfile` in the React app directory with the following content:

```Dockerfile
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
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Explanation:**

- We use Node 18 (alpine variant for smaller size) to install dependencies and build the React static files. The `npm run build` command creates an optimized production build in the `build/` directory.
- Then we use an Nginx alpine image, copy the build files into Nginx's web root, expose port 80, and run Nginx. This is a standard pattern for containerizing React frontends ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Exposes%20port%2080)).
- Multi-stage builds ensure the final image contains only Nginx and the static files, not the Node runtime or source code, which keeps it lean and secure ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)).

We should also create a `.dockerignore` file in the React project to avoid copying unnecessary files (node_modules, etc.) during build:

```
node_modules
Dockerfile
.git
.gitignore
```

This prevents large or irrelevant files from being sent to the Docker daemon.

To test the Dockerfile, from the `my-app-frontend` directory, run:

```bash
docker build -t react-app:latest .
```

This will produce a `react-app:latest` image locally. Then test it:

```bash
docker run -p 3000:80 react-app:latest
```

(We map to 3000 just to not require root privileges for binding 80, or you can do `-p 80:80` if allowed. The app should be accessible at http://localhost:3000 or http://localhost if using 80.)

If everything is correct, you should see your React app's content in the browser.

_Note on environment configuration:_ If your React app needs to communicate with the .NET API, consider the base URL. In development, you might use a proxy or different port. In production (in the container), since our plan is to have both containers on the same VM or accessible via the same load balancer (maybe different ports), you'll want to configure the React app to call the correct API endpoint. One approach is to use environment variables at build time or runtime. For example, you could set a placeholder in your React code for `API_URL` and replace it during CI or use a custom startup script to inject it. For simplicity, let's assume the React app will call the API via a relative path on the same domain (which could be configured if we route traffic accordingly). We'll revisit this when considering our deployment architecture (perhaps using Nginx to reverse proxy to the API container).

### Creating a .NET Core Backend API

Next, we create a .NET Core Web API project. Using the .NET CLI:

```bash
dotnet new webapi -o MyApi
```

This creates a new ASP.NET Core Web API project in the `MyApi` directory. It comes with a sample WeatherForecast controller by default (if .NET 6 or 7, you'll see a default example).

For our guide, we can use the default template or simplify it. The key is that it should run on a certain port and respond to requests. By default, an ASP.NET Core app will listen on port 5000 (HTTP) and 5001 (HTTPS) in development. In a container, we can configure it to listen on 5000 (we exposed 5000 in our cloud-init run command).

We might want to ensure that in `appsettings.Production.json`, Kestrel is configured to listen on 0.0.0.0 and port 5000 (so it's reachable from outside container if needed). In .NET 6+, this might be automatically handled by environment variables (`ASPNETCORE_URLS=http://+:5000`). We can set that in Dockerfile or docker-compose to be safe.

Let's write a Dockerfile for the .NET API with a multi-stage build:

```Dockerfile
# .NET 7 SDK (Build stage)
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY ["MyApi.csproj", "./"]
RUN dotnet restore "MyApi.csproj"
COPY . .
RUN dotnet publish -c Release -o /app/publish

# .NET 7 Runtime (Runtime stage)
FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
# Set environment to listen on port 5000
ENV ASPNETCORE_URLS=http://+:5000
EXPOSE 5000
ENTRYPOINT ["dotnet", "MyApi.dll"]
```

**Explanation:**

- We use the official .NET SDK image to build the project (restore packages and publish the app in Release mode).
- Then use the ASP.NET Core runtime image (which is smaller) to run the app.
- We set `ASPNETCORE_URLS` to ensure the app listens on port 5000 on all network interfaces. This aligns with our earlier plan to expose 5000 for the API.
- Expose 5000 for documentation (this is optional as it doesn't do anything by itself except inform).
- Then run the app with `dotnet MyApi.dll`.

Build this image:

```bash
docker build -t dotnet-api:latest .
```

(from the directory containing the Dockerfile and the .csproj, etc., likely the `MyApi` directory).

Test it:

```bash
docker run -p 5000:5000 dotnet-api:latest
```

The API should start. You can browse to http://localhost:5000/swagger (the template has Swagger by default) or http://localhost:5000/WeatherForecast (if using the default WeatherForecast controller) to see if it returns data. If it works, our containerized API is functional.

### Using Docker Compose for Local Testing

Individually running the frontend and backend containers is fine, but we should also test them together to mimic how they'll work in Azure. We can use **Docker Compose** to run both containers with one command and define their network.

Create a `docker-compose.yml` file at the root of your project (outside both app directories, for example):

```yaml
version: "3.8"
services:
  backend:
    build:
      context: ./MyApi
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - ASPNETCORE_URLS=http://+:5000
    networks:
      - app-net

  frontend:
    build:
      context: ./my-app-frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-net
```

In this compose file:

- We define two services: `backend` and `frontend`.
- Each service builds from the corresponding directory (assuming those contain the Dockerfile for each).
- The backend exposes port 5000, the frontend exposes port 80.
- We put them on the same network `app-net` so they can communicate.
- The `depends_on` ensures the backend starts before the frontend (though not strictly ensuring availability, but order).
- We set the environment for backend (though our Dockerfile already did, but this shows another way).

Now run `docker-compose up --build`. This will build both images (tagged as projectname_frontend and projectname_backend by default) and run them.

Test the integration:

- The React app should be accessible on http://localhost (port 80).
- If the React app tries to call the API, how will it reach it? Since they share a network, the frontend container can reach `backend:5000` (using the service name as DNS). But in the browser (outside container), if the React code calls `http://localhost:5000`, that would hit the host's port which is forwarded to backend. If it calls relative paths, the request will go to the same domain (localhost) on port 80, which would hit the frontend container (not correct). So, one solution is to configure the React app to proxy API calls to the backend. In development, CRA has a proxy feature. In production, since we are serving via Nginx, one could configure Nginx to reverse proxy certain paths to the backend service. Alternatively, expose the backend via another port (5000) on the LB and have the React app use the same domain but different port. This is a design choice:
  - _Simplest:_ React app calls a different subdomain or port for API. E.g. have users call api on port 5000 (which would require LB rule for 5000). But if port 5000 is not open externally, that fails.
  - _Better:_ Serve both behind one domain and path: e.g. requests to `/api/*` are forwarded to backend. With App Gateway, this is easy. With just an L4 LB, not so straightforward.
  - _Nginx proxy:_ We could run Nginx not just to serve static files, but also as a reverse proxy to the API container (which could even run on the same VM without exposing external port). This is advanced but doable by customizing the Nginx config in the frontend container.

For this guide, to avoid diving deep into Nginx config, let's assume the API is exposed on port 5000 and we document that in production we might access it via that port. Maybe our frontend isn't calling the API directly (if not needed) or we mention that a full integration would involve additional setup.

Anyway, ensure both containers run and can serve their respective content. If both are working in compose, that's a good sign for deploying to Azure.

We have containerized the applications. Next, we need to integrate this with our Azure deployment:

- We'll push the images to ACR.
- Ensure the VMSS cloud-init is pulling the correct image tags from ACR.
- Set up continuous integration so that building and pushing images, as well as updating Terraform (if needed), can happen automatically.

Before moving to the next section, let's summarize:

- We built a React app and containerized it using a multi-stage Docker build to get an Nginx-serving image. This approach yields a smaller, production-ready image ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)).
- We built a .NET Core API and containerized it using a multi-stage build (SDK -> runtime), which is a best practice for .NET containers to minimize size and include only runtime dependencies ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=The%20sample%20Dockerfile%20uses%20the,in%20Docker%20Hub%20by%20Microsoft)) ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=)).
- We tested using Docker Compose, which simulates how the two services run together, ensuring our configuration (ports, network) is correct.

With application containers ready, we can now focus on deploying these containers to our Azure VMSS environment.

## 4. Deployment on Azure VMSS

Now it's time to deploy our containerized applications on the Azure VM Scale Set. This involves a few steps:

- (Optional) Creating a custom VM image with Packer that has Docker (and possibly our images) pre-installed.
- Setting up a CI/CD pipeline (with GitHub Actions or Azure DevOps) to build and push the Docker images to Azure Container Registry.
- Using Terraform (possibly triggered in the pipeline) to deploy or update the VMSS.
- Ensuring that the VMSS instances pull the new images and run them.

We'll start by discussing the creation of a custom VM image, which can streamline deployment, and then move into CI/CD and automation.

### Creating a Custom Image with Packer (Optional)

In our Terraform config, we chose to use an Ubuntu base image and cloud-init to install Docker and run containers at boot. This works but has a disadvantage: each time a VM boots (especially the first instance of a new scale set or when scaling out), it spends time downloading and installing Docker and Azure CLI, etc. If the installation or ACR login fails for some reason, the instance might not come up correctly. Moreover, the provisioning adds to the instance startup time.

To mitigate this, we can use **Packer** to create a custom image that already has Docker (and even Azure CLI, and any other dependencies) installed. We could even pre-pull the application images into the VM image (though that might make the image large and stale quickly; usually better to just have Docker and let it pull fresh containers).

**Packer** allows us to script the creation of VM images. You can create an image from a base (Ubuntu) and run provisioners (shell scripts, etc.) to install software, then capture that image for use in VMSS. Azure supports custom images which can be stored in a resource group or shared via Azure Compute Gallery.

Let's outline a simple Packer template for our scenario:

- Base image: Ubuntu 18.04 or 20.04 LTS.
- Provisioning steps: Install Docker, install Azure CLI, maybe do `az login --identity` (can't really do that in image build because identity is at VM runtime) but we can ensure CLI is there. We could also copy our cloud-init script into the image or set it up as a systemd service.
- Possibly, as a final step, run `docker pull` for our images (but that would require the image to know ACR credentials at build time, which is complex. Better to skip pulling app images in the baked image; just ensure Docker is ready).
- Output: Azure managed image.

Packer has an Azure builder that can create an image and directly output an Azure image resource. Terraform can then reference that image for VMSS.

**Packer Template Example (HCL format)**:
Packer now supports HCL2 configuration files. We could create a file `ubuntu.pkr.hcl`:

```hcl
variable "azure_subscription_id" {}
variable "azure_client_id" {}
variable "azure_client_secret" {}
variable "azure_tenant_id" {}

source "azure-arm" "ubuntu_docker" {
  communicators       = ["ssh"]
  subscription_id     = var.azure_subscription_id
  client_id           = var.azure_client_id
  client_secret       = var.azure_client_secret
  tenant_id           = var.azure_tenant_id

  managed_image_resource_group_name = "rg-vmss-demo"   # or separate RG for images
  managed_image_name                = "vmssDockerImage"
  managed_image_location            = "East US"

  os_type       = "Linux"
  image_publisher = "Canonical"
  image_offer     = "UbuntuServer"
  image_sku       = "18.04-LTS"
}

build {
  name = "ubuntu-docker-image"
  sources = ["source.azure-arm.ubuntu_docker"]

  provisioner "shell" {
    inline = [
      "apt-get update",
      "apt-get upgrade -y",
      "apt-get install -y docker.io azure-cli",
      "systemctl enable docker"   # ensure docker starts on boot
    ]
  }
}
```

This is a simplified example. You would supply your Azure service principal credentials via variables to let Packer authenticate (or use Azure CLI login or managed identity if running in Azure Cloud Shell). The provisioner installs Docker and Azure CLI, and enables Docker. We could expand the provisioner to also add our user-data script to the image or create a service to run Docker containers on start. However, typically one might still use cloud-init at runtime for final steps, or use Azure Custom Script Extension at deployment time.

Alternatively, we can embed a startup script in the image. For example, create a script that does the `az login` and `docker run` steps and place it in `/etc/init.d` or a systemd unit. This way, the image, when booted, will automatically run that startup script. This might complicate updates (e.g., if image has the container versions hardcoded, updating would require new image).

Given the complexity, a middle ground:

- Use Packer to get an image with Docker and all necessary runtime installed (so no need for cloud-init to apt-get).
- Still use cloud-init or a custom script extension at deployment to run the latest containers.

This speeds up provisioning (since installing Docker is done once in the image) and reduces boot time variance. It also isolates the install steps (if Docker installation fails, Packer will catch it before deployment to prod).

Let's assume we've created a custom image using Packer and it's available as `rg-vmss-demo/providers/Microsoft.Compute/images/vmssDockerImage`. In Terraform, we can reference this instead of the public Ubuntu image:

```hcl
resource "azurerm_image" "custom" {
  name                = "vmssDockerImage"
  resource_group_name = azurerm_resource_group.main.name
}
# The above data resource isn't necessary if we know the image ID, but can be used if Packer just created it.

# In VMSS:
storage_profile_image_reference {
  id = azurerm_image.custom.id
}
```

By specifying `storage_profile_image_reference.id`, Terraform knows to use that image for the VMSS instances. We would remove `custom_data` in this case if the image itself handles container startup (or we still keep a minimal custom_data to run containers if not baked in image).

For example, maybe we still rely on cloud-init for `az acr login` and `docker run`. If Docker is already installed, cloud-init script becomes shorter (no need to install docker, just run commands). That might be acceptable. Or we could incorporate those commands in a systemd unit in the image that pulls on boot referencing some metadata (which would be complicated to change per deployment, so maybe not).

Given this is an advanced topic, one could implement either approach. For completeness, ensure to mention that using a custom image significantly reduces provision time ([Deploy an application to an Azure Virtual Machine Scale Set - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-deploy-app#:~:text=When%20you%20use%20one%20of,those%20configuration%20scripts%20and%20tasks)) by avoiding repetitive installation on each instance.

To summarize this sub-section:

- Packer can be used to create a custom VM image pre-installed with Docker (and other tools). This image can be specified in Terraform for the VMSS ([Deploy an application to an Azure Virtual Machine Scale Set - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-deploy-app#:~:text=When%20you%20use%20one%20of,those%20configuration%20scripts%20and%20tasks)).
- Using a custom image is recommended for faster scaling and consistency if you frequently create/destroy VMSS instances.
- Packer templates can include provisioners (shell scripts) to install required software (e.g., the example above installed Nginx; similarly we install Docker) ([Create an Azure virtual machine scale set from a Packer custom image by using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-using-packer-hcl#:~:text=inline%20%3D%20%5B%20%22apt,y%20install%20nginx)).
- If including application artifacts in the image, you would rebuild the image for each app update. This is possible (some pipelines build a new image with the updated app container baked in), but an alternative is to just bake the runtime and always fetch the latest container on boot.

For the rest of this guide, we'll assume either approach works. We'll proceed with the cloud-init approach we set up, but keep in mind that Packer could optimize it. We will include additional references or triggers in our pipeline to optionally build a Packer image if needed.

### Setting up CI/CD Pipelines (GitHub Actions or Azure DevOps)

To streamline deployment, let's set up a continuous integration/continuous deployment (CI/CD) pipeline. This pipeline will:

1. **Build the Docker images** for the React and .NET applications (and run tests if any).
2. **Push the images to Azure Container Registry**.
3. **Deploy infrastructure changes** using Terraform (if there are changes to the infrastructure or to trigger a redeployment of containers).

We can implement this pipeline using:

- **GitHub Actions**: if our code is in a GitHub repo.
- **Azure DevOps** (Azure Pipelines): if using Azure DevOps.
  The steps are similar; the syntax differs.

Let's outline a GitHub Actions workflow as an example. In your repository, create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy to Azure VMSS

on:
  push:
    branches: [main]

env:
  AZURE_RESOURCE_GROUP: rg-vmss-demo
  AZURE_REGION: eastus
  ACR_NAME: acrvmssdemo
  VMSS_NAME: vmss-app

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ env.ACR_NAME }}.azurecr.io
          username: ${{ secrets.AZURE_CLIENT_ID }}
          password: ${{ secrets.AZURE_CLIENT_SECRET }}

      - name: Build and push frontend image
        uses: docker/build-push-action@v4
        with:
          context: ./my-app-frontend
          file: ./my-app-frontend/Dockerfile
          push: true
          tags: ${{ env.ACR_NAME }}.azurecr.io/react-app:${{ github.sha }}

      - name: Build and push backend image
        uses: docker/build-push-action@v4
        with:
          context: ./MyApi
          file: ./MyApi/Dockerfile
          push: true
          tags: ${{ env.ACR_NAME }}.azurecr.io/dotnet-api:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_wrapper: false

      - name: Initialize Terraform
        run: terraform init

      - name: Apply Terraform (Deploy VMSS)
        run: |
          terraform apply -auto-approve \
            -var image_tag=${{ github.sha }}
```

Let's explain this workflow:

- It triggers on push to main (adjust branch as needed).
- It has two jobs: `build-and-push` and `deploy`. The deploy job depends on build-and-push (so it waits for images to be pushed).
- In build-and-push:
  - We log in to ACR using Azure credentials (here using a service principal's ID and secret stored as GitHub secrets). Alternatively, one could use an Azure CLI action to login to Azure and then use `az acr login` but the docker-login action is straightforward.
  - We build and push the frontend and backend images to ACR. We tag them with the Git commit SHA (or you could use a build number or `latest` tag). Using a unique tag (like the commit hash) is good for immutability. We could also tag `latest` if we want the cloud-init to always pull latest; but referencing specific tags is more controlled.
- In deploy:
  - We log in to Azure (the `AZURE_CREDENTIALS` secret would contain a JSON of service principal credentials).
  - Set up Terraform CLI.
  - Run `terraform init` and then `terraform apply`. We pass a variable `image_tag` to Terraform.

Now, we need to modify our Terraform to use that `image_tag` variable in the VMSS custom_data. Instead of hardcoding "latest" in cloud-init, we could templify it. For example, in our cloud-init.txt, replace hardcoded image tags with a placeholder (or use Terraform templatefile). Simpler: pass the tag into Terraform and use it via `templatefile` function to generate the custom_data.

For instance, in Terraform:

```hcl
variable "image_tag" {
  description = "Docker image tag for the deployment"
  default     = "latest"
}
data "template_file" "cloud_init" {
  template = file("${path.module}/cloud-init-template.txt")
  vars = {
    acr_name  = azurerm_container_registry.acr.name
    image_tag = var.image_tag
  }
}
```

And in the VMSS:

```hcl
os_profile {
  ...
  custom_data = base64encode(data.template_file.cloud_init.rendered)
}
```

Where `cloud-init-template.txt` has something like:

```yaml
#cloud-config
---
runcmd:
  - [bash, -c, "docker pull ${acr_name}.azurecr.io/react-app:${image_tag}"]
  - [bash, -c, "docker pull ${acr_name}.azurecr.io/dotnet-api:${image_tag}"]
  - [
      bash,
      -c,
      "docker run -d --restart always -p 80:80 ${acr_name}.azurecr.io/react-app:${image_tag}",
    ]
  - [
      bash,
      -c,
      "docker run -d --restart always -p 5000:5000 ${acr_name}.azurecr.io/dotnet-api:${image_tag}",
    ]
```

This way, when we run `terraform apply -var image_tag=commitsha`, it will embed that tag into the startup script. That triggers an update to the VMSS model (because custom_data changed). Since we set `upgrade_policy_mode = Manual`, Terraform will likely create a new VMSS instance or mark for upgrade. Actually, with VMSS, if the model changes and mode is Manual, the instances won't automatically update. We might need to call `az vmss rolling-upgrade` or do a manual instance refresh. If mode was Automatic, Terraform apply would cause a rolling upgrade of the instances with the new custom_data.

We have two strategies:

- Use **Automatic upgrade policy**: then each apply triggers Azure to roll out changes (reimage or reapply custom data).
- Use Manual and explicitly manage upgrades:
  - One way is to force instance recreation by changing some property that causes it, or use the VMSS API to upgrade.
  - Or incorporate a script or Azure CLI in pipeline to do `az vmss update-instances --instance-ids *` or similar after apply.

For simplicity, let's consider setting mode to **Automatic** during CI deployments so new images roll out. Automatic will slowly update all instances to the new model (you can specify `max_batch_instance_percent` etc. in Terraform to control rollout speed, which is advanced but available in the resource). We'll assume default rollout is fine (it usually updates 20% at a time by default for VMSS automatic rolling upgrades).

So, modify in Terraform:

```hcl
upgrade_policy {
  mode = "Automatic"
}
```

This means whenever the VMSS model (definition) changes, Azure will initiate a rolling upgrade of VMs. Our model changes whenever `custom_data` (with new image tag) changes, which is what we want on each deploy.

Back to the CI pipeline:
After `terraform apply`, our new images with tag (commit SHA) are set in VMSS. Azure VMSS then will start pulling those images and running them. The old containers will be replaced by new ones on each VM (since we used `docker run --restart always` without naming containers, it might just spawn new ones; we might want to handle container replacement logic in the script, e.g., stop old ones first by name or use `docker run --name` to have consistent container names that get replaced).

For a robust setup, the startup script could check if a container is running and replace it. But since on upgrade, Azure likely reimages the VM, perhaps it's like a fresh boot so it will run the script from scratch (thus killing old VM or resetting it). The exact mechanism for rolling upgrade might be that it creates new instances, then deletes old ones. If so, then each new instance will just run fresh.

Anyway, that covers CI/CD with GitHub Actions. In Azure DevOps, you'd create a pipeline with tasks:

- Azure CLI or Docker tasks to build and push images.
- Terraform CLI tasks to apply changes.

The logic is the same.

Additionally, you might incorporate Packer into the pipeline (for example, build a new image with the new app version, then update Terraform to use that image's ID). That is more complex and often not necessary if just pulling images.

### Pushing Images to Azure Container Registry (ACR)

We already touched on this in CI/CD, but to reiterate:

- ACR serves as the central storage for Docker images. By pushing our images there, we ensure the Azure VMSS (which is in the same Azure environment) can pull them quickly and securely.
- We should have created an ACR (which we did in Terraform). Ensure the CI pipeline or your local Docker is logged into ACR (`az acr login` or via service principal credentials) before pushing.
- Tag naming convention: It's useful to tag images with a version or unique tag for tracking. In CI, we used commit SHA. You could also use semantic versioning or date. Optionally, push a "latest" tag for convenience too.
- Example manual push (if not using CI):
  ```bash
  az acr login --name acrvmssdemo
  docker tag react-app:latest acrvmssdemo.azurecr.io/react-app:v1
  docker tag dotnet-api:latest acrvmssdemo.azurecr.io/dotnet-api:v1
  docker push acrvmssdemo.azurecr.io/react-app:v1
  docker push acrvmssdemo.azurecr.io/dotnet-api:v1
  ```
  This pushes the images. Our cloud-init was using `latest` or some tag; ensure those match (change either the script or tag accordingly).
- Confirm images in ACR via Azure Portal or `az acr repository list -n acrvmssdemo`.

One advantage of ACR is you can also scan images and use content trust, etc. For now, ensure the images are accessible.

Our VMSS VMs are configured with a system-assigned identity and we gave it AcrPull role ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Use%20the%20az%20role%20assignment,permissions%2C%20assign%20the%20AcrPush%20role)). This means we don't need to store ACR credentials in our cloud-init. The Azure CLI on the VM uses the VM's identity to auth to ACR ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Then%2C%20authenticate%20to%20the%20registry,command%20and%20docker%20commands%20with)). This is a security best practice: no hardcoded secrets on VMs, and if the identity is compromised, its scope is limited to pulling images from that ACR (and whatever other roles it has). Always prefer managed identities for such scenarios.

### Automating Deployment with Terraform and CI

At this stage, our pipeline automates building images and updating the VMSS. Let's consider how scaling or changes occur:

- If we change code and push, the pipeline builds new images, pushes, updates Terraform (with new tag), and Azure rolls out updates.
- If we change infrastructure (like want to open a new port, or change VM size, etc.), those are Terraform changes. We commit them, pipeline will run `terraform apply` (though careful: if image build didn't change, the pipeline still rebuilds images unnecessarily every push; one could optimize by separating infra changes pipeline vs app changes. But it's fine if images rebuild if code unchanged, it's just redundant work).
- You might split pipeline triggers: Code changes trigger image build and deploy; Terraform changes might be handled separately. Or use path filters in GitHub Actions (build only if certain directories change).
- Azure DevOps similarly can have multiple stages (build, image push, terraform apply) and approvals if needed.

**Deployment Order Consideration**: If the new code depends on infrastructure changes (e.g., you open port 5001 and app now uses 5001), you must coordinate. Usually, make infra changes first (applied via Terraform), then deploy app changes. Or vice versa depending on compatibility. In our case, we keep them in lockstep in one pipeline for simplicity.

**Verification**: After deployment, one can verify:

- The VMSS instances are up and running new containers. Use Azure Portal or CLI:
  - `az vmss list-instances -g rg-vmss-demo -n vmss-app -o table` to see instances.
  - Connect via SSH (if allowed) or use `az vmss run-command invoke` to run `docker ps` on an instance.
  - Or simply browse to the Load Balancer IP (output from Terraform). The React app should show the updated content. If you have a way to identify the version (e.g., the React app displays the commit hash or API fetch shows version), check that to ensure it's the latest.
- Monitor the rolling upgrade: Azure Portal's VMSS section will show upgrade in progress if in Automatic mode.

So far, we've achieved continuous deployment. We should ensure that the process is robust:

- The Terraform state is handled (we set backend).
- The service principal used in pipeline has necessary rights (likely Contributor on the resource group to allow creating all those resources, plus ACR push rights). We gave it client secret in GH Actions.
- Error handling: If Terraform fails, the action fails and we see logs. Ideally, protect against partial failures. If Terraform apply fails after images pushed, next run might find ACR has images but VMSS not updated. That's okay; it can retry apply.
- One potential issue: If multiple commits happen quickly, pipeline runs could overlap. Ensure you handle that (GitHub Actions will queue by default per branch). Or you might implement locks around terraform apply (though state locking will inherently serialize).

We have not explicitly covered **Azure DevOps** YAML, but similar steps: use tasks like `Docker@2` to build & push, and `AzureCLI@2` or Terraform tasks to apply infra. The specifics can be found in Azure DevOps docs. The key concepts remain identical.

### Blue-Green or Canary Deployments (Advanced)

For completeness, note that a more advanced deployment strategy could involve deploying new VMSS instances alongside old ones (blue-green) or upgrading a subset (canary) and then swapping. VMSS with automatic rolling upgrade essentially does a canary/rolling by updating in batches. If you needed blue-green (two separate sets), you might deploy a second VMSS, then switch traffic via Load Balancer or DNS. That complexity is beyond our main scope, but worth mentioning as a pattern for zero-downtime deploys. The current approach (rolling upgrade) should be fine for most cases, especially if you have more than one instance (so some instances serve traffic while others update).

Now that deployment is automated, let's focus on how to handle scaling, monitoring, and security in our environment.

## 5. Scaling, Monitoring, and Security

Our solution needs to be not only functional but also scalable, observable, and secure. In this section, we'll set up **autoscaling policies** for the VMSS, configure monitoring and logging so we can observe the application and infrastructure, and implement security best practices for network and identity management.

### Implementing Autoscaling Policies

One of the biggest advantages of using a VM Scale Set is the ability to automatically scale out or in based on load. While we set a fixed instance count earlier (e.g., 2 instances), we can define rules to adjust this count.

Azure VMSS can scale based on metrics (like CPU, memory if you have the Azure Monitor agent, or custom metrics) or on a schedule (e.g., scale out during business hours).

We will configure CPU-based autoscaling as an example:

- If average CPU across instances goes above 70% for 5 minutes, scale out (add VMs).
- If average CPU falls below 30% for 10 minutes, scale in (remove VMs).
- Always keep between 2 and, say, 10 instances. Start at 2 (default).

In Terraform, this is done using the `azurerm_monitor_autoscale_setting` resource. For example:

```hcl
resource "azurerm_monitor_autoscale_setting" "vmss_autoscale" {
  name                = "vmss-autoscale"
  resource_group_name = azurerm_resource_group.main.name
  target_resource_id  = azurerm_virtual_machine_scale_set.app.id

  parameters {
    min_count = 2
    max_count = 10
    default_count = 2
  }

  profile {
    name = "autoScaleProfile"

    capacity {
      minimum = 2
      maximum = 10
      default = 2
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_namespace   = "Microsoft.Compute/virtualMachineScaleSets"
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 70
      }
      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_namespace   = "Microsoft.Compute/virtualMachineScaleSets"
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT10M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }
      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT10M"
      }
    }
  }
}
```

Key points of this configuration:

- `min_count`, `max_count`, `default_count`: ensure we always have between 2 and 10 instances. Default (when no rules active or after creation) is 2.
- We define a profile with rules. We used a single profile "autoScaleProfile" with two rules (scale out and scale in).
- The metric trigger uses the built-in metric "Percentage CPU" of the VMSS (this metric is available without extra config). The trigger checks the average CPU over a window:
  - If >70% for 5 minutes, we increase by 1 instance.
  - If <30% for 10 minutes, we decrease by 1 instance.
- We set a cooldown of 5 minutes after scaling out, and 10 minutes after scaling in. This is to prevent rapid oscillations (scale flapping). We only adjust one VM at a time ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=match%20at%20L367%20parameter%20in,a%20maximum%20of%2010%20virtual)), then wait.
- These parameters can be tuned. E.g., if your app can tolerate more aggressive scaling, you can increase `value` to 2 (add two at a time) or shorten cooldown. But one-at-a-time is safer to observe impact ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=parameter%20in%20each%20autoscale%20rule,a%20maximum%20of%2010%20virtual)).
- We must ensure the application can handle scale-in gracefully. If a VM is removed, any in-flight requests to that VM will fail. Using multiple instances and the LB helps mitigate as LB will stop sending traffic to a VM being shut down (thanks to health probes). But stateful data should not be on the VM itself (e.g., user sessions should be stateless or stored externally).

Terraform will apply this autoscale setting. You can verify it in Azure Portal under the VMSS "Scaling" section, where it should show these rules.

Additionally, you can set **scheduled scaling** in the same resource (with additional profiles, e.g., one for off-hours scale in to 1 instance at night, and one for peak hours default to more). That involves adding a `fixed_date` or `recurrence` in profiles. For brevity, we won't detail that, but it's possible.

With autoscaling, our system will handle varying loads:

- Under high load, new VM instances will be spun up (and they'll automatically pull the Docker images and join the LB).
- Under low load, extra VM instances will be removed to save cost.

Remember, scaling out too quickly without controlling container startup can cause a thundering herd on your ACR (if many VMs start at once, all pulling images). Ensure your ACR SKU can handle the throughput or stagger the scaling (the cooldown helps somewhat).

### Monitoring and Logging with Azure Monitor and Log Analytics

**Monitoring** is crucial in production. We want visibility into:

- Infrastructure metrics (CPU, memory, disk, network of VMs).
- Application logs (perhaps container logs or app-specific logs).
- Container health and logs (Docker daemon logs, container stdout/stderr).

Azure provides several tools:

- **Azure Monitor Metrics**: collects metrics like CPU, memory, etc. For VMSS, basic metrics like CPU are available by default. Memory and disk require the Azure Monitor agent.
- **Log Analytics**: a log store and query system. If we install the Azure Monitor agent (formerly called Log Analytics agent or AMA/OMS) on VMs, we can send logs and performance counters to a Log Analytics Workspace.
- **VM Insights**: is an Azure Monitor solution that, when enabled, gives a curated view of VM performance and can even map processes, etc. It uses the Log Analytics and Dependency agent.
- **Azure Monitor for containers**: more oriented to AKS, but for standalone Docker on VMs, you can still collect Docker logs via the agent by configuring it to collect certain log files or syslog.

We will focus on enabling the Azure Monitor agent on the VMSS:
In Terraform, we can use the extension resource `azurerm_virtual_machine_scale_set_extension` to install the agent, or use the newer Azure Monitor VM extension for Linux.

However, Microsoft now has a unified Azure Monitor Agent (AMA) which is recommended over the older Log Analytics (MMA) agent. The AMA requires setting up a Data Collection Rule (DCR). This is a bit complex to do via Terraform (multiple resources: DCR, association, etc.). Alternatively, one can still use the legacy VMInsights method for simplicity:

- Create a Log Analytics Workspace.
- Enable the VMInsights solution on it.
- Add the VM extension for the Log Analytics agent and Dependency agent to the VMSS.

From Thorsten Hans' blog example, they did:

```hcl
# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "log" { ... }

# VMInsights solution
resource "azurerm_log_analytics_solution" "vmInsights" { ... }

# VMSS extension for Log Analytics (MMA)
resource "azurerm_virtual_machine_scale_set_extension" "mma" { ... }

# VMSS extension for Dependency Agent
resource "azurerm_virtual_machine_scale_set_extension" "dependency" { ... }
```

Let's outline a simplified version:

```hcl
resource "azurerm_log_analytics_workspace" "log" {
  name                = "log-analytics-vmss"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_log_analytics_solution" "vm_insights" {
  solution_name         = "VMInsights"
  location              = azurerm_log_analytics_workspace.log.location
  resource_group_name   = azurerm_resource_group.main.name
  workspace_resource_id = azurerm_log_analytics_workspace.log.id
  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/VMInsights"
  }
}

# Log Analytics agent extension (MMA)
resource "azurerm_virtual_machine_scale_set_extension" "log_analytics_agent" {
  name                       = "LogAnalyticsAgent"
  virtual_machine_scale_set_id = azurerm_virtual_machine_scale_set.app.id
  publisher                  = "Microsoft.Azure.Extensions"
  type                       = "OMSAgentForLinux"
  type_handler_version       = "1.0"
  settings = jsonencode({
    workspaceId = azurerm_log_analytics_workspace.log.workspace_id
  })
  protected_settings = jsonencode({
    workspaceKey = azurerm_log_analytics_workspace.log.primary_shared_key
  })
}

# Dependency agent (for VM Insights maps)
resource "azurerm_virtual_machine_scale_set_extension" "dependency_agent" {
  name                       = "DependencyAgentLinux"
  virtual_machine_scale_set_id = azurerm_virtual_machine_scale_set.app.id
  publisher                  = "Microsoft.Azure.Monitoring.DependencyAgent"
  type                       = "DependencyAgentLinux"
  type_handler_version       = "9.10"  # latest at time of writing
  auto_upgrade_minor_version = true
}
```

This will:

- Create a Log Analytics workspace.
- Enable VMInsights solution on it (which sets up some queries and views for VMs).
- Install the OMSAgent (Log Analytics agent) on each VM to send data to the workspace ([Integrate Virtual Machine Scale Sets with Azure Monitor and VMInsights using Terraform · Thorsten Hans' blog](https://www.thorsten-hans.com/integrate-virtual-machine-scale-sets-azure-monitor-vminsights-terraform/#:~:text=,extension)).
- Install the Dependency agent for service map (shows process interconnections, etc, also used by VMInsights).

After deploying this, within a few minutes the VM instances will start sending data. You can then:

- Go to Azure Portal -> Log Analytics workspace -> Logs, run queries like `Heartbeat` (to see if VMs are reporting), `InsightsMetrics` (for performance data).
- Use the Azure Monitor **VM Insights** dashboard to see CPU, memory, disk for each VM and aggregated for the scale set.
- Set up alerts if needed (e.g., alert on high CPU or if VMs are down; alerting config is another step, can be done with Azure Monitor Alert rules).

For container logs: If our apps write to console (stdout/stderr), by default, these are not collected by the Log Analytics agent (unless it is configured to collect Docker container stdout). We can configure the agent to collect certain files or Docker logs. One way: ensure Docker is writing to a log file and then have the agent pick it up. Or use `ContainerLog` table if AMA can collect it (but AMA is more for AKS in that context).
As a workaround, since our .NET app is behind an API, it might be more straightforward to include an Application Insights SDK in the .NET app for structured logging. But let's not expand too far; just note that container logs can be shipped by various means (for example, installing Filebeat/Elastic, or using Azure Diagnostics extension to tail docker logs, etc.).

However, for advanced monitoring of containers on VMs, one could use Azure Monitor's container insights by installing the Azure Monitor Container extension. That is typically used for Azure Arc or similar scenarios. Given complexity, we'll assume infrastructure metrics suffice, and app-level logs are handled by application code (the .NET app could log to App Insights or log files).

**Azure Monitor and Autoscale**: Note that the autoscale rules use Azure Monitor metrics. If CPU goes high, it's Azure Monitor that triggers the scale. We have already configured that.

**Logging for Troubleshooting**: If something goes wrong (say containers don't start), you can:

- Use `az vmss run-command` to execute commands on VMs (like checking the cloud-init log at /var/log/cloud-init.log or docker logs).
- Use Log Analytics: Query the `Syslog` table for entries from cloud-init or docker.
- Ensure your NSG isn't blocking needed traffic (we allowed outbound internet, but if not, ACR pull would fail. In our config, not explicitly allowing outbound, but Azure by default allows outbound from VMs unless you have a rule denying it or use forced tunneling).
- Use Azure Serial Console or boot diagnostics for low-level troubleshooting if VM fails to boot.

### Security Best Practices

Security spans many facets, but we'll focus on a few key areas relevant to our setup: network security, least privilege access, and data protection.

**Network Security:**

- We used NSGs to restrict inbound traffic to only ports 80 and 443 (and optionally 22 for SSH from certain IP). This minimizes the attack surface. All other ports are blocked. This means even if a container starts an unintended service on another port, it's not reachable externally.
- The VMSS is in a private subnet and only accessible through the load balancer's frontend IP. We might consider using an Application Gateway with Web Application Firewall (WAF) instead of a basic LB for enhanced security on HTTP traffic. That would protect against common web attacks.
- If using Application Gateway, we'd attach the VMSS to a backend pool of the AppGW and do SSL there. This involves more resources but is recommended for production web apps requiring TLS and WAF.
- Another network aspect: **Azure Firewall or NAT Gateway** for egress control. In our design, VMSS instances likely use a default outbound IP (since Standard LB without outbound rules gives them a default SNAT). If we wanted to restrict or log outgoing traffic, we could put a NAT Gateway in the subnet or an Azure Firewall to filter egress. This can be considered if the app should only call certain external endpoints.

**Managed Identity and Secrets:**

- We leveraged system-assigned Managed Identity for ACR access, avoiding storing ACR credentials on the VMs ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Use%20the%20az%20role%20assignment,permissions%2C%20assign%20the%20AcrPush%20role)). This is a best practice.
- If the .NET API needs to access other Azure resources (like Key Vault or Storage), we could similarly assign a user-assigned identity or use the same identity to grant permissions. For instance, the API could use the VM's identity to fetch secrets from Azure Key Vault (no secrets in config).
- Ensure that any sensitive data (like the admin password we used for VMSS) is not exposed. We used Terraform random_password but ideally, use SSH keys and disable password login. That is more secure. One could also integrate with Azure AD for Linux VM login to avoid static credentials.
- The Terraform state could contain sensitive info (like that password). Since it's stored in a secure storage and we recommended using Key Vault to store the access key ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=Key%20points%3A)), that mitigates risk.

**TLS/Certificates:**

- Our current setup serves the React app over HTTP (port 80). In production, you likely want HTTPS. If using Application Gateway or Azure Front Door, you can handle certs there. If not, and you want the VMSS itself to serve HTTPS:
  - You could add port 443 to LB, and have the Nginx container serve HTTPS. That means managing certs on the VMs. Possibly use Azure Key Vault to store an SSL certificate and use a startup script to retrieve it and configure Nginx. Or bake it into image (not recommended for rotation).
  - Alternatively, use Let's Encrypt in the Nginx container to auto-request a cert. That requires the container to have access to Let's Encrypt and handle renewal. This is doable (some use cases run certbot in a sidecar container or as part of Nginx).
  - Because this complicates things, often App Gateway is easier for SSL. But it's an architectural choice.

**Operating System Hardening:**

- The VMs are based on official Ubuntu images. Ensure they are updated regularly. We set `package_upgrade: true` in cloud-init, so they get updates on provisioning. But running VMs long-term should be patched. Azure can schedule automatic OS image upgrades or you could periodically redeploy the scale set with a newer image. We could enable automatic OS image upgrades (a property in VMSS) if not using custom images.
- Only required packages are installed. We installed Docker and Azure CLI. Azure CLI isn't strictly needed on the VM except for our login step. We might remove Azure CLI by using a more direct method to get ACR token. But for now, it's fine.
- Docker Hardening: By default, Docker daemon on Linux requires root privileges. We should ensure that the Docker socket isn't exposed or accessible to unprivileged users on the VM (which it isn't by default; only root or members of `docker` group can access it, and our cloud-init didn't add any extra users besides the admin). Also, the containers themselves could be run as non-root inside (our React Nginx runs as nginx user by default likely, and .NET app as user in the runtime image by default too). It's good to confirm your Dockerfiles don't run the app as root for security.
- We may consider enabling Azure Defender for Cloud on our subscription/resource group, which will monitor the VMs for vulnerabilities, missing updates, and misconfigurations (like exposed ports). This could be an additional layer of security monitoring.

**Network Egress for ACR**:

- Ensure ACR is in same region and if possible, enable **Private Link** for ACR and have VMSS use that (with a service endpoint or private endpoint) to avoid exposure of ACR over internet. This requires more network configuration (private endpoints in the VNet for ACR).
- At minimum, if not using private link, consider restricting ACR firewall to only allow the VNet or the Azure services tag for the VMSS's region.
- Our managed identity approach is secure for auth, but the traffic still goes over internet if not in private network. Private Link would allow it to stay within Azure backbone.

In summary, following security best practices: use least privilege (managed identity), restrict network traffic with NSGs, use encryption (TLS) for data in transit, and keep systems updated.

### Scaling and Resilience Considerations

We touched on autoscaling, but also consider resilience:

- VMSS can be deployed across availability zones (which we did by specifying zones). This means if one zone goes down, others still have instances. The LB is zone-redundant so it directs traffic accordingly. This is important for high availability.
- If using Flexible orchestration mode (newer VMSS mode), it allows mixing VM sizes or having VMs not all identical. We used Uniform which is fine here.
- We might also consider using multiple VMSS (one for frontend, one for backend) if we wanted to scale them independently. In our design, they scale together since both run on same VMs. If frontend and API have different resource profiles or scaling triggers, separating them might make sense. That introduces complexity in networking (two scale sets, two LB or one LB with two backend pools, etc.). We kept it simple with one.
- **Testing scaling**: You can simulate load (using Azure Load Testing service or Apache JMeter, etc.) to see that autoscaling works and that new instances properly join and serve traffic.

Now that we have scaling, monitoring, and security in place, our system is robust and ready for production-like usage. In the next section, we'll discuss some best practices and troubleshooting tips gleaned from such deployments.

## 6. Best Practices & Troubleshooting

Deploying applications on VM Scale Sets with Docker and Terraform involves many components. Let's go over some best practices to ensure efficient and reliable operations, and then cover common issues and troubleshooting methods.

### Performance Optimization Techniques

- **Right-size VM Instances**: Choose appropriate VM SKU for your workload. If your .NET API is CPU-intensive, choose a CPU-optimized VM (F series). If memory-intensive, use memory-optimized (E series). For general web workloads, DSv2 or B-series (burstable) might suffice for low traffic with auto-burst capabilities. Monitor your CPU/memory usage (via Azure Monitor) and adjust VM size if needed. Also consider using different VM sizes in different environment (e.g., smaller in dev/test to save cost).

- **Use VMSS Scaling proactively**: Instead of purely reactive scaling, if you know traffic patterns (e.g., high during daytime), use scheduled autoscale to scale out before the load hits, and scale in after. This ensures capacity is ready when needed without waiting for metrics to trigger.

- **Optimize Docker Image Size**: Smaller images pull faster from ACR, meaning faster scale-out. Use Alpine base images where possible (as we did for Node/Nginx). Remove unnecessary files in Dockerfile (we used multi-stage to avoid dev dependencies). Also periodically clean up old images in ACR (use ACR retention policies) to save space and cost.

- **Container Startup Health**: Ensure your containers start quickly and are healthy. The LB probe will check port 80; if your app container isn't ready, the probe fails and traffic won't route. You might adjust the probe delay if needed (there is a property for unhealthy threshold). Also consider implementing a health check endpoint in the .NET API and use that for LB probe if the backend is critical.

- **Parallel deployments**: If you have multiple services, consider deploying them in parallel if independent. But if they share VMSS, they deploy together. If you separated VMSS for front and back, you could deploy one after the other to ensure compatibility.

- **Caching and CDN**: Offload static content. Our React app is static and could be served via Azure CDN or Front Door caching to reduce load on VMs. Similarly, if API has heavy static responses, use Azure Cache (Redis) or output caching at the app level.

- **Threading and Connection Management**: For .NET, ensure it's configured for production (e.g., thread pool tuning if necessary, use asynchronous I/O to handle more requests). For Node (if any in React build, though we serve static so not much), ensure no dev mode.

- **Accelerated Networking**: Enable accelerated networking on the VMSS NICs if the VM SKU supports it (most DSv2 and above do). This can reduce network latency and CPU usage. In Terraform, set `enable_accelerated_networking = true` on the NIC configuration if available.

- **Disk and IOPS**: If your containers do heavy disk operations, consider using VMSS with Premium SSD (set managed_disk_type to Premium_LRS). For example, if the API writes files or uses local caching. In our scenario, mostly ephemeral usage, Standard SSD or even Standard HDD might be fine. Premium disks also have better IOPS for the OS, which can speed up things like Docker image loading.

- **Scale Unit Testing**: Test your app under load with incremental number of instances. See if any bottleneck arises (like database connections if your API connects to a database; ensure the DB can handle more connections when scaling out, etc.). This is not Terraform-specific but critical in an autoscaling scenario to avoid hitting a backend bottleneck (like exhausting DB, which could nullify benefits of scaling app tier).

### Debugging Common Deployment Issues

Even with best planning, issues occur. Here are some common ones and how to address them:

- **VMSS Instance Provision Failure**: Sometimes, VM instances may show a provisioning state of "failed". This often means the custom script or cloud-init had an error. Check:
  - Azure Portal: go to VMSS > Instances, see if there's an extension failure message or boot diagnostics screenshot.
  - Log Analytics: if the agent was installed early enough, maybe logs went there.
  - Use `az vmss run-command` to run `journalctl -u cloud-init` or view `/var/log/cloud-init-output.log` for errors. This will show if a command like `az acr login` failed (maybe managed identity not working?), or Docker pull failed (maybe image tag wrong or ACR issue).
  - If using custom script extension instead of cloud-init, that would surface error code and stdout/stderr in Portal.
  - Common fixes: Ensure the cloud-init YAML is valid (YAML spacing issues can break it). Ensure commands are correct (maybe `docker.io` package name might differ on newer Ubuntu or required apt-get upgrade).
  - If ACR login fails, ensure the VM's managed identity has AcrPull role and that `az login --identity` works. Sometimes, `az login --identity` might not work if Azure CLI isn't signed in and identity not available yet. We might add a retry or slight delay. Alternatively, use `docker login` with an identity token: `docker login acrName.azurecr.io -u 00000000-0000-0000-0000-000000000000 -p "$(curl --silent --fail -H \"Authorization: Bearer $(curl -s --fail --url http://169.254.169.254/metadata/identity/oauth2/token?resource=https://management.azure.com/ -H Metadata:true | jq -r .access_token)\" https://management.azure.com/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/<acrName>/listCredentials?api-version=2019-05-01 | jq -r .passwords[0].value)"`. That is complex; Azure CLI simplifies it. But if CLI is problematic, direct REST call to IMDS (Instance Metadata) for an ACR token might be done.
  - If Docker service didn't start, ensure `systemctl enable docker` was done or use cloud-init `runcmd` to start it explicitly (`service docker start`).
- **Terraform Apply Issues**:

  - Terraform may fail if Azure API issues or if we hit conflicts. For instance, changing custom_data on VMSS might say it needs to recreate or reimage. If manual upgrade mode, Terraform may want to recreate the VMSS resource to apply changes. This would destroy and recreate VMs (downtime). If you want to avoid downtime, consider `automatic` upgrade so it can do in-place.
  - Lock contention: If someone is running `terraform apply` while pipeline is also running, state lock will prevent the second. Wait or coordinate so only one runs at a time.
  - Authentication: ensure the service principal used has rights to create all resources (VMSS, network, etc., and assign roles to ACR, which requires RBAC permission on that scope).
  - Azure API version issues: The Terraform azurerm provider evolves, so ensure version is updated if any resource property required isn't available in older versions.

- **Application Errors**:
  - If the React app shows blank or API not working, possibly CORS issues when calling API at a different domain/port. In .NET, enable CORS for the frontend's domain or port. Or serve them under same domain to avoid CORS altogether.
  - If API isn't reachable, maybe LB rule missing or NSG blocking port. We only opened 80/443. If API is on 5000 and we didn't open 5000 on LB or NSG, the API wouldn't be accessible externally. (If it's meant to be only internal, that's fine). To expose API externally, add LB rule for 5000 and NSG rule for 5000. Or unify via one port with reverse proxy as discussed.
  - If containers crash repeatedly, the `--restart always` will keep trying. Use `docker logs <container>` to see why. Possibly the API can't connect to a database or some config missing. Ensure any required environment variables are set in Docker run (we didn't set any aside from ASPNETCORE_URLS; if needed e.g., DB connection, supply via env in cloud-init or use Azure App Config).
- **Cost Issues**:

  - If you see costs spiking, check that autoscale isn't stuck at a high instance count due to constant load or misconfiguration. Also, the Log Analytics workspace can incur costs if a lot of data is ingested (monitor data volume, adjust retention or filters if needed).
  - Using too large VMs or leaving them running at high count when not needed will cost. Optimize by turning off or scaling to zero in off hours if possible (min_count=0 is possible if you design for zero instances downtime).
  - ACR storage costs if many images; clean old images.

- **State File loss**:
  - If remote state misconfigured and you ran `terraform apply` with local state and lost it, you could have orphaned resources not tracked properly. Always ensure the backend is configured from day 1. If lost, you might need to `terraform import` existing resources to a new state or recreate environment.
- **Terraform drift**:
  - If someone manually changes something in Azure (outside Terraform), your state becomes out of sync. Running `terraform plan` will show differences. Avoid manual changes or import them if needed to Terraform to keep single source of truth.

### Infrastructure Cost Optimization

Running VMs can be costly; here are some tips to control cost:

- **Autoscale Aggressively Down**: We set min 2 for high availability. If your scenario allows going to 1 or 0, that saves cost. For example, dev environment could scale-in to 0 at night (VMSS supports min 0, and it will deallocate all VMs).
- **Use Spot Instances**: Azure VMSS can use Spot VMs (pre-emptible instances that are much cheaper). In Terraform, you can set `priority = "Spot"` and an eviction policy. This is great for non-critical or parallel workloads. For a web app, using spot VMs could cause random instance termination if Azure needs capacity, affecting availability. But you can mix: e.g., have 1 regular instance (to always have service) and additional ones as spot. This is a advanced scenario called **Spot Mix**. Azure VMSS flexible orchestration might allow a mix of spot and regular. Or use two VMSS (one regular, one spot behind same LB).
- **Shutdown during off hours**: If this is not 24/7, schedule scale set to 0 or use Azure Automation to shut it down. But note, scale set min 0 with autoscale rules might suffice (schedule-based autoscale could also do it).
- **Choose right ACR SKU**: Use Basic ACR (cheaper) if your throughput is low. We chose Basic in Terraform which is cost-effective for small teams. Monitor ACR usage; scale up SKU only if needed (like concurrent pulls pushing Basic limits).
- **Logging cost**: In Log Analytics, you're charged per GB ingested and retained. Filter out logs you don't need. For example, if container stdout logs are too verbose and not needed, don't collect them. Set retention to 30 days or less if you don't need long-term logs (we used 30 days; default can be 90).
- **Use B-series VMs for dev/test**: Burstable VMs (B1ls, B2s, etc.) are very cheap for dev/test environments that are idle most of the time and occasionally need CPU bursts. For production though, they may not sustain high load.
- **Reservations**: If you know you'll run X instances long-term, consider reserved instances for 1-year or 3-year to get discounts. But with autoscale, your instance count fluctuates. You could reserve a base amount (like 2 instances) and pay on-demand for the rest. Azure also has savings plan options which are more flexible than specific reservations.
- **Containers vs VMs**: Evaluate if VMSS is the best option. For purely container workloads, Azure Container Instances or AKS might, in some cases, be more cost-efficient when scaling to zero (ACI) or packing more containers per node (AKS). However, both have their own cost factors. Since our scenario specifically is VMSS, we stick to that.

Implementing these optimizations can significantly reduce your Azure bill without compromising the performance or reliability of the application.

With best practices covered, let's wrap up the guide with a brief summary and further resources.

## 7. Conclusion & Additional Resources

In this guide, we have covered the end-to-end process of deploying a React frontend and .NET Core API on Azure Virtual Machine Scale Sets using Terraform and Docker. We started with infrastructure provisioning, moved through application containerization, deployment automation, and addressed scaling, monitoring, and security aspects. This comprehensive approach ensures that the deployed applications are scalable, maintainable, and secure.

**Key Takeaways:**

- **Infrastructure as Code**: Using Terraform to define Azure resources (VMSS, networking, etc.) provides repeatability and version control for your infrastructure. Changes can be reviewed and tracked just like code, reducing configuration drift and manual errors.
- **Containerization**: Docker containers encapsulate the application and its dependencies, ensuring consistent behavior across environments. Multi-stage builds optimize the images for production use ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)).
- **Azure VM Scale Sets**: VMSS provide an easy way to scale VMs in/out with load balancing. They fill a niche for scenarios where using full container orchestration (like AKS) might not be feasible or necessary, while still offering automated scaling ([You can’t always have Kubernetes: running containers in Azure VM Scale Sets - Elton’s Blog](https://blog.sixeyed.com/you-cant-always-have-kubernetes-running-containers-in-azure-vm-scale-sets/#:~:text=Rule%20number%201%20for%20running,platform%20like%20Azure%20Container%20Instances)).
- **Continuous Deployment**: Automated pipelines (CI/CD) can greatly speed up the release process and reduce human error, by consistently building images and applying Terraform.
- **Scaling & Monitoring**: Autoscale rules keep the application responsive under varying loads, and Azure Monitor with Log Analytics offers visibility into system performance and application health, which is crucial for advanced operations.
- **Security**: We applied best practices like minimal open ports, managed identities for ACR access (no credentials on VMs) ([Managed Identity Authentication for ACR - Azure Container Registry | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity#:~:text=Use%20the%20az%20role%20assignment,permissions%2C%20assign%20the%20AcrPush%20role)), and discussed options for TLS, OS updates, and network controls.

By following this guide, an advanced developer or DevOps engineer should be able to implement a similar architecture, tailoring the specifics to their needs (for example, adjusting for multiple environments, adding a CI/CD for multiple branches, integrating with other Azure services like databases or caches, etc.).

**Terraform Script Repository Structure:**
It's often helpful to organize your Terraform configurations and related scripts in a repository for clarity:

```
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── network.tf        # VNet, Subnets, NSG, LB
│   ├── compute.tf        # VMSS, extensions, etc.
│   ├── autoscale.tf      # Autoscale rules
│   ├── acr.tf            # ACR and role assignment
│   ├── log_analytics.tf  # Monitoring resources
│   └── cloud-init-template.txt  # Template for custom_data
├── app/
│   ├── frontend/         # React app source
│   │   ├── Dockerfile
│   │   └── ...
│   └── backend/          # .NET API source
│       ├── Dockerfile
│       └── ...
├── packer/
│   └── ubuntu_docker.pkr.hcl   # Packer template if using custom image
└── .github/workflows/ci.yml    # CI/CD pipeline definition (if GitHub Actions)
```

This structure separates concerns: Terraform IaC, application code, packer image configs, and CI pipeline definitions. It makes it easy for developers to find and update relevant pieces without stepping on each other (for instance, front-end devs mostly in `app/frontend`, infra in `terraform/`).

**Additional Resources:**

For further reading and reference, consider these resources:

- _Official Azure Documentation_:
  - **Azure VM Scale Sets Overview** – high-level concepts and features ([Azure Virtual Machine Scale Sets overview - Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview#:~:text=Azure%20Virtual%20Machine%20Scale%20Sets,can%20automatically%20increase%20or%20decrease)) ([You can’t always have Kubernetes: running containers in Azure VM Scale Sets - Elton’s Blog](https://blog.sixeyed.com/you-cant-always-have-kubernetes-running-containers-in-azure-vm-scale-sets/#:~:text=You%20can%20spin%20up%20Windows,instance%20can%20run%20multiple%20containers)).
  - **Deploying Applications to VMSS** – methods including custom script and custom images ([Deploy an application to an Azure Virtual Machine Scale Set - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-deploy-app#:~:text=need%20to%20install%20the%20application,updates%20across%20a%20scale%20set)) ([Deploy an application to an Azure Virtual Machine Scale Set - Azure Virtual Machine Scale Sets | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-deploy-app#:~:text=Install%20an%20app%20with%20the,Custom%20Script%20Extension)).
  - **Terraform Azure VMSS Tutorial** – step-by-step similar to what we built ([Create an Azure virtual machine scale set using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-vm-scaleset-network-disks-hcl#:~:text=Azure%20virtual%20machine%20scale%20sets,more%20information%2C%20see%20%206)).
  - **Azure Autoscale Documentation** – details on autoscale settings and best practices.
  - **Azure Monitor (VM Insights)** – how to enable and use it, beyond what we did (like analyzing dependency maps, etc.).
- _Terraform Documentation_:
  - **Terraform AzureRM Provider Docs** – reference for all Azure resource arguments (e.g., `azurerm_virtual_machine_scale_set`).
  - **Terraform Best Practices** – how to manage state, use modules, etc.
- _Docker & DevOps_:
  - **Docker Official Docs** – especially on Dockerfiles and multi-stage builds, to further optimize images.
  - **Packer Documentation** – creating Azure images, if you want to fully implement custom image pipeline.
  - **GitHub Actions Docs** (or Azure DevOps Pipelines docs) – for customizing CI/CD pipeline, adding things like notifications, manual approvals for production, etc.
- _Community Articles_:
  - Elton Stoneman's blog post on running containers in VMSS ([You can’t always have Kubernetes: running containers in Azure VM Scale Sets - Elton’s Blog](https://blog.sixeyed.com/you-cant-always-have-kubernetes-running-containers-in-azure-vm-scale-sets/#:~:text=You%20can%20spin%20up%20Windows,instance%20can%20run%20multiple%20containers)) – a real-world scenario that shows an alternative approach, reinforcing some points we discussed (like custom images with containers).
  - HashiCorp Learn – has a section on Azure with VMSS and autoscaling ([Manage Azure Virtual Machine Scale Sets with Terraform | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/it-saas/azure-virtual-machine-scale-sets#:~:text=The%20,the%20scale%20set%20to%20deploy)), which we partially used, it’s a good simple reference.
  - Thorsten Hans' blog on VMSS with Azure Monitor ([Integrate Virtual Machine Scale Sets with Azure Monitor and VMInsights using Terraform · Thorsten Hans' blog](https://www.thorsten-hans.com/integrate-virtual-machine-scale-sets-azure-monitor-vminsights-terraform/#:~:text=By%20configuring%20a%20deep%20integration,feedback%20cycles%20become%20more%20important)) – we drew from this for monitoring steps.

Deploying on Azure VMSS with Terraform is a powerful combination that gives you flexibility of VMs with the convenience of containers. It's a bit of a hybrid approach between IaaS and PaaS. By mastering this, you have fine-grained control over your environment (down to OS level), while still automating scaling and deployment like in PaaS environments.

We hope this guide has been informative and enables you to successfully deploy and manage your own scalable applications on Azure. Happy deploying!
