# Advanced Spring Boot Application Development: A Step-by-Step Guide

Welcome to this comprehensive **step-by-step guide** for advanced developers building a Spring Boot application with a modern tech stack. We will create a robust RESTful service with **Spring Boot**, implement **CRUD APIs**, integrate with **MySQL** (relational DB), **Redis** (in-memory cache), and **MongoDB** (NoSQL DB), secure the application with **JWT-based authentication**, and apply best practices in testing, performance tuning, deployment, and monitoring. Each chapter provides hands-on instructions, code snippets, and explanations to ensure the application is scalable and maintainable.

**Tech Stack**: Spring Boot, Spring Data JPA (MySQL), Spring Data Redis, Spring Data MongoDB, Spring Security (JWT/OAuth2), JUnit 5, Docker/Kubernetes, ELK stack, Prometheus & Grafana.

Let's dive in!

## 1. Project Setup & Architecture

In this chapter, we’ll initialize the Spring Boot project and establish a sound architecture for our application. We will set up the project structure with clearly separated layers (controllers, services, repositories, etc.) and include all required dependencies.

### 1.1 Initialize the Spring Boot Project

1. **Use Spring Initializr**: Create a new Spring Boot project (for example, via [start.spring.io](https://start.spring.io)). Choose **Maven** (or Gradle) and Java 17+. Select the following **dependencies**:

   - **Spring Web** (for building RESTful APIs)
   - **Spring Data JPA** (to interact with MySQL)
   - **MySQL Driver** (JDBC driver for MySQL)
   - **Spring Data Redis** (for caching with Redis)
   - **Spring Data MongoDB** (to interact with MongoDB)
   - **Spring Security** (for authentication and authorization)
   - (Optional) **Spring Boot Actuator** (for monitoring)

   _(If "JSON Web Token" library is not available as a starter, we will add the JWT library manually later for token generation.)_

2. **Project Structure**: Use the standard Maven layout. Your directory structure should look like:

   ```plaintext
   src/main/java/com/example/yourapp
       ├── YourAppApplication.java  (Main class with @SpringBootApplication)
       ├── controller/             (REST controllers)
       ├── service/                (Service interfaces and implementations)
       ├── repository/             (Data access interfaces for JPA/Mongo)
       ├── model/                  (Entity and domain model classes)
       ├── exception/             (Custom exceptions and handlers)
       └── config/                 (Configuration classes e.g. security, caching)
   src/main/resources
       ├── application.properties (or .yml configuration)
       └── ... (other resources)
   ```

   This layered organization separates concerns: **Controllers** handle HTTP requests, **Services** contain business logic, and **Repositories** handle database operations ([Spring Boot folder structure best practices](https://symflower.com/en/company/blog/2024/spring-boot-folder-structure/#:~:text=,reside%20in%20the%20%E2%80%9CRepositories%E2%80%9D%20folder)). This clear separation makes the project easier to navigate and maintain, and also allows Spring to automatically detect components by their annotations (e.g. `@RestController`, `@Service`, `@Repository`) ([Spring Boot folder structure best practices](https://symflower.com/en/company/blog/2024/spring-boot-folder-structure/#:~:text=persistence,%E2%80%9CRepositories%E2%80%9D%20folder)).

3. **Main Application Class**: In `YourAppApplication.java`, annotate with `@SpringBootApplication`. This enables component scanning for the current package and subpackages, auto-configures Spring Boot based on dependencies, and marks this as the entry point. For example:

   ```java
   @SpringBootApplication
   public class YourAppApplication {
       public static void main(String[] args) {
           SpringApplication.run(YourAppApplication.class, args);
       }
   }
   ```

4. **Add Required Properties**: Open `src/main/resources/application.properties` (or `application.yml`) and add configuration placeholders:

   ```properties
   # MySQL configuration
   spring.datasource.url=jdbc:mysql://localhost:3306/yourapp_db
   spring.datasource.username=root
   spring.datasource.password=yourpassword
   spring.jpa.hibernate.ddl-auto=update
   spring.jpa.show-sql=true

   # MongoDB configuration
   spring.data.mongodb.uri=mongodb://localhost:27017/yourapp_db

   # Redis configuration
   spring.redis.host=localhost
   spring.redis.port=6379

   # (We will add security-related properties and others in later sections)
   ```

   - The above assumes local databases. In production, you’d use environment variables or external config for sensitive details.
   - `ddl-auto=update` is convenient for dev (auto-creates tables); for production, use a migration tool instead.
   - We enabled `show-sql` for JPA to log SQL statements (useful in debugging SQL and performance).

5. **Package Management**: Ensure your `pom.xml` has the necessary dependencies (Spring Boot starters for web, JPA, Security, etc.). Spring Boot will transitively include things like Tomcat (embedded server) and HikariCP (connection pool for MySQL). (By default, Spring Boot 2+ uses **HikariCP** for JDBC connection pooling, due to its high performance ([Configuring Hikari Connection Pool with Spring Boot](https://javadevjournal.com/spring-boot/spring-boot-hikari/#:~:text=Configuring%20Hikari%20Connection%20Pool%20with,implementation%20in%20Spring%20Boot%202)).)

With the project skeleton in place and dependencies added, we can proceed to implement features in a structured way.

### 1.2 Layered Architecture Overview

Our application will follow a **layered architecture**:

- **Model Layer**: Contains entities (for JPA) and domain models. For example, we’ll create a `Product` entity for MySQL, and maybe a `ProductDocument` for MongoDB.
- **Repository Layer**: Interfaces for data access (e.g., `ProductRepository extends JpaRepository` for MySQL, and a `MongoProductRepository extends MongoRepository` for MongoDB). Spring Data JPA and Mongo will provide implementation at runtime. Using Spring Data repositories allows us to perform CRUD without boilerplate SQL code ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=Explanation%3A)) ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb#:~:text=,create%2C%20read%2C%20update%2C%20and%20delete)).
- **Service Layer**: Defines business logic operations and coordinates between repositories and other components. We might have `ProductService` interface with methods like `createProduct, updateProduct, findProductById, ...`. The service implementation will use repositories and also handle things like caching and custom exceptions. (The service layer is where we enforce business rules and handle conditions such as "product not found" by throwing exceptions ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=,Todo%20item%20does%20not%20exist)).)
- **Controller Layer**: REST controllers expose endpoints (e.g., `/api/products`) and map HTTP requests to service calls. They handle request/response transformation (JSON to objects and vice versa) and input validation.
- **Configuration & Others**: Classes for cross-cutting concerns such as security config, caching config, global exception handlers (`@ControllerAdvice`), etc.

This architecture ensures **separation of concerns** and makes the app easier to test and maintain. For instance, we can test the service layer independently by mocking the repository layer.

Now that the foundation is ready, let's implement the core functionalities.

## 2. CRUD API Implementation

In this chapter, we will develop RESTful endpoints for a sample domain object (we'll use **Product** as an example). We will implement create, read, update, delete (CRUD) operations, along with input validation and exception handling for not-found cases. This will showcase how to build APIs using Spring Web and Spring Data JPA.

_(For simplicity, assume "Product" has fields like `id, name, description, price, quantity`. You can choose a domain relevant to your needs – the steps remain similar.)_

### 2.1 Define the JPA Entity and Repository (MySQL)

First, create the JPA entity to represent the Product in the MySQL database, and the repository interface to perform CRUD operations on it.

- **Entity Class**: In the `model` package, create `Product.java`:

  ```java
  package com.example.yourapp.model;

  import javax.persistence.*;

  @Entity
  @Table(name = "products")
  public class Product {
      @Id
      @GeneratedValue(strategy = GenerationType.IDENTITY)
      private Long id;

      @Column(nullable = false)
      private String name;

      private String description;

      private Double price;

      private Integer quantity;

      // Constructors, getters, setters omitted for brevity
  }
  ```

  Here:

  - `@Entity` and `@Table` map this class to a database table.
  - Fields are annotated with JPA annotations (`@Id`, `@GeneratedValue`, `@Column`) to define columns.
  - We enforce `name` as not null. We could also add Bean Validation annotations like `@NotBlank` on `name` to validate input (more on validation shortly).

- **Repository Interface**: In `repository` package, create `ProductRepository.java`:

  ```java
  package com.example.yourapp.repository;

  import com.example.yourapp.model.Product;
  import org.springframework.data.jpa.repository.JpaRepository;
  import org.springframework.stereotype.Repository;

  @Repository
  public interface ProductRepository extends JpaRepository<Product, Long> {
      // Additional query methods (if any) can be defined here
      // e.g., List<Product> findByNameContaining(String name);
  }
  ```

  By extending `JpaRepository<Product, Long>`, we inherit standard CRUD methods (`findAll`, `findById`, `save`, `deleteById`, etc.) without writing SQL or implementations ourselves ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=Explanation%3A)). Spring will treat this interface as a bean because of `@Repository` and create a proxy instance at runtime.

### 2.2 Service Layer Implementation

Create a service to encapsulate business logic for products. It will use the repository and also handle scenarios like "product not found".

- **Service Interface**: `ProductService.java` in `service` package:

  ```java
  public interface ProductService {
      List<Product> getAllProducts();
      Product getProductById(Long id);
      Product createProduct(Product product);
      Product updateProduct(Long id, Product product);
      void deleteProduct(Long id);
  }
  ```

- **Service Implementation**: `ProductServiceImpl.java` in `service` (or a subpackage, e.g., `service.impl`):

  ```java
  import org.springframework.stereotype.Service;
  import org.springframework.beans.factory.annotation.Autowired;
  import java.util.List;

  @Service
  public class ProductServiceImpl implements ProductService {

      @Autowired
      private ProductRepository productRepository;

      @Override
      public List<Product> getAllProducts() {
          return productRepository.findAll();  // fetch all products
      }

      @Override
      public Product getProductById(Long id) {
          return productRepository.findById(id)
              .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
      }

      @Override
      public Product createProduct(Product product) {
          // Additional business rules can be applied here
          return productRepository.save(product);
      }

      @Override
      public Product updateProduct(Long id, Product productDetails) {
          Product existing = productRepository.findById(id)
              .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
          // Update fields
          existing.setName(productDetails.getName());
          existing.setDescription(productDetails.getDescription());
          existing.setPrice(productDetails.getPrice());
          existing.setQuantity(productDetails.getQuantity());
          return productRepository.save(existing);
      }

      @Override
      public void deleteProduct(Long id) {
          Product existing = productRepository.findById(id)
              .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
          productRepository.delete(existing);
      }
  }
  ```

  Key points:

  - The service calls `productRepository` methods to interact with the DB.
  - If an entity is not found for a given id, we throw a custom `ResourceNotFoundException` (we will define this next). Throwing an exception here is a way to handle errors at the service layer, so the controller can catch it or a global handler can produce a proper HTTP 404 response ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=public%20Optional,%2B%20id%29%29%3B)) ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=%40Override%20public%20void%20deleteTodoById,)).
  - The `@Service` annotation makes this class a Spring bean. We use constructor injection or field injection (`@Autowired`) to get a `ProductRepository` instance.

### 2.3 Exception Handling and Validation

**Custom Exception**: Create `ResourceNotFoundException.java` in `exception` package:

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

This exception is annotated with `@ResponseStatus(HttpStatus.NOT_FOUND)` so that if it’s thrown in a controller, Spring will automatically respond with HTTP 404. It carries a message that we can return in the error response.

**Global Exception Handler** (optional but recommended for consistent error responses): Create `GlobalExceptionHandler.java` with `@RestControllerAdvice`:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleResourceNotFound(ResourceNotFoundException ex) {
        Map<String,Object> err = new HashMap<>();
        err.put("timestamp", LocalDateTime.now());
        err.put("message", ex.getMessage());
        err.put("status", HttpStatus.NOT_FOUND.value());
        return new ResponseEntity<>(err, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGeneralException(Exception ex) {
        Map<String,Object> err = new HashMap<>();
        err.put("timestamp", LocalDateTime.now());
        err.put("message", "An unexpected error occurred");
        err.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        return new ResponseEntity<>(err, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

This global handler will catch exceptions thrown by any controller:

- For `ResourceNotFoundException`, it returns a JSON with timestamp, error message, and 404 status.
- A fallback `Exception` handler returns 500 for any unhandled errors.  
  Using a **controller advice** like this centralizes error handling and ensures consistent structure in responses ([Spring Boot CRUD REST API Exception Handling with @RestControllerAdvice](https://www.javaguides.net/2024/09/spring-boot-crud-rest-api-exception-handling.html#:~:text=Explanation%3A)).

**Input Validation**: We should validate inputs to the API:

- Add Bean Validation annotations in the `Product` entity (or create separate DTO classes for requests). For instance, on `Product.name` you might have `@NotBlank`, on `price` maybe `@Min(0)`, etc.
- In controllers, use `@Valid` on method parameters to trigger validation. Spring will automatically throw `MethodArgumentNotValidException` if validation fails. We can handle this in the `GlobalExceptionHandler` too:
  ```java
  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, Object>> handleValidationException(MethodArgumentNotValidException ex) {
      Map<String, Object> errors = new HashMap<>();
      errors.put("timestamp", LocalDateTime.now());
      errors.put("status", HttpStatus.BAD_REQUEST.value());
      // collect field errors
      List<String> fieldErrors = ex.getBindingResult().getFieldErrors()
                                   .stream()
                                   .map(fe -> fe.getField() + ": " + fe.getDefaultMessage())
                                   .collect(Collectors.toList());
      errors.put("errors", fieldErrors);
      return new ResponseEntity<>(errors, HttpStatus.BAD_REQUEST);
  }
  ```
  This would produce a 400 response with details about which fields failed validation.

Now our service layer and exception handling are set. Next, we expose these operations via REST endpoints.

### 2.4 REST Controller Implementation

Create `ProductController.java` in the `controller` package:

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;
    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public List<Product> getAllProducts() {
        return productService.getAllProducts();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> getProductById(@PathVariable Long id) {
        Product prod = productService.getProductById(id);
        return ResponseEntity.ok(prod);
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@Valid @RequestBody Product product) {
        Product created = productService.createProduct(product);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id,
                                                @Valid @RequestBody Product product) {
        Product updated = productService.updateProduct(id, product);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }
}
```

**Explanation**:

- The controller is annotated with `@RestController` (which is a convenience for `@Controller + @ResponseBody`) and base request path `/api/products`.
- Each method corresponds to an API endpoint:
  - `GET /api/products` -> returns list of products.
  - `GET /api/products/{id}` -> returns single product or 404 if not found.
  - `POST /api/products` -> creates a new product. We use `@RequestBody` to bind JSON to a Product object, and `@Valid` to enforce our validation rules. A successful creation returns HTTP 201 (Created).
  - `PUT /api/products/{id}` -> updates an existing product.
  - `DELETE /api/products/{id}` -> deletes a product, returning 204 (No Content).
- We use `ResponseEntity` to have fine-grained control over status codes.
- The controller delegates to `productService`. If a product is not found, the service throws `ResourceNotFoundException`, which our global handler will convert to a 404 JSON error automatically.

At this point, we have a fully functional CRUD API for products. We can run the application (`mvn spring-boot:run` or from your IDE) and test these endpoints (using Postman or curl). For example:

```bash
# Create a product
curl -X POST -H "Content-Type: application/json" -d '{"name":"Laptop","price":1200.0}' http://localhost:8080/api/products

# Get all products
curl http://localhost:8080/api/products

# Get product by ID
curl http://localhost:8080/api/products/1

# Update a product
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Laptop Pro","price":1500.0}' http://localhost:8080/api/products/1

# Delete a product
curl -X DELETE http://localhost:8080/api/products/1
```

The CRUD foundation is ready. Next, we integrate databases and caching in more depth.

## 3. Database Integration

This chapter details integration with the specific data stores: **MySQL** as our primary relational database, **Redis** for caching, and **MongoDB** as a secondary NoSQL database. We will configure each, discuss schema design or data modeling considerations, and demonstrate interactions through Spring Data.

### 3.1 MySQL with Spring Data JPA

We have already set up the JPA entity `Product` and `ProductRepository` for MySQL in the CRUD implementation. Now, let's ensure MySQL is properly configured and discuss schema considerations.

- **Configuration**: In `application.properties`, we set the JDBC URL, username, and password for MySQL. Ensure that a MySQL server is running and an empty schema (database) named `yourapp_db` is created (you can change the name in the URL). The user should have privileges on that schema.

  - Example URL: `jdbc:mysql://localhost:3306/yourapp_db?useSSL=false&allowPublicKeyRetrieval=true`. The params disable SSL (for local dev) and allow retrieving public key if using caching SHA2 password (depending on MySQL version).
  - The `spring.jpa.hibernate.ddl-auto=update` will auto-create the `products` table based on our entity mapping. In production, it's safer to use `validate` or explicit migrations.

- **Schema Design**: Our `Product` table will have columns: id (PK), name, description, price, quantity. As an advanced consideration, ensure to add proper **indexes** on columns that will be used in queries (for example, if we frequently search products by name, add an index on name). With JPA and `@Column`, we can use `@Index` in the `@Table` annotation or manage it via the database directly.

- **Using Spring Data JPA**: Through `ProductRepository`, we can perform CRUD easily:

  - `productRepository.findAll()` -> returns all products (executes `SELECT * FROM products`).
  - `productRepository.findById(id)` -> returns Optional (executes `SELECT * FROM products WHERE id=?`).
  - `productRepository.save(product)` -> inserts or updates the product (`INSERT` or `UPDATE` based on if `id` is null or not).
  - `productRepository.delete(entity)` or `deleteById(id)` -> deletes the record.

  Spring Data JPA also allows defining **custom finder methods** by parsing method names. For example, if we add `List<Product> findByNameContaining(String name);` in `ProductRepository`, Spring will generate a query to find products where name LIKE %name%. These abstracted queries make data access convenient. As the Spring official docs say, repository interfaces come with many operations including standard CRUD out of the box ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb#:~:text=,create%2C%20read%2C%20update%2C%20and%20delete)).

- **Transaction Management**: By default, Spring Data JPA repository methods are transactional (Spring Boot will configure transaction managers). For our simple CRUD, the default is fine. If we need to manage transactions explicitly (for multiple operations in one unit), we could use `@Transactional` on service methods. Spring handles transactions via AOP proxies behind the scenes (an application of the Proxy pattern).

- **Lazy vs Eager Loading**: If our entity had relationships (e.g., a `Category` entity related to `Product`), JPA would load them lazily by default (i.e., only when accessed). For performance, it's often best to keep relationships lazy and fetch as needed. To avoid the N+1 query problem (multiple queries to fetch child entities), we can use **JOIN FETCH** queries or Spring Data’s `@EntityGraph` to fetch associations in one go. For example, one might define a JPA query with `fetch` join to load a product and its reviews in one query ([Boost the performance of your Spring Data JPA application](https://blog.ippon.tech/boost-the-performance-of-your-spring-data-jpa-application#:~:text=Method%201%3A%20Retrieving%20and%20loading,Query)). We don't have relationships in `Product` now, but it's a consideration for more complex schemas.

**Tip**: For managing database schema changes in a team or multiple environments, consider using a migration tool like **Flyway or Liquibase**. They integrate well with Spring Boot and allow version-controlled SQL scripts. This avoids reliance on `ddl-auto=update` in production (which may be unsafe).

### 3.2 Redis Integration (Caching Strategies)

**Why Redis?** Redis is an in-memory data store, often used as a cache to improve read performance. We will use Redis to cache frequently accessed data (for example, product details) so that repeated requests can be served quickly without hitting the MySQL database every time.

**Setup**:

- Add the dependency `spring-boot-starter-data-redis`. (If you used Spring Initializr with "Spring Data Redis", it's already in the pom.)
- Ensure a Redis server is running (default on port 6379).
- The `application.properties` should have Redis host/port configured (as shown earlier).

**Enable Caching**:

- In one of your configuration classes (or the main app class), add `@EnableCaching` to enable Spring's annotation-driven cache management. For example:
  ```java
  @SpringBootApplication
  @EnableCaching
  public class YourAppApplication { ... }
  ```
  This tells Spring to look for cache annotations like `@Cacheable`, `@CacheEvict`, etc.

**Using @Cacheable**:

- We decide which service methods to cache. A good candidate is the "get by ID" method, since product data changes infrequently but is read often.
- Modify `ProductServiceImpl.getProductById` to use caching:

  ```java
  @Override
  @Cacheable(value = "products", key = "#id")
  public Product getProductById(Long id) {
      return productRepository.findById(id)
          .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
  }
  ```

  The `@Cacheable` annotation will cause Spring to check the "products" cache for the given `id` first. If present, it returns the cached Product, skipping the repository call. If not, it will fetch from DB and then store the result in cache with key `id`. In our example, the cache name is "products". You can have multiple caches for different data (and configure their TTL, etc., in Redis if needed).

- **Cache Behavior**: After adding the above, if you call `getProductById(2)` twice in a row, the second call will be served from cache. For example, as a DigitalOcean tutorial illustrates, if a user with a certain ID is cached, subsequent requests return from cache, reducing database hits ([Spring Boot Redis Cache | DigitalOcean](https://www.digitalocean.com/community/tutorials/spring-boot-redis-cache#:~:text=In%20the%20above%20mapping%2C%20,are%20the%20calls%20we%20made)) ([Spring Boot Redis Cache | DigitalOcean](https://www.digitalocean.com/community/tutorials/spring-boot-redis-cache#:~:text=Notice%20something%3F%20We%20made%20four,call%20was%20made%20for%20this)).

**Cache Invalidation**:

- When data changes, the cache must be updated or cleared to avoid stale data:

  - Use `@CachePut` on update methods to update the cache entry for a key when you update the DB.
  - Use `@CacheEvict` on delete methods to remove an entry from cache upon deletion.

  For instance, on `updateProduct` you might add:

  ```java
  @Override
  @CachePut(value = "products", key = "#id")
  public Product updateProduct(Long id, Product productDetails) { ... }
  ```

  and on `deleteProduct`:

  ```java
  @Override
  @CacheEvict(value = "products", key = "#id")
  public void deleteProduct(Long id) { ... }
  ```

  Alternatively, you can evict all entries with `allEntries=true` if needed (e.g., evict entire "products" cache if a big change happens) ([Spring Boot Redis Cache | DigitalOcean](https://www.digitalocean.com/community/tutorials/spring-boot-redis-cache#:~:text=If%20some%20data%20is%20to,annotation)).

- **TTL (Time to Live)**: By default, Spring Cache with Redis will persist entries until evicted. You can configure expiration at the Redis cache level or programmatically. For example, you might configure a TTL of, say, 10 minutes for the "products" cache if eventual staleness is acceptable. Spring Data Redis allows setting TTL via Redis configuration or using `@Cacheable` conditionals (`unless` attribute).

**Testing the Cache**:

- Start the app, call a GET product endpoint twice and observe logs. The first call will log a DB query (due to `findById`), the second might not (if served from cache). This confirms caching is working ([Spring Boot Redis Cache | DigitalOcean](https://www.digitalocean.com/community/tutorials/spring-boot-redis-cache#:~:text=,Getting%20user%20with%20ID%202)).

Using Redis caching can significantly improve performance for read-heavy endpoints, as we've effectively eliminated repetitive database calls when data hasn't changed. We'll discuss more performance optimization in Section 6.

### 3.3 MongoDB Integration (NoSQL Database)

Now let's integrate **MongoDB** into our application. We will use it to handle some data that is better suited for a NoSQL store. For example, if we want to store **product reviews** or **logs** which can be large in number and don't require complex relational joins, MongoDB is a good choice. We'll demonstrate storing and retrieving data from MongoDB using Spring Data Mongo.

**Setup**:

- The dependency `spring-boot-starter-data-mongodb` is in our pom (if not, add it).
- Ensure a MongoDB instance is running (default on mongodb://localhost:27017).
- In `application.properties`, we've set `spring.data.mongodb.uri`. (Alternatively, you can set `spring.data.mongodb.host, port, database` separately.)

**Define a Mongo Document**:

- In `model` package (or a subpackage for Mongo documents), create a class for the data you want to store in Mongo. Let's say we create `ProductReview.java`:

  ```java
  import org.springframework.data.annotation.Id;
  import org.springframework.data.mongodb.core.mapping.Document;
  import java.time.LocalDateTime;

  @Document(collection = "product_reviews")
  public class ProductReview {
      @Id
      private String id;  // MongoDB uses String or ObjectId for IDs

      private Long productId;       // reference to Product (relational ID)
      private String reviewText;
      private String reviewerName;
      private LocalDateTime createdAt = LocalDateTime.now();
      // getters, setters, constructors...
  }
  ```

  This marks `ProductReview` as a Mongo document stored in the `product_reviews` collection. The `productId` can link the review to a Product by ID (though this is just by convention, not a foreign key constraint as in SQL).

**Mongo Repository**:

- In `repository` package (or under a `repository.mongo` package), create `ProductReviewRepository.java`:

  ```java
  import org.springframework.data.mongodb.repository.MongoRepository;
  import java.util.List;

  public interface ProductReviewRepository extends MongoRepository<ProductReview, String> {
      List<ProductReview> findByProductId(Long productId);
  }
  ```

  This repository provides CRUD for `ProductReview`. It also has a custom finder `findByProductId` to get all reviews for a given product. Spring Data Mongo will implement this method by deriving a query on the `productId` field.

**Multiple Data Sources Consideration**: We now have both JPA repositories and Mongo repositories. Spring Boot will auto-configure both a JPA EntityManager and a MongoTemplate. Usually, you can keep them in the same app without issue. However, if there is any ambiguity, you can use `@EnableJpaRepositories` and `@EnableMongoRepositories` on separate configuration classes to explicitly tell Spring where to scan JPA vs Mongo repositories. For example, you might put Mongo repos in a different package and enable scanning on that base package. (Spring Data Mongo by default scans the main package for interfaces extending `MongoRepository`.) If needed, you can specify a different base package for each to avoid overlap ([Getting Started | Accessing Data with MongoDB](https://spring.io/guides/gs/accessing-data-mongodb#:~:text=interfaces%20that%20extend%20one%20of,does%20not%20find%20your%20repositories)).

**Using MongoRepository**:

- Let's create a service for reviews or just use the repository directly in a controller for brevity:

  ```java
  @RestController
  @RequestMapping("/api/products/{productId}/reviews")
  public class ProductReviewController {

      private final ProductReviewRepository reviewRepo;
      public ProductReviewController(ProductReviewRepository reviewRepo) {
          this.reviewRepo = reviewRepo;
      }

      @GetMapping
      public List<ProductReview> getReviews(@PathVariable Long productId) {
          return reviewRepo.findByProductId(productId);
      }

      @PostMapping
      public ResponseEntity<ProductReview> addReview(@PathVariable Long productId,
                                                    @RequestBody ProductReview review) {
          review.setProductId(productId);
          ProductReview saved = reviewRepo.save(review);
          return ResponseEntity.status(HttpStatus.CREATED).body(saved);
      }
  }
  ```

  This demonstrates basic usage:

  - `findByProductId(productId)` will retrieve all reviews for a given product from Mongo (behind the scenes, a Mongo query `{ productId: productId }` is executed).
  - `save(review)` will insert a new document. (If `review.getId()` is non-null, it would update that document instead).

**Mongo Queries**:

- You can also use the powerful querying capabilities of Spring Data Mongo:
  - Define methods like `List<ProductReview> findByReviewerName(String name)`.
  - Use @Query annotation for more complex queries if needed (with MongoDB JSON query syntax or SpEL).
  - Aggregation framework for complex grouping if needed (beyond scope of this intro).

**Schema-less Nature**:

- Note that MongoDB is schema-less; it will store whatever fields the `ProductReview` object has. If you change the class (add/remove fields), old documents remain as they were (which can be both power and a responsibility to handle missing fields in code).

**Use Case**:

- In our app, we keep core product info in MySQL, and supplementary data (like reviews or maybe a **cache of product details** for quick text search) in Mongo. This kind of polyglot persistence leverages strengths of both DB types.

**Transactions across databases**:

- By default, a JPA transaction and Mongo operations are not tied together (they have separate transaction managers). If you perform an operation in MySQL and one in Mongo, and want them to both succeed or fail together, that is complex (you’d need distributed transactions or manual compensation). In practice, we often handle such cross-DB consistency at the application level or avoid strong consistency across radically different stores. For example, if adding a product and a first review at the same time, you might save product (SQL) and then save review (NoSQL). If the second fails, you might decide to retry or remove the product. It's an advanced pattern (saga, two-phase commit, etc.) beyond our scope here. For our purposes, we treat them separately.

We have now integrated MySQL, Redis, and MongoDB into our app:

- MySQL via JPA for primary data.
- Redis as a cache layer to boost performance.
- MongoDB for additional data storage demonstrating a NoSQL use.

Next, let's secure our application.

## 4. Security & Authentication

Security is crucial for any application. In this chapter, we implement **authentication** (issuing and validating JWTs for users) and **authorization** (role-based access control on endpoints). We will use Spring Security to secure the APIs and JSON Web Tokens for stateless auth. (We focus on JWT here; integrating OAuth2 providers would be similar in concept, but with different configuration.)

### 4.1 Adding Spring Security to the Project

With `spring-boot-starter-security` on the classpath, Spring Boot auto-configures basic security: by default it locks down all endpoints (requires authentication) and provides a default user/password (printed in console at startup). We will override this behavior.

**Password Encoder**: First, define a password encoder bean (for hashing passwords):

```java
@Configuration
public class SecurityBeanConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

We use **BCrypt** which is a secure hashing algorithm for passwords. It's a common practice to hash passwords for storage and to configure a `BCryptPasswordEncoder` in Spring apps ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=Enter%20fullscreen%20mode%20Exit%20fullscreen,mode)).

**User Details**: We need a way to load user information (username, password, roles) for authentication. There are a few approaches:

- In-memory users (for simplicity/testing).
- Database-backed users (using a User entity and Spring Data JPA).
- External identity provider (OAuth2/OpenID Connect) – out of scope here.

Let's create a simple `User` entity in MySQL and a `UserRepository`. (This could be similar to Product entity.)

```java
@Entity
@Table(name = "users")
public class User {
   @Id @GeneratedValue(strategy=IDENTITY) private Long id;
   private String username;
   private String password;  // stored as BCrypt hash
   private String roles;     // e.g. "ROLE_USER,ROLE_ADMIN"
   // getters, setters
}
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}
```

We will store roles as a comma-separated string for simplicity.

**UserDetailsService**: Spring Security uses a `UserDetailsService` to load a `UserDetails` (an interface with username, password, authorities) given a username. Implement one:

```java
@Service
public class MyUserDetailsService implements UserDetailsService {
    @Autowired
    private UserRepository userRepo;
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepo.findByUsername(username)
                  .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        // Convert our User to Spring Security's UserDetails
        List<GrantedAuthority> authorities = Arrays.stream(user.getRoles().split(","))
                                                   .map(SimpleGrantedAuthority::new)
                                                   .collect(Collectors.toList());
        return new org.springframework.security.core.userdetails.User(
                user.getUsername(), user.getPassword(), authorities);
    }
}
```

This service will be used to authenticate users from the database.

**JWT Utility**: We need a utility to generate and validate JWT tokens. We can use the popular JJWT library (io.jsonwebtoken) – add it to pom.xml if not already. For brevity, here's a sketch:

```java
@Component
public class JwtTokenUtil {
    private final String JWT_SECRET = "ReplaceThisWithASuperSecretKey";  // use env config in real apps
    private final long JWT_EXPIRATION_MS = 86400000; // 1 day

    public String generateToken(UserDetails userDetails) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + JWT_EXPIRATION_MS);
        return Jwts.builder()
                .setSubject(userDetails.getUsername())
                .claim("roles", userDetails.getAuthorities().stream()
                                           .map(GrantedAuthority::getAuthority).collect(Collectors.joining(",")))
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(SignatureAlgorithm.HS512, JWT_SECRET)
                .compact();
    }
    public String getUsernameFromToken(String token) {
        return Jwts.parser().setSigningKey(JWT_SECRET)
                   .parseClaimsJws(token).getBody().getSubject();
    }
    public boolean validateToken(String token, UserDetails userDetails) {
        String username = getUsernameFromToken(token);
        return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
    }
    private boolean isTokenExpired(String token) {
        Date exp = Jwts.parser().setSigningKey(JWT_SECRET)
                      .parseClaimsJws(token).getBody().getExpiration();
        return exp.before(new Date());
    }
}
```

This component signs tokens with a secret key (in real scenarios, keep this secret outside code and very safe!). It encodes username and roles in the token, and provides methods to validate and parse tokens.

**Authentication Controller**: Provide an endpoint for users to log in and obtain a JWT.

```java
@RestController
public class AuthController {
    @Autowired private AuthenticationManager authManager;
    @Autowired private MyUserDetailsService userDetailsService;
    @Autowired private JwtTokenUtil jwtTokenUtil;

    @PostMapping("/api/auth/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        // LoginRequest is a simple DTO with username & password fields.
        Authentication authentication = authManager.authenticate(
             new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword()));
        // If we reach here, authentication was successful
        UserDetails userDetails = userDetailsService.loadUserByUsername(request.getUsername());
        String jwt = jwtTokenUtil.generateToken(userDetails);
        return ResponseEntity.ok(Collections.singletonMap("token", jwt));
    }
}
```

We use Spring Security’s `AuthenticationManager` to authenticate. We need to configure it to use our `UserDetailsService` and `PasswordEncoder`.

**Security Configuration**: Create `SecurityConfig.java`:

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired private MyUserDetailsService userDetailsService;
    @Autowired private JwtTokenUtil jwtTokenUtil;
    @Autowired private PasswordEncoder passwordEncoder;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService).passwordEncoder(passwordEncoder);
    }

    @Bean @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // Define which endpoints are secured and which are open
        http.csrf().disable()  // disable CSRF for simplicity (enable in forms)
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // no sessions, use JWT
            .and().authorizeRequests()
            .antMatchers(HttpMethod.POST, "/api/auth/**").permitAll()  // allow login (and maybe sign-up) without auth
            .antMatchers(HttpMethod.GET, "/api/products/**").permitAll() // perhaps allow read-only product access to public
            .anyRequest().authenticated()  // everything else requires login
            .and().addFilterBefore(new JwtAuthenticationFilter(jwtTokenUtil, userDetailsService),
                                    UsernamePasswordAuthenticationFilter.class);
    }
}
```

Key points:

- We attach our `userDetailsService` and `passwordEncoder` to the auth manager so Spring knows how to verify credentials.
- We disable session creation (since JWT will be used for each request).
- We open some endpoints (like login, and maybe GET products for this example) to public, but secure others (e.g., create/update/delete product might require a role).
- We add our custom `JwtAuthenticationFilter` before the default username-password filter.

**JWT Filter**: This filter will run on each request to check for a JWT in the header and set the security context:

```java
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private JwtTokenUtil jwtTokenUtil;
    private MyUserDetailsService userDetailsService;
    public JwtAuthenticationFilter(JwtTokenUtil util, MyUserDetailsService uds) {
        this.jwtTokenUtil = util;
        this.userDetailsService = uds;
    }
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7);
            try {
                String username = jwtTokenUtil.getUsernameFromToken(token);
                if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    UserDetails userDetails = userDetailsService.loadUserByUsername(username);
                    if (jwtTokenUtil.validateToken(token, userDetails)) {
                        UsernamePasswordAuthenticationToken authToken =
                            new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                        authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                        // Set authentication to context
                        SecurityContextHolder.getContext().setAuthentication(authToken);
                    }
                }
            } catch (JwtException | IllegalArgumentException e) {
                // token parsing or validation failed
                logger.warn("JWT validation failed: " + e.getMessage());
            }
        }
        chain.doFilter(request, response);
    }
}
```

This filter:

- Checks the `Authorization` header for a Bearer token.
- If found, extracts the token, retrieves username from it, loads the user details, and if token is valid, it sets an authentication in the context so Spring knows the user is authenticated for this request.
- If token is missing or invalid, the filter just passes through (the request will be rejected by the `authorizeRequests` rules if it was required to be authenticated).

The above flow is an example of how JWT authentication is done in Spring Security:

1. **Login**: Client posts username/password, gets back a JWT.
2. **Subsequent Requests**: Client includes `Authorization: Bearer <token>` header. The filter verifies the token and sets the security context.
3. **Authorization**: Based on roles, we can restrict endpoints. For example, we could require admin role for creating products. We could do:
   ```java
   .antMatchers(HttpMethod.POST, "/api/products").hasRole("ADMIN")
   ```
   or use method-level security like `@PreAuthorize("hasRole('ADMIN')")` on controller methods after enabling `@EnableGlobalMethodSecurity(prePostEnabled=true)`.

This JWT setup is stateless – no session info on the server, which is good for scalability (any server instance can handle requests independently). It’s also quite secure if implemented correctly (make sure to use HTTPS in production so tokens are not intercepted, keep secret keys safe, etc.).

**Testing Security**:

- Without a token, try accessing a protected endpoint (e.g., DELETE product) – it should return 401 Unauthorized.
- Register a test user (either via database or create an endpoint for sign-up) with password encoded.
- Use the `/api/auth/login` to get a token.
- Use the token in subsequent requests (`Authorization: Bearer <token>`) and you should gain access to protected endpoints according to your role.

Spring Security can be tricky to configure, but our setup highlights the important parts (auth manager with custom user details, JWT filter, and configuring URL access rules) ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=,UserDetailsService)) ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=based%20on%20the%20username.%20,SecurityContextHolder)). We also used **BCrypt** to store passwords, which is a best practice for security ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=Enter%20fullscreen%20mode%20Exit%20fullscreen,mode)).

_(Optional: If we wanted to integrate OAuth2, Spring Security offers `spring-boot-starter-oauth2-client` and `spring-boot-starter-oauth2-resource-server`. We could configure an OAuth login with an external provider (like Google) and protect resources by validating JWTs issued by that provider. That would involve different configuration, but conceptually the resource server part is similar – verifying tokens and setting up roles.)_

### 4.2 Role-Based Access Control (RBAC)

We've included roles in our security. To implement RBAC:

- Decide roles (e.g., `ROLE_USER`, `ROLE_ADMIN`).
- Assign roles to users (our `User.roles` field).
- Protect endpoints accordingly. For example, in controllers:
  ```java
  @PreAuthorize("hasRole('ADMIN')")
  @DeleteMapping("/api/products/{id}")
  public ResponseEntity<Void> deleteProduct(@PathVariable Long id) { ... }
  ```
  This annotation (make sure global method security is enabled) will restrict access to admins. Alternatively, use `antMatchers` in security config as shown.

When a JWT is generated, we included roles in it (as a claim). We could retrieve that from the token instead of looking up the user again in `JwtAuthenticationFilter` (to optimize). The approach chosen here (loading from DB in filter) ensures we have fresh authorities (in case roles changed in DB). A more stateless approach is to trust the token fully and parse roles from it directly.

**Unauthorized Handling**:
We might want to handle what happens when an unauthenticated or unauthorized request comes in. Spring Security by default will send a 401 with a generic body. We can customize this by implementing `AuthenticationEntryPoint` to handle auth failures, and `AccessDeniedHandler` for logged-in but forbidden cases. For instance:

```java
@Component
public class JwtAuthEntryPoint implements AuthenticationEntryPoint {
    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response,
                         AuthenticationException authException) throws IOException {
        // This is invoked when user tries to access a secured endpoint without auth or with invalid token
        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized");
    }
}
```

And wire it in `http.exceptionHandling().authenticationEntryPoint(jwtAuthEntryPoint)` in `configure(HttpSecurity)`.

For brevity, we won't show full code, but it's mentioned that customizing unauthorized response is possible (returning 401 status with maybe a JSON message) ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=UnauthorizedEntryPoint%20UnauthorizedEntryPoint%20class%20is%20responsible,credentials%20to%20access%20the%20resource)) ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=%40Component%20public%20class%20UnauthorizedEntryPoint%20implements,AuthenticationEntryPoint%2C%20Serializable)).

At this stage, our application has security: clients must log in to get a token and then use that token to perform certain operations. We have protected critical endpoints from unauthorized use and established a basic RBAC.

## 5. Testing Strategies

Testing ensures our application works as expected and helps prevent regressions when code changes. We’ll cover **unit testing** (e.g., testing service logic in isolation) and **integration testing** (testing the API endpoints and database integration). We will use **JUnit 5** (Jupiter) along with Spring Boot’s test support and libraries like **Mockito** for mocking.

### 5.1 Unit Testing with JUnit and Mockito

**Scope**: Unit tests should focus on individual classes or layers. For example, test the `ProductService` logic without starting the whole Spring context or hitting the database. We can do this by mocking the `ProductRepository`.

- Add the dependency `spring-boot-starter-test` (it includes JUnit, Spring’s test framework, Mockito, etc.). This is usually added by default in a Spring Boot project (under test scope).

- Example: Test for `ProductServiceImpl`:

  ```java
  @ExtendWith(MockitoExtension.class)
  class ProductServiceTests {

      @Mock
      ProductRepository productRepository;

      @InjectMocks
      ProductServiceImpl productService;  // the service we are testing

      @Test
      void getProductById_existingId_returnsProduct() {
          Product prod = new Product();
          prod.setId(1L);
          prod.setName("TestProd");
          // define repository behavior
          Mockito.when(productRepository.findById(1L))
                 .thenReturn(Optional.of(prod));
          // call service
          Product result = productService.getProductById(1L);
          assertNotNull(result);
          assertEquals("TestProd", result.getName());
          // verify repository was called
          Mockito.verify(productRepository).findById(1L);
      }

      @Test
      void getProductById_nonExisting_throwsException() {
          Mockito.when(productRepository.findById(42L))
                 .thenReturn(Optional.empty());
          assertThrows(ResourceNotFoundException.class, () -> {
              productService.getProductById(42L);
          });
      }
  }
  ```

  Here we:

  - Use `@ExtendWith(MockitoExtension.class)` to enable Mockito.
  - Annotate `ProductRepository` with `@Mock` so it's a dummy that we can program with given responses.
  - `@InjectMocks` creates a `ProductServiceImpl` and injects the mock repository into it.
  - Test scenarios: when product exists, ensure correct object returned; when not, ensure exception.
  - We don't involve Spring context or real DB, making tests fast and focused.

We should also test other service methods (create, update, delete) similarly, including that they call the repository and handle conditions properly. These are pure Java tests.

**Testing Validation**: We can test that our validation annotations work by invoking the controller method with an invalid object, but that might require Spring's test framework. Alternatively, test the validation rules via a `Validator` manually on the object.

**Edge cases**: Write tests for edge conditions (null inputs, invalid values, etc.) to ensure our service or util methods handle them.

### 5.2 Integration Testing (Testing APIs and Repositories)

Integration tests involve starting (parts of) the Spring Boot application and actually invoking HTTP requests or repository calls, to see the whole system working together.

**Testing Repositories with an In-Memory DB**:

- We can use **H2** (an in-memory JDBC database) for tests to avoid requiring a real MySQL. Spring Boot can detect H2 on the classpath and use it if configured in tests.
- Alternatively, use **Testcontainers** to spin up a MySQL, Redis, and MongoDB in Docker for tests. This is more complex but gives you tests against the real DB engines. (It's advanced but very powerful for integration testing – you would annotate tests with `@Testcontainers` and use `@Container` to define e.g. a MySQL container, and override DB connection props for the test context.)

For demonstration, let's use H2 for JPA tests:

```java
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY) // Use embedded DB
class ProductRepositoryTests {
    @Autowired
    private ProductRepository productRepo;

    @Test
    void whenSaved_findByIdReturnsEntity() {
        Product p = new Product();
        p.setName("Phone");
        p.setPrice(500.0);
        Product saved = productRepo.save(p);
        assertNotNull(saved.getId());
        Optional<Product> found = productRepo.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("Phone", found.get().getName());
    }
}
```

This test uses `@SpringBootTest` to load the full application context (including an embedded Tomcat and all, unless we tell it not to). We restrict it to focus on JPA by just autowiring the repository. The `@AutoConfigureTestDatabase` with `Replace.ANY` will replace the real DataSource (MySQL) with an embedded data source if available (H2 needs to be on classpath).

**Testing Controllers (Web Layer)**:

- We can use `MockMvc` to perform HTTP requests to our controllers without actually running a server. Spring Boot can instantiate the web layer for test.
- Option 1: **Slice test** with `@WebMvcTest` – it will create the web layer beans (controllers, controllers advice, etc) but not the entire app (no DB). You can mock the service layer.
- Option 2: **Full context test** with `@SpringBootTest` + `@AutoConfigureMockMvc` – starts the whole context and allows MockMvc to call real endpoints.

For example, using slice approach for `ProductController`:

```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {
    @Autowired
    private MockMvc mockMvc;
    @MockBean
    private ProductService productService; // we mock the service

    @Test
    void getProductById_returnsProductJson() throws Exception {
        Product prod = new Product();
        prod.setId(100L); prod.setName("TestProd");
        Mockito.when(productService.getProductById(100L)).thenReturn(prod);
        mockMvc.perform(get("/api/products/100"))
               .andExpect(status().isOk())
               .andExpect(content().contentType("application/json"))
               .andExpect(jsonPath("$.id").value(100))
               .andExpect(jsonPath("$.name").value("TestProd"));
    }
}
```

We used `@WebMvcTest` which by default scans the specified controller and needed MVC components, and we provide a mock `ProductService` (with `@MockBean`, which places a mock in the Spring context for that bean). The test uses MockMvc to simulate an HTTP GET call and then checks the response status and JSON content using Spring’s JSONPath matchers.

In this test:

- The controller receives the request, calls the mocked service (which returns our fake product), and returns it as JSON. We verify the JSON contains the expected data.
- We did not start the full server; MockMvc calls the controller directly, which is fast.

We should also test other endpoints (POST, PUT, DELETE). For POST, we can send a JSON body with MockMvc `post` and verify a Created status and response JSON or headers.

**Testing Security**:

- We can include Spring Security context in tests. For unit tests of, say, a secured method, we can use `@WithMockUser` to simulate an authenticated user.
- For integration, we might test that protected endpoints return 401 when no token, and 200 when token is present. We could call our auth/login endpoint to get a token, then attach it to subsequent MockMvc requests (`header("Authorization", "Bearer ...")`).

**Integration Test Example (full context)**:

```java
@SpringBootTest
@AutoConfigureMockMvc
class ProductApiIntegrationTest {
    @Autowired MockMvc mockMvc;
    @Autowired UserRepository userRepo;
    @Autowired PasswordEncoder passwordEncoder;

    private String token;
    @BeforeEach
    void setupUser() throws Exception {
        // create a test user in H2 (with role USER)
        User u = new User();
        u.setUsername("testuser");
        u.setPassword(passwordEncoder.encode("testpass"));
        u.setRoles("ROLE_USER");
        userRepo.save(u);
        // obtain JWT token via login endpoint
        String loginJson = "{\"username\":\"testuser\",\"password\":\"testpass\"}";
        MvcResult result = mockMvc.perform(post("/api/auth/login")
                                  .contentType("application/json").content(loginJson))
                         .andExpect(status().isOk())
                         .andReturn();
        String responseBody = result.getResponse().getContentAsString();
        // parse JSON to get token value (could use JsonPath or Jackson)
        token = // ... parse from responseBody ... ;
    }

    @Test
    void createAndGetProduct_withAuth_success() throws Exception {
        String newProdJson = "{\"name\":\"Camera\",\"price\":299.99}";
        // Create product (should be allowed for ROLE_USER if we permitted in security, otherwise assign ROLE_ADMIN and adjust)
        MvcResult createRes = mockMvc.perform(post("/api/products").header("Authorization", "Bearer " + token)
                                .contentType("application/json").content(newProdJson))
                            .andExpect(status().isCreated())
                            .andReturn();
        String prodResponse = createRes.getResponse().getContentAsString();
        // parse created product ID from prodResponse (or return location header)
        // Then GET the product
        mockMvc.perform(get("/api/products/1").header("Authorization", "Bearer " + token))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.name").value("Camera"));
    }
}
```

This end-to-end test:

- Sets up a user and logs in to get a JWT.
- Uses that JWT to create a product and then retrieve it.
- We used the actual running app components (with H2 as DB, etc.).

Such tests are slower but verify that the app works as a whole (from HTTP to DB).

**Summary**: We should maintain a healthy balance of unit tests (fast, pinpointing logic errors) and integration tests (slower, but ensuring components work together). Spring Boot’s testing slices (like `@WebMvcTest`, `@DataJpaTest`) are useful to test one layer at a time in isolation ([Getting Started | Testing the Web Layer](https://spring.io/guides/gs/testing-web#:~:text=We%20use%20,Mockito)). For example:

- `@DataJpaTest` will start H2 and scan JPA entities/repos only, good for repository tests.
- `@WebMvcTest` as shown for controller with mocked dependencies.
- `@SpringBootTest` for full integration when needed.

Automating these tests (via Maven or CI pipeline) ensures we catch issues early. Aim for meaningful coverage, especially on core business logic and critical integrations.

## 6. Performance Optimization

As applications grow, performance becomes critical. We'll discuss strategies to optimize performance in our Spring Boot app:

- Efficient database access (avoiding common pitfalls in JPA).
- Utilizing connection pooling and tuning.
- Caching (we already implemented Redis caching).
- Asynchronous processing where applicable.
- Profiling and monitoring to find bottlenecks.

### 6.1 Optimize Database Queries and JPA Usage

**Query Efficiency**:

- Analyze the SQL queries being run (since we set `show-sql=true`, we can see them in logs, or use a profiler). Ensure queries use indexes properly. If you find slow queries, consider adding **indexes** in the database on the columns involved in `WHERE` clauses.
- Avoid pulling more data than needed. For example, if you have an endpoint just to list product names, don't fetch entire Product entities. You can use Spring Data JPA **projections** or write a custom JPQL to fetch only required fields.
- Use pagination for endpoints returning large data sets (Spring Data JPA provides paging with `Pageable`).

**N+1 Query Problem**:

- If you have relationships, fetching child entities lazily in a loop can kill performance. Use `fetch join` queries or `@EntityGraph` to fetch related data in one query when needed. For example, to fetch a Product and its Reviews in one go, define in `ProductRepository`:
  ```java
  @Query("SELECT p FROM Product p JOIN FETCH p.reviews WHERE p.id = :id")
  Product findProductWithReviews(@Param("id") Long id);
  ```
  This JPQL uses `JOIN FETCH` so that reviews are loaded together with product ([Boost the performance of your Spring Data JPA application](https://blog.ippon.tech/boost-the-performance-of-your-spring-data-jpa-application#:~:text=%40Repository%20public%20interface%20ArticleRepository%20extends,Long%20id%29%3B)). Alternatively, if using Spring Data, you could annotate a method with `@EntityGraph(attributePaths = "reviews")` ([Boost the performance of your Spring Data JPA application](https://blog.ippon.tech/boost-the-performance-of-your-spring-data-jpa-application#:~:text=Since%20version%201,with%20the%20entity%20when%20requested)). These techniques reduce multiple SQL selects into one.

**Batch Operations**:

- If inserting/updating in bulk, consider JPA’s batching capabilities or use JDBC directly for batch updates. (E.g., if you had to import 1000 products at once, doing one `save` at a time is slow; instead, use `saveAll` or a batch insert.)

**Hibernate Second-Level Cache**:

- We used Redis as an app-level cache. Hibernate also has a second-level cache mechanism that can cache entities across sessions. This can be configured with providers like EhCache, but given we have Redis, our approach is fine and more explicit.

### 6.2 Connection Pooling and Database Settings

Spring Boot (with HikariCP) handles a lot for us, but we should ensure the pool is tuned for our workload:

- The default HikariCP pool size is 10 connections. For a high-throughput app, you might increase it (via `spring.datasource.hikari.maximumPoolSize`) depending on your DB server's capability.
- Monitor pool usage in production (HikariCP exposes metrics if using micrometer).
- Ensure proper **timeouts**: Hikari has connection timeout, idle timeout settings. We don't want threads waiting forever for a connection if DB is unresponsive; tune these to fail fast or retry logic as needed.

On the MySQL side:

- Adjust MySQL config if necessary (e.g., max_connections, query cache (if using older MySQL versions), etc).
- Use read replicas for scaling reads if needed (Spring can route reads vs writes if configured or you handle it at service layer).
- Consider using stored procedures or native queries for performance-critical sections (rarely needed if JPA is tuned well, but an option).

### 6.3 Caching Strategies Recap

We implemented Redis caching for product lookups. Some best practices in caching:

- Identify **hot data** (frequently read, infrequently changed) to cache. Products catalog is a good example. Other examples: config data, reference data lists, etc.
- Keep cache updated on writes (we did with CachePut/CacheEvict).
- Consider cache **invalidation policies**: we set it to evict on changes. In some cases, might use a TTL to auto-expire entries to eventually sync with DB updates.
- Use cache metrics (Redis `INFO` stats or Spring Boot metrics) to monitor hit/miss ratio and adjust strategy if needed.

Be mindful not to cache excessively (don't cache very volatile data or extremely large data sets unnecessarily).

### 6.4 Asynchronous and Parallel Processing

Spring Boot allows methods to run asynchronously (using `@Async` and a TaskExecutor bean) which can improve throughput for tasks that can be done in parallel or outside the request-response cycle. For example:

- Sending an email or notification after a purchase can be done asynchronously so the API responds faster.
- If you had to call an external API for each product and aggregate results, you could do those calls in parallel threads.

Ensure to configure appropriate thread pools for async tasks (Spring Boot creates a default SimpleAsyncTaskExecutor which is not bounded – better to define a ThreadPoolTaskExecutor with a pool size).

### 6.5 Monitoring and Profiling for Performance

You can't optimize what you don't measure. Use monitoring tools (which we cover in the next section) to gather performance data:

- Spring Boot Actuator metrics (e.g., throughput, response times).
- Java profilers or APM (Application Performance Management) tools can profile CPU and memory usage to find bottlenecks.
- Database slow query log: enable MySQL's slow query log to catch queries that exceed a threshold.

For code-level optimization:

- Avoid unnecessary object creation in tight loops (Java level micro-optimizations).
- Use efficient algorithms or data structures if doing in-memory processing.
- In high-concurrency scenarios, watch out for synchronization locks that can reduce throughput.

In summary, to optimize performance:

- **Efficient DB queries** (use JPA wisely, add indexes, minimize round-trips).
- **Connection pooling** (tune sizes, use a fast pool like HikariCP which Spring provides by default ([Power of HikariCP in Spring Boot: The Complete Guide - GoPenAI](https://blog.gopenai.com/power-of-hikaricp-in-spring-boot-the-complete-guide-5200264599fc#:~:text=HikariCP%20became%20the%20default%20choice,Tomcat%20Connection%20Pool%20in))).
- **Caching** (use Redis or others to avoid repetitive work).
- **Concurrent processing** (async tasks for non-critical path work).
- **Monitor and iterate**: profile the app under load, identify slow parts, and address them.

Our app, with its caching and optimized DB access, should handle a decent load. Next, we will see how to deploy and monitor it in a production environment.

## 7. Deployment & Infrastructure

Deploying a Spring Boot application can be done on various environments: containerized with Docker, orchestrated with Kubernetes, or on cloud platforms (AWS, GCP, etc.). In this chapter, we'll outline containerization, Kubernetes deployment, and considerations for cloud infrastructure.

### 7.1 Docker Containerization

**Why Docker?** It provides a consistent environment for running the app across different machines and simplifies dependency management (Java, libraries, etc. are all bundled in the image).

**Dockerfile**: Create a `Dockerfile` at the project root:

```Dockerfile
# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set a working directory
WORKDIR /app

# Copy the jar file (assuming jar name is yourapp.jar)
COPY target/yourapp.jar app.jar

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Run the jar file
ENTRYPOINT ["java","-jar","app.jar"]
```

Build the jar (e.g., `mvn clean package`) so that `target/yourapp.jar` exists, then build the Docker image:

```
docker build -t yourapp:1.0 .
```

This Dockerfile is minimal: it uses a lightweight Alpine Linux with Java and simply copies the fat jar into the container and runs it. It's often all you need to run a Spring Boot app in Docker ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=This%20Dockerfile%20is%20very%20simple%2C,which%20is%20run%20in%20the)). We exposed port 8080 so it can be mapped by Docker.

You can run the container with:

```
docker run -p 8080:8080 --env SPRING_DATASOURCE_URL=... (and other env vars) yourapp:1.0
```

We can pass configuration via environment variables. Spring Boot will map env vars to `application.properties` keys if named appropriately (e.g., `SPRING_DATASOURCE_URL` for `spring.datasource.url`). This is useful for providing DB credentials at runtime.

**Docker Compose**: To run app with MySQL, Redis, Mongo all together, create a `docker-compose.yml`:

```yaml
version: "3"
services:
  app:
    image: yourapp:1.0
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/yourapp_db
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: example
      SPRING_REDIS_HOST: cache
      SPRING_DATA_MONGODB_URI: mongodb://mongo:27017/yourapp_db
    depends_on:
      - db
      - cache
      - mongo
  db:
    image: mysql:8
    environment:
      MYSQL_DATABASE: yourapp_db
      MYSQL_ROOT_PASSWORD: example
    ports:
      - "3306:3306"
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  mongo:
    image: mongo:5
    ports:
      - "27017:27017"
```

This composition sets up:

- MySQL (with a database and root password),
- Redis,
- MongoDB,
- and our app container linking to those. The app's environment variables point to the other containers by service name (`db`, `cache`, `mongo`). Docker’s network allows them to resolve hostnames.

By running `docker-compose up`, all services start. This is great for local development or dev/test environments to emulate the infrastructure.

### 7.2 Kubernetes Deployment

For production or larger-scale, you might use Kubernetes. We won't go deep, but let's outline how to deploy our app to K8s:

**Docker Image**: Ensure the image (built above) is pushed to a registry accessible by the cluster (e.g., Docker Hub, AWS ECR, GCP Container Registry).

**K8s Manifests**:

- **Deployment**: Manages replica pods of our application.
- **Service**: Exposes the pods internally or externally.
- **ConfigMap/Secret**: Store configuration (DB URLs, passwords) outside the container.

Example `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yourapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: yourapp
  template:
    metadata:
      labels:
        app: yourapp
    spec:
      containers:
        - name: yourapp
          image: yourrepo/yourapp:1.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              value: "jdbc:mysql://<mysql-service>:3306/yourapp_db"
            - name: SPRING_DATASOURCE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: yourapp-secret
                  key: db_user
            - name: SPRING_DATASOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: yourapp-secret
                  key: db_password
            - name: SPRING_REDIS_HOST
              value: "<redis-service>"
            - name: SPRING_DATA_MONGODB_URI
              value: "mongodb://<mongo-service>:27017/yourapp_db"
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: yourapp-secret
                  key: jwt_secret
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 30
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 60
```

This describes 3 replicas of our app. We use environment variables for config (pulling sensitive ones from a `Secret`). We also define health probes; Kubernetes will hit `/actuator/health` to ensure the app is up (the Actuator health endpoint is useful here). We configured readiness and liveness:

- **Readiness**: when pods start, we wait 15s then check health every 30s. Only mark pod ready if health is UP (meaning it's connected to DB, etc.). This ensures traffic isn't sent to a pod that's not ready.
- **Liveness**: checks periodically to restart the container if it becomes unresponsive.

We would also have YAML for MySQL, Redis, Mongo in K8s (or use managed services).

- MySQL could be a K8s deployment or (better in cloud) an RDS/Aurora instance (AWS) or Cloud SQL (GCP).
- Redis similarly could be Elasticache (AWS) or MemoryStore (GCP) or a pod.
- Alternatively, use K8s Operators for these databases or Helm charts to deploy them.

**Service & Ingress**:
To expose the app, define a Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: yourapp-service
spec:
  selector:
    app: yourapp
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

This maps port 80 of a cloud load balancer to our pods' 8080. Or use an Ingress controller for advanced routing.

Kubernetes allows easy scaling (`kubectl scale deployment yourapp-deployment --replicas=5`) and rolling updates of new versions. It also handles self-healing (via liveness probes) and service discovery (our env pointed to `<mysql-service>` etc., which would be defined as Services for those DBs).

### 7.3 Cloud Deployment Considerations

If not using Kubernetes, Spring Boot can also be deployed:

- **AWS EC2 or AWS Elastic Beanstalk**: Package the jar and deploy, or use Beanstalk with Docker to deploy the container. Elastic Beanstalk can take a Docker Compose as well.
- **AWS ECS** (Elastic Container Service): run the Docker container in a cluster (similar to Kubernetes but AWS-managed).
- **Google Cloud Run** or **AWS Lambda** (with Custom Runtime): You can run containers serverlessly. Spring Boot can run on Cloud Run easily with the Docker image; it will scale down to 0 on no traffic, up on demand.
- **Heroku**: Supports deploying Spring Boot via git, and will handle running it (just need a Procfile).
- **Azure Web Apps**: Also support Java jars or containers.

**Configuration**: In any cloud, externalize config (like we used env vars or a config server). Do not bake secrets into the image. Use Vault or cloud secret managers for sensitive config.

**Logging**: Ensure logs go to STDOUT/STDERR (Spring Boot by default logs to console). In Docker/K8s, that will capture logs which can be aggregated (e.g., via CloudWatch Logs on AWS or Stackdriver on GCP).

**Scaling**: Vertical (bigger instance) or horizontal (more instances/pods). With stateless design (using JWT and no in-memory session), horizontal scaling is straightforward.

**Monitoring on Cloud**: Use cloud monitoring services or integrate with Prometheus/Grafana as we'll discuss next.

In summary, containerization combined with orchestration (like Kubernetes) is a powerful way to deploy Spring Boot apps. It provides consistency and scalability. We created a basic Docker image ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=This%20Dockerfile%20is%20very%20simple%2C,which%20is%20run%20in%20the)) and showed how it might run in a cluster. The specifics will vary by choice of infrastructure, but the key is to ensure the app can be configured externally and is stateless for easy scaling.

## 8. Logging & Monitoring

Operating an application in production requires good logging and monitoring. Logging provides insight into what the application is doing, and monitoring provides metrics and alerting for system health. Here, we discuss integrating with the **ELK stack** for centralized logging and using **Prometheus & Grafana** for monitoring metrics.

### 8.1 Logging and ELK Stack Integration

**Application Logging**:

- Use a logging framework (Spring Boot uses Logback by default). We can configure log format in `application.properties` or logback.xml. For instance, use a JSON encoder for logs if shipping to ELK (makes parsing easier).
- Log at appropriate levels: INFO for high-level app flow, DEBUG for detailed info (disabled in prod), ERROR for exceptions.
- Include context in logs (e.g., user ID, request ID). Spring Boot’s `WebMvc` can log a request ID if you propagate one, or use Sleuth to tag logs with trace IDs.

**ELK Stack**:

- **Elasticsearch**: stores log data and allows search.
- **Logstash**: pipeline tool to transform and ship logs to Elasticsearch.
- **Kibana**: UI to search and visualize logs.

For a Spring Boot app, a common approach:

- The app writes logs to console (STDOUT) or a file.
- Use **Filebeat** (a lightweight log shipper agent) on the host to tail the log file (or STDOUT) and forward to Logstash/Elasticsearch ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20is%20considered%20one%20of,the%20part%20performed%20by%20Logstash)) ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20can%20either%20ship%20data,Elasticsearch%20or%20first%20to%20Logstash)).
- Alternatively, skip Logstash and send directly to Elasticsearch using Filebeat (less processing, but limited transformation).

**Filebeat vs Logstash**:
Filebeat is efficient for shipping logs but not for heavy processing. Logstash can parse and transform logs (e.g., convert them to JSON, add fields, etc.) ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20is%20considered%20one%20of,the%20part%20performed%20by%20Logstash)). In many modern setups, if logs are already in JSON, Filebeat -> Elasticsearch is enough.

**Steps**:

1. **Format logs in JSON**: e.g., in logback.xml:

   ```xml
   <appender name="stdout" class="ch.qos.logback.core.ConsoleAppender">
       <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
   </appender>
   <root level="INFO">
       <appender-ref ref="stdout" />
   </root>
   ```

   This uses Logstash Logback Encoder to output JSON. A sample log entry might then be a JSON object with message, level, timestamp, etc.

2. **Deploy ELK**: Set up Elasticsearch and Kibana (e.g., via Docker, or cloud service like Amazon Elasticsearch Service).

3. **Run Filebeat**: Configure Filebeat on the same host or as a sidecar container in K8s:

   - Tell Filebeat which file or STDOUT to read.
   - Point Filebeat output to Elasticsearch (or Logstash). For example, a filebeat.yml might specify:
     ```yaml
     filebeat.inputs:
       - type: log
         paths:
           - "/var/log/yourapp.log"
     output.elasticsearch:
       hosts: ["http://elasticsearch:9200"]
       username: elastic
       password: changeme
     ```
     (Or output.logstash if using Logstash). Filebeat will label logs with e.g. container info if configured, and push them.
   - If using Logstash, you'd have a Logstash config to take input from Beats, maybe apply grok patterns or filter, then output to Elasticsearch.

4. **Kibana**: Once logs are in Elasticsearch, Kibana can create an index pattern (e.g., filebeat-\*). Then you can search logs, set up dashboards, etc. For example, filter logs by `level: ERROR` to see errors, or by a custom field (like `userId`) to trace user activity.

Using ELK centralizes logs from all instances/pods so you don't have to ssh into boxes to read logs. It also keeps historical data for analysis.

Our Spring Boot app doesn't need code changes to integrate with ELK beyond producing logs. It's more about the ops setup. Just ensure logs are structured (or use Logstash to parse if not).

_(Alternatively, if on cloud, you might use cloud-specific logging: e.g., AWS CloudWatch Logs, GCP Stackdriver, which can ingest Docker stdout directly. Those can replace an ELK stack, though ELK gives more flexibility in self-hosted environments.)_

### 8.2 Metrics Monitoring with Prometheus & Grafana

**Spring Boot Actuator**:
We included Actuator which exposes endpoints like `/actuator/metrics`, `/actuator/health`. Actuator, together with **Micrometer**, collects a variety of metrics: CPU, memory, JVM stats, request rates, etc. By adding the Prometheus dependency, we can expose these metrics in a Prometheus-compatible format ([Configure Spring Boot to generate Prometheus metrics | Grafana Cloud documentation
](https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/enable-prom-metrics-collection/application-frameworks/springboot/#:~:text=Spring%20Boot%20is%20a%20popular,metrics%20in%20the%20Prometheus%20format)).

- Add `micrometer-registry-prometheus` to the classpath. This will add a `/actuator/prometheus` endpoint that outputs metrics in Prometheus format.
- Configure if needed in `application.properties`:
  ```properties
  management.endpoints.web.exposure.include=health,info,prometheus
  management.endpoint.health.show-details=always
  ```
  This ensures the Prometheus endpoint is exposed (if using Spring Boot 2.x, it often is by default when the dependency is present).

**Prometheus**:

- Deploy Prometheus server (e.g., as Docker or in K8s).
- Configure a **scrape job** for our Spring Boot app. In Prometheus `prometheus.yml`:

  ```yaml
  scrape_configs:
    - job_name: "yourapp"
      metrics_path: "/actuator/prometheus"
      scrape_interval: 15s
      static_configs:
        - targets: ["yourapp-host:8080"]
  ```

  If in Kubernetes, you'd configure it to discover pods via labels (using `kubernetes_sd_configs`).

- Prometheus will periodically GET the metrics endpoint and store the time-series data.

**Grafana**:

- Connect Grafana to Prometheus as a data source.
- Import a Spring Boot dashboard or create graphs for metrics:
  - e.g., Requests per second: metric `http_server_requests_seconds_count` (Micrometer exposes something like that labeled by endpoint and status).
  - Heap memory usage: `jvm_memory_used_bytes` with tags for heap or non-heap.
  - DB connection pool: Hikari metrics like `hikari_connections_active` (if Micrometer picks those up, which it does for many supported libraries).
  - Cache hits/misses: if using cache, micrometer can track hits if configured via CacheMetrics (you can enable it, or manually instrument).

Grafana allows setting alerts on metrics (e.g., if memory usage >80% for 5 minutes, send alert).

**Alerts**:
Prometheus Alertmanager can send alerts on conditions (Grafana can too in newer versions). For example, trigger an alert if:

- `http_server_requests_seconds_max{status="5xx"}` is above some threshold (meaning requests causing errors or taking too long).
- `jvm_memory_used_bytes{area="heap"}` nearing `jvm_memory_max_bytes{area="heap"}`.

**Using Actuator in K8s**:
We already utilized the health endpoint for liveness/readiness probes. The metrics endpoint similarly can be secured if needed (you might require a token to access it in production by enabling security for Actuator). Alternatively, run a sidecar Prometheus agent in the pod that has access. Many leave `/actuator/prometheus` open internally but not expose it externally.

**Business Metrics**:
Micrometer allows you to define custom metrics. For example, you could track "number of products sold" or "cache hit ratio" by incrementing counters or gauges in code. These would then appear in Prometheus and Grafana. This is powerful for monitoring not just system health but business KPIs.

With ELK logging and Prometheus/Grafana monitoring, we have **observability** on our application:

- Logs for tracing what happened with details.
- Metrics for aggregated health/performance data and alerting.

There are other aspects like **distributed tracing** (Spring Cloud Sleuth + Zipkin or Jaeger) especially if you have microservices. Sleuth can tag logs with trace IDs and also produce trace spans for distributed operations which can be viewed in Zipkin. Since this guide focuses on one application, we won't dive into tracing, but it's worth noting as part of observability toolset.

## 9. Best Practices & Design Patterns

To wrap up, let's summarize some best practices and design patterns applied (or relevant) in our application architecture, which ensure **scalability** and **maintainability**:

### 9.1 General Best Practices

- **Layered Architecture & Separation of Concerns**: As we did, keep presentation, business logic, and data access separate. This makes it easier to modify one layer without impacting others and to test components in isolation.

- **Single Responsibility Principle**: Each class/module has one responsibility. Our controllers only handle HTTP and delegate to services; services handle business logic, etc. This makes classes simpler and more maintainable.

- **Dependency Injection**: Rely on Spring to inject dependencies (we used `@Autowired` or constructor injection). This decouples implementation from usage and makes testing easier (we can inject mocks). It also aligns with the **Inversion of Control** principle central to Spring.

- **Configuration Management**: Externalize configuration (we used properties and env variables). For sensitive data, use `Spring Boot @ConfigurationProperties` and externalize via environment or use a secrets management tool. Avoid hardcoding configs or secrets in code.

- **Handling Sensitive Data**: Never log sensitive info (passwords, tokens). Secure keys (like JWT secret) in config, not code (we had it hardcoded in example for brevity, but in real apps, inject via env or vault).

- **Validation and Error Handling**: Validate inputs early (using Bean Validation) and provide clear error responses (via exception handlers). This results in a robust API that fails gracefully with useful messages rather than 500 errors or incorrect data persistence.

- **API Versioning**: As the API evolves, consider versioning your REST endpoints (e.g., `/api/v1/products`). This allows introducing breaking changes in a new version while supporting old clients on v1.

- **Documentation**: Document the APIs (use Swagger/OpenAPI by adding springdoc-openapi or springfox swagger—this generates interactive API docs). Document important modules and usage in a README or Wiki for developers. This helps onboarding and maintenance ([Spring Boot folder structure best practices](https://symflower.com/en/company/blog/2024/spring-boot-folder-structure/#:~:text=%2B1%3A%20Maintain%20adequate%20documentation)).

- **Keep It Stateless**: We ensured our app is stateless (especially with JWT auth). This is an important scalability best practice – any instance can serve any request without needing session stickiness. It simplifies scaling and recovery.

- **Graceful Shutdown**: In production, configure graceful shutdown for Spring Boot (Spring Boot 2.3+ does this by default) so that when a pod shuts down, it finishes in-flight requests before closing.

### 9.2 Performance and Scalability Best Practices

- **Think in Terms of Scale**: Design the database with indexing and relationships that can handle large data volumes. Optimize queries as discussed. If one database becomes a bottleneck, consider sharding or splitting data domains (for instance, user data vs product data separated if needed).

- **Use CDN and Caching on front**: Though not part of backend code, mention that static content (if any) should be served via CDN, and API responses that are cacheable should include proper cache headers to leverage browser or gateway caches.

- **Asynchronous Communication**: For very high scale or decoupling, consider using messaging (Kafka, RabbitMQ). For example, instead of immediately sending an email in a request, produce an event to a queue and let another service or a listener handle it. This improves user-facing performance and decouples services.

- **Rate Limiting and Throttling**: Implement measures (possibly at API gateway level) to prevent abuse or overload (e.g., too many requests from one IP). Spring Cloud Gateway or external API gateways can enforce rate limits.

- **Testing and CI/CD**: Automate tests and run them on each commit (CI pipeline). Use static code analysis (SonarQube or similar) to catch code smells or security issues. A CI/CD pipeline can also build the Docker image and maybe run a container scan for vulnerabilities.

- **Deploy gradually**: In Kubernetes, use rolling updates. Possibly use canary or blue-green deployments for critical systems to minimize risk.

### 9.3 Design Patterns in Use

Our application implicitly and explicitly uses several design patterns:

- **Singleton**: Spring Beans are essentially singletons by default (one instance per application context). This is beneficial for stateless service/repository beans – only one instance manages database operations, for example ([Top 5 Design Patterns in Java Spring Boot: Best Practices and Examples - DEV Community](https://dev.to/jackynote/top-5-design-patterns-in-java-spring-boot-best-practices-and-examples-4lch#:~:text=The%20Singleton%20pattern%20ensures%20that,implement%20it%20in%20Spring%20Boot)).

- **Factory Method**: Spring’s `ApplicationContext` is effectively a factory that instantiates beans. Also, our `UserDetailsService` + `PasswordEncoder` usage is akin to factory for authentication objects. If we had more complex object creation, we might implement factory methods to decide which implementation to return (e.g., a `PaymentProcessorFactory` to return a PayPal or CreditCard processor as in typical examples ([Top 5 Design Patterns in Java Spring Boot: Best Practices and Examples - DEV Community](https://dev.to/jackynote/top-5-design-patterns-in-java-spring-boot-best-practices-and-examples-4lch#:~:text=Factory%20Method%20Pattern)) ([Top 5 Design Patterns in Java Spring Boot: Best Practices and Examples - DEV Community](https://dev.to/jackynote/top-5-design-patterns-in-java-spring-boot-best-practices-and-examples-4lch#:~:text=public%20class%20CreditCardProcessor%20implements%20PaymentProcessor,))).

- **Strategy Pattern**: We could utilize Strategy if we had multiple algorithms for an operation. For example, if we had different caching strategies, we could have a Strategy interface and multiple implementations, choosing one at runtime. In Spring, you might autowire a list of strategies and pick one based on config. Our security filter is a strategy for authentication; if we switched to OAuth2, we'd plug a different strategy.

- **Template Method Pattern**: Spring provides many template methods (e.g., `JdbcTemplate`, `RestTemplate`) which handle the boilerplate of resource management and allow you to focus on the logic. In our app, using `JpaRepository` is a bit like Template pattern – it provides a template for CRUD operations so we only define queries or method names, not the actual SQL execution.

- **Proxy Pattern**: Spring AOP and proxies are heavily used. When we annotate `@Transactional` or `@Cacheable`, Spring creates a proxy around our object to implement that behavior (committing transaction after method, or checking cache before method) – that's the Proxy pattern in action. Similarly, our `JwtAuthenticationFilter` acts as a proxy for requests, adding auth logic around the request processing chain ([Building a Role-Based Access Control System with JWT in Spring Boot - DEV Community](https://dev.to/alphaaman/building-a-role-based-access-control-system-with-jwt-in-spring-boot-a7l#:~:text=,UserDetailsService)).

- **Observer Pattern**: Not directly used, but Spring’s event mechanism allows beans to publish events and others to listen (ApplicationEventPublisher). Could be used for decoupling components (e.g., publish an event when a product is created, handle it elsewhere to send notifications).

- **DTO (Data Transfer Object)**: We didn’t explicitly use DTOs (we passed entity to controller). For a real-world API, using DTOs to separate internal model from API schema is a good practice. That way, changes in internal entity don’t necessarily break API, and you can also shape data differently for clients. This is more of a design practice than a GoF pattern, but notable.

- **Clean Architecture / Hexagonal**: Our design is layered which is a basic form. Hexagonal (or ports-and-adapters) would take it further – e.g., define interfaces for repository (as ports) and have adapters for JPA, Mongo implementations. This allows swapping out the data source without changing core logic. We partially did this by coding mostly to `ProductRepository` interface (which could have different impl). Advanced apps might even abstract that further.

### 9.4 Maintainability Tips

- **Modularity**: Consider splitting into multi-module Maven project or microservices if the project grows very large or teams are big. In a multi-module setup, you might have separate modules for domain models, for each microservice, etc., improving modularity and reusability.

- **Upgrading**: Keep dependencies up to date (especially security-related ones). Spring Boot releases patches – upgrading can bring performance improvements and fixes.

- **Documentation & Comments**: Use Javadoc for public methods, especially in library modules. And maintain clear README or API docs for how to use the service. As noted, a well-documented project structure is valuable ([Spring Boot folder structure best practices](https://symflower.com/en/company/blog/2024/spring-boot-folder-structure/#:~:text=%2B1%3A%20Maintain%20adequate%20documentation)).

- **Monitoring & Alerting in place**: As we covered, ensure you are monitoring logs and metrics so that any issue in production can be quickly identified. Practice chaos engineering or at least simulate failures (like DB down) in a staging environment to see how the system behaves and recovers.

By adhering to these best practices and patterns, our Spring Boot application will be easier to maintain, scale, and extend in the future. We've applied many of them throughout this guide: a clean project structure, layered design, security best practices, caching for performance, and thorough testing.

---

## Conclusion

We have built a feature-rich Spring Boot application step-by-step:

- Set up a structured project with essential dependencies.
- Implemented robust CRUD APIs with validation and global exception handling.
- Integrated with MySQL (relational), Redis (cache), and MongoDB (NoSQL) to showcase polyglot persistence and caching.
- Secured the application with JWT-based authentication and role-based authorization using Spring Security.
- Written unit and integration tests to ensure code quality and correctness.
- Optimized performance with query tuning, caching, and by leveraging Spring Boot’s efficient defaults (like HikariCP).
- Containerized the application and outlined deployment strategies in Docker and Kubernetes, preparing it for cloud-scale operation.
- Incorporated logging and monitoring (ELK, Prometheus, Grafana) for observability in production.
- Followed best practices and applied design patterns to make the application scalable and maintainable.

By following this guide, you have a blueprint for developing real-world Spring Boot applications with a modern backend stack. The techniques and practices covered will help in building systems that are robust in the face of errors, efficient under load, and adaptable to changing requirements. Happy coding!
