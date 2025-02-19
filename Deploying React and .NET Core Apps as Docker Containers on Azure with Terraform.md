# Deploying React and .NET Core Apps as Docker Containers on Azure with Terraform

**Introduction:**  
This comprehensive guide walks through deploying a full-stack application – a React front-end and a .NET Core back-end – as Docker containers on Azure App Service using Terraform. Aimed at advanced developers, it covers the entire lifecycle: from setting up your environment and containerizing applications, to provisioning Azure infrastructure as code, implementing CI/CD pipelines, and applying security, performance, and monitoring best practices. The guide is organized into clear sections with step-by-step instructions, code examples, and references to official documentation for further detail. By the end, you will have a robust, scalable, and secure workflow for shipping containerized applications to Azure.

**Guide Scope & Sections:**

1. Setting Up the Environment – Installing Docker, Terraform, Azure CLI, and SDKs
2. Application Dockerization – Writing Dockerfiles for React and .NET Core (production-optimized)
3. Azure Web App Configuration – Creating container-based Web Apps, networking, env variables, scaling
4. Terraform Infrastructure as Code – Automating Azure resource provisioning (App Service, ACR, etc.)
5. CI/CD Automation – Using GitHub Actions or Azure DevOps to build, push, and deploy containers
6. Security and Performance Best Practices – Hardening the deployment and optimizing performance
7. Monitoring and Logging – Using Azure Monitor, Application Insights, and Log Analytics for observability

Each section provides a step-by-step walkthrough with practical examples and tips from real-world scenarios. Let’s dive in.

## 1. Setting Up the Environment

Before writing code or configuration, ensure your development environment is prepared with all necessary tools. This section covers installing and configuring Docker, Node.js/.NET SDKs, Terraform, Azure CLI, and verifying access to an Azure subscription.

### 1.1 Install Prerequisite Tools

**Docker:** Install Docker Desktop (on Windows/macOS) or Docker Engine (on Linux) to build and run containers. Docker provides installation packages for all platforms on its official site ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Build%20Stage%20FROM%20node%3A18,RUN%20npm%20run%20build)). After installation, verify it works by running a test container:

```bash
docker run hello-world
```

This should download a sample image and run it, printing a "Hello from Docker" message. If you see the message, Docker is up and running.

**Node.js and .NET SDKs:**

- **Node.js:** Required to build the React application. Install Node.js (prefer LTS version, e.g., Node 16 or 18) from the official website or via a package manager. Verify with `node -v` and `npm -v`.
- **.NET SDK:** Required to build and publish the .NET Core application. Install the .NET 6.0 or 7.0 SDK (matching your project’s target) from Microsoft’s website or via package manager. Verify with `dotnet --version`. This also includes the .NET CLI for building the project.

**Azure CLI:** The Azure Command-Line Interface allows you to interact with Azure from your terminal. Install Azure CLI from Microsoft’s docs (they provide installers for Windows, macOS, and instructions for Linux apt/yum) ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=Azure%20subscription%3A%20If%20you%20don%27t,free%20account%20before%20you%20begin)). After installation, run `az login` to authenticate. This will open a browser for you to log into your Azure account. Ensure you have access to an Azure subscription (run `az account show` to confirm).

**Terraform:** Terraform will be used to provision Azure infrastructure as code. Download Terraform from HashiCorp’s website (a single binary). On Windows, add the folder to your PATH; on macOS/Linux, you can use a package manager (Homebrew: `brew tap hashicorp/tap && brew install hashicorp/tap/terraform`). Verify with `terraform version`. We will be using the Azure provider (azurerm) in our configurations ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=,random_integer.ri.result%7D%22%20location%20%3D%20%22eastus%22)) ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=,1.2)).

**IDE/Code Editor:** While optional, using an IDE like Visual Studio Code with extensions for Docker, Azure, and Terraform can greatly enhance productivity. The Terraform VS Code extension, for example, offers syntax highlighting, autocompletion, and visualization of resource graphs ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=,with%20PowerShell)).

### 1.2 Configure Azure Environment and Credentials

After tools are installed, ensure Azure CLI is logged in (`az login`) and set the target subscription (`az account set -s <YourSubscriptionID>`). If using a Service Principal for automation, log in via `az login --service-principal` with appropriate credentials or configure environment variables for Terraform’s Azure provider (e.g., `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, etc., if not using Azure CLI authentication).

Optionally, create an Azure resource group to contain all resources for this guide (or Terraform can create it). For example, using Azure CLI:

```bash
az group create -n my-azure-container-rg -l eastus
```

This creates a resource group in East US region (adjust the name and region as needed). Terraform configurations will reference this resource group.

With the environment ready, we can proceed to containerize the applications.

## 2. Application Dockerization

Containerizing the applications involves writing Dockerfiles for both the React front-end and the .NET Core back-end. We will create production-ready Docker images using multi-stage builds to optimize size and performance. This section provides Dockerfile examples and explanations, as well as tips for building efficient images.

### 2.1 Dockerizing the React Application

A React app is typically a single-page application compiled into static files (HTML, JS, CSS). For production, we want to serve these static files efficiently via a web server (like **Nginx**) inside a container. We’ll use a multi-stage Docker build: first stage to compile the React app (using Node.js), second stage to serve it via Nginx.

**Dockerfile (React app):**

Create a file named `Dockerfile` in the React project root with the following content:

```Dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app

# Install dependencies and build
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
# Copy a default nginx configuration (optional, if custom config is needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Explanation:** We use the official Node 18 Alpine image for the build stage. The lightweight Alpine variant keeps the image small. We copy `package.json` and `package-lock.json` first, run `npm install` (Docker will cache this layer if dependencies don’t change), then copy the rest of the source and run `npm run build` to produce an optimized production build of the React app. In the second stage, we start from an official Nginx Alpine image and copy the build artifacts from the first stage into Nginx’s web root (`/usr/share/nginx/html`). We expose port 80 and use the default Nginx command to serve indefinitely. Multi-stage builds ensure the final image contains _only_ the static files and Nginx, not the Node build environment, yielding a smaller and more secure image ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)).

**Optimizations:**

- The multi-stage approach keeps the final image small (only Nginx + static files) and removes Node.js runtime and dev dependencies, which enhances security ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Nginx%20efficiently%20serves%20static%20files)).
- Use a **.dockerignore** file to exclude files not needed in the image (e.g., local config, node_modules from host, tests). For example, create a `.dockerignore` with entries like `node_modules`, `Dockerfile`, `.git`, etc. This prevents copying large or sensitive files into the build context, improving build speed ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=Step%203%3A%20Create%20a%20,file)).
- If environment-specific config is needed (e.g., API base URL), consider injecting those via environment variables at runtime or using a build-time config file.

**Building and Testing the React Image:**  
From the React project directory (with the Dockerfile), run:

```bash
docker build -t myreactapp:latest .
```

This builds the image with tag `myreactapp:latest`. Once built, test it locally:

```bash
docker run -d -p 3000:80 myreactapp:latest
```

This runs the container detached and maps port 80 in the container to port 3000 on your machine, so you can access the app at http://localhost:3000. Verify the React app loads correctly. (Why 3000? It’s arbitrary here to avoid requiring root privileges for port 80 on localhost, and assume port 3000 is free. In Azure, we’ll use port 80 as the container’s port.)

### 2.2 Dockerizing the .NET Core Application

For the .NET Core back-end (for example, an ASP.NET Core Web API), we’ll also use a multi-stage Dockerfile. The first stage will build and publish the .NET app, and the second stage will run it on the ASP.NET Core runtime image. This approach keeps the final image lean (excluding SDK and build tools) ([9 Tips for Containerizing Your .NET Application | Docker](https://www.docker.com/blog/9-tips-for-containerizing-your-net-application/#:~:text=With%20multi,then%20holds%20the%20application%20runtime)).

**Dockerfile (.NET Core app):**

In the .NET project folder (where the `.csproj` is), create a `Dockerfile`:

```Dockerfile
# Stage 1: Build and publish the .NET application
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything and build (publish) the release
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish ./
# (Optional) If using appsettings.Production.json or other config, copy if needed.
EXPOSE 80
ENV ASPNETCORE_URLS=http://+:80   # Listen on port 80 in container
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

**Explanation:**

- We use Microsoft’s official .NET SDK 6.0 image for the build stage. The SDK image includes compilers and build tools. We set a working directory and copy the project file(s) first, then run `dotnet restore` to fetch dependencies. Copying the csproj separately and restoring allows Docker to cache the restore layer – if your dependencies haven’t changed, subsequent builds skip re-downloading packages ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,output%20from%20the%20previous%20stage)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Nginx%20efficiently%20serves%20static%20files)).
- Next, we copy the rest of the source and run `dotnet publish` in Release configuration, outputting to `/app/publish`. This produces a self-contained set of DLLs and assets for the app.
- In the second stage, we use the lighter **ASP.NET Core Runtime** image (which only has .NET runtime, no build tools). We copy the published output from the build stage into this runtime image. We expose port 80 and set the `ASPNETCORE_URLS` environment variable so the app will bind to port 80 (App Service will route HTTP traffic to this port by default). Finally, the entrypoint runs the .NET application (replace "MyApp.dll" with the actual DLL name of your app, typically your project name).

This multi-stage build ensures the final container only has the necessary runtime binaries and your application, not the SDK or source code, reducing image size significantly ([Containerize A .NET 6 App With Docker](https://www.csharp.com/article/containerize-a-net-6-app-with-docker/#:~:text=FROM%20mcr.microsoft.com%2Fdotnet%2Fsdk%3A6.0%20AS%20build,App)) ([Containerize A .NET 6 App With Docker](https://www.csharp.com/article/containerize-a-net-6-app-with-docker/#:~:text=,DockerConsoleApp.dll)).

**.dockerignore for .NET:** Similar to the React app, create a `.dockerignore` in the .NET project to avoid copying unnecessary files. Common entries: `bin/`, `obj/` (build outputs that will be regenerated), `.git`, and any config files that shouldn’t go into the image (like `.vscode/` or secrets).

**Building and Testing the .NET Image:**  
Run a Docker build for the API:

```bash
docker build -t myapi:latest .
```

This builds the .NET API image. Test it locally (assuming your API, when run, listens on port 80 as set above):

```bash
docker run -d -p 5000:80 myapi:latest
```

This maps container port 80 to host port 5000 (so you can reach the API at http://localhost:5000). If the API has health endpoints or a swagger page, test those to ensure the containerized app works. You should see logs in the console (use `docker logs <container>` or run without `-d` to see output). If the app connects to external resources (like a database), you may need to configure connection strings via environment variables (we’ll handle such settings via Azure App Service configuration).

**Summary (Dockerization):** We now have two container images: one for the React app and one for the .NET API. Both are optimized for production:

- The React image uses Nginx to serve static files and is very lightweight.
- The .NET image contains only the compiled app and the ASP.NET runtime.

We tested both locally. In a real-world scenario, you might use a private container registry to store these images – in our case, Azure Container Registry (ACR) will serve that purpose. Next, we’ll configure Azure App Service to host these containers.

## 3. Azure Web App Configuration

Azure App Service is a PaaS offering that can run web apps or APIs on a fully managed platform. It also supports deploying _custom Docker containers_ (Linux or Windows) in Web Apps. We will use **Azure Web App for Containers** to deploy our React and .NET containers. In this section, we configure the necessary Azure resources (App Service plans and Web Apps), consider networking and environment settings, and plan for scaling.

### 3.1 Creating Azure App Service for Containers

**Resource Group:** Decide on a resource group (if you created one earlier, we'll reuse it). All resources (App Service, ACR, etc.) will live here for organization.

**App Service Plan:** This is the underlying VM pool that will host the Web App. Since we are using Linux containers, create a Linux App Service Plan. You can create it via Azure CLI for a quick start (Terraform will also create it later, but it's useful to know):

```bash
az appservice plan create --name myAppServicePlan --resource-group my-azure-container-rg \
  --is-linux --sku B1
```

This creates a Basic (B1) plan on Linux. For production, you might choose Standard or Premium SKU for better scaling options. The plan determines cost and available features (e.g., custom domains, TLS, scaling instances, etc.).

**Web Apps (for containers):** We will create two Web Apps – one for the front-end and one for the API – each bound to our container images. For now, conceptualize them: e.g., `my-react-app` and `my-dotnet-api`. In Azure CLI, you could do:

```bash
az webapp create --resource-group my-azure-container-rg --plan myAppServicePlan \
  --name my-react-app --deployment-container-image-name myregistry.azurecr.io/myreactapp:latest
```

The above would create a Web App and set it to use a container image from ACR (`myregistry.azurecr.io`). In practice, you need the Azure Container Registry and the image to exist (and the Web App to have permissions to pull it). We’ll handle those details with Terraform, but it's important to note the settings. If using Azure Portal, you’d specify that this Web App is a Docker container and provide the image name (and registry credentials if needed).

**Configuration for container images:** In App Service for Linux, the configuration of which container to run is typically done via settings like `LINUX_FX_VERSION` or the newer _Application Stack_ settings. For example, Terraform uses `site_config > application_stack` to specify `docker_image` and `docker_image_tag` ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=site_config%20,%7D)). Under the hood, App Service will pull the image from the registry. If the registry is private (like ACR), you need to provide credentials or use integrated authentication (managed identity). Azure App Service can use managed identity to access ACR without storing credentials, which is a best practice (so you don’t keep registry creds in app settings) ([Configure a custom container - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container#:~:text=Note)) ([Configure a custom container - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container#:~:text=Service%20Principal%20is%20no%20longer,both%20Windows%20and%20Linux%20containers)).

We will set up Azure Container Registry (ACR) to store our images and link it with the Web Apps. For now, keep in mind:

- **Image naming:** We might tag images with version numbers or “latest” for simplicity. In production, version tags (or using CI-generated tags like Git commit SHA) is better for traceability.
- **Continuous deployment:** If you want the Web App to automatically update when a new image is pushed, Azure provides a _webhook_ mechanism from ACR to App Service. Alternatively, our CI/CD pipeline can handle the deployment trigger.

### 3.2 Networking Considerations

By default, Web Apps are publicly accessible over the internet on `<appname>.azurewebsites.net`. Azure handles the networking, load balancing, and TLS termination (we can enforce HTTPS easily). However, in advanced scenarios you may need additional network configuration:

- **VNet Integration:** If the .NET API needs to access resources in an Azure Virtual Network (e.g., a database in a private subnet, or a Redis cache), you can use VNet integration. This feature (for Linux App Service, the regional VNet integration) allows the app to make outbound calls into a VNet. It’s configured by linking the Web App to a subnet in a VNet. In Terraform, this can be done using `azurerm_app_service_virtual_network_swift_connection` or similar resources. Keep in mind VNet integration is only available on Standard and above SKUs, not Basic.
- **Private Endpoint:** For high security, one can assign a private endpoint to the Web App, removing public access. This is more complex and often not needed for public web apps, but for internal APIs it’s an option.
- **Access Restrictions:** Azure App Service allows you to define IP allow/deny lists. For instance, you could restrict the API to only accept traffic from the front-end or from certain IP ranges. This can be a simple security measure if appropriate.
- **Outbound Networking:** Apps might need to call external services (e.g., third-party APIs). By default, they can. If you need to control or log this, consider using service endpoints or firewall rules on those services. Also note, App Service has a fixed set of outbound IPs (listed in Azure Portal) which you might need to whitelist on external systems.

For our scenario, we’ll assume the React app is public (needs to be accessed by users) and the .NET API is also public (accessible to the React front-end and perhaps directly by clients). Securing the API would typically involve authentication (JWT tokens, etc.), which is outside the scope of this deployment guide. We will not integrate a VNet or private endpoint, keeping things simpler – but remember these options for real-world production setups that require them.

### 3.3 Setting Environment Variables & App Settings

Applications often require configuration via environment variables (e.g., database connection strings, API URLs, secrets). In Azure App Service, you configure these in **Application Settings**. Each setting becomes an environment variable in the container runtime.

To add or modify these:

- **Azure Portal:** Navigate to the Web App > Configuration > Application Settings. Here you can add entries (Name, Value). For example, set `ASPNETCORE_ENVIRONMENT = Production` for the .NET app, or `API_BASE_URL = https://my-dotnet-api.azurewebsites.net` in the React app (if needed by front-end to know API endpoint).
- **Azure CLI:** Use `az webapp config appsettings set --name <app> --resource-group <rg> --settings KEY=VALUE`.
- **Terraform:** Use the `app_settings` block in `azurerm_linux_web_app` resource to define key-value pairs.

**Sensitive settings:** Do not store secrets (like DB passwords) in plain text. Instead, consider **Azure Key Vault** integration. App Service can directly reference Key Vault secrets by adding an app setting like `MySecret = @Microsoft.KeyVault(SecretUri=https://<vault-name>.vault.azure.net/secrets/<secret-name>/<version>)`. The App Service’s managed identity must have access to the Key Vault secret. This way, the actual secret value is not stored in App Service, just a reference. Alternatively, use Azure DevOps or GitHub Actions to inject secrets at deployment time from a secure store.

**Docker-specific settings:** When using custom containers, Azure defines a few special settings:

- `DOCKER_REGISTRY_SERVER_URL`, `DOCKER_REGISTRY_SERVER_USERNAME`, `DOCKER_REGISTRY_SERVER_PASSWORD`: These hold the container registry credentials (if not using managed identity). In Terraform, one would normally set these as `app_settings`, but as of newer Azure provider versions, they should be placed in the `site_config > container_registry` or `application_stack` settings ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=app_settings%20%3D%20,registry.admin_password)). Azure will use them to pull the image, but importantly, these are not exposed to the running container for security ([Configure a custom container - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container#:~:text=match%20at%20L251%20for%20accessing,are%20exposed%20to%20the%20application)). So your application won’t see these values.
- If you use **Managed Identity** for the web app to access ACR, you avoid needing these settings. Instead, you’d assign the web app’s identity the role “AcrPull” on the ACR, and Azure takes care of auth.

**Verify environment variables:** Once deployed, you can verify what environment variables are available to your container by hitting the special endpoint: `https://<app-name>.scm.azurewebsites.net/Env` (requires authentication). This is part of the Kudu (deployment) site. It’s a useful trick to debug configuration issues.

Plan out what settings you need for your app. For example:

- For .NET API: Connection strings (which can be put in Azure’s Connection Strings section, or as app settings), `ASPNETCORE_ENVIRONMENT`, perhaps an Application Insights key.
- For React: Maybe API endpoint, or it might be baked at build time. (If the React app is purely static and uses relative paths to call the API in same domain, you might not need any. If different domain, consider CORS config on API and an env for the URL in React.)

We will incorporate these settings into Terraform code. Also, consider using **slot settings** if you use deployment slots (settings that stick to a slot and don’t swap). For advanced scenarios, deployment slots allow zero-downtime releases – you deploy to a staging slot then swap it with production. This is beyond our primary scope but worth mentioning as a best practice for production deployments.

### 3.4 Configuring Scaling and High Availability

One major advantage of cloud deployments is easy scaling. Azure App Service provides two primary ways to scale:

- **Scale Up (vertical scaling):** Increase the instance size or move to a higher tier (e.g., from 1 core to 2 cores, or from Basic to Standard). This is done by changing the App Service Plan SKU.
- **Scale Out (horizontal scaling):** Increase the number of instances (e.g., 2, 3, ... N instances of your app running behind a load balancer). This is available in Standard and higher tiers (Basic only supports scale up, not auto-scale).

For stateless apps (which our containerized web apps should be – they don’t rely on local session or file state), scaling out is typically more effective for handling increased load ([Best practices for Azure App Service - Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices#:~:text=Best%20practices%20for%20Azure%20App,you%20more%20flexibility%20and)). Azure App Service can auto-scale based on metrics:

- You can configure **Autoscale rules** via Azure Monitor. For example, a rule might say: if CPU usage > 70% for 5 minutes, add 1 instance (scale out), and if CPU < 30% for 10 minutes, remove 1 instance (scale in), maintaining between 2 and say 10 instances. Another common metric is memory usage or HTTP request count. This helps handle spikes in traffic automatically ([Best Practices for Autoscaling in Azure App Service - Apps4Rent.com](https://www.apps4rent.com/blog/autoscaling-in-azure-app-service/#:~:text=Best%20Practices%20for%20Autoscaling%20in,the%20minimum%20value%20or)).
- Alternatively, schedule-based scaling can be used (e.g., scale out during business hours, scale in at night).

If using Terraform, the resource **`azurerm_monitor_autoscale_setting`** can define these rules in code, attaching to the App Service Plan ([Azure App Service Plan Auto Scaling Rules via Terraform](https://stackoverflow.com/questions/79085622/azure-app-service-plan-auto-scaling-rules-via-terraform#:~:text=I%20have%20used%20the%20azurerm_monitor_autoscale_setting,the%20azure%20app%20service%20plan)). For example, you’d specify the target resource (the plan) and define profiles for scaling.

Even without autoscale, you can manually adjust instance count in Azure Portal or with CLI (`az webapp scale` for instance count on the plan). Ensure you always have at least 2 instances in production for high availability – this way if one VM is down or restarting, the other can serve traffic ([Best Practices for Azure App Services - Techrupt Digital](https://techrupt.io/post/best-practices-for-azure-app-services#:~:text=Best%20Practices%20for%20Azure%20App,adding%20more%20instances%20to)). Azure’s load balancer will distribute requests.

**Planning for scale:** Because we separated the front-end and API into different web apps, they can be scaled independently. For instance, if the API is more CPU-intensive, you might give it more instances or a higher tier than the static front-end. Conversely, a static site might handle many more requests with minimal CPU, so it could run on fewer resources.

**Session state and data:** If your .NET API uses in-memory session or cache, remember that scaling out means instances won’t share that memory. Use external stores (Azure Cache for Redis, databases) to store session or cache data so that all instances can access the same data. This ensures a stateless architecture ready for cloud scale.

**Always On:** In the App Service settings, enable **Always On** (especially for the .NET API) to prevent the app from idling. This keeps at least one instance active and keeps your container loaded for faster responses (this setting is automatically enabled on paid tiers by default for Linux).

At this point, we have designed how our Azure App Service environment will look: A container registry for images, a Linux app service plan, two web apps configured to use our custom images, with proper environment settings and the ability to scale. Now, we’ll implement this with Terraform to ensure it’s all codified and repeatable.

## 4. Terraform Infrastructure as Code

Using Terraform, we will describe and provision all required Azure resources: Resource group, Azure Container Registry, App Service plan, Web Apps, networking configurations, etc. Storing infrastructure as code allows versioning and automating environment setups (e.g., you can recreate the whole environment for staging or testing easily, or destroy and rebuild if needed).

### 4.1 Terraform Project Structure and Provider Configuration

Create a directory for your Terraform configuration (e.g., `infra/`). Inside, create a main Terraform file (e.g., `main.tf`). We will keep everything in one file for simplicity, but in larger projects you might split into multiple .tf files or modules (for example, separate files for network, app service, etc.). Make sure you have logged in via Azure CLI or set service principal credentials so Terraform can authenticate to Azure.

**Initialize Terraform Azure provider:** Add the required provider block and Terraform settings at the top of `main.tf`:

```hcl
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  # (Optional backend configuration can go here if using remote state)
}

provider "azurerm" {
  features {}  # enables the Azure RM provider
}
```

This specifies we’re using the AzureRM provider version 3.x. If you want to store Terraform state remotely (recommended for team scenarios), you can configure an Azure Storage backend in the `terraform {}` block. For brevity, we’ll assume local state or that you configured a backend separately.

**Variables and outputs:** You may define variables for things like resource names, locations, etc., either inline or in a separate `variables.tf`. For readability, we’ll use direct values in this guide, but feel free to parameterize (e.g., a variable for location = "eastus").

### 4.2 Writing Terraform Configuration for Azure Resources

Now, we define each resource. We will go step by step in the order they should be created (Terraform will handle dependencies, but it’s logical to create supporting resources first like the registry and plan, then the web apps).

**Resource Group:** If you haven’t created it manually:

```hcl
resource "azurerm_resource_group" "rg" {
  name     = "my-azure-container-rg"
  location = "eastus"
}
```

This creates the resource group in East US region ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=,random_integer.ri.result%7D%22%20location%20%3D%20%22eastus%22)). All other resources will reference this.

**Azure Container Registry (ACR):**

```hcl
resource "azurerm_container_registry" "acr" {
  name                     = "myContainerRegistry123"    # must be globally unique in Azure
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"
  admin_enabled            = false  # disable admin user for security
}
```

This creates a private Azure Container Registry with Basic SKU. We disable the admin user – instead, we will use Azure AD authentication (managed identity) for pulling images. The ACR name must be lowercase and unique. Azure will assign a login server name like `mycontainerregistry123.azurecr.io`.

**App Service Plan:**

```hcl
resource "azurerm_service_plan" "app_plan" {
  name                = "containerAppPlan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "P1v2"  # e.g., PremiumV2 small (good for production; use B1 for basic test)
}
```

We choose a PremiumV2 plan (P1v2) here as an example ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=kind%20%3D%20,)), which supports VNet integration and gives better performance. You could choose "B1" for Basic or "S1" for Standard in non-production. The key is `os_type = "Linux"` since we use Linux containers, and `reserved = true` is implied for Linux (older Terraform versions required `reserved = true` for Linux plans, but on new `azurerm_service_plan` it’s determined by SKU and os_type).

**Managed Identity (for Web Apps):** We want our Web Apps to have an identity to pull from ACR (and potentially for other resource access). We can enable a system-assigned managed identity on the web app resources. Additionally, we need to grant the ACR pull permissions. Terraform can do role assignments too. Let’s include:

```hcl
# Managed identity for pulling images
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.react_webapp.identity.principal_id
}
```

We will create the web app next, but note we reference its identity’s principal_id. We’ll do one for each web app (React and API). The role “AcrPull” allows pulling from the registry. This assumes system identity is enabled on the app (set in the resource).

**Web App (React front-end):**

```hcl
resource "azurerm_linux_web_app" "react_webapp" {
  name                = "my-react-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      docker_image     = "${azurerm_container_registry.acr.login_server}/myreactapp"
      docker_image_tag = "latest"
      docker_registry_url      = azurerm_container_registry.acr.login_server
      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }

  app_settings = {
    # App settings (env vars) can be added here
    "WEBSITE_PORT" = "80"  # for Azure to know which port your container listens on, if needed
    # ... (any React-specific settings if we had)
  }
}
```

Let’s break down a few important parts of this resource:

- We use the resource type `azurerm_linux_web_app` (the newer resource type for Linux Web Apps).
- We enable a system-assigned identity (`identity { type = "SystemAssigned" }`). Terraform will output the principal id which we used above for ACR role assignment. We’ll add a second `azurerm_role_assignment` for the API web app’s identity similarly.
- In `site_config.application_stack`, we specify the Docker image and tag ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=site_config%20,%7D)). We compose the image name from the ACR login server and image name. We set the tag "latest" here; in production, you might use version tags. Azure will pull `mycontainerregistry123.azurecr.io/myreactapp:latest`.
- We also supply the registry credentials. In this example, we’re using the admin username/password of ACR ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=app_settings%20%3D%20,registry.admin_password)). This is not ideal for production (we disabled admin actually). Instead, since we have a managed identity, we could omit these and rely on identity. As noted in the StackOverflow snippet, the new Terraform supports specifying `docker_registry_url/username/password` in the application_stack. We’ve done that above using admin creds for simplicity. A better approach is to remove those three lines and instead ensure the web app’s identity has AcrPull role – then Azure handles auth (in which case you only need to specify `docker_registry_url` and omit username/password entirely, as per provider docs).
- The `WEBSITE_PORT` setting is an App Service setting that tells Azure which port your container listens on. Often for single-container Linux apps, Azure can figure it out (it tries 80 by default). But it’s good practice to set it if your app listens on a different port. In our case, both containers listen on 80 internally, so it’s not strictly required.
- You could add other app settings here (for React, maybe none needed; if we had environment toggles, we would). The React app being static likely doesn’t need runtime env variables, except possibly to enable Application Insights JavaScript SDK (in which case you might pass an instrumentation key as a setting and have your HTML read from `window.__env` or so – but that’s application-specific).

**Web App (ASP.NET Core API):**

Similarly, define the .NET web app resource:

```hcl
resource "azurerm_linux_web_app" "api_webapp" {
  name                = "my-dotnet-api"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      docker_image     = "${azurerm_container_registry.acr.login_server}/myapi"
      docker_image_tag = "latest"
      docker_registry_url      = azurerm_container_registry.acr.login_server
      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }

  app_settings = {
    "ASPNETCORE_ENVIRONMENT" = "Production"
    "WEBSITE_PORT"           = "80"
    # If using App Insights, e.g.:
    # "APPLICATIONINSIGHTS_CONNECTION_STRING" = "<your App Insights connection string>"
    # If using Key Vault reference, e.g.:
    # "DB_CONNECTION" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault.secret.connection_string.id})"
  }
}
```

This is analogous to the React web app. We specify the container image for the API. We pass an app setting to ensure the .NET app runs in Production mode (so it’s optimized and doesn’t display developer error pages, etc.). If our .NET app needed a connection string or other secrets, we would include them as settings (perhaps referencing Key Vault as commented).

**Grant ACR pull to API identity:** As mentioned, include another role assignment for the API app:

```hcl
resource "azurerm_role_assignment" "acr_pull_api" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.api_webapp.identity.principal_id
}
```

Now both web apps can pull from ACR using their identities (once Terraform applies, if using admin creds in settings, Azure will use those; if not, it will use identity since we assigned AcrPull).

**Outputs (optional):** It can be helpful to output the URLs of the sites:

```hcl
output "react_url" {
  value = azurerm_linux_web_app.react_webapp.default_hostname
}
output "api_url" {
  value = azurerm_linux_web_app.api_webapp.default_hostname
}
```

These would output something like `my-react-app.azurewebsites.net`. You can use these to test or configure your front-end to call the API.

**(Optional) Azure Storage for logs or other needs:** The prompt mentioned storage, but our scenario didn’t explicitly need an Azure Storage account. You might want a storage account if:

- You plan to enable **Web Server Logging** to blob storage (App Service can send logs to a blob container).
- Your app needs to read/write files (could use Azure Blob or File storage).
- Terraform state storage (if you choose to store state in Azure, you’d create a storage account and container for it).

For completeness, an example storage account via Terraform:

```hcl
resource "azurerm_storage_account" "logs_sa" {
  name                     = "myapplogsstore"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Standard_LRS"
  kind                     = "StorageV2"
  allow_blob_public_access = false
}
```

And a container for logs:

```hcl
resource "azurerm_storage_container" "log_container" {
  name                  = "logs"
  storage_account_name  = azurerm_storage_account.logs_sa.name
  container_access_type = "private"
}
```

We won’t delve further into using it, but it could be used for app service diagnostic logs or other telemetry.

**Reviewing Dependencies:** Terraform will understand that the Web Apps depend on the App Service Plan and ACR (since we reference those). We explicitly set role assignments that depend on web app identities. To be safe, you might add `depends_on = [azurerm_linux_web_app.react_webapp]` in the role assignment resource to ensure Terraform creates the web app (and its identity) before the role assignment (though often it infers this via the principal_id reference). Keep this in mind if you run into ordering issues.

### 4.3 Deploying with Terraform

With the configuration in place, run the Terraform commands:

1. `terraform init` – downloads the Azure provider and sets up the backend (if configured) ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=3)).
2. `terraform plan` – shows the execution plan. Review that it will create the resources we outlined ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=terraform%20init)). Pay attention to any placeholders (like if we use `azurerm_container_registry.acr.admin_*`, ensure admin was enabled or else those might not exist; if using managed identity only, use data source or remove those). If using admin disabled and not providing creds, Terraform might not have username/password (since we set admin_enabled=false). In that case, adjust the webapp block to not expect them. The safer route: enable admin for initial setup to simplify, or use `data "azurerm_container_registry"` to fetch the admin creds if admin is true ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=app_settings%20%3D%20,registry.admin_password)), then turn off admin once managed identity is confirmed working.
3. `terraform apply` – apply the changes. This will provision ACR, Plan, Web Apps, etc. It will output the URLs if you set those outputs.

Terraform should report success. In the Azure portal, you can verify the resource group has the new resources. The Web Apps might not be running successfully yet if the container images aren’t in ACR. At this point, since we haven’t pushed images to ACR, the Web Apps will keep trying and failing to pull the image (you might see errors in the App Service’s “Container Settings” or in the log stream indicating it cannot find the image). That’s expected – we will push the images next in our CI/CD pipeline. Alternatively, you could have built and pushed the images first (chicken-and-egg). In practice, one would include the image push in the deployment workflow.

One approach is to tag images with a version and include that version in the Terraform apply (e.g., `docker_image_tag = "v1"`). Terraform can then update the Web App when a new version tag is provided. However, constantly running `terraform apply` for each release might not be ideal – many teams use a separate mechanism to update just the container (like Azure CLI command or continuous deployment as mentioned). We’ll discuss this in CI/CD.

For now, with infrastructure in place, ensure:

- ACR exists (you can run `az acr list -g my-azure-container-rg` or check portal).
- Web Apps exist. You can access their URLs; they might show a default Azure “error” page or “welcome” if no container yet, or a 503 if container is failing. That’s fine for now.

## 5. CI/CD Automation

Automation is key to a repeatable and reliable deployment process. In this section, we’ll set up a Continuous Integration/Continuous Deployment (CI/CD) pipeline to build our Docker images, push them to Azure Container Registry, and deploy them to the Azure Web Apps. We’ll focus on **GitHub Actions** for the pipeline, but you can achieve similar results with Azure DevOps, GitLab CI, or other tools. We will also highlight differences if using Azure DevOps.

### 5.1 CI/CD with GitHub Actions

Assume our code (React and .NET projects plus Terraform configs) is in a GitHub repository. We’ll create a workflow file (e.g., `.github/workflows/deploy.yaml`) to define the pipeline.

**Overview of the pipeline steps:**

1. **Trigger:** e.g., on push to main or on pull request to main for testing.
2. **Build stage:**
   - Check out code.
   - Set up language environment if needed (for running tests maybe).
   - Build the Docker images for both applications.
   - Tag the images appropriately.
3. **Push stage:**
   - Log in to Azure Container Registry.
   - Push the built images to ACR.
4. **Deploy stage:**
   - Deploy the new images to Azure. This could be done by:
     - Running Terraform apply with updated `docker_image_tag`, or
     - Using Azure CLI to update the Web App configuration to the new image tag, or
     - Relying on App Service continuous deployment (if configured).
   - Alternatively, use the Azure Webapps Deploy action to push the image (this requires a publish profile or credentials).

We have a Terraform-based infrastructure, so one strategy is: keep the infrastructure (RG, Plan, ACR, Webapp) stable, and just update the image tag for releases. We could incorporate Terraform into the pipeline, passing a variable for the new tag. However, running Terraform on every code push might be heavy (and could risk unintended infra changes if not careful). Another approach is to decouple image deployment from Terraform after initial setup. For example, you could configure the web app to always use the `:latest` tag and then the pipeline just pushes `:latest` – the app will auto-update. But relying on `latest` can be risky (hard to roll back).

A compromise: use image tags per build (like the Git commit SHA) and update the web app via CLI. The Azure CLI command to update a container image is:

```
az webapp config container set --name my-react-app --resource-group my-azure-container-rg \
   --docker-custom-image-name myregistry.azurecr.io/myreactapp:<tag> --docker-registry-server-url https://myregistry.azurecr.io
```

(This also needs credentials or identity set – since we already have identity setup, the web app should be able to pull if the image name changes as long as ACR is the same.)

For brevity, we’ll illustrate using GitHub Actions to build and push, then use the Azure Webapps Deploy action which can deploy images.

**Setting up credentials for GitHub Actions:**

- **Azure Credentials:** The recommended way is to create a Service Principal with appropriate rights (e.g., Contributor on the resource group, or specific rights to ACR and App Service). Then add its details (client id, tenant id, client secret) as GitHub secrets, or use OpenID Connect (OIDC) federation for passwordless auth ([Deploying Docker to Azure App Service - GitHub Docs](https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=If%20your%20GitHub%20Actions%20workflows,and%20%20178)). Simpler but slightly less secure: use the App Service **Publish Profile** for deployment. Azure Webapp Deploy action allows using a publish profile (which you can download from Azure portal for your web app) – store it as a secret in GitHub (e.g., AZURE_WEBAPP_PUBLISH_PROFILE). For ACR push, you can either use the SP creds or enable ACR admin and use those as secrets (as shown in Thomas Thornton’s blog) ([Build and push Docker Image to Azure Container Registry using GitHub Action - Thomas Thornton Azure Blog](https://thomasthornton.cloud/2022/12/14/build-and-push-docker-image-to-azure-container-registry-using-github-action/#:~:text=uses%3A%20azure%2Fdocker,secrets.REGISTRY_PASSWORD)) ([Build and push Docker Image to Azure Container Registry using GitHub Action - Thomas Thornton Azure Blog](https://thomasthornton.cloud/2022/12/14/build-and-push-docker-image-to-azure-container-registry-using-github-action/#:~:text=tags%3A%20%24,core%2FDockerfile)). We will lean on Azure’s publish profile for deploying to the web app, and use Azure CLI or SP for ACR.
- **ACR Credentials:** If not using the admin user, you can have the Service Principal assigned the AcrPush role. Then use `az login` in GitHub Action and `docker push` directly (Azure login action logs you into Azure but you still need to `docker login` to ACR – which can be done with `az acr login` or using the docker login action with credentials). For simplicity, one method: enable ACR admin, and add `ACR_USERNAME` and `ACR_PASSWORD` as secrets (retrieved from Azure Portal ACR > Access Keys) ([Build and push Docker Image to Azure Container Registry using GitHub Action - Thomas Thornton Azure Blog](https://thomasthornton.cloud/2022/12/14/build-and-push-docker-image-to-azure-container-registry-using-github-action/#:~:text=Add%203%20secrets%20as%20below,the%20access%20keys%20tab%20above)), along with `ACR_LOGIN_SERVER` (yourregistry.azurecr.io).

**Sample GitHub Actions Workflow (deploy.yaml):**

```yaml
name: Build and Deploy to Azure

on:
  push:
    branches: [main]

env:
  ACR_LOGIN_SERVER: mycontainerregistry123.azurecr.io
  IMAGE_NAME_FRONTEND: myreactapp
  IMAGE_NAME_API: myapi

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx (builder)
        uses: docker/setup-buildx-action@v2

      - name: Log in to Azure Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.ACR_LOGIN_SERVER }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build and push React front-end image
        uses: docker/build-push-action@v5
        with:
          context: ./path-to-react-app
          file: ./path-to-react-app/Dockerfile
          push: true
          tags: ${{ env.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }}

      - name: Build and push .NET API image
        uses: docker/build-push-action@v5
        with:
          context: ./path-to-dotnet-api
          file: ./path-to-dotnet-api/Dockerfile
          push: true
          tags: ${{ env.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME_API }}:${{ github.sha }}

  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    steps:
      - name: Azure WebApp Deploy (React)
        uses: azure/webapps-deploy@v2
        with:
          app-name: "my-react-app"
          slot-name: "production"
          images: "${{ env.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }}"
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_REACT }}

      - name: Azure WebApp Deploy (API)
        uses: azure/webapps-deploy@v2
        with:
          app-name: "my-dotnet-api"
          slot-name: "production"
          images: "${{ env.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME_API }}:${{ github.sha }}"
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_API }}
```

Let’s explain this workflow:

- It triggers on pushes to the main branch (you might also set up pull request workflows for testing, which build but not deploy).
- In the build-and-push job: we log in to ACR using the Docker login action with credentials stored in secrets (from ACR admin or SP). Then we use Docker build-push action to build each image and push it. We tag images with the Git commit SHA (a unique identifier for that version) ([Deploying Docker to Azure App Service - GitHub Docs](https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=,file%3A%20.%2FDockerfile)). Using commit SHA ensures every push is versioned; alternatively, you could use something like an incrementing build number or a semantic version tag.
- The `context` for React and .NET should point to the directories containing their Dockerfile. Make sure the paths are correct if your repo is structured with separate folders.
- We set `push: true` so that the image is pushed to ACR in one step after build.

- In the deploy job (which runs after build-and-push, thanks to `needs:`): we use Azure Webapps Deploy action. This action uses a publish profile to deploy a container by updating the Web App’s container settings. We pass the image name(s) with tag. Under the hood, this likely calls the Azure CLI similar to `az webapp config container set` or does a PATCH to Azure resource. We use two separate steps for the two apps, each with its own publish profile secret. (You would obtain those publish profiles from Azure portal for each web app and add to GitHub secrets). The action will handle authenticating to Azure and deploying the new image tag.

After this runs, Azure should receive the updated image references and begin pulling the new images from ACR. Because we gave the full image including tag, it will update from the old `latest` (or whatever) to this new one. If everything is set up (ACR access, etc.), the Web Apps will fetch the images and start containers. You can monitor in Azure Portal (under WebApp > Container Settings or Log Stream).

**Alternative: Deploy using Terraform in CI/CD:** Another approach is to have Terraform apply run as part of the pipeline after pushing images. For example, use `terraform apply -auto-approve -var image_tag=${{ github.sha }}` and in the TF code, use `docker_image_tag = var.image_tag`. This is doable and keeps infra and app versions in sync in code, but it requires giving the pipeline broad rights to modify infra (which it already has in our example with publish profile, but Terraform would also possibly change other things). It’s a valid approach especially if your infrastructure might also change frequently alongside code (e.g., new env vars, new services, etc.). You could also separate infra changes (done via Terraform on demand) from app deploys (done via simpler means).

**Azure DevOps Pipelines:** If using Azure DevOps, the steps are similar:

- Use the **Docker** task to build and push images (or write script tasks). Azure DevOps has built-in tasks for Docker that can use a service connection to ACR.
- Use the **Azure Web App for Container** deploy task or Azure CLI task to update the web app. Azure DevOps can use a service connection (service principal) for authentication.
- YAML example for Azure DevOps might look like:

  ```yaml
  - task: Docker@2
    displayName: Build and push React image
    inputs:
      containerRegistry: myAcrServiceConnection
      repository: myreactapp
      command: buildAndPush
      Dockerfile: path-to-react-app/Dockerfile
      tags: $(Build.BuildId)

  - task: Docker@2
    displayName: Build and push API image
    inputs:
      containerRegistry: myAcrServiceConnection
      repository: myapi
      command: buildAndPush
      Dockerfile: path-to-dotnet-api/Dockerfile
      tags: $(Build.BuildId)

  - task: AzureCLI@2
    displayName: Update Web App container settings
    inputs:
      azureSubscription: myAzureSP
      scriptType: bash
      scriptLocation: inlineScript
      inlineScript: |
        az webapp config container set --name my-react-app --resource-group my-azure-container-rg \
           --docker-custom-image-name mycontainerregistry123.azurecr.io/myreactapp:$(Build.BuildId) --docker-registry-server-url https://mycontainerregistry123.azurecr.io
        az webapp config container set --name my-dotnet-api --resource-group my-azure-container-rg \
           --docker-custom-image-name mycontainerregistry123.azurecr.io/myapi:$(Build.BuildId) --docker-registry-server-url https://mycontainerregistry123.azurecr.io
  ```

  This example uses Azure CLI to set the new image tag (the $(Build.BuildId) is a pipeline variable that is unique per run). One would also handle authentication for `az` (AzureCLI@2 can use the service principal from the service connection automatically).

**Continuous Deployment Options:**

- Azure App Service for Containers supports automatic deployment when a container image is updated in ACR if you set up webhooks. You can configure ACR to send a webhook to the App Service (the webhook URL is something like `https://<app>.scm.azurewebsites.net/docker/hook`). However, this method can be brittle and is less transparent than having CI/CD do it. We chose an approach where our CI/CD explicitly tells Azure about the new image.
- If using the `:latest` tag always, Azure by default will not auto-pull new latest unless configured. The webhook can notify it to pull. But again, using unique tags is safer.

At this point, our CI/CD pipeline automates building and deploying the app. Each merge to main (or release pipeline) results in updated containers on Azure without manual intervention. Always monitor the pipeline outputs for any failures (e.g., Docker build errors or Azure deployment issues).

### 5.2 Ensuring Successful Deployment and Testing

After a deployment, verify:

- The React site is up (browse to the React Web App URL, it should show your app). Because the React app likely calls the API, ensure it can reach it. If they are on the same domain or if CORS is configured properly for cross-domain. Azure by default gives separate subdomains for each, so you might need to enable CORS on the API for the React app’s domain or have the React app call the API via a relative path (if you mapped a custom domain or using something like Azure Front Door to unify).
- The .NET API is responding (you could use `curl` or Postman to hit an endpoint). Also check Azure Portal -> Web App -> Log Stream to see container logs. If the app failed to start, logs here (or in Application Insights, if configured) will show errors.

If anything goes wrong, use the logging and monitoring tactics discussed in the next section to diagnose.

## 6. Security and Performance Best Practices

With the application deployed and running, we must ensure it adheres to security and performance best practices. Containers and cloud infrastructure introduce considerations that developers should plan for. Below, we outline key best practices for securing the application and optimizing performance/scalability in production.

### 6.1 Security Best Practices

**Use Private Container Registry:** We used Azure Container Registry, which is a private registry. Ensure the registry is not open to the public. By default, ACR requires authentication. We disabled the admin user and used managed identities for access, which is more secure. This prevents unauthorized access to your images. Consider enabling content trust and image signing if supply chain security is a concern.

**Scan Container Images:** Regularly scan your images for vulnerabilities ([Azure Cloud & Container Security Best Practices | Sysdig](https://sysdig.com/learn-cloud-native/azure-security/#:~:text=,it%2C%20falls%20to%20the%20customer)). Azure Security Center (Defender for Cloud) can scan images in ACR for known vulnerabilities. There are also third-party tools (Aqua, Twistlock, etc.) or even Docker’s built-in `docker scan` (which uses Snyk) you can integrate in CI. Catching vulnerabilities early helps prevent deploying insecure components.

**Least-Privilege for Azure Resources:** Follow the principle of least privilege for access. Our web apps have system identities with only AcrPull role on the registry ([Azure Cloud & Container Security Best Practices | Sysdig](https://sysdig.com/learn-cloud-native/azure-security/#:~:text=,use%20%2090%20Kubernetes%20audit)). Ensure the service principal or credentials used in CI/CD also have minimal required permissions (e.g., just enough to push to ACR and deploy to the web apps, not Owner of subscription unless necessary). Use Azure Role-Based Access Control (RBAC) effectively.

**Protect Secrets:** We advocated using Key Vault for any sensitive configuration. By using Key Vault references in app settings or fetching from Key Vault at runtime (with managed identity), you avoid having secrets in source control or in plain text on the server. Also, never commit sensitive info in Dockerfiles or Terraform files. Use variables or secret stores.

**Enforce HTTPS:** Always enable HTTPS-only on your web apps (Azure does this by default for new Web Apps) so that clients cannot connect over insecure HTTP ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=https_only%20%20%20%20,lts%22%20%7D%20%7D)). If you add a custom domain, acquire an SSL certificate (Azure App Service can create a free Managed Certificate for custom domains) and bind it. This ensures data in transit is encrypted.

**Container Hardening:**

- Ensure your Dockerfiles use minimal base images (we used alpine and official Microsoft images which are regularly patched). Keep base images updated (monitor for updates to `node:alpine` or `mcr.microsoft.com/dotnet/aspnet` and update your Dockerfiles periodically).
- Run containers with a non-root user when possible. By default, the Nginx image runs as root (to bind 80) – you can modify the Dockerfile to use a non-root user and a higher port, then tell App Service to use that port. For .NET, the image runs as a non-root user by default (in Linux, ASP.NET images use user App maybe). Verify and adjust if needed. Running as non-root limits impact of any compromise.
- Remove unnecessary packages from your images. Our multi-stage approach already helps. Don’t install debugging tools in production images.

**Network Security:** If the API should not be publicly reachable except by the front-end, consider using Azure App Service access restrictions to allow only the front-end’s outbound IP or use Azure Private Link. Another approach is deploying both behind an Application Gateway or Azure Front Door where you can enforce rules and combine into a single domain. Also ensure databases or other services that the API uses are secured (e.g., restrict their firewall to the App Service outbound IPs or VNet).

**Azure Security Center:** Enable Azure Defender for App Service and Container Registry. This will monitor for misconfigurations or unusual activity. For example, it can alert on issues like container vulnerabilities, suspicious processes in containers, etc.

**IAM and Auditing:** Use Azure AD accounts for user access to Azure, not shared accounts. Enable logging of Azure resource changes (Azure Activity Log). In Terraform, use state locking and source control to track changes to infra.

**Dependencies and Libraries:** Keep your application dependencies up to date. Regularly patch the .NET NuGet packages and npm packages to pick up security fixes. Automate dependabot or similar to get alerts for vulnerabilities in your app code.

By following these practices, you reduce the attack surface and protect data both in transit and at rest. Security is an ongoing process – periodically review Azure security recommendations (Azure Advisor and Defender will give alerts/recommendations in the portal).

### 6.2 Performance and Scalability Best Practices

**Optimize Docker Images for Size & Speed:** We used multi-stage builds to create lean images. Smaller images not only deploy faster (less data to transfer) but also start faster. Continue to optimize build context (don’t copy unnecessary files). Also pin specific versions for deterministic builds. Consider using Alpine-based images where possible (as we did) for smaller footprint, but be aware of any performance trade-offs (Alpine’s musl C library can have compatibility issues in some cases, but for our apps it’s fine).

**Resource Allocation:** Choose appropriate App Service Plan SKU and size based on performance tests. Monitor CPU and memory usage. For example, if the .NET API is CPU-bound, a higher CPU instance or more instances may be needed. If memory usage is high (e.g., large caching in memory), ensure the instance has enough RAM or externalize the cache.

**Scaling Strategy:** Implement autoscaling rules that suit your workload pattern. For instance, scale out on high CPU or increase in HTTP request queue length. But also set a reasonable scale-in (cool down) period to avoid flapping (rapid scale up/down) ([Best Practices for Autoscaling in Azure App Service - Apps4Rent.com](https://www.apps4rent.com/blog/autoscaling-in-azure-app-service/#:~:text=Best%20Practices%20for%20Autoscaling%20in,the%20minimum%20value%20or)). Azure Monitor autoscale allows setting a cooldown and threshold sensitivity. Always test how your application behaves under scale – ensure there are no single points of failure (e.g., a background job running on one instance assuming single instance – in multi-instance that logic must change or use leader election).

**Statelessness:** As mentioned, keep the services stateless to leverage horizontal scaling fully ([Best practices for Azure App Service - Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices#:~:text=Best%20practices%20for%20Azure%20App,you%20more%20flexibility%20and)). If you need sticky sessions or in-memory session, use Azure Cache or database to store session state so any instance can serve any request.

**Caching and CDN:** Use caching to reduce repeated work. For example, the React static content can be offloaded to a CDN like Azure CDN or Azure Front Door Caching. That will drastically improve load times for users globally by serving assets from edge locations and reduce load on the App Service (which currently serves static files via Nginx). The .NET API can also use caching for frequent queries (in-memory or distributed). Also leverage browser caching by setting appropriate headers on static files (Nginx by default can be configured to add cache headers).

**Database and Dependencies:** Ensure that your back-end is efficiently using database connections (use connection pooling, etc.). Azure SQL or other services should be scaled appropriately to handle the API load. Sometimes the bottleneck is the database, not the app service itself.

**Asynchronous Processing:** For better responsiveness, offload long-running tasks to background jobs or Azure Functions if possible. This keeps the web API responsive to new requests and can scale those background tasks separately.

**Cognitive of Limits:** Each App Service instance has certain limits (e.g., max concurrent requests, socket connections). If you use SignalR or WebSockets, for instance, there are limits per instance. Scale out or use Azure SignalR Service if needed. Also, App Service has a limit on number of outbound connections – if your app calls external services heavily, be mindful of SNAT port exhaustion; using VNet integration with NAT gateway can help in those cases.

**Testing and Profiling:** Do load testing on your deployed app (with Azure Load Testing or Apache JMeter etc.) to find performance bottlenecks. Profile the .NET application to ensure no slow algorithms. Also monitor the startup time of your container – if it’s slow, consider techniques like **application initialization** in App Service (for Windows) or just try to minimize what happens on app start (lazy initialization of large data, etc.). App Service on Linux container will wait for the container to start and listen on the port. If your .NET app takes a long time to start, users might see delays on first load (consider using warm-up pings or Always On to mitigate cold starts).

In summary, design with scale in mind: use multiple instances, externalize state, cache aggressively, and monitor continuously. Optimize your code and containers for the cloud environment to get the best performance.

## 7. Monitoring and Logging

Once deployed, maintaining visibility into the application’s health is crucial. Azure provides a rich set of monitoring and logging capabilities. This section discusses how to capture logs from the containers, monitor performance metrics, and use Application Insights for deeper application telemetry. We’ll also cover setting up alerts for proactive monitoring.

### 7.1 Application Logs and Container Logs

**App Service Logging:** Azure App Service can capture the stdout and stderr output of your container and treat them as application logs. In our Dockerfile for .NET, we did not redirect logs anywhere special, so console logs (e.g., from `Console.WriteLine` or ASP.NET’s logging) will appear in stdout. Similarly, for Nginx/React, Nginx will log access logs to stdout by default. These logs can be viewed in several ways:

- **Log Streaming (Portal or CLI):** In Azure Portal, go to your Web App -> Log Stream. This will show real-time logs from the app container. You can also use Azure CLI: `az webapp log tail -n my-dotnet-api -g my-azure-container-rg` to stream logs to your console.
- **Log Files:** You can configure App Service to store logs on the file system (not persistent across instance restarts unless you mount Azure Storage) or to blob storage. In Portal under App Service > Configuration > Logs, you can enable application logging and specify a quota/retention. Storing to Azure Blob is useful for long-term retention or offline analysis.
- **Azure Monitor (Log Analytics):** The recommended approach for production is to send logs to a Log Analytics workspace. You can create a Diagnostic Setting for the App Service to send “AppServiceAppLogs” and “AppServiceConsoleLogs” to a Log Analytics workspace. Once there, you can query them with Kusto Query Language (KQL) and even set up alerts on certain log patterns (e.g., exceptions).

**Structured Logging:** If possible, log in a structured format (JSON) for easier querying. The .NET app could use a logging framework like Serilog to output JSON to console, which then goes to Log Analytics. This makes it easier to filter by fields in the logs.

**Container-Specific Logs:** If the container itself has multiple components (for example, Nginx logs and the React app logs), both will usually go to stdout/stderr. If not, you may need to capture them manually (but in our case, static site has no server-side logs except Nginx access logs). The .NET app’s ASP.NET logs should appear if properly configured (e.g., use Microsoft.Extensions.Logging console provider which writes to stdout, which Application Insights can also capture).

**Error Tracking:** Make sure unhandled exceptions in .NET are logged (they typically are by ASP.NET’s middleware, but if not, catch and log them). For the front-end, you might use something like Application Insights JavaScript SDK or a third-party service (Sentry, etc.) to capture front-end errors.

### 7.2 Performance and Health Monitoring (Metrics)

Azure App Service provides metrics like CPU Usage, Memory working set, Http Queue Length, Requests/sec, etc. For containerized apps, these are still available (Azure monitors the container resource usage). You can view metrics in the Azure Portal (Web App -> Monitoring -> Metrics) and create charts or alerts.

Key metrics to watch:

- **CPU Percentage** and **Memory Percentage**: high values could indicate needing to scale out or up.
- **Http 5xx Errors**: count of server errors (should be 0 ideally). If increasing, something’s wrong in the app.
- **Http Queue Length**: if requests are getting queued (for instance, if more requests come in than the app can process concurrently), this might indicate the need for scaling out.
- **Average Response Time**: to track performance from the service side (though for more detailed breakdown, Application Insights is better).

You can set up **Azure Monitor Alerts** on these metrics. For example, an alert if CPU > 80% for 10 minutes, or if 5xx errors > 5 in 5 minutes. Alerts can send emails or trigger an Azure Action (like calling a Function or Logic App for advanced notifications or remediation).

**Application Insights (APM):** For deeper application monitoring, Azure Application Insights is very valuable. It can provide:

- Detailed request telemetry (request URL, response time, success/failure, dependency calls, etc.).
- Exceptions and stack traces.
- Custom events or metrics you track.
- Performance profiles and application map (how different components interact).

For our .NET API, enabling Application Insights is straightforward. We could have added an Application Insights resource via Terraform (an `azurerm_application_insights` resource) and then set the instrumentation key or connection string in the Web App’s settings. Alternatively, Azure has a feature called _Application Insights Codeless Attach_ for certain languages, but for .NET in containers, it’s recommended to use the SDK (since our container isn’t an App Service built-in runtime, it’s a custom container, so we should use the SDK explicitly).

**Enabling Application Insights (SDK method):**

1. Create an Application Insights resource in Azure (in the same region as your services ideally). Get its Connection String.
2. Add the Application Insights SDK to your .NET project (Microsoft.ApplicationInsights.AspNetCore). Configure it in `Program.cs` to use the connection string (like `services.AddApplicationInsightsTelemetry(Configuration);` with connection string in configuration or use `APPLICATIONINSIGHTS_CONNECTION_STRING` env var).
3. In the Web App app settings, set `APPLICATIONINSIGHTS_CONNECTION_STRING` to the value from Azure (or instrumentation key via older `APPINSIGHTS_INSTRUMENTATIONKEY`).
4. Redeploy the API. It will start sending telemetry to Application Insights.

Once running, you can use the Azure Portal’s Application Insights blades to see requests, failures, traces (console logs can also be forwarded to AI via the SDK’s logger integration), and even live metrics stream. Application Insights also has a powerful query interface and ability to set up alerts on specific conditions (like alert when an exception with certain type occurs more than X times in Y minutes, etc.).

For the React front-end, you can also use Application Insights via its JavaScript SDK to track page views and browser telemetry, sending data to the same Application Insights resource. This requires adding the JS snippet to the React app (commonly in index.html or via npm package). This helps monitor user behavior and client-side performance.

### 7.3 End-to-End Monitoring Scenario

Imagine an issue in production: the React app is loading slowly or showing errors when calling the API. How do we troubleshoot with our monitoring setup?

- First, check Application Insights for any server-side errors. Perhaps the API is throwing 500 errors. AI would show exceptions and stack traces – maybe a null reference exception in a controller. From there, you identify and fix the bug.
- If no server errors, check performance metrics. If response time is high, maybe a particular dependency (like the DB) is slow. Application Insights “Application Map” might show if the database calls are the bottleneck (with average durations).
- Check front-end logs: using the browser console or if AI JS is capturing exceptions, see if the error is on client side (maybe a JSON parsing error).
- Check Azure Log Analytics to see combined logs from multiple instances during the timeframe of issue. You could query by Correlation IDs if you implement distributed tracing between front and back.
- If a serious performance issue, use Application Insights Profiler (if enabled) or take a memory dump via the Diagnose and Solve Problems in Azure (though with containers, that might require attaching via the SCM site or remote debugging if enabled).

By having logs and metrics in place, you shorten the time to detect and resolve issues.

**Setting up a Dashboard:** Azure allows creating dashboards where you can pin charts from Application Insights (e.g., server response time, 5xx count) and App Service metrics (CPU, memory). This can be a quick operations dashboard. Tools like Azure Monitor Workbooks can also present combined views and analysis.

**Regular Health Checks:** Consider adding a health check endpoint to your API (e.g., `/health` returning OK if dependencies okay). Azure App Service can be configured with a Health check (under Monitoring settings) to ping an endpoint. If it fails consecutively, Azure can restart the container automatically. We can set this up via Azure (Portal or `az webapp config set --health-check-path`). This ensures if the app gets into a bad state, it might self-recover (restart).

**Logging for Compliance:** If required, enable access logs (HTTP logs) to be stored (for auditing who accessed what). Application Insights captures request info but storing raw access logs in storage might be needed for compliance in some industries.

Finally, ensure you have a plan for **incident response**: when alerts fire (e.g., high error rate), who gets notified and how to roll back or fix forward. With our CI/CD, you could redeploy an earlier image tag if needed (since each commit SHA tag is essentially immutable image, you can edit the web app to point to a previous tag or use Terraform to roll back the `docker_image_tag` variable).

## Conclusion

Deploying a React frontend and .NET Core API as Docker containers on Azure App Service with Terraform automation provides a powerful and scalable architecture. We covered setting up the development environment, containerizing both apps with best practices like multi-stage builds ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)) ([Containerize A .NET 6 App With Docker](https://www.csharp.com/article/containerize-a-net-6-app-with-docker/#:~:text=FROM%20mcr.microsoft.com%2Fdotnet%2Fsdk%3A6.0%20AS%20build,App)), and configuring Azure infrastructure with Terraform for consistency and repeatability ([Create an App Service app using a Terraform template - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/provision-resource-terraform#:~:text=,random_integer.ri.result%7D%22%20location%20%3D%20%22eastus%22)) ([azure - Terraform create app service for linux container - Stack Overflow](https://stackoverflow.com/questions/67410585/terraform-create-app-service-for-linux-container#:~:text=site_config%20,%7D)). With CI/CD pipelines, each code change can flow to Azure seamlessly, reducing manual effort and errors. We also emphasized security measures like using private ACR and scanning images ([Azure Cloud & Container Security Best Practices | Sysdig](https://sysdig.com/learn-cloud-native/azure-security/#:~:text=,the%20cluster%20infrastructure%3B%20responsibility%20for)), and performance optimizations such as autoscaling and caching to handle load.

By following this guide, you can confidently manage container deployments in Azure:

- You can provision identical environments (dev, test, prod) via Terraform, ensuring parity.
- Developers can focus on code, knowing that CI/CD will handle building and deployment, including infrastructure changes.
- Your applications will run in isolated, portable containers, making them easier to test locally and behave consistently in Azure.
- Monitoring and logging setup will give you insight into application behavior and assist in quick troubleshooting and performance tuning.

As a next step, consider extending this setup with additional Azure services as needed: e.g., Azure SQL or Cosmos DB for data, Azure Redis for caching, Key Vault for all secrets, or Azure Front Door/Traffic Manager for geo-distribution. The principles remain the same. Everything can be defined in Terraform and automated in pipelines.

Finally, always keep learning and improving the setup. Azure and Terraform offer many advanced capabilities (blue-green deployments, canary releases, policy enforcement, etc.) that can further enhance your deployment strategy. With the solid foundation from this guide, you are well on your way to mastering cloud deployments of containerized applications in a safe, efficient, and scalable manner.
