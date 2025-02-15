# Introduction to MySQL in Azure

Azure offers fully managed MySQL database services that ease the burden of database administration. Instead of running MySQL on your own VMs, you can leverage **Azure Database for MySQL** – a platform-as-a-service (PaaS) offering that handles infrastructure, backups, and patching. There are several deployment options under this service, each suited to different needs:

## Azure Database for MySQL Deployment Options

**Single Server vs. Flexible Server (Managed MySQL Instances):** Azure historically provided the _Single Server_ deployment and now the _Flexible Server_ deployment for MySQL. Both are fully managed, but they differ in customization and high-availability features.

- **Single Server:** An older offering designed for minimal configuration. It has a fixed compute/storage architecture and limited customization. It’s built on Windows OS, does not support availability zones, and was meant for simple workloads ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Less%20HA%20options%20than%20flexible)) ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Flexible%20server)). Single Server automates maintenance and offers 99.99% uptime in a single availability zone, but it’s less flexible for custom settings ([Azure MySQL: MySQL as a Service vs. Self-Managed in the Cloud](https://bluexp.netapp.com/blog/azure-cvo-azure-mysql-mysql-as-a-service-vs.-self-managed-in-the-cloud#:~:text=The%20architecture%20of%20Single%20Server,wide%20scope%20of%20Azure%20regions)). As of late 2024, Azure **retired the Single Server service** in favor of Flexible Server ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Microsoft%20position%20flexible%20server%20as,be%20the%20recommended%20deployment%20option)). For new deployments, Microsoft recommends using Flexible Server.

- **Flexible Server:** The newer, recommended MySQL PaaS model. It provides more granular control over server configurations and maintenance windows and supports both **zone-redundant high availability** and same-zone HA options ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Flexible%20server)) ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Can%E2%80%99t%20restore%20cross%20region)). Flexible Server runs on Linux and allows you to choose specific Azure availability zones for deployment (or let Azure manage HA across zones). It supports bursting (on low-tier instances), IOPS scaling, stop/start capabilities, and up to 10 read replicas for scaling reads ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Can%E2%80%99t%20restore%20cross%20region)). In short, Flexible Server is a production-ready MySQL service with more features and better performance optimizations than Single Server ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Microsoft%20position%20flexible%20server%20as,be%20the%20recommended%20deployment%20option)).

- **Managed Instance (Azure MySQL in VM or other):** Unlike Azure SQL Database, there isn’t a product called “MySQL Managed Instance” separate from the above PaaS offerings. In Azure context, a “managed MySQL instance” typically refers to using Azure Database for MySQL (Flexible or formerly Single) instead of running MySQL yourself. The alternative to PaaS is **self-managed MySQL on an Azure VM**, which gives full control but requires you to handle updates, backups, HA, etc. This is only recommended for scenarios needing custom MySQL configurations not supported by PaaS. Azure’s managed MySQL offloads routine tasks (scalability, backups, patching) to the cloud provider ([Azure MySQL: MySQL as a Service vs. Self-Managed in the Cloud](https://bluexp.netapp.com/blog/azure-cvo-azure-mysql-mysql-as-a-service-vs.-self-managed-in-the-cloud#:~:text=,in%20your%20local%20data%20center)), so most use cases benefit from Azure Database for MySQL service rather than a self-managed VM.

In summary, for fully managed solutions, **Flexible Server** is the go-forward choice for MySQL on Azure. Single Server is legacy (no longer available for new deployments as of 2024). If needed, you can still run MySQL on VMs or containers for total control, or use Azure Arc for hybrid deployments, but these require more management effort.

## Choosing the Right Deployment Model

When deciding between deployment models, consider your application’s requirements for performance, high availability, customization, and cost:

- **New Applications or Migrations:** Use **Azure Database for MySQL – Flexible Server**. It’s recommended for all new development and migration projects because of its flexibility and Azure’s long-term support ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Microsoft%20position%20flexible%20server%20as,be%20the%20recommended%20deployment%20option)). Flexible Server allows tuning of MySQL parameters and scheduling maintenance windows, which is ideal for production workloads requiring custom configurations.

- **Existing Single Server Instances:** Since Single Server is deprecated, existing instances should be migrated to Flexible Server for continued support and better performance. Azure provides migration tools (like Azure Database Migration Service) to move from Single to Flexible with minimal downtime ([What's happening to Azure Database for MySQL single server?](https://learn.microsoft.com/en-us/azure/mysql/migrate/whats-happening-to-mysql-single-server#:~:text=What%27s%20happening%20to%20Azure%20Database,Azure%20Database%20for%20MySQL)).

- **High Availability Needs:** If your application requires high uptime and resilience, choose Flexible Server with **Zone-Redundant HA**. This deployment will provision a standby MySQL server in a different availability zone within the same region for automatic failover, offering a 99.99% SLA even if one zone goes down ([What's New - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/select-right-deployment-type#:~:text=You%E2%80%99ll%20now%20benefit%20from%20the,Critical%20service%20tier)) ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server%20delivers)). If ultra-high availability is needed across regions (disaster recovery), you might set up cross-region read replicas or plan a geo-restore strategy (more on this later).

- **Customization and Control:** Flexible Server allows more server parameter changes and configuration (for example, switching slow query log on, adjusting `sql_mode`, etc.), which Single Server restricted. If your workload needs fine-tuning at the database level, Flexible gives that flexibility ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=Microsoft%20position%20flexible%20server%20as,be%20the%20recommended%20deployment%20option)). Only if PaaS limits a required feature would you consider self-managed MySQL on a VM (e.g., unsupported MySQL version or plugin).

- **Cost Considerations:** Both Single and Flexible have similar pricing models (tiers based on vCores, memory, storage). Flexible Server offers a **Burstable tier** for cost-effective dev/test environments and the ability to stop/start servers to save costs when not in use ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Can%E2%80%99t%20restore%20cross%20region)). Evaluate the pricing tiers (Burstable vs. General Purpose vs. Memory Optimized on Flexible) based on your performance needs. Also, Flexible supports **reserved capacity** pricing to save costs for steady workloads ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,can%20help%20you%20save%20costs)).

In essence, **Flexible Server** is usually the right choice for managed MySQL on Azure, unless you have a special scenario for self-managing MySQL. It provides a balance of convenience and control ideal for advanced users.

## Azure Regions and Availability Zones

When deploying MySQL on Azure, it's important to understand Azure’s global infrastructure – specifically **Regions** and **Availability Zones** – as they relate to database reliability and latency:

- **Azure Regions:** An Azure region is a set of datacenters in a specific geographic location (e.g., East US, West Europe). When you create Azure resources (like a MySQL server), you choose a region, which affects where your data resides and the network latency for users. It’s best practice to deploy your database in the same region as your application servers to minimize latency ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Physical%20proximity)) ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=To%20improve%20the%20performance%20and,as%20resources%20are%20closely%20paired)). Also consider data sovereignty and compliance – you may need to choose a region in a specific country for regulatory reasons.

- **Availability Zones (AZs):** Many Azure regions are composed of multiple availability zones – physically separate datacenters within the same region. Each zone has independent power, cooling, and networking. They are typically separated by enough distance to avoid a single point of failure, but close enough to have low latency between them ([What are Azure availability zones? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#:~:text=Many%20Azure%20regions%20provide%20availability,supported%20by%20the%20remaining%20zones)). In supported regions, Azure allows zone-redundant services, meaning you can deploy resources across multiple AZs for higher resilience. **Azure availability zones are physically and logically separated datacenters with their own independent power source, network, and cooling ([Azure availability zones – High Availability at Scale | Microsoft Azure](https://azure.microsoft.com/en-us/explore/global-infrastructure/availability-zones#:~:text=Azure%20availability%20zones%20are%20physically,Learn%20more)).** If one zone goes down (due to an outage or disaster), services in other zones remain available, providing fault tolerance.

- **Zone Redundancy for MySQL:** Azure Database for MySQL – Flexible Server supports deploying in a specific zone or across zones. You have two HA options:

  - _Same-Zone HA:_ Both primary and standby are in the same AZ (protects against server-level failures but not zone outage).
  - _Zone-Redundant HA:_ Primary and standby are in different AZs in the same region. This protects against an entire datacenter (zone) outage ([What's New - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/select-right-deployment-type#:~:text=You%E2%80%99ll%20now%20benefit%20from%20the,Critical%20service%20tier)). If zone-redundant HA is enabled, Azure guarantees a 99.99% uptime SLA, with automatic failover to the standby on zone failure ([What's New - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/select-right-deployment-type#:~:text=critical%20workloads%20running%20on%20the,Critical%20service%20tier)).
  - If you do not explicitly enable HA, you can still choose which AZ to deploy your single instance in (for latency or co-location reasons). But that instance won’t have a standby for failover.

- **Regions without Zones:** Not all Azure regions have multiple AZs. Some smaller or newer regions might not support AZs. If you deploy in such a region, you cannot have zone-redundant HA (only single-zone). Always check if your chosen region supports availability zones and plan accordingly ([What are Azure availability zones? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#:~:text=To%20see%20which%20regions%20support,regions%20with%20availability%20zone%20support)). For critical systems, prefer regions with AZ support so you can use zone-redundant deployments for higher resiliency.

- **Geo-Redundancy:** While AZs protect against datacenter failures in one region, they are not a substitute for multi-region disaster recovery. Azure pairs regions into geographies for disaster recovery (for example, East US is paired with West US for backup redundancy). Azure Database for MySQL offers geo-redundant backups (backup storage replicated to a paired region) and the ability to perform geo-restore – restoring your server in a different region from backup ([What's New - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/select-right-deployment-type#:~:text=January%202025)). We will discuss cross-region strategies later, but remember that region selection also ties into DR: you may want your primary in one region and have the ability to restore or replicate to another distant region for DR purposes.

In summary, **choose a region close to your users and your application** for low latency, and if available, leverage **availability zones for HA**. The combination of region + AZ selection in Flexible Server deployment is a key design decision for balancing performance and reliability.

---

# Setting Up the Azure Environment

Before deploying a MySQL database on Azure, you need to prepare your Azure environment. This includes having the right prerequisites in place and configuring networking and security to support the database. This section walks through the setup steps for an advanced Azure environment:

## Prerequisites for Azure Deployment

To follow along with CLI commands and Terraform scripts, ensure you have the following prerequisites:

- **Azure Subscription:** You need an active Azure subscription. If you don't have one, sign up for an Azure free account ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=If%20you%20don%27t%20have%20an,Flexible%20Server%20for%20free)). Verify you have contributor or owner rights in the subscription to create resources.

- **Azure CLI:** Install the Azure Command-Line Interface (Azure CLI) on your machine, or be ready to use the Azure Cloud Shell. Azure CLI enables scripting Azure resource management. You should have Azure CLI version 2.0 or later ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=If%20you%20prefer%20to%20install,see%20Install%20the%20Azure%20CLI)). To check, run `az --version`. If needed, install/upgrade via Microsoft’s instructions ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=If%20you%20prefer%20to%20install,see%20Install%20the%20Azure%20CLI)). Alternatively, you can use the **Azure Cloud Shell** in a browser, which comes pre-configured with Azure CLI and other tools ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=Open%20Azure%20Cloud%20Shell)).

- **Terraform:** Install Terraform (v1.x recommended) on your local machine if you plan to use it. The guide is tested with Terraform v1.2.7 and the AzureRM provider v3.20.0 ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=This%20quickstart%20was%20tested%20by,Terraform%20and%20Terraform%20provider%20versions)). Make sure you also have the Azure CLI or an Azure service principal set up for Terraform authentication. HashiCorp provides installation packages for all OS; ensure `terraform -v` works and shows a recent version.

- **Azure CLI Authentication:** Once CLI is installed, log in to Azure:

  ```bash
  az login
  ```

  This will open a browser for you to authenticate. After login, set the desired subscription context:

  ```bash
  az account set --subscription <YOUR_SUBSCRIPTION_ID>
  ```

  This ensures all subsequent CLI and Terraform commands target the correct subscription ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=az%20login)) ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=az%20account%20set%20,ID)). If using Cloud Shell, you’ll already be authenticated to the account associated with the shell.

- **Terraform Authentication:** Terraform can authenticate to Azure in multiple ways. A simple approach for dev is to run `az login` and let Terraform use your Azure CLI credentials (the AzureRM provider can pick up CLI auth). For automated setups (CI/CD), you might configure a service principal with client ID/secret or use managed identities. As an advanced user, consider using a remote backend with Azure storage (covered later) and ensure credentials are handled securely (e.g., environment variables for service principal secrets, or use Azure CLI/task identity in pipelines).

- **Resource Group:** Decide on a resource group name and Azure region for your resources. In CLI or Terraform scripts, the first step is often to create a Resource Group which acts as a container for all related resources. For example:
  ```bash
  az group create --name MyResourceGroup --location eastus2
  ```
  This creates a group in _East US 2_ region ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=Create%20an%20Azure%20resource%20group,location)). You can manage all MySQL servers, VMs, networking, etc., under this group.

Having these prerequisites in place sets the stage for deploying and managing Azure resources for MySQL. Next, we configure networking and security fundamentals required by an Azure Database for MySQL instance.

## Configuring Networking and Security

Proper network configuration is crucial for database security and connectivity. Azure Database for MySQL can be accessed either over the public internet (with firewall rules) or via a private network connection. We will set up a virtual network, subnets, and optionally private endpoints for secure access, as well as configure firewall rules as needed:

- **Virtual Network (VNet):** Create or identify an Azure Virtual Network for your application and database. A VNet is an isolated network in Azure where you can run resources (VMs, containers, PaaS endpoints, etc.) in a private address space. If you plan to use private access for MySQL, the server will need a subnet in a VNet. You can create a VNet with Azure CLI:

  ```bash
  az network vnet create -g MyResourceGroup -n MyVNet --address-prefixes 10.0.0.0/16
  ```

  And within it, define subnets for your database and maybe other components (web app, VM, etc.). For example:

  ```bash
  az network vnet subnet create -g MyResourceGroup --vnet-name MyVNet \
      -n MySQLSubnet --address-prefixes 10.0.0.0/24
  ```

  This creates a subnet with address range 10.0.0.x/24 for the MySQL Flexible Server.

- **Subnet Delegation:** When using private access for Azure Database for MySQL Flexible Server, the subnet must be delegated to the Azure MySQL service. Delegation simply means the subnet is marked for exclusive use by the service. If you create the server via CLI or Terraform with a `delegated_subnet_id`, Azure will automatically handle the delegation. In CLI, providing the `--vnet` and `--subnet` parameters during `az mysql flexible-server create` will delegate that subnet to `Microsoft.DBforMySQL/flexibleServers` ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=,zone%20%24dns)). Only one MySQL flexible server can be created per delegated subnet (to avoid overlap of network range and ensure isolation).

- **Private Access vs. Public Access:** When creating a MySQL Flexible Server, you must choose the connectivity method **at creation time**, and it cannot be changed later ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=,autogenerated%20virtual%20network%20and%20subnet)).

  - _Private Access (VNet Integration):_ The server is accessible only within the VNet (or via peered VNets/VPN). Azure will assign it a private IP in the subnet, and no public IP address will be available. This is the recommended option for production for enhanced security ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=The%20connectivity%20method%20can%27t%20be,the%20article%20about%20networking%20concepts)). Azure CLI defaults to private access if not specified, automatically creating a VNet and subnet if you don't supply one ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=,autogenerated%20virtual%20network%20and%20subnet)).
  - _Public Access (Allowed IP addresses):_ The server gets a public endpoint `<name>.mysql.database.azure.com`. You control access by firewall rules that allow specific IP ranges to connect. This is easier for quick setups or if VNet integration is not possible, but you must carefully restrict IPs. You can specify `--public-access <IP_RANGE>` or `--public-access 0.0.0.0` (which allows all Azure services traffic) in CLI ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=az%20mysql%20flexible,iops%20500)) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=Create%20a%20MySQL%20flexible%20server,endIpAddress)).

- **Firewall Rules (Public access scenario):** If using public access, set up firewall rules so only trusted sources can reach the MySQL server. By default, Azure Database for MySQL blocks all external connections. For example, to allow a specific office IP range:

  ```bash
  az mysql flexible-server firewall-rule create -g MyResourceGroup -s MyServerName \
      -n AllowOffice --start-ip-address 203.0.113.0 --end-ip-address 203.0.113.255
  ```

  Alternatively, `--public-access` in the create command can set a broad rule. Setting `--public-access None` means no public IP will be allowed (essentially locking it down to only a later Private Endpoint connection) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=Create%20a%20MySQL%20flexible%20server,endIpAddress)).

- **Private DNS Zone:** If you choose private access, Azure will often create a Private DNS zone for the MySQL server (e.g., `privatelink.mysql.database.azure.com`) and link it to your VNet so that the server's hostname resolves to the private IP internally. In Terraform or CLI, you might explicitly create a Private DNS Zone resource and a VNet link ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=resource_group_name%20%20%20%20,8.0.21)) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=high_availability%20,storage)). Ensure the DNS zone name matches the server’s domain (Azure’s default is `<mysqlserver>.mysql.database.azure.com` for public; for private, it uses a special private DNS zone). Terraform example:

  ```hcl
  resource "azurerm_private_dns_zone" "mysql" {
    name                = "privatelink.mysql.database.azure.com"
    resource_group_name = azurerm_resource_group.rg.name
  }
  resource "azurerm_private_dns_zone_virtual_network_link" "mysql_link" {
    name                  = "mysqlDnsLink"
    resource_group_name   = azurerm_resource_group.rg.name
    private_dns_zone_name = azurerm_private_dns_zone.mysql.name
    virtual_network_id    = azurerm_virtual_network.myvnet.id
  }
  ```

  Azure will create a DNS A record in that zone for your MySQL server name pointing to its private IP.

- **Network Security for VMs/App:** If you have an app running in a VM or Azure Kubernetes (AKS) and connecting to the MySQL in a VNet, ensure the NSGs (Network Security Groups) allow outbound traffic on port 3306 and any required inbound if the app is accessed from outside. By default, outbound to Azure services is allowed, but if you've locked down NSGs, permit traffic to the database subnet IP.

- **Service Endpoints and Private Links:** For Single Server (legacy), one could use service endpoints to allow a VNet to access the server. However, Flexible Server doesn’t support service endpoints ([What's happening to Azure Database for MySQL single server? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/migrate/whats-happening-to-mysql-single-server#:~:text=,We%20recommend%20configuring)). Instead, it uses the above-mentioned private VNet integration. If you have an existing MySQL Flexible Server with public access but want secure connectivity from a specific VNet, you could use **Azure Private Endpoint** to map the server’s public endpoint to a private IP in your VNet. This approach is useful for scenarios where the server was created as public but you later decide to integrate with a VNet without changing the server type. Private Endpoints create a network interface in your VNet linked to the MySQL service, and you would then use the Private Endpoint’s IP or alias to connect. Generally, if private connectivity is needed, it’s simpler to start with Private Access deployment from the beginning ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=The%20connectivity%20method%20can%27t%20be,the%20article%20about%20networking%20concepts)).

- **Basic Security Configuration:** Always enable SSL enforcement on the MySQL server (Azure usually has “Enforce SSL connection” enabled by default). This ensures all client connections use TLS encryption. Clients will need to specify `--ssl-mode=REQUIRED` (and perhaps provide the CA cert for verification) when connecting ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=wget%20)) ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=mysql%20,ca%3DDigiCertGlobalRootCA.crt.pem)). Additionally, decide if you will use Azure AD authentication or just MySQL logins (more on that in Security section). If using only MySQL logins, generate strong passwords for the admin and any user accounts, since those creds will be how people log in.

In summary, set up a **VNet and subnets** for your MySQL (if using private), configure **firewall rules or private DNS** appropriately, and **secure connectivity (SSL, limited IP ranges)** before creating the MySQL instance. Now that the environment is prepared, we can proceed to actually creating and managing the MySQL servers using Azure CLI.

---

# Creating and Managing MySQL Databases Using Azure CLI

Azure CLI provides a powerful, scriptable interface to create and manage Azure Database for MySQL instances. In this section, we will use Azure CLI commands to provision MySQL servers, configure them, manage databases and users, and set up backup/restore routines. Each step is accompanied by examples. This assumes you have Azure CLI configured and logged in (from the previous section).

## Creating MySQL Instances with Azure CLI

To create a new MySQL server instance (Flexible Server) using Azure CLI, you can use the `az mysql flexible-server create` command. This command has many options to customize the server. We will go through a simple creation first, then more advanced parameters:

- **Basic Creation:** If you run the command with minimal flags, Azure will create a MySQL Flexible Server with sensible defaults (Burstable B1MS instance, MySQL 5.7, 7-day backup retention, private access with new VNet). For example:

  ```bash
  az mysql flexible-server create -g MyResourceGroup -n mymysqlserver -l eastus2 \
      --admin-user dbadmin --admin-password <YourPassword>
  ```

  This specifies resource group, server name, region, and admin credentials. Azure CLI will fill in unspecified values with defaults. According to Microsoft’s docs, _“The server that's created has the following attributes: an autogenerated server name (if not provided), admin user/password (if not provided), default SKU (Burstable B1MS), MySQL version 5.7, backup retention 7 days, and by default **Private access** with an auto-generated VNet/subnet.”_ ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=az%20mysql%20flexible)) ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=,autogenerated%20virtual%20network%20and%20subnet)). It will output a JSON with the details of the created server, including the connection string and resource IDs ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=Creating%20Resource%20Group%20%27groupXXXXXXXXXX%27,forget%20your%20password%2C%20reset%20the)) ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=%7B%20%22connectionString%22%3A%20%22server%3D%3Cserver,East%20US%202)).

- **Custom Configuration:** Advanced users typically want to specify more settings at creation. Azure CLI supports parameters for compute tier, size, version, storage, connectivity, etc. For example:

  ```bash
  az mysql flexible-server create \
      --resource-group MyResourceGroup --name prod-db01 --location westus3 \
      --admin-user dbadmin --admin-password MySecureP@ssw0rd! \
      --sku-name Standard_D2ds_v4 --tier GeneralPurpose --storage-size 100 \
      --version 8.0.32 --high-availability ZoneRedundant --zone 1 --standby-zone 2 \
      --public-access None
  ```

  Let’s break down this example:

  - `--sku-name` and `--tier` specify the compute size. Here we chose a General Purpose 2 vCPU SKU (Standard_D2ds_v4). Azure has naming conventions for SKUs; you can list available SKUs in a region with `az mysql flexible-server list-skus --location <region>` ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=,location%20%22%24location)).
  - `--storage-size 100` allocates 100 GiB of storage. This can later be scaled up (but not below 100 once set).
  - `--version 8.0.32` picks MySQL version 8.0 (if Azure supports that exact minor version; if not, it will choose the latest 8.0.x). Azure currently supports MySQL 5.7 and 8.0 on Flexible.
  - `--high-availability ZoneRedundant --zone 1 --standby-zone 2` enables HA. We are deploying primary in zone 1 and secondary in zone 2 within the region. Azure will configure replication and failover accordingly.
  - `--public-access None` means we are using private access (no public endpoint). We did not explicitly specify VNet/subnet in this command; Azure will create a new VNet and delegated subnet for this server automatically ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=,autogenerated%20virtual%20network%20and%20subnet)). If we wanted to use an existing VNet, we’d add `--vnet MyVNet --subnet MySQLSubnet --private-dns-zone MyPrivateDNSZoneName` (where private DNS zone is optional if you want a custom one).

  This single CLI command will create the MySQL server with all specified settings. It might take a few minutes to provision especially if HA is enabled (since it sets up two instances).

- **Output and Verification:** After creation, check the output or use Azure CLI to verify:

  ```bash
  az mysql flexible-server show -g MyResourceGroup -n prod-db01
  ```

  This will display the server’s properties, including fully qualified domain name (FQDN), version, status, etc. The FQDN is typically `<servername>.mysql.database.azure.com`. If using private access, that DNS name maps to a private IP accessible in the VNet. If using public, it’s globally accessible (with firewall as gatekeeper).

- **Creating Databases via CLI:** An Azure MySQL server can hold multiple databases (just like on-prem MySQL instance). The `az mysql flexible-server create` command by default creates a database named _`flexibleserverdb`_ during provisioning ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=Your%20server%20%27serverXXXXXXXXX%27%20is%20using,name%3E.mysql.database.azure.com%3Bdatabas)). You can specify a different name with `--database-name` parameter during creation. If you need to add more databases later, use:
  ```bash
  az mysql flexible-server db create -g MyResourceGroup -s prod-db01 -d myappdb
  ```
  This creates a new empty database named _myappdb_ on that server ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=az%20mysql%20flexible)). Alternatively, you can create databases by connecting with a MySQL client and issuing SQL `CREATE DATABASE` commands – both achieve the same result.

Now you have a MySQL Flexible Server running on Azure. Next, we'll cover how to adjust configuration and security settings on this server via CLI.

## Configuring Database Parameters and Security Settings

One advantage of Flexible Server is the ability to configure server parameters and enhance security. Azure provides CLI commands to view or change MySQL server parameters and to manage security features:

- **Server Parameters:** You can list available MySQL server parameters and their values by:

  ```bash
  az mysql flexible-server parameter list -g MyResourceGroup -s prod-db01 --query "[*].{name:name, value:value, default:defaultValue, allowed:allowedValues}"
  ```

  This will show parameters like `innodb_buffer_pool_size`, `max_connections`, `sql_mode`, etc., and indicate if they are dynamic or require restart. To update a parameter:

  ```bash
  az mysql flexible-server parameter set -g MyResourceGroup -s prod-db01 \
      -n sql_mode -v "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION"
  ```

  This sets the `sql_mode` to a custom value (enabling strict mode, etc.) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=match%20at%20L2583%20az%20mysql,v%20%22ONLY_FULL_GROUP_BY%2CSTRICT_TRANS_TABLES%2CNO_ZERO_IN_DATE%2CNO_ZERO_DATE%2CER%20ROR_FOR_DIVISION_BY_ZERO)). For batch updates of multiple parameters at once, Azure CLI supports `az mysql flexible-server parameter set-batch` to apply a JSON or config file of parameters ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=az%20mysql%20flexible)). Be cautious: not all parameters are modifiable in PaaS (for example, some engine flags are fixed by Azure). Consult Azure’s documentation for which MySQL parameters are configurable in Flexible Server.

- **Admin Username and Password:** The admin user (created at server provisioning) is a MySQL account with full privileges. Azure names it as provided (e.g., "dbadmin") but the actual login username to use includes the server name (e.g., `dbadmin@prod-db01`). If you forget the admin password or want to rotate it, you can reset it via CLI:

  ```bash
  az mysql flexible-server update -g MyResourceGroup -n prod-db01 -p NewStr0ngPassw0rd
  ```

  This updates the administrator password ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=Creating%20MySQL%20database%20%27flexibleserverdb%27,password)). It’s good practice to rotate credentials periodically or use Azure AD authentication to avoid managing passwords (discussed later).

- **SSL Enforcement:** By default, Azure Database for MySQL requires SSL connections. This is a parameter (`require_secure_transport`) which should be Enabled. You can verify via CLI parameter list or on the Azure Portal. It’s recommended to leave this enabled for security. If for some reason your application cannot use SSL, you can disable it (not recommended for production) by setting that parameter to Disabled via CLI. But a better approach is to update the application to trust Azure’s CA and use SSL. Azure uses CA-signed certificates (Baltimore CyberTrust root or DigiCert depending on region), which you can download and use in your MySQL client connection (as shown in the earlier CLI example with `--ssl-ca=DigiCertGlobalRootCA.crt.pem` ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=wget%20))).

- **Azure AD Authentication (Microsoft Entra ID):** Azure Database for MySQL – Flexible now supports Azure AD (Entra ID) authentication ([Microsoft Entra Authentication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-azure-ad-authentication#:~:text=Microsoft%20Entra%20Authentication%20,defined%20in%20Microsoft%20Entra%20ID)). This allows you to connect to MySQL using identities managed in Azure AD, which can simplify user management and enhance security with features like MFA. To set this up, you need to perform steps including:

  - Enabling Azure AD authentication on the server (`az mysql flexible-server update --enable-adauth-only true` or via Portal).
  - Creating an Azure AD admin for the MySQL server:
    ```bash
    az mysql flexible-server ad-admin create -g MyResourceGroup -s prod-db01 \
        -u MyAzureADAdminUser -i <AzureAD-Object-ID-of-User/Group>
    ```
    This designates an Azure AD user or group as the Active Directory admin for MySQL ([Microsoft Entra Authentication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-azure-ad-authentication#:~:text=MySQL%20learn,defined%20in%20Microsoft%20Entra%20ID)). Once configured, that AD identity can connect to MySQL (with an access token rather than password) and create Azure AD contained users in MySQL.
  - Azure AD users in MySQL are created via special syntax in MySQL (e.g., `CREATE USER user1 FROM EXTERNAL PROVIDER;`). Azure AD authentication is an advanced feature but recommended for enterprises to centralize credential management ([Azure AD Authentication for MySQL Flexible Server now GA!](https://techcommunity.microsoft.com/t5/azure-database-for-mysql-blog/azure-ad-authentication-for-azure-database-for-mysql-flexible/ba-p/3689854#:~:text=Azure%20AD%20Authentication%20for%20MySQL,services%20in%20a%20central)).

- **Firewall and Network Settings:** If you need to adjust firewall rules after creation (for public servers), use `az mysql flexible-server firewall-rule`. For example, to allow Azure services or a developer IP dynamically. Also, if you initially created the server as private and now need to allow certain external connectivity, you’d typically use a VPN/ExpressRoute into the VNet or consider adding a **private endpoint** in another VNet, since you cannot switch the server to public mode after creation ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=The%20connectivity%20method%20can%27t%20be,a%20server%20that%20has%20private)).

- **Customer Managed Encryption Keys:** By default, Azure encrypts the MySQL data at rest with service-managed keys. Advanced users may require using a customer-managed key (CMK) from Azure Key Vault for encryption-at-rest (BYOK scenario). Azure Database for MySQL – Flexible supports data encryption with CMK ([Data Encryption With Customer Managed Keys - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-customer-managed-key#:~:text=Server%20learn,for%20data%20protection%20at%20rest)). Setting this up involves:

  - Creating a Key Vault and generating or importing a key.
  - Enabling the Soft Delete and Purge protection on the Key Vault (required for Azure to use it).
  - Granting the Azure MySQL service access to the Key Vault key (through a managed identity and Key Vault access policy or RBAC).
  - Updating the MySQL server to use that key:
    ```bash
    az mysql flexible-server update -g MyResourceGroup -n prod-db01 \
        --key <KeyVaultKeyID>
    ```
    This will assign the Key Vault key as the encryption key for the server ([Data Encryption With Customer Managed Keys - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-customer-managed-key#:~:text=Server%20learn,for%20data%20protection%20at%20rest)). After this, the storage encryption is done with your provided key. Ensure you maintain the key’s availability (rotation, not disabling it) — losing it could lock you out of your data.

- **Defender for Cloud (Advanced Threat Protection):** Azure offers Microsoft Defender for Cloud integration for MySQL. This is an optional security layer that alerts on anomalous activities (SQL injections, suspicious access patterns). You can enable it in the Portal or via CLI:
  ```bash
  az mysql flexible-server update -g MyResourceGroup -n prod-db01 --set threatDetectionPolicies.name=Default \
      --set threatDetectionPolicies.states=Enabled
  ```
  (The exact CLI syntax may vary, sometimes Azure CLI has a command group like `az security alert` or uses `az resource update` for enabling Defender on databases). Once enabled, you should configure an email or event hub to receive threat alerts. This feature can detect things like someone attempting to exploit vulnerabilities in MySQL or unusual data exfiltration attempts.

At this point, our MySQL server’s configuration and security posture are tuned: we’ve set parameters for performance or behavior, enforced secure connections, possibly enabled Azure AD auth, and ensured encryption and threat detection as needed. Now we’ll look at managing database users and permissions.

## Managing Users and Permissions

Managing MySQL users and permissions is mostly done within MySQL itself (by connecting to the database and running SQL statements), because Azure CLI does not provide commands to create individual database users (other than the admin and Azure AD admin). As an advanced user, you should be comfortable creating users via MySQL commands. Here’s how to manage users in an Azure MySQL context:

- **Connect to MySQL**: Use the MySQL client or MySQL Workbench to connect to your Azure MySQL instance. For example, using the MySQL CLI from a VM or Azure Cloud Shell:

  ```bash
  mysql -h prod-db01.mysql.database.azure.com -u dbadmin@prod-db01 -p -D mysql
  ```

  (Here we connect to the default `mysql` database as admin). Ensure you include `@servername` in the username when connecting (Azure requires that for the admin login over public endpoint). If SSL is required, add `--ssl-mode=REQUIRED`.

- **Create Additional Users**: Once connected, use standard SQL statements:

  ```sql
  CREATE USER 'appuser'@'%' IDENTIFIED BY 'StrongP@ssw0rd';
  ```

  This creates a new MySQL user. `'%'` as host means the user can connect from any IP (which is typical if using Azure AD auth or if you handle network restrictions via firewall). You could specify a particular subnet or IP range for more restriction. If Azure AD auth is enabled and you want to create an Azure AD user, you'd do:

  ```sql
  CREATE USER 'john.doe@yourtenant.com'@'%' IDENTIFIED WITH azure_authentication;
  ```

  (The exact syntax might be `FROM EXTERNAL PROVIDER` for Azure AD users in newer MySQL versions ([Microsoft Entra Authentication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-azure-ad-authentication#:~:text=MySQL%20learn,defined%20in%20Microsoft%20Entra%20ID)).)

- **Grant Permissions**: Use `GRANT` statements to assign privileges to the user. For example, to allow the user full access to a specific database:

  ```sql
  GRANT ALL PRIVILEGES ON myappdb.* TO 'appuser'@'%';
  ```

  Or follow least privilege principle: grant only needed rights (SELECT, INSERT, UPDATE, etc). Remember to `FLUSH PRIVILEGES;` if needed (though in modern MySQL it’s usually not necessary after GRANT).

- **Security Best Practices for Users**:

  - Always use strong, unique passwords for MySQL users.
  - Do not use the admin account for applications; instead create least-privilege application users.
  - Rotate user passwords periodically. This can be done via `ALTER USER ... IDENTIFIED BY ...` SQL command.
  - Leverage Azure AD authentication for users if possible, so password management is centralized. In that case, your app would obtain a token for an AD service principal/user and use that to log in (rather than a password).

- **Managing Permissions**: If you need to review permissions, you can query the MySQL metadata (tables like `mysql.user` or use `SHOW GRANTS FOR 'user'@'host';`). Removing a user is done via `DROP USER 'appuser'@'%'` if no longer needed.

- **Auditing Access**: Azure MySQL can output audit logs (tracking connections, queries, etc.) if you enable auditing. Enabling the MySQL Audit log (general log or the slow query log) is possible via server parameters. For example, `general_log` and `audit_log_enabled` (if supported) parameters could be set to ON. The audit logs can be collected to Azure Monitor (Log Analytics) via the Diagnostic settings, which we’ll discuss in Monitoring. This can help you keep track of who logged in and what they executed, which is important in an enterprise environment.

Azure CLI doesn’t directly manage MySQL users, but by using the CLI to enable certain features (like AD admin, or retrieving the server hostname and admin login info), and then running SQL, you have full control over user management.

## Implementing Backup and Restore

Azure Database for MySQL automatically performs backups, but it’s important to understand how to manage backups and perform restores, including using CLI for point-in-time restores or geo-restore scenarios:

- **Automatic Backups:** Azure by default takes **automated backups** of Flexible Server with a retention of 7 days (configurable up to 35 days) ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=%2A%20Zone,Elastic%20scaling%20within%20seconds)). These include full backups and transaction log backups, allowing point-in-time recovery within the retention window. The backups are stored in RA-GRS storage (read-access geo-redundant storage) if geo-redundant backup is enabled (`--geo-redundant-backup Enabled` on server creation) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=%5B,strategy)). You can adjust backup retention via CLI:

  ```bash
  az mysql flexible-server update -g MyResourceGroup -n prod-db01 --backup-retention 14
  ```

  This would change retention to 14 days.

- **On-Demand Backup (Manual):** Azure’s PaaS does not give direct access to take a “backup now” via CLI for MySQL. Instead, you rely on the automatic backups or you can perform a logical backup (mysqldump) manually if needed for immediate backup. Azure Portal has a “Backup now” option which effectively triggers a snapshot backup, but currently Azure CLI for MySQL doesn’t have a specific command for on-demand backup (it might be possible through an ARM API call).

- **Point-in-Time Restore (PITR):** If you need to restore the server to a previous state, you can use the Azure CLI to perform a point-in-time restore. This creates a new server from the backups of an existing server. The command is essentially to create a new server with `--source-server <resourceID>` and `--restore-time <timestamp>`:

  ```bash
  az mysql flexible-server restore \
      -g MyResourceGroup -n prod-db01-restore --source-server prod-db01 \
      --restore-time "2025-02-14T10:00:00Z"
  ```

  This will create a new server named `prod-db01-restore` in the same resource group, restored to the state that prod-db01 was at on Feb 14, 2025 10:00 UTC ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=Examples)). The new server will have the same admin login and password as the source (you can change password after restore if desired) and by default the same VNet settings as the source ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=Geo,Private%20access%20server%20will)) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=Restore%20%27testserver%27%20to%20a%20specific,with%20the%20same%20network%20configuration)). Make sure the name for the new server is unique. Also, note you cannot restore in-place; restore always creates a new instance.

- **Geo-Restore:** If your backups are geo-redundant, you can restore to a different region (disaster recovery scenario). The CLI usage is similar to PITR, but you specify a `--location` for the new server (different from source’s region) and ensure geo-backup was enabled on source. For example, to restore in “CentralUS”:

  ```bash
  az mysql flexible-server restore \
      -g DRResourceGroup -n prod-db01-dr --source-server prod-db01 \
      --restore-time "2025-02-14T10:00:00Z" --location centralus
  ```

  Azure will use the geo-replicated backup in the paired region to create the server. This provides a basic DR solution (though it’s a manual restore, not an automated failover).

- **Backup Storage and Monitoring:** Keep an eye on backup storage consumption; Azure provides some quota (e.g., backup up to 100% of your provisioned storage is free, beyond that you get charged). Use Azure Monitor metrics to watch “Backup Storage Used” if available ([Azure Database for MySQL - Flexible Server monitoring data reference](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-monitor-mysql-reference#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server)).

- **Export/Import (Logical backups):** In addition to Azure’s automated backups, you can always perform logical backups using tools like `mysqldump` or MySQL’s export utilities. For instance, from a VM or Cloud Shell:

  ```bash
  mysqldump -h prod-db01.mysql.database.azure.com -u dbadmin@prod-db01 -p \
      --all-databases > alldb_backup.sql
  ```

  and import similarly using `mysql < alldb_backup.sql` on a target server. This is useful for migrating data between servers or exporting data for development/testing. For large databases, consider using MySQL’s logical export with compression or Azure Database Migration Service for a more automated approach.

- **Consistency and Scheduling:** Azure's automatic backups are _transactionally consistent_ for InnoDB (they're snapshot-based). If you have MyISAM tables (not recommended), the snapshot might not guarantee consistency for those tables. Ensure your backup strategy accounts for your engine usage. Also, schedule periodic test restores (e.g., monthly spin up a new instance from backup) to verify backup integrity and your process.

By leveraging Azure’s built-in backups and the CLI for restore operations, you can meet most recovery point and recovery time objectives (RPO/RTO) for your MySQL databases. Advanced scenarios like replication-based HA or cross-region replicas will be discussed in the HA/DR section.

At this stage, you should be able to deploy MySQL servers via CLI, configure them, secure them, manage users, and handle backups/restores. Next, we will see how to automate these deployments and configurations using Terraform for infrastructure as code.

---

# Automating MySQL Deployment with Terraform

Using Terraform for infrastructure-as-code allows you to automate and version-control the deployment of Azure resources, including Azure Database for MySQL. In this section, we’ll create Terraform configurations to deploy MySQL Flexible Servers and related infrastructure, manage the Terraform state, utilize modules for reusability, and even automate scaling/monitoring setup via Terraform. This approach is critical for consistent, repeatable deployments in devops workflows.

## Writing Terraform Configurations for MySQL Setup

A Terraform configuration is typically composed of multiple `.tf` files (providers, variables, resources, outputs, etc.). We will outline a Terraform configuration that sets up the following: a resource group, a VNet and subnet, a MySQL Flexible Server, a database, and a private DNS zone for connectivity.

1. **Providers and Authentication:** First, define the Azure provider in a `providers.tf` file:

   ```hcl
   terraform {
     required_providers {
       azurerm = {
         source  = "hashicorp/azurerm"
         version = "~>3.20.0"  # or latest stable
       }
     }
   }
   provider "azurerm" {
     features {}  # enable the Azure provider
   }
   ```

   This ensures Terraform knows to use the AzureRM provider. Authentication to Azure can be done via environment variables or by Azure CLI login. As an advanced setup, you might also specify a backend here (more on state management later).

2. **Resource Group and Network (infrastructure):** In `main.tf` (or separate files):

   ```hcl
   resource "azurerm_resource_group" "rg" {
     name     = "${var.resource_group_name_prefix}-${random_string.suffix.result}"
     location = var.resource_group_location
   }

   resource "azurerm_virtual_network" "vnet" {
     name                = "mysql-vnet"
     location            = azurerm_resource_group.rg.location
     resource_group_name = azurerm_resource_group.rg.name
     address_space       = ["10.0.0.0/16"]
   }

   resource "azurerm_subnet" "mysql_subnet" {
     name                 = "mysql-subnet"
     resource_group_name  = azurerm_resource_group.rg.name
     virtual_network_name = azurerm_virtual_network.vnet.name
     address_prefixes     = ["10.0.0.0/24"]
     delegation {
       service_delegation {
         name = "Microsoft.DBforMySQL/flexibleServers"
       }
       name = "delegation"
     }
   }
   ```

   Here, we delegate the subnet to MySQL Flexible Servers (this is equivalent to CLI doing `--subnet ... --vnet ...`). We also have a random string resource `random_string.suffix` used to uniquify the RG name (not shown above but assumed defined). The delegation block ensures the subnet is ready for the MySQL service.

3. **Private DNS (for private access):** If using private access:

   ```hcl
   resource "azurerm_private_dns_zone" "mysql_private_dns" {
     name                = "privatelink.mysql.database.azure.com"
     resource_group_name = azurerm_resource_group.rg.name
   }

   resource "azurerm_private_dns_zone_virtual_network_link" "mysql_dns_link" {
     name                  = "mysql-dnslink"
     resource_group_name   = azurerm_resource_group.rg.name
     private_dns_zone_name = azurerm_private_dns_zone.mysql_private_dns.name
     virtual_network_id    = azurerm_virtual_network.vnet.id
   }
   ```

   This creates a Private DNS Zone for the MySQL private endpoint domain and links it to the VNet ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=,id)) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=resource%20,id%20geo_redundant_backup_enabled%20%3D%20false)). The zone name is the standard name used by Azure for MySQL flexible server private endpoints.

4. **MySQL Flexible Server Resource:** Now the main part – create the MySQL server:

   ```hcl
   resource "azurerm_mysql_flexible_server" "mysql" {
     name                = "${var.mysql_server_name_prefix}-${random_string.suffix.result}"
     location            = azurerm_resource_group.rg.location
     resource_group_name = azurerm_resource_group.rg.name

     administrator_login          = var.mysql_admin_login
     administrator_password       = var.mysql_admin_password
     version                      = "8.0"  # or "5.7"
     sku_name                     = "Standard_D2ds_v4"  # 2 vCore Gen Purpose
     storage_size                 = 50  # GB
     backup_retention_days        = 7
     geo_redundant_backup_enabled = true
     delegated_subnet_id          = azurerm_subnet.mysql_subnet.id
     private_dns_zone_id          = azurerm_private_dns_zone.mysql_private_dns.id

     high_availability {
       mode          = "ZoneRedundant"
       standby_zone  = 2
     }
     # optional maintenance_window block if we want to set a specific maintenance time
     maintenance_window {
       day_of_week  = 0   # Sunday
       start_hour   = 3   # 3 AM UTC
       start_minute = 0
     }
     tags = {
       Environment = var.env_tag
       Project     = "MyApp"
     }
   }
   ```

   This Terraform resource corresponds to creating the MySQL server similar to the CLI we ran. Notice:

   - We reference the `delegated_subnet_id` (linking to the subnet created) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=administrator_password%20%20%20%20,8.0.21)) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=storage%20,360%20size_gb%20%3D%2020)).
   - `private_dns_zone_id` is specified so Azure knows to link the server to that DNS zone ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=administrator_password%20%20%20%20,8.0.21)) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=storage%20,360%20size_gb%20%3D%2020)).
   - We set `high_availability.mode` to ZoneRedundant and specify a standby zone.
   - Provided admin credentials (in production, avoid hardcoding passwords; use Terraform variables, or better, use Key Vault + Azure AD to fetch secrets).
   - We enabled geo_redundant_backup (so backups are copied to paired region).
   - Added tags for clarity.
     Terraform will ensure the MySQL server is created after the network and DNS are ready (implicitly via the resource references; we could also add explicit `depends_on` if needed, e.g., to ensure DNS link is made before server tries to register, but since we provided the zone ID Azure will handle registration after server creation). In the example from Azure, they added `depends_on = [azurerm_private_dns_zone_virtual_network_link.mysql_dns_link]` for the MySQL resource to avoid any timing issue ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=size_gb%20%3D%2020%20)).

5. **Database Creation:** You can also have Terraform create a database inside the server:

   ```hcl
   resource "azurerm_mysql_flexible_database" "appdb" {
     name                = "myappdb"
     resource_group_name = azurerm_resource_group.rg.name
     server_name         = azurerm_mysql_flexible_server.mysql.name
     charset             = "utf8mb4"
     collation           = "utf8mb4_unicode_ci"
   }
   ```

   This will create a database named _myappdb_ once the server is up ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=4,and%20insert%20the%20following%20code)). The admin user can then connect to this DB.

6. **Variables and Outputs:** Use `variables.tf` to define inputs like location, admin username, etc., and `outputs.tf` to output important info:

   ```hcl
   variable "mysql_admin_login" {
     type = string
     default = "dbadmin"
   }
   variable "mysql_admin_password" {
     type = string
   }
   # ... other variables for names, etc.

   output "mysql_server_name" {
     value = azurerm_mysql_flexible_server.mysql.name
   }
   output "mysql_host" {
     value = azurerm_mysql_flexible_server.mysql.fqdn
   }
   output "admin_user" {
     value = azurerm_mysql_flexible_server.mysql.administrator_login
   }
   output "admin_password" {
     value     = azurerm_mysql_flexible_server.mysql.administrator_password
     sensitive = true
   }
   output "database_name" {
     value = azurerm_mysql_flexible_database.appdb.name
   }
   ```

   These outputs will show, for example, the MySQL server name, host, and credentials after `terraform apply`, which is useful for quickly grabbing connection info ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=output%20,name)) ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=match%20at%20L263%20value%20,administrator_password)).

7. **Applying Terraform:** Once your files are ready, run:
   ```bash
   terraform init        # initialize provider plugins and backend
   terraform plan        # see the execution plan
   terraform apply       # apply the changes (you'll be prompted to approve)
   ```
   Terraform will create all resources. The order is determined automatically by dependencies. For instance, the subnet must exist before the MySQL server is created (Terraform knows this via the `delegated_subnet_id` reference). Similarly, the DNS zone link must exist before MySQL tries to register DNS (that’s why the example had an explicit depends_on to be safe ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=size_gb%20%3D%2020%20))).

After apply, you should have a MySQL server running, identical to one created manually or via CLI. Terraform will output the values we specified, which you should store securely (especially the password). You can now use Terraform to manage updates: for example, change a parameter in .tf and run `terraform apply` to implement it, or use Terraform to destroy everything when no longer needed (`terraform destroy` will delete all these resources in the correct order).

## Managing Infrastructure State

Terraform maintains a **state file** that tracks the resources it created and their current state. Managing this state is crucial, especially in team environments:

- **State File Basics:** By default, Terraform stores state locally in a `terraform.tfstate` file. This file contains resource IDs and attributes. For collaborative usage or automation, storing state remotely is recommended.

- **Remote State (Azure Blob Storage):** A common practice is to use an Azure Storage account as a backend for Terraform state. This allows multiple team members or CI pipelines to work on the same infrastructure state safely. For example, in your Terraform configuration (in the `terraform { }` block), you can add:

  ```hcl
  backend "azurerm" {
    resource_group_name  = "<state-storage-rg>"
    storage_account_name = "<storageaccountname>"
    container_name       = "<container-name>"
    key                  = "terraform.tfstate"
  }
  ```

  Then run `terraform init` to migrate state to Azure. With this, the state is stored as a blob, and Terraform uses Azure Blob’s built-in **state locking** to prevent concurrent changes ([Backend Type: azurerm | Terraform - HashiCorp Developer](https://developer.hashicorp.com/terraform/language/backend/azurerm#:~:text=Backend%20Type%3A%20azurerm%20,Azure%20Blob%20Storage%20native)) ([Azure Blob Storage as Terraform backend - DEV Community](https://dev.to/cvitaa11/azure-blob-storage-as-terraform-backend-2bhj#:~:text=Azure%20Blob%20Storage%20as%20Terraform,Storage%20blobs%20are%20automatically)). Make sure the storage account is highly available (use GRS if needed) and restrict access (e.g., via SAS token or AD integration) because the state may contain sensitive info (like DB passwords in our outputs).

- **State Management Commands:** Terraform provides commands like `terraform state list` to see resources, `terraform state show <resource>` to see details, and if necessary, `terraform state rm` to remove a resource from state (if you managed it outside Terraform). Use these carefully. For example, if someone manually deletes a resource in Azure, Terraform state will be out of sync; running `terraform plan` will show that resource as to-be-created again. If the resource was deleted intentionally outside Terraform, best practice is to also remove it from state (or import it back if deletion was a mistake).

- **Infrastructure as Code Best Practices:**

  - Keep your Terraform code in source control (Git). Treat it like code – use pull requests, code reviews for changes.
  - Use workspaces or separate state files for different environments (dev, stage, prod) to avoid cross-environment interference.
  - Use Terraform Cloud or Azure Pipeline tasks for automation if needed. These can also handle state for you.
  - Protect your state file; if using local state for testing, don’t commit it to git, and if remote, ensure access is limited.

- **Upgrading Infrastructure:** When Azure releases new features (e.g., new MySQL versions or parameters), you may need to update the AzureRM provider. Keep an eye on provider release notes. Always run `terraform plan` after upgrading provider versions to see if it wants to make any unexpected changes.

By managing the Terraform state properly, you ensure that your MySQL infrastructure can be reliably maintained and shared across your team without conflicts.

## Applying Terraform Modules and Best Practices

As your infrastructure grows, your Terraform code can become complex. Terraform **modules** help encapsulate and reuse configurations. For MySQL deployment, you might create a module that includes all resources for a MySQL instance (server, DB, vnet etc.), making it easy to deploy multiple instances with similar configurations (e.g., a prod and a test database, or separate instances for different microservices). Here’s how to use modules and some best practices:

- **Creating a Module:** A module is essentially a directory with Terraform files. For example, you can turn the MySQL setup we wrote into a module by placing it in a folder like `modules/azure-mysql/` and adding a `variables.tf` to pass parameters (like server name, admin creds, etc.). Then, in your main terraform config, you use:

  ```hcl
  module "mydb" {
    source = "./modules/azure-mysql"
    mysql_server_name_prefix = "prod-db01"
    mysql_admin_login = "dbadmin"
    mysql_admin_password = var.db_password  # perhaps passed in from root module var
    env_tag = "Production"
    # ... other variables needed by module
  }
  ```

  This way, the module code can be reused for another DB:

  ```hcl
  module "mydb_test" {
    source = "./modules/azure-mysql"
    mysql_server_name_prefix = "test-db01"
    mysql_admin_login = "dbadmin"
    mysql_admin_password = var.test_db_password
    env_tag = "Test"
    # possibly override location or size if needed
  }
  ```

- **Using Community Modules:** Check Terraform Registry for community modules. For instance, there might be published modules like `claranet/azurerm-db-mysql-flexible` on GitHub or the registry ([claranet/terraform-azurerm-db-mysql-flexible - GitHub](https://github.com/claranet/terraform-azurerm-db-mysql-flexible#:~:text=claranet%2Fterraform,enabled%20logging%20and%20firewall%20rules)). These can simplify deployment by providing abstraction and best practices (like automatically enabling diagnostics, or creating multiple resources). If you choose to use one, carefully review the module’s input/output and behavior to ensure it matches your needs. A module might provision things you don’t need (like by default enabling public access or certain monitoring). Always override defaults appropriately.

- **Best Practices in Code:**
  - **Separate Concerns:** Organize Terraform code by resource types or functional areas. We did a bit: e.g., network in one section, DB in another. You might split into files: `network.tf`, `database.tf`, `monitoring.tf`, etc., for clarity.
  - **Variables and Defaults:** Provide reasonable defaults for variables (especially in modules) so that not everything needs to be specified every time. For example, default backup retention 7, etc., but allow override.
  - **Avoid Hardcoding Sensitive Data:** Use variables for any secrets (never commit plaintext passwords in .tf files). And consider using HashiCorp Vault or Azure Key Vault integration if Terraform needs to fetch secrets at runtime.
  - **Outputs:** Only output what’s necessary, and mark sensitive outputs (like passwords) with the `sensitive = true` flag so Terraform redacts them in logs ([Quickstart: Create a Flexible Server By Using Terraform - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-terraform#:~:text=)).
  - **Lifecycle Management:** If you have resources that shouldn’t be destroyed/recreated on minor changes, use lifecycle blocks to prevent destruction. For example, you might set `prevent_destroy` on the database resource to avoid accidental drops, or ignore changes for certain parameters that aren’t critical.
  - **Tags:** Enforce tagging via variables and locals. This helps with governance (Azure cost management, etc., by tagging environment, owner, etc.).

Using modules and following best practices ensures that your Terraform code for MySQL (and other infrastructure) is DRY (Don’t Repeat Yourself), maintainable, and scalable as your deployment grows.

## Automating Scaling and Monitoring with Terraform

Terraform can not only provision the MySQL server itself but also related components like alert rules, monitoring diagnostics, and even scaling configurations. While Terraform is not a live monitoring tool (it doesn’t react to load changes by itself), you can use it to set up Azure Monitor and even scheduled scaling scripts. Here are advanced scenarios:

- **Scaling MySQL via Terraform:** Scaling in Azure MySQL typically means changing the SKU (vCores/memory) or storage. If you anticipate scaling up the server as load grows, you could define those as variables (so you just change a var and re-apply to scale). For example, to scale from 2vCore to 4vCore, you’d update `sku_name` to a 4vCore SKU and `terraform apply`. This will trigger Azure to perform an online resize (for vCore scale up, this might cause a momentary disconnect but usually is quick). Storage increases are online and instant up to the MB level; reducing storage isn't allowed. You can also scale between tiers (Burstable to General Purpose) with a Terraform change, but note scaling _down_ tiers might not be supported if the current usage exceeds limits of lower tier.

- **Automated Scaling:** If you want automatic scaling based on load, Azure Database for MySQL doesn’t have an autoscale feature like VM scale sets. You would need to implement a custom solution. For example:

  - Use Azure Monitor metrics (CPU, connections, etc.) with alerts, and trigger an Azure Function or Logic App when thresholds are met. That function could run Terraform (via CI pipeline or using Terraform Cloud API) or call Azure CLI to scale the server (Azure CLI can update the SKU).
  - Another approach is using Azure Automation Runbooks or Azure Functions with Managed Identity that have permission to upscale the database. They can call `az mysql flexible-server update --sku-name ...` based on a schedule or event. This goes a bit outside Terraform (because Terraform by design doesn’t auto-trigger on events), but you can still keep the desired state in Terraform (e.g., if a scale up happened outside of Terraform, update the .tf to match actual state to avoid drift).

- **Monitoring Setup via Terraform:** Azure Monitor allows creating metric alert rules, log analytics workspaces, and diagnostic settings – all manageable by Terraform:

  - **Diagnostic Settings:** You can configure MySQL Flexible Server to send logs and metrics to Log Analytics or Storage. Terraform resource `azurerm_monitor_diagnostic_setting` can be used. For example:

    ```hcl
    resource "azurerm_monitor_diagnostic_setting" "mysql_diagnostics" {
      name               = "mysql-monitor"
      target_resource_id = azurerm_mysql_flexible_server.mysql.id
      log_analytics_workspace_id = azurerm_log_analytics_workspace.myworkspace.id

      metric {
        category = "AllMetrics"
        enabled  = true
      }
      log {
        category = "MySQLSlowLogs"
        enabled  = true
        retention_policy {
          enabled = false
        }
      }
      log {
        category = "MySQLAuditLogs"
        enabled  = true
      }
      # ... (other categories like MySQLConnectorLogs, etc., if available)
    }
    ```

    This will route metrics and specific logs (slow query log, audit log) to a Log Analytics workspace for analysis ([azurerm_monitor_diagnostic_set...](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_diagnostic_setting#:~:text=At%20least%20one%20enabled_log%20or,%28Optional%29)). Ensure the MySQL server has those logs enabled at the server (e.g., set `slow_query_log` parameter ON, etc.). Now you can use Azure Monitor Workbooks or queries on that workspace to analyze performance.

  - **Metric Alerts:** Terraform can create metric alert rules. Azure provides metrics such as CPU %, Memory %, Storage %, Connections count, etc., for MySQL. For instance, to create an alert when CPU exceeds 80% for 5 minutes:

    ```hcl
    resource "azurerm_monitor_metric_alert" "high_cpu_alert" {
      name                = "mysql-high-cpu"
      resource_group_name = azurerm_resource_group.rg.name
      scopes              = [azurerm_mysql_flexible_server.mysql.id]
      description         = "Alert if CPU > 80% for 5 min"
      severity            = 3
      frequency           = "PT5M"
      window_size         = "PT5M"

      criterion {
        metric_namespace = "Microsoft.DBforMySQL/flexibleServers"
        metric_name      = "cpu_percent"
        aggregation      = "Average"
        operator         = "GreaterThan"
        threshold        = 80
      }

      action {
        action_group_id = azurerm_monitor_action_group.pagerduty_ag.id
      }
    }
    ```

    This would fire an alert that can trigger an Action Group (e.g., email, PagerDuty, etc.). We reference a hypothetical `azurerm_monitor_action_group` which you would define with the details of notification (email/SMS/webhook) as needed. Azure’s best practice is to set alerts on key metrics like CPU, storage percent, active connections, etc., to catch issues early ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=Active%20connections)) ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=,connection%20limits%20for%20each%20SKU)). Terraform-managed alerts ensure that your monitoring configuration is version-controlled and consistent across deployments.

  - **Log Analytics and Workbooks:** You could use Terraform to create a Log Analytics workspace (`azurerm_log_analytics_workspace`) and even deploy a Workbook or queries. Azure’s MySQL team provides a sample workbook for performance analysis ([Configure Audit Logs - Azure Database for MySQL - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/tutorial-configure-audit#:~:text=Configure%20Audit%20Logs%20,Azure%20Database%20for%20MySQL)). While Terraform might not directly deploy a workbook JSON, you could use ARM template deployment via Terraform to push a workbook definition.

- **Ensuring Monitoring Best Practices:** After deploying, verify that:
  - You have **alerts for high utilization** (CPU, memory, connections, IOPS).
  - **Alerts for connectivity issues**: e.g., if the server is down (Azure will show metric like “server connectivity” or you may rely on availability metrics).
  - **Audit logs** are being collected if needed (especially if using Azure AD auth or to detect failed logins). Azure’s audit logs can be sent to Log Analytics where you can run queries or set alerts on certain events (like many failed logins).
  - **Storage auto-grow** is enabled (this can be set in Terraform by `auto_grow_enabled = true` in storage block or CLI `--storage-auto-grow Enabled` ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=%5B,tags)) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=,iops%20500))). This avoids running out of storage by automatically increasing the storage size when approaching capacity (up to a max of 16TB). It's often wise to enable this to prevent the database from becoming read-only if storage is full.

Using Terraform to set up these monitoring aspects means your environment comes out-of-the-box with the needed observability.

In summary, while Terraform itself doesn’t auto-scale or auto-heal the database, it’s an excellent tool to **deploy the hooks and configuration** for scaling and monitoring:

- You can declaratively set the database capacity and change it as needed (semi-automated scaling via IaC).
- You can deploy all monitoring rules and diagnostic settings so that any new environment has the same checks and balances.

---

# Security and Performance Optimization

Operating a production MySQL database in Azure requires careful attention to security and performance. This section covers advanced best practices for securing your Azure MySQL and tuning it for optimal performance. We also discuss high availability configurations and disaster recovery strategies to ensure business continuity.

## Best Practices for Securing MySQL in Azure

Security must be implemented in layers: network security, authentication/authorization, encryption, and monitoring for threats. Here are best practices in each area:

- **Network Security:** Favor private network connectivity. Deploy MySQL Flexible Server in a VNet (private access) so that it’s not exposed to the internet ([Quickstart: Create a Flexible Server By Using the Azure CLI - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-cli#:~:text=The%20connectivity%20method%20can%27t%20be,the%20article%20about%20networking%20concepts)). If you must use public access for certain reasons, lock down firewall rules to specific IPs – never leave it open to all IPs (0.0.0.0/0) except perhaps temporarily for troubleshooting. Also, consider using Azure Private Link for any services that need to talk to the database from other networks, instead of public endpoints. Within Azure, avoid data exfiltration by using service endpoints or private links such that the database isn’t accessible outside your Azure environment.

- **Authentication and Access Control:** Use Azure AD authentication for MySQL when possible, as it integrates with corporate identities and enables features like MFA. This avoids managing individual user passwords in MySQL. When using Azure AD auth, you can centrally revoke access (via AD) and use conditional access policies for strong security ([Microsoft Entra Authentication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-azure-ad-authentication#:~:text=Microsoft%20Entra%20Authentication%20,defined%20in%20Microsoft%20Entra%20ID)). For MySQL native users, enforce strong passwords and use the principle of least privilege – applications should have their own logins with only the necessary privileges on their specific database, not the all-powerful admin. Regularly review user accounts with `SELECT * FROM mysql.user;` and remove any that are unnecessary.

- **Encryption:** Ensure **encryption in transit** and **at rest**:

  - _Transit:_ SSL/TLS should be required (`require_secure_transport=ON`). Azure’s MySQL service provides SSL by default, with a certificate you can download. Configure your application’s MySQL connectors to use SSL and verify the server certificate. This prevents eavesdropping and MITM attacks on data in transit.
  - _At Rest:_ Azure automatically encrypts data at rest using service-managed keys. For extra control, use customer-managed keys (CMK) in Azure Key Vault ([Data Encryption With Customer Managed Keys - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-customer-managed-key#:~:text=Server%20learn,for%20data%20protection%20at%20rest)). This way, even Azure admins can’t access your data without your key, and you can revoke or rotate the key. Just ensure Key Vault availability (if the key is unavailable, database operations might be affected).

- **Patching and Maintenance:** Azure applies security patches to the underlying OS and MySQL engine. Use **Maintenance Windows** (as configured in Flexible Server) to control when patches are applied ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=%2A%20Zone,Elastic%20scaling%20within%20seconds)). Pick a time of low usage for your business, so any short interruptions (if a reboot is needed) have minimal impact. Stay on supported MySQL versions and plan upgrades (MySQL 5.7 goes out of community support eventually; Azure will schedule an upgrade to 8.0 at some point). Test your application on newer versions in advance.

- **Data Protection:** Implement role-based access control (RBAC) at the Azure level. For example, grant only specific Azure AD groups the ability to manage the Azure MySQL server (using Azure RBAC roles like _Azure DB for MySQL Contributor_). This prevents unauthorized Azure users from altering or deleting your instance. Also enable _Soft Delete_ for the MySQL server backups if available, so that if a server is accidentally deleted, backups still exist for recovery (Azure automatically keeps backups for the retention period even if the server is deleted, within that retention window).

- **Auditing and Threat Detection:** Turn on MySQL auditing to log connections and queries. Azure’s **MySQL Audit Logs** when enabled can record successful and failed logins, and other activity. Forward these to Log Analytics. Use **Microsoft Defender for Cloud** (previously Advanced Threat Protection) on your MySQL server – it can detect anomalous patterns like SQL injection or data exfiltration attempts and alert you ([What's happening to Azure Database for MySQL single server? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/migrate/whats-happening-to-mysql-single-server#:~:text=,isn%27t%20supported)) ([What's happening to Azure Database for MySQL single server? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/migrate/whats-happening-to-mysql-single-server#:~:text=,Cloud%20properties%20in%20Flexible%20Server)). While there’s a cost for this, it’s valuable for early threat detection. If you get an alert (e.g., unusual number of failed logins or a suspicious query pattern), respond immediately by investigating and potentially isolating the database (e.g., toggle to private access, change passwords, etc.).

- **Compliance:** If you have compliance requirements (PCI, HIPAA, etc.), ensure your configuration meets them. For instance, PCI might require encryption of data in transit and at rest (which we have), regular rotation of credentials, and separation of duties (don't use one admin account for everything). Azure MySQL is PCI DSS and HIPAA compliant as a service, but you must configure it correctly (e.g., enable audit, restrict access) to be compliant in practice.

- **Backup Security:** Your backups (especially if exported dumps) should be protected. Azure’s automated backups are secured by Azure (and by your Key Vault key if you use CMK). If you take manual dumps, store them in secure storage (Azure Blob with limited access, perhaps encrypted with your own key). Also, sanitize sensitive data if using copies of databases in lower environments.

By implementing these practices, you create a defense-in-depth for your Azure MySQL: network isolation, strong auth, encryption, continuous monitoring, and secure processes, aligning with the principle that your database security is only as strong as the weakest link.

## Performance Tuning and Query Optimization

Performance tuning for MySQL on Azure is similar to on-prem MySQL, with the additional consideration of cloud-specific resources and limits. Here are key areas and best practices for performance and query optimization:

- **Choosing the Right SKU and Tier:** Initially, choose the appropriate Azure MySQL SKU size and tier for your workload. The tiers (Burstable, General Purpose, Memory Optimized) offer different CPU/Memory ratios and IOPS limits ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server%20delivers)) ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Less%20HA%20options%20than%20flexible)). For example, use General Purpose for balanced workloads and Memory Optimized for heavy in-memory OLTP workloads. A common pitfall is under-provisioning the vCores or using the Burstable tier for a workload that requires consistent performance – Burstable instances can throttle if credits run out. Monitor CPU credits if on Burstable, or simply use GP tier if the workload is steady.

- **InnoDB Configuration:** Most MySQL deployments use InnoDB engine. Azure’s service sets InnoDB parameters based on the tier (e.g., `innodb_buffer_pool_size` is automatically tuned to a percentage of available memory on Flexible Server). Ensure your working set fits in memory (buffer pool) for optimal performance; if not, consider scaling up or optimizing queries to reduce working set. While you might not manually adjust `innodb_buffer_pool_size` in PaaS, you should be aware of how it scales with instance size.

- **Indexing and Schema Design:** No cloud magic can compensate for poor schema design. Regularly review slow queries (enable the slow query log: set `slow_query_log=ON` and `long_query_time` appropriately, e.g., 200ms) and analyze them. Use `EXPLAIN` plans to see if indexes are being used. Add indexes on columns used in JOINs, WHERE filters, and ORDER BY if needed. Be cautious not to over-index (which slows writes). Ensure each table has a primary key ([Best practices for server operations on Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-operation-excellence-best-practices#:~:text=Best%20practices%20for%20server%20operations,for%20MySQL%20Flexible%20Server%20instance)) – InnoDB works best with a primary key for clustering. Avoid very large numbers of partitions or extremely large multi-join queries that might not scale.

- **Query Optimization:** For heavy or frequent queries, consider:

  - **Caching:** Implement caching at the application layer (using something like Azure Cache for Redis) for frequent read queries results that don’t need to hit the DB every time.
  - **Connection Pooling:** Creating new connections is expensive. Use connection pooling in your application (most frameworks have this) to reuse MySQL connections rather than constantly connecting/disconnecting ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Establishing%20a%20new%20connection%20is,options%20for%20good%20connection%20practices)). This reduces connection overhead and helps avoid hitting connection limits. Azure MySQL has a connection limit depending on SKU (e.g., a few hundred connections). A pool will help you stay efficient with e.g., 50-100 connections reused by threads.
  - **Batching and Pagination:** Instead of doing many small queries, batch them if possible (e.g., insert multiple rows in one statement). For large result sets, use proper pagination (LIMIT/OFFSET) or retrieval in chunks rather than one huge result that can exhaust memory.
  - **Stored Procedures or JSON Processing:** Sometimes doing processing closer to the database can reduce data transfer (for example, filtering or aggregating in SQL rather than fetching raw data and processing in the app). But be mindful that complex stored procedures can be hard to maintain; weigh the trade-offs.

- **Monitoring and Tuning OS Level Metrics:** Azure abstracts the OS, but you can monitor resource metrics:

  - **CPU Usage:** If constantly high (over 80%), either queries are not optimized or you need more vCores. Check if the CPU is system or user – if system, it could be IO wait or context switching overhead; if user, it’s actually working on queries. Add indices or refactor queries to reduce CPU. If that’s insufficient, scale up the SKU (CPU).
  - **Memory:** Monitor memory% in Azure metrics. If memory is near 100% and you see evidence of swapping or eviction from buffer pool (metrics like “InnoDB buffer pool pages free” low, or high read IOPS indicating it’s reading from disk frequently), consider scaling to a tier with more memory or reducing memory usage (like caching fewer connections, etc.). Memory Optimized tier gives more memory per vCore.
  - **IOPS and Storage Throughput:** Azure GP tier storage has a max IOPS based on provisioned storage (e.g., 3 IOPS per GB up to a cap, etc.). If you see IOPS or IO latency as a bottleneck (Azure Monitor metric “Storage IO consumed” high), you might need to provision more storage to get more IOPS (even if you don’t need the space) ([
    Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,restore%20to%20a%20different%20region)) or consider upgrading to a higher tier that has better I/O (Azure’s Business Critical tier, if available for MySQL, which might use faster storage). Also, enabling **Accelerated Networking** on client VMs or using services like ProxySQL can improve network throughput to the DB ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Accelerated%20networking)).
  - **Query Performance Insights:** Although Azure MySQL doesn’t have a built-in “Query Performance Insight” like Azure SQL DB, you can derive similar insights by capturing slow query logs to Log Analytics and analyzing which queries take the most time or resources. There are third-party tools and also the Performance Schema in MySQL which can give insight on indexes usage, etc. You can enable Performance Schema (though it has some overhead) by setting `performance_schema=ON` if not already, and use it to find bottlenecks (like table lock contention, etc.).

- **Scaling Out Reads:** If you have a read-heavy workload, use **Read Replicas**. Azure MySQL Flexible allows up to 10 read replicas ([
  Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Can%E2%80%99t%20restore%20cross%20region)). These are async replicas that can offload read traffic. You can create replicas via CLI:

  ```bash
  az mysql flexible-server replica create -g MyResourceGroup -n prod-db01-replica1 --source-server prod-db01
  ```

  This will create a new server that replicates from the primary. Direct your read-only queries (analytics, report generation, etc.) to the replica. Keep in mind replicas are eventually consistent (some lag). Monitor the replication lag (there’s a metric for Seconds Behind Master in Azure). If lag is an issue, the replica might need to be a higher SKU or the write load on primary needs optimizing. For geo-distributed apps, you could place a replica in a different region close to users for read-local, but that will increase latency of replication.

- **Connection Latency:** Ensure your application is in the same region (and ideally same availability zone) as the MySQL server to minimize latency ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Physical%20proximity)) ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=To%20improve%20the%20performance%20and,as%20resources%20are%20closely%20paired)). Each extra millisecond adds up for queries. If using Azure Functions or App Services, deploy them in the same region and integrate with the same VNet if using private access. Use tools like `SELECT 1` ping times or `mysqladmin ping` to measure latency between app and DB. Azure’s backbone is fast, but region-to-region or zone-to-zone could add latency.

- **Benchmark and Test:** For critical applications, do load testing. Use a dataset similar to production and run simulations (using tools like sysbench or MySQLslap, or application-level tests). Identify which part fails or slows down first: CPU, memory, IO, or hitting a MySQL internal limit. Azure’s performance best practices guide suggests close pairing of app and DB, and using accelerated networking, etc., which we’ve covered ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Physical%20proximity)) ([Performance Best Practices - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concept-performance-best-practices#:~:text=Accelerated%20networking)).

- **Continuous Tuning:** Performance tuning isn’t a one-time task. Continuously monitor metrics and slow query logs. As data grows, previously fast queries may become slow (maybe an index is needed after data size crosses a threshold, or maintenance like index rebuild is needed occasionally if index fragmentation becomes an issue – though InnoDB auto-manages reasonably well). Use Azure Advisor or recommendations if available – sometimes Azure can detect suboptimal settings (for example, it might recommend enabling _Accelerated Logs_ feature for high throughput workloads ([What's New - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/select-right-deployment-type#:~:text=Accelerated%20Logs%20Enabled%20for%20All,New%20Business%20Critical%20Servers)), which is a new feature on Business Critical tier to improve commit latency).

In summary, combine **MySQL best practices** (proper indexing, query optimization, caching, connection pooling) with **Azure-specific tuning** (right tier/SKU, scaling resources as needed, minimizing network latency). This will ensure your Azure MySQL database performs well and can handle your application's workload efficiently.

## High Availability and Disaster Recovery Strategies

Ensuring that your database is highly available and can recover from failures is paramount for production systems. Azure provides capabilities for HA within a region, and you should design a DR strategy for region-wide outages. Let’s break down HA and DR:

- **High Availability (HA) Within a Region:** With Azure Database for MySQL – Flexible Server, you can configure HA when creating the server:

  - **Zone-Redundant HA:** As discussed, this creates a standby instance in a different availability zone. It uses synchronous replication (within region) to keep the standby up-to-date. In the event the primary fails or the entire AZ goes down, Azure automatically fails over to the standby in the other zone. Failover typically completes within ~30 seconds to a minute, during which there might be a brief outage (connections dropped, in-flight transactions may rollback). This option significantly increases resiliency and is recommended for mission-critical databases ([Azure Database for MySQL - Flexible Server Overview - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server%20delivers)). The cost is essentially double (since there's two instances), but the standby is only charged at a lower rate until failover.
  - **Same-Zone HA:** If you don’t have multiple AZs or choose to keep both nodes in one AZ (to minimize latency between them), you can deploy HA in the same zone ([
    Azure DB for MySQL – Single server vs Flexible | All About Tech ](https://blobeater.blog/2022/01/19/azure-db-for-mysql-single-server-vs-flexible/#:~:text=,Can%E2%80%99t%20restore%20cross%20region)). This protects against server-level failure (if the primary VM crashes, failover to standby VM in same datacenter). However, it won’t help if the whole datacenter goes offline.
  - **Replica as HA:** Another approach (for Single Server previously or even Flexible) is to create a read replica and in case of primary failure, you can perform a manual failover by promoting a replica to read-write (for Flexible, Azure CLI has `az mysql flexible-server replica stop-replication` which converts a replica to a standalone server ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=match%20at%20L345%20az%20mysql,replication))). This is not as seamless or fast as built-in HA, but it’s a backup approach. With built-in HA available, this is mainly useful for cross-region replicas (for DR) rather than within-region HA.

- **Backup and Restore (PITR) for HA:** Even with HA, always have backups. If a logical error occurs (e.g., someone accidentally deletes data or a bad migration query), HA won't save you because the deletion replicates to standby. In such case, you rely on backup to restore to point-in-time before the error. So, use HA for hardware/network failures, and backups for recovery from logical errors or total failures.

- **Disaster Recovery (DR) Across Regions:** HA covers region-internal issues. For region outages (rare but possible, e.g., due to natural disaster or major Azure incident), plan for DR:
  - **Geo-Redundant Backups:** Ensure geo-backup is enabled (`geo_redundant_backup = Enabled`) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=%5B,strategy)). This lets you perform a geo-restore in a secondary region. The RPO is the backup frequency (you could lose up to <5 minutes of data typically, since continuous backups are shipped). The RTO is the time to perform restore (could be several minutes to an hour depending on data size).
  - **Cross-Region Read Replicas:** Flexible Server introduced the ability to create a replica in another region (General Availability as of 2023) ([Cross-region read replicas in geo-paired regions (General Availability)](https://www.youtube.com/watch?v=Ow6il81_fC0#:~:text=Cross,only%20server%20in)). This is a great DR strategy: you have an active replica in (say) region B replicating from primary in region A. If region A goes down, you manually promote the replica in region B to become standalone (read-write) ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=match%20at%20L345%20az%20mysql,replication)). Your application would need to switch its connection strings to the new primary in region B. This approach can achieve much lower RPO (seconds) and RTO (a few minutes, basically DNS/application failover plus promotion time) compared to restoring from backup. _Note:_ Cross-region replication will incur data transfer costs for sending transaction logs between regions, and you'll be running another full server in the secondary region (cost consideration).
  - **Azure Traffic Manager / DNS for Failover:** If you implement a cross-region replica for DR, consider how your app will know to failover. You might use Azure Traffic Manager or a DNS CNAME that you can switch. For example, your app connects to a CNAME like `mydb.app.local` which points to primary’s FQDN. In failover, you update that CNAME to point to the DR server’s FQDN. Alternatively, have logic in app or an orchestrator to detect outage (maybe via the monitoring alerts) and reconfigure the connection string.
- **Testing DR:** Regularly test your DR plan. For instance, take a backup and restore it to a new server in DR region and connect a test app to validate data consistency. Or if you have a replica, try a planned failover during a maintenance window: stop replication to promote the replica, point a test workload to it. This will reveal any issues (like application not handling new host keys, etc.). After testing, you can re-establish replication (which might require re-creating the replica from scratch after the test, since once promoted it can’t sync back without reinitializing).

- **Handling Common Failover Issues:** On failover (even within region HA), some considerations:

  - The server name may change (in a geo-restore or new promotion scenario). If possible, abstract the connection string via config so it can be changed quickly.
  - The new primary might have a different IP (especially cross-region). If you use private endpoints, you’ll need to update DNS or link Vnets accordingly.
  - Ensure the application reconnect logic is robust – implement retry logic with exponential backoff, so that if the DB goes away for 30 seconds, the app will retry queries rather than crash. This is standard practice for transient fault handling in cloud environments.

- **Multi-Cloud or Hybrid DR:** In extreme cases where you want to guard against Azure-wide issues, you could replicate data out to an on-prem or AWS MySQL as a backup. Azure MySQL Flexible supports **Data-out replication** using binlog replication to an external MySQL server ([Configure Data-Out Replication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-data-out-replication#:~:text=Configure%20Data,the%20source%20and%20replica%20servers)). This requires configuring the MySQL primary to expose the binlog to the external replica (with appropriate firewall/VPN). This is advanced and rarely needed, but an option if required by policy. Similarly, **Data-in replication** can bring data from on-prem into Azure MySQL for migration or hybrid writes ([Azure Database for MySQL - Flexible Server Overview](https://docs.azure.cn/en-us/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server)).

- **Service Level Agreements (SLA):** With HA, Azure Database for MySQL offers a 99.99% SLA. Without HA, SLA might be 99.9%. Understand what that means: 99.99% uptime allows only ~4.4 minutes downtime per month. Use HA for critical apps to meet that. Also have an agreement on RPO/RTO with the business: e.g., RPO 5 minutes (meaning up to 5 min of data loss acceptable) and RTO 1 hour (service can be restored within 1 hour). With backups and cross-region replicas, you can likely achieve much better RPO/RTO, but set expectations and design accordingly.

By applying the above strategies, your MySQL deployment will be resilient against both minor disruptions and major disasters. High availability keeps your service running through common failures, and a solid disaster recovery plan ensures you can bring the system back online elsewhere if an entire region is impacted.

---

# Monitoring and Maintenance

Once your MySQL database is up and running, ongoing monitoring and maintenance are critical to ensure it remains healthy, performant, and secure. Azure provides extensive monitoring tools (Azure Monitor, Log Analytics) and easy ways to set up alerts. Maintenance tasks like updates and scaling should be regularly revisited. This section details how to monitor Azure MySQL and perform routine maintenance effectively.

## Setting up Azure Monitor and Alerts

**Azure Monitor** is the unified monitoring solution for Azure services, which Azure Database for MySQL plugs into. You can consume metrics and logs from your MySQL server in Azure Monitor and set up alert rules to notify you of important conditions. Here’s how:

- **Key Metrics to Monitor:** Azure Database for MySQL – Flexible exposes many metrics, such as CPU percentage, Memory percentage, Storage used, IOPS, Active Connections, Failed Connections, Network throughput, etc. ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=There%20are%20various%20metrics%20available,Azure%20portal%20or%20Azure%20CLI)). Focus on a few critical ones:

  - _CPU Utilization (%):_ High sustained CPU can indicate the need for query optimization or scaling up.
  - _Memory Utilization (%):_ If this is very high, you might risk hitting memory limits or swapping.
  - _Storage Used (% of allocated):_ This is crucial – if you approach 100%, the server will eventually enforce read-only mode to prevent data loss. Set alerts at, say, 80% and 90% used ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=5,choose%20Select%20condition)) ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=6,For%20example%2C%20select%20Storage%20percent)). Also monitor the storage auto-grow events if enabled.
  - _Active Connections:_ Monitor how close you are to the max connections limit. For instance, alert if > 80% of max connections in use ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=Active%20connections)) ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=,connection%20limits%20for%20each%20SKU)). If nearing limit, you may need to increase size (which raises max connections) or optimize connection usage (connection pooling).
  - _Failed Connections:_ A spike in failed connections could indicate an issue (like users failing to login, or the server hitting connection limits) ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=Failed%20connections)). If you see continuous failed connections, investigate authentication issues or client exceptions.
  - _Replica Lag:_ If using replicas, track replication lag. Azure might expose this as a metric (for Single server it was “Replication Lag”, for Flexible you might get it via performance_schema or the Azure portal metrics).
  - _Network In/Out:_ This shows the traffic. Unusually high outgoing traffic could indicate large data exfiltration (could be normal for a backup or abnormal if someone’s dumping your data).
  - _DTU or vCore % (if available):_ Some services have a computed “Compute Unit” usage. In MySQL’s case, CPU and IO are separate metrics.

- **Creating Alerts:** Use Azure Monitor Alerts to get notified or take action. For example:

  - An alert for CPU > 80% for 10 minutes ([Best practices for alerting on metrics with Azure Database for MySQL monitoring | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/best-practices-for-alerting-on-metrics-with-azure-database-for-mysql-monitoring/#:~:text=Active%20connections)).
  - An alert for storage > 85% ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=5,choose%20Select%20condition)).
  - An alert for replication lag > X seconds (if applicable).
  - An alert for any server going offline (there’s usually a metric “server_down” or you can alert on Heartbeat metric absence).
  - You can configure these via the Azure portal wizard ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=1,instance%20you%20want%20to%20monitor)) ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=5,choose%20Select%20condition)) or automate via Terraform as shown earlier. Make sure to set up an **Action Group** with your preferred notification method: email, SMS, or integration with incident management like PagerDuty or Azure DevOps.
  - If you prefer CLI: Azure CLI has `az monitor metrics alert` commands, but it might be simpler to configure via ARM template or Terraform.

- **Dashboarding:** Use Azure Portal to create a custom dashboard with key MySQL metrics charts. Pin CPU, Memory, Connections, etc., so you have at-a-glance view. Alternatively, use Azure Monitor Workbooks – there might be a pre-built workbook for MySQL performance (Azure provided a MySQL Insights workbook in preview). This can show top queries, resource utilization graphs over time, etc., in a single pane.

- **Log Monitoring:** If you enabled slow query or audit logs to Log Analytics, set up queries and alerts on those as well:

  - For slow logs: Query the log analytics for events where `duration > 1 sec` and maybe group by query to find top slow queries.
  - For audit: Alert on things like a particular user failing to login repeatedly (brute force attempt) or data export commands.
  - Example KQL for log analytics slow logs:
    ```kql
    AzureDiagnostics
    | where ResourceType == "MYSQL_FLEXIBLE_SERVERS"
    | where Category == "MySQLSlowLogs"
    | project TimeGenerated, QueryText, Duration, DatabaseName
    | order by Duration desc
    | take 5
    ```
    This would list the top 5 slowest queries in recent logs.

- **Integrating with Azure Monitor Alerts (advanced):** Consider enabling **Dynamic Thresholds** for alerts for metrics that have seasonal patterns. Azure Monitor can use ML to determine what’s “normal” and alert on deviations without you setting a static threshold ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=period%20dropdown%20list%20to%20select,longer%20history%20for%20the%20metric)) ([Configure Metrics Alerts - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-alert-on-metric#:~:text=,Every%2015%20Minutes)). For example, if CPU usage normally varies 20-50% but one day shoots to 70%, a dynamic alert might catch that if it’s out of norm.

## Using Log Analytics for Performance Insights

**Azure Log Analytics** (part of Azure Monitor) is a powerful tool to query and analyze logs and metrics. By funneling MySQL telemetry into Log Analytics, you can run complex analyses:

- **Enabling Diagnostic Logs:** As mentioned, enable diagnostic settings to send MySQL logs (slow query, audit, error logs) to a Log Analytics Workspace ([Deploy diagnostic settings to your Azure resources via a Terraform ...](https://medium.com/@antoine.loizeau/terraform-module-azure-diagnostic-settings-96b4bcd3737f#:~:text=Deploy%20diagnostic%20settings%20to%20your,This%20allows%20for%20in)). Also send metrics if you want to use Log Analytics for metrics (though metrics are natively in Monitor too).

- **Analyzing Query Performance:** With slow query logs in Log Analytics, you can identify which queries are slowing down the system. For example:

  - Find queries that appear frequently in slow logs: `summarize count() by QueryText`.
  - Compute average and max execution time per query: `summarize AvgDuration = avg(Duration), MaxDuration=max(Duration) by QueryText`.
  - Identify if slow queries correlate with certain times of day – cross reference timestamps with maybe workload patterns.

- **Auditing and Security via Logs:** If audit logs are enabled (or at least connection logs), you can track activity:

  - List all logins to the server and their source IP.
  - Detect if any unusual IP addresses connected (which might indicate a breach if firewall was too open).
  - Combine with Azure AD logs (if using AD auth) to see if unauthorized attempts correspond to AD sign-in logs.

- **Building Workbooks:** Azure Monitor Workbooks allow combining text, graphs, and queries into interactive reports. You could create a “MySQL Overview” workbook that shows:

  - Graph of CPU, memory over last 24h.
  - Graph of connections and failed connections.
  - Table of top 10 slow queries from logs in last 24h.
  - Table of recent security alerts or audit events.
  - This can be a one-stop for SREs/DBAs to monitor system health.

- **Retention and Analysis:** By default, Log Analytics retains data for 30 days (configurable). For long-term trending, consider increasing retention or exporting data to cold storage. For example, if you want to see performance trend over a year, you might export metrics to an Azure Storage or use Azure Data Explorer for long-term analysis.

- **Cost Consideration:** Sending logs and metrics to Log Analytics incurs costs (ingestion and retention costs). Filter out unneeded data – e.g., if you don't actively use audit logs, maybe don't enable them or route them to archive storage instead of Log Analytics. However, slow query logs and error logs are usually worth analyzing for performance improvements.

- **Proactive Performance Tuning:** By regularly reviewing Log Analytics data, you can proactively tune the database:
  - If you see a query’s duration creeping up over months, maybe the table is growing and needs an index.
  - If you notice memory usage trends upward as connections increase, perhaps implement better pooling or scale up before hitting a problem.
  - If at certain times (say end of month reports) CPU maxes out, maybe schedule scaling up the SKU during that period (and scale down after, which can be orchestrated with automation).

Using Log Analytics, you turn raw data into actionable insights – it’s like having a continuous audit of your database’s behavior.

## Scaling Database Resources Dynamically

Azure allows scaling of MySQL server resources relatively easily, but doing it with minimal downtime and in a controlled manner is important. “Dynamically” scaling implies you can adjust to load changes. Here’s how to approach scaling in practice:

- **Vertical Scaling (Scale Up/Down):** This is the primary way to handle changes in load. Azure Flexible Server supports scaling vCores up or down, changing the compute tier, and scaling storage up:

  - Scaling **compute (vCores)**: Increase vCores if CPU is saturated or you need more concurrency (also increases possible connections). Decrease vCores in off-hours to save cost if your workload allows (though frequent scaling down/up might not be ideal if it impacts performance briefly, and some tiers may not allow scaling down easily without downtime).
  - Scaling **tier**: Move from Burstable to General Purpose to get more consistent performance, or GP to Memory Optimized for more memory/vCore. This is a major change but Azure handles it as a simple update (may involve a restart of the instance).
  - Scaling **storage**: You can increase storage with zero downtime. This is useful if you’re nearing capacity or if you need more IOPS (since IOPS scale with storage size for GP tier). Enable **auto-grow** to let Azure add storage in 5 GB increments when free space is <10% ([az mysql flexible-server | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#:~:text=,iops%20500)). This prevents the app from ever encountering a “disk full” error, at the cost of extra storage charges (which is usually fine).
  - These actions can be done through Azure Portal sliders or via CLI/Terraform as discussed.

- **Horizontal Scaling (Read Scale-Out):** As noted, add read replicas to distribute read traffic. While not dynamic in the sense of auto-add/remove (you must add or remove them manually), you could script adding a replica if read load increases. Azure doesn’t auto-create replicas on demand, but you might maintain a couple of always-on replicas for load balancing reads. Some apps use a proxy (like ProxySQL or HAProxy) to split reads/writes between primary and replicas, which can effectively increase throughput by using more machines for reads.

- **Scaling with Minimal Downtime:** For vertical scaling:

  - In many cases, scaling vCores or changing performance tier in Azure Flexible Server is _online_ (the documentation suggests it performs the scale operation with minimal interruption, possibly a brief failover or a restart if moving to a different compute generation). When scaling, choose a low-traffic time if possible.
  - If you have HA enabled, some scale operations might be done by failing over to the standby which is already resized, to reduce downtime.
  - Always test scaling in a staging environment to understand the impact (e.g., how long a connection drop happens).
  - For storage, it’s online, but if you reduce storage (not supported directly), you’d need a dump and restore to a smaller server.

- **Automation of Scaling:** You might want to scale on a schedule or based on load:

  - **Scheduled scaling:** e.g., scale up every day at 9am and scale down at 9pm if nightly load is low. You can use Azure Automation or Logic Apps to trigger an `az mysql flexible-server update --sku-name ...` command on schedule. Or Terraform with a scheduled run (though Terraform is more state-centric; better to use CLI for purely scheduled changes).
  - **Reactive scaling:** As discussed, no native auto-scale for MySQL PaaS. But you can mimic it by hooking Azure Monitor alerts to an Action that calls an Azure Function to scale. For example, an alert when CPU > 80% for 1 hour triggers a Function that calls Azure CLI to increase vCores by 2. This function could also update some state store to avoid flapping (scale down only if CPU < 50% for some steady time).
  - Ensure your application can handle scaling events (like a momentary disconnect). Most can, but it’s worth verifying.

- **Maintaining Performance Post-Scaling:** After scaling up, monitor if the performance issue is resolved or if it shifts (e.g., after scaling vCores, maybe now IO is the bottleneck). Likewise, after scaling down, watch for any new constraints (maybe memory became insufficient).

- **Maintenance Tasks:** Besides scaling, routine maintenance includes:
  - Updating connection strings or rotating credentials (which we touched on security).
  - Upgrading MySQL engine version when the time comes (Azure will eventually force upgrades when old versions retire, but you should plan and test earlier).
  - Regularly cleaning up unused data or archiving old records (to keep tables smaller and performance optimal).
  - Analyzing and updating statistics or running optimize commands if needed (MySQL updates statistics automatically, but heavy write/delete workloads might benefit from `ANALYZE TABLE` or `OPTIMIZE TABLE` occasionally. Azure may throttle or not allow `OPTIMIZE TABLE` on very large tables, so be cautious.)

By staying proactive with monitoring and using scaling strategies, you can keep your Azure MySQL instance running smoothly without over-provisioning resources (which saves cost) while still meeting performance demands.

---

# Advanced Use Cases and Integration

Azure Database for MySQL can integrate with various Azure services and fit into complex architectures. In this section, we explore some advanced use cases: using MySQL with Azure Functions and App Services, deploying MySQL in containerized environments like AKS, hybrid cloud setups, and more. These scenarios demonstrate the flexibility of Azure’s MySQL service beyond just a standalone database.

## Integrating MySQL with Azure Functions and App Services

Azure Functions (serverless compute) and Azure App Service (web apps) are common places to run applications that need a database backend. Here’s how to integrate them with MySQL securely and efficiently:

- **Connection Strings and App Settings:** Both Functions and App Services allow you to store connection strings in the configuration (with encryption at rest). You should store something like:

  ```
  Server=prod-db01.mysql.database.azure.com; Database=myappdb; User Id=appuser@prod-db01; Password=<secret>; SslMode=Required;
  ```

  as a Connection String setting. Mark it as “MySQL” type if using App Service (there is a specific section for connection strings). The platform will inject these into environment variables that your application can read. Using configuration keeps credentials out of code.

- **VNet Integration:** If your MySQL is private (no public IP), your Function or Web App must be in the same VNet or have access:

  - For App Service, use **VNet Integration** (for outbound) to allow the app to reach into the VNet where MySQL lives. In App Service, this is the Feature where you integrate with a subnet (note: requires Standard tier or higher for App Service). Ensure the DNS settings of the App Service or its VNet can resolve the MySQL private DNS name (the Private DNS Zone linking we set up covers this if the VNet is the same or peered).
  - For Azure Functions, if on Consumption plan, VNet integration is possible via Regional VNet Integration or by running in a Premium plan with VNet access. Alternatively, deploy the Function in an App Service Plan which then can integrate with VNet similarly. Once integrated, the Function’s outbound traffic can reach the MySQL’s private endpoint.

- **Managed Identity for Secretless Connections:** Consider using **Azure Managed Identity** and Azure AD authentication for MySQL to avoid storing DB credentials at all. For example, you can give your App Service’s managed identity the rights as an Azure AD Admin or contained database user in MySQL. Then your app can obtain an access token for MySQL (with MSAL library, requesting the token for Azure Database for MySQL scope) and use that token to connect (supported in connector libraries that allow AD auth, like Azure’s MySQL connector for .NET or using `mysql` CLI with `--enable-cleartext-plugin` for AD tokens). This is complex but eliminates passwords in config, and rotation is handled by AD.

- **Performance Considerations for Functions/WebApps:** Functions are ephemeral, they might open new connections frequently. Use connection pooling globally in your function code if possible (e.g., in a static client or a globally cached connection). Azure Functions in .NET can reuse static objects across invocations on the same instance, so use that to hold a MySQL connection or pool. Similarly, web apps should use pooling (e.g., ADO.NET or JDBC connection pools). Without pooling, you may exhaust connection limits or pay performance penalty for each cold connection.

- **Scaling Out App Service:** If your App Service scales out to multiple instances, each will have its own set of DB connections. Ensure MySQL can handle it (maybe increase the max connections or scale up compute if needed). Use Azure Monitor to see connections spike when scaling.

- **Using MySQL with Azure PaaS Web Apps (LAMP stack):** Azure offers a Linux App Service where you can deploy PHP applications (WordPress, etc.) and use Azure MySQL as backend. This integration is straightforward since Azure provides MySQL connection info as app settings. There’s also an Azure Database for MySQL connector in Azure Web App’s UI that helps link the two. The key is to ensure the connection string is correctly configured and the networking is open (for example, allow the App Service outbound IPs in the MySQL firewall if using public). If both are in Azure, prefer VNet Integration and private MySQL to avoid exposing to internet.

In summary, Azure Functions and App Services can seamlessly use Azure MySQL – just pay attention to storing credentials securely (or use identities) and networking so they can talk to each other.

## Using MySQL with Kubernetes (AKS)

If your architecture uses containers and Kubernetes (AKS – Azure Kubernetes Service), you may want to use Azure MySQL as the database for apps running in AKS, or even run MySQL in a container (though running a stateful MySQL on AKS is usually not as managed as using the PaaS service). Let’s focus on using the managed MySQL from AKS:

- **Connectivity from AKS:** There are two main ways to connect from an AKS cluster to an Azure MySQL:

  1. **Public endpoint**: If Azure MySQL has a public IP and firewall allows the AKS node IP range or Azure services, the pods can connect over the internet (or Azure backbone). Ensure to enable SSL. This is simpler but less secure because you must allow the whole node subnet (which might be broad).
  2. **Private endpoint via VNet**: If you use Azure MySQL with VNet integration, you should deploy AKS into the same VNet or a peered VNet. AKS by default deploys agent nodes into a subnet of an Azure VNet. If MySQL is in that VNet (or peered), then the pods can resolve the MySQL private DNS and connect internally. You might need to configure the AKS DNS to use Azure’s DNS (which is default for AKS) so that the privatelink DNS zone is resolvable. Typically, you create AKS in the same VNet or peer the AKS VNet with the MySQL’s VNet and link the Private DNS zone to the AKS VNet as well.

- **Kubernetes Secrets for Credentials:** Store the MySQL connection string or credentials in a Kubernetes Secret object. Do not put them in ConfigMap in plain text. You can then mount these secrets as env vars in your pods. For example:

  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: db-credentials
  type: Opaque
  data:
    DB_USER: <base64-encoded-user>
    DB_PASS: <base64-encoded-password>
  ```

  And in Deployment:

  ```yaml
  env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: DB_USER
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: DB_PASS
  ```

  This way, your application in AKS gets the login info securely.

- **Scaling and Connection Pooling:** In Kubernetes, your app might scale horizontally (more pods). Just like App Service, each pod will have its DB connections, so ensure pooling and monitor connection counts. Use readiness/liveness probes wisely – if the probe executes a DB query, ensure that doesn’t overload the DB when many pods start at once (maybe have a lightweight check or use an HTTP app-level check that doesn't always hit the DB).

- **Running MySQL on AKS (alternative):** Some advanced users consider running MySQL cluster on AKS (using Helm charts like Bitnami’s MySQL or even managing a Galera cluster). While possible, this is a self-managed approach – you’d have to handle persistent storage via Azure Disks, ensure high availability, backups etc., within Kubernetes. This might be done for specific needs (like using MySQL with custom plugins, or want a single deployment managed along with app in the same cluster). But Azure Database for MySQL PaaS is generally easier for production due to built-in HA/backup. If you do run MySQL in AKS, consider using a StatefulSet with multiple replicas and some PV provisioning. Also be aware of performance – a PV (disk) attached to AKS may not match the IOPS throughput of Azure’s managed service which benefits from years of optimization.

- **Service Mesh or Proxy Integration:** In more complex AKS setups, you might run a sidecar like a ProxySQL or use a service mesh. For example, using ProxySQL as a DaemonSet on each node to funnel MySQL traffic can provide query caching or failover logic (if you have multiple MySQL replicas). This is quite advanced and specific. Alternatively, if using Istio or other mesh, you can configure mTLS for egress to MySQL – but since MySQL uses its own SSL, usually that’s enough.

- **Backup Strategy with AKS:** If using Azure MySQL, rely on its backups. If running MySQL in AKS, you need backup jobs (maybe a cronjob pod that runs mysqldump to a storage).

In essence, from an AKS perspective, using Azure’s managed MySQL is just using an external database. The main tasks are ensuring network connectivity (which is solved by Azure’s VNet integration and correct DNS) and managing secrets for creds.

## Hybrid Cloud Deployment Strategies

Hybrid cloud implies part of your infrastructure is on-premises or in another cloud, and part is in Azure. You might have an on-prem MySQL that needs to sync with Azure, or an application on-prem that wants to use Azure MySQL as a cloud backup or extension. Strategies include:

- **Data Migration to Cloud:** Often hybrid is a transitional phase when migrating a database to Azure. Use Azure Database Migration Service (DMS) for a live migration with minimal downtime – DMS can do continuous data replication from on-prem MySQL to Azure MySQL until cutover. Alternatively, use the **Data-in Replication** feature of Azure MySQL Flexible Server ([Azure Database for MySQL - Flexible Server Overview](https://docs.azure.cn/en-us/mysql/flexible-server/overview#:~:text=Azure%20Database%20for%20MySQL%20,Flexible%20Server)). Data-in replication allows an Azure MySQL to act as a replica of an external MySQL (on-prem or in another cloud). You’d configure binlog replication from the external source to the Azure target. This can be used to migrate with minimal downtime: set up replication, wait for sync, then cut over by pointing apps to Azure and stop external writes.

- **Burst to Cloud / Multi-write Scenarios:** Maybe you have on-prem database but you want to handle bursts or new workloads in Azure. True multi-master across on-prem and Azure is not trivial. One approach: designate one as read-only replica of the other. For example, on-prem is primary and Azure is a read replica (via Data-in replication). Cloud workloads that are read-heavy can use the replica. Or vice versa, if you have an IoT or web app in Azure writing to MySQL, and you want on-prem copy for compliance, you could replicate out from Azure to on-prem (Data-out replication ([Configure Data-Out Replication - Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-data-out-replication#:~:text=Configure%20Data,the%20source%20and%20replica%20servers))). Data-out replication allows the Azure server to be source and your on-prem MySQL as replica, using MySQL’s binlog mechanism. This way on-prem gets a near-real-time copy of data.

- **Latency Considerations:** If your app is hybrid (some parts on-prem connecting to Azure MySQL), ensure the network is low-latency (ExpressRoute or VPN). If latency is high (say >50ms), it might impact DB operations significantly. In such cases, having a local on-prem cache or partial dataset might be necessary. Or use replication such that on-prem reads local DB, writes go to Azure and then replicate back.

- **Azure Arc for Data Services:** Azure Arc is a service to manage databases across on-prem and cloud. Azure Arc for Data Services can run managed MySQL on your own infrastructure with Azure-like management. It's an emerging tech (Arc enabled MySQL was mentioned as a future service ([Azure Arc enabled data services - HPE Community](https://community.hpe.com/t5/alliances/azure-arc-enabled-data-services/ba-p/7168495#:~:text=Azure%20Arc%20enabled%20data%20services,CosmosDB%2C%20MySQL%2C%20and%20Synapse))). The idea is you could run a managed MySQL in your datacenter with containerization and Azure would manage it similarly to its cloud service. This is for truly hybrid setups requiring uniform management.

- **Consistent Tooling:** In hybrid, use the same IaC and automation where possible. For instance, manage on-prem pieces with Terraform as well (maybe using local-exec or other providers). Use Azure Pipelines or GitHub Actions to deploy both on-prem and Azure changes. And monitor both sides – you might use Azure Monitor’s extension to on-prem (via Arc or other means) to have single-pane monitoring.

- **Backup and DR between On-Prem and Azure:** Perhaps your DR strategy is to use Azure as a backup for on-prem DB. You can schedule nightly dumps from on-prem and upload to Azure Blob, or even restore them into an Azure MySQL (keeping it in sync via daily refresh). Or use replication as discussed for near real-time DR. Document the failover procedure: e.g., if on-prem fails, how quickly can Azure instance take over? If Azure is primary and on-prem is DR, how to failover if Azure goes down (similar concept, promote the on-prem replica). This duality can be complex, so often one environment is primary and the other is strictly for DR or read-only, to avoid conflict.

- **Application Layer:** Ensure your application can switch between on-prem and Azure DB if needed. This might mean abstracting the DB connection string in a config that can be toggled to point to DR. In a hybrid active-active scenario (rare for relational DBs due to consistency), you'd have to implement conflict resolution, which is beyond the scope here (usually avoid multi-master writes across on-prem/cloud due to complexity).

Hybrid strategies will be very specific to business needs, but Azure provides the tools like Data-in/out replication and Arc to support various configurations. The key is to plan the network and replication topology carefully and test the failover or migration steps.

---

# Troubleshooting and Common Issues

Even with the best planning, you may encounter issues when deploying or managing MySQL on Azure. This section covers common problems and their solutions, from connectivity troubles to performance bottlenecks, and errors encountered in CLI or Terraform.

## Debugging Connectivity Problems

Connection issues are among the first problems users might face. Here’s how to troubleshoot:

- **Cannot Connect to MySQL Server:**

  - _Error: Client denied by server_ – This usually points to firewall or network issues. If the error is like "Your connection is not authorized to this MySQL server," check that your client’s IP is allowed (if using public access) or that you are connecting from within the VNet (if private). For public servers, one quick test: try connecting from Azure Cloud Shell or an Azure VM in same region using the admin credentials (since Cloud Shell originates from an Azure datacenter, if you have "Allow Azure services" enabled or a broad rule, it might work). If it works from within Azure but not from your machine, likely firewall rules need adjusting.
  - _Error: Could not resolve hostname_ – If using private access, this could mean a DNS issue. Ensure your VM or environment is using the Azure-provided DNS or the private DNS zone is linked. A quick fix is to try connecting via the private IP of the server (you can find it in the portal under "Connection Strings" or via `az mysql flexible-server show` which might list private endpoint IP). If IP works but DNS doesn't, then it’s definitely a DNS config issue. Add an entry in your hosts file for testing or fix your DNS resolution.
  - _Timeouts_ – Could indicate the server is unreachable entirely. Check if the server is up (e.g., `az mysql flexible-server list` and see state, or portal to see if “Server is down for maintenance” or stopped). If the server was stopped (maybe manually to save cost), start it. If it's running, maybe NSG or firewall in between? For instance, if connecting from on-prem via VPN, ensure your network allows traffic on 3306. Azure MySQL doesn’t use custom ports by default, so 3306 is the port.

- **SSL Issues:**

  - If you get SSL errors like "SSL connection error" or certificate trust issues, ensure you have the correct SSL CA cert and your client is configured for SSL. Azure’s certificate might not be in your OS trust store (especially if using the DigiCert Global). Download the CA cert from Azure docs ([CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet - Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/scripts/sample-cli-create-connect-private-access#:~:text=wget%20)) and use `--ssl-ca` (for mysql client) or configure your driver to trust that CA. Alternatively, you can disable SSL certificate verification (ssl-mode=REQUIRED but not VERIFY_IDENTITY) but that’s not recommended for production.
  - If your application is not configured for SSL and Azure requires it, either configure SSL or temporarily disable the require_secure_transport (not recommended). Better to fix the app.

- **Authentication Failures:**

  - "Access denied for user ... (using password: YES/NO)": Double-check username (remember Azure admin user often needs "@servername" as part of user in some clients). Ensure the password is correct. Passwords set via CLI sometimes have special chars that need quoting in connection strings. If admin credentials lost, reset via `az mysql flexible-server update -p`.
  - If using Azure AD auth: ensure the user exists in Azure AD and they are properly added as MySQL user. AD auth errors can be tricky – you need to ensure the token you get has the right audience (the Azure MySQL). If connections using AD fail, test with a known SQL login to narrow down if it’s an AD config issue.

- **Private Endpoint DNS conflicts:** Sometimes after creating a private endpoint (or using private access), developers find that the public DNS for `mysql.database.azure.com` still resolves on their machine, causing confusion. If your machine is simultaneously connected to corp network and internet, DNS might resolve to public IP which won’t work. Solution: use your internal DNS that knows the private zone, or override the host resolution (e.g., in a jumpbox VM that is in the VNet).

- **Connectivity Drops Intermittently:**

  - Check if there are any maintenance operations or failovers happening. If you enabled HA, Azure might have done a planned failover during patching (if you see in metrics a dip or an event in Azure MySQL “Server was rebooted” around that time).
  - Long running connections might be closed by MySQL wait_timeout or Azure’s network if idle. Ensure your app is retrying or using a connection pool that tests connections. You can increase `wait_timeout` parameter if needed (default might be 600 seconds).
  - If using Azure Proxy (Single Server used a gateway proxy which sometimes had connectivity issues, but Flexible has mostly direct connections except in public with proxy for SSL termination). For Single Server, sometimes enabling "Redirect" connection policy improved latency/consistency (not applicable to Flexible as it’s by default direct in private).

- **Debugging Tools:** Use `telnet <host> 3306` or `nc` from the client to see if the port is open. Use `mysql -h ... -u ... -p` with `--ssl-mode=DISABLED` vs `REQUIRED` to isolate SSL issues. Check Azure MySQL server metrics "Connections Failed" for clues (if that metric rises when you attempt, likely firewall or auth issue). Also, Azure MySQL logs (Connection Logs if enabled) can show why connections were refused (e.g., ip not allowed or user authentication failed).

## Resolving Performance Bottlenecks

Performance issues might manifest as slow queries, high latency, or resource exhaustion. Here’s a troubleshooting approach:

- **Identify the Bottleneck Resource:** Use Azure Monitor metrics to see what’s maxed out when performance dips.
  - High CPU? Then likely query optimization or scaling up CPU is needed.
  - High Memory usage and perhaps increased IO? Could be the working set doesn’t fit in memory, causing swapping or buffer churn. Maybe scale memory or tune queries to be less memory-intensive (like avoid huge in-memory sorts).
  - High IO (IOPS near limit or disk queue increasing)? This could be heavy read or write load that saturates storage throughput. Check for queries doing table scans or large writes (bulk imports?). Mitigate by adding indexes or splitting workload, or increase provisioned storage or switch to a higher tier with more IOPS.
  - Many active connections? Perhaps connection pool is misconfigured, causing contention or context switching overhead. Or app is not releasing connections properly (leaks).
- **Slow Query Analysis:** Enable the slow query log (if not already). Review queries taking the longest. Focus on those with highest frequency _and_ high latency. Tools like pt-query-digest (Percona Toolkit) can summarize slow log results. Based on that:
  - Add missing indexes for slow queries.
  - Refactor queries (maybe break a complex join into simpler parts or introduce caching for results).
  - Consider MySQL configuration tweaks: e.g., if temp table usage is high (check status variables), you might increase `tmp_table_size` / `max_heap_table_size` to avoid disk temp tables for large operations. Azure might allow those changes.
- **Locking and Concurrency Issues:** Sometimes slowness is due to locks (one query waiting on another). Check if MySQL has any metadata locking issues: e.g., long-running transaction preventing others from completing. The `INFORMATION_SCHEMA.INNODB_LOCKS` or `SHOW PROCESSLIST` can reveal if threads are stuck waiting on locks. If so, find the blocking transaction and why. This could be due to missing index causing a query to lock more rows than needed or due to a bug in app not committing promptly. Killing the offending query is a short-term fix; long-term fix the root cause.

- **Out of Memory / Crashes:** If the MySQL server is restarting (check if uptime resets), maybe it ran OOM. Azure support can help if that happens frequently (they might see OOM killer logs). If so, either the instance is under-provisioned for the workload (scale up to more memory) or some query is using too much memory (like a huge sort or blob operation). Identify if specific operations trigger it, and optimize those.

- **Client-Side Bottlenecks:** Sometimes it's not the DB but the client. If one thread is doing too much sequentially, the app might appear slow even if DB is fine. Use App Insights or profiling at application side to ensure the bottleneck is indeed the DB.

- **Use Performance Schema or sys schema:** Azure MySQL likely has performance_schema enabled. You can query things like `sys.schema_table_statistics` to see which tables have most scans or `sys.user_summary_by_stages` for breakdown of where time is spent. This is advanced MySQL tuning but can provide insights beyond basic slow log.

- **Scaling Out or Up:** If after optimization you still hit limits, consider scaling up the server (more vCores or move to Memory Optimized if buffer pool is the issue). Or offload some workload to a replica (e.g., reporting queries to a replica). If writes are the bottleneck (and can’t scale a single instance further), one might consider sharding the database across multiple servers, but that adds complexity (managed sharding isn’t available in Azure MySQL, you’d handle it at app level or use something like MySQL Fabric or custom logic).

- **Engage Azure Support**: If there’s an underlying platform issue (for example, if you suspect the problem is on Azure’s side – say IOPS not reaching expected levels, or unpredictable pauses), raise a support ticket. There have been cases historically where underlying storage or networking issues affected DB performance. Azure can check backend logs for any anomalies (like patching events, hardware issues on the node hosting your instance, etc.).

## Handling Terraform and CLI Errors

While provisioning or managing via CLI and Terraform, you may run into errors. Here are common ones and resolutions:

- **Azure CLI Errors:**

  - _Invalid syntax or unrecognized arguments:_ Ensure your CLI is updated to the latest version if a command isn't recognized. For example, older CLI might not support `az mysql flexible-server` (which replaced `az mysql server` for flexible).
  - _“(AuthorizationFailed) The client 'XYZ' with object id '...' does not have authorization to perform action ...”_ – This means your Azure login doesn't have permission (perhaps trying to create resource in a subscription or resource group where you aren’t Contributor). Use `az login` with correct account or have an admin assign proper RBAC role.
  - _Quota Exceeded:_ If you try to create too many vCores or servers in a region, you might hit subscription quotas. For MySQL flexible server, Azure has quotas (e.g., max 10 servers per subscription in trial, or vCore quotas). Check quotas in Azure Portal and request increase if needed.
  - _Name already exists:_ MySQL server names must be globally unique (DNS name). If CLI says name taken, choose another (maybe incorporate random or your company prefix).
  - _Private DNS / VNet not found:_ If you specify `--private-dns-zone` or `--vnet` names, CLI might error if it can't find them. Make sure resource group context is correct for those resources or provide full resource IDs.
  - _Extension Errors:_ Azure CLI may prompt to install an extension for 'mysql' the first time. If it fails, try `az extension add -n db-up` or `az extension add -n mysql`. Ensure you have internet to fetch extension.

- **Terraform Errors:**

  - _Provider authentication errors:_ e.g., "Azure CLI Authorization not configured" or similar – meaning Terraform couldn’t get credentials. Ensure `az login` is done or environment variables for service principal are set (ARM_CLIENT_ID, etc.). If running in CI, double-check the service principal has appropriate rights.
  - _Resource conflict:_ If Terraform tries to create something that exists (maybe created manually outside Terraform), you might see an error like "Name already in use" or so. In that case, import the resource into Terraform state with `terraform import`, or remove the manual resource first.
  - _Dependent resource deletion:_ If you do `terraform destroy` and it fails on deleting a subnet because the MySQL server is still using it, that’s an ordering issue. Usually Terraform handles dependencies, but if something gets stuck (like if deletion of the server failed but Terraform moved on), you may need to manually clean up. Always destroy in reverse order: DB, then subnet, then VNet, etc., or let Terraform do it with proper depends_on.
  - _Timing issues:_ Azure might take time to finalize certain operations. Sometimes Terraform may try to create a DNS link before the DNS zone exists (though our config accounts for that). Use depends_on or add a small `time_sleep` if needed to serialize. These are rare if config is correct, but e.g., enabling geo-redundant backup requires the server to be created first sometimes. If you hit an error, you might split into two apply steps (first create server without some setting, then update).
  - _Terraform plan wants to change unrelated things:_ Sometimes after a manual change in Azure, Terraform shows changes. For instance, if someone changed a parameter in the portal, the next plan will show a diff. To resolve, either accept the change (let Terraform apply it back to desired state) or update your Terraform code to match the actual state if the manual change is intended to persist.
  - _Bugs:_ Terraform AzureRM provider occasionally has bugs. Check GitHub issues if something puzzling arises (like a property that won’t apply). Upgrading the provider might help if a bug was fixed. For example, earlier versions had issues with certain MySQL configurations. Always pin provider versions and test.

- **Common Mistakes:**
  - Forgetting that after Terraform deploys the MySQL, you still need to run `terraform output` to get the password if you didn’t supply one (if you used random_password resource). Otherwise you can’t connect.
  - Not saving the state file or losing it – then Terraform can’t track resources and a new `apply` might try to recreate things. Always back up the state or use remote state.

In any case, approach errors methodically: read the error message carefully (Terraform ones can be verbose). They often indicate which resource failed and why. If needed, use Azure CLI or Portal to verify the state of resources when troubleshooting Terraform issues (maybe the resource actually got created even if Terraform thought it failed).

---

Having covered planning, setup, security, performance, integration, and troubleshooting, you now have a comprehensive understanding of managing MySQL in Azure using CLI and Terraform. By following this guide, experienced cloud engineers and DevOps professionals should be able to confidently deploy scalable, secure, and high-performing MySQL databases on Azure, while using infrastructure-as-code practices to automate and maintain consistency across environments. Keep this guide as a reference as you implement your MySQL solutions on Azure, and combine it with Azure’s documentation and your own testing to achieve the best results for your specific use case.
