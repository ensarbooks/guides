# Building a Multi-Tenant Application with React, TypeScript, Spring Boot, and MySQL

Multi-tenancy is a software architecture where a single application instance serves multiple **tenants** (clients or customer organizations) while keeping each tenant's data isolated. This guide provides a step-by-step walkthrough for advanced developers to build a robust multi-tenant SaaS application using **ReactJS + TypeScript** for the frontend and **Spring Boot + MySQL** for the backend. We will cover key design decisions, setup steps, code examples, and best practices for security, performance, and maintainability.

## 1. Introduction to Multi-Tenancy

Multi-tenant applications allow multiple customer organizations (tenants) to share one application deployment, as opposed to having separate instances per customer. Each tenant feels like they have their own application, but in reality they share the application (and possibly database) with other tenants ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=A%20multi,served%20by%20a%20separate%20instance)). The core challenge is **data isolation** – ensuring tenants can only access their own data.

### Multi-Tenancy Concepts and Models

There are several models to achieve multi-tenancy, primarily differing in how data is partitioned in the database:

- **Database-per-tenant:** Each tenant has a completely separate database. The application connects to different DBs depending on the tenant. This provides strong isolation (one tenant’s data never even resides in the same database as another's) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=2,separate%20but%20otherwise%20identical%20schemas)).
- **Schema-per-tenant (Shared Database, Separate Schema):** Tenants share the same physical database, but each tenant’s data is in a separate schema (namespace). The schemas have identical table structures for each tenant ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=2,separate%20but%20otherwise%20identical%20schemas)). For example, you might have `tenant_a.users` and `tenant_b.users` tables in the same DB.
- **Shared Schema (Discriminator Column):** Tenants share the same database **and** the same tables. Each table includes a **tenant identifier column** to segregate rows belonging to different tenants ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=1,part%20of%20the%20primary%20key)). For instance, a `tenant_id` column in every table is used to filter data in queries.

Each approach has trade-offs. The table below summarizes them:

| **Approach**                      | **Description**                                                                                                 | **Pros**                                                                                                                               | **Cons**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Database per Tenant**           | Separate database for each tenant.                                                                              | _Highest isolation:_ one tenant’s data and workload is fully isolated. Easier to backup/restore per client.                            | More overhead in managing many databases (connections, maintenance). Harder to query across tenants (usually not needed). Scaling to thousands of tenants can be complex due to many DB instances.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Schema per Tenant**             | Shared DB, but separate schema (set of tables) per tenant.                                                      | _Strong isolation:_ no commingling of data in same tables. Only one database server to manage.                                         | Still requires managing schema creation for each tenant. All schemas share server resources (one tenant can impact DB performance for others if not controlled).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Shared Schema (Tenant Column)** | Single database and schema; tenant data distinguished by an attribute (e.g. tenant_id column) in shared tables. | _Simple to implement:_ one set of tables. Easy to add a new tenant (just add data with new tenant_id). Minimizes number of DB objects. | _Weaker isolation:_ bugs in filtering could expose data across tenants. One large set of tables can grow huge (all tenants combined) – requires proper indexing and careful query design to avoid one tenant’s workload affecting others ([Multi-Tenant Architecture - SaaS App Design Best Practices](https://relevant.software/blog/multi-tenant-architecture/#:~:text=of%20tenant%20identifier%20columns%2C%20while,scalability%20to%20a%20greater%20extent)) ([Multi-Tenant Architecture - SaaS App Design Best Practices](https://relevant.software/blog/multi-tenant-architecture/#:~:text=further%20augment%20operational%20management%20and,trial%20tiers%20and%20premium%20subscribers)). |

There are also hybrid strategies (e.g. a mix of separate DB for large tenants and shared schema for small ones) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Of%20course%2C%20you%20can%20dream,simple%20variants%20for%20these%20examples)) ([Multi-Tenant Architecture - SaaS App Design Best Practices](https://relevant.software/blog/multi-tenant-architecture/#:~:text=further%20augment%20operational%20management%20and,trial%20tiers%20and%20premium%20subscribers)), or sharding tenants across multiple databases for scalability ([Multi-Tenant Architecture - SaaS App Design Best Practices](https://relevant.software/blog/multi-tenant-architecture/#:~:text=streamline%20resource%20management.%20,or%20recombined%20just%20as)). The three models above are the most common and will be our focus.

### Choosing the Right Approach

Choosing a multi-tenancy model depends on the use case and requirements:

- **Number of Tenants:** A small number of high-value tenants might justify isolated databases, whereas hundreds or thousands of small tenants are easier to support with a shared schema.
- **Data Volume and Isolation:** If each tenant stores large volumes of data or has strict data isolation requirements (regulatory or security concerns), **DB-per-tenant** provides the best isolation. For moderate isolation needs, **schema-per-tenant** suffices, and for low-risk scenarios, a **shared schema** is simplest.
- **Tenant Workload Variability:** If one tenant could generate heavy load (queries or traffic) that might impact others, isolation at DB or schema level can prevent the “noisy neighbor” problem. In a shared table model, you must rely on query optimizations and maybe resource quotas to mitigate this.
- **Operational Complexity:** Shared schema is easiest to operate (one database to manage), whereas schema-per-tenant and DB-per-tenant require automating database or schema provisioning for each new tenant and tracking those. Consider your DevOps maturity – if you can automate database deployments and migrations, multiple schemas/DBs are feasible.
- **Deployment Flexibility:** With separate databases, you could host some tenant databases on different servers or regions (useful if tenants require data in specific locations). Shared schema ties all tenants to the same database server.
- **Hybrid Needs:** You may decide on a hybrid: e.g., start with shared schema for all to simplify onboarding, but migrate a tenant to their own schema or DB if they grow large or require dedicated performance ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Of%20course%2C%20you%20can%20dream,simple%20variants%20for%20these%20examples)).

For example, if building an enterprise SaaS where each customer is big and demands strict data isolation, you might choose **schema-per-tenant** for a balance of isolation and manageability. On the other hand, a self-service SaaS with many small customers might use **shared schema** with a tenant ID column for simplicity and then scale by sharding or moving heavy tenants to separate schemas later.

**Key takeaway:** There's no one-size-fits-all – evaluate security, scalability, and complexity. This guide will assume a design where tenants share the application server, and we will illustrate patterns for either separate schemas or a shared schema approach. Many concepts (like passing tenant context, isolating data in code) apply similarly to both. We will note where something is specific to one model.

## 2. Project Setup

In this section, we'll set up the development environment for both the frontend and backend. We’ll configure a React + TypeScript project for the client-side and a Spring Boot project for the server-side, and ensure MySQL is ready for multi-tenant data storage.

### Setting Up the Development Environment

To get started, make sure you have the required tools installed:

1. **Node.js and npm:** Install Node.js (which includes npm) for running React and build tools. Aim for an LTS version (e.g., Node 18+). Verify by running `node -v` and `npm -v`.
2. **Java Development Kit (JDK):** Install JDK 17 (or the latest LTS) for Spring Boot. Spring Boot 3.x requires Java 17+. Verify by `java -version`.
3. **IDE/Editors:** Use a suitable editor/IDE. _Frontend:_ VS Code (with the TypeScript and React plugins) is popular. _Backend:_ IntelliJ IDEA or VS Code with Java extensions works well.
4. **MySQL Database:** Set up a MySQL server (5.7 or 8.x). You can install MySQL locally or use a Docker container for MySQL. Make sure you know the root password or create a user for the app. Optionally, use a MySQL client (MySQL Workbench, TablePlus, etc.) to manage the DB.
5. **Maven or Gradle:** Ensure you have Maven or Gradle available to build the Spring Boot project. (Maven is standard with Spring Initializr, and comes bundled in many IDEs. You can verify Maven with `mvn -v` or use the Maven wrapper provided by Spring Initializr.)

With the tools ready, we will create two projects: one for the React frontend and one for the Spring Boot backend.

### Bootstrapping the ReactJS + TypeScript Frontend

We will create a new React project configured for TypeScript. There are a few ways to do this:

- **Using Vite (recommended for speed):** Vite is a fast build tool. You can create a React+TS app with:
  ```bash
  npm create vite@latest multi-tenant-ui -- --template react-ts
  cd multi-tenant-ui
  npm install
  npm run dev
  ```
  This sets up a React project with TypeScript, and starts a dev server (Vite's dev server) on http://localhost:5173 (default). The project will include a `tsconfig.json` with sensible defaults and an `index.tsx`.
- **Using Create React App (CRA):** Alternatively:
  ```bash
  npx create-react-app multi-tenant-ui --template typescript
  cd multi-tenant-ui
  npm start
  ```
  CRA will set up a development server on http://localhost:3000. CRA is a bit slower and more heavy-weight, but widely used. (As an advanced dev, you might prefer Vite for its speed and simplicity, but CRA is fine if you need its out-of-the-box features.)

Both approaches create a base React app. Open the project in your editor. Verify **TypeScript** is working by checking for a `tsconfig.json` file and `.tsx` files in `src/` (like `src/main.tsx` or `index.tsx`). The config should have `"strict": true` for best practices (ensures rigorous type-checking). If not, enable strict mode in tsconfig.

Now install any UI libraries or tools you plan to use:

- For example, you might add a UI component library like **Material-UI (MUI)** for ready-made components: `npm install @mui/material @emotion/react @emotion/styled`.
- If using **React Router** for navigation (we will for multi-page structure and protected routes): `npm install react-router-dom`.
- We'll use a state management solution for tenant-aware state: options include **Redux Toolkit** or **React Query** (more on this later). For now, you can add them:
  - Redux Toolkit: `npm install @reduxjs/toolkit react-redux`.
  - React Query (TanStack Query): `npm install @tanstack/react-query`.
- For authentication flows, we might use `axios` for API calls: `npm install axios`.

We will set up the project structure with meaningful folders, for example:

```
src/
  components/    # Reusable UI components
  pages/         # Page components (routes)
  store/         # Redux store setup (if using Redux)
  api/           # API helper functions (for calling backend)
  types/         # TypeScript type definitions (e.g. interfaces for data models)
```

This structure will help as the app grows.

**TypeScript configuration:** Ensure `tsconfig.json` has appropriate settings. The default from templates is usually fine. Key settings:

- `"target": "ES2017"` or later (as needed).
- `"jsx": "react-jsx"` (for React 17+ JSX transform).
- `"baseUrl": "src"` and perhaps `"paths"` if you want to use absolute imports (optional, for convenience).
- Strict flags (`strict`, `noImplicitAny`, etc.) ideally enabled.

At this point, you should have a running React TypeScript app (just showing a default page). We will come back to implement functionality after setting up the backend.

### Setting Up the Spring Boot Project (Maven/Gradle)

Next, initialize a Spring Boot project. The easiest way is to use **Spring Initializr** (http://start.spring.io):

- **Project settings:** Choose _Maven Project_ (or Gradle if you prefer), Java, Spring Boot version 3.x (or latest stable).
- **Group and Artifact:** Use something like `com.example.multitenant` as the group, and `multi-tenant-app` as the artifact (adjust as needed).
- **Dependencies:** Add the following essential dependencies:
  - **Spring Web** (for REST controllers).
  - **Spring Data JPA** (for database access via Hibernate).
  - **MySQL Driver** (JDBC driver for MySQL).
  - **Spring Security** (for authentication & authorization).
  - **Spring Boot DevTools** (optional, for hot reloading in dev).
  - Optionally, **Lombok** (to reduce boilerplate in models).
  - (We will also use Flyway or Liquibase for DB migrations later, which can be added now or later.)
- If using Gradle, similar dependencies apply.
- Generate and download the project, then open it in your IDE.

Alternatively, using Spring Boot CLI (if installed) or curl:

```bash
spring init -d=web,data-jpa,mysql,security,lombok,devtools -g com.example.multitenant -a multi-tenant-app multi-tenant-app
```

This will generate a Maven project named "multi-tenant-app" with those dependencies.

Once the project is set up, do the following:

1. **Application Properties:** Open `src/main/resources/application.properties` (or `.yml`) and configure basic settings:

   ```properties
   server.port=8080  # Port for the API server
   spring.datasource.url=jdbc:mysql://localhost:3306/multitenant_master?useSSL=false&allowPublicKeyRetrieval=true
   spring.datasource.username=your_mysql_user
   spring.datasource.password=your_mysql_password
   spring.jpa.hibernate.ddl-auto=none   # We'll handle schema with migrations
   spring.jpa.show-sql=true             # Log SQL for debugging (disable in prod)
   ```

   Here we assume a database named `multitenant_master` that will act as a **master** or default schema (especially useful for schema-per-tenant strategy). For now, create this database in MySQL (e.g., via MySQL client: `CREATE DATABASE multitenant_master;`). We will use it to hold tenant information and possibly shared tables.

   If you plan on a shared schema approach, you might not need a separate master schema; you could use the same database for everything. But having a master DB is useful to store metadata like tenant registry, and in code it's needed for multi-tenant routing (we'll see shortly).

2. **Verify Connection:** Run the Spring Boot application (e.g., via your IDE or `./mvnw spring-boot:run`). Check the console to ensure it starts without errors. If it fails to connect to MySQL, double-check the URL, username, and password. You might need to add `createDatabaseIfNotExist=true` in the URL if the database doesn't exist and you want Spring to create it (or create manually as advised).

3. **Project Structure:** In the generated project, you have an `Application` class (e.g., `MultiTenantAppApplication.java` with a `main` method). Create some base packages:

   - `com.example.multitenant.model` (for entity classes),
   - `com.example.multitenant.repository`,
   - `com.example.multitenant.web` (for controllers),
   - `com.example.multitenant.config` (for security and multitenancy configuration classes),
   - `com.example.multitenant.service` (for service layer).

   This grouping will keep code organized as we add multi-tenant specifics.

### Configuring MySQL for Multi-Tenancy

Before building features, decide on the multi-tenancy approach to implement in the database. For this guide, let's consider **schema-per-tenant** as the primary model (with notes on adapting to shared schema if needed). In schema-per-tenant:

- We have one MySQL database server. The default schema (e.g. `multitenant_master`) acts as a catalog holding tenant metadata and possibly any shared tables.
- For each tenant, we'll have a separate schema (database schema in MySQL terms, which is essentially a separate database namespace). For example, if a tenant is named "acme", we might have a schema `acme` in the MySQL server to hold that tenant's tables.

**MySQL setup:**

- Make sure the user account configured has privileges to create new schemas (databases) or at least to access multiple schemas. If using root (not recommended for production), it can do anything. In production, you might use an admin account for schema management and separate user accounts for each tenant DB access for security.
- If using separate schemas, you might create them manually or have the application create them on the fly when a new tenant is added. For development, you can create a couple of schemas now to simulate tenants (e.g., `tenant1_db` and `tenant2_db`).
- If using the shared schema approach, ensure every table will include a tenant ID column and plan to create needed indexes (we'll cover in Database Design).

**Spring Boot configuration for multi-tenancy:**
By default, Spring Boot will connect to one datasource (the `spring.datasource.url` provided). To support dynamic schemas or multiple DBs, we will need to extend Spring/Hibernate configuration. We won't configure that in `application.properties` alone; instead, we'll write custom configuration classes (in section 3 and 4) to route connections based on tenant context.

For now, confirm that we can connect to the master schema. In the next section, we'll design the database and set up the JPA/Hibernate multi-tenancy support.

## 3. Database Design

Database design for multi-tenancy must ensure **tenant-based data isolation**. We'll define how our data is structured across schemas or tables, and configure Hibernate (JPA) to work with our chosen model. We will also ensure that every query only sees data for the correct tenant.

### Schema Design for Multi-Tenancy

Let’s outline the database schema considering a typical SaaS use case (for example, a project management app where each tenant is a company, with its own users and projects). We'll consider **schema-per-tenant** design first:

- **Master Schema (Catalog):** This schema (e.g., `multitenant_master`) holds global information:

  - A `tenants` table: to register each tenant. Fields might include `tenant_id` (PK), `tenant_name`, and connection details if needed (like a JDBC URL or schema name). For example:
    ```sql
    CREATE TABLE tenants (
      tenant_id VARCHAR(50) PRIMARY KEY,
      name VARCHAR(100),
      db_schema VARCHAR(100),
      ... any other metadata ...
    );
    ```
    This table lists all tenant organizations. For schema-per-tenant, `db_schema` might store the schema name for that tenant (which could be same as tenant_id or some generated name). If using database-per-tenant, you might store the full JDBC URL or host info instead ([Multi-tenancy -The shared database, separate schema approach... with a flavour of separate database on top! | CIVIC UK](https://www.civicuk.com/blog-item/multi-tenancy-shared-database-separate-schema-approach-flavour-separate-database-top#:~:text=1,Separate)). This master table is crucial if the application needs to lookup tenant info dynamically (like during login or request routing).
  - (Optional) `users_master` table: In some designs, you keep all user credentials in the master database for authentication. However, it's often better to keep user records within each tenant's schema for data isolation. We will assume each tenant's users live in their own schema. The master `tenants` table can hold only tenant-wide info (name, plan, etc.), not individual user accounts.

- **Tenant Schemas:** For each tenant, we have a separate schema with the same set of tables. For example, each tenant schema could have:

  - `users` table (tenant-specific users),
  - `projects` table (or whatever domain entities),
  - other domain-specific tables.

  The structure of these tables is identical across schemas, but they contain different rows per tenant. E.g., `tenant1_db.users` holds users of tenant1, `tenant2_db.users` holds users of tenant2.

  We must ensure that when querying, our application is using the correct schema. We also must run schema migrations for each schema when the model changes (we'll discuss that in _Testing & Maintenance_).

If we were using the **Shared Schema (tenant column)** approach, the design would be:

- A single set of tables (e.g., `users`, `projects`) in one schema.
- Every table includes a `tenant_id` column (or similar) to identify which tenant each row belongs to.
- All primary keys could be composite (tenant_id + the entity's id) or at least have an index on tenant_id for fast filtering. For instance, you might enforce `(tenant_id, user_id)` as a unique composite key on the `users` table ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=2)). This ensures queries always filter by tenant_id (and the index helps performance).
- The `tenant_id` would likely reference a `tenants` table (or be a foreign key if you store tenants in the same schema).

No matter the approach, **indexing is critical**. For shared schema, _always index the tenant discriminator column._ Many experts advise making `tenant_id` the leftmost part of the primary key or clustered index, so that queries can efficiently seek by tenant ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=2)). This prevents full table scans across tenants and ensures each tenant’s data is clustered together on disk for locality ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=Although%20there%20are%20many%20considerations,seek%20on%20the%20composite%20key)) ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=2)). For schema-per-tenant, each schema’s tables can have their own PKs as usual (since each is smaller, containing one tenant’s data). But even there, adding an index on common search fields is important.

**Example Use Case Schema:**  
Imagine a simple model: each tenant has Users and Projects.

- In schema-per-tenant model, in each tenant schema:

  ```sql
  CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20)  -- e.g., "ADMIN" or "USER"
  );
  CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    description TEXT,
    owner_user_id BIGINT,
    FOREIGN KEY (owner_user_id) REFERENCES users(id)
  );
  ```

  There is no tenant_id column here, because the schema itself is specific to a tenant.

- In a shared schema model, a combined schema would be:
  ```sql
  CREATE TABLE users (
    id BIGINT,
    tenant_id VARCHAR(50),
    username VARCHAR(50),
    password_hash VARCHAR(255),
    role VARCHAR(20),
    PRIMARY KEY (tenant_id, id)
  );
  CREATE TABLE projects (
    id BIGINT,
    tenant_id VARCHAR(50),
    name VARCHAR(100),
    description TEXT,
    owner_user_id BIGINT,
    PRIMARY KEY (tenant_id, id),
    FOREIGN KEY (tenant_id, owner_user_id) REFERENCES users(tenant_id, id)
  );
  ```
  Here `tenant_id` is part of the key and is carried through to child tables. We would also have a `tenants` table listing valid tenant IDs to reference.

The rest of this guide will illustrate primarily using schema-per-tenant with a master `tenants` table for lookup, as it offers a good balance for demonstration. However, we will note what changes if you use shared schema.

### Using Hibernate JPA with Multi-Tenancy Support

**Hibernate** (the JPA provider used by Spring Boot by default) has built-in support for multi-tenancy. It supports all three models discussed: discriminator (partition), separate schema, or separate database. We need to configure Hibernate to use the tenant context to route queries appropriately.

Key Hibernate strategies and components:

- **`hibernate.multiTenancy` property:** This can be set to `DATABASE`, `SCHEMA`, or `DISCRIMINATOR` (partition) to indicate the approach. For schema-per-tenant, we'll use `SCHEMA`. For separate DB per tenant, use `DATABASE`. For shared table, use `DISCRIMINATOR` (and you must annotate entities with `@TenantId` or use filters).
- **Current Tenant Identifier:** We need to tell Hibernate which tenant identifier is in use for the current session/transaction. In a web app, this will vary per request (based on the logged-in user or the URL). Hibernate uses a `CurrentTenantIdentifierResolver` to obtain the tenant id (a string) for each session/connection.
- **Connection Provider:** In multi-tenant scenarios, a custom `MultiTenantConnectionProvider` is used to get database connections. For `SCHEMA` strategy, this provider can take a connection from a pool and set the schema (e.g., via `SET search_path` in Postgres or `connection.setSchema(...)` in JDBC) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=%40Override%20public%20Connection%20getConnection,setSchema%28schema%29%3B%20return%20connection%3B)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=public%20Connection%20getConnection,setSchema%28schema%29%3B%20return%20connection%3B)). For `DATABASE` strategy, the provider might look up a DataSource for the given tenant and return a connection from that DataSource ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Instead%2C%20the%20heavy%20lifting%20is,AbstractRoutingDataSource)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=HashMap,setTargetDataSources%28targetDataSources%29%3B)). Essentially, this component routes to the right DB or schema.

**Implementing schema-based multi-tenancy in Spring Boot:**

1. **Tenant Identifier Resolver:** Create a class that implements `CurrentTenantIdentifierResolver` (from Hibernate). For example:

   ```java
   @Component
   public class TenantIdentifierResolver implements CurrentTenantIdentifierResolver {
       private static final String DEFAULT_TENANT = "master"; // default schema

       private static final ThreadLocal<String> currentTenant = new InheritableThreadLocal<>();

       public static void setCurrentTenant(String tenant) {
           currentTenant.set(tenant);
       }
       public static void clear() {
           currentTenant.remove();
       }
       @Override
       public String resolveCurrentTenantIdentifier() {
           String tenant = currentTenant.get();
           return (tenant != null) ? tenant : DEFAULT_TENANT;
       }
       @Override
       public boolean validateExistingCurrentSessions() {
           return true;
       }
   }
   ```

   This uses a `ThreadLocal` to store the current tenant ID for each request thread. If none is set, it falls back to `"master"` (our master schema). We will ensure that at the start of each request (or when a user logs in), we call `TenantIdentifierResolver.setCurrentTenant(...)` with the tenant’s ID or schema name, and clear it at the end. This design allows Hibernate to call `resolveCurrentTenantIdentifier()` whenever it needs to know which schema/tenant to use ([Multi-tenancy -The shared database, separate schema approach... with a flavour of separate database on top! | CIVIC UK](https://www.civicuk.com/blog-item/multi-tenancy-shared-database-separate-schema-approach-flavour-separate-database-top#:~:text=Well%2C%20it%27s%20nothing%20more%20than,perfect%20for%20our%20use%20case)).

2. **Connection Provider:** Create a class that implements `MultiTenantConnectionProvider`. For schema-per-tenant, the implementation can use a single DataSource underneath (pointing to the MySQL server) and just switch schema on each connection:

   ```java
   @Component
   public class SchemaBasedMultiTenantConnectionProvider
           implements MultiTenantConnectionProvider, HibernatePropertiesCustomizer {
       @Autowired
       private DataSource dataSource;

       // Get a connection without tenant context (for startup or default schema usage)
       @Override
       public Connection getAnyConnection() throws SQLException {
           Connection conn = dataSource.getConnection();
           conn.setSchema("multitenant_master"); // default schema
           return conn;
       }
       @Override
       public void releaseAnyConnection(Connection connection) throws SQLException {
           connection.close();
       }
       // Get a connection for a specific tenant (schema)
       @Override
       public Connection getConnection(String tenantIdentifier) throws SQLException {
           Connection conn = dataSource.getConnection();
           conn.setSchema(tenantIdentifier);  // switch to tenant's schema
           return conn;
       }
       @Override
       public void releaseConnection(String tenantIdentifier, Connection connection) throws SQLException {
           connection.setSchema("multitenant_master");
           connection.close();
       }
       // Other required methods (supportsAggressiveRelease etc.) can return default values or false.
       @Override
       public boolean supportsAggressiveRelease() { return false; }
       // ... (implement other interface methods as needed)

       // HibernatePropertiesCustomizer allows hooking this into Hibernate config:
       @Override
       public void customize(Map<String, Object> hibernateProps) {
           hibernateProps.put(Environment.MULTI_TENANT_CONNECTION_PROVIDER, this);
       }
   }
   ```

   What this does: whenever Hibernate needs a DB connection for a given tenant, it calls `getConnection(tenantId)`, and we get a JDBC connection from the base DataSource and set its schema to the tenant’s schema ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=%40Override%20public%20Connection%20getConnection,setSchema%28schema%29%3B%20return%20connection%3B)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=public%20Connection%20getConnection,setSchema%28schema%29%3B%20return%20connection%3B)). When done, we reset to master (optional, but a good practice) and close. We also provide the `HibernatePropertiesCustomizer` interface so that Spring will automatically add our connection provider to Hibernate’s configuration (alternatively, we could set properties in `application.properties`, but programmatic customization is clearer here). Note: The above code uses `Connection.setSchema` (JDBC 4.1). In MySQL, this is effectively `USE <schema>`.

3. **JPA Configuration:** In your Spring Boot application configuration (could be the main class or a `@Configuration` class in `config` package), enable multi-tenancy:

   ```java
   @SpringBootApplication
   @EnableJpaRepositories(basePackages = "...")  // your packages
   public class MultiTenantAppApplication {
       public static void main(String[] args) {
           SpringApplication.run(MultiTenantAppApplication.class, args);
       }

       @Bean
       public LocalContainerEntityManagerFactoryBean entityManagerFactory(
               DataSource dataSource,
               SchemaBasedMultiTenantConnectionProvider connectionProvider,
               TenantIdentifierResolver tenantResolver) {
           LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
           emf.setDataSource(dataSource);
           emf.setPackagesToScan("com.example.multitenant.model");
           // JPA vendor and other config
           HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
           vendorAdapter.setDatabase(Database.MYSQL);
           emf.setJpaVendorAdapter(vendorAdapter);

           // Set Hibernate properties
           Properties jpaProps = new Properties();
           jpaProps.put(Environment.DIALECT, "org.hibernate.dialect.MySQLDialect");
           jpaProps.put(Environment.MULTI_TENANT, MultiTenancyStrategy.SCHEMA);
           jpaProps.put(Environment.MULTI_TENANT_CONNECTION_PROVIDER, connectionProvider);
           jpaProps.put(Environment.MULTI_TENANT_IDENTIFIER_RESOLVER, tenantResolver);
           // (If using DDL-auto, you might disable it because we'll use migrations)
           emf.setJpaProperties(jpaProps);
           return emf;
       }
   }
   ```

   This bean explicitly sets up the EntityManagerFactory with multi-tenancy. We specify:

   - `MULTI_TENANT` strategy = SCHEMA.
   - The `MultiTenantConnectionProvider` and `CurrentTenantIdentifierResolver` beans we wrote.
     If you prefer, you could rely on Spring Boot auto-config and just set equivalent properties in `application.properties`, like:

   ```properties
   spring.jpa.properties.hibernate.multiTenancy=SCHEMA
   spring.jpa.properties.hibernate.tenant_identifier_resolver=... (fully qualified class name)
   spring.jpa.properties.hibernate.multi_tenant_connection_provider=... (class name)
   ```

   But using the beans is often cleaner and ensures our custom logic (like customizing `DataSource` usage) is applied.

4. **Entity modeling:** If using schema-per-tenant or database-per-tenant, you do **not** include any tenant identifier in the entity classes; each entity is defined normally (id, fields, etc.). The isolation is done via the connection’s schema. If using shared schema (discriminator), you **would** include a tenant field in entities. Hibernate has a `@TenantId` annotation for marking that field, and requires some extra config for discriminator-based multi-tenancy ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=1,part%20of%20the%20primary%20key)). For our approach, we skip tenant field in entities.

Now, with the above in place, whenever we call a JPA repository or run a query, Hibernate will:

- Ask `tenantResolver` for the current tenant identifier.
- Use `connectionProvider` to get a JDBC Connection set to that tenant’s schema.
- Execute the SQL (which will implicitly run in that schema context).
- Thus, we get tenant-isolated data.

We must ensure to set the tenant identifier in the resolver **for each request**. We'll address that in the backend section (likely via a filter or interceptor that reads the tenant from the request).

For completeness, if implementing **DB-per-tenant** (separate database instances or separate DataSource per tenant):

- You might not switch schema on the connection (the connection itself goes to a different URL). Instead, you would maintain a map of DataSource objects keyed by tenant ID. The `MultiTenantConnectionProvider` would then pick the correct DataSource and get a connection ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Instead%2C%20the%20heavy%20lifting%20is,AbstractRoutingDataSource)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=HashMap,setTargetDataSources%28targetDataSources%29%3B)). Spring's `AbstractRoutingDataSource` can be helpful to route to a data source based on a context key ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Instead%2C%20the%20heavy%20lifting%20is,AbstractRoutingDataSource)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=HashMap,setTargetDataSources%28targetDataSources%29%3B)).
- The rest is similar in concept: set the current tenant context, and ensure the provider returns the right connection. The master table of tenants would store connection info for each tenant's DB if they're on different servers.
- The application logic of isolating per request remains the same.

### Implementing Tenant-Based Data Isolation

In addition to schema or connection-based isolation, it's good to have safeguards at the application level:

- **Service/Repository layer checks:** Even though switching the schema largely guarantees isolation, you should ensure that any query explicitly filters by tenant if working in a shared schema scenario. For example, if you somehow bypass JPA and run a native SQL, include `WHERE tenant_id = ?` bound to the current tenant.
- **No cross-tenant queries:** Do not design any query or join that pulls data across tenants. If there's a requirement to aggregate data across tenants (for a global admin view perhaps), treat that carefully (such queries should ideally run on the master database or through special admin-only paths that iterate tenants instead).
- **Testing isolation:** Write tests to assert that even if you try to switch context mid-transaction or accidentally use the wrong tenant ID, data doesn’t leak (more in Testing section).

For our purposes, once the `TenantIdentifierResolver` and `MultiTenantConnectionProvider` are in place, Spring Data JPA repositories will automatically operate in the current tenant's schema. For example:

```java
@Autowired UserRepository userRepo;
...
TenantIdentifierResolver.setCurrentTenant("tenant1_db");
List<User> users = userRepo.findAll();
// This will actually execute SELECT * FROM tenant1_db.users;
```

If we then set to another tenant and call findAll again, we'd get that tenant's users:

```java
TenantIdentifierResolver.setCurrentTenant("tenant2_db");
List<User> usersTenant2 = userRepo.findAll();
// Now SELECT * FROM tenant2_db.users;
```

A quick test like this can be done in a Spring Boot test with multiple tenants to verify the setup ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=createPerson%28PIVOTAL%2C%20)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=currentTenant.setCurrentTenant%28VMWARE%29%3B%20assertThat%28persons.findAll%28%29%29.extracting%28Person%3A%3AgetName%29.contai%20nsExactly%28)).

One more consideration: **initial schema creation.** When a new tenant is added, you need to create a new schema (for schema-per-tenant) or a new database. This can be done manually or via code:

- For example, you could have an SQL script or migration that runs `CREATE SCHEMA <tenant>` when needed ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=Note%20that%20we%20have%20to,now%20looks%20like%20this)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=create%20sequence%20pivotal,id)).
- Or use Flyway programmatically to set up initial schema structure (discussed later).

For now, ensure that in MySQL you have at least one tenant schema created (for testing). For instance, create schemas `tenant1_db` and `tenant2_db` and run the basic table creation DDL in each (matching your JPA entities). Alternatively, as a quick hack in dev, you could set `spring.jpa.hibernate.ddl-auto=create` and specify `spring.jpa.properties.hibernate.default_schema=tenant1_db` while running the app to auto-generate tables in that schema, then copy them to other schemas – but in production, you'll use migrations.

With the database design and Hibernate config ready, we can move to implementing the backend logic.

## 4. Backend Development with Spring Boot (Multi-Tenant)

Now we develop the backend features: authentication, tenant context setting, API endpoints for user and tenant management, role-based access control, and supportive infrastructure (exception handling, logging).

### Multi-Tenant Authentication with JWT (or OAuth2)

**Authentication** is the process of verifying user identity. In a multi-tenant app, we also need to identify which tenant the user belongs to during authentication.

We will use **JWT (JSON Web Tokens)** for stateless auth. Alternatively, one could use OAuth2 with an external Identity Provider, but implementing JWT ourselves gives more control in a custom multi-tenant setup. The idea:

- Users will log in with credentials (e.g., email/username and password) and specify their tenant (if the tenant isn’t implied by subdomain).
- If credentials are valid, the backend issues a signed JWT containing the user's identity, tenant ID, and roles.
- The React app stores this JWT and sends it with each API request (in an `Authorization: Bearer <token>` header).
- The backend will verify the token on each request and set the security context (including tenant info) accordingly.

**Identifying tenant on login:** There are a few patterns:

- **Subdomain per tenant:** If your application is served at URLs like `tenant1.myapp.com`, `tenant2.myapp.com`, you can infer the tenant from the request host. Users would go to their tenant-specific URL to log in. (This requires DNS and routing setup but is very user-friendly and professional ([Multi-tenancy -The shared database, separate schema approach... with a flavour of separate database on top! | CIVIC UK](https://www.civicuk.com/blog-item/multi-tenancy-shared-database-separate-schema-approach-flavour-separate-database-top#:~:text=2,customised%20as%20they%20need%20to%C2%A0be)).)
- **Tenant identifier field:** If using a unified URL, you can ask the user to input a tenant ID or select their organization during login. Alternatively, you can require a specific login endpoint per tenant (like `/tenant/{tenantId}/login`). For simplicity, you might include `tenant` as a field in the login form or have a dropdown.
- **Email domain mapping:** In some cases, you could derive tenant from the user's email domain (if each tenant uses distinct email domains), but this is less reliable.

In our guide, we'll assume either subdomain or a special header is used. Let's say we expect a header `"Tenant-ID"` on login and subsequent requests (if not using subdomains). The frontend will supply this from user input or configuration.

**User credential storage:** We decided each tenant's users live in their own schema. So on login, we need to:

- Determine the tenant (from subdomain or login form/header).
- Switch to that tenant's context (set `TenantIdentifierResolver.currentTenant`) so that we can load the user from the tenant’s `users` table.
- Verify password, then issue JWT.

Alternatively, one could have a centralized authentication DB. For example, the DZone article suggests storing all user info in each tenant DB and using the tenant approach for auth ([Developing a Multi-Tenancy Application With Spring Security](https://dzone.com/articles/dynamic-multi-tenancy-using-java-spring-boot-sprin#:~:text=2,and%20a%20tenant%20database)) ([Developing a Multi-Tenancy Application With Spring Security](https://dzone.com/articles/dynamic-multi-tenancy-using-java-spring-boot-sprin#:~:text=In%20the%20master%20database%2C%20we,is%20stored%20in%20the%20table)), which is what we do. Another approach is a _master_ user table with a tenant reference and do login in master DB, but then you'd need to query across tenants for user – not scalable unless users might belong to multiple tenants. We will stick to per-tenant user storage.

**Implementing login endpoint:**

Create an `AuthController` with a `/login` endpoint:

```java
@RestController
public class AuthController {
    @Autowired UserRepository userRepo;
    @Autowired PasswordEncoder passwordEncoder;  // configure a BCryptPasswordEncoder bean for this

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestHeader("Tenant-ID") String tenantId,
                                   @RequestBody LoginRequest loginReq) {
        try {
            // 1. Set tenant context for this request
            TenantIdentifierResolver.setCurrentTenant(tenantId);
            // 2. Find user by username (or email)
            User user = userRepo.findByUsername(loginReq.getUsername())
                    .orElseThrow(() -> new RuntimeException("User not found"));
            // 3. Check password
            if (!passwordEncoder.matches(loginReq.getPassword(), user.getPasswordHash())) {
                throw new RuntimeException("Invalid password");
            }
            // 4. Generate JWT token
            String token = jwtService.generateToken(user.getUsername(), tenantId, user.getRole());
            // 5. Return token
            Map<String, String> response = Collections.singletonMap("token", token);
            return ResponseEntity.ok(response);
        } finally {
            TenantIdentifierResolver.clear(); // clear context after
        }
    }
}
```

Here, `LoginRequest` is a simple DTO with `username` and `password`. We use `Tenant-ID` header to know which tenant DB to query ([Multi-tenancy -The shared database, separate schema approach... with a flavour of separate database on top! | CIVIC UK](https://www.civicuk.com/blog-item/multi-tenancy-shared-database-separate-schema-approach-flavour-separate-database-top#:~:text=2,customised%20as%20they%20need%20to%C2%A0be)). We set the `TenantIdentifierResolver` so that `userRepo.findByUsername` will query the correct schema. We then generate a JWT.

**JWT Generation:** Use a library like JJWT (io.jsonwebtoken) or the Java JWT from Auth0 to create tokens. A simple example using JJWT:

```java
@Component
public class JwtService {
    private final String JWT_SECRET = "MySuperSecretKey";  // in real app, load from config
    public String generateToken(String username, String tenantId, String role) {
        Instant now = Instant.now();
        String token = Jwts.builder()
            .setSubject(username)
            .claim("tenantId", tenantId)
            .claim("role", role)
            .setIssuedAt(Date.from(now))
            .setExpiration(Date.from(now.plus(1, ChronoUnit.HOURS)))
            .signWith(Keys.hmacShaKeyFor(JWT_SECRET.getBytes()), SignatureAlgorithm.HS256)
            .compact();
        return token;
    }
    // also have methods to validate token and retrieve claims...
}
```

This token will carry the tenantId and role in its payload (claims). The `sub` (subject) is the username.

**Securing API requests with JWT:** Now, for each subsequent request, the client will include `Authorization: Bearer <token>`. We need to verify and parse the JWT on the backend and establish the authenticated user and tenant context.

Use Spring Security configuration to add a filter for JWT:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Autowired JwtService jwtService;
    @Autowired UserDetailsService customUserDetailsService; // if we use one, or we can not use it since JWT has all info.

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf().disable()  // using tokens, not cookies
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            .authorizeRequests(auth -> {
                auth.antMatchers("/login", "/signup").permitAll();
                auth.anyRequest().authenticated();
            });

        // JWT filter
        http.addFilterBefore(new OncePerRequestFilter() {
            @Override
            protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
                    throws ServletException, IOException {
                String authHeader = request.getHeader("Authorization");
                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    String token = authHeader.substring(7);
                    try {
                        Jws<Claims> claimsJws = jwtService.parseToken(token);
                        Claims claims = claimsJws.getBody();
                        String username = claims.getSubject();
                        String tenantId = claims.get("tenantId", String.class);
                        String role = claims.get("role", String.class);
                        // Set tenant context for this request
                        TenantIdentifierResolver.setCurrentTenant(tenantId);
                        // Create Authentication object (Spring Security)
                        List<GrantedAuthority> authorities = List.of(new SimpleGrantedAuthority("ROLE_" + role));
                        UsernamePasswordAuthenticationToken authToken =
                                new UsernamePasswordAuthenticationToken(username, null, authorities);
                        SecurityContextHolder.getContext().setAuthentication(authToken);
                    } catch (JwtException e) {
                        // Invalid token
                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid JWT");
                        return;
                    }
                }
                // Proceed with filter chain
                filterChain.doFilter(request, response);
                // Clear tenant after request
                TenantIdentifierResolver.clear();
            }
        }, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
}
```

Let's unpack this:

- We disable CSRF since we won't use cookies for auth (more on security later).
- We allow `/login` (and perhaps a `/signup` or some public endpoints) to be accessed without auth. All other endpoints require authentication.
- We add a custom filter (extending `OncePerRequestFilter` for a single execution per request) **before** the standard UsernamePasswordAuthenticationFilter. This filter checks for an `Authorization` header with Bearer token.
- If present, it uses `jwtService.parseToken` (which would internally call JJWT to validate signature and expiration) and extracts claims. We retrieve `tenantId` and `role` from claims.
- We then set the tenant context via our TenantIdentifierResolver so that downstream code runs in the correct tenant schema.
- We also create an Authentication object for Spring Security, with the username and role. We prefix role with "ROLE\_" because Spring Security uses that convention (so if role claim is "ADMIN", we make it "ROLE_ADMIN").
- Put that Authentication into SecurityContext, which marks the request as authenticated.
- If token is invalid, we send 401.
- After the filter chain, in a finally-like manner, we clear the ThreadLocal tenant context to avoid leaking it to the next request on the same thread (in non-web container threads it might not happen, but with thread pools it's good practice to clear).

Now all incoming requests (except /login which is allowed through) will require a valid JWT. And as soon as the JWT is processed, our application "knows" which tenant it is dealing with (via TenantIdentifierResolver) and which user and role (via SecurityContext).

**Using OAuth2 and OpenID Connect (Optional alternative):** If you wanted, you could integrate with an OAuth provider (like Keycloak, Auth0, Cognito). In that case, you wouldn't manually issue JWTs; instead, the provider issues them and you configure `spring-security-oauth2-resource-server` to accept tokens. Multi-tenancy could be addressed by having a claim in the token for tenant, or separate issuers per tenant. For brevity, we stick to custom JWT as above.

### User and Organization (Tenant) Management APIs

We need endpoints to manage tenants (organizations) and users within tenants:

- **Tenant management (for system admins):**

  - `POST /tenants` – Create a new tenant (organization). This might only be accessible to a global admin role (if your app has a concept of a super-admin) or via a sign-up process.
  - `GET /tenants` – List tenants (again restricted to admin).
  - Possibly `PUT /tenants/{id}` to update tenant info, `DELETE /tenants/{id}` to deactivate a tenant, etc.

  When creating a new tenant in schema-per-tenant model, this endpoint would:

  1. Generate a unique tenant ID (e.g., a slug or UUID).
  2. Create a new schema in the database for this tenant. This can be done via a Flyway script or programmatically using a JDBC script (e.g., `CREATE SCHEMA tenant_x`).
  3. Initialize the schema with the required tables (you might run migrations for that schema or copy structure from a template).
  4. Insert a record in the master `tenants` table with the tenant info (id, name, etc).
  5. Perhaps create an initial admin user for this tenant.

  Example of a tenant creation service (simplified):

  ```java
  @Service
  public class TenantService {
      @Autowired DataSource dataSource;
      @Autowired TenantRepository tenantRepo;
      public Tenant createTenant(String name) {
          // 1. Create schema
          String schema = name.toLowerCase(); // simplistic schema name
          try (Connection conn = dataSource.getConnection();
               Statement st = conn.createStatement()) {
              st.execute("CREATE DATABASE " + schema);
              // Could also run schema SQL here or use Flyway (preferred)
          }
          // 2. Save tenant in master
          Tenant tenant = new Tenant(schema, name);
          return tenantRepo.save(tenant);
      }
  }
  ```

  In practice, use Flyway to handle the "run migrations in new schema" part (we will address in Testing & Maintenance how to run migrations for all tenants).

- **User management (tenant-level):**

  - `POST /users` – Create a new user in the current tenant.
  - `GET /users` – List users in the tenant (admin only).
  - `DELETE /users/{id}` – Remove a user, etc.
  - `PUT /users/{id}/role` – Change a user's role (if implementing role changes).

  These APIs would be secured so that only a tenant admin (or system admin) can create or modify users, and normal users might only list or update their own profile.

  Implementation is straightforward with Spring Data JPA:

  ```java
  @RestController
  @RequestMapping("/api")
  public class UserController {
      @Autowired UserRepository userRepo;
      @Autowired PasswordEncoder passwordEncoder;

      @PostMapping("/users")
      @PreAuthorize("hasRole('ADMIN')")  // only tenant admin can create user
      public User createUser(@RequestBody User user) {
          // encode password, ensure unique username
          user.setPasswordHash(passwordEncoder.encode(user.getPassword()));
          user.setRole("USER");
          return userRepo.save(user);
      }

      @GetMapping("/users")
      @PreAuthorize("hasAnyRole('ADMIN','USER')")
      public List<User> listUsers() {
          return userRepo.findAll();
      }
      // ... other endpoints ...
  }
  ```

  Note: When these methods call `userRepo.save` or `findAll`, thanks to our earlier setup, the _tenant context is already set_ (from the JWT filter). So `findAll` will only return users from that tenant's schema. There's no additional filter needed in the query. This is a huge benefit of schema-per-tenant with dynamic DataSource routing: we can reuse the same repository for all tenants without adding `tenantId` conditions, because the connection itself is scoped to the tenant. (In a shared schema approach, we'd instead add `@Filter` or manually filter by tenantId in each query.)

- **Project (or domain data) APIs:** Similarly, you would create controllers for the main domain entities (e.g., `ProjectController` for projects). These would again use repositories that automatically scope to the tenant schema. You would include security annotations so that, for example, any authenticated user in the tenant can create a project, but maybe only admins can delete projects, etc., depending on business rules.

**Ensuring tenant context:** It's worth reiterating that any entry point to the backend (controller or repository layer) must have the tenant set. In our setup, the JWT filter does this for all requests after login. If you have other entry points (like scheduled jobs or message queue listeners), those might need to set a default or handle multi-tenant logic differently (perhaps process data per tenant).

### Implementing Role-Based Access Control (RBAC)

We have touched on roles: let's detail RBAC in this app:

- **Role model:** Define a set of roles, e.g., `ADMIN` and `USER` as basic ones. Possibly `SUPERADMIN` for system-level admin who can manage tenants. Each `User` has a role field (as in our user table). We included that in JWT claims.
- **Enforcing roles in backend:** Using Spring Security annotations like `@PreAuthorize` or configuring URL access rules is the simplest way. For example:

  - In controllers, use `@PreAuthorize("hasRole('ADMIN')")` on methods that only tenant admins should access. We did that on `createUser` in the example. This checks the role from the SecurityContext (populated from JWT).
  - You can also do `hasAuthority('ROLE_ADMIN')` (Spring considers roles as authorities with "ROLE\_" prefix).
  - For system-level endpoints (like create tenant), you might have a `@PreAuthorize("hasAuthority('ROLE_SUPERADMIN')")` and only the global admin user (maybe one in the master DB or special config) would have that.
  - You might also consider method-level security in services for critical business logic enforcement beyond controller (Spring Security can secure service methods too if configured with `@EnableGlobalMethodSecurity(prePostEnabled=true)`).

- **Frontend awareness:** The front-end should also adapt to roles (more on that in Frontend section), but the backend is the source of truth. For instance, even if a malicious user modifies front-end code to attempt an admin-only action, the backend’s RBAC will prevent it.

**Example RBAC scenario:** Only users with ADMIN role can delete projects:

```java
@DeleteMapping("/projects/{id}")
@PreAuthorize("hasRole('ADMIN')")
public ResponseEntity<?> deleteProject(@PathVariable Long id) {
    projectRepo.deleteById(id);
    return ResponseEntity.noContent().build();
}
```

If a non-admin calls this, they’ll get HTTP 403 Forbidden automatically by Spring Security.

For more fine-grained control, sometimes RBAC is combined with ABAC (attribute-based). For instance, you might allow a user to edit a project if they are its owner. In such cases, you can use expressions like `@PreAuthorize("#project.ownerUsername == authentication.name")` given the method has access to the project or id. But implementing that typically means fetching the object first. This is business-specific and beyond general multi-tenancy, but keep in mind how tenant and roles interplay: you might ensure that any cross-tenant data access is completely prevented by design (our setup does that at connection level) so role checks only need to consider within-tenant permissions.

### Exception Handling and Logging

A professional application needs consistent error handling and robust logging, especially in a multi-tenant environment where debugging issues for a specific tenant is important.

**Global Exception Handling:** Use a `@ControllerAdvice` to handle exceptions thrown by controllers globally. This can transform exceptions into meaningful HTTP responses (JSON error messages):

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<Map<String,String>> handleNotFound(EntityNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                             .body(Map.of("error", ex.getMessage()));
    }
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Map<String,String>> handleAccessDenied(AccessDeniedException ex) {
        return ResponseEntity.status(HttpStatus.FORBIDDEN)
                             .body(Map.of("error", "Access denied"));
    }
    // ... other handlers ...
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String,String>> handleGeneral(Exception ex) {
        // Log the exception with details:
        logger.error("Unexpected error in request", ex);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                             .body(Map.of("error", "Internal server error"));
    }
}
```

This way, instead of raw stack traces or HTML errors, the API returns clean JSON with appropriate status codes. This is particularly useful when debugging issues per tenant; for instance, if something is misconfigured for one tenant, the error might propagate as an Exception that can be logged and traced.

**Logging:** Use a logging framework (Spring Boot by default uses Logback). Important logging practices in multi-tenant apps:

- **Include tenant context in logs:** When logging events, it's extremely helpful to know which tenant the log entry relates to. We can leverage the fact we have a `TenantIdentifierResolver.currentTenant` (ThreadLocal). Using Mapped Diagnostic Context (MDC) is common: in the filter where we set tenant context, also do something like:
  ```java
  MDC.put("tenantId", tenantId);
  ```
  and remove it at the end:
  ```java
  MDC.remove("tenantId");
  ```
  Then configure your log pattern in `logback-spring.xml` or application.properties:
  ```
  logging.pattern.console=%d{HH:mm:ss} [%X{tenantId}] %-5level %logger{36} - %msg%n
  ```
  This will prefix each log with the tenantId from MDC. For example:  
  `12:00:00 [tenant1] INFO  c.e.m.service.ProjectService - Created project X...`
  If a log message is not within a request (no tenant), it might show `[null]` or empty. You can default it to `[master]` or similar by adjusting the pattern.
- **Sensitive data:** Never log sensitive information (passwords, secrets, personal data) to avoid breaches. Logging the fact that "User X from tenant Y failed login" or "Tenant Z exceeded quota" is fine, but not their password or full JWT.

- **Log levels:** Use appropriate levels (INFO for high-level events, DEBUG for detailed debugging, ERROR for exceptions). In multi-tenant apps, if one tenant experiences an error, you'll likely see ERROR logs tagged with that tenant, making it easier to pinpoint issues.

- **Structured logging:** Consider logging key events in a structured format (JSON logs) to easily filter by tenant in log management systems.

**Audit Logging (optional):** You may want to log certain actions, like an admin creating a user or a user deleting data, along with tenant info, for compliance or audit trails. Spring's `@EntityListeners` with `AuditingEntityListener` can capture who created/modified an entity (and we know who by `authentication.name` and tenant by context). This can be stored in fields or separate audit logs.

**Testing exception and logging:** Ensure that your multi-tenant context doesn't break error handling. For example, if an exception occurs after setting the tenant but before clearing it, the `TenantIdentifierResolver.clear()` in filter will still execute in finally, so context is cleared. Logging an error within that request will still show the tenant (since MDC was set). This is good – you know which tenant had the error.

At this point, we have a functioning backend that can:

- Authenticate users per tenant with JWT.
- Authorize based on roles.
- Isolate data per tenant via schema switching.
- Provide APIs for managing users (and similarly, you would implement domain data CRUD).
- Gracefully handle errors and log what's happening, including tenant identifiers.

Next, we'll turn to the frontend to utilize these backend capabilities.

## 5. Frontend Development with ReactJS & TypeScript

The frontend will provide a user interface for tenant users and admins to interact with the system. We will build it with React and TypeScript, integrating authentication, calling the backend APIs, and ensuring the UI reflects tenant-specific data and permissions.

### React + TypeScript Project Configuration (Vite/Webpack)

We already created the React project in the setup phase. Let's adjust and verify a few things for our use case:

- **Base URL and environment config:** If using different backend URLs for different environments, set that up. For example, create a file `src/config.ts` or use environment variables (Vite allows `import.meta.env` usage, CRA uses `REACT_APP_...` variables). For now, assume our backend API is at `http://localhost:8080`. We might set something like:

  ```js
  export const API_BASE_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8080";
  ```

  And in development, have a `.env` file for Vite with `VITE_API_URL=http://localhost:8080`.

- **Routing:** Install React Router if not done. Set up a router with routes for:

  - Login page (`/login`).
  - Main app page (maybe `/app` or just `/` after login) with sub-routes for things like `/users`, `/projects`, etc.
  - Possibly a route for tenant selection if needed (or if subdomains, not needed).

  Example using React Router v6:

  ```jsx
  import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
  import LoginPage from "./pages/LoginPage";
  import DashboardPage from "./pages/DashboardPage";
  // ... other imports
  function App() {
    const { token } = useAuth(); // custom hook from context or redux
    return (
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={token ? <Navigate to="/" /> : <LoginPage />}
          />
          <Route
            path="/*"
            element={token ? <MainLayout /> : <Navigate to="/login" />}
          />
        </Routes>
      </BrowserRouter>
    );
  }
  ```

  Here `MainLayout` could be a component that renders the common layout (nav bar, etc) and nested routes inside for the protected part of the app. We use conditional routing to prevent unauthorized access (if no token, redirect to login, if logged in, redirect away from login).

- **State management setup:** Decide how to manage global state. Potential strategies:

  - **Context API:** Simpler for holding the current user/tenant info and token. We can create an `AuthContext` that provides `token, user, login(), logout()`.
  - **Redux Toolkit:** If the app is complex (many slices of state, many components needing to access/update global state), setting up a Redux store might be beneficial. For example, a `authSlice` for auth state, `usersSlice` for user list if needed, etc.
  - **React Query (TanStack Query):** For server state (data fetched from the API), React Query is excellent. It handles caching, loading states, and refetching out of the box. We can use it for things like fetching list of projects, users, etc. It can work alongside Redux or context (React Query for server data, context for auth/tenant info).

  For this guide, let's use **React Context** for auth (to store token and tenant) and **React Query** for data fetching, as it simplifies caching by key, including by tenant.

- **Configure React Query:** Wrap your app with `QueryClientProvider`:

  ```jsx
  import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
  const queryClient = new QueryClient();
  function Root() {
    return (
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );
  }
  ```

  This should be done in `main.tsx` when rendering `<Root />` to DOM.

- **Auth Context Implementation:** Create `AuthProvider` using `React.createContext`.

  ```tsx
  type AuthContextType = {
    token: string | null;
    tenantId: string | null;
    user: { username: string; role: string } | null;
    login: (
      token: string,
      tenantId: string,
      user: { username: string; role: string }
    ) => void;
    logout: () => void;
  };
  const AuthContext = React.createContext<AuthContextType>(/* ... */);

  const AuthProvider: React.FC = ({ children }) => {
    const [token, setToken] = useState<string | null>(null);
    const [tenantId, setTenantId] = useState<string | null>(null);
    const [user, setUser] = useState<{ username: string; role: string } | null>(
      null
    );
    // Possibly load from localStorage if already logged in:
    useEffect(() => {
      const savedToken = localStorage.getItem("token");
      const savedTenant = localStorage.getItem("tenantId");
      const savedUser = localStorage.getItem("user");
      if (savedToken && savedTenant && savedUser) {
        setToken(savedToken);
        setTenantId(savedTenant);
        setUser(JSON.parse(savedUser));
      }
    }, []);
    const login = (
      tok: string,
      tenant: string,
      userData: { username: string; role: string }
    ) => {
      setToken(tok);
      setTenantId(tenant);
      setUser(userData);
      // store in localStorage for persistence
      localStorage.setItem("token", tok);
      localStorage.setItem("tenantId", tenant);
      localStorage.setItem("user", JSON.stringify(userData));
    };
    const logout = () => {
      setToken(null);
      setTenantId(null);
      setUser(null);
      localStorage.clear(); // or remove specific keys
    };
    return (
      <AuthContext.Provider value={{ token, tenantId, user, login, logout }}>
        {children}
      </AuthContext.Provider>
    );
  };
  ```

  This context provides `login` and `logout` functions and stores token info. We use localStorage to persist across page refreshes. Storing the token in localStorage is generally acceptable for JWT (though it can be vulnerable to XSS - we'll discuss security later). Alternatively, one could use httpOnly cookies for JWT, but that complicates CORS and CSRF aspects. We'll stick to localStorage for simplicity, but **ensure to handle XSS prevention**.

  Use this `AuthProvider` in the app root:

  ```jsx
  <AuthProvider>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </AuthProvider>
  ```

- **HTTP Client setup:** We'll use Axios or fetch for API calls. With React Query, you can use fetch directly in query functions, but an Axios instance is convenient to set base URL and headers. For instance:

  ```ts
  import axios from "axios";
  import { API_BASE_URL } from "./config";
  export const apiClient = axios.create({
    baseURL: API_BASE_URL,
  });
  // Add interceptor to include auth header for requests if token is set
  apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    const tenant = localStorage.getItem("tenantId");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    if (tenant && config.headers) {
      config.headers["Tenant-ID"] = tenant;
    }
    return config;
  });
  ```

  This way, any axios request will automatically include the JWT and Tenant-ID header. Since our backend expects Tenant-ID for login only (and in other requests, we actually don't need to send Tenant-ID header because the JWT covers it; however, if we want to be explicit or if backend wasn't using subdomain, it's not harmful to send it on all requests – the backend can ignore it after login or use it for double verification).

  Alternatively, you could not send Tenant-ID on every request (since we embed tenant in JWT, it’s redundant). The Marmelab tutorial showed adding tenantId to every API call via query params or headers, but warned that trusting the client on that is a bad idea ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=Why%20It%27s%20A%20Bad%20Idea)). **Our approach uses JWT for trust**, so the server doesn't rely on the Tenant-ID header except at login. We include it here mainly for login and maybe some convenience. It's important to note: the backend will actually derive tenant from JWT after login to enforce security, ignoring any mismatched Tenant-ID header a malicious user might send.

### Building Reusable UI Components

In a multi-tenant application, it's common to have repeated UI patterns across tenant-specific pages. For example, forms for creating/editing users or projects, lists/tables of records, etc. We should create reusable components to avoid duplication and to maintain consistency. Some examples:

- **Form components:** TextInput, Select, Button that follow a consistent style (if not using a UI library).
- **Table component:** A generic table that can display data rows, possibly with sorting/pagination controls.
- **Modal dialog:** For confirming deletions or editing in a popup.
- **Navbar/Sidebar:** A component that shows navigation links. This likely will include tenant-specific info like the tenant name, and different menu items depending on role (admins see "Manage Users", normal users might not).
- **Layout components:** If each page has common layout (header with tenant name, sidebar with menu, etc.), create a layout component that wraps page content.

Consider multi-tenancy specific UI elements:

- If you support switching between multiple tenants for a single login (some apps allow a consultant to switch context between client accounts), you might have a tenant selector dropdown in the navbar. That would require the front-end to handle changing tenant context (clearing data, loading new data, updating token if needed). In our scenario, we assume one tenant per login session, but it's something to note for more advanced use cases.

**Example:** a `<TenantHeader>` component that displays the tenant name (from context) and maybe the user name, with a logout button:

```tsx
const TenantHeader: React.FC = () => {
  const { tenantId, user, logout } = useAuth();
  return (
    <header className="tenant-header">
      <h1>{tenantId ? `Tenant: ${tenantId}` : "My App"}</h1>
      <div className="user-info">
        {user && (
          <span>
            Welcome, {user.username} ({user.role})
          </span>
        )}
        <button onClick={logout}>Logout</button>
      </div>
    </header>
  );
};
```

We might style it with CSS to separate the sections. This header can be used at top of each page.

**Theming and customization:** Some SaaS platforms allow each tenant to have custom branding (logo, colors). Implementing that might involve storing a theme per tenant in the master DB and delivering it to frontend (maybe as part of login response or a static URL for logo). Our guide won't go deep into this, but our UI components could be designed with theming in mind (using CSS variables or styled-components theme that can be changed based on tenant info).

### Implementing Authentication and Authorization Flows

**Login Flow (frontend):** Create a `LoginPage` component:

```tsx
import { useState } from "react";
import { apiClient } from "../apiClient";
import { useAuth } from "../AuthContext";

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const [tenant, setTenant] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      // call login API
      const response = await apiClient.post(
        "/login",
        { username, password },
        {
          headers: { "Tenant-ID": tenant },
        }
      );
      const { token } = response.data;
      // Decode token to get user info (or have backend return them separately)
      const decoded: any = jwtDecode(token);
      const tenantId = decoded.tenantId;
      const role = decoded.role;
      login(token, tenantId, { username, role });
      // Redirect to main page (you can use useNavigate from react-router)
      // ...
    } catch (err: any) {
      setError("Login failed. " + (err.response?.data?.error || ""));
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleSubmit}>
        <h2>Login</h2>
        <input
          value={tenant}
          onChange={(e) => setTenant(e.target.value)}
          placeholder="Tenant ID"
          required
        />
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        {error && <div className="error">{error}</div>}
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};
```

We use `jwtDecode` (from a library like `jwt-decode`) to decode the token on the client (since our backend didn't explicitly return user info except token). In a real scenario, you might prefer the backend to return user data and tenant in the response along with token to avoid decoding in front-end. But decoding is fine if the token is not encrypted (JWT is just base64 encoded). The Marmelab example did this: it decoded token to get tenantId ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=localStorage,%2F%2F%20...)) and stored it ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=localStorage,%2F%2F%20...)). We are doing similarly but we store via our context's `login` function.

After successful login, we navigate to the main application. Make sure to include error handling for wrong credentials (perhaps show error message).

**Protected routes:** We already used context to decide route access. The main thing is ensuring the token is present in the context (or localStorage) for protected pages. Our `AuthContext` approach covers that.

**Using roles on front-end:** The front-end should also tailor UI based on role:

- We can check `authContext.user.role` to conditionally render admin links. For example, in a sidebar menu component:

  ```tsx
  const Menu: React.FC = () => {
    const { user } = useAuth();
    return (
      <nav>
        <a href="/projects">Projects</a>
        {user?.role === "ADMIN" && <a href="/users">Manage Users</a>}
      </nav>
    );
  };
  ```

  This ensures that only admins even see the "Manage Users" section. Non-admins won't know it exists (security is still enforced on backend regardless). This improves UX by not presenting options that will be forbidden.

- You can also have route-level guarding. For example, using `<PrivateRoute>` pattern or just in your routes:
  ```jsx
  {
    user?.role === "ADMIN" ? <UsersPage /> : <Navigate to="/unauthorized" />;
  }
  ```
  but since the backend already returns 403 if unauthorized, it might be sufficient to just handle that gracefully (e.g., show a message if API returns 403). Still, hiding the UI is nice.

**State Management with Tenant Context:** Because our backend deals with tenant separation, the front-end mostly just needs to ensure it calls the right APIs with the token. However, consider scenario: if the app allowed switching tenant without full logout (say an admin who manages multiple tenants):

- We would need to update the tenantId in context, refetch data for new tenant, etc. Possibly even get a new token if our token is tenant-bound.
- In our simpler design, we assume one tenant per login session. If switching is needed, one could implement a dropdown that calls `authContext.login` with new tenant (which implies getting a token for that tenant – maybe by prompting for login again or if the same credentials work across tenants, a special token).

**React Query usage for API calls:**
Let's implement data fetching with React Query for, say, fetching list of users (only for admin):

```tsx
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../apiClient";

const UsersPage: React.FC = () => {
  const {
    isLoading,
    error,
    data: users,
    refetch,
  } = useQuery(["users"], async () => {
    const res = await apiClient.get("/api/users");
    return res.data as User[];
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading users</div>;

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users?.map((u) => (
          <li key={u.id}>
            {u.username} - {u.role}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

When this component mounts, `useQuery` will call the function which performs `GET /api/users`. Our axios interceptor will attach the JWT. The server returns users for that tenant only (and only if current user is admin thanks to backend checks). React Query caches the result by the key `['users']`. If the tenant context was part of the state, we should include it in the key to differentiate between tenants. **Important:** In a multi-tenant app where you might switch tenant without a full reload, you'd want `queryKey` to include tenant: e.g. `['users', tenantId]`. In our case, since tenantId won't change during a session, it's fine either way, but including it is safer if context might change:

```js
useQuery(['users', tenantId], ...);
```

and get tenantId from context.

Similarly, for projects:

```tsx
const { data: projects } = useQuery(["projects", tenantId], async () => {
  const res = await apiClient.get("/api/projects");
  return res.data;
});
```

This would fetch only the current tenant's projects.

**Mutations:** For creating or modifying data, we could use `useMutation` from React Query or just call our `apiClient.post` in an event handler and then call `queryClient.invalidateQueries(['users', tenantId])` to refresh cache. For example, adding a new user:

```tsx
const queryClient = useQueryClient();
const createUser = async (newUser) => {
  await apiClient.post("/api/users", newUser);
};
const { mutate: addUser } = useMutation(createUser, {
  onSuccess: () => {
    queryClient.invalidateQueries(["users", tenantId]);
  },
});
```

We would call `addUser(user)` on form submit to create user and then refresh the user list.

**UI state:** We should handle loading and error states in the UI gracefully (React Query gives isLoading, error). Also consider feedback for actions (e.g. show a success message after creating a user, or confirm before deleting one).

**Tenant-based UI differences:** If needed, you can incorporate tenant-specific logic. For example, maybe each tenant has some config that changes what features are visible. You could fetch a config from an endpoint and conditionally render features. This is beyond core multi-tenancy but often part of SaaS customization.

Finally, ensure your frontend is **tested** with multiple tenants:

- You might simulate by running the backend with two tenants in the DB and two sets of credentials, and logging in as each (maybe open two browsers or an incognito window vs normal to have separate sessions) to ensure they only see their own data.
- Check that switching the token (logging out and in as another tenant) properly clears old data.

### Managing Tenant-Based State with Redux or React Query

We largely covered this in the above subsections, but to summarize key points:

- **Separate caches/state per tenant:** If there's any possibility a user might switch tenant context within a session (or an admin tool that can view different tenant data), you must partition the state by tenant. This can be done by including `tenantId` as part of state keys. In Redux, you might namespace the slices or store a dictionary keyed by tenant. In React Query, as mentioned, include tenant in query keys to differentiate data caches ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=In%20a%20multi,filter%20the%20data%20requests%20accordingly)) ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=On%20login%2C%20the%20SPA%20receives,happens%20in%20the%20authentication%20provider)).

  For example, if an admin user of a SaaS can use an admin UI to inspect any tenant's data (like a support tool), then when they select a tenant, you would set something like `currentTenantForAdmin` state, and then queries use that. We won't delve deeper as our scenario is one tenant per login.

- **Avoid mixing data:** Do not accidentally reuse state from one tenant for another. This is a logical isolation on the client. Even though the server won't give wrong data, you could show stale data if you don't clear it. For instance, if your app did allow tenant switch, and you forgot to clear the Redux state, the user might momentarily see the previous tenant’s info until new data loads.

- **Global vs Tenant-specific state:** Some state might be global regardless of tenant (like UI theme, or static reference data that is same for all tenants). Keep that separate. Only partition the data that is per-tenant (like user lists, project lists, etc.).

- **Redux example:**

  ```js
  const initialState = {
    tenants: {} // e.g., { 'tenantA': { users: [...], projects: [...] }, 'tenantB': { ... } }
    currentTenant: null
  };
  // actions like setCurrentTenant, receiveUsersForTenant, etc.
  ```

  However, this can get complicated. It's often simpler to completely flush the state on tenant change (like logging out and logging in as new tenant), which our approach effectively does by requiring a new login.

- **React Query context sharing:** One cool feature: if your user remains the same but just the tenant changes, you can even keep multiple QueryClient instances or just rely on keys. But in our app, login triggers a full reload (we didn't implement a switch feature), so it's fine.

**One more thing**: The **frontend must be mindful of performance** when handling data. If a tenant has a huge dataset, you might need pagination on lists, search features, etc. Those can be implemented via backend support (e.g., `/api/projects?offset=0&limit=50`). Our guide doesn't implement pagination, but keep it in mind for large tenants.

Next, we address securing the API and optimizing performance, which affects both backend and how frontend usage patterns might need to adjust.

## 6. API Security and Performance Optimization

With functionality in place, we must ensure the application is secure and performant. Multi-tenant apps face additional challenges: one tenant should not be able to affect others, either in terms of security (data leakage) or performance (excessive resource use). We'll cover key strategies: rate limiting, caching, query optimization, and general API security best practices.

### Implementing API Rate Limiting

**Rate limiting** controls how often clients can call the API, to prevent abuse (e.g., a single user or tenant flooding the system with requests). In a multi-tenant context, you might implement rate limits per user, per tenant, or both:

- **Per-User rate limit:** e.g., a user can make at most 100 requests per minute.
- **Per-Tenant rate limit:** e.g., all users of a given tenant collectively can make at most 1000 requests per minute. This prevents one tenant from hogging resources and potentially degrading service for others.
- **Global rate limit:** overall system limit, which is less common except to mitigate total load or attacks.

In Spring Boot, there's no built-in rate limiter, but we can integrate a library like **Bucket4j** or use an API gateway (like an Nginx or Spring Cloud Gateway) to enforce limits.

**Using Bucket4j** (a Java rate-limiting library):

- We can add the `bucket4j-core` dependency (or use the Spring Boot starter for Bucket4j).
- Configure a filter or aspect that tracks requests. For example, a simple approach:

  ```java
  @Component
  @Order(1)
  public class RateLimitFilter extends OncePerRequestFilter {
      private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();
      @Override
      protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
              throws ServletException, IOException {
          String user = request.getUserPrincipal() != null ? request.getUserPrincipal().getName() : "anonymous";
          Bucket bucket = buckets.computeIfAbsent(user, k -> Bucket4j.builder()
                  .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
                  .build());
          if (bucket.tryConsume(1)) {
              filterChain.doFilter(request, response);
          } else {
              response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
              response.getWriter().write("Too many requests");
          }
      }
  }
  ```

  This example limits each user to 100 requests per minute. For per-tenant, you could key the map by tenantId (which you can get from `TenantIdentifierResolver.resolveCurrentTenantIdentifier()` or from SecurityContext's details).

  With Bucket4j, you can also use a distributed cache (like Redis) to track counters if you have multiple app instances (so that limiting is consistent across a cluster).

- Instead of a custom filter, you could integrate at the controller layer using annotations if you find a library that supports it, but a filter gives central control.

**Consider using an API Gateway:** If your architecture has a gateway (like Kong, Apigee, AWS API Gateway, or even a simple Nginx reverse proxy), those can implement rate limiting externally. Nginx, for example, can rate limit by IP or header. But rate limiting by tenant or user usually requires identifying them – with JWT, you could have Nginx decode the token (not trivial) or better, use a gateway that can parse JWT (Kong has plugins for that).

For simplicity, many put rate limiting in the application or a simple filter like above for moderate needs. The key is to return a proper HTTP 429 "Too Many Requests" when limit is exceeded, and possibly include a Retry-After header.

**Rate limit strategies:**

- You might allow bursts and then refill (token bucket algorithm) ([Rate Limiting with Bucket4J - Medium](https://medium.com/dandelion-tutorials/rate-limiting-with-bucket4j-for-spring-boot-web-1a42af2b8b80#:~:text=Rate%20limiting%20is%20a%20strategy,within%20a%20certain%20time%20frame)).
- E.g., 60 requests/min with bursts up to 10 at once could handle typical user behavior.
- Monitor usage patterns to set limits that don't hinder normal use but cap extreme cases.

**Protecting one tenant from another:** If using per-tenant limit, a noisy tenant will hit their cap and not affect others (assuming their threads eventually free up – also consider applying resource quotas at other levels like DB connection pools per tenant if needed).

Our application should also consider thread pools: by default, Tomcat has a limited thread pool; if one tenant floods requests, they could occupy threads. Rate limiting helps by quickly rejecting excess so threads free up.

### Caching Strategies for Performance

Caching can significantly improve performance and reduce load, but it must be done carefully in multi-tenant systems to avoid serving one tenant's data to another.

**Types of caching:**

- **Backend caching (in-memory or distributed):** e.g., cache results of expensive queries or computations.
- **Hibernate second-level cache:** Hibernate can cache entities or query results between requests. This can be enabled with a provider like EhCache or Caffeine. The cache key automatically includes the tenant identifier if using separate SessionFactory per tenant or properly configured region factory. In Hibernate's multitenant setup, the second-level cache might not be tenant-aware by default unless you consider each tenant a separate cache region. An easier approach is to not use second-level cache in a multi-tenant environment unless you partition it per tenant (to avoid any bleed).
- **Application-level caches:** For example, caching reference data that is same for all tenants, like a list of countries or product list if it's not tenant-specific. That can be global.
- **Tenant-specific cache:** If certain data is heavy to compute per tenant (like an analytics summary), you can cache it keyed by tenant.

**Cache Implementation in Spring Boot:**

- Use Spring's caching abstraction (`@EnableCaching`, `@Cacheable` etc.). For instance,
  ```java
  @Cacheable(cacheNames="projectsById", key="#tenantId + ':' + #projectId")
  public Project findProjectById(Long projectId) { ... }
  ```
  Here we manually include tenantId in the key to isolate caches ([Indexing TenantID in Multi Tenant DB - sql server - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=Overflow%20stackoverflow,will%20filter%20on%20this%20column)). You can get tenantId via a method param or using `TenantIdentifierResolver.resolveCurrentTenantIdentifier()`.
  - Configure a CacheManager with caffeine or redis. For a small app, caffeine (in-memory) is simplest. Just include `spring-boot-starter-cache` and an implementation.
- Ensure that any cached data is **invalidated** on changes. E.g., if you cache a project's details, and someone updates a project, call `cacheManager.getCache("projectsById").evict(tenantId + ":" + projectId)` in the update logic or use `@CacheEvict` annotations.

- Consider caching at the **service layer** for read-heavy endpoints. For example, if all users of a tenant frequently access a list of common data, caching it for that tenant can reduce DB load (in shared DB scenario, also improves overall DB usage).
- **Distributed cache (Redis):** If running multiple instances, an in-memory cache would be local to each instance. For multi-instance deployments, consider Redis or similar to share cache. Redis can use keys like `tenant:project:123 -> {...}`. This also could be used for session or token blacklists if needed.

**Front-end caching:**

- We used React Query which caches API responses on the client side. This prevents refetching data if the user navigates away and back to a page (within a certain time, by default React Query caches for 5 minutes).
- We have to ensure to invalidate or refetch on events like new data creation (which we did with `invalidateQueries`).
- The front-end caching is per user session and naturally tenant-scoped because a user only has their tenant's data. There's no risk of cross-tenant data mixing in front-end cache since each user only ever sees their own.

**HTTP caching:**

- We could use HTTP cache headers for GET responses. For example, if some resources rarely change, set `Cache-Control: max-age=60` etc. But in multi-tenant, caches (like browser cache or CDN) might need to vary by tenant (and by auth token which usually means it's not cached by public CDNs). Typically, data APIs with Authorization are not cached at proxies by default. But the browser might cache if you set it.
- It's safer to rely on the application caching and avoid HTTP caching for dynamic multi-tenant data, unless it's something like a public CDN for assets or truly public data.

### Database Indexing and Query Optimization

With each tenant's data isolated, we need to ensure queries are efficient:

- **Indexing:** As mentioned, if using a shared schema, index the `tenant_id` column (often as part of primary key or at least an index) ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=2)). For other commonly queried fields (e.g., username in users table), use indexes. In separate schema approach, each schema's tables should have indexes on important columns too (like username unique index, foreign key indexes, etc.). It's easy to forget to add an index on a non-primary foreign key column in each schema; make sure your DDL (or JPA mappings with `@Index` annotations or auto indexes from foreign keys) handle that.
- **Composite Primary Key vs separate index:** If tenant_id is part of PK, it ensures uniqueness across tenants for that table (which might not be needed if tenant data separate). If using separate schemas, the primary key can just be the ID. In shared schema, either composite PK (tenant_id + id) or a separate index on tenant_id plus an ID that is unique only per tenant. Either way, queries should include tenant filter to hit that index.
- **Query plans:** Monitor slow queries using MySQL's slow query log or EXPLAIN plan. If a query scanning a large table appears, consider adding indexes. Example: if you have an orders table and often query by date range per tenant, consider index on (tenant_id, order_date).
- **Avoid cross-tenant joins:** With separate schema, you likely won't do this by design. With shared schema, never join tables by different tenant_id or forget to include tenant in where clause. If using Hibernate filters or `@TenantId`, it should automatically include tenant in queries. But be cautious with native SQL or custom queries – always include tenant predicate.
- **Limit data fetched:** Use pagination on large lists (don't fetch 10k rows to the frontend at once).
- **Optimize writes:** Multi-tenant can stress the DB if one tenant does bulk writes. Consider batch operations (like JDBC batch) for large imports, and tune InnoDB settings for concurrency if needed.
- **Connection pool sizing:** For shared DB, you have one pool. For separate schemas on same DB, also one pool. If separate DB per tenant, you might have multiple pools. Ensure that if you have e.g. 100 tenants, you don't open 100 pools of 10 connections each if all tenants are active – that would be 1000 connections to MySQL potentially. In our approach, we keep one DataSource and switch schema, so we have one pool sized maybe 10-20 connections total. That handles concurrent requests across all tenants. If tenants are highly concurrent, maybe increase pool or use one pool per tenant id (complicates config).
- **Identify performance bottlenecks per tenant:** Keep an eye if one tenant's data size is huge causing slow queries. Maybe that tenant needs extra indexes or to be moved to its own DB (vertical partitioning).
- **Sharding consideration:** If you hit scale (like thousands of tenants, each with significant data), a single MySQL instance might not suffice. You could then shard tenants across multiple DB instances (like tenants 1-100 on DB1, 101-200 on DB2, etc.). This complicates routing (mapping tenant to the right DataSource). This is beyond initial development but something to consider as an extension. Azure’s SaaS guidance, for example, discusses splitting tenants into multiple databases when a single database can't handle all ([Multi-Tenant Architecture - SaaS App Design Best Practices](https://relevant.software/blog/multi-tenant-architecture/#:~:text=streamline%20resource%20management.%20,or%20recombined%20just%20as)).

### Secure API Best Practices (CORS, CSRF, XSS Mitigation, etc.)

Finally, ensure general security hygiene:

- **CORS (Cross-Origin Resource Sharing):** If your React frontend is served on a different domain (e.g., localhost:5173 or example.com) than the API (localhost:8080 or api.example.com), you must enable CORS in the backend. Spring Boot can allow specific origins:

  ```java
  @Configuration
  public class WebConfig implements WebMvcConfigurer {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
          registry.addMapping("/**")
                  .allowedOrigins("http://localhost:5173", "https://app.example.com")
                  .allowedMethods("GET","POST","PUT","DELETE")
                  .allowedHeaders("*")
                  .exposedHeaders("Authorization")
                  .allowCredentials(true);
      }
  }
  ```

  This allows our frontend origin to call the API. Without this, the browser will block cross-site requests. If using JWT in header, you might not need `allowCredentials` (that's for cookies).
  Ensure in production to set the allowed origin to your actual domain and not `*` (never use `*` with credentials).

- **CSRF (Cross-Site Request Forgery):** We disabled CSRF in our security config because we use stateless JWT. CSRF mainly applies if you're using cookies for session – an attacker could trick a user's browser to use their session. With JWT in header and no cookies, CSRF is less of an issue. Just ensure you **do not accept the token from GET requests or in URL**, only from header. In our config, `.csrf().disable()` is appropriate. If you did use cookies, then you would need CSRF tokens in requests or SameSite cookies to protect.
- **XSS (Cross-Site Scripting):** This is mostly a frontend concern. However, the backend should be careful about output encoding if it ever injects data into HTML (which it typically doesn't in a JSON API). Still:
  - Validate or sanitize inputs that might contain HTML or script. For example, if tenants can set a company name and they put `<script>alert(1)</script>`, when your front-end displays that, it could execute. The front-end should escape it (React does this by default when rendering strings, unless using `dangerouslySetInnerHTML`).
  - If you store rich text (like descriptions), consider using libraries to sanitize HTML on input or output.
  - Ensure response headers like `Content-Type: application/json` are set so browsers don't interpret JSON as HTML.
- **SQL Injection:** Using JPA repositories or prepared statements prevents injection by default. Avoid constructing JPQL/SQL with string concatenation of untrusted input. If you must use `@Query` with native SQL and include a parameter, use placeholders like `:tenantId` or `?` binding. Parameter binding in JPA/PreparedStatement will handle escaping. This is particularly important if any admin interfaces allow running custom queries per tenant (rare, but just in case).
- **Sensitive Data in logs:** As mentioned, avoid logging credentials or personal data. Also, secure any secrets (JWT signing key should be in config not in code, and in production an environment variable or vault).

- **Encryption:** Use HTTPS for all client-server communication in production. This prevents sniffing JWTs or any data. Ensure TLS is properly configured if deploying (if using a load balancer or proxy, termination might be there).
- **JWT security:**

  - Choose a strong signing key. If using symmetric signing (HMAC), a long random secret. Or use RSA keys (asymmetric) for JWT so you could separate issuer and resource servers.
  - Set appropriate token expiration (we used 1 hour in example). Consider refresh token mechanism if needed for long sessions.
  - If a user logs out or is removed, the JWT is still valid until expiry. For high security, you could implement a token blacklist or revocation list (stored in Redis or DB) to invalidate tokens early. But that adds complexity. Many apps accept that token remains valid short time. You could also shorten expiry and require re-login or silent refresh.

- **Never trust the client for tenant enforcement:** We saw in Marmelab's tutorial that relying on the client to send the tenant ID is a bad idea because a malicious user could alter it and access someone else's data ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=Why%20It%27s%20A%20Bad%20Idea)). Our design defends against this by using JWT claims on the backend to set the tenant context. Even if an attacker manually set a different Tenant-ID header on requests, our backend would still use the tenant from the JWT (and if they somehow got a token for another tenant, that's another story - but that means they are authenticated as that tenant's user anyway).

  So rule: **Tenant isolation must be enforced server-side.** Double-check every place that queries data: is it using the proper tenant filter/context? In our case, yes, because of the connection switching. If we had a case where user input is used in a query (like an admin passing a tenant ID to view that tenant's data), ensure only authorized roles can do that, and still enforce it in query.

- **Penetration testing and audits:** It's wise to test the application for vulnerabilities. E.g., try to call an API with a token from another tenant or manipulated fields and ensure it fails. Use tools (OWASP ZAP or others) to scan for issues like injection or missing headers.

Finally, keep dependencies updated (security fixes) and consider using a Web Application Firewall (WAF) if the app grows (to mitigate generic attacks).

By applying these security and optimization practices, the application will be more robust and reliable for all tenants.

Next, we consider how to deploy and scale this multi-tenant application.

## 7. Deployment & Scaling

Deploying a multi-tenant application requires packaging the software, setting up the necessary infrastructure (for web, application, and database servers), and preparing for scaling as more tenants onboard. We'll discuss containerizing the app with Docker, deploying to a cloud environment with Kubernetes, setting up CI/CD pipelines, and monitoring the system in production.

### Dockerizing the Application

**Why Docker?** Using Docker containers ensures that the application runs consistently across environments (dev, staging, production). We can create separate images for the frontend and backend, or combine them depending on architecture. Typically, we'll have:

- A Docker image for the React app (which will likely serve static files via Nginx or be included in the Spring Boot jar as static resources).
- A Docker image for the Spring Boot API.
- A MySQL container for local dev or use managed DB in prod.

Let's create Dockerfiles:

**Frontend Dockerfile (if deploying separately):**
We can build the React app and serve it using a lightweight web server (Nginx):

```
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build  # produces static files in dist or build folder

# Stage 2: Serve with Nginx
FROM nginx:1.23-alpine
COPY --from=build /app/dist /usr/share/nginx/html  # for Vite, 'dist' is default build output
COPY --from=build /app/build /usr/share/nginx/html  # for CRA, 'build' folder
# Copy a custom nginx config if needed (to handle routing, etc.)
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

This multi-stage build first uses Node to compile the app, then uses Nginx to serve static content. The `nginx.conf` can be configured to route all requests to `index.html` (for client-side routing), and possibly proxy API calls to the backend if on the same domain (or we keep them separate domains).

If the frontend is just static files, we could also host it on a CDN or S3. But using Nginx in a container is fine for now.

**Backend Dockerfile:**

```
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn package -DskipTests

FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /app/target/multi-tenant-app.jar /app/app.jar
EXPOSE 8080
CMD ["java", "-jar", "/app/app.jar"]
```

This uses a multi-stage build as well: first stage compiles the Maven project, second stage runs the jar. We expose port 8080. (In a real pipeline, you might not build inside Docker like this but rather use CI to build the jar and then just copy it; both approaches are viable).

After creating these Dockerfiles, build the images:

```bash
docker build -t mycompany/multi-tenant-frontend:1.0 .
docker build -t mycompany/multi-tenant-backend:1.0 .
```

You might tag them with version or `latest`.

**Docker Compose (for local dev):** It can be helpful to have a `docker-compose.yml` to run multi containers together:

```yaml
version: "3"
services:
  frontend:
    build: frontend/.
    ports:
      - "3000:80" # serve front on 3000
    depends_on:
      - backend
  backend:
    build: backend/.
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/multitenant_master
      - SPRING_DATASOURCE_USERNAME=root
      - SPRING_DATASOURCE_PASSWORD=example
    ports:
      - "8080:8080"
    depends_on:
      - db
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: multitenant_master
    ports:
      - "3306:3306"
```

This defines three containers: frontend, backend, and db. In this config, the backend connects to the `db` service (we use service name in the JDBC URL). For production, you'd likely use a managed DB and not run MySQL in a container (unless you run it in K8s stateful set, but managed is easier).

**Configuration Management:** Use environment variables for things like DB credentials, JWT secret, etc., rather than hardcoding. We can supply them via Docker/K8s secrets.

### Deploying on AWS/GCP with Kubernetes

For scaling and robust management, Kubernetes is a common choice. Let's outline deploying our app to a K8s cluster (could be AWS EKS, GCP GKE, or Azure AKS – the process is similar).

**Kubernetes Setup:**

- Ensure you have a cluster running (for testing, you might use a local kind/minikube, but production will be cloud).
- Push your Docker images to a registry accessible by cluster (e.g., AWS ECR or Docker Hub).

**K8s manifests:**

- **Namespace:** Create a namespace, e.g., `multi-tenant-app`, to isolate resources.
- **Deployment for Backend:**

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: multi-tenant-backend
    namespace: multi-tenant-app
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: multi-tenant-backend
    template:
      metadata:
        labels:
          app: multi-tenant-backend
      spec:
        containers:
          - name: backend
            image: mycompany/multi-tenant-backend:1.0
            ports:
              - containerPort: 8080
            env:
              - name: SPRING_DATASOURCE_URL
                value: "jdbc:mysql://<db-host>:3306/multitenant_master"
              - name: SPRING_DATASOURCE_USERNAME
                valueFrom:
                  secretKeyRef:
                    name: db-secret
                    key: username
              - name: SPRING_DATASOURCE_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: db-secret
                    key: password
              - name: JWT_SECRET
                valueFrom:
                  secretKeyRef:
                    name: jwt-secret
                    key: secret
            resources:
              requests:
                cpu: "500m"
                memory: "512Mi"
              limits:
                cpu: "1"
                memory: "1Gi"
  ```

  We define 3 replicas for high availability (you can adjust). We pass DB connection info and secrets. `db-secret` would be a K8s Secret object containing the sensitive info. We also set resource requests/limits to help K8s schedule properly and to avoid one pod using unlimited CPU/memory.

- **Service for Backend:**

  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: backend-service
    namespace: multi-tenant-app
  spec:
    selector:
      app: multi-tenant-backend
    ports:
      - port: 8080
        targetPort: 8080
        name: http
    type: ClusterIP
  ```

  This allows other services (like frontend or ingress) to reach the backend via DNS `backend-service`.

- **Deployment for Frontend:**
  If we containerized the frontend:

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: multi-tenant-frontend
    namespace: multi-tenant-app
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: multi-tenant-frontend
    template:
      metadata:
        labels:
          app: multi-tenant-frontend
      spec:
        containers:
          - name: frontend
            image: mycompany/multi-tenant-frontend:1.0
            ports:
              - containerPort: 80
  ```

  - **Service for Frontend:**
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: frontend-service
      namespace: multi-tenant-app
    spec:
      selector:
        app: multi-tenant-frontend
      ports:
        - port: 80
          targetPort: 80
          name: http
      type: ClusterIP
    ```
    Alternatively, you might skip the frontend Deployment if you host static files on S3/CloudFront or serve it via the backend. But separate is cleaner scaling (you can scale backend separate from front).

- **Ingress:** To expose to the internet, set up an Ingress (with an ingress controller like Nginx Ingress or cloud-specific).
  For example:

  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: multi-tenant-ingress
    namespace: multi-tenant-app
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /$1
  spec:
    rules:
      - host: app.example.com
        http:
          paths:
            - path: /(.*)
              pathType: Prefix
              backend:
                service:
                  name: frontend-service
                  port:
                    number: 80
      - host: api.example.com
        http:
          paths:
            - path: /?(.*)
              pathType: Prefix
              backend:
                service:
                  name: backend-service
                  port:
                    number: 8080
  ```

  This assumes you have two domains, or you can have one domain and differentiate by path (less ideal for separating concerns). If using subdomains per tenant:

  - You would configure a wildcard in DNS (`*.example.com` pointing to ingress) and use an annotation like `nginx.ingress.kubernetes.io/server-alias: *.example.com` mapping to the frontend service. Then all `tenantX.example.com` go to the same frontend. The frontend code can read `window.location.hostname` to know tenant, or the backend can use it if it gets passed. This requires some additional config for multi-host in ingress.
  - For backend, you might just use one host (api.example.com) since it doesn't vary by tenant in domain (we rely on token or header for tenant).

  TLS can be added via cert-manager or specifying secrets for the hosts.

**Auto-scaling:**

- Configure Horizontal Pod Autoscaler for backend:

  ```yaml
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: backend-hpa
    namespace: multi-tenant-app
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: multi-tenant-backend
    minReplicas: 3
    maxReplicas: 10
    metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
  ```

  This will scale pods if CPU usage goes above 70%. Similar can be done based on memory or custom metrics (like request per second if metrics are fed to Kubernetes).

- **Scaling MySQL:** Use a managed DB service if possible which can scale vertically or use read replicas. For multiple tenants, you might eventually shard or have replicas for heavy read load. But initial deployment might be a single MySQL instance or cluster.

- **File storage:** If tenants can upload files, you'd want a shared storage (S3, etc.). Not covered here, but note if needed.

### CI/CD Pipelines with GitHub Actions or Jenkins

Automating build, test, and deployment is essential. Let's outline a GitHub Actions workflow:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          distribution: "temurin"
          java-version: "17"
      - name: Back-end - Build and Test
        run: mvn verify
      - name: Front-end - Install and Test
        run: |
          cd frontend
          npm ci
          npm run test -- --watchAll=false
      - name: Build Docker images
        run: |
          docker build -t mycompany/multi-tenant-backend:${{ github.sha }} -f backend/Dockerfile .
          docker build -t mycompany/multi-tenant-frontend:${{ github.sha }} -f frontend/Dockerfile .
      - name: Push Docker images
        uses: docker/login-action@v2
        with:
          registry: docker.io
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Push images
        run: |
          docker push mycompany/multi-tenant-backend:${{ github.sha }}
          docker push mycompany/multi-tenant-frontend:${{ github.sha }}
  deploy:
    needs: build-test
    runs-on: ubuntu-latest
    env:
      KUBE_CONFIG_DATA: ${{ secrets.KUBE_CONFIG_DATA }}
    steps:
      - name: Deploy to Kubernetes
        uses: appleboy/ssh-action@v0.1.6
        with:
          host: ${{ secrets.KUBE_HOST }}
          username: ${{ secrets.KUBE_USER }}
          key: ${{ secrets.KUBE_SSH_KEY }}
          script: |
            kubectl set image deployment/multi-tenant-backend backend=mycompany/multi-tenant-backend:${{ github.sha }} -n multi-tenant-app
            kubectl set image deployment/multi-tenant-frontend frontend=mycompany/multi-tenant-frontend:${{ github.sha }} -n multi-tenant-app
```

This is a simplified example:

- On push to main, it runs tests, builds images, pushes them to Docker Hub (with commit SHA as tag).
- Then it uses an SSH action to run kubectl to update the deployments' images (assumes we have access; one could also use the Kubernetes deploy action or set up a runner with kubectl config).
- Alternatively, for GitHub Actions, one might use the `azure/k8s-deploy` action or similar if on Azure, or configure OIDC to authenticate to cloud.
- For Jenkins, you would do similar steps in a Jenkinsfile (checkout code, run `mvn verify`, run `npm test`, then build/push docker images, then kubectl apply or helm upgrade).

**Deployment Strategy:** Consider using a rolling update (K8s does by default for Deployment). This ensures zero downtime (launch new pods with new version, then terminate old). If DB migrations are involved that are not backward compatible, you might need a strategy to apply migrations first or design backward-compatible changes.

**Infrastructure as Code:** Manage K8s manifests with Helm or Kustomize for easier updates. Helm can templatize and you can run `helm upgrade` in CI/CD.

### Monitoring and Logging with Prometheus & Grafana

Monitoring a multi-tenant app is crucial to catch issues early and ensure performance. **Prometheus** is a popular monitoring system and **Grafana** for dashboards.

**Metrics to monitor:**

- Application metrics: request rate, error rate, response time, memory usage, CPU usage, DB connection count, etc.
- Multi-tenant specific: Perhaps track number of active users per tenant, or separate metrics per tenant (though be careful with Prometheus label cardinality – having tenant as a label can explode if you have many tenants). If number of tenants is moderate and stable, you could tag metrics with tenant id. For large scale, aggregate metrics might be better.

**Spring Boot Actuator:** Include `spring-boot-starter-actuator` and enable Prometheus exposure:

```properties
management.endpoints.web.exposure.include=health,metrics,prometheus
management.endpoint.prometheus.enabled=true
```

This provides a `/actuator/prometheus` endpoint that Prometheus can scrape. It includes default metrics like HTTP request counts (if `spring-boot-starter-metrics` is on the classpath, which Actuator brings via Micrometer).

- By default, metrics like `http_server_requests_seconds_count{uri="/api/projects",status="200",...}` will be available. They might not have tenant dimension by default (Micrometer's Web metrics likely aggregate across all).
- If you want per-tenant metrics, you could use **Micrometer Tagging**. For example, in controllers or services, you might record a metric and tag it with tenant:
  ```java
  @Autowired MeterRegistry registry;
  ...
  registry.counter("tenant.requests", Tags.of("tenantId", currentTenant)).increment();
  ```
  But if `currentTenant` has high cardinality (like hundreds of distinct values), this can bloat Prometheus. If you have, say, under 50 tenants, it's okay to tag, but if you plan for 1000s, avoid using tenant as tag in metrics. Instead, aggregate by tenant outside Prom (e.g., logs analysis or separate DB).
- Grafana can visualize metrics. You might create graphs for overall throughput, error rates, etc. If you do have tenant tags, you can create a Grafana variable for tenant and filter dashboards by it (e.g., to see metrics for one tenant).
- Monitor JVM metrics too (Actuator provides memory, GC, threads).

**Logging**: Centralized logging is important. Use a solution like EFK (Elasticsearch-Fluentd-Kibana) or Grafana Loki for logs:

- Deploy a Fluent Bit/Fluentd to collect logs from containers and push to Elasticsearch or Loki.
- Kibana or Grafana Loki UI to search logs.
- As suggested, include tenant context in log statements ([Multi-tenancy -The shared database, separate schema approach... with a flavour of separate database on top! | CIVIC UK](https://www.civicuk.com/blog-item/multi-tenancy-shared-database-separate-schema-approach-flavour-separate-database-top#:~:text=Well%2C%20it%27s%20nothing%20more%20than,perfect%20for%20our%20use%20case)). This way, in Kibana you can filter logs by tenantId easily (e.g., search for `tenantId: "tenantA"`).

**Alerting:** Set up alerts for:

- High error rates (e.g., >5% requests failing in last 5 min).
- High latency (95th percentile response time above threshold).
- Resource saturation: CPU > 90% for sustained period, memory nearing limits, DB connections exhausted, etc.
- Specific tenant anomalies: if you decide on per-tenant metrics, maybe alert if one tenant's usage is extremely high (could indicate abuse or runaway process).
- Tenant onboard/offboard events (perhaps a Slack notification when a new tenant is created or if a tenant's DB migration fails).

**Scaling considerations:**

- Keep an eye on how adding tenants affects metrics. For example, memory usage might grow with more tenants if caches or thread contexts accumulate something per tenant.
- Database: Monitor slow queries or locks. If one tenant's pattern causes issues (like they start a heavy report that slows down queries), you might catch it via long query monitoring.

**Use cases:**

- Grafana Dashboard "Overall System Health": showing total requests, split by success/error, perhaps a breakdown per API endpoint.
- Grafana Dashboard "Tenant Usage": if possible, showing number of requests per tenant (maybe from logs or a custom metric).
- Prometheus can also monitor MySQL (via mysqld exporter) to see connections, slow queries, etc.
- Setup PromQL queries for things like `sum(rate(http_server_requests_seconds_count{status!~"2.."}[5m]))` for error rate.

By deploying on Kubernetes with proper monitoring and logging, you can scale horizontally and maintain visibility into the app’s behavior across all tenants. Use the elasticity of K8s to handle increasing load: the combination of HPA and careful DB scaling (vertical or read replicas) will help handle more tenants or higher usage.

Finally, we'll discuss testing and maintenance to ensure the system remains reliable and up-to-date.

## 8. Testing & Maintenance

Building the application is half the battle; ensuring it works correctly and can be maintained over time is equally important. We'll cover testing strategies (unit, integration, load testing), managing database schema changes across tenants (migrations), and general maintenance best practices for a multi-tenant system.

### Unit and Integration Testing

**Unit Testing (Backend):** Use JUnit (and possibly Mockito) to test service logic and controllers in isolation:

- Test edge cases of the multi-tenant logic. For example, test the `TenantIdentifierResolver` class to ensure it returns default if none set, etc.
- Test service methods for correct behavior per role. If you have a method to create a user, test that a normal user cannot execute it (this might be more of an integration test with Spring Security context).
- Use Spring's `@WebMvcTest` or `@DataJpaTest` for slice testing:

  - With `@DataJpaTest`, you can load JPA and test repository queries. For instance, you could manually set the tenant context and call repository to ensure it fetches correct data for that tenant.
  - However, `@DataJpaTest` by default uses an H2 in-memory DB; we need to ensure our multitenant config works with H2 or use Testcontainers for MySQL.
  - Alternatively, use `@SpringBootTest` to load full context with multi-tenancy and an H2/MySQL connection. You can define multiple schemas in H2 for testing schema-per-tenant (H2 supports schemas).

  Example integration test:

  ```java
  @SpringBootTest
  class MultiTenancyIntegrationTest {
      @Autowired UserRepository userRepo;
      @Autowired TenantIdentifierResolver tenantResolver;
      @Test
      void testIsolatedUserData() {
          // Setup: create user in tenant1
          tenantResolver.setCurrentTenant("tenant1_db");
          userRepo.save(new User("alice", "passhash", "USER"));
          // Setup: create user in tenant2
          tenantResolver.setCurrentTenant("tenant2_db");
          userRepo.save(new User("bob", "passhash2", "USER"));
          // Test: ensure each tenant sees only their user
          tenantResolver.setCurrentTenant("tenant1_db");
          List<User> users1 = userRepo.findAll();
          assertThat(users1).extracting(User::getUsername).containsExactly("alice");
          tenantResolver.setCurrentTenant("tenant2_db");
          List<User> users2 = userRepo.findAll();
          assertThat(users2).extracting(User::getUsername).containsExactly("bob");
      }
  }
  ```

  This test manually switches tenant context (which simulates different requests) and verifies data isolation ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=createPerson%28PIVOTAL%2C%20)) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=currentTenant.setCurrentTenant%28VMWARE%29%3B%20assertThat%28persons.findAll%28%29%29.extracting%28Person%3A%3AgetName%29.contai%20nsExactly%28)). Use similar approach for other entities.

- Test the security layer: use Spring Security's test support to run methods with certain `Authentication`. For example, use `@WithMockUser(username="admin", roles={"ADMIN"})` on a test method and call your controller method to see if it allows an admin and rejects a non-admin. Also test that unauthorized access returns 403.

**Unit Testing (Frontend):** Use Jest (which comes with CRA or can be added to Vite via libraries) plus React Testing Library:

- Test components render correctly given props (maybe not much tenant-specific logic inside components beyond props).
- Test that a page makes an API call and displays results (you can mock `apiClient` or use MSW to simulate API).
- Test context logic: e.g., simulate login and ensure it sets values.
- Ensure role-based UI hiding works (e.g., given a context with role USER, the admin menu link is not present).
- You can also use Cypress or Selenium for end-to-end: run the app and simulate a user logging in and performing actions. For multi-tenancy, you could have tests for two different tenants to ensure they each see their data.

**Integration Testing (Full Stack):** Optionally, use a tool like **Cypress** for end-to-end testing:

- Start the entire app (perhaps using Docker compose or local processes).
- Use Cypress to automate a browser: log in as tenant1 user, create an entity, log out, log in as tenant2 user, ensure tenant1's data isn't visible, etc. This gives confidence the app works in a real scenario.

**Testing configuration:**

- Use separate config for tests. E.g., `application-test.properties` to point to a test database (maybe H2 or a specific MySQL schema). Ensure multi-tenancy config is loaded (maybe some adjustments for H2 like `spring.jpa.properties.hibernate.default_schema=PUBLIC` etc).
- If using Testcontainers, you can spin up a MySQL container for integration tests and have schemas created.

**Continuous testing:** As part of CI, run these tests on each commit. This catches regressions early.

### Load Testing Strategies

Load testing helps ensure the application can handle multiple tenants and high usage:

- Use tools like **JMeter**, **Gatling**, or **Locust** to simulate load.
- Design test scenarios reflecting real usage:
  - e.g., 100 concurrent users spread across 10 tenants, each performing login and fetching some data, maybe creating some entries.
  - Ensure the test covers the multi-tenant nature: test both many users on one tenant and many users on many tenants.
- For Gatling (Scala-based), you could have a simulation where each virtual user is assigned a tenant ID and credentials (maybe pre-create 10 test tenants with test users).
- Measure throughput (requests/sec) and response times. Check if any errors occur under load.
- Identify bottlenecks: Perhaps the database CPU goes high, or memory usage spikes. Use APM (Application Performance Monitoring) tools or JConsole during load to see if any resource is saturated.
- Test scaling: If possible in a staging environment with Kubernetes, you can do a load test that triggers the autoscaler to add pods. Ensure the system continues serving requests while scaling up.
- Noisy neighbor test: Simulate one tenant doing something heavy (like uploading lots of data or making many rapid requests) while others are doing normal operations. See if the others experience slowdown. If yes, consider increasing isolation (e.g., per-tenant rate limit, more resources).
- Soak test: run a moderate load for an extended period to see if any memory leaks or stability issues arise over time.

Use the results to adjust configurations:

- Maybe you need a higher connection pool size or bigger instance if CPU is maxing out.
- Or maybe caching needs to be added if certain repeated requests cause load.

### Database Migrations and Versioning

As the application evolves, you'll need to update the database schema (add tables, columns, etc.). In a multi-tenant environment, schema changes must apply to all tenant schemas (and the master schema if needed).

**Use Flyway or Liquibase:** These tools version-control your database changes:

- Flyway: maintains a schema history table in each schema to track applied migrations.
- Liquibase: uses an XML/JSON/YAML changelog.

We will use Flyway for example:

- Add Flyway dependency: `spring-boot-starter-flyway`.
- By default, Flyway will run migrations on the primary `spring.datasource` schema. But in multi-tenant, we want:
  - Migrations on the master schema (for the `tenants` table, etc.).
  - Migrations on each tenant schema.

One approach (as noted in Sultanov's tutorial) is to run Flyway programmatically for each tenant ([Schema-based multi-tenancy with Spring Data, Hibernate and Flyway](https://sultanov.dev/blog/schema-based-multi-tenancy-with-spring-data/#:~:text=The%20tables%20in%20the%20shared,to%20perform%20different%20migrations%20in)) ([Schema-based multi-tenancy with Spring Data, Hibernate and Flyway](https://sultanov.dev/blog/schema-based-multi-tenancy-with-spring-data/#:~:text=these%20schemas%2C%20and%20we%20will,directory)):

- Disable Flyway auto-run by setting `spring.flyway.enabled=false` (so it doesn't try to migrate only the master on startup).
- Create a bean that on application startup (or on an admin command) does:

  ```java
  @Component
  public class FlywayRunner {
      @Autowired DataSource dataSource;
      @Autowired TenantRepository tenantRepo;
      @EventListener(ApplicationReadyEvent.class)
      public void migrateAll() {
          // Migrate master schema (default)
          Flyway.configure()
              .dataSource(dataSource)
              .schemas("multitenant_master")
              .locations("classpath:db/migration/master")
              .load()
              .migrate();
          // Migrate each tenant schema
          List<Tenant> tenants = tenantRepo.findAll(); // this reads from master schema
          for (Tenant t : tenants) {
              Flyway.configure()
                  .dataSource(dataSource)
                  .schemas(t.getDbSchema())
                  .locations("classpath:db/migration/tenant")
                  .load()
                  .migrate();
          }
      }
  }
  ```

  In this setup, you maintain two sets of migrations: one for master (in `db/migration/master`) and one for tenant schemas (in `db/migration/tenant`). For example:

  - `db/migration/master/V1__Create_tenants_table.sql`
  - `db/migration/tenant/V1__Create_user_and_project_tables.sql` (this will run in each tenant schema).
    And when you need to add a new column to a tenant table:
  - `db/migration/tenant/V2__Add_due_date_to_projects.sql` - this will be applied to each tenant schema.

  Flyway will keep a `flyway_schema_history` table in each schema to track migrations applied ([Schema-based multi-tenancy with Spring Data, Hibernate and Flyway](https://sultanov.dev/blog/schema-based-multi-tenancy-with-spring-data/#:~:text=The%20tables%20in%20the%20shared,to%20perform%20different%20migrations%20in)).

  Another idea: for schema-per-tenant, you could connect to each schema separately and run migration command, but the above loop is effectively doing that logically.

- If using database-per-tenant with separate DataSources, you'd loop through each DataSource or connection info similarly.

**Deployment ordering:** When deploying a new version that requires a DB change:

- Option 1: Run migrations first (out-of-band) then deploy app (which expects the new schema). This could cause new fields to be present that old code doesn't use (which is fine, forward-compatible) or if removing fields, that could break old code if done too early.
- Option 2: Deploy app which runs migrations on startup (as above). This is simpler but ensure the app can handle if migration takes time (it runs at startup serially; if many tenants, startup could be slow applying all migrations). In that case, you might prefer a manual migration step.

- Aim for _backwards-compatible migrations_: e.g., add new columns that new code will use, but old code ignoring them is fine. If removing or renaming columns, maybe do a phased approach (mark deprecated, update code to not use them, then remove in a later release after no code depends).

- Test migrations in a staging environment with multiple dummy tenant schemas to gauge if any issues.

**Versioning the application:** Keep track of application version vs database version. Flyway helps with DB version. If a certain version of app expects at least certain migration, document it. If you support rolling deployments (some nodes new, some old), ensure compatibility:

- E.g., new code should not break if it runs before migration (so maybe don't immediately require new column).
- Or do DB migration first, which older code can tolerate (like extra column doesn't affect old code), then deploy new code using it.

### Best Practices for Maintaining a Multi-Tenant System

Maintaining a multi-tenant application involves operational, security, and support practices:

- **Regular Backups:** Ensure you have backups for all tenant data. If using one database for all, back it up as a whole. If separate schemas, still one backup covers all (or you can export per schema for finer control). Test restore procedures. In case one tenant needs data recovery (due to some data issue), how will you restore just their portion? One idea: if using separate schemas, you can potentially restore that schema from backup to a temp location and then import. With shared schema, you'd need to restore the whole and extract that tenant's data – complicated. So, schema-per-tenant is beneficial for maintenance in that sense.
- **Monitoring per tenant usage:** Create internal reports or admin dashboards that show tenant-level usage: e.g., number of logins, API calls, data storage size. This helps identify if a tenant is growing significantly or if one is idle.
- **Scaling DB for tenants:** If one tenant becomes extremely large or performance-intensive, consider migrating them to their own database or cluster (a form of _tenant isolation_ upgrade). Your app can handle DB-per-tenant with minor config changes if built for it (like using routing DataSource). Plan a procedure for migrating a tenant's data from shared DB to a separate DB if needed (maybe an export-import and then point that tenant's entry in master to new DB connection).
- **Onboarding automation:** Streamline adding new tenants. Possibly provide a self-service sign-up that triggers tenant creation. Automate steps like schema creation and default data setup using scripts or code (maybe reuse Flyway to init new schema).
- **Offboarding:** If a tenant leaves, decide how to handle data. Likely archive their data or give them an export, then delete. Ensure deletion is thorough to meet GDPR or privacy requirements if applicable.
- **Upgrading Dependencies:** Keep dependencies (React, Spring Boot, etc.) up to date for security fixes. Test thoroughly in staging for regressions, especially any that could affect multi-tenancy features (like a major Hibernate upgrade).
- **Documentation:** Document the multi-tenant design and any operational procedures. New developers or DevOps engineers should understand how tenants are separated, how to run migrations, how to troubleshoot an issue that might only affect one tenant.
- **Support & Debugging:** When an issue is reported by a single tenant, your logging and metrics should allow you to zoom in on that tenant’s activity. For example, filter logs by their tenantId, or check if metrics (like errors) spiked for just that tenant. This helps in multi-tenant support to isolate the problem (maybe there's a data-specific bug).
- **Testing new features on specific tenants:** You might want to roll out features gradually. One approach: have a flag or config that enables a feature per tenant (feature toggles). This way you could test with one or two tenants before global enable. This adds complexity but is a strategy some SaaS use to mitigate risk.
- **Regular audits:** Periodically audit that data is properly isolated. For instance, run queries to ensure no data rows have wrong tenant IDs (in shared schema) or that each schema only contains its expected data. Perhaps use a script to verify that the number of users in tenant table equals what master thinks, etc.
- **Performance tuning:** As data grows, optimize queries and archiving. For example, if some tenants accumulate millions of rows, consider archiving old data or partitioning tables (MySQL partitioning by tenant or by date).
- **Security audits:** Penetration testing or code review focusing on multi-tenancy (make sure no endpoint forgets to filter by tenant, etc.). Use OWASP top 10 as guideline.

By adhering to these maintenance practices, you ensure the multi-tenant system remains reliable, secure, and efficient as it scales to more customers and adapts to new requirements.

---

**Conclusion:**  
Building a multi-tenant application requires careful planning at every layer: database design, application logic, and infrastructure. In this guide, we covered how to isolate tenant data at the database level (using separate schemas in MySQL and Hibernate’s multi-tenancy support) ([How to integrate Hibernates Multitenant feature with Spring Data JPA in a Spring Boot application](https://spring.io/blog/2022/07/31/how-to-integrate-hibernates-multitenant-feature-with-spring-data-jpa-in-a-spring-boot-application#:~:text=1,part%20of%20the%20primary%20key)), implement authentication and authorization such that each user is confined to their tenant ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=In%20a%20multi,filter%20the%20data%20requests%20accordingly)) ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=On%20login%2C%20the%20SPA%20receives,happens%20in%20the%20authentication%20provider)), and structure the frontend to handle tenant-specific state. We also discussed critical cross-cutting concerns like security (never trusting the client for tenant separation) ([Multi-Tenant Single-Page Apps: Dos and Don'ts](https://marmelab.com/blog/2022/12/14/multitenant-spa.html#:~:text=Why%20It%27s%20A%20Bad%20Idea)), performance optimization (through caching and indexing) ([sql server - Indexing TenantID in Multi Tenant DB - Stack Overflow](https://stackoverflow.com/questions/8144933/indexing-tenantid-in-multi-tenant-db#:~:text=2)), and strategies for scaling and updating the system over time ([Schema-based multi-tenancy with Spring Data, Hibernate and Flyway](https://sultanov.dev/blog/schema-based-multi-tenancy-with-spring-data/#:~:text=The%20tables%20in%20the%20shared,to%20perform%20different%20migrations%20in)).
