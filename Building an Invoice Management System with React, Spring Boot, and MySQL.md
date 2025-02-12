Got it! I will create a comprehensive 200-page step-by-step guide for advanced developers on building an invoice management system using React, Spring Boot, and MySQL. This guide will cover in-depth architectural design, performance optimization, security best practices, testing strategies, and deployment using modern tools like Docker and Kubernetes.

I'll notify you once the detailed guide is ready.

# Building an Invoice Management System with React, Spring Boot, and MySQL

Welcome to this comprehensive guide on building a full-stack **Invoice Management System** using **React, Spring Boot, and MySQL**. This step-by-step guide is structured as a book for advanced developers, covering every aspect from high-level architecture to deployment. We’ll explore system design considerations, delve into backend and frontend development, discuss security and testing best practices, set up CI/CD pipelines, and cover deployment and monitoring strategies. Along the way, you’ll find **code examples**, **exercises**, and **real-world best practices** to reinforce learning.

## Chapter 1: System Architecture & Design Patterns

In this chapter, we’ll define the overall architecture of our invoice management system. We will discuss high-level design, layered architecture principles, and compare monolithic and microservices approaches. Understanding these concepts ensures a strong foundation for building scalable, maintainable software.

### High-Level Architecture

At a high level, an invoice management system consists of a **frontend client**, a **backend server**, and a **database**:

- **Frontend (React + TypeScript)**: A single-page application (SPA) for users to interact with the system (creating invoices, viewing reports, etc.).
- **Backend (Spring Boot)**: Exposes RESTful APIs to handle business logic, data processing, and security.
- **Database (MySQL)**: Stores persistent data such as customer info, invoices, payments, and user accounts.

**Client-Server Interaction**: The React frontend communicates with the Spring Boot backend via HTTP/HTTPS requests to REST API endpoints. For example, the client might send a GET request to `/api/invoices` to fetch all invoices, or a POST request to `/api/invoices` to create a new invoice. The backend processes these requests, interacts with the database via JPA (Java Persistence API), and returns JSON data to the frontend.

**Layer Separation**: Even within each application, it's prudent to separate concerns:

- In the **frontend**, separate components, services (for API calls), and state management.
- In the **backend**, use a layered approach (controller, service, repository layers) to organize code (discussed in the next section).

**Design Goals**:

- **Scalability**: Ability to handle increasing loads by scaling horizontally (adding more instances) or vertically (adding resources to the server).
- **Maintainability**: Clear separation of concerns and modular design so new features can be added with minimal impact on existing code.
- **Security**: Protect data through authentication, authorization, and secure communication (HTTPS).
- **Performance**: Efficient data handling, use of caching, and optimized database queries for quick response times.

We’ll be using **RESTful design principles** for the APIs. Each resource (Invoice, Customer, User, etc.) will have dedicated endpoints for CRUD operations (Create, Read, Update, Delete). For instance:

- `GET /api/invoices` – retrieve list of invoices
- `GET /api/invoices/{id}` – retrieve details of a specific invoice
- `POST /api/invoices` – create a new invoice
- `PUT /api/invoices/{id}` – update an existing invoice
- `DELETE /api/invoices/{id}` – delete an invoice

This consistent URL structure and use of HTTP methods follow REST conventions, making the API intuitive.

### Layered Design Principles

Layered architecture (also known as n-tier architecture) divides the application into distinct layers, each with specific responsibilities. This separation helps manage complexity in large applications and promotes **modularity** and **testability**. A typical layered design for our Spring Boot backend might include:

- **Controller Layer**: Also called the presentation or web layer. It contains REST controllers (`@RestController` in Spring) that handle HTTP requests and responses. Controllers delegate work to the service layer. Example: `InvoiceController` handles endpoints like `/api/invoices`.
- **Service Layer**: Contains business logic. Services process requests from controllers, apply business rules, and coordinate with repositories. Example: `InvoiceService` might calculate totals or apply discounts before saving an invoice.
- **Repository/Data Access Layer**: Interacts with the database, typically through Spring Data JPA repositories or DAO (Data Access Objects). This layer contains entity queries, database connections, and transaction management (often handled by Spring behind the scenes). Example: `InvoiceRepository extends JpaRepository` handles CRUD operations for `Invoice` entities.

Each layer communicates only with its immediate neighbor: Controllers call Services, Services call Repositories. This enforces **loose coupling** – for instance, the controller doesn’t need to know how data is fetched from the database, and the repository doesn’t know how the data is presented to the user.

**Benefits of Layered Architecture**:

- **Separation of Concerns**: Each layer focuses on a specific aspect, making the code easier to understand and maintain.
- **Modularity**: You can modify or replace one layer’s implementation (e.g., switch data sources) with minimal changes to others, as long as the interface/contract between layers remains consistent.
- **Testability**: Layers can be tested in isolation using mocks. For example, you can unit test the Service layer by mocking the Repository layer.
- **Reusability**: Business logic in the Service layer can be reused across different contexts (e.g., a GUI application or a different microservice) by calling the same service methods.
- **Consistency**: A layered approach is a well-known pattern, so most developers will understand the structure quickly.

Our project will follow this layered approach within the **backend**. The **frontend** will also have structure (like separating presentational components and hooks or context for state), but it’s often less formally layered than backend code. For the frontend, we will ensure separation between:

- UI components (JSX/HTML with Tailwind/MUI for layout and styling),
- State management (using Context API or Redux for global state),
- API interaction logic (maybe placing all API calls in one module or using custom hooks with React Query),
- Utility functions (for formatting dates, currency, etc.).

Throughout the guide, as we implement features, we will maintain these divisions to keep code organized.

### Microservices vs Monolithic Approach

**Monolithic Architecture**: In a monolithic design, the entire backend (and often the frontend) is a single, unified application. All modules (invoice processing, user management, reporting, etc.) run within one process and are packaged together. Monoliths are simpler to start with and deploy (one deployable unit). They often use layered architecture internally, as described above.

**Microservices Architecture**: In a microservices approach, the application is broken into smaller, independent services that communicate over a network (typically using APIs). For example, you might have separate services for **Invoice Service**, **User Service**, **Notification Service**, etc. Each runs in its own process, possibly on different servers or containers, and they interact via REST APIs, messaging, or gRPC.

**Which to choose?** This depends on the project scope and organizational needs:

- A **monolith** can be easier to develop initially. All code in one place means no overhead of inter-service communication. You can avoid duplication by sharing code easily, and testing is straightforward (no need to launch multiple services).
- **Microservices** shine when your application grows large and you need independent scaling, independent deployments, or team autonomy. If one module becomes a bottleneck, it can be scaled or optimized separately. Microservices can also allow using different tech stacks for different services if needed (though in our case we stick to Spring Boot for backend services).

For an **invoice management system**, starting with a monolithic Spring Boot application is perfectly fine and likely more practical. Monoliths, being single units, are easier to test end-to-end and debug since you can run the entire app together. However, as Atlassian notes, _“when monoliths grow too big it may be time to transition to microservices.”_. If our system later needs to handle vastly more load or if we want to develop features in parallel by different teams, we could split off services (for example, a dedicated microservice just for generating PDF invoices or handling billing cycles).

**Transition example**: Start monolithic (one Spring Boot app). Suppose down the line, the invoice generation component becomes resource-intensive and needs separate scaling, or a new team needs to work on it without affecting others. That could be peeled out into a microservice (e.g., `InvoiceGenerationService`) with its own database or schema. The main app would then call this service’s API to generate invoices. The rest of the system (customers, payments, UI) could remain in the monolith until there's a reason to split further.

**Design Patterns**: Whether monolithic or microservices, you will employ design patterns:

- In the backend, patterns like **MVC (Model-View-Controller)** for web layers, **DAO/Repository** for data access, and possibly **Service Locator or Dependency Injection** (via Spring’s IoC container) are used.
- For microservices, patterns like **API Gateway**, **Circuit Breaker** (with tools like Resilience4j or Netflix Hystrix), and **Event Sourcing** or **CQRS** might come into play as the system evolves.
- In the frontend, common patterns include **Container-Presenter** (smart vs dumb components), **Custom Hooks** for abstracting logic, and design systems for consistent UI.

**Best Practice**: It’s usually wise to **design a monolith that can be modular** – meaning organize code by feature modules internally. This way, if you ever split into microservices, the separation is clearer. For example, keep invoice-related code in one package, user-related in another, etc. Some even call this a “modular monolith.” It gives some benefits of microservices (modularity) without the complexity of distributed systems.

### Exercises

- **Exercise 1.1 – Design Diagram**: Draw a high-level architecture diagram for the invoice system. Identify the user’s browser, the React app, the Spring Boot API, and the MySQL database. Indicate how data flows when a user creates a new invoice.
- **Exercise 1.2 – Identify Layers**: Take a feature (e.g., “Add New Invoice”) and describe how each backend layer (Controller, Service, Repository) will participate. For instance, what does the controller method do, what business rules might the service apply, and what does the repository query or save?
- **Exercise 1.3 – Monolith vs Microservice**: List 3 potential microservices that the invoice system could be broken into (e.g., Invoice Service, User Management Service, etc.). For each, describe one benefit and one drawback of having it as a separate microservice rather than part of a monolith.

---

## Chapter 2: Backend Development (Spring Boot + MySQL)

In this chapter, we’ll set up the backend of our application using **Spring Boot** and **MySQL**. We’ll start by creating a Spring Boot project, then model the database with entities and relationships. We’ll develop RESTful endpoints to manage invoices and other data, using Spring Data JPA to handle persistence. We’ll incorporate **Flyway** for database migrations and document the API with **Swagger/OpenAPI**. We’ll also implement **authentication** (using JWT or OAuth2) and role-based authorization, and discuss performance optimizations like caching and database indexing.

### Setting up a Spring Boot Project with Maven

To kick-start our backend, we’ll create a new Spring Boot project. You can use Spring Initializr (https://start.spring.io/) which is a web tool for generating Spring Boot projects. Alternatively, you can set it up manually with Maven:

1. **Generate Project**: Using Spring Initializr, select _Maven Project_, Java (appropriate version, e.g., 17), and Spring Boot (latest version). Choose dependencies: Spring Web, Spring Data JPA, MySQL Driver, Lombok (optional), Spring Security (for later), and any others we know we’ll need (like Spring Boot Actuator for monitoring, if desired). This will give a zip; unzip it to your workspace.
2. **Maven POM**: Open the `pom.xml`. We should see `<parent>` set to Spring Boot’s parent BOM (Bill of Materials) which manages dependency versions. It will also include the Spring Boot Maven Plugin. Ensure packaging is set to `jar` (for a standalone app) and the Spring Boot Maven plugin is present. The plugin enables us to build an **executable JAR** that can run with `java -jar`. For example, a snippet in `pom.xml`:

   ```xml
   <packaging>jar</packaging>
   ...
   <build>
       <plugins>
           <plugin>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-maven-plugin</artifactId>
           </plugin>
       </plugins>
   </build>
   ```

   Spring Boot’s Maven plugin bundles the application and all dependencies into a single JAR (sometimes called a "fat JAR") that’s easy to deploy. Setting packaging to JAR and including this plugin means Maven will package the project as an executable jar file.

3. **Application Entry Point**: Check the generated `Application` class (for example, `InvoiceSystemApplication.java`) in the source. It should have `@SpringBootApplication` annotation and a `main` method. This is the starting point that Spring Boot uses to launch the application:

   ```java
   @SpringBootApplication
   public class InvoiceSystemApplication {
       public static void main(String[] args) {
           SpringApplication.run(InvoiceSystemApplication.class, args);
       }
   }
   ```

   This triggers Spring Boot’s auto-configuration and component scanning.

4. **Configuration**: In `src/main/resources`, ensure there’s an `application.properties` (or `application.yml`). We will configure database connectivity here soon (JPA and MySQL settings).

5. **Run & Verify**: You can run the application (via your IDE or `./mvnw spring-boot:run`). It likely won’t do much yet, but checking that it starts without errors is a good sanity check.

#### Configuring MySQL Connection

We need to set up a connection to the MySQL database. Make sure you have MySQL running and have created a database (e.g., named `invoice_system`). In `application.properties`, add:

```
spring.datasource.url=jdbc:mysql://localhost:3306/invoice_system?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
spring.datasource.username=<your_mysql_user>
spring.datasource.password=<your_mysql_password>

spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
```

Explanation:

- `spring.datasource.url`: JDBC URL for MySQL. We include `useSSL=false` for local dev, `allowPublicKeyRetrieval=true` to avoid some authentication issues in newer MySQL, and set `serverTimezone` if needed.
- `spring.datasource.username`/`password`: Credentials for the MySQL database.
- `spring.jpa.hibernate.ddl-auto`: We set this to `validate` to ensure our JPA entities match the DB schema (but not automatically create or update schema in production). For initial development, you can use `update` to auto-create tables, but we’ll use Flyway for structured migrations.
- `spring.jpa.show-sql`: true will log SQL statements to the console for debugging.

Now our Spring Boot application knows how to connect to the database. On startup, if everything is correct, you should see a successful connection message in the logs. If credentials or URL are wrong, you'll see errors which you should fix before proceeding.

#### Packaging and Running

With Maven, common commands:

- `mvn clean package` – compiles and packages the app into a jar (found in `target/` directory).
- `mvn spring-boot:run` – runs the application directly (useful during development).
- After packaging, you can run `java -jar target/yourapp.jar` to start it.

We will use Maven for building and testing, and later in CI/CD.

### Entity Relationship Modeling

Designing the database schema and the corresponding JPA entities is a crucial step. We’ll use JPA (Java Persistence API) annotations to map Java classes to database tables. Let’s identify main entities for an invoice system:

- **User**: represents a system user (for authentication/authorization).
- **Customer**: represents a client/customer to whom invoices are issued.
- **Invoice**: represents an invoice record.
- **InvoiceItem**: line items within an invoice (each item could be a product or service billed).
- **Payment**: (optional) represents payments made towards invoices (if tracking payments).

For simplicity, we can start with Invoice and related entities:

- An **Invoice** likely has fields: `id`, `invoiceNumber`, `date`, `customer` (who is being billed), list of `items`, `totalAmount`, `status` (PAID/UNPAID).
- An **InvoiceItem** might have: `id`, `description`, `quantity`, `price`, `invoice` (the invoice it belongs to).
- A **Customer**: `id`, `name`, `address`, `email`, etc., and potentially a list of `invoices`.

Relationships:

- Customer to Invoice: One customer can have many invoices (One-to-Many).
- Invoice to InvoiceItem: One invoice has many items (One-to-Many).
- We might also have Many-to-One from Invoice back to Customer, and Many-to-One from InvoiceItem back to Invoice.

Let’s create the entity classes with JPA:

**Customer Entity** (`Customer.java`):

```java
@Entity
@Table(name = "customers")
public class Customer {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;
    private String address;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL)
    private List<Invoice> invoices = new ArrayList<>();

    // Getters and setters (or use Lombok @Data for brevity)
}
```

Explanation:

- `@Entity` marks it as a JPA entity.
- `@Table(name="customers")` specifies the table name (optional if it matches class name).
- `@Id` and `@GeneratedValue` denote primary key and auto-generation strategy (using MySQL’s auto-increment).
- Fields `name, email, address` are basic columns.
- `@OneToMany(mappedBy="customer")` indicates one customer to many invoices. `mappedBy` references the field in `Invoice` that owns the relationship.
- `cascade = ALL` means operations on customer cascade to its invoices (e.g., if we delete a customer, their invoices get deleted too – use carefully).
- We initialize `invoices` to avoid NullPointer issues.

**Invoice Entity** (`Invoice.java`):

```java
@Entity
@Table(name = "invoices")
public class Invoice {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String invoiceNumber;
    private LocalDate date;
    private Double totalAmount;
    private String status; // e.g., "PAID" or "UNPAID"

    @ManyToOne
    @JoinColumn(name = "customer_id")
    private Customer customer;

    @OneToMany(mappedBy = "invoice", cascade = CascadeType.ALL)
    private List<InvoiceItem> items = new ArrayList<>();

    // Getters and setters
}
```

- `invoiceNumber`: A unique number or code for the invoice (could be auto-generated).
- `date`: Date of issue.
- `totalAmount`: Redundant field (can be derived by summing items, but storing it can optimize queries).
- `status`: Just a string for status (an enum would be better, but string for simplicity).
- `@ManyToOne` with `@JoinColumn` defines the foreign key column `customer_id` linking to Customer.
- `@OneToMany` for items.

**InvoiceItem Entity** (`InvoiceItem.java`):

```java
@Entity
@Table(name = "invoice_items")
public class InvoiceItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String description;
    private Integer quantity;
    private Double unitPrice;

    @ManyToOne
    @JoinColumn(name = "invoice_id")
    private Invoice invoice;

    public Double getLineTotal() {
        return unitPrice * quantity;
    }
    // Getters and setters
}
```

- Fields for item description, quantity, and price.
- `getLineTotal()` is a convenience method (not a persisted field) to compute total for that line.

**User Entity** (`User.java`):

```java
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String password; // hashed password
    private String role; // e.g., "ROLE_ADMIN" or "ROLE_USER"

    // constructors, getters, setters
}
```

- We include this for authentication. It might have roles for access control.
- Storing `role` as a simple string for now. (Could also have a separate Role entity and a ManyToMany for users<->roles for more complex scenarios).

After defining these entities, we should update the database schema. If we run the application with `spring.jpa.hibernate.ddl-auto=update`, it could create the tables automatically. But for better control, we’ll use Flyway migrations next.

### REST API Development with Spring Boot

With entities in place, we can create REST controllers and services to expose the functionality. We’ll follow the layered approach:

- **Repositories**: Interfaces that extend Spring Data JPA’s repository interfaces for each entity.
- **Services**: Classes that use repositories to implement business logic.
- **Controllers**: REST controllers that map HTTP requests to service calls.

#### Repository Layer

Thanks to Spring Data JPA, we often don’t need to implement repository classes; we define interfaces and Spring Boot provides implementation at runtime. For example:

```java
public interface InvoiceRepository extends JpaRepository<Invoice, Long> {
    // You can define custom query methods if needed, e.g.:
    List<Invoice> findByCustomerId(Long customerId);
}
public interface CustomerRepository extends JpaRepository<Customer, Long> {}
public interface InvoiceItemRepository extends JpaRepository<InvoiceItem, Long> {}
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}
```

These interfaces give us basic CRUD and finder operations:

- `InvoiceRepository.findAll()` to list invoices, `findById()`, `save()`, etc., without writing SQL or implementation.
- We added a custom method `findByCustomerId` by following Spring Data’s naming conventions. Spring will parse that and generate a query to find invoices by customer’s id.

#### Service Layer

Services will use these repositories. Let’s implement a couple of services:

**InvoiceService**:

```java
@Service
@RequiredArgsConstructor // if using Lombok to generate constructor for final fields
public class InvoiceService {
    private final InvoiceRepository invoiceRepo;
    private final CustomerRepository customerRepo;

    public Invoice createInvoice(Invoice invoice) {
        // Perhaps set an invoice number or default date before saving
        if (invoice.getDate() == null) {
            invoice.setDate(LocalDate.now());
        }
        // Calculate total from items
        double total = invoice.getItems().stream()
                               .mapToDouble(item -> item.getQuantity() * item.getUnitPrice())
                               .sum();
        invoice.setTotalAmount(total);
        invoice.setStatus("UNPAID");
        return invoiceRepo.save(invoice);
    }

    public List<Invoice> listInvoices() {
        return invoiceRepo.findAll();
    }

    public Invoice getInvoice(Long id) {
        return invoiceRepo.findById(id)
               .orElseThrow(() -> new ResourceNotFoundException("Invoice not found"));
    }

    public Invoice updateInvoice(Long id, Invoice updatedData) {
        Invoice invoice = getInvoice(id);
        // Update fields if present in updatedData
        if (updatedData.getStatus() != null) {
            invoice.setStatus(updatedData.getStatus());
        }
        // (similar for other fields like date or items if we allow updating them)
        return invoiceRepo.save(invoice);
    }

    public void deleteInvoice(Long id) {
        invoiceRepo.deleteById(id);
    }
}
```

- We inject `InvoiceRepository` and `CustomerRepository` (for any customer lookups, if needed).
- `createInvoice`: business logic example – set default date if not provided, compute total amount from items, default status to "UNPAID", then save. Notice we didn’t explicitly save items or customer; JPA cascades will handle saving items when invoice is saved (because of `cascade = ALL` on invoice->items).
- `listInvoices` simply returns all invoices.
- `getInvoice` retrieves one or throws a custom exception if not found (you’d define `ResourceNotFoundException` to return HTTP 404).
- `updateInvoice` demonstrates updating an existing invoice (fetching first, then saving changes).
- `deleteInvoice` uses repository method to delete.

We’d have similar **CustomerService** for customers and possibly a **UserService** for user management (especially for auth, loading users by username, etc.). But to keep focus, the InvoiceService is our main example.

#### Controller Layer

Now, the REST controller exposes endpoints mapping HTTP methods to these service methods.

**InvoiceController**:

```java
@RestController
@RequestMapping("/api/invoices")
@RequiredArgsConstructor
public class InvoiceController {
    private final InvoiceService invoiceService;

    @GetMapping
    public List<Invoice> getAllInvoices() {
        return invoiceService.listInvoices();
    }

    @GetMapping("/{id}")
    public Invoice getInvoiceById(@PathVariable Long id) {
        return invoiceService.getInvoice(id);
    }

    @PostMapping
    public ResponseEntity<Invoice> createInvoice(@RequestBody Invoice invoice) {
        Invoice created = invoiceService.createInvoice(invoice);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public Invoice updateInvoice(@PathVariable Long id, @RequestBody Invoice invoice) {
        return invoiceService.updateInvoice(id, invoice);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteInvoice(@PathVariable Long id) {
        invoiceService.deleteInvoice(id);
        return ResponseEntity.noContent().build();
    }
}
```

- `@RestController` implies the methods will return data (as JSON by default, since Jackson is on the classpath).
- `@RequestMapping("/api/invoices")` sets the base URL for all endpoints in this controller.
- `@GetMapping` with no path returns all invoices.
- `@GetMapping("/{id}")` maps to e.g. `/api/invoices/5` and uses `@PathVariable` to get id.
- `@PostMapping` for creating. We take `@RequestBody Invoice invoice` which Spring will bind from JSON to an Invoice object. We return `201 Created` status with the created object.
- `@PutMapping("/{id}")` for updates – in real scenarios, partial updates might use PATCH, but here using PUT to replace the resource (though our service merges changes).
- `@DeleteMapping("/{id}")` returns 204 No Content on success.

We would similarly have `CustomerController` for customer endpoints (or include customer management endpoints in the same controller, which is also fine if related).

**Testing the API**: At this point, if you run the Spring Boot application and use a tool like **cURL** or **Postman**, you can hit these endpoints. For example:

```
GET http://localhost:8080/api/invoices
```

should return an empty list `[]` initially. You can then POST a JSON to create an invoice:

```json
POST http://localhost:8080/api/invoices
Content-Type: application/json

{
  "invoiceNumber": "INV-1001",
  "date": "2025-02-11",
  "customer": { "id": 1 },
  "items": [
    { "description": "Product A", "quantity": 2, "unitPrice": 50.0 },
    { "description": "Product B", "quantity": 1, "unitPrice": 75.0 }
  ]
}
```

If a customer with id 1 exists, this will create an invoice for them. The response JSON will include the computed totalAmount and default status. If no customer exists, you'd likely get an error (which indicates we might need to handle creating customer on the fly or require clients to create customers first).

We should ensure the API returns meaningful status codes and messages. For example, if `ResourceNotFoundException` is thrown, we can add an `@ExceptionHandler` in a `@ControllerAdvice` or in the controller to return a 404 status and message.

#### Handling DTOs vs Entities

**Note**: Exposing JPA entities directly in controllers (as done above) can be fine for quick development, but in a real-world system, you often use **DTOs (Data Transfer Objects)** to decouple the API from internal model. For instance, our `Invoice` entity might have a back-reference to customer and items – returning it directly could cause infinite recursion in JSON serialization or expose fields we don’t want (like `User.password` if we returned User). You can use annotations like `@JsonIgnore` on sensitive fields or use projection DTOs.

However, for brevity, this guide may often use entities directly in controllers. Just keep in mind the best practice: **use DTOs for API models** if the domain model is complex or to prevent over-posting (users sending fields they shouldn’t). Tools like **MapStruct** can help map between entity and DTO.

### Using Spring Data JPA with MySQL

We already touched on Spring Data JPA through the repository interfaces. Here are some key points and best practices when using JPA with MySQL:

- **Database Dialect**: Spring Boot will choose a MySQL dialect based on the JDBC driver on classpath. If needed, you can specify `spring.jpa.database-platform = org.hibernate.dialect.MySQLDialect` (or a specific version dialect) in `application.properties`. This ensures Hibernate (the JPA implementation) generates optimized SQL for MySQL.

- **Transactions**: By default, Spring Data JPA repository methods are transactional (read-only for find methods, read-write for others). If you write custom service methods that modify data, annotate them with `@Transactional` to ensure data integrity (Spring can roll back if an exception occurs).

- **Lazy Loading**: By default, many relationships (`@OneToMany`, etc.) are lazy-loaded. This means when you fetch an Invoice, the items collection is not loaded from DB until you access it. This can improve performance by avoiding unnecessary data retrieval, but be careful with JSON serialization (accessing lazy fields outside a transaction can lead to `LazyInitializationException`). Options include:

  - Fetch eagerly (`@OneToMany(fetch = FetchType.EAGER)`) – but that could retrieve too much data always.
  - Use DTOs as mentioned to control exactly what is fetched.
  - Use JPA queries with `fetch join` to get needed data.

- **Query Methods**: Spring Data JPA allows defining finder methods by naming conventions. E.g., `findByStatus(String status)` or `findByCustomerName(String name)` if the relationship exists. For more complex queries, you can use `@Query` annotation to write JPQL or native SQL.

- **Pagination and Sorting**: Useful for listing endpoints. Instead of returning `List<Invoice>`, you can return `Page<Invoice>` by having repository extend `PagingAndSortingRepository` or by using `Pageable` in method params. Example:

  ```java
  @GetMapping("/api/invoices")
  public Page<Invoice> listInvoices(Pageable pageable) {
      return invoiceRepo.findAll(pageable);
  }
  ```

  Then clients can add query params `?page=0&size=10&sort=date,desc` to manage pagination.

- **Database Indexing**: As data grows, ensure to add indexes on columns used in search or joins. In MySQL, the **optimal way to speed up SELECT queries is to create indexes on columns that are used in query conditions (WHERE clauses or joins)**. For our system, indexing fields like `invoice.customer_id`, `invoice.date`, or `invoice.status` could make retrieval faster. We can add these either via DDL in a migration or using JPA/Hibernate annotations (`@Index` on entity).

### Database Migrations with Flyway

Managing database schema changes is critical for long-term projects. **Flyway** is a popular tool for versioning database migrations. Instead of letting Hibernate auto-create or update tables (which is convenient in dev but risky in production), we use migration scripts.

**Setup Flyway**:

1. Add Flyway dependency in Maven:

   ```xml
   <dependency>
       <groupId>org.flywaydb</groupId>
       <artifactId>flyway-core</artifactId>
   </dependency>
   ```

   Spring Boot will detect Flyway on the classpath and automatically run it on startup (before Hibernate initializes).

2. Create a folder `src/main/resources/db/migration`. By convention, Flyway looks here for migration scripts. Each script name must follow `V<version>__<Description>.sql`, e.g., `V1__Init.sql`.

3. Write migration SQL scripts:

   - **V1\_\_Init.sql** – initial schema:
     ```sql
     CREATE TABLE customers (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       email VARCHAR(255),
       address VARCHAR(255)
     );
     CREATE TABLE invoices (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       invoice_number VARCHAR(50),
       date DATE,
       total_amount DOUBLE,
       status VARCHAR(20),
       customer_id BIGINT,
       CONSTRAINT fk_invoice_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
     );
     CREATE TABLE invoice_items (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       description VARCHAR(255),
       quantity INT,
       unit_price DOUBLE,
       invoice_id BIGINT,
       CONSTRAINT fk_item_invoice FOREIGN KEY (invoice_id) REFERENCES invoices(id)
     );
     CREATE TABLE users (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE,
       password VARCHAR(255),
       role VARCHAR(50)
     );
     ```
     This creates our initial tables and sets up foreign keys for relationships.
   - We could also insert a test or default user:
     ```sql
     INSERT INTO users (username, password, role) VALUES ('admin', '<hashed_pw>', 'ROLE_ADMIN');
     ```
     (We’d need to generate a hashed password, perhaps using BCrypt. Alternatively, leave the password plain for now and handle hashing in code.)

4. Run the application. Flyway will detect no previous migrations have been applied, then it will execute V1\_\_Init.sql. By default, Flyway creates a table `flyway_schema_history` to track applied migrations. If everything is correct, our database now has all required tables.

5. Future changes: If we need to alter a table or add a new one, we create a new migration script, e.g., `V2__AddInvoiceIndexes.sql` to add indexes, or `V3__AddPaymentTable.sql`, etc. Flyway will run those that haven’t been run yet in order.

Using Flyway ensures **schema version consistency** across different environments (dev, staging, prod). It also supports rolling back (to some extent) by applying reverse operations in new migrations (Flyway itself doesn’t undo migrations, but you can manually code a "downgrade" script if needed).

Spring Boot will automatically run Flyway at startup if `flyway-core` is on the classpath. If you prefer to control when migrations run (like only during deployments), you can disable this via properties or run Flyway via Maven plugin.

### API Documentation with Swagger/OpenAPI

Documenting your REST API is important for consumers of the API (including front-end developers or third parties). We will integrate **Swagger/OpenAPI** using the `springdoc-openapi` library which automates generation of an OpenAPI spec and provides a Swagger UI out-of-the-box.

**Setup Swagger/OpenAPI**:

1. Add the dependency:

   ```xml
   <dependency>
       <groupId>org.springdoc</groupId>
       <artifactId>springdoc-openapi-ui</artifactId>
       <version>1.7.0</version> <!-- or latest compatible with Spring Boot version -->
   </dependency>
   ```

   (This library might update, for Spring Boot 3+ they have `springdoc-openapi-starter-webmvc-ui` as a newer variant).

2. Once added, run the application and visit: `http://localhost:8080/swagger-ui/index.html`. You should see a Swagger UI with your APIs listed. The library scans the controllers and models to produce an OpenAPI 3.0 documentation automatically.

3. We can enhance documentation using annotations:

   - Use `@Operation` and `@ApiResponse` from `io.swagger.v3.oas.annotations` on controller methods to describe endpoints, parameters, responses.
   - Use `@Schema` on model classes or fields to add descriptions.
     Example:

   ```java
   @GetMapping
   @Operation(summary = "List all invoices", description = "Retrieves a list of all invoices in the system.")
   public List<Invoice> getAllInvoices() { ... }
   ```

   Or:

   ```java
   @Schema(description = "Total amount of the invoice in USD")
   private Double totalAmount;
   ```

4. The OpenAPI JSON spec is available at `http://localhost:8080/v3/api-docs`. This can be used to generate client code or be imported into tools.

By documenting as we go, we ensure our API is user-friendly for other developers. Swagger UI allows testing endpoints as well, which is convenient.

### Implementing Authentication (JWT, OAuth2)

Security is a major aspect. We will secure the REST API so that only authenticated users can access it (except perhaps some public endpoints). We’ll use **JWT (JSON Web Tokens)** for stateless authentication. Alternatively, OAuth2 could be used for integration with external providers or more complex scenarios, but for our guide, we focus on JWT with Spring Security.

**Overview of JWT Auth Flow**:

- **User Login**: The user (or front-end app) sends credentials (username/password) to an auth endpoint (e.g., `POST /api/auth/login`).
- **Token Issuance**: If credentials are valid, the server generates a JWT, signs it (with a secret key), and returns it to the client.
- **Client Stores Token**: The client (browser) stores the token, e.g., in localStorage or memory.
- **Authenticated Requests**: For subsequent API calls, the client includes the JWT in the HTTP `Authorization` header as a Bearer token: `Authorization: Bearer <token>`.
- **Token Validation**: The server, on each request, validates the token (checks signature, expiration, and optionally user roles/claims inside token) and if valid, treats the request as authenticated.

**Setting up Spring Security**:

1. Add Spring Security dependency (if not already added via Spring Initializr). Spring Boot auto-configures a lot, including requiring authentication on all endpoints by default (with a default user and random password if not configured otherwise). We will override those settings.
2. Create a **Security Configuration** class, e.g., `SecurityConfig.java`, annotated with `@Configuration` and `@EnableWebSecurity` (and perhaps `@EnableMethodSecurity` if we want method-level security with `@PreAuthorize`):

   ```java
   @Configuration
   @EnableWebSecurity
   @EnableMethodSecurity
   public class SecurityConfig {
       @Bean
       public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
           http
             .csrf().disable()  // disable CSRF for simplicity (enabled by default for form logins)
             .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS) // no sessions, we use JWT
             .and()
             .authorizeHttpRequests(auth -> auth
                 .requestMatchers("/api/auth/**").permitAll()  // allow auth endpoints without auth
                 .anyRequest().authenticated()                 // all other requests need auth
             )
             .oauth2ResourceServer().jwt(); // enable JWT authentication

           return http.build();
       }

       @Bean
       public PasswordEncoder passwordEncoder() {
           return new BCryptPasswordEncoder();
       }
   }
   ```

   This config:

   - Disables CSRF since we won't be using cookies for auth (if using JWT in SPA, CSRF is less an issue, but if cookies were used, need CSRF tokens).
   - Sets session policy to stateless (each request will be independent, expecting JWT every time).
   - Permits all requests to `/api/auth/**` (we will define login endpoint there). Everything else requires authentication.
   - The `oauth2ResourceServer().jwt()` part tells Spring Security to expect JWT tokens in the `Authorization` header. It integrates with Spring Security’s OAuth2 Resource Server support, which can validate JWTs if properly configured (e.g., with public keys or symmetric secrets).
   - We also define a `PasswordEncoder` bean to hash passwords (using BCrypt).

3. **UserDetailsService**: Spring Security needs a way to load user details (username, password, roles) from our database. We can create a service that implements `UserDetailsService`:

   ```java
   @Service
   public class MyUserDetailsService implements UserDetailsService {
       @Autowired
       private UserRepository userRepo;

       @Override
       public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
           User user = userRepo.findByUsername(username)
                     .orElseThrow(() -> new UsernameNotFoundException("User not found"));
           return new org.springframework.security.core.userdetails.User(
                     user.getUsername(),
                     user.getPassword(),
                     Collections.singletonList(new SimpleGrantedAuthority(user.getRole())));
       }
   }
   ```

   This uses our `UserRepository` to fetch a user and then returns a Spring Security `User` (which implements `UserDetails`), including the username, hashed password, and authorities (roles). We assume each user has one role stored as string like "ROLE_ADMIN".

   We should also ensure our `SecurityConfig` knows to use this service. Since Spring Boot auto-config will pick it up if it’s a bean, we might not need extra config, but if needed:

   ```java
   http.userDetailsService(myUserDetailsService);
   ```

   or use `AuthenticationManagerBuilder` to set it. In newer Spring Security (post Spring Security 5.7), one might instead expose an `AuthenticationManager` with a `UserDetailsService` and `PasswordEncoder` combination.

4. **Auth Controller**: Create a controller with an endpoint for login (and optionally signup if needed).

   ```java
   @RestController
   @RequestMapping("/api/auth")
   public class AuthController {
       @Autowired
       private AuthenticationManager authenticationManager; // need to configure this as a bean
       @Autowired
       private JwtUtil jwtUtil; // a utility to generate JWT tokens

       @PostMapping("/login")
       public ResponseEntity<?> login(@RequestBody LoginRequest loginReq) {
           try {
               Authentication auth = authenticationManager.authenticate(
                   new UsernamePasswordAuthenticationToken(loginReq.getUsername(), loginReq.getPassword()));
               // If we reach here, auth was successful
               org.springframework.security.core.userdetails.User userDetails =
                       (org.springframework.security.core.userdetails.User) auth.getPrincipal();
               String token = jwtUtil.generateToken(userDetails.getUsername(), userDetails.getAuthorities());
               return ResponseEntity.ok(new JwtResponse(token));
           } catch (BadCredentialsException ex) {
               return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
           }
       }
   }
   ```

   For this to work, we need to define `AuthenticationManager` as a bean. In Spring Boot, one approach is:

   ```java
   @Bean
   public AuthenticationManager authManager(HttpSecurity http) throws Exception {
       return http.getSharedObject(AuthenticationManagerBuilder.class)
                 .userDetailsService(myUserDetailsService)
                 .passwordEncoder(passwordEncoder())
                 .and()
                 .build();
   }
   ```

   Or use `AuthenticationConfiguration`:

   ```java
   @Bean
   public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
       return config.getAuthenticationManager();
   }
   ```

   The `LoginRequest` is a simple DTO with `username` and `password` fields, and `JwtResponse` could be a DTO with a `token` field.

5. **JWT Utility**: We need to generate and validate JWT tokens. We can use the Java JWT library (e.g., JJWT or Auth0's JWT library). A simple util using JJWT:

   ```java
   @Component
   public class JwtUtil {
       private final String SECRET_KEY = "very_secret_key_123"; // Ideally from config
       private final long EXPIRATION_MS = 3600000; // 1 hour

       public String generateToken(String username, Collection<? extends GrantedAuthority> authorities) {
           return Jwts.builder()
               .setSubject(username)
               .claim("roles", authorities.stream().map(GrantedAuthority::getAuthority).toList())
               .setIssuedAt(new Date())
               .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_MS))
               .signWith(SignatureAlgorithm.HS512, SECRET_KEY.getBytes())
               .compact();
       }

       public String validateTokenAndGetUsername(String token) {
           try {
               Claims claims = Jwts.parser()
                   .setSigningKey(SECRET_KEY.getBytes())
                   .parseClaimsJws(token)
                   .getBody();
               return claims.getSubject();
           } catch (JwtException e) {
               return null; // token invalid
           }
       }
   }
   ```

   This `JwtUtil` provides token generation and validation. It includes user roles in the token claims (so the frontend or backend could use that info if needed, though backend can always load roles from DB too).

6. **Testing Auth**:
   - Register a user in the database (through a migration or a separate signup endpoint).
   - Call `POST /api/auth/login` with JSON `{"username": "admin", "password": "password"}`.
   - If credentials match, you get a JWT token in response.
   - Then call a secure endpoint, e.g. `GET /api/invoices`, with header `Authorization: Bearer <token>`. If token is valid, you get data; if missing or invalid, you get 401 Unauthorized.

Spring Security’s filters will automatically validate the JWT if we use the `oauth2ResourceServer().jwt()` approach _and_ configure the JWT decoder. For a simpler approach, one can also manually intercept the requests with a filter to validate tokens. But using the built-in is cleaner:

- Add config to application properties for JWT decoding if using asymmetric key (e.g., if you had an authorization server). For symmetric (shared secret as above), can configure a `NimbusJwtDecoder` bean.

For our scope, the above is a sufficient outline. **Note**: If using OAuth2 with an external provider (like Google login), you'd configure `oauth2Login()` and clients, which is a different flow.

**Security Best Practices (quick preview)**: Use strong hashing for passwords (BCrypt is good), don’t embed sensitive info in JWT (like password or personal data, only use claims you need), and keep JWT expiration short – typically a few minutes or hours, not days. Consider using refresh tokens if you need longer sessions.

### Role-Based Access Control

With authentication in place, implementing **role-based access control (RBAC)** ensures that only authorized users (with the right roles) can access certain endpoints or perform certain actions.

In Spring Security:

- We gave each `User` a `role` (like "ROLE_USER", "ROLE_ADMIN"). These roles become **authorities** in Spring Security terms.
- In our `SecurityConfig`, we permitted all authenticated users to every endpoint (except the auth endpoints). We can tighten this:

  ```java
  .authorizeHttpRequests(auth -> auth
      .requestMatchers("/api/admin/**").hasRole("ADMIN")
      .requestMatchers("/api/**").hasRole("USER")
      .anyRequest().authenticated())
  ```

  This assumes standard role prefix “ROLE\_” is used under the hood. `.hasRole("ADMIN")` actually checks for authority "ROLE_ADMIN".

- If we want fine-grained control at the method level, we can use annotations:

  - `@PreAuthorize` on controller or service methods. For example:

    ```java
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/api/invoices/{id}")
    public ResponseEntity<Void> deleteInvoice(@PathVariable Long id) { ... }
    ```

    This ensures only admins can delete invoices. We enabled method security with `@EnableMethodSecurity` earlier to use this.

  - We could also use `@PreAuthorize("hasAuthority('ROLE_ADMIN')")` interchangeably.

- For a UI perspective, the frontend will likely also hide or show actions based on the logged-in user’s role (we’ll handle that in frontend section). The token might include the role, or we can have an API endpoint like `/api/auth/me` that returns the user profile including role.

**Additional RBAC considerations**:

- More complex systems use a separate **Role** entity and perhaps **Privileges**. For our needs, a single role string is enough.
- You might want to restrict certain operations like only allow a user to see their own invoices (if multi-tenant or multi-user system). That goes into permission-based access. E.g., `@PreAuthorize("#user.id == authentication.principal.id")` in SpEL can check the current logged-in user’s id matches the resource’s owner id. This is beyond scope, but be aware of it.
- Always validate on backend; even if frontend hides a button, a malicious user could still call the API, so backend must enforce roles properly.

### Performance Optimizations (Caching, Database Indexing)

As the system grows, performance tuning becomes important. Two low-hanging optimizations are **caching** frequently accessed data and creating proper **database indexes**.

#### Caching with Spring Cache

Spring Boot supports a caching abstraction (Spring Cache) that can be used with various providers (like ConcurrentHashMap for simple cache, or Ehcache, Caffeine, Redis for more robust solutions).

**Enabling Caching**:

1. Add `@EnableCaching` in your main application class or a config class. This enables Spring’s annotation-driven cache management.
2. Choose a cache provider. If none specified, Spring Boot will use a simple ConcurrentMap cache by default. For production, you might use Redis or Ehcache, but let's illustrate with the simple one for now.
3. Use `@Cacheable`, `@CacheEvict`, `@CachePut` annotations on service methods to cache results. Example:

   ```java
   @Service
   public class InvoiceService {
       ...
       @Cacheable(value = "invoices", key = "#id")
       public Invoice getInvoice(Long id) {
           // This method will be cached after first invocation
           return invoiceRepo.findById(id)...
       }

       @CacheEvict(value = "invoices", key = "#id")
       public void deleteInvoice(Long id) {
           invoiceRepo.deleteById(id);
       }
   }
   ```

   Here, `getInvoice` results are stored in cache named "invoices" keyed by the invoice id. Subsequent calls with same id will return cached Invoice without hitting the database (until the cache is evicted). When we delete an invoice, we evict it from cache to avoid stale data.

   We could also cache the list of invoices (`listInvoices`), etc., depending on access patterns. Be cautious to evict or update caches on any change to underlying data.

**Benefits**: Caching can significantly **speed up response times** and reduce load on the database by avoiding repetitive queries for frequently accessed data. For example, if many users frequently access the same invoice or list of invoices, caching those can dramatically enhance performance and scalability.

**Cache Provider**: In a real deployment, something like **Redis** can be used as a cache store, especially in a distributed system (multiple app instances). You’d add spring-boot-starter-data-redis and configure it, then Spring Cache will use it. This is beyond our scope, but keep it in mind.

#### Database Indexing

We touched on indexing earlier but to reiterate: indexing is crucial for database performance:

- **What is an index?** An index on a database column (or set of columns) is a data structure that allows quick lookup of rows based on those columns, at the cost of additional storage and slight overhead on writes. Think of it like an index in a book - it helps find information fast.
- **When to index?** Index columns that you frequently search by or join on. Primary keys are automatically indexed. Foreign keys (like `invoice.customer_id`) should be indexed to speed up joins. Columns used in `WHERE` clauses for filtering results (e.g., `status`, `date`) can benefit from indexes.
- **How to add index?** With Flyway, you can add in a migration:
  ```sql
  CREATE INDEX idx_invoice_status ON invoices(status);
  CREATE INDEX idx_invoice_customer ON invoices(customer_id);
  ```
  This creates indexes for invoice status and customer foreign key.
- **Verify performance**: Use EXPLAIN on SQL queries to see if indexes are used. If you have a query that is slow, often adding an appropriate index can reduce the time from seconds to milliseconds by avoiding full table scans.

Be mindful that **over-indexing** can hurt insert/update performance (every time you insert a row, indexes must update too). So index wisely based on query patterns.

For our invoice system:

- Likely queries: fetch invoices by customer, by status (like show all unpaid), by date range. So indexing `customer_id`, `status`, `date` on invoices makes sense.
- Searching customers by name might require index on customer.name if we implement that feature.
- If implementing search on invoice items, maybe index description (but full-text search could be another approach for that).

### Exercises

- **Exercise 2.1 – Create Entities**: Based on the described entities (User, Customer, Invoice, InvoiceItem), implement them in code with proper JPA annotations. Then, create and run a Flyway migration to generate the corresponding tables. Verify that the tables and columns appear in your MySQL database.
- **Exercise 2.2 – Repository Queries**: Write a custom query method in `InvoiceRepository` to find invoices by status (e.g., `List<Invoice> findByStatus(String status)`). Write a test or a main method snippet to call this and print results (you can insert some test data first).
- **Exercise 2.3 – Secure an Endpoint**: Modify the `InvoiceController` such that the delete operation is only allowed for admin users. Use Spring Security annotations or configuration to enforce this. Test it by calling the delete endpoint with and without an admin role.
- **Exercise 2.4 – Enable Caching**: Enable Spring’s cache in the application and apply caching to one of the service methods (e.g., cache an invoice by id). Simulate calling it twice and observe (maybe via logs) that the repository is hit only once for the same id.
- **Exercise 2.5 – Index Analysis**: Suppose retrieving all unpaid invoices is slow. Determine which database index could help. Write the SQL to create that index. How would you incorporate that into a Flyway migration (which version)?

---

## Chapter 3: Frontend Development (React + TypeScript)

This chapter focuses on building the frontend of our invoice management system using **React** with **TypeScript**. We will set up the project using Vite for a fast development experience. We’ll implement state management using Context API or Redux depending on complexity, and integrate our REST API using libraries like Axios and React Query for data fetching and caching. We’ll also cover UI design using Tailwind CSS (a utility-first CSS framework) and Material UI (component library) to make our application look professional. Additionally, we’ll manage forms with Formik and Yup (for easy form state and validation). Finally, we’ll ensure our components are robust by writing tests with Jest and React Testing Library.

### Setting up React Project with Vite

[Vite](https://vite.dev/) is a modern build tool that provides a lightning-fast development server and optimized build for React (and other frameworks). It’s a great alternative to Create React App, especially for advanced projects.

**Create a new React+TypeScript project**:

1. Make sure you have Node.js and npm installed.
2. Run the following command:
   ```
   npm create vite@latest
   ```
   This will prompt you for a project name and framework options.
3. Select the framework as **React** and variant as **React + TypeScript** when prompted. For example, you might name your project `invoice-system-frontend`.
4. Change directory into the project and install dependencies:

   ```
   cd invoice-system-frontend
   npm install
   npm run dev
   ```

   The `npm create vite` command already installed the basic dependencies (React, ReactDOM, Vite). `npm run dev` should start the dev server (usually on port 5173 or as indicated in console).

5. Open the URL (e.g., http://localhost:5173/) and you should see the default Vite/React welcome page, confirming that setup is successful.

The project structure will look like:

```
invoice-system-frontend/
├── index.html
├── src/
│   ├── main.tsx        (entry point)
│   ├── App.tsx         (root component)
│   ├── assets/         (for static assets if any)
│   └── ...
├── package.json
├── tsconfig.json       (TypeScript config)
└── vite.config.ts      (Vite config)
```

**TypeScript** is integrated, meaning you can start writing `.tsx` and `.ts` files. If you’re using VSCode or another IDE, ensure it’s picking up the tsconfig and providing intellisense.

**Project Configuration**:

- **Absolute Paths**: You might configure path aliases in vite.config and tsconfig for easier imports (e.g., `@/components` to refer to src/components).
- **Linting/Formatting**: It’s good to add ESLint and Prettier for code quality (optional for this guide, but recommended).
  - `npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-react`
  - Then set up an `.eslintrc.js` accordingly.
- **Testing Setup**: We’ll discuss Jest later; Vite can work with Jest or you can use Vitest (Vite’s own testing framework).

### State Management (React Context API vs Redux)

As our app grows, we need a strategy for managing state. This includes:

- Auth state (e.g., current logged-in user, auth token).
- UI state (like a toggle for dark mode, etc.).
- Data state (list of invoices, current invoice being viewed/edited, etc.).

We have two primary options:

- **React Context API**: Built-in mechanism for passing state deeply without prop drilling. It’s great for simpler state or things like theme, current user, etc.
- **Redux**: A state management library for more complex state needs with predictable updates via actions and reducers. Good for large apps with many state transitions.

**Context API**:
We can create contexts for, say, Auth and maybe for global app settings. Context is not exactly a full state management solution by itself; it just provides a way to share state. But combined with `useReducer` (for complex logic) or simple state, it can handle moderate needs.

Use Context when:

- The state is relatively small/simple.
- Only a few parts of the app need it.
- You want to avoid adding external dependencies.

**Redux**:
Redux shines in larger applications where multiple components across the app need to coordinate updates. Redux introduces a single store and actions to modify that store. It adds some boilerplate but provides powerful devtools for debugging state changes and a structured approach.

Use Redux when:

- The application state is large and frequently updated by different parts of the app.
- You want a central source of truth for all data and predictable state transitions.
- There’s a lot of user interactions that change state (forms, filters, etc. all in combination).

In our invoice app:

- If it's primarily forms and API calls, Context might suffice (for auth token, user info).
- If we anticipate features like offline support, complex caching beyond what React Query provides, or very intricate UI state, Redux might help.

Both can co-exist too (e.g., use Context for theme and Redux for data). But to keep it coherent, we might choose one.

For demonstration, let's proceed with a mix: use Context for authentication and global config, and use React Query for server state (data from API). React Query itself can often replace the need for Redux in many apps by handling data fetching and caching.

**Setting up Context (for Auth)**:
Create `src/context/AuthContext.tsx`:

```tsx
import React, { createContext, useState, useContext, ReactNode } from "react";

interface AuthContextType {
  user: string | null; // could be an object with more user info
  token: string | null;
  login: (username: string, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const login = (username: string, token: string) => {
    setUser(username);
    setToken(token);
    // maybe store token in localStorage for persistence
    localStorage.setItem("authToken", token);
    localStorage.setItem("username", username);
  };
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("authToken");
    localStorage.removeItem("username");
  };

  const value = { user, token, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
```

This context provides `user` and `token` state, and functions to login/logout (which update state and also sync with localStorage). We would wrap our app with `<AuthProvider>` in `main.tsx`:

```tsx
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
```

Now any component can call `const { user, token, login, logout } = useAuth();` to get or set auth info.

We’ll use this to store the JWT and current user after login, and to check if user is logged in for protecting routes.

**Redux (optional)**:
If we opted for Redux, we'd:

- Install Redux Toolkit: `npm install @reduxjs/toolkit react-redux`.
- Create a store with slices for different data (invoiceSlice, customerSlice, authSlice).
- Use `<Provider store={store}>` at root.
- Dispatch actions for things like `invoiceAdded`, `invoiceUpdated`, etc.
  Redux Toolkit simplifies a lot of boilerplate and uses Immer for immutable updates, which is helpful. But given our context + React Query approach, we may not need it. Keep in mind though: **Context API is light-weight and good for small to medium apps, whereas Redux is more robust for complex state**.

### API Integration with Axios and React Query

Our React app needs to communicate with the Spring Boot API. We will use **Axios** for making HTTP requests and **React Query** (now called TanStack Query) to handle the fetching and caching logic.

**Axios Setup**:

1. Install axios: `npm install axios`.
2. Create an Axios instance configured with base URL and perhaps an interceptor to attach the JWT token to headers:

   ```ts
   // src/api/axios.ts
   import axios from "axios";
   import { getAuthToken } from "./authToken"; // a function to get token (maybe from localStorage or context)

   const apiClient = axios.create({
     baseURL: "http://localhost:8080/api", // base URL for API
   });

   // Add a request interceptor to include JWT token if available
   apiClient.interceptors.request.use((config) => {
     const token = getAuthToken();
     if (token && config.headers) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });

   export default apiClient;
   ```

   Here `getAuthToken` might simply do `localStorage.getItem('authToken')`. Alternatively, we could integrate context directly by making this interceptor dynamic (or we pass the token in from context to our data fetching functions). The localStorage approach ensures token persists on refresh.

**React Query Setup**:

1. Install react-query (TanStack Query): `npm install @tanstack/react-query`.
2. Set up the QueryClient and QueryClientProvider at the root of the app:
   ```tsx
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
   const queryClient = new QueryClient();
   ReactDOM.createRoot(...).render(
     <React.StrictMode>
       <AuthProvider>
         <QueryClientProvider client={queryClient}>
           <App />
         </QueryClientProvider>
       </AuthProvider>
     </React.StrictMode>
   );
   ```
3. Use React Query in components or custom hooks for data fetching:

   - **Fetching list of invoices**:

     ```tsx
     import { useQuery } from "@tanstack/react-query";
     import apiClient from "../api/axios";

     const useInvoices = () => {
       return useQuery(["invoices"], async () => {
         const response = await apiClient.get("/invoices");
         return response.data;
       });
     };
     ```

     This custom hook `useInvoices` returns the query object from `useQuery`. Under the hood, `useQuery` will:

     - Fetch from `/api/invoices` (with Axios).
     - Cache the result with key 'invoices'.
     - While fetching (or on refetch), handle loading state and error state.
     - Re-fetch data automatically in certain conditions (e.g., if the user refocuses the tab, by default).
       It greatly simplifies data fetching and caching logic in the UI.

     In a component, we could do:

     ```tsx
     const InvoicesPage: React.FC = () => {
       const { data: invoices, isLoading, error } = useInvoices();
       if (isLoading) return <p>Loading...</p>;
       if (error) return <p>Error loading invoices</p>;
       return (
         <ul>
           {invoices.map((inv) => (
             <li key={inv.id}>
               {inv.invoiceNumber} - {inv.totalAmount}
             </li>
           ))}
         </ul>
       );
     };
     ```

     React Query ensures `invoices` is cached, so if this component unmounts and remounts, it may use cached data first. Also it can do background refresh. All configurable via the `useQuery` options (like `staleTime`, etc.). It's often described as _“the missing data-fetching library for React”_, handling caching, deduping, and updating of asynchronous data.

   - **Mutation (creating an invoice)**: React Query offers `useMutation` for posts/puts:

     ```tsx
     import { useMutation, useQueryClient } from "@tanstack/react-query";

     const useCreateInvoice = () => {
       const queryClient = useQueryClient();
       return useMutation(
         async (newInvoice) => {
           const response = await apiClient.post("/invoices", newInvoice);
           return response.data;
         },
         {
           onSuccess: () => {
             // Invalidate or update the invoices list query to refetch new data
             queryClient.invalidateQueries(["invoices"]);
           },
         }
       );
     };
     ```

     In a component:

     ```tsx
     const { mutate: createInvoice, isLoading: isCreating } =
       useCreateInvoice();
     const handleSubmit = (formData) => {
       createInvoice(formData);
     };
     ```

     This will call the API and on success, automatically refresh the invoices list via `invalidateQueries`.

**Protecting Routes**:
For pages that require auth (like viewing invoices), we should ensure the user is logged in. In a single-page app, we might use React Router for navigation:

- Install react-router: `npm install react-router-dom`.
- Define routes, e.g., some routes may be wrapped in a component that checks `authContext.token`. Or use a pattern like:

  ```tsx
  <Route
    path="/invoices"
    element={
      <PrivateRoute>
        <InvoicesPage />
      </PrivateRoute>
    }
  />
  ```

  Where `PrivateRoute` is a component that checks auth:

  ```tsx
  const PrivateRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
    const { token } = useAuth();
    if (!token) {
      return <Navigate to="/login" />;
    }
    return children;
  };
  ```

  This will redirect to login if no token (not authenticated).

- The login page will use the `AuthContext.login` method after a successful API call to login.

**Example Login process (frontend)**:

```tsx
const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await apiClient.post("/auth/login", { username, password });
      const token = res.data.token;
      login(username, token);
      // maybe redirect to dashboard
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleLogin();
      }}
    >
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
};
```

This simplistic login form calls the backend and uses context to store the token. After login, future Axios calls carry the token (thanks to the interceptor). We’d also configure Axios to handle 401 responses globally (e.g., if token expired, maybe logout).

### UI Design with Tailwind CSS and Material UI

We want our app to be visually appealing and responsive. We’ll use **Tailwind CSS** for rapid UI styling and possibly **Material UI (MUI)** components for complex UI elements (like modals, tables, etc.).

#### Tailwind CSS Setup

1. Install Tailwind: `npm install tailwindcss postcss autoprefixer`
2. Initialize Tailwind config: `npx tailwindcss init -p` (this creates `tailwind.config.js` and `postcss.config.js`).
3. Configure `tailwind.config.js` if needed (e.g., specify paths to your content so Tailwind can tree-shake unused styles):
   ```js
   module.exports = {
     content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
     theme: {
       extend: {},
     },
     plugins: [],
   };
   ```
4. In your CSS (you can create `src/index.css` or similar), include Tailwind directives:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
   Import this CSS in your entry (e.g., in `main.tsx`, `import './index.css';`).
5. Now you can use Tailwind classes in your JSX. Tailwind is a **utility-first CSS** framework, meaning it provides lots of small CSS classes for common styles (padding, margin, color, flex, grid, etc.) that you compose in your HTML/JSX.

Example:

```tsx
<div className="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
  <div className="flex-shrink-0">
    <!-- an icon or avatar -->
  </div>
  <div>
    <div className="text-xl font-medium text-black">Invoice #1001</div>
    <p className="text-gray-500">Due: 2025-03-01</p>
  </div>
</div>
```

This uses classes: padding-6, max-width small, centered block, white background, rounded corners, shadow, flex layout with items centered, etc. The advantage is you rarely leave your JSX to write separate CSS. It's quick to prototype and consistent. **Utility classes** mean you build custom designs by mixing and matching small class names.

Tailwind also allows customization (in the config, you can define theme colors, spacing scale, etc.) and adding custom utilities or components if needed.

#### Material UI Integration

Material UI (now officially called MUI) is a popular React component library that implements Google’s Material Design out of the box. It provides pre-built components like buttons, dialogs, tables, etc., which can save a lot of time.

To use MUI:

1. Install MUI core and icons: `npm install @mui/material @mui/icons-material @emotion/react @emotion/styled`
   (MUI uses Emotion for styling under the hood).
2. You can now import components and use them. For example:

   ```tsx
   import Button from "@mui/material/Button";
   import TextField from "@mui/material/TextField";

   function CustomerForm() {
     return (
       <form>
         <TextField label="Name" variant="outlined" />
         <TextField label="Email" variant="outlined" type="email" />
         <Button variant="contained" color="primary" type="submit">
           Save
         </Button>
       </form>
     );
   }
   ```

   This gives you styled input fields and a button without writing CSS.

MUI components are themable and accessible. You can use their default styling or customize the theme to match your brand. MUI encourages following a design system and Material Design principles.

We can mix Tailwind and MUI. For instance, use MUI for complex components, and Tailwind for overall layout or where MUI doesn’t provide something easily. Some developers choose one or the other, but they can co-exist (just be mindful to override MUI styles as needed if using Tailwind on MUI components).

**Example: Invoice List UI**:
Suppose we want to display invoices in a nice table with pagination – MUI provides a DataGrid or Table components:

```tsx
import { DataGrid, GridColDef } from "@mui/x-data-grid";

const columns: GridColDef[] = [
  { field: "invoiceNumber", headerName: "Invoice #", width: 130 },
  { field: "customerName", headerName: "Customer", width: 180 },
  { field: "date", headerName: "Date", width: 130 },
  { field: "totalAmount", headerName: "Total ($)", width: 130 },
  { field: "status", headerName: "Status", width: 100 },
];

const InvoiceTable: React.FC = () => {
  const { data: invoices, isLoading } = useInvoices();
  if (isLoading) return <CircularProgress />; // MUI loading spinner
  const rows = invoices.map((inv) => ({
    id: inv.id,
    invoiceNumber: inv.invoiceNumber,
    customerName: inv.customer ? inv.customer.name : "",
    date: inv.date,
    totalAmount: inv.totalAmount,
    status: inv.status,
  }));
  return (
    <div style={{ height: 400, width: "100%" }}>
      <DataGrid rows={rows} columns={columns} pageSize={5} checkboxSelection />
    </div>
  );
};
```

Here we use MUI’s DataGrid component for a paginated table. MUI’s approach provides a lot of functionality out of the box.

**Responsive Design**:
Tailwind includes utility classes for responsiveness (like `md:p-4` means padding 4 on medium screens, `sm:text-center` etc.). We should design the layout to be responsive. For instance, on smaller screens, maybe the invoice table becomes a list of cards instead of a wide table.

We can achieve that by combining CSS Grid or Flex with Tailwind’s responsive utilities. E.g.:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {invoices.map((inv) => (
    <div key={inv.id} className="p-4 border rounded">
      <h3 className="font-bold">{inv.invoiceNumber}</h3>
      <p>Customer: {inv.customer?.name}</p>
      <p>Total: ${inv.totalAmount}</p>
      <p>Status: {inv.status}</p>
    </div>
  ))}
</div>
```

This would show one invoice per row on small screens, two per row on medium, three on large, with some gap between, using Tailwind classes.

### Form Handling with Formik and Yup

Invoices and customers will involve forms (for data entry/editing). Managing form state and validation can be tedious. **Formik** is a popular library to manage form state in React, and **Yup** is a schema validation library that pairs well with Formik for form validation.

**Install**: `npm install formik yup`

**Creating a form with Formik**:
Let’s create a form for adding/editing an invoice.

Formik has two main approaches:

- Using the `<Formik>` component and render prop or children function.
- Using the `useFormik` hook.

We’ll use the hook here for clarity:

```tsx
import { useFormik } from "formik";
import * as Yup from "yup";

const InvoiceSchema = Yup.object().shape({
  invoiceNumber: Yup.string().required("Required"),
  date: Yup.date().required("Required"),
  customerId: Yup.number().required("Required"),
  items: Yup.array().of(
    Yup.object().shape({
      description: Yup.string().required(),
      quantity: Yup.number().min(1).required(),
      unitPrice: Yup.number().min(0).required(),
    })
  ),
});

const InvoiceForm: React.FC<{
  initialData?: InvoiceType;
  onSubmit: (data: InvoiceType) => void;
}> = ({ initialData, onSubmit }) => {
  const formik = useFormik({
    initialValues: initialData || {
      invoiceNumber: "",
      date: "",
      customerId: "",
      items: [{ description: "", quantity: 1, unitPrice: 0 }],
    },
    validationSchema: InvoiceSchema,
    onSubmit: (values) => {
      onSubmit(values);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} className="space-y-4">
      <div>
        <label className="block font-medium">Invoice Number</label>
        <input
          name="invoiceNumber"
          value={formik.values.invoiceNumber}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          className="border p-2 w-full"
        />
        {formik.touched.invoiceNumber && formik.errors.invoiceNumber ? (
          <div className="text-red-500 text-sm">
            {formik.errors.invoiceNumber}
          </div>
        ) : null}
      </div>
      <div>
        <label className="block font-medium">Date</label>
        <input
          type="date"
          name="date"
          value={formik.values.date}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          className="border p-2"
        />
        {formik.touched.date && formik.errors.date ? (
          <div className="text-red-500 text-sm">{formik.errors.date}</div>
        ) : null}
      </div>
      <div>
        <label className="block font-medium">Customer</label>
        <select
          name="customerId"
          value={formik.values.customerId}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          className="border p-2"
        >
          <option value="">Select Customer</option>
          {/* Assume we have a list of customers in state to map here */}
          {customers.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        {formik.touched.customerId && formik.errors.customerId ? (
          <div className="text-red-500 text-sm">{formik.errors.customerId}</div>
        ) : null}
      </div>
      {/* Invoice items can be complex; for brevity, handle one item or allow adding items dynamically */}
      <div>
        <label className="block font-medium">Item 1 Description</label>
        <input
          name="items[0].description"
          value={formik.values.items[0].description}
          onChange={formik.handleChange}
          className="border p-2 w-full"
        />
        {/* similarly inputs for quantity, unitPrice */}
      </div>
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Save Invoice
      </button>
    </form>
  );
};
```

Points:

- We define a Yup schema `InvoiceSchema` to enforce that fields are required and numbers have minimum values, etc.
- `useFormik` is given the initial values, validation schema, and onSubmit handler.
- `formik.handleChange` and `formik.handleBlur` manage updating the state and marking fields as touched.
- We display validation errors from `formik.errors` if the field was touched. Formik + Yup integration automatically populates those errors by running the schema against the values.
- This approach simplifies a lot of boilerplate: we don't manually track `errors` or `touched` for each field; Formik does it. And Yup provides declarative validation rules. On form submission, if validation fails, `formik.errors` will be populated and form not submitted until errors resolved.

Formik also supports array fields well and you can use `<FieldArray>` for managing the list of invoice items (adding/removing).

**Yup for Validation**:
Yup allows building a schema matching our data structure. It provides chainable validators (required, min, matches regex, etc.). This encourages defining validation logic in a single place (the schema) rather than scattered checks. It’s quite powerful (supports conditional validation, custom tests, etc.).

Example: We could add a conditional validation: if status is "PAID", maybe require a payment date, etc. Yup can do that.

**Formik in practice**:
Using Formik, the form state (values, errors) is contained in the hook. This prevents a lot of repetitive useState for each form field. It also makes it easy to show aggregate form state (like a submit disabled until no errors).

By integrating Formik with MUI, one can use MUI's TextField components and feed them the Formik props (MUI even has an example integration with Formik, or one can wrap TextField to show errors easily).

Overall, Formik and Yup combined result in cleaner, more maintainable form management and validation in React.

### Component Testing with Jest and React Testing Library

After building our UI, we need to ensure it works as expected. Automated tests for components and utilities help catch regressions. We’ll use **Jest** as the test runner and **React Testing Library (RTL)** for testing components in a way that mimics user interaction.

**Setup**:

- If using Create React App, Jest is already configured. In Vite, we might integrate Vitest or configure Jest manually. For this guide, assume we set up Jest.
- Install: `npm install --save-dev jest @types/jest ts-jest react-testing-library @testing-library/react @testing-library/jest-dom`.

We then configure a Jest config (if needed) to work with TSX (ts-jest can help). Also, import `@testing-library/jest-dom` in tests for additional matchers.

**Writing a test**:
Let's write a simple test for our `<InvoiceForm>` component to ensure validation works.

```tsx
// InvoiceForm.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { InvoiceForm } from "./InvoiceForm";

test("InvoiceForm shows validation errors on submit if required fields are missing", () => {
  render(<InvoiceForm onSubmit={jest.fn()} />);

  // Assuming the form has an invoiceNumber and date field and a submit button
  const submitButton = screen.getByText(/Save Invoice/i);
  fireEvent.click(submitButton);

  // After clicking submit without filling, we expect validation errors to show
  const errorMsg = screen.getByText(/Required/);
  expect(errorMsg).toBeInTheDocument();
});
```

This test:

- Renders the component.
- Simulates a user clicking the submit button without entering data.
- Expects that a "Required" error message appears (assuming our Yup schema triggers error messages that contain "Required").
- We use `screen.getByText` from RTL to query elements as a user would see them (by visible text). RTL encourages testing the UI from the user’s perspective, rather than relying on component internals or specific IDs unnecessarily. This makes tests more resilient to changes in implementation and focused on behavior.

Another test could simulate filling in fields and then ensure `onSubmit` is called with correct data when form is valid:

```tsx
test("InvoiceForm calls onSubmit with form data when valid", () => {
  const handleSubmit = jest.fn();
  render(<InvoiceForm onSubmit={handleSubmit} />);

  // Fill form fields
  fireEvent.change(screen.getByLabelText(/Invoice Number/i), {
    target: { value: "INV-123" },
  });
  fireEvent.change(screen.getByLabelText(/Date/i), {
    target: { value: "2025-01-01" },
  });
  fireEvent.change(screen.getByLabelText(/Customer/i), {
    target: { value: "1" },
  }); // selecting a customer

  fireEvent.click(screen.getByText(/Save Invoice/i));

  expect(handleSubmit).toHaveBeenCalled();
  // We could also inspect handleSubmit.mock.calls[0][0] for the form data values.
});
```

We used `getByLabelText` which finds input by its label content (assuming <label> has text and is associated). This is a recommended way as it mirrors how users associate fields by label.

**Component Testing Tips**:

- **Test Behavior, Not Implementation**: Ensure you test what the user sees or does (clicking buttons, entering text, seeing output). Avoid testing internal state or private functions.
- **Use `jest-dom` matchers**: like `toBeInTheDocument`, `toHaveClass`, `toBeDisabled` for readability.
- **Test accessibility**: e.g., if a modal opens, focus goes to it, or ARIA roles are present (RTL has queries like `getByRole`).
- **Mock external services**: For components that fetch data (like ones using `useInvoices()`), you might want to mock the React Query hook or the Axios calls. This can be done by mocking modules or passing a different QueryClient in tests.

For instance, to test an invoice list component that uses `useInvoices`, you could provide a custom QueryClient with pre-fetched data or simply mock the module that exports `useInvoices` to return preset data.

**Snapshot Testing** (optional):
Jest can create snapshots of component output to detect unexpected changes. E.g., `expect(container).toMatchSnapshot()`. However, be cautious with snapshot tests – they can become too brittle if overused. Focus more on interactive tests as above.

**Continuous Testing**:
Running `npm test` should run all tests. It's good to integrate this into CI (which we will discuss in the next chapter). Tests give confidence when refactoring or adding features.

### Exercises

- **Exercise 3.1 – Build a Page**: Create a React component for listing all customers. Use React Query to fetch customers from the API, and display them in a table or list. Use Tailwind or MUI to style it nicely.
- **Exercise 3.2 – Form Validation**: Implement a form for adding a new customer with fields Name, Email, etc., using Formik and Yup. Ensure that the email field is validated as a proper email format. Test the form manually by trying to submit invalid data (the UI should show validation errors).
- **Exercise 3.3 – Context Usage**: Use the AuthContext in a Navbar component to conditionally show “Login” or “Logout” buttons. If the user is logged in (context has a user), show “Hello, [username]” and a logout button; if not, show a login link.
- **Exercise 3.4 – Component Test**: Write a test for the customer form component. Simulate entering an invalid email and verify that a validation error appears. Simulate entering a valid email and form submission, and verify that the submission handler was called with the correct data.
- **Exercise 3.5 – Styling Challenge**: Without using MUI components, style a responsive navigation bar using Tailwind. It should collapse into a hamburger menu on mobile. (You don’t have to implement the menu functionality fully, just style it.)

---

## Chapter 4: Security Best Practices

Security should be woven throughout the application. In this chapter, we focus on best practices to ensure our invoice management system is secure. We will cover securing the backend APIs with Spring Security in more depth, including protecting against common vulnerabilities. We’ll also discuss proper data validation and sanitization to prevent injection attacks, and implement rate limiting/throttling to mitigate abuse and DoS attacks.

### Securing REST APIs with Spring Security

We already set up basic JWT authentication in Chapter 2. Now let's expand on best practices for securing REST APIs:

- **Use HTTPS**: Always deploy the application over HTTPS. This ensures tokens and sensitive data aren’t intercepted in plain text. While in development you might use HTTP, in production a TLS certificate is a must.
- **JWT Security**:
  - Choose a strong secret key (for HMAC signing) or use an asymmetric key pair (public/private key) for signing tokens. Do not expose the private key.
  - Set short expiration times on JWTs. A common pattern is access token valid for, say, 15 minutes, and a refresh token (stored securely) to get new tokens. Short-lived tokens minimize damage if stolen.
  - Validate the JWT signature and claims on every request. Spring Security does this if configured properly. If not using the built-in, ensure your filter checks the signature and the `exp` claim.
  - Include necessary claims, e.g., username and roles. Avoid putting sensitive info in the token (like passwords or personal data).
  - Consider token revocation strategies (JWTs by nature are stateless; you might keep a blacklist of tokens or use short expiry with refresh).
- **Limit exposure of endpoints**: Only expose what’s needed. For example, if the public should not create users, ensure that endpoint is either secured or not available at all (depending on requirements).
- **Spring Security Config**:
  - Principle of least privilege: lock down everything by default, then open up as needed.
  - We used `authorizeHttpRequests` to secure URLs. Ensure any new endpoints are covered. If using an admin role, double-check that any admin-only endpoints have the proper `.hasRole('ADMIN')` or similar.
  - Use `@PreAuthorize` on service methods as a secondary measure especially for critical business functions, e.g., `@PreAuthorize("hasRole('ADMIN') or #invoice.customer.id == principal.id")` if implementing that only invoice owners or admins can view an invoice.
  - If using **method level** security with SpEL expressions, validate that `principal` or `authentication` contains what you expect (our `UserDetails` user had username and role, for more info you might extend it to have user ID).
- **Exception Handling**: Customize access denied and unauthorized responses. Spring Security by default might redirect on 403 if not configured for REST. We should configure it to return 401/403 JSON responses. This can be done with `.exceptionHandling()` in `HttpSecurity` config:
  ```java
  http.exceptionHandling()
      .authenticationEntryPoint((req, res, ex) -> res.sendError(HttpServletResponse.SC_UNAUTHORIZED))
      .accessDeniedHandler((req, res, ex) -> res.sendError(HttpServletResponse.SC_FORBIDDEN));
  ```
- **Testing Security**: Use tools or write tests to ensure endpoints are indeed protected. For example, a test that calls `/api/invoices` without a token should get 401. With a normal user token, maybe can get, but cannot delete if that’s admin-only (should get 403).

The key is not just to implement security, but also _not to bypass it_ inadvertently. Be mindful when adding new controllers to apply security. Since we used a global rule that all `/api/**` require auth, new controllers under `/api` automatically are protected unless added to exceptions.

### Data Validation and Sanitization

**Input Validation**:
All input coming from users or external sources should be considered untrusted. This applies to:

- API request bodies and parameters (even if coming from our React app, a malicious actor could craft their own requests).
- Data imported or uploaded (if we had file upload, etc).

Input validation means checking that the data is in the expected format and within expected bounds:

- Use built-in validation frameworks. For Java, JSR 380 Bean Validation (Hibernate Validator) is handy. We can annotate our DTOs or entity classes with constraints:
  ```java
  public class InvoiceDTO {
      @NotBlank
      private String invoiceNumber;
      @FutureOrPresent
      private LocalDate date;
      @Min(1)
      private List<@Valid InvoiceItemDTO> items;
      // ... etc
  }
  ```
  Then in controller, use `@Valid @RequestBody InvoiceDTO dto`. Spring will automatically validate and return 400 Bad Request with errors if validation fails.
- For strings, consider patterns or allowed characters if applicable (e.g., invoice number maybe allow alphanumeric and dashes only).
- For more complex rules, manually check in service method and throw exceptions or return errors as appropriate.

**Sanitization**:
Even with validation, some data might include content that is potentially harmful if used in certain contexts. For example:

- If you display user-provided data in a web page (in our case, maybe invoice item description), it could contain HTML or script. If our React app naively sets `innerHTML` with it, it could run script (XSS).
- Or if data is used in a SQL query without proper ORM parameterization, it could cause SQL injection (though with JPA and prepared statements, that’s less an issue unless you use raw queries and string concatenation).

Sanitization is the process of cleaning data by removing or encoding undesirable parts:

- For output to HTML, use appropriate encoding (React by default escapes content in JSX, so it’s safe as long as you don't use `dangerouslySetInnerHTML`).
- In the backend, if you accept HTML (like a rich text field), use a sanitizer library (OWASP Java HTML Sanitizer, JSoup, etc.) to allow only safe tags.
- For SQL, always use prepared statements or parameter binding (never directly concatenate user input into queries).

**Example**:
If we had an endpoint that searches invoices by customer name via a raw query (not recommended, but for example):

```java
String name = request.getParameter("name"); // unsanitized input
String query = "SELECT * FROM invoices i JOIN customers c ON i.customer_id=c.id WHERE c.name LIKE '%" + name + "%'";
```

If `name` contained something like `John' OR '1'='1`, it could break the query or even return all records. Instead, we should do:

```java
@Query("SELECT i FROM Invoice i WHERE i.customer.name LIKE %:name%")
List<Invoice> searchByCustomerName(@Param("name") String name);
```

Spring Data JPA will handle the parameter safely.

For any raw SQL, use `PreparedStatement` or Spring JDBC template with placeholders.

**AllowList vs DenyList**:

- It’s generally better to define what _is allowed_ (whitelist) rather than trying to catch what’s malicious (blacklist), because new attack patterns emerge. For example, allow only certain characters in an invoice code. If binary data or special characters are needed, handle appropriately (e.g., Base64 encode binary data, etc).
- If an input doesn’t meet criteria, reject it with a clear message.

**Bean Validation in Spring**:
If using `@Valid`, also consider using groups if some fields are required only in certain cases (though that might be overkill for our app).
Additionally, handle the MethodArgumentNotValidException (Spring does by default return a 400 with errors in body in recent versions, due to `@RestControllerAdvice` that Boot configures).

**Sanitize Outputs**:
For logs, be mindful not to log sensitive info. For example, don’t log user passwords (even hashed) or tokens. Also, if logging user input (for debugging), consider that logs could be read by others, so maybe sanitize out things like credit card numbers, etc., if such data existed.

### Rate Limiting and API Throttling

To protect the API from abuse (like someone writing a script to bombard our endpoints, or brute-force passwords, or just accidental high load), implementing rate limiting is important.

**Approaches to Rate Limiting**:

- Server-side in the application: Use a filter or interceptor to count requests per user (or IP) and reject if too many in short time. Libraries like Bucket4j (for Java) can help implement token bucket algorithm for rate limiting.
- API Gateway or Load Balancer: If deployed behind a gateway (like Kong, or cloud API gateway), they often have rate limiting features.
- Reverse proxies like Nginx or CDN services can also enforce basic rate limits.

**We can implement a simple rate limiter filter**:
For example, limit each authenticated user to, say, 100 requests per minute for normal usage:

```java
@Component
@Order(1)
public class RateLimitingFilter extends OncePerRequestFilter {
    private final Cache<String, Integer> requestCounts = CacheBuilder.newBuilder()
            .expireAfterWrite(1, TimeUnit.MINUTES)
            .build();
    // Using Guava Cache as an in-memory store for counts that auto-expires entries every minute

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String user = request.getUserPrincipal() != null ? request.getUserPrincipal().getName() : request.getRemoteAddr();
        // If user is not authenticated, fall back to IP-based limiting.
        Integer count = requestCounts.getIfPresent(user);
        if (count == null) count = 0;
        if (count >= 100) {
            response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            return;
        }
        requestCounts.put(user, count + 1);
        filterChain.doFilter(request, response);
    }
}
```

This is a simplistic example:

- We identify a key (username if logged in, or IP if not).
- Use an in-memory cache to count requests in the last minute.
- If exceeding threshold, return 429 Too Many Requests.
- Otherwise increment count and proceed.

A robust solution would consider:

- Smoothing the limit (e.g., allow bursts but then refill).
- Possibly a longer-term limit too (100/minute and maybe 1000/hour).
- Distributed environment: if you have multiple instances, in-memory won’t be accurate across them. You’d use a shared store (Redis, etc.) or enforce at load balancer.

**Throttling specific endpoints**:

- For login, you might want stricter limit to prevent brute forcing passwords (e.g., no more than 5 login attempts per minute per IP or user).
- For expensive endpoints (maybe generating a large report), limit those differently.

**Exponential Backoff and Client Strategies**:
Clients should handle 429 responses gracefully — e.g., back off and retry after some time (the server can send `Retry-After` header). This isn’t our focus, but just note it.

**Monitoring**:
Track metrics for rate limiting, like how often limits are reached, to adjust thresholds.

**Why Rate Limiting**:
To ensure service availability and fair usage. It prevents one client (or attacker) from overwhelming the system and ensures capacity is shared. Best practices include defining a strategy, identifying clients (API keys or user accounts) to apply limits on, and implementing logic to enforce it.

We should document the limits in API docs (so users know e.g., "API is limited to 100 requests/min per user").

### Exercises

- **Exercise 4.1 – Break Security**: Intentionally try to break your own API security. For example, get a JWT for a normal user and try to delete an invoice via API (which should be admin-only). See if the server correctly returns 403. Try accessing without token, ensure 401. Document what you tried and the outcomes.
- **Exercise 4.2 – Add Validation**: Add Bean Validation annotations to the `Invoice` or `Customer` DTO classes (or entities). For instance, ensure an invoice’s totalAmount is non-negative, customer email is a valid email format (`@Email` annotation). Write a test for the controller (perhaps using MockMvc) to POST invalid data and assert that a 400 Bad Request is returned.
- **Exercise 4.3 – Implement Simple Rate Limiting**: Implement a basic rate limiting mechanism like the filter example above. Test it by creating a small script or loop that calls an endpoint more than the allowed times in a short period, and observe if you start getting HTTP 429 responses.
- **Exercise 4.4 – XSS Awareness**: Assume a user somehow put a script in an invoice item description (e.g., `"><script>alert('xss')</script>`). Render that description in the React app without sanitization. What happens? (Likely React escapes it and you just see the literal tags, which is good). Now, simulate a scenario where unsafe rendering could occur (like using `dangerouslySetInnerHTML`). Learn and note why React's default escaping protects against XSS.
- **Exercise 4.5 – SQL Injection Test**: If you have any search or filter endpoint (for example, a GET filter by query param), try injecting an SQL fragment in the param (like `' OR 1=1--`). Since we are using JPA repositories, it should be safe, but note how you might protect if using dynamic queries.
