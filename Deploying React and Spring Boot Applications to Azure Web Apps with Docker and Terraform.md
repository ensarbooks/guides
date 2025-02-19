# Deploying React and Spring Boot Applications to Azure Web Apps with Docker and Terraform: An Advanced Guide

This comprehensive guide walks through a production-ready deployment of a React frontend and Spring Boot backend on Azure Web Apps using Docker containers and Terraform. We cover everything from technology overviews to environment setup, containerization, infrastructure provisioning, deployment, networking, security, CI/CD, monitoring, scaling, and best practices. Each chapter provides step-by-step instructions, code examples, and tips for advanced developers.

## 1. Introduction to Technologies

In this chapter, we introduce the core technologies and explain why combining them creates a powerful, modern cloud deployment pipeline.

### React (Frontend)

**React** is a popular open-source JavaScript library for building dynamic user interfaces ([React – A JavaScript library for building user interfaces](https://legacy.reactjs.org/#:~:text=React)). It allows developers to create reusable UI components and manage application state efficiently in single-page applications. React focuses on the **view layer** in web apps, making it easy to build rich interactive interfaces. Its component-based architecture and virtual DOM system enable fast updates and a smooth user experience even as data changes frequently.

### Spring Boot (Backend)

**Spring Boot** is an open-source Java framework that simplifies building production-ready web services and microservices ([What Is Java Spring Boot? | IBM](https://www.ibm.com/think/topics/java-spring-boot#:~:text=Java%20Spring%20Boot%20,Spring%20Framework%20faster%20and%20easier)). It is built on the Spring Framework and provides **auto-configuration** and an **opinionated setup** to quickly create stand-alone applications with embedded servers (like Tomcat). Spring Boot favors convention over configuration, so you can get a REST API or web backend running with minimal boilerplate. It's ideal for creating robust backends, exposing RESTful APIs, and connecting to databases or other services, all with enterprise-grade capabilities.

### Docker (Containerization)

**Docker** is an open platform for developing, shipping, and running applications in lightweight containers ([Get Docker | Docker Docs
](https://docs.docker.com/get-started/get-docker/#:~:text=Docker%20is%20an%20open%20platform,developing%2C%20shipping%2C%20and%20running%20applications)). Containers package an application with its dependencies and environment, ensuring that it runs consistently across different environments (development, testing, production). By containerizing the React frontend and Spring Boot backend, we can eliminate "it works on my machine" issues. Docker allows us to define images (via Dockerfiles) that bundle the code, runtime, libraries, and system tools needed. This ensures the apps run the same way on any host that runs Docker. Containers are also portable and efficient, making deployment and scaling easier.

### Terraform (Infrastructure as Code)

**Terraform** is an open-source _Infrastructure as Code (IaC)_ tool that lets you define and provision infrastructure using declarative configuration files ([Terraform](https://www.sonicwall.com/glossary/terraform#:~:text=Terraform)). Instead of clicking through cloud consoles or running imperative scripts, you describe your Azure resources (Web Apps, databases, networks, etc.) in `.tf` files. Terraform then plans and applies those changes to Azure, while maintaining a state file to keep track of deployed resources. It provides a consistent CLI workflow to manage hundreds of cloud services and ensures infrastructure deployments are repeatable and version-controlled. Using Terraform, we can automate Azure resource creation (like App Service instances, resource groups, networks) in a reliable, traceable manner.

### Azure Web Apps (Azure App Service)

**Azure Web Apps**, part of Azure App Service, is a fully managed platform for hosting web applications, REST APIs, and backend services ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Azure,REST%20APIs%2C%20and%20mobile%20backends)). It supports multiple languages and frameworks (including Java/Spring and Node/React) and can directly run Docker containers. Azure Web Apps is an HTTP-based service with built-in features like load balancing, auto-scaling, and simplified SSL setup, so developers don't need to manage the underlying servers. We will use **Azure Web App for Containers**, which allows deploying our Dockerized React and Spring Boot applications to Azure with minimal management overhead. An App Service **plan** defines the compute resources (like VM size, scaling settings) for these web apps ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=)).

### Why Use These Technologies Together?

Combining React, Spring Boot, Docker, Terraform, and Azure Web Apps enables a modern, cloud-native deployment approach:

- **Decoupled Frontend & Backend**: React (frontend) and Spring Boot (backend) communicate over HTTP APIs. This separation of concerns allows independent development, scaling, and deployment of the UI and API. Both are proven, widely-used technologies for building scalable web applications.

- **Containerization**: Packaging both apps into Docker containers ensures environment consistency from development through production. If a full-stack JavaScript/Java developer already uses Docker for deployment, this approach fits naturally ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=If%20you%20are%20a%20modern,tied%20down%20to%20just%20Java)). Containers encapsulate all dependencies, so the apps run reliably on Azure as they did locally.

- **Managed Hosting**: Azure Web Apps provides a PaaS hosting environment, abstracting away server maintenance. It's easy to deploy Docker images to App Service via various methods (CLI, CI/CD, Terraform) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=Deploying%20Java%20web%20applications%20to,of%20deploying%20a%20web%20app)). Azure handles details like OS patching, load balancing, and scaling, so you focus on your application code.

- **Infrastructure as Code**: Terraform brings the principles of software development to cloud infrastructure. By writing Terraform configurations, you can version control your infrastructure, review changes, and avoid manual errors. This IaC approach prevents configuration drift and makes it easier to replicate environments (e.g., dev, staging, prod) ([Deploy to Azure with IaC and GitHub Actions - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/devops/deliver/iac-github-actions#:~:text=Benefits%20of%20using%20IaC%20and,automation%20for%20deployments)). Using Terraform with Azure ensures deployments are consistent and automated.

- **Scalability and DevOps**: With this stack, you can automate the entire pipeline: code, containerize, provision, deploy, and monitor. It supports advanced DevOps practices: continuous integration/continuous deployment (CI/CD), blue-green deployments, automated scaling, and monitoring. The synergy of these tools results in a highly reproducible and scalable architecture, suitable for production workloads.

In summary, using React and Spring Boot gives a powerful front/back-end combo, Docker ensures consistent deployment, Azure Web Apps provides a robust hosting platform, and Terraform automates infrastructure management. This combination is ideal for advanced developers building cloud-ready, microservice-style applications.

---

## 2. Setting Up the Development Environment

To get started, you need to prepare your local development environment with all necessary tools. This chapter covers installing and configuring the software you'll use to develop, containerize, and deploy the applications.

### Required Tools and Prerequisites

Ensure the following tools are installed on your development machine:

- **Node.js and npm** – Node.js (with npm or Yarn) is required to develop and build the React application. Download Node.js from the official site (choose the LTS version for stability). Installing Node.js will also install the Node Package Manager (npm). Verify the installation by running `node -v` and `npm -v` in a terminal.

- **Java Development Kit (JDK)** – A Java JDK (Java 11 or higher) is needed to develop and build the Spring Boot application. Install AdoptOpenJDK or Temurin (OpenJDK distribution) for your OS and verify with `java -version`. Spring Boot apps typically use Java 11 or Java 17 in modern setups.

- **Build Tool (Maven or Gradle)** – Spring Boot projects use Maven or Gradle to manage dependencies and build the application. Install Apache Maven (e.g., version 3.8+) or Gradle (if you prefer) and confirm by `mvn -v` or `gradle -v`. (If using Spring Initializr to bootstrap the project, you can choose Maven or Gradle.)

- **Docker** – Install Docker Desktop for your platform to build and run containers. Docker will allow us to create images for the React and Spring Boot apps and test them locally. You can get Docker Desktop from Docker's official site. Verify installation with `docker -v` and run `docker ps` to ensure the Docker daemon is running. Docker is essential for containerizing the applications.

- **Terraform** – Download and install Terraform (v1.x or newer) from HashiCorp. Terraform is a single binary; make sure it's in your PATH. Check with `terraform -v`. This tool will be used to define and provision Azure infrastructure as code.

- **Azure CLI** – Install the Azure Command-Line Interface (Az CLI) to interact with Azure from your terminal ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=To%20try%20this%20out%20you,to%20install%20them%20if%20needed)). You can get it from Microsoft’s docs. After installation, run `az login` to authenticate to your Azure account (this opens a browser for login). Verify Azure CLI with `az --version`. The CLI will be used for some manual Azure operations and can also be leveraged in automation scripts.

- **Git** (optional but recommended) – Install Git for version control, so you can manage your code and Terraform configuration in a repository. This is particularly useful when implementing CI/CD.

**System Requirements**: Ensure your system has sufficient resources (memory, CPU) to run Docker containers and build processes. Docker for Windows/Mac may require enabling virtualization in BIOS.

### IDE and Extensions (Optional)

While not strictly required, using a powerful IDE can boost productivity:

- **Visual Studio Code** with extensions for Docker, Terraform, and Azure is a great choice. The _Docker extension_ helps with container files, _HashiCorp Terraform extension_ provides syntax highlighting and linting for `.tf` files, and _Azure Account/Azure App Service extensions_ allow direct Azure interactions.
- **IntelliJ IDEA** (or VSCode) for Java/Spring development can assist with writing and debugging Spring Boot code. IntelliJ has built-in Spring support and can also work with Docker via plugins.

These tools aren't mandatory, but they make development easier.

### Configuring Local Environments

After installing the tools, do some one-time setup:

1. **Azure CLI Authentication**: Run `az login` to authenticate. If you have multiple Azure subscriptions, set the desired one as default with `az account set -s <Your-Subscription-ID>`. This ensures Terraform and CLI commands target the correct subscription.

2. **Azure Service Principal (optional)**: If you plan to use Terraform in an automated environment (CI/CD), consider creating an Azure Service Principal (an Azure AD application with credentials) for Terraform to use. You can create one via Azure CLI:

   ```bash
   az ad sp create-for-rbac --name terraform-sp --role="Contributor" --scopes="/subscriptions/<SUB_ID>"
   ```

   This will output an appId, tenant, and password. You can configure Terraform to use these credentials via environment variables (`ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID`). For local use, Azure CLI can also provide credentials to Terraform, so this is optional for now.

3. **Docker Configuration**: If on Windows or Mac, ensure Docker has enough memory allocated in settings (at least a few GB) because building the images can be resource-intensive (especially for Java builds). Linux users should just ensure Docker service is running.

4. **Verify Tools**: Open a terminal and run the following to verify each tool is ready:

   - `node -v && npm -v` – Confirm Node.js and npm.
   - `java -version` and `mvn -v` – Confirm JDK and Maven (if using Gradle, check `gradle -v`).
   - `docker run hello-world` – Test Docker can run a container.
   - `terraform -v` – Test Terraform is accessible.
   - `az account show` – Test Azure CLI (should show subscription details if logged in).

   If each command returns expected version info or output, you're set up correctly. Any issues here should be resolved (e.g., add tools to PATH, ensure Docker daemon running, etc.) before proceeding.

5. **Project Structure**: Create a directory structure for your project. For example:
   ```
   azure-fullstack-guide/
     ├── frontend-react/   (React app code and Dockerfile)
     ├── backend-spring/   (Spring Boot app code and Dockerfile)
     └── infra-terraform/  (Terraform configuration files)
   ```
   This separation helps manage the codebases. Initialize a git repository in `azure-fullstack-guide` if using version control.

By the end of this setup, you have all necessary tools installed and verified. Next, we will create the React and Spring Boot applications and containerize them.

---

## 3. Building and Containerizing Applications

Now that the environment is ready, we will build the frontend React application and the backend Spring Boot application, then create Docker container images for each. This chapter walks through application setup, optimizing builds for production, writing Dockerfiles, and using multi-stage builds for efficiency.

### Creating a React Application and Preparing for Production

First, let's create the React app. You can use Create React App for a quick start:

1. **Initialize React App**: Run the following in the `frontend-react` directory:

   ```bash
   npx create-react-app my-react-app
   ```

   This will scaffold a new React application in a folder named `my-react-app` inside `frontend-react`. (You can name it appropriately for your project.)

2. **Development Testing**: `cd my-react-app` and run `npm start` to ensure the app launches in development mode (on http://localhost:3000). You should see the default CRA homepage. This confirms the React setup is working.

3. **Customize App**: Replace the default content with your application's actual UI as needed. For this guide, we focus on deployment, so assume you have a functioning React app ready to be built.

4. **Production Build**: When ready to deploy, create an optimized production build with:

   ```bash
   npm run build
   ```

   This bundles the React app into static files (HTML, JS, CSS) under the `build/` directory. The bundle is minified and optimized for performance (React will produce a minified production build) ([Optimizing Performance - React](https://legacy.reactjs.org/docs/optimizing-performance.html#:~:text=If%20you%27re%20benchmarking%20or%20experiencing,with%20the%20minified%20production%20build)). Ensure no errors in this step; fix any build issues that arise.

5. **Serve vs Static**: Decide how to serve the React app in production. Common approaches:
   - **Static Hosting**: Because React builds static files, you could serve them via a simple static file server (like Nginx). In our Docker approach, we will use an Nginx container to serve the files.
   - **Node Server**: Alternatively, use a Node.js server (e.g., Express) to serve the static files. But using Nginx is simpler and more performant for static content.

We will proceed with using Nginx in the Docker container to serve the React app's build output.

### Setting up a Spring Boot Backend with Database Connectivity

Next, create the Spring Boot application:

1. **Initialize Spring Boot App**: Use Spring Initializr (https://start.spring.io) to generate a Spring Boot project, or use your IDE to create one. Include dependencies such as **Spring Web** (for REST APIs) and a **Spring Data** driver for your database (for example, MySQL or PostgreSQL driver if you plan to use those in Azure). Also include **Spring Boot Actuator** for monitoring (optional, but useful in production).

   Choose Maven (pom.xml) or Gradle for build, Java version (11 or 17), and packaging type "Jar". For this guide, assume a Maven project named "spring-backend".

2. **Project Structure**: The generated project (in `backend-spring/spring-backend`) will have a main application class (e.g., `Application.java`) and resource files. Implement your REST controllers and business logic as needed. For this deployment guide, a simple REST endpoint (e.g., `/api/hello`) is sufficient to test connectivity.

3. **Database Config**: If your Spring Boot app uses a database, configure it in `application.properties` (or YAML). For example, for a MySQL database, you might have:

   ```properties
   spring.datasource.url=jdbc:mysql://<DB_HOST>:3306/<DB_NAME>
   spring.datasource.username=<USER>
   spring.datasource.password=<PASSWORD>
   spring.jpa.hibernate.ddl-auto=update
   ```

   For local testing, you could use an in-memory database (H2) or a local MySQL. Ensure the app can start and connect to the database in a dev environment. We will later use Azure Database or a managed DB, and secure these credentials via Azure Key Vault or environment variables in production (no hardcoding secrets!).

4. **Test Locally**: Run the Spring Boot app locally to ensure it works. With Maven, `./mvnw spring-boot:run` (or run the `main()` from your IDE). Verify the API endpoints respond (e.g., GET http://localhost:8080/api/hello returns expected data). If connecting to a local DB, ensure that is running and the credentials are correct.

5. **Build JAR**: Package the application for production:
   ```bash
   ./mvnw clean package -DskipTests
   ```
   This creates a fat jar (e.g., `spring-backend-0.0.1-SNAPSHOT.jar` in `target/`). We'll use this JAR in the Docker image.

**Note on Profiles**: Spring Boot allows multiple environments via profiles. You might have a `application-dev.properties` for local development (H2 DB, etc.) and a `application-prod.properties` for production (Azure DB, different settings). We can activate profiles via environment variables or command-line flags in the container (e.g., `-Dspring.profiles.active=prod`). Planning profiles helps in configuration for cloud deployment.

### Writing Dockerfiles for Both Applications

Now, let's containerize each application by writing Dockerfiles. We will use **multi-stage builds** to optimize the image sizes.

#### Dockerfile for React App (Nginx approach)

Create a file `Dockerfile` inside the React app directory (where the `build/` folder is generated):

```Dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./   # copy manifest files
RUN npm install                         # install dependencies (you could use `npm ci` for exact installs)
COPY . .                                # copy all source code
RUN npm run build                       # build the React app (outputs to /app/build)

# Stage 2: Serve the app with Nginx
FROM nginx:alpine
# Copy built files from Stage 1
COPY --from=build /app/build /usr/share/nginx/html

# Optional: copy a custom nginx.conf if needed (for routing SPA)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 and specify default command
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Explanation**: The first stage uses a Node.js environment to compile the React application. We only keep the final build artifacts. The second stage starts from a small Nginx image and simply serves the static files. Multi-stage builds ensure that the final image does not include Node or source code, just the static content and Nginx – resulting in a smaller image and reduced attack surface ([Get Docker | Docker Docs
](https://docs.docker.com/get-started/get-docker/#:~:text=Docker%20is%20an%20open%20platform,developing%2C%20shipping%2C%20and%20running%20applications)) (the build tools are not present in the runtime image).

If your React app is a single-page app that uses client-side routing (e.g., React Router), you'll want a custom `nginx.conf` to redirect all requests to `index.html` (so refreshes or direct URL access route correctly). Otherwise, the default Nginx config will serve the static files.

#### Dockerfile for Spring Boot App

In the Spring Boot project directory, create a `Dockerfile`:

```Dockerfile
# Stage 1: Build the Spring Boot app using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the Spring Boot app on a lightweight JRE
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/spring-backend-0.0.1-SNAPSHOT.jar app.jar
# Optionally, add a non-root user for security
RUN adduser -u 1001 -D appuser && chown -R appuser /app
USER appuser
EXPOSE 8080
# Use exec form to start Java
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

**Explanation**: The first stage uses a Maven image with JDK 17 to compile the Spring Boot application. It copies the source and runs the Maven build, producing a JAR. The second stage uses a slim JRE base image (Alpine Linux + Temurin JRE) to run the application. We copy the JAR from the builder stage. We also create a non-root user (with UID 1001) to run the app for security (running as root in containers is a bad practice). The container listens on port 8080 (Spring Boot default). We set the entrypoint to run the jar.

This multi-stage approach ensures the final image only contains the JRE and our application jar, not the entire Maven toolchain or source code, reducing image size significantly (often by hundreds of MB).

**Managing Image Size and Optimizations**:

- The `maven:3.9-eclipse-temurin-17` image is heavy. You could optimize by using Maven's `dependency:go-offline` before copy src (to cache dependencies) or use build caching. However, for simplicity, the above is fine. Alternatively, use **Jib** (by Google) which can build container images without a Dockerfile, or **Spring Boot buildpacks**, but using a Dockerfile as above gives explicit control.

- The final JRE alpine image is tiny (~70MB). Ensure your Spring Boot app doesn't require libraries missing in Alpine's musl libc environment. If you face issues, use a debian-slim base instead (slightly larger but more compatible).

- The React image (Nginx) will be around ~20MB plus the static files, which is small.

#### Building the Docker Images Locally

Now build and test the images locally:

1. **Build React image**:

   ```bash
   docker build -t myreactapp:latest ./frontend-react/my-react-app
   ```

   (Use the appropriate path to your React Dockerfile). Docker will output the build steps. Verify it finishes successfully and the image is listed via `docker images`.

2. **Run React container**:

   ```bash
   docker run -d -p 3000:80 --name myreactcontainer myreactapp:latest
   ```

   This runs the container detached, mapping port 80 in the container to 3000 on host. Visit http://localhost:3000 to see the React app served by Nginx. It should show your production build. If something is wrong (e.g., site not found), check container logs (`docker logs myreactcontainer`) and adjust (common mistake: forgetting to copy build output to correct directory, or misplacing nginx config).

3. **Build Spring Boot image**:

   ```bash
   docker build -t myspringapp:latest ./backend-spring/spring-backend
   ```

   Ensure the JAR name in Dockerfile matches what Maven produces (adjust version if needed, or use a wildcard copy like `target/*.jar`). The build may take a few minutes as it downloads dependencies and compiles code.

4. **Run Spring Boot container**:
   ```bash
   docker run -d -p 8080:8080 --name myspringcontainer myspringapp:latest
   ```
   The app will start. Check logs with `docker logs -f myspringcontainer` for the Spring Boot startup logs. Once it's running, test an endpoint: e.g., `curl http://localhost:8080/api/hello`. You should get the expected response from the API.

If both containers work individually, we have successfully containerized the applications.

**Docker Compose (Optional)**: To streamline local testing of both containers together (especially if they need to talk to each other or share a network), you can use a `docker-compose.yml` to define both the React and Spring containers, plus perhaps a database container for local dev. This can simulate the production environment. For brevity, we won't cover Compose in depth, but it's a useful tool:

```yaml
version: "3.8"
services:
  frontend:
    image: myreactapp:latest
    ports:
      - "3000:80"
  backend:
    image: myspringapp:latest
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/mydb # example of linking to a DB service
      - SPRING_DATASOURCE_USERNAME=root
      - SPRING_DATASOURCE_PASSWORD=password
  db:
    image: mysql:8
    environment:
      - MYSQL_DATABASE=mydb
      - MYSQL_ROOT_PASSWORD=password
```

Running `docker-compose up` would start all services and allow the React app to call the Spring Boot service via `http://localhost:8080` (or by service name `backend` if configured for internal network). This is great for integration testing before deploying to Azure.

### Multi-Stage Builds and Image Optimizations

We have already applied multi-stage builds in the Dockerfiles. To reiterate best practices for Docker images:

- **Leverage Multi-Stage Builds**: Compile or build in an intermediate stage, and use a minimal base image for runtime. This removes dev dependencies and yields smaller images, which deploy faster and have fewer security vulnerabilities ([Get Docker | Docker Docs
  ](https://docs.docker.com/get-started/get-docker/#:~:text=Docker%20is%20an%20open%20platform,developing%2C%20shipping%2C%20and%20running%20applications)).

- **Use Specific Base Image Versions**: Pin versions (like `node:18-alpine` and `eclipse-temurin:17-jre-alpine`) to ensure consistency. Avoid using `latest` in production images, as updates could change the environment.

- **Small Base Images**: Alpine-based images are smaller but occasionally have compatibility issues. Test thoroughly. Another approach is to use distroless images for Java (Google Distroless for Java) which contain only the JRE and no package manager or shell.

- **Caching Dependencies**: Reorder Dockerfile steps to maximize layer caching. For example, copying `pom.xml` and running `mvn install` on it can cache dependencies before adding the rest of the source code (so that re-building after small code changes doesn't redownload all jars). Similarly for Node, copying `package.json` and running `npm install` first, then copying the rest, helps reuse the layer when code changes but dependencies don't.

- **Security**: Consider scanning your images for vulnerabilities (Azure Container Registry has scanning features). Also, running containers as non-root (we did for Spring) is recommended for security.

At this point, we have our two application images ready: `myreactapp:latest` and `myspringapp:latest`. In the next chapters, we'll push these images to a registry and use Terraform to set up Azure infrastructure to run them.

---

## 4. Terraform for Infrastructure as Code (IaC)

In this chapter, we'll dive into Terraform: setting up Terraform configuration for Azure resources, following best practices for IaC, and preparing to manage our infrastructure declaratively. We'll create scripts to provision an Azure App Service (for our containers), a database, networking components, and any other required resources. We will also discuss managing Terraform state.

### Understanding Terraform Basics

Terraform allows you to define cloud resources in a **HashiCorp Configuration Language (HCL)**. The workflow typically is: write .tf files, run `terraform init` (to set up provider plugins), run `terraform plan` (to see what changes will occur), then `terraform apply` to create/update infrastructure ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=Terraform%20enables%20the%20definition%2C%20preview%2C,plan%20to%20deploy%20the%20infrastructure)).

Key concepts:

- **Providers**: Plugins that enable Terraform to manage resources on a specific platform. For Azure, we use the `azurerm` provider (Azure Resource Manager). This will require Azure credentials (Terraform can use Azure CLI's logged-in context or environment variables for a service principal).
- **Resources**: Blocks in .tf files that describe a piece of infrastructure (e.g., an Azure Resource Group, an App Service Plan, an App Service, a Database server). Each resource has attributes (settings).
- **Variables and Outputs**: You can parameterize your scripts using input **variables** (for things like region, resource names, etc.) and produce **outputs** (like the site URL) after applying. We'll use variables to avoid hardcoding values.
- **State**: Terraform keeps a state file (`terraform.tfstate`) that maps your Terraform config to real-world resources. This state is critical – it’s how Terraform knows what is already deployed to decide what to add or destroy. We need to store this state securely, especially when working in teams or CI.

Benefits of using Terraform (and IaC) for our scenario include consistency and repeatability in deployments. The entire Azure environment (Web App, database, networking) can be recreated or updated by changing code, not clicking through the portal. This also allows code review and version control for infrastructure changes, increasing reliability ([Deploy to Azure with IaC and GitHub Actions - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/devops/deliver/iac-github-actions#:~:text=Benefits%20of%20using%20IaC%20and,automation%20for%20deployments)).

### Terraform Best Practices for Azure

Before writing our Terraform files, consider these best practices:

- **Organize Configuration**: Use separate files or directories for logical components. For a simple project, a few `.tf` files in one folder is fine (e.g., `main.tf`, `variables.tf`, `outputs.tf`). For larger, consider modules or separating by environment.

- **Use Variables**: Define variables for anything that might change or be environment-specific (like resource name prefix, Azure region, VM sizes, Docker image names, etc.). This makes your configuration reusable. Provide sensible defaults or use a `terraform.tfvars` for actual values not committed to source control (like passwords).

- **Remote State**: Do not keep state purely locally when collaborating or using CI. Instead, use a remote backend for Terraform state (Azure Storage is commonly used). Storing state in Azure Blob with locks prevents concurrent modifications and secures the state file. Local state is prone to loss and doesn't work well with teams ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=By%20default%2C%20Terraform%20state%20is,ideal%20for%20the%20following%20reasons)). We'll configure an Azure Storage account for this.

- **State Management**: Keep state secure because it can contain sensitive information (like generated passwords or keys). Use backend encryption (Azure Storage encrypts by default) and access controls. Also, enable state locking to prevent two `terraform apply` runs from clashing.

- **Terraform Version Control**: Lock the Terraform provider versions (in Terraform 0.13+, use a `required_providers` block). This ensures consistency across machines running Terraform. Also, maintain the Terraform version (you might use a `required_version` constraint in configuration).

- **Plan Before Apply**: Always run `terraform plan` in CI or manually to review changes, especially for destructive changes. This is standard, but in automation ensure plan output is reviewed or approved if needed.

- **Immutability and Idempotency**: Treat containers and cloud resources as immutable where possible. If config changes (e.g., environment variables for App Service), Terraform will update the resource. Make sure your config doesn't cause unintended replacements. For example, changing the name of a resource in Terraform will destroy and create a new one, which might not be what you want in production without planning downtime or migration.

Now, let's start writing the Terraform script for our infrastructure.

### Writing Terraform Configuration for Azure Resources

We'll create Terraform files under `infra-terraform/` directory:

**1. Provider Configuration (main.tf)** – We need to set up Azure provider and backend for state:

```hcl
// main.tf
terraform {
  required_version = ">= 1.3.0"
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstoragename123"
    container_name       = "tfstate"
    key                  = "prod.tfstate"
  }
}

provider "azurerm" {
  features {}  # required block, can set provider features here
}
```

In the above:

- The `backend "azurerm"` block configures remote state. It assumes an Azure Storage account (with name `tfstoragename123`) in resource group `tfstate-rg` exists. We might need to create this storage manually or via CLI (as per Azure docs) to bootstrap state storage. This stores the `prod.tfstate` file in a blob container named `tfstate`. This configuration will prompt for Azure credentials (or use environment/CLI). Once configured, running `terraform init` will set up remote state.

- The provider block initializes the Azure RM provider. `features {}` is needed (even if empty) for azurerm provider 3.x. We could specify subscription_id here, but Terraform will pick up the Azure CLI logged-in subscription by default if not given.

**2. Variables Definition (variables.tf)** – Let's define some variables for flexibility:

```hcl
// variables.tf
variable "prefix" {
  description = "Prefix for naming Azure resources (to ensure uniqueness)"
  type        = string
  default     = "myapp"  // e.g., will name resources like myapp-web, myapp-db
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"  // choose a region
}

variable "spring_image_name" {
  description = "Docker image for Spring Boot app"
  type        = string
}

variable "react_image_name" {
  description = "Docker image for React app"
  type        = string
}

variable "spring_image_tag" {
  description = "Docker image tag for Spring Boot app"
  type        = string
  default     = "latest"
}

variable "react_image_tag" {
  description = "Docker image tag for React app"
  type        = string
  default     = "latest"
}

variable "db_admin_password" {
  description = "Database admin password"
  type        = string
    // In practice, don't put secrets in plain text. Use environment variables or Azure Key Vault.
}
```

We define variables for:

- `prefix` – to name resources (so they group together and are unique; you might include your team or project name).
- `location` – region, default to East US.
- Docker image names/tags – for the container images (likely we'll push to Azure Container Registry or Docker Hub, and specify the full image name including registry).
- `db_admin_password` – the password for the database admin (we'll create a database, e.g., Azure Database for MySQL or Postgres, and need a password). In real usage, you would not want this in plain text; you could supply it via `-var` at apply time or use Key Vault. For now, it's a variable with no default (ensures user provides it).

**3. Resource Definitions (main.tf continued)** – Now add resources to `main.tf` for each needed component:

- **Resource Group**: All resources will reside in an Azure Resource Group.
- **App Service Plan**: Defines the hosting plan (Linux plan for containers).
- **Web App (for Containers)**: The actual Azure Web App that will run our Docker container(s).
- **Database**: For example, Azure Database for MySQL (or Postgres) server and a database.
- **Container Registry**: If we plan to use Azure Container Registry (ACR) to host images, create one.
- **Key Vault**: (Optional) to store secrets like DB password instead of passing via config.
- **Networking**: Virtual Network and maybe subnets, if we want to integrate the Web App with a VNet or use private endpoints.

For our scenario, let's assume:

- We'll use Azure Database for MySQL.
- We'll use Azure Container Registry for our images (alternatively, you could use Docker Hub public images without an ACR).
- We'll integrate the App Service with the database securely (maybe via VNet or at least restrict DB firewall to the Azure Web App).
- We'll not set up a full VNet integration and private endpoint just yet (we'll cover in Networking chapter), but keep it in mind.

**Resource Group and Network:**

```hcl
resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-rg"
  location = var.location
}
```

This creates a resource group named "myapp-rg" (if prefix is "myapp").

If needed to create a Virtual Network (for advanced scenarios like private DB access):

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-vnet"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}
resource "azurerm_subnet" "appservice" {
  name                 = "appservice-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
  // Note: App Service cannot be injected into a subnet directly unless it's an App Service Environment or using VNet Integration. We'll cover integration later.
}
```

The above defines a VNet with a subnet. Standard multi-tenant App Service uses **VNet integration** for outbound traffic to talk to resources in the VNet ([Integrate your app with an Azure virtual network - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration#:~:text=This%20article%20describes%20the%20Azure,or%20through%20a%20virtual%20network)) ([Integrate your app with an Azure virtual network - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration#:~:text=Virtual%20network%20integration%20gives%20your,endpoint%20for%20inbound%20private%20access)). We'll use that later for the app to reach the database privately.

**Azure Container Registry (ACR)** (optional but recommended for private images):

```hcl
resource "azurerm_container_registry" "acr" {
  name                     = "${var.prefix}acr"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.location
  sku                      = "Basic"
  admin_enabled            = false  // we will use managed identity or service principal for access
}
```

This creates an ACR named "myappacr". `admin_enabled` false means the admin username/password is disabled; we'll use Azure AD-based access for pulling images (more secure).

After creating the images locally, you would push them to this ACR:

- Use `az acr login -n myappacr` to authenticate Docker to the registry.
- Tag images as `myappacr.azurecr.io/myreactapp:latest` and `myappacr.azurecr.io/myspringapp:latest`.
- Push with `docker push`.

However, one can also automate image building and pushing via CI, or even use Azure DevOps pipelines or GitHub Actions to build and push into ACR (we'll discuss CI/CD later). For Terraform, we just need the image name and ensure the Web App has permission to pull from ACR.

**Database (MySQL)**:

```hcl
resource "azurerm_mysql_flexible_server" "db" {
  name                = "${var.prefix}-mysql"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  administrator_login = "mysqladmin"
  administrator_password = var.db_admin_password
  version             = "8.0"
  storage_mb          = 32768  # 32 GB storage
  sku_name            = "Standard_B1ms"  # instance size
}

resource "azurerm_mysql_flexible_server_database" "db_name" {
  name                = "appdb"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.db.name
  charset             = "utf8"
  collation           = "utf8_general_ci"
}
```

We use Azure Database for MySQL Flexible Server (a newer option) for the database. We set an admin login and use the provided password variable. The flexible server can be deployed with or without VNet integration. We haven't specified `private_dns_zone_id` or `vnet_name`, so this will be a public endpoint DB by default. We'll secure it via firewall rules or private access soon.

**Database Firewall**: By default, the DB will block all connections. We need to allow the Azure Web App to connect:
Azure Web Apps from a given region have a set of outbound IP ranges. We could find and allow those (complex), or easier, allow all Azure services or a specific vNet if integrated. There's a setting `public_network_access_enabled` and firewall rules for flexible server:

```hcl
resource "azurerm_mysql_flexible_server_firewall_rule" "allow_azure" {
  name                = "AllowAzureServices"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.db.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
```

This special rule (0.0.0.0 to 0.0.0.0) allows all Azure services (including our App Service) to connect ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=)) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=Now%20let%20us%20add%20the,for%20your%20IP%20as%20well)). It's a shortcut but note it allows any resource in any Azure subscription to attempt to connect; a more secure approach would be using VNet integration and a private endpoint for the database (discussed in Networking chapter).

**App Service Plan and App Service**:

```hcl
resource "azurerm_app_service_plan" "plan" {
  name                = "${var.prefix}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  kind                = "Linux"
  reserved            = true             # needed for Linux
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "springapp" {
  name                = "${var.prefix}-spring"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  app_service_plan_id = azurerm_app_service_plan.plan.id

  site_config {
    linux_fx_version = "DOCKER|${var.spring_image_name}:${var.spring_image_tag}"
    # This tells App Service to pull a Linux container image.
    # For ACR images, use format: DOCKER|myappacr.azurecr.io/myspringapp:latest
  }

  app_settings = {
    WEBSITES_PORT = "8080"  # inform Azure which port the container listens on
    # If using ACR:
    # DOCKER_REGISTRY_SERVER_URL = azurerm_container_registry.acr.login_server
    # DOCKER_REGISTRY_SERVER_USERNAME = <leave empty if using managed identity>
    # DOCKER_REGISTRY_SERVER_PASSWORD = <leave empty if using managed identity>
  }

  identity {
    type = "SystemAssigned"
  }
}
```

This defines an App Service Plan (Linux Basic B1, which is cost-effective for dev/test; for production you might use Standard or higher for SLA and scaling). The `reserved = true` is required for Linux plans.

The **App Service (springapp)** is configured to use a Docker container via `linux_fx_version`. Azure uses the format `DOCKER|<image name>:<tag>`. If the image is on Docker Hub and public, you can just provide it (e.g., `DOCKER|mydockerhubuser/myspringapp:latest`). If using ACR, the `login_server` will be something like `myappacr.azurecr.io`; include that prefix.

We also set `WEBSITES_PORT` = 8080, because our Spring Boot container listens on 8080. Azure by default assumes port 80 for containers; if not set, it might not route traffic correctly. This app setting ensures the container's exposed port is used.

We enabled a **SystemAssigned Managed Identity** for the App Service. This identity can be used to grant the app permissions to other Azure resources (like pulling from ACR without credentials, or accessing Key Vault). For example, to allow this identity to pull from ACR, we would assign the role `AcrPull` on the ACR to this identity ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=,%2A%20Have%20Terraform%20installed)). Terraform can do that:

```hcl
resource "azurerm_role_assignment" "acr_pull" {
  principal_id         = azurerm_app_service.springapp.identity.principal_id
  principal_type       = "ServicePrincipal"
  role_definition_name = "AcrPull"
  scope                = azurerm_container_registry.acr.id
}
```

This grants the App Service's managed identity the rights to pull from our ACR (so we don't need to specify username/password for ACR in app settings).

We would similarly add an **App Service for React**:

```hcl
resource "azurerm_app_service" "reactapp" {
  name                = "${var.prefix}-react"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  app_service_plan_id = azurerm_app_service_plan.plan.id

  site_config {
    linux_fx_version = "DOCKER|${var.react_image_name}:${var.react_image_tag}"
  }
  app_settings = {
    WEBSITES_PORT = "80"  # Nginx serving on port 80 inside container
  }
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "acr_pull_react" {
  principal_id         = azurerm_app_service.reactapp.identity.principal_id
  principal_type       = "ServicePrincipal"
  role_definition_name = "AcrPull"
  scope                = azurerm_container_registry.acr.id
}
```

This creates a separate web app for the React frontend container. Alternatively, one could serve the React app static files via the Spring Boot app (as a single container), but we've separated them for clarity and scalability.

However, deploying two separate App Services for frontend and backend means they have different URLs (e.g., myapp-react.azurewebsites.net and myapp-spring.azurewebsites.net). You might integrate them under one domain later (perhaps using Azure Front Door or at least config the React app to call the Spring API via its URL or a relative path if same domain). For now, note the separation.

**Environment Configuration**: We should pass necessary environment variables to the containers. For the Spring app, it needs to know how to connect to the database. Instead of hardcoding in `application.properties`, use App Service settings (which become env vars in the container):

Add to `azurerm_app_service.springapp`:

```hcl
  app_settings = {
    WEBSITES_PORT = "8080"
    SPRING_DATASOURCE_URL      = "jdbc:mysql://${azurerm_mysql_flexible_server.db.host}:3306/appdb"
    SPRING_DATASOURCE_USERNAME = azurerm_mysql_flexible_server.db.administrator_login
    SPRING_DATASOURCE_PASSWORD = var.db_admin_password
    # If using Key Vault, we would fetch these differently; for now passing directly.
  }
```

This injects the DB URL and credentials into the Spring Boot container's environment. The Spring Boot app should be configured to read these (Spring Boot automatically reads SPRING*DATASOURCE*\* env vars as overrides).

Later, we'll improve this by using Key Vault and not exposing password in plain text. Also, note the `db.host` output from the MySQL resource gives the server hostname.

**Outputs (outputs.tf)**:

```hcl
output "spring_app_url" {
  description = "URL of the Spring Boot App Service"
  value       = azurerm_app_service.springapp.default_site_hostname
}
output "react_app_url" {
  value = azurerm_app_service.reactapp.default_site_hostname
}
```

This will output the hostnames of the deployed web apps (e.g., `myapp-spring.azurewebsites.net`). We use these to access the apps after deployment.

### Managing Terraform State

We configured remote state earlier with Azure storage backend. To use it, ensure the storage account and container exist. You can create them manually or via Azure CLI. For example:

```bash
az group create -n tfstate-rg -l eastus
az storage account create -g tfstate-rg -n tfstoragename123 -l eastus --sku Standard_LRS
az storage container create --account-name tfstoragename123 -n tfstate
```

And retrieve the storage key to set environment variables that Terraform will use for backend (or Terraform will prompt):

```bash
ACCOUNT_KEY=$(az storage account keys list -g tfstate-rg -n tfstoragename123 --query "[0].value" -o tsv)
export ARM_ACCESS_KEY=$ACCOUNT_KEY   # Terraform will use this for backend auth if set
```

Now run `terraform init` in the `infra-terraform` directory. It should initialize the backend and Azure provider. Then `terraform plan -var="spring_image_name=myappacr.azurecr.io/myspringapp" -var="react_image_name=myappacr.azurecr.io/myreactapp" -var="db_admin_password=<yourpassword>"` to see the changes. Review the plan output to ensure it matches expectations (resources to create, no deletions since nothing exists yet).

Finally, apply the changes with `terraform apply` (with the same vars or use a `terraform.tfvars` file). Terraform will prompt for confirmation. Type "yes" to proceed. It will then provision all resources on Azure. This could take a few minutes, especially the database server provisioning.

Once complete, Terraform will output the app URLs ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=match%20at%20L466%20Once%20the,only%20during%20the%20first%20request)) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=Once%20the%20deployment%20is%20complete%2C,only%20during%20the%20first%20request)). Copy those URLs. The first deployment might take a bit because the App Service will pull the Docker images (from ACR or Docker Hub). You can monitor progress in the Azure Portal -> the Web App -> "Containers" -> "Logs" or use `az webapp log tail`. After the container starts (you might experience a cold start delay), accessing the URL should show the React app and the Spring API should be accessible (you might test the Spring API via its URL or through the React UI if it calls it).

Terraform has now codified our infrastructure. From now on, changes to Azure resources should be done by editing the `.tf` files and running Terraform commands, not by clicking the Azure Portal. This ensures the state stays in sync and infrastructure changes are tracked.

---

## 5. Deploying to Azure Web Apps

With our applications containerized and Terraform configurations ready, it's time to deploy to Azure. In this chapter, we discuss how to push Docker images to a registry, how to use Terraform to deploy the infrastructure, and alternative/manual ways to deploy containers to Azure Web Apps. We will also cover using deployment slots for zero-downtime releases.

### Pushing Container Images to a Registry

Before the Azure Web Apps can run our containers, the images must be available in a container registry accessible to Azure. We have two main options:

- **Azure Container Registry (ACR)** – private, secure registry in Azure (recommended for production).
- **Docker Hub or other public registry** – easier for testing if public.

Assuming we created an ACR (`myappacr`), let's push our images there:

1. **Azure CLI login to ACR**:

   ```bash
   az acr login -n myappacr
   ```

   This logs in your local Docker client to the Azure registry.

2. **Tag images for ACR**:

   ```bash
   docker tag myreactapp:latest myappacr.azurecr.io/myreactapp:latest
   docker tag myspringapp:latest myappacr.azurecr.io/myspringapp:latest
   ```

   Replace `myappacr` with your registry name. Now we have tags pointing to ACR.

3. **Push images**:
   ```bash
   docker push myappacr.azurecr.io/myreactapp:latest
   docker push myappacr.azurecr.io/myspringapp:latest
   ```
   The images will upload to Azure. Verify in Azure Portal under the ACR repository list that `myreactapp` and `myspringapp` images appear.

Make sure your Terraform variables for image name include this registry (as we did via `spring_image_name` and `react_image_name`). The Azure App Service will pull from the registry. Since we set up Managed Identity and role assignment (AcrPull), the Web App can authenticate to ACR to pull the image without explicit credentials.

If you opt not to use ACR, you could push to Docker Hub and set the image name accordingly (and if private, you'd need to supply Docker Hub creds in the App Service's `app_settings` or use Azure Container Settings). However, using ACR with managed identity is more seamless in Azure.

### Deploying with Terraform (IaC Deployment)

We essentially covered this in the previous chapter by running `terraform apply`. To recap the process in a structured way:

- Ensure your Terraform configuration is updated with the final image names and any config changes (like correct database connection info).
- Initialize and plan Terraform:
  ```bash
  terraform init        # (if not done or switching backend)
  terraform plan -var="spring_image_name=..." -var="react_image_name=..." -var="db_admin_password=..."
  ```
- Apply Terraform to create resources:
  ```bash
  terraform apply -var="spring_image_name=..." ... (same vars)
  ```
- Confirm the apply. Terraform will provision:
  - Resource group, network (if any),
  - ACR (if part of config),
  - MySQL DB,
  - App Service Plan,
  - App Services for front and back, with configuration to pull the Docker images.

Terraform will output the application URLs. Visit the React app URL in a browser. If all went well, you should see your React app's content (it may be the default CRA output or your custom UI). The React app likely needs to communicate with the Spring Boot API. If it's expecting the API at a certain URL, ensure that is configured. Possibly you might have a reverse proxy or simply configure React to talk to the Spring app's URL (like setting an environment variable REACT_APP_API_URL to the Spring app URL at build time).

**Initial Load**: The first load might be slow due to cold start (the container image has to be pulled and the app started). Azure App Service will cache the image for subsequent restarts.

**Verification**: Use `az webapp log tail -n <app_name> -g <resource_group>` to stream logs from the App Service. Check for any errors, such as:

- Container couldn't start (maybe due to wrong port config or crashing app).
- App failing to connect to DB (check connection string correctness, firewall).
- ACR pull issues (if misconfigured identity or wrong image name).

If there's an issue:

- Use Azure Portal's Container Logs and Event Log under the Web App's "Log Stream" or "Container Settings" to troubleshoot.
- Adjust Terraform or application configs and re-apply if needed. Terraform will update in-place if possible. For example, changing an app setting will typically apply without recreating the site (it will restart the app though).

### Manual Deployment (Using Azure CLI / Portal)

While Terraform is our main method, it's useful to know how to deploy containers to Azure Web Apps manually, for quick tests or debugging:

- **Via Azure Portal**: You could create a Web App through the UI, selecting "Docker container" and specifying the image and registry. Azure Portal allows setting Continuous Deployment from ACR or Docker Hub as well. This is not IaC, but for one-off testing it’s straightforward.

- **Via Azure CLI**: The CLI command to create a container-based web app in one go is:

  ```bash
  az webapp create -g myapp-rg -p myapp-plan -n myapp-spring \
      -i myappacr.azurecr.io/myspringapp:latest --assign-identity
  ```

  The `-p` references an App Service plan (which you must create with `az appservice plan create` if not exists). The `-i` flag sets the container image. `--assign-identity` gives a managed identity to the app (like we did). You would then need `az webapp config appsettings set` to set WEBSITES_PORT and other settings, and `az role assignment create` to give AcrPull to the identity.

  CLI can also configure a deployment from Docker Hub:

  ```bash
  az webapp create -g myapp-rg -p myapp-plan -n myapp-spring \
      -i mydockerhubuser/myspringapp:latest
  ```

  But if it's a private image, you'd supply `--docker-registry-server-url`, `--docker-registry-server-user` and `--docker-registry-server-password`. We avoid that with ACR + identity.

- **Azure DevOps or GitHub Actions**: (This will be covered in CI/CD section, but note that those pipelines often use CLI or Terraform under the hood to deploy.)

Using Terraform for deployment is advantageous since it codifies everything, but in some debugging scenarios you might manually tweak something. Always be cautious: if you manually change a setting in Azure that is controlled by Terraform, the next Terraform apply may detect it as drift and attempt to change it back or flag it. It's fine to experiment manually, but incorporate fixes into Terraform config ultimately.

### Deployment Slots for Blue-Green Deployments

Azure App Service has a feature called **deployment slots** available in Standard and above tiers. Slots are like parallel environments (e.g., "staging" slot and the main "production" slot) for your web app that live under the same App Service. They allow you to deploy a new version to a staging slot, warm it up, then swap it with production with zero downtime ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=In%20order%20to%20use%20blue%2Fgreen,go%20through%20the%20new%20version)).

For a Blue-Green (a.k.a. swap) deployment strategy:

- Create a slot (say "staging") for your App Service (Terraform resource `azurerm_app_service_slot` can create one).
- Deploy new versions of containers to the "staging" slot (either via Terraform or CI pipeline).
- Run tests or warm up the app on staging (it has a separate URL like myapp-spring-staging.azurewebsites.net).
- When ready, **swap** the slots. Azure will take the staging slot and swap it into production, and vice versa. The swap is very quick (generally just DNS/path routing switch internally) and results in minimal downtime. Users start hitting the new version, and the old version is now in the "staging" slot (which you could keep as a backup temporarily).

Terraform can set up slots:

```hcl
resource "azurerm_app_service_slot" "springapp_staging" {
  name           = "staging"
  app_service_id = azurerm_app_service.springapp.id
  configuration_source = azurerm_app_service.springapp.id  # copy settings from production
  site_config {
    linux_fx_version = "DOCKER|myappacr.azurecr.io/myspringapp:${var.new_tag}"
  }
  app_settings = {
    WEBSITES_PORT = "8080"
    # ... any config overrides for staging if needed
  }
}
```

However, automating the swap is not directly in Terraform (Terraform sees both slots as resources it manages, but the act of swapping is an operational action). Instead, the swap is usually triggered via Azure CLI or in a CI pipeline:

```bash
az webapp deployment slot swap -g myapp-rg -n myapp-spring --slot staging --target-slot production
```

This swaps staging into production.

Blue-Green deployment ensures that if something goes wrong with the new version, you can swap back quickly (or just have minimal impact as you verify health before swapping). It eliminates downtime since the new code is fully running before users are directed to it ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=In%20order%20to%20use%20blue%2Fgreen,go%20through%20the%20new%20version)).

We will discuss CI/CD pipelines for automating blue-green in the next section. For now, remember that deployment slots are a powerful feature for production deployments on Azure Web Apps. If your tier is Basic (which has no slots), you might use a more manual Blue-Green by deploying a separate App Service as "green" and then switching DNS – but that’s more complex and beyond our immediate scope.

### Rollbacks

If a deployment introduces an issue, how do we rollback? Strategies:

- **Slot Swap Back**: If you used a slot, simply swap back to the old version, effectively rolling back instantaneously.
- **Redeploy Previous Image**: If using CI/CD with versioned images (not "latest" always), you can redeploy the last known good image tag. For example, push an image with tag `v1.0` and later `v1.1`. If `v1.1` fails, instruct the App Service (via Terraform or CLI) to use `v1.0` again. This requires that the old image is still available in registry.
- **Terraform state**: If the infrastructure change itself caused issues (less likely than app code issues), you could use `terraform rollback` concept by checking out previous Terraform code and applying, but Terraform doesn't have a single command "rollback"; you'd just apply the old config to converge back. In general, app rollbacks are handled at the app level (image versions) more so than tearing down infra.

For the remainder of this guide, we assume forward progress (rollouts), but always keep a rollback plan ready in production.

Now we have our applications running in Azure App Service containers. The next step is to integrate this into a CI/CD workflow so deployments and infrastructure changes can happen automatically, and to ensure our system is monitored and secure.

---

## 6. Networking and Security

Enterprise deployments require careful attention to networking and security. In this chapter, we cover how to configure Azure networking features (Virtual Networks, Private Endpoints) to secure communication between the app and other services (like databases), how to use Managed Identities and Azure Key Vault to handle secrets securely, and how to set up TLS/SSL and custom domains for your apps. We also touch on using Azure Firewall or other network security services if needed.

### Configuring Virtual Networks and Private Access

By default, Azure Web Apps run in a multi-tenant environment, and the apps have public endpoints. Our Spring Boot API and React app are publicly accessible via their azurewebsites.net URLs. The Spring Boot app also by default is connecting to a publicly accessible database endpoint (unless we locked it down). To enhance security, we can use Azure Virtual Network integration and Private Endpoints:

- **VNet Integration (Outbound)**: Azure Web Apps can be configured to integrate with a Virtual Network for outbound traffic ([Integrate your app with an Azure virtual network - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration#:~:text=This%20article%20describes%20the%20Azure,or%20through%20a%20virtual%20network)). This means the app can access resources in a VNet (like a database in a private subnet) as if it were inside that VNet. VNet integration is used for making calls from the app to secured services (it does _not_ mean the app is inbound accessible via the VNet; it's not hosting the app in the VNet, unless using an isolated App Service Environment). In Terraform, we could use `azurerm_app_service_virtual_network_swift_connection` or in the resource specify a `virtual_network_subnet_id` (depending on the Azure provider version). For example:

  ```hcl
  resource "azurerm_app_service_virtual_network_swift_connection" "conn" {
    app_service_id = azurerm_app_service.springapp.id
    subnet_id      = azurerm_subnet.appservice.id
  }
  ```

  This attaches the app to the subnet we created. Once done, the Spring Boot app's outbound traffic to the database can go through the VNet. We would then configure the MySQL Flexible Server to allow **private access** from that VNet instead of via public internet.

- **Private Endpoint (Inbound)**: To eliminate public exposure of the database and even the Web App, Azure supports Private Endpoints. A **Private Endpoint** for the database will assign the database a private IP in our VNet, so only resources in that VNet (or via peering/VPN) can reach it. Similarly, **Private Endpoints for Web App** allow clients in a VNet to access the web app over a private IP, and we can disable public internet access to the web app ([Using private endpoints for App Service apps - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-private-endpoint#:~:text=You%20can%20use%20a%20private,exposure%20from%20the%20public%20Internet)). However, note: Private endpoint for Web App covers inbound access to the app (from on-prem or VNet), but our web app is publicly serving general users, so we might not want to turn that off unless we front it with something like Azure Front Door.

For our architecture:

- We likely want a Private Endpoint for the MySQL database and restrict database access to the Web App only.
- We might not use a Private Endpoint for the Web App (because the React app is public), but if this were an internal application, that would be an option.

**Implementing Private Database Access**:
Azure MySQL Flexible server can be created with a VNet integration (called "Private access (VNet)"). In Terraform, that means specifying `vnet_name` and `subnet_id` in the flexible server resource. Alternatively, for Azure Single Server or other DBs, you can create a `azurerm_private_endpoint` resource linking to the DB resource.

Example for Private Endpoint on MySQL:

```hcl
resource "azurerm_private_endpoint" "mysql_pe" {
  name                = "${var.prefix}-mysql-pe"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.appservice.id  # or a separate subnet for endpoints

  private_service_connection {
    name                           = "mysqlconn"
    private_connection_resource_id = azurerm_mysql_flexible_server.db.id
    subresource_names              = ["mysqlServer"]  # depending on the service, check docs
    is_manual_connection           = false
  }
}
```

And a corresponding `azurerm_private_dns_zone` for MySQL (`privatelink.mysql.database.azure.com`) with an `azurerm_private_dns_zone_group`. This gets complex, but the result is the Spring App can connect to the DB via the private IP from the VNet, and we can set `public_network_access = false` on the MySQL server (disabling public internet access entirely).

**Private Endpoint for Web App**: If needed:

```hcl
resource "azurerm_private_endpoint" "webapp_pe" {
  name                = "${var.prefix}-web-pe"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.appservice.id

  private_service_connection {
    name                           = "webappconn"
    private_connection_resource_id = azurerm_app_service.springapp.id
    subresource_names              = ["sites"]
    is_manual_connection           = false
  }
}
```

We also create a DNS zone for `privatelink.azurewebsites.net` and link it, so internal DNS resolves the web app's hostname to the private IP. This way, if you had a jumpbox or on-prem network, they could hit the app privately. We could then set the web app's `public_network_access_enabled = false` (if supported) or use Access Restrictions to only allow certain sources.

However, if our app is public-facing to users, we typically keep the front door public (and secure it with HTTPS and maybe WAF as needed), but use private endpoints for backend resources.

### Securing Applications with Managed Identity and Key Vault

**Managed Identities** (MI) provide Azure AD identities for our app, eliminating the need for secrets in many cases ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)). We already created system-assigned MIs for the web apps. How to use them:

- **Database Access**: Currently, our Spring Boot uses username/password for the MySQL DB. Azure MySQL doesn't support Azure AD authentication for MySQL (as of now), so we had to use password. If it were an Azure SQL DB, we could use Managed Identity to fetch a token and connect without password. But for MySQL, we should at least not store the password in code or config. Instead, we can store it in Azure **Key Vault** and have the app retrieve it at startup via Managed Identity.

**Azure Key Vault** is a secure store for secrets, keys, and certificates ([Load a secret from Azure Key Vault in a Spring Boot application - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/configure-spring-boot-starter-java-app-with-azure-key-vault#:~:text=This%20tutorial%20shows%20you%20how,passwords%20and%20database%20connection%20strings)). We can use it to store the database connection string or password:

1. Create a Key Vault via Terraform or Portal:

   ```hcl
   resource "azurerm_key_vault" "vault" {
     name                = "${var.prefix}-vault"
     resource_group_name = azurerm_resource_group.main.name
     location            = var.location
     tenant_id           = data.azurerm_client_config.current.tenant_id
     sku_name            = "standard"
     soft_delete_enabled = true
   }
   resource "azurerm_key_vault_access_policy" "app_policy" {
     key_vault_id = azurerm_key_vault.vault.id
     tenant_id    = data.azurerm_client_config.current.tenant_id
     object_id    = azurerm_app_service.springapp.identity.principal_id
     secret_permissions = ["Get", "List"]
   }
   ```

   The above creates a vault and allows the app's managed identity to get secrets.

2. Add secrets to the vault (outside Terraform, or using `az keyvault secret set`). For instance:

   ```bash
   az keyvault secret set --vault-name myapp-vault -n DBPassword --value "<the-db-password>"
   ```

   Now the secret is stored securely.

3. In Spring Boot, use the Azure Key Vault Spring Boot starter or Azure SDK to retrieve the secret using the managed identity. Alternatively, you can inject it as environment variable via Azure Key Vault references (App Service can natively reference Key Vault secrets if identity has access). For example, in App Service configuration, set an app setting:

   - Name: `DB_PASSWORD`
   - Value: `@Microsoft.KeyVault(SecretUri=https://myapp-vault.vault.azure.net/secrets/DBPassword/)`

   With a managed identity assigned, Azure will resolve that reference to the secret value at runtime (this is a feature of App Service). Then Spring can read `DB_PASSWORD` env var. This way, the actual password never appears in our config or in Terraform state.

Managed Identity can also allow the Spring app to directly call Key Vault via SDK:
In your Spring Boot code, you could use Azure Identity library:

```java
TokenCredential credential = new DefaultAzureCredentialBuilder().build();
SecretClient client = new SecretClientBuilder()
    .vaultUrl("<https://myapp-vault.vault.azure.net>")
    .credential(credential)
    .buildClient();
String dbPassword = client.getSecret("DBPassword").getValue();
```

The DefaultAzureCredential will detect the Managed Identity in Azure and get a token for Key Vault. This avoids any stored keys.

**Benefits**: Using Managed Identity + Key Vault means no sensitive configuration (like DB passwords, API keys) are stored in code, docker images, or config files. They are fetched securely at runtime ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=With%20Azure%20Key%20Vault%2C%20developers,will%20explore%20how%20Azure%20Managed)) ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)). This significantly reduces the risk of secret leakage. It is a best practice for production.

- **Other uses of MI**: If your Spring Boot needed to call an Azure Storage or Azure Service Bus, it could use its MI to authenticate to those as well (no keys needed). Similarly, the React app could use Azure AD to authenticate users or call protected APIs, but that goes into identity management beyond our scope.

### Setting up SSL/TLS and Custom Domains

By default, our apps are accessible at `https://<appname>.azurewebsites.net`. Azure provides a wildcard certificate for `*.azurewebsites.net`, so this URL is already HTTPS. However, in production, you'll likely use a custom domain (e.g., `www.yourapp.com`) for the front-end, and maybe a subdomain like `api.yourapp.com` for the Spring API.

**Custom Domain Setup**:

1. Purchase/own a domain (e.g., via a registrar).
2. In Azure Portal or via CLI, map the custom domain to the Web App:
   - You need to create a CNAME or A record in your DNS pointing to the Azure app's default hostname.
   - Verify domain ownership (Azure provides a TXT record or can use an app service managed domain verification).
   - In Terraform, you can use `azurerm_app_service_custom_hostname_binding`.
     Example:
   ```hcl
   resource "azurerm_app_service_custom_hostname_binding" "frontend_domain" {
     hostname            = "www.yourapp.com"
     app_service_name    = azurerm_app_service.reactapp.name
     resource_group_name = azurerm_resource_group.main.name
   }
   ```
   After running, you'd still need to ensure the DNS CNAME from `www.yourapp.com` to `myapp-react.azurewebsites.net` is in place.

**TLS/SSL Certificate**:
To secure the custom domain, you need a certificate:

- Azure offers **App Service Managed Certificate**, a free certificate for custom domains (supports standard domains, not wildcard) ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=the%20custom%20domain%20with%20an,App%20Service%20managed%20certificate)). It's easy to enable: in Portal, there's "Add TLS/SSL Binding -> Create App Service Managed Certificate". Or in Terraform via `azurerm_app_service_managed_certificate` resource. Managed certs auto-renew and are free, but they have some limitations (no wildcard, and require the domain to be validated and in Basic or higher tier).
- Alternatively, use your own certificate from an authority or from Azure Key Vault.

Let's mention the managed cert approach as it’s straightforward:
Azure documentation states that the default \*.azurewebsites.net is already TLS-secured, but your custom domain needs its own certificate ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=The%20%60%3Capp,TLS%20certificate%20to%20App%20Service)). The managed cert is easiest: it's free and provides basic security for your custom domain ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=The%20%60%3Capp,TLS%20certificate%20to%20App%20Service)). In Terraform:

```hcl
resource "azurerm_app_service_managed_certificate" "frontend_cert" {
  custom_hostname_binding_id = azurerm_app_service_custom_hostname_binding.frontend_domain.id
}
resource "azurerm_app_service_certificate_binding" "frontend_cert_binding" {
  app_service_name = azurerm_app_service.reactapp.name
  resource_group_name = azurerm_resource_group.main.name
  certificate_id = azurerm_app_service_managed_certificate.frontend_cert.id
  hostname_binding_id = azurerm_app_service_custom_hostname_binding.frontend_domain.id
  ssl_state = "SniEnabled"
}
```

This issues a managed cert for "www.yourapp.com" and binds it. After a short while, your custom URL will be accessible via HTTPS with a valid cert.

For the API domain `api.yourapp.com`, similar steps.

**Enforcing HTTPS**: Always enforce HTTPS on your Web App (this is a setting in Azure; in Terraform, via `https_only = true` in the azurerm_app_service resource). This ensures HTTP is redirected to HTTPS.

**Azure Application Gateway / Front Door (Optional)**: If you needed a Web Application Firewall (WAF) or global load balancing, you might put an Azure Front Door or Application Gateway in front of your App Service. For example, Front Door can handle SSL, custom domains, caching, and WAF, then route to the backend App Service (even across regions). This is advanced and out of scope, but noteworthy if high security and global scale is needed.

### Azure Firewall and Network Security

Azure Firewall is a managed network firewall that can control egress and ingress traffic at the network level. In our design:

- Ingress (coming to web app) is mostly handled by App Service platform (which you can secure with access restrictions or WAF at a higher level).
- Egress (outgoing from web app) includes calls to the database and perhaps external APIs.

If using VNet integration, you could route all outbound traffic from the web app into a subnet, and then force that through an Azure Firewall (via user-defined routes). This would let you control or log what external services the app is calling. For example, you could restrict that the app can only call your database's private IP and perhaps Azure service endpoints, and not the public internet (to mitigate threats if the app is compromised, it can't call out to malicious hosts).

Implementing Azure Firewall:

- Create an Azure Firewall in a Hub network, set it as the next hop for internet-bound traffic of the app service subnet.
- Configure firewall rules to allow necessary traffic (to Azure MySQL, to Key Vault, etc.) and deny others.
- This is heavy for small deployments, but common in corporate environments.

Additionally, simpler network security:

- **Access Restrictions**: Azure App Service has an Access Restrictions feature to allow/deny requests by IP or service tag. For example, you could restrict that only a certain IP range can hit the Spring Boot API (if it was internal use). Or restrict the Azure Portal SCM (Kudu) site to certain IPs. This can be done in Terraform via `azurerm_app_service_active_slot` or older `azurerm_app_service` settings.

- **CORS**: If the React app domain is different from the API domain, ensure you configure CORS on the API (either in Spring Boot via annotations/config or using App Service CORS setting). Only allow the known front-end domain in production to call the API.

- **Azure Front Door/Azure CDN**: If using these, ensure proper HTTPS and WAF policies are applied.

### Summary of Security Best Practices:

By implementing the above:

- The database is not exposed to the internet, only accessible via private network ([Using private endpoints for App Service apps - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-private-endpoint#:~:text=You%20can%20use%20a%20private,exposure%20from%20the%20public%20Internet)).
- Secrets (like DB password) are not in code or config, they're in Key Vault and accessed with managed identities ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)).
- The Web App uses HTTPS with custom domain and managed cert (no manual cert handling, and no plaintext HTTP for users) ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=The%20%60%3Capp,TLS%20certificate%20to%20App%20Service)).
- Optionally, the web app’s inbound access can be restricted or monitored if needed (WAF, Firewall).
- The containers run as non-root and images are regularly scanned.
- Managed Identity also avoids storing any cloud credentials (for example, if the app needed to access Azure Storage, it could use MI rather than storing an access key).

Networking and security are crucial for a production-ready solution. It’s better to design these in from the start, but Terraform makes it easier to add on later as well, since changes can be applied incrementally.

---

## 7. CI/CD Integration

Manual deployment is not sustainable for rapid iterations. In this chapter, we'll integrate our setup into a Continuous Integration and Continuous Deployment (CI/CD) pipeline. This will automate building the applications, creating Docker images, pushing to registry, running Terraform to update infrastructure, and deploying new versions to Azure – all triggered by code changes. We will explore using **GitHub Actions** as well as **Azure DevOps Pipelines** as examples. We also discuss implementing Blue-Green deployments in the pipeline and automated rollbacks.

### Overview of CI/CD Pipeline

A robust CI/CD pipeline for our scenario might look like:

1. **Continuous Integration (CI)**: Trigger on code push (e.g., to main branch or a PR merge). Build the React app and Spring Boot app, run tests, then build Docker images for each. Possibly scan images for vulnerabilities. Then push images to ACR with a new version tag (like a short commit SHA or version number).
2. **Continuous Deployment (CD)**: After images are pushed, update infrastructure if needed (Terraform apply) and deploy the new version to Azure. If using blue-green, deploy to staging slot first, run smoke tests, then swap to production.
3. **Rollback Mechanism**: If deployment fails or tests fail, stop and optionally rollback (swap back or redeploy previous images).
4. **Infra Changes**: If the commit included changes to Terraform config (e.g., scale changes, new resources), pipeline should run Terraform to apply those as well, in sync with app deployment.

Automation ensures consistency and reduces manual errors, enabling frequent deployments.

### Using GitHub Actions for CI/CD

GitHub Actions can orchestrate the pipeline with YAML workflow files in your repo (e.g., `.github/workflows/deploy.yml`). Let's outline a possible GitHub Actions workflow:

````yaml
name: CI-CD

on:
  push:
    branches: [ main ]  # trigger on pushes to main (or use pull_request for PR validation separately)

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Set up Node
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Build Spring Boot Jar
      working-directory: backend-spring/spring-backend
      run: ./mvnw clean package -DskipTests

    - name: Build React app
      working-directory: frontend-react/my-react-app
      run: npm ci && npm run build

    - name: Build Docker images
      run: |
        docker build -t myappacr.azurecr.io/myspringapp:${{ github.sha }} backend-spring/spring-backend
        docker build -t myappacr.azurecr.io/myreactapp:${{ github.sha }} frontend-react/my-react-app
    - name: Azure Login (for Azure CLI and ACR auth)
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
        enable-AzPSSession: false

    - name: Push images to ACR
      run: |
        az acr login --name myappacr
        docker push myappacr.azurecr.io/myspringapp:${{ github.sha }}
        docker push myappacr.azurecr.io/myreactapp:${{ github.sha }}

    - name: Terraform Init
      working-directory: infra-terraform
      run: terraform init
      env:
        ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
        ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
        ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
        ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}

    - name: Terraform Apply
      working-directory: infra-terraform
      run: terraform apply -auto-approve -var="spring_image_name=myappacr.azurecr.io/myspringapp" -var="spring_image_tag=${{ github.sha }}" -var="react_image_name=myappacr.azurecr.io/myreactapp" -var="react_image_tag=${{ github.sha }}" -var="db_admin_password=${{ secrets.DB_PASSWORD }}"
      env:
        ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
        ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
        ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
        ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}

    # Optionally, add steps to hit the health check endpoint or run tests on the deployed app
    - name: Run smoke tests
      run: curl -f https://api.yourapp.com/health || exit 1

    ```
Explanation:
- We trigger on push to main branch.
- We set up Java and Node environments.
- Build the backend and frontend.
- Build Docker images and tag them with the commit SHA (ensuring uniqueness for each version).
- Use `azure/login` GitHub Action to authenticate to Azure. We need to create an Azure Service Principal for GitHub and store JSON creds in `AZURE_CREDENTIALS` secret. Alternatively, use OIDC federation for passwordless auth.
- Push the images to ACR.
- Run Terraform: We export the Azure SP credentials for Terraform (or use Azure CLI auth, but using SP ensures pipeline independence). We call `terraform apply` with `-auto-approve` for non-interactive. We pass the new image names with tags as variables so that Terraform updates the App Service to the new container tags. We also pass the DB password (fetched from secrets store).
- After apply, the new containers are deployed. We then optionally run a smoke test (here a simple curl to a health endpoint) to ensure the app is running. If this fails, the action can be set to mark failure (which can trigger a rollback or alert).

**Storing Secrets**: `AZURE_CREDENTIALS` would contain JSON from `az ad sp create-for-rbac` output. `DB_PASSWORD` secret holds the database password. These secrets are stored in GitHub and accessed securely in the workflow.

**Blue-Green with Actions**: If we wanted to use deployment slots:
- Our Terraform could always deploy new image to the "staging" slot (by setting `spring_image_tag` on the slot resource for example).
- After Terraform apply, we would run tests on the staging slot URL.
- If tests pass, we then run Azure CLI to swap slots:
  ```yaml
    - name: Swap slots
      run: az webapp deployment slot swap -g myapp-rg -n myapp-spring --slot staging --target-slot production
````

- If tests fail, we abort and do not swap, leaving production untouched (and possibly notify developers).
- Rolling back a bad deployment would be as simple as not swapping (the new version never goes live), or if it already swapped and we detected an issue, swap back.

This approach gives zero downtime deployments with validation.

**Note**: Using Terraform with slots needs caution – if Terraform is not aware of the slot swap (which changes settings behind the scenes), next run might be confused. One strategy is to use separate Terraform runs for infrastructure vs slot content, or use Azure CLI for the swap exclusively. Some teams manage slot content outside of Terraform to avoid that state complexity.

### Using Azure DevOps Pipelines

Azure DevOps offers pipelines (YAML or classic) that similarly execute build and deploy steps. The principles are the same:

- Use tasks like `Maven` or `npm` for build,
- `Docker` tasks to build and push images,
- `AzureCLI` or Terraform tasks to deploy.

For example, Piotr's TechBlog described using Azure Pipelines to build and then deploy to Azure Spring Apps with approvals ([Azure DevOps and Terraform for Spring Boot - Piotr's TechBlog](https://piotrminkowski.com/2024/01/03/azure-devops-and-terraform-for-spring-boot/#:~:text=,artifact%20in%20the%20next%20stage)). In our case, an Azure Pipeline YAML might look like:

```yaml
trigger:
  - main

variables:
  imageTag: $(Build.BuildId) # use build ID or use source version

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        pool:
          vmImage: ubuntu-latest
        steps:
          - checkout: self
          - task: Maven@3
            inputs:
              mavenPomFile: "backend-spring/spring-backend/pom.xml"
              goals: "package -DskipTests"
          - script: |
              cd frontend-react/my-react-app
              npm ci
              npm run build
            displayName: "Build React app"
          - task: Docker@2
            displayName: "Build and push images"
            inputs:
              containerRegistry: "myACRServiceConnection" # ACR connection in Azure DevOps
              repository: "myappacr.azurecr.io/myspringapp"
              command: "buildAndPush"
              Dockerfile: "backend-spring/spring-backend/Dockerfile"
              tags: "$(imageTag)"
          - task: Docker@2
            displayName: "Build and push frontend image"
            inputs:
              containerRegistry: "myACRServiceConnection"
              repository: "myappacr.azurecr.io/myreactapp"
              command: "buildAndPush"
              Dockerfile: "frontend-react/my-react-app/Dockerfile"
              tags: "$(imageTag)"

  - stage: Deploy
    dependsOn: Build
    jobs:
      - deployment: DeployInfra
        environment: staging # use an environment for approvals if needed
        pool:
          vmImage: ubuntu-latest
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: "MyAzureSPN" # Service connection for SP
                    scriptType: bash
                    scriptLocation: inlineScript
                    inlineScript: |
                      cd infra-terraform
                      terraform init
                      terraform apply -auto-approve \
                        -var "spring_image_name=myappacr.azurecr.io/myspringapp" \
                        -var "spring_image_tag=$(imageTag)" \
                        -var "react_image_name=myappacr.azurecr.io/myreactapp" \
                        -var "react_image_tag=$(imageTag)" \
                        -var "db_admin_password=$(DB_PASSWORD)"
                  env:
                    ARM_CLIENT_ID: $(ARM_CLIENT_ID)
                    ARM_CLIENT_SECRET: $(ARM_CLIENT_SECRET)
                    ARM_TENANT_ID: $(ARM_TENANT_ID)
                    ARM_SUBSCRIPTION_ID: $(ARM_SUBSCRIPTION_ID)
                - script: "curl -f https://myapp-spring-staging.azurewebsites.net/health"
                  displayName: "Health check on staging"
                - task: AzureCLI@2
                  displayName: "Swap slots"
                  inputs:
                    azureSubscription: "MyAzureSPN"
                    scriptType: bash
                    scriptLocation: inlineScript
                    inlineScript: |
                      az webapp deployment slot swap -g myapp-rg -n myapp-spring --slot staging --target-slot production
```

This Azure DevOps pipeline is analogous to the GitHub Actions one:

- It builds the images and pushes to ACR (using a Docker task that requires an ACR service connection).
- It then runs Terraform via an AzureCLI task (with service principal creds from a secure file or pipeline variables).
- It checks health, then swaps slots.

Azure DevOps adds features like **Environments** where you can require manual approval before deploying to production, as mentioned by Piotr ([Azure DevOps and Terraform for Spring Boot - Piotr's TechBlog](https://piotrminkowski.com/2024/01/03/azure-devops-and-terraform-for-spring-boot/#:~:text=The%20next%20Deploy_Stage%20stage%20,the%20Azure%20Spring%20Apps%20service)) – e.g., an approval gate before executing the Deploy stage. This can enforce that a team lead reviews the plan or tests results before final swap.

### Blue-Green Deployments and Rollbacks in CI/CD

We've essentially integrated Blue-Green (slot swap) into the pipeline as above. Key things to ensure:

- The pipeline should clearly separate deploying to staging vs swapping to production. Possibly use separate stages (one for staging deploy, one for production swap) with an approval in between.
- Monitor the staging slot after deployment. You can run smoke tests or even short load tests.
- If any test fails, **do not swap**. Fail the pipeline and alert. The production slot remains with old version (blue) untouched. Developers can fix and redeploy.
- If everything passes, swap to make the new version live (green becomes blue).
- If after going live an issue is detected (maybe by an alert or user report), you can swap back manually or via a pipeline task.

Rollbacks can also be handled by maintaining previous image tags:

- For example, always tag images with version numbers and keep last N deployments tags. If needed, run a pipeline that redeploys the last known good tag (by setting Terraform variables to that tag or using `az webapp config container set` to point to older image).
- With slots, swapping back is fastest approach to rollback code. It’s good to keep the old version in a slot until you're confident in new version.

### Terraform in CI/CD

One challenge: Terraform state. If multiple developers or the pipeline run Terraform, they use the same remote state, which is good to avoid conflicts. But ensure only one apply runs at a time. State locking via the backend will serialize, but you don't want two pipelines colliding. It may be wise to have one pipeline responsible for Terraform (like an "infra" pipeline) and another for app deployment. However, combining as above is convenient for app version updates.

As best practice, use the pipeline to run `terraform plan` and maybe output it for review if it's making infra changes, and possibly require a manual approval if resources are being destroyed, etc. For purely changing image tags, it's low risk.

Also store your Terraform files in source control and protect them (review changes via PR). This prevents unauthorized or accidental infra modifications.

### Summary of CI/CD Benefits

Automating build and deployment:

- Reduces time to deploy new features (push code, pipeline does the rest).
- Ensures consistency (the same build process every time).
- Integrates tests and checks to catch issues before users see them ([Deploy to Azure with IaC and GitHub Actions - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/devops/deliver/iac-github-actions#:~:text=1,changes%20using%20your%20IaC%20provider)).
- Enables rapid rollback or roll-forward.
- Facilitates team collaboration (everyone merges to main and pipeline delivers).

By implementing GitHub Actions or Azure Pipelines, our full-stack application is now continuously delivered to Azure in a safe and repeatable manner. The next step is to ensure we have proper monitoring and logging to maintain the application in production.

---

## 8. Monitoring and Logging

Once your application is running in Azure, you need visibility into its behavior. In this chapter, we'll cover setting up monitoring for both the React front-end and Spring Boot back-end using Azure Application Insights and Log Analytics. We'll discuss capturing logs, metrics, and traces, setting up alerts for issues, and techniques for debugging common deployment problems through logs and diagnostic tools.

### Azure Application Insights (APM - Application Performance Monitoring)

**Application Insights** is an Azure service that provides performance monitoring, exception tracking, and telemetry for your applications. It can be integrated with Spring Boot and also used to track front-end metrics.

For **Spring Boot**:

- Microsoft provides an Application Insights Java agent and Spring starters that make integration straightforward. By attaching the Application Insights agent to the JVM, you can collect telemetry on incoming HTTP requests, outgoing dependencies (like database calls), exceptions, and custom logs, without code changes ([Configure Azure Monitor Application Insights for Spring Boot - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-spring-boot#:~:text=There%20are%20two%20options%20for,JVM%29%20argument%20and%20programmatically)).
- Alternatively, use the Spring Boot starter `applicationinsights-spring-boot-starter` which auto-configures telemetry.

**How to enable for Spring Boot**:

1. Create an Application Insights resource in Azure (this can be done via Terraform, `azurerm_application_insights`).
2. Note the Instrumentation Key or Connection String of the App Insights resource.
3. There are two options:

   - **Agent**: In the Docker container, include the Application Insights Java agent JAR and set `-javaagent` JVM arg on startup ([Configure Azure Monitor Application Insights for Spring Boot - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-spring-boot#:~:text=Enabling%20with%20JVM%20argument)). For example, modify the Dockerfile to add:
     ```Dockerfile
     RUN curl -sSL -o applicationinsights-agent.jar https://github.com/microsoft/ApplicationInsights-Java/releases/download/3.4.8/applicationinsights-agent-3.4.8.jar
     # (Use the latest version available)
     ```
     and then in the entrypoint, change:
     ```Dockerfile
     ENTRYPOINT ["java","-javaagent:/app/applicationinsights-agent.jar","-jar","/app/app.jar"]
     ```
     Also, provide the connection string as an environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING` in the App Service settings (or instrumentation key via `APPINSIGHTS_INSTRUMENTATIONKEY`). The agent will pick it up and send data to Application Insights.
   - **SDK (Manual)**: Add dependency `com.microsoft.azure:applicationinsights-spring-boot-starter` and configure the key. The starter will send metrics. This requires code or at least config changes but is more flexible to customize. The agent approach is simpler to add post-deployment.

4. Once enabled, you'll start seeing data in Azure Portal under Application Insights: server requests, response times, dependency call durations (e.g., how long queries to MySQL took), exceptions stack traces, logs, etc. You can use **Application Map** to see topology, and **Profiler** or **Snapshot Debugger** for in-depth analysis if needed.

For **React front-end**:

- Application Insights has a JavaScript SDK that can track page views, AJAX calls, and custom events in the browser. You can include it in your React app (npm package `@microsoft/applicationinsights-web`). Initialize it with the same instrumentation key (but typically you'd use a separate App Insights resource for front-end vs back-end, or at least separate "application" within App Insights).
- For instance, integrate in React index.js:
  ```js
  import { ApplicationInsights } from "@microsoft/applicationinsights-web";
  const appInsights = new ApplicationInsights({
    config: {
      connectionString: "<your-connection-string>",
      enableAutoRouteTracking: true,
    },
  });
  appInsights.loadAppInsights();
  appInsights.trackPageView();
  ```
  This will report page loads, and you can use `appInsights.trackEvent({name: 'something'})` for custom events.

This front-end telemetry will show user behavior, page load times, and any JS errors if tracked.

### Azure Log Analytics and Container Logs

**Log Analytics** is a service where logs from various sources can be aggregated and queried using Kusto Query Language (KQL). Application Insights actually uses a Log Analytics workspace under the hood (for newer resources or when configured).

For our container logs:

- Azure App Service by default captures stdout and stderr from the container and can send them to Application Insights as "Trace" logs or to a Log Analytics workspace via Diagnostic Settings. If using the App Insights agent, it might automatically capture console logs as traces ([Container Logs be ingested into Azure Application Insights?](https://stackoverflow.com/questions/74509678/can-web-app-for-containers-container-logs-be-ingested-into-azure-application-i#:~:text=Container%20Logs%20be%20ingested%20into,send%20them%20to%20Azure%20Monitor)).
- Alternatively, enable **Container diagnostics**: in App Service, you can enable logging to filesystem (not ideal for long term), or enable **Azure Monitor** integration. It's better to route logs to Application Insights or a Log Analytics workspace.

To set up via Terraform, you can use `azurerm_monitor_diagnostic_setting` on the App Service to send logs and metrics to a Log Analytics workspace:

```hcl
resource "azurerm_log_analytics_workspace" "log" {
  name                = "${var.prefix}-logs"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "PerGB2018"
}

resource "azurerm_monitor_diagnostic_setting" "appservice_diagnostics" {
  name               = "${var.prefix}-appservice-diag"
  target_resource_id = azurerm_app_service.springapp.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log.id

  logs {
    category = "AppServiceAppLogs"
    enabled = true
    retention_policy { enabled = false }
  }
  logs {
    category = "AppServiceConsoleLogs"
    enabled = true
    retention_policy { enabled = false }
  }
  metrics {
    category = "AllMetrics"
    enabled = true
    retention_policy { enabled = false }
  }
}
```

This will send application logs and console logs to the workspace. In Azure Portal, you can then run queries to see log entries. Alternatively, if using App Insights for everything, you might skip a separate workspace and rely on App Insights (since App Insights provides search and analytics too).

**Viewing Logs**:

- In Application Insights, under "Logs", you can query tables like `requests` (for HTTP requests), `dependencies` (for DB calls), `exceptions`, and `traces` (for custom logs or console output).
- Example KQL query:
  ```kql
  traces
  | where message contains "ERROR"
  | order by timestamp desc
  ```
  This would list error messages from logs.
- `requests | summarize avg(duration), count() by success` could show average request durations and count of successes vs failures.

**Setting up Alerts and Dashboards**:

- Azure Monitor allows creating alerts on metrics or log query results. For example, an alert if the Spring Boot app has more than 5 failed requests in 5 minutes, or if the response time goes above 2 seconds on average.
- Metric-based alert: CPU percentage on the App Service > 80% for 10 minutes -> trigger scale-out or notify team.
- Log-based alert: if exceptions table has > 0 entries in last 5 minutes -> trigger an email/Teams/Slack.
- You can configure alerts via Azure Portal or Terraform (using `azurerm_monitor_metric_alert` or `azurerm_monitor_scheduled_query_rules_alert` for log alerts).

Dashboards or Azure Monitor **Workbooks** can be used to create a visual dashboard of key metrics (requests per second, error rate, CPU, memory, DB DTU utilization, etc.).

**Common Monitoring Setup for Spring Boot**:
Using **Spring Actuator** metrics with App Insights: If Spring Boot Actuator is on, it can expose metrics. These might not automatically flow to App Insights, but you could push them to Azure Monitor via Micrometer (Azure Monitor exporter). This is advanced usage; often the App Insights agent covers basic performance metrics, and for custom app metrics, one could send custom telemetry.

### Debugging Common Deployment Issues

Even with monitoring, you'll occasionally face issues in deployment. Here are some common issues and how to debug them:

- **Container fails to start**: In Azure, if the container can't start, the Web App will show in the "Container Settings" an error log. Use `az webapp log tail` to see logs in real-time. Common causes:

  - Wrong port exposed (fix by setting WEBSITES_PORT correctly).
  - CrashLoop due to missing environment variable (e.g., app expecting a config that's not provided).
  - Image pull failure (check that image name/tag exists in ACR and that the identity has AcrPull rights).
  - Check App Service **"Events"** in portal for any pull/start errors.

- **App running but API not reachable**: Possibly CORS issues (browser blocking calls). Check browser dev console for CORS errors. Solve by enabling proper CORS config in Spring Boot (allowed origins) or API Management.
  Possibly network issues if using VNet integration and something misconfigured.
- **High latency or timeouts**: Check Application Insights "performance" to see if certain requests are slow or failing. Could be DB queries slow – check the dependencies telemetry to see query durations. If the database is slow, consider scaling DB or adding an index, etc.
- **Memory/CPU issues**: If the app is consuming too much memory, it might get restarted by Azure (App Service will restart containers if they crash or OOM). Monitor memory usage in App Insights (if agent collects it) or Log Analytics metrics. If out-of-memory, maybe increase the App Service Plan size or optimize the app's memory use (e.g., reduce caching in memory, etc.). CPU bound – consider a higher SKU or enabling autoscale.

- **Logging**: If you don't see logs you expect, ensure logging is properly configured:

  - Spring Boot default logs to console – which should appear in Azure logs. If using a specific logging framework, ensure console output is enabled or log to Application Insights via its appender.
  - Client-side, use App Insights JS to track errors or use browser console. Those won't appear in server logs by default.

- **Terraform errors**: If pipeline fails at Terraform:

  - See the error message. Common ones: A resource conflict (e.g., trying to create something that already exists due to name conflict) – adjust naming. Or Azure API issues.
  - State lock issues – ensure previous Terraform runs finished or manually unlock if stuck (terraform force-unlock).
  - Authentication issues – ensure service principal has adequate permissions to create all resources (e.g., if it lacks permission to create a Key Vault or assign a role, that needs to be granted).
  - Syntax or version issues – run `terraform validate` locally to catch mistakes.

- **Cost spikes or anomalies**: Use Azure Cost alerts and check if any resource is consuming more than expected (e.g., someone left app on higher tier). We'll discuss cost in next section.

For systematic debugging:

- Enable **Application Insights Snapshot Debugging** to capture stack traces of exceptions in Spring Boot.
- Use **App Service Diagnostics** (in Azure Portal) – there's a troubleshooting section that can auto-detect issues like "Out of Memory", "High CPU", etc., and give recommendations.
- The "Diagnose and solve problems" blade on App Service is quite helpful for pinpointing issues.

Setting up thorough monitoring and logging will help you maintain the app effectively. You will be notified of issues and have the data needed to resolve them quickly.

---

## 9. Scaling and Performance Optimization

A critical aspect of running applications in production is ensuring they can scale to meet demand and are optimized for performance. In this chapter, we discuss how to configure autoscaling for Azure Web Apps, how to fine-tune performance for both React and Spring Boot, and how to leverage caching (Azure Redis, CDNs) to improve responsiveness and throughput.

### Configuring Autoscaling for Azure Web Apps

**Scaling Options**:

- **Scale Up**: Move to a higher pricing tier or larger instance size (more CPU/RAM per instance).
- **Scale Out**: Increase the number of instances of the App Service (i.e., run multiple container instances behind a load balancer).

Azure App Service in Basic tier does not support autoscale (you can manually scale out), but Standard and above do. Also, Azure introduced **Automatic Scaling** in 2023 for certain tiers where it scales based on HTTP load without custom rules ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=Automatic%20scaling%20is%20a%20new,every%20instance%2C%20including%20prewarmed%20instances)).

To enable classic autoscaling:

- Use Azure Monitor autoscale rules. For example: if CPU > 70% for 5 minutes, add 1 instance (scale out), if CPU < 30% for 10 minutes, remove 1 instance (scale in). Also define min and max instances.
- In Terraform, use `azurerm_monitor_autoscale_setting` to define these rules.

Example:

```hcl
resource "azurerm_monitor_autoscale_setting" "autoscale" {
  name                = "${var.prefix}-autoscale"
  resource_group_name = azurerm_resource_group.main.name
  target_resource_id  = azurerm_app_service_plan.plan.id

  max_capacity = 5
  min_capacity = 1
  default_capacity = 1

  notification {
    email {
      send_to_subscription_administrator = true
    }
    # Could also webhook or other notifications
  }

  profile {
    name = "AutoScaleProfile"
    capacity {
      minimum = 1
      maximum = 5
      default = 1
    }
    rule {
      metric_trigger {
        metric_name = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.plan.id
        time_grain = "PT1M"
        statistic = "Average"
        time_window = "PT5M"
        time_aggregation = "Average"
        operator = "GreaterThan"
        threshold = 70
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
        metric_name = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.plan.id
        time_grain = "PT5M"
        statistic = "Average"
        time_window = "PT10M"
        time_aggregation = "Average"
        operator = "LessThan"
        threshold = 30
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

This set of rules will scale between 1 and 5 instances based on CPU usage.

Azure's new **Automatic Scaling** mode (for Premium plans) can manage scaling by itself based on HTTP queue length and loads, without rules ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=How%20automatic%20scaling%20works)). You simply specify a max, and Azure handles it. This can be enabled via CLI (`az appservice plan update --elastic-scale`) or possibly via Terraform (new property on app service plan). Automatic scaling pre-warms instances to avoid cold start when scaling ([How to enable automatic scaling - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/manage-automatic-scaling#:~:text=existing%20Azure%20autoscale%2C%20which%20lets,every%20instance%2C%20including%20prewarmed%20instances)), which is beneficial for sudden traffic spikes.

**Scale Up/Down**: If your app needs more memory or CPU per instance, you might scale up to a larger instance (like from P1v2 to P2v2). This often requires a manual or scripted action, as autoscale deals with count not size (though Azure can do scheduled scale-up/down, e.g., scale up during business hours, down at night via schedules in autoscale settings).

Ensure you choose a tier that supports your needs:

- For example, if you need VNet integration or more storage or higher connections, some features (like VNet integration, private endpoints) require Standard or Premium.
- If you need staging slots (blue-green), Standard allows 5 slots.

**Spring Boot Specific**: If the Spring Boot app experiences heavy load (many concurrent requests), having multiple instances will allow parallel processing. Spring Boot is stateless (if not storing in-memory session without sticky sessions), so scaling horizontally is fine. If you use HTTP sessions and want to load-balance without sticky sessions, consider enabling a distributed session store (like Spring Session with Redis).

**React App**: It's static content served by Nginx, which usually can handle many requests with low CPU. But if heavy traffic, scaling out the front-end container is also useful (though often using a CDN is more cost-effective to offload static content).

### Performance Tuning for React

React app performance is mostly about client-side optimization:

- **Production Build**: Always deploy the production build (which we did). The minified code is smaller and faster. React in production mode avoids extra runtime checks, improving speed ([Optimizing Performance - React](https://legacy.reactjs.org/docs/optimizing-performance.html#:~:text=If%20you%27re%20benchmarking%20or%20experiencing,with%20the%20minified%20production%20build)).
- **Code Splitting**: Use React's lazy loading or dynamic imports to split your JS bundle. This ensures not all code loads at once, speeding up initial load. For example, split out large libraries or rarely used parts of the app.
- **Caching**: Ensure that static assets (JS/CSS) are cached by the browser. By default, Create React App output has hashes in filenames (like `main.abcd1234.js`), so you can set long cache expiration on these files because their names change when content changes. The Nginx config can include:
  ```
  location / {
    try_files $uri $uri/ /index.html =404;
  }
  location ~* \.(js|css|png|jpg|ico)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
  }
  ```
  This caches static files for 30 days.
- **Compression**: Enable gzip or Brotli compression for assets. In Nginx, you can enable gzip compression on responses, which will compress the static files sent to clients, reducing bandwidth and load time.
- **Use CDN**: Offload delivery of static assets to a CDN (Content Delivery Network) like Azure CDN or Cloudflare. Azure CDN can be easily connected to an App Service (or directly to a storage account if you host static files there). CDN will cache files at edge locations globally, making access faster for geographically distributed users. To use Azure CDN: create a CDN endpoint and point origin to your Web App (hostname). Then serve static content via the CDN domain (or custom domain on CDN). This reduces load on your App Service and improves latency.
- **Images and Fonts**: Optimize images (use correct sizes, maybe serve WebP format for browsers that support it). Use lazy loading for images below the fold.
- **Profiling**: Use React Developer Tools profiler on a sample of your app to find slow components, excessive re-renders, or memory leaks. In production, these are less visible, but if the UI is sluggish, often it's a front-end code issue to fix (not Azure's concern).

### Performance Tuning for Spring Boot

Spring Boot, being on the server side, has multiple areas to optimize:

- **Database interactions**: Ensure your queries are efficient (check for N+1 query problems if using JPA/Hibernate). Use indexes on DB for frequent queries. Monitor DB metrics (Azure MySQL has performance recommendations).
- **Connection Pooling**: The default HikariCP should be fine, but ensure max pool size is sufficient to handle parallel requests under load (and not too high to overload DB). Typically, set pool size equal to expected concurrent DB connections needed.
- **Caching**: Use caching for expensive operations. Spring Boot with Spring Cache can cache results of methods. You might use an in-memory cache for small data or a distributed cache (Redis) for larger scale or sharing across instances. Azure Cache for Redis is a managed service that can store frequently used data (like results of costly DB queries, session data, etc.). For example, if the React app needs certain reference data, the Spring Boot could cache that from DB to Redis. This reduces DB load and speeds up responses.
- **Async/Non-blocking**: Consider if parts of the app can be made asynchronous or use reactive programming (Spring WebFlux) for high throughput especially when handling many I/O bound requests. WebFlux can handle more concurrent connections with fewer threads (using Reactor and Netty) at the cost of complexity. If your use case is standard web CRUD, Spring MVC is fine; just note its thread per request model might need more CPU for high concurrency.
- **JVM tuning**: Ensure memory settings (Xmx) in container are appropriate. App Service by default might set some limits. The container sees the cgroup memory limit. If experiencing GC issues, consider using a newer garbage collector (G1 is default on recent Java, which is usually fine). You could also explore using a more memory-optimized JVM or ahead-of-time compilation (Spring Native with GraalVM) to a native binary for lower memory footprint (though that's quite advanced and currently experimental for many).
- **Profiling and APM**: Use Application Insights or other APM tools to find slow endpoints or methods. For instance, App Insights can show which dependency calls take the longest. You might find one SQL query is slow – optimize that query or add caching for it.
- **Scale Up vs Scale Out**: If the app is single-threaded heavy tasks (like generating a report), scaling up (bigger CPU) might help more than scaling out. If it's many small requests, scale out. Use Azure metrics: if CPU is constantly high but instance count is at max, maybe scale up the instance SKU.
- **Batch jobs/Background tasks**: If the app has any background jobs, consider running them in separate WebJob or separate process to not block the web request threads.

### Caching Strategies with Azure Redis and CDN

To elaborate on caching:

- **Azure Cache for Redis**: It's an in-memory data store. Typical uses:

  - Store session state (so if user hits different instances, they share session via Redis).
  - Cache expensive DB queries or computations. For example, cache a user's dashboard data that is complex to compute, update it on certain triggers or timeouts.
  - Rate limiting or counters – storing hits in Redis to manage usage.
  - Pub/Sub for real-time updates (less common in our context unless we have such features).

  Spring Boot can use Redis easily via Spring Data Redis or Spring Cache with a RedisCacheManager. Setup a Redis instance via Azure (it gives you hostname and key), set it in Spring config. Use it for caches with annotations like `@Cacheable("products")` on methods, etc.

  Be mindful of eviction policies and memory sizing for Redis. Azure Redis of appropriate tier should be chosen based on data size.

- **Azure CDN**: As mentioned, it's great for static content (our React app assets). Even API responses can be cached on CDN if they're mostly static or have caching headers. For instance, if the Spring Boot provides a public resource that rarely changes, you could use Azure Front Door or CDN to cache it at edge (though caching dynamic API responses is tricky due to authentication or per-user data).

  Setting up Azure CDN:

  - In Azure, create a CDN Profile and an Endpoint, with origin as your web app.
  - Configure rules if needed (like caching specific paths differently).
  - Use the CDN endpoint (e.g., `<endpoint>.azureedge.net`) or custom domain for serving.
  - Ensure your app sets appropriate `Cache-Control` headers on responses so CDN knows whether to cache and for how long.

  Azure Front Door can act as a global entry point with caching and WAF and route to backend. It's more advanced but can unify the front-end and API under one domain and even allow routing by path (e.g., Front Door serves static content from a storage or CDN and API calls to App Service). But that might be beyond current needs.

### Ensuring High Availability

Azure App Service is region-specific. For critical systems, consider deploying to multiple regions for redundancy. Terraform can help deploy a clone of the infrastructure to a secondary region. Use Azure Front Door or Traffic Manager to distribute traffic. This way, if one region goes down, the app stays up in another. This is complex but part of scalability and resilience at architecture level.

Azure recommends at least 2-3 instances for high availability on App Service (so maintenance events don't take your single instance app down) ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20For%20high%20availability%2C%20Azure,done%20during%20the%20maintenance%20process)). Indeed, if you have only 1 instance in a Standard plan, Azure might restart it for maintenance, causing a brief outage. With 2 instances, one can handle traffic while other restarts ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20For%20high%20availability%2C%20Azure,done%20during%20the%20maintenance%20process)). So even if you don't need capacity scaling, consider min 2 instances in production for HA.

### Load Testing and Performance Testing

It's wise to do some load testing on your deployed app to see how it scales:

- Use tools like JMeter, Locust, or Azure Load Testing service to simulate traffic.
- Identify the throughput (requests per second) it can handle before latency degrades or errors appear.
- This helps set autoscale rules appropriately and catch any bottlenecks (maybe at 100 concurrent users the DB becomes the bottleneck, then consider scaling DB or adding caching).
- Test both front-end and back-end: front-end mainly serves static files (should be fine unless extremely large or no CDN), back-end test API endpoints with realistic usage patterns.

Optimize based on results:

- If CPU is hot, maybe code can be optimized or scale out more.
- If DB is hot, maybe queries need optimization or DB scaling.
- If network latency to DB is significant, ensure they are in same region (which they are if in same resource group region) – remember to **colocate resources** (App and DB in same region) to reduce latency and cost ([Best practices for Azure App Service - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices#:~:text=Colocation)).
- If memory is an issue (Large heaps causing GC delays), consider smaller but more instances vs few large.

### Summary of Performance Best Practices

- Keep your content delivery efficient (CDN for static files, caching for content).
- Use autoscaling to handle variable load automatically, but also ensure at least two instances for production HA ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20For%20high%20availability%2C%20Azure,done%20during%20the%20maintenance%20process)).
- Profile and monitor application performance with APM tools (App Insights) to find hotspots.
- Use appropriate service tiers – don't overspend on huge VMs if not needed, but also don't undersize and cause performance issues. Tune as usage grows.
- Consider capacity planning: if expecting a big increase in users, test scaling beforehand to ensure the architecture holds up.

By implementing these scaling and optimization strategies, your application should be able to handle production workloads smoothly and cost-effectively.

---

## 10. Best Practices and Troubleshooting

In the final chapter, we wrap up with a collection of best practices and common pitfalls to avoid. We also present troubleshooting tips and techniques to resolve issues. We'll cover security best practices, cost optimization guidance, and lessons learned that can save time and effort for advanced developers working on similar deployments.

### Common Pitfalls and Solutions

**Pitfall 1: Hardcoding Configuration** – Storing environment-specific values (like DB passwords, API keys, endpoints) directly in code or Dockerfiles. This is risky and inflexible. **Solution**: Externalize configuration. Use environment variables, config files, or better, Azure Key Vault for secrets. Spring Boot can read from environment or Vault, and React can use environment variables at build time (like `REACT_APP_API_URL`). This makes your images generic and promotes Twelve-Factor App principles.

**Pitfall 2: Terraform State Mismanagement** – Losing or corrupting Terraform state can lead to duplicate resources or inability to update properly. **Solution**: Always use remote state with locking ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=By%20default%2C%20Terraform%20state%20is,ideal%20for%20the%20following%20reasons)). Back up state (Azure blob has redundancy, but you can also version it). Avoid using `-target` or manual Azure changes that Terraform isn't aware of. If a manual change is needed in emergency, consider importing it into Terraform state afterwards (`terraform import`).

**Pitfall 3: Ignoring Resource Naming and Limits** – Azure resource names often need to be globally unique (like DNS names for Web App, storage accounts, etc.). If you hardcode a name like "myapp", it might already be taken or conflict when deploying another environment. **Solution**: Use naming conventions with prefixes/suffixes (we did via var.prefix) to ensure uniqueness. Also be mindful of length and character rules for each resource type (Terraform docs usually note them).

**Pitfall 4: Container Port Mismatch** – Deploying a container to App Service but not exposing the correct port or not informing Azure via WEBSITES_PORT. This results in "container unhealthy" errors because Azure pings port 80 by default and your app might be on 8080. **Solution**: Always set WEBSITES_PORT to your app's listening port (or modify your container to listen on 80). We did this in Terraform config for both apps.

**Pitfall 5: Not Utilizing Deployment Slots** – Deploying directly to production slot each time can cause downtime or immediate exposure of bugs. **Solution**: Use staging slots for zero-downtime and safe deployments ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=In%20order%20to%20use%20blue%2Fgreen,go%20through%20the%20new%20version)). They add complexity, but greatly reduce risk.

**Pitfall 6: Overlooking Logging** – It's frustrating to debug an issue if logs are not available or not capturing needed info. **Solution**: Ensure your app logs meaningful information and that those logs are being collected (App Insights or Log Analytics). Set log level appropriately (INFO normally, DEBUG for detailed troubleshooting toggled when needed). Use structured logging if possible (so logs can be queried easily).

**Pitfall 7: Security Neglect** – Not securing sensitive endpoints or using default configurations. E.g., leaving a database accessible to all IPs, or using admin default passwords, or not forcing HTTPS. **Solution**: Follow security best practices (below). E.g., restrict DB access (we did via either firewall or private endpoints), enforce HTTPS ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=The%20%60%3Capp,TLS%20certificate%20to%20App%20Service)), rotate credentials, and use managed identities to avoid credentials altogether ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)).

**Pitfall 8: Cost Surprises** – Ignoring the cost implications of certain choices (like leaving a high tier App Service running 24/7 or a large DB idle) can lead to unnecessary cloud spend. **Solution**: Use cost analysis tools and rightsizing. For example, scale down non-prod environments during off hours (could automate via Azure Automation or just manual schedule). Use Azure's pricing calculator to estimate costs for chosen SKUs. We'll discuss more cost tips below.

**Pitfall 9: Not Testing Infrastructure Changes** – Pushing Terraform changes directly to production without testing can be risky (e.g., an incorrect rule could delete a resource). **Solution**: If possible, test Terraform changes in a non-prod subscription or resource group. Or at least do a `terraform plan` and carefully review it (set up in CI to require human review for destructive changes). Also, modularize and reuse known good configurations rather than writing from scratch each time.

**Pitfall 10: Single Point of Failure** – Relying on one instance, one region, or one database node. **Solution**: Introduce redundancy. For App Service, multiple instances (with autoscale) ensures updates or reboots don't take down the site ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20For%20high%20availability%2C%20Azure,done%20during%20the%20maintenance%20process)). For region redundancy, consider secondary deployment or using Azure Availability Zones (App Service can be zone-redundant in Premium v3). For database, use high-availability features (Azure Database for MySQL has zone redundant deployment or read replicas for scaling reads). Plan backups for data (Azure DB auto backups daily, but know retention and test restore process).

### Security Best Practices

Security is paramount, especially when exposing services on the internet:

- **Use HTTPS and Latest TLS**: We enforced HTTPS and got certificates for custom domains. Azure manages TLS for azurewebsites.net; for custom, use App Service managed cert or your own. TLS ensures data in transit is encrypted.

- **Managed Identity over Service Principals**: Where possible, prefer managed identities for resource access since they're managed by Azure and don't require storing secrets ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)). We used MI for ACR and Key Vault. Also, an MI could be used for calling other Azure services (like Storage, Cosmos DB, etc.) eliminating secrets.

- **Least Privilege**: The service principal used by Terraform should have the minimal role needed (Contributor is broad; if you can, restrict its scope to only that resource group). The App Service's managed identity was given AcrPull on ACR, and Get on Key Vault – nothing more. Avoid giving overly broad permissions.

- **Secure Your Key Vault**: Key Vault is central for secrets; ensure access policies are tight (only the app and necessary devs or pipeline have access). Turn on Key Vault logging to monitor access. Use Key Vault firewalls or private endpoints to restrict access if appropriate.

- **Regularly Rotate Secrets**: E.g., rotate database passwords or any other credentials periodically. Key Vault can set reminders or even generate new secrets. This might mean updating Terraform variables or Key Vault entries and restarting the app to pick up new secrets.

- **Dependency Updates**: Keep your dependencies (both backend and frontend) updated to incorporate security patches. Use tools like Dependabot or OWASP Dependency Check. Also update base images regularly – e.g., the Node and OpenJDK images should be updated to get security fixes. Rebuild your images periodically to pull in patched base layers.

- **Image Scanning**: If using ACR, enable ACR Tasks or Microsoft Defender for Cloud to scan container images for vulnerabilities. This can alert on known vulnerabilities in OS packages or libraries.

- **Web Security for React**: Implement security in the front-end as well:

  - Use security headers (Content Security Policy, XSS Protection, etc., can be set via Nginx headers).
  - Protect against XSS and CSRF by proper coding practices (React by default escapes content, which helps).
  - If the app has authentication, use secure cookies or tokens with proper settings (HttpOnly, Secure, SameSite).

- **Backend Security**: Validate inputs on the API to avoid injection attacks. Use Spring Security if you need authN/Z. For example, if exposing APIs, consider using Azure AD or another identity provider for JWT tokens, and Spring Security to protect endpoints (beyond our scope but important for real apps).

- **Monitoring for Security**: Use Azure Monitor to detect unusual patterns, such as sudden spike in 500 errors (could indicate an attack) or weird user agents. Azure Web App has built-in Basic WAF (if behind Front Door or App Gateway with WAF). If high security, consider adding a Web Application Firewall to filter malicious requests.

- **Network Security**: As discussed, use VNet and private links to avoid exposing internal services. Also, set up NSGs or Firewall rules if applicable. For instance, if the App Service (in VNet integration) should only call the database and not the internet, use Azure Firewall to block other egress.

Implementing these practices significantly reduces the risk of breaches and downtime due to security issues.

### Cost Optimization Techniques in Azure

Running services in Azure incurs costs, but there are ways to keep them in check:

- **Right-Size App Service Plan**: Don't use a higher tier than necessary. For example, in dev/test, use the free tier or basic tier. In production, choose the smallest instance that can handle base load, and rely on autoscale for peaks. Azure charges per instance-second, so two small instances might be cheaper than one large instance and provide better HA. However, too many small can cost more than fewer mediums – evaluate based on pricing. Basic vs Standard: Standard adds autoscale and slots – if you need those, then Standard is justified. Otherwise Basic is cheaper.

- **Shut Down Unused Environments**: If you have a staging or test slot that's not in use, scale it down to 0 instances (slots share the same plan though, so they do consume resources unless you use a separate plan). Alternatively, deploy dev/test in a separate resource group and delete or deallocate when not in use. Azure Dev/Test subscriptions (for MSDN subscribers) have discounts – use them for non-prod.

- **Use Azure Reservations/Savings Plan**: If you know you'll run this app for at least a year or more at relatively steady state, consider a 1-year or 3-year Reserved Instance for the App Service Plan or an Azure Savings Plan. These can save ~30-50% compared to pay-as-you-go for that resource, in exchange for commitment ([Azure App Service Cost Optimization best practices - Medium](https://medium.com/serverless360/azure-app-service-cost-optimization-best-practices-8d21b64e966b#:~:text=Azure%20App%20Service%20Cost%20Optimization,the%20alternative%20within%20same)). Note: As of writing, Azure has reservations for App Service isolated instances and maybe a savings plan that covers compute like App Service.

- **Optimize Database Cost**: Don't oversize the database. If using Azure Database for MySQL, choose the appropriate SKU (maybe start with 1 vCore). Monitor usage – if CPU and IO are low, you might scale down. Use auto-pausing features if applicable (Azure SQL has serverless that can auto-pause; MySQL flexible doesn't auto-pause but you can scale down at off hours manually).
  If your DB workload is light and mostly read, maybe using a cheaper service like Azure Database for MySQL Basic or even an alternative like Azure Cosmos DB with MySQL API could be cheaper (depending on use).

- **Use Free/Included Services**: Application Insights has a free data quota per month (e.g., 5 GB free depending on pricing tier). Stick within it by adjusting sampling (App Insights by default samples data to reduce volume, you can configure sampling rate). Log Analytics also may incur costs per GB ingested – so be mindful of what debug logs you send (you might not want DEBUG logs in production always, or at least adjust retention). Consider setting lower retention for logs (maybe keep 30 days instead of default 90, to save storage costs) ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20when%20you%20add%20a,To%20avoid%20this%20downtime)).

- **Azure Front Door/Traffic Manager**: Only add these if needed – they cost extra. If you serve a global audience, the performance benefits might outweigh cost. If all users are in one region, you might skip it.

- **Clean Up Unused Resources**: Over time, make sure to remove things not needed. Orphaned Public IPs, NICs, unused storage accounts, etc., could incur minimal costs that add up. Terraform helps here – if it's not in code, it gets destroyed (as long as you remove it from config and apply).

- **Monitor costs**: Use Azure Cost Management to set a budget and alerts. For instance, get notified if monthly cost is trending to exceed a threshold. Tag resources with an owner or project so you can see breakdown.

- **Development Workstation**: For testing Azure things, leverage Azure's free services where possible (free tier App Service has no SSL for custom domain and sleeps after idle, but maybe fine for small tests). Or use local emulators (but App Service and MySQL aren't easily emulatable; though one could run MySQL in a container locally for dev). Use Azure's free credit offers if any or MSDN benefits for dev/test.

- **Use Open Source / Included Options**: For example, rather than paying for a separate monitoring tool, use Application Insights which is included (with some free quota). Rather than running a custom VM for Jenkins, use GitHub Actions (free for public repos or comes with some free minutes for private, beyond that use Azure DevOps which has a free tier of pipeline minutes).

### Final Thoughts

Implementing a production-ready solution with React, Spring Boot, Docker, Terraform, and Azure is complex but highly rewarding. We covered how to design and automate the deployment, how to secure and scale the system, and how to monitor and maintain it.

Always keep learning from each deployment:

- Conduct post-mortems on any incidents to improve.
- Stay updated with Azure improvements (for instance, new Azure services or features like Azure Container Apps or Azure Spring Apps may offer alternatives to consider for future).
- Refine your Terraform code into modules for reuse across projects if applicable.
- Backup your critical data and configurations.

Finally, engage with the developer community. Many have deployed similar stacks; blog posts (like the ones referenced throughout) and forums (Stack Overflow, Azure Docs Q&A) are invaluable when you encounter weird issues. No one knows everything, but with good practices and community knowledge, you can solve almost any problem.

This guide aimed to be a thorough blueprint for advanced developers. By following these steps and tips, you should be able to confidently implement a robust, scalable, and maintainable deployment of React and Spring Boot apps on Azure, using the power of Docker and Terraform to streamline your DevOps workflow.

**References:**

- Deepu K Sasidharan, _Deploy a web app to Azure App Service using Terraform_ – modern approach to deploying Dockerized apps on Azure ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=If%20you%20are%20a%20modern,tied%20down%20to%20just%20Java)) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=To%20try%20this%20out%20you,to%20install%20them%20if%20needed)).
- Padok Cloud blog, _How to terraform an Azure App Service using container_ – covers ACR integration, slots, and App Insights setup ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=,ARC01)) ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=In%20order%20to%20use%20blue%2Fgreen,go%20through%20the%20new%20version)).
- Microsoft Azure Documentation – App Service VNet integration ([Integrate your app with an Azure virtual network - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration#:~:text=Virtual%20network%20integration%20gives%20your,endpoint%20for%20inbound%20private%20access)), Private Endpoints ([Using private endpoints for App Service apps - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/overview-private-endpoint#:~:text=You%20can%20use%20a%20private,exposure%20from%20the%20public%20Internet)), Terraform state management ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=By%20default%2C%20Terraform%20state%20is,ideal%20for%20the%20following%20reasons)), custom domains and certificates ([Tutorial: Secure app with a custom domain and certificate - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate#:~:text=The%20%60%3Capp,TLS%20certificate%20to%20App%20Service)).
- IBM Cloud Learn, _What is Java Spring Boot?_ – overview of Spring Boot benefits ([What Is Java Spring Boot? | IBM](https://www.ibm.com/think/topics/java-spring-boot#:~:text=Java%20Spring%20Boot%20,Spring%20Framework%20faster%20and%20easier)).
- React Official Docs – React is a JavaScript library for building UIs ([React – A JavaScript library for building user interfaces](https://legacy.reactjs.org/#:~:text=React)).
- Docker Docs – Docker enables you to separate apps from infrastructure ([Get Docker | Docker Docs
  ](https://docs.docker.com/get-started/get-docker/#:~:text=Docker%20is%20an%20open%20platform,developing%2C%20shipping%2C%20and%20running%20applications)).
- SonicWall Glossary, _Terraform_ – Terraform provides a consistent CLI for managing infrastructure as code ([Terraform](https://www.sonicwall.com/glossary/terraform#:~:text=Terraform)).
- Microsoft Learn, _Benefits of IaC and CI/CD_ – declarative, consistent, secure deployments via code ([Deploy to Azure with IaC and GitHub Actions - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/devops/deliver/iac-github-actions#:~:text=Benefits%20of%20using%20IaC%20and,automation%20for%20deployments)).
- Azure Best Practices – keep resources in the same region to minimize latency and cost ([Best practices for Azure App Service - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices#:~:text=Colocation)).
- Azure Architecture Blog – recommendation for 3+ instances for HA due to maintenance events ([Terraform an Azure app service using Docker container | Padok](https://cloud.theodo.com/en/blog/terraform-azure-app-docker#:~:text=Warning%3A%20For%20high%20availability%2C%20Azure,done%20during%20the%20maintenance%20process)).
- Dev Genius (Jay Lee), _Managed Identity and Key Vault_ – eliminates need for storing secrets by using managed identities ([Azure Key Vault and Managed Identity for Java on Azure Application platforms | by Jay Lee | Apr, 2022 | Medium | Dev Genius](https://blog.devgenius.io/azure-key-vault-and-managed-identity-for-java-on-azure-platforms-f4b1b791a214#:~:text=%E2%80%9CA%20common%20challenge%20for%20developers,for%20developers%20to%20manage%20credentials)).
- And many more in-line references in the guide above for specific points and quotes.
