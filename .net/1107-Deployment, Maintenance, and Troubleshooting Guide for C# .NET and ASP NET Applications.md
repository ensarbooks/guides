# Deployment, Maintenance, and Troubleshooting Guide for C# .NET and ASP.NET Applications

This guide is structured into chapters covering **Deployment**, **Maintenance**, and **Troubleshooting** of C# .NET and ASP.NET applications. Each section provides step-by-step practices, detailed explanations, code examples, and diagrams for advanced developers.

---

## 1. Deployment

Deploying .NET applications involves preparing the app for various hosting environments (Windows, Linux, cloud) and setting up supporting infrastructure like web servers, CI/CD pipelines, databases, and infrastructure code.

### 1.1 Deploying on Windows Server (IIS)

**Publish and Copy**: First, publish your ASP.NET app to a folder (e.g. using `dotnet publish`). Then copy the output to the Windows server (for example under `C:\inetpub\wwwroot\YourApp`). The published output will include your app’s DLL/EXE and all necessary .NET assemblies ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=You%20will%20notice%20that%20with,100%20DLLs%20in%20the%20output)).

**IIS Setup**: In IIS Manager, create a new Application Pool **with .NET CLR set to “No Managed Code”** (because ASP.NET Core runs out-of-process). Then create a new Website or Application pointing to your deployed folder and assign it to the new app pool ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=While%20creating%20your%20application%20in,NET%20code)). The "No Managed Code" setting is required since IIS will act as a reverse proxy to your .NET Core app instead of directly hosting .NET runtime code ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=While%20creating%20your%20application%20in,NET%20code)).

**web.config**: Ensure a _web.config_ file is present in the deployment folder. This file is generated on publish for ASP.NET Core apps and instructs the IIS **ASP.NET Core Module (ANCM)** how to start your app (invoking the .NET Core runtime and your app DLL). If the app fails to start, enable logging in web.config (`stdoutLogEnabled="true"` and set a `stdoutLogFile` path) to capture startup errors ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=At%20this%20point%2C%20your%20application,see%20where%20they%20are%20set)).

**Launch and Verify**: Once deployed and configured, navigate to the site URL. IIS will listen on the configured binding (e.g. port 80/443) and forward requests to your ASP.NET Core app process via the ASP.NET Core Module. Microsoft recommends using IIS as a reverse proxy for ASP.NET Core in production, because IIS provides robustness (process management, security hardening, logging, etc.) on Windows ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=Advantages%20of%20Using%20IIS%20with,NET%20Core%20Hosting)) ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=One%20of%20the%20big%20advantages,monitor%20the%20process%20for%20you)). If the app crashes, IIS can automatically restart the process, improving reliability ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=One%20of%20the%20big%20advantages,monitor%20the%20process%20for%20you)).

### 1.2 Deploying on Linux (Docker & Nginx)

**Build a Docker Image**: .NET Core/5+/6+ apps are cross-platform and can be containerized. Write a Dockerfile that uses Microsoft’s official images. For example:

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet publish -c Release -o /app

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app .
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "YourApp.dll"]
```

This multi-stage Dockerfile first builds/publishes the app, then copies the output to a lightweight ASP.NET runtime image. The app will listen on port 5000 (Kestrel).

**Run the Container**: On a Linux server (with Docker installed), run the container exposing the appropriate port. For example: `docker run -d -p 80:5000 --name myapp yourimage:latest`. This maps port 80 on the host to Kestrel’s port 5000 inside the container.

**Reverse Proxy with Nginx**: For production, use Nginx to forward requests to Kestrel. Install Nginx (`sudo apt-get install nginx`) and configure a site. For example, in **`/etc/nginx/sites-available/default`**:

```nginx
server {
    listen        80;
    location / {
        proxy_pass         http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header   Connection keep-alive;
        proxy_set_header   Host $host;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

This config listens on port 80 and proxies all requests to `http://127.0.0.1:5000` (where Kestrel is running) ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=server%20,Host%20%24host%3B%20proxy_cache_bypass%20%24http_upgrade)) ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=This%20configuration%20instructs%20Nginx%20to,to%20validate%20the%20syntax)). Test the setup by visiting the server’s IP; Nginx should route to the ASP.NET app. Nginx will serve as the front-end web server, handling things like static files, TLS termination, etc., and offloading dynamic request processing to Kestrel ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=This%20configuration%20instructs%20Nginx%20to,to%20validate%20the%20syntax)).

**Run as a Service**: Ensure your ASP.NET app (Kestrel) runs continuously. On Linux, you can use **systemd** to run the app as a service. For example, create `/etc/systemd/system/kestrel-yourapp.service` with content specifying the working directory, the `ExecStart` command (`dotnet /path/YourApp.dll`), and restart policies. Enable and start the service using `systemctl enable kestrel-yourapp && systemctl start kestrel-yourapp`. This will automatically start the app on boot and restart it on failure ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=Configure%20the%20ASP,To%20Run%20as%20a%20Service)) ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=,running%20on%20Ubuntu)).

### 1.3 Deploying on Cloud Platforms (Azure & AWS)

**Azure App Service**: Azure App Service is a PaaS offering for hosting web apps. You can deploy your .NET application to App Service directly from VS, CI/CD, or via `az webapp deploy`. App Service can host ASP.NET Core apps on Windows or Linux containers and provides scaling, logging, and a fully managed runtime ([Quickstart: Deploy an ASP.NET web app - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/quickstart-dotnetcore#:~:text=In%20this%20quickstart%2C%20you%20learn,with%20a%20deployed%20web%20application)). After creating an App Service, you typically just publish your application (for example, via Git deploy, FTP, or using Azure DevOps pipelines). The platform takes care of setting up the IIS/Kestrel integration for you. _Azure App Service_ is highly scalable and self-patching, which reduces maintenance overhead ([Quickstart: Deploy an ASP.NET web app - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/quickstart-dotnetcore#:~:text=In%20this%20quickstart%2C%20you%20learn,with%20a%20deployed%20web%20application)). Optionally, you can deploy your app as a Docker container to Azure Web Apps for Containers.

**Azure VMs and Other Services**: Alternatively, deploy to Azure Virtual Machines (giving you full control of a Windows or Linux server), or Azure **AKS** (Kubernetes) if containerized, or Azure Functions for serverless scenarios. For traditional web apps, Azure App Service is the fastest route.

**AWS EC2/Beanstalk**: AWS offers multiple ways to run .NET apps. You can use **EC2** (virtual machines) with Windows Server (install IIS and .NET) or Linux (Docker as above). A simpler option is **AWS Elastic Beanstalk**, which can deploy an ASP.NET application and manage the IIS or Docker container setup for you. Elastic Beanstalk will auto-provision the necessary EC2 instances, load balancer, and deploy your app – you just provide the package or container. For instance, you can deploy a .NET app to Elastic Beanstalk through AWS Toolkit in Visual Studio or through CI pipelines ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Deploying%20an%20ASP,Elastic%20Beanstalk%20Deploy%20Application%20task)). AWS also supports running .NET in containers via **ECS/Fargate**. For example, you might containerize an ASP.NET Core API and deploy it on AWS Fargate (a serverless container service) ([amazon web services - Best practices to create an AWS architecture for ASP.NET projects - Stack Overflow](https://stackoverflow.com/questions/72392737/best-practices-to-create-an-aws-architecture-for-asp-net-projects#:~:text=)). AWS Elastic Beanstalk or ECS will handle provisioning and can auto-scale the containers. In general, AWS deployment options include running on EC2, Elastic Beanstalk, ECS/EKS (Kubernetes), or even AWS Lambda for certain .NET workloads. Choose the one that best fits your management preference (PaaS vs IaaS).

**Deployment Example**: You could deploy an ASP.NET Core Web API in a Docker container to **AWS Fargate** by pushing the image to AWS ECR and creating an ECS service. Alternatively, use Elastic Beanstalk to deploy the app directly with minimal changes ([amazon web services - Best practices to create an AWS architecture for ASP.NET projects - Stack Overflow](https://stackoverflow.com/questions/72392737/best-practices-to-create-an-aws-architecture-for-asp-net-projects#:~:text=)). Always ensure your cloud resources (e.g., database, storage) are provisioned and configured (see _Infrastructure as Code_ below).

### 1.4 CI/CD Pipeline Setup (GitHub Actions, Azure DevOps, Jenkins)

Having Continuous Integration/Continuous Deployment is crucial for automating builds, tests, and deployments:

([Tutorial: Jenkins CI/CD to deploy an ASP.NET Core application to Azure Web App service](https://opensource.microsoft.com/blog/2018/09/21/configure-jenkins-cicd-pipeline-deploy-asp-net-core-application/)) _Example CI/CD pipeline flow: developers commit code to source control, CI server (e.g., Jenkins) builds and tests the project, and then the application is deployed to the target (e.g., Azure Web App)._

**GitHub Actions**: You can define workflows in YAML in your repository. For a .NET app, use the official setup-dotnet action to install the SDK, then use `dotnet build/test/publish`. For example:

```yaml
name: CI Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-dotnet@v3
        with:
          dotnet-version: "8.0.x" # Install .NET SDK
      - run: dotnet restore
      - run: dotnet build --configuration Release --no-restore
      - run: dotnet test --no-build --verbosity normal
      - run: dotnet publish -c Release -o output
      # (Optional) Deploy steps...
```

This example checks out code, sets up .NET, then builds, tests, and publishes the app. You can add subsequent steps to deploy artifacts. For instance, deploying to Azure using the Azure CLI or to AWS by uploading a Docker image. GitHub Actions can also trigger on pull requests for CI and on merges to main for CD. The pipeline ensures every commit is built and tested, and deployments are consistent ([GitHub Actions CI/CD Pipeline for Deploying .NET Web API to Amazon ECS - codewithmukesh](https://codewithmukesh.com/blog/github-actions-deploy-dotnet-webapi-to-amazon-ecs/#:~:text=,how%20the%20containerized%20application%20runs)).

**Azure DevOps Pipelines**: Azure DevOps offers YAML pipelines or a visual editor. You can use Microsoft-hosted agents to build .NET apps similarly (`dotnet restore/build/test/publish`). Azure DevOps integrates well with Azure for deployment – for example, you can use the built-in Azure Web App Deploy task or AWS Elastic Beanstalk deploy task ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Deploying%20an%20ASP,Elastic%20Beanstalk%20Deploy%20Application%20task)) ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Add%20the%20AWS%20Elastic%20Beanstalk,task%20to%20the%20build%20definition)). In Azure DevOps, set up a build pipeline that produces an artifact (the published app or a Docker image), then a release pipeline that deploys to a target (App Service, VM, etc). YAML example snippet for Azure DevOps:

```yaml
pool:
  vmImage: "windows-latest"
steps:
  - task: DotNetCoreCLI@2
    inputs:
      command: "build"
      projects: "**/*.csproj"
  - task: DotNetCoreCLI@2
    inputs:
      command: "publish"
      publishWebProjects: true
      arguments: "--configuration Release --output $(Build.ArtifactStagingDirectory)"
  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: "$(Build.ArtifactStagingDirectory)"
```

This would build and publish the app, then you could have a deployment job to push to Azure. Azure DevOps can also use gates, approvals, and multi-stage pipelines for sophisticated workflows.

**Jenkins**: Jenkins can be set up on-prem or in the cloud to build .NET apps. Use a Jenkins **Pipeline (Jenkinsfile)** with steps to checkout code and run dotnet commands. For example, a Jenkinsfile might have:

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        bat 'dotnet build YourSolution.sln -c Release'
      }
    }
    stage('Test') {
      steps {
        bat 'dotnet test YourTests.csproj -c Release'
      }
    }
    stage('Publish') {
      steps {
        bat 'dotnet publish YourProject.csproj -c Release -o %WORKSPACE%/publish'
      }
    }
    stage('Deploy') {
      steps {
        // e.g., use AWS CLI or Azure CLI to deploy, or copy files via SSH
      }
    }
  }
}
```

Jenkins has plugins for .NET (or you can just call CLI commands as above). It also has plugins for cloud providers (Azure DevOps, AWS) to ease deployments ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Add%20the%20AWS%20Elastic%20Beanstalk,task%20to%20the%20build%20definition)). For example, the AWS Toolkit for Jenkins can deploy to Elastic Beanstalk or AWS CodeDeploy. In a Jenkins pipeline, you might integrate steps to build a Docker image and push to a registry, then deploy to a Kubernetes cluster or cloud service. The CI/CD flow typically is: code commit triggers Jenkins, Jenkins builds and tests the code, and on success, Jenkins deploys the new version to the server or cloud.

### 1.5 Configuring Web Servers: IIS, Kestrel, and Nginx

**IIS (Windows)**: Internet Information Services is the web server for Windows. For .NET Framework apps, IIS directly hosts the runtime. For .NET Core/ASP.NET Core, IIS plays a proxy role. In _out-of-process_ hosting (most common), IIS forwards requests to the Kestrel server running your app. In this setup, ensure the **ASP.NET Core Hosting Bundle** is installed on the server (it includes the ASP.NET Core Module for IIS). Key configurations:

- **Application Pool**: Use _No Managed Code_ for ASP.NET Core apps (since .NET Core runtime is separate) ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=While%20creating%20your%20application%20in,NET%20code)).
- **ASP.NET Core Module (ANCM)**: web.config entries configure ANCM. It will launch the `YourApp.exe` and forward traffic.
- **HTTPS**: Typically, IIS will terminate HTTPS and pass HTTP to Kestrel. In an out-of-process scenario, ANCM forwards requests over HTTP even if received as HTTPS ([Host ASP.NET Core on Windows with IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/?view=aspnetcore-9.0#:~:text=configured%20port%20is%20usually%2080,port%20isn%27t%2080%20or%20443)).
- **Processes**: IIS can manage the process (start on first request, restart on crash). Ensure _stdout_ logging is off or rotated in production to avoid large log files.

**Kestrel**: Kestrel is the cross-platform web server built into ASP.NET Core. By default, when you run an ASP.NET Core app (e.g. `dotnet YourApp.dll`), it uses Kestrel to listen on a port (configured by `ASPNETCORE_URLS` or in appsettings). Kestrel is optimized for .NET performance and should be used behind a full web server in production for security/hardening. In development you might run Kestrel alone (e.g. at `http://localhost:5000`). In production, run Kestrel behind IIS or Nginx/Apache. This combination gives you the performance of Kestrel and the robustness of a battle-tested web server (for things like SSL, static files, request buffering). **Important settings**: if not using a reverse proxy, Kestrel can face the internet directly, but you should configure it for HTTPS with a certificate. Common practice, however, is to always have a front-end proxy for internet-facing scenarios ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=Advantages%20of%20Using%20IIS%20with,NET%20Core%20Hosting)).

**Nginx (Linux)**: Nginx is a high-performance reverse proxy and web server often used in front of Kestrel on Linux. In the configuration snippet above, we saw how to proxy to Kestrel. Other considerations:

- **SSL/TLS**: Configure Nginx with an SSL certificate (in the `server` block, use `listen 443 ssl;` and provide `ssl_certificate` files) to terminate HTTPS at Nginx.
- **Compression/Caching**: You can enable GZip compression or caching of static files in Nginx for better performance.
- **Process Management**: Unlike IIS, Nginx does not auto-restart your app if it crashes. Use systemd or a container restart policy to ensure Kestrel stays running.

**Apache**: (Not listed in question, but for completeness) Apache can similarly proxy to Kestrel using `mod_proxy`. The principles are the same as Nginx.

### 1.6 Setting up Database Connections (SQL Server, PostgreSQL, MySQL)

Connecting your application to a database requires proper connection strings and drivers:

**Connection Strings**: In .NET, connection strings are usually stored in _appsettings.json_ or environment variables. For example, a SQL Server connection string:

```json
"ConnectionStrings": {
  "DefaultConnection": "Server=mydbserver;Database=mydb;User Id=dbuser;Password=secret;"
}
```

Use the appropriate ADO.NET provider or ORM for the database:

- **SQL Server**: Use Microsoft’s System.Data.SqlClient or the newer Microsoft.Data.SqlClient. In ASP.NET Core, you can use Entity Framework Core with the **SqlServer** provider (`Microsoft.EntityFrameworkCore.SqlServer`). Example in `Startup.cs`: `services.AddDbContext<MyContext>(opt => opt.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));`.
- **PostgreSQL**: Use Npgsql (ADO.NET provider and EF Core provider). For EF Core: `UseNpgsql(connectionString)`. Ensure you have installed the NuGet package **Npgsql.EntityFrameworkCore.PostgreSQL**.
- **MySQL**: Use MySqlConnector or Oracle’s MySQL Connector/NET. For EF Core: the Pomelo EF Core MySQL provider (`Pomelo.EntityFrameworkCore.MySql`). Example: `UseMySql(connectionString, ServerVersion.AutoDetect(connectionString))`.

Each database requires its client library (ensure it’s in your project). .NET’s database connectivity is abstracted such that EF Core or Dapper can work with various databases by switching the provider. ASP.NET Core’s configuration and dependency injection make it easy to switch between, say, SQL Server in dev and PostgreSQL in prod, by using different connection strings and context configuration for each environment.

**Providers and Compatibility**: .NET’s flexibility allows integrating with SQL Server, MySQL, PostgreSQL, Oracle, SQLite, and even NoSQL (via separate libraries) ([
ASP.NET Core Basics: Working with a Database
](https://www.telerik.com/blogs/aspnet-core-basics-working-database#:~:text=One%20of%20the%20main%20features,best%20suited%20to%20their%20needs)). Ensure that if you use different DB engines between dev and prod, you account for any SQL syntax differences. (It’s generally best to use the same DB engine in all environments to avoid surprises).

**Migrations**: If using EF Core, manage database schema changes via migrations (`dotnet ef migrations add ...` and `dotnet ef database update`). Ensure the app has the correct connection string and possibly run migrations on startup for automatic schema updates (optionally).

**Secure Credentials**: Don’t hard-code DB passwords. Use user-secrets in development and environment variables or Azure Key Vault/AWS Secrets Manager in production to supply the connection string securely (see **Security** section). For example, in Azure App Service, you can set an environment variable for the connection string which EF Core will pick up.

### 1.7 Infrastructure as Code (Terraform, Bicep, CloudFormation)

Treat your infrastructure (servers, network, databases, etc.) as code to enable reproducible deployments and easy environment setup:

**Terraform**: Terraform is a popular open-source IaC tool that works with many providers (Azure, AWS, GCP, etc.). You write declarative configs in HashiCorp Configuration Language (HCL). For example, to provision an Azure App Service via Terraform, you’d define an `azurerm_resource_group`, an `azurerm_app_service_plan`, and an `azurerm_web_app` resource with the necessary settings. Terraform then creates or updates those resources in Azure. Terraform allows you to version control your infrastructure and avoids manual clicks, reducing human error ([Deploy a web app in Azure App Service using Terraform | CloudIQ Tech](https://www.cloudiqtech.com/deploy-a-web-app-in-azure-app-service-using-terraform/#:~:text=From%20a%20developers%20perspective%20Azure,reach%20the%20required%20configuration%20state)). It also manages dependencies and order (e.g., ensure the App Service Plan exists before the Web App). For AWS, you could similarly define AWS resources (EC2, RDS, Elastic Beanstalk environments, etc.) using the AWS provider.

**Bicep**: Bicep is Azure’s domain-specific language for ARM (Azure Resource Manager) templates, providing a simpler syntax for Azure IaC. If your deployment is Azure-specific, Bicep can be very handy. It compiles down to Azure’s JSON ARM templates. For example, a Bicep file to deploy a Web App might look like:

```bicep
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'myAppPlan'
  location: 'WestUS'
  sku: {
    name: 'P1v2'
    tier: 'PremiumV2'
    size: 'P1v2'
  }
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'MyAspNetApp'
  location: 'WestUS'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      netFrameworkVersion: 'v8.0' // .NET version
    }
  }
}
```

Bicep has tight integration with Azure (VS Code extension, etc.), and if you’re only targeting Azure, it can be easier than Terraform. However, it is Azure-specific, whereas Terraform is multi-cloud ([Infrastructure as Code on Azure: Bicep vs. Terraform vs. Pulumi](https://xebia.com/blog/infrastructure-as-code-on-azure-bicep-vs-terraform-vs-pulumi/#:~:text=Bicep%20is%20Microsoft%27s%20own%20domain,Where%20Bicep%20and%20Terraform)). One key difference: Terraform uses state files to track deployments, while Bicep (ARM) relies on Azure’s current state (no external state file) ([Bicep vs Terraform and modifying resources - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1054302/bicep-vs-terraform-and-modifying-resources#:~:text=Bicep%20vs%20Terraform%20and%20modifying,Terraform%20maintains%20a%20state)).

**AWS CloudFormation**: CloudFormation is AWS’s IaC service. You write templates in JSON/YAML describing AWS resources (EC2, Elastic Beanstalk environments, S3 buckets, etc.). CloudFormation will create or update the stack of resources. For example, you could have a template that defines an Auto Scaling Group of EC2 instances running your .NET app behind a Load Balancer, and an RDS SQL Server instance for the database. CloudFormation is native to AWS and integrates with AWS IAM for permissions, CloudWatch for rollbacks, etc. It ensures that related resources are deployed in order and supports rollbacks if something fails. Using CloudFormation, you can automate deploying the entire architecture of your application in AWS in one command. _AWS CDK_ is another option (where you write infrastructure in C# code which synthesizes to CloudFormation templates). The benefit of CloudFormation (or Terraform) is consistent, repeatable environments. For instance, you can define your staging and production environment in code and deploy them with the same template, reducing configuration drift ([What is AWS CloudFormation? Key Concepts & Tutorial - Spacelift](https://spacelift.io/blog/what-is-aws-cloudformation#:~:text=What%20is%20AWS%20CloudFormation%3F%20Key,resources%20on%20the%20AWS%20cloud)).

**Example**: A Terraform script can provision an AWS ECS cluster with the necessary task definitions for your Dockerized .NET app, while a Bicep script can provision the same app on Azure App Service. Store these IaC files in source control and possibly integrate their application in your CI/CD (e.g., run `terraform apply` as part of deployment, or use Azure DevOps pipelines to deploy Bicep templates). This ensures your infrastructure setup is documented and reproducible.

---

## 2. Maintenance

Maintaining a .NET application in production involves monitoring performance, optimizing when necessary, keeping the app secure, and adjusting resources as load changes. Key areas include performance tuning, security best practices, logging/monitoring, and scaling.

### 2.1 Performance Tuning and Optimization

High performance ensures your app can handle load with minimal resources and provides a good user experience. Focus on efficient code and using .NET features properly:

**Memory Management**: .NET uses a Garbage Collector (GC) to manage memory. Typically you don’t manually free memory, but you must be mindful of allocations:

- Avoid holding onto large objects longer than needed (e.g., don’t store big data in static variables unless necessary, as it lives till process end).
- Dispose of unmanaged resources or expensive objects. Use the `IDisposable` pattern or `using` statements to release things like database connections, file handles, etc., promptly.
- If you notice memory growth, investigate object retention. Tools like dotnet-counters or memory profilers can help track Gen 0/1/2 collections and Large Object Heap usage. Ensure you’re not inadvertently preventing GC (for example, events or delegates that still reference objects can cause memory leaks if not unsubscribed).
- Minimize allocations in hot code paths. For example, reuse buffers or objects where possible instead of creating new ones repeatedly. Consider using ArrayPool or Span<T> for performance-critical scenarios to reduce GC pressure.

**Async Programming**: Embrace async/await for I/O-bound operations. In ASP.NET, asynchronous code frees up the thread to handle other requests while awaiting I/O. **Avoid blocking calls** on async code – do not call `.Result` or `.Wait()` on Tasks, as this can lead to thread pool starvation or deadlocks ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Avoid%20blocking%20calls)) ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Do%20not%20block%20asynchronous%20execution,does%20not%20prevent%20that)). For example, if you have a database call, use `await db.QueryAsync()` instead of `db.Query().Result`. By doing so, a small thread pool can handle thousands of concurrent requests by not being tied up waiting on I/O ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Avoid%20blocking%20calls)). **Do not use** Task.Run in ASP.NET for long-running work that is I/O-bound; just use async methods. Only use Task.Run for CPU-bound work offloading (rare in web apps). Also avoid synchronous locks in frequently accessed code – if you must coordinate, use async-compatible locks or design to minimize lock contention. The general rule: _make hot code paths asynchronous and non-blocking_ ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Do%20not%20block%20asynchronous%20execution,does%20not%20prevent%20that)) to improve scalability.

**Efficient Data Access**: If your app uses a database, ensure queries are optimized (use indexes, load only needed data). Use asynchronous DB drivers (e.g., `SqlClient` supports async I/O). For high-throughput scenarios, consider using Dapper or raw ADO.NET for simpler queries to reduce overhead, or ensure your ORM (EF Core) is configured with compiled queries, etc. Also, use connection pooling (enabled by default in ADO.NET) by reusing connection strings and not frequently opening/closing connections excessively (let the pool handle it).

**Caching Strategies**: Caching is one of the most effective performance improvements. Identify data or results that are expensive to compute or fetch, and cache them. ASP.NET Core provides **IMemoryCache** for in-memory caching within a single server, and **IDistributedCache** for cache shared across servers (e.g., Redis). Caching can drastically reduce database load and response times by serving stored results ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)). For instance, cache lookups of reference data (like country lists) or results of expensive computations. Always set an appropriate expiration (absolute or sliding) so stale data expires ([In-Memory Caching in ASP.NET Core for Better Performance](https://codewithmukesh.com/blog/in-memory-caching-in-aspnet-core/#:~:text=In,longer%20than%20the%20sliding)). Also, never assume cached data is always there – code should handle a cache miss by retrieving fresh data ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)) ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=ASP,requests%20to%20the%20same%20server)). In a multi-server environment (web farm), consider a distributed cache to keep data consistent across instances ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=sessions%20are%20sticky%20when%20using,requests%20to%20the%20same%20server)). Cache at various levels: response caching (set HTTP cache headers for static content), application data caching (using MemoryCache/DistributedCache), and even query results caching. But be cautious: cache only where it makes sense (data that is frequently read, not changed too often). **Example**: Use MemoryCache in a service:

```csharp
public class ProductService {
    private readonly IMemoryCache _cache;
    public ProductService(IMemoryCache cache) { _cache = cache; }

    public async Task<Product> GetProduct(int id) {
       string cacheKey = $"Product:{id}";
       if(!_cache.TryGetValue(cacheKey, out Product prod)) {
           prod = await _db.LoadProduct(id);
           _cache.Set(cacheKey, prod, TimeSpan.FromMinutes(5));
       }
       return prod;
    }
}
```

This caches products for 5 minutes to avoid frequent DB hits. Caching can greatly increase throughput by reducing work ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)).

**Optimize Hot Code Paths**: Profile your application to find bottlenecks. Use tools or even simple logging/Stopwatch timing to see which methods are taking long or being called very frequently. Sometimes a small inefficient logic (like a poorly performing LINQ query inside a loop) can degrade performance under load. Optimize algorithms (e.g., use a dictionary lookup O(1) instead of a list search O(n) for frequent operations).

**GC and Throughput**: .NET allows configuring the GC (workstation vs server GC, concurrent GC). For web apps on server, server GC is default and usually optimal. If you have high memory and CPU, investigate if GC is a bottleneck (memory thrash). You might need to tune object pooling or large object usage. In extreme cases, features like Span<T>, Memory<T> allow memory-efficient processing of data (avoiding copying). But these are advanced optimizations – first ensure you are following the above best practices (async, caching, minimizing allocations).

### 2.2 Security Best Practices (Authentication, Authorization, Secure Data Handling)

Security is paramount for web applications. ASP.NET Core provides a robust security framework:

**Authentication**: Use proven libraries/frameworks for authentication instead of rolling your own. ASP.NET Core Identity is the out-of-the-box solution for managing users, passwords, and login flows (with Identity you get hashing, password rules, etc.). You can also integrate external identity providers (OAuth/OIDC) – e.g., use Azure AD, Google, IdentityServer4, or Auth0. For API scenarios, JWT Bearer authentication is common (the client gets a JWT after login and sends it on each request). .NET has **AddAuthentication().AddJwtBearer(...)** to easily enable JWT auth. Always store credentials (like JWT signing keys or third-party client secrets) securely (never in source code). If using JWT, prefer robust signing algorithms (RS256 with proper key management, or HS256 with a strong secret). **Authentication** verifies who the user is – ensure every sensitive operation requires a valid, non-expired authentication token/cookie ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Authentication%20vs)).

**Authorization**: Implement role-based or policy-based authorization to restrict what authenticated users can do ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Authentication%20%20is%20a%20process,user%20is%20allowed%20to%20do)). In ASP.NET Core, you can use `[Authorize]` on controllers or actions, with roles or policy names. Define fine-grained policies for critical actions (e.g., an "AdminOnly" policy). Consider using claims-based auth to give users specific permissions. Always check authorization in your controllers or business logic for operations that modify or view sensitive data. For example, if user A tries to access user B’s data, your code should prevent it unless allowed. Avoid bypassing the framework’s authorization checks.

**Protect Data in Transit**: Always use HTTPS in production. Obtain an SSL/TLS certificate and configure your server (IIS or Nginx) to enforce HTTPS. In ASP.NET Core, use `app.UseHttpsRedirection()` to automatically redirect HTTP to HTTPS. Also use HSTS headers for strict transport security. Modern ASP.NET project templates often include HSTS and HTTPS redirection by default. This ensures data (including cookies, auth tokens, API calls) is encrypted in transit.

**Secure Sensitive Data at Rest**: Never store passwords in plain text (use strong one-way hashing like SHA-256 with salt or preferably use the built-in Identity which uses salted PBKDF2 hashing). For connection strings or secrets in config files, in development it’s okay to use user-secrets or environment variables. In production, use services like **Azure Key Vault** or **AWS Secrets Manager** to fetch secrets at runtime ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=,10)). At the very least, if secrets are in config, protect the config file (Azure App Service, for instance, can slot-stash connection strings which are hidden). Also consider encrypting config sections if on-prem (Windows has DPAPI which ASP.NET can use via Protected Configuration). Ensure database credentials have least privilege (the DB user should have just enough rights, e.g., if the app only needs read/write on one schema, don’t use a sysadmin account).

**Validate Inputs**: Prevent common attacks by validating and sanitizing user input:

- **SQL Injection**: Use parameterized queries or ORMs (never string-concatenate user inputs into SQL). ORMs like EF Core parameterize by default ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Common%20Vulnerabilities%20in%20software)).
- **XSS (Cross-Site Scripting)**: Always encode output that contains user input. In Razor views, the default @variable syntax HTML-encodes. Be cautious with `@Html.Raw` or building HTML from user data. If you accept HTML (e.g., rich text editor), consider sanitizing it server-side to remove scripts. Use Content Security Policy (CSP) headers to mitigate XSS by restricting sources of scripts ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Common%20Vulnerabilities%20in%20software)).
- **CSRF (Cross-Site Request Forgery)**: When using cookie-based auth, always include anti-forgery tokens for state-changing POST requests. ASP.NET Core MVC provides the `[ValidateAntiForgeryToken]` attribute and generates tokens in forms automatically (or you can use the `AntiForgery` service). This prevents malicious sites from forging a user’s action on your site ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=,10)) ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Common%20Vulnerabilities%20in%20software)).
- **CORS**: If building an API, configure Cross-Origin Resource Sharing properly. Only allow trusted origins if possible, especially for credentialed requests ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=,10)).

**Use Security Headers**: Set headers like `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection` (though CSP is more effective). ASP.NET Core has middleware or you can add headers in responses.

**Keep Packages Updated**: Stay on latest patches of .NET and any libraries. Security fixes are frequent. If using containers, use updated base images to avoid known vulnerabilities.

**Authentication Flows**: For web apps, prefer OAuth/OIDC flows instead of custom auth. For example, use Authorization Code flow with PKCE for SPA or mobile connecting to your API. Avoid older implicit flows. Managed identity (if your app runs in Azure and needs to call Azure services, use Managed Identity rather than secrets) is recommended for Azure resources ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Secure%20authentication%20flows)).

**Logging and Monitoring for Security**: Log important security events (logins, failures, permission denied, etc.) and monitor for anomalies. But avoid logging sensitive info (like passwords or full credit card numbers) to not leak them.

In summary, use the security framework provided by ASP.NET Core (Identity, authentication handlers, Data Protection API for things like cookie encryption), and follow the principle of **defense in depth**: validate at every layer, least privilege for accounts, secure by default settings.

### 2.3 Logging and Monitoring

Robust logging and monitoring allows you to maintain and troubleshoot your app in production:

**Structured Logging with Serilog (or Similar)**: Serilog is a popular logging library that integrates well with .NET. It allows structured logs (key-value pairs) which are useful for querying in log systems. In `Program.cs`, you might set up Serilog like:

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .WriteTo.File("logs/app.log", rollingInterval: RollingInterval.Day)
    .CreateLogger();
builder.Host.UseSerilog();
```

This configures Serilog to log to console and file. Serilog has many “sinks” (for example, to Seq, Elasticsearch, Application Insights, etc.). Structured logs mean instead of just text, you can log with properties: `Log.Information("Processed order {@Order} for {@User}", order, user);`. These logs can be indexed and searched (e.g., find all orders by user X). Logging should be used to record key events: startup, shutdown, errors/exceptions (at least on Warning/Error level), and important business or diagnostic info at Info or Debug level.

**Application Insights (Azure)**: If running in Azure, Application Insights is a powerful APM (Application Performance Monitoring) service. By installing the Application Insights SDK (or using the built-in integration), you get automatic collection of requests, dependencies (outgoing HTTP calls, DB calls), exceptions, and custom metrics. Simply adding the instrumentation key (or connection string) configures the telemetry pipeline ([Tutorial: Jenkins CI/CD to deploy an ASP.NET Core application to Azure Web App service](https://opensource.microsoft.com/blog/2018/09/21/configure-jenkins-cicd-pipeline-deploy-asp-net-core-application/#:~:text=Pre)). In Azure App Service, you can even enable App Insights without code by enabling it in Azure (via extension). App Insights will allow you to search logs (it stores both logs and telemetry), create alert rules (e.g., if server exceptions > X, alert), and even use the **Application Insights Profiler** for performance traces. It also supports Live Metrics Stream to see real-time metrics of your app. For advanced usage, you can track custom events or metrics: e.g., `telemetryClient.TrackEvent("OrderPlaced", new { ProductId = 123 })`.

**Prometheus & Grafana (for containers/Kubernetes)**: In containerized environments, a common approach is to expose metrics in Prometheus format. You can use libraries like `prometheus-net` to expose metrics (e.g., HTTP request count, GC memory, etc.) via an endpoint (like `/metrics`). Prometheus server will scrape these metrics periodically ([Collecting Metrics in ASP.NET Core Applications - DEV Community](https://dev.to/me_janki/collecting-metrics-in-aspnet-core-applications-49cm#:~:text=Monitoring%20and%20metrics%20are%20crucial,NET%20Core%20applications)) ([Collecting Metrics in ASP.NET Core Applications - DEV Community](https://dev.to/me_janki/collecting-metrics-in-aspnet-core-applications-49cm#:~:text=,200%2C%20404%2C%20500%20etc)). Grafana can then visualize the data with dashboards. For instance, you might chart the request rate, error rate, memory usage over time. Prometheus can also alert on conditions (via Alertmanager). Use Prometheus metrics for numeric monitoring and logs (via Serilog/ELK or other) for textual analysis – together they give a full picture of application health.

**Centralized Logging**: In production, aggregate logs from all instances. If using containers, consider using Elasticsearch, Logstash, Kibana (ELK stack) or Azure Monitor. Serilog has sinks for Elasticsearch which make it easy to push structured logs to ELK. This way, you can search across logs from multiple servers in one place. Alternatively, use cloud-specific log solutions: Azure Monitor (Log Analytics) or AWS CloudWatch Logs. The goal is to not have to SSH into machines to read text log files – instead, send logs to a centralized store with query capabilities.

**Logging Levels and Performance**: Be mindful of log levels. Info and above is usually enabled in production. Use Debug/Trace for more detailed logs but those should typically be off in prod (to avoid overhead and log noise, unless troubleshooting an issue). Ensure logging isn’t in a tight loop or high-frequency hot path (or adjust the level) to avoid performance issues.

**Exceptions and Crashes**: Use logging to capture exceptions with stack traces. ASP.NET Core’s built-in logging (Microsoft.Extensions.Logging) can automatically capture unhandled exceptions if you log them in middleware. You might set up a global exception handler (UseExceptionHandler) that logs and returns an error response. For harder crashes (process exits), see troubleshooting section on capturing dumps.

**Monitoring**: Besides logs and metrics, set up monitors:

- **Performance counters**: .NET on Windows still exposes some perf counters (or use dotnet-counters for cross platform). Monitor CPU, memory, garbage collections, thread pool usage. In Azure or AWS, use their monitoring tools to watch CPU% of your instances, memory, etc.
- **Availability**: Use a ping or health-check endpoint (ASP.NET Core has Health Checks middleware) and possibly have an external service or Azure Application Insights availability test ping it to ensure your app is responding.
- **APM Tracing**: Distributed tracing is valuable if your app calls downstream services. OpenTelemetry is becoming the standard to instrument traces. Application Insights and other APMs support distributed trace correlation. This helps follow a request across microservices. Consider adding trace IDs to your logs.

**Dashboards**: Create dashboards for key metrics: requests per second, error rate, average response time, memory usage, etc., so you can glance at the health. Grafana can combine data from Prometheus (metrics) and Loki or Elastic (logs) in panels. Azure has Application Insights dashboards (or use PowerBI). The important thing is to have visibility on how your app is performing in real time and historically ([Collecting Metrics in ASP.NET Core Applications - DEV Community](https://dev.to/me_janki/collecting-metrics-in-aspnet-core-applications-49cm#:~:text=Monitoring%20and%20metrics%20are%20crucial,NET%20Core%20applications)).

**Alerting**: Set up alerts on key conditions. For example, an alert if the HTTP 500 error rate exceeds some threshold in 5 minutes, or if memory usage is close to limit, or if response time average spikes. This ensures you are notified of issues pro-actively.

### 2.4 Automated Scaling Strategies

As load varies, you may need to scale out your application (add more instances). Different platforms offer different scaling mechanisms:

**Kubernetes (Horizontal Pod Autoscaler)**: If your .NET app is deployed on Kubernetes, you can use the Horizontal Pod Autoscaler (HPA) to scale the number of pods based on metrics ([Kubernetes HPA [Horizontal Pod Autoscaler] Guide - Spacelift](https://spacelift.io/blog/kubernetes-hpa-horizontal-pod-autoscaler#:~:text=Horizontal%20Pod%20Autoscaler%20,StatefulSets%20to%20match%20user%20demand)). Typically, you might configure HPA to keep CPU at, say, 70%. If CPU usage goes above, HPA will add more pod replicas; if it drops, it will remove pods. K8s HPA can also use custom metrics (via Prometheus Adapter or Custom Metrics API) such as request queue length or memory. Additionally, **Cluster Autoscaler** can add more VM nodes if the pods can’t be scheduled. Ensure your app is stateless or uses sticky sessions or a distributed cache so that adding/removing pods doesn’t lose data. .NET apps on Kubernetes should also handle graceful shutdown (catch SIGTERM to shut down cleanly) for autoscaling. Tools like KEDA (Kubernetes Event-Driven Autoscaling) can scale .NET workers based on queue length, etc., if using Azure Service Bus, Kafka, etc.

**Azure App Service Scaling**: Azure App Services can scale out (multiple instances) and up (higher SKU). You can configure **Autoscale rules**: for example, add an instance if CPU > 70% for 5 minutes, remove one if < 20% for 10 minutes. Azure’s autoscale can be time-based as well (schedule more instances during peak hours). The newer _Automatic Scaling_ feature in App Service can manage instance counts based on HTTP load without explicit rules ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=You%20enable%20automatic%20scaling%20for,out%20simultaneously)) – you just set a max. In an autoscaled App Service, Azure will route traffic via a load balancer to all instances. Make sure any session or cache is shared (use distributed cache or session state provider, or sticky sessions via Application Request Routing if needed). Azure also provides **Azure Functions** and **Azure Container Apps**, which automatically scale out based on demand (consumption plan or metrics).

**AWS Auto Scaling**: AWS has Auto Scaling Groups (ASG) for EC2 instances. If you host your .NET app on EC2 (e.g., in an ASG behind an ELB load balancer), you can configure scaling policies based on CloudWatch metrics. For instance, scale out when average CPU > 60% and scale in when < 30%. This requires that your app instances are stateless or share state externally, so any instance can handle any request behind the ELB. AWS’s auto scaling will launch new EC2 VMs (from a Launch Template/AMI that you prepare with your app) to scale out. AWS Auto Scaling will try to maintain steady performance at the lowest cost by adjusting capacity as needed ([Application Scaling - AWS Auto Scaling](https://aws.amazon.com/autoscaling/#:~:text=AWS%20Auto%20Scaling%20monitors%20your,at%20the%20lowest%20possible%20cost)). For containerized apps on AWS ECS, there’s ECS Service Auto Scaling which can add more tasks (containers) based on CloudWatch metrics (like CPU, memory, or even custom CloudWatch metrics). AWS Lambda (for serverless) scales automatically by default (concurrency scales out).

**Scaling Databases and Caches**: Remember that scaling the app layer might require scaling the database. If using cloud managed DBs, ensure you provision for read replicas or high-performance tiers as needed. Caching layers (Redis) can also be scaled (clustered Redis or Azure Cache scaling). The entire architecture should be designed to handle scaling without single bottlenecks.

**Testing Scaling**: It’s wise to load test your application to see at what point you need to scale. Determine the metric that correlates with stress (CPU, memory, or specific queue lengths) and set autoscale rules accordingly. Also, ensure the scaling event doesn’t degrade the service (for example, if new instances take time to start, consider using Azure’s _pre-warmed instances_ feature to avoid cold starts ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=existing%20Azure%20autoscale%2C%20which%20lets,every%20instance%2C%20including%20prewarmed%20instances)) ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=to%20improve%20your%20app%27s%20performance,every%20instance%2C%20including%20prewarmed%20instances))).

**Kubernetes vs Cloud-specific**: If you are using Kubernetes on cloud VMs, you rely on HPA/Cluster Autoscaler. If you are using PaaS (App Service, Cloud Run, etc.), use their autoscale. The principles remain: monitor load and adjust instance count. Always set an upper limit to avoid runaway costs or resource saturation.

**Scale In**: Scaling down is as important – ensure that when load subsides, you’re not over-provisioning to save cost. But handle scale-in carefully if your app has background jobs or in-memory jobs – they might be terminated when an instance goes away. Design idempotent, resumable jobs if possible.

---

## 3. Troubleshooting

Despite best practices, issues in production will arise. Troubleshooting involves diagnosing errors, performance problems, and crashes in a live (or staging) environment, where you have limited access compared to a development machine.

### 3.1 Debugging Techniques for Production Issues

**Logs First**: The first step in prod troubleshooting is usually examining logs. Ensure your logging (as discussed) captures errors and important context. Often the error itself (stack trace, message) will pinpoint the issue. For example, an exception “NullReferenceException at OrderService.CalculateTotal()” gives a starting point in code.

**Remote Debugging**: In some cases, you can attach a remote debugger to a running process. Visual Studio can attach to processes on a remote machine (with the remote debugger tool running on the server). Azure App Service even offers an attach debugger feature from VS. Be extremely careful using this on production as it can halt your app; it’s more common in a staging environment. Remote debugging allows setting breakpoints on the live app, but often production issues are timing or load related, which are hard to debug with breakpoints without altering behavior.

**Reproduce Locally**: Try to reproduce the issue in a non-production environment. This might involve using the same production data set or load. If an issue only happens under high load, use a load testing tool (JMeter, k6, etc.) against a staging deployment to see if you can replicate it. If it’s data-specific (e.g., a certain record causes a bug), take a backup of prod database (or just that part) to dev and run the scenario.

**Configuration Differences**: Many production issues stem from config differences. Verify that production settings (connection strings, service URLs, feature flags, etc.) are correct. A typo in a config or missing setting can cause errors (for instance, if a required API key is not set, calls will fail). Logging configuration values (not secrets) on startup can help confirm this.

**Live Application Monitoring**: Use your monitoring tools for clues. For example, Application Insights may show an increase in failed requests and you can drill in to see the exceptions and call stacks. It might also show a specific dependency (like the database or an external API) is slow or failing, leading to your issue. If you see, for instance, that all failures are timeouts calling a third-party API, you know where to focus. Application Insights and similar APMs often allow you to search by operation ID, so you can trace a single user’s journey or a single request’s path.

**Snapshot Debugging**: Application Insights has a feature called _Snapshot Debugger_ which can capture a snapshot of the process at the moment of exception (including local variables) without halting the process for other users. This can be extremely useful to inspect state when an error happened. Other APM tools have similar functionality (e.g., Dynatrace, New Relic can show variable values on exception). Enabling these can help gather more info for hard-to-reproduce issues.

**Memory Dumps**: If an app is hung or in a bad state, capturing a memory dump of the process and analyzing it offline is a powerful technique (see below for tools). For example, on Windows use ProcDump or Task Manager to get a dump (.dmp file) when the process is unresponsive or crashing. Then analyze with WinDbg or VS. On Linux, you can use `createdump` with the .NET runtime or `gcore`.

**Review Recent Changes**: If the issue is new, correlate it with recent deployments or configuration changes. A code change might have introduced a bug that wasn’t caught in testing. Version control history and CI release notes can give hints. Roll back if necessary to confirm if the new version caused the issue (and then diff to find the bug).

**Use Feature Flags**: For toggling features in production, use feature flags. This way if a new feature causes problems, you can disable it without a full rollback. This is more of a preventive strategy but aids troubleshooting by narrowing the problem to specific toggled sections of code.

**Interactive Diagnostics**: .NET global tools like `dotnet-trace`, `dotnet-counters`, and `dotnet-dump` can be run against a running process (even in production) to collect diagnostics without stopping the process:

- `dotnet-counters` can display real-time metrics like CPU, allocations, assembly loads, exceptions count.
- `dotnet-trace` can collect a trace of CPU and .NET runtime events which you can analyze to see what the app is doing (used for performance investigations).
- `dotnet-dump` can capture a dump that you can later analyze in WinDbg or with `dotnet-dump analyze` to inspect threads and objects.

These require access to the server. In containers, you might exec into the container to run them. Be mindful of overhead and try in staging if possible.

### 3.2 Common Errors and How to Resolve Them

**HTTP 500 Errors**: A 500 (Internal Server Error) means the app threw an exception and didn’t handle it. In ASP.NET Core, unhandled exceptions in request processing will result in a 500. The browser gets a generic message, but logs (and possibly the response if in Development mode) will have details. If you encounter 500s:

- Check the application logs for exceptions. The stack trace will show where it originated.
- A common cause is misconfiguration (null reference due to missing config, or failing to connect to DB throwing an exception). For instance, if your database is down or connection string is wrong, the first DB call might throw and give 500.
- Another cause can be runtime issues like missing dependencies. On IIS, if you see _500.30 Start Failure_ or _502.5 ANCM Failure_, it indicates the app didn’t start at all (check that .NET Hosting Bundle is installed, or that your app runs standalone). The Windows Event Log can have additional info for such startup failures.
- In Azure App Service, 500 errors might be accompanied by entries in the App Service Diagnostics Log (accessible via kudu or Log Stream).

To resolve 500s: fix the underlying exception. It could be code logic error (null handling etc.), or external dependency. For temporary relief, you might add a global exception handler to catch exceptions and return a friendly message, but fundamentally you should handle known exceptions (like catch specific exceptions around external calls to perhaps retry or fall back). For example, catch a SqlException around a DB call to log it and perhaps return a cleaner error to the user (like “Service unavailable”).

During troubleshooting, you can run the app **on the server** via command line (`dotnet YourApp.dll`) to see console output. Many errors that produce 500 will also show up in the console. This is a tip especially for IIS: run the deployed app outside of IIS to see if it starts and serves requests; the console log often reveals exceptions that IIS would only report as 500 ([Troubleshoot ASP.NET Core on Azure App Service and IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/troubleshoot-azure-iis?view=aspnetcore-9.0#:~:text=This%20error%20occurs%20within%20the,log%20to%20troubleshoot%20the%20problem)) ([Troubleshoot ASP.NET Core on Azure App Service and IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/troubleshoot-azure-iis?view=aspnetcore-9.0#:~:text=500%20Internal%20Server%20Error%20in,log%20to%20troubleshoot%20the%20problem)).

**Connection Issues (Database, API)**: If your app cannot connect to the database, you might see exceptions like SqlException “Network related or instance-specific error”, NpgsqlException for Postgres, or timeout exceptions. First, verify connectivity: from the server, can you ping the DB server or open the port? Firewalls or VNet rules might be blocking. Cloud databases often require enabling the client’s IP or putting the app in the same VNet/subnet. Ensure the connection string is correct (address, credentials). If the error is a timeout, the DB might be overloaded or the query is slow – check the database’s state and slow query logs. Increase timeouts only as a last resort; better to fix the performance or connectivity issue. If connecting to a third-party API, a common issue is TLS/SSL problems or incorrect endpoints. Check that the server has the root certs updated if needed (for HTTPS calls). Use tools like `curl` or `ping` from the server to test connectivity to the service. For any connection issue, also ensure DNS is resolving correctly on the server (e.g., if using a hostname in connection string).

**Memory Leaks**: Symptoms of memory leaks include the process memory continuously growing and possibly eventually causing OutOfMemory errors or triggering container restarts. .NET memory leaks usually mean you have rooted objects that the GC cannot collect (static collections, events not removed, etc.). To troubleshoot:

- Use performance counters or `dotnet-counters` to monitor GC Heap Size, Gen2 collections, LOH size. If memory only ever grows and Gen2 collections happen but don’t reclaim much, you might have a leak.
- Capturing a memory dump at an elevated memory usage and analyzing in WinDbg with SOS (`!dumpheap -stat` to see large objects and counts, `!gcroot` on some suspect objects to see why they are rooted) is the advanced way ([Understanding WinDbg report to findout memory leaks in .net](https://stackoverflow.com/questions/15807291/understanding-windbg-report-to-findout-memory-leaks-in-net#:~:text=,Then%20try%20%21dumpheap)). This can pinpoint, for example, a list that keeps growing or objects still referenced by static events.
- Common leaks in ASP.NET: not disposing IDisposables (e.g., HttpClient in a loop – use a single instance or reuse via IHttpClientFactory), or events like a static event handler that has references to objects. Another tricky one is where you cache too aggressively without eviction (memory cache growing without bounds).
- If the leak is found, fix by removing the root cause (unsubscribe events, add disposing, or limit cache size). In the interim, you might mitigate by recycling the process (IIS can recycle app pool on memory limit, or Kubernetes will restart container on OOM).

**Deadlocks and Thread Starvation**: A deadlock in a web app might manifest as requests hanging and eventually timing out. In .NET, a classic deadlock is syncing over async: e.g., GUI apps calling `.Result` on an async call can deadlock due to sync context. In ASP.NET Core, there’s no sync context in the same way, but blocking the thread can exhaust the thread pool. If you see that requests are piling up and not completing, or CPU is low but nothing happening, you might have a lock issue or thread pool starvation:

- Investigate thread usage: `dotnet-counters` can show ThreadPool queue length. If many work items are queued and threads all busy, and not completing, something’s wrong (perhaps waiting on an external resource).
- Review code for use of `lock`. A poorly scoped lock (like locking around a call that then waits for I/O) can deadlock or at least serialize throughput. If two threads wait on each other’s locks, that’s a classic deadlock – use WinDbg to `!dumpthread` and `!syncblk` to see if threads are stuck on locks.
- Database deadlocks (different from code deadlocks): if two SQL transactions are deadlocked, SQL Server will kill one – you’d see an exception about deadlock victim. Solve by handling the exception (maybe retry after random delay) and by optimizing transaction scope (keep transactions short and touch objects in consistent order to avoid deadlocks).

**High CPU / Performance Bottlenecks**: If CPU is pegged at 100%, find out where:

- Use profiling/tracing (dotnet-trace or PerfView) to capture CPU stacks. PerfView will show which methods are consuming the most CPU. Perhaps an algorithm is O(n^2) and with large input it spikes.
- If you cannot run a trace in prod, try to capture one in a similar environment under load. Or use Application Insights Profiler which periodically records short traces of CPU when CPU is high.
- High CPU could also be GC working too hard (if allocation rate is extremely high, the app might be spending a lot of time garbage collecting). In the trace, if you see a lot of GC, consider optimizing memory as above.

**HTTP 502 / 503 Errors**: 502 Bad Gateway or 503 Service Unavailable often indicate an upstream proxy can’t reach the app or the app crashed. For example, Azure App Service might show 502 if your Kestrel process isn’t responding. Or in IIS with ANCM out-of-process, a 502.5 indicates the process failed to start. Check if your process is running. 503 from a load balancer could mean no instances are available or health checks are failing. Ensure the app is running and listening on the expected port. Check event logs or diagnostics for why it might have failed (could be missing .NET runtime, misconfigured environment variables, etc.). If you see ANCM failures, reinstalling the Hosting Bundle or ensuring the right runtime is present on the server solves many of those issues ([Troubleshoot ASP.NET Core on Azure App Service and IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/troubleshoot-azure-iis?view=aspnetcore-9.0#:~:text=to%20troubleshoot%20the%20problem)).

**Front-end Errors**: Sometimes what surfaces as an application issue is actually a front-end/browser issue (e.g., CORS misconfiguration leading to the app not being called at all). Use browser dev tools and network traces to see if requests are reaching your server and what responses are. This can help distinguish a true server error vs something like a blocked request or JS error.

### 3.3 Profiling and Diagnostics Tools

When an issue is complex, leverage specialized tools to peer inside the application:

**dotnet-trace**: A cross-platform CLI tool to collect runtime **traces** of a .NET process. It can record events like method start/stop, exceptions, GC, threadpool, etc., without requiring the app to have a profiler attached at start ([diagnostics/documentation/dotnet-trace-instructions.md at main](https://github.com/dotnet/diagnostics/blob/main/documentation/dotnet-trace-instructions.md#:~:text=diagnostics%2Fdocumentation%2Fdotnet,without%20any%20native%20profiler)). You run `dotnet-trace collect -p <pid>` and then stop it to get a trace.nettrace file. Analyze it using PerfView or Visual Studio diagnostics or convert to speedscope format for flame graphs. dotnet-trace is great for CPU investigations (which functions are hot) and general timeline of what the app is doing.

**PerfView**: A powerful Windows tool from Microsoft (GUI) that analyzes ETW traces and .NET events. You can use PerfView to **collect** data (it can collect CPU stacks, allocation profiles, etc.) and then **view** the results with nice grouping by function name, etc. It focuses on ETW (Event Tracing for Windows) and can open `.etl` files or the traces from dotnet-trace ([PerfView is a CPU and memory performance-analysis tool - GitHub](https://github.com/microsoft/perfview#:~:text=PerfView%20is%20a%20free%20performance,also%20has%20some%20support)) ([Tracing .NET applications with PerfCollect. - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/trace-perfcollect-lttng#:~:text=Tracing%20,PerfView%20on%20a%20Windows%20machine)). PerfView is especially useful for CPU/memory performance tuning – it can show which methods allocate the most or consume the most CPU. It’s a bit complex but extremely useful; many performance issues have been solved by analyzing PerfView data.

**WinDbg with SOS**: WinDbg is the low-level Windows debugger. With the SOS extension (SOS.dll) loaded, you can debug .NET internals. This is used on memory dumps or live debugging for deep issues:

- `!dumpheap -stat` to see memory usage by type (to find memory leaks, large memory usage).
- `!gcroot <address>` to find what is keeping an object in memory (find the root reference preventing collection) ([Understanding WinDbg report to findout memory leaks in .net](https://stackoverflow.com/questions/15807291/understanding-windbg-report-to-findout-memory-leaks-in-net#:~:text=,Then%20try%20%21dumpheap)).
- `!clrstack` to get managed thread stack traces of all threads (to see what they’re doing, useful if threads are hung or deadlocked).
- `!syncblk` to find monitor locks and if any thread holds a lock that others are waiting for.
- `!dumpobj` to inspect an object’s fields, etc.

WinDbg is advanced but can crack open problems you can’t solve otherwise (like memory leaks or seeing what line of code is currently executing on a hung thread in production). Microsoft has documentation and labs on using WinDbg/SOS for .NET debugging. There are also global tools like `dotnet-dump` which let you do some SOS commands in a cross-platform way. On Linux, you might use lldb with SOS for similar analysis.

**Profilers**: There are GUI profilers (Visual Studio’s Diagnostic Tools, dotTrace by JetBrains, ANTS profiler, etc.) which attach to a running process or run one and give rich info (CPU, memory). In production, it’s harder to attach these due to overhead and necessity of UI. However, tools like **dotTrace** have a remote profiling feature. You could consider profiling in a staging environment under similar load if possible.

**dotnet-counters**: Quick and useful for live monitoring of performance counters (threadpool threads, gen0/1/2 collections, exception rate, etc.). Run it against a process to see metrics updating every second. This can confirm if, for example, a lot of exceptions are being thrown (even if caught, an excessive exception rate hurts performance) or if GC is running too frequently.

**GC Dump Analysis**: For memory leaks or high memory usage, sometimes capturing a GC dump and analyzing in Visual Studio’s Diagnostic Tools (Memory Dump analysis) can be easier than WinDbg. It will list the objects and who’s holding them. The VS debugger can debug a dump with managed context, allowing you to examine objects in a friendlier way, though not as deeply as WinDbg.

**PerfCounters / Event Logs**: On Windows, classical perf counters (visible in Performance Monitor) and Windows Event Logs can provide clues. E.g., check the Application Event Log for any .NET runtime errors, or IIS errors. Event Log often records unhandled exceptions or module failures in IIS scenarios. Also, the ASP.NET Health Monitoring (if enabled) might log certain things.

**Third-party APMs**: Tools like New Relic, Datadog, Dynatrace, etc., can instrument .NET apps. They often automatically inject profilers to collect detailed traces, metrics, and even database query performance. If your application is mission critical, these can simplify finding issues (at a cost). They may also provide transaction traces that show which method or external call is slow. If using these, leverage their diagnostic info (e.g., New Relic can show that 30% of time is spent in a specific method or remote call).

**Stack Dumps on Linux**: If running on Linux and the app is hung, you can send `SIGUSR2` to a .NET Core process which will trigger it to output its stacks to the console or log (feature called `DOTNET_DumpStacks`). This is a quick way to see what all threads are doing without a full memory dump.

In essence, use lightweight tools (logs, counters) for quick analysis, and heavier tools (profilers, debuggers) for deep analysis. It’s often useful to capture data while the issue is happening (like a trace or dump at high CPU time) and then analyze offline so as not to keep the app degraded.

### 3.4 Handling Application Crashes and Performance Bottlenecks

**Application Crashes**: A crash means the process exited unexpectedly (e.g., unhandled exception on a background thread, stack overflow, out of memory, or an environment kill like Kubernetes OOM). To handle crashes:

- **Ensure Logging on Crash**: Wrap background processing in try/catch to log errors. Unhandled exceptions on the main thread in .NET Core will crash the app; consider `AppDomain.CurrentDomain.UnhandledException` event to log something just before exit (though you cannot stop the exit in .NET Core console apps).
- **Crash Dumps**: Configure the environment to capture dumps. On Windows, you can use **ProcDump** in crash monitoring mode (`procdump -ma -e -t YourApp.exe C:\dumps\dump.dmp` which will write a dump when an exception (-e) or crash happens). Windows Error Reporting (WER) can also be set to save dumps when an app crashes ([How to capture crash dump for unhandled exception using procdump](https://stackoverflow.com/questions/40319220/how-to-capture-crash-dump-for-unhandled-exception-using-procdump#:~:text=procdump%20stackoverflow,have%20Windows%20Error%20Reporting%20enabled)) ([How to generate a dump file of a .NET application - Meziantou's blog](https://www.meziantou.net/how-to-generate-a-dump-file-of-a-dotnet-application.htm#:~:text=ProcDump%20is%20a%20command,process%20uses%20too%20much%20CPU)). On Linux, set `COMPlus_DbgEnableMiniDump` and related environment variables so the runtime writes a dump on crash. These dumps can then be analyzed to find the cause (e.g., an OutOfMemoryException).
- **Restart on Crash**: Use a process manager to auto-restart. IIS and systemd do this as mentioned. Even in Kubernetes, use a liveness probe so if the app becomes unresponsive or crashes, Kubernetes restarts the container. This does not _solve_ the root cause but reduces downtime.
- **Analyze and Fix**: Once you have the dump or log of the crash, fix the underlying issue. For example, if it’s an unhandled NullReference in some background task, add handling for it. If it’s OOM, find memory leak. If it’s StackOverflow (common cause: recursive call with no termination), you'll see that in dump stack traces – fix the code.

**Performance Bottlenecks**: These manifest as slow responses or high resource usage. To handle:

- **Identify**: Use profilers or logging of timing (e.g., log when a request takes > X seconds with details). Identify what is slow – database queries? An external API? A particular algorithm?
- **Quick Mitigations**: If a particular feature is slow under load, and you have feature flags, you might turn it off or degrade gracefully. For example, if generating a large report is tying up resources, you might disable that capability until a fix is ready.
- **Optimize Code**: Once identified (say an image processing function is slow), optimize it (maybe use a more efficient library, or do it in background instead of during request). If database queries are slow, add indexes or denormalize data for faster reads. There is a wide range of possible optimizations depending on the bottleneck.
- **Scale Up/Out**: If the bottleneck is simply too much load for the given resources, and optimization options are exhausted or for immediate relief, scale out or up. Add more CPU or memory, or more instances. This should be combined with optimization – scaling is not a fix for code issues, but it buys time.
- **Use Caching**: As mentioned, cache to avoid repetitive heavy computations. If an expensive operation can be done once and reused, cache the result.
- **Background Processing**: Offload work from the request/response cycle. For instance, if a user triggers something that involves heavy computation, consider using a queue (like Azure Service Bus or RabbitMQ) and a background worker to do it, then provide the result later. This prevents slow operations from blocking user requests.
- **Profiling in Production**: Use APM tools to continuously profile if possible. This helps catch things like performance regressions after deployments (maybe a new code path is much slower).

**Example**: Suppose your site is getting a lot of 500 errors under high load, and responses are slow, eventually causing the app to crash. You investigate and find an out-of-memory crash dump showing many large JSON strings in memory. You realize that your logging of request bodies for debug (which you left on in production accidentally) is consuming too much memory when many requests hit. The fix: disable that verbose logging in production (configuration change) and deploy the fix. The app stops crashing and performance improves because it’s not doing unnecessary work.

**Preventive Measures**: After fixing an issue, add monitoring to catch it early next time. If it was high CPU, set an alert for CPU > 90% for 5 minutes. If it was memory leak, monitor memory and GC metrics, perhaps even auto-restart the app if memory crosses a threshold (to avoid a crash, though the better solution is to fix the leak).

**Deadlock/Hang**: If the app is not crashing but hung (not processing requests), treat it similarly to a crash because from user perspective it’s down. Use a watchdog (like Kubernetes liveness probe or an external ping) to detect and restart it. Meanwhile, gather a dump to see where it hung (likely a deadlock or infinite loop) and fix the code.

In summary, **crash handling** is about capturing information (dumps, logs) and recovering (auto-restart), and **bottleneck handling** is about detecting slowness and methodically improving the code or scaling resources. Advanced tools like WinDbg and PerfView are your friends for the really tough problems, giving insight into what the application is doing internally when things go wrong or slow.

---

**Sources:**

1. Stackify (BMC) – _How to Deploy ASP.NET Core to IIS_: Step-by-step IIS deployment and why the App Pool is “No Managed Code” ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=While%20creating%20your%20application%20in,NET%20code)) ([How to Deploy ASP.NET Core to IIS - Stackify](https://stackify.com/how-to-deploy-asp-net-core-to-iis/#:~:text=At%20this%20point%2C%20your%20application,see%20where%20they%20are%20set)).
2. Code Maze – _Deploy ASP.NET Core to Linux with Nginx_: Nginx reverse proxy config and explanation ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=server%20,Host%20%24host%3B%20proxy_cache_bypass%20%24http_upgrade)) ([Deploy ASP.NET Core Application on Linux with Nginx - Code Maze](https://code-maze.com/deploy-aspnetcore-linux-nginx/#:~:text=This%20configuration%20instructs%20Nginx%20to,to%20validate%20the%20syntax)).
3. Stack Overflow – _AWS architecture for ASP.NET_: Options for deploying .NET on AWS (Fargate, Elastic Beanstalk) ([amazon web services - Best practices to create an AWS architecture for ASP.NET projects - Stack Overflow](https://stackoverflow.com/questions/72392737/best-practices-to-create-an-aws-architecture-for-asp-net-projects#:~:text=)).
4. Microsoft Learn – _Quickstart: Deploy ASP.NET to Azure App Service_: Benefits of App Service (PaaS, cross-platform hosting) ([Quickstart: Deploy an ASP.NET web app - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/quickstart-dotnetcore#:~:text=In%20this%20quickstart%2C%20you%20learn,with%20a%20deployed%20web%20application)).
5. AWS Docs – _Deploying an ASP.NET app to AWS Elastic Beanstalk_: Using CI/CD (Azure DevOps) to deploy to AWS ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Deploying%20an%20ASP,Elastic%20Beanstalk%20Deploy%20Application%20task)) ([Deploying an ASP.NET web app to AWS - AWS Toolkit for Microsoft Azure DevOps](https://docs.aws.amazon.com/vsts/latest/userguide/tutorial-eb.html#:~:text=Add%20the%20AWS%20Elastic%20Beanstalk,task%20to%20the%20build%20definition)).
6. CodewithMukesh – _GitHub Actions CI/CD for .NET_: CI pipeline steps for building, testing, Dockerizing, deploying a .NET app ([GitHub Actions CI/CD Pipeline for Deploying .NET Web API to Amazon ECS - codewithmukesh](https://codewithmukesh.com/blog/github-actions-deploy-dotnet-webapi-to-amazon-ecs/#:~:text=,how%20the%20containerized%20application%20runs)).
7. Microsoft Learn – _Host ASP.NET Core on Windows with IIS_: Out-of-process model and IIS-Kestrel relationship ([Host ASP.NET Core on Windows with IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/?view=aspnetcore-9.0#:~:text=configured%20port%20is%20usually%2080,port%20isn%27t%2080%20or%20443)).
8. Telerik – _ASP.NET Core with Databases_: .NET Core integrates with SQL Server, MySQL, PostgreSQL seamlessly via providers ([
   ASP.NET Core Basics: Working with a Database
   ](https://www.telerik.com/blogs/aspnet-core-basics-working-database#:~:text=One%20of%20the%20main%20features,best%20suited%20to%20their%20needs)).
9. CloudIQ Tech – _Terraform with Azure App Service_: Terraform IaC benefits (declarative, multi-cloud, reduces human error) ([Deploy a web app in Azure App Service using Terraform | CloudIQ Tech](https://www.cloudiqtech.com/deploy-a-web-app-in-azure-app-service-using-terraform/#:~:text=From%20a%20developers%20perspective%20Azure,reach%20the%20required%20configuration%20state)).
10. Reddit – _Bicep vs Terraform_: Bicep is Azure-specific DSL, Terraform is cloud-agnostic; state management differs ([Infrastructure as Code on Azure: Bicep vs. Terraform vs. Pulumi](https://xebia.com/blog/infrastructure-as-code-on-azure-bicep-vs-terraform-vs-pulumi/#:~:text=Bicep%20is%20Microsoft%27s%20own%20domain,Where%20Bicep%20and%20Terraform)).
11. Spacelift – _What is AWS CloudFormation?_: CloudFormation is AWS’s IaC service to model and provision AWS resources ([What is AWS CloudFormation? Key Concepts & Tutorial - Spacelift](https://spacelift.io/blog/what-is-aws-cloudformation#:~:text=What%20is%20AWS%20CloudFormation%3F%20Key,resources%20on%20the%20AWS%20cloud)).
12. Microsoft Learn – _ASP.NET Core Best Practices_: Avoid blocking calls, use async to handle many concurrent requests (prevent thread starvation) ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Avoid%20blocking%20calls)) ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Do%20not%20block%20asynchronous%20execution,does%20not%20prevent%20that)).
13. Microsoft Learn – _Caching in-memory in ASP.NET Core_: Caching boosts performance by storing infrequently-changing data in memory or distributed cache ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)) ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=sessions%20are%20sticky%20when%20using,requests%20to%20the%20same%20server)).
14. Microsoft Learn – _ASP.NET Core Security Topics_: Lists built-in security features (authentication, data protection, HTTPS, app secrets, XSS/CSRF prevention) ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=,10)) ([ASP.NET Core security topics | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-9.0#:~:text=Common%20Vulnerabilities%20in%20software)).
15. MS Open Source Blog – _Jenkins CI/CD for ASP.NET to Azure_: Application Insights configured via Instrumentation Key for monitoring deployments ([Tutorial: Jenkins CI/CD to deploy an ASP.NET Core application to Azure Web App service](https://opensource.microsoft.com/blog/2018/09/21/configure-jenkins-cicd-pipeline-deploy-asp-net-core-application/#:~:text=Pre)).
16. DEV Community – _Collecting Metrics in ASP.NET Core_: Importance of metrics for monitoring and common metrics to track (requests, CPU, memory, etc.) ([Collecting Metrics in ASP.NET Core Applications - DEV Community](https://dev.to/me_janki/collecting-metrics-in-aspnet-core-applications-49cm#:~:text=Monitoring%20and%20metrics%20are%20crucial,NET%20Core%20applications)) ([Collecting Metrics in ASP.NET Core Applications - DEV Community](https://dev.to/me_janki/collecting-metrics-in-aspnet-core-applications-49cm#:~:text=,200%2C%20404%2C%20500%20etc)).
17. Kubernetes Docs – _Horizontal Pod Autoscaler_: HPA automatically adjusts replica count of pods based on metrics (CPU, custom) to meet demand ([Kubernetes HPA [Horizontal Pod Autoscaler] Guide - Spacelift](https://spacelift.io/blog/kubernetes-hpa-horizontal-pod-autoscaler#:~:text=Horizontal%20Pod%20Autoscaler%20,StatefulSets%20to%20match%20user%20demand)).
18. AWS – _AWS Auto Scaling_: Monitors apps and adjusts capacity (e.g., EC2 instances) automatically to maintain performance at lowest cost ([Application Scaling - AWS Auto Scaling](https://aws.amazon.com/autoscaling/#:~:text=AWS%20Auto%20Scaling%20monitors%20your,at%20the%20lowest%20possible%20cost)).
19. Microsoft Learn – _Troubleshoot ASP.NET Core on Azure/IIS_: 500 errors indicate an error in app code; check stdout log or run app directly to see error details ([Troubleshoot ASP.NET Core on Azure App Service and IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/troubleshoot-azure-iis?view=aspnetcore-9.0#:~:text=This%20error%20occurs%20within%20the,log%20to%20troubleshoot%20the%20problem)) ([Troubleshoot ASP.NET Core on Azure App Service and IIS | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/troubleshoot-azure-iis?view=aspnetcore-9.0#:~:text=500%20Internal%20Server%20Error%20in,log%20to%20troubleshoot%20the%20problem)).
20. GitHub (dotnet/diagnostics) – _dotnet-trace tool_: dotnet-trace is a cross-platform CLI tool to collect traces from a running .NET process without a profiler attached ([diagnostics/documentation/dotnet-trace-instructions.md at main](https://github.com/dotnet/diagnostics/blob/main/documentation/dotnet-trace-instructions.md#:~:text=diagnostics%2Fdocumentation%2Fdotnet,without%20any%20native%20profiler)).
21. Jenkins.io – _.NET SDK Support in Jenkins_: PerfView is a free CPU and memory analysis tool focused on ETW events for .NET, helps identify performance issues ([PerfView is a CPU and memory performance-analysis tool - GitHub](https://github.com/microsoft/perfview#:~:text=PerfView%20is%20a%20free%20performance,also%20has%20some%20support)).
22. Stack Overflow – _Debugging memory leaks with WinDbg_: Use SOS in WinDbg (`!dumpheap`, `!gcroot`) to find .NET memory leaks by examining heap and roots ([Understanding WinDbg report to findout memory leaks in .net](https://stackoverflow.com/questions/15807291/understanding-windbg-report-to-findout-memory-leaks-in-net#:~:text=,Then%20try%20%21dumpheap)).
23. Microsoft Learn – _ProcDump - Sysinternals_: ProcDump can monitor an application for exceptions or CPU spikes and capture crash dumps for post-mortem analysis ([ProcDump - Sysinternals | Microsoft Learn](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump#:~:text=ProcDump%20,crash%20dumps%20during%20a%20spike)).
