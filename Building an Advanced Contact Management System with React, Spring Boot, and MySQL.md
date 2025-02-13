# **Building an Advanced Contact Management System with React, Spring Boot, and MySQL**

This guide provides a comprehensive, **step-by-step manual** for advanced developers to build a full-stack Contact Management System using **React.js (frontend)**, **Spring Boot (backend)**, and **MySQL (database)**. It covers everything from architecture design and environment setup to advanced features, testing, deployment, security, and future improvements. Throughout, we’ll include **code snippets**, conceptual **diagrams (described in text)**, **best practices**, and **hands-on exercises** to solidify understanding.

Each section below delves into a critical aspect of the project, ensuring you gain **deep insights** and can implement industry-standard solutions. Let’s get started!

## 1. **Introduction & System Overview**

### **1.1 High-Level Architecture and Technologies**

Our Contact Management System follows a **three-tier architecture**:

- **Frontend (Presentation Tier)**: A React.js application running in the user’s browser, responsible for the UI and client-side logic. It communicates with the backend via HTTP requests (REST API).
- **Backend (Application/Business Tier)**: A Spring Boot application running on a server (or cloud instance). It provides RESTful endpoints, implements business logic, and interacts with the database. The backend is structured in layers (controllers, services, repositories) for maintainability.
- **Database (Data Tier)**: A MySQL relational database that stores persistent data (e.g., user accounts, contact details). This tier runs on a DB server or cloud database service, separate from the application server.

In a deployed scenario, each tier can reside on a different machine or service. For example, React code runs on the user’s device, the Spring Boot app on an application server, and MySQL on a database server. This distribution into separate tiers is a hallmark of modern web apps. Within the Spring Boot app itself, we also enforce **layered architecture** (controller → service → repository) without mixing concerns, which aligns with best practices.

**Technologies Used:**

- **React.js** (with JavaScript or TypeScript): Builds a dynamic single-page application (SPA) frontend. We’ll use modern React features (Hooks, Context API) and possibly UI libraries (Tailwind CSS or Material-UI).
- **Spring Boot (Java)**: Simplifies building the backend with embedded server, REST API support, and integrations. We’ll leverage Spring Web, Spring Data JPA for database access, and Spring Security for authentication.
- **MySQL**: Stores data in tables with relationships. We’ll design a normalized schema for contacts, users, and roles.
- **JWT (JSON Web Tokens)**: Used for stateless authentication. Spring Security will issue and validate JWTs for API security.
- **Tools & Others**: Node.js and npm (for React development), Maven/Gradle (for Spring Boot builds), JUnit/Mockito (testing backend), Jest/React Testing Library (testing frontend), Docker (containerization), and AWS services (EC2, S3, RDS) for deployment.

### **1.2 Key Features of the System**

Our Contact Management System (CMS) will support the following **key features**:

- **User Management**: Users can register an account, log in, and log out. Passwords are stored securely (hashed) in the database.
- **Role-Based Access**: We’ll have at least two roles – e.g., **Admin** (full access) and **Standard User** (limited access). Admins might manage all contacts or other users, while standard users manage their own contacts. The system enforces role-based authorization in both the frontend and backend.
- **Contact CRUD Operations**: Users can **Create**, **Read**, **Update**, and **Delete** contacts. Each contact contains information like name, phone number, email, address, etc. Contacts are associated with the user who created them (each user has their own contact list).
- **Search & Filter**: Users can search contacts by name and filter the list (e.g., by city or company). This helps manage large contact lists efficiently.
- **Pagination & Sorting**: Contact lists support pagination (viewing in pages) and sorting (e.g., sort by name or date added) for usability and performance.
- **Security Features**: JWT-based authentication secures the API endpoints. We’ll implement input validation to prevent SQL injection, enable CORS properly for the frontend, and use HTTPS in production. We’ll also address common security concerns (CSRF, XSS, etc.).
- **Advanced Integrations**: (Optional) The system can integrate with external services. For instance, sending a welcome email when a new contact is added, importing contacts from a CSV file, or using third-party APIs for additional contact info. These integrations demonstrate extendability.
- **Responsive UI & UX**: The React app will be user-friendly and responsive. We plan to use a modern CSS framework (Tailwind CSS for utility-first styling or Material-UI for pre-built components) to ensure the interface is clean and responsive on various devices.

### **1.3 User Roles and Use Cases**

**User Roles:**

- **Admin User**: Can manage **all** users and contacts. Admins can create/edit/delete any contact in the system, manage user accounts (e.g., assign roles), and possibly see system metrics. They effectively have full access.
- **Standard User**: Can manage **their own** contacts. They can perform CRUD operations on contacts they’ve created, but cannot access other users’ contacts or administer users. Each contact is “owned” by a user.
- _(Optionally, we could define more roles, such as a “Manager” who can see contacts of users in their team. But for this guide, we’ll focus on Admin vs. User for simplicity.)_

**Typical Use Cases:**

- A user registers for an account and logs in.
- The user creates a new contact (fills a form with contact info).
- The user views a list of all their contacts, perhaps with pagination if the list is long.
- The user searches by name to find a specific contact, or filters by some criterion (e.g., show only contacts in a certain city).
- The user edits a contact’s details or deletes a contact.
- An admin logs in to view all contacts in the system or manage user roles.
- The system automatically logs out users after a period of inactivity (token expiration), requiring them to log in again (for security).
- (Advanced) The user imports contacts from an external source (like uploading a CSV file) to add multiple contacts at once.
- (Advanced) The system sends an email notification to the user when certain events happen, e.g., a summary of newly added contacts or a reminder of contacts’ birthdays.

With the overview in mind, we’re ready to set up our development environment and scaffold the project.

## 2. **Project Setup**

Setting up the project involves configuring the development environment and creating the base React and Spring Boot applications. We’ll install necessary tools, initialize projects, and ensure the backend and frontend can run and communicate in a dev setting.

### **2.1 Prerequisites and Environment Configuration**

Before coding, make sure you have the following installed and configured:

- **Java Development Kit (JDK)**: Install JDK 17 (LTS) or later. Spring Boot requires Java (we’ll use Java 17 for compatibility). Verify by running `java -version` in your terminal.
- **Apache Maven or Gradle**: We can use Maven (commonly used with Spring Boot) to manage dependencies. Many IDEs come with Maven bundled. Ensure `mvn -v` works or install Maven. Alternatively, use Gradle if preferred.
- **Node.js and npm**: Install Node.js (which includes npm, the Node Package Manager). We’ll use Node to create and run the React app. Confirm with `node -v` and `npm -v`.
- **MySQL Server**: Install MySQL Community Server and set up a database user. For development, you can use a local MySQL instance. Remember the username, password, and create a blank database (e.g., named `contact_db`) for the project.
- **IDE/Editors**: It’s recommended to use IntelliJ IDEA or Eclipse for the Spring Boot project (for Java support and Spring integration) and VS Code or WebStorm for React (for JavaScript/TypeScript and JSX). This isn’t a strict requirement, but a good IDE will increase productivity.
- **Postman or cURL**: Useful for testing API calls independently of the frontend during development.

**System Setup Steps:**

1. **Install Java & Maven**: Download Java 17 from AdoptOpenJDK or Oracle. Install Maven (if not using an IDE that handles it). Add them to your system PATH.
2. **Install Node.js**: Download from the official Node.js website. We’ll need a relatively recent version (Node 18+ is fine). NPM comes with Node.
3. **Install MySQL**: Install MySQL and start the server. Use MySQL Workbench or command line to create a new database schema (e.g., `CREATE DATABASE contact_db;`). Also create a user for the app (or use root in dev) and note the credentials.
4. **Choose IDEs**: Set up IntelliJ (with the Spring Assistant plugin, if available) for backend. Set up VS Code with React plugins (like ESLint, Prettier for code style) for frontend.

### **2.2 Initializing the Spring Boot Project**

We will create the Spring Boot project using **Spring Initializr**, which is a convenient way to bootstrap a new Spring Boot app with needed dependencies.

**Using Spring Initializr Web** (start.spring.io):

- Open the Spring Initializr site. Enter project metadata:
  - _Group_: com.example (or your organization domain)
  - _Artifact_: contact-manager
  - _Name_: Contact Manager
  - _Package Name_: com.example.contactmanager
  - _Packaging_: Jar
  - _Java_: 17
- Add the following **dependencies**:
  - **Spring Web**: for building RESTful APIs.
  - **Spring Data JPA**: for database access via JPA/Hibernate.
  - **MySQL Driver**: MySQL JDBC driver for database connectivity.
  - **Spring Security**: for authentication and security (needed for JWT later).
  - (Optional) Lombok: to reduce boilerplate code for models (getters/setters).
  - (Optional) Spring Boot DevTools: for hot reloading in dev.
- Generate and download the project, then unzip it.

Alternatively, **using Spring Initializr with Maven (command line)**:

```bash
mvn archetype:generate -DgroupId=com.example -DartifactId=contact-manager \
  -Ddependencies=web,data-jpa,mysql,security -DpackageName=com.example.contactmanager
```

Or using **Spring Boot CLI** if installed:

```bash
spring init -d=web,data-jpa,mysql,security -g com.example -a contact-manager contact-manager
```

Once created, open the project in your Java IDE. The structure typically includes:

- `src/main/java/com/example/contactmanager` – your Java source (will contain controllers, services, etc.).
- `src/main/resources` – for configuration (application.properties) and static resources.
- `pom.xml` – Maven configuration listing all dependencies.

**Configure the database** in `src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/contact_db?useSSL=false&allowPublicKeyRetrieval=true
spring.datasource.username=<your-mysql-user>
spring.datasource.password=<your-mysql-password>
spring.jpa.hibernate.ddl-auto=update   # auto-create/update tables based on entities
spring.jpa.show-sql=true              # show SQL queries in console (useful in dev)
```

Make sure to replace username/password with your MySQL credentials. The `ddl-auto=update` will auto-synchronize the database with our JPA entities on startup (convenient in dev; in production, you might use `validate` or manage schema via migrations).

**Run the Spring Boot app** to verify setup:
Use your IDE’s run configuration or run `mvn spring-boot:run`. You should see the app starting (Tomcat embedded server listening on port 8080 by default). No functionality yet, but if it starts without errors, the environment is fine.

**Troubleshooting**: If you get MySQL connection errors, check the URL, credentials, and that MySQL server is running. You may need to allow remote connections or adjust the port if not default.

### **2.3 Initializing the React.js Project**

We’ll use `create-react-app` (CRA) to bootstrap the React application. CRA sets up a modern React development environment with minimal configuration.

Open a terminal and run:

```bash
npx create-react-app contact-manager-ui
```

This uses NPX to ensure you have the latest CRA. It will create a folder `contact-manager-ui` with a React project inside. Once done:

```bash
cd contact-manager-ui
npm start
```

This should start the development server (on port 3000 by default) and open a browser at `http://localhost:3000/` with a default React welcome page. If you see the React logo spinning, the setup is successful.

**Project structure (frontend)**:

- `src/index.js` – entry point, renders the `<App />` component inside a React `<BrowserRouter>` (for routing) if using React Router.
- `src/App.js` – main App component. We will configure our routes and global context here later.
- `src/components/` – we will create this directory to hold reusable components.
- `src/pages/` – we will create pages (views) like Login, ContactList, etc.
- `package.json` – contains project metadata and dependencies.

We’ll use additional libraries:

- **Axios** for making HTTP requests from React to our API.
- **React Router** for navigation between pages (like Login page and Contacts page).
- **Tailwind CSS** or **Material-UI** for UI styling:
  - If Tailwind: we’ll need to install and configure it.
  - If Material-UI (MUI): we can install the component library directly and use ready-made components.

For now, install Axios and React Router:

```bash
npm install axios react-router-dom
```

This adds Axios (for REST calls) and React Router (for client-side routing). Confirm they appear in `package.json` dependencies.

If using Material-UI:

```bash
npm install @mui/material @emotion/react @emotion/styled
```

If using Tailwind CSS:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Then configure `tailwind.config.js` and add Tailwind directives in `src/index.css`. (Tailwind setup details can be done as needed; using Material-UI might be quicker for this guide).

At this point, we have:

- A Spring Boot app ready on `localhost:8080` (though no endpoints yet).
- A React dev server on `localhost:3000` showing a placeholder app.

### **2.4 Connecting Frontend and Backend in Development**

During development, our React app will run on a separate dev server (port 3000) from the Spring Boot API (port 8080). To allow the React frontend to call the API without CORS issues, we should enable CORS in the backend for our dev origin. We’ll cover CORS setup in the Security section, but for quick testing you might temporarily allow all origins.

In `application.properties`, add:

```properties
# Enable all origins for dev (not recommended for prod)
spring.mvc.cors.allowed-origins=http://localhost:3000
spring.mvc.cors.allowed-methods=*
```

This uses Spring’s global CORS config to allow the React dev server to make requests. Alternatively, we’ll use `@CrossOrigin` annotations on our controllers later.

Another dev tip: If you want the React dev server to proxy API calls to avoid CORS config, add a proxy in `package.json`:

```json
"proxy": "http://localhost:8080"
```

This way, when React makes a request to `/api/...`, the dev server will forward it to `localhost:8080/api/...`. This is convenient in development; however, we’ll still set up CORS properly for production when the frontend is served separately.

**Verify connectivity (once we have at least one endpoint)**: You can create a dummy endpoint now to test. For example, add a simple controller in Spring Boot:

```java
@RestController
public class HelloController {
    @GetMapping("/api/hello")
    public String hello() {
        return "Hello from Spring Boot";
    }
}
```

Restart the Spring Boot app. From React, modify `App.js` to call this on load:

```js
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  useEffect(() => {
    axios
      .get("/api/hello")
      .then((res) => setMessage(res.data))
      .catch((err) => console.error(err));
  }, []);
  return <div>{message}</div>;
}

export default App;
```

Because of the proxy or CORS setup, this call should succeed and display “Hello from Spring Boot” on the React page (at `http://localhost:3000`). If you see the message, the basic connectivity between React and Spring Boot is confirmed!

_Exercise:_ To further cement your setup, try changing the greeting message in the controller or returning a JSON (e.g., `return Map.of("greeting", "Hello")` and adjust React accordingly). This helps ensure you know how to handle JSON responses with Axios.

Now that our environment is ready and the skeleton applications are running, we can move on to designing the database schema for managing contacts and users.

## 3. **Database Design**

Designing the database is a crucial step. We will create an **Entity-Relationship (ER) diagram** (conceptually) and define the schema for our MySQL database. The goal is to have a clear, normalized design that avoids redundancy and ensures data integrity.

### **3.1 Entities and Relationships (ER Diagram)**

For a Contact Management System, the primary entities are:

- **User**: Represents a registered user of the system. Fields: `id`, `username`, `password`, `email` (if separate from username), etc. We store hashed passwords for security. Each User can have one or more contacts.
- **Contact**: Represents a contact person. Fields: `id`, `name`, `email`, `phone`, `address`, `company`, etc., as needed. Each Contact is associated with one **owner** (the User who added it).
- **Role** (optional for role-based auth): Fields: `id`, `name` (e.g., “ROLE_ADMIN”, “ROLE_USER”). A User can have multiple roles (many-to-many relationship).
- _(Optional)_ **UserRole**: Join table for the many-to-many relationship between Users and Roles. If using JPA with @ManyToMany, this can be implicit. But we might define an explicit entity for clarity.
- _(Optional)_ **Address**: We could normalize addresses into a separate table if contacts can have multiple addresses. But to keep things simpler, we might store a single address in the Contact table (or a JSON). If we need multiple addresses per contact, an Address entity with a foreign key to Contact would be used.
- _(Optional)_ **PhoneNumber**: Similarly, if we want multiple phone numbers per contact, we’d have a PhoneNumber entity with type (mobile, home, etc.) and number, linked to Contact. Again, to manage scope, we might treat phone as a single field in Contact for now, but it’s worth noting this approach in a more complex design.

**Relationships:**

- **User – Contact**: One-to-many. A single User **owns** many Contacts. In the database, the `contacts` table will have a foreign key `user_id` linking to `users`. We enforce that each contact must have an owner user (non-null foreign key).
- **User – Role**: Many-to-many. A user can have multiple roles, and each role can be assigned to multiple users. This is implemented via a join table `user_roles` (with columns `user_id` and `role_id`). Alternatively, JPA can manage it with a `@ManyToMany` annotation and an underlying join table.
- **Contact – (Address/Phone)**: If we went with separate tables for addresses or phone numbers, those would be one-to-many with Contact (one Contact, many PhoneNumbers, etc.). But if we keep them as fields in Contact, then no separate relationship.

**ER Diagram Description:**

- **Users** (User) – primary key `user_id`. Attributes: username, password, email, etc.
- **Roles** (Role) – primary key `role_id`. Attribute: name.
- **User_Roles** – composite primary key (user_id, role_id). Both are foreign keys referencing Users and Roles. This table assigns roles to users.
- **Contacts** (Contact) – primary key `contact_id`. Attributes: name, email, phone, address, etc., and a foreign key `user_id` referencing Users (owner).
- (If addresses separate) **Addresses** – primary key `address_id`, foreign key `contact_id` referencing Contacts.
- (If phones separate) **PhoneNumbers** – primary key `phone_id`, foreign key `contact_id` referencing Contacts.

For our scope, we’ll assume one address and phone per contact for simplicity, stored in the Contact record.

In a normalized design, we ensure minimal redundancy:

- Data like user details are stored once in Users.
- Contact details in Contacts, referencing the user rather than duplicating user info.
- Roles in a separate table to avoid repeating role names for each user (normalization).

**Normalization:** We aim for at least **Third Normal Form (3NF)**. This means no repeating groups, each field is atomic, and every non-key attribute depends only on the primary key of that table ([Database normalization description - Microsoft 365 Apps | Microsoft Learn](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description#:~:text=Normalization%20is%20the%20process%20of,eliminating%20redundancy%20and%20inconsistent%20dependency)) ([Database normalization description - Microsoft 365 Apps | Microsoft Learn](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description#:~:text=,data%20with%20a%20primary%20key)). For example:

- We don’t store multiple phone numbers in one field (that would violate atomicity/1NF). Instead, if needed, have a separate Phone table or multiple columns like phone1, phone2 (the latter is not fully normalized, so separate table is cleaner).
- Contacts table shouldn’t contain user-specific data beyond the foreign key; user info like username should not be duplicated in Contacts (that would violate 3NF, as contact’s user name depends on user, not on contact itself).
- We avoid redundant columns. For instance, we don’t store role names in the Users table directly; that’s what the Roles table is for.

By normalizing, we reduce anomalies (insertion, update, deletion issues) and keep the data consistent ([Database normalization description - Microsoft 365 Apps | Microsoft Learn](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description#:~:text=Normalization%20is%20the%20process%20of,eliminating%20redundancy%20and%20inconsistent%20dependency)). If a user’s email changes, it’s updated in one place (Users table) and automatically reflected for all their contacts through the relationship.

### **3.2 MySQL Schema and Table Definitions**

Now let’s define the tables using SQL DDL:

```sql
-- 1. Users table
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE  -- indicates if the user is active
);

-- 2. Roles table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE  -- e.g., 'ROLE_USER', 'ROLE_ADMIN'
);

-- 3. User_Roles join table
CREATE TABLE user_roles (
    user_id BIGINT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY(user_id, role_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- 4. Contacts table
CREATE TABLE contacts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    company VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

A few notes on the schema:

- We use **BIGINT** for `id` in users and contacts to allow a large number of records. Role IDs are INT since number of roles is small.
- `user_roles` has a composite PK, ensuring no duplicate user-role assignments.
- We set foreign keys with `ON DELETE CASCADE` so that if a user is deleted, their contacts and user_role entries are also removed automatically, maintaining referential integrity.
- The `contacts` table has `created_at` and `updated_at` timestamps for auditing changes.
- We included a `notes` field to demonstrate a TEXT field (for any notes about the contact).
- The `enabled` field in users can be used to soft-disable an account without deleting it (useful for admin control).

This schema is **normalized** and avoids duplication:

- We don’t store the user’s name in the contacts table, just the user’s foreign key.
- We don’t store role names in the user table, only in the roles table and link them.
- Contact information is in one table, with each field atomic (one piece of info per column).

### **3.3 JPA Entity Modeling**

In Spring Boot, we will model these tables as JPA entities. This way, Spring Data JPA can auto-generate the tables (because of `hibernate.ddl-auto=update`) and we can manipulate data via repositories.

For instance, the `User` entity (simplified):

```java
@Entity
@Table(name="users")
public class User {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @Column(nullable=false, unique=true)
    private String username;
    @Column(nullable=false)
    private String password;
    @Column(nullable=false, unique=true)
    private String email;
    private boolean enabled = true;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
       name = "user_roles",
       joinColumns = @JoinColumn(name = "user_id"),
       inverseJoinColumns = @JoinColumn(name = "role_id"))
    private Set<Role> roles = new HashSet<>();

    // getters and setters ...
}
```

`Role` entity:

```java
@Entity
@Table(name="roles")
public class Role {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer id;
    @Column(nullable=false, unique=true)
    private String name; // e.g., "ROLE_ADMIN"

    @ManyToMany(mappedBy = "roles")
    private Set<User> users = new HashSet<>();
    // getters, setters ...
}
```

`Contact` entity:

```java
@Entity
@Table(name="contacts")
public class Contact {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @Column(nullable=false)
    private String name;
    private String email;
    private String phone;
    private String address;
    private String company;
    private String notes;
    @Column(name="created_at")
    private Timestamp createdAt;
    @Column(name="updated_at")
    private Timestamp updatedAt;

    @ManyToOne
    @JoinColumn(name="user_id", nullable=false)
    private User owner;  // the User who owns this contact

    // getters and setters...
}
```

A few things to note:

- We map the relationships: a Contact `@ManyToOne` with a `User owner`. In the DB, this is the `user_id` foreign key.
- In `User`, we used `@ManyToMany` for roles with a join table of `user_roles`. We eagerly fetch roles because we often need to know user roles for auth.
- The cascade settings can be tuned (e.g., we might cascade operations on contacts when a user is deleted).
- We might add convenience methods in `User` to add/remove Role or Contact to keep both sides in sync.

This JPA model correlates to our MySQL tables. By using these entities and Spring Data repositories, we avoid writing SQL for common operations (the framework will generate safe SQL for us).

### **3.4 Database Normalization and Design Rationale**

Our design adheres to normalization principles:

- **First Normal Form (1NF)**: Each table has atomic columns (e.g., we don’t have multiple phone numbers in one column; if we needed multiple, we’d use a separate table rather than multiple columns like phone1, phone2).
- **Second Normal Form (2NF)**: Every non-key column in a table depends on the whole primary key. In Contacts, the primary key is a single column `id`, and all other fields describe that contact (they don’t partially depend on something else).
- **Third Normal Form (3NF)**: No transitive dependencies (non-key depending on another non-key). For example, if we had stored `user_name` in contacts, that would be a transitive dependency (contact -> user_id -> user_name). We avoided that by not duplicating the user’s data in the contacts table. Thus, contacts depend only on contact ID and any direct foreign keys.

Normalized design makes the database **more flexible and consistent** ([Database normalization description - Microsoft 365 Apps | Microsoft Learn](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description#:~:text=Normalization%20is%20the%20process%20of,eliminating%20redundancy%20and%20inconsistent%20dependency)). For example, if a user is renamed, we update the Users table once; all their contacts automatically reflect the new name when joined, with no stale data. It also prevents anomalies — e.g., we cannot have a contact row referencing a user that doesn’t exist (thanks to foreign key constraints).

**However, normalization vs performance**: Sometimes highly normalized designs are split into many tables which can require a lot of joins, possibly impacting performance for read-heavy operations. In our case, the design is straightforward: typically just joining contacts to users or users to roles. These are not expensive joins if indexed. For example, having an index on `contacts.user_id` helps when retrieving all contacts for a user. We should indeed add indexes:

```sql
CREATE INDEX idx_contacts_user ON contacts(user_id);
CREATE INDEX idx_users_username ON users(username);
```

Index on username helps quick lookup for login, and index on user_id in contacts speeds up queries for a user’s contacts.

If we anticipate extremely large contact lists, we might consider denormalization or caching for certain read operations, but that’s an optimization topic we’ll touch on later.

For now, the design is robust and **satisfies the requirements without redundancy**. Let’s proceed to implement this on the backend.

_Exercise:_ Draw out the ER diagram on paper or using a tool like MySQL Workbench. Identify the primary keys and foreign keys. As a challenge, consider how you would modify the design to allow contacts to be **shared** between users (e.g., a contact visible to multiple users). What changes in the schema would that require? (Hint: possibly a join table between users and contacts, making the relationship many-to-many instead of one-to-many.)

## 4. **Backend Development (Spring Boot)**

With the database schema in mind, we can start building the backend. This section covers creating the model (entities), repositories for data access, service layer for business logic, controllers for API endpoints, and configuring security (JWT authentication). We will also handle exceptions and logging to ensure maintainability and traceability.

Our approach will be to implement features incrementally:

- Define JPA entities for User, Contact, Role as per our design.
- Create repository interfaces for CRUD operations.
- Implement service classes that use the repositories (applying any business rules).
- Develop REST controllers that expose endpoints (mapping HTTP requests to service calls).
- Secure the APIs using Spring Security with JWT, applying authentication and authorization rules.
- Handle exceptions globally and add logging.

By following the layered architecture, each part of the code has a single responsibility and can be tested in isolation.

### **4.1 Creating JPA Entities and Repositories**

We partially defined the entities in the previous section. Now, create these classes under `src/main/java/com/example/contactmanager/model` (you can organize packages as `model` or `entity`). Ensure each class is annotated with `@Entity` and has an `@Table(name="...")` if the table name isn’t the same as the class name (JPA defaults would match class to table if names are identical, but explicit is clear).

**User Entity (with Roles and Contacts relationship):**

```java
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable=false, unique=true, length=50)
    private String username;
    @Column(nullable=false)
    private String password;  // hashed password
    @Column(nullable=false, unique=true, length=100)
    private String email;
    @Column(nullable=false)
    private boolean enabled = true;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name="user_id"),
        inverseJoinColumns = @JoinColumn(name="role_id")
    )
    private Set<Role> roles = new HashSet<>();

    @OneToMany(mappedBy="owner", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Contact> contacts = new ArrayList<>();

    // Constructors
    public User() {}
    public User(String username, String password, String email) {
       this.username = username;
       this.password = password;
       this.email = email;
    }
    // Getters and setters (omitted for brevity) ...
}
```

Here:

- `@ManyToMany` for roles: When we load a User, we often need to know roles for security, so we fetch eagerly. Alternatively, lazy fetch is default, but then you need to handle it carefully outside of transactions.
- `@OneToMany` for contacts: A user’s contacts. We cascade all so that if a User is deleted, all their contacts are removed (because of orphanRemoval = true, which aligns with ON DELETE CASCADE at DB level).
- We might add helper methods like `addContact(Contact c)` that sets `c.setOwner(this)` and adds to `contacts` list, etc., to manage both sides of relationships.

**Role Entity:**

```java
@Entity
@Table(name = "roles")
public class Role {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column(nullable=false, unique=true, length=20)
    private String name;

    @ManyToMany(mappedBy = "roles")
    private Set<User> users = new HashSet<>();

    public Role() {}
    public Role(String name) { this.name = name; }
    // getters, setters ...
}
```

(This is straightforward, with the inverse side of the user-role relationship.)

**Contact Entity:**

```java
@Entity
@Table(name = "contacts")
public class Contact {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable=false, length=100)
    private String name;
    @Column(length=100)
    private String email;
    @Column(length=20)
    private String phone;
    @Column(length=255)
    private String address;
    @Column(length=100)
    private String company;
    @Column(columnDefinition="TEXT")
    private String notes;
    @Column(name="created_at", nullable=false, updatable=false)
    private Timestamp createdAt;
    @Column(name="updated_at")
    private Timestamp updatedAt;

    @ManyToOne
    @JoinColumn(name="user_id", nullable=false)
    private User owner;

    // Constructors
    public Contact() {}
    public Contact(String name, String email, String phone) {
       this.name = name; this.email = email; this.phone = phone;
    }
    // Getters and setters...

    @PrePersist
    protected void onCreate() {
        createdAt = new Timestamp(System.currentTimeMillis());
        updatedAt = createdAt;
    }
    @PreUpdate
    protected void onUpdate() {
        updatedAt = new Timestamp(System.currentTimeMillis());
    }
}
```

We use `@PrePersist` and `@PreUpdate` lifecycle hooks to set timestamps automatically when a contact is created/updated. The `owner` field is a reference to the User; it will map to the `user_id` column.

With entities ready, we create repository interfaces in, say, `com.example.contactmanager.repository`:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
}
```

We’ll use `findByUsername` to authenticate users. JPA will implement it automatically based on the method name.

```java
@Repository
public interface RoleRepository extends JpaRepository<Role, Integer> {
    Optional<Role> findByName(String name);
}
```

This helps to fetch roles, e.g., find the Role entity for “ROLE_USER” or “ROLE_ADMIN” when assigning roles.

```java
@Repository
public interface ContactRepository extends JpaRepository<Contact, Long> {
    // Find contacts by owner
    Page<Contact> findByOwnerUsername(String username, Pageable pageable);
    // Or findByOwnerId(Long userId, Pageable pageable);
    // We can also add search:
    Page<Contact> findByOwnerUsernameAndNameContainingIgnoreCase(String username, String name, Pageable pageable);
}
```

The above shows how to get a user’s contacts (with pagination) and optionally filter by name (case-insensitive). Spring Data JPA will translate these method names into SQL with appropriate JOIN on users table, etc., automatically. This prevents SQL injection by design because it uses parameter binding internally (as opposed to manually concatenating strings).

We now have data access layer ready: these repository interfaces give us CRUD methods out of the box (via JpaRepository) and the custom finders defined.

### **4.2 Implementing Service Layer and Business Logic**

The **service layer** contains business logic and coordinates between controllers and repositories. For example, a `ContactService` might enforce that a user can only create a certain number of contacts if we had such a rule, or transform data if needed. It also makes unit testing easier: we can test services without the web layer.

Create services in `com.example.contactmanager.service`. We’ll implement the following services:

- **UserService**: For managing users (registration, finding by username, etc.), and implementing **UserDetailsService** (Spring Security’s interface) so that we can load user info during login.
- **ContactService**: For managing contacts (CRUD operations, search, etc.). This service ensures that the current user is associated correctly and might filter data by user.
- **AuthService**: (Optional) Could handle authentication-related tasks, like verifying passwords and generating JWT tokens, or this could be part of UserService.

Let’s implement `UserService` first, focusing on security integration:

```java
@Service
public class UserService implements UserDetailsService {
    @Autowired
    private UserRepository userRepo;
    @Autowired
    private RoleRepository roleRepo;
    @Autowired
    private PasswordEncoder passwordEncoder;  // we will configure a BCrypt PasswordEncoder bean later

    // For Spring Security to load user by username (for authentication)
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepo.findByUsername(username)
                      .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));
        // Spring Security UserDetails requires roles as GrantedAuthority
        List<GrantedAuthority> authorities = user.getRoles().stream()
                .map(role -> new SimpleGrantedAuthority(role.getName()))
                .toList();
        return new org.springframework.security.core.userdetails.User(
                user.getUsername(), user.getPassword(), user.isEnabled(),
                true, true, true, authorities);
    }

    public User registerUser(String username, String email, String rawPassword) throws Exception {
        if(userRepo.findByUsername(username).isPresent()) {
            throw new Exception("Username already taken");
        }
        if(userRepo.findByEmail(email).isPresent()) {
            throw new Exception("Email already registered");
        }
        // Create new user with ROLE_USER by default
        User user = new User(username, passwordEncoder.encode(rawPassword), email);
        Role userRole = roleRepo.findByName("ROLE_USER")
                         .orElseGet(() -> roleRepo.save(new Role("ROLE_USER")));
        user.getRoles().add(userRole);
        userRepo.save(user);
        return user;
    }

    // Additional methods like finding user by id, assigning roles, etc.
}
```

Points to note:

- `UserService` implements `UserDetailsService.loadUserByUsername` which Spring Security will call during authentication. We fetch the user, convert roles to `GrantedAuthority` list, and return a Spring Security `User` object (which implements `UserDetails`). This ties our user storage to Spring Security’s login process.
- `registerUser` is an example method to create a new user. It checks for duplicates by username/email, hashes the password (using `PasswordEncoder`), assigns a default role, and saves.
- We ensure a role “ROLE_USER” exists in DB (create if not found). Alternatively, roles could be pre-populated on startup.
- We would similarly have a method to create an admin user or upgrade a user to admin by adding “ROLE_ADMIN” to their roles.

**ContactService**:

```java
@Service
public class ContactService {
    @Autowired
    private ContactRepository contactRepo;
    @Autowired
    private UserRepository userRepo;

    public Contact addContact(String username, Contact contact) throws Exception {
        // Fetch the user (owner) by username
        User owner = userRepo.findByUsername(username)
                      .orElseThrow(() -> new Exception("User not found"));
        // Set the owner of the contact
        contact.setOwner(owner);
        // Save contact
        return contactRepo.save(contact);
    }

    public Page<Contact> getContacts(String username, int page, int size, String sortBy, String nameFilter) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy).ascending());
        if (nameFilter != null && !nameFilter.isEmpty()) {
            return contactRepo.findByOwnerUsernameAndNameContainingIgnoreCase(username, nameFilter, pageable);
        } else {
            return contactRepo.findByOwnerUsername(username, pageable);
        }
    }

    public Contact updateContact(String username, Long contactId, Contact updatedData) throws Exception {
        Contact contact = contactRepo.findById(contactId)
                         .orElseThrow(() -> new Exception("Contact not found"));
        // Ensure the contact belongs to the user trying to update (security check)
        if (!contact.getOwner().getUsername().equals(username)) {
            throw new Exception("Unauthorized to edit this contact");
        }
        // Update allowed fields
        contact.setName(updatedData.getName());
        contact.setEmail(updatedData.getEmail());
        contact.setPhone(updatedData.getPhone());
        contact.setAddress(updatedData.getAddress());
        contact.setCompany(updatedData.getCompany());
        contact.setNotes(updatedData.getNotes());
        // Save changes
        return contactRepo.save(contact);
    }

    public void deleteContact(String username, Long contactId) throws Exception {
        Contact contact = contactRepo.findById(contactId)
                         .orElseThrow(() -> new Exception("Contact not found"));
        if (!contact.getOwner().getUsername().equals(username)) {
            throw new Exception("Unauthorized to delete this contact");
        }
        contactRepo.delete(contact);
    }
}
```

Here:

- `addContact`: takes the username of the current user and a Contact object (from controller), finds the User, attaches it as owner, and saves. By doing `contact.setOwner(owner)`, we maintain consistency (so JPA knows the relation).
- `getContacts`: returns a page of contacts for a user, optionally filtering by name. We use Spring Data’s automatically implemented queries for simplicity.
- `updateContact` and `deleteContact`: first, retrieve the contact, verify that the username matches the owner (to prevent one user from tampering with another’s contact – an **authorization check** at the service level). If not authorized, throw exception. If authorized, update or delete.
- We throw generic `Exception` here for brevity. In a real scenario, we might create custom exceptions like `ContactNotFoundException` or `UnauthorizedActionException`. We will handle them in a global exception handler to send appropriate HTTP responses.

At this point, our service layer enforces business rules:

- Only owners can modify their contacts.
- Only unique usernames/emails allowed for users.
- Default roles assignment on registration.

We have not written an `AuthService` here; instead, we integrate auth in UserService and Security config. However, we will need a way to generate JWT tokens upon successful login, which we’ll handle in the controller or a dedicated utility.

### **4.3 Building REST Controllers**

Controllers map HTTP requests (from React or any client) to service layer calls. We’ll create controllers under `com.example.contactmanager.controller`. Key controllers:

- **AuthController**: for authentication endpoints like login (and registration, if open signup is allowed).
- **ContactController**: for CRUD operations on contacts (these will be protected by auth).
- **UserController**: possibly for user-related queries (e.g., get current user profile, list users if admin, etc.). This could be minimal for our needs.

Let’s implement them:

**AuthController** – to handle login (and register for this example):

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    @Autowired
    private AuthenticationManager authenticationManager;  // from Spring Security
    @Autowired
    private UserService userService;
    @Autowired
    private JwtUtil jwtUtil;  // a utility class we will create for JWT operations

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequest request) {
        try {
            // Perform authentication
            Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword()));
            // If we reach here, authentication was successful
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
            String token = jwtUtil.generateToken(userDetails.getUsername());
            return ResponseEntity.ok(new AuthResponse(token));
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
        }
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest request) {
        try {
            userService.registerUser(request.getUsername(), request.getEmail(), request.getPassword());
            return ResponseEntity.ok("User registered successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}
```

We need to create simple DTOs for the request/response:

```java
// AuthRequest.java
public class AuthRequest {
    private String username;
    private String password;
    // getters and setters
}
// AuthResponse.java
public class AuthResponse {
    private String token;
    public AuthResponse(String token) { this.token = token; }
    public String getToken() { return token; }
}
// RegisterRequest.java
public class RegisterRequest {
    private String username;
    private String email;
    private String password;
    // getters and setters
}
```

These will be used to parse JSON from client and to send responses.

AuthController logic:

- For login: We use `AuthenticationManager` to authenticate the credentials. If successful, we generate a JWT token using a `JwtUtil` (we’ll implement this shortly). If fails, return 401 Unauthorized.
- For register: We call our `userService.registerUser` and handle exceptions like duplicate user gracefully, returning a 400 Bad Request with the message.

**ContactController** – to manage contacts:

```java
@RestController
@RequestMapping("/api/contacts")
public class ContactController {
    @Autowired
    private ContactService contactService;

    // Get contacts for current user (possibly filtered and paginated)
    @GetMapping
    public Page<Contact> listContacts(
            @RequestParam(defaultValue="0") int page,
            @RequestParam(defaultValue="10") int size,
            @RequestParam(defaultValue="name") String sortBy,
            @RequestParam(required=false) String search,
            Authentication authentication) {
        String username = authentication.getName();
        // Use service to fetch contacts for this user
        return contactService.getContacts(username, page, size, sortBy, search);
    }

    // Create a new contact
    @PostMapping
    public ResponseEntity<Contact> createContact(@RequestBody Contact contact, Authentication authentication) {
        String username = authentication.getName();
        try {
            Contact created = contactService.addContact(username, contact);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch(Exception e) {
            // In real scenario, differentiate exceptions
            return ResponseEntity.badRequest().build();
        }
    }

    // Update an existing contact
    @PutMapping("/{id}")
    public ResponseEntity<Contact> updateContact(
            @PathVariable Long id, @RequestBody Contact contact, Authentication authentication) {
        String username = authentication.getName();
        try {
            Contact updated = contactService.updateContact(username, id, contact);
            return ResponseEntity.ok(updated);
        } catch(Exception e) {
            if(e.getMessage().contains("not found")) {
                return ResponseEntity.notFound().build();
            } else if(e.getMessage().contains("Unauthorized")) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
            } else {
                return ResponseEntity.badRequest().build();
            }
        }
    }

    // Delete a contact
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteContact(@PathVariable Long id, Authentication authentication) {
        String username = authentication.getName();
        try {
            contactService.deleteContact(username, id);
            return ResponseEntity.noContent().build();
        } catch(Exception e) {
            if(e.getMessage().contains("not found")) {
                return ResponseEntity.notFound().build();
            } else if(e.getMessage().contains("Unauthorized")) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
            } else {
                return ResponseEntity.badRequest().build();
            }
        }
    }
}
```

Key points:

- We inject `Authentication` (from Spring Security) into controller methods. Spring Security, when a request is authenticated, will supply an `Authentication` object (e.g., UsernamePasswordAuthenticationToken) which contains the current user’s details. `authentication.getName()` typically returns the username.
- We rely on the fact that these endpoints will be secured, so `authentication` is non-null and represents an authenticated user (the Security configuration will ensure that).
- Each endpoint delegates to `ContactService`. The service already checks authorization, but we do an extra simple check by using the username context (if the token was somehow compromised and used, the service still double-checks).
- We handle exceptions: return appropriate HTTP status (404 if contact not found, 403 if trying to access someone else’s contact, 400 for other errors).
- The listContacts returns a `Page<Contact>` directly, which Spring will serialize to JSON (including content, total pages, etc.). Alternatively, we could map to a DTO to avoid sending the `owner` object (which might contain user data) to the client. For now, perhaps we rely on JSON serialization properties (which might cause recursion if we’re not careful with bidirectional link between Contact and User). We might need to use `@JsonIgnore` on `User.contacts` or `Contact.owner` to avoid infinite recursion in JSON.
  - For simplicity, we can mark `Contact.owner` with `@JsonIgnore` when returning to the client, or create a ContactDTO that doesn’t include owner. In an advanced scenario, one would do that to avoid leaking user info. Let’s assume we add `@JsonIgnoreProperties({"contacts"})` on User or `@JsonIgnore` on Contact.owner for safe JSON serialization.

**UserController** – Not strictly required unless we want an endpoint for user info. But a common one is “get current user profile”:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserRepository userRepo;

    @GetMapping("/me")
    public ResponseEntity<User> getCurrentUser(Authentication authentication) {
        String username = authentication.getName();
        return userRepo.findByUsername(username)
            .map(user -> ResponseEntity.ok(user))
            .orElse(ResponseEntity.notFound().build());
    }

    // Perhaps an admin-only endpoint to list all users:
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public List<User> listUsers() {
        return userRepo.findAll();
    }
}
```

Here we introduce `@PreAuthorize("hasRole('ADMIN')")` on the listUsers endpoint to ensure only admins can call it. We will enable method security in our security config to make that work.

Now we have functioning controllers. The next critical piece is **security configuration**: we must configure Spring Security to use JWT authentication, so that when the React app includes a token in requests, the backend will validate it and set the `Authentication` accordingly.

### **4.4 Securing APIs with JWT (Spring Security Configuration)**

We will implement JWT-based authentication. This requires:

- A `JwtUtil` class to generate and validate tokens (using a secret key).
- A filter that intercepts requests, checks for the `Authorization: Bearer <token>` header, and if present, validates the token and sets the authentication in the security context.
- Configuring the security to use our custom filter and authentication logic, and to **disable session management** (stateless API).
- Configuring which endpoints are public (e.g., `/api/auth/**`) and which require authentication (everything else by default).
- A `PasswordEncoder` bean to hash passwords (BCrypt).
- Possibly disable CSRF since we’re not using cookies for auth (in JWT case typically we disable CSRF tokens as they’re not necessary for token auth).

**JwtUtil** (simplified):

```java
@Component
public class JwtUtil {
    private final String SECRET_KEY = "ReplaceThisWithASecretKeyForJWT";  // in production, use a stronger, externalized secret
    private final long EXPIRATION_MS = 3600000; // 1 hour expiration

    public String generateToken(String username) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + EXPIRATION_MS);
        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(SignatureAlgorithm.HS256, SECRET_KEY.getBytes())
                .compact();
    }

    public String extractUsername(String token) {
        return Jwts.parser()
                .setSigningKey(SECRET_KEY.getBytes())
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(SECRET_KEY.getBytes()).parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
}
```

This uses the io.jsonwebtoken library (jjwt). Ensure you added `jjwt` to Maven dependencies. For example, in `pom.xml`:

```xml
<dependency>
  <groupId>io.jsonwebtoken</groupId>
  <artifactId>jjwt</artifactId>
  <version>0.9.1</version>
</dependency>
```

(JWT libraries handle the heavy lifting of signing and parsing tokens.)

**Security Configuration**:
In Spring Boot 2, we’d extend `WebSecurityConfigurerAdapter`; in Spring Boot 3 (Spring Security 6), that is deprecated in favor of a SecurityFilterChain bean. We’ll outline one approach using the older style for clarity, but note you can achieve the same with the new style.

```java
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)  // for @PreAuthorize in controllers
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private UserService userService;
    @Autowired
    private JwtUtil jwtUtil;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        // Configure authentication provider to use our userService and password encoder
        auth.userDetailsService(userService).passwordEncoder(passwordEncoder());
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // We create an instance of our custom filter (defined below)
        JwtRequestFilter jwtRequestFilter = new JwtRequestFilter(userService, jwtUtil);

        http.csrf().disable()  // disable CSRF for stateless REST
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // no HTTP session
            .and()
            .authorizeRequests()
            .antMatchers("/api/auth/**").permitAll()  // auth endpoints are public
            .antMatchers(HttpMethod.POST, "/api/users").permitAll() // if we allow creating new user (registration)
            .anyRequest().authenticated()  // everything else requires login
            .and()
            .exceptionHandling().authenticationEntryPoint((request, response, ex) -> {
                // handle auth error (like no token or invalid token)
                response.sendError(HttpServletResponse.SC_UNAUTHORIZED, ex.getMessage());
            })
            .and()
            .addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);
    }
}
```

This configuration does the following:

- Disables CSRF (since our API is stateless and we’re using JWT, not cookies, we don’t need CSRF tokens).
- Sets session creation to stateless (Spring Security won’t create an HTTP session, which aligns with JWT usage).
- Defines URL access rules: anything under `/api/auth/` is allowed without authentication (for login/register), and any other request must have a valid token.
- We add our `JwtRequestFilter` to be executed **before** the built-in `UsernamePasswordAuthenticationFilter`. The UsernamePasswordAuth filter is used in form login (which we’re not using), but adding our filter ensures that every request goes through it early.
- We expose `AuthenticationManager` as a bean so our AuthController can `@Autowired` it (or get via constructor injection) to perform authentication.

The `JwtRequestFilter` is a custom filter:

```java
public class JwtRequestFilter extends OncePerRequestFilter {
    private final UserService userService;
    private final JwtUtil jwtUtil;

    public JwtRequestFilter(UserService userService, JwtUtil jwtUtil) {
        this.userService = userService;
        this.jwtUtil = jwtUtil;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        // Get Authorization header
        final String authHeader = request.getHeader("Authorization");

        String username = null;
        String jwtToken = null;

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            jwtToken = authHeader.substring(7);  // extract token without "Bearer "
            try {
                username = jwtUtil.extractUsername(jwtToken);
            } catch (Exception e) {
                // Invalid token or unable to parse
                logger.error("JWT parse error: {}", e.getMessage());
            }
        }

        // If we got a username and SecurityContext is not yet authenticated for this request:
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            // Load user details
            UserDetails userDetails = userService.loadUserByUsername(username);
            // Validate token
            if (jwtUtil.validateToken(jwtToken) && userDetails != null) {
                // Create authentication token
                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                // Set authentication in context
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // Continue filter chain
        filterChain.doFilter(request, response);
    }
}
```

This filter:

- Checks the `Authorization` header for a Bearer token.
- If present, uses `JwtUtil` to extract the username (subject) from the token.
- If a username is obtained and the user is not already authenticated in this request’s context, it loads the user (via `UserService`). Then it validates the token (checking signature and expiration).
- If valid, it creates an `Authentication` object (with no credentials, only authorities since user is already verified by token) and sets it in the `SecurityContext`.
- This means for the rest of the request processing, Spring Security sees the user as authenticated.
- If token is missing or invalid, it just proceeds without setting auth (which will eventually lead to 401 if an endpoint required auth).

With this in place, any request to protected endpoints must include a header `Authorization: Bearer <JWT>` obtained from the login step. If not, the Security context remains unauthenticated and our `exceptionHandling().authenticationEntryPoint` will kick in, sending 401.

We should also ensure our `AuthenticationManager` knows how to authenticate credentials at login time:

- In `configure(AuthenticationManagerBuilder)`, we tied it to `UserService` and `passwordEncoder` (BCrypt). So when `authenticationManager.authenticate` is called in AuthController, it uses `UserService.loadUserByUsername` to get user and then matches the raw password with the hashed password via the passwordEncoder.

Don’t forget to mark `@Bean` for `PasswordEncoder` and `AuthenticationManager` as shown, so Spring can inject them where needed.

Now, our backend is secure:

- `/api/auth/login` (POST) is public – we authenticate credentials and return a JWT.
- `/api/auth/register` (POST) is public – allows creating a new account.
- All other `/api/**` endpoints are protected by JWT. If a request has a valid JWT, our filter sets the user in context, then controllers can get `Authentication` injected or use `SecurityContextHolder` to know who the user is (as we did with `authentication.getName()`).
- The ContactController uses the `Authentication` object provided to get current username. Spring Security automatically provides this for authenticated requests (the filter we wrote ensures `authentication.getName()` will be the username from token).

**Testing the Security Flow:**

- First, call `/api/auth/register` with JSON `{"username":"alice", "email":"alice@example.com", "password":"secret"}`. Should get 200 OK if success.
- Then call `/api/auth/login` with `{"username":"alice","password":"secret"}`. If credentials match, you get a response containing `token: <JWT>`.
- Now call a protected endpoint, e.g., `GET /api/contacts` with header `Authorization: Bearer <JWT-from-login>`. If everything is correct, it should call ContactController and (if Alice has contacts) return them, or empty list if none. If token was missing or invalid, you’d get 401.
- Try calling `/api/contacts` without a token: should get 401 Unauthorized (due to our AuthenticationEntryPoint sending that).
- Try calling an admin-only endpoint like `GET /api/users` with a normal user’s token: should get 403 Forbidden (because user lacks ADMIN role). If you assign an admin role to a user (e.g., via DB or code), their token (once they login again to get a token with updated roles) would allow access.

This completes our backend security setup with JWT.

### **4.5 Exception Handling and Logging**

Throughout the backend, we’ve thrown exceptions for error cases. We should handle these in a unified way so that the API returns consistent error responses (instead of possibly a generic 500).

**Global Exception Handler**: We can use `@ControllerAdvice` for a global exception handler. For example:

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<String> handleNotFound(NoSuchElementException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Resource not found");
    }
    @ExceptionHandler(UsernameNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UsernameNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User not found");
    }
    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<String> handleBadCredentials(BadCredentialsException ex) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid username or password");
    }
    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleOtherExceptions(Exception ex) {
        // Log the exception
        logger.error("Error: ", ex);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                             .body("An unexpected error occurred: " + ex.getMessage());
    }
}
```

This is a simple example. It catches certain exceptions (like when our service throws NoSuchElement or we propagate UsernameNotFound) and returns an appropriate status and message. The last handler catches any exception not caught by earlier ones, logs it, and returns 500 with a message.

We already set an auth entry point in security config for authentication failures, so we might not need to handle those via ControllerAdvice.

**Logging**: Use a logging framework (Spring Boot uses Logback by default with SLF4J API). In each class (especially services and controllers), it’s good practice to have a logger:

```java
private static final Logger logger = LoggerFactory.getLogger(ContactService.class);
```

Use `logger.info()`, `logger.debug()`, `logger.error()` as appropriate:

- Info for high-level events (user created, contact deleted, etc.).
- Debug for detailed internal state (only in development).
- Error for exceptions (as in global handler above, or inside catch blocks if recovering).

For example, in ContactService `deleteContact`, instead of throwing generic exception, you might:

```java
if (!contact.getOwner().getUsername().equals(username)) {
    logger.warn("User {} attempted to delete contact {} not owned by them", username, contactId);
    throw new AccessDeniedException("Unauthorized");
}
```

And have a handler for AccessDeniedException returning 403.

Likewise, in AuthController, if login fails, you log a warning:

```java
logger.warn("Failed login attempt for username: {}", request.getUsername());
```

But careful not to log sensitive info like the password (never log raw passwords).

It’s also useful to log at startup which profiles are active, or log configuration settings (like what URL the DB is connected to, though credentials should not be logged).

**Testing the Backend (so far)**: We will later write proper tests, but at this stage you can use Postman or cURL to test each endpoint:

- Register, login, try CRUD on contacts (with token).
- Try unauthorized actions (e.g., using one user’s token to delete another user’s contact by manipulating URL, should get 403).
- Ensure token expiry is handled (you can shorten the expiration in JwtUtil for testing, and after expiry time, the endpoint should return 401 because `validateToken` fails).
- Also test that invalid token (garbage string or tampered token) returns 401.

If all looks good, then our backend core functionality is working securely.

Next, we’ll switch to the frontend to build the user interface and integrate these APIs.

_Exercise:_ As a practice, extend the backend with a feature to upload a profile picture for a contact. This would involve an endpoint to upload an image (binary), saving the file (maybe on the server or cloud storage), and storing the URL in the Contact’s data. This touches on handling multipart/form-data in Spring (via @RequestPart or @RequestParam MultipartFile) and perhaps using an external storage (like AWS S3). Sketch out how you would add an Image field to Contact and the corresponding controller method to upload/download images.

## 5. **Frontend Development (React.js)**

With the backend ready, we can focus on the React frontend. The frontend will provide a user-friendly interface for our system’s features, interacting with the backend via the REST APIs we created. We’ll set up the project structure, create components for login and contact management, integrate the API calls using Axios, and manage state (including authentication state and contact data).

### **5.1 Structuring the React Project**

A well-structured React project improves maintainability. We will organize our code by features:

- **components/** – reusable UI components (e.g., form input components, navbar, contact item card).
- **pages/** – page-level components corresponding to routes (e.g., LoginPage, ContactsPage, ContactDetailsPage).
- **services/** – for API calls (we can define an Axios instance and functions to call backend endpoints).
- **context/** – define a React Context for authentication (to store current user and token globally).
- **App.js** – define routes and layout here.
- **AppProvider (optional)** – a context provider that wraps the app (for auth context or any other context).

Let's outline the structure:

```
src/
  components/
    ContactCard.js
    ContactForm.js
    Navbar.js
    ... (other small reusable components)
  pages/
    LoginPage.js
    RegisterPage.js
    ContactsPage.js
    ContactEditPage.js
  services/
    api.js        (Axios instance configuration)
    authService.js (functions like login, register)
    contactService.js (functions to get contacts, create, update, delete)
  context/
    AuthContext.js
  App.js
  index.js
```

We use **React Router** to handle navigation:

- “/login” → LoginPage
- “/register” → RegisterPage
- “/contacts” → ContactsPage (listing contacts)
- “/contacts/new” → ContactEditPage (for adding a new contact)
- “/contacts/:id” → ContactEditPage (for editing an existing contact, perhaps same component used for create/edit)
- and maybe a default route to redirect to /contacts if logged in or /login if not.

### **5.2 Setting Up React Router and Context**

First, install React Router (we did with `react-router-dom`). In `App.js`, configure routes:

```jsx
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ContactsPage from "./pages/ContactsPage";
import ContactEditPage from "./pages/ContactEditPage";
import Navbar from "./components/Navbar";
import { AuthProvider, useAuth } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes: require auth */}
          <Route path="/contacts" element={<PrivateRoute />}>
            <Route index element={<ContactsPage />} />
            <Route path="new" element={<ContactEditPage />} />
            <Route path=":id" element={<ContactEditPage />} />
          </Route>

          <Route path="/" element={<Navigate to="/contacts" />} />
          <Route path="*" element={<p>404 Not Found</p>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

// PrivateRoute component ensures the user is authenticated
function PrivateRoute() {
  const { user } = useAuth();
  // if user is present in context, render child routes, otherwise redirect to login
  return user ? (
    <Routes>
      <Route path="*" element={<Outlet />} />
    </Routes>
  ) : (
    <Navigate to="/login" replace />
  );
}

export default App;
```

In the above:

- We wrap the app in `<AuthProvider>` which will provide auth context to all components.
- `<Navbar />` is always visible (maybe showing links and a logout button if logged in).
- We define routes. Note that for protected routes, one pattern (React Router v6) is to nest them in a layout route that does the auth check. Here, `<PrivateRoute />` is conceptually a component that either renders an `<Outlet />` (which represents the child routes /contacts or /contacts/new etc.) if authenticated, or `<Navigate>` to /login if not. We used a particular pattern with nested Routes inside PrivateRoute. Another approach is to define `<Route path="/contacts/*" element={<PrivateRoute>}>` with children. For clarity, we have this separate PrivateRoute component reading from context.
- If the user is not logged in, any attempt to go to /contacts or sub-routes will redirect to /login.

We should implement `AuthContext` next to supply `user` and `token` and methods like `login`, `logout`:

```jsx
// AuthContext.js
import { createContext, useContext, useState, useEffect } from "react";

// Define what auth state includes
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // On mount, check local storage for token
  useEffect(() => {
    const savedUser = JSON.parse(localStorage.getItem("user"));
    const savedToken = localStorage.getItem("token");
    if (savedToken && savedUser) {
      setUser(savedUser);
      setToken(savedToken);
    }
  }, []);

  // Function to handle login (using authService)
  const login = async (username, password) => {
    // call API via service
    const response = await authService.login(username, password);
    if (response.token) {
      setToken(response.token);
      // decode token if needed to get user info, or get from separate call
      const userData = { username }; // we can store username and perhaps roles if encoded
      setUser(userData);
      // Save to local storage to persist login state
      localStorage.setItem("token", response.token);
      localStorage.setItem("user", JSON.stringify(userData));
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  const register = async (username, email, password) => {
    return authService.register(username, email, password);
  };

  // Provide context value
  return (
    <AuthContext.Provider value={{ user, token, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook for easy context usage
export function useAuth() {
  return useContext(AuthContext);
}
```

A few considerations:

- We store the token in localStorage so that if the user refreshes the page, they remain logged in (we retrieve it on `useEffect` in AuthProvider). This is a common approach. Storing JWT in localStorage is generally fine but has a small risk if XSS attacks occur (an attacker script could potentially read localStorage). Since we will implement content security and avoid XSS, it’s acceptable. Another approach is storing in HttpOnly cookies, which would require CSRF protection; our scenario keeps it simpler.
- The user info we store is minimal (just username). We might also store roles if we encoded them in JWT. We did not explicitly add roles in JWT payload but we could. Alternatively, after login, we could call `/api/users/me` to get user details (including roles) and store that. For simplicity, we assume user’s username is enough to identify and check roles on frontend if needed (we could decode JWT to get roles, but decoding on frontend can be done with a JWT library or manually because roles might be in token claims).
- The `authService.login` returns a token (and possibly user info). We’ll implement that next in **services/api**.

### **5.3 Creating Reusable Components**

Before diving into services and pages, let’s outline some key reusable components:

- **Navbar**: A top navigation bar that shows links and login status. If user is logged in, show a “Logout” button and maybe user’s name. If not, show links to Login or Register.
- **ContactCard**: A component to display a contact’s info in a card or list item format (name, email, phone, etc., possibly with edit/delete buttons).
- **ContactForm**: A form for creating/editing a contact (inputs for name, email, etc., and Save/Cancel buttons).

**Navbar.js**:

```jsx
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <h1>Contact Manager</h1>
      <ul>
        {user ? (
          <>
            <li>Hello, {user.username}!</li>
            <li>
              <button onClick={logout}>Logout</button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/register">Register</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}
export default Navbar;
```

(We’ll style this with CSS or a framework; className “navbar” is arbitrary here.)

**ContactCard.js**:

```jsx
function ContactCard({ contact, onEdit, onDelete }) {
  return (
    <div className="contact-card border p-4 flex justify-between items-center">
      <div>
        <h3 className="text-xl font-bold">{contact.name}</h3>
        <p>Email: {contact.email || "N/A"}</p>
        <p>Phone: {contact.phone || "N/A"}</p>
        {contact.address && <p>Address: {contact.address}</p>}
        {contact.company && <p>Company: {contact.company}</p>}
      </div>
      <div>
        <button onClick={onEdit} className="btn btn-edit">
          Edit
        </button>
        <button onClick={onDelete} className="btn btn-delete">
          Delete
        </button>
      </div>
    </div>
  );
}
export default ContactCard;
```

This component expects a `contact` object and callbacks for edit and delete. We can style it with Tailwind classes (like I used `border p-4 flex` etc. above assuming Tailwind; or we would use equivalent in CSS or MUI components).

**ContactForm.js**:

```jsx
import { useState } from "react";

function ContactForm({ initialData = {}, onSave, onCancel }) {
  const [formData, setFormData] = useState({
    name: initialData.name || "",
    email: initialData.email || "",
    phone: initialData.phone || "",
    address: initialData.address || "",
    company: initialData.company || "",
    notes: initialData.notes || "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="contact-form space-y-4">
      <div>
        <label>Name:</label>
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Email:</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Phone:</label>
        <input name="phone" value={formData.phone} onChange={handleChange} />
      </div>
      <div>
        <label>Address:</label>
        <input
          name="address"
          value={formData.address}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Company:</label>
        <input
          name="company"
          value={formData.company}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Notes:</label>
        <textarea name="notes" value={formData.notes} onChange={handleChange} />
      </div>
      <div>
        <button type="submit" className="btn btn-primary">
          Save
        </button>
        <button type="button" onClick={onCancel} className="btn btn-secondary">
          Cancel
        </button>
      </div>
    </form>
  );
}
export default ContactForm;
```

This form is controlled by React state. We initialize with `initialData` (so it can be used for editing existing contact pre-filled). On submit, calls `onSave` with the form data. `onCancel` triggers when user cancels (e.g., to navigate away).

We could enhance it with form validation (e.g., require email format if provided, etc.), but basic required for name is shown.

### **5.4 Axios Integration for API Calls**

To keep API calls organized, we create a centralized Axios instance with base URL and interceptors:

**api.js**:

```jsx
import axios from "axios";
import { getToken } from "./authService"; // a function to get current token, or we can use context directly.

const api = axios.create({
  baseURL: "http://localhost:8080/api", // base URL for our API
});

// Attach token to every request if available
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

This sets up Axios to prefix all URLs with our backend’s base (`/api`). If backend and frontend in production are served from same domain, baseURL could be relative (just "/api"), but in development `localhost:8080` vs `:3000` differ, so we provide full host. (We could also rely on the proxy setting in package.json as earlier, but using baseURL explicit is fine.)

We also use an interceptor: before each request, we get the token (we need to define `getToken` in authService that perhaps reads from localStorage or from a context; since context may not be directly imported into this file easily, a quick solution is to export a function from AuthContext to get current token. Or simpler, read from localStorage here as well since we keep token in localStorage).

Alternatively, inside AuthContext, when user logs in and we set token state, we could also set axios default header:

```js
axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
```

But an interceptor is a cleaner approach and ensures up-to-date token usage.

Now define some API calls:

**authService.js**:

```jsx
import api from "./api";

export async function login(username, password) {
  try {
    const response = await api.post("/auth/login", { username, password });
    return response.data; // expected to be { token: "..." }
  } catch (error) {
    console.error("Login error", error);
    return { error: error.response?.data || "Login failed" };
  }
}

export async function register(username, email, password) {
  try {
    const response = await api.post("/auth/register", {
      username,
      email,
      password,
    });
    return { success: true, message: response.data };
  } catch (error) {
    return {
      success: false,
      message: error.response?.data || "Registration failed",
    };
  }
}

export function getToken() {
  return localStorage.getItem("token");
}
```

We export `getToken` to be used by axios interceptor.

**contactService.js**:

```jsx
import api from "./api";

export async function fetchContacts(search = "", page = 0, size = 10) {
  const params = { page, size };
  if (search) params.search = search;
  const res = await api.get("/contacts", { params });
  return res.data; // will be a Page object: { content: [...contacts], totalElements, totalPages, etc. }
}

export async function createContact(contact) {
  const res = await api.post("/contacts", contact);
  return res.data;
}

export async function updateContact(id, contact) {
  const res = await api.put(`/contacts/${id}`, contact);
  return res.data;
}

export async function deleteContact(id) {
  await api.delete(`/contacts/${id}`);
  // no need to return anything on successful deletion
}
```

We leverage our interceptor so that these calls automatically include auth header. The baseURL in dev is `http://localhost:8080/api`, which matches our backend. If the backend is running on same machine, this should work (CORS must be allowed for localhost:3000 which we did).

### **5.5 Building the Pages (Login, Register, Contacts List, Contact Edit)**

Now, implement the page components to tie everything together with UI and service calls:

**LoginPage.js**:

```jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const auth = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const success = await auth.login(form.username, form.password);
    if (success) {
      navigate("/contacts");
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Username</label>
          <input
            name="username"
            value={form.username}
            onChange={handleChange}
            className="w-full border"
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            className="w-full border"
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button type="submit" className="btn btn-primary w-full">
          Login
        </button>
      </form>
      <p className="mt-4">
        No account?{" "}
        <Link to="/register" className="text-blue-500">
          Register here
        </Link>
      </p>
    </div>
  );
}
export default LoginPage;
```

It uses `useAuth().login` method to attempt login. If success, navigates to contacts, else shows error. This demonstrates using context in a component.

**RegisterPage.js** (similar to login, but calls `auth.register` and perhaps auto-login or redirect to login after success):

```jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function RegisterPage() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const auth = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    const result = await auth.register(
      form.username,
      form.email,
      form.password
    );
    if (result.success) {
      // registration success - redirect to login
      setMessage("Registration successful! You can now log in.");
      navigate("/login");
    } else {
      setMessage(result.message || "Registration failed.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl mb-4">Register</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Username</label>
          <input
            name="username"
            value={form.username}
            onChange={handleChange}
            required
            className="w-full border"
          />
        </div>
        <div>
          <label>Email</label>
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
            className="w-full border"
          />
        </div>
        <div>
          <label>Password</label>
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
            className="w-full border"
          />
        </div>
        {message && <p className="text-red-500">{message}</p>}
        <button type="submit" className="btn btn-primary w-full">
          Register
        </button>
      </form>
      <p className="mt-4">
        Already have an account?{" "}
        <Link to="/login" className="text-blue-500">
          Login
        </Link>
      </p>
    </div>
  );
}
export default RegisterPage;
```

We show message on success or failure.

**ContactsPage.js**:

```jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchContacts, deleteContact } from "../services/contactService";
import ContactCard from "../components/ContactCard";

function ContactsPage() {
  const [contacts, setContacts] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadContacts = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchContacts(search);
      setContacts(data.content || data); // depending if Page or array
    } catch (err) {
      setError("Failed to load contacts.");
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadContacts();
  }, []); // load initially

  const handleSearch = (e) => {
    e.preventDefault();
    loadContacts();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this contact?")) {
      try {
        await deleteContact(id);
        // Filter out deleted contact from state to update UI
        setContacts((prev) => prev.filter((c) => c.id !== id));
      } catch (err) {
        alert("Failed to delete contact");
      }
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl">My Contacts</h2>
      {/* Search form */}
      <form onSubmit={handleSearch} className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search contacts"
          className="border p-1"
        />
        <button type="submit" className="btn btn-secondary ml-2">
          Search
        </button>
        <button
          type="button"
          onClick={() => {
            setSearch("");
            loadContacts();
          }}
          className="ml-2"
        >
          Clear
        </button>
      </form>

      {loading ? <p>Loading...</p> : null}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && !contacts.length && <p>No contacts found.</p>}

      {/* Contacts list */}
      <div className="space-y-2">
        {contacts.map((contact) => (
          <ContactCard
            key={contact.id}
            contact={contact}
            onEdit={() => (window.location.href = `/contacts/${contact.id}`)}
            onDelete={() => handleDelete(contact.id)}
          />
        ))}
      </div>

      <Link to="/contacts/new" className="btn btn-primary mt-4 inline-block">
        Add New Contact
      </Link>
    </div>
  );
}
export default ContactsPage;
```

This page:

- Loads contacts on mount using the service. If the backend returned a Page object (with content), we handle that. (Alternatively, we could adjust fetchContacts to return data.content).
- Allows searching: we have an input bound to search state, and on form submit, we call loadContacts (which uses search state to fetch).
- On clear, resets search and loads all.
- Delete: asks for confirmation, calls API then updates state by removing that contact (optimistic update).
- Edit: here for simplicity, we redirect to the edit page by setting `window.location.href`. We could use `useNavigate` for a SPA navigation. Let’s do that properly:

Better approach:

```jsx
import { useNavigate } from 'react-router-dom';
...
const navigate = useNavigate();
...
onEdit={() => navigate(`/contacts/${contact.id}`)}
```

Use that instead of window.location.

We need also to handle pagination if lots of contacts. We could use the Page info returned. Perhaps not implementing fully here, but advanced user likely can. We could display `data.totalPages` and show next/prev buttons that modify page param. For brevity, omitted.

**ContactEditPage.js**:

```jsx
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ContactForm from '../components/ContactForm';
import { createContact, updateContact, fetchContacts } from '../services/contactService';

function ContactEditPage() {
  const { id } = useParams();  // id will be "new" or an actual id, depending on route setup. We separated /contacts/new vs /contacts/:id
  const navigate = useNavigate();
  const [contact, setContact] = useState(null);
  const [loading, setLoading] = useState(true);

  const isNew = id === undefined; // because we used separate route for new, in this design if path is 'new', we wouldn't get here due to separate route definition
  // Actually, our routes are:
  // <Route path="/contacts" element={<PrivateRoute />}>
  //    <Route index ... />
  //    <Route path="new" ... />
  //    <Route path=":id" ... />
  // If we navigate to '/contacts/new', this component will be rendered with useParams().id = 'new'? Actually since we separated path "new" and path ":id", React Router will match "new" vs a param. So in /contacts/new, it matches the "new" route not the :id route. Thus, in this ContactEditPage component, id likely only exists for editing case.
  // So isNew can be determined by checking id param existence or maybe we use separate components for create vs edit. But we can unify here by using same component for both if carefully handling it.
```

Given our route setup, maybe it's easier to create two separate page components: one for creating new and one for editing existing. But we can combine by logic:

- If the route is /contacts/new, we rendered ContactEditPage (assuming path new goes to same component). But we gave separate route elements for new and :id pointing to the same component in our example which is slightly tricky. Perhaps we should have used one route with a param that could be "new" or ID. But better to just do:
  - `<Route path="new" element={<ContactEditPage isNew={true} />}`
  - `<Route path=":id" element={<ContactEditPage isNew={false} />}`

So we can pass a prop via route. But react-router v6 doesn’t allow passing props directly in route element (besides wrapping in an element inline). We can do: `<Route path="new" element={<ContactEditPage key="new" />} />` and inside component check location or something.

Alternatively, simply create two components NewContactPage and EditContactPage to avoid confusion. But let's try to handle in one:

We'll assume if there's a param id, then it's editing, if not, creating:
But since in route we have separate definitions, maybe use same component for both in router:
Instead do:

```jsx
<Route path="/contacts/:id" element={<ContactEditPage />} />
```

And in ContactEditPage, treat id = "new" as meaning new contact.
That is hacky but possible:

- If id === 'new', show empty form and on save call createContact.
- If id is numeric (like "5"), fetch that contact and on save call updateContact.

Yes, let's do that:

```jsx
const { id } = useParams();
const isNew = id === "new";
```

(This means we handle /contacts/new by calling it /contacts/new in URL but router should interpret 'new' as :id param with value 'new' if not matching a static route. Actually, if we put `:id` route, it will catch "new" as id. So we wouldn't define path "new" separately at all; we just always use :id route. Then within component see if id === 'new'. This approach conflates an id param with a keyword 'new'. Not best practice, but doable.)
A cleaner approach is to have two routes:

- path "new" uses a different key to not conflict with id:
  We could name param contactId:

```jsx
<Route path="/contacts/new" element={<ContactEditPage mode="new" />} />
<Route path="/contacts/:contactId" element={<ContactEditPage mode="edit" />} />
```

But to keep simpler, we do the id/new trick.

So adjust route:

```jsx
<Route path=":id" element={<ContactEditPage />} />
```

(And remove the separate new route to rely on this single route. Then in UI, we navigate to /contacts/new when adding new.)

Given complexity, for clarity we might separate:

- NewContactPage
- EditContactPage

But let's show how to combine, as an advanced trick:

**ContactEditPage.js** (assuming route param id can be 'new' or an actual id):

```jsx
function ContactEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(true);

  const isNew = id === "new";

  useEffect(() => {
    if (!isNew) {
      // Fetch existing contact
      fetchContacts().then((data) => {
        // We could have an API endpoint to fetch single contact by id,
        // better than fetching all. Suppose we had /contacts/{id}.
        // Actually, implement a new service function getContact(id) to fetch one contact.
      });
      // For now, assume we have getContact service:
      getContact(id)
        .then((contact) => {
          setInitialData(contact);
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [id]);

  const handleSave = async (contactData) => {
    if (isNew) {
      try {
        await createContact(contactData);
        navigate("/contacts");
      } catch (err) {
        alert("Failed to create contact");
      }
    } else {
      try {
        await updateContact(id, contactData);
        navigate("/contacts");
      } catch (err) {
        alert("Failed to update contact");
      }
    }
  };

  const handleCancel = () => {
    navigate("/contacts");
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h2 className="text-2xl mb-4">
        {isNew ? "New Contact" : "Edit Contact"}
      </h2>
      <ContactForm
        initialData={initialData || {}}
        onSave={handleSave}
        onCancel={handleCancel}
      />
    </div>
  );
}
```

We used a hypothetical `getContact(id)` in service. We should implement that:

In **contactService.js**:

```jsx
export async function getContact(id) {
  const res = await api.get(`/contacts/${id}`);
  return res.data;
}
```

We didn't implement such endpoint in backend explicitly. We have GET /contacts for all, but not GET one. We can add:
In ContactController:

```java
@GetMapping("/{id}")
public ResponseEntity<Contact> getContact(@PathVariable Long id, Authentication auth) {
    Optional<Contact> contactOpt = contactRepo.findById(id);
    if(contactOpt.isEmpty()) {
        return ResponseEntity.notFound().build();
    }
    Contact contact = contactOpt.get();
    // ensure current user is owner or admin
    if (!contact.getOwner().getUsername().equals(auth.getName()) &&
        auth.getAuthorities().stream().noneMatch(a -> a.getAuthority().equals("ROLE_ADMIN"))) {
        return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
    }
    return ResponseEntity.ok(contact);
}
```

This allows fetching one contact if authorized.

Given advanced dev, they can add that. For our focus, assume it's done.

Now the ContactEditPage should work for both new and edit.

**Testing the Frontend**:

- Run `npm start` to start the React app.
- Ensure the backend (`mvn spring-boot:run`) is running too.
- Try registering a user via UI, then log in.
- Once logged in, should redirect to ContactsPage (which should list "No contacts found." initially).
- Try adding a new contact (click "Add New Contact", fill the form, hit Save). It should go back to list and show the new contact.
- Try editing the contact (click Edit, change something, Save). It should go back to list with updated info.
- Try the search bar: type part of name or something and press Search. It should filter the list. (This depends on backend search working; our contactRepo method findByOwnerUsernameAndNameContainingIgnoreCase should handle it).
- Try deleting a contact: click Delete, confirm, and see it removed from list.
- Also test the logout button in Navbar: it should clear context and localStorage and likely the PrivateRoute will redirect to login (since user becomes null).
- After logout, try manually accessing /contacts in browser: it should redirect to /login.

**Styling**:
We used Tailwind utility classes in some places (like border, p-4, etc.). If we actually use Tailwind, ensure it's set up (Tailwind CSS file imported in index.js or App.css). If not using Tailwind, one could use plain CSS or use Material-UI components for styling (which would change the code a bit). For example, using MUI:

```jsx
import { TextField, Button } from "@mui/material";
```

and use `<TextField label="Name" variant="outlined" fullWidth value={...} />` etc., instead of raw input.

Given advanced dev, they can adjust styling easily, so we focus on structure and logic.

### **5.6 Ensuring Frontend Security**

We must ensure that certain frontend routes or actions are only shown to authorized roles:

- For example, if we had admin features (like viewing all users), we would check the user’s roles from context and conditionally render admin links or pages.
- In our context, we did not explicitly store roles. We could decode JWT to get roles claim. If JWT has `authorities` or similar claims, decode it:
  - e.g., using atob (if not JWT-specific decode) or a library like jwt-decode.
  - For instance: `import jwtDecode from 'jwt-decode';` and then `const decoded = jwtDecode(token);` might give an object with `roles` or `authorities`.
  - Then set `user = { username, roles: decoded.roles }` in AuthContext login.
- We could add that to AuthProvider. Then, for admin route:
  - In PrivateRoute or separate AdminRoute, check `user.roles.includes('ROLE_ADMIN')`.
  - Or use the `hasRole` in UI like: `{ user.roles.includes('ROLE_ADMIN') && <Link to="/admin">Admin Panel</Link> }`.

**Protecting against XSS**:
React by default escapes content, so as long as we do not use `dangerouslySetInnerHTML` with untrusted data, we are safe from injecting scripts. E.g., if contact.name contains `<script>...`, React will render it as text, not execute. This is a major security benefit of React’s rendering engine.

**Preventing sensitive data exposure**:
We should ensure we’re not showing e.g. user’s token or password anywhere. We do not. The token stays in memory/localStorage. Also, our backend doesn’t send password anyway. We might show user’s username or email which is fine.

**Handling token expiration**:
Right now, if the JWT expires (say after 1 hour), subsequent API calls will fail with 401. The frontend should handle that gracefully by logging the user out (and maybe redirecting to login). We can achieve this by an Axios response interceptor:

```jsx
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // token might be expired or invalid -> force logout
      AuthContext.logout(); // but we are outside context here.
      // Perhaps we can import store or context, or set a flag that triggers logout in UI.
      // Simpler: redirect to login page:
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

This is a bit hacky but will catch any 401 from API and send user to login.

Alternatively, in each service function we already handle error by e.g., in login function if 401, we returned an error message.

Maybe an improvement: If any API returns 401 while user is logged in, treat it as session expired:

- Could have an effect in AuthProvider that listens for that (but need a global event or the above intercept trick).
  Given advanced dev, they could implement a better state management (maybe using Redux for auth state to dispatch a logout on 401 globally).

For simplicity, the user will figure out if token expired when their actions stop working (maybe gets kicked to login if we handle 401 in each call as needed).

Now the frontend is feature-complete for our scenario.

_Exercise:_ Enhance the ContactsPage to support pagination. Use the `totalPages` from the API’s Page response to render pagination controls (e.g., next and prev buttons or page numbers). Ensure that clicking next/prev updates the page state and triggers `fetchContacts` with the new page number.

Another _Exercise:_ Implement an **import contacts from CSV** feature on the frontend: Provide a file input, on file select, read the file (CSV parsing can be done in browser or sent to backend to parse). Perhaps use a library like PapaParse to parse CSV in frontend, then send an array of contacts to a new backend endpoint to batch create. This requires backend handling (as we hinted in advanced features section for CSV import).

Now, having built both backend and frontend, we should thoroughly test the end-to-end functionality and then consider deployment.

## 6. **Authentication & Authorization**

_(We have implemented authentication and basic authorization in earlier sections, but here we recap and emphasize the security model, ensuring both backend and frontend enforce proper access control.)_

**Authentication** is verifying identity (login), and **authorization** is enforcing access rights (what an authenticated user can or cannot do). Our system uses JWT for stateless authentication and role-based checks for authorization.

### **6.1 JWT Authentication in Spring Boot (Recap)**

In the backend, we configured Spring Security to use JWT tokens:

- **User Login**: The user sends credentials to `/api/auth/login`. Spring Security (via our AuthController) authenticates the credentials against the database (using `UserService` and the `UserDetailsService` implementation). On success, we generate a JWT signed with our secret key. This JWT includes the username (and can include roles/authorities in its claims if we choose). The JWT is returned to the client.
- We chose JWT because it allows the server to remain stateless: all info to validate a user is in the token itself, so we don’t need to keep session data on the server side. The token’s signature and expiration help ensure it’s not tampered with and has a limited lifetime.
- **Token Structure**: The JWT has a header, payload, and signature. We sign it with HS256 algorithm using a secret key. The payload includes `sub: username` and `exp: <expiry time>`. If we included roles, we might have something like `roles: ["ROLE_USER"]` in payload.
- **Password Storage**: User passwords in DB are stored as bcrypt hashes. Spring Security’s `PasswordEncoder` automatically verifies the hash. This ensures even if our database is compromised, raw passwords are not exposed (bcrypt is one-way). During login, Spring Security (via our config `auth.userDetailsService(userService).passwordEncoder(passwordEncoder())`) takes the raw password, hashes it, and compares to stored hash – providing secure authentication.
- **Protecting Endpoints**: In our `SecurityConfig`, we set `.antMatchers("/api/auth/**").permitAll()` (so login and registration are open), and `.anyRequest().authenticated()` for all other endpoints. This means without a valid token, the request won’t reach our controllers (the filter or security chain will block it).
- **JWT Validation Filter**: We created `JwtRequestFilter` which runs for each request, looking for the token in `Authorization` header, and if found, validates it and sets the user authentication in context. It specifically:
  - Checks the token’s signature and expiration using the secret key.
  - If token is invalid or expired, it fails silently (and the request will ultimately be seen as unauthenticated).
  - If valid, it loads the user’s details (to get roles) and then manually creates an authenticated token in the SecurityContext. This effectively “logs in” the user for that single request based on the JWT.
- **CSRF**: We disabled CSRF protection in Spring Security config because we are not using cookies for session, and each request is authenticated via token. CSRF tokens are mainly to protect cookie-based sessions from cross-site request forgery. With JWT (usually sent in header or non-cookie storage), CSRF is not applicable in the same way (an attacker site cannot read the user’s token from localStorage due to browser same-origin policies, and cannot directly steal the token unless XSS, which is a different vector).
- **Logout**: We did not implement a server-side logout because with JWT, “logout” is usually handled on client side by discarding the token. If needed, we could implement token blacklisting or short expiration with refresh tokens, but for our scope, we assume logout = client not sending token anymore (or token expired). We did add a logout in frontend context that just clears local data.

**Testing JWT Flow**:
Using an HTTP client:

```
POST /api/auth/login
{ "username": "alice", "password": "secret" }
--> Response: { "token": "<JWT here>" }

GET /api/contacts (without token)
--> Response: 401 Unauthorized

GET /api/contacts with Header "Authorization: Bearer <JWT>"
--> Response: [ {id: ..., name: ... , ...} ] (list of contacts or empty list)
```

If you decode the JWT (e.g., on jwt.io) you should see the username in payload and correct signature if you use the known secret.

### **6.2 Securing Frontend Routes with Context and PrivateRoute**

On the frontend, we also implemented **route protection**:

- We maintain an `AuthContext` that stores if the user is logged in (and their token). This is provided at the top level of the app.
- The component `PrivateRoute` (or in our case, a check inside the router) uses the context to see if `user` is present. If not, it redirects to `/login`. This ensures that routes like `/contacts` cannot be accessed when not authenticated – the user will be navigated to the login page if they try.
- We also use the context in the Navbar to conditionally show logout button vs login/register links.
- The token is stored in localStorage, so if the user refreshes, the `AuthProvider` will restore the user state (so they don’t have to log in again every time, until the token expires).
- We have not implemented an _idle timeout_ on the frontend, but since the token expires in 1 hour, after that, the next API call will get 401 and we handle it (which can trigger a logout).
- The **React Context API** is a convenient way to pass auth state without prop drilling. We use `useContext(AuthContext)` via our custom `useAuth()` hook anywhere in the component tree to get `user` or call `login/logout` functions, rather than passing those as props down from a top component.

**Role-Based Access Control on Frontend**:
While critical authorization (like preventing access to other users’ data) is enforced in the backend, we often also hide or show UI elements based on roles for a better UX. For example:

- Only show an “Admin Dashboard” link if `user.roles` contains "ROLE_ADMIN".
- If a user somehow navigates to an admin page without the role (e.g., by typing URL), the backend would anyway reject the data fetch. But the frontend should ideally prevent reaching that page. We could implement an `<AdminRoute>` similar to PrivateRoute that checks `user.roles`.
- In our case, since we did not have an admin-specific frontend feature, we mostly ensure a user can only see their contacts. We rely on backend to enforce that if they try to load someone else’s contact by ID.

**Validation & Feedback**:
We implemented simple form validation (required fields). For an advanced system:

- Check password strength on registration (frontend).
- Confirm password field on registration.
- Validate email format (HTML5 `type="email"` covers basic check).
- Show errors from backend (e.g., if username exists, our backend returns an error message, which we do pass back to frontend to display in RegisterPage).

**Storing JWT Securely**:
We used localStorage for convenience. It's worth noting:

- XSS is the primary threat to tokens in localStorage. We mitigate XSS by React’s default escaping and careful coding.
- Another approach: store the token in an HttpOnly cookie so JS can’t access it. But then to avoid CSRF, you’d use SameSite cookies or CSRF tokens. This approach is more involved but slightly more secure against XSS (though if an attacker can run JS, they could also just perform actions directly rather than stealing token).
- Because our app is a first-party client (same domain deployment likely), localStorage is acceptable and simpler. We just have to be vigilant about sanitizing any dynamic content (which React does automatically except in certain cases).

**Session Expiry UX**:
We should handle token expiry gracefully:

- Optionally, implement a countdown or use the `exp` field in JWT (decode it in AuthProvider, and set a timeout to auto-logout or refresh before expiry).
- Or simply catch 401 responses globally and redirect to login with a message "Session expired, please log in again."

Given advanced developers, they might implement a token refresh mechanism:

- One method: Use a refresh token (longer-lived, stored more securely, maybe HttpOnly cookie) and a short-lived access token (our JWT). On 401 due to expiry, use the refresh token endpoint to get a new token, without forcing user to re-login.
- That adds complexity and is beyond scope, but it's an industry standard for JWT auth to avoid forcing logins frequently.

### **6.3 Role-Based Authorization (Backend)**

The backend enforces roles in two ways:

- **Route access**: We used `.anyRequest().authenticated()`, not distinguishing roles in the config, but we could easily restrict certain endpoints by roles. For example:
  ```java
  .antMatchers("/api/admin/**").hasRole("ADMIN")
  .antMatchers("/api/contacts/**").hasAnyRole("USER","ADMIN")
  ```
  This would ensure anything under `/api/admin` only accessible to admin. We did simpler broad rules, but we also enabled method-level security with `@PreAuthorize` on the `listUsers` method (to require ADMIN).
- **Data access**: Even if an endpoint is accessible, we double-check in service methods that the user can only modify their resources (as in ContactService checking `owner.username == currentUsername`). This is important because a malicious user with a valid token for user A should not be able to, say, delete user B’s contact by hitting an API with B’s contact ID. Our check prevents that, returning 403.

If we had different levels of access (like Manager can see contacts of subordinates), we’d implement accordingly in service or via repository queries that filter by allowed scope.

**Adding an Admin User**:
If the system requires an admin, one approach:

- Initialize a default admin at startup (application.properties could contain an admin username & password, or run a SQL script to insert one).
- Or allow user registration and then manually update that user’s roles in DB to include ADMIN (since normal registration gave ROLE_USER).
- The admin can then manage things like all contacts or all users.

**Context of Roles in JWT**:
We didn’t explicitly add roles to JWT generation. We could have:

```java
String token = Jwts.builder()
    .setSubject(username)
    .claim("roles", userDetails.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList())
    ...
    .signWith(...).compact();
```

Then in the filter:

```java
Claims claims = Jwts.parser().setSigningKey(SECRET).parseClaimsJws(token).getBody();
String username = claims.getSubject();
List<String> roles = claims.get("roles", List.class);
```

And then convert roles to `SimpleGrantedAuthority` list. This way, the filter wouldn’t need to call database for user details at all, as all needed info is in token. This is a valid optimization (with the trade-off that if a user’s roles are changed in DB, their existing token still carries the old roles until expiry, which is usually acceptable for short token life).

We kept it simpler by loading user details in filter, which ensures we get latest roles from DB.

### **6.4 Additional Security Measures**

Beyond auth, consider:

- **SQL Injection**: Our use of Spring Data JPA and parameterized queries inherently protects against SQL injection. We never construct SQL manually with string concatenation. Even in custom queries (if we had used `@Query` with `:param` placeholders, that’s safe due to binding). This means inputs like contact name cannot break our queries or drop tables.
- **Validation**: We should validate inputs on backend as well (not rely solely on frontend). For instance, ensure required fields are present, enforce max length (to prevent extremely large inputs), etc. We could use Spring’s Bean Validation (JSR 303, e.g., annotate entity fields with `@NotEmpty`, `@Size(max=100)` and use `@Valid` in controller).
- **Exception Messages**: Be careful not to leak sensitive info in error responses. E.g., our login returns "Invalid credentials" for any bad username or password, rather than "User not found" vs "Password wrong" which could let an attacker brute-force to find existing usernames. We did that correctly by treating both as generic failure.
- **CORS Configuration**: We allowed `http://localhost:3000` for dev. In production, if the React app is served from the same domain, this isn’t an issue (requests will be same-origin). If not, we should configure the allowed origin to the actual domain of the front-end. We should not leave it as open to all (`*`) especially if using credentials.
  - Our usage: since we store token in JS and send in header, not as cookie, we don’t necessarily need to allow cookies. We just need to allow the origin and maybe methods.
  - In Spring, we can fine-tune CORS either in config or with annotations. For global config we did or could do:
    ```java
    @Bean
    public WebMvcConfigurer corsConfigurer() {
      return new WebMvcConfigurer() {
        @Override
        public void addCorsMappings(CorsRegistry registry) {
          registry.addMapping("/api/**")
            .allowedOrigins("https://myapp.example.com")
            .allowedMethods("GET","POST","PUT","DELETE");
        }
      };
    }
    ```
    This ensures in production only our domain can call the APIs.
- **Encryption**: If deploying on production, always use HTTPS so that tokens and data are encrypted in transit. For our AWS deployment, we’ll mention using SSL with CloudFront or Load Balancer.
- **Server Security**: Basic things like updating dependencies to avoid known vulnerabilities (for example, an older Spring Boot might have a vulnerability; keep it updated). Also, securing the server OS, using firewalls, etc., but those are beyond coding scope.
- **Logging and Monitoring**: Log suspicious events (like repeated failed login attempts could indicate brute force). One might implement account lockout after X failed attempts, or use something like reCAPTCHA on login if needed.

The combination of **JWT auth, password hashing, CORS restrictions, input validation, and proper authorization checks** provides a robust security posture for our application.

By this point, we have a fully functional and secure application. Next, we’ll introduce some advanced features to enhance usability and integrability of the system.

## 7. **Advanced Features**

Beyond the basic CRUD and authentication, a production-grade Contact Management System may include advanced features to improve the user experience and integrate with other systems. We will explore a few such features:

- **Search and Filter**: Already touched in our implementation, we allow searching contacts by name. We can extend this to filter by other fields (like company or email domain).
- **Sorting and Pagination**: Improving how we display large lists by allowing sorting by different fields and paginating results.
- **Integrations**: Connecting with external services or automating certain tasks, such as sending emails, importing/exporting contacts, etc.
- **Optimistic Updates**: On the UI, making it feel snappy by updating state before server confirms (with rollback if server fails) – an advanced UX technique.
- **Bulk Operations**: e.g., selecting multiple contacts to delete at once, or tagging multiple contacts.

We will provide guidance on implementing some of these.

### **7.1 Implementing Search and Filter**

**Backend**: We implemented search by name using a Spring Data method `findByOwnerUsernameAndNameContainingIgnoreCase`. To add more filters:

- We could add additional methods, e.g., `findByOwnerUsernameAndCompanyContaining(String username, String company, Pageable p)`.
- Or use Spring Data JPA **Specifications** or Criteria API for flexible filtering on multiple fields. For instance, a Specification could build a query based on which parameters are non-null:
  ```java
  public Page<Contact> searchContacts(String username, String name, String company, Pageable pageable) {
      Specification<Contact> spec = Specification.where(ContactSpecs.isOwner(username));
      if(name != null) spec = spec.and(ContactSpecs.nameContains(name));
      if(company != null) spec = spec.and(ContactSpecs.companyContains(company));
      return contactRepo.findAll(spec, pageable);
  }
  ```
  where ContactSpecs defines static methods returning Specification<Contact>. This is a more complex approach but very powerful for advanced search (e.g., combining multiple criteria).

**Frontend**: If we have multiple filters (say text fields or dropdowns for company, etc.), we collect those and send as query params. Our current UI only filters by name (search box). We could add a dropdown of companies (populated from contact list or a static list) to filter by company, etc. Then include it in request: e.g., `GET /api/contacts?company=ACME`.

**Full-text search**: If requirements were advanced, one might integrate a search engine (like Elasticsearch) for large datasets. But for contacts, and given indexing on columns, the SQL LIKE queries we use should suffice for moderately sized data.

_Integration tip_: Use indexes on fields you search by (we mentioned adding index on `name`, `company` columns to speed up `LIKE` queries).

### **7.2 Sorting and Pagination**

We already used Spring Data’s `Pageable` which supports sorting. The client can specify a sort field and direction.

**Backend**:

- Our `ContactRepository extends JpaRepository` automatically gets methods like `findAll(Pageable)`. We used a custom findByOwnerUsername(Pageable) which also supports sorting within it.
- If we wanted to allow sorting by multiple fields (say name or email), we can accept a parameter and apply it:
  e.g., in service, use `Sort.by(sortBy)` where sortBy is a string like "name" or "email". We should validate that string to avoid allowing arbitrary sorting (though JPA sort by unknown field would error out anyway).
- We might also allow sorting direction (asc/desc). For simplicity, our example always ascending. We could accept a param `sortDir` and do:
  ```java
  Sort sort = sortDir.equalsIgnoreCase("desc") ? Sort.by(sortBy).descending() : Sort.by(sortBy).ascending();
  PageRequest.of(page, size, sort);
  ```
- Ensure the sort field is one of the allowed ones (we wouldn’t want to allow sorting by `password` or something irrelevant, or an extremely large text field perhaps).

**Frontend**:

- We did not fully implement the UI for sorting beyond default. We could add clickable column headers or a sort dropdown (e.g., "Sort by Name | Email | Company").
- On change, call `fetchContacts` with the sort parameter. The backend should then return sorted data.
- Pagination UI: we can add "Previous" and "Next" buttons or page numbers. Since Spring Data provides totalPages, current page, etc., we can utilize that:
  ```jsx
  const [page, setPage] = useState(0);
  // in loadContacts, use page state
  // after loading, set totalPages from response if available.
  ```
  Then in JSX:
  ```jsx
  <div>
    Page {page + 1} of {totalPages}
    <button
      disabled={page === 0}
      onClick={() => {
        setPage((p) => p - 1);
        loadContacts();
      }}
    >
      Previous
    </button>
    <button
      disabled={page === totalPages - 1}
      onClick={() => {
        setPage((p) => p + 1);
        loadContacts();
      }}
    >
      Next
    </button>
  </div>
  ```
  and also call loadContacts when page changes (useEffect dependency on page or directly in onClick as above).
- For a smoother user experience, you might pre-fetch the next page in background or use infinite scroll (e.g., load next page when scrolling near bottom).

Using pagination prevents overloading the client by sending thousands of contacts at once, and improves perceived performance.

### **7.3 Automation and Integrations**

**Email Notifications**: A common feature is sending an email when certain events happen. For instance:

- When a new contact is added, send a confirmation email to the user (or maybe send an introduction email to the contact if applicable).
- When a user registers, send them a welcome email (with Spring Boot, we can use JavaMailSender or an API like SendGrid).

To send email in Spring Boot:

- Include `spring-boot-starter-mail` dependency.
- Configure SMTP settings (e.g., Gmail SMTP or use a service).
- Use `JavaMailSender` to send an email in the service layer after contact creation.
  ```java
  @Autowired JavaMailSender mailSender;
  ...
  SimpleMailMessage msg = new SimpleMailMessage();
  msg.setTo(user.getEmail());
  msg.setSubject("New Contact Added");
  msg.setText("You have added contact " + contact.getName());
  mailSender.send(msg);
  ```
- Or for production, use a service like SendGrid (via API, which might be more reliable).

**SMS or Messaging**: Integration with Twilio API to send an SMS to the user’s phone when something happens (or to send contact info via SMS).

**Third-party API integration**:

- **Gravatar**: Based on contact’s email, you could fetch their Gravatar image (if they have one) – there's a URL convention for that (MD5 of email).
- **Social Media lookup**: If you have an API key for, say, LinkedIn or Clearbit, you could enrich contact info (get company info, profile picture, etc.).
- **Google Contacts API**: If this app needed to sync with Google Contacts, you could use Google People API, but that involves OAuth flow for Google account access.

**Import/Export**:

- **Import CSV**: We mentioned reading a CSV file of contacts. On backend, one can parse CSV using libraries (Apache Commons CSV, OpenCSV). On frontend, one can parse CSV and call the API in a loop or in batch.
- For example, implement an endpoint `/api/contacts/import` that accepts a CSV file upload (multipart) and then backend reads it and creates contacts in batch. Spring Boot makes file upload easy with `@RequestParam MultipartFile file`.
- **Export CSV**: Provide a button to download all contacts as a CSV. Implement `/api/contacts/export` that queries all contacts for the user and returns a CSV (set content type text/csv, Content-Disposition attachment; user gets a file download).
- **Sync with device contacts**: This would be advanced; web apps have limited access to device contacts (usually through user uploading an export from phone or via a mobile app).

**Scheduled Tasks**:

- Use Spring’s `@Scheduled` to run periodic tasks, for example:
  - A birthday reminder: If contacts have a birthday field, a daily job at 8 AM could find contacts whose birthday is today and send the user an email reminder to wish them.
  - Data cleanup: maybe remove contacts that are duplicates, etc., on a schedule.
- Ensure to enable scheduling: `@EnableScheduling` in a config class, and use `@Scheduled(cron="...")` or fixedRate on methods in a Service class.

**Microservice Architecture** (Advanced integration):

- If the system grows, one might split the backend into multiple services: e.g., an Auth Service (for user login, JWT issuing), a Contacts Service (for managing contacts), maybe a Notification Service (for sending emails).
- They would communicate either through HTTP or messaging. We could use an API Gateway to unify them for the frontend.
- This is overkill for our current scope but is something advanced devs might consider for scalability or team separation. Spring Cloud or other technologies would come into play.

**API Documentation**:

- Integrating Swagger/OpenAPI: It’s an advanced feature to generate interactive API docs. We can use **springdoc-openapi** to scan our controllers and generate documentation UI (Swagger UI) automatically.
  - Add dependency `springdoc-openapi-ui`.
  - Access `/swagger-ui.html` or similar to see docs.
    This is helpful for integrations (if external systems or teams use your API).

### **7.4 Performance and User Experience Enhancements**

- **Optimistic UI**: For example, when deleting a contact, we removed it from UI immediately before waiting for server response. We did wait in our code (we awaited deleteContact). But we could optimistically remove it and then if server fails, show an error and re-add it. This yields faster UI response. Same for add/edit: we could update UI immediately (maybe assuming success if network is good).
- **Spinners and Feedback**: We added basic loading states. For better UX, use spinners or skeleton loading indicators for lists.
- **Autosave**: In ContactEdit form, we could auto-save as user types (maybe using debouncing to call updateContact API).
- **Offline Support**: Use service workers or local storage to allow viewing contacts offline, and syncing changes when back online (this turns it into a progressive web app or PWA). This is advanced but libraries like Workbox can help.

By implementing these advanced features, the contact manager becomes more robust and user-friendly. Developers should evaluate which features are necessary for their use case (to avoid unnecessary complexity). It’s often best to implement core functionality first (as we did) then iteratively add enhancements like search, pagination, and integrations.

_Exercise:_ Implement a **bulk delete** feature on the ContactsPage. Add checkboxes next to each ContactCard, and a “Delete Selected” button. When clicked, send one request to delete multiple contacts (you could create an endpoint accepting a list of IDs in the request body for deletion). Ensure that the UI state updates by removing those contacts upon success. Consider confirmation to avoid accidental bulk deletion.

Another _Exercise:_ Add a **tagging** system for contacts. Users can create tags (like “Friend”, “Work”, “VIP”) and assign to contacts. This involves creating a Tags entity and a many-to-many with Contact (similar to roles with users). Update the UI to display and filter by tags. This helps categorize contacts and is a common CRM feature.

Having explored these advanced topics, let's move on to testing our application to ensure quality.

## 8. **Testing**

Testing is crucial to ensure our system works as expected and to prevent regressions when making changes. We will cover testing in three parts: **backend unit and integration tests**, **frontend component tests**, and **API testing** (manual or automated).

We aim to achieve good coverage on critical pieces like service logic, security, and UI components.

### **8.1 Backend Testing (JUnit & Mockito)**

For the Spring Boot backend, we can write tests using JUnit 5 (JUnit Jupiter) and use Mockito to mock dependencies or use Spring’s test context for integration tests.

**Setting up Test Environment**:

- Spring Boot Starter Test is likely already included (if not, add `spring-boot-starter-test` to pom). It includes JUnit, Mockito, Spring Test, etc.
- We may use an in-memory database for tests (H2) to avoid needing a running MySQL for unit tests. Spring Boot test can automatically use H2 if on classpath and if we override properties for test.

**Unit Testing Service Layer**:
We can test services by mocking the repository layer. For example, test `ContactService`:

```java
@ExtendWith(MockitoExtension.class)
public class ContactServiceTest {
    @Mock
    private ContactRepository contactRepo;
    @Mock
    private UserRepository userRepo;
    @InjectMocks
    private ContactService contactService;

    @Test
    public void testAddContactSuccess() throws Exception {
        // Arrange
        User user = new User("alice", "pass", "alice@example.com");
        user.setId(1L);
        Contact contact = new Contact("Bob", "bob@example.com", "1234567890");
        // Stub userRepo to return user when findByUsername
        Mockito.when(userRepo.findByUsername("alice")).thenReturn(Optional.of(user));
        // Stub contactRepo to return contact (with id) when save
        Contact savedContact = new Contact("Bob", "bob@example.com", "1234567890");
        savedContact.setId(10L);
        Mockito.when(contactRepo.save(any(Contact.class))).thenReturn(savedContact);

        // Act
        Contact result = contactService.addContact("alice", contact);

        // Assert
        assertNotNull(result);
        assertEquals(10L, result.getId());
        assertEquals("Bob", result.getName());
        // Verify that contactRepo.save was called with a Contact that has owner set to user
        Mockito.verify(contactRepo).save(argThat(c -> c.getOwner().equals(user)));
    }

    @Test
    public void testAddContactUserNotFound() {
        // Arrange
        Mockito.when(userRepo.findByUsername("alice")).thenReturn(Optional.empty());
        Contact contact = new Contact("Bob", "bob@example.com", "123");
        // Act & Assert
        assertThrows(Exception.class, () -> {
            contactService.addContact("alice", contact);
        });
    }

    @Test
    public void testDeleteContactUnauthorized() {
        // Arrange: contact exists but with different owner
        User owner = new User("bob", "pass","bob@ex.com"); owner.setId(2L);
        Contact contact = new Contact("Jane","j@ex.com",""); contact.setId(5L);
        contact.setOwner(owner);
        Mockito.when(contactRepo.findById(5L)).thenReturn(Optional.of(contact));
        // Act & Assert
        Exception ex = assertThrows(Exception.class, () -> {
            contactService.deleteContact("alice", 5L);
        });
        assertTrue(ex.getMessage().contains("Unauthorized"));
    }
}
```

This uses **Mockito** to stub repository calls. We test:

- Successful addition sets the right owner and returns the saved contact.
- Throwing exception if user not found.
- Unauthorized deletion attempt results in exception.

We would similarly test `UserService`: e.g., registering a new user (mock roleRepo and userRepo to ensure unique email enforcement, etc.), and `loadUserByUsername` returns proper UserDetails.

**Controller Tests**:
We can test controllers either by mocking service (unit test of controller) or via Spring’s MockMvc (integration test including the web layer and maybe service with mocks or actual service).

Example using MockMvc:

```java
@SpringBootTest
@AutoConfigureMockMvc
@TestInstance(Lifecycle.PER_CLASS)
public class ContactControllerTest {
    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private UserRepository userRepo;
    @Autowired
    private ContactRepository contactRepo;
    @Autowired
    private JwtUtil jwtUtil;

    private String token;
    @BeforeAll
    void setupUserAndToken() {
        // create a test user in H2
        User user = new User("testuser", passwordEncoder().encode("testpass"), "test@example.com");
        Role role = new Role("ROLE_USER");
        user.getRoles().add(role);
        userRepo.save(user);
        // generate a token for this user
        token = jwtUtil.generateToken("testuser");
    }
    @Test
    public void testGetContactsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/contacts"))
               .andExpect(status().is(401));
    }
    @Test
    public void testAddAndGetContact() throws Exception {
        String newContactJson = "{ \"name\": \"Tim\", \"email\": \"tim@example.com\" }";
        // Add contact
        mockMvc.perform(post("/api/contacts").contentType("application/json")
                      .header("Authorization", "Bearer " + token)
                      .content(newContactJson))
               .andExpect(status().isCreated())
               .andExpect(jsonPath("$.id").exists())
               .andExpect(jsonPath("$.name").value("Tim"));
        // Get contacts and verify new contact appears
        mockMvc.perform(get("/api/contacts").header("Authorization","Bearer "+token))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.content[*].name").value(Matchers.hasItem("Tim")));
    }
}
```

This is an integration test:

- It uses @SpringBootTest to bring up the context (with an H2 DB by default).
- We manually inserted a user into the H2 via repository, then manually created a JWT for that user using our JwtUtil (which we autowired).
- Then we call endpoints using MockMvc, adding the Authorization header.
- We check HTTP status and response JSON using MockMvc result matchers.

This test hits the real controller, and real service and repository (using H2). It’s a good end-to-end test for the API. We used jsonPath to verify the JSON content.

We also test unauthorized access returns 401 correctly.

For thoroughness, we would test other endpoints similarly (update, delete, login, etc.). Spring Security in tests: we manually provided token, which is fine. Alternatively, we could use MockMvc with `with(user("testuser").roles("USER"))` to mock an authenticated user without JWT, but since our security relies on JWT filter, it’s easier to just provide the token.

**Edge Cases**:

- Test login with wrong credentials returns 401.
- Test cannot register two users with same username.
- Test a user cannot get another user’s contact (e.g., create contact for user A, then user B with their token tries to get it -> should 403).
- If using roles, test that admin can access admin endpoints and non-admin cannot.

### **8.2 Frontend Testing (Jest & React Testing Library)**

For React, we use **Jest** (which comes with Create React App) and **React Testing Library (RTL)** for component testing. The idea is to test components in isolation by rendering them and simulating user interactions.

**Setup**:

- Ensure `npm run test` runs the tests (CRA is pre-configured).
- We might need to mock certain modules (like Axios calls) to not actually call the API in unit tests. We can use Jest mocks for that.

Test example: **LoginPage**:

```jsx
// LoginPage.test.js
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import LoginPage from "../pages/LoginPage";

// We will mock useAuth to simulate login function without actually calling API
const mockLogin = jest.fn();
jest.mock("../context/AuthContext", () => {
  const originalModule = jest.requireActual("../context/AuthContext");
  return {
    __esModule: true,
    ...originalModule,
    useAuth: () => ({ login: mockLogin }),
  };
});

test("renders login form", () => {
  render(<LoginPage />, { wrapper: MemoryRouter }); // or wrap with AuthProvider
  expect(screen.getByText(/Login/)).toBeInTheDocument();
  expect(screen.getByLabelText(/Username/)).toBeInTheDocument();
  expect(screen.getByLabelText(/Password/)).toBeInTheDocument();
});

test("calls login on form submit with correct data", async () => {
  mockLogin.mockResolvedValueOnce(true); // simulate login returning success
  render(
    <AuthProvider>
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    </AuthProvider>
  );
  // fill form
  fireEvent.change(screen.getByLabelText(/Username/), {
    target: { value: "alice", name: "username" },
  });
  fireEvent.change(screen.getByLabelText(/Password/), {
    target: { value: "password", name: "password" },
  });
  fireEvent.click(screen.getByText("Login"));
  // expect login to be called with given credentials
  expect(mockLogin).toHaveBeenCalledWith("alice", "password");
  // We could also assert that navigate was called to /contacts.
  // But since we didn't mock useNavigate from react-router, that might actually navigate in MemoryRouter which has no UI effect.
  // Instead, we can check if navigate would have been called by mocking useNavigate similarly if needed.
});
```

We mocked `useAuth` to isolate the LoginPage from actual AuthContext implementation. This way, we can control `login` function behavior.

**Testing ContactForm** (a pure component):

```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import ContactForm from "../components/ContactForm";

test("ContactForm calls onSave with entered data", () => {
  const initialData = { name: "Old", email: "old@example.com" };
  const onSave = jest.fn();
  const onCancel = jest.fn();
  render(
    <ContactForm
      initialData={initialData}
      onSave={onSave}
      onCancel={onCancel}
    />
  );
  // Change the name
  fireEvent.change(screen.getByLabelText(/Name/), {
    target: { value: "New Name", name: "name" },
  });
  fireEvent.submit(screen.getByRole("button", { name: /Save/i }));
  expect(onSave).toHaveBeenCalled();
  const savedArg = onSave.mock.calls[0][0];
  expect(savedArg.name).toBe("New Name");
  expect(savedArg.email).toBe("old@example.com"); // didn't change email field
});
```

This ensures the form collects data properly and triggers callback.

**Testing ContactCard**:
We can test that clicking edit/delete calls the callbacks:

```jsx
test("ContactCard edit and delete buttons trigger callbacks", () => {
  const contact = { id: 1, name: "Test", email: "t@e.com", phone: "123" };
  const onEdit = jest.fn();
  const onDelete = jest.fn();
  render(<ContactCard contact={contact} onEdit={onEdit} onDelete={onDelete} />);
  fireEvent.click(screen.getByText(/Edit/));
  expect(onEdit).toHaveBeenCalled();
  fireEvent.click(screen.getByText(/Delete/));
  expect(onDelete).toHaveBeenCalled();
});
```

**Testing an asynchronous component** like ContactsPage is trickier because it calls API on mount. We should mock `fetchContacts` and possibly `deleteContact` from contactService:
Use jest.mock to mock the entire module `../services/contactService`.

```jsx
jest.mock("../services/contactService", () => ({
  fetchContacts: jest.fn(),
  deleteContact: jest.fn(),
}));
import { fetchContacts, deleteContact } from "../services/contactService";
```

Then define behavior:

```jsx
test("ContactsPage displays contacts list", async () => {
  fetchContacts.mockResolvedValue({
    content: [
      { id: 1, name: "A", email: "a@x.com" },
      { id: 2, name: "B", email: "b@x.com" },
    ],
  });
  render(
    <AuthProvider>
      <MemoryRouter>
        <ContactsPage />
      </MemoryRouter>
    </AuthProvider>
  );
  // Wait for the contacts to be rendered
  expect(await screen.findByText("A")).toBeInTheDocument();
  expect(screen.getByText("B")).toBeInTheDocument();
});
```

We used `findByText` which returns a promise that resolves when the element is found (or times out). This is how RTL handles async content (it keeps querying until condition meets or default timeout ~1s).

We should also test that the delete button calls deleteContact and updates the UI:

```jsx
test("deleting a contact removes it from list", async () => {
  fetchContacts.mockResolvedValueOnce({
    content: [{ id: 1, name: "X", email: "x@c.com" }],
  });
  deleteContact.mockResolvedValueOnce({});
  render(
    <AuthProvider>
      <MemoryRouter>
        <ContactsPage />
      </MemoryRouter>
    </AuthProvider>
  );
  // ensure contact X appears
  await screen.findByText("X");
  fireEvent.click(screen.getByText(/Delete/));
  // confirm dialog appears, but we can simulate confirmation by not actually using window.confirm in tests (we might need to mock window.confirm)
});
```

However, `window.confirm` in our code will actually open a dialog which can’t be handled by test easily. We should mock `window.confirm` in tests to always return true:

```jsx
window.confirm = jest.fn(() => true);
```

Then after firing delete, we should wait for UI update:
One approach: after deletion, our code does `setContacts` filtering. That will remove element "X" from DOM. We can assert it's gone:

```jsx
expect(screen.queryByText("X")).not.toBeInTheDocument();
```

We might need to wait a tick for state update, but since our deleteContact call is awaited, after the click and confirm, presumably state updates synchronously. If needed, use `await waitFor(() => expect(screen.queryByText("X")).toBeNull());`.

**End-to-End Testing**:
We can use tools like **Postman** for API testing or Cypress for end-to-end UI testing. But given scope, likely manual or Postman tests are enough.

Postman collection can have:

- A request for user registration (or skip if focusing on main flows).
- Login request.
- Environment variable to store token from login response.
- Then contacts requests (GET all, POST create, PUT update, DELETE) using the token.

This ensures the API works correctly. We already did similar in development manually.

**Continuous Integration**:
In CI pipeline (discussed next section), we would run these tests. The backend tests can run with `mvn test`. The frontend tests run with `npm test -- --watchAll=false` (to run once in CI environment).
Ensuring tests pass in CI gates our deployment.

By writing these tests, we achieve:

- Confidence that each unit works (services, components).
- Protection against breaking something (if we refactor code, tests failing will alert us).
- Documentation of expected behaviors (tests often serve as spec of how code should behave under certain conditions).

## 9. **Deployment Strategy**

Deploying our application involves preparing both the frontend and backend for a production environment, containerizing them for consistency, and setting up infrastructure to host them. We will explore a deployment scenario using **Docker** for packaging and **AWS** for hosting, with a CI/CD pipeline for automation (using GitHub Actions as an example).

### **9.1 Dockerizing the Applications**

**Why Docker?** Docker allows us to package the application along with all its dependencies into a portable container image. This ensures that the app runs the same in production as it did in development, eliminating environment inconsistencies.

We will create separate Docker images for:

- The React frontend (which will be built and served as static files).
- The Spring Boot backend (which will run as a Java process in a container).
- The MySQL database (we could use the official MySQL image in production, or use AWS RDS which is a managed MySQL – we'll opt for RDS in AWS section).

**Dockerfile for Backend (Spring Boot)**:
We will use a multi-stage build. In the first stage, we build the jar using Maven. In the second, we run it with a lightweight JRE.

Create a file `Dockerfile` in the Spring Boot project root:

```
# Stage 1: Build the jar
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM openjdk:17-jdk-slim
WORKDIR /app
# Copy the jar from the build stage
COPY --from=build /app/target/contact-manager-0.0.1-SNAPSHOT.jar app.jar
# Environment variables (if any, e.g., for DB connection) can be declared
# e.g. ENV SPRING_PROFILES_ACTIVE=prod
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
```

Explanation:

- We first use an official Maven image with JDK 17 to compile the project. We copy source code and run `mvn package`. The output jar is inside `target/`.
- Then we use a smaller base image for just running. `openjdk:17-jdk-slim` is fine; even better could be a JRE-only image or a distroless Java image for minimal attack surface.
- We copy the built jar from stage1.
- We expose port 8080 (the container’s port; in AWS, the load balancer will map to it).
- The app likely will connect to a database. We should externalize DB credentials via environment variables. We can, for example, have in application.properties placeholders:
  ```
  spring.datasource.url=${DB_URL}
  spring.datasource.username=${DB_USER}
  spring.datasource.password=${DB_PASS}
  ```
  Then in the Docker (or AWS config), set these env variables. Alternatively, use AWS RDS’s instance endpoint and credentials configured via Spring Boot's environment.

We'll handle config via environment variables in deployment.

**Dockerfile for Frontend (React)**:
The React app is static after build. We can serve it via an Nginx web server in the container. Multi-stage Dockerfile:

```
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .  # copy all source
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
# Copy built files from stage1
COPY --from=build /app/build /usr/share/nginx/html
# Copy a default nginx config if needed (to handle routing)
# For SPA routing, we might add an nginx config to redirect 404 to index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
```

Explanation:

- Use a Node alpine image to install and build React app. The output goes to `/app/build`.
- Then use Nginx (small Alpine version). Copy the static files into Nginx’s default web root.
- We expose port 80 (Nginx default HTTP).
- Optionally, provide a custom nginx.conf. For a React SPA, if using client-side routing (we are, with react-router), you need to configure Nginx to serve `index.html` for any unknown path (so that routes like /contacts still return the index page, and React router takes over). A simple nginx.conf:

  ```
  server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html index.htm;

    location / {
      try_files $uri /index.html =404;
    }
  }
  ```

  This `try_files` ensures if a file is not found (like /contacts which isn’t a real file), it serves index.html.

- This container image will serve the frontend.

Now we can build these images:

```
docker build -t myapp-backend:1.0 .
```

(in backend project folder with Dockerfile)

```
docker build -t myapp-frontend:1.0 .
```

(in frontend project folder)

Test locally:

```
docker run -p 8080:8080 -e DB_URL=jdbc:mysql://host:3306/db -e DB_USER=user -e DB_PASS=pass myapp-backend:1.0
```

(using a local MySQL or container network if you have MySQL container).

```
docker run -p 3000:80 myapp-frontend:1.0
```

Then check `http://localhost:3000` loads UI, which calls `localhost:8080/api`. If not same host, adjust proxy or deploy such that they are accessible.

In production on AWS, we won't directly run these manually, but it's good to ensure images work.

### **9.2 Setting Up CI/CD Pipeline**

We want to automate building, testing, and deploying the app. We can use **GitHub Actions** as an example CI/CD solution (Jenkins or GitLab CI could similarly be used).

**Continuous Integration (CI)**:

- When code is pushed to main or a release branch, run backend tests and frontend tests.
- If tests pass, build the Docker images.
- Push the images to a container registry (like Docker Hub or AWS ECR).

**Continuous Deployment (CD)**:

- After building images, deploy to AWS:
  - This could be done by connecting to an EC2 and running docker-compose or updating services.
  - Or by using AWS services like ECS (Elastic Container Service) or EKS (Kubernetes) which run containers.
  - Or using AWS Elastic Beanstalk (which can handle a Docker multi-container setup).
  - For simplicity, we can also just use EC2 VMs and run Docker manually or via docker-compose.

Given the user specifically mentioned EC2, RDS, S3:

- We’ll deploy frontend to S3 (as static site) instead of containerizing it (an alternative approach, but since we have a container approach, let’s combine: perhaps easier is indeed to use S3+CloudFront for frontend).
- Spring Boot to EC2, DB on RDS.

However, since we already made a Docker for frontend with Nginx, we can also run it on an EC2, but that’s less efficient than using S3+CloudFront. Using S3 is great for static files because AWS will serve them with a CDN (CloudFront) cheaply and efficiently.

We should choose one:
**Preferred**: S3 for static (so no need to maintain a server for it).
We can still use our build process to get static files (from `npm run build` stage), then upload to S3 bucket.

**CI Steps Outline**:

1. **Checkout code**.
2. **Set up Java and Node** for tests/build.
3. **Back-end build & test**: run `mvn test`.
4. **Front-end build & test**: run `npm ci && npm run test -- --watchAll=false`.
5. **Build production artifacts**:
   - Run `mvn package` to get jar (for non-container artifact).
   - Run `npm run build` to get static files (for S3).
   - Or directly build Docker images if deploying via Docker.
6. **If all good, deploy**:
   - Option 1: Build & push Docker images to registry, then update containers in AWS.
   - Option 2: Upload frontend build to S3, and deploy backend jar to an EC2 or use Elastic Beanstalk (EB supports running a jar or a Docker image).

We'll focus on using Docker images:

- We'll push images to **Docker Hub** or **ECR**. Let's say Docker Hub for demonstration (need Docker Hub creds in GitHub Actions secrets).
- Then on the EC2 server, we need a mechanism to pull the new images and restart containers. This could be via SSH commands in the Action or use a deploy service (like AWS CodeDeploy or just do manually).
- Alternatively, use an ECS cluster with a service. The GitHub Action can update the ECS service with new task definition pointing to new image tags (this is a bit involved but doable with AWS CLI).

To keep it simpler, consider using **Elastic Beanstalk**:

- EB can host a Docker app or a JAR easily. We could set up EB environment for the backend (platform: Docker or Java).
- For frontend, EB could host if we containerize it, but S3 is simpler.

However, since they've explicitly said deploy to EC2, RDS, S3 (which sounds like separate handling for each):

- RDS: we use AWS RDS MySQL as DB.
- EC2: run the Spring Boot (maybe via Docker or directly java -jar).
- S3: host the React static files.

This is a straightforward approach:

1. Create an EC2 (Amazon Linux 2 or Ubuntu).
2. Install Docker on it (if using container).
3. Or install Java and run jar.
4. Create RDS MySQL, configure SG so EC2 can connect, note endpoint, username, password.
5. On EC2, set environment variables DB_URL, DB_USER, DB_PASS (or put in properties file).
6. Run container: `docker run -d -p 80:8080 ... -e DB_URL=... ... backend-image`.
   (Mapping port 8080 container to 80 host so it's easier).
7. Alternatively, not use Docker: copy jar to EC2 and run as service (less ideal because you must manage Java environment manually).
8. S3: create bucket (enable static site hosting or use CloudFront), upload the contents of `build/` directory (index.html, static assets).
   - Ensure bucket policy allows public read or use CloudFront that handles it.

**GitHub Actions YAML** (conceptual snippet):

```yaml
name: CI-CD

on:
  push:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    env:
      AWS_REGION: us-east-1
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          java-version: "17"
          distribution: "temurin"
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: "18"
      - name: Back-end tests
        run: mvn --batch-mode test
      - name: Front-end install & tests
        run: |
          cd contact-manager-ui
          npm ci
          npm run test -- --watchAll=false
      - name: Build back-end jar
        run: mvn --batch-mode package -DskipTests
      - name: Build front-end production
        run: |
          cd contact-manager-ui
          npm run build
      - name: Docker login
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build and push backend image
        run: |
          docker build -t myapp-backend:${{ github.sha }} .
          docker tag myapp-backend:${{ github.sha }} mydockerhubuser/myapp-backend:latest
          docker push mydockerhubuser/myapp-backend:latest
      - name: Build and push frontend image
        run: |
          cd contact-manager-ui
          docker build -t myapp-frontend:${{ github.sha }} .
          docker tag myapp-frontend:${{ github.sha }} mydockerhubuser/myapp-frontend:latest
          docker push mydockerhubuser/myapp-frontend:latest
      - name: AWS Deploy Backend
        uses: appleboy/ssh-action@v0.1.6
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ec2-user
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            docker pull mydockerhubuser/myapp-backend:latest
            docker stop myapp-backend || true
            docker rm myapp-backend || true
            docker run -d --name myapp-backend -p 80:8080 \
              -e DB_URL=${{ secrets.RDS_JDBC_URL }} \
              -e DB_USER=${{ secrets.RDS_USER }} \
              -e DB_PASS=${{ secrets.RDS_PASS }} \
              mydockerhubuser/myapp-backend:latest
      - name: AWS Deploy Frontend to S3
        uses: jakejarvis/s3-sync-action@v0.5.1
        with:
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          args: --acl public-read --delete
          source_dir: "./contact-manager-ui/build"
          destination_bucket: "my-frontend-bucket"
```

This workflow does:

- Run tests, build artifacts.
- Build Docker images and push to Docker Hub.
- SSH into EC2 and run docker commands to update backend container.
- Sync built static files to S3 (making them public). In production, better to use CloudFront in front of that S3 for CDN and HTTPS. But one could also serve from an EC2 Nginx.

Note: We used `appleboy/ssh-action` to run commands on EC2 via SSH (requires adding the EC2 private key in secrets or use user/pw). We pass RDS info as secrets to not expose them.

Also, ensure EC2’s security group allows port 80 (HTTP) or 443. For production, maybe we want HTTPS terminated at load balancer or at least open 443 with a cert.

**Setting up AWS**:

- **EC2**: Use an Amazon Linux 2 AMI. SSH in, install docker:
  ```bash
  sudo yum update -y
  sudo amazon-linux-extras install docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  ```
  (logout & in to apply group). Also, install docker-compose if needed (not strictly if one container).
- **RDS**: Launch MySQL instance, set username/password. In RDS security group, allow inbound from EC2's security group or IP. Use multi-AZ for prod reliability.
- **S3**: Create bucket (unique name). Enable static website hosting (gives an endpoint). Or attach CloudFront for custom domain and HTTPS. Also, set bucket policy to allow public read on `/*` if using static site endpoint (the Jarvis action above sets `public-read` ACL on objects, which might suffice).

**Deployment Verification**:

- After pipeline runs, go to the S3 static site URL or CloudFront URL: the React app should load.
- It will try to call API (assuming our Axios baseURL is configured properly for production). If React is served from domain, and API is on EC2 (different domain/IP), ensure CORS allows it, or consider pointing a subdomain to EC2.
- E.g., API could be accessible at `api.myapp.com` and front at `myapp.com`.
- If using CloudFront, you can create a distribution for S3 (with a custom domain like `app.myapp.com`).
- For API, could set up an Application Load Balancer in front of EC2 (especially if scaling to multiple EC2 instances) and attach a domain with SSL.

**Scaling Considerations**:

- To scale backend: run multiple containers or use ECS Service with multiple tasks behind a load balancer. RDS will handle moderate load, can scale up or add read replicas if needed for heavy read.
- To scale frontend: S3+CloudFront is already highly scalable (just static delivery).
- Using AWS Elastic Beanstalk could simplify deployment (it would manage EC2, load balancing, scaling for you; you just push the Docker or Jar).
- Alternatively, use Kubernetes (EKS) if going cloud-native with more complexity.

### **9.3 Deployment to AWS: EC2, RDS, S3**

Let's walk through a manual perspective (assuming not fully automated, or for understanding):

**Database (RDS)**:

- After RDS is ready, note the endpoint, e.g., `mydb.c123456789.us-east-1.rds.amazonaws.com`.
- In our Spring Boot config on EC2, set:
  ```
  DB_URL=jdbc:mysql://mydb.c123...amazonaws.com:3306/contact_db?useSSL=false&allowPublicKeyRetrieval=true
  DB_USER=mydbuser
  DB_PASS=mypassword
  ```
- Also ensure the RDS SG allows EC2's SG access.

**Backend (EC2)**:

- We might not want to expose backend directly on internet port 80/8080 without SSL. For quick deployment, maybe fine for testing.
- Better approach: Put an ALB (Application Load Balancer) in front of EC2:
  - ALB listens on 80/443, forwards to EC2 on 8080.
  - Then we attach an ACM (AWS Certificate Manager) SSL cert to ALB for `api.myapp.com`.
  - Then our React app can call `https://api.myapp.com` with secure connection.
- If skipping ALB, at least ensure traffic is limited. But for production, ALB is recommended for TLS and scaling.

**Frontend (S3)**:

- Upload build to S3. Enable static site hosting (gives a URL like `http://bucket-name.s3-website-us-east-1.amazonaws.com`).
- If using CloudFront:
  - Create distribution, origin is the S3 bucket (as website endpoint or S3 origin with OAC).
  - Attach ACM cert for `app.myapp.com`.
  - CloudFront will cache and serve content globally.
  - Use `app.myapp.com` for front-end, `api.myapp.com` for backend in config.
- Adjust React's base API URL accordingly. In our code, we set baseURL as "http://localhost:8080/api" for dev. For production, we should set it to the actual API endpoint.
  - We can do this dynamically via environment variables at build time or detect hostname:
  - Simplest: set `REACT_APP_API_URL` env var before build and use that in axios config.
    For example, in `.env.production`: `REACT_APP_API_URL=https://api.myapp.com/api`.
    Then in api.js: `baseURL: process.env.REACT_APP_API_URL`.
  - This way, front-end knows to call correct URL.

**Monitoring & Logging**:

- Use AWS CloudWatch to collect logs. You can run the CloudWatch agent on EC2 to push Docker logs or application logs.
- Set up alarms for high CPU, errors, etc.

**Backup**:

- For RDS, enable automatic backups and snapshots.
- The app data (contacts) is in DB, so backup DB regularly.

**CDN & Caching**:

- CloudFront will cache static assets. Also consider enabling caching for API responses if appropriate (maybe not for dynamic data like contacts).
- The Contacts API could use conditional GET or ETags to avoid sending unchanged data repeatedly.

At this stage, our app should be live and accessible. The pipeline ensures new changes can be deployed swiftly.

### **9.4 Alternative Deployment: Docker Compose on a VM**

Alternatively, one could have a single VM running both frontend and backend containers with docker-compose:

```yaml
version: "3"
services:
  backend:
    image: mydockerhubuser/myapp-backend:latest
    environment:
      - SPRING_DATASOURCE_URL=${DB_URL}
      - SPRING_DATASOURCE_USERNAME=${DB_USER}
      - SPRING_DATASOURCE_PASSWORD=${DB_PASS}
    ports:
      - "8080:8080"
  frontend:
    image: mydockerhubuser/myapp-frontend:latest
    ports:
      - "80:80"
```

Then one would just update images and do `docker-compose pull && docker-compose up -d` via SSH or in pipeline.
This runs both on same server. It’s okay for small scale, but separating is more scalable and secure (front-end static can be offloaded to S3/CloudFront as we did, freeing backend server to just handle API).

**Wrap up**:
We now have a deployment process:

- **Local**: dev environment with React dev server and Spring Boot local.
- **CI**: verifying code with automated tests.
- **CD**: building images/artifacts and deploying to cloud (AWS in our case).
- The app runs in cloud with real domain and is accessible to end users.

_Exercise:_ Set up a custom domain for your application:

- Register a domain (if not already).
- Use Route 53 (AWS) to create DNS records: e.g., CNAME `app.mydomain.com` to CloudFront distribution for front-end, and CNAME `api.mydomain.com` to ALB or directly to EC2 (not recommended to point CNAME to EC2 IP as it changes; better use an Elastic IP or an ALB which has DNS).
- Request an SSL certificate via ACM for both subdomains, attach to CloudFront and ALB respectively.
- Update React config to use `https://api.mydomain.com` for API.
- Test that `https://app.mydomain.com` loads and communicates securely with the API.

By completing deployment, your contact management system is now live. The next section will discuss security and optimization considerations in production.

## 10. **Security & Optimization**

Now that the application is deployed, we must ensure it is secure against threats and performs well under load. We will cover:

- Protecting the system from common vulnerabilities (CSRF, XSS, SQL injection, etc.).
- Optimizing performance (both backend and frontend) with caching, query tuning, and scaling.
- Ensuring the app can scale (load balancing, statelessness, etc.).

### **10.1 Security Best Practices**

**CSRF Protection**:

- As mentioned, since we use JWT in headers and not cookies for auth, CSRF (Cross-Site Request Forgery) is not a primary concern. CSRF typically requires an authenticated session via cookie. In our design, an attacker cannot force the victim’s browser to add the Authorization header with JWT (because it's stored in localStorage and only our JS reads it).
- If we had used cookies, we’d need to include CSRF tokens. Our Spring Security config disabled CSRF for stateless APIs, which is correct.
- We should still ensure that sensitive endpoints require proper auth (which they do via JWT). There's a slight nuance: if JWT were stored in a cookie, then a CSRF attack could occur (since browser auto-sends cookies). But we are not doing that.

**XSS (Cross-Site Scripting)**:

- XSS could allow stealing tokens or impersonating users. Our defense:
  - React’s escaping of content by default. We never insert raw HTML from contacts or users into the DOM.
  - We should validate or sanitize any data that could contain HTML. For instance, if a contact’s name was `<img src=x onerror=alert(1)>`, React would render it as text, not execute it, which is good.
  - In case we ever need to display rich text (not in our use case), use a sanitizer or carefully handle `dangerouslySetInnerHTML`.
  - Also, HTTP headers like Content-Security-Policy (CSP) can mitigate XSS by restricting script sources. We could configure CSP in our Nginx for frontend (e.g., only allow scripts from our domain).
- We should also ensure error messages or data returned by backend are properly escaped if inserted into HTML. Our UI prints errors directly but as text nodes, so safe.

**SQL Injection**:

- We prevent it by using prepared statements or JPA. e.g., JPA repository methods automatically parameterize queries. If we built dynamic queries for search, we used method naming or Specification which also parameterizes inputs.
- **Never** concatenate user input into JPQL/SQL without binding. If using `@Query`, use `:param` for binding, not string concatenation.
- Our use of Spring Data means we effectively used prepared statements behind the scenes, so injection is mitigated.

**Encryption (HTTPS)**:

- Ensure the application is accessed via HTTPS only. For our AWS setup, use CloudFront and ALB with certificates, and optionally enforce HTTP->HTTPS redirect.
- The connection to RDS from EC2 can be encrypted by enabling SSL. That might need adding `?useSSL=true&verifyServerCertificate=false` in JDBC URL and using RDS’s public SSL cert. If EC2 and RDS are in same VPC, encryption might be less critical, but still good practice if data is sensitive.

**Authentication Hardening**:

- Use strong secrets for JWT signing and keep them out of code (we did, presumably via env variable).
- Set a reasonable expiration for JWT (we set 1 hour). Too long tokens can be a risk if stolen; too short can annoy users by requiring frequent re-login or refresh flows.
- Possibly implement refresh tokens if wanting long sessions: short-lived access token, long-lived refresh token (httpOnly cookie or so).
- Password policies: ensure users use strong passwords. We didn’t enforce complexity in code, but could in registration (e.g., at least 8 chars, one number, etc.). This can be done via Bean Validation (like `@Size(min=8)` on password field and maybe a custom validator for complexity).
- Account lockout: to prevent brute force, after N failed login attempts, lock account for some time. Spring Security can handle this via an `UserDetails` field (accountNonLocked) and some custom logic or using something like Spring Security’s login throttling. Alternatively, use something like Google reCAPTCHA on the login form after a few failures.

**Authorization**:

- We covered role checks. If more roles are added, ensure endpoints specify correct `@PreAuthorize` or config rules.
- Verify that no sensitive data is leaked through any endpoint:
  - For example, our `/api/contacts` returns Contact objects with an `owner`. We should ensure that JSON serialization doesn't inadvertently expose the owner's password or other info. We didn't put password in Contact, but Contact references User (owner). By default, Jackson might serialize User (which includes roles, and password?). Actually, our User has password field. If Jackson tries to serialize Contact.owner, it could include the user’s password hash. That’s a leak.
  - Solution: add `@JsonIgnore` on sensitive fields in entities. For instance, on `User.password` put `@JsonIgnore`. Also possibly on `User.roles` or `Contact.owner` to avoid deep recursion or exposing internals.
  - Or use DTOs: we could return ContactDTO to front-end that does not include owner or any user info, only necessary contact fields.
  - This is important — in production, never expose password hashes or unnecessary relations via API. We should double-check our JSON output.
- Testing auth: attempt actions as different users to confirm security. E.g., user A trying to load user B’s contact via API should get 403 (we handle that).

**CORS**:

- Currently allowed origin for dev. In production, set allowedOrigins to the actual domain(s) of your front-end. For instance, `https://app.myapp.com`.
- Alternatively, in Spring Security config, we could do:
  ```java
  http.cors();
  ```
  with a bean configuring allowed origins as needed. Or use `@CrossOrigin` on controllers methods specifically for needed cases.
- If not properly configured, either frontend calls will be blocked by browser, or if too permissive, other sites could attempt to use the API. But since they’d need a JWT, risk is lower, but better to restrict.

**Server Hardening**:

- Ensure the EC2 security group only allows necessary traffic (80/443 from internet, 22 from your IP for SSH).
- Keep the server OS updated (apply patches).
- Use non-root user in Docker containers (we didn’t explicitly set user in Dockerfile; could add a step to run as non-root for security).
- Use tools like Docker Bench for security to audit container config.
- In Nginx, implement rate limiting (to mitigate brute force on login or scraping).
- In Spring Boot, consider enabling security headers:
  - Spring Security by default adds some, like X-Content-Type-Options, X-XSS-Protection, etc.
  - When using our JWT config, ensure `.headers().frameOptions().disable()` only if using H2 console. Otherwise keep default frameOptions to DENY to avoid clickjacking.
  - Use Content-Security-Policy header from Nginx to restrict sources.

**Monitoring and Incident Response**:

- Set up CloudWatch alarms for unusual activity (e.g., sudden spike in 4xx or 5xx responses).
- Use AWS WAF (Web Application Firewall) on ALB/CloudFront to block common attack patterns (SQLi, XSS – AWS has managed rulesets).
- Regularly review logs (login failures, etc.) for suspicious activity.

### **10.2 Performance Tuning and Caching**

**Database Performance**:

- Ensure indexes on frequently queried fields:
  - We should index `contacts.user_id` (to speed up get user’s contacts).
  - Index on `contacts.name` if using LIKE queries might not fully utilize it unless we use prefix search. But an index still helps for filtering by exact matches or prefixes.
  - If adding filters for email or phone, index those if needed.
- Avoid N+1 query issue: If we fetch contacts and then access `contact.owner` lazily for each, JPA would issue a query per contact. In our JSON serialization it might happen. We might add `@JsonIgnore` on `Contact.owner` to avoid fetching it at all for JSON. Or use fetch join in queries if needed to batch.
- Use query tools or logs (`spring.jpa.show-sql=true` was on in dev) to identify slow queries and add indexes or optimize as needed.
- Connection pool: Spring Boot uses HikariCP by default, which is efficient. We might tune pool size if high concurrency (the default might be 10 connections; if expecting many concurrent requests, ensure enough DB connections in pool and that RDS can handle them).
- For read-heavy scenarios, consider caching frequently read data:
  - e.g., if many users share some contacts (not our model though).
  - Or caching the results of an expensive query in memory (Spring Cache + Ehcache or Caffeine). Not as relevant for simple contact queries but an example could be caching the list of all industries or something if we had that data static.

**Backend Performance**:

- Use asynchronous processing for non-critical tasks: e.g., sending an email on contact creation, we could do that asynchronously with `@Async` or using a message queue, so the user doesn’t wait on it.
- Ensure logging in production is at INFO or WARN level (not DEBUG) to avoid overhead.
- Use profiling or APM (Application Performance Monitoring) tools like New Relic, AppDynamics or Spring Boot Admin/Actuator to monitor performance.
- Garbage Collection tuning for JVM might be considered if memory is high usage. But default G1GC in Java 17 is usually fine for moderate loads.

**Frontend Performance**:

- The React build is already optimized (minified, bundled).
- Use code splitting if our app grows large: e.g., lazy load routes using React.lazy for pages that aren’t needed on initial load (maybe not needed for small app).
- Use a CDN (CloudFront) for static assets which we did, to reduce latency globally.
- Leverage browser caching: The build output has hashed filenames for assets, so they can be cached long-term (a year) since they change when content changes. Ensure proper cache headers (Nginx probably by default serves static with some caching; CloudFront can add cache-control as well).
- For API calls: consider client-side caching of data to avoid refetching unnecessarily. E.g., if user navigates away and back to contacts quickly, we could reuse the last loaded contacts (depending on freshness requirements).
- Use React performance tools to ensure not doing heavy computations in rendering. Our app is small, but for example, ensure large lists are virtualized if needed (e.g., thousands of contacts).
- If using Context extensively, be mindful of re-renders it causes. Our AuthContext is small, but if we had a context that triggers on every keystroke, that could slow things.

**Scaling**:

- We built the app to be stateless (the server doesn’t keep session state, JWT is stateless). This means we can run multiple backend instances behind a load balancer easily. If traffic grows, launch another EC2 or use ECS to run multiple tasks. The ALB will distribute traffic. Because no session stickiness needed (JWT is presented to any instance and works).
- For DB, vertical scaling (bigger instance) or read replicas for heavy read scenarios. Possibly caching layer like Redis if needed for certain data.
- Frontend on CloudFront can handle virtually unlimited scale.

**Load Testing**:

- Simulate load using tools like JMeter or k6. See how many requests per second the current setup handles.
- Monitor CPU and memory on EC2. If CPU high, consider scaling out/in. If memory issues, consider increasing memory or optimizing the app (e.g., memory leaks).
- Check database metrics (RDS CloudWatch): if high CPU or slow queries at load, optimize queries or add read replicas if mainly read load.

**Caching Strategy**:

- We could introduce a Redis cache for frequently accessed data. For example, if we had a dashboard showing some summary counts (like total contacts) that many users request often, caching that in Redis could reduce DB hits.
- Also, caching JWT verification public keys if using asymmetric JWT (not in our case, but in general).
- Spring Cache abstraction could be used on service methods. For instance:
  ```java
  @Cacheable("contactsByUser")
  public List<Contact> getContactsByUser(String username) { ... }
  ```
  This would cache the result for a given username in memory (Ehcache/Caffeine). It helps if user frequently refreshes page; but in our app, user data changes often (if they add/edit contacts, we’d need to evict cache on updates with `@CacheEvict`).
  We opted not to implement caching because the dataset for one user is not huge. But if it was large or expensive to compute, caching could help.

**Preventing Denial of Service (DoS)**:

- Rate limit APIs per IP or user. For instance, limit login attempts (to avoid brute force or credential stuffing).
- Use WAF to throttle or block IPs that make too many requests.
- Ensure resource usage per request is reasonable (our operations are relatively cheap).
- If expecting scrapers or misuse, introduce API keys or other mechanisms if this were a public API.

**Use of HTTP/2**:

- If using ALB/CloudFront, they support HTTP/2 which is more efficient for multiple requests (multiplexing).
- Ensure SSL is enabled to benefit from HTTP/2 (which requires TLS).

**SQL and Code Optimization**:

- Check if any heavy operation can be done more efficiently. E.g., if deleting many contacts, doing one by one could be slow; maybe provide a batch delete in SQL.
- If adding bulk import, use batch insert queries or bulk operations to be efficient (JPA’s saveAll or JDBC batch).
- Use `@Transactional` on service methods that do multiple DB operations to ensure they're done in one transaction and reduce overhead.

By following these security and optimization practices, we ensure the application is robust, secure, and performant:

- We secured against OWASP Top 10 vulnerabilities (injection, broken auth, XSS, etc.).
- We implemented proper access controls.
- We tuned performance at database, application, and delivery layers.
- We set up the foundation for scaling out if needed.

Continuous monitoring is key: using logs, metrics, and user feedback to identify any bottlenecks or vulnerabilities, and addressing them promptly via updates and patches.

_Exercise:_ Conduct a security audit of the application:

- Use OWASP ZAP (Zed Attack Proxy) to scan the running app for vulnerabilities.
- Try to perform a SQL injection via the REST API (e.g., put SQL wildcards or quotes in name search) to confirm it doesn’t break.
- Attempt XSS: add a contact with name `<script>alert('XSS')</script>` and see if alert triggers anywhere in UI (it shouldn’t, it should just show the literal string).
- If any issues are found, apply fixes (e.g., additional escaping, input validation).
- Also consider load testing: Use a tool to simulate 100 concurrent users listing contacts and measure response times. Tune DB or app accordingly.

By completing this, you’ll be confident that the system is ready for production use.

## 11. **Final Thoughts & Next Steps**

Congratulations on developing a full-stack Contact Management System! We have covered the architecture, implemented both backend and frontend, secured the application, added advanced features, tested it, and deployed it to a production environment. In this final section, we reflect on maintenance and suggest possible future enhancements to keep improving the system.

### **11.1 Maintenance and Updating the Application**

Maintaining a software project involves regular updates, monitoring, and improvements:

- **Bug Fixes**: Despite testing, users might encounter bugs. Establish a process to log bugs (using an issue tracker) and address them. Use semantic versioning for releases.
- **Dependency Updates**: Keep an eye on updates to React, Spring Boot, and other libraries:
  - Spring Boot releases regular updates including security patches (e.g., 3.x updates). Test and upgrade the backend dependencies periodically.
  - Same for React (though minor React updates usually not breaking, major version upgrades require testing).
  - Also update other dependencies like Spring Security, Axios, etc., to patch known vulnerabilities.
  - Use tools like Dependabot or Snyk to alert for vulnerable dependencies.
- **Database Maintenance**: As data grows, consider performance tuning (indexes, queries) and possibly archiving old data if needed.
- **Monitor Logs and Metrics**: Use monitoring to catch errors or performance issues in real time. For example, set up CloudWatch or ELK stack to aggregate logs. If you see many 500 errors or slow queries, act on them.
- **Scaling Infrastructure**: If usage grows, you might need to:
  - Scale up DB instance or move to a cluster.
  - Increase number of backend servers (ensure statelessness, which we did, so just add instances behind LB).
  - Perhaps container orchestration (ECS/Kubernetes) if managing many instances.
  - Implement a proper CI/CD if not already (we sketched one with GitHub Actions).
- **Documentation**: Maintain documentation for the system. For example:

  - API documentation (with Swagger UI or a README for endpoints).
  - Developer guide (how to set up dev environment, we essentially wrote one here).
  - User guide (for end users, how to use the app).
    Keeping docs updated will help new developers or operators of the system.

- **Security Monitoring**: Stay updated on security news (e.g., if a vulnerability is found in Spring, apply patches). Also, consider running periodic security scans (OWASP ZAP as mentioned, or code analysis tools).
- **Data Backup**: Ensure RDS backups are happening. Test restoring backups occasionally to ensure you can recover from data loss.
- **Uptime Monitoring**: Use a service or a simple cron to hit a health endpoint (like Spring Boot Actuator /health) to ensure the app is up, and alert if down.

The system should also have an accessible **health check**. Spring Boot Actuator can expose health and metrics endpoints (we could include `spring-boot-starter-actuator` to get /actuator/health, /actuator/metrics etc. and secure them behind auth or IP whitelist).

### **11.2 Future Enhancements and Features**

There are many possibilities to extend the Contact Management System. Depending on user needs, you might consider implementing:

- **User Interface Enhancements**:
  - A more sophisticated UI using component libraries (if not already). Perhaps drag-and-drop for reordering contacts or grouping them.
  - Adding profile pictures for contacts (file upload feature, storing images in S3).
  - Better mobile responsiveness or even a mobile app (React Native or a PWA).
  - A dashboard or analytics: e.g., show number of contacts added per month, etc.
- **Contact Sharing**:

  - Allow users to share contacts with others. This would involve a many-to-many between users and contacts (as suggested in an exercise, adjusting the data model).
  - Implement permissions: e.g., read-only share vs full-edit share.

- **Tagging and Grouping**:

  - We mentioned tags. Implementing a tag or category system helps users organize contacts.
  - Also grouping contacts into groups (like "Family", "Work"). This is similar to tags but hierarchical possibly.

- **Advanced Search**:

  - Use a search engine like Elasticsearch for full-text search across all fields (maybe even attachment search if contacts had attachments, etc.).
  - Or implement auto-suggest when typing in search (client-side filtering if dataset is small enough, or via an API endpoint that searches partial matches).

- **Integrations**:
  - Social media integration: e.g., fetch LinkedIn profile data for a contact via an API if available.
  - CRM integration: If this system needs to integrate with CRM systems like Salesforce, or Slack for notifications, etc.
  - Sync or import from Google Contacts or Outlook contacts. This is complex but possible with their APIs and OAuth flows.
- **Notifications**:

  - If this is multi-user (say an organization’s contacts system), allow notifying other users when a contact is updated or added (web push notifications or emails).
  - Reminders: e.g., set a reminder on a contact (like "follow up in 1 week") and send an email or app notification.

- **Multi-language support**:

  - Internationalize the frontend for multiple languages (using i18n libraries).
  - Ensure backend supports storing data in various charsets (which MySQL does by default with UTF-8).

- **Microservices**:

  - If the app grows, splitting into microservices could be considered: one service for contacts, one for user management, etc., with an API gateway. This helps independently scale and deploy parts.
  - Use Spring Cloud Netflix or Spring Cloud Gateway for routing, and possibly OAuth2 for authentication in a distributed system.

- **GraphQL API**:

  - Offer a GraphQL endpoint in addition to REST. GraphQL could allow clients to fetch exactly the data they want (for instance, a custom selection of contact fields or nested data in one request).
  - This would be an advanced feature and require adding a GraphQL library (like graphql-kickstart for Spring Boot).

- **Offline Mode**:

  - Make the web app a Progressive Web App (PWA) that can work offline. Cache contacts data in browser (IndexedDB) so user can view them offline, and sync changes when back online.
  - This would involve adding service worker, which CRA can do with a config to enable serviceWorker support.

- **Audit Logging**:

  - Keep an audit trail of changes: who added/edited/deleted contacts and when. This could be a separate table logging these events, or use an aspect to log changes.
  - Useful for compliance or just tracking usage.

- **Admin Tools**:

  - If you have admin users, build admin UI for them to manage all users, see all contacts, maybe remove inappropriate data, etc.
  - Also perhaps an admin setting to configure application (like turn registration on/off, etc.).

- **Testing Enhancements**:

  - Write more exhaustive tests, maybe integration tests with an actual browser (Selenium/Cypress for UI).
  - Set up a staging environment identical to production where new releases are tested with real deployment before production.

- **Alternative Frontend**:

  - Could create a mobile app (React Native or native iOS/Android) that uses the same backend API. The backend is already set up with JWT which mobile can handle similarly.
  - Or a desktop app (Electron) if needed.

- **Performance improvements**:
  - If contact list is huge (say thousands of entries), implement virtual scrolling so that rendering is efficient.
  - Partition database if data and users become very large (though likely unnecessary unless millions of contacts).
  - Implement request caching at the network level (CloudFront can cache GET /api/contacts if we set it, though with auth that gets tricky unless using something like key by Authorization header or moving to a stateless API key model).

Each new feature should be approached carefully:

- Update the design (ERD if database changes).
- Add necessary backend endpoints or modify existing.
- Ensure security implications of new feature are thought through (e.g., if sharing contacts, ensure one cannot access shares without permission).
- Write tests for new features.

One should also consider user feedback; often, real users will have ideas or pain points that can guide which enhancements are most valuable.

Finally, keep the system **simple and clean** where possible. It's easy for software to become complex as features pile on. Refactor periodically to improve code structure (e.g., if some service becomes too large with many responsibilities, split it).

**Conclusion**:
We embarked on building an advanced contact management system and covered the full development lifecycle using modern technologies:

- _Architecture_: Ensuring a scalable, tiered design.
- _Development_: Implementing each layer with best practices and clean code principles.
- _Security_: Integrating robust authentication/authorization and guarding against vulnerabilities.
- _Advanced capabilities_: Enhancing the system beyond CRUD to make it more usable and powerful.
- _Testing_: Verifying correctness and reliability through various testing methods.
- _Deployment_: Releasing the system in a reproducible and scalable manner on cloud infrastructure.
- _Maintenance_: Outlining how to keep the system healthy and iteratively improve it.

By following this guide, you as an advanced developer should be able to not only build this specific application but also apply these patterns and practices to similar full-stack projects. The key is understanding the interplay between frontend, backend, and database, and managing complexity through clear structure and robust tooling.

Good luck with your Contact Management System development, and happy coding!
