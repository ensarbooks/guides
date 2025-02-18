# **Full-Stack Application Guide: React Frontend & Spring Boot Backend**

This guide provides a comprehensive, step-by-step walkthrough for building, dockerizing, and deploying a full-stack application using **React** (frontend) and **Spring Boot** (backend). We will cover everything from initial project setup to production deployment on **Azure App Service** with CI/CD and best practices. The content is organized into the following sections:

1. **Project Setup** – Installing tools and initializing React and Spring Boot projects
2. **Development** – Building a basic UI and REST API with authentication, database integration, and testing
3. **Dockerization** – Writing Dockerfiles and using Docker Compose for local development, with image optimizations
4. **Infrastructure as Code (Terraform)** – Provisioning Azure resources (App Service, PostgreSQL, etc.) via Terraform scripts (and managing state)
5. **Deployment to Azure App Service** – Configuring and deploying both frontend and backend on Azure, plus environment variables, Azure Database, logging and monitoring
6. **CI/CD with GitHub Actions** – Automating build, test, and deployment for multiple environments (staging/production) with security checks and rollback strategies
7. **Best Practices & Optimization** – Ensuring security (HTTPS, auth, API gateway), performance (caching, CDN), observability (logging/monitoring), and cost optimizations on Azure

Each section contains headings, code snippets, and clearly delineated steps. Let’s begin!

## 1. **Project Setup**

Before writing any code, we need to set up our development environment with the necessary tools and initialize the frontend and backend projects.

### 1.1 **Install Necessary Tools**

To develop a React + Spring Boot application and containerize/deploy it, make sure the following tools are installed on your system:

- **Node.js and npm** – Required for building and running the React frontend. Install the latest LTS version (Node 18+). You can download Node.js from the official website and follow the installer instructions ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=1,if%20not%20already%20installed)). After installation, verify by running `node -v` and `npm -v` in a terminal.
- **Java Development Kit (JDK)** – Required to build and run Spring Boot (Java 17 or later is recommended ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=,or%20IDE))). Install OpenJDK 17 (or the latest LTS) from AdoptOpenJDK or Temurin, or use your OS package manager. Verify installation with `java -version`.
- **Spring Boot CLI (optional)** – A command-line tool to initialize and run Spring Boot apps quickly. This is optional but useful for quick prototyping ([9. Installing Spring Boot](https://docs.spring.io/spring-boot/docs/1.1.4.RELEASE/reference/html/getting-started-installing-spring-boot.html#:~:text=The%20Spring%20Boot%20CLI%20is,without%20so%20much%20boilerplate%20code)). You can install it via SDKMAN (`sdk install springboot`), Homebrew on macOS (`brew install springboot`), or by downloading the Spring Boot CLI zip from the Spring Initializr site ([Spring Boot CLI Setup and HelloWorld Example | DigitalOcean](https://www.digitalocean.com/community/tutorials/spring-boot-cli-setup-and-helloworld-example#:~:text=We%20can%20install%20Spring%20Boot,CLI%20software%20in%20Windows%20Environment)). Verify with `spring --version`.
- **Docker** – To containerize the app. Install Docker Desktop for your OS from the official Docker site ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=necessarily%20tied%20down%20to%20just,Java)). Verify with `docker --version`.
- **Terraform** – To provision infrastructure as code. Download Terraform from HashiCorp’s site or use a package manager ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=necessarily%20tied%20down%20to%20just,Java)). Verify with `terraform -v`.
- **Azure CLI** – To interact with Azure services from the command line (for deployment, managing resources, etc.) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=necessarily%20tied%20down%20to%20just,Java)). Install from Microsoft’s docs (the installer or via package manager) and verify with `az --version`. After installing, run `az login` to authenticate to your Azure account.

> **Note:** Ensure these tools are on your system PATH so that commands can be run from any directory. It’s also recommended to use a code editor or IDE (VS Code, IntelliJ IDEA, etc.) for development.

### 1.2 **Initialize a New React Project**

For the frontend, we’ll create a new React project. You have two popular options: using **Vite** (a fast modern build tool) or **Create React App (CRA)** (the classic way). In this guide, we’ll demonstrate using **Vite** for its speed and simplicity, but CRA can be used similarly.

**Using Vite:**

1. Open a terminal and navigate to the directory where you want your project.
2. Run the Vite scaffolding command via npm:
   ```bash
   npm create vite@latest my-app
   ```
   Replace "`my-app`" with your desired project name ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=Run%20the%20following%20command%20to,new%20React%20app%20using%20Vite)). This will prompt you for a framework – choose **React**, and then choose a variant (JavaScript or TypeScript). For example, select **React** and **JavaScript** when prompted ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=Once%2C%20enter%20this%20command%2C%20you,Select%20React)) ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=Next%2C%20select%20a%20variant%20of,JavaScript)). Vite will generate a new project in the `my-app` folder with the chosen configuration.
3. Change into the project directory:
   ```bash
   cd my-app
   ```
4. Install dependencies:
   ```bash
   npm install
   ```
   This will download all required packages listed in `package.json` ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=4)).
5. Start the development server:
   ```bash
   npm run dev
   ```
   This launches Vite’s dev server. Open the suggested URL (usually http://localhost:5173) in your browser to see the default React app running ([How to Create React App using Vite](https://www.javaguides.net/2023/06/how-to-create-react-app-using-vite.html#:~:text=5)).

The Vite project structure will include an `index.html`, a `src` directory with main React files (`main.jsx`, `App.jsx` or `.tsx` if TypeScript, etc.), and configuration files. We’ll customize these soon.

**Using Create React App (CRA) (Alternative):**

If you prefer CRA, you can run:

```bash
npx create-react-app my-app
```

This will create a similar React project (with a slightly different structure, using Webpack under the hood) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=npx%20create)). After creation, run `npm start` to launch the development server. The rest of the guide will be agnostic to how the app was created, so either approach works. (If using CRA, adjust build commands accordingly – e.g., `npm run build` outputs to a `build` directory, whereas Vite outputs to `dist`.)

### 1.3 **Initialize a New Spring Boot Project**

For the backend, we will create a Spring Boot project with REST API capabilities. The easiest way is to use **Spring Initializr**, which allows you to configure dependencies and generate a project.

**Using Spring Initializr (Web UI):**

1. Go to **start.spring.io** in your browser ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=1,of%20the%20setup%20for%20you)). This is the Spring Initializr interface.
2. Choose project settings: select **Maven** (or Gradle) project, **Java** language, and the Spring Boot version (use the latest stable version). Fill in group and artifact (e.g., Group: `com.example`, Artifact: `myapp-backend`). These will form your base package name.
3. Add dependencies: click “Add Dependencies” and select:
   - **Spring Web** – for building RESTful APIs (this brings in Spring MVC and an embedded Tomcat server) ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=2,assumes%20that%20you%20chose%20Java)).
   - **Spring Data JPA** – for database access via JPA/Hibernate.
   - **PostgreSQL Driver** (assuming we’ll use PostgreSQL; if using MySQL, add MySQL Driver instead).
   - **Spring Security** – for securing the API (needed for JWT/OAuth2 later).
   - (Optional) **Spring Boot DevTools** – for hot reloading during development.
   - You can also add **Lombok** (to reduce boilerplate) if desired.
4. Click **Generate** to download the project as a ZIP file ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=1,of%20the%20setup%20for%20you)). Unzip it to your desired location.

**Using Spring Boot CLI or Maven (Alternative):**

If you installed Spring Boot CLI, you could run a command to initialize a project. For example:

```bash
spring init --dependencies=web,data-jpa,postgresql,security --java-version=17 --build=maven myapp-backend
```

This would create a `myapp-backend` project with the specified dependencies and Java version. If not using the CLI, you can achieve the same with the Initializr web or by using curl (see Spring’s guide for using cURL to hit the Initializr API ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=1,of%20the%20setup%20for%20you))).

After generating the project, open it in your IDE. Notable files and structure:

- `src/main/java/.../Application.java` – The main class with `@SpringBootApplication` (entry point). Spring Initializr creates this for you. It contains a `main` method to run the app.
- `pom.xml` (or `build.gradle`) – The build file with dependencies and plugin configurations.
- Initially, no controllers or other classes exist yet – we will create those.

**Verify the Spring Boot app runs:** Open a terminal in the project directory and run the app:

- If using Maven: `./mvnw spring-boot:run` (or `mvn spring-boot:run` if Maven is installed).
- If using Gradle: `./gradlew bootRun`.
- Or run `Application.java` directly from your IDE.  
  This should start the Spring Boot application. By default, it will start on port 8080 and do nothing (no endpoints defined yet). You should see a banner and “Started Application in X seconds” in the console, indicating a successful launch.

We now have both projects initialized:

- **Frontend** (React) in the `my-app` directory (or your chosen name).
- **Backend** (Spring Boot) in `myapp-backend` (or chosen name).

In the next section, we’ll implement a basic functionality to ensure the frontend and backend can communicate.

## 2. **Development**

With our projects set up, we can start developing the application’s functionality. We’ll create a simple scenario: the React frontend will call a REST API from the Spring Boot backend. We will also configure Cross-Origin Resource Sharing (CORS) so the React app (running on localhost:3000 during development) can talk to the API (localhost:8080). Additionally, we’ll outline how to add authentication (using JWT or OAuth2) and connect the backend to a database (PostgreSQL). Finally, we’ll write basic tests for both frontend and backend to ensure our setup works correctly.

### 2.1 **Build a Basic React UI**

Open the React project in your editor. By default, Vite/CRA provides a template `App` component. We will modify this to call our backend API.

**Step 1: Configure a Proxy (Dev only)** – When running the dev server, you may want to proxy API calls to avoid CORS issues during development. If using Vite, you can configure a proxy in `vite.config.js`. If using CRA, add a `"proxy": "http://localhost:8080"` entry in `package.json`. This way, calls from the React dev server to `/api/...` will be forwarded to the backend on port 8080.

**Step 2: Create a UI for demonstration** – For example, we will create a simple component that fetches a greeting message from the backend and displays it.

In `src/App.jsx` (assuming JavaScript), replace the content with something like:

```jsx
import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    // Fetch a greeting from the backend API
    fetch("http://localhost:8080/api/hello")
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message); // assuming backend returns JSON { "message": "Hello, World!" }
      })
      .catch((err) => {
        console.error("API call failed:", err);
        setMessage("Error fetching message");
      });
  }, []);

  return (
    <div className="App">
      <h1>Greeting from Backend:</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
```

A few notes:

- We use `useEffect` to call the API on component mount (empty dependency array `[]` means it runs once on load).
- The fetch URL is pointing to `localhost:8080/api/hello`. In production, this URL will be different (and we might not hardcode it; we’ll handle that later). For development, ensure the backend runs on 8080 and the frontend can reach it.
- We handle JSON response and error case.
- We display the message or an error.

This simple UI will display “Loading...” initially, then update to whatever message the backend returns from `/api/hello`.

**Step 3: Run the React app** – Start the dev server (`npm run dev` for Vite or `npm start` for CRA). It should open your app at http://localhost:3000. If you visit now, the fetch will likely fail (because we haven’t created the API endpoint yet). But you can at least see the front-end is working. We will implement the backend next to complete the loop.

### 2.2 **Implement REST API Endpoints in Spring Boot**

Now, let’s create a REST API endpoint in the Spring Boot app to respond to the frontend’s request.

**Step 1: Create a REST Controller** – In the Spring Boot project (e.g., under `src/main/java/com/example/myapp`), create a class `HelloController` (or any name) with the `@RestController` annotation:

```java
package com.example.myapp.controller;  // choose appropriate package

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")  // base path for all endpoints in this controller
public class HelloController {

    @GetMapping("/hello")
    public Map<String, String> hello() {
        // Return a simple JSON response
        return Collections.singletonMap("message", "Hello, World!");
    }
}
```

Explanation:

- `@RestController` marks this class as a web controller where every method returns a domain object instead of a view. It implicitly adds `@ResponseBody` to all methods, so return values are serialized to JSON (assuming Jackson is on the classpath, which it is by default with Spring Web ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=package%20com)) ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=In%20Spring%E2%80%99s%20approach%20to%20building,class))).
- `@RequestMapping("/api")` sets a common prefix for routes in this controller (so our method will actually respond at `/api/hello`).
- The `hello()` method handles GET requests to `/api/hello` (`@GetMapping("/hello")`). It simply returns a Map with a “message” key. Spring Boot will convert this Map to JSON `{"message": "Hello, World!"}` automatically (because of Jackson JSON library included with Spring Web) ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=public%20record%20Greeting,)) ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=import%20org,RestController)).
- We use `Map<String,String>` for simplicity here. In a real app, you might return a proper DTO object.

**Step 2: Enable CORS for the API** – During development, our React app at localhost:3000 will call the API at localhost:8080. The domains differ, so the browser will enforce **CORS**. We need to allow the frontend’s origin. There are a few ways to enable CORS in Spring Boot:

- **Option 1: @CrossOrigin annotation** – We can annotate the controller or specific handler method with `@CrossOrigin` to allow requests from a given origin. For example, modify the controller class declaration:
  ```java
  @RestController
  @RequestMapping("/api")
  @CrossOrigin(origins = "http://localhost:3000")
  public class HelloController { ... }
  ```
  This will allow cross-origin GET requests from localhost:3000 to any endpoint in this controller ([Getting Started | Enabling Cross Origin Requests for a RESTful Web Service](https://spring.io/guides/gs/rest-service-cors#:~:text=private%20final%20AtomicLong%20counter%20%3D,format%28template%2C%20name%29%29%3B)). You could also put the annotation on individual methods if you want fine-grained control ([Getting Started | Enabling Cross Origin Requests for a RESTful Web Service](https://spring.io/guides/gs/rest-service-cors#:~:text=private%20static%20final%20String%20template,s)). For development, allowing the React dev server origin is sufficient.
- **Option 2: Global CORS configuration** – Alternatively, you can define a global CORS policy. For instance, add a config class:
  ```java
  import org.springframework.context.annotation.Bean;
  import org.springframework.web.servlet.config.annotation.CorsRegistry;
  import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
  // ...
  @Configuration
  public class WebConfig {
      @Bean
      public WebMvcConfigurer corsConfigurer() {
          return new WebMvcConfigurer() {
              @Override
              public void addCorsMappings(CorsRegistry registry) {
                  registry.addMapping("/api/**")
                          .allowedOrigins("http://localhost:3000")
                          .allowedMethods("GET","POST","PUT","DELETE","OPTIONS");
              }
          };
      }
  }
  ```
  This will allow the specified methods from the React origin for any endpoint under `/api/**`. Use this approach if you have many controllers and want a centralized configuration.

For now, using `@CrossOrigin` on `HelloController` is straightforward. Add the annotation and specify `origins = "http://localhost:3000"`. Now our `/api/hello` should be accessible from the React app in the browser.

**Step 3: Test the API and Integration** – Restart the Spring Boot application (stop and rerun it so that the new controller is picked up). Ensure it starts with no errors. With both the backend (on 8080) and frontend (on 3000) running, open the React app in a browser. You should see the message “Hello, World!” appear (fetched from the backend).

Open the browser’s developer console to verify the network request. The request to `http://localhost:8080/api/hello` should return a 200 OK with the JSON. If you see a CORS error, double-check the `@CrossOrigin` configuration. If it succeeded, congrats – you have a full-stack connection working!

We’ve built a minimal feature set. Next, we will enhance this by considering **authentication** and **database integration** in our application.

### 2.3 **Add Authentication (JWT/OAuth2)**

In many applications, you’ll want to secure the backend API so that only authorized users can access it. Two common approaches in modern architectures are **JWT (JSON Web Tokens)** and **OAuth2/OIDC** (using an external identity provider). Spring Boot makes it possible to implement either via Spring Security.

**Using JWT Authentication:**

JWT involves issuing a token to a client after verifying credentials, then the client attaches this token to subsequent requests (typically in the `Authorization: Bearer <token>` header). The backend validates the token on each request.

Basic steps to implement JWT in Spring Boot:

1. **Add Spring Security and JWT dependencies:** We already added Spring Security. We also need a JWT library (e.g., JJWT by io.jsonwebtoken). Ensure your `pom.xml` includes something like:
   ```xml
   <dependency>
     <groupId>io.jsonwebtoken</groupId>
     <artifactId>jjwt</artifactId>
     <version>0.9.1</version>  <!-- or the latest version -->
   </dependency>
   ```
   (Newer Spring Security might also support JWT via `spring-boot-starter-oauth2-resource-server` and properties, but using JJWT is a fine manual approach.)
2. **Configure Spring Security:** By default, Spring Security will lock down all endpoints. You need to define a security configuration that:
   - Permits the authentication endpoint (e.g., `/api/auth/login`) publicly.
   - Requires a valid JWT for other API endpoints.
   - Disables CSRF for APIs (since we’re using tokens, not cookies).
   - Enables CORS support in Spring Security (if using Spring Security 5+, add `.cors()` to the `HttpSecurity` config to allow our earlier CORS config to apply ([How to configure CORS in a Spring Boot + Spring Security ...](https://stackoverflow.com/questions/36968963/how-to-configure-cors-in-a-spring-boot-spring-security-application#:~:text=How%20to%20configure%20CORS%20in,will%20leverage%20Spring%20MVC))).
   - You may write a filter to parse and validate JWT from headers, or use Spring Security’s built-in support. For built-in, you can do something like:
     ```java
     @Configuration
     @EnableWebSecurity
     public class SecurityConfig extends WebSecurityConfigurerAdapter {
         @Override
         protected void configure(HttpSecurity http) throws Exception {
             http.csrf().disable();
             http.cors();  // enable CORS based on global config
             http.authorizeRequests()
                     .antMatchers("/api/auth/**").permitAll()   // open auth endpoints
                     .anyRequest().authenticated()             // secure all other endpoints
                     .and()
                     .addFilter(new JwtAuthenticationFilter(authenticationManager()))
                     .addFilter(new JwtAuthorizationFilter(authenticationManager()));
         }
         // ... define authenticationManager bean, etc.
     }
     ```
     Here, `JwtAuthenticationFilter` would be a custom filter handling login (validating user credentials and generating a token), and `JwtAuthorizationFilter` would validate the token on each request (setting security context if valid). This is a bit involved to code fully, but plenty of tutorials exist to guide you ([Spring Security JWT Tutorial | Toptal®](https://www.toptal.com/spring/spring-security-tutorial#:~:text=Spring%20Security%20JWT%20Tutorial%20,EnableWebSecurity%20annotation%20in%20our%20classpath)) ([Simplified Guide to JWT Authentication with Spring Boot - DEV Community](https://dev.to/abhi9720/a-comprehensive-guide-to-jwt-authentication-with-spring-boot-117p#:~:text=Securing%20your%20applications%20is%20paramount,to%20enhance%20your%20app%27s%20security)).
3. **Implement a Login endpoint:** Create an `AuthController` with a POST `/api/auth/login` that accepts user credentials (username/password). In a real app, you'd verify these against a database or external service. On success, generate a JWT (using JJWT, sign it with a secret key, include claims like username/roles, and set an expiration). Return the token to the client (usually in the response body or as a header).
4. **Implement token validation:** The `JwtAuthorizationFilter` (or equivalent) will intercept incoming requests, check for the `Authorization` header, parse the token using the same secret key, and if valid, allow the request to proceed with an authenticated principal. Otherwise, it rejects with 401 Unauthorized.
5. **Frontend changes:** The React app would need a login page/form. Upon successful login (probably via a call to `/api/auth/login` with credentials), store the returned JWT (typically in localStorage or a cookie). Then for subsequent API calls, include the token in headers. If using `fetch`, you can do:
   ```js
   fetch("/api/hello", {
     headers: { Authorization: "Bearer " + token },
   });
   ```
   The server will then authorize the request.

Spring Security + JWT can be complex, but it provides robust security. Many guides (e.g., from Okta, Baeldung, etc.) detail the exact implementation ([Simplified Guide to JWT Authentication with Spring Boot - DEV Community](https://dev.to/abhi9720/a-comprehensive-guide-to-jwt-authentication-with-spring-boot-117p#:~:text=Securing%20your%20applications%20is%20paramount,to%20enhance%20your%20app%27s%20security)) ([Simplified Guide to JWT Authentication with Spring Boot - DEV Community](https://dev.to/abhi9720/a-comprehensive-guide-to-jwt-authentication-with-spring-boot-117p#:~:text=%3C%21,%3Cdependency)). In summary, **JWT** gives a secure way to verify user identities with each request by using signed tokens.

**Using OAuth2 (Third-party or Azure AD):**

Alternatively, you could use OAuth2 and OpenID Connect if you want to offload authentication to an identity provider (like Google, Facebook, or Azure Active Directory). Spring Boot’s `spring-boot-starter-oauth2-client` and `oauth2-resource-server` can integrate with external providers. For instance, Azure AD can protect your API – you’d register the app in Azure, and the React frontend would acquire tokens from Azure AD (using MSAL library), then the backend (as resource server) would validate those tokens. This approach is more setup in Azure but provides centralized identity management.

For this guide, detail on OAuth2 is out of scope, but remember that **Spring Security** supports both JWT and OAuth2. **Choose JWT** for custom auth or **OAuth2** to use an external identity platform. In either case, ensure your application uses HTTPS in production (more on that later) to protect tokens in transit.

### 2.4 **Connect Spring Boot to a Database**

Most real applications need a database. We will use **PostgreSQL** as specified. The plan:

- Run a PostgreSQL database (locally for dev, and Azure DB for prod).
- Configure Spring Boot with the DB credentials.
- Use Spring Data JPA to interact with the database (define an entity and repository).

**Step 1: Set up a Dev Database:** Install PostgreSQL locally, or run one via Docker for development. For example, to run via Docker:

```bash
docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypass -e POSTGRES_DB=mydb -p 5432:5432 -d postgres:15-alpine
```

This starts a Postgres container on port 5432 with a database `mydb`. Note the username/password you set.

Alternatively, install Postgres on your machine and create a database and user.

**Step 2: Configure Spring Boot application.properties:** Open `src/main/resources/application.properties` (or .yml). Add the JDBC URL, username, and password for the database. For example:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=myuser
spring.datasource.password=mypass

spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

Let’s break this down:

- The `spring.datasource.url` points to your DB. Format: `jdbc:postgresql://<host>:5432/<database>`. Use `localhost` (or the container’s host) and the database name you created.
- Username and password as set when configuring the DB.
- `ddl-auto=update` tells Hibernate to automatically create/update database tables based on our entities. This is convenient in dev (it will create tables if they don’t exist, updating the schema as our entities change) ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=Add%20some%20elementary%20information%20in,auto%20property%20to%20update)) ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=spring,MySQL5Dialect)). In production, you might use `validate` or manage schema with migrations instead.
- The dialect is set to PostgreSQL explicitly. Hibernate can often pick it up, but it’s good practice to specify it ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=Hibernate%20has%20different%20dialects%20for,practice%20to%20specify%20it%20explicitly)). We use `PostgreSQLDialect`.

**Step 3: Create an Entity and Repository:** To test DB integration, let’s create a simple entity. For example, a `User` entity:

```java
// In src/main/java/com/example/myapp/model/User.java
package com.example.myapp.model;

import javax.persistence.*;

@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String name;
    private String email;
    // + constructors, getters, setters (or use Lombok @Data to generate)
}
```

This defines a `users` table with an auto-generated `id`, and `name` and `email` columns ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=Create%20a%20simple%20User%20entity,set%20the%20GenerationType%20to%20AUTO)) ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=private%20long%20id%3B%20private%20String,name%3B)).

Next, a repository interface to perform CRUD operations on `User`:

```java
// In src/main/java/com/example/myapp/repository/UserRepository.java
package com.example.myapp.repository;

import com.example.myapp.model.User;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends CrudRepository<User, Long> {
    // We get basic CRUD methods for User for free
}
```

By extending `CrudRepository`, Spring Data JPA will automatically provide implementations for common operations (save, findById, findAll, delete, etc.) ([Getting Started with Spring Boot REST API - Learn | Hevo](https://hevodata.com/learn/spring-boot-rest-api/#:~:text=Step%204%3A%20Creating%20Repository%20Classes)). The `@Repository` annotation is not strictly required (Spring will detect it via component scanning because it extends a Spring Data interface), but it’s a good marker.

**Step 4: Use the Repository (optional test):** We could create a service or command-line runner to test the database connection. For example, add a CommandLineRunner bean that saves a User and queries it:

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) { SpringApplication.run(Application.class, args); }

    @Bean
    CommandLineRunner initDatabase(UserRepository userRepo) {
        return args -> {
            User u = new User();
            u.setName("Test User");
            u.setEmail("test@example.com");
            userRepo.save(u);
            System.out.println("User count: " + userRepo.count());
        };
    }
}
```

When you run the app, it should print `User count: 1` on startup (and a new row in the `users` table). This confirms connectivity and that Hibernate created the table.

**Step 5: Create API endpoints for the Entity (optional):** You could add endpoints to the controller to create or retrieve users. For example, in `UserController`:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserRepository userRepo;

    @GetMapping
    public List<User> getAllUsers() {
        return (List<User>) userRepo.findAll();
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        return userRepo.save(user);
    }
}
```

This would allow fetching all users with GET `/api/users` and adding a new user with POST `/api/users` (with JSON body). For brevity, we won’t go deeper, but this shows how easily Spring Data JPA + Spring Boot let you build data-driven endpoints.

At this point, our Spring Boot application is connected to a database and can perform operations. In production, we will use **Azure Database for PostgreSQL**, but the code doesn’t change – just the connection URL and credentials will.

### 2.5 **Implement Testing for Frontend and Backend**

Testing is crucial for maintaining code quality. We’ll write basic tests for both the backend (using JUnit) and the frontend (using Jest and React Testing Library).

**Backend Testing (JUnit + Spring Test):**

Spring Boot supports tests with Spring’s testing framework and JUnit 5 by default. The Initializr project includes `spring-boot-starter-test` which brings in JUnit, AssertJ, Spring Test, etc.

- **Smoke Test the Context Load:** A simple test to start with is to ensure the Spring context loads without issues. You can create a test class in `src/test/java/...`:

  ```java
  import org.junit.jupiter.api.Test;
  import org.springframework.boot.test.context.SpringBootTest;

  @SpringBootTest
  class ApplicationTests {
      @Test
      void contextLoads() {
          // if the context fails to start, this test will fail
      }
  }
  ```

  This uses `@SpringBootTest` which will attempt to start the full application context for testing ([Getting Started | Testing the Web Layer](https://spring.io/guides/gs/testing-web#:~:text=%40SpringBootTest%20class%20TestingWebApplicationTests%20)). If any bean configuration is broken, this test will catch it. Running `mvn test` will execute this.

- **Controller Test (Web Layer):** We can test the API without starting the whole server by using Spring’s MockMvc. For example, test the hello endpoint:

  ```java
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
  import org.springframework.boot.test.context.SpringBootTest;
  import org.springframework.test.web.servlet.MockMvc;
  import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
  import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
  import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

  @SpringBootTest
  @AutoConfigureMockMvc
  class HelloControllerTest {
      @Autowired
      private MockMvc mockMvc;

      @Test
      void helloEndpointReturnsMessage() throws Exception {
          mockMvc.perform(get("/api/hello"))
                  .andExpect(status().isOk())
                  .andExpect(jsonPath("$.message").value("Hello, World!"));
      }
  }
  ```

  This test starts the context (with a random port by default due to MockMvc usage) and injects a `MockMvc` object ([Getting Started | Testing the Web Layer](https://spring.io/guides/gs/testing-web#:~:text=match%20at%20L357%20%40SpringBootTest%20%40AutoConfigureMockMvc,class%20TestingWebApplicationTest)). The test performs an HTTP GET request to `/api/hello` and expects a 200 OK and a JSON body with `{"message": "Hello, World!"}` (using JSONPath to verify the message). This ensures our controller is working as expected.

- **Repository/Service Tests:** For the data layer, you can use Spring’s testing support to, for example, use an in-memory DB for tests (or testcontainers for Postgres). But at minimum, you could test repository methods if any custom logic exists. Given `CrudRepository` is standard, not much to test there, but if you had a service method with business logic, you’d write unit tests for it (using mocks for the repository, possibly with Mockito).

Run tests with `mvn test`. All tests should pass if everything is configured correctly. You will see Spring Boot test context starting logs, and the results of assertions.

**Frontend Testing (Jest + React Testing Library):**

If you used CRA, Jest and React Testing Library are set up out of the box. If using Vite, you might use **Vitest** or configure Jest. For demonstration, we’ll assume a Jest environment (which is similar in both).

- **Component Test:** Write a test for a React component, e.g. for the App component, we can simulate it rendering and check initial state. Create a file `src/App.test.jsx`:

  ```jsx
  import { render, screen, waitFor } from "@testing-library/react";
  import App from "./App";

  beforeEach(() => {
    // Optionally, mock fetch for the test environment
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ message: "Hello, Test!" }),
      })
    );
  });

  test("renders greeting from backend", async () => {
    render(<App />);
    const heading = screen.getByText(/Greeting from Backend/i);
    expect(heading).toBeInTheDocument();

    // Wait for the state update after fetch
    await waitFor(() => {
      const messagePara = screen.getByText("Hello, Test!");
      expect(messagePara).toBeInTheDocument();
    });
  });
  ```

  In this test, we mock the `global.fetch` to return a preset value (`{ message: "Hello, Test!" }`) so that the component doesn’t actually call the real API. Then we render `<App />` using React Testing Library’s `render`. We check that the heading is present, and then wait for the asynchronous update of the paragraph to "Hello, Test!". The test passes if the component behaves correctly (initial render and state update after fetch).

- **Run frontend tests:** Use `npm test` (for CRA, it will run Jest in watch mode). The test should pass.

You can add more tests:

- Test that clicking a button triggers an API call (you can spy on `fetch`).
- Snapshot tests for UI components.
- Redux or context logic tests if you use those.
- For login logic (if implemented), test that entering correct credentials sets token, etc., perhaps by mocking API responses.

At this stage, we have a working application with a basic feature, proper CORS config, optional authentication scaffolding, database connectivity, and tests ensuring things work. Next, we will move to containerizing the application with Docker.

## 3. **Dockerization**

Dockerizing the application means packaging the frontend and backend into container images, so they can run anywhere consistently. We will create separate Docker images for the React frontend and the Spring Boot backend. Then we’ll use **Docker Compose** to run them together (including a database container for local dev). We will also apply best practices to optimize these images for production (using multi-stage builds to keep them small and efficient).

### 3.1 **Dockerfile for the Spring Boot Backend**

For the Spring Boot application, we want a Docker image that can run the Java application (the fat JAR). We can build the JAR using Maven/Gradle and then copy it into a lightweight image with a JRE. The ideal approach is a **multi-stage build**:

**Dockerfile (backend):**

Create a file named `Dockerfile` in the Spring Boot project directory (where pom.xml is). Add the following content:

```dockerfile
# Stage 1: Build the application
FROM maven:3-openjdk-17 AS builder
WORKDIR /app
COPY pom.xml .
# Optional: download dependencies (improves build cache usage)
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Run the application
FROM openjdk:17-jdk-slim
# Add a non-root user for security
RUN useradd -ms /bin/bash spring
USER spring

WORKDIR /app
# Copy only the built jar from the builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose port 8080 and set entrypoint
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

Let’s explain and justify some parts (with reference to best practices):

- We use an official Maven image (`maven:3-openjdk-17`) as the **builder stage**. This image has Maven and JDK, which we need to compile the code. We label it `AS builder`.
- We set a working directory and then copy the `pom.xml`. We run `mvn dependency:go-offline` which downloads all dependencies without building the project. This leverages Docker layer caching: if `pom.xml` hasn’t changed, Docker can cache the dependencies layer ([Dockerizing a Spring Boot Application: A Step-by-Step Guide | by Berkay Ozcan | Medium](https://medium.berkayozcan.com/dockerizing-a-spring-boot-application-a-step-by-step-guide-b0491b9e0c3d#:~:text=FROM%20maven%3A3)) ([Dockerizing a Spring Boot Application: A Step-by-Step Guide | by Berkay Ozcan | Medium](https://medium.berkayozcan.com/dockerizing-a-spring-boot-application-a-step-by-step-guide-b0491b9e0c3d#:~:text=RUN%20mvn%20clean%20package)). This speeds up iterative builds.
- Then we copy the source code and run `mvn package`. This produces the jar (in `target/*.jar`). We skip tests in the container build to save time (since we assume tests run in CI).
- The second stage starts from a **slim JDK image** (OpenJDK 17). Using a slim base keeps the image size down by excluding unnecessary OS packages.
- Security best practice: create a non-root user (`spring`) and switch to it ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=Running%20applications%20with%20user%20privileges,root%20user)). Running as non-root in the container limits impact of any container breach.
- Copy the jar built in stage1 into stage2 (we use the wildcard `*.jar` assuming only one jar, or adjust if multiple).
- Expose port 8080 (the app listens on 8080 by default).
- Set the entrypoint to run the jar with java. We name the jar `app.jar` inside the container and run it.

This multi-stage Dockerfile ensures the final image contains only the JDK runtime and our jar (no Maven, no source code, no .m2 repository), making it much smaller and secure ([Dockerizing a Spring Boot Application: A Step-by-Step Guide | by Berkay Ozcan | Medium](https://medium.berkayozcan.com/dockerizing-a-spring-boot-application-a-step-by-step-guide-b0491b9e0c3d#:~:text=This%20Dockerfile%20uses%20a%20multi,includes%20the%20necessary%20runtime%20components)). For example, using this method, you can get a Spring Boot image size down significantly (often ~200MB or less, depending on the app).

**Build and run (locally):** To test the Dockerfile, from the `myapp-backend` directory, run:

```bash
docker build -t myapp-backend:latest .
```

This will create the image (it will take a bit on first build, downloading Maven image and dependencies). Then run:

```bash
docker run -p 8080:8080 myapp-backend:latest
```

Access http://localhost:8080/api/hello to ensure it works inside the container.

### 3.2 **Dockerfile for the React Frontend**

For the React app, we also create a multi-stage Dockerfile. The goal is to **build the static files** (HTML, JS, CSS) with Node, then serve them with a lightweight web server (like Nginx) in production. In development, you might not dockerize the frontend (you’d use the dev server for hot-reload), but for production, containerizing the frontend is common.

**Dockerfile (frontend):**

In the React project folder, create a file `Dockerfile` with content:

```dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine
# Copy build output to Nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html
# If using CRA, the build output might be in /app/build instead of /app/dist
# Copy a custom nginx config if needed (optional)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Explanation:

- We use Node 18 Alpine as the builder. Alpine is a small Linux distro which keeps Node image size small. We copy the package.json and package-lock (using `package*.json` wildcard) and run `npm install` first – again, this is to leverage caching (dependencies rarely change compared to source code) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Copy%20package.json%20and%20package,json)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=COPY%20package,RUN%20npm%20run%20build)).
- Then copy the rest of the app code and run the build (`npm run build`). For Vite, this outputs to `dist` by default; for CRA, to `build`. Adjust accordingly.
- The second stage uses the official Nginx Alpine image. We copy the build output from the first stage into Nginx’s default content directory (`/usr/share/nginx/html`) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=FROM%20nginx%3Astable,g%22%2C%20%22daemon%20off)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)). This means Nginx will serve our React app’s static files.
- We expose port 80 (Nginx default HTTP port). The CMD runs Nginx in the foreground (as required in containers) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=FROM%20nginx%3Astable,g%22%2C%20%22daemon%20off)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)).
- Optionally, you could include a custom `nginx.conf` to set cache headers or do URL rewrites (for single-page app routing). For example, copying a file into `/etc/nginx/conf.d/default.conf` to handle React Router routes by always returning `index.html`. But for now, default is okay if our app doesn’t have client-side routing beyond root.

Build the frontend image with:

```bash
docker build -t myapp-frontend:latest .
```

in the React project directory. Then run:

```bash
docker run -p 3000:80 myapp-frontend:latest
```

and visit http://localhost:3000. You should see the React app being served by Nginx. The API calls in the React app will fail unless it’s pointing to a running backend. In a combined environment, we’ll network them – that’s where Docker Compose comes in.

**Production image optimizations benefits:** By using multi-stage builds for the React app:

- We don’t include the Node.js runtime in the final image, only Nginx and static files. This greatly **reduces the attack surface and image size** (Node and build tools are not present in the runtime image) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)).
- The image is smaller and contains only what’s needed to serve the app, which improves startup time and security ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Nginx%20efficiently%20serves%20static%20files)).
- Nginx is very efficient at serving static files, outperforming a Node server for this purpose.

### 3.3 **Docker Compose for Multi-Container Setup**

For local development and testing of the full stack, Docker Compose is invaluable. It allows us to define multiple services (frontend, backend, database) and their relationships (networking, environment variables, volumes, etc.) in one YAML file and start them with a single command.

Create a file `docker-compose.yml` at the root of your project (you can also have it in a separate infra directory if you prefer):

```yaml
version: "3"
services:
  backend:
    build:
      context: ./myapp-backend # path to backend Dockerfile
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/mydb
      - SPRING_DATASOURCE_USERNAME=myuser
      - SPRING_DATASOURCE_PASSWORD=mypass
      - SPRING_JPA_HIBERNATE_DDL_AUTO=update
      # If using any other env vars like JWT secret or OAuth config, set them here
    depends_on:
      - db

  frontend:
    build:
      context: ./my-app # path to frontend Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypass
      - POSTGRES_DB=mydb
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db-data:
```

In this compose file:

- We define three services: **backend**, **frontend**, and **db**.
- **backend**:
  - `build.context` points to the directory containing the backend’s Dockerfile (update the path accordingly to where your backend code is).
  - We map port 8080 of the container to 8080 on the host, so we can call the API directly if needed.
  - We set environment variables for the Spring Boot app: these override values in `application.properties`. We point the datasource URL to `db:5432/mydb`. In Docker Compose, all services are networked by default, and each can reach others by the service name. So the hostname `db` will resolve to the Postgres container’s IP. We supply the same credentials as set for the db service.
  - We also include `SPRING_JPA_HIBERNATE_DDL_AUTO=update` just to ensure the schema will auto-create on first run (since we might be running a fresh Postgres with empty data volume).
  - `depends_on: db` ensures Docker starts the db service before the backend (though it doesn’t wait for DB to be ready, Spring Boot will retry a few times by default if DB isn’t up immediately).
- **frontend**:
  - Similarly built from context `./my-app` (adjust if your folder name is different).
  - We map port 3000 on host to 80 in container (Nginx). So http://localhost:3000 will hit the React app served by Nginx.
  - `depends_on: backend` ensures backend is up first. (The frontend might try to call API on startup; if backend isn’t ready, it will retry on fetch or show error until backend comes up.)
  - We did not explicitly link any environment variables here. If the React app needs to know the API URL, one approach is to bake it in at build time (e.g., using an environment variable when running `npm run build`). Another approach is to have the front and back on the same domain in production (which we will, on Azure, perhaps using relative paths or a reverse proxy). For dev, we might just call `localhost:8080`. In container, `localhost:8080` from the browser won’t work (since the browser is on host machine hitting the frontend container). To address this in dev environment: one could configure the React app to call `http://localhost:8080` (which works since our compose maps 8080 to host) or use the Nginx to proxy to the backend container. A simpler solution: change the fetch in React to `/api/hello` (relative path) and configure Nginx to forward `/api` to the backend. But that requires custom Nginx config. For now, using the host mapping is okay (since both 8080 and 3000 are mapped to host, the front-end in browser can reach backend via host).
- **db**:
  - Uses official Postgres image.
  - We set the environment for user, password, db name.
  - A volume `db-data` is attached to persist data between container restarts (so your dev data isn’t lost).
  - Ports mapping "5432:5432" is optional for local development if you want to connect with a DB client from host. The backend container can reach the DB without this because of internal networking.
- `volumes` defines a named volume `db-data` so Docker Compose will manage a persistent volume for Postgres data.

To start everything, run:

```bash
docker-compose up --build
```

The `--build` flag builds images if not already built. Compose will then start all services. You will see logs from all three (in one intertwined stream; you can also use `docker-compose up -d` to run in background). Watch for:

- Postgres start log (it should initialize and say it’s ready to accept connections).
- Spring Boot logs (it will attempt to connect to DB, apply any schema changes, then start the web server on 8080).
- Nginx logs (should be minimal, basically it’s ready).

Once up, test the integration:

- Open http://localhost:3000 in your browser. This hits the Nginx-served React app.
- The React app will try to fetch the greeting. If configured correctly (and backend is reachable), it should display the message from backend.
- Alternatively, directly test the backend: http://localhost:8080/api/hello should return JSON greeting.

If any container crashes, check its logs:

```bash
docker-compose logs backend   # or frontend, or db
```

Common issues: backend can’t connect to DB (check env vars, network), port conflicts on host (ensure nothing else using 3000 or 8080).

**Iterating during development:**

- You might not want to rebuild the image on every code change when actively developing. Typically, for Spring Boot you’d rely on hot reload on host (DevTools) and for React you use its dev server. Docker is more for consistent env and deployment. One approach is to use Compose with volumes to mount code inside container and rerun (but configuring that is complex for multi-stage builds).
- Many developers run backend on host (via IDE) and frontend dev server on host for rapid dev, using Compose mainly to spin up dependent services (like Postgres or Redis). And then use Docker for final testing and deployment. Choose a workflow that fits your needs.

### 3.4 **Optimize Docker Images for Production**

We already employed several optimization techniques in the Dockerfiles:

- **Multi-stage builds** to separate build-time and run-time, resulting in smaller images ([Dockerizing a Spring Boot Application: A Step-by-Step Guide | by Berkay Ozcan | Medium](https://medium.berkayozcan.com/dockerizing-a-spring-boot-application-a-step-by-step-guide-b0491b9e0c3d#:~:text=This%20Dockerfile%20uses%20a%20multi,includes%20the%20necessary%20runtime%20components)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)).
- Using **Alpine** base images for Node and Nginx to reduce image size.
- Running as **non-root** in the backend container for security ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=Running%20applications%20with%20user%20privileges,root%20user)).
- Copying only necessary artifacts (jar or build directory) into final image.

Additional optimizations to consider:

- **Dockerignore:** Create a `.dockerignore` file to exclude files that shouldn’t be sent to Docker build context. For example, in the backend, ignore `target/` (except the jar if needed in multi-stage), `.git`, etc. In frontend, ignore `node_modules` (as they’ll be installed inside Docker) and `dist` (which will be generated in build stage). This reduces build context size and speeds up builds.
- **Layer caching:** Order instructions in Dockerfile from least likely to change to most likely to change. We did this by copying `pom.xml` and running `npm install` before adding the rest of code, so dependency installation can be cached.
- **Minimize layers:** Each `RUN` in Dockerfile adds a layer. We combined some when logical (though readability sometimes trumps minimal layers). For instance, in backend, we could combine adding user and switching user in one layer.
- **Use JRE instead of JDK in final image:** We used `openjdk:17-jdk-slim`. We could use a JRE (runtime only) image or even a distroless Java image for even smaller footprint. OpenJDK has `17-jdk-slim` vs `17-jre-slim`. The jre variant excludes compiler and other dev tools. If available, prefer JRE.
- **Enable Java container optimizations:** Newer Spring Boot versions can create layered jars, which can be used with tools like Jib or Buildpacks to optimize Docker image layers. We won't delve into that, but it’s something to explore for production (the Spring Boot Maven plugin’s `build-image` goal can build an optimized container image as well).
- **Resource limits:** Not in Dockerfile, but in Kubernetes or Compose you can restrict CPU/memory for containers. For App Service, we’ll allocate via plan size.
- **Healthchecks:** You can add `HEALTHCHECK` in Dockerfile to automatically check container health (e.g., curl the `/actuator/health` endpoint if available). This helps orchestrators (like Kubernetes or Azure) know if container is unhealthy and restart it.
- **Logging to stdout/stderr:** We already by default have Spring Boot logging to console, and Nginx logs to stdout; this is good for container environments so logs can be collected by Docker/host.

By applying these optimizations, our images are **production-ready**: small, secure, and efficient. For example, the multi-stage Dockerfile for React yields an image that contains only static files and Nginx, leaving out Node runtime ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)). Similarly, the backend image contains just the JDK and our app. These optimizations reduce cold-start times and storage costs and improve security by excluding build tools from the runtime image.

Now that our application can run in containers, the next step is to prepare infrastructure on Azure to host these containers. We will use Terraform to script the creation of Azure resources.

## 4. **Infrastructure as Code (Terraform)**

To deploy our application in the cloud, we need to provision resources like Azure App Services (for hosting the containers), an Azure Database for PostgreSQL, networking configurations, and possibly storage for static files or Terraform state. **Terraform** allows us to define these resources declaratively and manage them as code.

Using Infrastructure as Code (IaC) has many benefits: consistent environments, easy provisioning and teardown, and version control for infrastructure changes. We will write Terraform configurations to set up everything required on Azure. We will also configure remote state management for Terraform (to safely store the state file in Azure Storage). Finally, we will see how to run the Terraform scripts to deploy the infrastructure.

### 4.1 **Terraform Project Setup**

First, ensure Terraform is installed (we did this in section 1.1). Decide on a structure: you can create a directory (e.g., `infra/terraform`) in your project to store Terraform files. We’ll create a main configuration file `main.tf` and possibly separate files for variables and outputs (optional for clarity).

**Configure the Azure provider and state backend:**

In `main.tf`, start by specifying the Azure provider and backend:

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"  # use latest version
    }
  }
  backend "azurerm" {
    resource_group_name  = "myapp-terraform-rg"
    storage_account_name = "myappstatestore"
    container_name       = "tfstate"
    key                  = "infrastructure.tfstate"
  }
}

provider "azurerm" {
  features {}  # enable default features
}
```

Explanation:

- We declare the use of the **AzureRM provider** (HashiCorp’s official Azure provider). Version 3.x is current.
- The `backend "azurerm"` block configures remote state storage in Azure ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=terraform%20,storage_account_name)) ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=container_name%20%20%20%20,)). This means our Terraform state (which tracks deployed resources) will be stored in an Azure Storage Account instead of locally. We need to specify the resource group, storage account, container, and key (file name) for the state. **Note:** The storage account and resource group themselves need to exist. We have a chicken-and-egg situation: we could manually create this RG and storage account first (one-time) or use Terraform itself (with local state for just that creation). A simple approach: create an Azure Storage account via Azure Portal or CLI beforehand for state. Alternatively, run Terraform twice: once to make the storage and then enable remote backend. Due to complexity, many will create the backend resources outside of Terraform.
- The provider `azurerm` requires authentication. Since we have Azure CLI, Terraform can reuse that if you do `az login` (it picks up CLI auth). Or you can configure a service principal. For simplicity, ensure you’re logged in with Azure CLI to the correct subscription before running Terraform.

**Define Variables (Optional):** We can parameterize some values like region, prefix for names, etc. For clarity, we'll inline values or use local variables in code below. In real use, consider using `variables.tf` for things like location, environment name, etc., and a `terraform.tfvars` for sensitive info (though secret management is better via Azure Key Vault integration or environment variables).

### 4.2 **Terraform: Azure Resource Definitions**

Now let’s define the Azure resources needed:

- Resource Group
- Container Registry (optional, if using for storing images)
- App Service Plan
- App Service (Web App) for backend
- App Service for frontend (or we might use static site, but per requirements, using App Service)
- Azure Database for PostgreSQL
- Networking (maybe allowing connectivity between App Service and DB)
- Storage Account (for state, if not created outside, and possibly for other use like storing assets or logs)

We’ll create a single Resource Group to contain all resources for this application.

**Resource Group:**

```hcl
resource "azurerm_resource_group" "app" {
  name     = "myapp-prod-rg"
  location = "East US"  # choose a region close to you or required by business
}
```

This creates a resource group named "myapp-prod-rg". (Use a naming convention, maybe include environment if needed.)

**Azure Container Registry (ACR) (optional):**

If we plan to push our Docker images to a private registry, Azure Container Registry is a good choice. Azure App Service can pull images from ACR. Alternatively, we could use Docker Hub, but ACR integration is seamless (especially with managed identities). Let’s include ACR:

```hcl
resource "azurerm_container_registry" "acr" {
  name                     = "myappacr2025"    # globally unique name
  resource_group_name      = azurerm_resource_group.app.name
  location                 = azurerm_resource_group.app.location
  sku                      = "Basic"           # Basic SKU is cost-effective for small apps
  admin_enabled            = false             # disable admin user for security (we'll use SP or managed identity)
}
```

We set `admin_enabled = false` to avoid using the admin username/password for the registry; we will instead give the Web App access to pull (discussed later). The name must be unique across Azure (like DNS name). Basic SKU is fine for a few images and moderate usage.

**App Service Plan:**

This defines the underlying VM plan for the App Services. Since we plan to run Linux containers, we need a **Linux Plan**. We can decide the size (pricing tier). For production, at least a `B1` (Basic) or `S1` (Standard) might be used. If minimal cost is needed and performance is not critical, a free or shared tier could work for very low usage (but free tier doesn’t support custom domains or always-on).

```hcl
resource "azurerm_app_service_plan" "plan" {
  name                = "myapp-plan"
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  kind                = "Linux"
  reserved            = true   # this flag indicates a Linux container plan
  sku {
    tier = "Basic"
    size = "B1"
  }
}
```

We chose a Basic B1 plan (1 CPU, 1.75 GB RAM). `reserved = true` with `kind = "Linux"` ensures it’s a Linux App Service Plan ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=,%3D%20true)) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=tier%20%3D%20,%7D)).

**App Service (Backend):**

```hcl
resource "azurerm_web_app" "backend" {
  name                = "myapp-backend"
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  app_service_plan_id = azurerm_app_service_plan.plan.id

  site_config {
    linux_fx_version = "DOCKER|myappacr2025.azurecr.io/myapp-backend:latest"
    # The format for linux_fx_version is "DOCKER|<registry>/<image>:<tag>"
    # If using Docker Hub public image, use "DOCKER|username/image:tag"
    # If using a private registry, we add app settings for creds below.
    always_on        = true  # keep the app running (no idle unload, important for background tasks or faster cold start)
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"  # not mounting Azure storage as persistent storage in container
    "DOCKER_REGISTRY_SERVER_URL"          = azurerm_container_registry.acr.login_server  # ACR login URL, e.g., https://myappacr2025.azurecr.io
    # If not using managed identity for ACR, also set DOCKER_REGISTRY_SERVER_USERNAME and DOCKER_REGISTRY_SERVER_PASSWORD from ACR credentials (admin must be enabled for that).
    # For connecting to PostgreSQL, set connection string or use environment as below:
    "SPRING_DATASOURCE_URL"      = "jdbc:postgresql://${azurerm_postgresql_flexible_server.db.fqdn}:5432/${azurerm_postgresql_flexible_server.db.database_name}?sslmode=require"
    "SPRING_DATASOURCE_USERNAME" = "${azurerm_postgresql_flexible_server.db.administrator_login}@${azurerm_postgresql_flexible_server.db.name}"
    "SPRING_DATASOURCE_PASSWORD" = azurerm_postgresql_flexible_server.db.administrator_login_password
    "SPRING_JPA_HIBERNATE_DDL_AUTO" = "update"
    # Include any other env vars needed, e.g., JWT secrets or OAuth settings
  }

  identity {
    type = "SystemAssigned"
  }
}
```

Let’s break it down:

- We use `azurerm_web_app` (the newer resource type name for App Services in Terraform) for a Web App on Linux ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=,azurerm_app_service_plan.main.id)).
- `linux_fx_version` is a critical setting: it specifies the Docker image for the Web App. We set it to our ACR image. The format is `"DOCKER|<registry-url>/<image>:<tag>"` ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=site_config%20%7B%20app_command_line%20%3D%20,%3D%20true)). We are using `latest` tag here for simplicity – in real CI/CD, you might use versioned tags or use “:latest” to always pick the latest push (but then triggering a restart is needed). If you prefer not to use ACR, you could put a Docker Hub image name here.
- `always_on = true` keeps the app always running, which is recommended for production (especially if using background jobs or to avoid cold starts).
- We add `app_settings` which are environment variables for the app:
  - `WEBSITES_ENABLE_APP_SERVICE_STORAGE=false` is recommended when running containers on App Service to not use the legacy persistent storage binding (not needed since our container is self-contained) ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=app_settings%20%3D%20%7B%20,https%3A%2F%2Findex.docker.io)).
  - `DOCKER_REGISTRY_SERVER_URL` points to the registry. For ACR, this is `https://<name>.azurecr.io`. We inject it via Terraform using the `login_server` attribute of ACR.
  - If ACR’s admin user is disabled (as we did), we need another way for the Web App to authenticate to pull the image. One way: set `azurerm_web_app.backend.identity` to give the app a **Managed Identity** (which we did with `identity { type = "SystemAssigned" }`). Then, on ACR, assign the role `AcrPull` to that identity, so the Web App can pull images securely without storing credentials. Terraform can manage that role assignment too (using `azurerm_role_assignment` resource, linking the web app’s principal ID to the ACR resource). For brevity, assume we’ll do that:
    ```hcl
    resource "azurerm_role_assignment" "acr_pull" {
      scope                = azurerm_container_registry.acr.id
      role_definition_name = "AcrPull"
      principal_id         = azurerm_web_app.backend.identity.principal_id
    }
    ```
    This grants the managed identity permission to pull from ACR.
  - If not using managed identity, an alternative is enabling ACR admin user and setting `DOCKER_REGISTRY_SERVER_USERNAME` and `DOCKER_REGISTRY_SERVER_PASSWORD` in app_settings (fetching them from ACR resource outputs or as secret variables). We aim for the more secure managed identity approach.
  - **Database settings:** We pass the JDBC URL, username, and password as environment variables. `azurerm_postgresql_flexible_server.db.fqdn` gives the fully qualified domain name of the Postgres server (e.g., `<name>.postgres.database.azure.com`). We include `sslmode=require` in the URL to enforce SSL as Azure requires by default. The username in Azure Postgres is typically formatted as `<admin_login>@<server_name>` when connecting ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=,)). The Terraform resource provides `administrator_login` and the server name, which we use to construct the full username. We stored the password in Terraform state (not ideal for security to keep plaintext, but we can use Terraform variables with sensitive flag or Azure Key Vault integration to avoid plaintext in code).
  - You might also include `SPRING_PROFILES_ACTIVE=prod` or other Spring Boot settings to switch to production profile if you have one.
- The `identity { type = "SystemAssigned" }` block instructs Azure to create a Managed Identity for this Web App ([[NoBrainer] Deploy a Spring Boot Application to an Azure App Service – blog.rufer.be](https://blog.rufer.be/2022/10/26/nobrainer-deploy-a-spring-boot-application-to-an-azure-app-service/#:~:text=again%20impressed%20by%20Azure%20%E2%80%93,commit%20to%20the%20selected%20branch)). We use it for ACR as discussed, and we can also use it to access other Azure resources (like Key Vault for secrets) if needed later.

**App Service (Frontend):**

We’ll create another Web App for the React frontend. Alternatively, one might consider using Azure Static Web Apps or an Azure CDN + storage for static site, but given the request is to use App Service, we’ll proceed similarly to backend.

```hcl
resource "azurerm_web_app" "frontend" {
  name                = "myapp-frontend"
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  app_service_plan_id = azurerm_app_service_plan.plan.id

  site_config {
    linux_fx_version = "DOCKER|myappacr2025.azurecr.io/myapp-frontend:latest"
    always_on        = true
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = azurerm_container_registry.acr.login_server
    # Frontend might not need many env vars, but we can pass API URL if needed
    # e.g., "REACT_APP_API_URL" = "https://${azurerm_web_app.backend.default_hostname}/api"
  }

  identity {
    type = "SystemAssigned"
  }
}
```

- We point this Web App to the frontend image in ACR (myapp-frontend:latest).
- Also use managed identity for ACR pull (and similarly assign `AcrPull` role to this identity).
- We include an example of passing an environment variable to the React app: If our React code is set up to read `REACT_APP_API_URL` (Create React App exposes env vars prefixed with REACT_APP), we could set it to the backend’s URL. Azure Web Apps have a default hostname like `myapp-backend.azurewebsites.net`. If both front and back are in the same App Service Plan and region, you could also set up a private environment or VNet, but likely they are just accessible over the internet. We might decide to call the API by its public URL (with HTTPS). In production, consider fronting both with a single domain or Azure Front Door, but that’s beyond scope here. For now, maybe set `REACT_APP_API_URL = "https://myapp-backend.azurewebsites.net/api"` in the frontend’s settings. (We can get `default_hostname` from the backend resource, which yields something like `myapp-backend.azurewebsites.net` ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=output%20,)).)
- Setting "always_on" for front-end isn't strictly necessary (since it’s just serving static files on request), but it’s fine.

**Azure Database for PostgreSQL:**

Azure offers “Flexible Server” and “Single Server” for Postgres. Flexible Server is the newer offering. We’ll use that. We need to create:

- The PostgreSQL server
- A database (the flexible server comes with the default db, but we can create additional if needed)
- Configuration like firewall rules to allow the App Service to connect.

```hcl
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "myapp-db"
  resource_group_name    = azurerm_resource_group.app.name
  location               = azurerm_resource_group.app.location
  version                = "14"  # PostgreSQL version
  administrator_login    = "dbadmin"  # choose admin name
  administrator_password = "P@ssw0rd1234"  # strong password, in real use get from secure source
  storage_mb             = 32768  # 32 GB storage
  sku_name               = "B_1_1" # Burstable 1 vCPU, 1 GiB (small)
  # By default, flexible server is created in a VNet. We can create a public one by specifying network.
  public_network_access_enabled = true
  # We will add firewall rules below to allow Azure services or specific access.
}
```

This creates a Postgres flexible server. Important settings:

- `public_network_access_enabled = true` means it will have a public endpoint. Alternatively, one could set up VNet integration. Here, for simplicity and since App Service can access it publicly, we allow public access but will restrict by firewall.
- `sku_name` picks a performance tier. We chose a basic burstable (B1) instance. Adjust as needed for production load.
- Credentials: These are sensitive. In production, consider not hardcoding the password in Terraform files that might be in source control. You can use Terraform variables and supply the password via command line or store it in something like Azure Key Vault (Terraform can retrieve secrets from key vault if configured). For demonstration, we show it in code.

**PostgreSQL Database and Firewall:**

Terraform `azurerm_postgresql_flexible_server` automatically creates a default database named "postgres". We might want a specific database for our app:

```hcl
resource "azurerm_postgresql_flexible_database" "appdb" {
  name                = "myappdb"
  resource_group_name = azurerm_resource_group.app.name
  server_name         = azurerm_postgresql_flexible_server.db.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}
```

This creates a database `myappdb`. In our Spring config above, we used `${azurerm_postgresql_flexible_server.db.database_name}` which refers to the default (likely "postgres"). We should update the Spring env to use `myappdb` or ensure `database_name` attribute picks up this one (the flexible server resource might allow specifying database_name, but documentation suggests it’s for initial db). Alternatively, we set `SPRING_DATASOURCE_URL` to use `myappdb`. For clarity, let's adjust the env:

```hcl
"SPRING_DATASOURCE_URL" = "jdbc:postgresql://${azurerm_postgresql_flexible_server.db.fqdn}:5432/myappdb?sslmode=require"
```

And we won't use `database_name` in that context.

Now firewall rules. By default, even with public access, flexible server requires setting rules to allow connections. We have two things to allow:

- The App Service outbound IPs (which can be dynamic or multiple)
- Or a broad approach: allow all Azure services (including App Service) by using the special 0.0.0.0 address rule (Azure’s shorthand for “Allow Azure”).

For simplicity:

```hcl
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name                = "AllowAzureServices"
  resource_group_name = azurerm_resource_group.app.name
  server_name         = azurerm_postgresql_flexible_server.db.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
```

This rule ([Deploy a web app to Azure App Service using Terraform | Technorage](https://deepu.tech/deploy-a-web-app-to-azure-app-service-using-terraform#:~:text=,)) allows all Azure IPs to connect, which includes App Service since it comes from Azure datacenters. This is easiest but a bit open (any Azure resource in any tenant could technically connect, though the DB still needs correct credentials). A more secure way is to specifically allow the outbound addresses of your Web App, but App Service can have multiple and can change on scaling. Using VNet integration is the more secure approach (then you’d create a VNet, place the DB in that VNet and integrate the web app with the VNet). Given time, we stick with the broad allow Azure.

We could also allow our local IP for admin access if needed (for connecting with psql for debugging). Example:

```hcl
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_my_ip" {
  name                = "AllowHomeIP"
  resource_group_name = azurerm_resource_group.app.name
  server_name         = azurerm_postgresql_flexible_server.db.name
  start_ip_address    = "X.Y.Z.W"
  end_ip_address      = "X.Y.Z.W"
}
```

Replace X.Y.Z.W with your public IP (or use a data source to fetch it dynamically).

Now we have DB server, DB, firewall open to Azure. The credentials (admin user `dbadmin` and password) we used are set in the web app env so Spring Boot can connect.

**Storage Account (for Terraform state or assets):**

We mentioned using Azure storage for Terraform state in the backend config. The config references a RG `myapp-terraform-rg` and account `myappstatestore`. We should create those as well if not done externally. They could even be in the same `myapp-prod-rg` to avoid an extra RG.

For clarity, let’s create them here (although normally backend config should reference an existing storage, you can actually have Terraform create its own backend by doing partial apply).
We might do:

```hcl
# Create storage account for state (in separate RG to avoid deletion when main RG is destroyed, to preserve state)
resource "azurerm_resource_group" "tfstate" {
  name     = "myapp-terraform-rg"
  location = azurerm_resource_group.app.location
}
resource "azurerm_storage_account" "tfstate" {
  name                     = "myappstatestore"  # must be globally unique, all lowercase, 3-24 characters
  resource_group_name      = azurerm_resource_group.tfstate.name
  location                 = azurerm_resource_group.app.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}
```

This sets up the storage. However, using it as backend means we have a chicken-egg (Terraform wants to init backend before applying). One workaround: apply once with local state just for storage resources, then enable backend and reinitialize. Given complexity, let's assume we manually created these outside of Terraform. In practice, that’s often done (set up a remote state storage by other means).

**Outputs (optional):**

We might output some useful info like the backend URL or DB host after apply:

```hcl
output "backend_url" {
  value = "https://${azurerm_web_app.backend.default_hostname}"
}
output "frontend_url" {
  value = "https://${azurerm_web_app.frontend.default_hostname}"
}
```

Terraform will show these after apply, so you know where the sites are.

### 4.3 **Executing Terraform Deployment**

Now that we have Terraform code, let's outline how to run it:

1. **Initialize Terraform:** In the `infra/terraform` directory (where `main.tf` is), run:

   ```bash
   terraform init
   ```

   This will download the Azure provider and initialize the backend. If the storage account for backend doesn’t exist yet, `init` will error. Make sure it exists or temporarily comment out the backend block, run init/applies to create it, then uncomment and re-init with migration (Terraform will prompt to copy local state to remote).

   After init, Terraform knows to use Azure and has your credentials from Azure CLI (or environment if you set `ARM_CLIENT_ID` and others for service principal).

2. **Review the plan:** Run:

   ```bash
   terraform plan
   ```

   Terraform will refresh (none, since new) and then show what resources it will create and their details. Review the plan to ensure resources and names are correct. This is your chance to catch mistakes (e.g., naming conflicts, wrong sizing).

3. **Apply the plan:** Run:

   ```bash
   terraform apply
   ```

   Terraform will ask for confirmation (type "yes"). It will then proceed to create all resources in order.

   - It will create the resource group.
   - Then ACR, App Service Plan, then Web Apps (which depend on plan and ACR role assignment).
   - Create the DB server (this may take a few minutes – deploying a Postgres flexible server can be a few minutes operation).
   - Then create firewall rules, etc.

   Watch for any errors. Common issues:

   - Name already taken (especially for global names like ACR, storage account, web app DNS). You may need to use unique prefixes.
   - Password not meeting complexity requirements (Azure requires certain length and complexity for admin passwords).
   - Typos in resource properties.
   - Ensure that the Web App’s setting `linux_fx_version` uses the correct image name/tag that will exist. Right now, if you haven’t pushed an image yet, the web app might fail to pull. That’s okay initially – once we push the images via CI, the app will start working. The infrastructure can be set up in advance.

   After a successful apply, Terraform state is stored (locally or remotely if configured). Keep that state file safe (especially if locally and not using remote backend, it contains sensitive info like DB passwords, albeit possibly base64 encoded).

4. **Verify in Azure Portal:** You can navigate to the Azure Portal to see the created resources:
   - Resource Group "myapp-prod-rg" with the web apps, plan, and database.
   - Resource Group "myapp-terraform-rg" with the storage account (if created via TF).
   - In the Web App settings, check that the configuration (environment variables) is set as expected (you should see the ones we set).
   - The Web Apps might show "container not deployed" or an error until we push images. That’s expected.
   - The Postgres server should be running. You can connect to it using the admin credentials (e.g., use `psql` or Azure Cloud Shell) to verify the `myappdb` exists.

We have now provisioned all necessary Azure infrastructure via Terraform, which means our cloud environment is ready for the application. The Terraform scripts can be stored in version control, and any changes (like scaling up the plan, or adding new resources like Redis cache) can be done by modifying code and re-applying, ensuring consistent environment.

One more thing: **Terraform State Management** – Since we configured remote backend, our state is in an Azure blob. That allows team collaboration (everyone runs Terraform against the same remote state with locking to avoid conflicts) ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=4)). If not using remote state, the `terraform.tfstate` file generated is what you need to keep track of and not lose (losing it means Terraform loses track of what’s deployed, causing potential duplicates or manual import needs later). Always use either remote backend or have good backups of the state file.

We should also secure access to the state file because it contains sensitive values (like that DB password). Azure Storage backend encrypts the blob by default at rest ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=5.%20Understand%20encryption)) and state locking prevents concurrent modifications ([Store Terraform state in Azure Storage | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#:~:text=4)).

Finally, note that Terraform is just one IaC tool; others like Bicep, ARM templates, Pulumi, or AWS CloudFormation (for AWS) exist. We chose Terraform for its cloud-agnostic language and popularity.

## 5. **Deployment to Azure App Service**

With infrastructure in place (Azure App Services for front and back, ACR, PostgreSQL, etc.), the next step is to deploy our application containers to these services and configure everything for production. In this section, we will:

- Push the Docker images to the Azure Container Registry (or alternative registry).
- Ensure the Azure App Service instances are configured with the correct image and environment variables (which we did via Terraform).
- Set up any necessary environment variables or secrets on Azure (like database credentials, JWT secrets, etc. – partially done in Terraform).
- Start the applications on Azure and verify they run.
- Configure custom domains (if any) and HTTPS.
- Enable logging and monitoring tools (Azure Monitor, Application Insights) for observability.

### 5.1 **Publishing Docker Images for Deployment**

Our Azure Web Apps are expecting Docker images (as per the `linux_fx_version` setting). We need to make sure those images (frontend and backend) are available in the registry (ACR) with the specified tags (we used `latest` tag in our Terraform config).

**Option 1: Push images manually (for initial deployment):**

We can build and push from our local machine:

```bash
# Assuming you're already logged in to Azure CLI
az acr login --name myappacr2025

# Tag the images we built (if you have them locally from earlier steps) to ACR
docker tag myapp-backend:latest myappacr2025.azurecr.io/myapp-backend:latest
docker tag myapp-frontend:latest myappacr2025.azurecr.io/myapp-frontend:latest

# Push to ACR
docker push myappacr2025.azurecr.io/myapp-backend:latest
docker push myappacr2025.azurecr.io/myapp-frontend:latest
```

This requires that you built `myapp-backend:latest` and `myapp-frontend:latest` locally. Alternatively, you can have the CI/CD pipeline (GitHub Actions, next section) build and push these images automatically.

Once the images are in ACR, Azure App Service will detect (if continuous deployment is enabled on the app) and pull them. If not, you might need to trigger a restart or a deployment via `az webapp restart`. In our Terraform, we didn't explicitly enable auto continuous deployment, but the Web App will periodically try to pull the image (especially if you re-push with same tag, it might not auto-update unless the image digest changes – typically it does if you push new image). To force update, one can use `az webapp config container set` command or restart the web app.

**Verify deployment:**

- Go to Azure Portal, find the backend Web App "myapp-backend". In the overview, after a few minutes, it should show it's running and which image it's using. You can also check the "Containers" tab to see logs from container startup.
- Access the backend URL given (e.g., `https://myapp-backend.azurewebsites.net/api/hello`). It should return the greeting JSON. (Remember our Spring Boot app context; if it requires a JWT now due to security config, it might block unauthorized access. For testing, perhaps ensure security is disabled or permitAll on that endpoint or test with a token.)
- Check the frontend by visiting `https://myapp-frontend.azurewebsites.net`. You should see the React app. If it’s trying to call the API, ensure it calls the correct URL (perhaps we set REACT_APP_API_URL to the backend's URL, or it might still be calling `localhost:8080` if not configured – that would fail in Azure). If misconfigured, we may need to adjust environment or the code to use a relative path that goes to same domain (could deploy front and back under same domain or configure a proxy).

**Setting Environment Variables and Secrets in Azure:**

We largely did this via Terraform’s `app_settings`. You can also set these via Azure CLI or Portal:

- Azure CLI example:
  ```bash
  az webapp config appsettings set -g myapp-prod-rg -n myapp-backend --settings SPRING_DATASOURCE_PASSWORD=NewPasswordValue
  ```
  This would update an app setting. (Note: If you change via CLI or Portal, it may drift from Terraform state unless you also update Terraform config. To keep consistency, either update through Terraform and re-apply, or use a parameter store approach. But for sensitive runtime secrets, some prefer using Azure Key Vault and link it to App Service.)
- Portal: navigate to Web App > Configuration > Application Settings, and you can add/edit settings. They take effect on save (App Service will restart the app to apply new settings).

**Security of secrets:** App Settings in Azure are encrypted at rest and not visible to users without proper access. Marking a setting as "Slot setting" can keep it separate per deployment slot. If you have highly sensitive data (like a JWT signing key), consider using Azure Key Vault to store it and have the app read it securely (there’s integration where App Service can fetch from Key Vault into an env var).

### 5.2 **Configuring HTTPS and Custom Domains**

By default, Azure App Service provides a domain like `your-app.azurewebsites.net` which is served over HTTPS with a Microsoft certificate. If you have a custom domain (e.g., myapp.com), you can bind it to the web apps and set up HTTPS.

Basic steps for custom domain:

- Verify domain ownership by creating the required DNS records (Azure provides a specific token as a TXT record).
- Bind the custom domain in App Service (Portal or CLI).
- Upload or create a certificate for that domain and bind it. Azure App Service can provide a free managed certificate for custom domains (HTTPS) for root and wildcard domains (currently free certs for custom domains that aren’t sub-subdomains).

If using solely the azurewebsites.net domain, you already have HTTPS. Ensure "HTTPS Only" is enabled on the web app (this forces redirect HTTP to HTTPS). In Portal, under TLS/SSL settings, set HTTPS Only to On. This can also be done via Terraform or CLI:

```bash
az webapp update -g myapp-prod-rg -n myapp-backend --set httpsOnly=true
```

This ensures all traffic is encrypted.

Our React app likely should call the backend over HTTPS as well. In production, we’ll ensure the URL it uses is `https://myapp-backend.azurewebsites.net` (or custom domain). That prevents mixed content (HTTPS page calling HTTP API would be blocked by browsers).

### 5.3 **Logging and Monitoring on Azure**

**Application Logs:** Azure App Service can capture the stdout/stderr from our containers. Spring Boot logs to stdout by default. These logs can be viewed via:

- **Azure Portal Log Stream:** See real-time logs in the portal (Web App > Log Stream).
- **Azure CLI:** `az webapp log tail -n myapp-backend -g myapp-prod-rg` to tail logs.
- **Log Analytics:** We can configure an Azure Log Analytics workspace and send logs there for query and analysis. If using containers, an easier method is to use Application Insights for structured logging.

**Application Insights:** This is an APM (Application Performance Monitoring) service part of Azure Monitor. It can collect request metrics, logs, exceptions, and custom telemetry from your app. For Java, you have two main ways:

- Use the **Application Insights Java Agent**. This is a .jar that you attach to the JVM on startup which automatically instruments the app. Azure App Service for Java has a setting to enable this easily.
- Or manually use the Application Insights SDK (not as common for Java, agent is easier).

Enabling Application Insights:

- Create an Application Insights resource (can be done via Terraform or Portal). For example:
  ```hcl
  resource "azurerm_application_insights" "appinsights" {
    name                = "myapp-insights"
    location            = azurerm_resource_group.app.location
    resource_group_name = azurerm_resource_group.app.name
    application_type    = "java"
  }
  ```
  This gives an instrumentation key or connection string.
- Configure the Web App to use it. In Portal, under Application Insights, you can “Turn on Application Insights” which if the app is a Java app, it might prompt to restart with agent. Alternatively, set App Settings:
  ```
  "APPINSIGHTS_INSTRUMENTATIONKEY" = "<your-key>"
  "APPLICATIONINSIGHTS_CONNECTION_STRING" = "<connection string>"
  ```
  and
  ```
  "AzureWebJobsStorage" = ""  (sometimes needed to disable some connection stuff)
  ```
  Also set `-javaagent` in startup if needed. In App Service for Linux containers, another approach: use the Docker image with built-in AI agent, or mount the agent. There's an extension but that’s for Windows. For Linux containers, perhaps build the agent into the image or use an environment variable `APPLICATIONINSIGHTS_AGENT_SETTINGS` to point to config.
- A simpler method on App Service: Go to Web App > Application Insights > “Enable”. It might handle injecting the agent. Check docs for "Application Insights with Azure App Service Linux Java".

Once Application Insights is running, you can:

- See metrics like server response times, request rates, failure rates.
- View logs in the Application Insights Logs (Kusto queries).
- Enable **Live Metrics Stream** for real-time insight.
- Use **Profiler** to capture performance traces.

**Azure Monitor Alerts:** You can set up alerts on metrics/logs. For example:

- Alert if CPU > 80% for 5 minutes (scale out or investigate).
- Alert if memory usage high or if instance count increases (if auto-scale, to track costs).
- Alert if a certain exception is logged frequently or if a 500 response occurs too often (via Application Insights alert rules).
- Alert on HTTP 5xx rate beyond threshold.

**Azure Monitor for containers:** Since these are single-container app services, App Insights covers app-level. If using Azure Kubernetes Service, one would use Container insights.

For our needs:

- Ensure that logs from Spring Boot (and Nginx) are accessible. (Nginx logs would be in container stdout too.)
- Possibly configure log retention. App Service retains some logs for a short time. You might want to ship them to Azure Blob or Log Analytics for longer retention.
- We can also enable **Azure Monitor logging**: in Web App > Diagnostics, you can enable sending logs to Azure Monitor.

**Testing Monitoring:** Generate some test traffic (open the sites, hit the APIs). Then check Application Insights "Requests" blade to see if it logged them, and "Logs" to query traces.

### 5.4 **Final Verification**

At this point, your application should be fully deployed:

- The React frontend accessible via its Azure URL (or custom domain), served over HTTPS.
- The Spring Boot backend accessible via its URL, serving data from the database.
- The two can communicate (if you configured the frontend with the correct API URL).
- Authentication (if implemented) would be in place - ensure any OAuth redirect URIs or JWT issuers are configured appropriately to the new domain.
- You have Terraform managing the infra, and Docker images representing the app, so the deployment is reproducible.

Try a full integration test:

- Open the frontend in a browser, ensure it displays data from the backend.
- Try creating a database entry through the UI if such feature exists, verify it goes to DB.
- Check Azure Portal for any errors (Web App blade shows if container start failed, etc.).

If any issues arise:

- Use Azure's diagnostic logs. For instance, if the container fails to start, Azure will show logs (like if Spring Boot crashed due to wrong DB credentials).
- Adjust environment settings as needed (like fixing a wrong password or URL) and restart the app.
- Use the `Console` feature in Azure Web App (accessible via Portal) to open a shell inside the container – you can inspect environment vars (`printenv`) to confirm they are set, or logs in `/var/log` if any.

We should also consider **deployment slots** for the backend if doing production deployments with minimal downtime. Azure App Service slots allow having a staging slot with the new version, warm it up, then swap with production. This also provides rollback (swap back if needed). For simplicity, we did single slot (production).

Everything being up, we can proceed to establishing a CI/CD workflow to automate building and deploying new versions of this app.

## 6. **CI/CD with GitHub Actions**

Manually building and deploying is error-prone. We will set up **GitHub Actions** to automate our CI/CD pipeline. The goals:

- **Continuous Integration (CI):** On each push or pull request, automatically run our tests (both backend JUnit and frontend Jest) to ensure nothing is broken.
- **Continuous Deployment (CD):** On merging to main (or pushing a new tag/release), automatically build the Docker images and deploy them to Azure (push to ACR and update the App Services).
- Handle separate environments: e.g., deploy to a **staging** slot or site for testing, and only deploy to **production** when ready (perhaps on tag or manual approval).
- Integrate security and quality checks: e.g., run dependency scans, code linting, etc., as part of the pipeline.
- Provide rollback capabilities: e.g., if a deployment fails or a critical bug is detected, we can revert to the previous working version quickly (perhaps using deployment slots or by redeploying the previous container image).

We will focus on using **GitHub Actions**, as the code is presumably hosted on GitHub. (If using Azure Repos or other, Azure Pipelines or other CI systems can do similar steps.)

### 6.1 **Setting up GitHub Actions Workflow**

In your repository, create a directory `.github/workflows`. Inside, create a file `ci-cd.yml` (name is arbitrary). We’ll design this workflow to cover build, test, and deploy.

**Trigger conditions (when to run):**

- On pull requests to main: run CI (build & test) but not deploy.
- On push to main (merging a PR): deploy to a staging slot or directly to production.
- Possibly on push to a specific tag (like a release tag) or to a prod branch, then deploy to production.

For simplicity, assume a branching model: `main` is the production branch. We might use `dev` or `staging` branch for staging environment. Alternatively, use manual approvals.

Example triggers:

```yaml
on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]
```

This means:

- CI runs on every PR to main (so team can see tests passing before merge).
- When something is pushed to main or staging branch, we trigger deployment to respective environment.

**Jobs:**

We can have multiple jobs:

- `build_test` job – for running tests (perhaps in parallel for front and back).
- `deploy` job – depends on `build_test` success, and handles pushing images and updating Azure.

Let's outline a combined workflow:

```yaml
name: CI-CD Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [staging, main]

jobs:
  # 1. Build and Test job
  build_test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        part: [backend, frontend]
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Java
        if: matrix.part == 'backend'
        uses: actions/setup-java@v3
        with:
          distribution: "temurin"
          java-version: "17"

      - name: Set up Node
        if: matrix.part == 'frontend'
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Backend - Build & Test
        if: matrix.part == 'backend'
        run: mvn install -B -DskipTests=false

      - name: Frontend - Install & Test
        if: matrix.part == 'frontend'
        run: |
          npm ci
          npm run test -- --ci --passWithNoTests

      # Could add code quality scans, linters here for each part.
```

This `build_test` job uses a **matrix** to run two variations: one for backend and one for frontend in parallel. It sets up Java on the backend one and Node on the frontend one. Then runs Maven for backend (which compiles and runs tests) ([Simplified Guide to JWT Authentication with Spring Boot - DEV Community](https://dev.to/abhi9720/a-comprehensive-guide-to-jwt-authentication-with-spring-boot-117p#:~:text=Step%201%3A%20Setting%20Up%20Your,Security%2C%20and%20Spring%20Data%20JPA)), and npm for frontend (install deps and run tests) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Copy%20package.json%20and%20package,json)). If any test fails, this job fails.

We skip building the Docker images here to save time if tests fail. Alternatively, we could build images after tests in the same job (but pushing to ACR should be separate to avoid pushing if tests fail).

Now, the deploy job:

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build_test # only run if build_test job passes
  if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/staging'
  steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Azure CLI
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Build Backend Docker image
      run: docker build -t myapp-backend:${{ github.sha }} -f myapp-backend/Dockerfile ./myapp-backend

    - name: Build Frontend Docker image
      run: docker build -t myapp-frontend:${{ github.sha }} -f my-app/Dockerfile ./my-app

    - name: Azure Container Registry Login
      run: az acr login --name myappacr2025

    - name: Tag and Push Backend Image
      run: |
        docker tag myapp-backend:${{ github.sha }} myappacr2025.azurecr.io/myapp-backend:${{ github.sha }}
        docker push myappacr2025.azurecr.io/myapp-backend:${{ github.sha }}
        # Also tag "latest" if pushing to main (prod)
        if [ "${{ github.ref }}" == "refs/heads/main" ]; then
          docker tag myapp-backend:${{ github.sha }} myappacr2025.azurecr.io/myapp-backend:latest
          docker push myappacr2025.azurecr.io/myapp-backend:latest
        fi

    - name: Tag and Push Frontend Image
      run: |
        docker tag myapp-frontend:${{ github.sha }} myappacr2025.azurecr.io/myapp-frontend:${{ github.sha }}
        docker push myappacr2025.azurecr.io/myapp-frontend:${{ github.sha }}
        if [ "${{ github.ref }}" == "refs/heads/main" ]; then
          docker tag myapp-frontend:${{ github.sha }} myappacr2025.azurecr.io/myapp-frontend:latest
          docker push myappacr2025.azurecr.io/myapp-frontend:latest
        fi

    - name: Deploy to Azure (Staging or Production)
      run: |
        if [ "${{ github.ref }}" == "refs/heads/staging" ]; then
          # Use Azure CLI to deploy images to staging slot or staging app
          az webapp config container set -g myapp-prod-rg -n myapp-backend --slot staging \
            --docker-custom-image-name myappacr2025.azurecr.io/myapp-backend:${{ github.sha }} --docker-registry-server-url https://myappacr2025.azurecr.io
          az webapp config container set -g myapp-prod-rg -n myapp-frontend --slot staging \
            --docker-custom-image-name myappacr2025.azurecr.io/myapp-frontend:${{ github.sha }} --docker-registry-server-url https://myappacr2025.azurecr.io
        else
          # Deploy to production
          az webapp config container set -g myapp-prod-rg -n myapp-backend \
            --docker-custom-image-name myappacr2025.azurecr.io/myapp-backend:${{ github.sha }} --docker-registry-server-url https://myappacr2025.azurecr.io
          az webapp config container set -g myapp-prod-rg -n myapp-frontend \
            --docker-custom-image-name myappacr2025.azurecr.io/myapp-frontend:${{ github.sha }} --docker-registry-server-url https://myappacr2025.azurecr.io
        fi
```

Let’s unpack this:

- We use `needs: build_test` to only run after successful tests.
- We also use an `if:` to only run deploy for certain branches (main or staging).
- **Azure login:** We use the Azure CLI action to authenticate. We need to create a Service Principal or use OIDC. The simplest is using a Service Principal’s JSON credentials stored in repository secrets as `AZURE_CREDENTIALS`. (This secret can be created via `az ad sp create-for-rbac` and must have appropriate rights on the resource group, e.g., contributor role, to update web app settings and push to ACR. Alternatively, we can just use `az acr login` with admin creds if admin enabled, but we disabled that. Using SP or OIDC with a role assignment for ACR and Web App is better.)  
  For a more secure approach, GitHub Actions supports OpenID Connect (OIDC) where it can request a token from Azure AD without storing a secret, but that’s advanced configuration (requires setting up federated credentials in Azure AD).
- We build Docker images for both services. We tag them with the commit SHA (github.sha) for uniqueness. If on main branch, we also tag as "latest" because our production config points to `:latest`. Alternatively, we could avoid using latest and always deploy by setting the webapp to the specific sha tag. That might actually be cleaner for rollback: e.g., Terraform could set a dummy image initially, and we always update via CLI to specific tags. We show tagging both for demonstration.
- We log in to ACR using Azure CLI (since `az login` was done, `az acr login` should succeed).
- We push the images to ACR with both the SHA tag and possibly the "latest" tag for main.
- Finally, we deploy:
  - If pushing to `staging` branch, we assume we have deployment slots created named "staging" for both web apps. (We didn't create them in Terraform earlier, but we can do it or set up separate "myapp-backend-staging" site. Let's assume slots for simplicity: `az webapp deployment slot create -g rg -n myapp-backend -s staging` can be done outside this flow.)
  - The `az webapp config container set` command updates the web app's container image to the new tag. For staging, we set the slot to use the new commit image.
  - If main, we update the production slot with the new image.
  - Because we manage ACR via managed identity, no need to pass username/password as long as the Web App is already configured with the ACR. Actually, if using managed identity, we might not even need to run this command if using `:latest` and continuous deployment is toggled. But to be explicit, we do it.
  - Another strategy: If using slots, you might deploy commit-specific image to staging slot, run tests (maybe some integration tests or manual verification), then when ready, swap slots (staging -> production). That provides zero-downtime and easy rollback (swap back). We can automate slot swap as well in the workflow when promoting to production.
  - For brevity, we directly update production on main push. A safer production deployment might be to push to staging, then manual approval to swap to prod.

**Secrets in GitHub Actions:**

- `AZURE_CREDENTIALS`: JSON containing Azure SP clientId, clientSecret, tenantId, subscriptionId. Create SP with `Contributor` role to resource group.
- Alternatively, store `ACR_USERNAME` and `ACR_PASSWORD` (if using admin) as secrets and use `docker/login-action` to login to ACR. But using `az acr login` after az login is straightforward here.
- Database credentials or other secrets might be needed during integration tests (if any). For example, if we had integration tests that connect to Azure DB or use some secret, those could be stored as secrets. But in our pipeline, tests run against ephemeral environment (maybe an H2 or local PG if we set up).
- Ensure sensitive data (like Azure creds) are in GitHub repository secrets or organization secrets, not in code.

**Security checks integration:**

- We can add a step to run a dependency vulnerability scanner. GitHub has Dependabot alerts out-of-the-box. Also, the Docker build will show if base images have vulnerabilities if you use something like `docker scan` (Snyk). We might add a `uses: docker/login@...` and `docker scan myapp-backend:...`.
- We might run code scanning (like CodeQL analysis) as a separate workflow triggered daily or on push – GitHub has templates for CodeQL which can be enabled for security scanning.

**Automated Rollback:**

- If deployment fails (the action fails), the previous version is still running – so in that sense, it's not taken down.
- If deployment succeeds but we discover a bug, rolling back can be as easy as re-running the workflow using the previous commit’s SHA (or re-tagging latest to the previous image). If using slots, swapping back is a quick rollback.
- We could automate that if a monitoring alert triggers, but usually that’s manual or via an orchestrator with health checks.

**Isolation of environments:**

- We used branches to separate staging vs prod. Some use separate Azure resources (like a separate resource group with its own app service and DB for staging). If so, the Terraform could be parameterized by environment, or use separate Terraform state/workspace for staging vs prod. For simplicity, we assumed same RG but with slots.
- In the pipeline, one could do: on push to main, deploy to slot; on push of a version tag, swap to prod, etc.

### 6.2 **GitHub Actions Workflow Summary**

With the above workflow:

- Every PR to main triggers `build_test` (runs tests). If something fails, contributors see it in the PR status.
- If PR is merged to `staging` branch (or push to staging), it triggers build, test, then deploy job, deploying images tagged by commit to the staging slot. QA can then test the staging slot (which might be accessible via a URL like `myapp-backend-staging.azurewebsites.net`).
- If PR is merged to `main` (production), build & test run (good to double-check it still passes on merge), then deploy job pushes images and updates production to the new version. Ideally done after staging verification.
- We might refine triggers: e.g., only allow deploy job on main if it was not a PR but an actual push (to avoid double deploying on merge commit). The condition could be refined with `github.event_name`.
- We integrated building of both parts and deploying both. This is convenient since front and back are versioned together. In microservice architecture, you might separate these or version independently.

**Storing the workflow in repo:** Commit the YAML. If repository is private, GitHub Actions minutes usage is free for a certain limit, if public, it’s free.

**Run an example pipeline:**

- Developer opens PR -> tests run -> if green, merge to staging -> pipeline builds, deploys to staging slot -> testers verify -> when approved, merge staging to main -> pipeline deploys to production -> monitoring on production for any issues.

Our CI/CD pipeline thus covers testing, building, and deploying with minimal manual steps, improving reliability and speed of releases.

## 7. **Best Practices & Optimization**

We’ve covered the technical steps. Now let's summarize some best practices and additional optimizations for a production-grade system in terms of security, performance, observability, and cost management.

### 7.1 **Security Best Practices**

- **Use HTTPS Everywhere:** Ensure that your frontend and backend are served over HTTPS only. Azure App Service allows you to enforce HTTPS only ([[NoBrainer] Deploy a Spring Boot Application to an Azure App Service – blog.rufer.be](https://blog.rufer.be/2022/10/26/nobrainer-deploy-a-spring-boot-application-to-an-azure-app-service/#:~:text=again%20impressed%20by%20Azure%20%E2%80%93,commit%20to%20the%20selected%20branch)). If using a custom domain, get an SSL certificate (Azure’s free managed cert or another provider) and bind it. This encrypts all data in transit.
- **Secure Secrets:** Never expose database passwords, JWT secret keys, or OAuth client secrets in source code or Docker images. Use environment variables or Azure Key Vault. Azure Key Vault can be used with Managed Identities such that your Web App can fetch secrets without them ever being in code or config. At minimum, use App Settings (which are encrypted) rather than hardcoding secrets.
- **HTTP Security Headers:** Implement security headers in the responses (CSP, XSS-Protection, etc.). For the React app served by Nginx, configure Nginx to add headers like Content Security Policy (restrict domains for scripts), Strict-Transport-Security (HSTS for HTTPS), X-Content-Type-Options, etc. Spring Boot can also add security headers in responses easily via Security config.
- **Authentication & Authorization:** If using JWT, ensure strong signing keys and short token lifetimes. Validate tokens on each request (Spring Security filters do this). If using OAuth2 (e.g., Azure AD), leverage its robust identity management, and validate scopes/roles in the app. For user authentication flows, consider libraries or services (like using Azure AD B2C or Okta for user login to avoid building your own auth).
- **Input Validation & Sanitization:** Validate all API inputs (Spring Boot can use Bean Validation on request DTOs). Sanitize outputs if needed to prevent XSS (though React by default escapes content, unless dangerously set HTML).
- **CORS in Production:** In dev we allowed localhost, but in production, restrict `@CrossOrigin` to only your known frontend domain. Or disable it if the frontend and backend are served from the same domain (e.g., if you use a reverse proxy or same domain for API).
- **API Gateway (Optional):** For larger systems or for additional security layers, an API gateway or Azure Application Gateway/WAF could be placed in front of the backend. This can provide a Web Application Firewall to filter malicious requests, rate limiting, IP allow/block lists, etc. Azure also offers **Azure API Management** which can be used to secure and monitor APIs (with keys, JWT validation, etc.). For a single-app, this might be overkill, but for microservices, it’s useful.
- **Penetration Testing & Scanning:** Use tools to scan your app (both static code scans and dynamic pen-test). For example, run OWASP Zap or Burp Suite against your deployed site to catch any obvious security holes. Also keep dependencies up to date (the CI could use Dependabot).
- **Least Privilege for Azure Resources:** The service principal used in CI/CD should have only needed permissions. The database credentials given to app (we used admin for simplicity) ideally should be a limited user with just necessary privileges on that specific database, not the server admin. Create a specific DB user for the app with least privileges (only required tables).
- **Network Security:** If possible, restrict database access to only the App Service. We used firewall rules (allow Azure). A more secure approach is VNet integration: put the DB in a subnet and restrict access to that subnet; integrate the Web App with that VNet so it can reach the DB privately. Azure App Service can use Regional VNet Integration for outbound traffic to a VNet. This would completely remove public exposure of the DB.
- **Container Security:** Continuously scan the container images for vulnerabilities (use Dependabot for base image updates or Azure Security Center scanning). Also ensure you regularly update base images (we use `node:18-alpine`, `openjdk:17-slim`; keep an eye on updates like 17.0.x JDK releases).
- **Backups:** Enable backups for critical components. For database, set up automated backups (Azure DB typically has automated backups and point-in-time restore; verify the retention meets your needs). For App Service, you might not need file backup since code is in containers and DB holds state, but if you do allow uploads or use Azure Storage, ensure those are backed or redundant.
- **Monitoring for security events:** Use Azure Monitor or a SIEM to track anomalies (like sudden spike in 500 errors or in auth failures which could indicate an attack). Azure AD and App Service logs can be piped to Sentinel or third-party SIEM for analysis.

### 7.2 **Performance Optimization**

- **Caching (Backend):** Introduce caching for expensive operations. Spring Boot with Spring Cache can be used with a cache provider like Redis. Azure offers **Azure Cache for Redis** as a managed service. For example, cache database query results that are frequently read but rarely change, to reduce load on DB. Or use caching for session data if not stateless. In microservices, consider caching HTTP calls between services.
- **Caching (Frontend):** Use a CDN for static assets. Azure CDN or Azure Front Door can cache and serve the static files globally, reducing load on the App Service and improving latency for users far from the origin server. In our case, because we used App Service, we could put Azure Front Door in front of it and enable caching rules for `*.js`, `*.css` files. Alternatively, host static files in an Azure Blob Storage static website and put CDN in front.
- **Browser caching:** Ensure your static files have long cache headers (React build by default appends hashes to filenames and can be cached indefinitely). Nginx can be configured (via a config file in the image) to add `Cache-Control: max-age=31536000, immutable` for hashed assets, and shorter for index.html.
- **Database performance:** Use connection pooling (Spring Boot does this by default via HikariCP). Monitor DB for slow queries – add indexes or optimize queries as needed (analyze query plans). Scale up the DB SKU if needed or enable read replicas for heavy read load.
- **Asynchronous and Non-blocking:** If certain API calls are slow (e.g., calling external services), use asynchronous processing (Spring Boot’s `@Async` or webflux/reactor if appropriate) to not block threads. You can also use message queues (Azure Service Bus) for processing work in background.
- **Load Testing:** Perform load testing (using JMeter, Locust, etc.) on staging to see how many users/requests the app handles. Identify bottlenecks (CPU, memory, DB, external API). Use that to decide scaling and caching strategies.
- **Scale-Out and Scale-Up:** Azure App Service can scale out (multiple instances). You can set up **Auto-scaling** rules (in the App Service Plan or via Azure Monitor autoscale) to add instances when CPU or memory is high or queue length grows. Ensure the app is stateless (or use distributed cache for session) so scaling out is seamless. Also scale up to a higher tier if needed (more CPU/RAM or Premium tier for faster processors).
- **Compression:** Enable gzip/Brotli compression for responses. Nginx by default can compress text files (we can ensure it's on). Spring Boot also can compress responses (property `server.compression.enabled=true`). This reduces bandwidth usage and speeds up loading for clients.
- **HTTP Keep-Alive and Connection Pooling:** By default, HTTP keep-alive is on so that multiple requests reuse connections, which is fine. If using a heavy API usage from frontend, consider using HTTP/2 (Azure Front Door or App Service support HTTP/2) for multiplexing requests.
- **Front-End Performance:** Besides network, ensure the React app is optimized – e.g., use code splitting to reduce initial bundle size, remove any large unused dependencies, and use performance tools (Lighthouse) to audit the frontend.

### 7.3 **Observability & Maintenance**

- **Structured Logging:** Use a structured logging framework (e.g., log in JSON) to make it easier to query logs in Azure Monitor. Spring Boot can be configured with JSON format logs (Logback encoder or using Application Insights appender).
- **Distributed Tracing:** With Application Insights (or Zipkin/Jaeger if self-hosting), you can get distributed traces. If you had multiple services, use correlation IDs. Even with one service, tracing helps find slow operations. Ensure the front-end includes a correlation ID header (or the Application Insights JavaScript SDK to trace user actions) that ties into backend traces. Application Insights can correlate a frontend browser event to backend request if configured.
- **Metrics:** Use Micrometer (built into Spring Boot Actuator) to collect metrics. Application Insights can automatically capture some metrics (requests/sec, etc.), and you can push custom metrics (like business metrics, e.g., orders placed per minute).
- **Health Checks:** Implement a health endpoint (Spring Boot Actuator’s `/actuator/health`) which can be used by Azure for monitoring. App Service doesn’t automatically use it, but if behind Azure Front Door or Application Gateway, those can ping a health URL to determine if instance is healthy.
- **Analytics:** For front-end, utilize Azure Application Insights front-end (via JavaScript SDK) to track page views, user behaviour, etc., if needed.
- **Maintenance:** Plan for regular updates: keep dependencies updated (Spring Boot releases, Node updates). Automate tests and maybe have a regular job for dependency updates (GitHub Dependabot can automate PRs for version bumps).
- **Data Maintenance:** Implement database migration strategy (Flyway or Liquibase) for schema changes through versions, especially as the app evolves.
- **Documentation & Knowledge Transfer:** Maintain README or wiki for developers/operators that covers how to run, how to deploy, how to rollback, etc., so team members can easily operate the system.

### 7.4 **Cost Optimization Techniques**

Running apps in Azure incurs costs on App Service, DB, ACR, bandwidth, etc. Strategies to reduce or optimize cost:

- **Right-size the App Service Plan:** Don’t over-provision instance size or count. Start with the smallest that meets your performance needs (Basic/Standard tiers). Monitor utilization; if CPU and memory are low, you might be able to scale down. If they're high and you scale out, ensure you're utilizing the instances.
- **Use Auto-scaling to handle load efficiently:** Instead of running N instances 24/7, configure autoscale to add instances during peak and remove during off-peak. This way you pay for extra instances only when needed.
- **Shut down/stage when not in use:** For non-production environments (dev/test/staging), you can stop those App Services when not actively in use (e.g., on nights/weekends) to save cost – App Service (except free tier) charges as long as the plan is allocated. If using slots on same plan for staging, that’s more cost-effective than separate plan.
- **Database SKU:** Use a cheaper SKU for dev/test (or even Azure’s serverless PostgreSQL if available – it can scale down to 0 when idle). For production, ensure you're not vastly over-provisioned; adjust vCores and storage to what's needed. Azure DB has a pricing difference between provisioned and serverless tiers; serverless can auto-pause when idle to save cost, which might be good for infrequently used systems (though latency on resume).
- **Use Azure Reserved Instances/Savings Plan:** If you know you'll run this App Service for 1 or 3 years, buying a reserved instance for that plan can significantly reduce cost (up to ~55% savings). Similarly, reserved capacity for database vCores saves cost.
- **Optimize Bandwidth and CDN:** Egress bandwidth from Azure costs money. Using a CDN might reduce egress from your origin (though CDN itself has cost, but if many repeat requests, it can save). Also serve compressed content to reduce bandwidth.
- **Deallocate unused resources:** Regularly check Azure for resources that are incurring cost but not used. For example, if you created extra test Web Apps or have old containers/images stored (ACR storage cost is low but can clean old images). Azure Cost Management tool can help identify such items.
- **Use Free/Dev SKU where possible in non-prod:** Azure App Service has a free tier (limited to 1GB and single instance, no custom domain) – could be used for a dev environment. Azure Database has a free tier for certain amount of usage for 12 months (depending on offers) or use Azure SQL dev edition if that fits. There’s also an Azure Cosmos DB free tier etc. But weigh the effort vs savings for short-term.
- **Monitor costs:** Use Azure Cost Management to set up budgets and alerts. For instance, set a monthly budget and get alerted if costs approach it. Azure Advisor also gives cost optimization recommendations (like suggesting a different tier or identifying underutilized VM/Service) ([Azure Well-Architected Framework Perspective on Azure App ...](https://learn.microsoft.com/en-us/azure/well-architected/service-guides/app-service-web-apps#:~:text=Azure%20Well,For%20more)).
- **Use Bicep/Terraform to tear down test environments easily:** If you have an isolated QA environment, you can spin it up with Terraform when needed and destroy it when done to not pay when it's idle.
- **Energy/Performance trade-offs:** For extreme cost optimization, if usage is very low, one might even use Azure Functions (serverless) for a small API rather than App Service, and Static Web Apps for frontend (they have generous free quotas). Our scenario uses App Service likely for consistent long-running service.

In summary, balance performance and cost: use what you need, and scale or turn off what you don’t. Regularly review the Azure cost breakdown (which service is costing how much) to identify anomalies or opportunities to save.

---

**Conclusion:** We have now gone through the entire lifecycle: development, containerization, deployment, CI/CD, and maintenance. Following this guide, you can build a robust full-stack application with React and Spring Boot, deploy it on Azure with modern DevOps practices, and keep it running smoothly, securely, and cost-effectively.

By automating infrastructure with Terraform and deployments with GitHub Actions, you achieve reliable and repeatable releases. Adhering to best practices in each phase ensures the application is production-ready.

Feel free to review each section of this guide. When you're confident everything is set up correctly, you can proceed to deploy the application and enjoy your scalable full-stack system running in the cloud. If any adjustments are needed, you can iterate using the same processes described. Happy coding and deploying!
