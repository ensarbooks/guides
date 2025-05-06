# Building a Spring Boot Microservice with Health Checks and AWS Auto-Scaling

_This comprehensive guide is tailored for experienced developers, offering a step-by-step journey (~200 pages in a full document) into building a robust Spring Boot microservice. It covers health checks, AWS deployment (ECS Fargate vs. EC2), auto-scaling configurations, monitoring, infrastructure as code, CI/CD pipelines, security best practices, and performance testing with real-world scenarios and best practices._

**Table of Contents:**

1. [Spring Boot Application Setup](#spring-boot-application-setup)  
   1.1 [Project Structure and Dependencies](#project-structure-and-dependencies)  
   1.2 [Implementing REST APIs](#implementing-rest-apis)  
   1.3 [Setting up Spring Boot Actuator for Health Checks](#setting-up-spring-boot-actuator-for-health-checks)  
   1.4 [Custom Health Indicators (Database, Message Queues, etc.)](#custom-health-indicators)
2. [Deploying to AWS](#deploying-to-aws)  
   2.1 [Choosing ECS with Fargate vs. EC2 with Auto Scaling Groups](#ecs-fargate-vs-ec2-asg)  
   2.2 [Dockerizing the Spring Boot Application](#dockerizing-spring-boot)  
   2.3 [Pushing Images to AWS Elastic Container Registry (ECR)](#pushing-images-to-ecr)  
   2.4 [Deployment Options: Elastic Beanstalk, ECS, EC2](#deployment-options)
3. [Monitoring and Health Checks](#monitoring-and-health-checks)  
   3.1 [Configuring Spring Boot Actuator Endpoints](#configuring-actuator-endpoints)  
   3.2 [Publishing Metrics to AWS CloudWatch](#publishing-metrics-to-cloudwatch)  
   3.3 [AWS CloudWatch Logs and Alarms](#cloudwatch-logs-and-alarms)  
   3.4 [Custom CloudWatch Metrics for Detailed Monitoring](#custom-cloudwatch-metrics)
4. [AWS Auto Scaling Configuration](#aws-auto-scaling-configuration)  
   4.1 [Creating AWS Auto Scaling Groups or ECS Service Auto Scaling](#creating-auto-scaling-groups)  
   4.2 [Defining Scaling Policies (CPU, Requests, Latency, etc.)](#defining-scaling-policies)  
   4.3 [Configuring CloudWatch Alarms for Scaling Events](#configuring-cloudwatch-alarms)  
   4.4 [Testing Auto-Scaling Behavior](#testing-auto-scaling)
5. [Infrastructure as Code (IaC)](#infrastructure-as-code)  
   5.1 [Terraform Scripts for AWS Setup](#terraform-scripts-for-aws-setup)  
   5.2 [AWS CDK for Dynamic Provisioning](#aws-cdk-provisioning)  
   5.3 [Managing Resources with AWS CloudFormation](#managing-resources-with-cloudformation)
6. [CI/CD Pipeline for Deployment](#ci-cd-pipeline-for-deployment)  
   6.1 [CI/CD with GitHub Actions or Jenkins](#ci-cd-github-actions-jenkins)  
   6.2 [Automating Docker Builds and Deployments](#automating-docker-builds-deployments)  
   6.3 [Rolling Updates and Zero-Downtime Deployments](#rolling-updates-zero-downtime)
7. [Security and Best Practices](#security-and-best-practices)  
   7.1 [Using IAM Roles and Policies for Access Control](#iam-roles-and-policies)  
   7.2 [Encrypting Sensitive Data with AWS Secrets Manager](#encrypting-sensitive-data)  
   7.3 [Spring Boot and AWS Security Best Practices](#spring-boot-aws-security)
8. [Final Testing and Optimization](#final-testing-and-optimization)  
   8.1 [Load Testing with AWS Auto Scaling](#load-testing-with-auto-scaling)  
   8.2 [Debugging Scaling Issues](#debugging-scaling-issues)  
   8.3 [Performance Tuning and Optimization](#performance-tuning-optimization)

Throughout this guide, **code snippets** and **diagrams** illustrate key concepts, and **real-world scenarios** provide context. Look out for citations (formatted as【†source】) referencing external resources for deeper dives and verification.

---

## 1. Spring Boot Application Setup <a id="spring-boot-application-setup"></a>

Before diving into AWS integration, we start by setting up a Spring Boot microservice with robust health check mechanisms. This section walks you through structuring the project, adding necessary dependencies, building RESTful APIs, and configuring the Spring Boot Actuator for health monitoring.

### 1.1 Project Structure and Dependencies <a id="project-structure-and-dependencies"></a>

A well-organized project structure and the right dependencies lay the foundation for a scalable microservice:

- **Maven/Gradle Project Structure**: Organize the codebase following standard conventions:
  - `src/main/java` for application code
  - `src/main/resources` for configuration (like `application.yml` or `application.properties`)
  - `src/test` for tests.
- **Key Dependencies**:
  - **Spring Boot Starter Web** for building REST APIs (e.g., `spring-boot-starter-web`).
  - **Spring Boot Actuator** for health checks and metrics (`spring-boot-starter-actuator`).
  - **Spring Boot Starter Test** for testing (`spring-boot-starter-test`).
  - **Database driver** (e.g., `mysql-connector-java` or `postgresql` if a database is used).
  - **Messaging clients** (Kafka, RabbitMQ, etc.) if applicable.
  - **Micrometer and CloudWatch registry** for custom metrics (later in monitoring section).

**Maven `pom.xml` excerpt (with key dependencies):**

```xml
<dependencies>
    <!-- Spring Boot Web and Actuator -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <!-- Database (MySQL example) -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>
    <!-- Messaging (RabbitMQ example) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-amqp</artifactId>
    </dependency>
    <!-- Monitoring (Micrometer for CloudWatch) -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-registry-cloudwatch2</artifactId>
    </dependency>
    <!-- (Other dependencies like security, etc.) -->
</dependencies>
```

If using **Gradle**, dependencies in `build.gradle` look similar, declared in the `dependencies` block. A typical project might use the Spring Initializr to generate this setup.

**Project Structure Example:**

```
my-microservice/
├── src/
│   ├── main/
│   │   ├── java/com/example/mymicroservice/
│   │   │   ├── MyMicroserviceApplication.java  (Main class with SpringBootApplication)
│   │   │   ├── controller/ ... (REST controllers)
│   │   │   ├── service/ ... (Service layer beans)
│   │   │   └── ... (other packages)
│   │   └── resources/
│   │       ├── application.yml (configuration)
│   │       └── static/ (if any static files)
│   └── test/
│       └── java/com/example/mymicroservice/ ... (test classes)
├── pom.xml or build.gradle (build configuration)
└── Dockerfile (for containerization, later)
```

**Dependency Best Practices:**

- Use **Spring Boot BOM (Bill of Materials)** for consistent dependency versions. This ensures compatibility between Spring Boot, Actuator, etc.
- Only include necessary dependencies to keep the application lightweight—avoid “fat” jars with unused libraries which increase the image size and potential attack surface.

### 1.2 Implementing REST APIs <a id="implementing-rest-apis"></a>

Implementing a simple REST API helps verify that the application works before adding complexity like AWS. We'll create a basic controller and a couple of endpoints:

- **Example**: A `UserController` to manage users with endpoints `GET /users/{id}`, `POST /users`, etc.
- Use `@RestController` for defining REST endpoints and `@RequestMapping` or specialized annotations like `@GetMapping`, `@PostMapping`.

**Sample Controller:**

```java
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService; // Assume a service layer exists

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.findById(id)
                .map(user -> ResponseEntity.ok(user))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User newUser) {
        User created = userService.save(newUser);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

- The above uses standard Spring MVC annotations. `UserService` handles business logic (omitted for brevity).
- Return `ResponseEntity` to control HTTP status codes (e.g., 201 Created for a new user).
- Validate input and handle exceptions (possibly using `@ControllerAdvice` for global exception handling, not shown here but important for production readiness).

**Testing**: Write unit tests for controllers using Spring MockMvc or WebTestClient (for reactive). Also, test the service layer and repository (if any). Ensuring our API works correctly is a foundation before layering on AWS deployment.

### 1.3 Setting up Spring Boot Actuator for Health Checks <a id="setting-up-spring-boot-actuator-for-health-checks"></a>

**Spring Boot Actuator** provides production-ready features such as health checks, metrics, info, and more. Out of the box, Actuator offers a `/actuator/health` endpoint that reports the application’s health status. We will configure Actuator to include liveness and readiness probes (especially useful in container environments and Kubernetes/ECS), and expose additional details.

**Enabling Actuator Endpoints:**

- By default, only a minimal health indicator is shown at `/actuator/health`. We can configure Actuator to expose other endpoints like `info`, `metrics`, etc. via the application properties.
- For example, to expose all endpoints (or a subset) over HTTP:
  ```yaml
  management:
    endpoints:
      web:
        exposure:
          include: health, info, metrics, prometheus # etc. Only expose what's necessary
    endpoint:
      health:
        show-details: always # include details (like down components) in health
        probes:
          enabled: true # enable liveness/readiness if using Spring Boot 2.3+
  ```
- The `show-details: always` setting allows the health endpoint to show details of each component (like database status, disk space) to authorized users. In a secure environment, you might restrict this to admin or internal use.

**Liveness and Readiness**:

- Spring Boot (2.3 and above) supports **liveness** and **readiness** probes via Actuator health groups. They expose `/actuator/health/liveness` and `/actuator/health/readiness`.
- Liveness indicates if the app's internal state is good (if not, the container might need restarting).
- Readiness indicates if the app is ready to serve requests (if not, remove from load balancer until it is ready).

These are beneficial in container orchestrators. For AWS ECS:

- You can use the general `/actuator/health` for ECS container health checks (or define a specific custom health endpoint).
- In Kubernetes (if that were a context), you'd wire liveness/readiness to Kubernetes probes.

**Security for Actuator**: Ensure that sensitive endpoints are secured (especially if exposing metrics or env). In development, you might leave them open, but in production, integrate with Spring Security or network policies to restrict access.

**Quick test**: Run the application (`./mvnw spring-boot:run` or via your IDE) and access `http://localhost:8080/actuator/health`. You should see a JSON response like:

```json
{ "status": "UP" }
```

If details are enabled and, say, a DB is configured, you'll see sub-components:

```json
{
  "status": "UP",
  "components": {
    "db": { "status": "UP", "details": { "database": "MySQL", "result": 1 } },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 499963174912,
        "free": 299865128960,
        "threshold": 10485760
      }
    },
    "ping": { "status": "UP" }
  }
}
```

_(The above structure may vary with Spring Boot versions, but it shows an example with a database and disk space indicator.)_

### 1.4 Custom Health Indicators (Database, Message Queues, etc.) <a id="custom-health-indicators"></a>

Spring Boot Actuator includes many **built-in health indicators**:

- DataSource health (checks database connectivity).
- Disk space health.
- Ping (always up).
- Others for caches, messaging systems (if using Spring integration for those).

However, advanced microservices often need **custom health indicators** for external dependencies or business logic checks. Examples:

- Checking connectivity to an external REST API your service depends on.
- Verifying a message queue (Kafka/RabbitMQ) is reachable.
- Ensuring a non-standard component (e.g., a hardware sensor) is functioning.

**Creating a Custom HealthIndicator**:  
Implement the `HealthIndicator` interface and register it as a Spring bean (using `@Component` or via configuration). Override the `health()` method to perform the custom check and return a `Health` status (`Health.up()`, `Health.down()`, or with custom status).

**Example – URL Shortener Service Health Indicator** (from Reflectoring’s example):

```java
@Component
public class UrlShortenerServiceHealthIndicator implements HealthIndicator {
    private static final String URL = "https://cleanuri.com/api/v1/shorten";
    @Override
    public Health health() {
        // Check if external URL is reachable
        try (Socket socket = new Socket(new URL(URL).getHost(), 80)) {
            // Connection successful
        } catch (Exception e) {
            return Health.down()
                    .withDetail("error", e.getMessage())
                    .build();
        }
        return Health.up().build();
    }
}
```

In this snippet:

- It tries to open a socket to `cleanuri.com` on port 80. If it fails, the health status is set to **DOWN** with an error detail.
- If the connection succeeds, it reports **UP**.

**Example – Database Health Indicator (Custom Query)**:  
While Spring’s default DB health check simply tries to acquire a connection, you might want to run a lightweight query to ensure the database responds:

```java
@Component("databaseHealth")
public class DatabaseHealthIndicator implements HealthIndicator {
    @Autowired DataSource dataSource;
    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            // Run a simple validation query (depending on DB, e.g., "SELECT 1")
            boolean valid = conn.isValid(2);
            if (!valid) {
                return Health.down().withDetail("error", "Connection invalid").build();
            }
        } catch (SQLException e) {
            return Health.down(e).build();
        }
        return Health.up().build();
    }
}
```

Naming the component `"databaseHealth"` will make its health status appear under that name in the health endpoint.

**Example – Messaging Queue Health Indicator** (pseudo-code):

```java
@Component
public class QueueHealthIndicator implements HealthIndicator {
    @Autowired RabbitTemplate rabbitTemplate; // or Kafka template/connection
    @Override
    public Health health() {
        try {
            // perhaps check queue length or publish a test message
            rabbitTemplate.getConnectionFactory().createConnection().close();
            // If we reach here, connection could be opened
            return Health.up().build();
        } catch (Exception e) {
            return Health.down().withDetail("error", e.getMessage()).build();
        }
    }
}
```

This simply tries to open and close a connection to RabbitMQ. In real scenarios, you might be more specific (like checking a reply from a heartbeat queue).

**Registering Custom Status**:  
Sometimes, you might define custom `Status` (like `WARN` or `FATAL`). Spring Boot allows this, but you must also configure how to aggregate or map these statuses:

- Define order: `management.endpoint.health.status.order=fatal,down,out-of-service,unknown,up` so Spring knows `FATAL` is considered worse than `DOWN`.
- Map custom statuses to HTTP codes if needed, e.g., map `FATAL` to 503 (service unavailable) via properties.

**Health Endpoint Responses**:  
By default, overall health is **UP** if all components are UP. If any single component is DOWN, the overall status is DOWN (and Actuator will return HTTP 503 for `/health` by default for DOWN or OUT_OF_SERVICE statuses). This is important for AWS’s load balancers and auto-scaling health checks: typically, if the `/health` endpoint returns a 503, the instance or container might be replaced or marked unhealthy.

**Composite Health Indicators**:  
For advanced cases, you can create composite health checks where one logical health indicator aggregates multiple others. Spring Boot offers `CompositeHealthContributor` to group health indicators (useful if, say, multiple downstream services collectively determine readiness). For example, grouping database + an external API check for a specific functionality:

- Implement `CompositeHealthContributor` (return an iterator of health contributors).
- Mark individual contributors with `@Component` and implement `HealthIndicator` and the marker interface `HealthContributor`.

In practice, custom health indicators ensure your microservice’s `/health` reflects all critical dependencies. AWS can then use this to detect issues (e.g., if DB is down, the instance might report unhealthy and be replaced depending on setup). We’ll revisit how AWS uses health checks in the auto-scaling section.

---

## 2. Deploying to AWS <a id="deploying-to-aws"></a>

Deploying a microservice on AWS introduces options: using containers on ECS (with Fargate or EC2), leveraging Elastic Beanstalk for simplicity, or manually managing EC2 instances. This section compares **ECS Fargate vs EC2**, walks through Dockerizing the app, pushing to **ECR (Elastic Container Registry)**, and deploying via different AWS services.

### 2.1 Choosing ECS with Fargate vs. EC2 with Auto Scaling Groups <a id="ecs-fargate-vs-ec2-asg"></a>

**Amazon ECS (Elastic Container Service)** is a fully managed container orchestration service. It can run containers in two modes:

- **ECS on EC2**: You manage a cluster of EC2 instances that run your containers.
- **ECS with Fargate**: A serverless approach where you don’t manage servers; AWS runs containers on-demand.

**Auto Scaling** applies in both:

- With EC2, you typically use an Auto Scaling Group (ASG) to add/remove EC2 instances based on load, and ECS then places tasks on them.
- With Fargate, scaling is at the service/task level (no explicit EC2 management, Fargate launches new tasks directly).

**ECS with Fargate (Serverless Containers)**:  
Pros:

- No server management; you specify CPU/memory per task.
- Scales to zero (you pay per running task).
- Simplified deployment – you don't worry about AMIs, patching, etc.
  Cons:
- Slightly higher cost per unit (you pay for the convenience).
- Some AWS features might have limitations or require platform versions (e.g., certain secret injection features require newer Fargate platform versions).

Use Fargate if you want to minimize ops overhead or have spiky workloads where you benefit from scaling to zero or quick scaling.

**ECS on EC2 (Self-Managed Nodes)**:  
Pros:

- Potentially lower cost if you have consistent high usage (you utilize EC2 fully).
- More control over instance types (e.g., GPU instances for special workloads).
- Can use spot instances to reduce cost.
  Cons:
- Need to manage AMIs (or use ECS-optimized AMIs), patch OS, handle cluster capacity.
- Slightly more complex scaling (scale both tasks and instances).

This approach might be chosen if you need more control or have steady workloads and want cost optimization.

**Elastic Beanstalk**: Another option – AWS Elastic Beanstalk can deploy Docker containers or JVM apps with minimal setup. It handles EC2, load balancing, scaling under the hood. It’s simpler to start with but less flexible for complex microservice architectures. Given our advanced scenario, ECS gives more fine-grained control.

**Decision**: For our guide, we'll lean towards **ECS with Fargate** for deployment, but also mention how to do it with EC2 and auto scaling. The principles of health checks and scaling apply similarly. ECS integrates with ELB (Elastic Load Balancer) for distributing traffic and health checks.

### 2.2 Dockerizing the Spring Boot Application <a id="dockerizing-spring-boot"></a>

We need to package our Spring Boot app into a Docker image. This allows running it consistently anywhere, including AWS ECS or other container platforms.

**Creating a Dockerfile**: Place a `Dockerfile` at the root of the project (or in the directory you’ll build from). For a Spring Boot app (which is a jar), a common approach is:

1. **Use a Multi-Stage Build** to keep the image small:
   - Stage 1: Build the application using a Maven or Gradle image.
   - Stage 2: Use a lightweight JDK or even JRE image to run the app.
2. Alternatively, build the jar on the host (via Maven/Gradle) and use a single-stage Dockerfile to copy it into a base image.

**Example Dockerfile (Multi-stage with Maven):**

```Dockerfile
# Stage 1: Build the jar
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the app
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
# Copy only the jar from the builder stage
COPY --from=build /app/target/my-microservice.jar /app/my-microservice.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/my-microservice.jar"]
```

In the above:

- We used OpenJDK 17 (adjust JDK version as per your Spring Boot version, e.g., if using Java 11, use an appropriate base image).
- We copy the jar from the Maven build stage.
- We expose port 8080 (where Spring Boot runs by default). Exposing is not strictly required, but it’s good documentation.

**Building the Image**: If you have Docker installed locally:

```bash
docker build -t my-microservice:latest .
```

This tags it as `my-microservice:latest`. We’ll later tag it for ECR.

**Test the Container Locally** (optional but recommended):

```bash
docker run -p 8080:8080 my-microservice:latest
```

Then hit `http://localhost:8080/actuator/health` or your API endpoints to ensure it runs.

**Minimize Image Size**:

- Use Alpine-based images or JRE images to reduce size. Our example used `alpine` (Temurin JRE on Alpine).
- You can also consider tools like Jib (for Java) or Cloud Native Buildpacks which create optimized images without a Dockerfile.
- Keep the number of layers small (our multi-stage approach helps).
- Don’t include source files or credentials in the final image.

### 2.3 Pushing Images to AWS Elastic Container Registry (ECR) <a id="pushing-images-to-ecr"></a>

AWS ECR is a private Docker registry for your AWS account, which is the source for ECS to fetch images.

**Steps to push to ECR:**

1. **Create an ECR Repository**:

   - Go to AWS ECR (in the AWS Console under "Elastic Container Registry").
   - Click “Create repository”. Give it a name (e.g., `my-microservice`). You can use either a single name or include a namespace (like `team1/my-microservice`).
   - Note if using AWS CLI, you could also do:
     ```bash
     aws ecr create-repository --repository-name my-microservice
     ```
     The output will contain the repository URI.

2. **Authenticate Docker to ECR**:

   - ECR uses AWS CLI to provide a login password. For example:

     ```bash
     aws ecr get-login-password --region <your-region> | \
       docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
     ```

     Replace `<your-region>` (e.g., `us-east-1`) and `<aws_account_id>` (your numeric AWS account ID). The AWS CLI v2 simplifies this with `get-login-password` (no need for older `$(aws ecr get-login ...)` commands).

   - This command uses temporary credentials to log Docker into ECR. It’s valid for 12 hours typically.

3. **Tag the Image for ECR**:

   - ECR repositories are addressed by URI. For example, if your account is `123456789012` and region `us-east-1`, and repository `my-microservice`, the full image name might be:  
     `123456789012.dkr.ecr.us-east-1.amazonaws.com/my-microservice:latest`
   - Tag your local image to that:
     ```bash
     docker tag my-microservice:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-microservice:latest
     ```
   - You can use a version instead of `latest`. E.g., `:v1.0.0` or the Git commit hash for versioning.

4. **Push the Image**:
   - ```bash
     docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-microservice:latest
     ```
   - This uploads the image layers to ECR. After completion, the image is in the repository.

These steps align with typical ECR usage. AWS console also provides a “View push commands” which essentially list the above steps.

**Verify on AWS Console**: You should see your image in the ECR repository, with the tag and image size. This confirms that AWS now holds our container image.

### 2.4 Deployment Options: Elastic Beanstalk, ECS, EC2 <a id="deployment-options"></a>

Now that we have an image in ECR, we have multiple options to deploy it:

#### Option A: AWS Elastic Beanstalk (Docker)

**Elastic Beanstalk (EB)** supports deploying a Docker container (single container) or a Docker Compose (multi-container) via its Docker platform. EB will provision EC2 instances, a load balancer, auto-scaling, monitoring, etc., automatically. It’s one of the quickest ways to get a containerized Spring Boot app running on AWS.

Steps with EB (high level):

- In AWS Console, go to Elastic Beanstalk.
- Create a new Application and Environment.
- Choose Platform: Docker (and select single Docker image).
- It will ask for the Docker image: provide the ECR image URL and tag.
- EB will handle the rest: launching an EC2 (or multiple with auto-scaling if configured), running Docker, health checks etc.
- You can also use the EB CLI, where you’d have a `Dockerrun.aws.json` that references the image.

**Pros**: Very quick to deploy, minimal AWS knowledge needed, managed health checks, and basic auto-scaling.
**Cons**: Less control over underlying resources (though you can customize via configuration files), and for a microservices ecosystem, EB for each service can become a bit unwieldy compared to using ECS/EKS.

We will not delve deep into EB specifics since our focus is advanced AWS usage (ECS, IaC, etc.), but it’s good to be aware that EB is an available path.

#### Option B: Amazon ECS on Fargate

This is the main path we'll detail, as it offers fine control with minimal server maintenance:

To run our container on ECS Fargate, we need:

- An ECS **Cluster** (logical grouping for ECS services; with Fargate, no EC2s needed in cluster).
- A **Task Definition** that defines how to run the container (image, CPU, memory, env variables, IAM roles, etc.).
- An **ECS Service** to run and maintain a desired number of tasks, optionally behind a load balancer, and with auto-scaling.

**1. Create an ECS Cluster**:

- In AWS Console ECS section, "Clusters" -> "Create Cluster".
- Choose "Networking only (for Fargate)" if available (in newer consoles, they may simplify this).
- Give it a name (e.g., `my-microservice-cluster`). You might choose to put in a VPC and subnets (you can use default VPC for simplicity or a custom one for more control).
- The cluster will basically be a placeholder as Fargate doesn’t need EC2 container instances.

**2. Task Definition (Fargate type)**:

- In ECS, go to Task Definitions -> Create new Task Definition.
- Choose **Fargate** launch type ([How to Deploy a Spring Boot App on AWS Fargate](https://mydeveloperplanet.com/2021/10/12/how-to-deploy-a-spring-boot-app-on-aws-fargate/#:~:text=In%20step%201%2C%20choose%20Fargate,click%20the%20Next%20step%20button)).
- Configure:
  - **Task name** (e.g., `my-microservice-task`).
  - **Task Role** (IAM role for the app's AWS permissions, e.g., if app calls S3 or Secrets Manager – more on this in security section).
  - **Execution Role** (IAM role that ECS agent uses to pull image and manage logs; if you use the console, it can auto-create one named like ecsTaskExecutionRole with AmazonECSTaskExecutionRolePolicy attached).
  - **Fargate Platform Version** (use latest, e.g., 1.4.0 or LATEST).
  - **Task size**: CPU and Memory. Fargate requires you pick a combo, e.g., 0.25 vCPU & 0.5GB memory for a small app. For a Spring Boot app, you might choose 0.5 vCPU, 1GB as a starting point. Ensure memory is enough for your JVM heap plus overhead.
- **Define Container** in the task:

  - Container name (e.g., `my-microservice`).
  - Image: `123456789012.dkr.ecr.us-east-1.amazonaws.com/my-microservice:latest` (the ECR image URL).
  - Memory Limits: you can optionally set Hard/Soft limits inside the task’s total. For simplicity, you might leave this if not needed, or set as described (soft 256, hard 512 out of 0.5GB).
  - Port Mapping: `8080` (container port). With Fargate + awsvpc networking, the container gets its own ENI, so you just expose the port your app listens on.
  - (Optional) Health check command here is more for Docker to check inside container. Instead, we will rely on the load balancer for health checks. However, you could specify: health check command like `["CMD-SHELL", "curl -f http://localhost:8080/actuator/health || exit 1"]` with interval/timeout if you want ECS to directly check container health.
  - Environment Variables: e.g., set `JAVA_OPTS` or Spring profiles. Avoid putting secrets directly; if needed, use ECS’s integration with Secrets Manager (discussed later).
  - Log Configuration: choose awslogs driver to send logs to CloudWatch Logs (requires the execution role to have permissions; the AmazonECSTaskExecutionRolePolicy includes CloudWatch Logs permissions). Provide a log group name and region.

- Save the task definition.

**3. Create ECS Service**:

- In ECS console, go to your Cluster, then Services -> Create.
- Launch type: Fargate.
- Task Definition: select the one created above, choose a revision if needed.
- Platform version: LATEST (or specific).
- Cluster: ensure your cluster is selected.
- Service name: e.g., `my-microservice-service`.
- Number of tasks: e.g., 2 (to start with two containers running for high availability).
- Deployment type: Rolling update (default).
- **Networking**:
  - Choose VPC and subnets (for Fargate, must be private subnets if using a public load balancer).
  - Assign Security Group(s): likely one that allows inbound on port 8080 from the load balancer security group.
  - Enable Auto-assign public IP if using a public ALB in public subnets for the tasks (or use private subnets + NAT).
- **Load Balancer Integration**:
  - If high availability is needed, it's recommended to use an ALB (Application Load Balancer) with your ECS Service.
  - Select Application Load Balancer.
  - Create or select an existing ALB. Ensure the ALB is in public subnets (for internet-facing) and has a security group allowing HTTP/HTTPS.
  - Listener: typically HTTP (or HTTPS) on port 80 (or 443).
  - It will require you to specify a **Target Group** for ECS:
    - Create a new Target Group (for ALB) of type IP (for Fargate) on port 8080.
    - Health check path: `/actuator/health` (our Spring Boot health endpoint). You might use `/actuator/health/liveness` if you want a shallow check, but generally `/health` is fine as it aggregates.
    - The health check should expect 200 for healthy (Actuator returns 200 when status is UP; returns 503 if DOWN).
  - Back in ECS service config, select container name:port (e.g., my-microservice:8080) and the target group you just created.
- **Auto Scaling (optional at setup)**:
  - You can click "Configure Service Auto Scaling" to set up auto-scaling (or do it later). We’ll cover details in the Auto Scaling section. If doing now, you might set a target of e.g., 50% CPU target tracking.
- Review and create the service.

AWS will now launch the tasks. Each task is a running container of our microservice in Fargate.

**Verify deployment**:

- In ECS -> Cluster -> Services -> your service, check that tasks are in RUNNING state.
- In EC2 -> Target Groups, check the target health. It should show each IP (task) as healthy if `/health` returned 200.
- Access the service:
  - If ALB is set up: find the ALB’s DNS name (in EC2 -> Load Balancers). Open it in a browser (HTTP). It should route to one of the tasks.
  - If no ALB and you used public IPs, find the task’s public IP in ECS task details and hit port 8080 (not recommended for production, better to use ALB).

For example, `http://my-loadbalancer-123456.us-east-1.elb.amazonaws.com/users/1` should retrieve a user (if one exists or else 404), and `.../actuator/health` should show health status.

**ECS on EC2 (Launch type EC2)** differences:

- You’d create an ECS Cluster with EC2 capacity (either launch EC2 instances manually or attach an Auto Scaling Group).
- Use the ECS-optimized AMI or Amazon Linux 2 + ECS Agent installed.
- Task Definition: choose EC2 launch type and possibly host port mappings (host port can be 0 for dynamic or a fixed port – with dynamic, the ALB can route to the dynamic port).
- The rest is similar, but you manage EC2 sizing and scaling.
- Auto-scaling involves scaling both ASG (for EC2 count) and ECS Service (task count).

#### Option C: Manually on EC2 with Auto Scaling Group

This is an approach without containers. You can package the Spring Boot fat jar and run it directly on EC2 instances, perhaps using a startup script or a service runner (like Systemd).

However, given our microservice is Dockerized and Actuator health checks are easy to integrate with ALB, using ECS is more straightforward. Running directly on EC2 might involve:

- Setting up a Launch Template with User Data script that installs Java and runs the jar.
- An Auto Scaling Group to maintain X instances.
- An ALB for traffic and health checks (pointing to an EC2 health endpoint, e.g., same `/actuator/health`).
- S3 or CodeDeploy to deliver the jar to instances, or bake it into an AMI.

This approach is more DIY and beyond our main scope, but it’s worth noting as a possible route if containerization is not desired. For advanced use, tools like Packer can create an AMI with the app pre-installed, then ASG uses that.

**Conclusion of Deployment Section**:
We’ve chosen ECS (especially Fargate) as our target for auto-scaling. At this point, you should have a Spring Boot container running on AWS, accessible and reporting health to an ALB (or at least to ECS). Next, we’ll set up monitoring and metrics so we can observe and automatically scale this service.

---

## 3. Monitoring and Health Checks <a id="monitoring-and-health-checks"></a>

Monitoring is critical in production. We will use Spring Boot Actuator’s metrics and health endpoints, and integrate with AWS CloudWatch for logging and alarms. This section covers configuring Actuator endpoints, enabling metrics (via Micrometer) to CloudWatch, setting up CloudWatch Logs for container logs, and creating alarms and custom metrics.

### 3.1 Configuring Spring Boot Actuator Endpoints <a id="configuring-actuator-endpoints"></a>

We already enabled the health endpoint. Actuator provides more:

- `/actuator/info` – for general info (we can populate build info or custom details).
- `/actuator/metrics` – shows various metrics (requires having metrics data).
- `/actuator/loggers` – to check and modify log levels at runtime (though careful with exposure).
- `/actuator/threaddump`, `/actuator/env`, etc. – many endpoints, but not all should be exposed publicly.

**Production Tip**: Expose only what you need. For instance, you might expose:

- Health (for LB checks).
- Info (if it has non-sensitive build info).
- Metrics (if you use a monitoring system like Prometheus, but with CloudWatch we might push metrics instead).
- Maybe `/actuator/prometheus` if using Prometheus metrics scraping.
- Avoid exposing `/env` or `/beans` in production as they can leak sensitive config.

Our earlier `application.yml` snippet with `management.endpoints.web.exposure.include` controls this.

Additionally:

- If using Kubernetes liveness/readiness, Spring Boot (2.3+) will auto-configure separate health groups if `management.endpoint.health.probes.enabled=true` which we set.
- The default `/actuator/health` then includes all health indicators except those tagged as liveness/readiness only. It can be configured further, but defaults often suffice.

**Spring Boot Admin (Optional)**: Consider using Spring Boot Admin or similar to aggregate and view actuator endpoints from multiple instances in one UI if you have many microservice instances.

### 3.2 Publishing Metrics to AWS CloudWatch <a id="publishing-metrics-to-cloudwatch"></a>

AWS CloudWatch is the primary monitoring service for AWS resources and custom metrics. There are a few ways to get Spring Boot metrics into CloudWatch:

- Use **Amazon CloudWatch Agent** on EC2 (not relevant for Fargate, more for EC2) to collect metrics and logs.
- Push custom metrics via AWS SDK (CloudWatch PutMetricData).
- Use **Micrometer** with a CloudWatch Registry – this is a convenient way with Spring Boot.

**Using Micrometer with CloudWatch**:
Micrometer is the metrics library integrated with Spring Boot Actuator. By default, Spring Boot configures a MetricsRegistry (usually the composite one). If we add the CloudWatch registry dependency (`micrometer-registry-cloudwatch2` as included earlier ([Publishing Metrics from Spring Boot to Amazon CloudWatch](https://reflectoring.io/spring-aws-cloudwatch/#:~:text=CloudWatch%20so%20we%20will%20add,cloudwatch2%60%20module%20in%20our%20project))), we can configure Micrometer to publish to CloudWatch.

Steps:

1. Add dependency: `micrometer-registry-cloudwatch2`.
2. Configure AWS credentials for CloudWatch:
   - If running on ECS/EC2 with a proper IAM role, you don't need to explicitly configure keys; the IAM role’s permissions will be used.
   - Ensure the task’s IAM Role (or EC2 IAM role) has permission `cloudwatch:PutMetricData` for your namespace.
3. In `application.yml`, add CloudWatch settings:
   ```yaml
   management.metrics.export.cloudwatch:
     enabled: true
     namespace: MyMicroserviceMetrics # A namespace for your app metrics
     batchSize: 20 # how many metrics to send at once
     step: 1 minute # interval at which to send
   ```
   The namespace is like a container for all metrics from this app ([Publishing Metrics from Spring Boot to Amazon CloudWatch](https://reflectoring.io/spring-aws-cloudwatch/#:~:text=management)). For example, `MyMicroserviceMetrics` could contain metrics like jvm.memory.used, request count, etc.
4. Spring Boot will auto-configure the CloudWatch registry if it sees it on the classpath and the above properties.

**Generating Metrics**:

- Spring Boot Actuator (with Micrometer) automatically provides many metrics: CPU, memory, GC, web request timings, etc., under various metric names. The `/actuator/metrics` endpoint can list them.
- For instance, `http.server.requests` is a Timer metric for HTTP requests (with tags like method, status, endpoint).
- You can add custom metrics using `MeterRegistry` bean. e.g., create counters or timers for specific business events.
- Example: Count user registrations:

  ```java
  @Autowired
  MeterRegistry meterRegistry;

  Counter userRegistrationsCounter = meterRegistry.counter("user.registrations");
  userRegistrationsCounter.increment();
  ```

  This would create a CloudWatch metric `user.registrations` (with the specified namespace).

**CloudWatch Metrics Console**:

- Once the app is running with metrics publishing, go to CloudWatch Console -> Metrics.
- Find your namespace (e.g., "MyMicroserviceMetrics"). You should see metrics coming in (each combination of metric + dimensions).
- You can graph them, set alarms, etc.

**Alternative: CloudWatch SDK**:

- Micrometer is recommended for ease. But for deep control, you could use AWS SDK `PutMetricData` directly.
- Example: use AWS CloudWatch client in Java to push a custom metric:
  ```java
  CloudWatchAsyncClient cloudWatch = CloudWatchAsyncClient.create();
  PutMetricDataRequest req = PutMetricDataRequest.builder()
       .namespace("MyMicroserviceMetrics")
       .metricData(MetricDatum.builder()
           .metricName("ExternalServiceLatency")
           .value(123.45)
           .unit(StandardUnit.MILLISECONDS)
           .timestamp(Instant.now())
           .build())
       .build();
  cloudWatch.putMetricData(req);
  ```
  This would push a single data point. Micrometer essentially does this under the hood but batches and standardizes it.

**Note on Costs**: Custom metrics in CloudWatch have a cost per metric per month. Use a namespace to group metrics, but the cost is per unique metric time series. Publishing many metrics (like one per user or per request detail) can become costly; stick to key metrics.

### 3.3 AWS CloudWatch Logs and Alarms <a id="cloudwatch-logs-and-alarms"></a>

**Logging**:
Our Spring Boot app logs (Spring Boot uses Logback by default) can be routed to CloudWatch:

- For ECS, if we configured the **awslogs log driver** in the Task Definition, logs from the container’s stdout/stderr will go to a CloudWatch Log Group (which you named in the task definition). For example, a log group `/ecs/my-microservice`.
- Ensure the task execution role has `logs:CreateLogStream` and `logs:PutLogEvents` (the default ecsTaskExecutionRole covers this).

If using EC2:

- Installing the CloudWatch Logs agent or using CloudWatch Agent to push `/var/log/myapp.log` to CloudWatch.
- Or use a Logback appender to CloudWatch (via AWS SDK, but that’s less common since using the agent or ECS integration is easier).

**Verifying Logs**:

- Go to AWS CloudWatch Console -> Logs -> Log Groups. Find the log group (if following conventions, ECS might prefix with `/ecs/`).
- You should see log streams for each ECS task (named by ECS task ID or container ID).
- Within a log stream, you see your application logs (whatever Spring Boot printed to console).

**Setting up CloudWatch Alarms**:
Alarms in CloudWatch track a metric and perform actions if it goes out of bounds.

What metrics to alarm on for a microservice? Common ones:

- **CPUUtilization** (for EC2 instances or ECS service). High CPU might indicate need to scale up, or sustained high CPU could trigger investigation.
- **MemoryUtilization** (for ECS tasks if using Fargate or if pushing a custom metric for memory).
- **RequestCount** or **ErrorRate** – on ALB or on custom metrics. For example, if 5XX errors spike.
- **Latency** – e.g., ALB Target Response Time, or a custom app metric for response time.

**Example Alarm – High CPU on ECS Service**:
If we use ECS Service Auto Scaling with target tracking, it already uses CPU CloudWatch metrics (more on that later). But you might still set an alarm:

- Metric: `ECS/Service/CPUUtilization` (namespace AWS/ECS, dimensions cluster, service).
- Condition: Average > 80% for 5 minutes.
- Action: send notification (SNS or trigger lambda, etc.). For auto scaling, target tracking covers scaling, but alarm can notify devops.

**Example Alarm – Unhealthy Task Count**:

- Metric: `ECS/Service/UnhealthyTaskCount`.
- If > 0 for a certain period, something’s wrong (tasks failing health checks).
- Could trigger an alert to investigate.

**Alarm via CloudWatch on custom metric**:

- Suppose we have a custom metric `user.registrations` – you might alarm if count drops below a threshold (for something expected regularly) or if it spikes unexpectedly (if that indicates something wrong).
- Or an alarm on `jvm.memory.used` if memory usage approaches the container limit, indicating possible memory leak.

**CloudWatch Alarms for Auto Scaling**:

- We will explicitly discuss scaling alarms in the next section, but they are created similarly. AWS can auto-create them when you set up scaling policies (especially for target tracking ECS, AWS manages the alarms ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=With%20target%20tracking%20scaling%20policies%2C,in%20the%20number%20of%20tasks)) ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=Target%20tracking%20policies%20remove%20the,on%20the%20target%20you%20set))).

**Cross-Service monitoring**: If the microservice is part of a bigger system, consider AWS X-Ray for distributed tracing, or 3rd party APM solutions. Actuator can integrate with tracing too (Spring Cloud Sleuth, etc.), but that’s beyond our focus here.

### 3.4 Custom CloudWatch Metrics for Detailed Monitoring <a id="custom-cloudwatch-metrics"></a>

We touched on custom metrics in 3.2 using Micrometer. Let’s detail some useful custom metrics in a microservice context and how to utilize them in AWS:

**Useful Custom Metrics**:

- Business-specific counts (e.g., number of orders processed, number of messages consumed).
- Third-party API latency or error count (to monitor dependencies).
- Thread pool utilization or queue lengths (if using custom executors).
- Garbage Collection pause time (though Java metrics are already collected by Micrometer via JMX if enabled).
- Custom health check metrics (e.g., if an external dependency is down, emit a metric).

**Using Micrometer Annotations**:

- Spring Boot + Micrometer allows annotations like `@Timed` to automatically time methods, and `@Counted` (in some extensions) to count calls.
- Example:
  ```java
  @Timed(value = "service.order.placement.time", description = "Time to place order")
  public OrderResponse placeOrder(Order order) {
      // ... method logic
  }
  ```
  This would create a Timer metric "service.order.placement.time" with mean, max, count of calls.

**Custom Dimensions (Tags)**:

- Metrics can have tags (Micrometer calls them tags, CloudWatch calls them dimensions). For example, tagging metrics by region, or endpoint, or result type.
- Actuator’s `http.server.requests` already has tags like `uri` (endpoint), `status`, etc.
- Be cautious: CloudWatch treats each unique combination of metric + dimensions as a separate metric stream (with its own costs). E.g., if you have a tag for userId on a metric and you have thousands of users, that would blow up metrics count – not good. Instead, aggregate or categorize metrics to a manageable level.

**Enabling Actuator metrics**:

- Ensure `management.endpoints.web.exposure.include=metrics` (and optionally `prometheus` if scraping).
- For CloudWatch, you might not need to expose metrics over HTTP, since Micrometer pushes them directly.
- You might still expose for local debugging or if you use Prometheus/Grafana in addition.

**Visualization**:

- CloudWatch dashboards can graph metrics. You might create a dashboard for your service, showing CPU, memory, request count, error count, latency, etc.
- Each graph can be a CloudWatch metric query. For example, a line for P99 latency if you publish that, or a bar for number of errors vs successes.
- Alternatively, use third-party or open-source tools: e.g., if metrics also go to Prometheus (Micrometer can publish to multiple systems), use Grafana for rich visualization.

**Aggregating Logs as Metrics**:

- Sometimes, rather than instrumenting code, you might parse logs. CloudWatch Logs offers metric filters. For example, if your log has a line "ERROR" or a specific error code, you can create a metric filter to count occurrences of that in logs and emit a CloudWatch metric. This is a coarse way to detect anomalies (e.g., count of exceptions per minute).
- However, since Actuator and Micrometer give direct metrics, it’s usually better to use those for application metrics.

We have our monitoring in place: Actuator endpoints, metrics to CloudWatch, logs centralized, and alarms for key conditions. Next, we’ll configure AWS Auto Scaling so that when those metrics (like CPU or load) hit thresholds, AWS can automatically add or remove instances/containers.

---

## 4. AWS Auto Scaling Configuration <a id="aws-auto-scaling-configuration"></a>

Auto Scaling ensures our service can handle varying load by adjusting the number of instances or tasks. We need to consider scaling on different triggers (CPU, request count, latency), set up the scaling policies and CloudWatch alarms accordingly, and test the behavior.

### 4.1 Creating AWS Auto Scaling Groups or ECS Service Auto Scaling <a id="creating-auto-scaling-groups"></a>

Depending on the deployment choice:

- **If using ECS on EC2**:

  - You have an Auto Scaling Group (ASG) for EC2 instances (the underlying machines).
  - You also have ECS Service Auto Scaling for tasks (within the ECS service).
  - Both might need to scale: e.g., scale out tasks, then maybe add EC2 instances if capacity is low.

- **If using ECS on Fargate**:
  - No EC2 ASG to manage (Fargate tasks are serverless).
  - Only ECS Service scaling (increase or decrease task count).

We focus on **ECS Service Auto Scaling** (which applies to both ECS on EC2 and ECS on Fargate at the service level).

**ECS Service Auto Scaling** uses **Application Auto Scaling** under the hood:

- You create a scaling target (the service’s desired count).
- Then define scaling policies:
  - **Target Tracking** (e.g., keep CPU at 50%). This is like a thermostat ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=With%20target%20tracking%20scaling%20policies%2C,tasks%20running%20in%20your%20service)).
  - **Step Scaling** (cloudwatch alarm triggers steps, e.g., add 2 tasks if CPU > 70%).
  - **Scheduled Scaling** (scale at specific times, not needed for us except maybe daily cycles).

**Setting up ECS Service Auto Scaling via Console** (if not already done when creating the service):

- Go to ECS > Cluster > Service > "Auto Scaling" tab.
- Create a new Scaling policy.
- It will ask to create a Service Auto Scaling IAM Role (if not exists) – allow it (called AWSServiceRoleForApplicationAutoScaling_ECSService).
- Choose Target Tracking Policy (most common):
  - e.g., "Scale on CPU", target value 50% CPU.
  - Minimum number of tasks (e.g., 2), maximum (e.g., 10).
  - Cooldown default (e.g., 60 seconds scale out cooldown, 120 seconds scale in).
- Alternatively, choose Step Scaling:
  - Define CloudWatch alarm (or pick an existing one) e.g., CPU > 70% for 5 minutes triggers adding +1 task; CPU < 30% for 5 minutes triggers removing -1 task.
  - Step scaling gives more fine-grained control and multiple steps (like add 1 for moderate high, add 3 if extremely high).

**ASG for EC2 (if applicable)**:

- If we had an ASG for container instances, similar target tracking can be set on EC2 metrics (like average CPU of instances).
- Also, ECS has a concept of Capacity Providers (one way to link ASG to ECS tasks, so it knows to add instances when tasks need placement).

For our Fargate scenario, we skip ASG, focusing on ECS service scaling.

**Auto Scaling Group for EC2 (non-ECS)**:

- If not using ECS at all, you’d have an ASG for your EC2 running the Spring Boot app.
- You’d attach an ALB health check to the ASG so unhealthy instances are replaced.
- Policies could be CPU based or request based via ALB metrics.
- The principles are similar: define min, max, scaling policies.

### 4.2 Defining Scaling Policies (CPU, Requests, Latency, etc.) <a id="defining-scaling-policies"></a>

Choosing the right metric for scaling is crucial:

- **CPU Utilization**: Common and easy – if CPU is high, add more instances. Many apps are CPU-bound under load. ECS reports CPU for tasks; CloudWatch has it as `CPUUtilization` per service (average CPU of tasks).
- **Memory Utilization**: If app is memory-bound (or to prevent OOM), scale on Memory. CloudWatch ECS service metrics include MemoryUtilization.
- **Request Count or Load on LB**: ALB provides `RequestCountPerTarget`, which can be used to keep each instance at X requests/sec. Or you can scale on concurrent connections.
- **Latency**: ALB’s `TargetResponseTime` can be used – if p99 latency goes beyond e.g. 2 seconds, scale out (assuming it’s due to load). However, latency can also increase due to other factors (DB slow, external dependency) not solved by scaling out, so use carefully.
- **Custom metrics**: If you have a critical business metric. E.g., length of an internal queue – if it grows, scale out to handle backlog. For that, you’d push the metric and use CloudWatch alarm on it.

**Target Tracking vs Step Scaling**:

- _Target Tracking_: simpler – you say, e.g., “keep CPU at ~50%”. AWS then creates an alarm if above 50% (scale out) and below some margin (scale in) automatically ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=Target%20tracking%20policies%20remove%20the,on%20the%20target%20you%20set)). It will add/remove tasks to try to meet that target. Think of it like cruise control.
  - Good for most use cases because of simplicity.
  - It handles scale in cautiously to avoid flapping ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=,but%20scales%20in%20more%20gradually)) (scale-out fast, scale-in slower).
  - You can have multiple target metrics, but they act OR for scale-out (if any says scale out, it will) and AND for scale-in (all must indicate scale-in).
- _Step Scaling_: more control.
  - You define exact CloudWatch alarms and what to do when they trigger.
  - E.g., an alarm for CPU > 70% triggers +2 tasks, CPU > 90% triggers +4 tasks (bigger step for extreme load).
  - And another for CPU < 30% triggers -1 task.
  - This can be tuned if you know patterns of your load or want minimal oscillation.
- _Scheduled Scaling_: e.g., every day at 8am scale to 5 tasks, at midnight scale to 2 tasks (if you have predictable cycle). Not our focus, but possible to define in ECS or ASG.

**Example scaling policy**:
Let’s say our microservice is mostly CPU-bound. We choose **target tracking on CPU 50%**:

- When new load comes, CPU goes above 50%, the policy will add tasks to bring it down. If idle, CPU goes near 0%, scale in to maybe 1 or 2 tasks minimum.
- We set min tasks = 2 (for high availability), max = 10.
- If each task can handle ~50 req/s at 50% CPU, then at 10 tasks we can do ~500 req/s easily at 50% CPU each, or push to maybe 800 req/s at 80% CPU each if needed (just an illustrative number; actual capacity should be tested).

**Scaling on Request Count**:

- ALB provides a metric `RequestCountPerTarget`. You can target track this. E.g., keep ~100 requests per instance.
- AWS’s _Application Auto Scaling_ supports an ALB RequestCountPerTarget policy out of the box.
- However, note from AWS: _"The ALBRequestCountPerTarget metric for target tracking scaling policies is not supported for blue/green deployments."_ (but that is a niche case when doing ECS CodeDeploy blue/green).
- If using request count, ensure your ALB target group health is correct and evenly distributing. CPU scaling is sometimes more direct because CPU correlates with work done (for CPU-bound apps).

**Multi-metric considerations**:

- You can have multiple scaling policies, e.g., one on CPU, one on memory. But be careful: by default, they both could scale out independently (which is fine, availability first), but scale-in only happens when _all_ scale-in conditions are satisfied.
- For simplicity, one metric might suffice. If using both CPU and memory, you're basically saying “if either CPU or memory is high, add more; only remove if both are low”.

### 4.3 Configuring CloudWatch Alarms for Scaling Events <a id="configuring-cloudwatch-alarms"></a>

If using **Target Tracking**, AWS will **automatically manage** the CloudWatch alarms ([Use a target metric to scale Amazon ECS services - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html#:~:text=Target%20tracking%20policies%20remove%20the,on%20the%20target%20you%20set)):

- It will create an alarm for high metric (> target) and maybe for low metric (< target).
- These alarms will have names like `ecs-target-tracking-alarm:PolicyName:alarmHigh` etc.
- You are advised not to delete or edit these alarms manually, as they are managed by ECS.

If using **Step Scaling**, you have to create the alarms:

- Either beforehand via CloudWatch (or CloudFormation/Terraform).
- Or through the Auto Scaling policy creation in the console (which gives an interface to create a new alarm).
- Each alarm needs:
  - Metric (e.g., CPUUtilization of service).
  - Statistic (e.g., Average over all tasks).
  - Period (e.g., 60 seconds).
  - Evaluation periods (e.g., 3 data points > threshold).
  - Threshold (e.g., > 70).
  - Comparison (GreaterThanThreshold).
  - And an SNS action if you want notification (optional for scaling, not needed to scale).
- Then, in the scaling policy:
  - Link the alarm to an action: add X capacity.
  - You can specify cooldown periods after a scale-out or scale-in to stabilize.

**Alarm for Scale Out Example**:

```
AlarmHighCPU:
  Metric: ECS/CPUUtilization
  Dimensions: Cluster=..., Service=...
  Condition: Average of 3 datapoints >= 70%
  Period: 60 sec
  -> Action: Add 2 tasks
```

**Alarm for Scale In Example**:

```
AlarmLowCPU:
  Metric: ECS/CPUUtilization
  Dimensions: ...
  Condition: Average of 5 datapoints <= 20%
  Period: 60 sec
  -> Action: Remove 1 task
```

Usually give a higher number of periods for scale-in to avoid premature scale-in (hence 5 datapoints over 5 minutes in the example).

**Notification on Scaling**:

- You might want to know when scaling happens. You can configure the ASG or ECS service events to feed to an SNS or CloudWatch Event (EventBridge) that notifies you or triggers something (maybe a log of scaling events).
- ECS service will show events (in the console or CLI) like "setting desired count to X".
- CloudWatch Alarm can have SNS notifications too (like email you when scale-out alarm triggers). But if it's frequent, that could spam – perhaps better for scale-in failures or unusual conditions.

### 4.4 Testing Auto-Scaling Behavior <a id="testing-auto-scaling"></a>

After configuring, you **must test** that auto-scaling works as expected:

- **Load Testing**: Use a tool like **Apache JMeter**, **Gatling**, or **Apache Bench** to simulate load on your service. For example, simulate 100 req/sec steadily and see if it scales out.
  - JMeter can run on your machine or an EC2. If large scale (hundreds of RPS), consider distributed JMeter or an AWS service like Distributed Load Testing or third-party SaaS.
  - Keep an eye on CloudWatch metrics during the test.
- **Manual Trigger**: You can also temporarily lower the alarm threshold to force a scale out, then put it back.
- **AWS FIS (Fault Injection Simulator)**: For advanced testing, simulate instance failures or spike load events.

**During a load test**:

- Watch the ECS service in the console; it should increase tasks when CPU goes high.
- The ALB target group will register new targets as tasks start, and route traffic to them as they pass health checks.
- Monitor response times to ensure scaling is helping.

**Scale In test**:

- After the load subsides, ensure tasks scale back down (not below minimum).
- Note scale-in happens after some delay to ensure stability (target tracking waits a bit after things calm).

**What to observe**:

- Does the CPU usage drop after new tasks come? Ideally yes, spreading load.
- Is the scaling quick enough? If not, maybe adjust target or add a step scaling for faster response on sudden spikes.
- Any errors during peak? If requests spike faster than new tasks start, you might see some 503s or timeouts. If so, maybe start with a bigger cluster or use queue buffering.
- Check that when tasks are removed, the remaining can handle the lower load.

**Troubleshooting**:

- If auto-scaling didn’t trigger, check CloudWatch if metrics crossed thresholds.
- Ensure the Service Auto Scaling is enabled and not suspended.
- Ensure the ALB health check isn’t too sensitive causing instance churn (our earlier example from a blog mentioned instances being replaced due to health check issues – ensure the health check grace period in ECS is adequate for the app to start).
- If tasks fail to start (maybe due to out-of-memory), CloudWatch may show errors and ECS events will tell (fix by increasing memory or changing JVM settings).

**Real-World Scenario**: As seen in a tuning story, if health checks are misconfigured or memory is low, auto-scaling groups might cycle instances unnecessarily. Ensure:

- Health check grace periods cover startup time.
- Proper memory sizing to avoid random unhealthy kills.
- Utilize the metrics from tests to fine-tune scaling policies (maybe 50% CPU target is too high or low).

By the end of this, you should have confidence that under heavy load, AWS will add more instances, and under light load, it will remove extras, all the while your service stays healthy (or self-heals if not).

---

## 5. Infrastructure as Code (IaC) <a id="infrastructure-as-code"></a>

Manually clicking in the AWS Console is fine for initial exploration, but Infrastructure as Code allows you to **reproduce** and **version control** your environment. Here, we'll look at using **Terraform**, **AWS CDK**, and **CloudFormation** for our Spring Boot microservice deployment, focusing on automating ECS, load balancers, auto-scaling, and related resources.

### 5.1 Terraform Scripts for AWS Setup <a id="terraform-scripts-for-aws-setup"></a>

**Terraform** is an open-source IaC tool by HashiCorp, supporting AWS and many other providers. Using Terraform, you describe AWS resources in code (HCL - HashiCorp Configuration Language) and it creates/updates them.

For our microservice deployment, Terraform can manage:

- VPC, Subnets, Security Groups.
- ECS Cluster.
- ECR Repository (for completeness).
- IAM Roles (Task Execution Role, Task Role).
- ECS Task Definition.
- ALB and Target Group.
- ECS Service with Auto Scaling.

**Example Terraform structure** (simplified):

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "my_cluster" {
  name = "my-microservice-cluster"
}

resource "aws_ecs_task_definition" "my_task" {
  family                   = "my-microservice-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"   # 0.25 vCPU
  memory                   = "512"   # 0.5 GB
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "my-microservice"
      image     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/my-microservice:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-region"        = var.aws_region
          "awslogs-group"         = "/ecs/my-microservice"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}
```

Explanations:

- `aws_ecs_task_definition`: defines our container and its settings. We use `jsonencode` to avoid manual JSON for container definitions.
- `requires_compatibilities = ["FARGATE"]` indicates it's a Fargate task.
- We reference IAM roles (to be defined separately).
- We reference an existing ECR image via variables for account and region.

**IAM Roles**:
Terraform can create an `aws_iam_role` for ECS execution with the right policy, e.g.:

```hcl
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_assume.json
}

data "aws_iam_policy_document" "ecs_task_execution_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}
resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
```

This attaches the AWS-managed policy for ECS task execution (pulling images, logs, XRay, etc.).

**Load Balancer & Target Group**:

```hcl
resource "aws_lb" "my_alb" {
  name            = "my-microservice-alb"
  internal        = false
  load_balancer_type = "application"
  subnets         = aws_subnet.public[*].id  # assume these are defined
  security_groups = [aws_security_group.alb_sg.id]
}

resource "aws_lb_target_group" "my_tg" {
  name        = "my-microservice-tg"
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.main.id
  health_check {
    path                = "/actuator/health"
    matcher             = "200"
    interval            = 15
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.my_alb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_tg.arn
  }
}
```

We set up ALB on port 80 forwarding to our target group on port 8080.

**ECS Service**:

```hcl
resource "aws_ecs_service" "my_service" {
  name            = "my-microservice-service"
  cluster         = aws_ecs_cluster.my_cluster.id
  task_definition = aws_ecs_task_definition.my_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  platform_version = "1.4.0"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.app_sg.id]  # SG allowing ALB traffic
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.my_tg.arn
    container_name   = "my-microservice"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.http_listener]
}
```

We add `depends_on` to ensure the listener is created first (so target group is ready for service registration).

**Auto Scaling with Terraform**:
Terraform can also configure Application Auto Scaling for ECS:

```hcl
resource "aws_appautoscaling_target" "ecs_scaling_target" {
  service_namespace  = "ecs"
  resource_id        = "service/${aws_ecs_cluster.my_cluster.name}/${aws_ecs_service.my_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  min_capacity       = 2
  max_capacity       = 10
}
resource "aws_appautoscaling_policy" "ecs_cpu_policy" {
  name               = "cpu-target-tracking"
  service_namespace  = "ecs"
  resource_id        = aws_appautoscaling_target.ecs_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_scaling_target.scalable_dimension
  policy_type        = "TargetTrackingScaling"
  target_tracking_scaling_policy_configuration {
    target_value       = 50.0
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 60
    scale_out_cooldown = 30
  }
}
```

This sets up the target tracking policy for CPU at 50%. (Terraform uses Application Auto Scaling under the hood to attach to ECS service.)

**Running Terraform**:

- Write these configs into .tf files.
- Run `terraform init` (to download providers).
- Run `terraform plan` to see what will be created.
- Run `terraform apply` to create the infrastructure.
- With proper config, this will output the ALB DNS, etc., and you get the same result as manual steps.

The benefit: source control these files, so your infra is documented. Team members or different environments can apply the same config (with variables changes). You can also destroy (teardown) easily for testing in a sandbox.

Terraform also has community modules, e.g., `terraform-aws-modules/ecs/aws` that can simplify some of this (it codifies best practices, like creating the cluster and associated roles).

### 5.2 AWS CDK for Dynamic Provisioning <a id="aws-cdk-provisioning"></a>

**AWS CDK (Cloud Development Kit)** allows you to write IaC in programming languages (TypeScript, Python, Java, etc.). It's essentially an abstraction over CloudFormation.

Using AWS CDK for our scenario (in TypeScript, as an example):

```typescript
import * as cdk from "aws-cdk-lib";
import { Stack, StackProps, Duration } from "aws-cdk-lib";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as applicationautoscaling from "aws-cdk-lib/aws-applicationautoscaling";

class MicroserviceStack extends Stack {
  constructor(scope: cdk.App, id: string, props?: StackProps) {
    super(scope, id, props);

    // VPC (could use default or define new one)
    const vpc = ec2.Vpc.fromLookup(this, "Vpc", { isDefault: true });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, "EcsCluster", { vpc });

    // Task Role and Execution Role
    const taskRole = new iam.Role(this, "TaskRole", {
      assumedBy: new iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
      // attach policies as needed (S3, SSM, etc.)
    });
    const executionRole = new iam.Role(this, "ExecutionRole", {
      assumedBy: new iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
    });
    executionRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AmazonECSTaskExecutionRolePolicy"
      )
    );

    // Task Definition
    const taskDef = new ecs.FargateTaskDefinition(this, "TaskDef", {
      memoryLimitMiB: 512,
      cpu: 256,
      executionRole: executionRole,
      taskRole: taskRole,
    });
    taskDef.addContainer("AppContainer", {
      image: ecs.ContainerImage.fromRegistry(
        "<ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/my-microservice:latest"
      ),
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: "my-microservice" }),
      portMappings: [{ containerPort: 8080 }],
    });

    // ALB
    const albSG = new ec2.SecurityGroup(this, "AlbSG", { vpc });
    albSG.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80));

    const alb = new elbv2.ApplicationLoadBalancer(this, "Alb", {
      vpc,
      internetFacing: true,
      securityGroup: albSG,
    });
    const listener = alb.addListener("HttpListener", { port: 80 });
    const targetGroup = listener.addTargets("EcsTargets", {
      port: 8080,
      protocol: elbv2.ApplicationProtocol.HTTP,
      targets: [], // we'll attach ECS service later
      healthCheck: {
        path: "/actuator/health",
        healthyHttpCodes: "200",
      },
    });

    // ECS Service
    const serviceSG = new ec2.SecurityGroup(this, "ServiceSG", { vpc });
    // allow ALB to reach service
    serviceSG.addIngressRule(albSG, ec2.Port.tcp(8080));

    const service = new ecs.FargateService(this, "Service", {
      cluster,
      taskDefinition: taskDef,
      desiredCount: 2,
      securityGroups: [serviceSG],
      assignPublicIp: true, // or false if using NAT
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
    });
    // Attach ALB Target to ECS service
    service.registerLoadBalancerTargets({
      containerName: "AppContainer",
      containerPort: 8080,
      newTargetGroupId: "EcsTargetGroup",
      listener: ecs.ListenerConfig.applicationListener(listener, {
        protocol: elbv2.ApplicationProtocol.HTTP,
      }),
    });

    // Auto Scaling
    const scaling = service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10,
    });
    scaling.scaleOnCpuUtilization("CpuScaling", {
      targetUtilizationPercent: 50,
      scaleInCooldown: Duration.seconds(60),
      scaleOutCooldown: Duration.seconds(30),
    });
    // Optionally: scaling.scaleOnRequestCount or scaleOnMemoryUtilization
  }
}
```

The CDK code:

- Defines resources similarly to Terraform, but in code form with constructs.
- Notice how we could easily attach a scaling policy with `scaleOnCpuUtilization` – CDK provides high-level abstractions.
- We used default VPC for simplicity.
- The ECS Fargate service creation automatically dealt with some wiring (but we manually did ALB target registration to show how).
- CDK will output CloudFormation under the hood. Running `cdk deploy` creates a CloudFormation stack with these resources.

**Pros of CDK**:

- Use programming logic/loops for complex infra (e.g., create N similar services).
- Leverage IDEs and type checking (especially with TypeScript/Java, etc.).
- Easier to manage if you’re comfortable with code vs config syntax.
- Can integrate with application code repo (though some prefer infra separate).

**Cons**:

- Learning curve to understand the library classes.
- Adds a build step (you need Node or your language to synthesize templates).
- Underlying CloudFormation limits still apply.

### 5.3 Managing Resources with AWS CloudFormation <a id="managing-resources-with-cloudformation"></a>

**CloudFormation** is AWS's native IaC (declarative, in YAML/JSON). Terraform and CDK ultimately translate to CloudFormation (CDK uses it directly; Terraform uses AWS APIs without an intermediate template).

If writing directly in CloudFormation YAML, it would be similar in structure to the Terraform example, just AWS:: prefixed resource types and using intrinsic functions for ARNs and references. For brevity, we won't write out a full CloudFormation template (it would be quite verbose for ECS + ALB).

**Snippet**:

```yaml
Resources:
  EcsCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: my-microservice-cluster

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: my-microservice-task
      Cpu: "256"
      Memory: "512"
      NetworkMode: awsvpc
      RequiresCompatibilities: [FARGATE]
      ExecutionRoleArn: !GetAtt EcsExecutionRole.Arn
      TaskRoleArn: !GetAtt EcsTaskRole.Arn
      ContainerDefinitions:
        - Name: my-microservice
          Image: !Sub "${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/my-microservice:latest"
          PortMappings:
            - ContainerPort: 8080
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: /ecs/my-microservice
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs
```

(And similarly, define the ALB, TargetGroup, Listener, ECS Service with references to target group and container.)

**CloudFormation Auto Scaling** can use AWS::ApplicationAutoScaling::ScalingPolicy and Target.

One interesting addition is **CloudFormation StackSets** or nested stacks, which can help if deploying to multiple regions or multi-stack architectures.

**State Management**:

- CloudFormation state is managed by AWS (stack state), you don't worry about storing state (unlike Terraform where state file management is key).
- If a stack update fails, it can rollback (so it’s both good and tricky to manage incremental changes).

**IaC Best Practices**:

- Regardless of tool, store your IaC in source control.
- Plan changes (e.g., Terraform plan or CDK diff) for review.
- Keep production and staging config separate or parameterized, to avoid accidental cross-impact.
- Use consistent naming conventions in resources for clarity.
- Use outputs from IaC (like ALB URL output) to feed into documentation or other systems as needed.

In summary, IaC ensures consistency and is almost essential for advanced setups. For our microservice, using Terraform or CDK means we can spin up the whole environment with one command, making it easier to deploy to new stages or implement disaster recovery (recreate in a new region if needed).

---

## 6. CI/CD Pipeline for Deployment <a id="ci-cd-pipeline-for-deployment"></a>

Continuous Integration and Continuous Deployment (CI/CD) pipelines automate building, testing, and deploying our microservice. This section discusses setting up a CI/CD pipeline using tools like **GitHub Actions** or **Jenkins**, automating Docker builds and ECS deployments, and strategies for rolling updates and zero downtime.

### 6.1 CI/CD with GitHub Actions or Jenkins <a id="ci-cd-github-actions-jenkins"></a>

We'll outline both approaches:

**GitHub Actions** (if your code is on GitHub):

- GitHub Actions allows writing workflows in YAML in your repo under `.github/workflows`.
- You can have an action trigger on push or PR to master/main (CI for tests), and on tagging or merging to deploy branch (for CD).
- Example:

  ```yaml
  name: CI-CD Pipeline

  on:
    push:
      branches: [main]

  jobs:
    build-and-test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up JDK 17
          uses: actions/setup-java@v3
          with:
            distribution: "temurin"
            java-version: "17"
        - name: Build with Maven
          run: mvn clean verify
        - name: Build Docker Image
          run: docker build -t my-microservice:${{ github.sha }} .
        - name: Push to ECR
          env:
            AWS_REGION: us-east-1
            ECR_REPOSITORY: my-microservice
            AWS_ACCOUNT_ID: ${{ secrets.AWS_ACCOUNT_ID }}
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          run: |
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
            docker tag my-microservice:${{ github.sha }} $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:${{ github.sha }}
            docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:${{ github.sha }}
    deploy:
      needs: build-and-test
      runs-on: ubuntu-latest
      steps:
        - name: Deploy to ECS
          env:
            AWS_REGION: us-east-1
            CLUSTER: my-microservice-cluster
            SERVICE: my-microservice-service
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          run: |
            # Update ECS service to use new image (here using latest git commit tag)
            aws ecs update-service --cluster $CLUSTER --service $SERVICE \
              --force-new-deployment --region $AWS_REGION
  ```

  In this simplified workflow:

  - We check out code, set up JDK, run tests (`mvn verify`).
  - Build Docker image tagged with commit SHA.
  - Push to ECR (requires AWS creds in GitHub secrets for a user/role with ECR access).
  - Then deploy: in ECS, to deploy a new image, one way is to push image with a unique tag and call `update-service --force-new-deployment` which tells ECS to refresh tasks (which will pull the latest image). This works if the Task Def is configured with `:latest` tag in ECR, or you can register a new Task Def revision with the new image tag and update service to that (more controlled).
  - The above uses `force-new-deployment` which essentially restarts tasks with the same task def (so if using `:latest`, it fetches the new image).
  - For production, consider versioning images and task definitions explicitly.

- You might also integrate tagging/versioning: e.g., on git tag, push a Docker image with that tag and update a production service.

**Jenkins**:

- Jenkins would have similar stages: checkout code, build, test, build image, push to ECR, update ECS.
- Use Jenkins plugins or pipeline (Jenkinsfile with declarative pipeline).
- Ensure Jenkins has AWS credentials (via environment variables or AWS credential providers).
- Jenkins can also integrate with AWS CodeDeploy or other services if not using ECS.

Example Jenkinsfile snippet (declarative):

```groovy
pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'my-microservice'
        AWS_ACCOUNT_ID = credentials('aws-account-id') // using Jenkins credentials store
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Build & Test') {
            steps {
                sh 'mvn clean verify'
            }
        }
        stage('Docker Build') {
            steps {
                script {
                    IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
                sh "docker build -t $ECR_REPO:${IMAGE_TAG} ."
            }
        }
        stage('Push to ECR') {
            steps {
                sh "aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
                sh "docker tag $ECR_REPO:${IMAGE_TAG} $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:${IMAGE_TAG}"
                sh "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:${IMAGE_TAG}"
            }
        }
        stage('Deploy to ECS') {
            steps {
                sh """
                   aws ecs update-service --cluster my-microservice-cluster --service my-microservice-service \
                   --force-new-deployment --region $AWS_REGION
                   """
            }
        }
    }
}
```

**AWS CodePipeline/CodeBuild**:

- Alternatively, AWS CodePipeline and CodeBuild could be used. CodeBuild to build/test, and then deploy via CodeDeploy or direct ECS integration. AWS provides an "ECS Blue/Green Deploy" action that integrates with CodeDeploy for zero downtime (more complex but powerful for safe deploys).

### 6.2 Automating Docker Builds and Deployments <a id="automating-docker-builds-deployments"></a>

The CI/CD examples above already show Docker build automation. Some points to highlight:

- **Docker Build Caching**: To speed up builds, you can use caching mechanisms. In GitHub Actions, use actions/cache to cache `~/.m2` (Maven dependencies) so that `mvn package` is faster. Similarly caching Docker layers by pulling previous image (if possible).
- **Multi-Arch builds**: If you needed to support ARM and AMD (some AWS Graviton use ARM), consider using `docker buildx` to build multi-arch images or have separate builds.
- **Deployment Automation**:
  - For ECS, AWS CLI as shown is straightforward. Another way is to use the AWS SDK (e.g., a Java program or Python script to register new task def and update service).
  - There are also GitHub Actions for ECS deploy (e.g., `aws-actions/amazon-ecs-deploy-task-definition` action).
  - For Elastic Beanstalk, you'd use the EB CLI or AWS CLI to create new app versions and update environment.
  - For an Auto Scaling Group (non-ECS) scenario, one could use user data to pull latest artifact on boot, but more robust is using CodeDeploy: push new version to instances gradually.

**Zero-Downtime Considerations**:

- ECS with a load balancer can do rolling updates without downtime: by default, it will launch new tasks, wait for them to be healthy, then stop old tasks. If configured right, clients won’t notice (maybe a slight increase in latency during scale-out).
- Ensure health checks are solid (so that new tasks only get traffic when ready).
- If using blue/green (like ECS has an option to use CodeDeploy to shift traffic between old/new tasks, or using separate target groups), you can achieve near-zero downtime with validation hooks.
- For non-ECS, say using ASG, you can similarly do rolling deploy (spin up new instances via new launch template, shrink old ones). CodeDeploy can assist with in-place or blue/green updates on ASGs or EC2.

**Rollback**:

- Have a rollback plan: if new deployment has issues, how to revert quickly? With ECS, perhaps keep previous task definition and set service back to it (or re-run pipeline with previous image tag).
- Automated detection: in advanced pipelines, you might run smoke tests after deploy and auto rollback if they fail.

**CI for Infrastructure**:

- Not only app code, but also IaC should be in CI. E.g., if using Terraform, you might have a pipeline that runs `terraform apply` when changes occur (with manual approval for prod). Similarly for CDK with `cdk deploy`.
- This ensures infra changes (security group tweaks, scaling changes) are tracked and applied systematically.

### 6.3 Rolling Updates and Zero-Downtime Deployments <a id="rolling-updates-zero-downtime"></a>

As touched on, rolling updates are key to not interrupt service:

- **ECS Rolling Update**: When updating the service (new task def revision or force new deployment):
  - It follows the deployment configuration (in ECS service settings you can adjust maxSurge, maxUnavailable for tasks).
  - By default, ECS might bring up 1 extra task (10% extra by default, I think) and terminate old tasks after new ones are ready. For example, with desired 10 tasks, it might temporarily go to 11 then back to 10.
  - Ensure your service code can handle two versions briefly (backwards compatibility on interfaces/db if needed).
- **Database Migrations**: Often part of deployments; ensure if a new version requires a DB migration, it’s handled in a way that doesn’t break old version if they’re running concurrently (e.g., additive schema changes).
- **Session State**: If the microservice was stateful (it shouldn’t be ideally; use external store for session), ensure sticky sessions or external session store so that if one task goes down, users aren’t logged out. With stateless microservices (REST APIs), usually not an issue.
- **Zero downtime trick for Spring Boot**: Spring Boot Actuator has `/actuator/health` so we rely on that. We might also consider a preStop hook (if on K8s) to deregister before shutting down. On ECS, when a task is set to stop, the ALB is informed to stop sending traffic (connection draining) for a grace period, which is usually enough.

**Blue/Green Deployments**:

- For absolute zero downtime and safer deploys, consider blue/green:
  - You create a separate environment (blue = current live, green = new version), then switch traffic.
  - In ECS, AWS CodeDeploy can orchestrate this with two target groups: one for current, one for new, then shift traffic gradually and allow testing.
  - This is more complex to set up, but can eliminate issues where new version fails by keeping old around until confirmed.
- Canary releases: a variant where you send a small % of traffic to new tasks (maybe by duplicating service with 1 task receiving 5% traffic via weighted target groups) to test in production.

**Jenkins and Blue/Green**:

- Jenkins can integrate with AWS CodeDeploy to orchestrate ECS blue/green (there are Jenkins plugins or just use AWS CLI to create a CodeDeploy deployment).

**Continuous Deployment Safeguards**:

- Use deployment rings or environments (dev -> staging -> prod).
- Possibly require a manual approval step for production deploy in the pipeline.
- Automated tests at each stage (unit, integration, load test on staging, etc.).
- Monitoring hooks: e.g., after deploy, auto-check if error rate increased (some advanced pipelines can query CloudWatch or an APM tool to decide success).

By automating CI/CD, deployments become routine and less error-prone, enabling frequent releases without manual toil.

---

## 7. Security and Best Practices <a id="security-and-best-practices"></a>

Security is woven through all steps: from code to AWS infrastructure. We will cover IAM roles, secrets management, and general Spring Boot and AWS security best practices.

### 7.1 Using IAM Roles and Policies for Access Control <a id="iam-roles-and-policies"></a>

AWS IAM roles should be used instead of long-term credentials:

- **ECS Task Role**: This is the IAM role that the application container assumes. In our setup, we created one. Grant it least privilege:
  - If the app needs to read from S3, give it only read access to the specific bucket or path.
  - If it needs DB credentials from Secrets Manager, give it permission to `GetSecretValue` for that secret ARN.
  - Avoid using root account credentials or IAM users with wide privileges in the app. Roles are automatically provided to the EC2 instance or ECS container via metadata service, and AWS SDK picks it up.
- **ECS Execution Role**: Already covered – should have the AmazonECSTaskExecutionRolePolicy which includes ECR pull and CloudWatch logs. Usually no need to change it, unless using additional features (like AWS XRay – then add XRay write permissions, etc.).
- **Instance Profile (if EC2)**: If running on EC2 (non-Fargate), the EC2 instances should have an IAM role that allows ECS agent to register, and perhaps the app uses that too unless you separate (but if the app runs directly on EC2, that’s its role). Again, least privilege.
- **CI/CD IAM user/role**: If using GitHub Actions, you're likely using AWS Access Key (user or OIDC). If Jenkins on EC2, attach an IAM role to that Jenkins instance. Keep CI limited: e.g., access to ECR, ECS update, maybe Secrets Manager for pipeline if needed. Don’t give it full admin.
- **Developer Access**: Control who can push to environments via code. Use IAM or GitHub branch protections to restrict who can deploy to production.

**Security Groups**:

- At network level, ensure SGs restrict access appropriately. For example, your microservice might only be accessed via ALB, so the SG on ECS tasks allows ingress from ALB’s SG, not from the world. The ALB SG allows 0.0.0.0/0 on 80/443 (or better, restrict to IPs if internal).
- DB SG: if your service talks to a DB on RDS, ensure the DB SG allows the ECS tasks SG.

**VPC and Isolation**:

- Keep production in its own VPC or at least separate subnets from dev/test.
- Use private subnets for ECS tasks so they aren't directly exposed, only ALB in public (if internet facing).
- NACLs (network ACLs) can add another layer, though SGs suffice in many cases.

**Least Privilege Principle**:

- Review IAM policies: e.g., if using Secrets Manager, an example policy for task role might be:
  ```json
  {
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue"],
    "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:MyMicroserviceDBCreds-*"
  }
  ```
  So it cannot retrieve other secrets not named accordingly.
- For S3: limit to specific bucket and actions (GetObject, PutObject if needed).
- For SQS/SNS: specify the ARN of the queue/topic, not "\*".

**Auditing**:

- Use AWS CloudTrail to log who did what (it will log if someone updates ECS, etc.).
- Use AWS Config or third-party tools to check for open SGs or overly permissive roles.

### 7.2 Encrypting Sensitive Data with AWS Secrets Manager <a id="encrypting-sensitive-data"></a>

Avoid storing sensitive config (DB passwords, API keys) in plaintext in configs or code. **AWS Secrets Manager** (or Parameter Store) should be used:

- We saw an AWS Prescriptive Guidance scenario of using Secrets Manager to manage DB credentials. The idea is to call Secrets Manager at runtime to fetch the secret.
- Spring Boot can integrate with Secrets Manager via Spring Cloud AWS or using the Secrets Manager JDBC driver for databases.

**Fetching secrets in Spring Boot**:

- Option A: **Spring Cloud AWS Secrets Manager Config**: by adding `spring-cloud-starter-aws-secrets-manager-config`, you can have Spring Boot automatically fetch secrets and treat them like config properties. For example, a secret named `myapp/db` with JSON `{"username":"foo","password":"bar"}` can be mapped.
  - You then reference `spring.datasource.username = #{secret:myapp/db:username}` in config (the exact syntax might differ, but Spring Cloud AWS supports this).
- Option B: Use AWS SDK in a @Configuration class:
  ```java
  @Configuration
  public class SecretConfig {
      @Bean
      public DataSource dataSource() {
          String secretName = "prod/MyMicroserviceDB";
          SecretsManagerClient client = SecretsManagerClient.create();
          GetSecretValueResponse secretValue = client.getSecretValue(r -> r.secretId(secretName));
          String secretString = secretValue.secretString();
          // parse JSON or plain text
          JSONObject json = new JSONObject(secretString);
          String url = json.getString("jdbcUrl");
          String user = json.getString("username");
          String pass = json.getString("password");
          DataSource ds = DataSourceBuilder.create()
                        .url(url).username(user).password(pass).build();
          return ds;
      }
  }
  ```
  This way, at startup, it retrieves the secret and configures the DataSource. Secrets Manager ensures the secret is stored securely and your code only gets it at runtime (over TLS).
- Option C: **ECS integration**:
  - As per AWS docs, ECS allows specifying secrets in the task definition. For example, in the container definition, instead of giving an environment variable value, you give `"valueFrom": "arn:aws:secretsmanager:...:secret:MySecret"` and in the container, that env var will have the secret value.
  - This is very convenient. You would just set env `SPRING_DATASOURCE_PASSWORD` to come from Secrets Manager. The app then uses it normally.
  - Ensure correct platform version and permissions (platform 1.4+ for JSON key, we can just store the password as a single secret or a JSON and reference a key).
  - The task execution role will need permission to fetch that secret, or the task role (depending on how ECS implements it, likely execution role since fetch happens at startup).
  - This approach means no code change in app – ECS injects the secret as env var.

**AWS Systems Manager Parameter Store** is a cheaper alternative for plain config values and can also be used with ECS in similar way. But Secrets Manager provides rotation and is intended for sensitive data.

**Encrypting at Rest and In Transit**:

- Secrets Manager secrets are encrypted at rest (AWS manages that by default with KMS).
- Ensure any config files (if you absolutely must have a secret in a file) are at least encrypted if in VCS or use tools like git-crypt, but strongly prefer not to have them there at all.
- Use SSL/TLS for any calls (e.g., if your service calls an external API, ensure https).

**Database Encryption**:

- If using RDS, enable encryption (it’s mostly transparent).
- Use IAM auth for RDS if possible (then the app would use a token rather than a password, but that’s more complex and often using Secrets Manager is fine).

### 7.3 Spring Boot and AWS Security Best Practices <a id="spring-boot-aws-security"></a>

Finally, some general best practices and hardening tips:

**Spring Boot App Security**:

- If your microservice has any authentication/authorization, use Spring Security to secure endpoints (maybe the service is internal behind ALB, but if not, secure it).
- If it's public API, implement proper auth (OAuth2, JWT, etc.) – beyond scope, but vital.
- Sanitize inputs to prevent SQL injection (use JPA or parameterized queries) and validate data to protect against XSS, etc. (though as an API, XSS mainly if data flows to frontends).
- Keep Spring Boot and dependencies up to date with security patches. E.g., update Spring Boot version if a CVE is announced.
- Use tools like OWASP Dependency Check or Snyk in CI to catch vulnerable dependencies.

**AWS Security**:

- Use **AWS WAF (Web Application Firewall)** on the ALB if exposing to internet – can help block common attacks or limit abuse.
- **Shield / Shield Advanced** for DDoS protection on ALB (AWS by default Shield standard).
- **CloudWatch Alarms on security events**: e.g., alarm if too many 4XX/5XX (could indicate an attack).
- **VPC Flow Logs**: optional, to monitor traffic for anomalies.
- If using AWS API Gateway + Lambda instead of ECS, you could take advantage of auth at the gateway, but we stick to ECS here.

**Secrets in Code**:

- Ensure no AWS keys or passwords are hardcoded. Use IAM roles as said.
- Redact sensitive info from logs. E.g., if an exception contains sensitive info, consider a filter to not log it or sanitize.

**Monitoring and Alerts for Security**:

- AWS GuardDuty can be enabled to alert on unusual API calls or EC2 instance anomalies.
- VPC can have endpoints for S3/SM to avoid traffic going over internet.

**One IAM gotcha**: If your ECS tasks need to call other services, ensure they don’t accidentally get more access. E.g., using a wildcard resource for S3 can be dangerous (task could read any bucket if compromised). Always scope resources in IAM policies.

**CORS (if API)**:

- If this microservice is directly called from browsers, configure CORS properly to only allow trusted origins.
- If internal (only other servers call it), maybe disable CORS or it’s not relevant.

**Penetration Testing**:

- Consider doing a pentest or using scanner tools on your deployed endpoint (some companies have to do this for compliance).

**Dependency Vulnerability**:

- Spring Boot actuator has /health endpoint open – that’s fine, but do not expose /heapdump or /env publicly, as those can leak info.
- Use management server port/credentials if necessary to segregate Actuator endpoints.
- Remove any test consoles or default passwords (some apps have H2 console, etc., but not in a typical microservice).

By adhering to these practices, your microservice will be resilient not just in performance but also against security threats. Security is an ongoing process: keep auditing and improving it.

---

## 8. Final Testing and Optimization <a id="final-testing-and-optimization"></a>

We have built, deployed, scaled, and secured our microservice. Before wrapping up, it's crucial to test under production-like conditions and optimize for cost and performance. This section covers load testing, debugging scaling issues, and fine-tuning for optimal performance.

### 8.1 Load Testing with AWS Auto Scaling <a id="load-testing-with-auto-scaling"></a>

Now that auto-scaling is configured, perform thorough **load tests** to validate:

- The application can handle expected peak loads.
- Auto-scaling triggers appropriately and in time.
- No resource (CPU, memory, DB connections) becomes a bottleneck or fails under load.

**Tools**:

- **Apache JMeter**: Create a test plan simulating realistic usage patterns (varied endpoints, think time between requests, concurrent users). For heavy load (thousands of req/s), you may need multiple machines or an AWS service like **AWS Distributed Load Testing** or even using **AWS Fargate** to run JMeter in parallel.
- **Gatling**: If you prefer Scala DSL for load tests, or k6 (JavaScript based) – any tool is fine, ensure it can scale the load you need.

**Scenarios to test**:

- **Steady ramp-up**: gradually increase load and see at what point new instances kick in. For example, ramp from 0 to 500 req/s over 10 minutes.
- **Spike load**: suddenly go from 50 req/s to 500 req/s. See if auto-scaling reacts quickly or if there's a short period of high latency/ errors.
- **Sustained high load**: run at high level for 30 minutes or an hour – ensure system stabilizes (no memory leaks, no accumulating errors).
- **Scale down**: reduce load to near zero, and watch system scale back down smoothly without dropping any in-flight requests.

**Observations**:

- **CloudWatch metrics** during tests: CPU, Memory, target response time, request count. See how closely the auto-scaling kept CPU near target.
- **Application logs**: watch for errors or warnings (maybe an external service rate limit hit under high load, etc.).
- **Response times**: Analyze JMeter/Gatling results for percentiles. Ensure 95th/99th percentile latencies are within acceptable range (e.g., if SLA is 2 seconds for 99th percentile).
- If using JMeter, you can integrate it with CloudWatch metrics (just manually correlating timestamps or use JMeter PerfMon plugin on server if EC2).

**Tweaking after tests**:

- If CPU was only ~30% at max load and you had max instances running, maybe you over-provisioned or target too low – could raise target to use fewer instances (cost saving).
- If response time spiked before scale-out happened, maybe lower the target CPU (so it scales out sooner) or consider step scaling for faster reaction on sudden spikes.
- If DB CPU or connections maxed out, that’s beyond ECS – need to scale DB or optimize queries.
- Check Garbage Collection: If GC was an issue (see CloudWatch/Actuator metrics for GC time), maybe adjust heap size or GC algorithm (e.g., if using G1GC by default which is fine for most cases).
- Verify no significant memory leaks – memory usage should plateau or cyclic but not keep growing beyond expected.

**Cost considerations**:

- While load testing, be mindful of cost – running 10 tasks of a service and large load instances for JMeter can incur costs. But a short test is usually fine. Use lower regions (e.g., us-east-1 which is cheaper than some).
- After tests, remember to scale back or shut down test resources.

### 8.2 Debugging Scaling Issues <a id="debugging-scaling-issues"></a>

Despite careful setup, things can go wrong. Some issues and how to address:

**Issue: Auto-scaling not happening or too slow**:

- Check if CloudWatch metrics are delayed. By default, ECS service metrics have 1-minute granularity. If you need faster, you might push custom metrics or use Enhanced Monitoring (like ECS now supports 30-second metrics if I recall for CPU? Or maybe not, 1 min is standard).
- If using target tracking and a sudden spike, it might take one interval to see it and scale. Consider a step scaling policy for rapid changes: e.g., if CPU > 80% one data point, add one task immediately (besides target tracking).
- Ensure the service's maximum isn’t too low. If max is 4 and you need 10, it will hit ceiling.
- Check Service events in ECS (they might say "unable to scale: provisioning tasks failed" etc., maybe hitting AWS account limits like Fargate concurrent tasks or ECR pull rate limit).

**Issue: Tasks stuck in PROVISIONING/PENDING**:

- Possibly no free IP or CPU in cluster (if EC2).
- If Fargate, maybe hitting limits or resource unavailability (rare).
- Check ECS Capacity Provider settings if any.

**Issue: New tasks start but are unhealthy**:

- If container can't start or Actuator health returns DOWN (maybe DB not reachable). That would cause ALB health check to fail and ECS might kill the task.
- Check task logs for exceptions on startup.
- Increase health check grace period if needed (ECS service has health check grace period setting, e.g., 60 seconds to ignore health check on new tasks until they warm up).
- If DB connection pool is exhausted as new tasks come (each task making too many connections), tune the pool size or ensure DB can handle more connections (Aurora has auto-scaling for read replicas if needed, etc.).

**Issue: Flapping (scale in and out repeatedly)**:

- Maybe target tracking set too tight or step thresholds overlapping.
- Increase cooldowns.
- Ensure the CloudWatch alarm for scale-in uses `breaching` > X periods, to avoid scale in during a transient lull.
- Check if workload is spiky; sometimes you need to allow a buffer (e.g., keep a minimum that covers typical spikes without needing to scale every minute).
- Investigate the mention from the tuning blog: instances were replaced with no apparent reason. That was ASG replacing instances due to health check possibly failing. Ensure health check is robust (maybe the app responded slow due to GC and missed a heartbeat).
- Possibly use the ALB latency metric as a condition to not scale in if it’s high (i.e., if latency still high, don't scale in even if CPU dropped, indicating requests in flight).

**Logs and Traces**:

- In difficult cases, distribute the load and see logs of each instance. If one instance has errors (maybe specific data causes a bug), it might skew metrics or health.
- Use distributed tracing (e.g., AWS X-Ray or Sleuth/Zipkin) to find if certain operations slow down under load.

**Memory issues**:

- If using too much memory, tasks might get OOM-killed. ECS will mark it as Exit code 137 typically. Check CloudWatch Logs for OOM Kill from kernel.
- Solutions: allocate more memory or tune the app memory. E.g., use `-Xmx` to ensure heap fits within container memory with headroom. If container has 512MB, don't let JVM use more than say 300-400MB heap, leaving rest for Metaspace, stack, etc.
- Could use `-XX:MaxRAMPercentage` (in Java 11+) to e.g. 75% so it auto-sizes.

**Thread pool exhaustion**:

- If using an async server (Netty or Tomcat with NIO, likely not an issue), but if you have limited thread pool (like a fixed threadpool handling some tasks), ensure it's sized for load.
- Check Actuator metrics like `executor.pool.size` if you instrumented any.

By systematically analyzing metrics and logs, you can root-cause scaling issues and iterate on configuration.

### 8.3 Performance Tuning and Optimization <a id="performance-tuning-optimization"></a>

Finally, optimizing the system:

- **JVM Tuning**:
  - Choose a suitable garbage collector. G1GC is default and usually good. For very latency-sensitive (and if using Java 17, consider ZGC or Shenandoah if needed).
  - Set `-Xms` (initial heap) to a reasonable value to avoid too many resizes; often equal to `-Xmx` in container environments to avoid surprises.
  - Enable container awareness flags (Java 11+ does by default). For Java 8, use `-XX:+UseContainerSupport` and `-XX:MaxRAMPercentage`.
  - Monitor GC logs if needed (can add `-Xlog:gc:gc.log` and send to CloudWatch via sidecar/agent).
- **Spring Boot Tuning**:
  - If startup time is an issue (for scale-out latency), consider trimming classpath (do you need all starters? Remove unused).
  - Use Spring Boot 3 native image (GraalVM) for faster startup if extreme (though then memory usage might drop, trade-offs).
  - Tune Tomcat threads if using Tomcat (server.tomcat.max-threads property). Default 200 is often fine.
- **Database**:
  - Use connection pool (HikariCP default in Spring Boot) and monitor its usage (Actuator metrics for Hikari).
  - If high load, consider read replicas for reads, or caching layers (Redis) for frequent reads to offload DB.
- **Caching**:
  - Implement caching where possible (Spring Cache with Redis/Memcached for expensive operations).
  - This reduces load on DB or external APIs.
- **Optimize code hotspots**:
  - Profilers or even analyzing logs can show if some operation is slow. E.g., an external API call could be the bottleneck; maybe make it async or batch calls.
  - Use asynchronous processing for non-critical path tasks (e.g., if after handling a request you need to call another service but can do it in background).
- **Cost Optimization**:
  - After seeing real traffic, adjust instance sizes or counts. Perhaps 2 vCPU tasks are more efficient than 4x 0.5 vCPU tasks due to less overhead.
  - Use AWS Compute Savings Plans or ECS on spot instances (for EC2 launch type) if appropriate.
  - Turn off dev/test environments when not needed (use Terraform to spin up on demand, etc.).

**Documentation and Knowledge Sharing**:

- Document these optimizations and lessons (like, how much RPS one task can handle with config X).
- Prepare runbooks for on-call: e.g., if traffic spikes beyond auto-scaling, what to do (maybe raise max or shard traffic).
- Keep diagrams updated: architecture diagram of microservice, AWS components (ECS, ALB, RDS, etc.), and data flows. This helps new team members quickly understand the setup.

**Real-world scenario wrap-up**:
Recall how tuning the instance type and heap in the earlier blog excerpt improved performance and reduced errors ([How we tuned the performance of Spring Boot applications on AWS](https://blog.requirementyogi.com/tuned-performance-spring-boot-on-aws/#:~:text=Upgrade%20the%20instance%20type)). Apply a similar approach:

- Baseline, change one factor at a time (instance size, heap, etc.), test, and measure.
- The result in that case: moving from t4g.small to t4g.medium dropped error count and improved response ([How we tuned the performance of Spring Boot applications on AWS](https://blog.requirementyogi.com/tuned-performance-spring-boot-on-aws/#:~:text=Upgrade%20the%20instance%20type)). Setting `-Xmx` appropriately further improved stability.
- This iterative tuning is key to reach optimal performance per cost.

---

**Conclusion:** You have now built a Spring Boot microservice with comprehensive health checks and metrics, deployed it on AWS with a scalable, resilient architecture. You’ve integrated infrastructure as code for repeatability, set up CI/CD for agility, enforced security best practices, and fine-tuned the system through rigorous testing. With this guide, you can confidently develop and maintain cloud-native Spring Boot services that meet high standards of availability and performance.
