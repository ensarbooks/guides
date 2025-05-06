Guide on building a full-stack application using ReactJS, Spring Boot, MySQL, and Azure while ensuring ISO 27001 compliance. This guide will be tailored for advanced developers and will cover:

- **Architectural considerations** for full-stack development
- **Setting up development environments**
- **Best practices for secure coding** in ReactJS and Spring Boot
- **Database security** and encryption techniques in MySQL
- **Cloud security measures** using Azure services
- **ISO 27001 compliance requirements** with relevant controls
- **DevSecOps integration** for continuous security monitoring
- **CI/CD pipeline security**
- **Deployment strategies** in Azure
- **Audit and logging practices** to meet compliance standards

I will let you know once the guide is ready for review.

# 1. Introduction

## Overview of Full-Stack Development and ISO 27001

Full-stack development involves building both the frontend and backend of an application, along with its database and infrastructure. In our case, the tech stack includes **ReactJS** for the frontend, **Spring Boot** (Java) for the backend API, **MySQL** for the database, and deployment on **Microsoft Azure** cloud. This combination allows developers to create a complete, production-ready application. However, building a full-stack application isn’t just about functionality – it must also be secure and compliant with industry standards. This guide emphasizes **security best practices** and compliance with **ISO 27001**, an international standard for information security management. ISO 27001 provides a framework for managing sensitive data and keeping it secure by implementing an Information Security Management System (ISMS) ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=ISO%2027001%20is%20an%20internationally,information%20entrusted%20by%20third%20parties)). In the context of software development, ISO 27001 compliance means incorporating security at every stage of the development lifecycle ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=Relevance%20to%20Website%20and%20Mobile,App%20Development)), ensuring that our full-stack application not only works as intended but also protects data and resiliency against threats.

**What is ISO 27001?** ISO/IEC 27001 is a well-known standard that outlines how organizations should manage and secure information. It includes a set of security controls and processes to mitigate risks. For a development team, adhering to ISO 27001 means following a “security by design” approach – building the application with security considerations from the ground up. It’s not just about writing secure code; it’s about having policies, risk assessments, and continuous improvements in place to protect information. By the end of this guide, you’ll see how each component – frontend, backend, database, and infrastructure – can be configured and developed in line with ISO 27001 requirements. We will map technical practices (like encryption, access control, logging, etc.) to the high-level controls that ISO 27001 demands, ensuring that the resulting application can be part of a compliant system.

## Understanding Security and Compliance Requirements

Before diving into coding and configuration, it’s crucial to understand the security and compliance requirements we aim to meet. **Security requirements** often come from best practices (such as OWASP Top 10 for web security) and from specific regulatory or compliance needs (like ISO 27001, GDPR, etc.). Key areas include: protecting sensitive data (both in transit and at rest), ensuring only authorized users can access certain functionality (authentication and authorization), guarding against common web vulnerabilities (XSS, SQL injection, CSRF, etc.), and maintaining visibility through logging and monitoring. Throughout this guide, we will highlight how to address common vulnerabilities by using secure coding practices and design patterns. For instance, we’ll ensure user inputs are validated and sanitized, database queries are parameterized to prevent SQL injection, and so on. We will also implement measures to enforce data privacy and integrity, such as encryption and strict access controls.

**Compliance requirements** refer to meeting the standards set by ISO 27001 and any other relevant standards. ISO 27001 has numerous controls that could affect software development – from having a secure development policy, conducting risk assessments, controlling access to systems, to maintaining audit logs. A core concept of ISO 27001 is conducting regular **risk assessments** and mitigating identified risks with appropriate controls. In practice, this means as we plan and build our app, we identify potential security risks (e.g., what if an attacker tries to steal our database data? What if an unauthorized user tries to access an admin API?). We then implement controls to reduce those risks (like encryption, authentication checks, input validation, etc.). By proactively considering risks, we align with the ISO 27001 mindset of continual risk management ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=)).

It’s also important to note that ISO 27001 compliance is not a one-time task but an ongoing process. This means our responsibilities don’t end when the app is built. We need to deploy and operate it in a secure manner, monitor for issues, keep software up-to-date, and be ready to respond to incidents. This guide will cover those aspects in later chapters, ensuring that after development, you know how to securely deploy and maintain the application in Azure and prepare for audits or certification. In summary, the goal is to build a robust full-stack application where security is woven into every layer – from React components to Spring Boot services, from the database configuration to the cloud network settings – thereby fulfilling both best practices and ISO 27001 compliance requirements.

**Key Takeaways from this Chapter:**

- A full-stack app involves multiple layers (frontend, backend, database, cloud) and each must be secured.
- ISO 27001 is an international standard guiding how to manage information security via an ISMS ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=ISO%2027001%20is%20an%20internationally,information%20entrusted%20by%20third%20parties)). For developers, this means following a secure development lifecycle, where security is considered at each phase ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=Relevance%20to%20Website%20and%20Mobile,App%20Development)) (“security by design”).
- Understanding common security requirements (authentication, authorization, data protection, vulnerability mitigation) up front helps in designing a compliant system.
- Compliance (ISO 27001) adds requirements like risk assessment, documented policies, access control measures, and audit logging. We will map technical steps to these compliance controls throughout the guide.

With the foundation set, we can move on to setting up our development environment with security in mind.

---

# 2. Setting Up the Development Environment

Before writing code, we need to prepare our development environment. This includes installing the necessary frameworks and tools for ReactJS and Spring Boot, setting up a MySQL database, and configuring Azure resources that will host our application. In each setup step, we will also consider security configurations (even in development) to build good habits that carry over to production.

## Installing and Configuring ReactJS

To build the frontend, you should have **Node.js** and **npm** (Node’s package manager) installed on your development machine. Begin by installing the latest LTS (Long Term Support) version of Node.js, as it ensures better stability and security updates. Once Node.js is installed, you can create a new React application. One common way is using **Create React App**:

```bash
npx create-react-app secure-fullstack-app
```

This scaffolds a React project with a basic structure. Advanced developers might choose alternatives like **Vite** or Next.js for React apps, but Create React App is sufficient for our needs. After creation, navigate into the project directory and start the development server:

```bash
cd secure-fullstack-app
npm start
```

This should launch the app on `http://localhost:3000` by default, showing a starter page. At this stage, the focus is just to ensure React is set up properly.

**Security considerations during React setup:** Even though this is a local dev setup, it’s good to start with secure defaults. For example, if your app will make API calls to the backend, you might want to configure a proxy or CORS settings later – keep in mind the domain/origin to avoid cross-origin issues securely. Also, plan how you will manage environment variables for any secrets the frontend might need (like API base URLs or API keys for third-party services). In a React app, you should avoid embedding any sensitive secrets (like an API secret key) in the JavaScript, because frontend code runs on the user’s browser and can be inspected. Use React environment variables (prefixed with `REACT_APP_`) for configuration values, but **never put secret tokens or passwords in these**, since they end up in the bundle. For truly secret values, we will rely on the backend or secure storage (like Azure Key Vault) – more on that later.

After setting up the basic app, you can install additional libraries that we’ll use: for example, **React Router** for routing (if needed), **Axios** for making HTTP requests, and state management libraries if you plan to use them (Redux or context API, which we’ll cover in the frontend chapter). Install these via npm as needed:

```bash
npm install react-router-dom axios
```

We will configure these libraries in the upcoming sections. The main outcome of this step: you should have a working React development environment ready to build the frontend of our application.

## Setting up Spring Boot with Maven/Gradle

For the backend, ensure you have **Java JDK** (at least Java 17, since Spring Boot 3.x requires Java 17+) installed. We’ll use **Spring Boot** to quickly set up a RESTful backend. The easiest way to start a Spring Boot project is via the Spring Initializer (start.spring.io) or your IDE’s project wizard: select **Spring Boot** (latest version), and add the necessary dependencies. For our application, we will need at minimum: **Spring Web** (for REST APIs), **Spring Security** (for authentication/authorization), **Spring Data JPA** (to interact with MySQL), and the MySQL driver. If using Maven, these will be added as `<dependency>` entries in your `pom.xml`. If using Gradle, they’ll be in the `build.gradle` file’s dependencies section.

An example `pom.xml` snippet (if using Maven) might look like:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <scope>runtime</scope>
</dependency>
```

With these, Spring Boot will bring in the libraries we need for building a secure API and connecting to MySQL. After generating or updating the project, open it in your IDE and ensure that you can run it. By default, Spring Boot will start on port 8080. You can test it by creating a simple controller. For example, create a file `HelloController.java` in the appropriate package:

```java
@RestController
public class HelloController {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, Secure World!";
    }
}
```

Run the application (via `mvn spring-boot:run` or your IDE’s run function) and visit `http://localhost:8080/hello` to see the greeting. This confirms the environment is set up correctly.

**Security configurations for Spring Boot environment:** Out of the box, Spring Boot’s starters come with some secure defaults. For instance, including `spring-boot-starter-security` will, by default, secure all endpoints with a generated password (which is printed in the console on startup). We will override and configure Spring Security later for JWT and role-based access, but it’s good to know that by default everything is locked down. In development, you might want to disable or configure certain settings for convenience (like enabling CORS for localhost:3000 so your React dev server can call the APIs). You can do this via properties or a config class (we’ll cover CORS setup in the backend chapter). Also, plan to use a separate application configuration for development vs production. Spring Boot supports profiles (e.g., `application-dev.properties` and `application-prod.properties`). In dev, you might log more verbosely and use test credentials, but in prod, you’d tighten those up. Keep this in mind as we proceed.

Finally, ensure your Spring Boot application can connect to the MySQL database. We’ll configure the database next, but in your application properties, you’ll need to set: the JDBC URL, the database username, and password (and perhaps the driver class name). For example:

```
spring.datasource.url=jdbc:mysql://localhost:3306/secure_app_db?useSSL=true
spring.datasource.username=appuser
spring.datasource.password=<<yourpassword>>
spring.jpa.hibernate.ddl-auto=update
```

Here we include `?useSSL=true` to enforce SSL connection to MySQL (assuming it’s configured, more on that below). The `ddl-auto=update` is convenient for development (it will create/update tables based on JPA entities), but for production you might handle schema migrations more carefully. In any case, with these properties set, when you run the Spring Boot app it should attempt to connect to MySQL.

## Configuring MySQL Securely

MySQL will serve as our primary data store. First, install MySQL server (if you haven’t already) or use a Docker container for MySQL. For an advanced developer, using Docker might be preferable to avoid installing directly on your machine. For example, you could run:

```bash
docker run -d -p 3306:3306 --name mysql-dev -e MYSQL_ROOT_PASSWORD=StrongRootPassw0rd mysql:8.1
```

This runs a MySQL 8.1 container, exposing it on port 3306. After MySQL is running, create a database for the application and a dedicated user. **Do not use the root account for your application’s database operations.** Instead, create a least-privileged user. For example, log into MySQL as root (via `mysql -u root -p`) and then:

```sql
CREATE DATABASE secure_app_db;
CREATE USER 'appuser'@'%' IDENTIFIED BY 'AppUserStr0ngPassword!';
GRANT ALL PRIVILEGES ON secure_app_db.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
```

Here we created a user `appuser` with a strong password and gave it privileges only on our application’s database. In a tighter security scenario, you might grant more limited rights (e.g., only SELECT/INSERT/UPDATE if the app doesn’t need to create tables), but for development ease we granted all on that schema. The `'@'%'` means the user can connect from any host – in development that’s fine, but in production we’d likely restrict this (for instance, to the App Server’s IP or hostname, or use socket connections if on same host). Keep a note to adjust that later for production security.

Now, in terms of **secure configuration** for MySQL: There are several things to consider:

- **Enable SSL/TLS for connections:** By default, MySQL may allow unencrypted connections which could expose data in transit. It’s recommended to require SSL for client connections, especially in production. We will enforce this in Azure later. Locally, you can also set up MySQL with SSL certificates. If `useSSL=true` in the JDBC URL, ensure MySQL is configured with SSL keys or it might refuse the connection. At minimum, **using TLS ensures data in transit is encrypted**, protecting against eavesdropping ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=By%20default%2C%20MySQL%20uses%20unencrypted,the%20user%E2%80%99s%20integrity%20and%20privacy)). We will cite more on this in the database security chapter.
- **Strong Passwords and Account Policies:** Use strong, unique passwords for all accounts. Since MySQL 8, you can even enforce password policies and lock out accounts after failed attempts. For example, MySQL supports locking a user account after a number of failed logins (this can help thwart brute force attempts). If available, consider enabling such policies for production users ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Lock%20Users%20Accounts%20on%20Suspicious,Activity)) ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=MySQL%208,and%20the%20account%20lock%20time)). In dev, this might not be critical, but it’s good practice to mirror production settings as much as possible.
- **Remove or secure default accounts:** The `root` user (especially if accessible remotely) is a high risk. Ensure root has a strong password and remote root login is disabled if not needed. Also, MySQL often comes with an anonymous user or test database – remove those in production.
- **Secure Configuration**: There are a few MySQL configuration tweaks for better security. For example, consider adding `skip-symbolic-links`, `skip-networking` (if the DB server should not be accessible via network, not our case since app needs it), or restricting the `bind-address` to specific interface. Also, as a minor but interesting tip: MySQL keeps a command history (`~/.mysql_history`). In a shared environment, that could leak sensitive info (like if someone typed a password in SQL). It’s recommended to disable or delete that history file ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Disable%20and%20Delete%20Your%20MySQL,History)). This is more of an operational security detail.
- **Principle of Least Privilege:** Beyond the database user permissions, also consider OS-level permissions if MySQL is on a server – e.g., who can read the database files. On Azure’s managed service this is handled for you, but on a VM, ensure proper file permissions and perhaps encryption of the filesystem.

At this point, you should have MySQL running and the Spring Boot application (from the previous step) configured to connect with the `appuser` account. When you run the Spring Boot app now, it should successfully connect to MySQL and possibly create tables (if you have entities defined). We will dive deeper into database security in Chapter 5, including encryption options and user management in more detail.

## Setting up Azure Cloud Resources

While development can be done locally, our target deployment is Azure. It’s beneficial to set up your Azure resources early, so you can test deployment and integration as you build. We will use the following Azure services for our application:

- **Azure App Service**: to host the Spring Boot backend (and possibly the React frontend if we choose to serve it statically from the backend or a separate App Service). Azure App Service is a platform-as-a-service (PaaS) that can run Java applications easily and manage the underlying servers. We’ll create an App Service instance configured for Java 17 / Spring Boot.
- **Azure Database for MySQL**: a managed MySQL database service on Azure. Instead of running MySQL on a VM, this PaaS provides MySQL with automatic updates, backups, and built-in security features. We will provision an Azure Database for MySQL instance for our data.
- **Azure Key Vault**: a service for secure storage of secrets, keys, and certificates. We’ll use Key Vault to store sensitive configuration like the database credentials (so that they are not stored in plaintext in our App Service settings or code).
- **Networking (Virtual Network, NSGs)**: to secure communication, we might use an Azure Virtual Network to connect App Service and the database privately. Although Azure App Service in a consumption plan doesn’t sit inside your VNet by default, it supports VNet integration. We also will use **Network Security Groups (NSGs)** or firewall settings to restrict access to our resources (for example, ensuring the database is not wide open to the internet, only accessible by the App Service).

**Initial Azure setup**: Log in to the Azure Portal (or use Azure CLI/PowerShell) and create a **Resource Group** for this project (e.g., “SecureFullStackRG”). Within this group:

- Create **Azure Database for MySQL**: Choose the Flexible Server deployment option if available (it offers more control and VNet integration). Select a suitable size (for dev, the smallest tier is fine). Configure admin username and password (this is separate from the app user we created locally; we’ll similarly create an app-specific user in this DB later). Very importantly, in the networking settings of the database, you have two options: open access via IP or private VNet. For initial testing, you might allow your development IP to access it, but for production we’ll want to use **Private access**. If using private access, you’d set up a VNet and a subnet for the database. You can skip that for now and use the Azure firewall to allow your IP (and later the App Service’s outbound IP) to connect. In any case, **ensure SSL connection is required** on the MySQL server. Azure Database for MySQL by default requires SSL encryption for connections (unless you disable that option). Keep it **enabled** to enforce encryption in transit – this helps prevent man-in-the-middle attacks on database connections ([Azure security baseline for Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline#:~:text=,enabled%20for%20accessing%20your%20database)). Azure’s MySQL will have a server parameter for “Enforce SSL” which should be ON.

- Create **Azure App Service**: Choose to create a Web App. For runtime, select a Java runtime (Java 17) and a web container (we can use the built-in Tomcat if we deploy a WAR, or simply use a “Java SE” if we deploy a fat JAR). Spring Boot can be deployed as an executable JAR, so Java SE runtime is enough. Set the region same as your database (for minimal latency). For now, you can use the Free or Basic tier in dev. In production, use at least a Standard tier for better performance and VNet integration. When the App Service is created, one immediate security configuration to do is enforce HTTPS: Azure allows you to turn off HTTP and require HTTPS only. Go to the “TLS/SSL settings” of your App Service and set “HTTPS Only” to On. This ensures that all inbound traffic to the app must be encrypted. We will also eventually upload an TLS certificate if we use a custom domain, but for Azure provided domain, it comes with a wildcard cert for `*.azurewebsites.net`. Additionally, consider enabling Azure App Service’s logging and AppInsights for monitoring (we’ll cover monitoring later).

- Create **Azure Key Vault**: In the portal, create a new Key Vault resource. Give it a name and set the region (again same region ideally). Key Vault will by default be accessible to your Azure AD account and can be used right away. We will later store secrets (like the DB connection string or credentials) in it. One thing to note: by default Key Vault allows any Azure service to access it if they have the right credentials, but it also has a firewall that can limit access by network. For simplicity in dev, you can leave it open to all Azure services. For stricter security, you might integrate it with a private endpoint. We’ll discuss Key Vault usage more in the deployment chapter. For compliance, remember to restrict access to Key Vault to only the necessary identities (principle of least privilege) ([Best practices for using Azure Key Vault | Microsoft Learn](https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices#:~:text=,6%20firewall%20and%20virtual)).

- **Networking**: If you plan to use a VNet, create a Virtual Network with at least two subnets: one for the database (if using private access) and one for the App Service integration. Note: App Service doesn’t sit _in_ a subnet but can be integrated with one for outbound traffic via VNet Integration feature. Alternatively, Azure also offers a feature called **Private Link** for Key Vault and Database, which gives them private IPs in your VNet and you access them over those. Setting these up can be a bit advanced, but the idea is to avoid any traffic going over the public internet. At minimum, if you don’t use a VNet for dev, ensure you configure firewall rules: e.g., on the Azure MySQL, only allow the IP of your App Service (you might not know this until you deploy, but you can find out the outbound IPs from App Service’s properties) and perhaps your dev machine if needed. Similarly, restrict Key Vault if possible.

This initial Azure setup will allow us to later deploy our app securely. We will revisit Azure in Chapter 6 with more detailed steps on deploying the frontend and backend, configuring environment settings (like connection strings and Key Vault references), and enabling security features like **Azure Monitor, Azure Defender** etc. For now, just ensure the resources exist and are properly configured (SSL enforced on DB, HTTPS enforced on App, etc.). It’s fine if you don’t deploy anything yet – we’ll do that after building the application.

**Recap of environment setup:** We now have React and Spring Boot development environments running locally, a MySQL database for development, and cloud resources prepared on Azure for deployment. In the next chapters, we’ll focus on building the frontend and backend with security in mind, then circle back to using the Azure resources when deploying. Keep in mind the compliance angle: even in these setup steps, we practiced good security (least privilege DB user, enforcing TLS, etc.) which are part of ISO 27001’s recommended controls for protecting data. In a compliant project, you would document these decisions (for example, writing down that “database connections are encrypted to protect data in transit” as part of control implementation).

---

# 3. Building the Frontend (ReactJS)

Now that our environment is ready, we start building the frontend of our application using ReactJS. The frontend is what users interact with, so it’s crucial to implement robust security on this side as well – this includes secure handling of authentication, proper state management (especially for security-related state like user tokens/roles), and safe communication with the backend. In this chapter, we’ll cover:

- Implementing a secure authentication mechanism (we’ll focus on JWT-based auth, and touch on OAuth2 if needed).
- Managing application state (with Redux or Context API) in a way that doesn’t expose sensitive info.
- Making secure API requests from React to our Spring Boot backend (including how to attach tokens, handle errors, etc.).
- Implementing Role-Based Access Control (RBAC) in the UI – so that users see only what they should and cannot perform unauthorized actions through the interface.

Throughout this, remember that the frontend is not fully trusted – users can inspect and modify front-end code. So, never rely solely on front-end checks for security (all critical enforcement must happen in the backend too). However, a secure front-end can greatly improve user experience and overall security (for example, by preventing tokens from leaking, warning users of unsaved changes, etc.).

## Secure Authentication with JWT and OAuth2

**Authentication** is the process of verifying who the user is. In modern web apps, a common approach is to use **JWT (JSON Web Tokens)** for authentication. Another approach is **OAuth2** (often used for delegated auth with providers like Google or Azure AD). We will primarily discuss JWT as issued by our own backend (Spring Boot) since we control both sides. We will also mention how OAuth2 flows could be integrated (e.g., using OAuth2 codes to get tokens from an identity provider).

**How JWT Auth works in our context:** The user will log in via the React frontend (usually by submitting a username/password or some credentials to an authentication API endpoint on the Spring Boot backend). The backend verifies the credentials (for example, by checking the username/password against the database or an identity service) and if valid, issues a JWT token. This token is then sent back to the frontend, which will store it and include it in subsequent API requests to prove the user’s identity and permissions. The JWT is digitally signed (and optionally encrypted) string that the backend can validate on each request without needing to look up session info in a database (it’s stateless authentication).

**Implementing the login flow in React:** Create a component for login, which might contain a form for username and password. On form submission, you’ll call the backend API (for example, `POST /api/auth/login`) with the credentials. Using a library like Axios for the request:

```js
// Example using Axios in a React component
axios
  .post("/api/auth/login", { username, password })
  .then((response) => {
    const token = response.data.token;
    // TODO: store the token securely
  })
  .catch((error) => {
    console.error("Login failed:", error);
  });
```

On success, the backend will return a JWT (and possibly user details/roles). The crucial part on the frontend is **how to store the JWT**. Two common ways:

1. Store in browser **localStorage/sessionStorage**.
2. Store in a **HTTP-only cookie**.

Storing in localStorage is straightforward (e.g., `localStorage.setItem('token', token)`), but comes with a security caveat: if your app is vulnerable to XSS (cross-site scripting), an attacker could potentially read the token from localStorage and hijack the session. On the other hand, storing in an HttpOnly cookie (sent by the server as a Set-Cookie) can protect against XSS theft, because JavaScript cannot read HttpOnly cookies ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=Secure%20HttpOnly%20cookies)). However, cookies come with their own considerations: they will be sent automatically with requests to the server (which could expose them to CSRF attacks if not protected). A common modern approach is: use HttpOnly, Secure cookies for the tokens, and implement CSRF protections on the server. Alternatively, store JWT in memory (React state or context) which is not easily accessible to other sites’ scripts (but it will be lost on refresh unless you refresh it from a cookie or so).

For our guide, we’ll assume we use the token in a Bearer header for simplicity (which is typical with SPA + JWT usage). So we might store it in memory or localStorage. **Best practice:** if using localStorage, be very cautious and ensure your app does proper XSS sanitization. Using HttpOnly cookies is considered more secure for JWT storage ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=include%20using%20HttpOnly%20cookies%20with,side%20session%20management)) ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=Secure%20HttpOnly%20cookies)). We will demonstrate using localStorage for simplicity but highlight the risks and mitigations (like using a short token expiry and refresh mechanism).

**Storing the token (frontend code):** Suppose we decide to use localStorage for now. After login success, do:

```js
localStorage.setItem("authToken", token);
```

Now the user is “logged in” from the client perspective. We should update application state to reflect that (maybe store the user info in a context or Redux store). For example, if using React Context:

```js
// In AuthContext.js
const [auth, setAuth] = useState({ token: null, user: null });

const login = async (username, password) => {
  const response = await axios.post("/api/auth/login", { username, password });
  const token = response.data.token;
  const userData = response.data.user; // assume server returns user info (name, roles, etc.)
  localStorage.setItem("authToken", token);
  setAuth({ token, user: userData });
};
```

This way, any component wrapped with AuthContext can know if user is logged in and what their info/roles are.

**OAuth2 integration (optional):** If instead of managing user credentials ourselves, we wanted to integrate with an external identity provider (like signing in with Google, or corporate Azure AD), we could use OAuth2/OIDC. In that case, our Spring Boot backend might be configured as an OAuth2 client or resource server, and the React front-end might redirect users to the provider’s login page. After login, the provider redirects back with an authorization code or token. This scenario can be complex, but libraries like **MSAL.js** (for Azure AD) or **Passport.js** can help in the frontend, and Spring Security OAuth can help in the backend. Covering a full OAuth2 flow is beyond our scope here, but keep in mind ISO 27001 compliance also requires secure handling of third-party login tokens and user data. No matter the auth method, the front-end should never expose sensitive data or tokens to unintended parties.

## State Management with Redux or Context API

State management in a React app is crucial, especially when dealing with authentication state. You want a reliable way for components to know if a user is logged in, what their profile/roles are, and to react to changes (like logging out). You can use the built-in Context API or a library like Redux for this.

**Using Context for Auth State:** React’s Context API allows us to provide state globally. We can create an `AuthProvider` that wraps our app and provides the current user state and actions (login, logout). For instance:

```jsx
// Pseudocode for AuthProvider using Context
import { createContext, useState } from "react";
export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState({ user: null, token: null });

  const login = (user, token) => {
    // Save token in storage for persistence
    localStorage.setItem("authToken", token);
    setAuth({ user, token });
  };

  const logout = () => {
    localStorage.removeItem("authToken");
    setAuth({ user: null, token: null });
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

This is a simple approach. In a more advanced setup, you might also include a method to refresh the token, and on app load, check if a token is stored and still valid (auto-login). Redux would follow a similar pattern: you’d have an auth slice of state and actions to set user and token.

**Security considerations for state management:** Treat the auth state carefully. For example, if using Redux DevTools, be aware that the state (including tokens) might be exposed in the browser’s Redux extension. If you use Redux, consider not putting the raw token in the store (or mark it as non-persistent). Using context with localStorage as backup as shown above at least confines the token to our code. Another tip: if storing tokens in memory only (not even localStorage), you reduce risk of token theft via XSS (since the token is not easily accessible after a script injection that runs later). Some apps do this: they keep the token in a React state and if the page reloads, they force re-login or use a refresh token (which might be in a secure cookie). This is arguably more secure at the cost of some user convenience.

From a compliance perspective, ensure that if any sensitive data is stored in the front-end state, it is handled properly (e.g., personal data in state should be protected – perhaps by not storing more than needed on the client). Also, plan for a session timeout or logout mechanism to prevent indefinite tokens. We will implement a logout that simply removes the token.

## Handling Secure API Requests and Responses

With authentication in place, the React app will communicate with the Spring Boot backend through HTTP requests (likely RESTful APIs returning JSON). We need to ensure these requests are done securely:

- **HTTPS**: Always call the backend over HTTPS. In development, you might be using `http://localhost:8080`, which is okay for local. But in production on Azure, we will enforce HTTPS. So the React app should ideally call `https://your-api-endpoint`. If using Azure App Service, it will provide an HTTPS URL by default. We already set “HTTPS Only” on the App Service, so any HTTP calls would be redirected or blocked. So configure your React app’s API base URL accordingly.
- **Including JWT in requests**: For authenticated endpoints, the React app must include the JWT token in the request. The common method is adding an `Authorization` header: `"Authorization": "Bearer <token>"`. If using Axios, you can set a default header after login, for example:
  ```js
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  ```
  This way, every subsequent request will have the header. Alternatively, manually include it in each request call. Ensure that you never send the token to a different domain than your API (to avoid leaking it to an attacker’s site). This is usually not an issue if your API base URL is correct and you don’t make requests to untrusted domains with the auth header.
- **CSRF considerations**: If you chose to store the token in an HttpOnly cookie, then every request will include the cookie automatically, which means you **must** protect against CSRF (Cross-Site Request Forgery). Typically, this is done by having a CSRF token that the server provides and the client sends it back in a header. Since in our design we are using the Authorization header with a token from a script, CSRF is not a big concern (CSRF mainly targets cases where browser automatically sends credentials like cookies). Nonetheless, it’s good to be aware: our Spring Boot security configuration will likely disable CSRF protection because we’re not using cookies for auth (this is a common practice in stateless JWT setups). If you do go the cookie route, React would need to read a CSRF token from a response (perhaps as a cookie or header) and include it in future write requests.
- **Handling responses securely**: When the backend returns data, ensure the frontend treats it properly. For example, if the backend returns user-generated content that might contain HTML, you should be careful to escape it or use it in a way that doesn’t introduce XSS. In React, inserting raw HTML can be dangerous – prefer rendering data as text, or if using `dangerouslySetInnerHTML`, make sure the data is sanitized. In our app, we might not have such content, but it’s a consideration for any full-stack app (especially if you render some HTML from the database).
- **Error handling**: If an API call returns an error (401 Unauthorized, 403 Forbidden, etc.), handle it gracefully. For instance, if we get 401, we might want to redirect the user to the login page. If 403 (forbidden), perhaps show an “Access Denied” message. Do not just fail silently. Also, avoid exposing raw error messages from the server to the user (they might contain sensitive info). The backend will be configured to send user-friendly error messages or codes.

**Example of making an authenticated API request:** Suppose we want to fetch a list of customer records from the backend at `/api/customers`. After setting the auth header as above, simply:

```js
axios
  .get("/api/customers")
  .then((response) => {
    const customers = response.data;
    // use the data in your component state
    setCustomers(customers);
  })
  .catch((error) => {
    if (error.response && error.response.status === 401) {
      // Token might be expired or invalid – handle logout
      logout();
    } else {
      console.error("API error:", error);
    }
  });
```

Notice we check for a 401, which likely means our token is no longer valid (or user is not authenticated). In that case, we call `logout()` (which should clear state and maybe redirect to login). You might also show a notification to user. The key is to not leave the app in a broken state if auth fails – handle it. Similarly, a 403 might mean the user is logged in but not allowed to perform that action (for example, a normal user trying to access an admin-only API). In that case you might not log them out, but perhaps show a message.

**Security headers in responses:** The backend can (and should) set certain HTTP headers to improve security (like `Content-Security-Policy`, `X-Frame-Options`, etc.). As a React developer, you normally don’t need to handle these manually, but be aware of them. If you ever see issues (like content not loading due to CSP), coordinate with backend to adjust these. For ISO 27001 compliance, using such security headers can be part of secure deployment standards (mitigating clickjacking, XSS, etc.).

## Implementing Role-Based Access Control (RBAC) on the Frontend

Role-Based Access Control means different users have different permissions in the system based on roles (or groups). For example, you might have roles like “ADMIN” and “USER”. The backend will enforce what each role can do (we’ll configure Spring Security to restrict endpoints by role). On the frontend, we also want to adapt the UI based on roles to improve user experience and add a layer of access control (though remember, it’s not a strong security layer by itself).

**Obtaining user roles:** Typically, when the user logs in, the JWT token contains their roles/authorities (in its payload). We can decode the JWT in the frontend to get this info, or (simpler) the backend can include the user’s role info in the login response JSON. For example, after login, we might get `user: { username: "alice", roles: ["ADMIN","USER"] }` along with the token. We stored that in `auth.user` state earlier.

Given we have the roles, we can implement checks in our components. For instance:

- Conditionally render admin navigation links if `auth.user.roles` contains “ADMIN”.
- Protect certain routes so only admins can access them.
- Possibly show/hide buttons (like only admins see an “Delete User” button, etc.).

**Example: Protecting routes with roles using React Router:**

If using React Router v6, you can create a component that acts as a guard:

```jsx
// A component to wrap protected routes
import { useContext } from "react";
import { AuthContext } from "./AuthProvider";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, requiredRoles }) {
  const { auth } = useContext(AuthContext);
  const { user } = auth;
  if (!user) {
    // Not logged in
    return <Navigate to="/login" replace />;
  }
  if (
    requiredRoles &&
    !requiredRoles.some((role) => user.roles.includes(role))
  ) {
    // Logged in but doesn't have required role
    return <Navigate to="/unauthorized" replace />;
  }
  // User has access
  return children;
}
```

Then use it in your routes configuration:

```jsx
<Route
  path="/admin"
  element={
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <AdminDashboard />
    </ProtectedRoute>
  }
/>
```

This ensures that if the user is not an admin, they get redirected away from the admin dashboard route.

We also included a check for not logged in at all (`!user`), redirecting to login.

Additionally, within components, you can check roles to conditionally render elements. Example in a component:

```jsx
const { auth } = useContext(AuthContext);
...
{ auth.user && auth.user.roles.includes('ADMIN') && (
    <button onClick={handleAdminAction}>Admin Only Action</button>
) }
```

This button will only show if the user is an admin. If a non-admin somehow tries to call `handleAdminAction` (say by manually triggering it via dev console), the backend should still reject it – because we will enforce role checks there too. So the front-end RBAC is mostly for UI/UX and minor safety, whereas the backend RBAC (coming in next chapter) is the actual security enforcement.

**Edge cases and security:** Always assume a malicious user can alter the frontend code (because they can, in their own browser). They might remove those checks and attempt to call admin APIs. This is why the backend must check roles on every request. Our Spring Boot will do that. The frontend’s role-based rendering is just to prevent normal users from accidentally stumbling into forbidden areas and to present the app cleanly.

From an ISO 27001 standpoint, RBAC is part of access control policies (Annex A control on user access management). Implementing RBAC in both frontend and backend ensures the principle of least privilege is followed – users only get access to what they need. We will have documentation of roles and rights which is something often required for compliance (e.g., a doc saying “Admin can do X, normal user can do Y”). Our implementation should align with that.

**Summary of Frontend Security Measures:** We have now set up a React frontend that handles authentication securely (with JWT), manages user state appropriately (with Context/Redux), communicates with the backend over secure channels using tokens, and adjusts UI based on user roles. We have taken precautions in storing tokens and included error handling for API calls. As we proceed to build the backend, keep in mind how the two will interface: for example, the backend must produce the JWT and include roles in it, and must accept the token on each request to authorize the user. The next chapter will focus on building the backend (Spring Boot) where we will implement those critical pieces: the login endpoint, JWT generation/validation, role-based authorization on APIs, and secure coding practices to protect the system from common threats.

Before moving on, here’s a quick **checklist** of what we achieved for the frontend and what to verify for compliance/security:

- [x] **Authentication flow implemented** (login UI, calls to API, token handling).
- [x] **JWT storage decision made** (e.g., using HttpOnly cookies for better security ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=Secure%20HttpOnly%20cookies)), or localStorage with caution).
- [x] **Global state management** for auth, ensuring user info and roles are accessible and persistent (at least for session).
- [x] **Protected routes and components** based on roles (RBAC in UI) to avoid unauthorized UI access.
- [x] **All API calls use HTTPS and include auth tokens** in header (no plaintext credentials in requests).
- [x] **Frontend does not expose sensitive info** (no secret in JS, no debug info shown to users, etc.).
- [x] **Input handling is safe** (e.g., if displaying any data from backend, ensure it’s sanitized or not vulnerable to injection on the client side).

With these in place, the frontend is well-prepared to interact with a secure backend, which we will construct next.

---

# 4. Building the Backend (Spring Boot)

The backend is the core of our application’s logic and data handling. We will use Spring Boot to build a RESTful API that the React frontend communicates with. In this chapter, we focus on making the backend secure and robust, covering:

- Designing and implementing **secure REST APIs** following best practices.
- Setting up **authentication and authorization** using Spring Security (with JWT and possibly OAuth2 support).
- Applying **secure coding practices** to avoid common vulnerabilities (we’ll reference OWASP Top 10 and how to mitigate them in our code).
- Implementing **secure logging and monitoring** so that security-relevant events are recorded, but sensitive data is protected in logs.

By the end of this chapter, our Spring Boot application will have endpoints that require proper auth, will enforce role-based access control, and will be hardened against typical attacks. This sets a strong foundation for ISO 27001 compliance, as many technical controls (access control, secure system engineering, etc.) are implemented here.

## Secure API Development with RESTful Best Practices

Designing RESTful APIs means creating endpoints that logically represent resources or actions in our system, using HTTP methods (GET, POST, PUT, DELETE, etc.) in a consistent way. While designing these, we should incorporate security from the start:

**1. Use HTTPS (TLS):** Though we mentioned it in frontend and Azure setup, it bears repeating: the API should only be served over HTTPS in any non-local environment. Spring Boot can be configured with an SSL certificate to serve HTTPS directly, or if behind a reverse proxy (like Azure’s front-end), ensure that is taken care of. In Azure App Service, as we set, HTTPS is enforced. In local dev, it’s okay to use HTTP, but one can also simulate HTTPS if needed (by configuring a self-signed cert in Spring Boot).

**2. Proper HTTP methods and status codes:** For example, use GET for fetching data (no side effects), POST for creating, PUT/PATCH for updating, DELETE for deletion. This by itself isn’t security, but consistency helps when later adding things like idempotency keys or ensuring safe reads. Use correct status codes (401 for unauthorized, 403 for forbidden, 400 for bad input, etc.) so the client can react appropriately.

**3. Validate input data:** Any data coming in via API (path params, query params, request bodies) should be considered untrusted. Use Spring’s validation (@Valid with JPA or DTOs) to enforce constraints on input size, format, etc. For example, if we have a User registration endpoint, ensure fields like email are valid format, password meets complexity (though password complexity can also be checked on front-end, always re-check on backend). **Never trust user input ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=3))** – this mantra helps prevent a lot of issues. Validate length of strings to avoid overly large payloads (which could be used for DoS attacks). Validate numeric ranges to avoid overflow or logic issues. If expecting certain formats (like an ID should be numeric), ensure non-numeric input is rejected with 400 Bad Request.

**4. Prevent SQL Injection:** Because we use JPA (with Hibernate) and/or Spring Data repositories, we typically don’t write raw SQL queries. This greatly reduces SQL injection risk since ORM will use prepared statements under the hood. If you do write custom queries (with `@Query` or JDBC), **always use parameters binding** (never string concatenation to build queries). Spring’s JPA and JDBC templates support placeholders (`?1` or named `:param`) which are safe. As a general rule, **use parameterized queries to avoid SQL injection ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=4))** – the database will treat the input as data, not code, preventing attackers from injecting SQL commands.

**5. Handle data output carefully:** When sending data back to the client, consider what you include. For example, never return passwords (even hashed) via API. Even for admin APIs, you generally don’t want to expose sensitive fields. Use DTOs or Jackson JSON views to control output. Also be mindful of large data outputs – paginate results to avoid denial of service by large responses. If returning user-provided content, you might need to sanitize it (though typically you’d sanitize on input and store only safe content).

**6. Use consistent and secure error messages:** Don’t leak sensitive info in error messages. E.g., on a login API, if login fails, don’t reveal “user not found” vs “password incorrect” distinctly – this can let attackers enumerate valid usernames. Instead, return a generic “Invalid credentials” for both cases. In exception handling, you might log the detailed error internally, but to the client return a generic message or an error code. In Spring Boot, you can use an `@ControllerAdvice` to globally handle exceptions and send safe responses.

**7. Rate Limiting / Throttling:** Although not built-in by default, consider applying rate limits on certain APIs (like login attempts) to prevent brute force attacks. There are libraries or you can use filters to track IP and count requests. In Azure, you could also use API Management or App Service features to throttle. This is a security measure to align with availability and attack prevention.

**8. RESTful design for security:** Keep endpoints simple and intuitive from an API perspective, but also make sure they don’t do more than needed. For instance, an endpoint `/api/users` (GET) that returns all users – should an average user be allowed to fetch that? Probably not, so that would be admin-only. Meanwhile, `/api/users/me` could return the current user’s profile (allowed for any authenticated user for their own info). Designing with least privilege in mind means each endpoint should clearly correspond to an allowed action for a role.

In our application, let’s say we have a couple of domain objects: perhaps Users, and some Business Data (could be customer records, etc.). We’ll ensure that:

- Endpoints like `/api/admin/**` are for admin roles only.
- Endpoints like `/api/data` or `/api/customers` return only data that the user is allowed to see (if multi-tenant or by roles).
- We might include the login endpoint `/api/auth/login` (public) and maybe a `/api/auth/register` if self-service signup is allowed (with appropriate checks, maybe email verification in a real app).
- Possibly a `/api/auth/refresh` if implementing token refresh flows.

We’ll implement security on these endpoints using Spring Security in the next section.

## Implementing Authentication and Authorization (Spring Security & JWT)

Spring Boot integrates with Spring Security, which is a powerful and customizable framework for securing the application. We’ll configure Spring Security to do the following:

- Authenticate users based on JWT tokens in the request headers.
- Authorize requests based on user roles (authorities).
- Provide an endpoint for logging in (issuing JWT) and possibly logging out (though logout in JWT context might just be handled on client side by discarding token).
- Secure all other endpoints by default, requiring authentication, except those we explicitly allow (like the login or public info).

**Setting up JWT in Spring Security:** Unlike session-based auth, JWT is stateless. We don’t store session on server; instead, each request carries a token. Spring Security doesn’t support JWT out-of-the-box in older versions, but we can integrate it by using filters or the newer Spring Security 5+ support for OAuth2 resource servers (which can validate JWT). There are two common approaches:

1. Write a custom **OncePerRequestFilter** that reads the Authorization header, validates the JWT, and sets the authentication in Spring’s SecurityContext.
2. Use Spring Security’s **OAuth2 Resource Server** support and configure it with a JWT decoder. This is suitable if JWTs are signed with e.g. an asymmetric key and you can provide the public key or JWK set. For simplicity, a custom filter is straightforward.

We’ll outline using a custom filter here for clarity.

First, add necessary library for JWT handling. We can use **jjwt** (Java JWT) or Spring Security’s jwt support. For example, include the dependency for jjwt:

```xml
<dependency>
   <groupId>io.jsonwebtoken</groupId>
   <artifactId>jjwt-api</artifactId>
   <version>0.11.5</version>
</dependency>
<dependency>
   <groupId>io.jsonwebtoken</groupId>
   <artifactId>jjwt-impl</artifactId>
   <version>0.11.5</version>
   <scope>runtime</scope>
</dependency>
<dependency>
   <groupId>io.jsonwebtoken</groupId>
   <artifactId>jjwt-jackson</artifactId>
   <version>0.11.5</version>
   <scope>runtime</scope>
</dependency>
```

(Alternatively, use the spring-boot-starter-oauth2-resource-server which has Nimbus JOSE JWT support.)

**Creating a JWT token:** When a user logs in (we will have a `AuthController.login()` that checks credentials), upon success we create a JWT. The JWT should contain claims like username and roles, and have an expiration. For example, using JJWT:

```java
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

public String generateToken(UserDetails userDetails) {
    long now = System.currentTimeMillis();
    Date expiry = new Date(now + TOKEN_VALIDITY); // e.g., TOKEN_VALIDITY = 3600_000 (1 hour)
    return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .claim("roles", userDetails.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList())
            .setIssuedAt(new Date(now))
            .setExpiration(expiry)
            .signWith(secretKey, SignatureAlgorithm.HS256) // secretKey is a Key or key bytes for HMAC
            .compact();
}
```

We will have to define `secretKey` (could be a static secret or loaded from config/Key Vault for security). In production, use a strong random secret or an RSA key pair. Keeping the secret safe is critical – if someone gets it, they can forge tokens. We might store it in Azure Key Vault (we’ll discuss that in deployment).

**Validating JWT on incoming requests:** Now, we create a filter class extending `OncePerRequestFilter`:

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    @Autowired
    private JwtUtil jwtUtil; // a utility with methods to validate token and extract username/roles
    @Autowired
    private UserDetailsService userDetailsService; // to load user details if needed

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            try {
                String username = jwtUtil.extractUsername(token);
                if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    // Token is present and no current auth (not already authenticated this request)
                    if (jwtUtil.validateToken(token)) {
                        UserDetails userDetails = userDetailsService.loadUserByUsername(username);
                        // Note: In JWT, we could trust the token fully and not hit DB. But if we want to double-check user existence or roles, we load.
                        UsernamePasswordAuthenticationToken authToken =
                            new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                        SecurityContextHolder.getContext().setAuthentication(authToken);
                    }
                }
            } catch (JwtException ex) {
                // Token validation failed (expired or malformed)
                logger.warn("JWT validation failed: " + ex.getMessage());
                // Optionally, you could abort filter chain here for invalid token
            }
        }
        filterChain.doFilter(request, response);
    }
}
```

This filter does: if an Authorization header with Bearer token is present, it tries to validate it and set the authentication in context. If the token is invalid, we just proceed without setting auth (which will result in Spring Security denying access later, or we could explicitly send error). You might choose to send a 401 immediately by not calling `filterChain.doFilter` when token is invalid. But often, letting it through and letting the framework handle it is fine as long as no auth is set (Spring will see no auth and if endpoint requires it, will throw 401).

We need to register this filter in security config.

**Spring Security Configuration:** With Spring Boot 3 (Spring Security 6), the configuration is typically done by exposing a SecurityFilterChain bean. For example:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    JwtAuthenticationFilter jwtFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.csrf().disable(); // we disable CSRF as we use stateless JWT (no session cookies)
        http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
        http.authorizeHttpRequests(auth -> {
            auth.requestMatchers("/api/auth/**").permitAll(); // allow login and possibly signup without auth
            auth.requestMatchers("/api/admin/**").hasRole("ADMIN");
            auth.anyRequest().authenticated();
        });
        // Possibly require https (though in Azure this might be done at platform)
        http.requiresChannel(channel -> channel.anyRequest().requiresSecure()); // this forces HTTPS
        // Add our JWT filter
        http.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
}
```

This configuration:

- Disables CSRF (because we’re not using cookies for session; if we were, we’d need CSRF tokens).
- Marks the session as stateless (no HTTP session will be used to store security context; every request must have token).
- Sets authorization rules: anything under `/api/auth/` is open (so e.g. `/api/auth/login`), anything under `/api/admin/` requires ADMIN role, and all other endpoints require authentication (logged in). You can further fine-tune, e.g., maybe `/api/public/info` if such exists could be permitAll.
- It also forces HTTPS on all requests (`requiresSecure()`), adding an extra layer to ensure the app isn’t served on HTTP accidentally.
- Registers our JWT filter so that it runs before the built-in UsernamePasswordAuthenticationFilter (which normally handles form login).

Now, we also need to define how users are loaded for authentication. In a JWT scenario, once logged in, we might not need to load the user for each request (since token has roles). But in our filter above, we chose to load UserDetails from database for additional check. We should implement a `UserDetailsService` that fetches user data (username, password, roles) from our database (if we have a users table) or any source. This is used at login time too to verify password. Spring Security can encode passwords with BCrypt etc., and verify.

**Storing user credentials securely:** Make sure to hash passwords in the database (e.g., using BCrypt with strength 10 or higher). Spring Security’s `PasswordEncoder` can be used to encode and match passwords. At user registration time, encode the password before saving. At login, Spring Security can automatically check if you use something like `AuthenticationManager` with DaoAuthenticationProvider. However, since we’re doing JWT, we might manually authenticate in a controller: for example:

```java
@Autowired AuthenticationManager authManager;  // configured with our userDetailsService and password encoder

@PostMapping("/api/auth/login")
public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
    try {
        UsernamePasswordAuthenticationToken authToken =
            new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword());
        Authentication auth = authManager.authenticate(authToken);
        // If we reach here, authentication was successful
        UserDetails user = (UserDetails) auth.getPrincipal();
        String jwt = jwtUtil.generateToken(user);
        LoginResponse resp = new LoginResponse(jwt, user.getUsername(), user.getAuthorities());
        return ResponseEntity.ok(resp);
    } catch (BadCredentialsException ex) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(null);
    }
}
```

This uses Spring’s `AuthenticationManager` to authenticate the credentials against the UserDetailsService (which checks the password). If successful, we generate the JWT and return it (and user info). If fail, we return 401. (In reality, you might want to send a message in the body, but keep it generic like “Login failed”.)

**Authorization (RBAC) in backend:** We already set the URL-based restrictions in the config (like `hasRole('ADMIN')` on certain paths). We can also use method-level security. Enabling method-level security (`@EnableMethodSecurity` in config class) allows using annotations like `@PreAuthorize`. For example:

```java
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/api/admin/users")
public List<User> getAllUsers() { ... }
```

This adds an extra layer such that even if someone reached this controller, the call will be intercepted and checked for role. It’s useful especially if you want fine-grained control inside service methods or for non-HTTP invocation (like if you secure service methods called from multiple controllers). For our purposes, URL config might suffice, but adding method security is a good practice (defense in depth).

**Preventing common vulnerabilities (OWASP) in code:**  
We touched on validation and SQL injection earlier, but let’s systematically address some OWASP Top 10 issues in the context of Spring Boot:

- **Broken Authentication**: We are using Spring Security which is a robust framework, and JWT for stateless auth. We must ensure tokens cannot be guessed or forged (use strong secrets, proper signing). Also implement short expiration and possibly refresh tokens to minimize impact of a stolen token. Additionally, consider implementing account lockout after several failed logins (as mentioned for DB, but on app level too). Spring Security can be configured with an AuthenticationProvider that tracks attempts. Alternatively, handle in the login method (e.g., count login failures and if >N, disable the account for some time).
- **Sensitive Data Exposure**: Use HTTPS so data in transit is safe. For data at rest, ensure passwords are hashed, and if any sensitive fields (like personal info) maybe encrypted in DB if needed (this can be done via JPA converters or at DB level). Also ensure that we don’t expose sensitive data via APIs or error messages. We should also consider encryption of sensitive config (like DB credentials) – which we will do using Azure Key Vault rather than storing in plaintext config.
- **XML External Entities (XXE)**: If your app parses XML (unlikely in our scenario unless we have an XML input), be sure to disable external entity resolution. With JSON and standard libs, we’re mostly safe from XXE.
- **Broken Access Control**: We have RBAC in place; ensure all endpoints are covered by security rules. Pay attention to any endpoint that might not be under `/api` or any filter exclusions – we don’t want an unprotected path leaking data. Also, enforce access control at the data level if needed: e.g., if a user can only see their own record, ensure they cannot fetch others by changing an ID in the URL. That might mean adding a condition in the query or filtering server-side based on the authenticated user. This is part of authorization too.
- **Security Misconfiguration**: Spring Boot’s defaults plus our config should be okay. Some specifics: make sure directory listing is off (if static content being served), do not enable any debug or actuator endpoints without protection. If we expose Actuator (for health, metrics), secure it (with at least basic auth or IP restrictions). We should also ensure that CORS is configured properly so that only allowed domains can call our APIs in production (to prevent rogue websites from making requests with a user’s token if JWT is in cookie). In development, you might allow localhost, but in prod maybe only your domain.
- **Cross-Site Scripting (XSS)**: Most XSS defense is on the front-end (escaping output). The backend should ensure that any data stored that might be displayed later is sanitized or at least flagged. If our app does not store rich text or HTML from users, we are relatively safe. If it does (like comments, etc.), use a library to strip or encode malicious input.
- **Logging and Monitoring**: We will address it later, but basically, log important security events (logins, suspicious activities) but do not log sensitive info like passwords or full credit card numbers, etc. Also protect logs (set file permissions etc.).

By following these secure coding practices, we align with many of the technical controls required for a secure development (in fact, ISO 27001’s secure development control expects that developers follow guidelines to prevent such flaws).

One additional measure: **Secure configuration of frameworks**. For instance, Spring by default has CSRF on (we turned it off because we use stateless JWT). That’s fine but document the rationale. If this app was partially using sessions, we’d keep it on and include CSRF tokens. Also ensure that our session cookie (if any) is marked HttpOnly and Secure. Spring does that by default for `JSESSIONID` if using `ServerProperties` settings or by the container’s config. Since we aren’t using sessions for auth, it’s less relevant, but just to note.

## Secure Logging and Monitoring in Spring Boot

Logging is essential for troubleshooting and security auditing, but it must be done carefully. We want to log enough information to detect issues or fulfill audit requirements, but not so much that we expose sensitive data or flood with noise.

**What to log:** Key security events – such as login success, login failure (with username attempted), access denials (403s), important data changes (e.g., if an admin deletes something, log which admin did it). Also log error stacktraces for exceptions (to debug issues), but consider logging them at a level that doesn’t send them to users. In Spring Boot, by default, errors might be printed to console or logs. We can customize the logging pattern to include contextual info like timestamp, log level, thread, maybe the user (we can add MDC info for user). If using a centralized logger or APM (Application Insights in Azure), these logs will help create alerts for suspicious behavior.

**Don’t log sensitive information:** Be mindful not to log things like passwords (never do that), or full JWT tokens, or personal data unnecessarily. For example, if an exception includes user data in the message, consider extracting only needed parts. If you catch an exception for a SQL query failure, don’t log the full query with all data if it contains sensitive info. A general rule is to assume logs could be read by others, so minimize sensitive content. This is also an ISO 27001 concern – control over “log information protection” ensures that logs are safeguarded and don’t have sensitive stuff.

**Spring Boot logging setup:** Spring Boot uses Logback by default. You can configure logback.xml or use application.properties for simple configs. For example, set logging level for various packages. In production, you might set root logging to INFO and only errors for certain noisy packages. For security auditing, you might want to increase logging for Spring Security events. Spring Security can actually log details at DEBUG level. If you set `logging.level.org.springframework.security=DEBUG`, you’ll see every authentication attempt and decision – useful for debugging security issues, but maybe too verbose for production. Instead, you might implement custom logging in our auth logic (like logging “User X logged in from IP Y at time Z”).

**Audit logging:** If the application has critical actions, consider an audit log (separate from normal log). For instance, a table or file where you append records of user actions like “User Alice (ROLE_ADMIN) deleted record 123 at 2025-02-15T10:00 from IP …”. This can help in forensics. Spring has an `AuditEvent` mechanism if using Spring Security’s auditing. Or one can simply use a logger dedicated to audit events.

**Monitoring integration:** Logging is one side (post-facto analysis), monitoring is active observation of the system. We should integrate with Azure’s monitoring: Azure App Service can send logs to Azure Monitor or App Insights. We can also use Spring Boot Actuator to expose metrics and health info. Actuator has a /health and /metrics endpoint. If we include `spring-boot-starter-actuator`, be sure to secure those endpoints (by default, in Spring Boot 2+, if security is on, actuator endpoints are secured as well unless configured otherwise). We might configure actuator to require an admin role or a separate API key.

Azure App Insights SDK can be included to automatically track requests, performance, exceptions, etc. That’s more performance/diagnostics, but it can also detect anomalies. Azure also has **Microsoft Defender for Cloud** which can monitor App Service and MySQL for unusual activities ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Secure%20MySQL%20in%20the%20Cloud)) – for example, it might alert on unusual query patterns (SQL injection attempts) or a sudden spike in failed logins. Enabling such services contributes to compliance because you have active security monitoring. We’ll mention that in deployment.

**Example of adding a log in our Spring Security filter:** In `JwtAuthenticationFilter`, where we catch a JwtException (token invalid), we did a `logger.warn`. We might improve that to record the source IP and perhaps the token substring for tracking. Also, in the login controller, after successful auth, do something like `logger.info("Login success for user: " + user.getUsername() + " from IP: " + request.getRemoteAddr());`. For failures: `logger.warn("Failed login attempt for user: " + username + " from IP: " + request.getRemoteAddr());`. These logs, when aggregated, can reveal brute force attempts or unauthorized use, which is something an ISO auditor would like to see you have the ability to detect.

**Retention of logs:** ISO 27001 requires keeping audit logs for a certain period (depends on org policy, often 6 months or 1 year). Ensure the logs we generate are stored securely and retained. In Azure, we can ship them to Azure Storage or Log Analytics with retention policies. That’s part of deployment considerations.

To conclude this backend chapter, we have: configured robust authentication with Spring Security and JWT, locked down endpoints by role, written code following secure practices (validation, error handling, no sensitive leaks), and set up logging for security events. This addresses many of the critical security control points. An ISO 27001 auditor would check that we have access control (yes, via Spring Security roles), secure development guidelines (we followed OWASP best practices), and audit logging (we configured logs for important events).

**Checklist for Backend Security:**

- [x] Spring Security configured (JWT filter, auth manager, password encoding, role-based access) – ensuring only authorized access to APIs.
- [x] Passwords stored hashed, and secrets (like JWT secret) not hard-coded in code (we will externalize those to config and secure them via Key Vault).
- [x] Input validation in place (using Spring’s validation on request bodies, checking path params) to prevent bad data and attacks.
- [x] All database queries use parameters or ORM to avoid injection.
- [x] Errors to clients are sanitized (no stack traces or sensitive info in API responses).
- [x] Logging in place for login attempts, security-related events; logs do not contain sensitive data like passwords or full personal info.
- [x] Appropriate use of HTTP status codes and responses for security events (401, 403, etc.).
- [x] No debug endpoints or misconfigurations left open (ensure Actuator or H2 console etc. are secured or disabled in prod).
- [x] Unit/Integration tests for security if possible (test that a normal user cannot call admin API, etc.). This isn’t explicitly required by ISO but is a good practice to verify our security.

With the backend and frontend now built with security in mind, we can focus on the database specifics in the next chapter, followed by deployment to Azure where we will tie everything together and implement cloud-specific security measures.

---

# 5. Database Security (MySQL)

Databases often contain the crown jewels of an application – the sensitive data. Securing MySQL is therefore a critical part of our full-stack app’s security posture. In this chapter, we dive deeper into MySQL security, covering:

- Secure configurations for MySQL (both general and Azure-specific configurations).
- Encryption of data at rest (how to ensure stored data is encrypted) and in transit (SSL/TLS for connections).
- Proper management of database user accounts, roles, and permissions following least privilege.
- Additional best practices like backups security, and auditing database activities.

By implementing these measures, we align with ISO 27001 controls around cryptography, access control, and operational security for databases. Many breaches occur due to misconfigured databases (e.g., default credentials, open network access) – we will avoid those pitfalls.

## Secure Database Configuration

Whether you’re running MySQL on a VM, on-premises, or using Azure’s managed MySQL service, certain configurations improve security:

**1. Update and Patch MySQL:** Use a supported, up-to-date version of MySQL. Security patches fix known vulnerabilities, so staying current is key. Azure’s managed MySQL handles patching for you to an extent, but if self-managed, have a schedule to apply updates. ISO 27001 requires a patch management process – ensure database is included in that.

**2. Strong Access Control:** We already created a separate `appuser` for the application. In production, consider using even more restricted accounts for different purposes. For example, the web app might have a read/write user for normal data, but maybe a separate user for administrative tasks if needed. Ensure no user has more privileges than necessary. The principle of least privilege applies strongly here. For instance, if the app never needs to drop tables, don’t grant `DROP` privilege. In MySQL, privileges can be granular (SELECT, INSERT, UPDATE, DELETE, etc., on specific tables). For simplicity, one might give ALL on the schema to the app user, but least privilege would mean tailoring it.

**3. Remove or disable default accounts:** MySQL’s default `root` user and any anonymous accounts created initially should be secured. Set a strong root password. If possible, disallow root login remotely (`skip-networking` or limiting root to `localhost`). Azure MySQL will require a custom admin user (it doesn’t actually use "root", but an admin you name).

**4. Secure the MySQL configuration (my.cnf):**

- Ensure `bind-address` is set appropriately. If the database is on the same server as the app, you can bind to localhost so it’s not exposed externally. In a cloud environment with separate DB service, Azure MySQL is already accessible only through its endpoint with firewall rules.
- Consider enabling `skip_name_resolve` to avoid DNS overhead (security benefit: avoid certain DNS-based attacks).
- Disable `LOCAL_INFILE` if not needed, to prevent certain file-based attacks.
- Set `sql_mode` to include strict modes and `NO_AUTO_CREATE_USER` etc. (to avoid accidental weak user creation).
- If MySQL is on a VM, consider a host-based firewall (e.g., allow port 3306 only from application server IP).

**5. Monitoring and Auditing:** Enable MySQL logs for monitoring. General Query Log and Slow Query Log help with performance and potentially spotting unusual queries. The Error Log is key for detecting failed logins or errors. MySQL Enterprise and some community plugins offer an Audit Log that logs every connection and query (with some performance cost). On Azure, you can enable **Auditing** on the MySQL server which logs to Azure Monitor certain events (like logins, schema changes). You should also enable Azure Defender for MySQL (if available) which can detect anomalous activities (SQL injection patterns, data exfiltration attempts) ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Secure%20MySQL%20in%20the%20Cloud)).

**6. Backup security:** Regular backups of the database are essential (Azure provides automated backups by default with point-in-time restore). Ensure backups are protected (encrypted, and access to them is restricted). A stolen backup is as good as a data breach if not encrypted. Azure’s backups for DB are encrypted at rest by default. If you do your own dumps, encrypt them and store securely (Key Vault could store the keys).

## Encryption at Rest and in Transit

**Encryption in Transit (SSL/TLS):** We’ve emphasized connecting to MySQL using SSL. In Azure Database for MySQL, SSL is enforced by default (the connection string requires `SSL=true` and it will only accept SSL connections unless you disable that). If running MySQL on your own server, you should configure it with SSL certificates. That involves creating a server certificate and key (or using ones from a CA) and updating my.cnf with `ssl-cert`, `ssl-key` parameters. Then require SSL for connections (`REQUIRE SSL` on user accounts or globally). The goal is that any data moving between the app and database is encrypted to thwart eavesdropping. This is especially important in cloud or network environments where others could potentially sniff traffic. As noted earlier, **unencrypted MySQL traffic can be intercepted by attackers via MITM attacks**; using TLS mitigates this ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=By%20default%2C%20MySQL%20uses%20unencrypted,the%20user%E2%80%99s%20integrity%20and%20privacy)). Azure’s service will typically use TLS 1.2 or higher. On the client (Spring Boot side), the JDBC URL `useSSL=true` and possibly `verifyServerCertificate=true` with the server CA cert can ensure no MITM with fake cert. We should obtain the Azure MySQL SSL certificate (public) and configure our app to trust it, or use the `?sslMode=REQUIRED` (or VERIFY_IDENTITY) in JDBC URL for stronger verification.

Citing an Azure baseline: _"Enforcing SSL connections between your database server and your application helps protect against 'man in the middle' attacks by encrypting the data stream between the server and your application."_ ([Azure security baseline for Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline#:~:text=,enabled%20for%20accessing%20your%20database)). We will definitely do that.

**Encryption at Rest:** This means data is encrypted when stored on disk. Azure Database for MySQL automatically does encryption at rest using AES 256 by default for all data, with keys managed by Microsoft. For compliance, sometimes you might want to manage your own keys (customer-managed keys - CMK). Azure allows that: you can link an Azure Key Vault key to the MySQL server for TDE (Transparent Data Encryption), which then uses that instead of the service-managed key ([Data Encryption With Customer Managed Keys - Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-customer-managed-key#:~:text=With%20data%20encryption%20with%20customer,for%20data%20protection%20at%20rest)). If you manage MySQL on a VM, you could use disk encryption (BitLocker or Linux DM-Crypt/LUKS) to encrypt the volume containing MySQL data files. MySQL also has features like InnoDB tablespace encryption and per-table encryption using a keyring plugin ([17.13 InnoDB Data-at-Rest Encryption - MySQL :: Developer Zone](https://dev.mysql.com/doc/refman/en/innodb-data-encryption.html#:~:text=Zone%20dev,redo%20logs%2C%20and%20undo%20logs)) ([Appendix A, Transparent Data Encryption (TDE) and MySQL Keyring](https://dev.mysql.com/doc/mysql-secure-deployment-guide/5.7/en/secure-deployment-data-encryption.html#:~:text=Appendix%20A%2C%20Transparent%20Data%20Encryption,rest%20encryption)), but those are more complex to set up and usually the whole disk encryption is simpler. Regardless, **ensuring encryption at rest means if someone got hold of the physical storage or a backup file, they couldn’t read the data without the key**. This is often a compliance requirement, especially for sensitive personal data. We should note that Azure’s default covers it, but if our policy requires we hold the keys, we can go the BYOK route with Key Vault.

**Column-level encryption:** In some cases, you might encrypt certain fields at the application level before storing (for example, encrypting a credit card number column with an application key). This provides data security even from database admins or in case of some SQL injection that reads data, they’d get cipher text. Our application might not need this level of granularity, but it’s something to consider depending on data sensitivity. If you do it, you must manage keys securely (Key Vault is ideal for storing such keys or using an envelope encryption scheme).

In summary, between TLS in transit and TDE at rest, MySQL data is well-protected from interception and theft. We should verify these are active: e.g., after deployment, test that the JDBC connection is indeed using TLS (MySQL has a status variable to show if connection is SSL). Also, document these for auditors: “All connections to database are encrypted (TLS1.2) ([Azure security baseline for Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline#:~:text=,enabled%20for%20accessing%20your%20database)) and data at rest is encrypted by Azure (AES-256)”.

## User Roles and Permission Management in MySQL

MySQL’s user management system is slightly less granular than some DBMS, but we can still apply roles. In MySQL 8, roles were introduced. A role is a collection of privileges that can be granted to users. For instance, you could create a role `app_readwrite` with certain privileges on the schema and then just grant that role to the user. This makes it easier if you had multiple users or want to adjust privileges centrally.

Given our application likely just uses one user for DB, using roles is optional. But in a larger org, you might have multiple apps or components accessing the DB, and you might define roles like `webapp_role`, `reporting_role` (maybe read-only), etc.

Important practices for user/roles:

- **Unique accounts:** If there are multiple applications or services needing DB access, give each its own account. Don’t share accounts. That way, if one account’s credentials leak, it doesn’t affect others, and you can also track which application performed what action in audit logs (MySQL CURRENT_USER() in logs would show the account).
- **Least Privilege:** As mentioned, tailor privileges. For example, if you have a reporting read-only user, only `SELECT` on necessary tables. If you have a batch job that only inserts records to one table, only `INSERT` on that table.
- **No wildcard host if possible:** We used `'appuser'@'%'` which allows any host. In production, better to restrict to the app server’s host or Azure’s subnet. In Azure Database for MySQL, the concept of hosts is a bit different (it uses username like user@servername). But if self-managed, `'appuser'@'appserverhostname'` or an IP can be used.
- **Account locking and password policies:** MySQL supports policies like password expiration, reuse limits, etc., and as cited, account lock on failed attempts ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Lock%20Users%20Accounts%20on%20Suspicious,Activity)) ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=FAILED_LOGIN_ATTEMPTS%204%20PASSWORD_LOCK_TIME%2010%3B)). For example:
  ```sql
  ALTER USER 'appuser'@'%' PASSWORD EXPIRE INTERVAL 90 DAY;
  ```
  would force password rotation every 90 days for that account (you then have to update app config when it changes, so maybe not for app account frequently, but for human accounts it’s useful). The failed login lock we saw:
  ```sql
  ALTER USER 'someuser'@'%' FAILED_LOGIN_ATTEMPTS 5 PASSWORD_LOCK_TIME 1;
  ```
  This would lock the account for 1 day after 5 failed attempts. Use these carefully for application accounts (if your app has a bug or something, you don’t want it locking itself out), but for interactive accounts it’s great.
- **Remove unused users:** Sometimes you have old accounts or the default `test` user. Drop them to reduce attack surface.

**Principle of Segregation:** If the org has a DBA and developers, ensure that the DBA accounts are separate and highly protected. Application shouldn’t use DBA accounts. Also, consider the environment separation: dev/test environment databases should not connect to production databases and vice versa. For compliance, controlling access to production data is important (only authorized personnel should be able to view production data, etc.).

**Auditing access:** If someone logs into the DB directly (like a DBA via MySQL client), that should be audited. Azure can log admin logins. If self-managed, enable the general log at least for connect/disconnect (but careful, general log logs everything which can be performance heavy; the audit plugin is better for targeted logging).

Finally, ensure you use secure passwords for all DB accounts and rotate them periodically. We’ll use Azure Key Vault to store the DB password so we can update it and update the app config without exposing it.

**Recap:** At this point, our MySQL is configured such that:

- It only accepts secure connections (TLS).
- Data is encrypted on disk.
- The app uses a specific account with only needed privileges.
- All default or unnecessary accounts are removed/disabled.
- We have monitoring and possibly Azure Defender watching the DB for threats ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=Secure%20MySQL%20in%20the%20Cloud)).
- We have backups and know they’re secure.
- If applicable, we’ve documented what data is sensitive in the DB and perhaps added an extra encryption or at least classification tags (Azure allows classifying columns like marking them as containing e.g. Customer Info, which helps in data governance).

These measures address ISO 27001 controls around cryptographic controls (for encryption), access control (database user privileges), operations security (secure configuration, backups, logs), and incident detection (monitoring). In an audit, we’d present evidence like “Database forces SSL and uses TDE, see config here ([Azure security baseline for Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline#:~:text=,enabled%20for%20accessing%20your%20database)), and only authorized service accounts have access, etc.”

**Checklist for Database Security:**

- [x] **Network security**: Database not publicly accessible except to needed components (e.g., via firewall or VNet rules).
- [x] **Accounts**: Only necessary accounts exist, with least privileges. Strong passwords in place, and stored securely (not in code).
- [x] **Encryption**: TLS enforced for connections ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=By%20default%2C%20MySQL%20uses%20unencrypted,the%20user%E2%80%99s%20integrity%20and%20privacy)) ([Azure security baseline for Azure Database for MySQL - Flexible Server | Microsoft Learn](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline#:~:text=,enabled%20for%20accessing%20your%20database)), and at-rest encryption enabled (Azure default or disk encryption).
- [x] **Configs**: Defaults hardened (no anon access, secure config params, etc.).
- [x] **Monitoring**: Logging of DB events enabled (or Azure audit logs), and alerts on suspicious activity (via Azure Defender or manual review).
- [x] **Maintenance**: Regular backups and tested restores (and backups are encrypted).
- [x] **Separation**: Dev/test data is separate from prod (to avoid leaking prod data in less secure environments – more of data governance).

With the database properly secured, we can move on to deploying our application on Azure, where we will apply further security measures at the infrastructure level.

---

# 6. Deploying on Azure

Deploying our full-stack application to Azure will bring our work to life. Azure offers many services and configuration options that can enhance security and help with compliance. In this chapter, we’ll cover:

- Deploying the Spring Boot backend and React frontend on Azure App Service (or alternatives) and ensuring secure configuration.
- Configuring Azure Database for MySQL securely (network isolation, SSL enforcement, Azure-specific settings).
- Using Azure Key Vault to manage secrets (like DB password, JWT secret, etc.) so they are not stored in code or plain config.
- Implementing network security through NSGs and firewalls to restrict access to our resources at the network level.
- Additional Azure security features: managed identities, Azure Monitor, and Azure Firewall/WAF if needed.

By leveraging Azure’s capabilities, we can achieve a robust cloud environment that meets ISO 27001’s requirements for cloud security (which involves secure configuration of cloud resources, controlling access, and protecting data in the cloud).

## Using Azure App Service for Hosting

**Deploying the Spring Boot Backend:** We will use Azure App Service (Web Apps) to host our Spring Boot application. There are a few ways to deploy:

- Build a JAR and use the Azure Maven/Gradle plugin or Azure CLI to deploy it directly.
- Containerize the app (Docker) and deploy to Azure App Service (if using the Web App for Containers feature).
- Use Azure Spring Apps (a managed Spring Cloud service), but that’s a separate service and not needed unless you want a Spring-specific PaaS.
  We’ll proceed with a straightforward approach: package the Spring Boot app as a JAR (`mvn package`) and deploy it to App Service.

**App Service configuration:** We created the App Service earlier with Java runtime. We should double-check settings:

- **Java version**: ensure it matches our app (Java 17).
- **Environment Variables**: We will need to set environment variables or App Settings for things like the database connection URL, DB username, password (or Key Vault reference), JWT secret, etc. App Service has a settings section where you can add these. They will be available as environment vars to the app. Spring Boot can pick them up if we use `spring.datasource.url` etc., we could also use Azure’s Application Settings to override Spring properties (App Service will inject them as if they are in properties).
- **HTTPS Only**: ensure this is On (we did that).
- **TLS version**: App Service by default supports TLS 1.2, but just ensure no old TLS versions are allowed (should be fine by default).
- **Scaling and slots**: If using deployment slots (for staging, etc.), replicate configurations on them.
- **App Service Plan**: For production, use at least Standard or above for better performance and features (like VNet). The Free tier is not for production (also doesn’t support SSL custom certs etc.).

**Deploying the React Frontend:** There are a couple of ways:

- Build the React app into static files (HTML/CSS/JS) and serve them. We can serve static files via Azure Blob Storage static websites or via the Spring Boot app itself (by placing them in `src/main/resources/static` or using a CDN).
- Or create a separate App Service (Node.js or static web app) for the frontend. Azure also has a service called Static Web Apps which is tailored for static frontend + serverless backend, but since we already have a backend, we might not use that here.

A simple way: After building React (`npm run build` produces a `build` folder), we can copy those files into Spring Boot’s resources so the same App Service serves the API and UI. This way, you have one deployment artifact. This is fine for small scale. If you expect heavy traffic, separating might be better.

For completeness, let’s assume we deploy React separately: We could use **Azure Static Web Apps** (which has global CDN and custom domain support). But Static Web Apps might be overkill if we already have infra. Alternatively, create another App Service (Linux with a runtime that can serve static or run Node to serve). But serving static doesn’t need a full App Service; Azure Storage static website is cheaper and simpler. Let’s outline using Azure Storage:

1. Create an Azure Storage account, enable static website hosting on it.
2. Upload the `build` folder contents (especially the index.html and static assets) to the $web container of the storage.
3. That gives you a URL like `https://<storageaccount>.z20.web.core.windows.net`.
4. You can also map a custom domain if needed, and enable HTTPS (Azure provides a CDN or FrontDoor for custom domain HTTPS if needed, or use Static Web Apps service which bundles that).

However, in many enterprise settings, serving the React from the Spring Boot (which might be behind an internal network) is okay. We’ll assume for now maybe we keep them together to reduce complexity: Spring Boot can serve the static files.

**App Service Deployment Steps (for Spring Boot with static React):**

- Use Maven Plugin:
  ```
  mvn azure-webapp:deploy
  ```
  (after configuring the plugin with your Azure details).
- Or, zip deploy: zip the JAR and deployment scripts.
- Or in Azure Portal, use “Deploy from source” connecting to GitHub Actions/DevOps pipeline. Setting up CI/CD is actually part of next chapter (DevSecOps).

Ensure after deployment, the app is running. Check the App Service’s logs (enable application logging in App Service settings, and stream logs) to see if Spring Boot started properly. If any environment variable is missing, the app might fail on connecting to DB, etc. So, set:

- `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD` as App Settings (or use Azure Key Vault references for the password).
- `JWT_SECRET` (if we externalized the JWT signing key).
- Any other config (like if you have an email service API key, etc., put it here or Key Vault).

App Service App Settings are encrypted at rest and not visible to other users, but they are visible (in plaintext) to anyone who has access to that Azure resource in the portal. Using Key Vault references can further limit exposure (the secret’s value isn’t even shown in the portal, just a reference). Let’s discuss that next.

## Configuring Azure SQL (MySQL) Securely

We have the Azure Database for MySQL instance running. A few Azure-specific security measures to cover:

- **Firewall / Network:** If not using private VNet access, ensure the firewall rules on the MySQL server allow only the necessary IPs (the App Service’s outbound IPs). App Service has a set of possible outbound IP addresses (findable in the portal under properties). Add those or a wildcard for Azure datacenter if absolutely needed. A more secure approach: use **VNet integration**. If your App Service is on a Standard tier or above, you can integrate it with a VNet (in Networking settings of App Service). Then, if your MySQL is a Flexible server in a VNet, the app can connect privately. If using MySQL Single Server with no VNet, then you rely on firewall IP rules. For ISO compliance, reducing public exposure is good: ideally, MySQL should not be accessible from the internet at all, only through the App’s network. So Private link it or restrict to App’s IP.
- **SSL Enforcement:** Ensure the MySQL server parameter “require_secure_transport” is ON (it is by default). This means any non-SSL connection is rejected. We already planned for that in the app’s JDBC string.
- **Credentials in Azure:** We should not keep the DB password in the App Service settings in plain text if possible. Instead, store it in Key Vault and use a reference (we’ll do that in the Key Vault section). Alternatively, use Azure Managed Identity to avoid passwords entirely (unfortunately, MySQL doesn’t support Azure AD auth like Azure SQL does; if it were Azure SQL Database, we could use an AD service principal to auth to DB, but for MySQL, password is the way).
- **Azure Defender for MySQL:** In the Azure portal, enable Microsoft Defender for the MySQL server. This will continuously monitor for threats (suspicious queries, vulnerabilities, brute force attacks) and provide alerts. It might cost a bit per hour, but for compliance it's valuable. It corresponds to having intrusion detection on your database.
- **Auditing:** Enable Auditing on the MySQL server (in the Azure portal’s Auditing settings). You can have it store audit logs to Azure Storage or Log Analytics. This will log events like logins, schema changes, etc. Auditing is an ISO 27001 requirement to keep track of database access. We should also configure retention for those logs (say 90 days or as needed).
- **Performance & Availability Settings:** Not directly security, but ensure the MySQL is configured for reliability (zone redundant if available, backups enabled which they are by default). From a security viewpoint, high availability means less chance of downtime (availability is one of the CIA triad).
- **MySQL Credentials management:** If we ever need to rotate the DB password, with Key Vault references and App Service, the process would be: generate new password, update in DB (add new user or change existing), update Key Vault secret, App Service will auto-update the env var (if using reference) or we restart the app, and then remove old credentials. Plan for that as part of maintenance.

## Setting up Azure Key Vault for Secrets Management

Azure Key Vault is a central component for securing secrets. We will use it to store:

- Database password (as a secret).
- Perhaps the JWT signing key/secret.
- Any other secret values (API keys, etc., if any).
- Possibly certificates if we were using custom TLS certs (Key Vault can store certs too, but App Service also can manage certs separately).

**Storing secrets:** Go to the Key Vault, add a secret for each item. For example, add a secret named `DBPassword` with the value of our MySQL app user password. Add a secret named `JwtSecret` for the JWT signing key (which should be a strong random string). Now, Key Vault secrets have versions – each time you update, it creates a new version. This is good for rotation (you can even set an expiry on a secret).

**Accessing secrets from App Service:**
We have two main ways:

1. **Key Vault reference in App Settings:** As found in our earlier search, we can set an App Setting like: `DB_Password` with a value `@Microsoft.KeyVault(SecretUri=https://<yourvault>.vault.azure.net/secrets/DBPassword/<version>)`. App Service will then fetch that secret and make it available as an environment variable `DB_Password` to the app. This requires the App Service’s identity to have permission to Key Vault.
2. **Azure Managed Identity + code integration:** We could give the App Service a Managed Identity (a service principal automatically managed by Azure). Then in our Spring Boot code, use Azure SDK to connect to Key Vault and pull secrets at runtime. This is more complex and not necessary if we can use references. But sometimes you might do it for on-demand fetch or if not using App Service (like in a container on VM you’d code it).

We’ll use method 1 for simplicity:

- Enable **Managed Identity** on the App Service: In the App Service’s Identity section, turn on System-Assigned Identity. This gives the App Service a service principal ID.
- In Key Vault’s Access Policy (if using Vault policy model) or Azure RBAC (if using that model for Key Vault), grant this identity **Get** and **List** permissions on secrets (at least). If using RBAC, assign the role `Key Vault Secrets User` to the App’s principal on the Vault.
- Now, you can use the `@Microsoft.KeyVault(SecretUri=...)` syntax in the App Service settings. Alternatively, Azure now also allows using Key Vault references in connection strings section similarly.
- For example, go to App Service > Configuration > New Application Setting:
  - Name: `SPRING_DATASOURCE_PASSWORD` (to override Spring’s password property).
  - Value: `@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/DBPassword/********)` (you can use the current version URI or the secret base URI to always get latest).

Once you save that, the App Service will attempt to fetch from Key Vault (it may take a minute and if identity or access not set right, it will show an error in a log or on that settings blade). When it works, the value will appear as something like `@Microsoft.KeyVault(...)` still (they don't show the secret, obviously).

Do the same for `JWT_SECRET` or other secrets. Alternatively, you can also store entire DB connection string in Key Vault; but we can just store parts.

**Benefits:** Now the actual secret values are not visible in the App Service or in our code repo; they are safely in Key Vault (which is heavily protected: it requires Azure AD auth to access, and can have its own firewall and purge protection etc.). This reduces risk: even if someone got read access to the App Service config, they wouldn’t see the actual password. Also, rotating secrets is easier: update in Key Vault, and the next time the app reads it (App Service refreshes them roughly every 24h or on restart, but one can manually trigger sync or keep short-lived secrets accordingly).

We should cite best practices: _"Lock down access to your key vaults by allowing only authorized applications and users... restrict network access with Private Link or firewall" ([Best practices for using Azure Key Vault | Microsoft Learn](https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices#:~:text=,6%20firewall%20and%20virtual))._ That means we should also consider Key Vault’s firewall. Key Vault can be made accessible only via selected networks or via Private Endpoint. If we integrate with a VNet, we could restrict Key Vault to that VNet. However, App Service managed identity access doesn’t require the vault be on VNet (it goes over Azure backbone). But for extra lock-down, enabling the firewall to only allow trusted Azure services and perhaps certain IPs can be done. ISO 27001 would want Key Vault tightly controlled: definitely use RBAC to restrict who (which identities) can get secrets ([Best practices for using Azure Key Vault | Microsoft Learn](https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices#:~:text=,6%20firewall%20and%20virtual)). We’ve done that by only giving the App and perhaps certain admin user access.

**Managed Identity usage elsewhere:** We could also use the App’s managed identity to access other services (like Azure SQL if we had it, or Storage accounts). For example, if our app needed to write files to Azure Blob, we could assign it a role on a storage account and use Azure SDK without connection strings.

## Implementing Network Security Groups (NSG) and Firewalls

Network Security Groups in Azure act as virtual firewalls at the network interface or subnet level, controlling traffic based on rules (allow/deny for IPs/ports). In our architecture:

- If App Service and Database are fully PaaS, we can incorporate NSGs only if we use a VNet. If we put MySQL in a VNet (private), and App Service integrates with that VNet, we can attach an NSG to the subnet where MySQL’s private endpoint resides. That NSG could, for example, allow traffic on port 3306 from the App Service subnet only, and deny all else.
- Additionally, if we had VMs or other services, we’d use NSGs similarly. In an App-Service only scenario, the platform somewhat abstracts network, but using Private Endpoints essentially places a network interface in your VNet for the service.

**We should aim to restrict network access so that:**

- The database is not reachable by anything except the App Service (and perhaps an admin IP for maintenance if needed).
- The App Service (our web app) is reachable by end users via HTTPS, but perhaps we block certain ports (App Service by default only opens 80/443 for HTTP and maybe FTP for deploy – we should disable FTP in App Service if not needed, and use FTPS or disable completely as it's another potential vector).
- Key Vault access is restricted to the App’s managed identity, and optionally via network rules.

For NSGs:
If using a VNet for MySQL (in case of flexible server with private access):

- Create an NSG for the MySQL subnet: default might already allow MySQL within VNet. Add an explicit rule: allow source = AppServiceSubnet on port 3306, deny others. This way, even if someone got onto the VNet from another route, by default others are denied.
- The App Service outbound to VNet is usually dynamic, but since we integrated, it will come from a specific subnet (the one you integrated with).
- Use Application Security Groups (ASG) if dealing with many IPs: e.g., define an ASG for “AppServers” containing the App Service subnet’s instances, and use that in NSG rules for clarity.

If not using VNet integration:

- We rely on Azure MySQL firewall at platform level. We already set that to allow only App Service’s fixed outbound IPs. That essentially acts like an NSG. There's no NSG because it's not in our VNet.

**Azure Firewall / WAF:**
For web traffic, you might consider using a Web Application Firewall (WAF) in front of App Service. Azure offers WAF via Azure Front Door or Application Gateway. This can filter malicious HTTP requests (like blocking known SQL injection patterns, XSS patterns at the edge). If our app is high-risk or needs extra layer, a WAF is recommended. It’s not explicitly in the question, but network security also encompasses that. A WAF can help meet requirements for detecting and preventing web attacks (which could be part of ISO controls or just best practice). We won't detail it fully, but mention that enabling a WAF could be done by putting App Service behind an App Gateway WAF and locking direct access (Service Endpoints). That’s a more complex architecture though.

**Restricting outbound from App Service:** By default, App Services can call out to the internet (for example, to call external APIs). If our app doesn’t need that, Azure is introducing features to restrict outbound. However, often you might need some outbound (to Key Vault, to maybe send emails via an API, etc.). Ensure any such external call is to a trusted endpoint and use HTTPS.

**Summary of NSG/Firewall**: In Azure, multiple layers:

- App Service: ensure no unwanted ports (disable FTP or use FTPS only, and restrict its user). Consider IP restrictions on App Service (it has an Access Restriction feature where you can limit which IPs or VNets can reach the app; e.g., if this was internal app, you could restrict client IPs).
- Database: firewall rules or NSG such that only app can talk to DB ([Best practice check list for Virtual network for security and ...](https://learn.microsoft.com/en-us/answers/questions/1320460/best-practice-check-list-for-virtual-network-for-s#:~:text=Best%20practice%20check%20list%20for,only%20necessary%20ports%20and%20protocols)). “Restrict network access by allowing only necessary ports and protocols” ([Best practice check list for Virtual network for security and ...](https://learn.microsoft.com/en-us/answers/questions/1320460/best-practice-check-list-for-virtual-network-for-s#:~:text=Best%20practice%20check%20list%20for,only%20necessary%20ports%20and%20protocols)) – we do exactly that.
- Key Vault: firewall to restrict as needed.
- Possibly an overall NSG on the VNet if we have one, with default deny inbound from internet on private subnets, etc.
- If using a jumpbox or bastion for admin access, that should be locked down, etc.

**Enabling NSG Flow Logs:** If heavy on compliance, you might even log NSG flow logs to see what traffic was allowed/denied. Usually not needed unless investigating an incident.

Now, at the end of deployment, do a sanity check:

- Visit the React frontend (on the given domain or static site) and see that it loads over HTTPS.
- Try logging in, ensure it works (calls to the API succeed).
- Test that you cannot access restricted data without auth (maybe using a tool like curl to call an API without token returns 401).
- Possibly run a vulnerability scan or penetration test against the app to catch anything we missed (this is part of DevSecOps/testing, covered next).
- Ensure monitoring is capturing events: e.g. see App Service access logs, see if Application Insights capturing requests (if integrated).
- Check Azure Monitor for any security recommendations: Azure Security Center (Defender for Cloud) might flag things if misconfigured (like if we left DB open to all IP, it will warn). Address any of those.

**Checklist for Azure Deployment Security:**

- [x] App Service running with HTTPS enforced and correct environment configuration (no secrets in code or settings, using Key Vault references).
- [x] Managed Identity enabled and functioning (for Key Vault access).
- [x] Key Vault holds all sensitive secrets; Key Vault access is restricted to needed principals ([Best practices for using Azure Key Vault | Microsoft Learn](https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices#:~:text=,6%20firewall%20and%20virtual)) and optionally via network.
- [x] Database accessible only to App Service (verified by firewall or VNet NSG) ([Best practice check list for Virtual network for security and ...](https://learn.microsoft.com/en-us/answers/questions/1320460/best-practice-check-list-for-virtual-network-for-s#:~:text=Best%20practice%20check%20list%20for,only%20necessary%20ports%20and%20protocols)).
- [x] Database has SSL on (test by trying a non-SSL connection which should fail).
- [x] Azure Defender and Auditing enabled on DB (verify alerts/logs generation).
- [x] Any administrative interfaces (Azure Portal, SSH to VMs if any, etc.) are protected (MFA on Azure accounts, etc., which is beyond app but part of ISO compliance to secure cloud console access).
- [x] Logging from app and database is being collected/stored securely (we will detail in final section how we monitor).

Now the application is live and secure in Azure. Next, we address the practices around DevSecOps – making sure our CI/CD pipeline and development process continuously keep security in mind.

---

# 7. DevSecOps and CI/CD Security

Security should be integrated into the development pipeline – this concept is often called DevSecOps (Development, Security, Operations). In this chapter, we focus on how to set up a Continuous Integration/Continuous Deployment (CI/CD) pipeline that not only automates build and deployment of our React/Spring Boot app, but also incorporates security at each stage. We’ll cover:

- Establishing a secure CI/CD pipeline (e.g., using GitHub Actions, Azure DevOps, or others) with proper access controls.
- Integrating automated security tests into the pipeline, such as static code analysis (SAST), dependency vulnerability scanning, and dynamic security testing.
- Secrets management in CI/CD (ensuring that deployment keys, credentials, etc., are handled safely).
- Ensuring the pipeline itself is secure (guarding against supply chain attacks, malicious commits, etc.).
- Code scanning for vulnerabilities on an ongoing basis.

These practices help catch issues early (shift-left security) and ensure that every code change is evaluated for security, which is essential for maintaining ISO 27001 compliance over time. ISO 27001 emphasizes not just one-time security, but continuous improvement and monitoring – a secure pipeline plays a big part in that.

## Setting Up a Secure CI/CD Pipeline

Let’s assume we use a common setup like **GitHub** for code and **GitHub Actions** for CI/CD, or **Azure DevOps** (ADO) repos and pipelines. The principles apply to any platform (GitLab CI, Jenkins, etc.). Key steps for a secure pipeline:

**1. Code Repository Security:**

- Use private repositories (our code should not be public unless intentionally open source).
- Enforce multi-factor authentication for repository access (so developers need MFA to push code, this might be done via the platform’s policy).
- Use branch protection rules: e.g., require pull request reviews for merging into main branch, and perhaps require CI tests (including security scans) to pass before merge. This ensures no single developer can push code to production without oversight – reducing risk of malicious or poor-quality code.
- Sign commits or use verified commits if possible. Not all workflows use commit signing, but it adds trust (ensuring commits come from who they say they are).
- Limit who has write access to main branches, and who can approve PRs. This ties into ISO’s access control for source code.

**2. Least Privilege for CI/CD accounts:**
If using a dedicated CI server or service, ensure it has only the needed access. In GitHub Actions, the runner by default has permissions to the repo content; you can adjust token permissions (for example, if the workflow doesn’t need to push back to repo, set those permissions to read-only). For deployment, create an Azure Service Principal with narrow rights (just enough to deploy to that App Service and manage that Resource Group, not owner of entire subscription). In Azure DevOps, use service connections with minimal scope. This practice is part of **“Enforce Least Privilege Access”** in CI/CD ([Secure Your CI/CD Pipelines: 7 Best Practices You Can’t Ignore - Spectral](https://spectralops.io/blog/secure-your-ci-cd-pipelines-7-best-practices-you-cant-ignore/#:~:text=1)) – avoid using an all-powerful credential when a limited one suffices.

**3. Secure Build Environment:**
If using cloud-hosted runners, keep secrets (like signing keys or environment secrets) in the platform’s secure secret store (GitHub Secrets, Azure DevOps Library). **Never store secrets in plaintext in the repo.** Rotate these secrets periodically. Use the CI provider’s features like secret masking (they usually mask secrets in logs). Avoid echoing secrets or storing them in artifacts. Also, ensure the build agents are up-to-date – but if using cloud agents, this is handled by provider.

**4. Dependency Management:**
Our application uses dependencies (npm packages for React, Maven dependencies for Spring). We should automate checking these for known vulnerabilities (this is part of SCA – Software Composition Analysis). For example:

- Use tools like **Dependabot** (GitHub) to automatically alert and even PR updates for vulnerable libraries.
- Use **OWASP Dependency Check** or Snyk or Whitesource scans in the build. GitHub has Dependabot and also a built-in advisory database and secret scanning.
- In Maven, we could run the OWASP dependency-check plugin which generates a report on vulnerable dependencies. We can fail the build if any high severity issues are present.
- For npm, `npm audit` can be run as part of build (though in recent times it's noisy; better to use a more curated audit or Snyk CLI to break build on issues above threshold).

**5. Static Code Analysis (SAST):**
This involves analyzing our code for vulnerabilities without executing it. There are tools for different languages:

- For Java (Spring Boot), we can use tools like **SpotBugs with find-sec-bugs**, or **SonarQube** (with security rules), or commercial ones like Checkmarx, Fortify. SonarCloud (cloud SonarQube by SonarSource) can integrate in CI easily and has rules that cover OWASP Top 10 issues.
- For JavaScript/React, ESLint can catch some issues, but specialized security linters or Sonar might catch things like use of `innerHTML` (potential XSS), usage of dangerous APIs, etc.
- Integrate these tools in the CI pipeline (e.g., run `mvn verify sonar:sonar` if using SonarCloud with the token, or run a SpotBugs analysis and possibly fail on certain findings).
  The updated ISO 27001:2022 explicitly calls for security testing in the SDLC ([For ISO 27001 compliance, test application security across your SDLC | Invicti](https://www.invicti.com/blog/web-security/iso-27001-compliance-test-application-security-across-your-sdlc/#:~:text=its%20companion%20document%2C%20ISO%2027002%2C,the%20SDLC%2C%20stating%3A%20%E2%80%9CSecurity%20testing)). This includes SAST as an early step.

**6. Container scanning:** If we containerize our app, scan the Docker image for vulnerabilities (e.g., using Trivy or Aqua). Even if not, scanning the OS of the App Service is Azure’s domain, but any container or VM images should be scanned.

**7. Integration and Unit Tests:** While functional tests ensure app works, security tests ensure app securely handles edge cases. Include some unit tests for security-critical code (e.g., does the password encoder properly reject invalid matches, are certain endpoints unauthorized for normal users). Also, integration tests that simulate an unauthorized access should get 401/403.

**8. Infrastructure as Code scanning:** If we used Terraform or ARM templates or GitHub Actions to define infra, use a scanner (like Checkov or Azure Resource Manager Analyzer) to catch misconfigurations (e.g., if a storage account allows public access, etc.). This might be less relevant for our setup since we did a lot manually, but good to note.

After building, have the pipeline deploy (if tests pass). Use environment approvals if needed (e.g., manual approval to deploy to production, or ring deployments). Keep artifact management secure (the built JAR should be stored or directly deployed; ensure no tampering between build and deploy. Use checksums or signed artifacts for integrity if needed).

**Pipeline Example:** Using GitHub Actions pseudo-code:

```yaml
name: CI-CD

on:
  push:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          distribution: "Temurin"
          java-version: "17"
      - name: Cache Maven
        uses: actions/cache@v3
        with:
          path: ~/.m2
          key: ${{ runner.os }}-maven-${{ hashFiles('pom.xml') }}
          restore-keys: ${{ runner.os }}-maven-
      - name: Build Backend
        run: mvn verify -DskipTests=false
      - name: Run OWASP Dependency Check
        run: mvn org.owasp:dependency-check-maven:check
      - name: Analyze with SonarCloud
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: mvn sonar:sonar -Dsonar.projectKey=myproj -Dsonar.organization=myorg
      - name: Build Frontend
        uses: actions/setup-node@v3 # set up Node
        with:
          node-version: "18"
      - run: npm ci && npm run build --if-present
      - name: Lint and Audit Frontend
        run: |
          npm run lint
          npm audit --production
      - name: Dependency review (GitHub built-in)
        uses: github/dependency-review-action@v2
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: app-package
          path: target/app.jar
    # Only proceed to deploy if above steps succeed and on main branch merges, possibly manual approval
  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v3
        with: { name: app-package }
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }} # Service principal JSON
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: "SecureFullStackApp"
          package: "target/app.jar"
```

The above is a rough idea. It includes dependency checks, Sonar scan, lint, audit, etc. If any step fails (e.g., Sonar finds quality gate fail or dependency check finds a vulnerability), the pipeline fails and code won’t deploy until addressed. This addresses multiple points:

- **Multiple security testing approaches**: SAST (Sonar), dependency scan (OWASP DC, npm audit), which aligns with guidance that a “multi-level approach” is needed ([For ISO 27001 compliance, test application security across your SDLC | Invicti](https://www.invicti.com/blog/web-security/iso-27001-compliance-test-application-security-across-your-sdlc/#:~:text=%3E%20%20%20,is%20available%20for%20doing%20so)).
- **Secrets in pipeline**: uses GitHub Secrets for Sonar token and Azure credentials. The Azure credentials secret would be a JSON with clientId, clientSecret, tenant, which has rights only to that resource group ideally (least privilege).
- **Compliance**: we can demonstrate to an auditor that for every code change, these security checks run, and we don’t deploy if something’s wrong – fulfilling secure development lifecycle controls.

## Automated Security Testing Tools Integration

To elaborate on tools:

- **Static Application Security Testing (SAST)**: Tools like SonarQube (with security rules enabled) or dedicated SAST (Fortify, Veracode) can be integrated to run on each build or regularly. They scan for things like SQL injection, XSS, insecure config in code. We want to ensure these run automatically and results are reviewed. Perhaps enforce that no high-severity issue is allowed before release (set a quality gate).
- **Software Composition Analysis (SCA)**: This covers dependency scanning as discussed. Also container image scanning if applicable.
- **Dynamic Application Security Testing (DAST)**: This is where you run a running app and scan it like an attacker (e.g., OWASP ZAP, Burp Suite automated scans). You might do this in a staging environment as part of CI/CD. For example, deploy the app to a test environment and run OWASP ZAP in CI against it to fuzz for XSS, SQLi, etc. This is a bit heavier but can be scheduled maybe nightly or for each major release. Invicti (from earlier reference) and others can do it.
- **Interactive Application Security Testing (IAST)**: Tools that run inside the app during tests to find vulns (like Contrast Security) could also be used if desired.
- **Unit tests for security**: We can include some security-specific tests (like ensure our security config indeed requires auth on certain endpoints by calling them in a test context and expecting 401).

**Automated Code Scanning**: If using GitHub, you can also enable “CodeQL” scanning – GitHub’s code scanning that finds security issues for supported languages (Java, JS included). It’s quite powerful and can be run on schedule or PRs.

**Quality Gates**: It’s important not just to run these tools but to have a policy. For example, Sonar quality gate might say: build fails if new code introduces any blocker or critical security issue. Dependency check might fail on any Critical CVE. These thresholds should be set in consultation with the security team. Also, provide developers with training on how to fix issues found.

One must balance false positives and true issues – tune the tools to reduce noise so developers don’t get habituated to ignoring them. For ISO, showing that you have these tools integrated and you act on them is great evidence of proactive security.

## Code Scanning for Vulnerabilities

We partly covered this, but to emphasize:

- **Continuous scanning**: Tools like Dependabot create PRs for updating vulnerable libs; ensure someone is assigned to handle those promptly. Maybe even auto-merge minor updates after tests pass.
- **Periodic manual reviews**: In addition to automated scanning, maybe quarterly or so, do a manual code review focusing on security-critical areas. Or have an external review for fresh eyes. This might not be in pipeline but is part of a secure development process.
- **Secret scanning**: Ensure no secrets accidentally committed. GitHub by default scans for known secret patterns (like AWS keys) and alerts. Use that. Also consider running truffleHog or GitLeaks on the repo as a check.
- **Infrastructure scanning**: If you have infrastructure config, use tools like Terraform-compliance or ARM review for vulnerabilities.

All of this ties back to ISO 27001 control that requires testing security of systems throughout development ([For ISO 27001 compliance, test application security across your SDLC | Invicti](https://www.invicti.com/blog/web-security/iso-27001-compliance-test-application-security-across-your-sdlc/#:~:text=%3E%20%20%20,)) ([For ISO 27001 compliance, test application security across your SDLC | Invicti](https://www.invicti.com/blog/web-security/iso-27001-compliance-test-application-security-across-your-sdlc/#:~:text=throughout%20the%20software%20development%20life,the%20SDLC%2C%20stating%3A%20%E2%80%9CSecurity%20testing)). We are establishing a practice that every build and release goes through rigorous security gates. Additionally, maintain documentation of these processes – e.g., a secure coding guideline document for developers (which might list all these practices, rules to follow, etc.), and records of scan results (so if an auditor asks “do you scan for vulns?”, you can show reports and that you fixed them).

**DevSecOps Cultural Aspect:** Encourage developers to treat security findings with the same importance as bugs. Possibly include security tasks in sprint planning if using agile. The pipeline helps automate enforcement, but team mindset matters too.

**Protecting the CI infrastructure:** If using self-hosted build agents, ensure those VMs are secured (patched, not accessible to outside, etc.). If a build agent is compromised, an attacker could inject malicious code into builds or steal secrets. Cloud-hosted ones reduce that risk but still ensure your pipeline definitions are not allowing untrusted code to run in privileged context. For example, if you run PR builds from forked repos, be careful as that could run code from an unknown contributor in your environment (GitHub actions mitigates with reduced permissions for fork PRs tokens, but still something to be aware of).

**Deployment environment segregation:** Have separate environments for dev/test/prod in pipeline. Possibly use Infrastructure as Code so that dev environment mimics prod. This aligns with having separate dev/test environments in secure dev lifecycle (Annex A 8.25 expects separate env for dev/test/prod) ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Separate%20Environments)).

**Notifications and Monitoring of CI/CD:** If a build fails due to a security scan, ensure it's visible (notifications to devs). Also, monitor your CI runs for any abnormal activity (like if a unknown job triggers or an odd pattern that could indicate someone abusing it).

**Checklist for DevSecOps Pipeline:**

- [x] **Version control security**: MFA, access control, branch protections in place.
- [x] **Pipeline access**: CI service principles with least privileges (no overly broad credentials) ([Secure Your CI/CD Pipelines: 7 Best Practices You Can’t Ignore - Spectral](https://spectralops.io/blog/secure-your-ci-cd-pipelines-7-best-practices-you-cant-ignore/#:~:text=1)).
- [x] **Secrets in CI**: stored in secure vaults (e.g., GH Secrets or Azure Key Vault) and not visible in logs (check logs for any accidental prints).
- [x] **Automated tests**: unit/integration tests covering critical scenarios pass.
- [x] **SAST** integrated (and failing build on high issues).
- [x] **Dependency scanning** integrated (fail on severe vulns, and routine updates).
- [x] **DAST** scheduled or run on staging environment.
- [x] **Code review**: human review required for merges, focusing on security in reviews.
- [x] **Documentation**: Security considerations documented (maybe a section in PR template “Does this change affect security? If so, what tests done?” – some teams do that).
- [x] **Issue tracking**: If any vulnerability is found, track it to resolution (ISO likes to see that issues are not ignored; maybe maintain a log of vulnerabilities and how they were fixed).

By implementing DevSecOps, we ensure security is not a gate at the end but a built-in quality metric from the start. This greatly aids in ISO 27001 compliance as it demonstrates a repeatable, managed process for security in development. Next, we will discuss ISO 27001 compliance more directly, summarizing how all these controls fulfill the standard and what additional steps are needed for certification readiness.

---

# 8. ISO 27001 Compliance Best Practices

Up to now, we’ve been implicitly addressing many ISO 27001 requirements by implementing security controls in our app and environment. In this chapter, we’ll explicitly focus on ISO 27001 compliance, ensuring we haven’t missed any key aspects. We will cover:

- Implementing required security controls from ISO 27001 Annex A as they relate to software development and operations.
- Conducting risk assessment and how it feeds into what controls we apply.
- Maintaining logs and audit trails not just in the app, but for overall system (covering who did deployments, who accessed what, etc.).
- Preparing for ISO 27001 certification: documentation needed, evidence to collect, and how to demonstrate compliance.

ISO 27001 compliance is about having a systematic approach to managing information security (the ISMS). It’s not only about tech, but also people and processes. Our focus will be on what an advanced developer or DevOps engineer should do in this project to align with those practices.

## Implementing Required Security Controls

ISO 27001 Annex A (especially the 2022 revision) lists 93 controls categorized into themes like Organizational, People, Physical, Technological. Many controls apply to processes beyond coding (like security policy, HR security, supplier management). We will focus on those relevant to our full-stack application development and hosting.

Key controls and how we implemented them (or plan to):

- **A.5 Information Security Policies**: Ensure an overall security policy exists. As developers, be aware of it. For instance, a policy may state “All software must be developed following secure coding guidelines and undergo security testing.” We effectively followed this by incorporating OWASP best practices and pipeline scans. For compliance, there should be a written Secure Development Policy ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Secure%20Development%20Policy)) in the company. Advanced developers might help draft technical guidelines in it.

- **A.6 Organization of Information Security**: This covers roles and responsibilities. In a project context, make sure someone is responsible for security of the app (could be a security champion in the dev team). Also, if working with cloud, define who can access what (we did by restricting Azure roles). If an outsourced component is used, ensure contracts cover security.

- **A.8 Human Resource Security**: Not directly development, but ensure developers are trained in security (which we assumed as advanced devs). Possibly maintain training records or certs (some orgs require devs to take annual secure coding training – that helps compliance).

- **A.8.25 Secure Development Life Cycle** (from ISO 27001:2022 Annex A) ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=What%20is%20ISO%2027001%20Secure,Development)): This control specifically requires organizations to have secure development practices (we have been detailing those throughout):

  - Having secure coding guidelines (like OWASP, which we followed) ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Coding%20Guidelines)).
  - Using version control, code review (we included branch protections).
  - Separate dev/test/prod environments ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Separate%20Environments)).
  - Security testing at appropriate stages (we integrated SAST/DAST).
  - Managing open source risk (we included dependency scanning).
  - Ensuring secrets are not in code (we used Key Vault).
  - Also, cryptographic controls (we used TLS, encryption).
  - The standard also calls for consideration of security in design – we did by designing with RBAC, threat modeling implicitly.
  - It expects documentation of these practices and evidence that they’re applied.

- **A.8.28 Secure Coding**: This new control (if specifically present) would likely align with following guidelines and using tools to detect code issues. We can show we have a coding standard (like “we follow OWASP Top 10 in development”) and we actually use static analysis to enforce it.

- **A.5.23 Control of Software Installation**: Make sure only authorized software is installed on servers/environments. In Azure PaaS, this is less an issue (we deploy what we need). But ensure no one installs random software on the App Service (can't really) or on build agents. Company might have an approved list of libraries. As a dev, be mindful not to include suspicious packages.

- **A.8.9 Configuration Management**: We maintained config securely (externalized secrets, used Azure config management). Ensure we have a process to track config changes (Infra as Code helps, or at least keep a record of changes in Azure). Also ensure default credentials in any component were changed (we did for DB, none in app since we made accounts).

- **A.5.18 Access Control** (and related controls in A.8): We implemented RBAC at app level and also Azure RBAC. Good practice: maintain an Access Control Matrix for the application – a document listing which roles can access which functions/data. We basically have: Admin vs User capabilities as code, but writing it out helps communication and compliance. Also ensure user accounts in the app are managed securely (e.g., if a user leaves, their account gets disabled if it's separate from AD integration, etc.). For admin access to the system (like Azure admins, DB admins), ensure principle of least privilege and multi-factor auth. These align with ISO controls on system access control and user access management.

- **A.8.27 Secure Authentication**: Ensure robust authentication mechanisms. We used JWT with strong secrets, password hashing. Also consider implementing MFA at application level for user login if high security (not done in code here, but maybe using OAuth to Azure AD which can enforce MFA). ISO loves MFA for sensitive systems.

- **A.8.8 Vulnerability Management**: We set up scanning and updating which is vulnerability management in dev. Also ensure there's a process to get alerts (like via mailing list for new vulns, or vendor notices) and act. Document how quickly critical patches are applied (patch policy). We already planned immediate dependency updates and monthly patch for OS (Azure PaaS covers OS mostly).

- **A.8.31 Monitoring Activities**: We have logging and monitoring. Ensure logs (both application and Azure logs) are reviewed regularly. Maybe set up alerts on certain events (like many failed logins or maybe unusual high 500 errors). As part of compliance, define monitoring procedures: e.g., have a dashboard or weekly log review for security events. We set logging of admin actions (like user deletion) which should be reviewed by someone.

- **A.8.30 Event Logging**: We ensure all security-relevant events are logged ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=9,events)). We should also protect log integrity – only authorized can delete logs. In Azure, give limited access to who can clear diagnostic logs. Perhaps export logs to a secure log analytics workspace where only certain roles can modify.

- **A.5.30 Backup**: Make sure backups of code and data are done. Code is in git (with redundancy if cloud), database backups via Azure auto-backup (verify it’s enabled and tested). Document backup schedule and retention and test restoration.

- **A.5.21 Cryptography**: We used encryption but need to document our cryptographic controls. For compliance, maintain an inventory of where encryption is used and key management. For instance:

  - Data in transit: TLS 1.2 for all HTTPS and MySQL (managed by certs, some by Azure).
  - Data at rest: Azure-managed AES-256 for DB, also VM disks if any.
  - JWT secret key: managed in Key Vault (which uses HSM potentially).
  - Password hashing: using bcrypt with appropriate work factor.
  - All these should be in line with any cryptographic policy (maybe the policy says “must use approved algorithms like AES, RSA, SHA-256, etc.” We are using AES for rest (by Azure) and TLS which is typically using AES for symmetric cipher, and bcrypt (which is fine).

- **A.8.1 User endpoint protection**: If developers use their laptops to code, ensure their endpoints are secure (AV, disk encryption, etc.). Not directly our app, but part of compliance.

- **A.5.7 Threat Intelligence & A.5.23 Monitoring and Review**: This is more organizational, but in context, stay updated on threats relevant to our stack (subscribe to security bulletins, e.g., Spring security issues like Spring4Shell was cited ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=Spring%20Boot%20is%20widely%20used,a%20severe%20implications%20for%20organizations)), we should patch as soon as known). And regularly review the security posture of our system.

- **A.8.26 Outsourced Development**: If using third-party components or services, ensure contracts or assessments of their security. We rely on Azure (which has its certifications) and libraries (where we manage via license checks and vulnerability scans). If we hired an external dev for part, ensure they follow same standards.

In implementing these controls, **documentation is key**. For each control, have something written:

- e.g., Secure Coding Guidelines (maybe referencing OWASP Cheat Sheets).
- Access Control Policy (which covers how user roles are managed).
- Incident Response Plan (coming up).
- Change Management procedure (how changes to code/config are approved, which we did via PRs and pipeline as technical enforcement, but also note in process docs).
- Asset inventory: list our components (frontend, backend, DB, what data is stored, classification of data if needed like personal data classification).
- Risk assessment report: identify risks (like “unauthorized access to data” mitigated by auth & encryption, “SQL injection” mitigated by coding practice and WAF, etc.) with their severity and how we handle them.

## Risk Assessment and Mitigation Strategies

Risk assessment is fundamental in ISO 27001. Let's outline how one might approach it for our full-stack system:

1. **Identify Assets**: e.g., Web Application (frontend & backend), Database, Azure infrastructure, Source code repository, CI/CD pipeline. Also data assets like user data stored in DB.
2. **Identify Threats/Vulnerabilities**: For each asset, what could go wrong? (threat modeling)
   - Web application: could be attacked via web vulnerabilities (SQLi, XSS, CSRF, auth bypass). Data could be stolen if broken.
   - Database: might be targeted via network (if exposed) or SQL injection, or weak cred.
   - Infrastructure: misconfiguration could allow unauthorized access (like leaving DB open or losing keys).
   - Source code repo: if compromised, attacker can inject malicious code (supply chain attack).
   - CI/CD: If pipeline is insecure, secrets could leak or malicious code deployed.
   - Admin actions: a malicious admin or dev could misuse privileges (insider threat).
   - Physical: not so much here with cloud, but dev machines could be stolen (hence dev machine encryption).
3. **Evaluate Risks**: Determine likelihood and impact. For example, SQL injection: likelihood medium (if code not protected) and impact high (DB compromised) – which we mitigate. Or Data center outage: Azure region down (impact high, likelihood low).
4. **Mitigation Controls**: We list controls we have for each threat:
   - Web vulns: mitigated by secure coding (SAST, code reviews) ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=3)), input validation, Spring Security, WAF.
   - Unauthorized access: mitigated by strong auth (JWT, hashed passwords), RBAC, logging attempts, account lockouts.
   - Data exposure: mitigated by encryption (TLS, at rest) ([MySQL Security Best Practices | IEEE Computer Society](https://www.computer.org/publications/tech-news/trends/mysql-security-best-practices/#:~:text=By%20default%2C%20MySQL%20uses%20unencrypted,the%20user%E2%80%99s%20integrity%20and%20privacy)).
   - DB attack: mitigated by network isolation, least privilege user, Azure Defender.
   - Pipeline attack: mitigated by secrets management, least privilege creds ([Secure Your CI/CD Pipelines: 7 Best Practices You Can’t Ignore - Spectral](https://spectralops.io/blog/secure-your-ci-cd-pipelines-7-best-practices-you-cant-ignore/#:~:text=Where%20Do%20Security%20Risks%20Occur,in%20CI%2FCD%20Pipelines)), code scanning.
   - Etc.
     We also note any residual risk (maybe if using a new library that could have 0-day, residual risk accepted).
5. **Risk Treatment Plan**: For any high risks not mitigated, plan how to treat (add controls or accept if cost too high, etc.).
6. **Document and approve**: Management should approve the risk assessment and decisions.

We should maintain this document and update when things change (like new features or new threats discovered). ISO auditors will want to see a risk assessment process. We should tie our controls to specific risks (traceability).

## Maintaining Logs and Audit Trails

We've implemented logging in the app and enabled logs in Azure. Now, ensure we **retain** and **monitor** those logs:

- Set up centralized logging. For instance, use Azure Monitor (Log Analytics) to gather App Service logs, Key Vault logs (KV can log secret access), and possibly OS logs if any VM (we have PaaS mostly). The database auditing logs can go to Log Analytics as well.
- Retention: decide how long logs are kept. Many keep 90 days online, older archived for a year or more. Azure allows setting retention on Log Analytics. Ensure it meets any regulatory requirement (maybe 1 year for security logs).
- Protect logs: Only give read access to logs to necessary roles (like security team). Write access (to configure logging) to admins. This prevents log tampering.
- Audit trails: For our context, audit trail includes:
  - Application logs of user actions (like admin events).
  - Azure AD logs for who accessed Azure resources.
  - Azure Activity Log (who created/modified resources).
  - CI/CD audit (who ran what pipeline, who approved a deployment).
  - Database logs of queries or logins.
  - If dealing with personal data, also log data access events if needed for compliance with privacy (maybe beyond ISO, more GDPR).
- Regularly review these logs. Perhaps use Azure Sentinel or another SIEM to analyze logs for anomalies and generate alerts (like multiple failed logins, unusual IP access, etc.). This can significantly aid in incident detection (which is required, to have a process for detecting and responding to incidents).

**Audit example**: If an admin user deletes a record via the API, our logs should show "Admin X deleted record Y at time Z". If later there's an investigation (maybe data was wrongly deleted), we can trace who did it. Similarly, if a new user is created, log which admin created them.

The logs also help in demonstrating compliance: we can show we log security events ([10 best practices to secure your Spring Boot applications](https://escape.tech/blog/security-best-practices-for-spring-boot-applications/#:~:text=9,events)) and that we have a process to review them.

Additionally, consider enabling **audit logging on the application level for security-related changes** (like config changes). For instance, if we had a feature toggles or something, log when they're changed and by whom.

## Preparing for ISO 27001 Certification

If the goal is actual certification, beyond implementing controls, we need to ensure the ISMS (Information Security Management System) is documented and functioning. Steps to prepare:

- **Documentation**: Create an ISMS document repository including:
  - Statement of Applicability (mapping which ISO controls are implemented or not applicable).
  - Risk Assessment Report.
  - Information Security Policy (approved by management).
  - Asset inventory and data classification.
  - Secure Development Policy ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Secure%20Development%20Policy)), Access Control Policy, Cryptography Policy, etc.
  - Incident Response Plan, Business Continuity/DR plan (we talk about DR in next chapter).
  - Procedures for managing backups, user access provisioning, etc.
  - Records: training records, risk treatment decisions, supplier security agreements (for Azure, maybe just note Azure is ISO 27001 certified as a supplier).
- **Training and Awareness**: Ensure all team members (devs, ops) are aware of their roles in ISMS. Perhaps conduct an internal training on secure dev and ISO responsibilities.
- **Internal Audit**: Before the certification audit, do an internal audit (or hire someone) to check compliance. They will point out gaps. For example, maybe they find that while we implemented controls, we didn't formally document the secure coding guideline – so fix that before external audit.
- **Management Review**: ISO requires management to review the ISMS regularly. Probably out of scope for dev guide, but in a smaller context, maybe project manager or CTO reviews the security posture regularly and signs off.

- **Continuous Improvement**: Show that we act on incidents or near-misses. If a vulnerability was found in a past scan, show how we resolved and improved the process (for example, after Spring4Shell, maybe we implemented additional detection).
- **Scope**: Define scope of certification (likely the whole product and its environment).
- **Evidence readiness**: Collect evidences:
  - Copies of policies.
  - Screenshots or exports of system configurations (like “enforce HTTPS” toggled on, “DB requires SSL” parameter, sample of audit log).
  - Reports from our security tools (like latest SAST scan report showing no high issues).
  - Training logs of DevSecOps.
  - Possibly penetration test reports (maybe an external pentest is conducted annually and issues fixed).
  - List of users with access to prod (to show controlled).
  - Change tickets from deployments (or our CI logs and PRs can serve as evidence of change control).
  - Incident logs (if any incidents happened, how handled).

During the audit, auditors will check that our implemented controls align with what's in the documentation. They might interview devs – so devs should know the secure coding practices and show awareness (which as an advanced dev writing this, you do). They may ask how we manage vulnerabilities – we can explain the pipeline integration and patch process ([Secure Your CI/CD Pipelines: 7 Best Practices You Can’t Ignore - Spectral](https://spectralops.io/blog/secure-your-ci-cd-pipelines-7-best-practices-you-cant-ignore/#:~:text=Where%20Do%20Security%20Risks%20Occur,in%20CI%2FCD%20Pipelines)). They could ask how we ensure only authorized changes go live – we show the PR process and CI approvals. They will definitely check if we have considered risk and applied controls accordingly – our design and risk doc covers that.

**Important ISO 27001 concepts**:

- **Continuous risk management**: It's not one-time. So even after implementing, keep revisiting risk. For example, if we plan a new feature (say integrate a third-party API), do a mini risk assessment for that change.
- **Scope boundaries**: Make sure the cloud environment (Azure) is included in scope and that we've covered cloud-specific risks (we did with Key Vault, NSGs).
- **Annex A 8.28 (Secure System Architecture)**: If present, ensure our architecture is documented and follows security principles (we have a layered architecture with separation of concerns).
- **Annex A 5.15 (Access control to source code)**: We did via repo security and using GitHub's features.
- **Anex A 5.1 (Information Security Roles)**: Possibly designate a product security lead.

## Summary and Compliance Checklist

Bringing it all together, let’s summarize best practices and ensure we have a checklist for compliance:

- **Security Controls Implemented**: We integrated numerous controls: network security, access control, encryption, secure development, etc., fulfilling many Annex A items.
- **Documentation**: Every control needs corresponding documentation/policy. For example, document that “All APIs require JWT auth and implement role-based access as per design; encryption is used for all sensitive data in transit and at rest; logs are kept for X days and reviewed weekly; CI/CD pipeline has SAST and SCA tools (list them) and policy that build fails on high issues; etc.” This can be in a technical report or included in the risk treatment plan.
- **Risk Assessment**: Completed with sign-off, and mitigations are traced to controls in place.
- **Compliance of Cloud**: Azure services we use (App Service, Key Vault, etc.) are themselves compliant (Azure has ISO certs). We might include Azure compliance letters as appendix. But more importantly, we configured them securely (because misconfiguration can void the benefit).
- **Audit Trails**: Verified that we can produce logs of actions (e.g., if asked “show who deployed the last release” – we have CI logs and commit history).
- **Incident Response**: Although not asked in detail yet, likely the next section covers it, but mention: if a security incident occurs (like suspected breach), we have a plan: e.g., who to notify (maybe an on-call SRE or security officer), how to isolate (maybe disable user or regen keys), preserve evidence (don't delete logs), and how to recover. We'll detail a bit in next chapter.
- **Continuous Improvement**: We plan periodic reviews (e.g., quarterly risk meeting, etc.).

**ISO 27001 compliance checklist (for our app)**:

- [x] Secure Development Policy exists and developers follow it (with evidence of training or adherence) ([How To Implement ISO 27001 Annex A 8.25 and Pass The Audit](https://hightable.io/iso27001-annex-a-8-25-secure-development-life-cycle/#:~:text=Secure%20Development%20Policy)).
- [x] Risk assessment done for the application and updated.
- [x] All applicable Annex A controls addressed or have justification if not (e.g., physical security might not apply beyond Azure’s).
- [x] Access to all systems (code, pipeline, cloud, app) is controlled and regularly reviewed (maybe do user access review every 6 months).
- [x] Change management: we have version control and pipeline to manage changes (no ad-hoc changes in prod).
- [x] Third-party services (Azure) and open source libs are assessed for risk (we trust Azure due to its certifications; we monitor open source libs).
- [x] Backups and DR: tested (in next chapter).
- [x] Incident response plan in place (who does what, contact info, etc.).
- [x] Top management is aware and supportive of these measures (for certification, need management buy-in).
- [x] Undergo internal audit and fix any gaps before inviting external auditors.

By following all these best practices, our application and development process should be well-aligned with ISO 27001. The result is not only to pass an audit but to actually have a more secure and well-managed system, which benefits the product’s reliability and trustworthiness.

---

# 9. Final Deployment and Maintenance

Achieving a secure deployment is not a one-time effort. Ongoing maintenance and monitoring are crucial to ensure the application remains secure and compliant over time. In this final chapter, we cover the practices for maintaining security post-deployment, including:

- Continuous security monitoring in production to detect any anomalies or breaches.
- Regular patching and vulnerability management for all components (application, dependencies, underlying platforms).
- Incident response planning – how to react if a security incident occurs, and what steps to take.
- Disaster recovery planning to handle major outages or data loss, ensuring business continuity.
- Ongoing compliance tasks like periodic audits, reviews, and improvements.

By implementing these maintenance practices, we close the loop on the secure development lifecycle and ensure that our application stays resilient and secure throughout its life.

## Security Monitoring in Production

Now that our app is live on Azure, we need to keep an eye on it. **Monitoring** involves collecting data (logs, metrics, alerts) and analyzing it for signs of trouble. We have set up much of the logging infrastructure, so let's ensure we use it effectively:

- **Application Performance Monitoring (APM)**: Use Azure Application Insights (or a similar tool) to monitor the application’s performance and behaviors. Application Insights can track requests, responses, exceptions, and custom events. It can also use adaptive AI rules to detect anomalies (like a sudden spike in failed logins or errors). Setting it up involves adding the Application Insights SDK or using the App Service extension. Once enabled, define some custom metrics: e.g., count of 401 responses (could indicate someone scanning endpoints), high response times (could be a performance issue or DoS attack).
- **Log Analysis**: Use Azure Monitor (Log Analytics workspace) to write queries on logs. For example, query Web Server logs for any HTTP 500 errors or security-related messages in our app logs. You can set up alerts: if more than X 500 errors in 5 minutes, alert the on-call; if an admin function is invoked outside business hours, maybe trigger an alert if that’s unusual.
- **Security alerts**: Azure Security Center (Defender) will produce alerts if it sees suspicious activity on resources. For example, if someone tries a brute force on the DB login, or if unusual application behavior matches a known pattern. Make sure there's an email or incident management integration to catch those alerts.
- **External monitoring**: Consider using external uptime monitors and scanners. For uptime, services like Azure Application Insights availability tests or external services to ping your endpoint. For security, occasional external vulnerability scans or penetration tests (even after go-live, do scheduled pentests perhaps yearly).
- **Network monitoring**: If using NSGs, enable NSG flow logs to see if any blocked traffic events occur. Azure also has Traffic Analytics if you want to see patterns (this might be more for larger networks).
- **Database monitoring**: The Azure MySQL “Threat Detection” (if part of Defender) will alert on unusual queries, access from unknown IPs, SQL injection attempts etc. Make sure to configure who gets those alerts. Also check DB metrics like CPU, which could spike under attack.
- **User Monitoring**: If possible, monitor user behavior for anomalies. For instance, if a user account normally uses the app 1 hour a day but suddenly is downloading massive data at 2 AM, that might be a compromised account. This level is advanced; might require logs to be fed to a SIEM and some user entity behavior analytics (UEBA).
- **Key Vault monitoring**: Turn on Key Vault logging to see if there are failed attempts to access secrets or unusual patterns (should normally only be our app accessing every so often).
- **Audit log reviews**: Establish a routine (maybe weekly or monthly) where someone reviews critical logs (admin actions, security logs) to ensure everything is normal. This could be as simple as scanning a summary report that can be auto-generated by a script or SIEM query.

Remember, monitoring is only useful if someone responds. So ensure alerts have clear owners and runbooks (like if an alert "High number of 403 responses" triggers, the runbook might say: investigate if someone is repeatedly hitting an API they aren’t authorized to – maybe an attack or a misconfigured client; steps to mitigate might be block an IP via firewall if malicious).

**Protecting monitoring data**: The logs and metrics themselves should be protected. We touched on access control to logs. Also consider data retention and disposal – e.g., if logs contain personal data, have a plan to delete them after some time in compliance with privacy laws (though ISO 27001 is more about security, not privacy, but just to mention).

## Patching and Vulnerability Management

Even with all our precautions, new vulnerabilities will be discovered in software over time. We need a process to keep the system up-to-date:

- **Application code patches**: We should periodically update our dependencies. We have tools like Dependabot to notify. Key is to schedule time for maintenance. For example, every sprint or every month, review dependency updates (especially if security fixes). For critical vulnerabilities (like a zero-day in Spring or a popular library), do an immediate out-of-cycle patch. Track these in our issue tracker with high priority.
- **Platform patches**: Azure PaaS services (App Service, DB) are patched by Microsoft (we get OS, runtime updates automatically). But if we were on VMs, we’d need to patch OS (we’re not in this case). Still, we must update our JDK when a new security release comes (Azure might handle if using built-in, but if we containerize, then we handle). Also update Node for React build environment if needed (though that’s dev side).
- **Database engine updates**: Azure MySQL will handle minor version updates. For major version (e.g., MySQL 8 to future 8.x or 9), plan it once stable. Usually, rely on Azure’s recommendations. If self-hosting MySQL, schedule patching.
- **Key Vault and other service updates**: Not much to patch but keep an eye on deprecations or changes (like TLS versions support).
- **Operating environment**: Developer machines and CI agents should be updated. For GH Actions cloud, GitHub does it. If using self-hosted agents or Jenkins, patch those too (they're part of environment).
- **Penetration Testing**: Conduct regular pentests. Usually, an external team tries to hack your app. They will find any missed issues. Then patch those issues and adjust processes to prevent similar ones. Having a record of pentest and fixes is good for compliance (and some standards explicitly require annual pentest).
- **Vulnerability scanning**: Continue to run scans (SAST, SCA, DAST). If any new vulnerability pops up, create a ticket, fix it.
- **Bug bounty**: If applicable, some organizations open a bug bounty program to let ethical hackers report issues. That might be beyond our scope, but something to consider if appropriate.

**Patching timeline**: Define SLAs for fixing vulnerabilities. For example, "Critical vulns: fix within 48 hours, High in 7 days, Medium in 30 days, Low in 90 days". This kind of policy ensures timely patching. We essentially follow that by our process (we wouldn't wait on a critical anyway). Document it in a vulnerability management procedure.

**Configuration drift**: Over time, people might make config changes (maybe someone opens a port for troubleshooting and forgets to close). Use Azure Policy or scripts to check compliance. For instance, set Azure Policy that App Service must have HTTPS only (so if someone tries to disable, it flags). There are built-in Azure Policy definitions for many of these best practices. Similarly, policy for Key Vault to require firewall, etc. That can enforce our desired state.

**Dependency management**: We should also keep track of all open source licenses to ensure none become a legal issue. Not ISO 27001, but important for business. There are tools in CI to identify licenses too.

## Incident Response and Disaster Recovery Planning

Despite all prevention, incidents can happen. Being prepared is crucial.

**Incident Response Plan (IRP)**: Create a plan that outlines steps when a security incident is suspected or confirmed:

- Define what constitutes an incident (e.g., any unauthorized access, malware infection, DoS attack causing outage, data breach, etc.).
- Roles: Who is on the Incident Response Team? Likely a combination of dev lead, ops engineer, security officer, etc. Have contact info accessible (including after hours contacts).
- Procedures:
  - Detection: how issues are detected (monitoring alerts, user reports, etc.).
  - Analysis: how to investigate (e.g., gather logs, identify scope).
  - Containment: actions to limit damage (e.g., disable certain accounts, block IPs, take app offline if needed).
  - Eradication: remove the threat (e.g., apply patch, remove malicious code).
  - Recovery: restore systems to normal (e.g., bring servers back up, ensure no backdoors remain).
  - Post-Incident: document what happened, do a root cause analysis, identify improvements (update controls, maybe add new monitoring or change processes to prevent repeat).
- Communication: Who needs to be notified? Internal management, possibly affected customers (if data breach, you might have legal obligations to notify), regulators if any. This should be defined. Also, who speaks externally (maybe only PR or certain person to avoid inconsistent messaging).
- Simulate incidents: Do drills (for example, simulate a breach to test if team can follow the plan effectively). This helps refine the plan.

The plan should cover common scenarios like:

- Data breach (what do we do if data is stolen?).
- Service outage due to attack (like DDoS).
- Lost credential (if a password or key is leaked, how to rotate quickly).
- Website defacement or malicious code injection (how to take it down quickly, etc.).

For our app: if we find a critical vulnerability in production that is being exploited, our IR might involve taking the app offline or rolling back to a safe state, applying a patch, etc., in coordination with Azure support if needed (though likely we handle ourselves). Key Vault gives ability to quickly roll secrets, etc. We should ensure backups of code and data in case we need to rebuild from scratch if compromise is deep.

**Disaster Recovery (DR) Planning**: While incident response often deals with security incidents, disaster recovery is about major disruptions (could be security-related like ransomware, or non-security like hardware failure, natural disaster).

- **Define RPO and RTO**: Recovery Point Objective (how much data loss is tolerable) and Recovery Time Objective (how quickly to restore service).
  - For example, RPO of 1 hour might mean we need hourly database backups. RTO of 4 hours means within 4 hours of a disaster we should be back up.
- For our Azure deployment:
  - Azure DB for MySQL has point-in-time restore (maybe can restore to within ~5 min of any point). That covers RPO decently (likely RPO minutes).
  - RTO: If Azure region goes down, how to recover? We might consider using Azure’s cross-region replicas for the DB or a backup restore in another region. And similarly have a deployment of the app in secondary region.
  - If not doing active-active, at least have documented steps: “If region down, we will deploy the infrastructure from our Infrastructure-as-code to region B, restore latest backup to new MySQL, switch DNS.” Possibly use Azure Traffic Manager or Front Door to route to secondary when primary fails.
  - Also consider smaller scale disasters: e.g., database corruption or accidental deletion. That’s handled by backup restore too.
- **Backup testing**: At least annually, test restoring backups to ensure they work. Also test the failover process to the secondary region if we have one (could be a drill where we simulate primary down).
- **Redundancy**: Check we don’t have single points of failure. App Service is redundant in an Azure region. DB can be single instance (not multi-AZ unless using flexible with HA). If HA needed, set up the MySQL in zone redundant or use read replica in another zone for failover. Key Vault is redundant in region (and in DR scenario, you can recover KV by redeploying infra).
- Document the DR plan: who invokes it (maybe if downtime exceeds X or certain triggers). Also include communication plan in disasters (update status pages, etc., though again beyond coding).

**Maintenance and Monitoring of Backups**: Ensure backups are secure (they contain sensitive data). Azure’s are encrypted, but if we make custom backups, encrypt them and store maybe in Key Vault or secure storage. Limit who can access backup files (should be just a couple of admins).

**Resilience Testing**: Perhaps occasionally do chaos testing or scenario simulations to gauge system resilience (like simulate DB down, see if alerts fire and runbook followed).

## Keeping Compliance in Check

After deployment, maintain compliance by:

- Conducting **periodic audits**: ISO requires internal audits. So maybe every year (or 6 months) an internal audit team reviews everything – including code repository rights, server configs, evidence of security patches, etc. We need to assist by providing info and fixing any findings.
- **Surveillance audits**: If ISO certified, external auditors come yearly (with full recertification every 3 years). Be prepared to show updated documents, new risk assessments (especially if scope changed).
- **User access reviews**: e.g., every 6 months review who has access to Azure and remove those who don’t need it (maybe someone left team).
- **Policy reviews**: Update policies to reflect any changes (if we adopt new tech, include it; if new threats emerge, maybe emphasize those in guidelines).
- **Keep training**: Bring new developers up to speed on our secure dev practices and ISO obligations.
- **Awareness**: Keep team aware that security is ongoing. Perhaps share monthly security newsletters or have a Slack channel for CVE alerts relevant to our stack.
- **Continuous Improvement**: If an incident or near-miss happens, update controls. For example, if an internal developer accidentally pushed a secret to repo and we caught it, maybe we decide to enforce pre-commit hooks for secret scanning to prevent that.

By following through with these maintenance steps, we help ensure that the application remains secure and that the organization remains compliant with ISO 27001 over the long term. It’s a journey of constant vigilance and improvement.

**Final Checklist for Post-Deployment Security & Compliance:**

- [x] Monitoring dashboards and alerts are set up; alerts tested (simulate an event and see if alert triggers).
- [x] Team is aware of what to do when an alert fires (runbooks in place).
- [x] Regular patching schedule established; responsible persons identified for applying patches.
- [x] Vulnerability scans continue to run; there's a process to triage and fix findings promptly.
- [x] Incident Response Plan written and accessible; team has been briefed on it (maybe did a tabletop exercise).
- [x] Disaster Recovery plan documented; backups verified; failover procedure tested at least once.
- [x] All security controls and policies are periodically reviewed and updated as needed (this can be part of the ISMS management meetings).
- [x] Evidence for compliance is being collected (logs of training, records of patch updates, audit logs etc.) to show during audits.

## Conclusion

We have now gone through a comprehensive journey of building a full-stack application (ReactJS frontend, Spring Boot backend, MySQL database) on Azure with security and ISO 27001 compliance as a constant focus. By following the steps in this guide, an advanced development team should be able to:

- Set up a robust development environment and toolchain that bakes in security (from secure frameworks to secret management).
- Implement frontend and backend code that incorporates authentication, authorization, encryption, and other security best practices to guard against common threats.
- Secure the database layer by configuration and controls like encryption, access restrictions, and monitoring.
- Deploy the application to Azure using services like App Service, Azure Database for MySQL, and Key Vault in a manner that leverages cloud security features and minimizes exposure.
- Create a DevSecOps pipeline that automates security checks and ensures only vetted, secure code is deployed.
- Align their development and operations practices with ISO 27001 standards, by implementing necessary controls and maintaining documentation and processes for compliance.
- Plan for maintenance by continuously monitoring the system, keeping everything up-to-date, and being prepared to respond to incidents or outages.

Security and compliance are ongoing commitments. By integrating them into every phase – from design, coding, testing, deployment, to maintenance – we build not just a working application, but a trustworthy one. This not only satisfies the ISO 27001 standard for an Information Security Management System ([How ISO 27001 Compliance Impacts the Development Process of Websites and Mobile Apps - SoftwareSeni](https://www.softwareseni.com/how-iso-27001-compliance-impacts-the-development-process-of-websites-and-mobile-apps/#:~:text=ISO%2027001%20is%20an%20internationally,information%20entrusted%20by%20third%20parties)) but also gives users and stakeholders confidence that their data and the business are well-protected.

**Final Thoughts**: Embrace a culture of security. Encourage developers to always think about the security impact of their choices. Keep learning about new threats and defenses. And use ISO 27001 not just as a checkbox exercise, but as a framework to continually improve your organization’s security maturity. With this approach, your full-stack application will stand on a strong foundation of both functionality and security, ready to serve users while keeping risks at bay.
