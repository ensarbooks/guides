# 1. Introduction to Azure AD Authentication

Modern applications often require robust **authentication** and **authorization** mechanisms to secure data and functionality. **Authentication** (AuthN) is the process of verifying a user's identity – confirming that the user is who they claim to be ([Authentication vs. authorization - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization#:~:text=Authentication)). **Authorization** (AuthZ) is the process of granting an authenticated user permission to access certain resources or perform specific actions ([Authentication vs. authorization - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization#:~:text=Authorization)). In simpler terms: authentication answers _“Who are you?”_, while authorization answers _“What are you allowed to do?”_. In a secure app, both are essential – first authenticate the user, then authorize their access based on roles or permissions.

Azure Active Directory (Azure AD), now part of **Microsoft Entra ID**, is a cloud-based identity provider that implements standard protocols to handle authentication and authorization for applications. Instead of apps managing user credentials themselves, they can delegate identity management to Azure AD (a centralized identity provider), reducing complexity and improving security ([Authentication vs. authorization - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization#:~:text=Microsoft%20Entra%20ID%20is%20a,it%20enables%20scenarios%20such%20as)). Azure AD supports industry-standard protocols like **OAuth 2.0** and **OpenID Connect (OIDC)** for user sign-in, token issuance, and API access. This guide will focus on implementing Azure AD authentication in a full-stack application: a React frontend (written in TypeScript), a Spring Boot backend (Java), and MySQL for data storage.

## 1.1 Overview of Authentication and Authorization

In our context, **authentication** will ensure that only legitimate users (for example, employees of an organization or registered app users) can log into the React application via Azure AD. Azure AD will handle verifying user credentials (such as email/password or MFA) and return **tokens** that the application can use. There are different types of tokens Azure AD issues:

- **ID Token** – A JSON Web Token (JWT) that contains identity information about the user (name, email, etc.). It is issued as part of the OpenID Connect flow and is used by the client (React app) to confirm the user's identity ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Access%20tokens%20,granted%20by%20the%20authorization%20server)).
- **Access Token** – A JWT intended for the backend API (Spring Boot). It contains scopes or roles that authorize the user to access certain API endpoints ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Access%20tokens%20,granted%20by%20the%20authorization%20server)). The React app will attach this token to API requests.
- **Refresh Token** – A token that the client can use to silently obtain new access tokens when the current ones expire, without forcing the user to log in again ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=client%20application,get%20basic%20information%20about%20them)).

**Authorization** in this app will determine what the authenticated user can do on the backend. For example, we may restrict certain REST API endpoints to users with an “Admin” role. Azure AD can help with authorization by including **claims** in tokens (like user roles or group memberships), which the Spring Boot application can inspect to enforce Role-Based Access Control (RBAC).

**Why Azure AD?** Azure AD provides a secure, enterprise-ready solution with features like single sign-on, multi-factor authentication, password policies, and integration with Microsoft 365 and thousands of other apps. By using Azure AD, we offload user identity management and benefit from its compliance and security features. It also means our app can leverage **SSO (Single Sign-On)** – if a user is already signed into Azure AD (for example, via Office 365), they can seamlessly sign into our app without re-entering credentials ([Authentication vs. authorization - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization#:~:text=Microsoft%20Entra%20ID%20is%20a,it%20enables%20scenarios%20such%20as)).

In summary, our React application will authenticate users via Azure AD and obtain tokens. The Spring Boot API will **validate those tokens** on each request to ensure the caller is authenticated and authorized. MySQL will store any additional user data or roles required by the application.

## 1.2 Understanding OAuth2 and OpenID Connect in Azure AD

Azure AD implements the OAuth 2.0 and OpenID Connect protocols in what Microsoft calls the **Microsoft identity platform**. Understanding these protocols is key to implementing the solution:

- **OAuth 2.0** is an authorization framework that allows a user to grant a third-party application limited access to their resources on another service without sharing credentials. In Azure AD, OAuth2 is used to obtain **access tokens** that grant access to APIs. The main roles in OAuth2 are:

  - _Resource Owner_: the user who owns the data/resource.
  - _Client_: the application requesting access (our React app).
  - _Resource Server_: an API hosting protected data (our Spring Boot backend).
  - _Authorization Server_: the identity provider that authenticates the user and issues tokens (Azure AD in this case) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=server,authenticated)) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Resource%20server%20,or%20deny%20access%20to%20resources)).

- **OpenID Connect (OIDC)** is an identity layer on top of OAuth2. While OAuth2 alone is about authorization (access tokens), OIDC adds authentication by issuing an **ID token** that proves the user's identity and provides profile information ([OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#:~:text=OpenID%20Connect%20,token%20called%20an%20ID%20token)) ([OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#:~:text=Enable%20ID%20tokens)). When our React app signs in a user with Azure AD, it uses OIDC to get an ID token (to identify the user) and OAuth2 to get an access token (to call the API).

**How the flow works in our app:** We will use the **OAuth 2.0 Authorization Code Flow with PKCE** (Proof Key for Code Exchange), which is recommended for SPAs. The high-level steps are:

1. The React app (OAuth2 client) redirects the user to Azure AD with a request for authorization (including scopes it needs).
2. Azure AD prompts the user to sign in (if not already signed in) and asks for consent to the requested permissions (if not already granted).
3. After successful login, Azure AD sends an **authorization code** back to the React app (to a redirect URI we specify).
4. The React app (via the MSAL library) silently exchanges this code for tokens (ID token & access token) by contacting Azure AD. PKCE is used to enhance security for this public client exchange.
5. Azure AD returns the tokens to the React app. The ID token is used to establish the user's session on the client side (who is logged in), and the **access token** is stored for API calls.
6. The React app includes the access token in the `Authorization` header (as a Bearer token) on requests to the Spring Boot API.
7. The Spring Boot API (resource server) validates the token on each request – checking its signature, issuer, audience, expiration, etc. If valid, the request is allowed and the API can further check claims (like roles) to authorize the user for specific operations.
8. When the access token expires, the MSAL library can use the stored refresh token (or silent re-auth behind the scenes) to get a new access token without user involvement, providing a smooth experience.

Azure AD follows standards, so the **access token and ID token are JWTs** (JSON Web Tokens) signed by Azure AD. The Spring Boot backend will not need to call Azure AD for each request; it can **validate JWTs locally** using Azure AD’s public keys (JWKS) that it fetches from Azure AD’s metadata endpoint ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=spring%3A%20security%3A%20oauth2%3A%20resourceserver%3A%20jwt%3A,uri%3A%20https%3A%2F%2Fidp.example.com%2Fissuer)). This makes the system scalable and efficient, as each API instance can independently verify tokens.

## 1.3 Azure AD Setup and Application Registration

Before writing any code, we must configure Azure AD to recognize our application and define the authentication parameters. This is done through **App Registration** in Azure AD. Registering an app in Azure AD establishes a trust relationship between our application and Azure AD – Azure AD will know to issue tokens to our app, and our app will know to accept tokens from Azure AD.

**Application Registration** involves providing Azure AD with details about our application such as the application name, the type of application (web, SPA, native, etc.), redirect URIs, and what permissions it will need. When we register, Azure AD assigns a **Client ID** (also known as Application ID) to our app – a unique identifier used in token requests ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Application%20%28client%29%20ID%20,client%20types%20use%20redirect%20URIs)). We may also generate a **Client Secret** for confidential applications (like server-side apps) which acts like a password for the application. However, for a public client like a React SPA, we do **not** use a secret (since it can't be safely kept in a browser).

For our architecture, we will perform **two app registrations** in Azure AD: one for the frontend (React SPA) and one for the backend API (Spring Boot). This separation follows best practices:

- The **API registration** will represent the Spring Boot REST API. We will define the permissions (scopes or roles) this API exposes.
- The **Client (SPA) registration** will represent the React application. This client will request tokens to access the API (acting on behalf of the signed-in user).

This separation allows us to manage API permissions and consent independently, and it mirrors real-world scenarios where multiple client apps (mobile, web, etc.) might access the same API.

**Azure AD Tenant:** You will need access to an Azure AD tenant (commonly the Azure AD associated with your organization or a test tenant). Ensure you have rights to create app registrations in the tenant. If working in a dev/test scenario, you can use a free Azure AD tenant.

In the next sections, we will go step-by-step through setting up the environment, configuring Azure AD, and building both the frontend and backend to use Azure AD for authentication and authorization.

---

# 2. Setting Up the Development Environment

Before diving into coding, it's important to set up all necessary tools and ensure the project structure is organized. We are building a full-stack project, so our environment will span frontend (Node.js/React) and backend (Java/Spring Boot), as well as a database (MySQL).

## 2.1 Installing Required Tools

Make sure the following tools and frameworks are installed on your development machine:

1. **Node.js (JavaScript Runtime)** – Install Node.js (which includes **npm**, the Node package manager). Node.js is required to create and run the React development server and build the React app. Download Node.js LTS (Long Term Support) version from the [official website](https://nodejs.org) and run the installer. After installation, verify it by running:

   ```bash
   node -v
   npm -v
   ```

   You should see version numbers (e.g., Node v18.x and npm v8+). Having Node.js also gives you npm or Yarn to install JavaScript dependencies.

2. **Create React App or Vite (for React TypeScript)** – We will use a React framework to bootstrap our frontend. The easiest is Create React App. You can install the Create React App tool globally:

   ```bash
   npm install -g create-react-app
   ```

   (Alternatively, we can use `npx` to run it without global install.) We will use a TypeScript template to generate a React project with TypeScript support.

3. **Java Development Kit (JDK)** – Install JDK 17 (or the latest LTS, as Spring Boot 3.x requires Java 17+). You can get it from [Adoptium Temurin](https://adoptium.net) or Oracle. Verify installation with:

   ```bash
   java -version
   ```

   Ensure Java is in your PATH and showing the correct version.

4. **Apache Maven or Gradle** – Spring Boot projects can use Maven or Gradle for build. Maven is more common for beginners. Install Maven (if not already, many IDEs bundle it). Verify with: `mvn -v`. Alternatively, if using Gradle, verify with `gradle -v`. We will assume Maven in this guide for simplicity, but you can adapt to Gradle if preferred.

5. **Spring Boot Initializer (optional)** – We won't _install_ Spring Boot as a tool, but it's helpful to use [Spring Initializr](https://start.spring.io/) (web-based) or IntelliJ/Eclipse with Spring initializer support to generate the initial Spring Boot project structure with needed dependencies.

6. **MySQL Database Server** – Install MySQL Community Server (version 8.x) or use a Docker container for MySQL. For local development, you can download MySQL from the official site. During installation, note the root password. Alternatively, if using Docker:

   ```bash
   docker run -d -p 3306:3306 --name mymysql -e MYSQL_ROOT_PASSWORD=MySecretPW mysql:8.0
   ```

   This command would run MySQL 8.0 container listening on port 3306. Ensure MySQL is running and you can connect (using a tool like MySQL Workbench or the `mysql` CLI).

7. **Postman (API Testing Tool)** – Download and install [Postman](https://postman.com) to test API endpoints with various authentication scenarios. Postman will help us simulate HTTP requests with tokens to verify our backend security.

8. **Azure CLI (optional)** – The Azure Command-Line Interface can be handy for Azure AD tasks or deploying to Azure. It's optional if you prefer using the Azure Portal for everything. You can install it from Microsoft’s docs and run `az login` to authenticate. In this guide, we'll mostly use the Azure Portal UI for initial setup.

9. **IDE or Text Editor** – Use an editor you're comfortable with. For React/TypeScript, **VS Code** is popular. For Spring Boot, **IntelliJ IDEA** (Community or Ultimate) or VS Code with Java extensions will work. Ensure your IDE has the necessary plugins for syntax highlighting and building for both TypeScript and Java.

Once all tools are installed, you have a baseline environment:

- Node.js and npm for frontend dependencies.
- Java and build tools for backend.
- MySQL running for the database.
- Postman for testing.
- Azure access for configuration.

### Verifying the Environment

It's good to verify everything is ready:

- Run `create-react-app --version` (if using CRA) to see it’s installed.
- Run `mysql --version` to ensure MySQL client is accessible (or confirm your DB container is up).
- If using an IDE, try creating a simple “Hello World” React app and running `npm start`, and a simple Spring Boot app to ensure no environment issues.

With the tools in place, let's set up the project structure.

## 2.2 Setting Up the Project Structure

We will set up two separate projects: one for the React frontend and one for the Spring Boot backend. Keeping them separate is clean and mimics how you'd deploy them (frontend as static files, backend as a service).

**a. Initialize the React (TypeScript) project:**

Create a new React app using Create React App with the TypeScript template. In a suitable directory, run:

```bash
npx create-react-app azure-ad-react-frontend --template typescript
```

This will generate a new folder `azure-ad-react-frontend` with a React application scaffolded for TypeScript. If successful, you can `cd azure-ad-react-frontend` and run `npm start` to verify the dev server comes up on [http://localhost:3000](http://localhost:3000). We will later add code to this app for authentication.

The important files in this React project will be:

- `src/index.tsx`: entry point of the React app.
- `src/App.tsx`: main App component.
- We will add an `authConfig.ts` (or similar) to configure Azure AD credentials and an `AuthProvider` using MSAL.
- Optionally, we'll create components for login and secure content.

**b. Initialize the Spring Boot project:**

Using Spring Initializr:

- **Group**: e.g., `com.example` (or your organization’s domain).
- **Artifact**: e.g., `azure-ad-backend`.
- Choose **Maven** (if using Maven) and language **Java**.
- Spring Boot version: 3.x (latest stable).
- Dependencies: select **Spring Web**, **Spring Security**, **Spring Data JPA**, **MySQL Driver**. We will add Azure AD specific config manually, so no need for Azure starters yet (though Spring offers an Azure AD starter, we will demonstrate manually for learning).
- You can also add **Spring Boot DevTools** (for hot reload, optional) and **Lombok** (to reduce boilerplate, optional).
- Generate the project and download the ZIP, or if using IntelliJ IDEA, use the New Project wizard with Spring Initializr to create it directly.

Once created, the Spring Boot project structure will look like:

```
azure-ad-backend/
├── src/main/java/com/example/azureadbackend/Application.java  (Spring Boot entry)
├── src/main/java/com/example/azureadbackend/controllers/...   (REST controllers folder)
├── src/main/java/com/example/azureadbackend/config/...        (security config will go here)
├── src/main/java/com/example/azureadbackend/models/...       (JPA entities for MySQL)
├── src/main/java/com/example/azureadbackend/repositories/... (JPA repositories)
├── src/main/resources/application.properties  (Spring config)
└── pom.xml  (Maven dependencies)
```

We will create appropriate packages for controllers, config, models, etc., to keep code organized.

**c. Configure database for the backend:**

Before running the backend, we need a MySQL database setup:

- Create a database schema for the app. For example, connect to MySQL and run:

  ```sql
  CREATE DATABASE azure_ad_app_db;
  CREATE USER 'azureappuser'@'%' IDENTIFIED BY 'StrongPassword123';
  GRANT ALL ON azure_ad_app_db.* TO 'azureappuser'@'%';
  ```

  This creates a database and a user with password. (Adjust credentials and privileges as needed; in production you'd restrict privileges more tightly.)

- In `application.properties` of Spring Boot, add the DB connection settings:
  ```properties
  spring.datasource.url=jdbc:mysql://localhost:3306/azure_ad_app_db
  spring.datasource.username=azureappuser
  spring.datasource.password=StrongPassword123
  spring.jpa.hibernate.ddl-auto=update
  spring.jpa.show-sql=true
  ```
  This assumes MySQL is on default port 3306 and accessible. `ddl-auto=update` will auto-create tables based on JPA entities (convenient for dev; in production you might use migrations). `show-sql=true` will log SQL queries for debugging.

We will define our JPA entities (for user roles etc.) in a later section.

**d. Linking frontend and backend in development:**

During development, we'll run the React app on port 3000 and Spring Boot on port 8080 (default). We must ensure CORS is handled so the React app can call the API on a different port – we will configure Spring Boot to allow the React dev origin. Also, note the network calls: the React app will call `http://localhost:8080/api/...` endpoints.

We do not need to serve the React app from Spring Boot during development, but in production we might deploy them separately (React as static site and Spring Boot as API service).

**e. Version Control:**

It’s recommended to initiate version control (e.g., git) for your projects:

- Run `git init` in each project folder (or have a single repository with both, structured accordingly).
- Create a `.gitignore` for Node (which Create React App provides) and one for Java (to ignore `target` directory, etc., which Spring Initializr provides).

At this point, our environment setup is complete:

- We have two projects (frontend and backend) ready for coding.
- Necessary tools are installed and verified.
- Database is set up for the backend to use.

Next, we will configure Azure AD itself to prepare for authentication, which involves creating app registrations and defining how tokens will work for our app.

---

# 3. Configuring Azure AD for Authentication

With the development environment ready, the next critical step is to configure Azure AD so that it knows about our application and can issue tokens for it. This involves creating app registrations for the frontend and backend and setting up secrets, redirect URIs, and API permissions.

**Overview:** We will register two applications in Azure AD – one representing the backend API and one for the frontend SPA. Then we'll configure the API to expose permissions (scopes) and the client to be allowed to request those permissions. We'll also set up necessary identifiers like redirect URIs and a client secret (for the backend, if needed).

> **Note:** You will need appropriate Azure AD permissions to create app registrations (typically an Azure AD admin or developer role in the tenant). Log in to the [Azure Portal](https://portal.azure.com) and navigate to **Azure Active Directory** > **App registrations**.

## 3.1 Registering the Applications in Azure AD

**Register the Backend API App:**

1. In Azure AD’s App registrations, click **New registration**.
2. **Name:** Give a name like "MyApp-API" (this is just a friendly name).
3. **Supported account types:** Choose based on who will use your app. For development, "Accounts in this organizational directory only (Single tenant)" is simplest (only your tenant's users). If you plan multi-tenant support (allowing other orgs' Azure AD accounts), choose multi-tenant – we'll discuss multi-tenancy in Section 7.2.
4. **Redirect URI:** For an API, we typically **do not need a redirect URI**, since it isn't an interactive client. (Redirect URIs are used in auth flows for client apps. The API will just accept tokens.) You can leave this blank for now.
5. Click **Register**. You will be taken to the app's overview page. Note the **Application (client) ID** (GUID) and **Directory (tenant) ID** – we will use these in our Spring Boot config later.

Now, some configuration for this API app:

- **Expose an API (Scopes):** We need to define at least one scope that client apps can request to access this API.

  1. In the registered "MyApp-API", go to **Expose an API** in the left menu.
  2. Click **Set** (or **Add**) an **Application ID URI** if prompted. Azure will suggest a URI like `api://<client-id>` by default. You can use that or a more readable one (e.g., `api://myapp-api` if globally unique). This URI is the prefix that identifies your API in tokens.
  3. Click **Add a scope**. In the dialog, create a scope for the API, for example:
     - Scope name: `API.Access` (or `access_as_user` – naming is up to you).
     - Who can consent: Typically "Admins and users" for user-delegated permissions.
     - Admin consent display name: e.g., "Access MyApp API".
     - Admin consent description: e.g., "Allows the app to access the MyApp API on behalf of the signed-in user."
     - User consent display name/description: similar but phrased for end-users (if you want users to see it).
     - State: Enabled.
  4. Click **Add scope** to save. You should see your new scope listed (e.g., `api://<client-id>/API.Access`). This means Azure AD can issue tokens with this scope in the `scp` claim to indicate permission.

  _Why define a scope?_ Scopes represent specific API permissions. By creating `API.Access`, we define a permission that client apps must request to call our API. This also allows users or admins to consent to granting that permission to the client app.

- **App Roles (Optional):** If you plan to implement role-based access using Azure AD (app roles), you can define them in the **App roles** section of the API registration. For example, define roles like "Admin" or "User". These roles, when assigned to users or groups in this app context, will appear in tokens as `roles` claim ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=These%20application%20roles%20are%20defined,the%20form%20of%20role%20membership)). We will cover app roles and their usage later (Section 7.3 and 5.3). If you want to set them now:

  - Go to **App roles**, click **Create app role**. Define a role name, value (like "Admin"), description, and specify that it can be assigned to Users (or to Applications if needed).
  - Add as many roles as needed (e.g., Admin, User).
  - After adding, you (or an admin) would need to assign these roles to users or groups via Enterprise Applications -> [Your API] -> Users and groups. (We can do that later when testing, if using this feature.)

- **Client Secret:** Although our API itself won’t log into Azure AD, we might create a client secret in case the backend needs to call Azure AD (for example, to use Graph API or for testing with Postman using client credentials flow). To create a secret:
  - Go to **Certificates & secrets** for the API app.
  - Click **New client secret**. Give it a name (e.g., "MyAPITestSecret") and an expiration period.
  - After creation, **copy the secret value** and store it securely (you won't be able to view it again). We will not use this in the React app, but might use it for testing or if the backend needed to authenticate to Azure AD for some reason. In our scenario, the backend is just a resource server (verifying tokens), so it doesn't strictly need a secret at runtime for token validation. Token validation uses the Azure AD public keys, which are openly available.

**Register the Frontend SPA App:**

1. Again, go to **App registrations** > **New registration**.
2. **Name:** e.g., "MyApp-SPA".
3. **Supported account types:** Usually same as API – use Single Tenant for now (or multi-tenant if that’s your goal).
4. **Redirect URI:** This time we need one. Select **Single-page application (SPA)** as the platform (Azure might show separate fields or a dropdown). Enter the URL where Azure AD should send the auth response. In development, our React app runs at `http://localhost:3000`. We can use `http://localhost:3000` as the redirect URI (for simplicity, sending the user to the homepage after login). Alternatively, you could use a specific route like `http://localhost:3000/auth/callback` and handle it, but MSAL can handle the root as well.
   - Ensure the URI exactly matches where your app will be served. For production, you'll add another redirect (like `https://myapp.com` or a specific path).
5. Click **Register** to create the SPA app. Note the **Client ID** for this SPA app.

Now configure the SPA app:

- **Authentication settings:** In the SPA app's **Authentication** blade, verify that your redirect URI is listed under "Single-page application". Also, ensure **Implicit grant** settings (if visible) – historically you'd enable "Access tokens" and "ID tokens" for SPAs. However, since we are using the Authorization Code flow with PKCE, we do _not_ need to use the implicit flow. If there's a section for "Implicit grant & hybrid flow", you can leave those boxes unchecked (they are not needed and staying unchecked ensures you're using the more secure auth code flow). Azure will allow the SPA to use auth code with PKCE by default when it's registered as a SPA.

- **Expose an API:** _Do not do this for the SPA._ The SPA is not providing an API, it's a client. So we don't expose scopes or roles here. (The SPA will use the API app’s scope.)

- **API Permissions:** This is crucial – we must grant this SPA permission to call the API.
  1. In the SPA app registration, go to **API Permissions**.
  2. Click **Add a permission**. In the Request API permissions dialog, choose **My APIs** (or "APIs my organization uses" and search for your API name).
  3. You should see your "MyApp-API" that we created. Select it.
  4. Under **Delegated Permissions** (permissions granted on behalf of a signed-in user), you should see the scope we defined (e.g., `API.Access`). Check that. This means the SPA wants to call the API as the user.
  5. Add the permission. Now it will appear in the list, likely with a status "Not granted for <Tenant>".
  6. We need to **grant consent** for this permission. If you're an admin on the tenant, you can click the **Grant admin consent** button on the API Permissions page. Granting admin consent means users won't individually be prompted to consent for this API; it's pre-approved. In a dev scenario with your own tenant, this is convenient.
     - After granting, the status should change to "Granted for ...".
  7. The SPA app by default also has **Microsoft Graph** "User.Read" permission (if created with certain settings). You can remove that if not needed, or leave it if you plan to call Graph (our scenario doesn't require it explicitly, but MSAL might request profile by default).
  8. Ensure **openid** and **profile** are implicitly included – these are standard OIDC scopes. Azure AD will always allow openid and profile (and email) by default, so you won't see them listed, but MSAL will request them to get user info in ID token.

At this point, the SPA app is configured with permission to request tokens for the API app. The relationship:

- The SPA's Client ID and Redirect URI are set.
- The API's scope (API.Access) is exposed.
- The SPA has **delegated permission** to API.Access and (via admin consent) can receive an access token for that scope.

**Summary of IDs and configurations to note down for later:**

- **Tenant ID:** (GUID of Azure AD tenant) – used as part of authority URL in MSAL and issuer in Spring Boot.
- **SPA Client ID:** for MSAL configuration in React.
- **SPA Redirect URI:** e.g., `http://localhost:3000`.
- **API Client ID:** will be used as the **Audience** for token validation in the backend (the access token’s `aud` should match this).
- **API Scope name:** e.g., `api://<API-Client-ID>/API.Access` – used when requesting token in MSAL.
- **Client Secret (API)**: if generated (for potential future use or testing).
- **Any App Roles**: names of roles if created.

We will use these values in code configuration:

- In React MSAL config: tenant (or authority URL), SPA clientId, and the scope for API.
- In Spring Boot config: tenant ID (for issuer), API clientId (for audience), and possibly the JWKS URL which is derived from tenant ID.

## 3.2 Setting up Redirect URIs and Client Secrets

We already set up redirect URIs in the process above:

- The **frontend SPA** has `http://localhost:3000` as a redirect URI. Azure AD will only redirect tokens to this URL for that app. If this doesn't match exactly what the app uses, authentication will fail. For production, you'll add the production URL (e.g., `https://myapp.com`) in the SPA app's Authentication settings as an additional redirect.

For **logout**, Azure AD can also have a **Logout URL** (front-channel logout). In the SPA app registration's Authentication settings, you can specify a logout URL (e.g., `http://localhost:3000`, or a specific route like `.../logout` or simply the home). This is where Azure AD will redirect after a logout is initiated. It's optional; MSAL can handle clearing session without a redirect, but if you want Azure AD to call the app on logout to cleanup, set it.

Regarding **Client Secrets**:

- The **SPA app** is public, and we do _not_ create a secret for it. In OAuth2 terms, it's a public client (cannot securely maintain a secret). MSAL in the browser will use PKCE for security rather than a client secret.
- The **API app** can have a client secret (we created one optionally). This secret would be used if an application (like a daemon or server) wants to do **client credential flow** to authenticate as the API itself or to get a token to call another service. In our scenario, the Spring Boot API just validates incoming tokens and doesn't act as a client, so we don't need to use the secret in code. However, if later we build integration tests or use Postman to get a token via client credentials, that secret is useful.

**Protecting the secret:** If you did create a client secret, remember it should be kept confidential. Do not commit it to source code. In production, you'd store it in a secure configuration (Azure Key Vault, environment variable, etc.). For now, just note it somewhere safe.

## 3.3 Configuring Permissions and API Access in Azure AD

We have effectively configured the core permissions by adding the API scope to the SPA app and granting consent. Let's double-check the configuration from a high-level perspective:

- **User Consent & Permissions:** Because we granted admin consent for the SPA to access the API, users will not see a consent prompt for our custom API when they log in. If you skipped admin consent, the first user login would show a prompt "App would like to: Access MyApp API". Since this is our own app, it’s convenient to pre-consent it.

- **Microsoft Graph (optional):** If you plan to fetch user profile info via Graph API, ensure the SPA has `User.Read` permission (delegated) and consent. This usually is default for a new registration. Our guide primarily uses ID token for basic info and doesn't call Graph, but it's worth noting.

- **Token claims configuration:** Azure AD by default will include common claims in ID and access tokens: user's name, email, oid (object ID), tenant id, etc. If you created **app roles** or enabled **group claims**:

  - For app roles: when a user with a role signs in, the token will have a `roles` claim listing their roles for this app ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=These%20application%20roles%20are%20defined,the%20form%20of%20role%20membership)).
  - For groups: if you want group IDs in the token, you need to configure the **Token Configuration** for the API app registration. You can choose to include group claims (for security groups or distribution lists). Be mindful of the 150-group limit – if a user is in many groups, the token might omit them and include `hasgroups` instead ([Secure Java Spring Boot apps using groups and group claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-group-entra-id#:~:text=token%20%20from%20Microsoft%20Entra,ID)). We will discuss using groups for RBAC in Section 7.3.

- **Multi-Tenant considerations:** Currently, if we set single-tenant, only accounts from our Azure AD can login. Multi-tenant apps require some additional settings (like verifying domain, and handling consent from external tenants). If you need multi-tenant, ensure "Accounts in any organizational directory" was chosen for both app registrations. We will cover specifics later, but just know that in multi-tenant scenario, tokens might have different issuer (the user's tenant) and you'll need to adjust backend validation.

Now Azure AD is configured to know about:

- A resource API identified by `api://...` with a scope.
- A client SPA allowed to request that scope.

The next steps are implementing the frontend and backend to use these details:

- The React app will use the MSAL library to log users in via Azure AD and acquire tokens for the defined scope.
- The Spring Boot app will enforce that incoming requests have a valid token with that scope or appropriate roles.

Before moving on, double-check that you have:

- **Tenant ID** (GUID) – used for authority URL.
- **Frontend Client ID**.
- **Backend (API) Client ID and scope name**.
- Redirect URI configured for frontend.
- (If testing via Postman or others, the secret if needed).

With Azure AD ready, let's implement the React frontend authentication.

---

# 4. Implementing Authentication in React (TypeScript)

The frontend will use **MSAL (Microsoft Authentication Library)** for JavaScript to handle the OAuth2/OIDC flow with Azure AD. MSAL provides high-level methods to manage user login, token acquisition, and session. We will use the official `@azure/msal-react` package, which is a wrapper around `@azure/msal-browser` for integration with React.

Key tasks in the React app:

- Install MSAL packages and configure them with our Azure AD app details.
- Initialize an MSAL instance and wrap our app with the provider to manage auth state.
- Create a login flow (redirect or popup) and a logout flow.
- Acquire access tokens and call the secured API.
- Reactively display content based on authentication state (e.g., show login button when not logged in, show app content when logged in).

## 4.1 Installing and Configuring MSAL (Microsoft Authentication Library)

Start by adding the MSAL libraries to the React project. In the `azure-ad-react-frontend` folder, run:

```bash
npm install @azure/msal-browser @azure/msal-react
```

This installs the core MSAL browser library and the React integration.

**MSAL configuration:** Next, create a configuration file (e.g., `src/authConfig.ts`) to hold Azure AD settings:

```typescript
// src/authConfig.ts
import { Configuration, LogLevel } from "@azure/msal-browser";

const tenantId = "<YOUR-TENANT-ID>";
export const msalConfig: Configuration = {
  auth: {
    clientId: "<YOUR-SPA-CLIENT-ID>",
    authority: `https://login.microsoftonline.com/${tenantId}`, // Azure AD authority URL
    redirectUri: "http://localhost:3000", // The redirect URI you registered
  },
  cache: {
    cacheLocation: "sessionStorage", // Tokens will be stored in session storage (not persisted across tabs)
    storeAuthStateInCookie: false, // Set to true if experiencing issues with cookies (e.g., IE)
  },
  system: {
    loggerOptions: {
      loggerCallback: (level, message) => {
        if (level === LogLevel.Error) {
          console.error(message);
        } else if (level === LogLevel.Info) {
          console.info(message);
        } else if (level === LogLevel.Verbose) {
          console.debug(message);
        } else if (level === LogLevel.Warning) {
          console.warn(message);
        }
      },
      logLevel: LogLevel.Info,
      piiLoggingEnabled: false,
    },
  },
};

export const loginRequest = {
  scopes: ["<YOUR-API-SCOPE-URI>"], // e.g., api://{api-client-id}/API.Access
};

export const logoutRequest = {
  // Optionally, specify a postLogoutRedirectUri if different from redirectUri
  postLogoutRedirectUri: "http://localhost:3000",
};
```

Let's break this down:

- `clientId`: The Application (client) ID of the SPA app registration.
- `authority`: The URL of the Azure AD tenant’s authorization server. By using `https://login.microsoftonline.com/<tenantId>/`, we ensure the user is directed to our specific tenant. (If multi-tenant, you might use `common` or `organizations` here.)
- `redirectUri`: Must match one of the URIs in Azure AD for this app. For development, it's `http://localhost:3000`.
- `cacheLocation`: We choose `sessionStorage` to store tokens. This means tokens persist per browser tab (not accessible to other tabs or after closing tab). This is safer than `localStorage` in terms of not persisting tokens on disk, but if you want SSO between tabs, you might opt for localStorage. We'll go with sessionStorage for security (less surface for token theft if XSS occurs).
- `storeAuthStateInCookie`: false is fine for most modern browsers. If dealing with older browsers or if cookies are needed for certain scenarios, one might enable it.
- Logging options: optional, but helpful for debugging authentication issues. We set a callback to output messages to console based on level.

We also define `loginRequest` which contains the scopes we want for login. We include our API scope (and MSAL will automatically include "openid" and "profile" by default when using MSAL's login methods for OIDC). If we wanted Graph API or other scopes, we'd include them too. For our case:

```js
scopes: ["api://<API-CLIENT-ID>/API.Access"];
```

This ensures the access token we get will allow calling our API (carrying that scope as proof of permission).

The `logoutRequest` can specify where to redirect after logout. Azure AD by default will go to the `redirectUri` if not specified, but we can explicitly set a `postLogoutRedirectUri` (here we just send user back to home page).

**Initialize MSAL in the app:** In the entry file (likely `src/index.tsx` with Create React App), we need to create an MSAL instance and wrap the app.

```tsx
// src/index.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";

import App from "./App";
import { msalConfig } from "./authConfig";

const msalInstance = new PublicClientApplication(msalConfig);

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <App />
    </MsalProvider>
  </React.StrictMode>
);
```

By wrapping `<App />` with `<MsalProvider instance={msalInstance}>`, we provide the MSAL context to the React app. All components within can now use hooks and context to interact with authentication state ([microsoft-authentication-library-for-js/lib/msal-react/docs/getting-started.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-react/docs/getting-started.md#:~:text=%60%40azure%2Fmsal,as%20a%20prop)) ([microsoft-authentication-library-for-js/lib/msal-react/docs/getting-started.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-react/docs/getting-started.md#:~:text=ReactDOM.render%28%3CAppProvider%20%2F%3E%2C%20document.getElementById%28)). This setup is required: _"@azure/msal-react is built on the React context API and all parts of your app that require authentication must be wrapped in the MsalProvider component."_ ([microsoft-authentication-library-for-js/lib/msal-react/docs/getting-started.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-react/docs/getting-started.md#:~:text=%60%40azure%2Fmsal,as%20a%20prop))

Now our React app has MSAL configured. Next, we implement the UI/logic to log in and log out.

## 4.2 Managing Authentication State in React

After MSAL setup, we can leverage the hooks and components provided by `@azure/msal-react` to manage user authentication status in the UI:

- **AuthenticatedTemplate** and **UnauthenticatedTemplate**: These are components that conditionally render children based on whether a user is logged in or not ([microsoft-authentication-library-for-js/lib/msal-react/docs/getting-started.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-react/docs/getting-started.md#:~:text=)). We can use them to show different parts of the UI.
- **useMsal() hook**: Provides the MSAL context, including methods like `instance` (the PublicClientApplication) and accounts info.
- **useIsAuthenticated() hook**: Returns a boolean indicating if a user is authenticated.
- **useAccount()** or **useMsalAuthentication()** can provide details of the current account.

Let's modify `App.tsx` as an example to use these:

```tsx
// src/App.tsx
import React from "react";
import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
} from "@azure/msal-react";
import { loginRequest } from "./authConfig";

const App: React.FC = () => {
  const { instance } = useMsal(); // MSAL instance to initiate login/logout

  const handleLogin = () => {
    // Choose between redirect and popup
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error(e);
    });
    // If using popup:
    // instance.loginPopup(loginRequest).catch(e => console.error(e));
  };

  const handleLogout = () => {
    instance.logoutRedirect({
      postLogoutRedirectUri: "/", // navigate to home after logout
    });
    // Or instance.logoutPopup() if using popup method
  };

  return (
    <div className="App">
      <h1>Welcome to My Azure AD Protected App</h1>

      <UnauthenticatedTemplate>
        {/* Shown only when not logged in */}
        <p>Please sign-in to continue.</p>
        <button onClick={handleLogin}>Login with Azure AD</button>
      </UnauthenticatedTemplate>

      <AuthenticatedTemplate>
        {/* Shown only when logged in */}
        <p>You are signed in!</p>
        <button onClick={handleLogout}>Logout</button>

        {/* Protected content goes here, e.g., call an API */}
        <SecureContent />
      </AuthenticatedTemplate>
    </div>
  );
};

export default App;
```

In this snippet:

- We use `<UnauthenticatedTemplate>` to render a login prompt and button when the user is not signed in.
- `<AuthenticatedTemplate>` renders when a user is signed in, showing a welcome and a logout button, and possibly some secure content component.
- The `handleLogin` function triggers the login process. Here we've chosen `loginRedirect`. This will redirect the browser to the Azure AD login page. After successful authentication, Azure will redirect back to our app (to the redirect URI), and MSAL will handle processing the response. (If we used `loginPopup`, a popup window would be used instead, keeping the SPA on the same page.)
- The `loginRequest` we pass includes the scopes (so Azure knows which resources the token should allow).
- The `handleLogout` calls `logoutRedirect` which will clear the MSAL cache and redirect to Azure AD to log out the user from Azure AD (and then back to the provided URL). This ensures a full logout (so that if the user tries to log in again, they might be asked for credentials if no other sessions are present).

Under the hood, when `instance.loginRedirect` is called:

- MSAL builds the authorization URL with our clientId, scopes, redirectUri, etc., and navigates the browser there.
- After login, Azure AD sends the user back to `http://localhost:3000` with an auth code (and state).
- MSAL intercepts this (the MSAL provider internally calls `handleRedirectPromise()` on page load) and exchanges the code for tokens. This happens quickly, and MSAL then stores the tokens in the chosen cache (sessionStorage).
- The user is now considered logged in; `AuthenticatedTemplate` will render and `useIsAuthenticated()` would return true.
- The account info (like username) is accessible via `instance.getAllAccounts()` or the `useMsal` hook (e.g., `instance.getActiveAccount()` if one account).

We can also display the logged-in user's name/email by using MSAL:

```tsx
import { useAccount, useIsAuthenticated } from "@azure/msal-react";

// inside AuthenticatedTemplate
const accounts = instance.getAllAccounts();
const username = accounts[0]?.username; // or .name depending on claims (username often is email or UPN)
<p>Welcome, {username}!</p>;
```

Alternatively, `useAccount({ username: desiredUsername })` can retrieve a specific account object.

**Important**: The first time a user logs in, if admin consent wasn't pre-granted, Azure AD would show a consent screen listing the requested permissions (e.g., "Allow this app to access MyApp API on your behalf"). We granted admin consent for our custom API, so the user likely will only see a generic "Permissions you granted: Sign you in and read your profile" (the default openid and profile) or none at all if even that is pre-consented. This smooths the UX.

Now, with a user logged in, MSAL stores:

- An **ID token** (in cache) with user info.
- An **access token** for our API (for the scope `API.Access`), along with a **refresh token** if applicable.

The next step is to use the access token to call our Spring Boot API.

## 4.3 Handling Login, Logout, and Token Renewal

We already implemented the basics of login and logout in the UI. Let's delve a bit deeper into token management and renewal:

- **Login (Auth code flow)**: On calling `loginRedirect` or `loginPopup`, MSAL takes care of the PKCE challenge and storing the code verifier, so that when Azure AD returns with the code, MSAL can redeem it. We do not see the code directly; MSAL handles it behind the scenes. MSAL will request both an ID token and an access token in the code exchange. The ID token is for the client app (contains user identity, no need to send it to backend), and the access token is for the API scope we requested.

- **Storing tokens**: We configured `cacheLocation: "sessionStorage"`, so if you open developer tools -> Application -> Session Storage, you will see entries for MSAL. They include access token, ID token, refresh token, etc., keyed by client and scopes. MSAL abstracts this; we rarely need to directly manipulate it.

- **Token renewal**: Access tokens have limited lifetimes (often ~1 hour for Azure AD tokens). MSAL will automatically attempt to renew tokens when they expire. Typically:
  - MSAL keeps track of expiration times. If you call `acquireTokenSilent` for a scope, and the existing token is still valid (or within a comfortable refresh window), it will return it from cache.
  - If the token is expired or nearly expired, MSAL will try to use the refresh token to get a new one without user interaction. This is done behind the scenes – you usually just call `acquireTokenSilent` and MSAL handles whether it can get a fresh token silently.
  - If the refresh token is also expired or invalid (maybe user revoked consent or password changed), `acquireTokenSilent` will throw an `InteractionRequiredAuthError`. At that point, you need to prompt the user to login again (likely by calling `loginRedirect` again). Our app could catch this scenario and trigger a re-login. MSAL's hooks or higher-order components might also handle it for you if using `MsalAuthenticationTemplate`.
  - Azure AD’s default refresh token lifetime is long (e.g., 24 hours with sliding window up to 90 days of inactivity), so typically users won't have to fully log in often if they use the app regularly and the refresh token remains valid.

MSAL React also provides a component `MsalAuthenticationTemplate` or hook `useMsalAuthentication` to automatically handle ensuring a user is authenticated before showing some component, including attempting silent token acquisition and falling back to interactive if needed. For simplicity, we used manual login handling.

**Logout**: Calling `instance.logoutRedirect()` will clear MSAL's cache and redirect to Azure AD's logout endpoint. That will clear the user's session cookie with Azure AD (so they are logged out of the identity provider as well). If the user had been signed into multiple apps using that same Azure AD session, logging out of one could sign them out of others, depending on whether those apps check for the session. Azure AD supports single sign-out but it’s not always automatic for SPAs; however, clearing the server session ensures any new token requests will prompt for login again. After logout, Azure AD redirects to our `postLogoutRedirectUri`.

We should test these flows:

- Start the React app (`npm start`), click login. You should see Azure AD’s login, enter your credentials (for a user in your tenant).
- After login, you come back to the app, and "You are signed in!" appears (AuthenticatedTemplate content).
- Open console to see if any errors. (If misconfigured, MSAL would log errors. Common mistakes: incorrect redirect URI (leading to error in redirect), or scope not granted (leading to consent error).)
- Try the logout button; it should send you to an Azure page briefly then back to homepage with "Please sign-in".

At this stage, our React app can authenticate against Azure AD and knows who the user is. Next, let's integrate the API call with the obtained access token.

## 4.4 Secure API Calls using Access Tokens

The whole point of obtaining an access token is to call our protected Spring Boot API. We will assume the Spring Boot API will have endpoints that require a valid token (which we'll implement in Section 5). Here in the React app, we need to attach the token to HTTP requests.

Let's create a new component or function to call the API. For demonstration, we'll add a `SecureContent` component that calls a `/api/hello` endpoint on our backend and displays the result.

```tsx
// src/SecureContent.tsx
import React, { useState } from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";

const SecureContent: React.FC = () => {
  const { instance, accounts } = useMsal();
  const [apiResponse, setApiResponse] = useState<string>("");

  const callApi = async () => {
    if (accounts.length === 0) {
      setApiResponse("No signed-in account.");
      return;
    }
    try {
      // Acquire an access token silently
      const response = await instance.acquireTokenSilent({
        ...loginRequest,
        account: accounts[0], // use the first account (currently active user)
      });
      const accessToken = response.accessToken;
      console.log("Access Token acquired: ", accessToken);

      // Call the API
      const result = await fetch("http://localhost:8080/api/hello", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!result.ok) {
        throw new Error("API response status: " + result.status);
      }
      const data = await result.text(); // assuming the API returns plain text
      setApiResponse(data);
    } catch (err: any) {
      if (err.name === "InteractionRequiredAuthError") {
        // Token couldn't be acquired silently - need user to login again
        try {
          const response = await instance.acquireTokenPopup(loginRequest);
          const accessToken = response.accessToken;
          const result = await fetch("http://localhost:8080/api/hello", {
            headers: { Authorization: `Bearer ${accessToken}` },
          });
          const data = await result.text();
          setApiResponse(data);
        } catch (popupError) {
          console.error(popupError);
          setApiResponse("Failed to acquire token: " + popupError);
        }
      } else {
        console.error(err);
        setApiResponse("Error: " + err.message);
      }
    }
  };

  return (
    <div>
      <button onClick={callApi}>Call Secure API</button>
      {apiResponse && (
        <div>
          <strong>API Response:</strong> {apiResponse}
        </div>
      )}
    </div>
  );
};

export default SecureContent;
```

And include this `<SecureContent />` inside the AuthenticatedTemplate in `App.tsx` as shown earlier.

What this does:

- `instance.acquireTokenSilent` is used to get a fresh access token for our API scope, using the cached account. We pass the same `loginRequest` scopes. Since the user is already logged in and consented, this should usually return quickly with a token from cache or refresh it if needed.
- We then do a `fetch` call to `http://localhost:8080/api/hello` with the `Authorization: Bearer <token>` header. This is how we authenticate to the API.
- If the token is expired and cannot be refreshed silently (maybe user’s session expired or some conditional access), `acquireTokenSilent` will throw an `InteractionRequiredAuthError`. We catch that and attempt `acquireTokenPopup` as a fallback, which will prompt the user interactively to sign in again (likely just a quick popup if their session is still active, or credentials if not).
- We handle any errors and display them or log them.

We should ensure CORS is configured on the backend (we’ll do this in the Spring Boot section) so that this fetch is not blocked by the browser. Also, for local dev, the URL is hard-coded; in production, you'd have a config or environment variable for the API base URL.

With this code, clicking "Call Secure API" will:

1. Acquire a token (if not already in cache).
2. Send request to the API with the token.
3. Show the response or errors.

For now, the API endpoint `/api/hello` is hypothetical. We will implement a simple controller in Spring Boot that returns some text (e.g., "Hello [username], you have accessed a protected endpoint") to test this round-trip.

### Frontend Recap:

- We have set up MSAL for login/logout.
- We manage state with MSAL's context and show UI accordingly.
- We retrieve tokens and use them to call the backend.

From a security perspective on the frontend:

- We never store user passwords; Azure AD handles that.
- The tokens (particularly access token and refresh token) are stored in sessionStorage (which is reasonably secure from other sites, but could be accessed by JS on our site if XSS occurs). We should ensure our app is free of XSS vulnerabilities because if an attacker can run JS in our SPA, they could potentially grab tokens. Using React (which escapes content by default) helps prevent injection, but be mindful when integrating any user-provided data.
- When calling the API, always use HTTPS in production. In development, we're on HTTP for ease, but in production the API should be HTTPS and same for the SPA if not on a trusted domain. Azure AD won’t allow non-HTTPS redirect URIs in production (except for `localhost`).
- We use Bearer tokens directly. Another approach could be to use MSAL to acquire an ID token and then use a secure cookie with session on backend, but that complicates things and loses the benefit of pure JWT auth. Our approach is standard for SPA + API.

Now that the frontend can obtain tokens and attempt to call the API, let's build the Spring Boot backend to accept and validate these tokens.

---

# 5. Building a Secure Spring Boot Backend

The backend will use **Spring Boot** with **Spring Security** to validate Azure AD JWT tokens on incoming requests. We will configure it as an **OAuth2 Resource Server**, meaning it will accept Bearer tokens and verify them. We'll also implement **role-based access control (RBAC)** for endpoints and ensure that only authorized tokens can retrieve protected data.

Key tasks for the backend:

- Add Spring Security configuration to enable JWT authentication using Azure AD as the issuer.
- Validate the JWT’s signature and claims (issuer, audience, etc.).
- Map token claims (like scope or roles) to Spring Security authorities for RBAC.
- Secure specific URL patterns or methods with roles/scopes.
- Interact with MySQL (via Spring Data JPA) if needed for additional user data (we'll cover in Section 6, but minimal for now).
- Provide endpoints that the frontend can call (e.g., `/api/hello`).

## 5.1 Setting up Spring Security with OAuth2 (Azure AD Integration)

Spring Boot makes it relatively straightforward to set up a resource server for JWT validation. We need to:

- Add the OAuth2 Resource Server dependency (already included via Spring Security + Spring Boot starters we chose).
- Configure the OAuth2 resource server properties (issuer URI, audience).
- Write a security configuration class to specify how requests are secured.

First, ensure the Maven `pom.xml` has the needed Spring Security and OAuth components. If you used Spring Initializr with "Spring Security" and "OAuth2 Resource Server", you should have:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

And possibly `spring-boot-starter-web` (for MVC/REST) and `spring-boot-starter-jpa` (for DB).

With these, Spring Security auto-configures a lot for us. The key configuration is to point Spring Security to Azure AD as the OAuth2 issuer.

Add the following to `application.properties` (or `application.yml` if you prefer YAML):

```properties
# Azure AD (Microsoft identity platform) configuration
spring.security.oauth2.resourceserver.jwt.issuer-uri = https://login.microsoftonline.com/<TENANT_ID>/v2.0
spring.security.oauth2.resourceserver.jwt.audience = <API-CLIENT-ID>
```

Explanation:

- The `issuer-uri` is the base URL that identifies the token issuer (including `v2.0` for the Microsoft identity platform endpoint). By setting this, Spring Security will **discover** the OpenID Provider Configuration automatically (it will call `/.well-known/openid-configuration` on that issuer) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=spring%3A%20security%3A%20oauth2%3A%20resourceserver%3A%20jwt%3A,uri%3A%20https%3A%2F%2Fidp.example.com%2Fissuer)). From that, it gets the JWKS (keys for verifying tokens) and accepted issuer claim. Essentially, this one property allows Spring to know how to validate the token's signature and issuer.
- The `audience` property is used to validate the `aud` (audience) claim in the JWT. Azure AD tokens for our API should have the API's client ID or the App ID URI as the audience (commonly it’s the client ID, but Azure might also put the App ID URI in some cases). Setting this ensures that a token intended for another app is not accepted by our API. If a token's audience doesn't match, it will be rejected.

With these properties, **Spring Security will automatically configure JWT validation** at startup ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=Startup%20Expectations)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=4,idp.example.com)). The application will fetch Azure AD’s public signing keys and be ready to verify tokens. If Azure AD is unreachable at startup (no internet), the app might fail to start by default because it wants to get the JWKS; in dev make sure internet is accessible (or consider using jwk-set-uri property to a cached JWKS file if needed).

Next, we need to configure **authorization rules** – i.e., which endpoints require authentication, and what roles/scopes are needed.

Let's create a security config class `SecurityConfig.java`:

```java
// src/main/java/com/example/azureadbackend/config/SecurityConfig.java
package com.example.azureadbackend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // By default, Spring Security will authenticate all requests
        http.authorizeHttpRequests(authorize -> authorize
                // define public endpoints if any
                .requestMatchers("/public/**").permitAll()
                // everything else requires authentication
                .anyRequest().authenticated()
        );

        // Enable JWT bearer token authentication
        http.oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter()))
        );

        // (Optional) If using cookies for JSESSIONID and want stateless, disable session creation:
        http.oauth2ResourceServer().and().csrf().disable().sessionManagement().disable();

        return http.build();
    }

    private Converter<org.springframework.security.oauth2.jwt.Jwt, ?> jwtAuthenticationConverter() {
        // This converter will extract roles or scopes from the token to grant authorities
        JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
        // By default, JwtGrantedAuthoritiesConverter looks at "scope" or "scp" claim for permissions.
        // We can also configure it to look at "roles" claim if Azure AD app roles are used:
        grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
        grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
        // Also, it will parse "scp" with prefix "SCOPE_" by default if scope present.

        JwtAuthenticationConverter jwtAuthConverter = new JwtAuthenticationConverter();
        jwtAuthConverter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
        return jwtAuthConverter;
    }
}
```

Let's explain this configuration:

- We use the newer component-based security configuration (`SecurityFilterChain` bean) rather than extending `WebSecurityConfigurerAdapter` (which is deprecated in Spring Security 5+).
- We call `authorizeHttpRequests` to define URL access rules. We allow `/public/**` to be open (just as an example if we have a health check or landing page), and require any other request to be authenticated (`.anyRequest().authenticated()`).
- `http.oauth2ResourceServer().jwt()` enables JWT token processing for OAuth2 Bearer authentication. We supply a `jwtAuthenticationConverter` which is used to convert a validated JWT into a Spring Security **Authentication** (specifically a `JwtAuthenticationToken`).
- In the `jwtAuthenticationConverter()` method:
  - We create a `JwtGrantedAuthoritiesConverter`. This class by default will take the token's "scope" or "scp" claim and turn each scope string into an authority like `SCOPE_<scopeName>`. That is useful if we want to check scopes in security rules (like `.hasAuthority('SCOPE_API.Access')`).
  - We configure it to also use the "roles" claim and prefix them with "ROLE\_". This means if our token has `"roles": ["Admin"]`, it will produce a `GrantedAuthority` named "ROLE_Admin". This fits Spring’s convention so that we can use `hasRole("Admin")` in method security or config.
  - We set this converter into a `JwtAuthenticationConverter` and return it. Spring Security will then use it for each incoming JWT. The result is that any roles in the JWT will be mapped to Spring Security roles, and scopes (if present) will map to `SCOPE_...` authorities.
- We also disable CSRF and session management. Because we are using stateless tokens, we typically disable CSRF (especially if not serving a browser client from this domain) and ensure the server doesn't create HTTP sessions for each request. `.sessionManagement().disable()` might not be strictly needed (and in some setups you might prefer `.sessionCreationPolicy(SessionCreationPolicy.STATELESS)` instead), but the idea is to not store security context in a session. Each request will be authenticated via token afresh.

Now, with this config:

- If a request comes to `/api/hello`, Spring will check for an `Authorization: Bearer <token>` header. If present, it will validate the JWT:
  - Check signature using Azure AD public keys.
  - Check `iss` (issuer) matches `https://login.microsoftonline.com/<tenantId>/v2.0` (and optionally the tenant in the token must match if single-tenant).
  - Check `aud` (audience) matches our configured audience (the client ID).
  - Check expiration (`exp`) is in the future, etc.
- If token is valid, it will build an Authentication object with authorities as per converter:
  - If the token has `"roles": ["Admin"]`, the user gets authority "ROLE_Admin".
  - If token has `"scp": "API.Access"`, user gets authority "SCOPE_API.Access" (assuming default scope claim reading).
- Because `.anyRequest().authenticated()`, as long as the token is valid, the request passes general security. If token is missing or invalid, Spring Security will automatically reject the request with HTTP 401 (Unauthorized) or 403 (Forbidden) as appropriate. (By default, missing token -> 401, token present but invalid or insufficient -> 403.)
- We haven't restricted by role in this config at the URL level, but we will show usage via method-level security next.

**Add a sample Controller:**

Let's create a simple REST controller to test:

```java
// src/main/java/com/example/azureadbackend/controllers/HelloController.java
package com.example.azureadbackend.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String hello(Principal principal) {
        // Principal name in case of JWT is typically the "sub" or "name" claim. Azure AD by default sets "name" claim to user's name.
        String username = principal.getName();
        return "Hello, " + username + "! You have accessed a protected endpoint.";
    }

    @GetMapping("/admin")
    // Only allow users with Admin role (assuming roles claim was mapped)
    // We'll add method security to enforce this:
    public String adminOnly() {
        return "Secret admin data";
    }
}
```

The `Principal` injected will be a `JwtAuthenticationToken` under the hood, but Spring gives it as interface. `principal.getName()` by default will return the JWT's subject or preferred username. Azure AD populates `preferred_username` or `name` claim typically. By default, Spring Security uses `JwtAuthenticationToken.getName()` which returns the token’s `sub` (subject, a GUID). We might want the human-friendly name. We could configure a converter to use `name` claim as principal name if desired. For simplicity, it's fine.

For the `/admin` endpoint, we want only admins. We can enforce that by adding Spring Security method-level annotation:
First, enable method security in our config:

```java
// Add to SecurityConfig class:
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;

@Configuration
@EnableMethodSecurity
public class SecurityConfig { ... }
```

Now in the controller:

```java
@PreAuthorize("hasRole('Admin')")
@GetMapping("/admin")
public String adminOnly() { ... }
```

This requires the authentication to have ROLE_Admin authority, which our converter provides if token contains "Admin" in roles claim. Alternatively, we could use `@PreAuthorize("hasAuthority('SCOPE_API.Access')")` to require the scope instead (if not using roles). But roles are more straightforward for RBAC.

Don't forget to include the necessary imports for `@PreAuthorize` (from `org.springframework.security.access.prepost.PreAuthorize`) and annotate the class or method accordingly. We also added `@EnableMethodSecurity` to activate those annotations.

**CORS Configuration:**

Since our React app is on localhost:3000 and our API on 8080, we need to allow cross-origin requests. Easiest way:

- We can use Spring's `@CrossOrigin` annotation on the controller or method: `@CrossOrigin(origins = "http://localhost:3000")` above the class or specific methods. This sends the appropriate CORS headers to let the browser call from that origin.
- Or define a global CORS config bean:

```java
// In SecurityConfig or another config class
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Bean
public WebMvcConfigurer corsConfigurer() {
    return new WebMvcConfigurer() {
        @Override
        public void addCorsMappings(CorsRegistry registry) {
            registry.addMapping("/api/**")
                    .allowedOrigins("http://localhost:3000")
                    .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS");
        }
    };
}
```

This will allow our frontend origin to access any `/api/**` endpoints with GET/POST etc. In production, you'd restrict the allowed origin to your actual domain or use a config.

Now, let's run the Spring Boot application (via `mvn spring-boot:run` or your IDE). If configured correctly, it should start without errors:

- Check the logs – Spring Security might log that it found issuer config or loaded keys. If something wrong with contacting Azure AD, you'll see errors.
- The app will be listening on port 8080.

Test manually (without the React app):

- Try accessing `http://localhost:8080/api/hello` in a browser or with curl without a token. You should get a 401 Unauthorized (because no token).
- With Postman, you could test by getting a token from Azure AD and attaching it. But easier: use the React app.

Now use the React app (which we set to call /api/hello):

- Ensure the React dev server is running.
- Log in, then click "Call Secure API".
- The fetch should return "Hello, [some identifier]! You have accessed a protected endpoint." displayed on the page.
- If there's an error, open dev console and network tab:
  - 401 or 403 would indicate something with token (maybe token not accepted – check the audience claim in the token vs what backend expects).
  - CORS error would indicate the request never reached because the browser blocked it (means our CORS config didn't work). If so, fix the CORS (check response headers in network for Access-Control-Allow-Origin).
  - If you see an error like "invalid token signature" or similar, it might mean misconfigured issuer or keys not matching. Make sure tenantId in issuer URI is correct and using `/v2.0`. The token's `iss` claim must match exactly what Spring expects (which is the issuer-uri we set, possibly with tenant).
  - If it's working but `principal.getName()` shows a GUID, and you'd rather see user email or name, consider customizing principal name. But it's not critical for function.

If everything is correct, we have:

- Completed a full login on front, got token, made API request, validated token, and returned data.

At this stage, our application is functioning with Azure AD authentication:

- The frontend handles user login via MSAL (OAuth2/OIDC).
- The backend secures endpoints with Spring Security using JWT validation.
- Both are integrated using Azure AD token issuance.

However, we have not yet integrated MySQL or persistent user data beyond Azure AD. Right now, our app relies solely on Azure AD for authentication and roles (if any roles were added to token).

In the next section, we'll integrate MySQL, which could be used to store application-specific user information, such as additional profile details or roles not managed in Azure AD. This could also demonstrate how to combine Azure AD identity with a local database for extended functionality (common in enterprise apps that use AD for login but maintain their own user database for domain-specific settings).

---

# 6. Integrating MySQL for User Data Management

In many real-world scenarios, Azure AD provides authentication, but applications maintain their own database of users for additional metadata or fine-grained permissions. We will integrate MySQL via Spring Data JPA to store and manage user roles and permissions. Our plan:

- Define **JPA entities** for `User` and `Role`.
- When a user authenticates via Azure AD, ensure they have an entry in the `users` table (possibly auto-create it if new).
- Manage roles either by syncing with Azure AD roles/groups or by assigning within the app.
- Use the database roles in the authorization logic (perhaps merging with Azure roles).

For demonstration, let's assume we want to allow app-specific roles that might not be directly tied to Azure AD app roles. We could, for example, treat Azure AD as the source of identity (who the user is), but trust our own DB for what roles they have in the application. This might be the case if the app admin wants to assign roles to users within the app without creating those roles in Azure AD (or if not all roles are coming from AD groups).

## 6.1 Setting up the MySQL Database

We already created a database (`azure_ad_app_db`) and configured Spring Boot's datasource in Section 2.2. Let's ensure the DB is running:

- If using local MySQL, start the service.
- If using Docker, ensure the container is up.
- Test connectivity (maybe via MySQL Workbench or `mysql -u azureappuser -p -h 127.0.0.1 azure_ad_app_db`).

In `application.properties`, we have the connection URL, user, password set. With Spring Data JPA and `ddl-auto=update`, it will create tables based on our entities.

## 6.2 Configuring Spring Data JPA

We need to create the entity classes and repositories.

**User Entity:**
We will store minimal info: an `id`, the user's Azure AD identifier or username, and their roles.

What unique identifier to use for users? Options:

- Azure AD Object ID (`oid` claim from token, a GUID for the user) – globally unique and immutable for the user in that tenant.
- User principal name or email (`preferred_username` claim, typically the login email).
- We could use email as username in our DB, but note that if email changes or user has multiple, the stable one is `oid`.

Using `oid` (GUID) is safe for uniqueness. But for readability, we'll also store email or name.

We'll assume the token’s `oid` claim as our `userId` and `name` claim or `preferred_username` as email.

```java
// src/main/java/com/example/azureadbackend/models/AppUser.java
package com.example.azureadbackend.models;

import jakarta.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
public class AppUser {
    @Id
    @Column(length = 50)
    private String id;  // we'll store Azure AD oid as string

    private String email;
    private String displayName;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<AppRole> roles = new HashSet<>();

    // Constructors, getters, setters omitted for brevity

    public AppUser() {}
    public AppUser(String id, String email, String displayName) {
        this.id = id;
        this.email = email;
        this.displayName = displayName;
    }

    // ... getters and setters ...
}
```

**Role Entity:**
We'll have a roles table to define roles.

```java
// src/main/java/com/example/azureadbackend/models/AppRole.java
package com.example.azureadbackend.models;

import jakarta.persistence.*;
import java.util.Set;

@Entity
@Table(name = "roles")
public class AppRole {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String name;  // e.g., "Admin" or "User"

    private String description;

    @ManyToMany(mappedBy = "roles")
    private Set<AppUser> users;

    // Constructors, getters, setters
    public AppRole() {}
    public AppRole(String name) {
        this.name = name;
    }
    // ... other getters/setters ...
}
```

We define a bidirectional many-to-many (users <-> roles) with a join table `user_roles` (user_id, role_id). The `fetch = EAGER` on roles for user is to easily get roles when we load a user.

**Repositories:**
Now create Spring Data JPA repositories to easily query these:

```java
// src/main/java/com/example/azureadbackend/repositories/UserRepository.java
package com.example.azureadbackend.repositories;

import com.example.azureadbackend.models.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<AppUser, String> {
    Optional<AppUser> findByEmail(String email);
}
```

And:

```java
// src/main/java/com/example/azureadbackend/repositories/RoleRepository.java
package com.example.azureadbackend.repositories;

import com.example.azureadbackend.models.AppRole;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RoleRepository extends JpaRepository<AppRole, Long> {
    Optional<AppRole> findByName(String name);
}
```

These give basic CRUD operations. We can find users by id or email, find roles by name, etc.

We need to ensure Spring scans these packages. With Spring Boot, if our main Application class is in `com.example.azureadbackend`, and our repos are in a sub-package, they will be auto-scanned.

**Database initialization:**
With `spring.jpa.hibernate.ddl-auto=update`, running the app will create tables:

- `users` with columns (id, email, display_name).
- `roles` with (id, name, description).
- `user_roles` join table.

We might want to pre-populate some roles. We could do this with a data SQL or programmatically on startup:
One quick way: use Spring Boot’s data.sql or schema.sql, but let's do via code for flexibility.

Write a runner to initialize roles:

```java
// src/main/java/com/example/azureadbackend/config/DataInitializer.java
package com.example.azureadbackend.config;

import com.example.azureadbackend.models.AppRole;
import com.example.azureadbackend.repositories.RoleRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final RoleRepository roleRepo;

    public DataInitializer(RoleRepository roleRepo) {
        this.roleRepo = roleRepo;
    }

    @Override
    public void run(String... args) throws Exception {
        // Create default roles if not exist
        if (roleRepo.findByName("Admin").isEmpty()) {
            roleRepo.save(new AppRole("Admin"));
        }
        if (roleRepo.findByName("User").isEmpty()) {
            roleRepo.save(new AppRole("User"));
        }
    }
}
```

This will run at startup to ensure "Admin" and "User" roles exist in DB.

Now, how do we assign roles to users upon login? We have a few approaches:

- Since this is stateless API, there's no explicit "login" event on backend. The user just presents a token.
- We could create an endpoint that the frontend calls after login to register the user.
- Or we could intercept the first request with a token and auto-provision the user in DB if not present.
- Spring Security allows adding custom logic via filters or customizing the JwtAuthenticationConverter to load user details.

A relatively straightforward way:
We can create a filter in the security chain that runs after JWT authentication and does:

- Check if `userRepository.findById(jwt.getSubject())` exists.
- If not, create a new AppUser with id = jwt.getSubject() (or maybe use `oid` claim directly), set email = `preferred_username`, displayName = `name` claim.
- Assign default role (maybe "User" role) to them.
- Save to DB.
  This way, any new user logging in gets auto-added.

However, writing a filter might be a bit complex for a guide. Alternatively, we create a simple controller endpoint `/api/register` which the frontend can call once after login, passing the token (or just rely on token in call). But since the token is already present in calls, a dedicated register endpoint is not necessary.

Let's attempt the filter approach for completeness (advanced devs can follow). We can use Spring Security’s `JwtAuthenticationToken` which is set in SecurityContext after JWT validation.

One way is to use Spring Security's ability to add an `AuthenticationManagerResolver` or just a once-per-request hook.

A simpler approach: in the `HelloController.hello()` method, we can check if user exists in DB and create if not. But that mixes concerns in a controller. Better to do it as a @Service or filter.

Let's do a filter that runs for authenticated requests:

```java
// src/main/java/com/example/azureadbackend/config/UserProvisioningFilter.java
package com.example.azureadbackend.config;

import com.example.azureadbackend.models.AppUser;
import com.example.azureadbackend.repositories.RoleRepository;
import com.example.azureadbackend.repositories.UserRepository;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Optional;

@Component
public class UserProvisioningFilter implements Filter {

    private final UserRepository userRepo;
    private final RoleRepository roleRepo;

    public UserProvisioningFilter(UserRepository userRepo, RoleRepository roleRepo) {
        this.userRepo = userRepo;
        this.roleRepo = roleRepo;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
                          throws IOException, ServletException {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.isAuthenticated()
                && auth.getPrincipal() instanceof org.springframework.security.oauth2.jwt.Jwt) {
            // Authenticated with a JWT
            org.springframework.security.oauth2.jwt.Jwt jwt = (org.springframework.security.oauth2.jwt.Jwt) auth.getPrincipal();
            String oid = jwt.getClaim("oid");  // Object ID
            String email = jwt.containsClaim("preferred_username")
                            ? jwt.getClaim("preferred_username")
                            : jwt.getClaim("email");
            String name = jwt.containsClaim("name") ? jwt.getClaim("name") : email;
            if (oid != null) {
                Optional<AppUser> userOpt = userRepo.findById(oid);
                if (userOpt.isEmpty()) {
                    // User not in DB, create
                    AppUser newUser = new AppUser(oid, email, name);
                    // Assign default "User" role
                    roleRepo.findByName("User").ifPresent(role -> {
                        newUser.getRoles().add(role);
                    });
                    userRepo.save(newUser);
                    System.out.println("Provisioned new user in DB: " + email);
                } else {
                    // User exists, optionally update any details like email or name if changed
                    AppUser existing = userOpt.get();
                    boolean updated = false;
                    if (email != null && !email.equals(existing.getEmail())) {
                        existing.setEmail(email);
                        updated = true;
                    }
                    if (name != null && !name.equals(existing.getDisplayName())) {
                        existing.setDisplayName(name);
                        updated = true;
                    }
                    if (updated) {
                        userRepo.save(existing);
                    }
                }
            }
        }
        // continue filter chain
        chain.doFilter(request, response);
    }
}
```

This filter:

- Checks if the request is authenticated and principal is a Jwt (meaning we have a JWT from Azure AD).
- Extracts `oid`, `preferred_username` (or email), and `name` from the token.
- If the user (by oid as ID) is not in DB, it creates an `AppUser` with that ID, sets email/name, and gives them the "User" role by default.
- If they exist, updates their email or name in DB in case those changed (keeping DB in sync with AD).
- Saves changes.

We mark it with @Component so Spring registers it as a bean. But we need to ensure it is added to the security filter chain _after_ JWT authentication has happened (so that `SecurityContextHolder` is populated). In Spring Security config, the `oauth2ResourceServer().jwt()` adds a filter for JWT auth. Our filter should come after that.

We can rely on default order by just adding it as a bean of type Filter, or we can explicitly add it via `http.addFilterAfter(new UserProvisioningFilter(...), OAuth2AuthenticationProcessingFilter.class)` etc. But simpler: since it’s a @Component and Spring Boot auto registers filters, and because Security filters are typically ordered, we might need to specify order or rely on registration bean. Perhaps easier: use `@Order` on the component to place it appropriately.

We want it to run after Spring Security’s authentication filter. The JWT auth filter in Spring Security (resource server) likely runs around `FilterSecurityInterceptor`.

Alternatively, we integrate this logic into the JwtAuthenticationConverter where we already intercept the JWT to convert roles. But writing to DB in the converter might be unconventional (as converters usually just map claims).

A filter is fine. Let's ensure ordering:
We can try with `@Order(1)` (security filter chain is at a higher precedence I think by default).
Alternatively, we can register it via `http.addFilterAfter(userProvisioningFilter, UsernamePasswordAuthenticationFilter.class)` in security config, but since it's JWT, maybe `BearerTokenAuthenticationFilter` is the specific filter.

Actually, `spring-boot-starter-oauth2-resource-server` likely uses `BearerTokenAuthenticationFilter`. We want after authentication, so after `BearerTokenAuthenticationFilter`.

We can do:

```java
@Autowired
private UserProvisioningFilter userProvisioningFilter;

@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    ...
    http.addFilterAfter(userProvisioningFilter, BearerTokenAuthenticationFilter.class);
    return http.build();
}
```

Add `import org.springframework.security.oauth2.server.resource.web.BearerTokenAuthenticationFilter`.

This ensures our filter runs after the token is processed and authentication is set.

Now, with that in place, whenever an authenticated call comes in, the user is auto-provisioned.

We should test:

- If a new user logs in (not in DB), the filter logs "Provisioned new user in DB".
- If they call endpoints, roles from DB aren't automatically applied to Spring authorities in the current request. Actually, we added the user to DB, but that doesn't affect the current token's authorities. If we want to enforce DB roles, we might need to incorporate them into the security context authorities. That’s a bit more involved because the token already had roles or not.

One approach: After provisioning or fetching the user from DB, we could manually set the Spring Security `Authentication`'s authorities to include the DB roles. But `Authentication` at this point is a JwtAuthenticationToken, which got roles from Azure AD (if any). We could wrap it in another Authentication with combined roles. That gets complicated; an alternative is to not use Azure AD roles at all, and instead solely rely on DB roles by mapping all users to their DB roles.

For example, we could ignore the "roles" claim from token, and instead, after verifying JWT, look up user in DB and assign their roles as authorities. This essentially means Azure AD is only providing identity, not roles.

This can be achieved by customizing the Jwt to authorities conversion:
Instead of using `JwtGrantedAuthoritiesConverter` for roles, we could write a custom `Converter<Jwt, AbstractAuthenticationToken>` that:

- Validates token (Spring does it)
- Looks up AppUser in DB (like we just did in filter)
- Creates authorities from AppUser.roles (prefix with ROLE\_).
- Returns an `UsernamePasswordAuthenticationToken` or `JwtAuthenticationToken` with those authorities.

This is doable, but now we have complexity: needing the repository in the converter (which is a bean we can autowire if we declare converter as a bean).

Given the advanced nature, it's fine, but let's see if a simpler compromise:
We already ensure the user has at least "User" role in DB. We can still use Azure AD roles for enforcement if any (like if we set up Azure app roles), but we could also now allow app-specific roles by manually checking DB within endpoints or via a service.

However, for a clean RBAC, ideally the Spring Security should be aware of DB roles. Let's attempt to incorporate DB roles:

We can modify our SecurityConfig:

- Remove `grantedAuthoritiesConverter.setAuthoritiesClaimName("roles")` to not auto map Azure roles.
- Instead, in the `UserProvisioningFilter`, after saving or retrieving user, we have their roles. We can add those roles as GrantedAuthorities to the Authentication.

But SecurityContextHolder holds an immutable Authentication at that point (the JwtAuthenticationToken from the filter chain). We could replace the Authentication:

```
List<GrantedAuthority> combinedAuthorities = new ArrayList<>(auth.getAuthorities());
for each role in user.getRoles(): combinedAuthorities.add(new SimpleGrantedAuthority("ROLE_"+role.getName()));
Then create new Authentication e.g. UsernamePasswordAuthenticationToken or JwtAuthenticationToken with same principal and combined authorities.
SecurityContextHolder.getContext().setAuthentication(newAuth)
```

If we do that in the filter, then further down the chain, the controller’s `@PreAuthorize("hasRole('Admin')")` will see the updated authorities.

Let's do that:

In `UserProvisioningFilter` after we ensure user exists, fetch user from DB (whether new or existing):

```java
AppUser user = userRepo.findById(oid).get();
// Build authorities from DB roles
Collection<GrantedAuthority> extraAuth = user.getRoles().stream()
    .map(role -> new SimpleGrantedAuthority("ROLE_" + role.getName()))
    .collect(Collectors.toSet());
// Combine with existing authorities (like scopes or Azure roles)
Collection<GrantedAuthority> currentAuth = new ArrayList<>(auth.getAuthorities());
currentAuth.addAll(extraAuth);
// Create new authentication token
Authentication newAuth = new JwtAuthenticationToken(jwt, currentAuth);
SecurityContextHolder.getContext().setAuthentication(newAuth);
```

We need to import proper classes:
`import org.springframework.security.core.GrantedAuthority;`
`import org.springframework.security.core.authority.SimpleGrantedAuthority;`
`import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;`

Now, note: If Azure AD also gave a "Admin" app role and we also have an "Admin" in DB, the authority "ROLE_Admin" might be duplicate. That's okay as set, no harm.

This effectively means Spring Security will consider both Azure roles and DB roles for authorization checks.

But one consideration: if a user is _not_ given an "Admin" app role in Azure AD, but we assign them "Admin" in DB, our code will add ROLE_Admin authority. That means they can access endpoints requiring Admin even if Azure AD didn't mark them as admin. This might be intended if we want to manage roles only in our app DB. But if we consider Azure AD as the source of truth for roles, maybe we wouldn't do this override.

However, the requirement likely was to demonstrate storing roles in DB and using them, so yes, this allows the app to have roles independent of Azure AD's app roles.

Alternatively, if we wanted to ensure that only if Azure AD and DB both indicate admin then allow, we would intersection, but that's unusual.

We'll assume the app roles in DB are the effective roles.

So now our flow:

- User logs in -> token might have no roles (assuming we didn't assign Azure app roles).
- DB auto creates user with "User" role.
- Filter attaches ROLE_User authority to their Authentication.
- They can call user-level endpoints.
- If we want to promote someone to Admin, an admin could update DB to add Admin role to that user.
- Next time user makes a request, filter will attach ROLE_Admin to them (even though token didn't have it).
- Thus, in app RBAC, they become admin.

This shows using Azure AD purely for authentication and app DB for authorization.

To test this:

- We should have an Admin role in DB (we added it in initializer).
- We can manually assign a user to Admin role by, say, adding some endpoint to do that or directly in DB. For demonstration, maybe we won't fully implement admin management UI, but we can simulate:
  - E.g., using a repository call in some Admin controller to add role to user by id.

Let's quickly create an admin endpoint to assign role:
(This might not be requested by user, but for completeness to test roles.)
We'll make an endpoint that requires an existing admin to call to grant another user admin (just hypothetical, or use same user).

Actually, to test easily, perhaps after one user is created, we can manually update DB:
Using MySQL CLI:

```
INSERT INTO user_roles(user_id, role_id) VALUES ('<user-oid>', <id_of_Admin_role>);
```

We can get role IDs by `select * from roles;` likely id 1: User, id 2: Admin as inserted by DataInitializer.

Anyway, leaving that aside.

**Update Security Annotations:**
We already put `@PreAuthorize("hasRole('Admin')")` on /admin endpoint. That should now work either if Azure gave role or if our DB provided it via filter.

**Double-check fetch=EAGER:**
We used `fetch=EAGER` for roles in AppUser. That means when we do `userRepo.findById`, it will join fetch or fetch roles, so we have roles to iterate. Should be fine.

**One more thing:** The filter and user creation calls are happening during requests. If multiple requests come concurrently for first time from same new user, it could double-create (though we check if empty and then save, but still possible race). Not a big issue here, but typically one might synchronize or handle unique constraint on DB (id is PK, so second insert would fail gracefully anyway, and then find would find one).

Now integrate filter:
In SecurityConfig:

```
http.addFilterAfter(userProvisioningFilter, BearerTokenAuthenticationFilter.class);
```

We need to add `@Autowired private UserProvisioningFilter userProvisioningFilter;` at top, or use constructor injection in security config (but security config is config class, maybe autowiring filter bean in method possible, easier to field autowire and mark @Autowired).

Given it's a small addition, we'll do field autowire:

```java
@Autowired
private UserProvisioningFilter userProvisioningFilter;
```

Then in securityFilterChain builder, after configuring `http.oauth2ResourceServer()...`, do:

```
http.addFilterAfter(userProvisioningFilter, BearerTokenAuthenticationFilter.class);
```

This should register our filter in chain.

Alright.

## 6.3 Storing and Managing User Roles and Permissions

We have effectively implemented the storing (in DB) and mapping of user roles. To summarize:

- **Storing Users**: Each unique Azure AD user is stored in `users` table (id = Azure AD object id). This can store additional info like email, displayName for reference. We gave every new user a default "User" role.
- **Storing Roles**: Roles are stored in `roles` table. We created "User" and "Admin". We can add more if needed.
- **Assigning Roles**: By default, new users get "User". If an admin wants to assign "Admin" role to someone, they'd update the DB (in a real app, via some admin UI or script).
- **Using Roles in Authorization**: Our Spring Security now checks roles either provided by Azure AD token or attached from DB. So endpoints can be secured with `@PreAuthorize("hasRole('Admin')")` etc., and it will work with our DB roles injection.

**Using Azure AD Groups for roles (Alternate)**:
We did the DB approach. Alternatively, one might simply use Azure AD groups (with group claims or via MS Graph) to manage roles, which we will talk about in Section 7.3. But the DB approach shown here is helpful when application needs its own user management beyond Azure AD.

**User Lifecycle**:
One thing to note is if a user is removed or disabled in Azure AD, our app DB might still have them. Our app would stop seeing them only if they cannot authenticate anymore (Azure AD would not issue tokens). But the DB entry would remain (or we could have some cleanup process, usually not automatic).
If user's email changes, our filter updates it as we coded.
If user's roles in DB need to be updated, an admin (with perhaps an admin UI) can do so.

**Performance consideration**:
Our approach adds a DB hit on each request (to load user and roles). This can be cached if needed. For instance, we could cache user roles in memory for some minutes keyed by user id, to avoid hitting DB every request. Given JWT validation itself is quick (just cryptography), adding a DB query might slow things if traffic is high. But since it's demonstration, it's fine.

Alternatively, one might only load DB roles on first request or if token refresh indicates something. There's complexity in caching because if admin changes roles, might need to propagate.

For now, it's okay.

**Test the integration**:

- Start backend with MySQL running. Ensure tables are created.
- Watch console for DataInitializer adding roles.
- Use the React app to login as a user. First call to /hello triggers filter:
  - Check DB, user not found, should print "Provisioned new user..."
  - Now user is in DB.
  - Check DB tables: user row inserted with id (guid), email etc; also user_roles linking to role "User".
  - /hello returns greeting.
- Now to test /admin:
  - That user isn't admin yet, so calling /admin should return 403 Forbidden (Spring Security should block because hasRole('Admin') fails).
  - If you want to test success, either:
    a) In Azure AD, assign that user the "Admin" app role (if we had created an app role and token contains it). If token then has roles claim Admin, they'd have authority via JWT as well. But we didn't explicitly assign in Azure.
    b) Or simulate giving them Admin in DB: update user_roles table for that user to also have role_id of Admin role. Then call /admin again (with same token). Our filter on each request will fetch roles and now add ROLE_Admin authority. Now the PreAuthorize should pass and "Secret admin data" is returned.
  - Let's do (b): e.g., run `INSERT INTO user_roles(user_id, role_id) VALUES ('<user-oid>', 2);` if 2 is Admin's id.
  - Then in React, clicking a button to call /admin (if we make one or use Postman with token) should now succeed. The token hasn't changed, but our filter sees DB role.
  - Alternatively, stop and restart the app to get new token? Actually not needed because we didn't even have Azure roles.

So we see the power (and potential pitfalls) of decoupling authN and authZ: our app can give privileges independent of Azure AD's notion.

Now, we have covered integrating MySQL for storing users and roles, and using them in the security context.

Next, we'll discuss some advanced auth features like SSO and multi-tenant, which don't require a ton of coding beyond config but important to mention.

---

# 7. Advanced Authentication Features

Having implemented the core authentication and authorization, let's explore some advanced features and scenarios that are often relevant in enterprise applications using Azure AD:

## 7.1 Implementing Single Sign-On (SSO)

**Single Sign-On** means a user can sign in once and gain access to multiple applications without re-entering credentials. In our context:

- Because our React app uses Azure AD, if the user has already authenticated with Azure AD in their browser (for example, logged into Office 365 or another app using the same Azure AD tenant), the MSAL login flow can silently authenticate them. Azure AD sees an existing session cookie and won't prompt for password again. The result: from the user perspective, they might click "Login" in our app and get signed in immediately without a credential prompt (or if using `loginRedirect`, it may flash and return).
- Similarly, if we had multiple frontends (say a separate admin portal and a main app) on the same Azure AD, once the user logs into one, they can be signed into the other without another full login.

Our implementation already supports SSO to the extent Azure AD allows:

- MSAL by default will attempt to use any existing Azure AD session. If none, it will prompt.
- If you wanted to silently login without any user action, MSAL offers `ssoSilent` or you can call `acquireTokenSilent` with only the `openid` scope when your app loads, but that might require a known login hint or a previously cached account. In practice, simply initiating `loginRedirect` or `loginPopup` will utilize SSO under the hood.

**Cross-application SSO:** If you have two SPAs registered in Azure AD (with different client IDs), Azure AD can still give SSO if they are in the same tenant and the user is already logged in. They will likely just see a prompt "Application would like to sign you in" and then instantly proceed without password (since session exists). If both apps use the same **redirect domain** and are under one Azure AD app with multiple redirect URIs, you could even share MSAL cache if on same domain.

**Single Sign-Out:** Logging out of our app (via `logoutRedirect`) will:

- Clear the MSAL cache for our app (so our app forgets the user).
- Redirect to Azure AD's logout endpoint which clears the Azure AD session cookie and then returns to our specified post-logout URL.
- If the user was logged into multiple apps via Azure AD, clearing the Azure AD session cookie means those other apps _will_ require login next time they try to acquire a token. However, those apps won't automatically know the user logged out. They might still consider the user logged in until their token expires or a check fails. There is a concept of front-channel or back-channel logout notifications for OpenID Connect, but Azure AD in pure SPA scenario doesn't push a logout event to the SPAs (since no server session to notify).
- In our design (stateless SPA), after logout, if the user goes to another app using Azure AD, that app will redirect to login and since the session is gone, the user must log in again (which is what we want for single sign-out).

So effectively, Azure AD gives us single sign-on and single sign-out across any apps using the same Azure AD. As developers, we don't need extra code to handle SSO beyond properly configuring MSAL and Azure AD (which we did).

One tip: If multiple apps use different tenants or you want SSO with personal Microsoft accounts, you might use the `common` or `organizations` authority. But using a specific tenant (tenantId) provides SSO for that tenant’s accounts which is typical for an org.

## 7.2 Multi-Tenancy with Azure AD

**Multi-tenancy** in Azure AD context means allowing users from other Azure AD tenants (directories) to access your application. By default, our app registrations were single-tenant (only our org). To make it multi-tenant:

- In Azure AD app registration, set "Accounts in any organizational directory" as supported account types.
- This changes the issuer behavior: tokens from other tenants will have their own tenant ID in `iss` and `tid` claims.

Considerations:

- **Authority**: In MSAL, if we still use a specific tenantId in the authority URL, that will restrict logins to that tenant. For multi-tenant, we would use `https://login.microsoftonline.com/organizations` (only Azure AD work/school accounts) or `common` (Azure AD + Microsoft personal accounts if we allowed those). Using `organizations` is common for multi-tenant enterprise apps.
  - Alternatively, we could dynamically set authority based on user input (like if we know their tenant). But usually `common` or `organizations` covers it.
- **Token Validation on Backend**: Our backend is currently expecting a specific issuer (our tenant). If we allow multi-tenant, we have two choices:
  1.  **Validate tokens from any Azure AD tenant** (any issuer that matches the pattern `https://login.microsoftonline.com/{tenantId}/v2.0`). We might skip strict issuer check and only verify signature (the keys used by all Azure AD tenants share a common endpoint as well, but keys are tenant-specific in v2? Actually, the JWKS endpoint includes tenant in URL, but the keys themselves might be signed by common MSFT authority). This is tricky because we want to ensure the token is for our app but could be from any tenant.
  2.  Validate issuer dynamically: Spring Security `issuer-uri` property is static. To allow any, one approach is to not set issuer-uri but instead use a custom `JwtIssuerAuthenticationManagerResolver` that picks an issuer validator based on the token's `iss`. Spring Security provides this class which can handle multi-tenant scenarios by caching issuers.
  3.  Alternatively, register our API as multi-tenant and have one specific issuer? Actually in multi-tenant, the `iss` will vary per tenant, so no single static issuer will work.

Simpler approach:

- Accept all Azure AD issuers and check the audience. But that might inadvertently allow any Azure AD tenant to sign tokens for your client ID (which is actually possible if admin of another tenant consents your multi-tenant app). That is intended for multi-tenant apps. So yes, if other tenant's admin consents, their users can get tokens for your app, with `aud = your-client-id` and `iss = that-other-tenant`.
- So on backend, we should verify:
  - The token is issued by Azure AD (we can ensure the `iss` ends with `/v2.0` and domain login.microsoftonline).
  - The `aud` is our client ID (so it's for our app).
  - Optionally, that the token has an appid or azp claim equal to our client ID (for some flows, Azure includes `azp` = authorized party).
  - The signature is valid (via known Azure AD keys - which might require using the common JWKS or retrieving per tenant).

Spring's `AzureADJwtBearerTokenAuthenticationConverter` (from Azure Spring libs) might handle multi-tenant, but let's not dive there.

Given advanced dev audience, they might manage multi-tenant by configuring the **Spring Cloud Azure Starter** which simplifies multi-tenant, or do manual.

Due to complexity, we'll just highlight:

- To support multi-tenant, set app as multi-tenant in Azure (which we do in Azure portal).
- In MSAL, use `authority = https://login.microsoftonline.com/organizations` so that any org tenant user can login.
- On backend, one option: set `issuer-uri = https://login.microsoftonline.com/common/v2.0` (common endpoint's issuer). But actually tokens from common have issuer specific to tenant, not "common".
  Actually, Azure AD multi-tenant tokens will have issuer `https://login.microsoftonline.com/{tenantId}/v2.0`. You can't validate all with one static issuer.
- Instead, use Spring Security's `JwtAuthenticationProvider` and supply a custom `JwtDecoderProvider` that looks up issuer from token. Spring documentation suggests using `NimbusJwtDecoder.withJwkSetUri(jwkSetUri)` and a `JwtClaimValidator` for audience. But multi-tenant would need to adjust jwkSetUri per token.
- There's a known pattern: if multi-tenant, you might ignore issuer validation or implement a custom validator that checks that `issuer` claim matches `https://login.microsoftonline.com/{tid}/v2.0` for some tid that matches token's `tid`. Essentially ensure tid in token matches iss in token (which Azure does anyway).
- For brevity, one could skip validating iss if they trust signature from Microsoft and audience. This is a slight risk but maybe acceptable if you trust MS to not mint cross-tenant tokens incorrectly.

We'll note: _For multi-tenant, additional backend configuration is needed to validate tokens from any tenant, often by implementing a custom validator or using the Spring Cloud Azure starters._ ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=Role%20claims%20aren%27t%20present%20for,used%20as%20the%20authority%20to))

In summary, enabling multi-tenancy broadens your user base but requires careful validation to not inadvertently allow tokens from unauthorized sources. In a multi-tenant app, you might also maintain a list of tenant IDs that have onboarded or are allowed. You could check `tid` in token against allowed tenants list in your DB, for example, to restrict who can use the app.

## 7.3 Using Azure AD Groups for Role Management

Azure AD **Security Groups** can be used to manage authorization as well:

- You can assign users to groups in Azure AD (e.g., a group "MyAppAdmins").
- You can configure the app registration to include group memberships in the token. In Azure AD portal: App Registration -> Token Configuration -> Add Groups Claim. Options:
  - All groups (security groups user is a member of) – not recommended if user is in many groups.
  - Groups assigned to the application – more efficient, only groups that were explicitly set in Enterprise App blade for this app or in App roles assignment.
  - Or Directory roles (not needed for us).
- If enabled, the token will have a `groups` claim listing group object IDs (GUIDs). If the user is in more than 150 groups, instead a `hasgroups: true` claim is present, and you must query Microsoft Graph to get group memberships ([Secure Java Spring Boot apps using groups and group claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-group-entra-id#:~:text=token%20%20from%20Microsoft%20Entra,ID)).
- To make use of group IDs, your app would need to map those GUIDs to meaningful roles. Typically you'd maintain a mapping of Azure AD Group Object ID -> Role in the app config or DB.

Another approach: **App Roles with Groups**:

- Azure AD App Roles (which we touched on in Section 3.1) can be assigned not just to users but to groups ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=,the%20Regular%20Users%20page)). For example, create an app role "Admin", then in the Enterprise Applications -> [Your App] -> Assign Users and Groups, assign the Azure AD group "MyAppAdmins" to the "Admin" app role.
- When a user in that group signs in, the token's `roles` claim will include "Admin" (the app role) ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=These%20application%20roles%20are%20defined,the%20form%20of%20role%20membership)). This way, group membership is translated to roles in the token directly. This is a powerful method because it avoids exposing raw group IDs to the app and leverages Azure AD's role claim.
- We could use that method and then our Spring Boot would natively get "Admin" in roles claim and map to ROLE_Admin (which we configured).

If using raw group claims:

- We would need to fetch group details. We might preconfigure known group IDs in our app: e.g., treat group with objectId X as Admins. Then in the filter or converter, if jwt.groups contains X, add ROLE_Admin authority.
- This is possible to implement by checking claims in our `jwtAuthenticationConverter` or filter. We could maintain a list in config or DB of admin group IDs.

However, app roles are simpler for RBAC. Many enterprise setups use app roles or group->app role assignment.

**In our guide context**:
We already covered using DB roles. If an organization wanted to manage everything in Azure AD, they'd likely:

- Not use DB roles at all (except possibly to store user records for other info).
- Instead rely on roles claim from Azure AD or parse group claims.

We can mention that as an alternative:
"For enterprise scenarios, you might use Azure AD groups or app roles to manage roles:
If Azure AD includes a `roles` claim in JWT (like "Admin"), our SecurityConfig mapping of roles claim will automatically apply ([Secure Java Spring Boot apps using roles and role claims - Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/identity/enable-spring-boot-webapp-authorization-role-entra-id#:~:text=These%20application%20roles%20are%20defined,the%20form%20of%20role%20membership)). No additional DB needed to enforce role-based access – Azure AD is the source of truth and admins can assign roles via Azure AD UI.
If using group claims, one can map them to roles in code or via Azure AD App roles assignments to groups, as described above."

One advantage of Azure AD roles/groups: central management and the token carries the info so backend doesn't query DB for roles. But sometimes you need app-specific logic or data as we showed.

In summary, our app could support Azure AD groups in addition to DB roles:

- E.g., if `jwt.getClaim("groups")` contains a known admin group id, we add ROLE_Admin as well in converter. This is similar to what we did with DB. We could even combine: an Azure AD group assignment could result in adding the user to DB role maybe.

We won't implement further in code since we did DB roles. We'll just note it.

## 7.4 Handling Refresh Tokens and Session Management

As mentioned, MSAL handles refresh tokens for the SPA. On the backend, since we accept JWTs, there's no concept of refresh token; the frontend just sends a new JWT when it gets one.

**Session Management**:

- Our backend is stateless (we disabled session creation). Each request is authenticated via token. This scales well and means we don't have server-side session state to manage or expire.
- If you wanted to, you could use stateful sessions (e.g., if using Spring Security differently), but that complicates a distributed system. We stick to stateless.

**Token Lifetimes**:

- Access tokens: Azure AD v2 default is around 1 hour for access tokens. Refresh tokens can last longer (with sliding window).
- If a user stays on the app for a long time, MSAL will seamlessly use the refresh token to get new access tokens. If the refresh token expires (after e.g. 24h of inactivity or 90 days absolute), MSAL will require login again (InteractionRequired).
- It's good to handle that gracefully (maybe prompt user "session expired, please login").

**Revoke and sign-out**:

- If an admin revokes a user's session in Azure AD (e.g., via Azure AD "Revoke sessions" or disabling account), the refresh token becomes invalid. The access token might still be valid until expiry, but once MSAL tries to refresh or user tries logging in, it will fail.
- We might want to force re-auth after certain time or on critical actions require a fresh token with re-auth (like step-up auth or conditional access requiring MFA).
- Azure AD Conditional Access can enforce MFA or device compliance, which is mostly handled by Azure AD at login time. Our app might just get a claim (like `acr` or `amr`) indicating MFA was done, if needed.

**Storing tokens securely**:

- We stored in sessionStorage. That's reasonably secure for a SPA (not accessible by other domains, and not persisted to disk beyond tab session).
- We avoided cookies for tokens because that can introduce CSRF issues and also because CORS would complicate sending cookies.
- If using cookies (like if we had a scenario to store token in a secure cookie and then the backend uses it), then we must implement anti-CSRF tokens to avoid cross-site requests using that cookie.
- Since we didn't, no need for CSRF protection (we disabled it).

**Parallel sessions**:

- If user opens two tabs of our app, each has its own sessionStorage. So they might each go through login (though one might reuse SSO so second tab logs in quickly).
- They will each have separate MSAL caches. Logging out in one tab won't automatically log out the other (unless Azure AD's session is cleared, then other tab's next request to get token might fail).
- This is acceptable, though there are ways to sync logout across tabs by listening to storage events if using localStorage.

**Multi-factor & Conditional Access**:

- If enabled, Azure AD will handle it during login. MSAL just shows the Azure AD web flow, which might prompt for MFA or any other step. Our app doesn't need changes except to be aware that login might require those steps.

**Sessions in MySQL**:

- If we needed to track user sessions or logins, we could store an entry when user logs in. But since we don't have a login event server-side (it's all token based), we might not do that. We could use the DB to log user last seen or track active sessions by storing refresh token (not advisable in SPA).
- Instead, rely on Azure AD sign-in logs for auditing logins.

We've covered advanced considerations now. The main heavy-lifting coding was in earlier sections.

---

# 8. Testing and Debugging

Thorough testing and effective debugging are crucial when dealing with authentication, as misconfiguration can lead to elusive errors. Let's outline strategies for testing and diagnosing issues:

## 8.1 Debugging Authentication Issues

Common issues that might arise and how to debug them:

- **Misconfigured Redirect URI**: If the redirect URI in Azure AD app registration does not exactly match the one used by MSAL, login will fail. The user might see an error like "redirect_uri_mismatch" after authentication. To debug:

  - Check the URL in the browser's address bar when the error occurs, Azure AD often includes an error description.
  - Ensure the `redirectUri` in `msalConfig` matches an entry in Azure portal (including scheme, host, port, path).
  - Remember that `http://localhost` is allowed for dev, but in production it must be HTTPS.

- **Invalid Authority or Tenant**: If the authority is wrong (e.g., wrong tenant ID or using common when not allowed):

  - MSAL might throw errors during login attempts. Check console logs (we enabled MSAL logging at Info level).
  - Azure AD might show an error page if tenant is not found or user not in tenant.
  - Verify the `authority` URL is correct (should contain the correct tenant ID or 'common/organizations' if multi-tenant).

- **Consent and Permission Issues**: If you didn't grant admin consent for the API scopes:

  - The first user login will show a permission consent prompt. If the user is not an admin and the scope requires admin consent, login will fail with an error and Azure AD saying admin consent is required.
  - Solution: As an admin, grant the required permissions in Azure AD for the SPA app (we did this in API Permissions).
  - You can also allow user consent for lower-privilege scopes if appropriate.

- **CORS errors**: If the React app calls the API and you see errors in the browser console like _"Access-Control-Allow-Origin missing"_ or a blocked request:
  - That means the backend didn't allow the origin. Check that your Spring Boot CORS config is correct (allowedOrigins matches exactly `http://localhost:3000` during dev).
  - Look at the network trace: the preflight (OPTIONS) request should get a 200 with CORS headers. If not, adjust config or use `@CrossOrigin` on controllers for quick test.
  - Ensure the endpoint path matches what you configured for CORS (we did `/api/**`).
- **401 Unauthorized from API**: If the React app provides a token but the API returns 401:

  - Possible causes: token missing or malformed, token signed by unknown issuer, token audience mismatch.
  - Check the Authorization header is being sent correctly. In browser dev tools, inspect the network request headers for `Authorization: Bearer ...`.
  - If it's missing, perhaps the token acquisition failed silently. Check MSAL logs or ensure `acquireTokenSilent` succeeded.
  - If token is present, check Spring Boot logs. With `logging.level.org.springframework.security=DEBUG` in application.properties, Spring will log details about JWT validation. It may log why a token was rejected. Common message: "JWT Verification failed: audience invalid".
  - Audience invalid means the `aud` claim in JWT didn't match our expected client ID. Use a JWT decoder (e.g., [jwt.ms](https://jwt.ms)) to decode the token (it's just base64 strings). Look at the `aud` and `iss` claims.
    - If `aud` is something like a different GUID, maybe you requested wrong scope. For instance, if MSAL used a clientId scope instead of the API scope, the token might be intended for Microsoft Graph or itself. Make sure `loginRequest.scopes` is our API's scope URI.
    - Or maybe on backend, our `spring.security.oauth2.resourceserver.jwt.audience` doesn't match exactly. If you set audience to client ID, but Azure uses the Api URI as audience in token, that could fail. Try removing the audience property (then Spring will only check issuer and signature, not audience) – not ideal for security, but for debug to see if that's the issue.
    - Ideally, ensure Azure AD is issuing token with `aud = <API-client-id>`. In our case, since we created a custom scope on the API, Azure should issue aud as the API's App ID URI or clientId (actually in v2, aud is the resource app's clientId).
  - If issuer invalid: ensure tenant ID matches. If you set single-tenant, token's `tid` should be that. If user from different tenant tries, it'll fail (by design, or you implement multi-tenant as above).

- **403 Forbidden**: This indicates the token was accepted (valid authentication) but the user is not authorized for the resource:

  - In our app, that happens if `@PreAuthorize` or antMatchers require a role the user doesn't have.
  - Example: calling `/admin` with a normal user token yields 403. The backend logs might show something like "Access Denied: ... lacks role ADMIN".
  - The fix is to assign the proper role either in Azure AD or DB as needed, or adjust the security rules.
  - If you expected the user to have that role, verify the claims. Did Azure AD include "roles": ["Admin"]? If not, perhaps you forgot to assign the user the app role in Azure AD Enterprise App.
  - With our DB approach, check the `user_roles` table for that user.

- **MSAL Specific Errors**:

  - InteractionRequiredAuthError: This is thrown when a silent token request fails because user interaction is needed (e.g., no refresh token, or conditional access like MFA). Our code catches this and does acquireTokenPopup, but if not handled, the app would stall. If you see this in console, ensure our logic to handle it is executed. Or call login again.
  - Error: `The provided value for the input parameter 'response_type' isn't allowed for this client. Expected value is 'code'.` – This occurs if you request an ID token but the app isn't configured for implicit flow. We avoided implicit. If it appears, might mean somehow an implicit flow was triggered but not enabled. Ensuring we're using `loginRedirect` with code and that ID token checkbox in Azure AD is enabled (for implicit/hybrid, but for code flow it's not needed).
  - Slow response or timeouts: sometimes if network issues to Azure AD, MSAL might hang. It's rare, but you can add timeouts or check network connectivity.

- **Logging**:

  - We enabled MSAL logging (it will output to console for levels Info and up). This helps track the login progress, token cache events, etc. In production, you might lower that to warn or error.
  - On backend, enable Spring Security debug logs as mentioned to see each step of filter chain decisions.

- **Tools**:
  - [jwt.ms](https://jwt.ms) is extremely helpful. You can copy a JWT (ID or access token) and paste there to see contents. It is by Microsoft and will show claims and whether signature is valid (if it's an ID token or if it can fetch appropriate metadata).
  - Postman: as we'll see, can simulate calls with tokens.
  - Browser network tab: to see if requests are going out and what comes back (especially looking at 302 redirects during login, or XHR to API).
  - Azure AD Sign-in logs: in Azure Portal > Azure AD > Sign-ins, you can see each login attempt, whether it was successful, what application ID, and if any conditional access applied. This is useful to diagnose if Azure AD is blocking something or if user failed MFA, etc.

## 8.2 Testing API Security with Postman

**Postman** is a great way to test your API in isolation from the frontend, including with OAuth2 tokens:

To test a protected endpoint:

1. **Obtain an Access Token**:
   - Option A: Use MSAL in the app to get a token, then manually copy it. For example, after logging in via the app, open developer console and inspect the token from `instance.acquireTokenSilent` result or from sessionStorage. Or modify the app to display the token.
   - Option B: Use Postman's built-in OAuth2 flow:
     - In Postman, create a new Request for, say, GET `http://localhost:8080/api/hello`.
     - Go to the Authorization tab, choose "OAuth 2.0" as type.
     - Click "Get New Access Token".
     - Fill details:
       - Token Name: (anything, e.g., "MyAppToken").
       - Grant Type: "Authorization Code" (with PKCE since SPA has no client secret).
       - Callback URL: `http://localhost:3000` or better, Postman provides its own callback like `https://oauth.pstmn.io/v1/callback`. Add that URL to your SPA app's Redirect URIs in Azure AD temporarily (Postman can capture the token via that).
       - Auth URL: `https://login.microsoftonline.com/<tenantID>/oauth2/v2.0/authorize`
       - Access Token URL: `https://login.microsoftonline.com/<tenantID>/oauth2/v2.0/token`
       - Client ID: your SPA client ID.
       - Client Secret: (blank, since it's public client).
       - Scope: `api://<API-Client-ID>/API.Access offline_access openid profile`
         - Explanation: include your API scope, and possibly `offline_access` (so that Postman can get a refresh token if needed), and openid profile to get ID token (not strictly needed).
       - PKCE: enable "Authorize using browser" which will handle PKCE automatically. Postman will launch a browser to login.
     - Click "Get New Access Token". It should open a browser, let you log in to Azure AD, then redirect to Postman callback and close.
     - Postman then shows a token details dialog. If successful, you can hit "Use Token".
   - If using Postman's callback, ensure to add it to the Azure AD app or it won't redirect properly.
   - Option C: Use Azure CLI or a curl script with client credentials (only possible if you made a confidential client and gave it delegated permission - not applicable here, or if API accepted client credentials tokens which it currently doesn't since we require user roles).
   - Option D: Use the Azure AD "Test" feature in App registration (for delegated token, it often requires a user login anyway).
2. Once you have the token (via copy or Postman retrieval), attach it:
   - In Postman Authorization tab, choose Bearer Token and paste the JWT as value. Or if you did the OAuth2 flow in Postman, it will handle putting "Bearer <token>" in the header if you selected "Use Token".
3. Send the request.
   - For `/api/hello`, you should get the hello message (with principal name likely a GUID or email).
   - For `/api/admin`, try with a user that is admin. If not, you'll get 403 (which is correct if not admin).
   - You can test error scenarios: e.g., remove one character from token to corrupt it and see that you get 401.
   - You can also test token expiration by manually tweaking `exp` in the token (though signature won't match if you do, so not straightforward).
   - To test multi-tenant or other accounts, you could log in with another Azure AD account if app is multi-tenant (ensuring consent etc).
   - Using Postman helps ensure the backend is correctly configured independent of the frontend.

**Testing refresh tokens**:

- Since our front-end uses MSAL, it's hard to manually test refresh except by waiting an hour and see if app still can call API (it should).
- You can shorten token lifetime in Azure AD (through preview features) to test, but it's not critical for functionality, MSAL covers it.

**Testing logout**:

- After logging out via app, test that using the old access token no longer works for new requests (should already not if expired; if not expired the token is technically still valid until exp, since logout doesn't revoke it immediately - unless you have conditional revocation).
- For strictness, Azure AD provides something called **access token revocation** on logout for some flows, but not guaranteed for all. Generally, you consider tokens valid until expiry.

**Automated testing**:

- For backend, you could write unit/integration tests using MockMvc and mocking authentication, or using an actual JWT. For example, you can create a JWT signed by your own test issuer and configure the resource server to accept that for test profile.
- Or use WireMock to simulate Azure AD endpoints for testing the filter logic.
- Given complexity, many will test manually or with end-to-end tests.

## 8.3 Logging and Monitoring Authentication Events

**Logging**:

- We added some console logs (e.g., "Provisioned new user..."). In a real app, you'd use a logging framework (slf4j) to log important security events at INFO or WARN level.
- E.g., log login attempts, new user registrations, access denied events. Spring Security can log an access denied event; you can also implement an `AccessDeniedHandler` to log and return custom message.
- Keep sensitive data out of logs (e.g., do not log tokens or passwords). A token could be somewhat sensitive if logged, although it's short-lived. We avoided logging the token itself.

- The `SecurityContextHolder` can be inspected if needed in a filter to log user id and request path for auditing.

**Monitoring**:

- On Azure AD side, use Azure AD Sign-in logs to monitor who logged in, from where, and if any failures.
- Azure AD also emits audit logs for app registrations changes, consent grants, etc.

- For the application, consider integrating Application Insights or another monitoring tool to track requests and exceptions. This can be useful to see if a lot of 401/403s happen (maybe an indicator of an attack or misconfiguration).
- Also, monitor performance: check if token validation or DB lookups are causing latency.

**Post-production best practices**:

- Turn off overly verbose logging in production (e.g., MSAL logs or Spring Security debug) as they can be verbose and possibly expose info. Use INFO level for important messages only.
- Ensure any secrets (like client secret, DB passwords) are not in logs. We didn't put secret in our app, but if you had to (like for Graph API calls from backend), keep them secure.

**Penetration testing**:

- It's wise to have a security test where someone tries to bypass auth:
  - Try calling API without token (should get 401).
  - Try calling with an expired token (should get 401).
  - Try calling with a token for another app (should get 403 if aud is wrong or at least not succeed).
  - Try calling an admin endpoint with a normal user token (should get 403).
  - Ensure things like SQL injection or other web vulnerabilities are mitigated (less related to auth but overall).
  - Ensure no sensitive data in error responses (Spring Boot might by default show a lot for errors if not handled; we might want to disable stacktrace in error for security).

At this stage, we should have a fully functioning authentication system. We will consider deployment next.

---

# 9. Deployment Considerations

Deploying our React + Spring Boot + MySQL application to production (especially on Azure cloud) requires additional planning. We want to maintain security and performance in the deployed environment.

## 9.1 Deploying React and Spring Boot Applications to Azure

**Frontend (React) Deployment**:

- We can treat the React app as a static website once built (using `npm run build`). The output is static HTML, CSS, JS.
- **Azure App Service (Static site)**: Easiest route is to use [Azure Static Web Apps](https://docs.microsoft.com/azure/static-web-apps/) if the frontend is static and maybe the backend is separate (though Static Web Apps often assumes a serverless backend). But we can just deploy the static files to a storage account or App Service.
- **Azure Storage Static Website**: We can upload the `build/` directory to an Azure Storage account configured for static website hosting. This provides a URL for the content. We would probably use a custom domain or an Azure Front Door/CDN in front for production.
- **Azure App Service (Web App)**: Alternatively, host the static site in an App Service container. You could create an App Service for the frontend, use a runtime that can serve static files (Node runtime can serve it with a simple server, or use an Azure feature to serve static content directly).

  - There's an App Service setting for static content, or we could include a simple Node/Express to serve files.
  - Since no server logic is needed for the frontend, using a simpler static host is recommended for cost and simplicity.

- If using App Service for both front and back, you might want them under the same domain or subdomains for simplicity in CORS. But separate is fine too, just configure CORS properly.

- **Environment variables**: If any config (like API base URL) is needed in React, you might set it via environment at build time (React picks from REACT*APP*\* env vars during build). In our case, the API URL is hardcoded to localhost:8080 which in production would change (maybe to an actual domain). We should make that configurable.

**Backend (Spring Boot) Deployment**:

- Azure offers multiple options:

  - **Azure App Service for Linux (Jar deployment)**: You can deploy the Spring Boot JAR directly to Azure App Service. Azure App Service can host Java apps; you specify Java version and upload the jar (via FTP, or use the Maven plugin "azure-webapp-maven-plugin" to deploy).
  - **Azure App Service (Containers)**: Package the app into a Docker container, push to Azure Container Registry, and use Web App for Containers to run it.
  - **Azure Spring Apps (formerly Azure Spring Cloud)**: A managed service for Spring Boot apps. You can deploy the jar to Azure Spring Apps and it manages infrastructure (but it's a premium service).
  - **Virtual Machines or AKS**: Less PaaS, more control, but more management overhead. Usually not needed for simpler cases.

- If using App Service:

  - Create an App Service instance (Linux, Java 17, maybe Tomcat if war or just use "JAR" deployment).
  - Use Azure Database for MySQL (fully managed MySQL) for the database. You can provision an Azure Database for MySQL server, create the same schema and user. Then update your Spring Boot config to point to that DB (update `spring.datasource.url`, username, password). Use SSL for DB connection as required by Azure (often by adding `?sslMode=REQUIRED` or similar in JDBC URL).
  - Ensure to set environment variables in App Service for any sensitive config: e.g., put the DB password, perhaps the Azure AD config (tenant ID, client ID if needed). In our app, tenant and client IDs are in application.properties which is okay as they are not secret. But DB password definitely must be provided securely (App Service settings are secure and not in code).
  - If you had a client secret (for backend to call Graph etc.), that should also be in env or Azure Key Vault, not in code.

- **CORS in production**:

  - If front-end is at `https://myapp.com` and backend at `https://api.myapp.com`, update allowedOrigins in CORS config accordingly. Or consider using the same domain and perhaps path for API to avoid CORS altogether (e.g., serve UI from `myapp.com` and API at `myapp.com/api`).
  - If on separate subdomains, configure CORS, and ensure both use HTTPS.

- **Domain and HTTPS**:

  - Azure provides default \*.azurewebsites.net domains. For production, you'd likely use a custom domain (like yourcompany.com). Azure App Service and Static Web Apps allow custom domains and you can upload certificates or use Azure-managed free certificates.
  - Azure Static Web Apps come with a front door and certificate setup out of the box for custom domains.
  - Make sure redirect URIs in Azure AD are updated to use the production domain (and HTTPS). Add those before deployment. E.g., `https://app.mycompany.com` for SPA, and if your backend might ever do OAuth flows (not in our case), add those too if needed.
  - Also update MSAL config in React to use `authority` with your tenant still, and redirectUri to production URL.

- **Azure AD app registration**:
  - If you used a dev environment (maybe a dev tenant or dev app registration), consider using separate app registrations for prod (so you can have separate client IDs, redirect URIs, etc., and not interfere with testing). Or carefully modify the existing one for prod and hope dev still works with localhost (which it can).
  - Often, companies have separate Azure AD tenants for dev/test, or at least separate app registrations in same tenant for dev vs prod (to avoid messing with consents).
  - Decide that based on need. If separate, you'll have to configure environment-specific MSAL settings (like client ID, etc., in some config file or env var).
- **Key Vault**:

  - For managing secrets (DB password, any API keys, etc.), consider using Azure Key Vault. App Service can integrate with Key Vault to fetch secrets as environment variables. It's more secure than storing directly in config or even App Service settings.
  - At minimum, use App Service settings (they are encrypted at rest and not visible to code except as env var).

- **CI/CD**:

  - Use GitHub Actions or Azure DevOps pipelines to automate building and deploying:
    - Build React app, publish artifacts (the static files).
    - Build Spring Boot (run tests, package jar).
    - Deploy React files to chosen hosting (maybe attach to a branch trigger if using Static Web Apps, which has its own Action).
    - Deploy Spring Boot jar to App Service (there is an official Azure WebApp action).
    - Or build Docker image and push to ACR, then deploy to Web App for Containers.
  - Ensure pipeline does not log sensitive info. Use secret variables for passwords, etc.
  - Also ensure to run tests in pipeline (unit tests for backend, maybe a headless build for front).

- **Scaling**:

  - Both App Service and Static Web Apps support scaling. Our architecture is stateless (React is static, backend is stateless JWT auth, DB is external), so scaling horizontally is easy:
    - App Service can scale out to multiple instances and since no session affinity is needed, any instance can handle any request (just ensure they all have same config and connect to same DB).
    - Azure Database for MySQL can scale up for performance, but scaling out MySQL is more complex (read replicas possible, but writes scale vertically).
  - Use Azure Monitor or App Insights to watch for load and configure autoscale if needed (based on CPU, memory, etc.).

- **Security best practices in deployment**:
  - Use HTTPS only. App Service by default has HTTPS endpoints; enforce HTTPS by redirecting HTTP to HTTPS (there's a setting).
  - Consider using Azure Front Door or Application Gateway if you want WAF (web application firewall) features in front of your app for extra protection.
  - Keep your OS and runtime updated (Azure handles most for PaaS).
  - Set up monitoring alerts for anomalies (e.g., sudden spike in 500 errors might indicate an issue).
  - Back up your database (Azure DB for MySQL can have automated backups).

## 9.2 Setting up CI/CD Pipelines for Automated Deployment

As touched above:

- Use GitHub Actions: For example, a workflow that triggers on push to main or on release:

  - Jobs to build frontend: `npm ci && npm run build`. Then `azure/static-web-apps-deploy` action or an Azure CLI action to upload to storage.
  - Jobs to build backend: `mvn clean package`. Then use `azure/webapps-deploy@v2` action for the jar (specify the Azure publish profile or credentials).
  - Or if using containers, build and use `azure/webapps-deploy` with images or Azure CLI to update.

- Use Azure DevOps: Similar pipeline with tasks for npm and Maven, then Azure CLI or Azure App Service deploy tasks.

- Ensure to store Azure credentials (like service principal for Azure CLI or publish profile) in pipeline secrets.
- Also store any secrets like DB connection strings or environment config in pipeline or feed them into the app after deploy (like setting App Settings via Azure CLI in pipeline, so that the app picks them up on restart).

- Automating Azure AD steps is more complex (often manual). But you can script some Azure AD with Azure CLI or PowerShell (like `az ad app update` to add redirect URIs if needed).

- After deployment, run some smoke tests:

  - Possibly a simple script to hit the health endpoint or the homepage to see if it loads.
  - (We might add a `/public/health` unauthenticated endpoint in backend to return "OK" for such checks.)

- Include the test stage in pipeline where possible (maybe run backend unit tests, and maybe a Selenium or Cypress test for the whole login flow in a staging environment if sophisticated).

## 9.3 Security Best Practices for Production

Some additional best practices to finalize:

- **Use App Config/Key Vault**: Never leave secrets (DB password, client secrets) in source control. We followed that (none in code).
- **Limit Client Secret usage**: Our app didn't need a client secret for normal operation. If you did have one (say backend to call Graph or for some daemon), consider using **Managed Identity** if the app is on Azure (Azure AD can give the App Service a managed identity and you can assign API permissions to that identity instead of storing a secret).
- **HTTPS and Certificates**: Always serve both frontend and backend over HTTPS. Use HSTS header on frontend to enforce subsequent HTTPS. Azure Front Door or App Gateway can help enforce TLS.
- **Content Security Policy (CSP)**: On the frontend, consider adding a CSP meta-tag or header to restrict sources of scripts. This can mitigate XSS by not allowing injected scripts to load from untrusted origins. MSAL loads login in an iframe or popup from Microsoft, so ensure \*.login.microsoftonline.com is allowed for frames if using popup (and for redirect, it's top-level so not a CSP issue).
- **XSS/Injection**: Continue to code carefully to avoid introducing XSS in React (e.g., avoid `dangerouslySetInnerHTML` unless needed, validate any user input displayed). Our backend, using JPA with prepared statements, is safe from SQL injection for those queries (don't use string concatenation for queries).
- **API Security**: We already secure all endpoints. If any endpoint should be public, mark it permitAll explicitly. Everything else should require auth (we did anyRequest().authenticated).
- **Dos Protection**: Azure AD has its own DDoS protection for the auth endpoints. For our API, Azure App Service can handle a lot, but consider scaling or using a WAF for large-scale DDoS. Also perhaps implement rate limiting on sensitive endpoints if needed (e.g., if you had a login endpoint, but we delegate to Azure AD which has its own).
- **Logging Sensitive Info**: Ensure no personal data or secrets are logged inadvertently. E.g., our logs might include user email in "Provisioned new user..." message. That's probably okay at INFO, but consider privacy rules (in some jurisdictions, even an email might be considered personal data - decide based on policies).
- **Compliance**: If necessary, ensure to comply with regulations (GDPR etc.) for storing user data. For example, if an employee leaves, and they were in our DB, do we need to purge their data from DB if requested? Possibly, so have an admin function to remove a user (and maybe their data).
- **Testing in Production**: After deployment, test again with a real scenario on production domain. The OAuth flow might have differences (like needing to allow pop-ups if using popup - instruct users accordingly).
- **User Experience**: For production, possibly implement a better user experience:

  - E.g., if the token expires and user needs to login, handle it gracefully (maybe a message "Your session expired, please sign in again" and redirect).
  - Possibly use MSAL's event callbacks to detect login, logout events to update UI globally.
  - Provide a loading state during redirect to login.
  - If multi-tenant and user from another org tries to login, handle the case where admin consent is required (maybe catch the error and show a message "Your admin needs to approve this app" and provide a link/instructions).

- **Documentation & Secrets Management**: Document all the IDs and secrets and who owns them. For example, client IDs, tenant IDs etc., in a secure internal doc, so that maintenance or rotation can be done by the team.

Now our application is ready to deliver secure authentication and authorization in production.

---

# 10. Best Practices and Performance Optimization

Finally, let's consolidate best practices and some performance considerations for our architecture:

## 10.1 Optimizing Authentication Flows

- **Use Authorization Code + PKCE**: We implemented this (via MSAL). It's the most secure for SPAs as it avoids tokens in URLs and doesn't require a client secret. Never revert to the implicit flow unless absolutely necessary (which it shouldn't be).
- **Request Minimal Scopes**: Only ask for the permissions you need. We asked for our API access and basic openid/profile. Avoid asking for overly broad permissions (like Graph scopes you don't need) as it complicates consent and security.
- **Token Size**: Azure AD tokens can have a lot of claims (especially if user is in many groups). Large tokens can slightly impact performance (network overhead). If a user has many groups, consider using App Roles or filtering groups. Azure AD has an option to issue group IDs only if user is in <= 150 groups; beyond that, you'd have to fetch via Graph (which we didn't do, but in extreme cases plan for it).
- **Silent Renewals**: Rely on MSAL to do silent token acquisition. Avoid forcing the user to login repeatedly. Our app already does this.
- **User Experience**: If possible, use **Redirect** for login on first sign-in (for reliability), and you can use **Popup** for subsequent interactive requests (like if needing re-consent) so as not to navigate away. We primarily did redirect which is fine.
- **Home Realm Discovery**: If multi-tenant and you know a user's domain, you can skip the Azure AD common endpoint home realm discovery by using `authority` with the tenant (like user@domain.com, you might set authority to that tenantId directly if known). But MSAL common will direct them anyway after login.

## 10.2 Implementing Security Measures to Prevent Attacks

- **XSS Protection**: As noted, be vigilant about XSS. The biggest threat to an SPA's tokens is XSS, since an attacker who runs JS in the context can read the tokens from MSAL cache. Use React's protections, and consider a Content Security Policy. Keep dependencies updated to avoid known XSS vulnerabilities.
- **CSRF**: We are using tokens in JS, not cookies, so CSRF risk is low (an attacker site cannot read our token or force the user's browser to attach it automatically via cookie). Just ensure no sensitive operation is accepted via GET (we use appropriate methods).
- **Clickjacking**: Consider adding an `X-Frame-Options: DENY` or CSP frame-ancestors header on your UI responses to prevent the app from being framed by another site. Since login might use iframes (for silent refresh) or popups, ensure CSP allows frames from the identity provider if needed. MSAL might open an iframe to handle hidden requests if needed (less common in code flow).
- **Secure Cookies**: If you ever use cookies (we didn't for auth, but maybe for other things), mark them Secure and HttpOnly as appropriate.
- **Validating JWT**: We rely on library which checks signature and expiration. Good. We also set audience check. Ensure to also check `nbf` (not-before) claim if present (Spring does by default).
- **Account Lockout/Brute-force**: Azure AD itself will lockout or protect accounts from brute force login attempts, so we inherit that. We should consider DoS though - an attacker could send tons of requests with invalid tokens to our API. That might waste some CPU on JWT parsing. Mitigate by a WAF or rate limiting at a gateway if necessary.
- **Least Privilege for Backend**: The backend (Spring Boot) in our design doesn't call external resources, so it doesn't hold credentials except DB. If it needed to call Graph, use least privileged Graph scopes.
- **Input Validation**: Any data coming from users via API (not much in our case, maybe none) should be validated to avoid injection or logic issues.

- **Regular Updates**: Keep MSAL and Spring Boot/Security libraries up to date. They get improvements and security patches. Same for MySQL and its connector.
- **Penetration Testing**: Before go-live, doing a pen test or using scanning tools (like OWASP ZAP or Burp) on your deployed app can find issues like missing security headers or other vulnerabilities.

## 10.3 Improving Performance and Scalability

- **Caching Azure AD Metadata**: Spring Security fetches the public keys at startup. It will cache them. By default, the JWKS are cached with some default time. You might want to adjust the cache duration or key rotation policy (Azure rotates keys infrequently). Usually no issue, but be aware if using multiple instances, each will fetch at startup (small overhead).
- **Minimize Database Lookups**: Our DB filter currently queries every request. To optimize:
  - We could implement a simple cache for user roles. For instance, cache the roles for a given user ID in memory for, say, 5 minutes. That way, repeat requests in that window don't hit DB. But ensure to invalidate if roles change (maybe clear cache when Admin changes something).
  - Alternatively, accept the slight overhead if traffic isn't huge. A single primary key lookup and a join on roles should be quite fast (with proper indexes and the fact that roles and users are small tables in most apps).
- **Connection Pooling**: Spring Boot by default uses HikariCP for datasource pooling. Ensure the pool is sized appropriately (usually default is fine, but if high concurrency, consider tuning maximumPoolSize).
- **Threading**: Spring Boot will use a certain number of threads for handling requests (tomcat or netty if reactive). Ensure your instance size can handle the expected number of concurrent users. JWT validation is CPU cryptography heavy but usually negligible unless thousands of tokens per second; our DB hits could become bottleneck if thousand req/s as well.
- **Load Testing**: It's good to do a load test (using JMeter, Locust, etc.) to see how the app performs with e.g. 100 concurrent users making requests. Monitor CPU (JWT validation uses CPU, DB uses CPU IO).
- **Scale Up/Out**: We touched on scaling out (multiple instances). You might also scale up (a bigger VM size on App Service) if CPU is bottleneck. Or better, scale out to distribute load.
- **MySQL Performance**: If user base grows a lot, ensure the user table is indexed by id (primary key) which it is. Lookups by email we have (index email maybe if used). The join table might grow, but still small. Nothing heavy here. Just ensure to tune MySQL if needed (Azure DB for MySQL typically fine out of box for moderate load).
- **Asynchronous calls**: Our app doesn't really have heavy synchronous external calls except DB. If we had to call Graph or other APIs within a request, consider making them async or caching their results. But not needed now.
- **Bundle and Minify**: Our React build is minified and bundled (Create React App does that in production build). That reduces load times for front-end. We should also enable gzip compression on the hosting (most static hosts and App Service do by default) to compress JS files over network.
- **CDN**: If we have global users, consider putting a CDN in front of static files to speed up delivery across regions. Azure Static Web Apps uses Azure CDN automatically. For App Service, you can use Azure Front Door + CDN.
- **Monitoring and Autoscale**: Set up Azure Monitor autoscale rules so that if CPU goes beyond e.g. 70% for 10 minutes, spin up another instance. Similarly, scale down when idle to save cost. Test that scaling does not break anything (it shouldn't with stateless design).

By following these best practices and optimizations, our application should be secure, robust, and performant. It is now a comprehensive solution: from Azure AD configuration, through a React/MSAL frontend, a Spring Boot JWT-secured backend, to a MySQL-driven user data store, covering advanced scenarios like SSO, multi-tenancy, and role management.
