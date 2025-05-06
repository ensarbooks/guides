# Building Spring Boot Microservices with Elasticsearch, Kibana, and More

## Introduction

Microservices architecture involves building an application as a suite of small services, each running independently and communicating via APIs ([Spring | Microservices](https://spring.io/microservices#:~:text=Microservices%20are%20a%20modern%20approach,manageable%20pieces%2C%20independent%20of%20others)). Spring Boot makes it straightforward to create these standalone services, with embedded servers and minimal configuration, allowing developers to iterate quickly ([Spring | Microservices](https://spring.io/microservices#:~:text=With%20Spring%20Boot%2C%20your%20microservices,ready%20to%20go%20in%20minutes)). In this guide, we will walk through a step-by-step approach to building an advanced microservices system with Spring Boot. We will cover how to set up multiple Spring Boot services, enable them to discover each other, and communicate through RESTful APIs. We will also implement centralized logging and monitoring using the ELK stack (Elasticsearch, Logstash, Kibana) so that logs from all services can be searched and visualized in one place. Additionally, we will establish correlation IDs and distributed tracing (with tools like OpenTelemetry/Zipkin) to trace requests across services for debugging and performance analysis.

Security is a crucial aspect: we will apply OAuth2 with JWT tokens to secure service APIs and discuss best practices like using a centralized identity provider and stateless authentication. Each microservice will manage its own data, showcasing integration with both PostgreSQL (relational database) and MongoDB (NoSQL) to demonstrate polyglot persistence. To ensure our system is robust and performant, we'll introduce resilience patterns such as circuit breakers, retries, and bulkheads using Spring Cloud and Resilience4j, and share performance tuning tips (caching, connection pooling, etc.). Finally, we will containerize the microservices with Docker and deploy them to Kubernetes, discussing deployment strategies and considerations for scaling, resilience, and security in production.

Throughout this guide, **best practices** and optimizations will be highlighted. By the end, you will have a comprehensive blueprint for building and deploying Spring Boot microservices with enterprise-grade capabilities in logging, tracing, security, and resilience.

## Setting Up a Microservices Architecture with Spring Boot

Building a microservices architecture starts with splitting the system into multiple independent services. Each microservice should implement a specific business capability and **follow the Single Responsibility Principle** – one service’s failure or change should not heavily impact others ([Eureka Server: The Heart of Microservice Communication](https://www.mindbowser.com/microservices-with-eureka/#:~:text=Each%20service%20in%20the%20architecture,can%20have%20its%20own%20database)). For example, an e-commerce application might be composed of an **Order Service**, **Inventory Service**, **Payment Service**, and **User Service**, each with its own database and logic. To get started, you can use Spring Initializr to bootstrap each service project with the necessary dependencies (e.g., Spring Web, Spring Data JPA, etc.) ([Spring | Microservices](https://spring.io/microservices#:~:text=With%20Spring%20Boot%2C%20your%20microservices,ready%20to%20go%20in%20minutes)). This generates baseline Spring Boot applications that are ready to run.

**Project Structure:** Organize your codebase such that each microservice is a separate Spring Boot application (it could be in its own repository or module). For instance, create modules or folders like `order-service/`, `inventory-service/`, etc. Each will have its own `pom.xml` (or Gradle config) including Spring Boot starters for web, data, etc., and will produce an independent executable JAR. It’s common to define a parent Maven POM to manage common dependencies and versions (especially Spring Boot and Spring Cloud versions) across services.

**Main Application Class:** Each service has a main class annotated with `@SpringBootApplication`. For example, an Order Service main class might look like:

```java
package com.example.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
```

This class boots up the Spring context and the embedded server (Tomcat by default for web applications). At this stage, you can run each microservice on a different port (Spring Boot will default to 8080; you can override `server.port` in each service’s configuration to avoid clashes).

**Configuration Management:** In a microservices setup, it's important to externalize configuration (like database URLs, credentials, etc.). Initially, you can use each service’s `application.properties` or `application.yml`. For example, in `order-service/src/main/resources/application.yml`:

```yaml
spring:
  application:
    name: order-service
server:
  port: 8081
```

This sets a unique service name and port. We will introduce **service discovery** shortly so that services can find each other by name instead of hardcoding URLs. In a real scenario, you might use a Spring Cloud Config Server or Kubernetes ConfigMaps for centralized config, but for now we keep it simple with local configs.

**Separate Databases:** Ensure each microservice has its own database or schema. For example, Order Service might use a PostgreSQL database for orders, while Inventory Service uses MongoDB for product catalog data. This independence improves modularity and scaling, and it aligns with microservices best practices (each service manages its own data) ([Eureka Server: The Heart of Microservice Communication](https://www.mindbowser.com/microservices-with-eureka/#:~:text=Each%20service%20in%20the%20architecture,can%20have%20its%20own%20database)).

**Build and Run:** You can build all services (e.g., with Maven) and run them. Verify each service starts on its designated port and perhaps expose a basic health endpoint (Spring Boot Actuator’s `/actuator/health` can be used by adding the dependency). At this point, the services are up but not yet interacting. Next, we will implement REST APIs and allow them to communicate.

## Implementing RESTful Services and Inter-Service Communication

Each microservice should expose a well-defined **RESTful API** for its functionality. Spring Boot with Spring Web makes it easy to create REST endpoints using `@RestController`. Let’s say our **Inventory Service** needs to provide an endpoint to retrieve product stock by product ID. We can create a controller like:

```java
@RestController
@RequestMapping("/api/inventory")
public class InventoryController {

    @GetMapping("/stock/{productId}")
    public ResponseEntity<Integer> getStock(@PathVariable String productId) {
        int stockLevel = ... // fetch from database or service
        return ResponseEntity.ok(stockLevel);
    }
}
```

This defines a GET endpoint `/api/inventory/stock/{productId}` that returns the stock quantity for a given product. Similarly, an **Order Service** might have an endpoint like `POST /api/orders` to place a new order.

When microservices need to call each other (e.g., Order Service checking stock via Inventory Service), there are a few patterns for **inter-service communication**:

- **Synchronous REST calls:** One service calls another over HTTP using a REST client. Spring provides `RestTemplate` (in Spring Framework) and the newer `WebClient` (in Spring WebFlux) for making HTTP calls. Spring Cloud also offers **OpenFeign**, a declarative HTTP client, which can simplify calling other services by interface. We can also utilize Ribbon or Spring Cloud LoadBalancer to do client-side load balancing when we have service discovery.

- **Asynchronous messaging:** Services communicate via messaging systems (Kafka, RabbitMQ, etc.), which decouples producers and consumers. This is useful for events (e.g., an Order Placed event consumed by other services). We will focus on REST calls in this guide for simplicity, but keep in mind messaging is an option for certain use-cases.

For **synchronous calls** in our example, suppose Order Service needs to get product stock from Inventory Service before creating an order. Without service discovery, you would have to know the Inventory Service’s base URL (hostname and port) and call it. However, hardcoding URLs is brittle; using service discovery (like Eureka, covered next) will allow lookup by service name.

Let's illustrate using Spring Cloud OpenFeign, which integrates well with Eureka for dynamic discovery. First, include the dependency `spring-cloud-starter-openfeign` in your Order Service. Then define a Feign client interface:

```java
@FeignClient(name = "inventory-service")  // 'inventory-service' is the service name registered in Eureka
public interface InventoryClient {
    @GetMapping("/api/inventory/stock/{productId}")
    Integer getStock(@PathVariable("productId") String productId);
}
```

When Eureka is set up, Feign will use the service registry to find an instance of **inventory-service** and call the `/api/inventory/stock/{id}` endpoint. In the Order Service code, you can autowire this `InventoryClient` and use it as if it were a normal Java service. For example:

```java
@Service
public class OrderService {
    private final InventoryClient inventoryClient;
    public OrderService(InventoryClient inventoryClient) { this.inventoryClient = inventoryClient; }

    public Order createOrder(OrderRequest request) {
        Integer stock = inventoryClient.getStock(request.getProductId());
        if (stock != null && stock > 0) {
            // proceed to create order and reduce stock...
        } else {
            throw new OutOfStockException();
        }
    }
}
```

If you prefer not to use Feign, you can use `RestTemplate` with a `@LoadBalanced` annotation (provided by Spring Cloud). For example:

```java
@Autowired
@LoadBalanced  // allows resolving service names via Eureka
private RestTemplate restTemplate;
...
Integer stock = restTemplate.getForObject("http://inventory-service/api/inventory/stock/{id}",
                                         Integer.class, productId);
```

Here, the URL uses `inventory-service` as a hostname, which Ribbon or Spring Cloud LoadBalancer will intercept and resolve to an actual host:port from the service registry ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=Spring%20Cloud%20makes%20it%20very,services%20using%20Load%20Balanced%20RestTemplate)). This way, Order Service doesn’t need to know if Inventory Service runs on port 8082 or 8083, etc. The **client-side discovery** mechanism will query Eureka and load-balance requests across available instances ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=We%20can%20use%20Netflix%20Eureka,ID%20to%20invoke%20REST%20endpoints)) ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=Spring%20Cloud%20makes%20it%20very,services%20using%20Load%20Balanced%20RestTemplate)).

In summary, define REST controllers for each service’s API and use Spring’s HTTP clients (RestTemplate/WebClient or Feign) to call other service APIs. Synchronous communication is straightforward but introduces tight coupling; be mindful of timeouts and failure handling (we will address resilience patterns later). Next, let’s set up Eureka for service registration and discovery so that our services can dynamically find each other.

## Service Discovery with Eureka

In a microservices system, service instances may come and go (for scaling or updates), and they often run on dynamic addresses (especially in container or cloud environments). **Service discovery** solves the problem of how services find each other without hard-coded endpoints ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=We%20can%20use%20Netflix%20Eureka,ID%20to%20invoke%20REST%20endpoints)). Netflix Eureka is a popular service registry that allows services to register themselves and discover others by logical names.

**Setting up Eureka Server:** We will create a dedicated Spring Boot application to act as the Eureka Server (service registry). Add the dependency `spring-cloud-starter-netflix-eureka-server` to this project. In the main application class, enable Eureka server:

```java
@SpringBootApplication
@EnableEurekaServer
public class ServiceRegistryApplication {
    public static void main(String[] args) {
        SpringApplication.run(ServiceRegistryApplication.class, args);
    }
}
```

The `@EnableEurekaServer` annotation activates the Eureka service registry in this application ([Getting Started | Service Registration and Discovery](https://spring.io/guides/gs/service-registration-and-discovery#:~:text=You%20first%20need%20a%20Eureka,shows%20the%20server%20application)). By default, Eureka Server will attempt to register itself as a client too, which is not needed for a stand-alone registry. We disable that in configuration and set a fixed port. In `application.yml` for the registry:

```yaml
spring:
  application:
    name: eureka-server
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

These settings ensure the Eureka server doesn’t try to register with itself and runs on port 8761 (a common default for Eureka) ([Getting Started | Service Registration and Discovery](https://spring.io/guides/gs/service-registration-and-discovery#:~:text=spring%3A%20application%3A%20name%3A%20eureka,registry%3A%20false)). Now you can run this Service Registry application. Eureka provides a web dashboard at `http://localhost:8761` where you can see registered services (it will be empty initially). Once running, other microservices can register to it.

**Enabling Eureka Clients:** For each microservice (Order, Inventory, etc.), add the dependency `spring-cloud-starter-netflix-eureka-client`. You don’t necessarily need a special annotation (Spring Boot will detect the dependency and register with Eureka), but it’s good practice to specify the Eureka server URL and a service name in configuration:

```yaml
spring:
  application:
    name: inventory-service # The name used in Eureka registry
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/ # URL of Eureka Server
```

Now, when the Inventory Service starts, it will contact the Eureka server at the given URL and register itself under the name **inventory-service**. Similarly, the Order Service would have `spring.application.name: order-service` and point to the same Eureka server. Eureka clients by default use **heartbeat** mechanism to keep their registration alive and to inform Eureka of their status.

When both Order Service and Inventory Service are up and registered, you can verify via the Eureka dashboard (on Eureka Server’s UI) that **ORDER-SERVICE** and **INVENTORY-SERVICE** are listed as UP instances. At this point, your Feign client or RestTemplate calls using the service name (as shown earlier) will work through Eureka. The client-side load balancer will query Eureka’s registry to resolve `inventory-service` to an actual IP and port ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=We%20can%20use%20Netflix%20Eureka,ID%20to%20invoke%20REST%20endpoints)).

([Pattern: Client-side service discovery](https://microservices.io/patterns/client-side-discovery.html)) **Client-Side Service Discovery Pattern:** The diagram illustrates how services register with Eureka and how a client (e.g., Order Service) queries Eureka to find available instances of another service (Inventory Service) before making a request ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)) ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=We%20can%20use%20Netflix%20Eureka,ID%20to%20invoke%20REST%20endpoints)). In this **client-side discovery** pattern, the service client is “registry-aware” and does the load balancing. Eureka acts as the **Service Registry** where each service instance (A, B, C) registers itself and is discoverable by others ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)).

Eureka also provides some additional features:

- **Health Checking:** Eureka can perform basic health checks. Spring Boot Actuator can integrate with Eureka so that if a service goes DOWN (health check fails), Eureka marks it unavailable.
- **Self-Preservation:** Eureka has a mode to handle network partitions, protecting registrations if too many clients miss heartbeats (to avoid mass eviction during network glitches).
- **Replication:** In production, you would run multiple Eureka servers (a cluster) for high availability ([Getting Started | Service Registration and Discovery](https://spring.io/guides/gs/service-registration-and-discovery#:~:text=In%20a%20production%20environment%2C%20you,configuring%20the%20Eureka%20Server%20here)). They replicate registration info between them.

With Eureka in place, our microservices are decoupled from hard-coded URLs. We can scale the Inventory Service horizontally (multiple instances); they will all register under the same service name, and Eureka will list all instances. The Order Service’s client calls will round-robin or use a load balancing strategy across them automatically. This dynamic discovery is essential in cloud environments where services may scale up/down.

At this stage, our microservices can communicate and discover each other. Next, we’ll implement centralized logging so that as these services interact, we can trace what's happening across the whole system.

## Configuring Centralized Logging with Logback and Logstash

In a microservices setup, logs are scattered across many services. During debugging or auditing, it’s invaluable to aggregate these logs in one place with clear context. We will use the **ELK stack** (Elasticsearch, Logstash, Kibana) for centralized logging. Spring Boot uses Logback as the default logging framework, which we can configure to send logs to Logstash, which in turn will push them to Elasticsearch. Kibana will be used to visualize and search the logs.

**Logback Configuration:** Instead of logging only to console or local files, we’ll configure Logback to send logs to Logstash over a network socket. One convenient way is using the **Logstash Logback Encoder** library. Add the dependency to each microservice’s pom:

```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.3</version> <!-- choose the latest compatible version -->
</dependency>
```

This provides Logback appenders that can encode logs as JSON for Logstash. Next, create a `logback-spring.xml` in the `src/main/resources` of the service (Spring Boot will auto-load this). Here’s an example configuration for Logback to send logs via TCP:

```xml
<configuration>
    <appender name="LOGSTASH" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
        <remoteHost>localhost</remoteHost>        <!-- Logstash host -->
        <port>5044</port>                         <!-- Logstash port (TCP input) -->
        <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
            <providers>
                <timestamp />
                <logger />
                <thread />
                <level />
                <message />
                <logstashMarkers />
                <arguments />
                <mdc />            <!-- Include Mapped Diagnostic Context (for correlation IDs) -->
                <context />
            </providers>
        </encoder>
    </appender>

    <root level="INFO">        <!-- Log level threshold -->
        <appender-ref ref="LOGSTASH" />
    </root>
</configuration>
```

In this config, we define a `LOGSTASH` appender of type `LogstashTcpSocketAppender` that sends JSON-formatted logs to `localhost:5044` ([Send Spring Boot Logs Directly to Logstash With No File | Better Stack Community](https://betterstack.com/community/questions/send-spring-boot-logs-directly-to-logstash-with-no-file/#:~:text=%3Cappender%20name%3D%22LOGSTASH%22%20class%3D%22net.logstash.logback.appender.LogstashTcpSocketAppender%22%3E%20%3CremoteHost%3Elocalhost%3C%2FremoteHost%3E%20%3C%21,logger)) ([Send Spring Boot Logs Directly to Logstash With No File | Better Stack Community](https://betterstack.com/community/questions/send-spring-boot-logs-directly-to-logstash-with-no-file/#:~:text=%3Croot%20level%3D%22INFO%22%3E%20%3Cappender,root)). We include various data in the JSON (timestamp, logger name, thread, level, the message, arguments, and MDC). The MDC is important because it will carry contextual data like our correlation ID (we will set that up soon). By attaching this appender to the root logger, all logs of INFO level or above will be sent to Logstash. (You can also keep a Console appender for local debugging if you like, or adjust log levels per package as needed.)

With this in place, whenever the microservice logs something (using `Logger.info()` etc.), the log is serialized to JSON and sent to the Logstash listener. For example, a log message in JSON might look like:

```json
{
  "@timestamp": "2025-03-15T10:15:30.123Z",
  "level": "INFO",
  "logger": "com.example.order.OrderService",
  "thread": "http-nio-8081-exec-3",
  "message": "Created order 12345 for product 987",
  "mdc": {
    "CorrelationId": "abc123-def456-ghi789"
  }
}
```

Here we see the timestamp, log level, which class logged it, thread, the message, and an MDC field for `CorrelationId` (more on this in the next section).

**Setting Up Logstash:** We need a Logstash instance to receive these logs. Logstash is typically configured with input, filter, and output sections. For a simple setup, we can configure Logstash with a **TCP input** plugin for port 5044 to receive the JSON lines. For example, `logstash.conf`:

```ruby
input {
  tcp {
    port => 5044
    codec => json_lines    # decode incoming JSON logs
  }
}
filter {
  # (Optional) add filters here, e.g., parse fields or add tags
}
output {
  elasticsearch {
    hosts => ["http://localhost:9200"]    # Elasticsearch URL
    index => "spring-boot-logs-%{+YYYY.MM.dd}"   # daily index pattern
  }
}
```

This tells Logstash to listen on TCP 5044, expect JSON log lines ([Send Spring Boot Logs Directly to Logstash With No File | Better Stack Community](https://betterstack.com/community/questions/send-spring-boot-logs-directly-to-logstash-with-no-file/#:~:text=input%20,)), and then output to Elasticsearch on `localhost:9200` (default ES port) with an index named `spring-boot-logs-YYYY.MM.dd` (the date pattern creates a new index each day) ([Send Spring Boot Logs Directly to Logstash With No File | Better Stack Community](https://betterstack.com/community/questions/send-spring-boot-logs-directly-to-logstash-with-no-file/#:~:text=output%20,)). Make sure Elasticsearch is running and Logstash can connect to it.

Start Logstash with this configuration (e.g., `bin/logstash -f logstash.conf`). Now, when your Spring Boot microservice emits a log, it will be sent to Logstash and then stored in Elasticsearch index `spring-boot-logs-2025.03.15` (for example). In the Elasticsearch document, all those fields (timestamp, level, logger, message, etc.) become indexed fields.

**Verifying Log Flow:** You can verify logs are flowing by querying Elasticsearch directly (for example, using curl or Kibana). A quick check via CLI:

```bash
curl -X GET "http://localhost:9200/spring-boot-logs-*/_search?pretty=true&q=message:Created"
```

This would search across the log indices for logs with “Created” in the message. If everything is set up, you should see search results with your JSON log entries ([Send Spring Boot Logs Directly to Logstash With No File | Better Stack Community](https://betterstack.com/community/questions/send-spring-boot-logs-directly-to-logstash-with-no-file/#:~:text=Step%206%3A%20Verify%20Logs%20in,Elasticsearch)).

Centralized logging via ELK gives us **real-time aggregated logs**. Even if we have five instances of Order Service and three of Inventory Service, all their logs end up in Elasticsearch, which we can search and analyze from one UI. In the next section, we will look at using Kibana to easily explore these logs. But before that, we will incorporate **Correlation IDs** in our logging, so that log entries from different services that belong to the same transaction can be tied together.

## Sending Logs to Elasticsearch and Visualizing Them in Kibana

We have configured Logback and Logstash to ship logs to Elasticsearch. Now, we will set up Kibana to visualize those logs and discuss some best practices for log management.

**Elasticsearch Index and Mapping:** The logs are stored in indices named `spring-boot-logs-YYYY.MM.dd`. Each index contains log documents with fields like `@timestamp`, `level`, `logger`, `message`, etc. By default, Elasticsearch will infer mappings (data types) for these fields (for example, `@timestamp` as date, maybe `level` as text or keyword). It’s often useful to ensure consistent mappings (for sorting by timestamp, aggregating by level, etc.), but for now default is fine.

**Setting up Kibana:** Kibana is the visualization UI for Elasticsearch. After installing or running Kibana (e.g., accessible at `http://localhost:5601`), do the following in Kibana:

1. Navigate to **Stack Management > Index Patterns** (Kibana UI may vary by version, but look for “Index Patterns” or “Data Views”).
2. Click “Create Index Pattern”. Enter the pattern name as `spring-boot-logs-*` to capture all daily indices.
3. Kibana will detect indices matching that pattern (e.g., `spring-boot-logs-2025.03.15`). Choose `@timestamp` as the time filter field when prompted.
4. Save the index pattern.

Now Kibana knows about our log indices. Go to the **Discover** section in Kibana, and select the “spring-boot-logs-\*” index pattern (if not already selected). You should start seeing log entries streaming in (assuming logs are being generated). You can filter by fields; for example, filter where `level` is “ERROR” to see error logs, or search for a specific text in messages.

**Visualizing Logs:** Kibana’s Discover view lets you search and view individual log documents. You can expand a log entry to see all its fields. For instance, you might filter `service.name: inventory-service AND level: ERROR` to see all error logs from the Inventory Service. (Note: we have `spring.application.name` configured per service; we can send that to Logstash too. If it’s not automatically in MDC or context, we might want to add a custom field for service name in the log output. One way is to set a property in Logback config like `<property name="serviceName" value="${spring.application.name:-}"/>` and include it in the JSON.)

Kibana also allows creating visualizations. For logs, a common one is a **time histogram** of log counts, or a pie chart of logs by level (INFO, WARN, ERROR). But more valuable is using Kibana’s filtering to debug flows. For example, if an error happened while processing an order, and we have a correlation ID for that order flow, we can search by that correlation ID to see _all_ logs from all services that participated in that transaction. This is immensely helpful in pinpointing issues across microservices.

**Best Practices in Logging:**

- **Log Levels:** Use appropriate log levels (`DEBUG`, `INFO`, `WARN`, `ERROR`). Avoid logging sensitive data (like passwords, tokens) in logs. In production, you might run at INFO or WARN level to reduce noise, and use DEBUG only for troubleshooting due to verbosity.
- **Structured Logging:** We are already outputting logs as JSON, which is good. Use key-value pairs in your log messages or MDC for important variables (like `orderId=12345`) instead of burying them in unstructured text. This way, you can search and aggregate by those fields in Kibana.
- **Correlation:** Always include a correlation or trace ID (discussed next) so that related log entries can be grouped. This is critical for debugging in distributed systems ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)).
- **Retention:** Logs can grow rapidly. Plan index lifecycle management – for example, keep 7-14 days of logs in Elasticsearch (depending on storage and compliance needs) and archive or delete older indices. Elasticsearch ILM can automate moving old indices to cheaper storage or deleting them.
- **Centralize Error Alerts:** Kibana (with X-Pack or using Watcher) can trigger alerts, or use an external tool, if too many errors occur. This can complement your monitoring.

At this point, our microservices are emitting logs that we can search in Kibana. Let’s improve our logging by adding **Correlation IDs**, which will greatly simplify tracing a single transaction across multiple services in those logs.

## Implementing Correlation IDs to Track Service Calls

When a single client request flows through multiple microservices, it is useful to tag all logs for that flow with a unique **Correlation ID** (also known as a trace ID). This way, you can search logs by that ID and retrieve the complete picture of what happened across services ([Home | Java By Examples](https://www.javabyexamples.com/logging-with-request-correlation-using-mdc#:~:text=In%20this%20tutorial%2C%20we%27ll%20look,logs%20for%20a%20specific%20request)) ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)). Without correlation IDs, debugging an issue that spans services (e.g., an Order request that involves Inventory and Payment services) would require manually guessing time windows or matching messages, which is error-prone.

**What is a Correlation ID?** It’s typically a UUID or similar unique string generated at the start of a request and passed along to every service involved. Every log line during that request carries the ID (often in the MDC). Think of it as a “request identifier.” In a monolith, you might rely on thread context or built-in tracing, but in microservices, since a single transaction hops between processes, we explicitly propagate this context.

**Generating and Propagating the ID:** In a typical web service, the correlation ID is generated at the edge (for example, by an API Gateway or the first service that receives the client request). It can be passed as an HTTP header (commonly named something like `X-Correlation-ID` or `X-Request-ID`). Downstream services should pass it forward when they call other services.

In our setup, if we don’t have an API gateway, each service can generate the ID if it’s the origin of a request (e.g., when an HTTP request comes in from outside or from an upstream service without an ID). We’ll implement a **Servlet Filter** in each service to handle this:

1. Check incoming HTTP request for an `X-Correlation-ID` header.
2. If present, use that value; if not, generate a new UUID.
3. Put this ID into the MDC (Mapped Diagnostic Context) so that our Logback appender will automatically include it in all log statements on the current thread.
4. Also set the `X-Correlation-ID` header on the HTTP response (so the client can know the ID, useful for client-side logging or troubleshooting).
5. Ensure that after the request is processed, we clear the MDC to avoid leaking the ID to other requests (especially in thread pools).

Here’s a simple implementation using a filter:

```java
@Component
@Order(1)  // ensure this runs early
public class CorrelationIdFilter extends OncePerRequestFilter {

    public static final String CORRELATION_HEADER = "X-Correlation-ID";

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        try {
            String corrId = request.getHeader(CORRELATION_HEADER);
            if (corrId == null || corrId.isEmpty()) {
                corrId = UUID.randomUUID().toString();
            }
            MDC.put("CorrelationId", corrId);  // put in MDC
            response.setHeader(CORRELATION_HEADER, corrId);
            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}
```

This filter (registered as a Spring `@Component`) will assign a CorrelationId for every request. We use `MDC.put("CorrelationId", corrId)` which makes it available to Logback’s `%X{CorrelationId}` in our log pattern ([Home | Java By Examples](https://www.javabyexamples.com/logging-with-request-correlation-using-mdc#:~:text=response%2C%20FilterChain%20filterChain,%7D)) ([Home | Java By Examples](https://www.javabyexamples.com/logging-with-request-correlation-using-mdc#:~:text=In%20MDCFilter%2C%20we%27re%20putting%20the,run%C2%A0even%20if%20an%20exception%20occurs)). Recall we included `<mdc/>` in our Logback JSON encoder, which will include all MDC entries. So now every log line in our services will have a field for `CorrelationId`. We also attach the correlation ID to the HTTP response for transparency.

If using OpenFeign or RestTemplate to call other services, we need to propagate the header. For RestTemplate, one can use an interceptor like:

```java
@Bean
public RestTemplate restTemplate(RestTemplateBuilder builder) {
    return builder.interceptors((request, body, execution) -> {
        String corrId = MDC.get("CorrelationId");
        if (corrId != null) {
            request.getHeaders().add(CorrelationIdFilter.CORRELATION_HEADER, corrId);
        }
        return execution.execute(request, body);
    }).build();
}
```

For Feign, you can define a `RequestInterceptor` that adds the header from MDC to outgoing requests:

```java
@Bean
public RequestInterceptor correlationIdFeignInterceptor() {
    return template -> {
        String corrId = MDC.get("CorrelationId");
        if (corrId != null) {
            template.header(CorrelationIdFilter.CORRELATION_HEADER, corrId);
        }
    };
}
```

This ensures that when Order Service calls Inventory Service, it passes along the same `X-Correlation-ID` header it received (or generated). The Inventory Service’s filter will see that header and use it instead of generating a new one, thereby keeping the ID consistent across services ([java - Intercept requests and responses to get/add correlation id with spring boot - Stack Overflow](https://stackoverflow.com/questions/70963120/intercept-requests-and-responses-to-get-add-correlation-id-with-spring-boot#:~:text=I%27m%20developing%20a%20microservice%20and,MDC%20for%20logging%20purposes)) ([java - Intercept requests and responses to get/add correlation id with spring boot - Stack Overflow](https://stackoverflow.com/questions/70963120/intercept-requests-and-responses-to-get-add-correlation-id-with-spring-boot#:~:text=public%20boolean%20preHandle,return%20true%3B)).

**Logging with Correlation ID:** Now, when a single user action triggers logs in multiple services, all those log entries share one CorrelationId. In Kibana, you can simply search by that ID (which might look like `f781dc3e-30f5-4e9f-9b5e-3f63bada1df0`) and you’ll immediately get the chronological trace of what happened across the system. For instance:

- `OrderService - CorrelationId f781dc... - Received create order request`
- `InventoryService - CorrelationId f781dc... - Checking stock for product 987`
- `InventoryService - CorrelationId f781dc... - Stock is available`
- `OrderService - CorrelationId f781dc... - Order 123 created successfully`

From these, you can piece together the journey of that request. This is a manual form of **traceability** which greatly aids debugging.

**Using Spring Cloud Sleuth:** It’s worth mentioning that Spring Cloud Sleuth can automate much of this. Sleuth, by including `spring-cloud-starter-sleuth`, will automatically generate a trace ID and span IDs for you and inject them into logs (it modifies the logging pattern to include `[traceId, spanId]`) ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Spring%20Cloud%20Sleuth%20%28%60org.springframework.cloud%60%3A%60spring,automatically%20instruments%20common%20communication%20channels)) ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=,etc)). It also propagates these over Feign/RestTemplate calls if using the Spring Cloud context. Since we will discuss distributed tracing next, know that if you use Sleuth, you essentially get a correlation mechanism out-of-the-box (with the trace ID serving as the correlation ID). Our manual approach above is akin to implementing a subset of Sleuth’s functionality.

**Cleaning up MDC:** One must be careful to clear the MDC (as done in the `finally` block of the filter) ([Home | Java By Examples](https://www.javabyexamples.com/logging-with-request-correlation-using-mdc#:~:text=try%20%7B%20MDC.put%28,%7D)) ([Home | Java By Examples](https://www.javabyexamples.com/logging-with-request-correlation-using-mdc#:~:text=In%20MDCFilter%2C%20we%27re%20putting%20the,run%C2%A0even%20if%20an%20exception%20occurs)). In web servers, thread pools reuse threads for multiple requests, and MDC is stored per thread. If not cleared, the next request on the same thread might accidentally log the old request’s ID. Our filter’s `finally` ensures each request’s ID is removed after completion.

With correlation IDs in place, our logs in Elasticsearch become significantly more powerful. We can trace transactions end-to-end by a single identifier. This sets the stage for full **distributed tracing**, which not only correlates logs but also measures execution times across services. We’ll cover that next.

## Distributed Tracing with OpenTelemetry or Zipkin

While correlation IDs in logs help to trace requests, **distributed tracing** systems provide a more structured and visual approach to see how a request propagates through multiple services, along with timing information. Tools like **Zipkin** and **OpenTelemetry** (often with Jaeger or other backends) allow you to capture spans of execution and build a timeline of a request.

**Concepts:** In distributed tracing:

- A **trace** represents a single end-to-end request (identified by a trace ID, which can be our correlation ID).
- A trace is composed of **spans**. A span is a named unit of work in a service (e.g., “InventoryService checkStock() method”). Spans have timestamps for start and finish, so you can see how long each step took ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)).
- Spans can be nested or sequential, capturing the call graph through microservices. For example, trace ID _X_ might have a parent span in Order Service (“handleOrderRequest”) and a child span for the Inventory Service call (“GET /api/inventory/stock”) and maybe another for Payment Service call, etc.

**Using Spring Cloud Sleuth + Zipkin:** Spring Cloud Sleuth (prior to Spring Boot 3) integrates tracing (using Brave under the hood) into Spring Boot applications easily. By adding the dependency `spring-cloud-starter-sleuth`, your application will:

- Generate a trace ID for each incoming request and create an initial span.
- Propagate the trace and span IDs via headers (`X-B3-TraceId`, etc., in Zipkin’s B3 propagation standard, or the newer W3C Trace Context).
- Log entries will automatically include the trace and span IDs for context (Sleuth adds them to MDC) ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=,etc)).
- If you also add `spring-cloud-starter-zipkin`, the app will send the collected tracing data to a Zipkin server.

In Spring Boot 2.x, by default, Sleuth looks for a Zipkin server at `http://localhost:9411` (the default Zipkin address). You can configure in properties:

```yaml
spring.zipkin.base-url: http://zipkin-host:9411
spring.zipkin.sender.type: web # use HTTP to send spans
spring.zipkin.enabled: true
```

With these, the service will report spans to Zipkin. Zipkin Server can be run as a separate application (e.g., using the openzipkin/zipkin Docker image). Once running, you can open the Zipkin UI (usually at `http://zipkin-host:9411`) and use it to search traces by trace ID or service name.

When our Order Service calls Inventory Service with Sleuth enabled, here’s what happens:

- Order Service receives a request, Sleuth assigns a trace ID (say `abcd1234`) and a span ID for the “OrderService handling” span.
- Order Service calls Inventory Service via REST; Sleuth adds headers `X-B3-TraceId: abcd1234` and `X-B3-SpanId` (and `X-B3-ParentSpanId` equal to the Order span’s ID) to the HTTP call ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=in%20a%20system%2C%20through%20ingress,it%27s%20easy%20to%20associate%20semantically)).
- Inventory Service receives the request; Sleuth in Inventory sees the trace headers and continues the trace. It creates a new span (with parent span as the Order span). All logs in Inventory will carry the same trace ID.
- Both services send span data to Zipkin. Zipkin now can display a trace “abcd1234” that shows two spans: one in Order Service, one in Inventory Service, with timing info.

Zipkin’s UI would show a **timeline**: e.g., OrderService span took 120ms, inside it InventoryService span took 80ms, etc. It also offers a **dependency diagram** to show service call relationships (e.g., OrderService -> InventoryService) based on tracing data.

Zipkin and Sleuth greatly ease troubleshooting latency issues since you can pinpoint where time is spent. For instance, if an inter-service call is slow, the tracing UI will highlight that span as the longest portion.

**OpenTelemetry with Spring Boot:** OpenTelemetry (OTel) is the modern CNCF standard for tracing (and metrics and logs). Spring Boot 3 / Spring Cloud 2022.0 (and above) have shifted to use Micrometer Tracing (which can use Brave or OpenTelemetry) ([Let’s use OpenTelemetry with Spring](https://spring.io/blog/2024/10/28/lets-use-opentelemetry-with-spring#:~:text=The%20Power%20of%20Micrometer%E2%80%99s%20Observation,API)) ([Let’s use OpenTelemetry with Spring](https://spring.io/blog/2024/10/28/lets-use-opentelemetry-with-spring#:~:text=We%20wanted%20to%20introduce%20the,Brave%29%20and%20OpenTelemetry)). You can use OpenTelemetry in two ways:

- **Manual instrumentation or OTel Java Agent:** Attach the OpenTelemetry Java Agent to your microservice at startup. It will auto-instrument common libraries (including Spring, JDBC, etc.). You configure it to send data to an OpenTelemetry Collector or Jaeger.
- **Micrometer Tracing + OTel:** Add `io.micrometer:micrometer-tracing` and the OpenTelemetry exporter (`io.opentelemetry:opentelemetry-exporter-otlp`) to your app. Spring will then publish traces via OTLP. You run an OpenTelemetry Collector to receive these and forward to a backend (could be Zipkin, Jaeger, or others).

For example, to use OpenTelemetry and see traces in Jaeger:

- Run a Jaeger instance (which can accept OTLP or Zipkin format).
- Configure your Spring Boot app (with Micrometer Tracing) with:

```yaml
management.tracing.enabled: true
management.tracing.sampling.probability: 1.0 # sample all requests for tracing (in production, you might sample less)
management.otlp.tracing.endpoint: http://otel-collector:4317 # if using collector, or Jaeger’s OTLP endpoint
```

- The app will send trace data to the collector. Jaeger UI (similar to Zipkin) will show traces.

OpenTelemetry’s advantage is vendor-neutral, and a broad ecosystem support. Micrometer’s advantage in Spring is it lets you switch tracers easily (Brave/Zipkin or OpenTelemetry) without changing your code instrumentation ([Let’s use OpenTelemetry with Spring](https://spring.io/blog/2024/10/28/lets-use-opentelemetry-with-spring#:~:text=Introducing%20Micrometer)) ([Let’s use OpenTelemetry with Spring](https://spring.io/blog/2024/10/28/lets-use-opentelemetry-with-spring#:~:text=We%20wanted%20to%20introduce%20the,Brave%29%20and%20OpenTelemetry)).

**Viewing Traces:** Whether using Zipkin or Jaeger (or another APM tool), the result is a visual trace. For example, a **trace view screenshot** in Zipkin would list services and their spans with timestamps. It might show:

```
TraceID: abcd1234 (duration: 150 ms)
|--- Order-Service: handleOrder (150 ms)
     |--- Inventory-Service: GET /stock (80 ms)
```

This tells us the Inventory check took 80ms out of the 150ms total for the order handling. If another service (Payment) was called, it would be another span.

Additionally, trace systems often capture metadata (tags) on spans, like HTTP status codes, error flags, method names, etc. Sleuth by default tags HTTP method and response status, for instance. OpenTelemetry has semantic conventions for such tags.

**Correlation with Logs:** We now have two parallel mechanisms – log correlation and distributed tracing. It’s good to link them. For instance, the trace ID from Sleuth is the same as our correlation ID. We ensured our logs carry the correlation ID in MDC, which Sleuth also does. Spring Sleuth will include the trace ID in logs by default (in the format `[traceId=abcd1234, spanId=...]`). If using OpenTelemetry, you may integrate with logging via MDC as well (OpenTelemetry Java can inject the trace ID into MDC; there are appenders for this). Spring Boot 3’s default log format even includes tracing info if tracing is enabled ([Tracing :: Spring Boot](https://docs.spring.io/spring-boot/reference/actuator/tracing.html#:~:text=Tracing%20%3A%3A%20Spring%20Boot%20Correlation,Boot%20will%20include%20correlation)) ([Logging :: Spring Boot](https://docs.spring.io/spring-boot/reference/features/logging.html#:~:text=Correlation%20ID%3A%20If%20tracing%20is,The%20log%20message)).

Thus, if you see an error log in Kibana with traceId `abcd1234`, you can go to Zipkin/Jaeger, find trace `abcd1234`, and see the timeline of what happened around that error (and vice versa).

**Sampling:** One consideration – capturing every trace can be heavy in high-throughput systems. You might configure sampling (e.g., only trace 10% of requests). Even then, having correlation IDs in logs ensures you can always correlate logs, but you might not have a trace for every single request if sampling is applied. For debugging specific incidents, you could increase sampling or use log-based triggers.

In summary, adding distributed tracing provides deep insights into the performance and behavior of your microservices. Spring’s integration (Sleuth or Micrometer Tracing) makes it relatively easy to implement. Our microservices can now be observed via logs and traces, which greatly helps in maintaining and troubleshooting the system.

## Security Best Practices including OAuth2 and JWT Authentication

Security is paramount in microservices, especially as each service exposes network APIs. We will focus on using OAuth2 with JWTs to secure service-to-service and user-to-service communication, as it’s a common and robust approach.

**Overview of OAuth2 and JWT in Microservices:** In a typical OAuth2 setup for microservices:

- There is an **Authorization Server/Identity Provider** (like Keycloak, Okta, Auth0, or a custom OAuth2 server) that handles user authentication and issues tokens.
- Microservices act as **Resource Servers** that accept **Bearer** tokens (usually JWTs) to authorize requests. They delegate the authentication of the token to the issuer by validating the token’s signature and claims.
- Optionally, there may be an API Gateway that handles authentication and routing, but even with a gateway, it’s wise to secure the services themselves.

**JSON Web Tokens (JWT):** A JWT is a self-contained token that includes claims (user identity, roles/scopes, etc.) and is signed by the issuer. Because it’s signed (and optionally encrypted), resource servers can verify it without a database lookup (the signature ensures the token is authentic and unaltered). JWTs are perfect for microservices since they are stateless – no session store needed. The downside is if a token must be revoked early, it’s tricky (you often rely on short expiry times and possibly token introspection for long-lived tokens). Nonetheless, JWTs are widely used for performance and simplicity.

**Spring Security for Resource Servers:** Spring Boot makes it straightforward to configure a service as a resource server that expects JWT tokens. Add the dependency `spring-boot-starter-oauth2-resource-server`. Then in `application.yml` configure either the **issuer URI** (if your auth server supports OIDC discovery) or the JWKS URI (URL to fetch the public keys for JWT):

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/myrealm # example (Keycloak/OIDC issuer)
          # or alternatively:
          # jwk-set-uri: https://auth.example.com/realms/myrealm/protocol/openid-connect/certs
```

With this, Spring Security will automatically:

- Validate incoming `Authorization: Bearer <token>` JWTs on protected routes.
- Check the token’s signature against the keys from the issuer (discovered via the `.well-known/openid-configuration` if using `issuer-uri` ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=resourceserver%3A%20jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=Where%20,and%20subsequently%20validate%20incoming%20JWTs))).
- Verify token expiration and other claims (like audience, issuer match).
- Create a security context with the token’s claims. For instance, if the JWT has a claim of roles or scopes, you can map those to Spring authorities.

In your security configuration (or via properties), you specify which endpoints require authentication. The simplest way: in application.properties set `spring.security.oauth2.resourceserver.jwt.issuer-uri`, and by default Spring Security will secure all endpoints (except perhaps `/actuator/health` depending on config). Or you can use a WebSecurityConfigurer:

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests(authorize -> authorize
                .antMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer().jwt();  // enable JWT authentication
    }
}
```

This means any request (except those explicitly permitted) must have a valid JWT. If a request is missing or has an invalid token, it will get a 401 Unauthorized automatically. Spring Security will use the configuration to know how to validate the token (via issuer-uri or jwk-set-uri as provided) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=Startup%20Expectations)).

**Obtaining JWTs (Authentication Flow):** Typically, a client (like a front-end or mobile app) will authenticate via the Authorization Server (perhaps using OAuth2 Authorization Code flow with PKCE for a single-page app). The result is an access token (JWT) that the client then includes in requests to our microservice endpoints. We won’t dive deep into the auth server side here, but the flow is:

1. User logs in and consents, receives a JWT access token (and possibly a refresh token).
2. The client calls `Order Service /api/orders` with `Authorization: Bearer <access_token>` header.
3. Order Service (resource server) verifies the token (signature, expiration, etc.) and then allows the request, often populating a `Authentication` object that you can access in controllers (e.g., via `@AuthenticationPrincipal` to get user details or `SecurityContextHolder`).
4. The service can make authorization decisions based on token claims. For example, only allow users with role "CUSTOMER" to create orders, etc. This can be done with annotations like `@PreAuthorize("hasRole('CUSTOMER')")` on controller methods, which Spring Security will enforce.

**Service-to-Service calls:** When one service calls another, we also need to handle authentication. Two common strategies:

- **Token Relay:** If an incoming user token exists (the service was called by a user with a JWT), the service can forward that JWT in calls to downstream services (so downstream also knows the user context). This way, the user identity flows through. You have to ensure the token contains necessary audience or scope for the downstream service.
- **Client Credentials:** In some cases, a service might act on its own (no user context). You can use OAuth2 Client Credentials flow where each service has its own client ID/secret and obtains a token representing the service identity. Spring’s `@EnableOAuth2Client` or using Spring Security’s WebClient support can allow a service to fetch a token from the auth server and use it. For simplicity, many systems avoid this by using an API Gateway that injects a token or by having services trust each other in a secure network. But a truly zero-trust setup would use mutual authentication (either mutual TLS or signed tokens for inter-service calls).

**JWT Claims and Roles:** How do we represent user roles/permissions in JWT? With OAuth2 and OIDC, access tokens can have a `scope` claim or custom claims. For example, a JWT might have `"scope": "orders:create orders:view"` or `"roles": ["ROLE_USER","ROLE_ADMIN"]` depending on your auth server configuration. Spring Security’s JWT converter can map those into `GrantedAuthority`. By default, if you follow standard OIDC, there is a claim `scp` or `scope` and Spring will turn `scope=read` into authority `SCOPE_read`. You can tweak this conversion.

For instance, if using Keycloak, you might get a `realm_access.roles` claim. You could write a custom converter to extract that into authorities. Once that’s done, your microservice can simply use `@PreAuthorize` or `hasRole()` conditions to protect methods.

**Protecting Eureka and Sensitive Endpoints:** Don’t forget that not only user-facing APIs need security. If you have Eureka, by default it has an open dashboard and allows registrations. In a secure environment, you would lock down Eureka with a username/password or mutual TLS. Spring Cloud Eureka supports basic auth on the server side. Similarly, Actuator endpoints should either be secured or limited. When deploying on Kubernetes or behind firewalls, network policies can restrict access as well.

**OAuth2 and API Gateway:** Often, a **gateway** is used to centralize authentication (so each microservice doesn’t need to parse tokens). For example, Netflix Zuul or Spring Cloud Gateway can check tokens and then pass requests (with a user context) to services. This is fine, but still each service should validate tokens if it’s directly accessible or to enforce defense in depth. Also, consider internal service-to-service calls – securing those ensures that if one service is compromised, it can’t freely call others without a valid token.

**Security Best Practices Recap:**

- Use **short-lived access tokens** (e.g., 15 minutes) and utilize refresh tokens for clients to get new ones. This limits exposure if a token is stolen.
- Use **HTTPS** everywhere to protect tokens in transit.
- Validate JWTs carefully: check the signature (Spring does this), the `iss` (issuer) to match expected issuer, and `aud` (audience) if present to ensure the token is intended for your service. Spring Security can be configured to expect a certain audience or you can check in code.
- Do not trust any input that’s not validated – even a JWT needs proper validation. Also, use library methods to parse/validate JWT; do not roll your own cryptographic checks.
- Principle of least privilege: if using client credentials for inter-service, give each service its own credentials and scopes that allow only the necessary access.
- Store secrets (like OAuth2 client secrets or JWT signing keys if you manage them) in secure storage (Kubernetes Secrets, AWS Secret Manager, etc.), not in plaintext config.
- Log security events (log authentication failures, etc.) but **avoid logging sensitive info** from tokens (don’t log the token string or user’s personal info).

By securing each microservice as a resource server, our architecture ensures that only authenticated and authorized requests are processed. In development you might use dummy tokens or turn off auth, but in production these measures protect both data and the services themselves from unauthorized access.

## Database Integration with PostgreSQL and MongoDB

Microservices often follow the pattern of **database per service** – each service manages and persists its own data, which can even be a different type of database from other services (relational, document, etc.) ([Eureka Server: The Heart of Microservice Communication](https://www.mindbowser.com/microservices-with-eureka/#:~:text=They%20should%20be%20deployed%20independently,and%20another%20may%20use%20MongoDB)). This isolates data concerns and allows each service to choose the database best suited to its needs. We will integrate two common databases: **PostgreSQL** (a relational database) and **MongoDB** (a NoSQL document database) in different services to demonstrate how to use Spring Boot with each.

### Using PostgreSQL with Spring Data JPA (Relational Database)

For a service that requires strong consistency and relational data modeling, PostgreSQL is a great choice. Spring Boot simplifies connecting to PostgreSQL via Spring Data JPA (which uses Hibernate as the ORM by default).

**Dependencies:** In your microservice (e.g., Order Service), include:

- `spring-boot-starter-data-jpa` (for JPA and Hibernate).
- The PostgreSQL JDBC driver: `org.postgresql:postgresql`.

Your `pom.xml` might have:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
  <groupId>org.postgresql</groupId>
  <artifactId>postgresql</artifactId>
  <scope>runtime</scope>
</dependency>
```

**Configuration:** In `application.yml`, configure the data source and JPA settings:

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/orderdb
    username: order_user
    password: secretpassword
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: false
```

Replace URL, username, password with your actual database credentials. The `ddl-auto: update` will auto-create/alter tables based on entity classes (convenient for dev, but in production you might use `validate` or manual migrations). For clarity, ensure the `driverClassName` if needed (Spring Boot usually figures it out from the URL). The `show-sql` can be true for debugging SQL queries, but off in production.

**Entity Definition:** Create a JPA entity class for the data you want to store. For example, an Order entity:

```java
@Entity
@Table(name = "orders")
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String productId;
    private Integer quantity;
    private Instant orderDate;
    // getters and setters...
}
```

Here, `@Entity` marks it as a JPA entity mapped to a table (if no `@Table` given, it defaults to the class name) ([Getting Started | Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa#:~:text=The%20,Customer)). We have an `id` as primary key with auto-generation. Other fields map to columns (e.g., productId, quantity). JPA will create the table `orders` with columns id, product_id, quantity, order_date (naming conventions can be controlled via @Column or a naming strategy).

**Repository Interface:** Spring Data JPA can generate implementations of repository interfaces at runtime. Define an interface:

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByProductId(String productId);
}
```

By extending `JpaRepository<Order, Long>`, you inherit standard CRUD methods (save, findById, findAll, delete, etc.) ([Getting Started | Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa#:~:text=,entities)). We also declare a finder `findByProductId` – Spring Data JPA will derive a query to find Order entities by their productId field ([Getting Started | Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa#:~:text=,entities)).

You can now inject this `OrderRepository` into your service layers or controllers to perform database operations. For example:

```java
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepo;

    public Order createOrder(String productId, int qty) {
        Order order = new Order();
        order.setProductId(productId);
        order.setQuantity(qty);
        order.setOrderDate(Instant.now());
        return orderRepo.save(order);
    }

    public List<Order> getOrdersByProduct(String productId) {
        return orderRepo.findByProductId(productId);
    }
}
```

Spring Boot will automatically configure a connection pool (HikariCP by default) for the DataSource. On startup, you should see logs like “HHH000418: Connecting to database” and if `ddl-auto` was set to update, Hibernate will execute DDL to create the table if it doesn’t exist (you can see these SQL statements if `show-sql=true`). It’s often recommended to handle schema with a migration tool (Flyway or Liquibase) in real applications, but auto DDL is fine for small apps or initial development.

**Testing DB Integration:** You can write a quick unit or integration test (with `@DataJpaTest` or using the repository in a running app) to verify that saving and retrieving works. Example:

```java
Order saved = orderRepo.save(new Order(null, "prod-987", 3, Instant.now()));
List<Order> orders = orderRepo.findByProductId("prod-987");
assertFalse(orders.isEmpty());
```

This should return the saved order.

**Transactions:** Spring Data JPA repository methods are transactional by default (for write operations). If you need to ensure multiple operations are atomic, you can use `@Transactional` on service methods. Spring Boot by default enables transaction management with JPA. For example, if an Order creation should also update inventory (in same service), you’d put both repo calls in one @Transactional method so they commit or rollback together. Across microservices, distributed transactions are complex (often avoided in favor of eventual consistency or saga patterns).

**Performance Tips for JPA:**

- Use **lazy loading** wisely. By default, to-one relationships are eager which can lead to unnecessary queries. Annotate relations with `fetch = FetchType.LAZY` if needed and manage fetching via JPQL or Entity Graphs.
- For frequent read operations that don’t change often, consider using caching (Second-level cache or method-level caching via Spring Cache).
- Monitor the HikariCP pool size and tune it (e.g., `spring.datasource.hikari.maximumPoolSize`) if needed based on your load.
- If encountering the "N+1 query problem" (multiple SQL selects due to lazy fetch in loops), refactor queries to fetch needed data in one go (using `@Query` or join fetch, etc.).

### Using MongoDB with Spring Data Mongo (Document Database)

For data that is document-oriented or where schema flexibility and horizontal scalability are desired, MongoDB is a popular choice. Let’s integrate MongoDB in another service, say **Inventory Service** for storing product info and stock levels.

**Dependencies:** In Inventory Service, add:

- `spring-boot-starter-data-mongodb` (it brings in the Mongo Java driver and Spring Data MongoDB).
  No separate driver dependency is needed because the starter includes the Mongo driver.

**Configuration:** If MongoDB is running on default localhost:27017, Spring Boot will connect automatically to it (to a database named “test” by default). You can configure:

```yaml
spring:
  data:
    mongodb:
      database: inventorydb
      host: localhost
      port: 27017
      username: inventory_user # if you have auth enabled
      password: secretpassword
```

If using a connection string (especially for cloud MongoDB like Atlas), you could use:

```yaml
spring.data.mongodb.uri: mongodb://inventory_user:secretpassword@localhost:27017/inventorydb
```

If no username/password, omit those. Ensure MongoDB is running and the `inventorydb` is accessible (Mongo will create the database on the fly the first time data is stored if it doesn't exist).

**Document Definition:** Instead of JPA’s `@Entity`, we use Spring Data’s `@Document` annotation to map a class to a Mongo collection. For example:

```java
@Document(collection = "products")
public class Product {
    @Id
    private String id;         // MongoDB uses String or ObjectId for IDs
    private String name;
    private int stock;
    private String category;
    // getters, setters, constructors...
}
```

Here, `@Document(collection="products")` marks this class for MongoDB, and if not specified, the collection name defaults to the class name (or you can let it default, in this case it’d use “product” or “product” collection). We use `@Id` on the id field to mark it as the primary identifier ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb/#:~:text=public%20class%20Customer%20)) ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb/#:~:text=)). If you leave `id` as null and save, Spring Data will generate a Mongo ObjectId. We can also use `ObjectId` type for the id field if we want.

**Repository Interface:** Similar to JPA, Spring Data Mongo has `MongoRepository`. For example:

```java
public interface ProductRepository extends MongoRepository<Product, String> {
    List<Product> findByCategory(String category);
}
```

This gives you CRUD operations for Product and the derived query finder by category ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb/#:~:text=import%20java)). Spring Data will implement this at runtime.

**Using the Repository:** For instance, in an InventoryService class:

```java
@Autowired
private ProductRepository productRepo;

public Product addProduct(Product p) {
    return productRepo.save(p);
}

public Product getProduct(String id) {
    return productRepo.findById(id).orElse(null);
}

public List<Product> getProductsByCategory(String category) {
    return productRepo.findByCategory(category);
}
```

Operations like `save` and `findById` translate to MongoDB insert/find commands. When you call `save` on a new object, the driver will insert a new document in the `products` collection; if the object already has an id, it will do an upsert (replace).

**Mongo Console Check:** You can use the Mongo shell or another tool to verify data. E.g., after running a save, connect to Mongo and do:

```js
use inventorydb
db.products.find({})
```

You should see your product documents.

**Schema-less but Structured:** MongoDB doesn’t enforce a schema on the database level, but your application does have a class definition. If you add new fields later, old documents won’t have them (which is usually okay). If you remove fields, they’ll just be ignored if present in old docs. This flexibility is useful for evolving schemas without migrations, but be cautious to handle missing fields in code (by providing defaults).

**Transactions in MongoDB:** MongoDB from version 4 supports multi-document transactions _if using a replica set or cluster_. Spring Data Mongo can participate in transactions via `@Transactional` on methods – behind the scenes it will start a Mongo transaction across operations on that template. However, most MongoDB usage in microservices is single-document operations (which are atomic by themselves). If you need multi-document or multi-collection consistency, ensure your Mongo deployment supports it and enable transactions in Spring Data (it requires Spring Data Mongo 2.x+ and Mongo driver 4+).

**Mixing JPA and Mongo in one service:** It’s possible (Spring can configure two different database connections in one app), but in microservices architecture, typically you wouldn’t mix in one service – instead, one service uses one type of database that fits its needs, and another service might use another. This avoids one service becoming dependent on two different data sources unnecessarily.

**Polyglot Persistence Example:** In our scenario:

- Order Service (with Postgres) stores structured order records with relationships (maybe linking to customer, etc., if it had those – relational makes sense here).
- Inventory Service (with Mongo) stores product info, which might be a document containing arrays of attributes, etc., and can scale easily – a document model fits well.
  These services communicate via REST, not directly at the DB level, preserving the microservice autonomy.

**Database best practices:**

- **Connection management:** The default HikariCP for SQL and Mongo client's internal pooling are usually fine. Monitor connections if under heavy load.
- **Indexes:** Ensure you create indexes for fields you query often. For JPA, you can add `@Column` with indexes via DDL, or manually create them. For Mongo, you might define an index on `category` if `findByCategory` is frequent (using a `@Indexed` annotation on the field or via a CommandLineRunner to create index on startup).
- **Handling Failures:** If a database is down, how does the service behave? Use appropriate timeout settings and fallbacks if needed (this ties into resilience – e.g., circuit breaker on repository calls if the DB is unreachable, though often you trust the DB and handle at a higher level).
- **Migrations:** For PostgreSQL, manage schema changes carefully. In microservices, since each DB is owned by one service, you can version your schema alongside the service’s code changes. Tools like Flyway can run migrations on startup to ensure the DB schema is at the correct version for the service code.
- **Data backups and safety:** Have backups for your databases. For Mongo, maybe use MongoDB’s backup or a cluster with replication. For Postgres, frequent dumps or streaming replication to a standby.

By integrating PostgreSQL and MongoDB, we demonstrated how Spring Boot embraces different storage technologies under one umbrella (Spring Data has similar support for many databases). Each microservice can choose SQL or NoSQL as needed, and Spring will handle a lot of the boilerplate, letting you focus on domain logic.

Next, we’ll discuss ensuring these data operations (and overall service interactions) perform well and are resilient to failures.

## Performance Tuning and Resilience Patterns (Circuit Breaker, Retry, Bulkhead)

Microservices need to be robust and fast. In this section, we’ll cover techniques to **tune performance** and introduce **resilience patterns** to handle failures gracefully. Ensuring high performance and fault tolerance will make the system responsive and stable under load or when dependencies fail.

### Performance Tuning Best Practices

**1. Caching:** Caching is a classic way to improve performance. Identify frequently read data that doesn’t change often (e.g., product catalog info) and cache it. Spring Boot supports simple caching with `@EnableCaching` and annotations like `@Cacheable`. For example, in Inventory Service:

```java
@Cacheable("productCache")
public Product getProductById(String id) {
    return productRepo.findById(id).orElse(null);
}
```

The first call will hit the database, but subsequent calls with the same `id` will return the cached Product (until cache eviction). By default, Spring Boot uses a concurrent map for cache; in production you might plug in a more robust cache (Caffeine for in-memory, or Redis for distributed caching). **Note:** caching must be used carefully to ensure consistency (evict or update cache on writes, or use short TTL if data changes frequently).

**2. Database Optimization:**

- For SQL, write efficient queries (use JPQL or Criteria when needed to fetch only necessary data). Ensure you have proper indexes in the database for fields used in `WHERE` clauses or joins. For example, indexing `product_id` on the orders table if you often query by productId.
- Use connection pools – Spring Boot already pools JDBC connections; verify the pool size is adequate (not too low to cause wait, not too high to overload DB).
- Avoid N+1 query issues: If you log SQL (e.g., `spring.jpa.show-sql=true`) and see dozens of small queries, consider using joins or fetch graphs.
- Consider **pagination** for endpoints that return large lists to avoid loading too much into memory (Spring Data JPA has `findAll(Pageable)` for this).

**3. Async and Non-blocking:** If some tasks can be done asynchronously, offload them to separate threads. For example, sending confirmation emails after order placement can be done in the background (using Spring’s `@Async` or a messaging queue) so the user’s request isn’t delayed by email sending. Similarly, Spring WebFlux (reactive programming) can handle large loads with fewer threads by using non-blocking I/O – if extreme scalability is required, you might consider using WebFlux for certain services.

**4. Thread Pool Tuning:** Tomcat (Spring MVC) by default has a max thread pool (e.g., 200) for handling requests. In high-load scenarios, you can tune `server.tomcat.max-threads`. But more threads isn’t always better due to context switching – monitor CPU and response times. For blocking operations (like I/O or DB), ensure you have enough threads so others aren’t waiting too long. For any custom executors (like with `@Async` or scheduling), configure their pool sizes to suit the workload.

**5. Reduce Network Overhead:** Microservices call each other over the network – minimize payload sizes (don’t fetch or send giant responses if not needed). Use compression (Spring Boot can enable GZIP compression of responses with properties). Avoid chatty communication patterns – if one service needs data from another repeatedly, see if you can batch requests. For example, instead of Order Service calling Inventory for each item in an order individually, modify Inventory API to accept a batch of product IDs in one call and return all stocks in one go. This reduces overhead and latency.

**6. GC and Memory:** Ensure the JVM has appropriate heap size for each service (container memory limits etc.). Monitor garbage collection – high GC times can impact performance. If services handle large payloads or many objects, consider newer GCs (G1GC is default in recent JDKs and usually fine). For memory leaks, use profiling tools; Spring generally doesn’t leak memory if used right, but be cautious with caches or large static structures.

**7. Profiling and Monitoring:** Use tools like JProfiler or VisualVM in non-production to find slow spots in code. In production, use metrics: Spring Boot Actuator with Micrometer can send metrics to monitoring systems (Prometheus, etc.). Key metrics: response time, DB query counts, thread pool usage, CPU, memory. Identify if certain requests are consistently slow and dig into why (maybe an external call or DB query). Often, performance tuning is an iterative process: measure, identify bottleneck, fix, then measure again.

**8. Content Delivery and CDN:** For services that serve static content (images, etc.), offload those to a CDN. For dynamic responses, perhaps use an edge cache if possible (not trivial for personalized data, but consider caching common responses at gateway level for a short time if it reduces load).

By following these practices, you ensure each microservice runs efficiently. But even a highly optimized service can face issues if a downstream service it calls is slow or down. That’s where resilience patterns come into play.

### Resilience Patterns (Circuit Breaker, Retry, Bulkhead, Timeout)

Distributed systems inevitably face failures: a service might be down, network might have hiccups, or operations might time out. **Resilience patterns** help services fail gracefully and prevent one failure from cascading through the system.

**Circuit Breaker:** This pattern is like an electrical circuit breaker in your code. It monitors calls to a remote service (or any potentially failing operation). If the failure rate exceeds a threshold, the circuit “opens,” causing subsequent calls to fail immediately without attempting the remote operation ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=The%20Circuit%20Breaker%20pattern%20can,try%20to%20invoke%20the%20operation)). This prevents saturating threads waiting on a down service and gives that service time to recover ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=The%20Circuit%20Breaker%20pattern%20can,try%20to%20invoke%20the%20operation)). After a pause (half-open state), a limited number of test calls are allowed to see if the service has recovered; if they succeed, the circuit closes again, resuming normal operation ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=A%20circuit%20breaker%20acts%20as,or%20return%20an%20exception%20immediately)).

Using **Resilience4j**, which is a lightweight fault tolerance library, we can easily add a circuit breaker to a call. For example, in Order Service when calling InventoryService via Feign or RestTemplate, we wrap that call in a circuit breaker. Spring Cloud Circuit Breaker offers a common abstraction and Resilience4j implementation.

Example with Resilience4j annotations:

```java
@CircuitBreaker(name = "inventoryService", fallbackMethod = "fallbackStock")
public Integer getStockWithBreaker(String productId) {
    // This is the remote call that might fail
    return inventoryClient.getStock(productId);
}

public Integer fallbackStock(String productId, Throwable ex) {
    // Fallback logic, e.g., return a default value or read from a cache
    System.err.println("Inventory service unavailable, exception: " + ex);
    return -1;
}
```

Here, we define a circuit breaker named “inventoryService” for the `getStockWithBreaker` method. If Inventory Service starts failing (exceptions or timeouts), after a threshold, further calls to `getStockWithBreaker` will not actually invoke `inventoryClient.getStock` but will directly go to `fallbackStock`. The fallback method can degrade functionality – e.g., return `-1` or some sentinel to indicate stock is unknown, which the Order Service can interpret as “cannot verify stock right now.” This stops the endless waiting and failing attempts ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=The%20Circuit%20Breaker%20pattern%20can,try%20to%20invoke%20the%20operation)). Once Inventory Service is back (Resilience4j will allow a trial call after a wait), the circuit closes and normal operation resumes.

Resilience4j allows configuration of circuit breaker parameters: failure rate threshold (% of calls failing to trip the breaker), wait duration before half-open, minimum number of calls to evaluate, etc. These should be tuned to your needs. For instance, you might say if 50% of the last 10 calls failed, open the breaker for 30 seconds.

**Retry:** Sometimes failures are transient – a momentary network glitch or a timeout that might succeed if tried again. The **Retry pattern** attempts an operation again a few times before truly treating it as a failure ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=due%20to%20transient%20faults%2C%20such,strategy%20such%20as%20the%20Retry)). Combined with backoff (small delays between retries), this can smooth over temporary issues. However, indiscriminate retries can worsen load (e.g., retrying on a truly down service just adds more traffic). So use it mainly for operations known to be flaky or when the extra latency is acceptable.

In Spring Cloud/Resilience4j, you can configure retries:

```java
@Retry(name = "inventoryService", maxAttempts = 3, fallbackMethod = "fallbackStock")
@CircuitBreaker(name = "inventoryService", fallbackMethod = "fallbackStock")
public Integer getStockWithRetry(String productId) {
    return inventoryClient.getStock(productId);
}
```

Here, we attempt up to 3 times before failing. Often you use both a retry and circuit breaker together: the retry handles quick transient failures, and the circuit breaker handles longer outages or persistent failures (after retry attempts also fail) ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=,a%20fault%20is%20not%20transient)).

Be mindful to not retry if the failure is a definitive one (e.g., 404 Not Found – retrying won’t change that). You can configure what exceptions to retry on (like IO exceptions, timeouts).

**Timeouts:** Underlying all these, always set sensible timeouts on your calls. For example, if using RestTemplate with a SimpleClientHttpRequestFactory, set connect and read timeouts. With Feign, set `feign.client.config.default.connectTimeout` and `readTimeout`. Without timeouts, a call could hang indefinitely, tying up a thread. A circuit breaker might not even trigger if the call never returns (Resilience4j has a TimeLimiter that can wrap a call to enforce a timeout). So define, for instance, that InventoryService calls timeout after 2 seconds. This ensures a slow service doesn’t hold others hostage. It’s better to fail fast (and perhaps retry or fallback) than to wait too long.

**Bulkhead:** The Bulkhead pattern is about partitioning resources so that a failure in one part doesn’t overwhelm the whole system ([Resilience4J: Introduction to Bulkhead - Knoldus Blogs](https://blog.knoldus.com/resilience4j-introduction-to-bulkhead/#:~:text=patterns%20for%20building%20resilient%20applications,and%20how%20Resilience4J%20implements%20it)). In microservices, a classic bulkhead is using separate thread pools for different types of work. For example, if Order Service calls both Inventory and Payment, you could isolate those calls in different thread pools. If Inventory calls start hanging, only the inventory-dedicated threads are consumed, and payment-related threads are free to handle other tasks ([Resilience4J: Introduction to Bulkhead - Knoldus Blogs](https://blog.knoldus.com/resilience4j-introduction-to-bulkhead/#:~:text=patterns%20for%20building%20resilient%20applications,and%20how%20Resilience4J%20implements%20it)). This prevents a domino effect where one external dependency exhausts all your service's threads (or other resources like memory).

Resilience4j Bulkhead provides two modes:

- Semaphore bulkhead: limits number of concurrent calls to a component.
- ThreadPool bulkhead: routes calls to a separate thread pool (queueing if necessary up to a limit).

For instance:

```java
@Bulkhead(name = "inventoryService", type = Bulkhead.Type.SEMAPHORE, maxConcurrentCalls = 10, fallbackMethod = "fallbackStock")
public Integer getStockBulkhead(String productId) {
    return inventoryClient.getStock(productId);
}
```

This would allow at most 10 concurrent executions of `getStockBulkhead`. The 11th call will immediately hit fallback (or block/wait depending on config) ([Bulkhead pattern in Microservices: Spring Boot example - Medium](https://medium.com/@sivaramansankar2019/bulkhead-pattern-in-microservices-spring-boot-example-d82db2c0cc5#:~:text=Bulkhead%20pattern%20in%20Microservices%3A%20Spring,of%20your%20dependencies%20is)). This ensures if more than 10 threads try to call Inventory (maybe it hung and threads piled up), the 11th is stopped, preserving threads for other tasks.

If using a thread pool bulkhead:

```java
@Bulkhead(name = "inventoryService", type = Bulkhead.Type.THREADPOOL, fallbackMethod = "fallbackStock")
```

You’d configure in properties something like:

```yaml
resilience4j.thread-pool-bulkhead:
  instances:
    inventoryService:
      coreThreadPoolSize: 5
      maxThreadPoolSize: 10
      queueCapacity: 20
```

This offloads calls to InventoryService to a pool of at most 10 threads, separate from the main request handling threads. If Inventory is slow, those 10 can all be busy, but your Tomcat threads are not all consumed – they’re free to handle other work or other endpoints. Bulkhead thus contains the impact of a slowdown.

**Fallbacks and Graceful Degradation:** We hinted at fallback methods. Designing good fallback behavior is important:

- If Inventory service is down, maybe Order Service can proceed with an order but mark it as “pending inventory confirmation” instead of outright failing. Or it can respond to the user: “Order placed, but will be processed later due to inventory check issues.”
- If one microservice (e.g., Recommendation service for products) is down, maybe just skip recommendations rather than failing the whole page.

The goal is the system should still deliver core functionality even if some components are compromised, perhaps with reduced feature set. Always communicate clearly (to logs or to user) when a fallback path is taken so issues aren’t silent.

**Rate Limiting and others:** Another pattern (not asked, but related) is throttling: limit how many requests are allowed to prevent overload. This can be done at gateway or service level (Resilience4j has a RateLimiter too). Ensure upstream clients cannot spam a service into overload.

**Testing Resilience:** It’s worth testing these patterns by simulating failures. For example, stop the Inventory Service and see that Order Service’s circuit breaker opens and falls back correctly – the Order API should return a graceful response rather than stacktrace. Likewise, test latency by adding sleep in a downstream call to ensure timeouts and bulkheads behave as expected.

By applying circuit breakers, retries, bulkheads, and timeouts, our microservices become **self-healing and robust**:

- A temporary glitch -> retry will likely solve it.
- A prolonged outage -> circuit breaker will prevent resource exhaustion and degrade service instead of crashing.
- A slow service -> timeout + fallback ensures users aren’t left hanging.
- Overload -> bulkheads and possibly rate limits ensure failures are localized and system remains partially functional.

Together with good logging/tracing, you’ll have visibility into these events (e.g., log when circuit opens or when retries happen, many libraries do this or you can tap events in Resilience4j). Operational monitoring for these resilience events can inform you of underlying issues (like “circuit open” alerts could mean that service is down).

We have now covered making our microservices not only _performant_ but also _resilient_ to failures. The last step is to package and deploy these services reliably, for which we turn to Docker and Kubernetes.

## Deployment Strategies with Docker and Kubernetes

Once our microservices are developed and tested, we need to deploy them consistently across environments (dev, staging, production). **Containerization** with Docker has become standard for packaging microservices, and **Kubernetes** is a powerful platform for running and managing these containers at scale. Let’s outline how to containerize Spring Boot applications and deploy them to a Kubernetes cluster, as well as strategies for effective deployments (rolling updates, etc.).

### Containerizing Spring Boot Microservices with Docker

**Why Docker?** Docker provides a lightweight isolation for applications. By packaging a microservice and its environment into an image, we ensure it runs the same way everywhere. It encapsulates the JDK, application JAR, and any required OS libraries. This eliminates “it works on my machine” problems.

**Dockerfile for Spring Boot app:** A simple approach is to use a base image with JDK and add the executable JAR. For example, create a file `Dockerfile` in the Order Service project:

```
# Use an official OpenJDK runtime as a parent image
FROM eclipse-temurin:17-jre-alpine      # lightweight Java 17 runtime

# Set working directory (optional)
WORKDIR /app

# Copy the Spring Boot jar to the container
COPY target/order-service-1.0.0.jar order-service.jar

# Expose the port the app runs on (optional, for documentation)
EXPOSE 8081

# Command to run the jar
ENTRYPOINT ["java","-jar","order-service.jar"]
```

In this Dockerfile:

- We use a slim Alpine-based JRE image for minimal size.
- We copy the built jar into the image.
- We define the entrypoint to run the jar.

Make sure you have built the Jar (e.g., via `mvn package`) before building the Docker image. Then:

```bash
docker build -t myorg/order-service:1.0.0 .
```

This creates a Docker image named `myorg/order-service:1.0.0`. Repeat similar steps for other services (just changing jar names, expose port etc. as needed). Alternatively, Spring Boot can generate an image with `./mvnw spring-boot:build-image`, which uses Buildpacks to make an image (this is another convenient route, yielding images like `docker.io/library/order-service:0.0.1-SNAPSHOT`).

**Running Containers:** To test locally:

```bash
docker run -d -p 8081:8081 --name order-service myorg/order-service:1.0.0
```

This will run Order Service in a container, mapping container port 8081 to localhost 8081. Do the same for inventory (just ensure each uses their respective ports or adjust if needed). If services need to talk to each other (Eureka, etc.), you might use Docker networks so they can resolve each other by container name, or run them with Docker Compose (which sets up a network and easy linking).

A Docker Compose file (for dev convenience) might look like:

```yaml
version: "3"
services:
  eureka-server:
    image: myorg/eureka-server:1.0.0
    ports:
      - "8761:8761"
  order-service:
    image: myorg/order-service:1.0.0
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka-server:8761/eureka
    ports:
      - "8081:8081"
    depends_on:
      - eureka-server
  inventory-service:
    image: myorg/inventory-service:1.0.0
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka-server:8761/eureka
    ports:
      - "8082:8082"
    depends_on:
      - eureka-server
```

This would start Eureka, Order, and Inventory containers and link them on a common network so they can find `eureka-server` by name.

**Docker Best Practices:**

- Keep images small: using JRE instead of JDK for runtime, cleaning up any package manager caches if you install things, etc. Our base alpine JRE is already quite small (tens of MB).
- Use multi-stage builds if you need to compile code inside the container (but we usually build jar externally and just copy it in).
- Don’t run as root: the above image by default might run as root user. You can add a user in Dockerfile (`RUN adduser -D spring && chown -R spring /app`, then `USER spring`). Also avoid running on default ports <1024 as non-root cannot bind them without extra setup.
- Externalize configuration: Instead of baking config into the image, use environment variables or volumes. For example, our Eureka URL was passed via env var in compose. Spring Boot will pick up environment variables (like we did for Eureka URL, as it maps to `eureka.client.service-url.defaultZone`). Similarly, for database passwords or other secrets, don’t put them in the image, pass them at runtime (or use Docker secrets/K8s secrets).
- Healthchecks: Docker allows a `HEALTHCHECK` instruction. You can add:
  ```
  HEALTHCHECK CMD curl -f http://localhost:8081/actuator/health || exit 1
  ```
  This would periodically check the health endpoint. Kubernetes also has its own liveness/readiness checks, so often we rely on those rather than Docker healthcheck.

Now that we have Docker images, we can deploy to any container platform. The next step is to use Kubernetes to manage these containers in a clustered environment.

### Deploying Microservices to Kubernetes

Kubernetes (K8s) is an orchestration platform that manages container lifecycles, scaling, networking, and more. We’ll outline the basic K8s resources needed to deploy our microservices and discuss deployment strategies.

**Kubernetes building blocks:**

- **Pod:** The smallest unit, which can contain one or more containers (often just one container per pod for microservices).
- **Deployment:** A controller that manages a set of identical pods, ensuring the desired number are running. It allows rolling updates.
- **Service (K8s Service):** An abstraction for networking – it provides a stable IP or DNS name and load-balances across a set of pods (selected by labels). This is how other pods or external clients find our microservice pods.
- **ConfigMap and Secret:** Ways to provide configuration data to pods (as env vars or files) without baking into images (similar concept to externalize config).
- **Ingress:** (Optional for external access) Manages external HTTP(S) routing into cluster services, often providing a single endpoint (with host/path rules routing to internal services).

Let’s create Kubernetes manifests for our Order Service as an example; others will be similar:

**Deployment YAML (order-deployment.yaml):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-deployment
  labels:
    app: order-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: myorg/order-service:1.0.0
          ports:
            - containerPort: 8081
          env:
            - name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
              value: "http://eureka-service:8761/eureka"
            - name: SPRING_DATASOURCE_URL
              value: "jdbc:postgresql://postgres:5432/orderdb"
            - name: SPRING_DATASOURCE_USERNAME
              value: "order_user"
            - name: SPRING_DATASOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: order-db-secret
                  key: db-password
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8081
            initialDelaySeconds: 30
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8081
            initialDelaySeconds: 30
            periodSeconds: 15
```

This defines a Deployment for Order Service:

- 2 replicas (so two pods of order-service).
- The pods use the Docker image we built.
- It passes environment variables to configure Eureka location (pointing to a service name `eureka-service` – we’ll create a Service for Eureka too).
- It also passes DB connection info (assuming perhaps a Postgres deployed as `postgres` Service; credentials from a Secret named order-db-secret).
- We define liveness and readiness probes using Actuator endpoints (you would enable separate health groups or use the same /health with appropriate content). Liveness probe tells K8s if the app is running; if it fails, K8s will restart the container. Readiness probe tells if app is ready to serve traffic; if it fails, K8s will temporarily remove that pod from service endpoints (but not kill it). We delay them a bit to give time for app startup.

**Service YAML (order-service-svc.yaml):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - port: 8081
      targetPort: 8081
      protocol: TCP
```

This creates a stable network identity for the Order pods. Any other pod in the cluster can resolve `order-service` (or `order-service.default.svc.cluster.local` fully) and reach an Order pod on port 8081. We don’t expose this externally yet (ClusterIP type by default), it's internal. The Eureka client in Order was configured to talk to eureka-service (which will be another Service). Similarly, Inventory Service will have its own Deployment and Service, and Eureka (discovery) can be a Deployment + Service.

**Eureka on Kubernetes:** In Kubernetes, you might wonder if Eureka is needed since Kubernetes itself has service discovery. It’s optional. Kubernetes _service_ discovery uses DNS (the `order-service` Service we made) for discovery inside the cluster. If our Spring Boot apps can use that directly, Eureka isn’t strictly necessary on K8s ([Service Discovery | Kf - Google Cloud](https://cloud.google.com/migrate/kf/docs/2.2/concepts/service-discovery#:~:text=Service%20Discovery%20%7C%20Kf%20,programming%20languages%20and%20applications)). However, if we want to remain environment-neutral or use client-side load-balancing logic of Eureka, we can run Eureka in K8s. There’s also Spring Cloud Kubernetes which allows using K8s API as a discovery client (so apps query K8s for endpoints instead of Eureka) ([Quick Guide to Microservices with Kubernetes, Spring Boot 2.0 and Docker – Piotr's TechBlog](https://piotrminkowski.wordpress.com/2018/08/02/quick-guide-to-microservices-with-kubernetes-spring-boot-2-0-and-docker/#:~:text=Spring%20Cloud%20and%20Kubernetes%20may,the%20whole%20Spring%20Cloud%20project)) ([Quick Guide to Microservices with Kubernetes, Spring Boot 2.0 and Docker – Piotr's TechBlog](https://piotrminkowski.wordpress.com/2018/08/02/quick-guide-to-microservices-with-kubernetes-spring-boot-2-0-and-docker/#:~:text=Before%20we%20proceed%20to%20the,and%20ingresses%20for%20API%20gateway)). Either approach is valid. To keep things simple, suppose we stick with Eureka in cluster:

- Deploy Eureka as a Deployment (maybe 1 replica or 2 for HA) and a Service called `eureka-service`. Then the apps use that.
- Alternatively, skip Eureka: use Spring Cloud Kubernetes or just use the fact that `order-service` can call `inventory-service` by name (with Ribbon replaced by Spring Cloud LoadBalancer which can use service discovery of K8s). For this you’d include `spring-cloud-starter-kubernetes-client-discovery`, etc. It might reduce complexity to drop Eureka on K8s.

But since our examples assume Eureka, we can deploy it similarly and treat `eureka-service:8761` as discovery URL. (Note: if dropping Eureka, we’d remove those env configs and likely use the Spring Cloud K8s way, which would make `inventory-client.getStock()` work via service name resolution under the hood).

**Config and Secrets:** We used an example of `SPRING_DATASOURCE_PASSWORD` coming from a Secret. We would create that Secret like:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-db-secret
type: Opaque
stringData:
  db-password: "secretpassword"
```

Kubernetes will base64-encode it. The Deployment then pulls it. Similarly, other sensitive config like OAuth2 client secrets, etc., should be in Secrets.

**Ingress for External Access:** If these services need to be accessed from outside the cluster (say our Order Service has a UI or is called by external clients), we set up an Ingress or a LoadBalancer service. For example, with an Ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /orders/*
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 8081
          - path: /inventory/*
            pathType: Prefix
            backend:
              service:
                name: inventory-service
                port:
                  number: 8082
```

This would route external traffic from `api.example.com/orders/...` to our Order Service pods, etc. You need an ingress controller (like NGINX or Traefik) installed for this to work. Alternatively, one could deploy an API Gateway (like Spring Cloud Gateway or Zuul or an Envoy) as an ingress.

**Scaling:** With the Deployment, scaling is as easy as changing `replicas` or using `kubectl scale deployment order-service --replicas=3`. Kubernetes will spin up more pods and the Service will include them automatically for load balancing. We can also set up an Horizontal Pod Autoscaler (HPA) to scale based on CPU or custom metrics. For example, HPA could monitor CPU of the pods and if above 70%, scale from 2 to maybe up to 5 replicas.

**Rolling Updates:** When you update the Docker image (say a new version of Order Service), you update the Deployment (either by changing the image tag in the YAML or using `kubectl set image`). Kubernetes will do a rolling update: it will start a new pod with the new version before terminating an old one, ensuring some pods are always serving. Our readiness probe is critical here – it ensures a new pod is only added to service load balancing when it's actually ready. If a new pod fails readiness, K8s won’t send traffic to it and can even abort or roll back the update if configured. This enables zero-downtime deployments if done correctly.

**Blue-Green/Canary:** More advanced deployment strategies can be done on Kubernetes:

- _Blue-Green:_ Deploy new version as a separate deployment (green) while old (blue) still runs. Then switch traffic (could be done by switching Service label selectors or an ingress route). This can be achieved manually or using tools like Argo Rollouts.
- _Canary:_ Run a few pods of the new version along with old, and gradually increase traffic to new version. This often requires an ingress or service mesh that can do traffic splitting by weights.

**Resilience and K8s:** We already built resilience in app, but note that Kubernetes also increases resilience:

- If a container crashes or is unresponsive (failing liveness probes), Kubernetes will restart it automatically (self-healing).
- If a node (VM) in the cluster dies, the Deployment controller will schedule new pods on remaining nodes.
- If configured with multiple replicas across different nodes (and if using a cloud environment with multi-zone cluster), even data center issues can be mitigated.

However, K8s isn't a substitute for our resilience patterns – it works at a coarse level (pod level restarts), whereas circuit breakers and retries handle application-level failures faster and more granularly.

**Monitoring and Logging in Kubernetes:** Ensure you have a strategy for monitoring (Prometheus can scrape metrics from our Actuator /prometheus endpoint). And logging – in Kubernetes, stdout/stderr of containers can be aggregated with tools like EFK (Elasticsearch + Fluentd + Kibana). We already output logs to Elasticsearch ourselves via Logstash inside the app, which is fine. Alternatively, one could log to stdout and use a Fluentd sidecar to ship logs. Since we have ELK integrated at app level, we might stick to that, which is okay but keep an eye on complexity (sometimes centralizing logging via sidecars can be simpler in K8s). Regardless, our Kibana should still work as long as the Logstash and Elasticsearch are reachable (maybe we deploy ELK within K8s or use a managed Elastic). There's also OpenTelemetry logging that can integrate, but our existing setup is fine.

**Security on K8s:** Consider network policies (to restrict which services can talk to which – zero trust networking). Use RBAC so that if a service’s credentials are compromised, an attacker can’t escalate. Also, keep images updated to avoid vulnerabilities and use minimal privilege (which we did by running as non-root).

By deploying on Kubernetes, we achieve a scalable, self-healing deployment for our microservices. It eases operations like scaling, updating, and isolating issues. The diagram below conceptualizes how our services run on Kubernetes:

([Quick Guide to Microservices with Kubernetes, Spring Boot 2.0 and Docker – Piotr's TechBlog](https://piotrminkowski.wordpress.com/2018/08/02/quick-guide-to-microservices-with-kubernetes-spring-boot-2-0-and-docker/)) _Microservices deployed on Kubernetes._ The diagram shows three Spring Boot services (Organization, Department, Employee as an example) each running in their own set of containers (pods), and core Kubernetes components: ConfigMap/Secret provide configuration, **Ingress** routes external requests to the appropriate service, and a **Service Discovery** mechanism (Kubernetes service or Eureka) allows services to find each other internally ([Quick Guide to Microservices with Kubernetes, Spring Boot 2.0 and Docker – Piotr's TechBlog](https://piotrminkowski.wordpress.com/2018/08/02/quick-guide-to-microservices-with-kubernetes-spring-boot-2-0-and-docker/#:~:text=Before%20we%20proceed%20to%20the,and%20ingresses%20for%20API%20gateway)). Each service can be scaled independently and uses config and secrets provided by the platform instead of hardcoding ([Eureka Server: The Heart of Microservice Communication](https://www.mindbowser.com/microservices-with-eureka/#:~:text=Each%20service%20in%20the%20architecture,can%20have%20its%20own%20database)) ([Quick Guide to Microservices with Kubernetes, Spring Boot 2.0 and Docker – Piotr's TechBlog](https://piotrminkowski.wordpress.com/2018/08/02/quick-guide-to-microservices-with-kubernetes-spring-boot-2-0-and-docker/#:~:text=%28%60employee,and%20ingresses%20for%20API%20gateway)).

Finally, let’s talk strategy: in production, use a continuous integration/continuous deployment (CI/CD) pipeline to build Docker images and apply Kubernetes manifests (or use Helm charts for templating). Automated canary deployments can reduce risk. Always monitor after deployments, and have the ability to roll back (Kubernetes keeps revision history for Deployments – a simple `kubectl rollout undo deployment/order-service` can revert to previous version if something goes wrong).

With Docker and Kubernetes, our microservices are truly cloud-ready – they can be deployed onto any cloud or on-prem cluster in a reproducible way. This completes our journey: from design and development to deployment and operations.

## Conclusion

In this comprehensive guide, we built an advanced Spring Boot microservices architecture from the ground up. We started by designing small, single-responsibility services and enabling them to communicate through REST APIs and service discovery (Eureka) for location transparency. We tackled the critical cross-cutting concerns of logging and observability by implementing centralized logging to Elasticsearch/Kibana and distributed tracing with correlation IDs and tools like Zipkin/OpenTelemetry, giving us deep insight into the system’s behavior ([Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin#:~:text=Tracing%20is%20simple%2C%20in%20theory,it%27s%20easy%20to%20associate%20semantically)) ([MicroServices - Part 3 : Spring Cloud Service Registry and Discovery | SivaLabs](https://www.sivalabs.in/microservices-springcloud-eureka/#:~:text=We%20can%20use%20Netflix%20Eureka,ID%20to%20invoke%20REST%20endpoints)).

Security was addressed by leveraging OAuth2 and JWTs to secure microservice endpoints, following best practices to keep our services safe and adopting a token-based authentication model suitable for cloud environments. We integrated different data storage technologies (PostgreSQL and MongoDB) to showcase how each microservice can use the database that best fits its needs, while encapsulating data behind service boundaries ([Eureka Server: The Heart of Microservice Communication](https://www.mindbowser.com/microservices-with-eureka/#:~:text=They%20should%20be%20deployed%20independently,and%20another%20may%20use%20MongoDB)).

Performance and resilience were not afterthoughts but built-in: we introduced caching and other tuning measures to speed up our services, and we employed resilience patterns (circuit breakers, retries, bulkheads) to ensure the system stays responsive even when parts of it fail or slow down ([Circuit Breaker pattern - Azure Architecture Center | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker#:~:text=The%20Circuit%20Breaker%20pattern%20can,try%20to%20invoke%20the%20operation)) ([Resilience4J: Introduction to Bulkhead - Knoldus Blogs](https://blog.knoldus.com/resilience4j-introduction-to-bulkhead/#:~:text=patterns%20for%20building%20resilient%20applications,and%20how%20Resilience4J%20implements%20it)). These patterns, combined with Spring Cloud and Resilience4j, allow our microservices to **fail fast and recover gracefully**, preventing cascading failures and improving overall stability.

Finally, we containerized the microservices with Docker, ensuring consistent deployments across environments, and deployed them to Kubernetes for orchestration. Kubernetes brings features like self-healing, easy scaling, and rolling updates, which let us operate the microservices in production with confidence. We discussed how to manage configurations and secrets in a Kubernetes setup and how to expose and scale services, always with an eye on maintaining uptime and enabling continuous delivery.

Throughout this guide, we highlighted important **best practices** – from structuring code (modularity, clear API contracts) to handling data (transaction management and migration strategies), from writing idempotent retry-friendly operations to not logging sensitive information. We also stressed **observability**: logs, metrics, and traces form the nervous system of a microservices application in production. With our ELK and tracing setup, we can detect issues, debug incidents, and monitor performance trends proactively.

In summary, building microservices with Spring Boot is not just about writing business logic in smaller services – it’s about building an ecosystem around those services to support them in a production setting. This includes service discovery, centralized logging, distributed tracing, robust security, database management, resilience engineering, and scalable infrastructure. By following the step-by-step approach in this guide, you can create microservices that are **well-architected, observable, secure, and resilient**, and deploy them in a cloud-native fashion.

As you implement these in your own projects, remember to continuously test both functionality and failure modes. Invest in automating your deployment and incorporate feedback (like monitoring alerts) into your iterations. With these tools and practices, you’re well-equipped to build a production-grade microservices system using Spring Boot, Elasticsearch, Kibana, and the broader Spring Cloud ecosystem.
