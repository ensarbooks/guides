# Building a ReactJS and Spring Boot Application with a Real-Time Notification System

This guide provides a comprehensive, step-by-step walkthrough for advanced users to develop a full-stack application using **ReactJS** for the frontend and **Spring Boot** for the backend. The application will feature a robust real-time **notification system**, including persistent notifications, real-time updates with WebSockets, security via JWT authentication, and deployment considerations. Each section covers a major aspect of the development process, from initial setup to performance optimizations.

## 1. Setting Up the Project

To begin building our ReactJS and Spring Boot application with a notification system, we need to set up the development environment and create the initial project structure for both the frontend (React) and backend (Spring Boot). This section will guide you through installing the required tools and initializing both the React application and the Spring Boot application.

### 1.1 Installing Required Tools

Before creating the project, ensure you have the necessary software installed on your development machine:

- **Node.js and npm**: Node.js is required to run React's development server and build the frontend. npm (Node Package Manager) comes bundled with Node.js and will be used to install JavaScript dependencies. Download and install the latest LTS version of Node.js from the official website (which includes npm). After installation, verify by running `node -v` and `npm -v` in your terminal.
- **Java Development Kit (JDK)**: Spring Boot runs on Java, so install JDK 17 (or the latest LTS release). Ensure the `java` and `javac` commands are available in your PATH (check with `java -version`).
- **Build Tool (Maven or Gradle)**: Spring Boot projects typically use Maven or Gradle for build and dependency management. Maven is widely used; if you choose Maven, ensure Maven is installed (`mvn -v` to check) unless you plan to use the Maven wrapper provided by Spring Initializr. For Gradle, similarly ensure it's installed or use the wrapper.
- **Database**: Decide on a database system (PostgreSQL or MySQL) for storing notifications. Install the chosen database server (for example, PostgreSQL) and note the connection details (host, port, database name). Alternatively, you can use a containerized database or an in-memory database (like H2) for development.
- **IDE/Code Editor**: Choose an IDE or text editor suitable for both Java and JavaScript. For backend, IntelliJ IDEA (with Spring Boot support) or Eclipse (with Spring Tools) is recommended. For frontend, VS Code or WebStorm are popular choices. These tools will help manage and navigate the code easily.
- **Docker (optional at this stage)**: Install Docker Desktop if you plan to containerize the application later for deployment. While not needed for development, having Docker now will allow you to set up containers for services like the database or for testing the final build.

With these tools installed, you're ready to create the project structure.

### 1.2 Creating the ReactJS Application

First, let's set up the React application. We will use **Create React App** to bootstrap a new React project. Open a terminal and run the following command in the directory where you want your project to reside:

```bash
# Using npx (which comes with npm 5.2+)
npx create-react-app notification-ui
```

This will create a new folder named `notification-ui` containing a basic React project. The process may take a few minutes to install all dependencies. Once it's done, navigate into the project directory (`cd notification-ui`) and start the development server to verify everything works:

```bash
npm start
```

This should launch the React development server on [http://localhost:3000](http://localhost:3000) and display the default Create React App welcome page in your browser. If you see that page, your React setup is successful.

**Project Structure:** The React project has a standard structure created by Create React App:

- `src/` – Contains the application source code (React components, etc.).
- `public/` – Static assets and the HTML template.
- `package.json` – Configuration file listing dependencies and scripts.

We will customize this project in later sections to add our notification UI.

Next, we'll add a UI library for convenience. We will use **Material-UI (MUI)** for a modern look and pre-built components. To install Material-UI, run:

```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
```

This installs the core Material-UI components, Emotion (for styling, which MUI uses under the hood), and Material Icons (which includes an icon for notifications). After installing, you can test import a component (like a simple button from MUI) to ensure it's working, but we'll integrate it in detail in the frontend development section.

### 1.3 Creating the Spring Boot Application

Now, set up the Spring Boot backend. The easiest way to start a Spring Boot project is by using **Spring Initializr**, which can generate a skeleton project with the needed dependencies configured. Spring Initializr is a web service that generates a Spring Boot project structure for you ([RoadToWebDev Day#8- Building REST APIs with Spring Boot](https://shethradhika9.medium.com/roadtowebdev-day-8-building-rest-apis-with-spring-boot-f62cea282eaf#:~:text=The%20Spring%20Initializr%20is%20ultimately,It%20doesn%27t%20generate%20any)). It doesn't produce application code but provides a basic project structure with a build file (Maven POM or Gradle script) ([Expose a discoverable REST API of your domain model using HAL ...](https://cristina.tech/2017/03/28/hypermedia-driven-services-with-spring-data-rest#:~:text=,Gradle%20build%20specification%20to)).

Go to [start.spring.io](https://start.spring.io/) in your web browser. On the Spring Initializr page:

1. Select **Maven Project** (or Gradle if you prefer) and **Java** as the language.
2. Choose the Spring Boot version (use the latest stable release).
3. Fill in the group and artifact (for example, group: `com.example`, artifact: `notification-backend`).
4. Under "Dependencies", add the following:
   - **Spring Web** (for building REST APIs).
   - **Spring Security** (for implementing JWT security).
   - **Spring WebSocket** (often listed as "Websocket" or included in Spring Messaging, for real-time communication).
   - **Spring Data JPA** (for database access via JPA).
   - **Database Driver**: PostgreSQL or MySQL depending on your choice (e.g., "PostgreSQL Driver" if using PostgreSQL).
   - **Spring Boot DevTools** (optional, for hot reloading during development).
   - **Lombok** (optional, to reduce boilerplate code).
5. Click "Generate" to download the project as a zip file. Extract this zip to a folder, for example `notification-backend`.

If you prefer using your IDE, many IDEs (IntelliJ, VS Code with extensions, Spring Tools Suite) allow you to create a new Spring Boot project with similar options. This will result in the same project setup.

**Project Structure:** The Spring Boot project will have a structure like:

- `src/main/java/...` – Your Java source code (with a main application class annotated with `@SpringBootApplication`).
- `src/main/resources/` – Configuration files (like `application.properties`) and static resources.
- `pom.xml` or `build.gradle` – Build configuration listing dependencies.

Before moving on, open the project in your IDE and locate the main application class (usually named something like `NotificationBackendApplication.java` in the `com.example.notificationbackend` package). You can run this main class or use Maven to start the application:

```bash
# Inside notification-backend directory
./mvnw spring-boot:run
```

(This uses the Maven wrapper script included by Initializr. Alternatively, run it from your IDE.)

At this point, the Spring Boot application will start (by default on port 8080) but with no endpoints defined yet. You should see a log indicating the application started. We'll be adding functionality in upcoming sections.

### 1.4 Setting Up the Development Environment

Now that both projects are created, let's ensure a smooth development workflow:

- **Directory Structure**: If you plan to keep frontend and backend in one repository, you might structure your directories as:
  ```
  /project-root
     /notification-ui       (React app)
     /notification-backend  (Spring Boot app)
  ```
  This separation makes it clear which part is which. You can manage them separately (open two IDE windows or use one IDE that can handle multiple projects).
- **IDE Tips**: In IntelliJ IDEA, you can open the backend project and run it; for the frontend, open a separate VS Code window for the React project, or use IntelliJ's ability to open a project inside another. Alternatively, you can run the React dev server from the terminal. Debugging can also be done in respective IDEs (Chrome/Browser dev tools for React, and IDE debugger for Spring Boot).
- **Concurrent Running**: During development, you'll run the React app (on port 3000) and the Spring Boot app (on port 8080) simultaneously. Ensure there are no port conflicts. You might set up a proxy in the React dev server to API calls (Create React App allows specifying a proxy in `package.json` to forward calls to the backend during dev).
- **Source Control**: Initialize a git repository for your project if you haven't, to track changes. This is especially important as we proceed to add a lot of code. Commit frequently with clear messages.
- **Verify Setup**: As a quick test, try modifying the React `App.js` to display "Hello World" and verify it updates in the browser. For Spring Boot, consider adding a simple REST controller now (for example, a `@RestController` that returns "Hello" at some endpoint) to verify you can develop and hit an endpoint at [http://localhost:8080](http://localhost:8080). We'll add real endpoints in the next section, so this step is optional but helps confirm your environment is ready.

With the project scaffolded and environment ready, we can proceed to develop the backend functionality for notifications.

## 2. Backend Development (Spring Boot)

In this section, we will develop the backend of our application using Spring Boot. The backend will expose RESTful APIs for fetching and updating notifications, use WebSocket (with STOMP) to send real-time notification updates to clients, secure the endpoints with JWT authentication, and store notification data in a relational database.

### 2.1 Creating Notification REST APIs

We'll start by defining the data model and REST endpoints for the notification system. The backend will manage notifications as a JPA entity and provide APIs for common operations such as retrieving a user's notifications and marking them as read.

**Define the Notification Entity:**

Create a JPA entity class `Notification` in the backend project (e.g., under `com.example.notificationbackend.model`). This class will map to a database table for notifications. For example:

```java
@Entity
@Table(name = "notifications")
public class Notification {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String recipient;        // The username or user ID of the recipient
    private String type;            // Type of notification (e.g., "ALERT", "MESSAGE")
    private String content;         // Notification message content
    private boolean read = false;   // Read/unread status
    private Instant timestamp;      // When the notification was created

    // Constructors, getters, and setters omitted for brevity
}
```

Here, `recipient` is used to identify which user the notification is for. In a real application, this might be a foreign key to a User entity, but for simplicity we use a username or user ID. The `type` can distinguish notification categories, and `read` indicates if the user has seen the notification. The `timestamp` uses `java.time.Instant` to record creation time.

**JPA Repository:**

Create a repository interface to perform database operations on notifications. For example, in `repository/NotificationRepository.java`:

```java
@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {
    List<Notification> findByRecipientOrderByTimestampDesc(String recipient);
}
```

This repository provides built-in CRUD methods and the custom finder `findByRecipientOrderByTimestampDesc` to retrieve notifications for a specific user, most recent first.

**Service Layer:**

Although optional for simple cases, it's good practice to have a service layer. Create a `NotificationService` that uses the repository to fetch and update notifications. It might have methods like `getNotificationsForUser(String username)`, `markAsRead(Long notificationId)`, and `createNotification(String recipient, String type, String content)`.

For example, in `service/NotificationService.java`:

```java
@Service
public class NotificationService {
    @Autowired
    private NotificationRepository repo;

    public List<Notification> getNotificationsForUser(String username) {
        return repo.findByRecipientOrderByTimestampDesc(username);
    }

    public Notification createNotification(String recipient, String type, String content) {
        Notification notif = new Notification();
        notif.setRecipient(recipient);
        notif.setType(type);
        notif.setContent(content);
        notif.setTimestamp(Instant.now());
        notif.setRead(false);
        return repo.save(notif);
    }

    public void markAsRead(Long notificationId) {
        repo.findById(notificationId).ifPresent(notification -> {
            notification.setRead(true);
            repo.save(notification);
        });
    }
}
```

**REST Controllers:**

Next, create a REST controller that exposes endpoints for the frontend to interact with notifications. In `controller/NotificationController.java`:

```java
@RestController
@RequestMapping("/api/notifications")
public class NotificationController {
    @Autowired
    private NotificationService notificationService;

    @GetMapping
    public List<Notification> getUserNotifications(Authentication authentication) {
        // The Authentication object holds the current user's details after JWT validation
        String username = authentication.getName();
        return notificationService.getNotificationsForUser(username);
    }

    @PostMapping
    public ResponseEntity<Notification> createNotification(@RequestBody Notification newNotification) {
        // This could be restricted to admins or system services in a real app
        Notification saved = notificationService.createNotification(
                newNotification.getRecipient(), newNotification.getType(), newNotification.getContent());
        return ResponseEntity.ok(saved);
    }

    @PutMapping("/{id}/read")
    public ResponseEntity<Void> markAsRead(@PathVariable Long id) {
        notificationService.markAsRead(id);
        return ResponseEntity.noContent().build();
    }
}
```

Let's break down these endpoints:

- `GET /api/notifications`: Returns the list of notifications for the authenticated user. We obtain the username from the `Authentication` principal (populated by Spring Security after JWT verification). The service returns notifications from the database.
- `POST /api/notifications`: Creates a new notification. In a real scenario, notifications might be created by server-side events (e.g., someone sends you a message triggers a notification), not directly by an API call. But this endpoint allows creation for testing or by an admin/system. It expects a JSON body with at least `recipient`, `type`, and `content`. We call the service to save it to the database.
- `PUT /api/notifications/{id}/read`: Marks a specific notification as read. The client can call this when a notification is viewed. The service finds it and sets its `read` flag to true.

These APIs form the basic CRUD for notifications. Note that the `Notification` entity is returned directly here for brevity. In a production environment, you might use Data Transfer Objects (DTOs) to send only necessary fields to the client.

At this stage, if you start the Spring Boot application, these endpoints exist but are unsecured. In Section 2.3 we'll secure them with JWT, and after implementing WebSockets in Section 2.2, the creation of a notification will also trigger a real-time push to the user.

### 2.2 Implementing WebSockets for Real-Time Updates

One core feature of our notification system is to push new notifications to the user in real-time using WebSockets. Spring Boot supports WebSockets with an optional messaging protocol called STOMP (Simple Text Oriented Messaging Protocol), which makes it easier to send messages to specific destinations (topics or user queues) and integrate with Spring's messaging template.

**Enable WebSocket Messaging:**

Create a configuration class `WebSocketConfig` (e.g., under `config/` package) and annotate it with `@EnableWebSocketMessageBroker`. Also implement `WebSocketMessageBrokerConfigurer` to configure the STOMP endpoints and message broker:

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // Register a WebSocket endpoint that the client will use to connect.
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("http://localhost:3000")
                .withSockJS();
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        // Enable a simple in-memory broker and designate the message destinations
        registry.enableSimpleBroker("/topic", "/queue");
        registry.setApplicationDestinationPrefixes("/app");
        registry.setUserDestinationPrefix("/user");
    }
}
```

Explanation:

- `registerStompEndpoints`: We define the endpoint `/ws` that clients will connect to for WebSocket communication. We allow the development origin (React dev server at localhost:3000) for cross-origin requests. `.withSockJS()` enables a fallback to SockJS for browsers that don't support native WebSockets or for handling the handshake in a more robust way.
- `configureMessageBroker`: We enable a simple broker with destinations prefixed by `/topic` and `/queue`. The simple broker keeps messages in-memory and sends them to connected clients. We set an application prefix `/app` for messages that will be routed to server-side methods (if clients send messages), and a user destination prefix `/user` for messages directed to specific users. Spring's STOMP support recognizes destinations starting with `/user/` for this purpose (for sending messages to specific user sessions) ([User Destinations :: Spring Framework](https://docs.spring.io/spring-framework/reference/web/websocket/stomp/user-destination.html#:~:text=An%20application%20can%20send%20messages,with%20%2Fuser%2F%20for%20this%20purpose)).

With this setup, the server can send messages to:

- `/topic/xyz` for broadcast to all subscribers of a topic.
- `/user/{username}/queue/notifications` for a specific user (the broker will handle routing to the session of that authenticated user).

**Sending Notifications to Clients:**

We want new notifications to be pushed to the intended user in real-time. We'll use `SimpMessagingTemplate`, which is provided by Spring to send messages to WebSocket clients.

Inject `SimpMessagingTemplate` into the `NotificationService` (or a dedicated messaging service). For example, modify `NotificationService.createNotification` to send a message after saving:

```java
@Autowired
private SimpMessagingTemplate messagingTemplate;

public Notification createNotification(String recipient, String type, String content) {
    Notification notif = new Notification(...); // build notification as before
    Notification saved = repo.save(notif);
    // Convert to a DTO if necessary before sending
    Notification dto = saved; // here we can reuse the entity or map to a DTO
    // Send to the specific user's queue via WebSocket
    messagingTemplate.convertAndSendToUser(
        recipient, "/queue/notifications", dto
    );
    return saved;
}
```

Here, `convertAndSendToUser` targets a specific user. The first parameter is the username (it should match the principal name of the authenticated user session), the destination is `/queue/notifications`, and the payload is the notification data (we send the notification object, but you might send a simplified version to the client). Spring will internally prepend the `/user/` prefix for user destinations. As a result, the message is delivered only to the client that is authenticated as that user.

**Security Note:** By default, if using an in-memory simple broker, any connected client who knows the destination could subscribe to it. We will rely on Spring Security to ensure only the authenticated user can subscribe to their own `/user/queue/notifications` destination. The use of the `/user` prefix automatically isolates sessions so that one user cannot receive another's messages, assuming the user is authenticated as a unique principal.

With the above in place, whenever `createNotification` is called (e.g., via the POST endpoint or any server logic), the notification will be saved to the database and a real-time message will be sent to the user. The frontend (if connected via WebSocket and subscribed to the proper destination) will receive it instantly.

We should also consider broadcasting notifications. For example, system-wide announcements could be sent to all users. In that case, we could use a destination like `/topic/announcements` and call `messagingTemplate.convertAndSend("/topic/announcements", message)`. Any client subscribed to that topic would get the message. In our notification system, we'll focus on user-specific notifications, but the same infrastructure can be extended for broadcasts.

### 2.3 Using JWT Authentication for Security

Our application needs to ensure that only authorized users can access notifications. We'll use JSON Web Tokens (JWT) for stateless authentication. JWT will secure both the REST APIs and the WebSocket connections.

**Overview of JWT in our App:**

- When a user logs in (this implementation detail is outside our scope), the server issues a JWT signed with a secret key. The JWT contains the user's identity (username) and possibly roles.
- The React frontend stores this token (e.g., in memory or localStorage) and includes it in the `Authorization` header for each request or handshake.
- The Spring Boot backend will validate the JWT on each request. If valid, it sets the user principal (so `authentication.getName()` returns the username). If invalid or missing, the request is unauthorized.

**Spring Security Configuration:**

Create a security config class (e.g., `WebSecurityConfig` annotated with `@Configuration` and `@EnableWebSecurity`). If using Spring Boot 3+ and Spring Security 5.7+, you can configure via a `SecurityFilterChain` bean:

```java
@Configuration
@EnableWebSecurity
public class WebSecurityConfig {
    @Autowired
    private JwtAuthFilter jwtAuthFilter; // custom filter we will create

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.cors().and().csrf().disable();

        http.authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/auth/**").permitAll()         // allow auth endpoints (if any)
                .requestMatchers("/ws/**").permitAll()           // allow WebSocket handshake endpoint
                .requestMatchers("/api/**").authenticated()      // secure the API endpoints
                .anyRequest().permitAll()
        );

        // Add JWT filter before the default UsernamePasswordAuthenticationFilter
        http.addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

Here we disable CSRF (since we're using tokens, not cookies, for auth, and also to allow WebSocket without CSRF issues). We allow unauthenticated access to any `/auth/**` endpoints (which would be login or token issuance endpoints you create) and to `/ws/**` (more on this in a moment). All `/api/**` endpoints (our notification APIs) require authentication. We then register our JWT filter to run for every request before Spring's built-in authentication processing.

**JWT Filter:**

Implement a `JwtAuthFilter` that extends `OncePerRequestFilter`. This filter will:

- Check the `Authorization` header of incoming HTTP requests.
- If a JWT is present, validate it (using a JWT library or custom code).
- If valid, set the authenticated user in the security context.

For example:

```java
@Component
public class JwtAuthFilter extends OncePerRequestFilter {
    private String jwtSecret = "MySuperSecretKey"; // in real app, use secure config

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            try {
                // TODO: validate the token (e.g., parse claims, verify signature & expiration)
                String username = JwtUtil.validateTokenAndGetUsername(token); // pseudo-code
                // If token is valid, create an Authentication and set it
                UsernamePasswordAuthenticationToken auth =
                        new UsernamePasswordAuthenticationToken(username, null, List.of());
                SecurityContextHolder.getContext().setAuthentication(auth);
            } catch (Exception e) {
                // Invalid token - optionally, you can set an error attribute or send an error response here
            }
        }
        // Continue filter chain
        filterChain.doFilter(request, response);
    }
}
```

In the above, `JwtUtil.validateTokenAndGetUsername(token)` represents logic using a JWT library (like io.jsonwebtoken's Jwts parser or the JWT decoder from Spring Security's oauth2resource server) to verify the token signature and extract the username. We then create an `Authentication` object with that username (and normally you'd fetch authorities/roles too) and set it in the `SecurityContext`. If no token or an invalid token is present, we just proceed without setting auth (which means later, access will be denied by our security config for protected URLs).

**Securing WebSocket Connections:**

WebSocket connections do not use the `Authorization` header in the same way as HTTP calls. However, our goal is to ensure only authenticated users connect and receive messages. Spring Security's WebSocket support expects authentication to be established during the HTTP handshake (transport level) or through an authenticated session ([JSON Web Token (JWT) with Spring based SockJS / STOMP Web ...](https://stackoverflow.com/questions/30887788/json-web-token-jwt-with-spring-based-sockjs-stomp-web-socket#:~:text=,level%20authentication)). Since we're stateless and using JWT, there's no session. We must manually propagate the JWT during the WebSocket handshake and verify it.

One way to do this:

- When the client tries to connect via STOMP/WebSocket, include the JWT in the connection headers (this will be shown in the frontend section).
- Implement a `ChannelInterceptor` in the WebSocket configuration to intercept the CONNECT frame and authenticate it.

For example, in `WebSocketConfig`, add:

```java
@Override
public void configureClientInboundChannel(ChannelRegistration registration) {
    registration.interceptors(new ChannelInterceptor() {
        @Override
        public Message<?> preSend(Message<?> message, MessageChannel channel) {
            StompHeaderAccessor accessor = StompHeaderAccessor.wrap(message);
            if (StompCommand.CONNECT.equals(accessor.getCommand())) {
                String authHeader = accessor.getFirstNativeHeader("Authorization");
                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    String token = authHeader.substring(7);
                    // Validate JWT (similar to JWT filter)
                    String username = JwtUtil.validateTokenAndGetUsername(token); // pseudo-code
                    if (username != null) {
                        // Set user authentication for the WebSocket session
                        Authentication auth = new UsernamePasswordAuthenticationToken(username, null, List.of());
                        accessor.setUser(auth);
                    } else {
                        // If token is invalid, prevent connection by returning null
                        return null;
                    }
                }
            }
            return message;
        }
    });
}
```

What this does: when a CONNECT message comes in through the WebSocket channel, it checks for an "Authorization" header. If present, it strips "Bearer " and validates the token. If valid, it sets the `user` property of the `StompHeaderAccessor`, which effectively associates an authenticated `Principal` with the WebSocket session. Later, when we call `convertAndSendToUser(recipient, ...)`, Spring will compare the recipient to the `Principal.getName()` of connected sessions to route messages properly.

The `.requestMatchers("/ws/**").permitAll()` in our HTTP security config above means we are not blocking the handshake at the HTTP level (since we handle token auth in the CONNECT at message level instead). If you prefer, you could also attempt to authenticate during the handshake by customizing the handshake handler, but the interceptor approach above is simpler for our JWT scenario.

**Issuing JWTs (Authentication Endpoint):**

For completeness, you would have an endpoint like `POST /auth/login` where the user provides credentials, and if valid, you generate a JWT (using a library) and return it. The details of user storage and password checking are beyond this guide, but you can use Spring Security's authentication manager with an in-memory or database user details service. After authenticating, generate a token (signing it with a secret or private key).

For example, using the JJWT library:

```java
String token = Jwts.builder()
    .setSubject(username)
    .setExpiration(new Date(System.currentTimeMillis() + JWT_EXPIRATION_MS))
    .signWith(SignatureAlgorithm.HS512, jwtSecret)
    .compact();
```

Return this token to the client, which will use it for subsequent requests.

Now, with JWT security in place:

- The REST controller methods (like `getUserNotifications`) will only execute if a valid JWT is provided. The `Authentication` object passed to the controller contains the user's details (we used username as principal).
- The WebSocket `simpMessagingTemplate.convertAndSendToUser` will only deliver messages to sessions where the principal name matches the target username (because we set the `accessor.setUser(auth)` on connect).

This ensures that User A cannot receive User B's notifications, and that an unauthenticated client cannot connect to receive any notifications.

### 2.4 Database Configuration (PostgreSQL/MySQL)

With the code in place, we need to configure the database so that our Notification entity is persisted. We will use either PostgreSQL or MySQL as mentioned. In your Spring Boot application's configuration (in `src/main/resources/application.properties` or `.yml`), set the connection properties for your database.

For example, for **PostgreSQL**:

```
spring.datasource.url=jdbc:postgresql://localhost:5432/notifications_db
spring.datasource.username=postgres
spring.datasource.password=yourpassword
spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

For **MySQL**, it would be similar, with the URL, username, password, and the MySQL dialect:

```
spring.datasource.url=jdbc:mysql://localhost:3306/notifications_db
spring.datasource.username=root
spring.datasource.password=yourpassword
spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
```

Make sure you have created a database named `notifications_db` (or any name you used in the URL) in your database server, and that the credentials match. The `ddl-auto=update` setting tells Hibernate to automatically create or update database tables to match the entities. This is convenient in development so that when you run the application, a table `notifications` with appropriate columns will be created. In production, you might use `validate` or handle schema migrations manually for safety.

Since we included the database driver dependency (via Initializr), Spring Boot will attempt to connect to the database on startup. If the connection fails (wrong URL or DB not running), the application will not start. So ensure the database server is running and accessible.

**Test the Repository:** After configuring, you can run the application and perhaps use the POST endpoint to add a notification and then GET to retrieve it, confirming that the data is being stored and retrieved from the database.

**Switching Databases:** The configuration is database-specific, but our code (using Spring Data JPA) is database agnostic. If you want to use MySQL instead of PostgreSQL, include the MySQL driver dependency and adjust the URL and dialect as shown. The rest of the code remains the same.

At this point, our backend is complete with REST APIs, WebSocket messaging, security, and persistence. Next, we will build the frontend to interact with these backend capabilities.

## 3. Frontend Development (ReactJS)

Now that the backend is up and running, we will build the frontend user interface using React and Material-UI. The frontend will allow users to see their notifications, get real-time updates via WebSockets, and interact (like marking notifications as read). We'll also manage the notification state on the client side using a global state container (Redux or React Context).

### 3.1 Setting up React and Material-UI

We already created the React project using Create React App (in section 1.2). Before implementing the notification features, let's integrate Material-UI and set up a basic layout:

- Ensure Material-UI (MUI) is installed (`@mui/material`, `@mui/icons-material`, and Emotion for styling) – which we did in section 1.2.
- Plan the UI structure. We'll likely have a top navigation bar that includes a notifications icon (bell). When clicked, it will show a dropdown list of notifications. We will use MUI components like `AppBar`, `Toolbar`, `IconButton`, `Badge`, and `Menu` to build this.

**App Layout:**

In your main App component (e.g., `App.js`), you can create a simple AppBar:

```jsx
import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";
import NotificationMenu from "./NotificationMenu";

function App() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          My Application
        </Typography>
        {/* Notification icon/menu in the top-right corner */}
        <NotificationMenu />
      </Toolbar>
    </AppBar>
    /* Possibly other components or routes */
  );
}

export default App;
```

This creates a header bar with a title on the left and the notifications menu component (which we'll create next) on the right.

We choose to implement the notifications UI as a separate `NotificationMenu` component for clarity.

### 3.2 Implementing the Notification Icon and Menu

The `NotificationMenu` component will display a bell icon with a badge indicating the number of unread notifications. Material-UI provides a `Badge` component to easily show counts on icons ([How to create Badges in Material-UI React - WebDevAssist](https://www.webdevassist.com/reactjs-materialui/material-ui-badge#:~:text=WebDevAssist%20www.webdevassist.com%20%20Material,a%20badge%20on%20that%20icon)). We can wrap a bell icon (from Material Icons) with `Badge` to display the unread count.

Let's implement `NotificationMenu.js`:

```jsx
import React, { useState } from "react";
import { IconButton, Badge, Menu, MenuItem, ListItemText } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";
import { useSelector, useDispatch } from "react-redux"; // if using Redux

function NotificationMenu() {
  const [anchorEl, setAnchorEl] = useState(null);
  const dispatch = useDispatch();
  const notifications = useSelector((state) => state.notifications.items);

  // Calculate unread count
  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleIconClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // When a notification is clicked, mark it as read
  const handleNotificationClick = (notification) => {
    // Dispatch Redux action to mark as read in state
    dispatch({ type: "notifications/markRead", payload: notification.id });
    // Also call backend API to mark as read
    fetch(`/api/notifications/${notification.id}/read`, {
      method: "PUT",
      headers: { Authorization: "Bearer " + localStorage.getItem("jwt") },
    });
    // Close menu (optional: you might keep it open to allow multiple reads)
    setAnchorEl(null);
  };

  return (
    <>
      <IconButton color="inherit" onClick={handleIconClick}>
        <Badge badgeContent={unreadCount} color="secondary">
          <NotificationsIcon />
        </Badge>
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{ style: { maxHeight: 300, width: "300px" } }}
      >
        {notifications.length === 0 ? (
          <MenuItem disabled>You have no notifications</MenuItem>
        ) : (
          notifications.map((notification) => (
            <MenuItem
              key={notification.id}
              onClick={() => handleNotificationClick(notification)}
              selected={!notification.read} // highlight if unread
            >
              <ListItemText
                primary={notification.content}
                secondary={new Date(notification.timestamp).toLocaleString()}
                // Unread notifications could be shown in bold
                primaryTypographyProps={{
                  fontWeight: notification.read ? "normal" : "bold",
                }}
              />
            </MenuItem>
          ))
        )}
      </Menu>
    </>
  );
}

export default NotificationMenu;
```

A breakdown of this component:

- We use `IconButton` with a `NotificationsIcon` wrapped in a `Badge`. The `badgeContent={unreadCount}` will display a small circle with the number of unread notifications. The badge automatically positions itself on the top-right of the icon.
- We maintain local state `anchorEl` to control the MUI `Menu` (dropdown). When the icon is clicked, we set the anchor (open the menu), and clicking outside or selecting an item will close it.
- We retrieve notifications from a global state (here via Redux's `useSelector`). We'll discuss setting up this state in section 3.4. For now, assume `notifications` is an array of notification objects the frontend knows about.
- We compute `unreadCount` by filtering the notifications where `read` is false.
- The Menu displays each notification as a `MenuItem`. We use `ListItemText` to display the content and a formatted timestamp. If a notification is unread, we visually distinguish it (e.g., by bold text or using the `selected` prop to highlight).
- On clicking a notification, we dispatch an action to mark it read in our state and also send a request to the backend (`PUT /api/notifications/{id}/read`) to mark it as read in the database. We include the JWT in the request header for authentication. (Here, for simplicity, we assume the JWT is stored in `localStorage` under key 'jwt'; in a real app, you might use a context or Redux store for the auth token or a hook to get it.)
- We close the menu after handling the click. (Alternatively, one might keep the menu open to allow marking multiple items and add an explicit close button or auto-close when it loses focus.)

This UI gives the user a way to see notifications and their read status. Next, we need to load notifications and listen for new ones in real-time.

### 3.3 Fetching Notifications and Real-Time Updates via WebSockets

When the app loads, we should fetch existing notifications from the backend and then set up a WebSocket connection to receive new notifications in real-time.

**Fetching existing notifications:**

In a React application, a good place to load initial data is within a `useEffect` hook in a top-level component (like `App` or a dedicated context provider). If the user is already authenticated with a JWT, we can call the GET notifications API we built.

For example, in `App.js` (or in a custom hook or context that runs on mount):

```jsx
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    // Assume JWT is stored in localStorage
    const token = localStorage.getItem('jwt');
    if (token) {
      fetch('/api/notifications', {
        headers: { 'Authorization': 'Bearer ' + token }
      })
      .then(res => res.json())
      .then(data => {
        // data is the list of notifications
        dispatch({ type: 'notifications/setAll', payload: data });
      });
    }
  }, [dispatch]);
  ...
}
```

This uses a relative URL (`/api/notifications`). During development, if your React dev server is running on port 3000, you'll either need to configure a proxy (so that `/api` calls are forwarded to `localhost:8080`) or enable CORS on the backend for `http://localhost:3000`. An easy solution is to add a proxy in `package.json` of the React app:

```json
  "proxy": "http://localhost:8080",
```

This way, calls from the dev server to `/api/...` will be proxied to the Spring Boot server.

After fetching, we dispatch an action `notifications/setAll` to store the notifications in our Redux store (or update context state). At this point, the user sees their current notifications (maybe none if none exist).

**Setting up the WebSocket connection:**

To receive notifications in real-time, we connect to the backend WebSocket endpoint (`/ws`) using SockJS and STOMP. We'll do this once when the app initializes and keep the connection open.

Install the STOMP client libraries in the React project if not already:

```
npm install sockjs-client stompjs
```

Now, in our app, we can create a STOMP client and subscribe to the user-specific notifications topic. We should do this in a `useEffect` that runs on mount (and clean up on unmount).

For example, in `App.js` (continuing from the previous snippet, or a new effect):

```jsx
import SockJS from 'sockjs-client';
import Stomp from 'stompjs';

function App() {
  ...
  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (!token) return; // if not logged in, skip

    // Create a SockJS connection
    const socket = new SockJS('http://localhost:8080/ws');
    // Initialize STOMP over the socket
    const stompClient = Stomp.over(socket);
    // Optionally, disable console debug logs from STOMP for cleaner output
    stompClient.debug = null;

    // Connect with JWT in header
    stompClient.connect({ Authorization: `Bearer ${token}` }, frame => {
      console.log('Connected: ' + frame);
      // Subscribe to the user notifications queue
      stompClient.subscribe('/user/queue/notifications', msg => {
        const notification = JSON.parse(msg.body);
        // Dispatch Redux action to add the new notification
        dispatch({ type: 'notifications/received', payload: notification });
      });
    }, error => {
      console.error('WebSocket error: ', error);
    });

    // Cleanup on unmount
    return () => {
      if (stompClient && stompClient.connected) {
        stompClient.disconnect(() => console.log('WebSocket disconnected'));
      }
    };
  }, [dispatch]);
  ...
}
```

Let's unpack this:

- We create a SockJS client pointing to our backend `/ws` endpoint (make sure the URL matches exactly the endpoint configured in Spring Boot, including the correct protocol/host/port).
- We get a STOMP client wrapper by calling `Stomp.over(socket)`. (Note: If using the newer `@stomp/stompjs` library, the syntax differs slightly, but the concept is the same.)
- We pass the Authorization header with the Bearer token when calling `connect`. This ensures our backend's handshake interceptor receives the JWT (as we implemented in section 2.3).
- On successful connection (the `frame` callback), we subscribe to `/user/queue/notifications`. This is the destination where our backend will send user-specific notifications. The STOMP client automatically knows the user context (because we provided the token and Spring set the user), so `/user/queue/notifications` will map to this user's personal queue on the server.
- When a message is received on that subscription, the callback is executed. We parse the message body (which should be the notification data in JSON) and dispatch an action to add this notification to our state.
- We also handle a connection error (logging it) and ensure to disconnect the client if the component unmounts (to avoid memory leaks or multiple connections if the component re-mounts, though in our single-page app scenario, App unmounting is unlikely except on logout).

Now, whenever the backend sends a notification via WebSocket (e.g., when a new Notification is created for the user), the subscribed callback will dispatch an update. The Redux store will update the notifications list, and because our `NotificationMenu` component uses `useSelector` to get notifications, it will automatically re-render and show the new notification (and the badge count will increment).

**Real-time Read Status Update:** If notifications can be marked read on one client and you want others (or other tabs of the same user) to update, you could also send a WebSocket message for read updates. However, in this single-client scenario, updating state locally on click is sufficient. The next time the user fetches notifications (or if they reconnect), they will get the updated read status from the DB.

We have now connected the frontend to the backend: initially loading notifications and then receiving new ones in real time.

### 3.4 Managing State with Redux (or Context)

To manage the notifications data across the application, we use a global state container. This ensures that, for example, the notifications icon in the header and a notifications page or dropdown share the same data source.

**Using Redux:** Redux is a popular state management library that provides a single source of truth for application state ([javascript - Redux - multiple stores, why not? - Stack Overflow](https://stackoverflow.com/questions/33619775/redux-multiple-stores-why-not#:~:text=REDUX%20HAS%203%20MAIN%20PRINCIPLES%3A,2)). We already saw usage of `useDispatch` and `useSelector` from the Redux library in the code above. To set this up:

- Install Redux and React-Redux:
  ```
  npm install redux react-redux
  ```
- Create a Redux store. For simplicity, we can create a store with a single reducer for notifications. For example, create `store.js`:

  ```jsx
  import { createStore } from "redux";

  const initialState = { notifications: { items: [] } };

  function rootReducer(state = initialState, action) {
    switch (action.type) {
      case "notifications/setAll":
        return { ...state, notifications: { items: action.payload } };
      case "notifications/received":
        // Add new notification to the front of the list
        return {
          ...state,
          notifications: {
            items: [action.payload, ...state.notifications.items],
          },
        };
      case "notifications/markRead":
        return {
          ...state,
          notifications: {
            items: state.notifications.items.map((notif) =>
              notif.id === action.payload ? { ...notif, read: true } : notif
            ),
          },
        };
      default:
        return state;
    }
  }

  const store = createStore(rootReducer);
  export default store;
  ```

  This is a very basic Redux setup. In a larger app, you might use Redux Toolkit to simplify the syntax or split reducers, but the above is clear for understanding.

  The reducer handles:

  - Setting all notifications (replacing the array) on initial fetch.
  - Adding a received notification to the front of the array.
  - Marking a notification as read by updating the corresponding item.

- Provide the store to the React app. In `index.js` (entry point):

  ```jsx
  import React from "react";
  import ReactDOM from "react-dom";
  import { Provider } from "react-redux";
  import store from "./store";
  import App from "./App";

  ReactDOM.render(
    <Provider store={store}>
      <App />
    </Provider>,
    document.getElementById("root")
  );
  ```

Now any component can connect to the store. In our case, `NotificationMenu` uses `useSelector` to get the notifications array and `useDispatch` to modify it.

Whenever a new notification comes in via WebSocket, we dispatch `notifications/received` with the notification data, and the reducer adds it to the state. The components will reflect this change (unread count goes up, new item appears in menu). When the user clicks a notification, we dispatch `notifications/markRead`, and the reducer updates that item to `read: true` (so we can style it differently and reduce the unread count). We also call the backend to update the database, but that doesn't directly affect the UI state since we've already updated it optimistically.

**Using React Context (alternative):** If you prefer not to add Redux, you can achieve a similar result with the Context API:

- Create a `NotificationContext` with `React.createContext()`.
- Provide a context provider component that holds state (using `useReducer` or `useState`) for notifications and functions to update it (like addNotification, markAsRead).
- Use the provider at a high level (like in App) to wrap the component tree.
- Use `useContext(NotificationContext)` in child components to access notifications and dispatch updates.

For example, using `useReducer`:

```jsx
const NotificationContext = React.createContext();

function notificationReducer(state, action) {
  switch (
    action.type
    // similar cases as Redux reducer
  ) {
  }
}

export function NotificationProvider({ children }) {
  const [state, dispatch] = useReducer(notificationReducer, { items: [] });
  const value = { notifications: state.items, dispatch };
  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}
```

Then in `index.js`:

```jsx
ReactDOM.render(
  <NotificationProvider>
    <App />
  </NotificationProvider>,
  document.getElementById("root")
);
```

And in `NotificationMenu` (or any component needing it):

```jsx
const { notifications, dispatch } = useContext(NotificationContext);
```

You would then use this `dispatch` similarly to trigger state changes. The logic remains much the same; the difference is you're not using an external library. Context is fine for moderate complexity, but Redux may provide better structure for larger apps or more complex state interactions. Since this guide is for advanced users, we've demonstrated Redux, but both approaches are valid.

**State Management Summary:** Both Redux and Context achieve our goal of sharing state across components. Redux emphasizes a single store for the whole app state, making it predictable and easier to debug (with tools like Redux DevTools). Context integrates smoothly with React but can become cumbersome if not organized well for very large state or many update patterns. For an advanced user, the choice often comes down to personal/team preference and app needs. In either case, ensure your state updates are immutably handled (as we did) to avoid unexpected bugs.

At this stage, our frontend can:

- Display notifications with a Material-UI interface.
- Show unread counts and differentiate unread vs read.
- Fetch initial notifications from the backend via REST.
- Receive new notifications in real-time via WebSocket and update the UI immediately.
- Allow the user to mark notifications as read, updating both frontend state and backend status.

Next, we will look at additional features of the notification system, testing, and eventually deployment considerations.

## 4. Notification System Features

We have laid the groundwork for the notifications system. Now let's delve into some key features and design considerations that make the notification system robust and user-friendly: notification types, read/unread handling, and data storage.

### 4.1 Types of Notifications

In many applications, not all notifications are the same. We often have categories such as:

- **Alerts** – critical notifications that might need immediate attention (e.g., security alerts, errors).
- **Messages** – notifications that indicate someone sent a message or comment.
- **System Updates** – general information from the system (e.g., "Your profile was viewed", "New version available").

Designing for multiple notification types involves:

- **Defining Types**: In the backend, we included a `type` field in the `Notification` entity. It could be a string or an enum. For better type safety, you can define an enum in Java (e.g., `public enum NotificationType { ALERT, MESSAGE, UPDATE }`) and use it in the Notification entity. This ensures the type is one of the known values.
- **Differentiating Behavior**: Different types might have different handling. For instance, clicking a "MESSAGE" notification might navigate the user to a messaging screen or open a conversation, whereas clicking an "ALERT" might open a specific alert details page or modal. Plan how your frontend will know what to do for each type. One approach is to include additional data in the notification payload, such as a URL or reference ID (e.g., a message ID or link) that the UI can use to route the user appropriately.
- **UI Indicators**: You might want to visually distinguish types. For example, use different icons or colors in the notification list (a mail icon for messages, a warning icon for alerts, etc.). With Material-UI, you can include an icon next to the text in each MenuItem based on `notification.type`. Perhaps use a `<Mail>` icon for "MESSAGE" type and a `<Warning>` icon for "ALERT" type, etc., to give a visual cue.

  For example, to incorporate this in UI, you might adjust the notification list rendering:

  ```jsx
  {
    notification.type === "MESSAGE" && (
      <MailIcon fontSize="small" style={{ marginRight: 8 }} />
    );
  }
  {
    notification.type === "ALERT" && (
      <WarningIcon
        fontSize="small"
        style={{ marginRight: 8, color: "orange" }}
      />
    );
  }
  {
    notification.content;
  }
  ```

  This would prepend an icon to the content text for certain types.

On the backend, using the `type` field, you could route how notifications are created or processed:

- If you have different triggers, for example, a new message in a chat triggers a `"MESSAGE"` notification, whereas a system event triggers an `"ALERT"`, you might have separate service methods to handle each scenario (as hinted in the code snippet in section 2.1). This isn’t strictly necessary, but it can help keep logic organized.

Having clear notification types makes it easier to filter notifications (maybe the UI allows filtering by type), and helps users prioritize (often critical alerts are highlighted differently).

### 4.2 Handling Read/Unread State

Marking notifications as read or unread is crucial to help users identify new notifications. We have implemented a simple mechanism:

- Each notification record has a boolean `read` flag, defaulting to false (unread).
- When the user views or clicks a notification, we mark it as read (both in the UI state and via an API call to update the database).

There are different strategies to manage read status:

- **Mark on click (explicit)**: This is what we implemented – the user explicitly clicks a notification entry to mark it as read (or triggers a specific action).
- **Mark on open (implicit)**: Some systems mark all notifications as read as soon as the notification dropdown or page is opened, under the assumption that opening the list implies the user has seen them. This is easier to implement (just one API call to mark all as read when the user opens the list). However, it can mark items read that the user didn't actually look at, which might not be desired in all cases.
- **"Mark all as read" option**: It's useful to provide an option (e.g., a button in the UI) for "Mark all as read", allowing the user to clear the badge in one action. This would require a corresponding API endpoint to mark all of a user's notifications as read.

In our design:

- We chose to mark individually on click, which gives the user control. We could add a small "Mark all as read" button at the bottom of the menu if needed, which would call a new endpoint (e.g., `PUT /api/notifications/mark-all-read`) that the backend should implement (looping through user's notifications to update the flag, or preferably using a batch query).
- The unread count is simply the count of notifications with `read=false` for that user. The backend can provide this count as a separate endpoint (for efficiency) or the frontend can compute after fetching notifications. Given our implementation fetches all notifications anyway, we computed on the client side. Alternatively, an endpoint like `/api/notifications/unread-count` could return just the number, which is useful if the client wants to poll for count without fetching all data.

Another consideration is syncing read status across devices or tabs. If a user has the app open on multiple devices or in multiple browser tabs, marking a notification as read in one should update others. Our backend can help achieve this by:

- When a notification is marked read (via the PUT endpoint), not only update the DB but also send a WebSocket message to the user (similar to how we send new notifications) indicating that a particular notification was read. The client could listen for such messages (perhaps on the same `/user/queue/notifications` channel or a separate channel for updates) and update state accordingly (e.g., set that notification's `read` to true in state).
- In our current setup, we did not implement a separate WebSocket notification for read events (to keep things simpler), but it is a feasible extension. Given that marking read isn't as time-sensitive as receiving new notifications, some systems might just rely on the next refresh or user action to update other views. It's a UX decision.

**Badge Behavior:** Typically, the badge count (unread count) will reset to zero when all notifications are marked read. In our UI, once we mark items as read, the count will decrement accordingly. If we were doing "mark on open", we would simply set all to read and thus the count would drop to 0 immediately when the menu opens (and possibly not show which ones were unread since they all flip to read).

Our chosen approach is explicit marking, which is often clearer to users. They control when a notification is marked read (by clicking it). If needed, we could consider marking as read when the user _closes_ the menu, assuming by then they've seen them. Again, this is a UX nuance.

### 4.3 Storing Notifications in the Database

Storing notifications persistently allows users to retrieve past notifications and ensures no data is lost if the user is offline. We have set up a relational database with a `notifications` table via JPA. Some important points regarding storage:

- **Schema**: The Notification table typically has columns for id (primary key), type, content, recipient (and/or recipient_id if linking to a users table), timestamp, and read flag. We might also store related data like a reference link or additional metadata (for example, if a notification relates to a specific entity like an Order or Message, we might store that entity ID).
- **User Relationship**: In our simplified model, we used a `recipient` string. In a real application, you'd likely have a `User` table and a foreign key relationship. For instance, the Notification entity could have `@ManyToOne private User recipient;` instead of a string. This would let JPA handle joining notifications to users. We omitted that to keep the focus, but it's a good enhancement if user management is in scope. With a foreign key, you could also easily query things like "all unread notifications for all users", etc.
- **Offline Scenario**: Because notifications are stored in the DB, if a user was offline when a notification was sent, they will fetch it on next login. This is essential for a reliable notification system. The real-time WebSocket is just an enhancement for immediacy. The DB is the source of truth for what notifications a user has.
- **Size and Cleanup**: Over time, notifications can accumulate. Depending on the nature of your app, you might prune old notifications. For example, you might decide to only keep the last 1000 notifications per user, or delete notifications older than 1 year. This could be done with a scheduled job or on-demand. Alternatively, you might move old notifications to an "archive" table or storage if they need to be retained for compliance or history.
- **Database Indexing**: Ensure you have an index on the `recipient` field (and possibly on `read` in combination if you often query unread notifications). In JPA, you can use `@Index` on the entity or add the index via a schema migration. An index on recipient will make `findByRecipientOrderByTimestampDesc` efficient even as the table grows.
- **Transaction Management**: Our simple service methods rely on Spring's transaction management (the repository calls are wrapped in a transaction by default since it's a single operation). If you expand functionality, ensure that creating a notification and sending via WebSocket are in the appropriate transactional context. In our code, once `repo.save(notif)` completes successfully, then we send the WebSocket message. If the save fails for some reason, we wouldn't want to send a notification that isn't in the DB, which is handled by the code order.

**Alternate Storage Options:** While a relational DB works for many cases, consider if your use-case might benefit from alternatives:

- For extremely high volume or distributed systems, a NoSQL store (like MongoDB, DynamoDB) might be used for notifications. These can simplify some aspects (e.g., storing a JSON document per notification) but complicate others (like querying and relationships). Often, NoSQL is chosen if you need to handle a firehose of events or flexible schema.
- Some architectures use a message queue or event streaming platform (like Kafka) to log notifications events. Consumers can then store them in DB or push them as needed. This is usually for very high-scale or for decoupling the generation of notifications from their storage and delivery.
- For our scenario, the relational DB with JPA is sufficient and convenient.

In summary, we have implemented support for multiple notification types, maintained read/unread status per notification, and stored everything in a reliable database. These features ensure that users have a clear and persistent view of their notifications across sessions and devices.

## 5. Testing and Debugging

Building a complex application requires thorough testing and effective debugging strategies, especially for features like real-time notifications that span the backend and frontend. In this section, we outline how to test both the Spring Boot backend and the React frontend, and offer tips for debugging WebSocket communications.

### 5.1 Backend Testing (Unit and Integration Tests)

**Unit Testing Services and Components:**

- _Service Layer:_ Write JUnit tests for `NotificationService`. You can use Mockito to mock the `NotificationRepository`. For example, test that `getNotificationsForUser("alice")` calls `repo.findByRecipientOrderByTimestampDesc("alice")` and returns the expected result (you can simulate repository returning a list of notifications). Similarly, test that `markAsRead(id)` actually changes the `read` flag by verifying that `repo.save` is called with a notification whose `read` is true.
- _Repository Layer:_ Since we're using Spring Data JPA, you generally don't test the repository methods themselves (they are provided by the framework), but you can write a **slice test** with `@DataJpaTest` to ensure the JPA mapping and query methods work as expected with an in-memory database. For example, using H2 in tests, save a few Notification entities via the repository and then verify `findByRecipientOrderByTimestampDesc` returns them in the right order.
- _Controller Layer:_ Use Spring's MockMvc (from `spring-boot-starter-test`) to perform requests against the controller in a test context. You can load the controller (and perhaps security config) with `@WebMvcTest(NotificationController.class)` and mock the service. Then test:
  - Unauthorized access returns 401. (You might need to apply Spring Security to MockMvc; Spring Security Test offers `@WithMockUser` to simulate an authenticated user.)
  - With a mock authenticated user, a GET `/api/notifications` returns a JSON array of notifications. You can set up the mock service to return a list of Notification objects, then use MockMvc to perform the GET and expect JSON content that matches that list (using JSONPath or basic contains).
  - Test that POST `/api/notifications` with a given request body calls `notificationService.createNotification` with correct params and returns the saved Notification in the response.
  - For the WebSocket part, testing can be a bit more involved (see below), but you might not unit-test that in isolation since it's more of an integration concern. However, you could test that `NotificationService.createNotification` calls `messagingTemplate.convertAndSendToUser` (by injecting a mock SimpMessagingTemplate in the service for test).

**Integration Testing WebSocket:** Full end-to-end testing of WebSockets can be done with Spring's integration test support:

- Spring provides a `WebSocketStompClient` that you can use in tests to connect to your WebSocket endpoint. You can spin up the server using `@SpringBootTest(webEnvironment=SpringBootTest.WebEnvironment.RANDOM_PORT)` and then use the stomp client to connect to `ws://localhost:{randomPort}/ws` and subscribe to `/user/queue/notifications`.
- In such a test, you might simulate sending a notification: for example, call the REST endpoint to create a notification, or directly invoke the service. Then, the stomp client subscription should receive a message. You can use latches or CompletableFutures in tests to wait for the message.
- Handling authentication in WebSocket tests: You could configure the test's Stomp client with the same JWT header approach (you might generate a JWT for a known test user, or disable the security in a profile for testing the WS). Alternatively, you can simplify by disabling the ChannelInterceptor in a test profile and allowing all connects (since in integration tests you might focus on functionality not security).
- Spring's documentation mentions two main approaches for testing STOMP over WebSocket: writing **server-side tests** (testing the controller methods or messaging template in isolation) or **end-to-end tests** with a client ([Testing :: Spring Framework](https://docs.spring.io/spring-framework/reference/web/websocket/stomp/testing.html#:~:text=Testing%20%3A%3A%20Spring%20Framework%20There,side%20tests)). For our scenario, since our controller is minimal (we don't have a @MessageMapping), end-to-end testing would be about verifying the messaging flow.

**Testing Security Configuration:** Use Spring Security's test support to verify that security rules are enforced:

- You can write tests with MockMvc to ensure that without authentication, calls to `/api/notifications` are unauthorized (status 401 or 403).
- With a valid JWT, you can either manually set the header in MockMvc (`header("Authorization", "Bearer ...")`) if you have a way to generate a test token, or use `@WithMockUser` on the test method to simulate an authenticated user (bypassing JWT for test). For example:
  ```java
  @Test
  @WithMockUser(username="alice")
  public void testGetNotificationsAuthorized() throws Exception {
      // given notificationService returns some list
      when(notificationService.getNotificationsForUser("alice"))
          .thenReturn(List.of(new Notification(...)));
      mockMvc.perform(get("/api/notifications"))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.length()").value(1));
  }
  ```
  This avoids needing a real JWT in the test environment.
- Similarly, test that connecting to `/ws` without a token might be allowed (since we permit it), but if you wanted to test the ChannelInterceptor, you could simulate a CONNECT message. This is low-level, though; often it's sufficient to test the outcome (that an unauthorized connect gets no messages, etc., which is tricky to automate).

**Test Database Considerations:** For repeatable tests, use an in-memory database (H2) or a testcontainer for PostgreSQL. With `@DataJpaTest`, Spring will auto-configure H2 (if on classpath) and even set `ddl-auto` to create-drop by default. This ensures each test method has a fresh schema.

The backend tests ensure each piece works and that overall the API and WebSocket behave as expected (within the limits of what can be automated). They also guard against regressions when you refactor code.

### 5.2 Frontend Testing (React)

For the React application, you can use Jest and React Testing Library (which come with Create React App) to test components and logic:

- **Component Rendering and Behavior:** Write tests for `<NotificationMenu />`. You might need to wrap it with a Redux provider for the state. One approach is to use the `render` method from `@testing-library/react` with a custom wrapper that provides the store.
  For example:

  ```jsx
  import { render, fireEvent, screen } from "@testing-library/react";
  import { Provider } from "react-redux";
  import configureStore from "redux-mock-store";
  import NotificationMenu from "./NotificationMenu";

  const mockStore = configureStore([]);
  test("displays unread count and notifications list", () => {
    const initialNotifications = [
      { id: 1, content: "Test 1", read: false, timestamp: Date.now() },
      { id: 2, content: "Test 2", read: true, timestamp: Date.now() },
    ];
    const store = mockStore({ notifications: { items: initialNotifications } });
    render(
      <Provider store={store}>
        <NotificationMenu />
      </Provider>
    );
    // badge should show '1' (one unread)
    const badge = screen.getByText("1");
    expect(badge).toBeInTheDocument();

    // Click the icon to open menu
    fireEvent.click(screen.getByRole("button"));
    // Now the menu items should be visible
    expect(screen.getByText("Test 1")).toBeInTheDocument();
    expect(screen.getByText("Test 2")).toBeInTheDocument();
  });
  ```

  This test checks that the badge content is correct and that after clicking the icon (simulated by `fireEvent.click` on the button role), the notifications text appear.

- **Reducer Testing:** If your reducer logic is complex, test it separately. We can test that actions produce the expected new state:

  ```jsx
  import reducer from "./store";
  it("should add a new notification on received", () => {
    const initialState = { notifications: { items: [] } };
    const newNotif = { id: 5, content: "Hello", read: false };
    const newState = reducer(initialState, {
      type: "notifications/received",
      payload: newNotif,
    });
    expect(newState.notifications.items.length).toBe(1);
    expect(newState.notifications.items[0]).toEqual(newNotif);
  });
  it("should mark notification as read", () => {
    const initialState = {
      notifications: { items: [{ id: 5, content: "Hello", read: false }] },
    };
    const newState = reducer(initialState, {
      type: "notifications/markRead",
      payload: 5,
    });
    expect(newState.notifications.items[0].read).toBe(true);
  });
  ```

  This ensures our logic for updating state works as expected.

- **Integration Tests (optional):** Using a tool like Cypress, you could run the whole application (possibly against a test backend) to simulate real user interactions in a browser. For example, have the backend running in a test profile, use Cypress to log in, trigger a notification (maybe by calling an API endpoint directly or having a test control to create one), and then check that the notification appears in the UI and the unread count updates. This goes beyond unit testing and is more for ensuring the whole system works. It might be complex to set up with WebSockets, but you could, for instance, trigger a notification via an HTTP call and then within a few seconds check that the UI updated (since the WebSocket should deliver it).

- **Mocking WebSocket in tests:** In unit tests for components, you might not actually open a WebSocket connection. If you factor out the WebSocket logic (maybe into a custom hook like `useNotifications`), you could mock that hook in component tests. Or, in a simpler approach, you trust the backend integration tests for WebSockets and not test WebSocket communication at the component unit test level.

The goal is to test that:

- Components render correct information given certain state.
- Components call the right functions when interacted with (e.g., clicking a notification calls the fetch to mark read and dispatches action).

Using Jest mocks, you can spy on `window.fetch` to ensure it's called with the correct URL and method when `handleNotificationClick` is executed. For example:

```jsx
global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
);
...
fireEvent.click(screen.getByText('Test 1')); // click the first notification
expect(global.fetch).toHaveBeenCalledWith(
  expect.stringContaining('/api/notifications/1/read'),
  expect.objectContaining({ method: 'PUT' })
);
```

This would verify that our component attempted to mark notification 1 as read via the API.

- **Security in Frontend:** Not much to test here, but you might verify that if no token is present, the fetch isn't called and no WebSocket is opened. For instance, if `localStorage.getItem('jwt')` is null, the effect should skip. You can simulate that in a test by not setting up a token in localStorage and ensuring no API calls are made (spies again on fetch, or checking that state remains empty).

By combining backend and frontend tests, we cover the application fairly well. The backend tests ensure data correctness and security, and the frontend tests ensure the user interface behaves as expected. Real-time features are a bit trickier to test, but careful integration tests and manual testing can ensure those work too.

### 5.3 Debugging WebSocket Communication

Debugging WebSockets can be challenging because it involves asynchronous communication between client and server. Here are some strategies:

- **Browser DevTools Network Panel:** Most browser dev tools have a "Network" section where you can inspect WebSocket connections. For example, in Chrome, after your app initiates the WebSocket connection, you'll see an entry for it (it might show as **ws** or as the upgrade request to `/ws` with status 101 Switching Protocols). Click on that, and you'll be able to see **Frames** being sent and received. This is extremely useful to see if messages are actually arriving. You can see the content of messages (frames) and their direction (sent from client or received from server).
- **Console Logging on Client:** Add `console.log` in the STOMP client's callbacks. For instance, in our connect callback:
  ```js
  stompClient.connect(headers, frame => {
      console.log('Connected to WS');
      stompClient.subscribe(...);
  }, error => {
      console.error('WS connection error', error);
  });
  ```
  and in the subscribe:
  ```js
  stompClient.subscribe('/user/queue/notifications', msg => {
      console.log('Received WS message:', msg.body);
      ...
  });
  ```
  This way, when running the app, you can open the browser console and see the flow: whether connection succeeded and what messages were received or if an error occurred.
- **Server-side Logging:** You can enable debug logging for Spring's WebSocket and STOMP support. In `application.properties`, set:
  ```
  logging.level.org.springframework.web.socket=DEBUG
  logging.level.org.springframework.messaging.simp=DEBUG
  ```
  This will cause Spring to log details about the WebSocket handshake, subscription events, and message dispatching. For example, when a client subscribes to `/user/queue/notifications`, you might see a log like "User [username] subscribed to /user/queue/notifications". And when `convertAndSendToUser` is called, you may see logs about sending message to user destination. These logs can confirm that the server is doing what you expect.
- **Verify Subscription Destinations:** A common issue is mismatch between server and client destinations. Ensure that the server sends to `/user/{user}/queue/notifications` (which our `convertAndSendToUser` does under the hood by targeting a user and `/queue/notifications`) and the client subscribes to `/user/queue/notifications`. If, for instance, the client subscribed to `/queue/notifications` without the `/user`, they would never receive messages because those messages are being sent to user-specific queues. Remember Spring's user destinations automatically prepend an identifier, so you can't subscribe to another user's queue if you're not that user.
- **ChannelInterceptor Debugging:** If using the ChannelInterceptor for JWT, you can log inside it:
  ```java
  if (StompCommand.CONNECT.equals(accessor.getCommand())) {
      logger.info("Incoming WS connect with token: " + accessor.getFirstNativeHeader("Authorization"));
  }
  ```
  This will tell you if the token is making it to the server side. If you see `null` or it's missing, then the client didn't send it properly. If it's present but your `JwtUtil` returns null, then it might be an invalid token (maybe expired or wrong secret).
- **Test Token Manually:** If suspecting an issue with JWT in WS, try copying the JWT from your browser (e.g., from localStorage or network calls) and using a tool to decode it (like jwt.io) to ensure it's valid. Also check the backend secret and algorithm match what was used to create the token.
- **Simulate WebSocket with a Client:** You can use external tools or scripts to simulate a WebSocket client. For example, use `wscat` (a Node CLI for websockets) or write a small Node script using `stompjs` to connect to your server. This can isolate the problem (whether it's in the frontend code or server). If your script can connect and get messages, the issue is likely in the React code; if it can't, then likely server side.
- **CORS and Handshake Issues:** If the WebSocket connection isn't being established at all (no 101 Switching Protocols in network), ensure:
  - The endpoint URL is correct (including scheme: use `http://` for SockJS even if upgrading to WS).
  - The allowed origins in `WebSocketConfig` match the protocol and host of your React dev server or production domain.
  - If using HTTPS in production, the WebSocket endpoint should be `wss://` and you should allow the secure origin.
  - Sometimes proxies or firewalls can block WebSocket traffic. In development, that’s unlikely. In production, if behind a proxy (like Nginx or a cloud load balancer), ensure WebSocket upgrade headers are handled.
- **Multiple Devices/Tabs:** To debug behavior with multiple clients, open two different browsers (or one in normal and one in incognito to avoid shared localStorage) and log in as the same user (or different users if testing private messages). Trigger notifications and see if both receive appropriately. This can catch issues like missing user isolation or race conditions.

**Debugging Read/Unread Sync:** If you implemented WebSocket messages for read status, similarly test by marking read on one client and see if the message reaches the other.

**General Strategy:** When debugging, try to isolate each part:

- Is the backend sending the message? (Check server logs or debug after `convertAndSendToUser`.)
- Is the message reaching the client? (Check browser network frames or client console log.)
- Is the client handling it correctly? (Check that the Redux action fired or the state updated.)

Because our notifications rely on several pieces (DB, REST, WebSocket, Redux), careful logging and monitoring each step will pinpoint where something might be going wrong.

The combination of testing and debugging techniques above should give you confidence in building and maintaining the notification system. After verifying functionality in development, you'll be ready to consider deploying the application.

## 6. Deployment

Deploying your React + Spring Boot application involves preparing it to run in production environments, containerizing the components for consistency, and setting up infrastructure (cloud or on-premises) to host them. We'll go through Dockerizing the application, deploying to cloud (for example, AWS or a Kubernetes cluster), and automating the process with CI/CD.

### 6.1 Dockerizing the Application

**Dockerizing the Backend (Spring Boot):** Containerizing the Spring Boot app allows you to run it anywhere without worrying about the host environment's JDK or dependencies. Here's a simple Dockerfile for the Spring Boot backend:

```
# Use an official OpenJDK runtime as the base image
FROM openjdk:17-jdk-alpine
# Set working directory (optional)
WORKDIR /app
# Copy the Spring Boot jar (assuming it's built already)
COPY target/notification-backend-0.0.1-SNAPSHOT.jar app.jar
# Expose the application port
EXPOSE 8080
# Run the jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

A few notes on this Dockerfile:

- Make sure to build your Spring Boot project first (`mvn package`), so the jar is available in the `target` directory.
- You might not want to hard-code the jar name. A common practice is to use a Maven plugin or Maven build argument to specify the JAR name, or use the Maven Wrapper in the Docker build to build inside the container (multi-stage build).
- The base image `openjdk:17-jdk-alpine` is a lightweight Alpine Linux with JDK 17. In production, you might even use a JRE base image (since running the jar doesn't require the JDK). For example, `adoptopenjdk:17-jre-hotspot` or an Eclipse Temurin JRE image.
- The container will listen on port 8080 by default. We expose it for documentation purposes; you will map it to a host port or use it in a Kubernetes Service later.

**Dockerizing the Frontend (React):** For the React app, we need to build the static files and serve them. There are two common approaches:

1. **Serve with a dedicated web server (Nginx)**: Build the React app and serve the build directory with Nginx (or another static server).
2. **Serve with the backend**: Copy the React build into the Spring Boot resources and let Spring Boot serve it. (This merges front and back into one service.)

The first approach (separate frontend container) is more microservice-oriented and scalable, while the second approach simplifies deployment (one service instead of two). We will illustrate the first approach, as it's more flexible:

Create a Dockerfile for the React app (in the `notification-ui` directory):

```
# Stage 1: Build the React app
FROM node:16-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
# Copy build files to Nginx's default static directory
COPY --from=build /app/build /usr/share/nginx/html
# (Optional) Copy a custom nginx.conf if you need to handle routing for SPA
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Explanation:

- **Stage 1** uses Node to install dependencies and build the application. This results in static files in `/app/build`.
- **Stage 2** starts from an Nginx image and copies the build output into the directory Nginx serves by default. We expose port 80.
- If your React app uses client-side routing (like React Router), you'll need to configure Nginx to redirect 404s to `index.html` (so that refreshes on client routes still load the React app). That can be done by supplying a custom `nginx.conf`. If your app is simple or you handle routing differently, the default might be fine.

After writing these Dockerfiles, build the images (from the project root, for example):

```bash
# Build backend image
docker build -t myapp/notification-backend:1.0 -f notification-backend/Dockerfile ./notification-backend
# Build frontend image
docker build -t myapp/notification-frontend:1.0 -f notification-ui/Dockerfile ./notification-ui
```

Replace `myapp` with your Docker Hub username or registry as appropriate. The `-f` flag specifies the Dockerfile location, and the context (`./notification-backend` etc.) should be such that the Dockerfile can see the necessary files (like the jar or the React source).

**Docker Compose (for development or testing):** You can use Docker Compose to run the whole stack easily, especially if you also need a database container:

```yaml
version: "3"
services:
  backend:
    image: myapp/notification-backend:1.0
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/notifications_db
      - SPRING_DATASOURCE_USERNAME=postgres
      - SPRING_DATASOURCE_PASSWORD=postgres
    depends_on:
      - db
  frontend:
    image: myapp/notification-frontend:1.0
    ports:
      - "80:80"
    depends_on:
      - backend
  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=notifications_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

This Compose file:

- Runs the backend, mapping its 8080 port to host 8080.
- Runs the frontend, mapping to host port 80.
- Runs a Postgres database.
- Passes environment variables to the backend container to configure the database connection (Spring Boot will pick these up automatically if named accordingly, thanks to Spring Boot's relaxed binding of env vars to properties) ([How to set 'spring.datasource.url' inside a Docker Container](https://stackoverflow.com/questions/66169935/how-to-set-spring-datasource-url-inside-a-docker-container#:~:text=Container%20stackoverflow,to%20dynamically%20set%20these%20variables)).
- The `depends_on` ensures the backend waits for the db (though you might still need retry logic or `SPRING_DATASOURCE_URL` with `?loginTimeout=5` etc., but for simplicity, it's okay).

In production, you might not use docker-compose, but rather separate services. However, docker-compose is great for local testing or a simple single-machine deployment.

**Alternative: Single Jar Deployment:** If not using Docker, you could just deploy the Spring Boot jar on a server (or a service like Heroku) and serve the React build via an object storage or CDN. But using Docker is more standard for modern deployment (especially if aiming for Kubernetes or container services).

Now that we have container images, let's discuss deploying on cloud platforms or Kubernetes.

### 6.2 Deploying to AWS and/or Kubernetes

**AWS ECS (Elastic Container Service):** With Docker images, you can push them to Amazon Elastic Container Registry (ECR) and deploy using ECS:

- Create an ECR repository for each image and push your images there (or use Docker Hub, but many enterprises use ECR for AWS deployments).
- Define an ECS Task Definition for the backend and frontend. Each will reference the respective image and set needed environment variables. For the backend, you'll provide the database connection info (likely pointing to an AWS RDS database endpoint).
- Use AWS Fargate to run tasks without managing EC2 servers. You'd create an ECS Service for the backend (1 or more tasks), and one for the frontend.
- For networking, you'd typically place these in the same VPC. The frontend service could be internet-facing (if it's serving the UI directly). Alternatively, you might host the frontend on AWS S3 + CloudFront if it's purely static.
- The backend service would likely be in a private subnet (not directly exposed), and you would configure a load balancer or API gateway if it needs to be accessible. If the frontend is separate, the frontend will call the backend via a load balancer DNS.
- **AWS Elastic Beanstalk** is a simpler alternative if you don't want to manually manage ECS. You can give Elastic Beanstalk a Docker Compose file or even a code base and it can manage deploying both containers. It simplifies some aspects at the cost of flexibility.

**AWS EKS (Kubernetes on AWS):** If you prefer Kubernetes:

- Push images to a registry (ECR or Docker Hub).
- Write Kubernetes Deployment manifests for backend and frontend, and Service manifests for each. For example:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata: { name: notification-backend }
  spec:
    replicas: 2
    selector: { matchLabels: { app: notification-backend } }
    template:
      metadata: { labels: { app: notification-backend } }
      spec:
        containers:
          - name: backend
            image: myapp/notification-backend:1.0
            ports: [{ containerPort: 8080 }]
            env:
              - name: SPRING_DATASOURCE_URL
                value: jdbc:postgresql://<rds-endpoint>:5432/notifications_db
              - name: SPRING_DATASOURCE_USERNAME
                value: <username>
              - name: SPRING_DATASOURCE_PASSWORD
                value: <password>
              - name: JWT_SECRET
                value: <your-jwt-secret>
  ---
  apiVersion: v1
  kind: Service
  metadata: { name: notification-backend }
  spec:
    ports: [{ port: 8080, targetPort: 8080 }]
    selector: { app: notification-backend }
    clusterIP: None # if you only access via ingress or from frontend
  ```
  And similarly for frontend:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata: { name: notification-frontend }
  spec:
    replicas: 2
    selector: { matchLabels: { app: notification-frontend } }
    template:
      metadata: { labels: { app: notification-frontend } }
      spec:
        containers:
          - name: frontend
            image: myapp/notification-frontend:1.0
            ports: [{ containerPort: 80 }]
  ---
  apiVersion: v1
  kind: Service
  metadata: { name: notification-frontend }
  spec:
    type: LoadBalancer
    ports: [{ port: 80, targetPort: 80 }]
    selector: { app: notification-frontend }
  ```
  The frontend Service is a LoadBalancer, so it gets a public IP or DNS. The backend Service here is headless (ClusterIP None) meaning it's only for internal discovery (maybe the frontend will call it via cluster DNS, or you could expose it via an Ingress if needed). Another approach is to create an Ingress that routes `/<api-path>` to the backend service and `/` to the frontend service (for a unified domain).
- Use `kubectl apply` or Helm to deploy these to your EKS cluster. EKS will provision the LoadBalancer for the frontend. If using an Ingress controller (like ALB Ingress or Nginx Ingress), you'd set that up as well.

**Database in Production:** You typically wouldn't run the database as a container in production. Instead, use a managed database service (like AWS RDS for PostgreSQL/MySQL). This provides reliability, backup, and performance. In our configuration, the backend gets the database connection info via env vars or config. Ensure those are set in your cloud environment (for example, in ECS task definition or in Kubernetes Secrets/ConfigMaps, don't store plaintext passwords in Git).

**Serving Frontend:** If you deploy the frontend separately, ensure the backend API URL is correctly configured (CORS or same domain):

- If on separate domains, enable CORS in Spring Boot for the frontend's origin (or use a proxy).
- If on the same domain via Ingress rules or serving through the same origin, then no CORS issues.

**Scaling Considerations:** With containers:

- You can increase replicas of the backend Deployment or ECS Service to handle more load. Thanks to using a stateless JWT auth and external DB, scaling horizontally is straightforward.
- The WebSocket aspect: if you run multiple backend instances, as noted in Section 7, you should use a broker relay (like RabbitMQ) to ensure notifications reach users connected to any instance. For deployment, that means running a RabbitMQ cluster or using a cloud service for messaging, and configuring Spring profiles accordingly (e.g., set `spring.rabbitmq.host` and use `enableStompBrokerRelay`). This is an advanced setup, but necessary if you anticipate multiple backend instances and users connected to all of them. Otherwise, you might use sticky sessions on the load balancer (ensuring a user always hits the same instance for WebSocket), but that's less scalable long-term.

**Other Cloud Providers:** The process is similar on other platforms:

- **Kubernetes** (self-managed or other cloud): Use the same manifests or adapt to their specifics (e.g., GKE, Azure AKS).
- **Heroku:** You could deploy the backend as a Heroku app (they support Spring Boot well) and the frontend as a static site (Heroku can serve static or use a buildpack for create-react-app). Or containerize and use Heroku's container registry.
- **DigitalOcean:** They have an App Platform where you can deploy directly from source or use their Kubernetes offering.

The key is that with Docker images, you're not tied to one environment; you can run them anywhere Docker is supported.

### 6.3 CI/CD Pipeline Setup

To streamline deployment, a CI/CD pipeline is essential. This ensures that whenever you update code, it gets built, tested, and deployed automatically or with minimal manual intervention.

**Continuous Integration (CI):**

- Use a service like **GitHub Actions**, **GitLab CI**, **Jenkins**, or others. The pipeline should:

  1. **Checkout code** and set up environment (Java, Node, Docker as needed).
  2. **Build and Test Backend**: Run `mvn clean verify`. This compiles the code and runs all tests. If tests fail, the pipeline should stop and report failure.
  3. **Build and Test Frontend**: Run `npm install` and `npm run build` (for production build to ensure no errors) and `npm test -- --watchAll=false` to run tests once. Linting can also be included.
  4. **Produce artifacts** (optional): Save the built jar and the frontend build output, mainly if you want to archive them or use them in further steps.
  5. **Static Analysis**: (Optional) Run tools like SonarQube, ESLint, Prettier, etc., as part of CI to maintain code quality.

- Example (GitHub Actions):
  ```yaml
  name: CI
  on: [push]
  jobs:
    build:
      runs-on: ubuntu-latest
      services:
        db:
          image: postgres:14-alpine
          env:
            POSTGRES_DB: notifications_db
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
          ports: ["5432:5432"]
          # health checks can be added
      steps:
        - uses: actions/checkout@v2
        - name: Set up JDK 17
          uses: actions/setup-java@v2
          with:
            java-version: "17"
            distribution: "temurin"
        - name: Build and Test Backend
          working-directory: notification-backend
          run: mvn clean verify
        - name: Set up Node
          uses: actions/setup-node@v2
          with:
            node-version: 16
        - name: Build and Test Frontend
          working-directory: notification-ui
          run: |
            npm ci
            npm run build
            npm test -- --watchAll=false
  ```
  This is a simplified example. It also starts a Postgres service for the backend tests (so that the backend can connect to a DB if needed, or use testcontainers).

**Continuous Deployment (CD):**

- After CI passes, have a workflow to deploy the application:

  1. **Build Docker images**: You can do this in the CI pipeline if the CI runner has Docker. Alternatively, use a separate workflow or a build service. For GitHub Actions, there's `docker/build-push-action`.
  2. **Push Docker images to registry**: e.g., Docker Hub or ECR. Use secrets to authenticate (GitHub Actions can store secrets for your Docker credentials or AWS keys).
  3. **Deploy to environment**: This could be done by:
     - Triggering AWS CodeDeploy or updating an ECS service (via AWS CLI).
     - Applying Kubernetes manifests (using `kubectl` or a tool like Argo CD/Flux if GitOps).
     - Using specific plugins (for example, a GitHub Action for EKS or Amazon ECS).
     - For simplicity, if using a VM or Docker Compose server, you could SSH and pull the new images then restart containers.
  4. **CI/CD Pipelines** often separate stages for dev, staging, production. You might deploy automatically to a staging environment, run some integration tests, and then require a manual approval for production deployment.

- Example (continuing GitHub Actions for deployment):
  ```yaml
  name: CD
  on:
    push:
      branches: [main]
      # maybe only on certain tags or merges to main
  jobs:
    deploy:
      runs-on: ubuntu-latest
      needs: build # ensure CI job passed
      steps:
        - uses: actions/checkout@v2
        - name: Build and push backend image
          uses: docker/build-push-action@v2
          with:
            context: notification-backend
            file: notification-backend/Dockerfile
            push: true
            tags: myregistry/notification-backend:latest
        - name: Build and push frontend image
          uses: docker/build-push-action@v2
          with:
            context: notification-ui
            file: notification-ui/Dockerfile
            push: true
            tags: myregistry/notification-frontend:latest
        - name: Deploy to Kubernetes
          uses: azure/k8s-deploy@v1
          with:
            kubeconfig: ${{ secrets.KUBECONFIG }}
            manifests: |
              k8s/backend-deployment.yaml
              k8s/frontend-deployment.yaml
            images: |
              myregistry/notification-backend:latest
              myregistry/notification-frontend:latest
  ```
  This example uses a GitHub Action for Kubernetes deployment (in this case it's an Azure one, conceptually similar for other K8s). It assumes you have a kubeconfig stored as a secret.

**Environment Variables & Secrets:** Ensure sensitive data like DB passwords, JWT signing secrets, etc., are not hardcoded. In Docker/K8s, these should be passed as env variables or mounted from secrets. In CI, do not log them. Use the CI secret storage to pass them to deployment steps (for example, AWS credentials to push to ECR, kubeconfig or cluster credentials to deploy).

**Monitoring Deployment:** Once deployed, have monitoring in place:

- Use CloudWatch or another monitoring to ensure the services are healthy.
- Use health endpoints (Spring Boot actuator `/health`) maybe behind authentication for your own checks or Kubernetes readiness probes.

**Rollbacks:** Ensure you can rollback if something goes wrong:

- On Kubernetes, keep previous ReplicaSets or use image tags for versions.
- On ECS, you might keep the previous task definition.

The CI/CD, once configured, will greatly speed up your development cycle:

1. You push code to main (or merge a PR).
2. The pipeline runs tests. If something fails, you fix it before it goes live.
3. If all good, it builds and deploys your changes to the server/cluster.
4. You get your new feature or fix in production with minimal manual steps.

This completes the journey from development to deployment. Next, we consider performance optimizations to ensure the system runs efficiently in production.

## 7. Performance Optimization

After implementing functionality, it's important to ensure the application performs well, especially under high load or with many users. We will discuss optimizing the WebSocket usage and improving database performance for the notifications system.

### 7.1 Optimizing WebSocket Connections and Real-Time Handling

**Efficient Use of Connections:** We already ensure one WebSocket connection per user session. This is crucial; opening multiple connections from the same client (for example, one per component) would be wasteful. If your app grows, consider how many concurrent WebSocket connections the server needs to handle. Each user = 1 connection is optimal. Also, if a user logs in from multiple devices, that's one connection per device which is fine.

**Heartbeat Intervals:** STOMP (and SockJS) supports heartbeats to keep the connection alive and detect dead connections. Spring’s default is often something like 10,000ms outbound, 0ms inbound (meaning server will send heartbeats every 10s if client doesn't, and not expect heartbeats from client unless configured). The STOMP JS client default is usually 0ms, 0ms (disabled) unless you call `client.heartbeat.outgoing = 10000` etc. In a production scenario, enabling heartbeats can help quickly detect half-open connections (e.g., if a client unexpectedly disconnects, the server will know when it misses a heartbeat). However, heartbeats add a small overhead. It's a trade-off. For most applications, you can rely on TCP keepalive or simply the fact that if a user is disconnected, they’ll reconnect when needed.

**Horizontal Scaling & Broker Relay:** If your user base grows, you might run multiple instances of the backend service. With WebSockets and STOMP, scaling horizontally can be challenging because not all users are connected to the same instance. As mentioned, Spring provides a **STOMP broker relay** to connect to external message brokers (like RabbitMQ or ActiveMQ). If you configure `enableStompBrokerRelay`, each Spring Boot instance will act as a STOMP client to the broker. When you call `convertAndSendToUser`, the message goes to the broker, which then routes it to the correct instance that has the subscription for that user. This allows you to scale out without sticky sessions, as the broker mediates message delivery across nodes ([Spring Boot Scaling Strategies: WebSockets - Level Up Coding](https://levelup.gitconnected.com/spring-boot-scaling-strategies-websockets-f7acf7ef45e5#:~:text=Spring%20Boot%20Scaling%20Strategies%3A%20WebSockets,without%20changing%20your%20application)).

Implementing a broker relay:

- Install/configure a RabbitMQ broker (with STOMP plugin) or another STOMP 1.2 broker.
- In your `WebSocketConfig`, instead of `enableSimpleBroker`, use:
  ```java
  registry.enableStompBrokerRelay("/topic", "/queue")
          .setRelayHost("rabbitmq-host")
          .setRelayPort(61613)
          .setClientLogin("guest")
          .setClientPasscode("guest");
  registry.setApplicationDestinationPrefixes("/app");
  registry.setUserDestinationPrefix("/user");
  ```
- This will send all messaging traffic to RabbitMQ. The `.setUserDestinationPrefix("/user")` still works as before.
- With this, you can run, say, 3 instances of the backend. A user might connect to any one of them; when a notification is sent for that user, even if sent from instance A while the user is connected to instance B, the message goes through RabbitMQ and then to instance B, then to the user.

The trade-off is the complexity of running an external broker and slight additional latency (usually negligible on local network). But it's the proper way to scale WebSocket messaging in Spring.

**Load Balancer and Sticky Sessions:** If you don't use a broker, an alternative is to configure your load balancer to use sticky sessions (session affinity) so that once a WebSocket is established with instance X, all further traffic from that client goes to X. This avoids cross-node issues but has downsides: uneven load distribution and if instance X goes down, that user's connection breaks and they might miss messages from others unless they reconnect quickly (and even then, any message sent during the downtime of X wouldn't reach them unless the app handles re-fetching missed notifications on reconnect via REST). Using the database as the source of truth helps mitigate loss (they'll fetch any missed ones on reconnect), but real-time delivery might be interrupted.

**Concurrency and Threading:** The Spring WebSocket implementation uses a few thread pools under the hood for handling messages (inbound/outbound channels). By default, it might use the main application task executor or a simple sync executor for the simple broker. Monitor CPU usage: if your app sends a burst of notifications to thousands of users, you might need to tune the size of these thread pools. You can do that by configuring the MessageBrokerRegistry (there are executor settings) or defining a TaskExecutor bean named `brokerChannelExecutor`, etc. This is advanced, but it's available if needed.

**Client Optimization:** On the client side, our approach is straightforward and should scale in the browser:

- Only one open WebSocket means low resource usage in the browser.
- Our Redux state will accumulate notifications; if that list grows very large, updating it might become slow, and rendering a huge list is also slow. Consider implementing a limit (e.g., only keep last 100 notifications in state) or UI virtualization (rendering only what's visible).
- If many notifications arrive in a short time, the client might re-render many times quickly. In our case, each new notification dispatch triggers a re-render of the menu (if it's open) or at least the badge. React can handle many quick state updates, but we could batch them if needed. (React batch updates that occur in the same event loop tick, but our notifications come in separate WebSocket frames typically.)
- Debouncing updates: If you had a scenario of a flood of notifications, you could consider accumulating them client-side for a few seconds and then updating state once with a batch. But this complicates the real-time nature, so usually not done unless absolutely needed.

**Network Usage:** Each WebSocket message has some overhead (STOMP frame headers, etc.). Ours are small (notification JSON). If network bandwidth or server processing becomes an issue, possible optimizations:

- **Compress WebSocket traffic**: Some WebSocket servers and clients support per-message compression. Browsers do support Sec-WebSocket-Extensions for permessage-deflate. Spring's Tomcat WebSocket support can be configured to allow compression. This helps if notifications content is large or numerous.
- **Reduce frequency**: If you have some event that triggers a rapid series of notifications, consider combining them into one (like "5 new messages" instead of 5 separate notifications). We mentioned this in testing real-time events.

**Alternate Approaches:** In some applications, instead of continuous WebSocket, a polling mechanism or Server-Sent Events might suffice. Polling (say every 30s ask for new notifications) is easier to scale (no persistent connections) but has higher latency and overhead of repeated HTTP. SSE is one-way but simpler than WebSocket. However, since we've established WebSocket and STOMP, these alternatives are not needed unless troubleshooting leads you there.

**Monitoring WebSocket Performance:** Keep an eye on:

- Number of active WebSocket sessions (Spring metrics or logs can tell you).
- Message throughput (msgs per second).
- Latency from server to client (not built-in, but you could measure by timestamping messages).
- If using a broker, monitor the broker's performance (queue sizes, etc.).
- The effect on the JVM: lots of WebSocket sessions means lots of objects and potentially threads in use. Ensure you allocate sufficient heap and stack.

### 7.2 Improving Database Query Performance

The database will store a growing list of notifications. It's crucial to optimize how we query and update this data:

- **Indexes:** As mentioned, ensure indexes on columns used in WHERE clauses or sorting. The query `findByRecipientOrderByTimestampDesc` will benefit from an index on `(recipient, timestamp)`. This allows the DB to quickly seek to all rows for that user and already have them sorted by timestamp (depending on the DB, it might use the index for sorting if it's a covering index).
- **Selective Loading:** If the Notification table becomes very large (millions of rows), fetching all notifications for a user might still be fine if they have, say, at most a few thousand. But if a user can also have tens of thousands, consider **pagination** or limits:
  - For example, load the 50 most recent notifications on page load. If the user wants older, provide a "Load more..." which calls an API with an offset or last timestamp.
  - This not only improves performance but also UX (the user doesn’t really want to scroll through hundreds at once).
- **Optimize Mark-as-read operations:** If a user marks notifications one by one, our current approach (findById, save) is okay. If "mark all as read" is implemented, doing that in a loop of save can be slow for many notifications. Instead, a single SQL `UPDATE` can mark all in one go.
- **Batch inserts:** If your system creates notifications in batches (maybe a system job that generates many at once), consider using `saveAll` with a batch size or JPA batch configurations to do bulk inserts efficiently.
- **Read replicas:** In very high read-heavy scenarios, you might have a read-replica of the DB and direct the GET notifications calls to it, while writes go to master. Spring can be configured with multiple data sources or you can manage at a layer above. This is likely overkill for most notification systems, but it's a thought if you have global notifications or heavy analytics.
- **Caching layer:** You could introduce Redis or an in-memory cache to store recent notifications for a short period. For example, after fetching notifications for user X, cache it for 1 minute. This way, if they open the dropdown multiple times or if multiple components request it, it doesn't hit the DB each time. However, note that our design pushes new notifications in real-time, so subsequent opens would already have them. If the user is actively using the site, the in-memory state (Redux store) already caches their notifications. A server-side cache could help if multiple instances keep requesting from DB, but again since the state is client-specific and short-lived, caching is not as beneficial here as in other scenarios like global content.
- **Clean up old data:** Periodically removing old notifications can keep queries fast simply by keeping table smaller. If you have an archive requirement, you can move them to another table or backup then delete. Smaller indexes = faster queries.

**Stress Testing:** It's good to simulate a worst-case scenario:

- Many notifications in DB: you could script to insert 100k notifications for a test user and see how the API performs. Then optimize (maybe you find you need an index or the response is too large).
- Many concurrent connections: use a tool like JMeter or Gatling to simulate, say, 1000 users connecting via WebSocket (which is tricky to simulate, but you can approximate or do long-running connections).
- Many notifications incoming: simulate a scenario where 100 notifications are created within a second (perhaps via a loop calling the POST endpoint or by calling the service in a test). Observe if any messages are dropped or delayed, and how the system handles it.

**Memory Usage on Backend:** Each Notification entity is not large, but if you fetch a huge list, that's memory. Also, the WebSocket broker will hold messages briefly. Monitor memory usage. If memory is a concern, limit list sizes and maybe stream data (Spring can stream JSON responses if needed for very large datasets rather than building huge lists in memory).

**Database Connection Pool:** If the app is under heavy load, ensure the connection pool (HikariCP by default) is sized appropriately so that queries aren't waiting for a connection. But don't oversize it beyond what the DB can handle concurrently.

In summary, by applying standard database optimizations (indexing, query tuning, caching, batch operations) and by being mindful of the unique aspects of real-time systems (persistent connections, cross-node messaging), we can ensure our React + Spring Boot notification application remains performant and scalable as usage grows.
