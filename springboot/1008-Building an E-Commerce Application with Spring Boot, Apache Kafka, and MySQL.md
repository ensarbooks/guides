# Building an E-Commerce Application with Spring Boot, Apache Kafka, and MySQL

This guide provides a step-by-step approach for advanced developers to build a **microservices-based e-commerce application** using Spring Boot as the framework, Apache Kafka for event-driven communication, and MySQL as the relational database. We will cover everything from setting up the development environment to implementing core features, integrating Kafka, managing the database, ensuring security, deploying at scale, optimizing performance, testing, and even discuss future improvements like AI-driven recommendations. The content is structured into logical sections with clear headings, short paragraphs, code examples, best practices, and case-study insights.

## 1. Development Environment Setup

Setting up a robust development environment is the first step. We need to install the necessary platforms (Java, Spring Boot, Kafka, MySQL), configure our IDE and tools, and set up build processes.

### 1.1 Installing and Configuring Java, Spring Boot, Kafka, and MySQL

- **Java Development Kit (JDK)**: Install JDK 17 (or the latest LTS) for compatibility with Spring Boot 3.x. Verify the installation by running `java -version` in your terminal. Set `JAVA_HOME` environment variable to the JDK path.
- **Spring Boot CLI (optional)**: You can install the Spring Boot CLI for quick project setup, but it's not required. Many developers prefer using Spring Initializr (via the web or IDE integration) to generate a Spring Boot project.
- **Apache Kafka**: Download Kafka (which includes ZooKeeper for older versions) from the [Apache Kafka website](https://kafka.apache.org/quickstart). Extract it to a desired location. Kafka requires a running ZooKeeper instance for coordination (for Kafka < 3.x). Start ZooKeeper and Kafka servers using the provided scripts:

  ```bash
  # Start ZooKeeper (if using Kafka with ZooKeeper)
  bin/zookeeper-server-start.sh config/zookeeper.properties

  # Start Kafka broker
  bin/kafka-server-start.sh config/server.properties
  ```

  Alternatively, use Docker to set up Kafka quickly. For example, using Docker Compose can bring up Kafka and ZooKeeper containers. (We'll show a Docker Compose example in the Deployment section.)

- **MySQL Database**: Install MySQL Community Server and the MySQL Workbench if needed. On Linux, use apt or yum to install `mysql-server`; on Mac, use Homebrew; on Windows, use the MySQL installer. Secure your MySQL installation (set a root password). Create a database for each microservice (e.g., `catalog_db`, `order_db`, etc.) and create a dedicated user for each service with appropriate privileges. Verify you can connect (e.g., via `mysql -u username -p`).
- **Spring Initializer Project Setup**: Navigate to **start.spring.io** (Spring Initializr) or use IDE integration to generate a Maven/Gradle project. Select Java 17, Spring Boot version 3.x, and add dependencies: Spring Web, Spring Data JPA, Spring Security, Spring for Apache Kafka, MySQL Driver, Lombok (optional for reducing boilerplate), etc. You can also include Spring Boot DevTools for hot reloading in development.

After generating, import the project into your IDE. Ensure that the `application.properties` (or `application.yml`) has the basic configuration, for example for MySQL and Kafka connectivity:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/catalog_db
    username: catalog_user
    password: secret
  jpa:
    hibernate.ddl-auto: update # for development only, to auto-create tables
  kafka:
    bootstrap-servers: localhost:9092
```

(We will expand on configuration in later sections.)

### 1.2 Setting Up IDE (IntelliJ, VS Code) and Development Tools

- **Integrated Development Environment**: Choose an IDE that supports Spring Boot well. **IntelliJ IDEA** (Community or Ultimate) has excellent Spring and Spring Boot support, including live templates and code completion. **Visual Studio Code** with the _Spring Boot Extension Pack_ is another lightweight option. Ensure you have the Lombok plugin enabled in your IDE if you use Lombok.
- **Build and Dependency Management**: If you chose **Maven**, ensure Maven is installed or use the wrapper (`mvnw`). For **Gradle**, you can use the Gradle wrapper (`gradlew`). These tools will handle fetching dependencies and packaging the application. Verify the build by running `./mvnw clean package` or `./gradlew build` in the project directory.
- **Version Control**: Initialize a Git repository for your project. Use `.gitignore` to exclude build files (Maven’s target/ or Gradle’s build/ directories, etc) and any sensitive config (like `.env` files with passwords).
- **API Testing Tools**: Install Postman or VS Code REST Client plugin to test your REST APIs once you start building them. This helps in quickly verifying endpoints.
- **Other Tools**:
  - _cURL_ for quick API calls from the terminal.
  - _Docker_ for containerizing services (we'll use this later for deployment).
  - _Docker Compose_ for orchestrating multi-container environments (useful for running Kafka, ZooKeeper, and MySQL in development).
  - _Kafkacat (kcat)_ or Kafka CLI for sending/reading test messages to Kafka topics during development.

### 1.3 Configuring Build Tools: Maven or Gradle

Choose either Maven or Gradle based on your preference or organizational standards. Both can accomplish the same tasks:

- **Maven**: Check the `pom.xml` generated by Spring Initializr. It should contain dependencies such as:

  ```xml
  <dependencies>
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
      </dependency>
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-data-jpa</artifactId>
      </dependency>
      <dependency>
          <groupId>org.springframework.kafka</groupId>
          <artifactId>spring-kafka</artifactId>
      </dependency>
      <dependency>
          <groupId>mysql</groupId>
          <artifactId>mysql-connector-java</artifactId>
      </dependency>
      <!-- ... other dependencies like Spring Security, etc. -->
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-test</artifactId>
          <scope>test</scope>
      </dependency>
  </dependencies>
  ```

  The Spring Boot Maven plugin should also be present to allow running the app easily (`mvn spring-boot:run`) and to create executable jars.

- **Gradle**: If using Gradle, your `build.gradle` (or `build.gradle.kts`) will list similar dependencies. Ensure you apply the Spring Boot plugin and the dependency management plugin for Spring:

  ```groovy
  plugins {
      id 'org.springframework.boot' version '3.1.4'
      id 'io.spring.dependency-management' version '1.1.3'
      id 'java'
  }
  dependencies {
      implementation 'org.springframework.boot:spring-boot-starter-web'
      implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
      implementation 'org.springframework.kafka:spring-kafka'
      implementation 'mysql:mysql-connector-java'
      implementation 'org.springframework.boot:spring-boot-starter-security'
      testImplementation 'org.springframework.boot:spring-boot-starter-test'
  }
  ```

  You can run `./gradlew bootRun` to start the application in development.

- **Build Profiles**: Set up profiles (dev, prod) in application.yml for different configurations. For instance, in dev you might use `spring.jpa.hibernate.ddl-auto=update` and in prod use `validate` or migrations. Kafka broker address might differ (localhost for dev, a cluster for prod).

At this stage, you should have a basic Spring Boot application skeleton for each microservice in the system (or you can start with one multi-module project and split later). We will proceed to design the architecture before diving into coding each service.

## 2. Application Architecture

Designing the application architecture upfront helps in building a scalable and maintainable system. Our e-commerce platform will follow a **microservices-based architecture** where each core domain (products, orders, users, etc.) is a separate service. We will use an **event-driven architecture** with Kafka to enable services to communicate asynchronously. We'll plan the **database schema** for each service using MySQL, and outline the **API design** (using REST and possibly GraphQL) that the services expose.

### 2.1 Microservices-Based Design

**Decompose by Business Capability**: We divide the application into multiple microservices, each responsible for a specific business capability. Typical services in an e-commerce system might include:

- **Product Catalog Service** – manages products and their details.
- **User Service (Authentication & Profile)** – manages user accounts, authentication, and roles.
- **Order Service** – handles order creation and order lifecycle (processing, status).
- **Shopping Cart Service** – manages users' cart items (this could be combined with Order or separate).
- **Inventory Service** – tracks stock levels and warehouse operations.
- **Payment Service** – processes payments (or integrates with external payment gateways).
- **Notification Service** – sends emails or notifications for order status updates, etc.

Each microservice will have its own **database** (database-per-service pattern) to ensure loose coupling at the data level. This means, for example, the Product service has its own `products` schema in MySQL, the Order service has an `orders` schema, etc. Having separate databases per service avoids tight coupling and shared schemas, and it enables each service to evolve its database structure independently. In a microservice architecture, _“each service has its own database”_ is a recommended approach, and cross-service transactions are handled in other ways (discussed below) ([spring boot - Microservice database architecture for Ecommerce web app - Stack Overflow](https://stackoverflow.com/questions/61021346/microservice-database-architecture-for-ecommerce-web-app#:~:text=If%20you%20are%20using%20micro,idea%20on%20Saga%20pattern%20link)).

However, a challenge arises when a business process (like placing an order) spans multiple services and databases. We cannot use a traditional ACID transaction across microservices. Instead, we implement **distributed transactions** using the **Saga pattern**. A saga is essentially a sequence of local transactions in each service, coordinated via events. Each local transaction updates its own DB and then publishes an event to trigger the next step in the saga. If one step fails, compensating transactions are executed to undo the previous steps ([Pattern: Saga](https://microservices.io/patterns/data/saga.html#:~:text=Implement%20each%20business%20transaction%20that,by%20the%20preceding%20local%20transactions)). For example, an "Order Placement" saga might involve: Order service creates an order -> publishes an "Order Created" event -> Inventory service reserves stock -> publishes an event -> Payment service charges the customer -> publishes an event -> Order service marks order as confirmed. Should the payment fail, a compensation could be to release the stock and cancel the order.

Services communicate through **APIs** (for synchronous operations) and **events** (for asynchronous). We will use RESTful APIs for things like retrieving product info or placing an order (initial request from client to the system), but once an order is placed, the subsequent internal communications (inventory update, payment processing) will happen via Kafka events. This design ensures that services are not tightly coupled by direct calls.

In a microservices architecture:

- Each service can be built, deployed, and scaled independently.
- Failures are isolated (e.g., if the payment service is down, orders can still be accepted and queued for processing).
- We can use different tech stacks per service if needed (though in this guide we use Spring Boot for all, a homogeneous choice).
- **Database per service** also means we may duplicate some data or use events to maintain consistency. For example, the Order service may store a user's name or product snapshot to have historical data, even though that data originates in User or Product service. This avoids needing cross-service joins at runtime.

If we need to query data that spans services (say, display an order with product details and user info), one approach is **API Composition** (the client or an API Gateway calls multiple services and combines the data). Another approach is **CQRS (Command Query Responsibility Segregation)** combined with an event-driven approach: commands (transactions) are handled by the services, and query models are built by subscribing to events. For instance, a separate **Reporting service** could listen to order and product events and maintain a read-optimized view (maybe in a NoSQL or search index) for queries that require joining data from multiple services ([spring boot - Microservice database architecture for Ecommerce web app - Stack Overflow](https://stackoverflow.com/questions/61021346/microservice-database-architecture-for-ecommerce-web-app#:~:text=Since%20you%20are%20using%20multiple,to%20get%20an%20idea%20link)).

### 2.2 Event-Driven Architecture with Kafka

We leverage Apache Kafka to implement an **event-driven architecture (EDA)**. In an event-driven system, services communicate by publishing and consuming events rather than calling each other directly. **This decouples the services, making the overall system more scalable and resilient** ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=Event,reliability%2C%20scalability%2C%20and%20response%20times)). Instead of the Order service calling the Inventory and Payment services synchronously (which would create tight coupling and temporal dependencies), it simply emits an event to Kafka (e.g., "Order Placed"). Other services subscribe to the relevant topics and react accordingly.

**Why Kafka?** Kafka is a distributed event streaming platform that can handle a huge volume of events with low latency. It provides durability (events are stored on disk, replicated across brokers) and scalability (through topic partitioning). Kafka acts as a **message broker** that buffers and dispatches events, allowing our microservices to communicate asynchronously. By using Kafka, _microservices can communicate via events instead of direct HTTP calls, improving reliability and response times_ ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=Event,reliability%2C%20scalability%2C%20and%20response%20times)) ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=Kafka%20kafka,reliability%2C%20scalability%2C%20and%20response%20times)). Key benefits of Kafka for our architecture include: scalability (it can handle millions of events per second), fault tolerance (brokers form a cluster with data replication), and the ability to retain events for a period of time which enables event replay or auditing ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=Apache%20Kafka%20is%20a%20distributed,features%20that%20benefit%20microservices%20are)).

**Event Flow Example (Order Processing)**: For an e-commerce workflow:

1. **Order Placed** – When a customer places an order (via an API call to Order service), the Order service creates a new order in its database and emits an `"OrderPlaced"` event to a Kafka topic (say `order-events` topic).
2. **Inventory Update** – The Inventory service has a Kafka consumer listening on `order-events`. When it receives the `"OrderPlaced"` event, it will reserve or deduct the stock for the ordered items in its own database. After updating inventory, it could emit an `"InventoryReserved"` event (or if stock is insufficient, an `"InventoryFailed"` event).
3. **Payment Processing** – The Payment service, also listening on `order-events`, sees the `"OrderPlaced"` event and initiates payment processing (charging the customer via some gateway). It then emits a `"PaymentCompleted"` or `"PaymentFailed"` event.
4. **Order Completion** – The Order service listens on a Kafka topic (like `order-updates`) for results. It might wait for both Inventory and Payment outcomes. If both succeed, it updates the order status to "Confirmed" and emits an `"OrderConfirmed"` event (or sends a notification). If any fails, it emits `"OrderCancelled"` and possibly triggers compensating actions (e.g., if payment failed, release inventory via an event to inventory service).

By designing these events, each service only worries about its local transaction and business logic, and Kafka ensures the events get to where they need to go. For example, _when an order is placed, an “Order Placed” event is produced; other services like inventory and payment consume this event to perform their actions_ ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=In%20an%20event,each%20service%20is%20loosely%20coupled)). This **choreography-style saga** uses events for coordination. It's also possible to have an orchestration approach (with a central orchestrator telling each service what to do), but Kafka-based choreography fits well and avoids a single point of failure.

**Topics and Event Schema**: Define Kafka topics for each event stream. For clarity:

- `orders` topic – could carry events like OrderPlaced, OrderConfirmed, OrderCancelled.
- `inventory` topic – events like InventoryReserved, InventoryAdjusted.
- `payments` topic – PaymentCompleted, PaymentFailed.
- `notifications` topic – events for notifications (OrderConfirmed could be consumed by Notification service).
  We might also use a single topic per event type, or a combined topic with an event type field. For simplicity, using separate topics by domain is common.

Events can be represented as JSON structures or using a schema format like Avro with a schema registry for versioning. For now, assume JSON encoded events (Spring Kafka can use a JSON serializer to convert Java objects to JSON strings automatically).

**Scaling Consideration**: Kafka topics are partitioned. If we have high throughput (many orders), we can increase partitions on the `orders` topic so that multiple instances of Inventory service can parallelize processing (each instance in the same consumer group will get different partitions). This ensures our system can scale horizontally. With Kafka, _partitioning of topics across multiple brokers is a key to scalability and high throughput_ ([What makes Kafka high in throughput? - Stack Overflow](https://stackoverflow.com/questions/44621384/what-makes-kafka-high-in-throughput#:~:text=,flight%20messages)).

### 2.3 Database Schema Design with MySQL

Each microservice will have its own MySQL database schema tailored to its needs. Let's outline the schema for each main service:

- **Product Catalog DB (`catalog_db`)**: Contains a `products` table. Fields might include `id` (primary key), `name`, `description`, `price`, `stock` (or stock might be in Inventory service instead), `category_id`, etc. If there's category or brand, separate tables (or microservices if those are large domains).
- **User DB (`user_db`)**: Contains a `users` table for user accounts (fields: `id`, `email`, `password_hash`, `name`, etc.), a `roles` table or user_roles mapping if using roles. If using OAuth2, might not store passwords here but rather use an external IdP; but for our case, we can store hashed passwords for authentication.
- **Order DB (`order_db`)**: Contains an `orders` table (`id`, `user_id`, `status`, `total_amount`, `created_at`, etc.) and an `order_items` table (`order_id` -> `product_id`, quantity, price, etc.). Note: `user_id` here is a foreign key referencing a user in `user_db` logically, but since separate DB, it won't actually enforce the foreign key. It's just an identifier. We rely on the application to ensure the user exists (the Order service could call User service or use an event to validate user).
- **Inventory DB (`inventory_db`)**: If separate from product, contains an `inventory` table with `product_id` and `quantity` (stock). Alternatively, we could keep stock in the product table of catalog service if we don't want a separate service. In a larger system, inventory (warehouses, etc.) is often separate, so we're treating it separately.
- **Payment DB (`payment_db`)**: Might store records of payments: `payment_id`, `order_id`, `status`, `transaction_ref`, etc. Often, payment might not have a large internal DB if delegating to external gateways, but recording what happened is useful.
- **Others**: A `cart_db` if a Cart service exists (or we can keep cart in memory/Redis keyed by user session, to simplify not using MySQL for cart). A `notification_db` if we want to log notifications sent, etc., but these are optional.

**Schema Design Principles**:

- Use **normalized tables** to avoid data duplication within a service (3NF usually). For example, if Order needs product info, it might store only `product_id` and fetch details from Product service when needed, or store a snapshot of product name/price at time of order if needed for history (denormalization for a purpose).
- Ensure each table has a primary key (ints or UUIDs). Auto-increment integers are fine since each service DB is isolated (no conflict). We could use UUID for globally unique ids if that helps tracing across services, but that's optional.
- **Foreign Keys**: Since each service has its own DB, we do **not** have cross-service foreign key constraints. Within a service, you can use foreign keys (e.g., order_items.order_id references orders.id within Order DB).
- **Indexes**: Plan indexes on columns that will be searched or used in joins (within that service's context). For example, index `orders.user_id` to fetch orders by user quickly, index `products.name` if allowing name search, etc. We'll discuss indexing more in Section 5.3.

**Distributed Data Considerations**: With separate databases, joining data across services is done at the application level or via an aggregator. For example, to display an order confirmation page, the Order service might return order data including item IDs, then the UI or an API Gateway could call the Product service for names of those items. Another approach is to maintain a denormalized view: e.g., an _Order Read Model_ that gets product name and user info via events when an order is placed (CQRS pattern) ([spring boot - Microservice database architecture for Ecommerce web app - Stack Overflow](https://stackoverflow.com/questions/61021346/microservice-database-architecture-for-ecommerce-web-app#:~:text=Since%20you%20are%20using%20multiple,to%20get%20an%20idea%20link)). For now, design schemas such that each service can fulfill most of its own data needs, and use IDs to reference external data. Events will carry enough information to update other services if needed (for instance, an OrderPlaced event might contain the list of items with their names and prices to avoid another lookup).

We'll create the actual entities and relationships using JPA in code later, but having a clear mental model of the tables now is valuable.

### 2.4 API Design with REST and GraphQL

**RESTful APIs**: Each microservice exposes REST endpoints for its core functionality:

- Product Service might expose endpoints like:
  - `GET /products` (with filtering and pagination) – list products.
  - `GET /products/{id}` – get product details.
  - `POST /products` – add new product (admin only).
  - `PUT /products/{id}` – update product.
  - `DELETE /products/{id}` – remove product.
- Order Service endpoints:
  - `POST /orders` – place a new order (the client provides cart details or references).
  - `GET /orders/{id}` – get order status and details.
  - `GET /orders/user/{userId}` – list orders for a user (with auth, a user sees their orders).
- Cart Service endpoints:
  - `GET /cart` (for current user) – view cart.
  - `POST /cart` – add item to cart.
  - `DELETE /cart/{itemId}` – remove item from cart.
- User Service endpoints:
  - `POST /users` – create new user (registration).
  - `POST /auth/login` – authenticate and obtain a token (if doing JWT ourselves).
  - `GET /users/me` – get current user profile (after auth).
- etc.

We aim for **clean REST design**: use nouns and HTTP methods, proper status codes (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, etc.), and include HATEOAS links if needed (not mandatory).

**GraphQL**: GraphQL can be introduced for more flexible querying needs or to minimize round trips. With GraphQL, the client can ask for exactly the data it needs, potentially aggregating from multiple sources in one query. For example, a single GraphQL query could fetch a list of products with their inventory and category info, which might otherwise require calling product service then inventory service. GraphQL is beneficial if:

- The client (like a React app) wants to reduce multiple REST calls into one.
- You want to give clients the ability to query varying data shapes (avoiding the need for many specific REST endpoints).

Spring Boot has the **Spring for GraphQL** library that integrates GraphQL with Spring (which uses the graphql-java library under the hood). In a microservices scenario, you might implement GraphQL at the API Gateway level, or have a GraphQL service that federates calls to underlying services.

**When to use GraphQL**: If your application needs more flexibility in responses (e.g., mobile vs web clients need different data amounts), strong schema type safety, or to easily retrieve connected data, GraphQL can help ([Getting Started | Observing GraphQL in action](https://spring.io/guides/topicals/observing-graphql-in-action#:~:text=,information%20is%20returned%20by%20endpoints)). For example, retrieving an order and including product details might be a complex operation via REST (or require the client to call both Order and Product APIs). With GraphQL, you could define a query like:

```graphql
query getOrder($orderId: ID!) {
  order(id: $orderId) {
    id
    status
    items {
      product {
        name
        price
      }
      quantity
    }
    user {
      name
      email
    }
  }
}
```

This single query would fetch an order, and for each item get the product info and the user info, possibly by behind the scenes calling multiple services or using a data loader cache. Essentially, GraphQL provides a **flexible, strongly-typed schema** that can span multiple underlying REST services, helping to expose connected data in a single request ([Getting Started | Observing GraphQL in action](https://spring.io/guides/topicals/observing-graphql-in-action#:~:text=,information%20is%20returned%20by%20endpoints)).

For our guide, implementing GraphQL is optional, but we outline it for completeness. In practice, you might start with REST for each service and later introduce GraphQL if the front-end requires it. It's possible to run GraphQL within each microservice (e.g., Product service could offer GraphQL for product queries), but a more common approach is a **BFF (Backend-For-Frontend)** or API Gateway that aggregates.

We will primarily focus on REST for core implementation and mention GraphQL as an enhancement. If implementing, Spring for GraphQL would be added and you'd define GraphQL schemas and controllers (Query and Mutation resolvers) in the relevant service.

Next, let's dive into implementing core functionalities for each service, following the architecture we've laid out.

## 3. Core Functionalities Implementation

In this section, we break down the development of key services and features of the e-commerce application. We'll go through each major functionality: product catalog, user authentication, shopping cart & orders, payment integration, inventory management, and notifications. Each will be treated as a microservice or module, showing important code snippets and design considerations.

### 3.1 Product Catalog Service (CRUD, Search, Caching)

The **Product Catalog Service** is responsible for managing product information and making it available to other parts of the system. This service will handle creating, reading, updating, and deleting products (CRUD operations), providing search functionality, and leveraging caching to improve performance.

**Project Setup**: We create a Spring Boot application (e.g., `catalog-service`). Include dependencies: Spring Web, Spring Data JPA, MySQL driver, (Spring Cache with a cache provider like Redis if we plan to use caching).

**Domain Model**: Define a JPA entity for Product:

```java
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String description;
    private BigDecimal price;
    private String category;
    // If Inventory is separate, maybe no stock here; otherwise include stock field
    // getters and setters...
}
```

A repository interface for data access:

```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    // Derived query example:
    List<Product> findByNameContaining(String keyword);
}
```

This gives basic CRUD methods by default and a custom finder for searching by name (using JPA query derivation).

**Service Layer**: Create a `ProductService` class to handle business logic (like applying caching or handling any complex operations). For instance, if a product is updated, maybe we clear some caches or publish an event (if other services need to know product data changed – e.g., if product name changes, maybe notify search service, etc.).

**Controller**: Expose REST endpoints:

```java
@RestController
@RequestMapping("/products")
public class ProductController {
    @Autowired private ProductService productService;

    @GetMapping
    public List<Product> listProducts(@RequestParam(value="q", required=false) String query) {
        if (query != null) {
            return productService.searchProducts(query);
        }
        return productService.getAllProducts();
    }

    @GetMapping("/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productService.getProductById(id);
    }

    @PostMapping
    public Product createProduct(@RequestBody Product newProduct) {
        return productService.saveProduct(newProduct);
    }
    // ... PUT for update, DELETE for delete
}
```

This provides endpoints to list products (optionally filtering by a query), get one by ID, and modify products. In a real application, you'd add input validation and error handling (e.g., return 404 if product not found, etc.), and restrict modification endpoints to admin roles (with Spring Security).

**Search functionality**: The simple approach shown uses JPA's `findByNameContaining` for basic substring search. For more advanced search (by category, tags, full-text, etc.), you might introduce specifications or use Spring Data JPA's Criteria API. At a certain scale or complexity, integrating a search engine like Elasticsearch would be beneficial, but that's beyond our current scope. We'll stick to simple search queries in MySQL for now.

**Caching Mechanism**: To improve read performance, especially for expensive operations (like loading a product list or details that don't change often), we can introduce caching. Spring Boot’s caching abstraction makes it easy to add cache with annotations. For example, we can annotate the `getProductById` method in the service:

```java
@Service
public class ProductService {
    @Autowired private ProductRepository repo;

    @Cacheable(value = "products", key = "#id")
    public Product getProductById(Long id) {
        // This will be cached after first retrieval
        return repo.findById(id)
                   .orElseThrow(() -> new ProductNotFoundException(id));
    }

    public List<Product> getAllProducts() { return repo.findAll(); }

    public List<Product> searchProducts(String keyword) {
        return repo.findByNameContaining(keyword);
    }

    @CacheEvict(value = "products", key = "#product.id")
    public Product saveProduct(Product product) {
        // Evict cache for this product (if updating existing)
        return repo.save(product);
    }
}
```

We choose a cache provider – e.g., Redis – to back this. In `application.yml`, you'd configure:

```yaml
spring.cache.type: redis
spring.redis.host: localhost
spring.redis.port: 6379
```

Assuming a Redis server is running. Redis is a great choice for caching because it’s in-memory and can handle frequent reads/writes. It significantly improves response times for read-heavy workloads ([Redis as a Cache Boosting Performance and Scalability](https://www.inexture.com/redis-as-a-cache-spring-boot-java/#:~:text=1.%20Read,on%20backend%20databases%20and%20APIs)). _Redis caching offers substantial performance improvements, reducing database load and providing faster data access for frequently requested data ([Redis as a Cache Boosting Performance and Scalability](https://www.inexture.com/redis-as-a-cache-spring-boot-java/#:~:text=1.%20Read,on%20backend%20databases%20and%20APIs))_.

In our context, if the product data doesn't change often, caching product details in Redis means subsequent requests for the same product ID will be served quickly without hitting MySQL repeatedly. Keep cache entries updated: when a product is modified or removed, evict or update the cache accordingly (as shown with `@CacheEvict` on save/delete methods).

**Event Publishing** (optional): If other services need to know about changes in products (for example, if the product name or price change should update a search index or an analytics service), the Product service could publish Kafka events on changes. For instance, after saving a product, send a `"ProductUpdated"` event to a `product-events` topic. This can be done by autowiring a `KafkaTemplate` and sending the message. However, to keep things simpler, we'll not delve deep into product events here.

At this point, the Product Catalog Service can run independently, connect to its `catalog_db`, and serve product information. We should test it (via unit tests and by running the app to call the endpoints) to ensure CRUD and search work, before moving on.

### 3.2 User Authentication and Authorization (OAuth2, JWT, Spring Security)

The **User Service** handles user registration, login, and authentication/authorization concerns. Security is critical in e-commerce (for protecting user data, preventing fraud, etc.), so we'll use Spring Security to implement robust auth with JWT tokens and possibly OAuth2.

**User Domain**: A `User` JPA entity with fields like id, email, password (hashed), roles, etc. For example:

```java
@Entity
@Table(name="users")
public class User {
    @Id @GeneratedValue
    private Long id;
    private String email;
    private String password; // stored as bcrypt hash
    private String role; // e.g., "USER" or "ADMIN"
    // ... getters/setters
}
```

We can store a simple role string, or have a separate Role entity and a many-to-many relation if users can have multiple roles. Simplicity is fine for now.

**Password Hashing**: Always store passwords securely. Use BCrypt (Spring Security provides `BCryptPasswordEncoder`). E.g., when registering, do:

```java
String rawPw = user.getPassword();
user.setPassword(passwordEncoder.encode(rawPw));
userRepo.save(user);
```

This way, even if the database is compromised, passwords are not stored in plain text.

**Spring Security Configuration**: We configure Spring Security to handle authentication. There are a couple of approaches:

- Use Spring Security's built-in form login or basic auth (not ideal for an API).
- Implement JWT-based stateless authentication, where a user provides credentials to get a token, then uses that token for subsequent requests.
- Use OAuth2 Authorization Server (like Keycloak or Okta) – since this is an advanced guide, one could set up an external identity provider. But we can also simulate it by issuing JWTs ourselves for brevity.

Let's outline a JWT approach:

1. **Login Endpoint**: `POST /auth/login` with JSON body containing email and password. The User service verifies the credentials (using `UserDetailsService` to load the user and `PasswordEncoder` to match password). If valid, it generates a JWT token signed with a secret key.
2. **JWT Token**: Contains user identifier and roles in claims. The token is returned to the client.
3. **Subsequent Requests**: The client includes the JWT in `Authorization: Bearer <token>` header. Spring Security filters will validate this token on each request.
4. **Security Filter**: Use `spring-boot-starter-oauth2-resource-server` library to validate JWT tokens (if we use OAuth2 JWT). Or manually use a OncePerRequestFilter to parse tokens. The recommended way in Spring Security 5+ is to configure it as a Resource Server with JWT if possible.

**Spring Security Setup**:
In a Spring Boot 3 app, we can define a SecurityFilterChain bean:

```java
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
          .csrf().disable()  // disable CSRF for API (if not using cookies)
          .authorizeHttpRequests(auth -> auth
              .requestMatchers("/auth/**").permitAll()
              .anyRequest().authenticated()
          )
          .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        // JWT filter configuration:
        http.oauth2ResourceServer().jwt(); // if using JWT as OAuth2 resource server
        return http.build();
    }
}
```

We also need to provide the public key or secret for JWT validation. For simplicity, using a symmetric secret:

```yaml
spring.security.oauth2.resourceserver.jwt.secret: my-jwt-signing-secret
```

With this, Spring Security will automatically validate incoming tokens for us.

**Issuing JWT**: Create a controller for auth:

```java
@RestController
@RequestMapping("/auth")
public class AuthController {
    @Autowired AuthenticationManager authManager;
    @Autowired JwtTokenProvider tokenProvider;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest login) {
        try {
            Authentication authentication = authManager.authenticate(
                new UsernamePasswordAuthenticationToken(login.getEmail(), login.getPassword()));
            UserDetails user = (UserDetails) authentication.getPrincipal();
            String jwt = tokenProvider.generateToken(user);
            return ResponseEntity.ok(new JWTResponse(jwt));
        } catch (BadCredentialsException ex) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
        }
    }
}
```

Where `JwtTokenProvider` is a component that generates JWT using a library like io.jsonwebtoken (JJwt) or the JWT support in Spring Security (we might need to manually sign here since we used Resource Server just to validate). This is a bit involved but essentially:

```java
public String generateToken(UserDetails userDetails) {
    Date now = new Date();
    Date expiry = new Date(now.getTime() + JWT_EXPIRATION);
    return Jwts.builder()
        .setSubject(userDetails.getUsername())
        .claim("roles", userDetails.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList())
        .setIssuedAt(now)
        .setExpiration(expiry)
        .signWith(SignatureAlgorithm.HS256, jwtSecret)
        .compact();
}
```

This token will include username (email) and roles.

**Using OAuth2**: The above is a custom JWT solution. Alternatively, one could use Spring Authorization Server or Keycloak, but that would add complexity beyond the scope. The key point is the **User service (or Auth service)** is in charge of authenticating users and issuing tokens. All other services will trust these tokens for authorization. Each service will need to share the JWT validation configuration (same secret or public key if using RSA).

**Authorization**: We ensure proper access control:

- Normal users can retrieve and modify their own data, place orders, etc.
- Admin users can manage product catalog, view all orders, etc.
  We can enforce this via method-level security (`@PreAuthorize("hasRole('ADMIN')")` on admin endpoints) or via URL patterns in the Security config (`.requestMatchers("/admin/**").hasRole("ADMIN")` etc).

Also consider **OAuth2 scopes** if this were a third-party integration scenario (probably not needed here).

**Preventing vulnerabilities**: Using Spring Security and following best practices covers a lot: e.g., it protects against session fixation, CSRF (if enabled for forms), etc. We'll discuss specific security best practices in Section 6, but note that our JWT approach is stateless so CSRF is less of a concern (since we don't rely on cookies by default).

**Testing Security**: After implementing, test:

- Register a new user (or insert one in DB with hashed password).
- Login via `/auth/login`, get token.
- Call a protected endpoint (like GET /products) with the token in Authorization header and verify you get data. Without token, you should get 401 Unauthorized.
- Test role restrictions by marking an endpoint admin-only and verifying a normal user token is forbidden (403).

At this point, we have a basic auth system in place. The User service could also manage profiles, addresses, etc., but we focus on auth here. Now users can securely interact with the system. We'll integrate this with other services (e.g., Order service will require a valid user token to place an order, so the Order service will trust the JWT and extract the user ID from it to know who is ordering).

### 3.3 Shopping Cart and Order Management

The **Shopping Cart** and **Order** functionality form the crux of the e-commerce workflow. We will handle them together, as the cart is often a precursor to an order.

**Shopping Cart Service**: This service (or component) keeps track of items a user intends to purchase. There are multiple ways to handle a cart:

- Keep it client-side (in browser local storage) and send all items during checkout – not secure or reliable.
- Keep it server-side in a database.
- Keep it in an in-memory store like Redis (which is fast and can persist if needed).
  For scalability, a distributed cache like Redis is a great option for cart data, since cart data is often ephemeral and tied to user sessions. However, implementing it in MySQL is also fine if we ensure to clean up stale carts.

For simplicity, let's assume we manage cart server-side in memory (with Redis or an in-memory map for a single server scenario). If using microservices, a dedicated **Cart service** could be created that offers APIs to add/remove items and retrieve the cart.

**Cart API Example**:

```java
@RestController
@RequestMapping("/cart")
@PreAuthorize("hasRole('USER')")
public class CartController {
    @Autowired CartService cartService;

    @GetMapping
    public Cart getCart(Authentication auth) {
        String userEmail = auth.getName();
        return cartService.getCart(userEmail);
    }

    @PostMapping
    public ResponseEntity<?> addToCart(Authentication auth, @RequestBody CartItem item) {
        cartService.addItem(auth.getName(), item);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{productId}")
    public void removeFromCart(Authentication auth, @PathVariable Long productId) {
        cartService.removeItem(auth.getName(), productId);
    }
}
```

Here, `Authentication auth` is provided by Spring Security (the JWT filter populates it). We use `auth.getName()` (which by default is username/email) to identify the user.

The CartService might use a `ConcurrentHashMap<String, Cart>` as a simple store (for single-instance demo) or ideally use Redis (storing cart items under a key like `"cart:user@example.com"`).

**CartItem** could have productId and quantity (we can fetch product details from Product service when displaying cart, or store name/price snapshot as well for convenience).

**Order Service**: The Order service orchestrates the order placement. When a user is ready to checkout, they will call the Order service to convert their cart into an order.

**Order Placement (Synchronous)**:
We expose an endpoint in Order service, e.g.:

```java
@PostMapping("/orders")
public ResponseEntity<Order> placeOrder(Authentication auth) {
    String userEmail = auth.getName();
    Order order = orderService.createOrder(userEmail);
    return ResponseEntity.status(HttpStatus.CREATED).body(order);
}
```

This assumes the Order service knows how to get the user's cart. There are a couple of approaches:

- **Approach A**: The client sends the cart data along with the request (e.g., in the body of `/orders` call, include list of items). The Order service then uses that directly. This is stateless from the server perspective.
- **Approach B**: The Order service calls the Cart service internally (or if Cart is not separate, it reads the cart from cache/DB) to get the user's cart items.
  We can use approach A for simplicity: let the client send cart items. However, that trusts the client data. For security, approach B is better – since our cart is stored server-side tied to the user, the server can fetch the authoritative list of items.

Let's say we do Approach B for integrity:

```java
@Service
public class OrderService {
    @Autowired CartService cartService;
    @Autowired OrderRepository orderRepo;
    @Autowired OrderItemRepository itemRepo;
    @Autowired KafkaTemplate<String, Object> kafkaTemplate;

    @Transactional
    public Order createOrder(String userEmail) {
        Cart cart = cartService.getCart(userEmail);
        if (cart.isEmpty()) {
            throw new IllegalStateException("Cart is empty");
        }
        // Create Order record
        Order order = new Order();
        order.setUserEmail(userEmail);
        order.setStatus("PENDING");
        order.setOrderDate(LocalDateTime.now());
        orderRepo.save(order);
        // Create OrderItems records
        for (CartItem ci : cart.getItems()) {
            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setProductId(ci.getProductId());
            item.setProductName(ci.getProductName()); // storing snapshot
            item.setQuantity(ci.getQuantity());
            item.setPrice(ci.getPrice());
            itemRepo.save(item);
        }
        // Clear the user's cart
        cartService.clearCart(userEmail);
        // Publish OrderPlaced event
        OrderPlacedEvent event = new OrderPlacedEvent(order.getId(), userEmail, order.getItems());
        kafkaTemplate.send("orders", event);
        return order;
    }
}
```

The above does several important things:

- Begins a database transaction to save the order and items atomically in the order service DB.
- After saving, clears the cart.
- Constructs an `OrderPlacedEvent` containing order details (at least order ID, maybe item IDs/quantities, and user info needed by others) and publishes it to the `"orders"` Kafka topic. This event will be consumed by Inventory and Payment services to continue the process asynchronously.

Notice we've set the order status to "PENDING". The order isn't confirmed until payment and inventory steps succeed. The status will be updated later (we'll handle that in the Kafka integration part).

We should define the `OrderPlacedEvent` class (could be a simple POJO or a record, and it will be serialized to JSON by Spring Kafka if properly configured with a JSON serializer). For example:

```java
public class OrderPlacedEvent {
    private Long orderId;
    private String userEmail;
    private List<OrderItemInfo> items;
    // constructors, getters...
}
public class OrderItemInfo {
    private Long productId;
    private int quantity;
    // maybe price, name if needed by other services
}
```

We include necessary info for Inventory (needs productId and quantity) and Payment (might need order total amount or orderId to correlate payment).

Now, focusing on **Inventory and Payment reactions**:

### 3.4 Payment Gateway Integration

The **Payment Service** is responsible for handling payments. In a real-world scenario, this service would integrate with an external payment gateway (such as Stripe, PayPal, Braintree, etc.) to actually charge the customer's credit card or account. For our design:

- The Payment service listens for Order events (likely the "OrderPlaced" event).
- Upon receiving an order event, it attempts to process payment for that order.
- We'll simulate this by perhaps just waiting a moment and then marking as paid (in a real integration, you'd use the gateway's SDK or REST API).
- The service then emits a result event: either "PaymentCompleted" (with orderId, maybe transactionId) or "PaymentFailed" (with orderId and reason).

**Integration with external gateway**: Typically involves:

- Collecting payment details (credit card info, etc.). Usually, you don't want to handle raw card data directly due to PCI compliance. Instead, one would use a tokenization mechanism (the front-end might use Stripe.js to get a token representing the card, then your backend uses that token to charge).
- For our guide, we assume the payment details are provided at checkout. Perhaps the Order placement request includes a payment token or method. The OrderPlacedEvent might carry a payment token or an identifier to use for charging. Alternatively, the Payment service could call back to a stored payment method for the user.

To keep it high-level, let's say the OrderPlacedEvent contains a field `paymentInfo` (could be an ID or token). Payment service uses that to call an external API. We'll pseudocode it:

```java
@KafkaListener(topics = "orders", groupId = "payment-service")
public void handleOrderPlaced(OrderPlacedEvent event) {
    // Attempt payment
    PaymentResult result = paymentGateway.charge(event.getPaymentInfo(), event.getTotalAmount());
    if (result.isSuccess()) {
        // Save payment record in DB
        PaymentRecord rec = new PaymentRecord(event.getOrderId(), result.getTransactionId(), "COMPLETED");
        paymentRepo.save(rec);
        // Emit PaymentCompleted event
        PaymentCompletedEvent completed = new PaymentCompletedEvent(event.getOrderId(), result.getTransactionId());
        kafkaTemplate.send("payments", completed);
    } else {
        // Save failed attempt
        paymentRepo.save(new PaymentRecord(event.getOrderId(), null, "FAILED"));
        PaymentFailedEvent failed = new PaymentFailedEvent(event.getOrderId(), result.getFailureReason());
        kafkaTemplate.send("payments", failed);
    }
}
```

This assumes we configured Kafka consumer for Payment service. We'll cover Kafka integration in Section 4, but suffice to say Payment service subscribes to the "orders" topic events.

**External Payment API**: This could be an HTTP call to Stripe or another service. Many provide SDKs. For instance, using Stripe's Java library:

```java
Stripe.apiKey = "sk_test_123...";
ChargeCreateParams params = ChargeCreateParams.builder()
    .setAmount(event.getTotalAmount().movePointRight(2).longValue()) // amount in cents
    .setCurrency("usd")
    .setDescription("Order #" + event.getOrderId())
    .setSource(event.getPaymentInfo()) // token from client
    .build();
Charge charge = Charge.create(params);
```

We won't include the library code in detail, but this is how one would charge.

**Payment Service DB**: The service might have a `payments` table to log transactions. Fields: orderId, status, transactionId, amount, timestamp.

**Edge cases**: Payment could succeed but Inventory fails (or vice versa). Our Saga must handle that: If payment succeeded but inventory not available, we might refund/cancel payment. Saga coordination could get complex – possibly the Order service waits for both and then if one fails, triggers compensation. For now, assume both services do their best and Order service will decide outcome (if any failure event comes, it cancels the order and if payment was done, perhaps issue a refund event which Payment service could act on).

### 3.5 Inventory and Warehouse Management

The **Inventory Service** manages stock levels for products. It ensures that when an order is placed, the items are in stock and reserves or deducts the stock quantity. It may also handle restocking, low-stock alerts, etc., but we'll focus on the order flow.

**Inventory Reaction to OrderPlaced**:

- On receiving an OrderPlacedEvent, for each item, check if the requested quantity is available.
- If all items are available, deduct the quantities (reserve the stock for that order).
- Emit an InventoryReservedEvent (with orderId, maybe a list of item IDs reserved).
- If any item is out of stock, emit an InventoryFailedEvent for that order (and possibly trigger a restock alert, not covered here).

**Data**: The Inventory service likely has an `inventory` table: product_id, quantity_available (and perhaps location if multiple warehouses, but skip that detail). The Product and Inventory services could be separate or combined; we have them separate for demonstration.

**Consistency**: Inventory must ensure thread-safe operations on stock. Since orders come in via Kafka events possibly in parallel, if two orders request the last unit of a product at the same time, only one should succeed. With a single Inventory service instance, we can synchronize on update or use DB row locking (`SELECT ... FOR UPDATE` or optimistic locking with a version column). In a distributed environment, an approach is to handle each product's stock in a single thread/partition to avoid concurrent modifications (for example, partition Kafka events by productId for inventory events).

Our approach: use the database with proper constraints. A simple solution: in InventoryService, when deducting stock:

```java
@KafkaListener(topics = "orders", groupId = "inventory-service")
@Transactional
public void handleOrderPlaced(OrderPlacedEvent event) {
    boolean allAvailable = true;
    for (OrderItemInfo item : event.getItems()) {
        Inventory inv = inventoryRepo.findByProductId(item.getProductId());
        if (inv.getQuantity() < item.getQuantity()) {
            allAvailable = false;
            break;
        }
        inv.setQuantity(inv.getQuantity() - item.getQuantity());
        inventoryRepo.save(inv);
    }
    if (allAvailable) {
        kafkaTemplate.send("inventory", new InventoryReservedEvent(event.getOrderId()));
    } else {
        // If not available, maybe roll back changes for this order (transaction rollback will undo any partial deduction)
        kafkaTemplate.send("inventory", new InventoryFailedEvent(event.getOrderId()));
    }
}
```

By wrapping in a @Transactional, if any item fails availability, we throw an exception to roll back the whole transaction (so we don't partially deduct). Then we send a failure event. If all succeed, we commit and send a reserved event.

**InventoryReservedEvent** could list the items reserved or at least identify the order. The Order service will use this to know inventory step succeeded.

**Warehouse Management**: If we had multiple warehouses, the Inventory service might choose which warehouse to fulfill from, and possibly split the order. That's beyond our scope, but just to note: the system could be extended for multi-warehouse by adding an attribute for location in events.

**Stock Replenishment**: Not covered here, but one could have an admin interface or automated supplier integration to increase inventory. That would likely also be an event or an API (e.g., a `REST PUT /inventory/{productId}` to set new stock, which could emit an event if needed).

After Inventory processes an order, the next step is finalizing the order based on inventory and payment results.

### 3.6 Notifications and Email Service (Kafka Integration)

The **Notification Service** handles sending out notifications to users. Common notifications in e-commerce:

- Order confirmation email when an order is placed (or confirmed).
- Shipping notification when an order is shipped (not in our simplified flow, but could be a future event).
- Password reset emails, promotional emails, etc., could also be handled similarly.

For our scenario, we will send an email when an order is confirmed (payment and inventory succeeded). The Notification service can subscribe to a topic that indicates order completion or status changes.

**Design**:

- The Order service, after processing outcomes from Inventory and Payment, will determine the final order status. If order is confirmed, it emits an "OrderConfirmed" event (to perhaps an `orders` or `notifications` topic). If order failed (due to payment or stock), it might emit "OrderCancelled".
- The Notification service listens on these events. When an OrderConfirmedEvent is received, it composes an email (or any notification like SMS) to the user with the order details.

**Using Kafka for notifications** decouples it nicely – the Order service doesn't need to directly call an email API, it just emits an event and forgets. The dedicated service handles the rest.

**Tech for Email**: We can use JavaMail (Jakarta Mail) to send SMTP emails, or use a third-party service API (SendGrid, Mailgun, etc.). For simplicity, let's assume we have SMTP configured.

**Code**:

```java
@KafkaListener(topics = "orders", groupId = "notification-service")
public void handleOrderEvents(OrderStatusEvent event) {
    if (event.getStatus().equals("CONFIRMED")) {
        // Lookup user email from event (if not included, might need to call User service or include email in event)
        String userEmail = event.getUserEmail();
        // Compose email content
        String subject = "Order #" + event.getOrderId() + " Confirmed";
        String text = "Dear customer, your order has been confirmed. Details: ...";
        emailService.sendEmail(userEmail, subject, text);
    }
    // handle other statuses if needed (CANCELLED -> send cancellation email, etc.)
}
```

Here `OrderStatusEvent` is a generic event that Order service would emit containing orderId, userEmail, and status. We might prefer a specific `OrderConfirmedEvent(userEmail, orderId)` for simplicity.

**EmailService** could use Spring's `JavaMailSender`:

```java
@Component
public class EmailService {
    @Autowired JavaMailSender mailSender;

    public void sendEmail(String to, String subject, String text) {
        SimpleMailMessage msg = new SimpleMailMessage();
        msg.setTo(to);
        msg.setSubject(subject);
        msg.setText(text);
        mailSender.send(msg);
    }
}
```

And configure SMTP in application.yml (like host, port, username, password for an SMTP server).

**Notification Types**: We focus on email, but the service could also send SMS (using an SMS gateway API) or push notifications (to a mobile app). Kafka helps to add more without affecting order processing – e.g., a separate consumer could listen for the same events and send a push notification.

This completes the core flow from adding to cart -> placing order -> inventory & payment -> confirmation & notification. We have intentionally offloaded the cross-service communication to Kafka events, which we will detail next in the Kafka integration section.

## 4. Kafka Integration

We have mentioned Kafka in the architecture and core implementation sections as the glue for our microservices' communication. In this section, we'll go deeper into how to integrate Kafka with Spring Boot: setting up topics, producers, consumers, and using Kafka Streams for further data processing (like analytics).

### 4.1 Setting Up and Configuring Kafka Topics, Producers, and Consumers

**Kafka Configuration in Spring Boot**: Spring Boot simplifies Kafka integration via the **spring-kafka** library. In each service that uses Kafka (Order, Inventory, Payment, Notification, etc.), we include `spring-kafka` dependency. Configuration is typically done in `application.yml`:

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: <service-group-id>
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "*"
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

This config:

- Points to Kafka running on localhost.
- Sets a default consumer group ID (each service should have its own group).
- Configures JSON serialization/deserialization for values, so we can send Java objects (events) and have them automatically converted to/from JSON.
- `spring.json.trusted.packages: "*"` is set to trust all packages for deserialization (in a real app, list specific packages for security).

We also ensure each event class is in the package known to the deserializer. Alternatively, we could use StringSerializer and manually handle JSON (but Spring Kafka's JsonSerializer is convenient).

**Creating Topics**: Kafka doesn't require pre-creating topics if `auto.create.topics.enable` is true on the broker (often it is by default). However, in production it's better to create topics with proper partitions and replication. We can use Spring Kafka's `KafkaAdmin` to declare topics on startup:

```java
@Bean
public NewTopic ordersTopic() {
    return TopicBuilder.name("orders").partitions(3).replicas(1).build();
}
@Bean
public NewTopic paymentsTopic() {
    return TopicBuilder.name("payments").partitions(3).replicas(1).build();
}
@Bean
public NewTopic inventoryTopic() {
    return TopicBuilder.name("inventory").partitions(3).replicas(1).build();
}
```

This would create topics if they don't exist. We choose 3 partitions for each as an example, which means we can have up to 3 consumer instances in a group processing in parallel.

**Producer Implementation**: In Spring, we typically autowire a `KafkaTemplate<K, V>` for sending messages. We've shown usage in OrderService (sending OrderPlacedEvent) and in other services. For example, sending an event:

```java
@Autowired private KafkaTemplate<String, Object> kafkaTemplate;

public void publishOrderPlaced(OrderPlacedEvent event) {
    kafkaTemplate.send("orders", event.getOrderId().toString(), event);
}
```

We use orderId as the key so that all events for a given order go to the same partition (useful for ordering guarantees per order). The value is the event object. Because of JsonSerializer, it will convert the object to JSON.

The KafkaTemplate also has asynchronous send (returns a Future) which we can handle or add a callback to log success/failure. At least logging exceptions from `send` is recommended.

**Consumer Implementation**: Spring Kafka allows creating listeners using `@KafkaListener` on methods. We saw an example in InventoryService and PaymentService pseudocode:

```java
@KafkaListener(topics = "orders", groupId = "inventory-service")
public void handleOrderPlaced(OrderPlacedEvent event) {
    // process event...
}
```

We specify `groupId` either in the annotation or rely on the spring.kafka.consumer.group-id property. The method signature can directly take the event object (provided we configured JsonDeserializer with trusted packages). Alternatively, the method can take a `ConsumerRecord<String, OrderPlacedEvent>` if we need metadata (like offset, headers).

Ensure to handle exceptions in consumer logic. By default, if an exception is thrown, the listener container will retry (depending on config) or stop. Spring Kafka provides a SeekToCurrentErrorHandler or DeadLetterPublishingRecoverer to deal with poison pills (messages that always fail). For example, we could configure a dead-letter topic for events that repeatedly fail processing. Given this is an advanced guide, mention that:

- Use **error handlers** or **Dead Letter Queues** for robust processing. For instance, configure the consumer factory with `SeekToCurrentErrorHandler` to retry a few times and then send the message to a `_DLQ` topic if still failing.

**Example**: In Payment service, if calling external gateway fails due to network issues, we might throw an exception. We want to retry that a few times before giving up. Kafka can handle this by not committing the offset until success. We could also catch exceptions and emit a failure event directly.

**Logging & Monitoring**: It's helpful to log events consumption and production in each service. Also, use Kafka metrics or JMX to monitor consumer lag, etc., which we will integrate into monitoring later.

By establishing these producers and consumers, our services are now **linked by Kafka topics**. The sequence when an order is placed is:

1. Order service produces to `orders` topic.
2. Inventory and Payment consume from `orders` topic (in their own consumer groups "inventory-service" and "payment-service"). Both see the OrderPlacedEvent and process in parallel.
3. Inventory produces to `inventory` topic with result (success/failure).
4. Payment produces to `payments` topic with result.
5. Order service has consumers for `inventory` and `payments` topics (or possibly the same `orders` topic if it listens to those events there). It receives InventoryReserved or InventoryFailed, PaymentCompleted or PaymentFailed.
6. Order service, upon receiving both outcomes, updates order status and emits an OrderConfirmed or OrderCancelled event.
7. Notification service (consumer group "notification-service") listens for order status events (either on `orders` topic or a separate notifications topic) and sends out emails.

This flow achieves eventual consistency across services without tight coupling.

Let's illustrate the code for Order service receiving results:

```java
@KafkaListener(topics = "inventory", groupId = "order-service")
public void handleInventoryResult(InventoryResultEvent event) {
    Order order = orderRepo.findById(event.getOrderId()).orElseThrow();
    if (event instanceof InventoryReservedEvent) {
        order.setInventoryStatus("RESERVED");
    } else if (event instanceof InventoryFailedEvent) {
        order.setInventoryStatus("FAILED");
    }
    orderRepo.save(order);
    checkAndFinalizeOrder(order);
}

@KafkaListener(topics = "payments", groupId = "order-service")
public void handlePaymentResult(PaymentResultEvent event) {
    Order order = orderRepo.findById(event.getOrderId()).orElseThrow();
    if (event instanceof PaymentCompletedEvent) {
        order.setPaymentStatus("COMPLETED");
    } else if (event instanceof PaymentFailedEvent) {
        order.setPaymentStatus("FAILED");
    }
    orderRepo.save(order);
    checkAndFinalizeOrder(order);
}

private void checkAndFinalizeOrder(Order order) {
    // If both inventory and payment have been processed for this order, finalize:
    if (!order.getInventoryStatus().equals("PENDING") && !order.getPaymentStatus().equals("PENDING")) {
        if (order.getInventoryStatus().equals("RESERVED") && order.getPaymentStatus().equals("COMPLETED")) {
            order.setStatus("CONFIRMED");
            orderRepo.save(order);
            kafkaTemplate.send("orders", new OrderConfirmedEvent(order.getId(), order.getUserEmail()));
        } else {
            order.setStatus("CANCELLED");
            orderRepo.save(order);
            kafkaTemplate.send("orders", new OrderCancelledEvent(order.getId(), order.getUserEmail()));
            // Optionally, trigger compensation: if payment succeeded but inventory failed, issue refund by sending an event to Payment service, etc.
        }
    }
}
```

This logic waits for both pieces of information. We introduced `inventoryStatus` and `paymentStatus` fields in Order to track intermediate state. Initially these might be "PENDING". Once both are non-pending, we know we got responses. If both were successful, confirm order; if either failed, cancel order and possibly undo the other if needed (e.g., if payment was done but inventory failed, we might send a "Refund" event).

This is one way to coordinate. Another approach is to use a **state machine** or orchestrator, or have inventory and payment talk to each other (not preferred). Our method keeps Order service as the coordinator after initial event.

**Important Kafka Settings**:

- Set consumer `enable-auto-commit: false` (which is default in Spring if using a listener container) so that we only commit offset when processing is complete. Or use manual ack mode if needed for fine control.
- `acks=all` on producer (as seen in our config snippet) to ensure events are not lost (the producer will get acknowledgment only when the event is replicated to all in-sync replicas) ([Event-Driven Microservices with Spring Boot & Kafka - Java Code Geeks](https://www.javacodegeeks.com/2024/10/event-driven-microservices-with-spring-boot-kafka.html#:~:text=,for%20stronger%20durability%20guarantees)).
- Proper `group.id` per service ensures each service gets its own copy of events. Payment and Inventory use different group IDs when listening to the same `orders` topic so they each get the message. Order service uses its own group for `inventory` and `payments` topics.
- Use separate topics for different event types to avoid confusion and to allow different retention or partitioning policies. For example, `orders` events might be retained short term since once processed, we might not need them much, whereas `payments` events could be retained longer for audit.

### 4.2 Handling Event Streaming for Order Processing and Real-Time Updates

We have essentially handled order processing through events in the above flow. Let's summarize it as a cohesive event-driven process:

- **Order Processing Pipeline**: The moment an order is placed, it becomes an event in a pipeline. This pipeline asynchronously triggers inventory and payment actions. This decoupling allows those actions to happen in parallel and potentially faster. It also means the front-end (or client) doesn't have to wait for these to complete; the client could receive a quick response that order is being processed. This improves user experience (they get a response faster and maybe see "Order is processing" status).
- **Real-Time Updates**: How do we inform the user of the outcome (success or failure of their order)? We could continually poll the order status via an API, but a nicer approach is to push updates to the front-end in real-time. This can be done by:
  - WebSocket or Server-Sent Events: The Notification service (or Order service) could send a WebSocket message to the user’s browser when the order is confirmed or failed.
  - Or simpler, when the user checks their orders next time, it will show the updated status. But real-time is a better UX.

For example, if using WebSockets, we might have a WebSocket service subscribed to the same order events to notify the client.

**Kafka Streams for Real-Time Aggregation**: Aside from processing individual events, Kafka enables building real-time analytics or computed views via Kafka Streams. We cover that next.

### 4.3 Implementing Kafka Streams for Analytics

**Kafka Streams** is a powerful API for transforming and aggregating data streams directly within your Java application. Instead of consuming events one-by-one in a traditional consumer, Streams provides a high-level DSL to define processing topologies (streams, maps, joins, aggregations, windows, etc.) on Kafka topics. It runs in your app as a library – you can even have a dedicated microservice for analytics that uses Kafka Streams.

**Use Case**: Let's say we want to maintain real-time analytics like:

- Total number of orders per day.
- Revenue per hour.
- Top selling products in the last 24 hours.
- Or generate data to feed a recommendation engine (like counting views or purchases of products).

We can do this with Kafka Streams without storing all events in our own DB for analysis, leveraging Kafka topics as the source of truth.

**Example**: Count orders by status or per time window:
We have an `orders` topic (with events like OrderConfirmed, OrderCancelled). We can use a KStream on the `orders` topic, filter only confirmed events, then aggregate.

Set up a Streams builder in a separate Spring Boot application (or even within Order service if we want, but better separate):

```java
@Configuration
public class AnalyticsStream {
    @Bean
    public KStream<String, OrderStatusEvent> kstream(StreamsBuilder builder) {
        KStream<String, OrderStatusEvent> orderStream = builder.stream("orders",
            Consumed.with(Serdes.String(), new JsonSerde<>(OrderStatusEvent.class))
        );
        // Filter confirmed orders
        KStream<String, OrderStatusEvent> confirmedStream = orderStream
            .filter((key, event) -> "CONFIRMED".equals(event.getStatus()));
        // Map to day key for counting per day
        KTable<String, Long> ordersPerDay = confirmedStream
            .map((key, event) -> {
                String day = event.getTimestamp().toLocalDate().toString();
                return KeyValue.pair(day, 1);
            })
            .groupByKey(Grouped.with(Serdes.String(), Serdes.Integer()))
            .count(Materialized.as("orders-per-day-store"));
        ordersPerDay.toStream().to("orders-per-day", Produced.with(Serdes.String(), Serdes.Long()));
        return orderStream;
    }
}
```

This is a conceptual example:

- We consume from "orders" topic as a stream of OrderStatusEvent.
- We filter only confirmed ones.
- We transform each into a key of the day string and value 1, then group by that key and count.
- The result is stored in a state store (for fault-tolerance and windowing) and also written to an output topic "orders-per-day".

Now, any consumer (or a monitoring dashboard) can read "orders-per-day" topic to get an updated count of orders each day.

You can do more complex things like 1-hour tumbling windows for hourly sales:

```java
TimeWindows window = TimeWindows.ofSizeWithNoGrace(Duration.ofHours(1));
KTable<Windowed<String>, Double> revenuePerHour = confirmedStream
    .groupBy((key, evt) -> "revenue", Grouped.with(Serdes.String(), new JsonSerde<>(OrderStatusEvent.class)))
    .windowedBy(window)
    .aggregate(
       () -> 0.0,
       (aggKey, event, aggValue) -> aggValue + event.getOrderTotal(),
       Materialized.with(Serdes.String(), Serdes.Double())
    );
```

This would accumulate revenue in each one-hour window. The output key would be a Windowed<String> containing the time window and the "revenue" key, and value the double sum.

**Kafka Streams Benefits**: It allows stateful processing (maintaining aggregates) with exactly-once processing guarantees when used with Kafka's transactional semantics. In our example above, state is stored in a local RocksDB (and changelog in a Kafka internal topic) so that counts are fault-tolerant. This is perfect for real-time dashboards or feeding data to other systems (like updating an ElasticSearch index of statistics, etc.).

**Integration**: Running Kafka Streams in Spring Boot can be done by defining the KStream bean as shown. Spring Boot (with spring-kafka) will start the Streams application on startup. Ensure to configure:

```yaml
spring.kafka.streams.application-id: analytics-service
spring.kafka.streams.bootstrap-servers: localhost:9092
```

Each Kafka Streams app needs a unique `application-id` which acts like a consumer group ID for the streams processors and also namespaces the state stores.

For advanced analytics or recommendation engines, one might also use frameworks like Apache Flink or Spark Streaming, but Kafka Streams is lightweight and fits well for many use cases within the Kafka ecosystem.

To summarize, we've set up:

- Core Kafka producers/consumers for business logic.
- Optionally, Kafka Streams for analytical processing of those same event streams in real-time.

Next, we focus on managing the database efficiently.

## 5. Database Management with MySQL

MySQL backs each microservice’s data storage. Proper database design and usage is crucial for scalability and consistency. In this section, we'll discuss designing scalable schemas, using JPA/Hibernate for ORM, query optimization with indexes, and handling transactions and concurrency.

### 5.1 Designing Scalable Schemas

We already drafted the schema design in section 2.3. Now we emphasize **scalability considerations** in schema design:

- **Normalization vs Denormalization**: Highly normalized schemas (3NF) avoid data duplication and anomalies, but in microservices, some denormalization is acceptable to reduce cross-service calls. For instance, storing `productName` and `price` in the Order Items is duplication of data from Product service, but it allows the Order service to show order history without querying Product service for historical data (especially if the product name or price changes later, the order should reflect what the user saw at purchase time).
- **Bounded Contexts**: Each schema is small (few tables) focusing on one context. This keeps queries simpler and transactions short, aiding performance.
- **Primary Keys**: Use auto-increment IDs (MySQL's BIGINT UNSIGNED for large range, or use UUID). Auto-increment is simpler for joining within service and for foreign keys. If using UUID, ensure to use binary(16) storage to save space if needed.
- **Character Set**: Use UTF8MB4 for internationalization (product names, user names might have emojis or non-Latin characters).
- **Large Text and Blobs**: If product descriptions are large text, consider storing them as TEXT column. Images should not be in the DB (store in an object storage or CDN, and just save URLs or references in the DB).
- **Multi-tenancy**: If this application is multi-tenant (support multiple stores), you might include a tenant/shop ID column in tables and possibly partition on that. That's advanced use, not addressed here unless needed.

**Growth Planning**:

- The Product table could grow large if many products. Ensure to index important columns (like `name` for search if needed, or `category_id` for filtering).
- The Orders table will continuously grow. Partitioning by date (by year or month) might be considered if it becomes huge over years, but initially an index on `user_id` and `order_date` might suffice.
- Clean up or archive data that is not needed live. For example, if you have a lot of expired sessions or carts, you can purge them.

### 5.2 Using JPA and Hibernate for ORM

Using Spring Data JPA with Hibernate (the default JPA implementation) provides many benefits:

- **Productivity**: Developers can work with Java objects and have them automatically persisted, without writing SQL for every operation.
- **Abstraction**: It abstracts database-specific details. For example, you can switch from MySQL to PostgreSQL with minimal code changes since JPA covers the differences in dialects (though careful with native queries).
- **Prevents SQL Injection**: By using parameter binding and JPA's generated queries or JPQL with parameters, you avoid constructing SQL with string concatenation, thus avoiding SQL injection vulnerabilities ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=Prevent%20Injection%20Attacks%3A%20Use%20parameterized,XSS%20and%20other%20injection%20vulnerabilities)).
- **Transaction Management**: Spring handles transactions for JPA easily via @Transactional. Either at the service methods or repository methods (by default, CrudRepository methods run in transactions).
- **Lazy Loading**: Relationships like `Order -> OrderItems` can be loaded on-demand. But be cautious: lazy loading outside of a transaction (like in a web controller after session closed) can cause exceptions. Fetch what you need within the service.

**Best Practices with JPA**:

- Keep the persistence context (session) short-lived (commonly per request in Spring). Don't hold on to entities outside transactions.
- Use **DTOs or Projections** for read operations when you don’t need the entire entity graph to avoid loading unnecessary data.
- For batch inserts/updates, consider JPA’s batching or use JDBC directly if extremely performance sensitive (JPA has overhead per entity).
- Manage the N+1 query problem: If you see multiple SQL selects for related data, use `@EntityGraph` or join fetch in JPQL to fetch associations in one query when appropriate.

**Example**: Query all orders with their items:

```java
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.userEmail = :userEmail")
List<Order> findOrdersWithItemsByUser(@Param("userEmail") String userEmail);
```

This JPQL ensures we fetch Order and OrderItems in one go, rather than one query for orders and N queries for items.

**Custom Queries**: Spring Data allows native SQL queries via `@Query(nativeQuery=true)` if needed (e.g., for a complex report). But try JPQL or repository methods first.

**Caching with JPA**: JPA has a first-level cache (the persistence context) for the scope of a transaction (so within one service method call, if you `findById` the same entity twice, second time it’s cached in memory). There's also a second-level cache (shared across sessions, e.g., using Ehcache or Hazelcast). Enabling second-level cache can improve performance for read-mostly data (like products), but in a microservices environment, it might be better to handle caching at the service layer or use Redis as done above for products, to ensure consistency across instances.

**Migration Management**: While not asked specifically, mention that using a tool like Flyway or Liquibase for managing database schema migrations is advisable in a multi-environment scenario (development, staging, production). For development, we used `ddl-auto: update` to auto-create tables, but in production, you'd apply SQL migrations in a controlled way.

### 5.3 Query Optimization and Indexing Strategies

Efficient database queries are vital for performance. Key strategies:

- **Indexes**: The primary tool for speeding up queries. MySQL uses indexes to quickly lookup rows by key instead of scanning full tables. _The best way to improve SELECT performance is to create indexes on columns used in query conditions (WHERE, JOIN, ORDER BY)_ ([MySQL :: MySQL 8.4 Reference Manual :: 10.3 Optimization and Indexes](https://dev.mysql.com/doc/en/optimization-indexes.html#:~:text=The%20best%20way%20to%20improve,data%20types%20can%20be%20indexed)). For example:
  - Index `product.name` if you frequently do `WHERE name LIKE '%foo%'` (though MySQL’s index helps only with prefix for LIKE unless using full-text).
  - Index `order.user_email` if we query orders by user.
  - Composite index if a combination of columns is often used (e.g., (user_email, order_date) to get recent orders of a user).
  - Index foreign key columns (even if not actual FK across microservices, e.g., index `order_items.product_id` to speed up joining product info in queries, etc.).
- **Avoid unnecessary indexes**: Every index slows down writes (inserts/updates) because it must be maintained. So identify the minimal set of indexes that cover your common query patterns ([MySQL :: MySQL 8.4 Reference Manual :: 10.3 Optimization and Indexes](https://dev.mysql.com/doc/en/optimization-indexes.html#:~:text=other%20column%20values%20for%20those,data%20types%20can%20be%20indexed)).
- **Query Analysis**: Use `EXPLAIN` on your SQL queries to see if indexes are being used. If you find table scans on large tables, that's a red flag. Ensure conditions use indexed columns.
  - If you see "Using filesort" or "Using temporary" in EXPLAIN for large data sets, consider adding an index to cover the ORDER BY or the columns in the SELECT to make it a covering index.
- **Pagination**: Use `LIMIT/OFFSET` for paging results (e.g., products list) and have an index on the ordering column to avoid full scans. For large offsets, an alternative is to remember the last seen key (pagination by key, which is more efficient).
- **Joins**: Within a service, design your queries to minimize joins on very large tables. For example, joining orders and order_items is fine (moderate size each), but avoid joining orders with products across microservice boundary (instead, do two separate queries or call the other service).
- **Full Text Search**: MySQL supports full-text indexes on TEXT/VARCHAR columns to enable text search (with MATCH ... AGAINST). If search is a major feature, consider enabling that on product.name/description. Alternatively, integrate ElasticSearch for advanced search features if needed (would be a separate service that syncs data via events).
- **Prepared Statements**: Use JPA or JDBC prepared statements so that MySQL can cache execution plans. Spring JDBC and JPA do this under the hood for you with parameter binding.
- **Connection Pooling**: Rely on HikariCP (Spring Boot's default pool) to reuse connections. Ensure the pool is sized appropriately (not too small to throttle concurrency, not too large to overwhelm DB; maybe on the order of 10-20 per service depending on load).
- **Read/Write Splitting**: If you implement replication (one primary, multiple replicas), you can direct read queries to replicas. Spring doesn't do this out-of-the-box, but you can configure two data sources or use a load-balanced JDBC URL or a proxy like ProxySQL. We discuss scaling in 7.5.

In summary, be mindful of each SQL query's cost:

- Run load tests or at least explain plans for critical queries.
- Add indexes where needed, and verify improvement.
- Monitor slow query logs in MySQL (enable `slow_query_log` to log queries taking > X seconds).

### 5.4 Handling Transactions and Concurrency

In multi-user, distributed systems, concurrency control and transaction management ensure data integrity:

- **Transactional Annotation**: Use `@Transactional` on service methods that modify data. This ensures that either all operations in that method succeed or all are rolled back if any failure occurs. For example, the OrderService `createOrder` method earlier is transactional so that an order and all its items are either fully saved or none if something goes wrong mid-way.
- **Isolation Levels**: MySQL's default (InnoDB) isolation level is REPEATABLE READ, which works fine for most cases. Under high concurrency, you might encounter deadlocks – you can catch `DeadlockLoserDataAccessException` in Spring and retry the transaction if needed. For certain operations, you might use a lower isolation (READ COMMITTED) to reduce locking contention, or higher (SERIALIZABLE) if you need strict consistency (rare in microservices, since cross-service consistency is eventually achieved via saga).
- **Optimistic Locking**: In JPA, you can use @Version field on an entity to enable optimistic locking. This is useful to prevent lost updates in concurrent environment. For example, if two processes try to update the same Inventory row at once, with a @Version column, one will succeed, the other will get an OptimisticLockException which you can handle (maybe retry). This is a good pattern for something like inventory updates if they might occur from different sources (though in our design, all inventory changes funnel through the Inventory service single-threaded via Kafka, so it might not be needed).
- **Pessimistic Locking**: JPA supports `lock()` or using `@Lock(LockModeType.PESSIMISTIC_WRITE)` on queries to force DB row locks. For instance, if implementing a straightforward checkout without Kafka, one might do:
  ```java
  Inventory inv = inventoryRepo.findByProductId(productId, LockModeType.PESSIMISTIC_WRITE);
  // then check and update inv.quantity
  ```
  This ensures no one else can read/modify that inventory row until the transaction commits. Pessimistic locks can reduce concurrency (others will wait), but ensure safety. Use them only when necessary (e.g., transferring balance between accounts pattern).
- **Distributed Transactions**: We avoid 2-phase commit (XA transactions) across microservices due to complexity and tight coupling. Instead, as discussed, we rely on Saga and Kafka for eventual consistency. This means each service transaction is local and can use regular ACID, and cross-service consistency is managed at app level. Saga ensures that if one part fails, other changes can be compensated. For example, if Inventory failed after Payment succeeded, we might need to issue a refund (compensating transaction in Payment service). This compensation is triggered by the Order service saga logic (it would listen for failure and send a "CancelPayment" event to Payment service perhaps).
- **Concurrency in MySQL**: InnoDB handles concurrent writes with locking and MVCC for reads. If you design so that contention is minimized (e.g., not every transaction updates the same row), you'll avoid most deadlocks. For example, orders typically each affect different rows (one order row and some inventory rows for those products). It's different from, say, an accounting system where many transactions update the same balance row. We are relatively safe. If a deadlock occurs (MySQL will abort one transaction), Spring will throw an exception which you can catch and retry if the operation is idempotent or can be retried.

**Example**: The inventory deduction approach we wrote is effectively doing all updates in one transaction. If two OrderPlacedEvents with the same product come concurrently, one might deadlock or one might wait. Because we subtract stock for each item in a loop and then commit, another transaction might be trying to do the same. InnoDB might detect a deadlock if the two orders have overlapping products in different order. To handle, either process events sequentially per product (partition by product id, advanced), or catch exceptions and handle. A simpler approach is to process one order at a time (which is what a single-threaded Kafka consumer does by default in each partition). If we ensure all events for a given product go to the same partition, then the Inventory service effectively handles them serially, avoiding conflicts. This is something to consider when designing the Kafka topic key.

**Conclusion**: Use Spring's transaction support for maintaining data integrity within each service, and use saga patterns for maintaining consistency across services. Ensure the database is tuned with correct indexes to handle concurrent access efficiently.

Next, we'll address security concerns and best practices beyond authentication.

## 6. Security and Best Practices

Security is paramount in an e-commerce application as it deals with sensitive customer data and financial transactions. We have set up authentication and authorization; now we cover additional security measures: protecting against common vulnerabilities, enforcing best practices, rate limiting, and monitoring for security issues.

### 6.1 Implementing Authentication and Authorization

We covered the implementation of authentication (with JWT tokens and Spring Security) in section 3.2. To recap and add context:

- Use **strong encryption** for passwords (BCrypt hashing).
- Implement **JWT expiration** (tokens should expire after a reasonable time, e.g., 15 minutes or 1 hour, and perhaps use refresh tokens for longer sessions).
- Secure the JWT signing secret or keys. If using symmetric signing (HS256), keep the secret very safe (e.g., in an environment variable or secret manager, not in code). If using asymmetric (RS256), protect the private key and only distribute the public key for resource servers.
- The microservices (Order, Product, etc.) should validate JWTs on each request. We did this by enabling Spring Security's resource server support. That means each request's Authorization header is checked. If valid, `SecurityContext` is populated with user details (username, roles).
- Use roles to protect endpoints (authorization). For example, ensure only admins can create or update products:
  ```java
  @PreAuthorize("hasRole('ADMIN')")
  @PostMapping("/products") public Product createProduct(...) { ... }
  ```
  Similarly, an endpoint like `GET /orders/{id}` should ensure the authenticated user matches the order's user or has admin role. You can enforce that with `@PreAuthorize("#order.userEmail == authentication.name or hasRole('ADMIN')")` on a method, or manually check inside.
- Use **TLS/HTTPS** everywhere. Even though not a code change, it's a security must-have. All client-server communication should be over HTTPS to encrypt the data in transit (including JWTs, user info, etc.). Typically, if deploying on Kubernetes or a cloud, you'd use an ingress or load balancer with TLS certificates.

**OAuth2 Considerations**: If you integrate third-party login or plan to expose APIs to third-party developers:

- You might use OAuth2 authorization code flow for user login via Google/Facebook etc., or client credentials flow for server-to-server.
- Spring Security can be configured for OAuth2 login (the Spring Boot OAuth2 starter can help connect to external providers easily).
- Issue and scope refresh tokens carefully.

### 6.2 Preventing Common Security Vulnerabilities

Here we address specific common vulnerabilities (many listed in OWASP Top 10) and how to mitigate them:

- **SQL Injection**: Since we use JPA with prepared statements under the hood, and even if we use JDBC, we use parameterized queries, we avoid injection. The key is to **never construct SQL by concatenating user input**. If you do need dynamic queries, use JPA Criteria API or Spring Data Specifications. By relying on JPA and ORM, we effectively protect ourselves from SQL injection because the framework will handle escaping/param binding ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=Prevent%20Injection%20Attacks%3A%20Use%20parameterized,XSS%20and%20other%20injection%20vulnerabilities)).
- **Cross-Site Scripting (XSS)**: XSS is an issue on the front-end primarily (injection of malicious scripts in web pages). If our app has a web UI, any data from the server (like product names, user-generated content in reviews, etc.) that is rendered in a browser should be properly escaped/encoded. On the server side, if this were a Thymeleaf or JSP app, we would ensure to HTML-encode outputs. Since our focus is on the backend API, we need to ensure that we don't store malicious scripts blindly. Best practice is to **validate and sanitize input** on the server. For example, if product descriptions allow HTML, consider using an allowlist of tags or sanitize with a library. Often, the front-end will handle display encoding. But we can still use frameworks to strip out script tags from inputs to be safe ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=Prevent%20Injection%20Attacks%3A%20Use%20parameterized,XSS%20and%20other%20injection%20vulnerabilities)).

  - In Spring, one can use Spring Security's `HtmlUtils.htmlEscape()` if needed when rendering data in views ([How to address top 5 security issues in Java Spring Boot | ‍ Code Arsenal](https://codearsenalcommunity.github.io/top-5-security-issue-java-springboot/#:~:text=Output%20encoding%3A%20Properly%20encode%20user,libraries%20provided%20by%20the%20framework)).
  - For data that goes to the front-end, ensure the front-end uses frameworks that auto-escape or use safe methods to insert into DOM.

- **Cross-Site Request Forgery (CSRF)**: CSRF is a vulnerability where an attacker tricks a logged-in user's browser to make a request to your server (like changing password) without the user intending it. Spring Security has built-in CSRF protection for web apps (it expects a CSRF token to be sent with state-changing requests). In our case, since we use stateless JWT and likely not serving a traditional server-side session, CSRF is less of a concern because the browser will only send our JWT if we explicitly set it in a header (not automatically like a cookie). If we were using session cookies for auth, we must ensure CSRF tokens on any forms or non-idempotent requests.

  - By default, when using `http.csrf().disable()` in a stateless API, we turned it off. That's acceptable for pure token-based APIs. If any part of our app serves pages or forms (like maybe an admin UI served from Order service), we should enable CSRF for those and include tokens.
  - Summary: **If using cookies for auth, always use CSRF tokens** ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=privileges)). For JWT, ensure CORS is configured properly so only allowed domains can use the API.

- **Injections in general**: Besides SQL injection, consider OS command injection (not common unless we take input that goes to exec commands, which we don't here), or NoSQL injection if using NoSQL (not applicable here).
- **Deserialization vulnerabilities**: Spring Boot with JSON is generally safe if using Jackson with known types. If you accept serialized objects or untrusted JSON, be mindful of polymorphic deserialization. We set `spring.kafka.consumer.properties.spring.json.trusted.packages` earlier to "\*" which is a slight risk if someone managed to push a malicious class in the classpath. In web endpoints, Jackson by default does not allow unknown types to instantiate, so we are okay. Just keep libraries updated to avoid known exploits.

- **Sensitive Data Exposure**:
  - Do not log sensitive info like passwords or full credit card numbers. Mask them if needed (e.g., show only last 4 digits).
  - Use HTTPS (already mentioned) to encrypt in transit.
  - If storing any very sensitive info (like payment tokens, etc.), consider extra encryption at rest or in the database.
  - Back up data securely, and scrub data in non-production environments (no real customer credit card numbers in dev/test).
- **Access Control**:

  - We must ensure that one user cannot access another's data. This involves checking IDs in requests against the authenticated user's ID. For example, if `/orders/{id}` is called, the Order service should verify that the order belongs to `authentication.name` (unless the role is ADMIN). We can enforce this either in the query (`SELECT ... where id=:id and user_email=:email`) to automatically return nothing if not matching, or via code checks.
  - Similarly, a user should not be able to add items to someone else's cart, etc. By scoping everything to the `auth.getName()` as we've done, we're in good shape.
  - In microservice internal communications (Kafka events), one service might trust data from another. For instance, the OrderPlacedEvent includes userEmail. The Inventory service trusts that. Could someone malicious send a fake OrderPlacedEvent? If Kafka is secure internally, only our services produce to that topic. We may consider enabling client authentication on Kafka or network-level security to prevent rogue producers/consumers.

- **Rate Limiting**: To prevent abuse (like someone scripting to hit our login endpoint or search endpoint aggressively, possibly causing denial of service or brute forcing), implement rate limiting. **Rate limiting restricts the number of requests a client can make in a time window** ([Rate Limiting a Spring API Using Bucket4j - Baeldung](https://www.baeldung.com/spring-bucket4j#:~:text=Rate%20limiting%20is%20a%20strategy,within%20a%20certain%20time%20frame)). We can implement at the API gateway level or in each service:

  - Use a library like Bucket4j or Resilience4j RateLimiter. For example, Bucket4j can be used to limit by IP or user ID. It could be applied as a filter in Spring Boot that counts requests.
  - Alternatively, if deploying behind a cloud load balancer or API Gateway (like Kong, Apigee, etc.), those can enforce limits per API key or IP.
  - Given our advanced developer audience, they might be interested in a token bucket algorithm approach: e.g., allow 100 requests per minute per user. We could store counters in Redis and decrement for each request.
  - At minimum, protect the login and expensive endpoints. For login, also use account lockouts or exponential backoff after failed attempts to slow down brute force on passwords.

- **Monitoring and Alerts**: Use monitoring (which we'll do in Section 7 and 9) to detect unusual activity. E.g., use Grafana to set up an alert if traffic spikes abnormally (could indicate a DoS attempt). Also track error rates (spike in 401s might mean someone is trying lots of bad tokens, etc.).

By following these practices, we mitigate most common vulnerabilities:

- We **use prepared statements/ORM** for SQL safety ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=Prevent%20Injection%20Attacks%3A%20Use%20parameterized,XSS%20and%20other%20injection%20vulnerabilities)).
- We **sanitize input and encode output** to handle XSS and other injections ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=Prevent%20Injection%20Attacks%3A%20Use%20parameterized,XSS%20and%20other%20injection%20vulnerabilities)).
- We **use CSRF tokens** if applicable to prevent cross-site attacks ([Spring Boot Security](https://www.puredome.com/blog/spring-boot-security#:~:text=privileges)).
- We **limit access** with robust auth checks.
- We **encrypt data in transit** (HTTPS) and secure data at rest.
- We **audit and log**: Keep an audit trail of important actions (e.g., admin accesses, payment transactions). Spring Security can log authentication events, and we can log custom events like "User X placed Order Y".

### 6.3 API Rate Limiting and Monitoring

Expanding on rate limiting and adding monitoring:

- **Simple Rate Limiting Implementation**: Suppose we want to limit each IP to 10 requests per second for the Product search endpoint. We could maintain an in-memory counter with timestamps (but that resets if app restarts or with multiple instances, not global). For global limit, use Redis or an external store:
  - Use Redis INCR and EXPIRE commands to count hits. For example, have a key like `rate:search:IPADDRESS` that expires in 1 second. On each request, do INCR and if value > 10, reject the request with HTTP 429 Too Many Requests.
  - Libraries like Bucket4j Spring Boot Starter can integrate with Redis to do this distributed rate limiting.
- **User-based Rate Limit**: Instead of IP, use user ID from JWT to rate limit per user (this prevents a single user from overwhelming, but if one user uses many IPs or in a cluster scenario).
- **Leaky Bucket vs Token Bucket**: Most implementations (like Bucket4j) allow a refill rate and capacity, smoothing bursts. For instance, allow bursts of 20 requests but refill 1 token per second, etc. Fine-tuning this depends on expected usage patterns.

**Apply Rate Limits Strategically**:

- Login and sensitive modifications (to prevent brute force or abuse).
- Search endpoints (to prevent scraping of data via rapid queries).
- Maybe not on retrieving a single product by id (unless you suspect scraping by iterating IDs, but having auth somewhat prevents mass anonymous scraping).

We also mention **monitoring**:

- Use Spring Boot Actuator metrics to monitor rate limiting events, or simply log when a rate limit is exceeded for audit.
- Also monitor security events. Spring Security can provide some metrics, but often it's logs that are inspected (e.g., track repeated failed logins for a user to possibly blacklist an IP).

**API Monitoring** overlaps with performance monitoring:

- We will incorporate metrics like request count, response time, etc., in the next section with Prometheus.
- For security, also monitor 4xx/5xx rates (spikes in 401/403 could indicate attacks).

**Dependency Security**:

- Keep libraries up to date to get latest security fixes (Spring, Kafka client, etc.).
- Use tools (like OWASP Dependency Check or Snyk) to scan for known vulnerabilities in dependencies.

By applying these best practices, we create a robust security posture for the application.

Next, we'll focus on deployment strategies and scaling considerations.

## 7. Deployment and Scaling

Building a great application is half the battle; deploying it reliably and scaling it to handle real-world traffic is the other half. In this section, we’ll discuss containerizing the microservices with Docker, deploying them using Kubernetes, setting up CI/CD pipelines, monitoring with Prometheus/Grafana, and strategies for scaling the Kafka brokers and MySQL database for high availability.

### 7.1 Containerization with Docker

**Why Docker?** Docker allows us to package each microservice with all its dependencies into a lightweight container. This ensures consistency across environments (development, testing, production). Each service (Spring Boot app) can run in its own container, and we can run many containers on a host or cluster.

**Creating a Dockerfile**: Each microservice project gets a Dockerfile. For a Spring Boot fat jar, a simple Dockerfile might be:

```
# Use a base image with Java runtime
FROM openjdk:17-jdk-slim
# Set working directory
WORKDIR /app
# Copy the jar (assuming jar name is app.jar)
COPY target/*.jar app.jar
# Expose the port (not strictly needed for Kubernetes but good documentation)
EXPOSE 8080
# Run the jar
ENTRYPOINT ["java","-jar","app.jar"]
```

This assumes you've built the jar via Maven/Gradle. For efficiency, you could use a multi-stage build:

```
# Stage 1: build
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /build
COPY pom.xml ./
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: runtime
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /build/target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
```

This way you don't include Maven and source code in the final image, only the built jar. This reduces image size.

**Building the Image**: Run `docker build -t myorg/catalog-service:1.0 .` in the service directory (with appropriate name). Do this for each service, tagging with a version.

**Docker Compose for Local Dev**: To run multiple services plus Kafka and MySQL locally, a docker-compose.yml can define all:

```yaml
version: '3'
services:
  zookeeper:
    image: bitnami/zookeeper:latest
    ports: ["2181:2181"]
  kafka:
    image: bitnami/kafka:latest
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
    depends_on: [zookeeper]
    ports: ["9092:9092"]
  mysql:
    image: mysql:8.1
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=catalog_db
      - MYSQL_USER=catalog_user
      - MYSQL_PASSWORD=catalog_pass
    ports: ["3306:3306"]
  catalog-service:
    image: myorg/catalog-service:1.0
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/catalog_db
      - SPRING_DATASOURCE_USERNAME=catalog_user
      - SPRING_DATASOURCE_PASSWORD=catalog_pass
    depends_on: [mysql, kafka]
    ports: ["8081:8080"]
  order-service:
    image: myorg/order-service:1.0
    environment:
      - ... (similar DB config for its DB)
    depends_on: [mysql, kafka]
    ports: ["8082:8080"]
  ...
```

This is illustrative. You might have separate MySQL for each service or one with multiple schemas; typically each has its own instance to avoid interference (in production, separate or on same server depends on scaling needs).

Using compose, you can spin up the entire stack with one command, which is great for end-to-end testing locally.

### 7.2 Deploying Microservices with Kubernetes

Kubernetes (K8s) has become the standard for deploying containerized applications at scale. It handles container scheduling, self-healing (restarting failed containers), scaling, networking, and more.

**Setting up Kubernetes**:

- In a cloud environment, you might use managed services (EKS, AKS, GKE, etc.) or on-prem k8s.
- You define desired state in YAML files (Deployment, Service, ConfigMap, etc.) or use Helm charts for templating.

**Deployment for each Service**: A Kubernetes Deployment ensures a certain number of pod replicas for a service. For example, a deployment for Catalog service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalog-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: catalog
  template:
    metadata:
      labels:
        app: catalog
    spec:
      containers:
        - name: catalog
          image: myorg/catalog-service:1.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              value: jdbc:mysql://catalog-mysql:3306/catalog_db
            - name: SPRING_DATASOURCE_USERNAME
              value: catalog_user
            - name: SPRING_DATASOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: catalog-db-secret
                  key: password
```

We would also define a Service (Kubernetes Service) for the Catalog deployment to allow it to be discovered by other services or the gateway. For internal communication, you might use K8s DNS: e.g., Order service can reach Catalog service at `http://catalog:8080` if we set the service name to "catalog". Or more commonly, you use an API Gateway or ingress for inter-service or external traffic.

**Database on K8s**: Running MySQL on k8s is possible (as a StatefulSet), but often one uses a managed database or a stable environment for the database. If on K8s, ensure persistent volumes for data. For dev/test, it's fine; for prod, maybe use a cloud DB service.

**Kafka on K8s**: Kafka can run on K8s (with StatefulSets and headless services, plus persistence). There are operators like Strimzi to simplify that. Alternatively, use a managed Kafka service (Confluent Cloud, Amazon MSK, etc.) or run it on VMs. Running Kafka on k8s needs careful configuration for networking (advertised listeners, etc). There's also KRaft mode (Kafka without ZooKeeper, in newer versions) that can simplify deployment.

Given our focus is application, we assume Kafka is available at some address; deploying it is another project in itself.

**Service Discovery & API Gateway**:

- Within k8s, each service can talk to others via service DNS names (assuming network policies allow).
- For external access (like clients calling our APIs), we set up an **Ingress** or an API Gateway (like Zuul, Spring Cloud Gateway, or a cloud LB).
- An example Ingress might route `api.mysite.com/catalog` to catalog service, `api.mysite.com/orders` to order service, etc. Or if using a gateway, the gateway pod receives all traffic and forwards internally.
- If we want GraphQL as a unified API, a BFF service might aggregate calls or subscribe to Kafka for asynchronous parts.

**Scaling**:

- To scale a service, increase its Deployment replicas (manually or via Horizontal Pod Autoscaler which can scale based on CPU/memory or custom metrics).
- For instance, if product browsing is heavy, scale Catalog service to more pods.
- K8s can schedule these across nodes to balance load.
- Ensure statelessness: our services are mostly stateless (they rely on DB and Kafka, but not storing session in memory - JWT means no session storage needed). This makes scaling out easy.
- Kafka consumers: if we scale, say, Inventory service to 2 pods, and Kafka topic has e.g. 3 partitions, the 2 pods will share partitions (one might get 2 partitions, the other 1). That parallelizes event processing up to the partition count. If you need more parallelism, ensure enough partitions, or further scale to 3 pods for 3 partitions, etc.
- MySQL scaling we cover in 7.5, but typically you scale reads by adding replicas.

**Kubernetes benefits**:

- Self-healing: if a container goes down, k8s restarts it.
- Rollouts: Deployments allow rolling updates (zero downtime if multiple pods: it will slowly replace pods with new version).
- Rollback: If something goes wrong, you can rollback to previous Deployment revision.
- ConfigMaps/Secrets: externalize config like DB credentials, Kafka URLs, etc. (We used env in YAML, but ideally use ConfigMap and Secret resources).
- Observability: K8s doesn't do monitoring itself but makes it easy to integrate with Prometheus, etc. via sidecar or exporters.

### 7.3 Implementing CI/CD Pipelines for Automated Deployments

Continuous Integration (CI) and Continuous Deployment (CD) pipelines automate building, testing, and deploying your application. This ensures quick, reliable releases.

**CI Pipeline**:

- When code is pushed to a repository (e.g., GitHub/GitLab), a CI workflow triggers.
- Steps might include: compile, run unit tests, run integration tests (maybe with testcontainers to spin up Kafka/MySQL), run static code analysis or security scans.
- If tests pass, build the Docker images for each service.
- Possibly push the images to a registry (DockerHub, ECR, etc.).

**CD Pipeline**:

- After a successful build (maybe on merge to main branch or a tag), the pipeline can deploy the new version to a staging or production environment.
- Using tools like Jenkins, GitLab CI, GitHub Actions, or specialized tools like Argo CD or Flux for Kubernetes GitOps:
  - One approach: Jenkins pipeline uses kubectl/helm to apply new YAML or Helm charts to the cluster.
  - Another: use GitOps (a Git repo contains environment manifests; when CI pushes updated manifests with new image tags, Argo CD automatically syncs the cluster to that state).
- Ensure deployment is done in a rolling fashion. Kubernetes by default does rolling updates for Deployments (can configure max surge, max unavailable).
- Run smoke tests post-deployment (for example, ping the health endpoint of each service, run a quick end-to-end test on staging).

**Pipeline Example** (simplified in Jenkinsfile format):

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh './mvnw clean package'
      }
    }
    stage('Test') {
      steps {
        sh './mvnw test'
      }
    }
    stage('Build Docker Images') {
      steps {
        sh 'docker build -t myorg/catalog-service:$BUILD_NUMBER catalog-service/'
        sh 'docker build -t myorg/order-service:$BUILD_NUMBER order-service/'
      }
    }
    stage('Push Images') {
      steps {
        withCredentials([usernamePassword(...)]){
          sh 'docker login ...'
        }
        sh 'docker push myorg/catalog-service:$BUILD_NUMBER'
        sh 'docker push myorg/order-service:$BUILD_NUMBER'
      }
    }
    stage('Deploy to K8s') {
      steps {
        sh 'kubectl set image deployment/catalog-deployment catalog=myorg/catalog-service:$BUILD_NUMBER'
        sh 'kubectl set image deployment/order-deployment order=myorg/order-service:$BUILD_NUMBER'
      }
    }
  }
}
```

This is a basic idea: after building and pushing, we update the Kubernetes deployments to use the new image tag. Kubernetes then does the rolling update.

For more sophisticated setups:

- Use **Helm** charts to templatize Kubernetes YAML, and use `helm upgrade` in CD to deploy new versions (which can also manage versioned rollbacks).
- Use **Argo CD**: treat your deployment configs as code (GitOps). So you update a values file with new image tag, commit to a repo, Argo detects change and deploys.
- Ensure secrets (like passwords) are handled securely in CI (use credential stores, not plain text in pipeline scripts).

**Continuous Testing**:

- Possibly include performance tests in pipeline (maybe nightly) to catch regressions.
- Also security tests (like dependency scans, container image scans for vulnerabilities).

**Blue/Green or Canary deployments**:

- For zero downtime and verifying new version, one might deploy a new set of pods (green) while old (blue) still running, then switch traffic. In Kubernetes, this can be done by having two deployments and switching a service label selector, or simpler: scale up new version via rolling update gradually.
- Canary: deploy new version to a small subset (say 10% pods) and see if metrics are good, then increase to 100%. Service mesh (Istio) or Kubernetes progressive delivery controllers (Argo Rollouts, Flagger) can do weighted routing for canaries.

Given our scenario is straightforward, a rolling update via Deployment is sufficient.

### 7.4 Monitoring Application Performance using Prometheus and Grafana

Once deployed, monitoring ensures the application is healthy and helps in troubleshooting. **Prometheus** is a popular open-source monitoring tool that scrapes metrics from instrumented services. **Grafana** is used to visualize those metrics in dashboards.

**Integrating Prometheus**:

- Spring Boot Actuator exposes a `/actuator/prometheus` endpoint if you add the Micrometer Prometheus registry dependency. Include `io.micrometer:micrometer-registry-prometheus` in each service.
- Configure Actuator in `application.yml`:
  ```yaml
  management.endpoints.web.exposure.include: health,prometheus
  management.endpoint.health.show-details: never
  ```
  This will allow Prometheus scraping. (In production, you might secure this endpoint or have it only accessible internally).
- Deploy Prometheus server in Kubernetes (or use a managed one). Configure Prometheus to scrape each service. If using the ServiceMonitor CRD (with the Prometheus Operator), it's even easier. Without that, edit prometheus.yml to add a job for our services, perhaps using service discovery labels. Example scrape config:

  ```yaml
  scrape_configs:
    - job_name: "catalog-service"
      metrics_path: "/actuator/prometheus"
      scheme: "http"
      kubernetes_sd_configs:
        - role: endpoints
      relabel_configs:
        - source_labels: [__meta_kubernetes_service_name]
          action: keep
          regex: catalog-service
  ```

  This tells Prometheus to find k8s endpoints for service name "catalog-service" and scrape them.

- Metrics collected: Spring Boot Actuator + Micrometer automatically provides:
  - JVM metrics (memory, GC, threads)
  - HTTP request metrics (`http_server_requests_seconds_count`, sum, etc. for each endpoint and status)
  - Database metrics if using datasource pool (Hikari provides pool stats)
  - Kafka metrics (if Micrometer binder for Kafka is active, or JMX -> Micrometer integration).
  - Custom metrics: you can define your own counters or timers via Micrometer in the code if needed (e.g., count of orders placed, etc., though we can derive that from events as well).

**Grafana Setup**:

- Deploy Grafana (or use a cloud Grafana).
- Add Prometheus as a data source.
- Import or create dashboards:
  - There are many community dashboards for Spring Boot metrics, JVM, etc.
  - Create a custom dashboard for business metrics: e.g., a graph of orders per hour (we could use our Kafka Streams output or directly count events via a PromQL query on an event counter metric).
  - Dashboard for Kafka: monitor consumer lag. You can use Kafka Exporter (a tool that exports consumer lag metrics to Prometheus) to track if any consumer group is falling behind.
  - Dashboard for MySQL: if using a MySQL exporter or if the database is monitored by an external system.

**Key Things to Monitor**:

- **System Metrics**: CPU, Memory of pods (Kubernetes can expose those via cAdvisor metrics to Prometheus).
- **JVM Metrics**: Heap usage, GC time - to catch memory leaks or capacity issues.
- **Throughput**: Number of HTTP requests per second on each service. Latency of requests (Micrometer gives percentile or average timings).
- **Errors**: Rate of 5xx responses. If suddenly lots of errors, trigger an alert.
- **Kafka**: Consumer lag (if lag keeps increasing, consumers are overwhelmed or down), broker health (if using JMX metrics from Kafka brokers).
- **MySQL**: Throughput of queries, slow query count, connections count.

Grafana can be set to send alerts (via email, Slack, etc.) when certain thresholds are breached:

- e.g., alert if 5xx errors > 10/minute.
- alert if consumer lag > X for Y minutes.
- alert if MySQL replication lag (if replicating) is high or if any MySQL is down.

By visualizing metrics, we can also do capacity planning (e.g., see CPU usage trends to decide if we need to scale out/in).

### 7.5 Scaling Kafka and MySQL for High Availability

As usage grows, or for fault tolerance, we need to scale Kafka and MySQL:

**Scaling Kafka**:

- **Brokers**: Kafka is designed to run as a cluster of brokers. Initially you might have 3 broker nodes (common minimum for fault tolerance). Adding more brokers increases capacity (in terms of both throughput and total data storage).
- **Topic Partitions**: Ensure topics have enough partitions to utilize the brokers and allow parallelism. If one partition = one consumer thread at a time, and if you have more potential consumers or more throughput needs, increase partitions. This can be done with `kafka-topics.sh --alter --partitions`.
- **Replication Factor**: For high availability, set replication factor of topics to at least 3 (so if one broker goes down, data is still on others). Kafka will then tolerate broker outages without losing data. _Kafka's replication of partitions across multiple brokers ensures that if one broker fails, another broker with the partition copy can take over, preventing data loss and downtime ([How to achieve high availability for Apache Kafka](https://www.redhat.com/en/resources/high-availability-for-apache-kafka-detail#:~:text=match%20at%20L546%20The%20number,more%20brokers%20from%20the%20cluster))._
- **In-Sync Replicas and Acks**: In production, configure producers with `acks=all` and set `min.insync.replicas` to >= 2 (for replication factor 3) so that a message is only acknowledged if at least 2 brokers wrote it ([How to achieve high availability for Apache Kafka](https://www.redhat.com/en/resources/high-availability-for-apache-kafka-detail#:~:text=Partitions%20may%20be%20replicated%20across,the%20log%20are%20called%20replicas)). We saw earlier setting `acks: all` in config.
- **Throughput Scaling**: As load grows, you can horizontally scale by adding brokers and increasing partitions. Consumers can also scale out. Kafka can handle very high throughput given enough brokers and proper configuration (avoid very large messages, use compression).
- **Monitoring Kafka**: It's important to monitor broker metrics (e.g., if a broker's disk is nearing capacity or if GC pauses are frequent indicating heap issues). Also monitor network IO and throughput to see if approaching limits of the NIC or disk.

- **Handling Failure**: If a broker fails, Kafka's controller will automatically redistribute partition leadership to other brokers that have the replicas (this is why replication factor > 1 is crucial). When the broker comes back, it catches up the data. This is mostly transparent to producers/consumers (consumers might experience a brief pause during rebalance).
- **Scaling consumers**: If the processing in a consumer (like Inventory or Payment) becomes a bottleneck, you can deploy more instances. Just ensure the number of partitions >= number of instances for full utilization (some instances will be idle if more instances than partitions since each partition can only be owned by one in the group). If needed, increase partitions accordingly (Kafka allows increasing partitions, though not decreasing without manual steps).

**Scaling MySQL**:
MySQL is typically scaled for high availability and read throughput via replication. _MySQL replication copies data from a primary to one or more secondaries, allowing automatic failover if primary fails, and distributing read queries to replicas ([What is MySQL High Availability? How to Choose a Solution](https://www.percona.com/blog/choosing-mysql-high-availability-solutions/#:~:text=MySQL%20replication%20contributes%20to%20high,by%20directing%20read%20queries%20to))_.

- **Master-Slave (Primary-Replica)**: Set up MySQL replication where one node is primary (accepts writes) and others are replicas (read-only copies). The replicas asynchronously apply the primary's log.
  - Use this to offload read-heavy operations (like product catalog queries) to replicas. Spring can be configured to route reads to replicas. This can be done by having two DataSources (one for write, one for read) or using an intermediate proxy.
  - Ensure eventual consistency awareness: a read after a write might not immediately reflect if it hit a replica that hasn't caught up. Usually acceptable for most parts of an e-commerce except maybe reading your just placed order (in which case ensure that read either goes to primary or use read-your-writes consistency via some strategy).
- **Failover**: If primary goes down, promote a replica to primary. This can be done manually or via orchestrator software. MySQL can also be set up in an InnoDB Cluster (Group Replication) which provides a form of multi-master or automatic failover (but it's more complex).
  - Alternatively, use keepalived or an HAproxy with virtual IP that points to the primary and switches on failure.
  - Applications should ideally be aware or handle reconnecting if a failover happens. Using a JDBC URL with multiple hosts can help (some MySQL drivers support failover addresses).
- **Partitioning/Sharding**: If the dataset or write volume grows beyond what one primary can handle, you'll consider sharding data across multiple MySQL servers (each shard is its own primary with replicas). For example, shard users by region or user ID range, each shard has its own order table, etc. This is a big design undertaking and usually only needed at large scale. Alternatively, moving certain data to specialized databases (like using NoSQL for sessions, or using an analytics DB for large historical data) can alleviate the load.
- **Performance tuning**: Upgrade hardware (SSD storage, more RAM for buffer pool) as needed. Use connection pooling to not overload with too many connections (MySQL can handle many, but context switching has overhead).
- **MySQL High Availability Solutions**:
  - InnoDB Cluster / Galera Cluster provides a multi-master virtually synchronous replication (like Percona XtraDB Cluster). This can allow writes on any node with automatic conflict resolution, but network latency can limit throughput and there is complexity. It gives 99.99% availability if properly configured ([MySQL Enterprise High Availability](https://www.mysql.com/products/enterprise/high_availability.html#:~:text=MySQL%20InnoDB%20Cluster%20delivers%20a,all%20members%20of%20the%20cluster)).
  - Regular async replication is simpler and often sufficient for mostly read scale out.
  - Ensure backups in place (regular snapshots or mysqldump) and test restoration.

**Load Balancing**:

- For microservice instances: Kubernetes Service or external load balancer will distribute requests among pods. For Kafka, producers normally have a list of broker addresses and the client library does load balancing by picking the broker leader for each partition internally.
- For MySQL replicas: If using a proxy like ProxySQL or HAProxy, you can configure to distribute SELECTs among replicas and send DML to primary, giving a single endpoint to the application. Alternatively, in code separate dataSources.

**Testing Failover**:

- You should test what happens if a Kafka broker is killed (should not lose data and consumers should reconnect).
- Test if a MySQL primary is killed and a replica promoted (maybe your app needs a restart or will it reconnect properly?).
- Incorporate these into chaos testing if possible (simulate failures in staging environment).

At the end of the day, **scaling** is about ensuring the system can handle increased load and that there's no single point of failure. We scale **vertically** (use bigger machine) until it limits, then **horizontally** (more machines) for Kafka and services easily, for MySQL with a bit more planning via replication or clustering.

Next, we'll discuss performance optimization in more detail, beyond just scaling hardware.

## 8. Performance Optimization

Even with proper scaling, we should optimize the system to use resources efficiently and respond quickly. In this section, we cover load balancing and caching strategies, Kafka tuning for throughput, and database optimization via replication and partitioning (some of which we already touched on, but we'll expand or reiterate key points).

### 8.1 Load Balancing and Caching Strategies

**Load Balancing**:

- As mentioned, any stateless service can be horizontally scaled and traffic distributed.
- In Kubernetes, a Service of type ClusterIP paired with an Ingress or Gateway can spread load among pods (which effectively uses round-robin or IP hashing).
- If not using k8s, a cloud LB or Nginx/HAProxy can do round-robin balancing across service instances. For example, if you had 3 instances of catalog-service running on VMs, you could put an Nginx upstream with those 3 IPs and it will balance requests.
- Use health checks in the LB so it stops sending traffic to instances that are down or unhealthy.
- At the global level, if you have users in different regions, consider geo-distributed deployment with a global load balancer or CDN (especially for static content).

**Caching Strategies**:
We implemented caching in the application (product info caching in service memory/Redis). Let's outline a few layers of caching:

- **Client-side caching**: Browsers will cache static resources (images, JS, CSS) if you set cache headers. Also for API responses, one can use HTTP caching (ETag or Last-Modified headers, so the browser can do conditional GET). If an API returns product data with an ETag (hash of content), the next request from same client could include `If-None-Match: <ETag>`, and server can reply 304 Not Modified if unchanged, saving bandwidth.
- **CDN (Content Delivery Network)**: For media like product images, using a CDN (CloudFront, Akamai, etc.) to serve those from edge locations speeds up content delivery and offloads traffic from your servers. Even for API responses that are cacheable (like a public GET of product list), a CDN could cache those for a short time if your data isn't changing every second. But typically, dynamic APIs are not served via CDN unless they are mostly read-only and can tolerate slightly stale data.
- **Application-level caching**: We did via Spring Cache on product data. Similarly, you might cache other expensive operations:
  - E.g., caching the result of a complex SQL query or an external API call (like shipping rates calculation).
  - Use appropriate eviction policies. In Spring Cache with Redis, items can have TTL (time-to-live). For example, product details might refresh every hour automatically or be evicted when product updates.
- **Database caching**: The MySQL buffer pool caches frequently accessed data in memory. Make sure the DB server has enough RAM to hold working set of data. This is handled by MySQL itself (the InnoDB buffer pool).
- **Second-level cache (Hibernate)**: If a certain entity is read very often and rarely changes (like a configuration table), enabling second-level cache might be useful. We would plug in Ehcache or Redis as a Hibernate L2 cache provider. But in microservices, since each instance has its own memory, a distributed cache (like Redis) at service level is often more straightforward to reason about.

**Example - Caching in Order Service**: Suppose calculating the total price of an order requires fetching each product's latest price from product service (if we didn't store price in Order). This could be expensive if many items. We could cache product prices in Order service for quick access (maybe with a short TTL to not be stale for too long).
But as a design, it's better to include price in the Order at creation time to avoid needing that lookup at all later.

**Session Cache**: If we had user sessions (not with JWT but if we did sticky sessions), using something like Redis to store session data so any instance can retrieve it (not relying on sticky session) is a known pattern. We avoided that complexity by using JWT (stateless sessions).

**Cache Invalidation**: Always consider how caches update:

- We set @CacheEvict on product update to remove stale cache. That's one strategy: evict on changes.
- Or choose a TTL such that stale data is acceptable only for a short time, then auto-refresh.
- For distributed caching, ensure all nodes see the invalidation. Using Redis, it's centralized so that's fine. If using local caches per instance, consider using a messaging topic or Spring Boot's ability to send cache invalidation messages to all instances (there are libraries to broadcast cache evict events).

**Avoiding Cache Stampede**: If cache entries expire and suddenly many requests cause a thundering herd to the DB, consider techniques:

- Use cache-aside: first request triggers DB fetch and populates cache ("dogpile prevention": some libraries allow one thread to populate and others wait).
- Pre-warm caches on startup (load some common data into cache).
- Ensure your DB can handle a miss storm or mitigate by staggering TTLs of different keys.

### 8.2 Optimizing Kafka Event Processing for High Throughput

Kafka itself can handle high throughput, but we need to ensure our usage of it is optimized:

- **Batching**: Kafka producers can batch multiple messages before sending to reduce network overhead. The config `batch.size` (default 16KB) and `linger.ms` (default 0) control this. If throughput is more important than per-message latency, increase `batch.size` (to say 64KB or 128KB) and set `linger.ms` to a few milliseconds (5-100ms) so that the producer waits to batch more messages. This yields larger sequential writes, boosting throughput.
- **Compression**: Enable compression on producer (e.g., `compression.type=zstd` or `snappy`). Compressed messages use less network and disk, allowing faster transfer especially for text-based events like JSON. It does add CPU cost to compress/decompress, but usually worth it unless CPU is your bottleneck. Kafka will compress batches as one unit which is efficient.
- **Consumer Tuning**:
  - Increase `fetch.min.bytes` and `fetch.max.wait.ms` on consumer to allow server to send larger batches per fetch request.
  - Process messages in batches if possible. For example, if 100 order events come in, maybe commit offset after processing them in a loop rather than per message (Spring Kafka by default will batch commits).
  - Tune `max.poll.records` (how many records a poll() returns). If your processing per message is light, you can increase this to process more per poll call.
  - If using Spring Kafka concurrency (multiple threads), ensure partitions are sufficient. The concurrency setting will create that many threads in the listener container, each thread can handle one or more partitions.
- **Parallel Processing inside Consumer**: If message processing involves IO or external calls, you can parallelize handling of messages from one partition as long as you preserve order for those that need it. This is complex, as Kafka's guarantee is per partition ordering. If you reorder within partition, you break that, so only do parallel if order doesn't matter for a set of messages (or use a pattern like work-stealing).
- **Idempotency and Retries**:

  - Kafka producer has an idempotent mode (setting `enable.idempotence=true`) which ensures that resending due to ack timeouts won't duplicate messages on broker. This is enabled by default in latest Kafka clients when using transactions or if explicitly set. We didn't explicitly cover it, but it's a good idea for critical exactly-once flows.
  - Consumer side, design idempotent processing: if a consumer crashes after processing but before commit, it will reprocess on restart. Ensure that if an order is already marked confirmed, processing the event again doesn't double-confirm or duplicate an entry (i.e., check state or use unique constraints).
  - You can also use **Kafka transactions** to achieve exactly-once between producers and consumers (e.g., Payment service could consume OrderPlaced and produce PaymentCompleted in one transaction so that either both the consumption and production are committed or none). Spring Kafka supports this (KafkaTemplate with transactions), but it adds complexity and usually idempotent logic + at-least-once is enough.

- **Monitoring Kafka throughput**: measure the producer send rate and consumer lag. If lag is growing, likely consumers are not keeping up. Possibly scale consumers or optimize their code. If producers saturate network or broker disk, consider adding brokers or splitting topics.

- **Avoid Very Large Messages**: Kafka is not ideal for huge messages (like megabytes). It prefers many small messages. If you have to send something like an image or a big JSON, consider storing it in cloud storage or a DB and send a reference. Or increase broker `max.message.bytes` carefully. Large messages can cause high memory usage and longer GC pauses on brokers, affecting throughput.

- **Kafka Streams optimization**: If using Streams, it also has configs for caching, commit interval, etc., to optimize stateful operations. For example, enabling record cache in Streams can combine many updates to the same key before flushing to the state store, reducing downstream churn.

- **Backpressure**: If a consumer cannot keep up, the broker will stop sending when consumer's internal buffers (fetch buffer) are full. This will lead to lag. You should either speed up consumer or if not possible (maybe external calls are slow), consider adding more consumer instances to divide the work (with more partitions).

- **Scaling Out**: As volume grows, scale out horizontally which Kafka handles well. For instance, an event spike on Black Friday – ensure partitions are enough and maybe temporarily run more consumer instances.

### 8.3 Database Replication and Partitioning Strategies

We have discussed replication in 7.5, but let's focus on using it for performance and partitioning:

- **Replication for Reads**: Setup one or more read replicas for MySQL. Then:
  - If your application is read-heavy, route read-only queries to replicas. E.g., product catalog browsing (which might be 90% reads) can mostly hit replicas. Only writes (adding product or updating price) go to primary.
  - This can dramatically improve throughput by not overloading the primary with reads, and by utilizing additional hardware. Essentially, it's horizontal scaling for reads.
  - Ensure you have a mechanism to route queries. One approach: use Spring AbstractRoutingDataSource to choose DataSource based on read vs write context (this can be done by AOP marking methods as read-only). Or simpler, manually use a different repository bean that uses a replica. In microservices, you might not need it if each service’s load is manageable, but e.g., product service might benefit if a lot of traffic.
- **Partitioning**:
  - MySQL supports partitioning a single table by a key or by date. This splits data into multiple physical files, which can improve query performance if it can skip partitions. For example, partition orders by year; a query for this year's orders only touches that partition (faster and smaller index).
  - Partitioning can also help maintenance (you can drop old partitions easily, or place different partitions on different storage).
  - However, it's somewhat advanced to tune and sometimes not necessary until tables are huge (millions of rows).
  - Range partitioning by date is common for logs, events, etc. For orders, maybe by order date or by order ID range.
  - MySQL 8 also has generated columns and you can partition by that if needed (like partition by hash of user_id to spread a table across partitions).
- **Sharding** (Application-level partitioning):

  - If one database server cannot handle the write load, you might shard. Example: users with ID 1-1M on one DB, 1M-2M on another. The application (or an ORM extension like Hibernate Shards, or middleware) decides which DB to use per request based on user.
  - This requires your code to be shard-aware. Also complicates joins (can't easily join across shards).
  - It's usually a last resort when scaling a single DB vertically or via replication isn't enough.
  - Alternatively, break the monolithic database by service (which we already do) or by use-case. We already did per microservice, so each service is easier to scale individually.

- **NoSQL / Caching**:

  - Offload certain data to caches or search engines. E.g., if doing full-text search or analytics queries on orders, rather than hitting MySQL which is OLTP, use ElasticSearch or a data warehouse for those heavy read queries. This way the primary DB is free for main transactional workload.
  - Similarly, use Redis or in-memory caches for frequently accessed reference data to reduce DB hits.

- **Connection Pool & Concurrency**:

  - If scaling out to many instances, each running a DB connection pool, be cautious not to overwhelm DB with too many connections. MySQL can handle thousands of connections, but memory and context switching overhead can become an issue. Sometimes using a proxy with connection pooling helps.
  - The optimal pool size per instance might be 10-20. If you have 10 instances, that could be up to 200 connections. If a replica can handle that, fine. Otherwise, you might tune down pool or increase MySQL's max connections and OS limits.

- **High Availability**:
  - If using replication, implement automated failover (like MySQL router or Orchestrator to detect primary failure and promote a replica). This ensures minimal downtime.
  - Conduct failover drills to ensure the application reconnects properly.

In summary, **optimize database usage** by:

- Using caches to reduce direct DB load.
- Scaling reads via replication.
- Partitioning data to keep queries on smaller chunks.
- Considering sharding if absolutely needed for writes.
- Optimizing queries and indexing (from 5.3) to make each query as efficient as possible, so the DB can handle more load per unit of time.

With these optimizations in place, the system should handle high traffic and large data volumes with grace.

Finally, we will focus on testing and debugging which ties together ensuring everything works and how to troubleshoot issues in such a distributed environment.

## 9. Testing and Debugging

Testing is critical to ensure each part of our system works in isolation and together. Debugging issues in a distributed microservices architecture can be challenging, so it's important to have strategies and tools for troubleshooting.

### 9.1 Writing Unit, Integration, and Performance Tests

**Unit Tests**:

- Write JUnit tests for individual classes: services, utility methods, etc. Use mocking (e.g., Mockito) to isolate from external dependencies. For example, test ProductService with a mock ProductRepository to ensure business logic (like caching or transformation) works.
- Test edge cases: empty inputs, invalid inputs (expect exceptions), typical outputs.
- Aim for high coverage on critical parts (authentication logic, order total calculation, etc.).

**Integration Tests**:

- Spring Boot allows writing tests that start a slice of the application or the whole context. Use `@SpringBootTest` for a full context test (which will start the app, connect to DB if configured, etc. - often with in-memory DB for testing).
- Use profiles or configuration for tests: e.g., point to an H2 in-memory database for integration tests of repository layer.
- For testing Kafka integration, you can use **Testcontainers** to spin up a Kafka and MySQL in Docker just for tests ([Testing Spring Boot Kafka Listener using Testcontainers](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/#:~:text=MySQL%2C%20where%20we%20implement%20a,modules%20in%20conjunction%20with%20Awaitility)). As referenced earlier, **Testcontainers** library is great for this: it can automatically start Kafka, ZooKeeper, and MySQL in the background and provide the connection info to your Spring context. _You can create a Spring Boot project selecting Testcontainers for Kafka and MySQL, which allows writing tests that bring up ephemeral Kafka and MySQL instances to test the Kafka listeners and repository operations end-to-end ([Testing Spring Boot Kafka Listener using Testcontainers](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/#:~:text=Getting%20Started))_.

  Example using Testcontainers in a test:

  ```java
  @Testcontainers
  @SpringBootTest
  class OrderServiceIntegrationTest {
      @Container static KafkaContainer kafka = new KafkaContainer("5.5.0"); // starts Kafka
      @Container static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.1");

      @DynamicPropertySource
      static void configureProperties(DynamicPropertyRegistry registry) {
          registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
          registry.add("spring.datasource.url", () -> mysql.getJdbcUrl());
          registry.add("spring.datasource.username", mysql::getUsername);
          registry.add("spring.datasource.password", mysql::getPassword);
      }

      @Autowired OrderService orderService;
      @Autowired OrderRepository orderRepo;
      // ... set up any needed data (e.g., product stub or connect to product service stub)

      @Test
      void testPlaceOrderEndToEnd() {
          // Setup: maybe insert a product in DB or stub a response
          // Execute
          Order order = orderService.createOrder(testUserEmail);
          // Now, because Kafka events are async, we might need to wait or use Awaitility to wait for inventory & payment to process
          Awaitility.await().atMost(5, TimeUnit.SECONDS).until(() -> {
              Order updated = orderRepo.findById(order.getId()).get();
              return updated.getStatus().equals("CONFIRMED");
          });
          // Verify final state
          Order finalOrder = orderRepo.findById(order.getId()).get();
          assertEquals("CONFIRMED", finalOrder.getStatus());
          assertNotNull(finalOrder.getConfirmationDate());
      }
  }
  ```

  This example demonstrates how we can test the saga flow in one JVM, albeit it can be complex. Alternatively, test smaller pieces: e.g., test that Inventory listener correctly deducts stock when receiving a message (using Spring Kafka test to send a record to a topic), etc.

- **Mocking External Services**: For example, when testing OrderService, you don't want it to call an actual Payment gateway. You can inject a Mock PaymentClient that simulates responses. For inter-service calls, perhaps use WireMock to stub HTTP calls if any.

- **API Tests**: Use MockMvc (for Spring MVC) to test REST controllers without starting the server. Or use WebTestClient for WebFlux if applicable. This ensures endpoints return expected JSON and status codes given certain inputs (with services mocked).

**Performance Tests**:

- Use a tool like **JMeter** or **Gatling** to simulate load on the application. For example, simulate 100 concurrent users browsing products and placing orders. This can be part of your test plan to see how the system performs, though typically done outside of unit test suite.
- Alternatively, do performance testing on a deployed staging environment to get more realistic results (including network, etc.).
- Identify the throughput and response time under load, and see where the bottlenecks are (maybe the DB CPU or Kafka I/O).
- Also test scaling: try doubling the pods to see if throughput roughly doubles, indicating no single bottleneck. If not, find what limits it.

**Testing in CI**: Ensure that unit and integration tests run on each CI pipeline to catch regressions early. Possibly use separate stages for slow integration tests so they don't run on every small change, but at least on main branch merges.

### 9.2 Debugging Kafka Message Failures and Troubleshooting MySQL Performance Issues

**Debugging Kafka Issues**:

- A common scenario: a message is not processed as expected, or the consumer seems stuck (maybe due to an exception causing retries).
- Enable DEBUG logging for the `org.springframework.kafka` and `org.apache.kafka` packages when troubleshooting. This can show if consumers are polling, if there's any deserialization error, etc. For example, if a JSON can't map to the object, you'll see an error in logs. Or if offset commits fail, you'll see logs.
- **Dead Letter Topic**: Consider configuring a dead-letter topic for each consumer group. Spring Kafka can be configured such that after 3 failures of a message, it publishes it to a topic like `orders.DLT`. You can then have a process or just logs that monitor that. That helps avoid one bad message blocking the queue.
- **Consumer Lag**: If noticing that something isn't processing, check the lag. Use Kafka tools:
  - The Kafka CLI `kafka-consumer-groups.sh --describe --group order-service` shows the lag per partition.
  - If lag is increasing, maybe the consumer thread died or is stuck. Check if the consumer application is still running. If using Spring Boot Actuator, the health endpoint for Kafka can show if the consumer is up.
  - If consumer is alive but lagging, maybe it's slow processing. Check metrics of consumption rate vs production rate.
- **Resilience**: Make consumers idempotent and capable of reprocessing. E.g., if Inventory service crashed after reserving inventory but before sending event, on restart it might process OrderPlaced again. Ensure either the operation is idempotent (e.g., check if that order already marked inventory reserved before doing it again).
- **Ordering issues**: If events come out of expected order (maybe due to multi-partition), ensure that keys are set such that order-sensitive events go to same partition. For example, "OrderPlaced" and "OrderCancelled" for the same order should have same key (orderId) so the cancellation won't be processed before placement by inventory if it were cross-partition. If a design bug happened there, fix the key usage.

**MySQL Performance Issues**:

- If the application experiences slow queries in runtime, enable the MySQL slow query log (log queries taking > 2 sec for example). Analyze those queries, and add indexes or optimize them.
- Use `EXPLAIN` on problematic queries to see if they are using indexes or doing full table scans.
- Check MySQL server performance metrics:
  - CPU usage high? Could mean inefficient queries or lack of indexes causing a lot of scanning.
  - Disk I/O high? Perhaps too many writes or not enough memory (causing caching to be ineffective).
  - Lock waits or deadlocks? Run `SHOW ENGINE INNODB STATUS\G` to see recent deadlocks. If deadlocks happen, you'll see which queries deadlocked. Then you can try to redesign to avoid that (maybe processing in a different order, or adding an index so locks are row-level not gap locks, etc.).
- **Connection Issues**: If you see errors like "Too many connections", you might need to raise MySQL `max_connections` or ensure the app is closing connections (with HikariCP, it should). Possibly some connections are not returned (connection leak) - use Hikari metrics or logs to detect leaks.
- **Timeouts**: If some queries time out, consider if they are waiting on locks or just slow. For locks, see above. If just slow (lack index or doing heavy computation like a giant join or sort), optimize query or add caching for that query result.

- **Using Profilers**: There are tools like Java Mission Control for profiling the app if CPU is high (to see if the bottleneck is in the app code vs DB).
- **Database Profiler**: You can log all SQL executed by Hibernate (`spring.jpa.show-sql=true` and log level for SQL) but that's too verbose for production. Instead, maybe for a test scenario log to see if any unexpected queries are being called excessively.

**Memory Issues**:

- If an OutOfMemoryError happens in a service, get the heap dump and analyze. Common causes: too many objects (could be due to an infinite loop producing objects, or reading a huge result set into memory).
- For example, accidentally loading all products (when millions) into memory could OOM. Use pagination or streaming if needed for large data processing.

**Distributed Tracing for Debugging**:

- It can be hard to trace a request across microservices. This is where distributed tracing (Zipkin/OpenTelemetry) helps. If we integrate OpenTelemetry with our services, each event or HTTP call carries a trace context. Then in Zipkin/Grafana Tempo/Jaeger, you can see a trace that might look like:
  - HTTP request to Order Service (traceID:123 spanID:a1)
    - OrderService placed order, produced Kafka event (span a1 might log an annotation or event)
  - InventoryService consuming OrderPlaced (span a2, with same traceID:123 maybe, if we propagate somehow via headers in Kafka - that requires custom propagation since Kafka doesn't automatically propagate trace context).
  - PaymentService consuming OrderPlaced (span a3).
  - OrderService consuming InventoryReserved (span a4).

If you ensure trace context flows (one way: include trace info in message headers when publishing, and configure Kafka instrumentation to pick it up), you can trace an end-to-end flow and spot where delays occurred.

**Using Logs**:

- Consolidate logs with a tool like ELK (Elasticsearch, Logstash, Kibana) or Splunk. Use correlation IDs (like trace ID or order ID) in log messages to correlate events across services. For example, log "Order 123 placed" in Order service and "Processing Order 123 in Inventory" in Inventory service. If an order failed, you can search logs for "Order 123" and see what happened in each service.
- Log at appropriate levels (info for major events, debug for detailed internals, error for exceptions with stacktrace).
- In production, set log level to INFO or WARN generally; DEBUG only for diagnosing because it can be verbose and affect performance.

**Common Microservice Debugging Issues**:

- Network issues: e.g., one service can't reach another due to DNS or config. Use tools like `kubectl exec` into a pod and use curl to test connectivity. Or check service endpoints.
- Misconfiguration: e.g., wrong Kafka topic name or wrong credentials for DB. These usually show up as exceptions on startup.
- Serialization issues: version mismatch of classes between services. If you change an event structure, ensure backward compatibility or deploy services in order that consumers can handle old and new. If a service throws ClassCast or JsonMappingException on message, consider using a schema (like Avro + Schema Registry) to manage versioning or at least handle unknown fields gracefully (Jackson by default will ignore unknown JSON fields if configured so).
- Timeouts: if synchronous REST calls are used anywhere, implement timeouts and fallback. E.g., if Order service had to call Payment service via REST synchronously (we avoided by async design), and Payment is down, the request would hang. Set a reasonable timeout and handle it (maybe cancel order or try later).

In microservices, **failures will happen**, so design for resiliency:

- Implement retries with backoff for transient errors (e.g., if Kafka send fails due to network glitch, Spring Kafka template already retries internally by default a few times).
- Circuit breakers (via Resilience4j/Spring Cloud Circuit Breaker) if a dependent service is failing constantly – route around or fail fast.
- Graceful degradation: e.g., if recommendation service is down, still serve the main page, just without recommendations.

By thoroughly testing (unit, integration, perf) and using the above debugging techniques, you can ensure the system works correctly and efficiently, and quickly find and fix issues in production.

### 9.3 Using Distributed Tracing Tools (Zipkin and OpenTelemetry)

As systems grow complex, just logs and metrics might not give the full picture of how a single request flows through multiple services. Distributed tracing helps track a request across service boundaries by assigning a unique trace ID and propagating it.

**OpenTelemetry** is the emerging standard for instrumentation. Spring Boot supports it via Micrometer Tracing or the older Spring Cloud Sleuth (which is now phased into Micrometer/OTel).

**Setting up tracing**:

- Add dependencies: e.g., `io.micrometer:micrometer-tracing-bridge-brave` and the OpenTelemetry exporter (or use Brave (Zipkin) as implementation). Or use the newer `spring-boot-starter-actuator` in Spring Boot 3 which includes Micrometer and then add `micrometer-tracing` dependencies.
- Configure an exporter: For Zipkin, add `micrometer-tracing-bridge-brave` and `zipkin-reporter-brave`. Or use OpenTelemetry with an OTLP exporter to something like Jaeger.
- With Spring Cloud Sleuth (if using Spring Boot 2.x), it was easier: just include `spring-cloud-starter-sleuth` and `spring-cloud-sleuth-zipkin` and it auto-traces and sends to Zipkin.

**Trace context propagation**:

- In our asynchronous flow (HTTP -> Kafka -> HTTP), we need to propagate trace IDs. Sleuth could propagate over messaging by adding trace IDs in headers. OpenTelemetry can do similar with the W3C Trace Context (which is typically carried in HTTP headers `traceparent`, and can be carried in Kafka headers too).
- If configured right, when Order service sends a Kafka message, it should include the trace context in message headers. Inventory and Payment services should pick that up and continue the trace. This way one trace ID links the entire flow.

**Zipkin/Jaeger**:

- Deploy Zipkin server (which collects traces, or use a SaaS like Grafana Tempo or Jaeger all-in-one).
- The services then send trace data to that server (e.g., via HTTP for Zipkin).
- Use the UI to search traces by ID or by tags (like search by "orderId" if you add that as a tag, or by operation name).
- A trace timeline will show spans for each service with durations. For example:

  - Span: `OrderService.placeOrder [200ms]`
    - Span: `Kafka produce orders topic [5ms]` (as a child or following span)
  - Span: `InventoryService.handleOrderPlaced [50ms]`
  - Span: `PaymentService.handleOrderPlaced [1200ms]` (maybe calling external, so longer)
  - Span: `OrderService.handleInventoryReserved [3ms]`
  - Span: `OrderService.handlePaymentCompleted [3ms]`
    - Span: `Kafka produce order-confirmed [2ms]`
  - Span: `NotificationService.handleOrderConfirmed [30ms]`
    - Span: `EmailService.sendEmail [25ms]`

  This kind of trace shows the critical path (Payment took 1200ms, dominating the timeline), which helps performance tuning (maybe use a faster payment gateway or handle async). It also shows if any service was waiting on something or if something retried (would see multiple spans attempts).

- The trace also helps debug errors: if a span has error flag, you see exactly where it occurred. E.g., if Payment failed, the PaymentService span would have an error tag with exception.

**Adding custom tags**:

- You can annotate spans with custom data. E.g., tag orderId on the relevant spans. Or if an error happens, attach the error message.
- With Micrometer, you might use an aspect or manually do `Tracer.currentSpan().tag("orderId", orderId)` within the processing method.

**Performance Overhead**:

- Tracing every request can add overhead (small, but if sample 100% and heavy load, the tracer could be a bottleneck). Usually you sample a small percentage of requests (like 1%) in production, unless troubleshooting an issue or in lower environments.

**Outcome**:

- _Zipkin is an open-source tracing system that helps gather timing data needed to troubleshoot latency problems in microservice architectures ([Implementing Distributed Tracing with Spring Boot and Zipkin](https://vitiya99.medium.com/implementing-distributed-tracing-with-spring-boot-and-zipkin-d46079c38372#:~:text=Implementing%20Distributed%20Tracing%20with%20Spring,latency%20problems%20in%20microservice%20architectures))._ Using it or similar, we gain insight into how requests traverse the system and where the slow points or failures are.
- It greatly speeds up debugging in distributed systems by providing a clear picture of the request path and timings.

By incorporating tracing, our debugging capabilities become much stronger, complementing logs and metrics.

### 9.4 Testing Recap and Continuous Improvement

To wrap up the testing/debugging section, remember:

- Automate tests and run them regularly (CI).
- Monitor in production and have alarms to catch issues before users notice.
- Practice chaos testing (e.g., kill pods randomly, drop Kafka messages in a staging environment) to ensure the system is resilient.
- When bugs occur, write new tests to cover them to avoid regressions.
- Keep improving logging and tracing as the system evolves (what you think is enough logging today might not be enough when new features add complexity).

Now, in the final section, let's look at future enhancements and roadmap ideas to extend our platform.

## 10. Future Enhancements and Roadmap

Software projects are never truly "done" – there's always room to add features or improve the architecture. In this last section, we look at potential future enhancements for our e-commerce application, especially leveraging AI/ML for recommendations and exploring more advanced event-driven patterns to further increase resilience and functionality.

### 10.1 Adding AI-Based Recommendations

One powerful addition to an e-commerce platform is a **recommendation engine** to personalize the user experience. AI-based recommendations can increase user engagement and sales by suggesting products the user is likely to buy.

**Types of Recommendations**:

- **Collaborative Filtering**: "Users who bought X also bought Y". This uses user behavior data (ratings or purchase history) to find similarities between users or items.
- **Content-Based Filtering**: Recommend items similar to what a user liked in the past (e.g., similar category or attributes).
- **Hybrid Approaches**: Combine multiple signals, possibly with machine learning models.

For example, when a user views a product, show a list of related products they might like, or on the home page have a "Recommended for you" section based on their past interactions.

**Data for Recommendations**:

- User behavior events: page views, add to cart, purchases. We have a stream of these events (we could produce a "ProductViewed" event when a user looks at a product page, etc., in addition to Order events).
- Product metadata: categories, price, etc.

**Building the Engine**:

- We could use Apache Mahout or create a custom ML pipeline using Python libraries (pandas, scikit-learn, TensorFlow).
- Possibly use **Kafka Streams** or Spark to maintain real-time counts (like which products are often bought together).
- One could train an **ALS (Alternating Least Squares)** model for collaborative filtering on user-product interactions (Spark's MLlib has this).
- A simpler approach: maintain a co-purchase graph. If order contains product A and B, increment a counter for (A,B). Later, to recommend for someone viewing A, suggest the top B associated. This can be done streaming with Kafka Streams join of order items, or offline with periodic batch.

**Real-Time vs Batch**:

- **Batch processing**: e.g., daily offline job that crunches logs or DB data to update a model (like a matrix factorization for user factors and item factors). Then store that model (maybe as matrices or rules) and query it for recommendations.
- **Real-time streaming**: e.g., use Kafka Streams to update counts of co-occurrences continuously ([Building a Kafka-Powered Recommendation Engine | Reintech media
  ](https://reintech.io/blog/building-kafka-powered-recommendation-engine#:~:text=,databases%20like%20Cassandra%20or%20Elasticsearch)). This could feed into a store or directly serve simple recommendations (like "trending products" or "frequently bought together").

**Deployment of ML**:

- If using a heavy ML model (like a deep learning model for recommendations), you might train it outside and then deploy it behind an API (could be a microservice e.g., `recommendation-service`) which given a userId returns list of recommended productIds.
- That service could be backed by a precomputed model (like a TensorFlow model loaded into memory to do predictions).
- Alternatively, on each request it could do a look-up in a precomputed table (like we computed top N products for each user nightly).

**Example Roadmap**:

1. **Phase 1**: Implement a simple rule-based recommender: e.g., for product detail page, use "people also bought" logic via co-purchase counts. Compute those counts from past orders (maybe using a cron job or a Kafka Streams job as events come in). This doesn't involve complex ML but adds immediate value.
2. **Phase 2**: Implement user-based recommendations: gather each user's purchase history and compare with others to recommend new products (collaborative filtering). This could be done by integrating with a library or service. Possibly start with an open-source solution or a SaaS (like Amazon Personalize or Google Recommendations AI if we wanted managed).
3. **Phase 3**: Use advanced ML techniques: train a model that uses not just co-purchase, but browsing history, ratings, even product images or descriptions (NLP or computer vision could be used to find similar products). This is more R&D heavy.
4. **Phase 4**: Real-time personalization: as the user interacts (clicks or buys), immediately update recommendations shown (maybe via streaming updates to their user profile vector).

**Data considerations**:

- Ensure privacy: if using personal data, follow regulations (GDPR etc.). But for recommendations, usually it's non-sensitive behavioral data.
- Cold start problem: new users or new products with no history. Use fallback like popular items or category bestsellers in that case.

In short, adding AI-driven recommendations can be done gradually, starting from basic analytics to sophisticated AI. It leverages the data flowing through our system (which Kafka makes easy to tap into, since we can branch the event stream to feed the recommender logic). For example, _user interactions and behaviors are captured and sent to Kafka topics, stream processing (Kafka Streams or Flink) processes these streams, and machine learning models use the processed data to generate recommendations ([Building a Kafka-Powered Recommendation Engine | Reintech media
](https://reintech.io/blog/building-kafka-powered-recommendation-engine#:~:text=,databases%20like%20Cassandra%20or%20Elasticsearch))_.

### 10.2 Implementing a Recommendation Engine using Machine Learning

Let's detail a specific approach to integrate a machine learning-based recommendation engine:

**Architecture** ([Building a Kafka-Powered Recommendation Engine | Reintech media
](https://reintech.io/blog/building-kafka-powered-recommendation-engine#:~:text=Architecture%20of%20a%20Kafka,Engine)):

- We have a dedicated **Recommendation Service**. It might consist of two parts: offline model training and online serving.
- _Data Ingestion_: All relevant events (views, carts, orders) are published to Kafka topics (already in our architecture or easily added). This streaming data forms the backbone for training data.
- _Stream Processing_: Use Kafka Streams to aggregate or prepare features. For example, maintain a rolling count of views per product, or a list of products each user viewed.
- _Model Training_: Could be done outside the live system. For instance, set up a nightly job (could be a Spark job on a separate cluster or even a Python script that consumes from Kafka or reads from a data lake) to train a collaborative filtering model. The model could be something like matrix factorization (ALS) or neural collaborative filtering. After training, the model (parameters) need to be accessible to make predictions.
- _Model Serving_: The Recommendation Service loads the model. If it's a simple model (like a matrix of user and item factors), the service can in-memory load those or store in a fast DB. If it's a neural network, maybe use TensorFlow Serving or a microservice that hosts the model.
- _API_: Provide an endpoint like `GET /recommendations?userId=123` which returns a list of recommended product IDs (which the UI can then fetch details for from product service).
- _Alternatively_, instead of on-demand computing, pre-compute top N recommendations for each user and store them, update periodically. Then the service just reads that list.

**Machine Learning aspects**:

- Use user's past orders as implicit feedback (they purchased = they liked that product). Possibly also use "view but not purchase" as weaker feedback.
- Represent this as a user-item matrix and factorize it (ALS) to get latent features.
- The output: for each user, a vector of preferences; for each product, a vector of attributes. To recommend, find products not purchased by user with high predicted rating (dot product of user vector and item vector).
- If using ALS, platforms like Spark or Nvidia Rapids can handle training on large data.
- If we want to incorporate product content (like description or category), we could train a hybrid model (like content-based filtering for new items and collab filtering for existing).
- A simpler interim solution: popularity within categories, or recently trending. For example, "hot deals" which is basically top sellers of last week in each category – can be computed with Kafka Streams windowing and then shown to everyone or segmented by category browsing.

**Tools**:

- **Apache Spark**: can subscribe to Kafka via Structured Streaming, aggregate and then do ALS training (Spark MLlib's ALS).
- **TensorFlow/PyTorch**: if we go for deep learning (like using an Embedding approach for users and items and training a neural network to predict interaction).
- **Python + Surprise library**: There's a library called Surprise for building recsys that can do SVD etc. on rating data easily for a prototype.

**Integration**:

- If using Spark or similar externally, results (like user factors and item factors, or recommendations) could be written to a database table or a Redis cache where the Recommendation service can pick them up.
- Alternatively, use **Kafka for model distribution**: once model is trained, produce an event with new model version. The Recommendation service listens and updates its in-memory model (this is more advanced, but Kafka can distribute updates in real-time).

This shows how we can _enhance the system with machine learning, turning our data into tangible personalization features for users_.

### 10.3 Exploring Additional Event-Driven Patterns with Kafka

We've used Kafka mainly for saga orchestration. There are more advanced patterns in event-driven microservices we can implement:

- **Event Sourcing** ([Design Patterns for Microservices Communication with Apache Kafka - NashTech Insights](https://blog.nashtechglobal.com/design-patterns-for-microservices-communication-with-apache-kafka/#:~:text=)): Instead of storing just the final state in the database, store all state changes as an event log. For example, rather than Order having a status field that gets updated, we would store events like OrderCreated, InventoryReserved, PaymentCompleted, OrderConfirmed events in an event store (Kafka or a log). The current state can be derived by replaying events.
  - The advantage is an audit trail of all changes and the ability to rebuild state if needed (e.g., if a new service needs to reconstruct all orders, it can consume the event log from the beginning).
  - We partially do this by keeping events in Kafka, but typically event sourcing would mean the primary source of truth is the event log, and perhaps we use Kafka as the event store with a compacted topic or something like Event Store DB.
  - In our design, we still used MySQL as the source of truth for final state; to adopt event sourcing, we'd shift to using Kafka (or another store) as the source of truth and maybe use MySQL as a projection for querying.
  - We might explore using Kafka compacted topics for entity state. Each order could be a key on a compacted topic, with events as values updating it. Or integrate something like Debezium if we wanted to capture DB changes to produce events (but we already produce events natively).
- **CQRS** ([Design Patterns for Microservices Communication with Apache Kafka - NashTech Insights](https://blog.nashtechglobal.com/design-patterns-for-microservices-communication-with-apache-kafka/#:~:text=,CQRS)) (Command Query Responsibility Segregation):

  - We touched on this: separate write models and read models. We could introduce dedicated read services that consume events to maintain read-optimized views. For example, a service that builds a materialized view of orders with product details (so that UI can call one service to get an order with all info, instead of calling Order and then Product). This read service (maybe built on Elasticsearch or even a graph database if querying relationships) subscribes to events from Order and Product services to keep its view updated.
  - Using Kafka, implementing CQRS is straightforward: each event (Command side changes) is published, the Query side microservice updates its store accordingly ([spring boot - Microservice database architecture for Ecommerce web app - Stack Overflow](https://stackoverflow.com/questions/61021346/microservice-database-architecture-for-ecommerce-web-app#:~:text=Since%20you%20are%20using%20multiple,to%20get%20an%20idea%20link)).
  - If at some point we need to provide complex reports (like "total revenue by category per month"), a separate reporting service could consume events and update a reporting DB optimized for such queries.

- **Saga Orchestration**:

  - We used a choreography saga (no central coordinator, events trigger next actions). For complex workflows, sometimes an orchestrator is easier to manage. We could implement an **Orchestration Saga** pattern with a dedicated "Order Orchestrator Service" that listens for order events and explicitly calls or commands other services.
  - For example, instead of Inventory and Payment independently consuming OrderPlaced, the Orchestrator could consume OrderPlaced and then send explicit command messages: "ReserveInventory" to inventory service, then wait, then send "ProcessPayment" to payment service, etc. This can simplify handling of failure compensation in one place. The trade-off is that it introduces a central brain which could be a single point of failure or bottleneck if not careful (though it can be made stateless and redundant).
  - Tools like Camunda or Temporal are workflow engines that can help manage such orchestrations reliably (with state machines and timers, etc., for things like if payment doesn't respond in time).

- **Outbox Pattern**:
  - To ensure atomic write to DB and produce event (without distributed txn), one can use the outbox pattern: write the event to an "outbox" table in the same DB transaction as the entity update, then a separate process reads that table and publishes to Kafka. There are frameworks and Debezium (CDC) solutions for this. This guarantees no order update occurs without its event being sent.
  - In our implementation, we somewhat assumed events could be produced after commit (potentially risking a lost event if service crashes after DB commit but before producing event). The outbox pattern would eliminate that risk. We might plan to introduce it for robustness.
- **Kafka as Communication Backbone**:
  - We can further use Kafka for other async communications: for example, sending notifications, which we did. We can also integrate with external systems using Kafka Connect (e.g., stream data to an Elasticsearch sink connector for search, or to S3 for archive).
  - Use **Kafka Streams for monitoring**: one could even use Streams to detect anomalies, e.g., a sudden spike in orders in a short time (could indicate a bot or just a peak load).
- **Exactly-Once Processing**:

  - Kafka has transaction APIs that can ensure a set of operations (consuming a message and producing another) is done exactly once, even in failure. We might explore using this for critical paths (like Payment to ensure we don't charge twice or miss charging).
  - Currently, we rely on idempotency, which is simpler and usually enough. But if we wanted, enabling idempotent producer (which we did implicitly, perhaps) and using transactional producer/consumer could guarantee no duplicates end-to-end.

- **Microservices Evolution**:

  - As features grow, we might split services further (e.g., separate an Email service from Notification if that becomes large, or split user auth vs user profile).
  - Or use Domain-Driven Design to reorganize boundaries. But with events, splitting or merging services is easier because as long as they respect the event contracts, others don't need to know internals.

- **Polyglot**:
  - Kafka being language agnostic means we could add services in other languages if needed (e.g., a Node.js service for some real-time webSocket push, or a Python service for some ML work) and integrate them by consuming/producing to topics.

**Roadmap Recap**:

- Short term: implement recommendations and perhaps a basic reporting service via Kafka events.
- Mid term: consider event sourcing/CQRS where beneficial to improve flexibility (with caution on complexity).
- Long term: fine-tune the architecture with saga orchestration or workflow management for easier maintenance if business processes get complicated (returns, cancellations flows, etc., can be orchestrated).
- Also, evaluate new tech: maybe use **GraphQL federation** to let front-end query multiple microservices in one go if GraphQL is adopted widely.
- Keep an eye on tech upgrades: e.g., newer Kafka features (KRaft mode removing ZooKeeper), MySQL innovations, Spring Boot updates, etc.

Finally, always gather feedback from production usage to guide what enhancements matter. If, for example, search is slow, maybe integrating ElasticSearch becomes a priority. If deployment is problematic, maybe invest in better CI/CD or container orchestration.

This concludes the guide. We've covered setting up the environment, building the application step by step, utilizing Spring Boot, Kafka, MySQL effectively, and ensuring the system is secure, performant, and scalable. By following these steps and best practices, you can develop a robust e-commerce platform ready for real-world demands, and with the roadmap ideas, you can continue to evolve it with advanced capabilities over time.
