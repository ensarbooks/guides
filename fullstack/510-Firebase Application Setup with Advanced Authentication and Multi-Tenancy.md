# Firebase Application Setup with Advanced Authentication and Multi-Tenancy

This document provides a comprehensive, step-by-step guide for advanced developers to set up a Firebase-backed application with secure authentication, multi-tenancy, OAuth redirect URIs, secure API exposure, and secret management. We will cover everything from configuring Firebase Authentication (with multi-tenant support) and OAuth client settings, to integrating with a React frontend and securing a Spring Boot backend API. Best practices for handling secrets and deploying both frontend and backend are also included. The guide is organized into clear sections with code examples, conceptual diagrams, and deployment instructions.

**Table of Contents:**

1. [Introduction and Architecture Overview](#introduction-and-architecture-overview)
2. [Setting Up Firebase Authentication with Multi-Tenancy](#setting-up-firebase-authentication-with-multi-tenancy)
   - 2.1 [Enabling Multi-Tenancy in Firebase (Identity Platform)](#enabling-multi-tenancy-in-firebase-identity-platform)
   - 2.2 [Managing Tenants and Tenant-Specific Configuration](#managing-tenants-and-tenant-specific-configuration)
3. [Configuring OAuth Clients, Redirect URIs, and Authorized Domains](#configuring-oauth-clients-redirect-uris-and-authorized-domains)
   - 3.1 [OAuth Client IDs and Secrets in Firebase](#oauth-client-ids-and-secrets-in-firebase)
   - 3.2 [Setting Authorized Redirect URIs](#setting-authorized-redirect-uris)
   - 3.3 [Adding Authorized Domains for Web OAuth Operations](#adding-authorized-domains-for-web-oauth-operations)
4. [Exposing APIs Securely and Generating/Handling Secrets](#exposing-apis-securely-and-generatinghandling-secrets)
   - 4.1 [Secure API Architecture and Token Flow](#secure-api-architecture-and-token-flow)
   - 4.2 [Service Accounts and API Credentials](#service-accounts-and-api-credentials)
   - 4.3 [Managing Secrets and API Keys Safely](#managing-secrets-and-api-keys-safely)
5. [Implementing Authentication and Authorization in Firebase](#implementing-authentication-and-authorization-in-firebase)
   - 5.1 [Firebase Authentication Methods and Setup](#firebase-authentication-methods-and-setup)
   - 5.2 [Custom Claims for Role-Based Access Control](#custom-claims-for-role-based-access-control)
   - 5.3 [Security Rules and Tenant Isolation](#security-rules-and-tenant-isolation)
6. [Integrating Firebase Authentication with a React Frontend](#integrating-firebase-authentication-with-a-react-frontend)
   - 6.1 [Initializing Firebase in a React Project](#initializing-firebase-in-a-react-project)
   - 6.2 [User Sign-Up and Sign-In (Email/Password & OAuth)](#user-sign-up-and-sign-in-emailpassword--oauth)
   - 6.3 [Handling Multi-Tenant Logins on the Frontend](#handling-multi-tenant-logins-on-the-frontend)
   - 6.4 [Storing Tokens and Calling Secure APIs from React](#storing-tokens-and-calling-secure-apis-from-react)
7. [Securing a Spring Boot API Backend with Firebase Auth](#securing-a-spring-boot-api-backend-with-firebase-auth)
   - 7.1 [Setting Up Firebase Admin SDK in Spring Boot](#setting-up-firebase-admin-sdk-in-spring-boot)
   - 7.2 [Verifying Firebase ID Tokens in Spring (JWT Verification)](#verifying-firebase-id-tokens-in-spring-jwt-verification)
   - 7.3 [Protecting Endpoints and Role-Based Authorization in Spring](#protecting-endpoints-and-role-based-authorization-in-spring)
8. [Best Practices for API Security and Secret Management](#best-practices-for-api-security-and-secret-management)
   - 8.1 [Securing API Endpoints (HTTPS, CORS, and Rate Limiting)](#securing-api-endpoints-https-cors-and-rate-limiting)
   - 8.2 [Environment Variables and Secret Storage](#environment-variables-and-secret-storage)
   - 8.3 [Principle of Least Privilege and Key Rotation](#principle-of-least-privilege-and-key-rotation)
9. [Deployment of Frontend and Backend Applications](#deployment-of-frontend-and-backend-applications)
   - 9.1 [Deploying the React Frontend (Firebase Hosting)](#deploying-the-react-frontend-firebase-hosting)
   - 9.2 [Deploying the Spring Boot Backend (Cloud Run/App Engine)](#deploying-the-spring-boot-backend-cloud-runapp-engine)
   - 9.3 [Post-Deployment Configurations (Domains, Environment, Monitoring)](#post-deployment-configurations-domains-environment-monitoring)
10. [Conclusion](#conclusion)

---

## Introduction and Architecture Overview

In modern applications, **Firebase Authentication** provides an easy-to-use identity solution for user sign-up and login, while **Firebase (Google) Identity Platform** enables advanced features like multi-tenancy. In this guide, we will build a **multi-tenant** web application where multiple organizations or client apps (tenants) share a single backend, but each tenant has isolated user accounts and data. The frontend is a React single-page app that uses Firebase Auth for user login, and the backend is a Spring Boot REST API that validates Firebase-issued JWTs for secure data access.

**Architecture at a Glance:**

- **Firebase Project (Identity Platform)** – Central identity provider supporting multi-tenant authentication and various sign-in methods (email/password, Google OAuth, etc.).
- **Tenants** – Separate authentication tenant spaces under the Firebase project, each with its own users and configuration (for example, Tenant A and Tenant B each have their own user pool and allowed sign-in methods).
- **React Frontend** – A single-page application that initializes Firebase Auth (with the appropriate tenant), allows users to sign in/sign up, and obtains an **ID token** (JWT) after authentication.
- **Spring Boot Backend** – A RESTful API server that expects a Firebase ID token on protected requests (via an `Authorization: Bearer <token>` header). It uses the Firebase Admin SDK to verify tokens and enforce authorization (e.g., checking user roles or tenant membership) before accessing secure resources.
- **Secure API Calls Flow** – After a user logs in on React, the app includes the Firebase ID token with each API request. The Spring Boot server verifies the token and uses the token’s claims (such as `uid` and custom roles) to determine access. All communication occurs over HTTPS to protect tokens in transit.

Below is a simplified flow diagram of the authentication process:

1. **User Authentication (Frontend)**: A user signs into the React app using Firebase Authentication (either via email/password or an OAuth provider). If using multi-tenancy, the app specifies the tenant the user belongs to during this sign-in.
2. **Token Retrieval**: Firebase returns an **ID token** (JWT) for the authenticated user. This token contains the user's unique ID (`uid`), issuer info, expiration, and any custom claims or tenant ID.
3. **API Request with Token**: The React app sends an API request to the Spring Boot backend, including the ID token in the `Authorization` header (`Bearer <ID_TOKEN>`). This token acts as a credential proving the user's identity and tenant.
4. **Token Verification (Backend)**: The Spring Boot API uses Firebase’s Admin SDK (or a JWT library) to **verify the integrity and authenticity** of the ID token (checking signature, expiration, issuer, etc.) ([reactjs - Firebase Auth, after logging a user from react client, how do I verify user is legitimate within my other api? - Stack Overflow](https://stackoverflow.com/questions/61828463/firebase-auth-after-logging-a-user-from-react-client-how-do-i-verify-user-is-l#:~:text=If%20your%20Firebase%20client%20app,in%20user%20on%20your%20server)). Upon successful verification, the backend trusts the token’s claims (user identity and possibly roles/tenant).
5. **Authorization (Backend)**: The backend checks if the authenticated user is allowed to perform the requested operation. This could involve checking the user’s roles (custom claims in the token, like admin privileges) or ensuring the user’s tenant matches the data being accessed.
6. **Protected Resource Access**: If verification and authorization succeed, the backend executes the request (e.g., reads or writes data) and returns a response. If the token is missing, invalid, or the user lacks permission, the backend returns an error (e.g., 401 Unauthorized or 403 Forbidden).
7. **Frontend Usage**: The React app receives the response. If it was a successful call, it updates the UI with the secured data. If an error occurred (e.g., token expired or invalid), the app may prompt the user to re-authenticate.

Throughout this guide, we will build and configure each part of this flow. By the end, you'll have a working example of a **secure, multi-tenant Firebase Authentication setup** with a React client and a Spring Boot server, and knowledge of best practices for secrets and deployment.

---

## Setting Up Firebase Authentication with Multi-Tenancy

Multi-tenancy in Firebase allows you to use a single Firebase/Identity Platform project to serve **multiple distinct user groups (tenants)** with isolated authentication configurations. Each tenant can have its own users, identity providers, and even custom settings under the umbrella of one Firebase project ([
Solved: Multitenancy with Firebase (Is that possible?) - Google Cloud Community
](https://www.googlecloudcommunity.com/gc/Databases/Multitenancy-with-Firebase-Is-that-possible/m-p/637291#:~:text=Yes%2C%20it%20is%20possible%20to,users%2C%20authentication%20methods%2C%20and%20roles)). This is useful if you are building a software-as-a-service application where each client organization should have its own user base and cannot see other tenants’ users.

**Key Concepts:**

- **Identity Platform**: Firebase Authentication's multi-tenancy feature is available through Google Cloud Identity Platform (an enterprise version of Firebase Auth). You will need to ensure Identity Platform is enabled for your project to use multi-tenancy.
- **Tenant**: A tenant represents an isolated user pool. Users signing in under one tenant won't be able to sign into another tenant's space. Each tenant can enable different authentication methods (email/password, Google, etc.) as needed.
- **Tenant-aware Authentication**: When multi-tenancy is enabled, the Firebase Auth client and Admin SDK become tenant-aware. You can specify a `tenantId` in auth requests to target a specific tenant.

In this section, we'll enable multi-tenancy in our Firebase project and set up tenants.

### Enabling Multi-Tenancy in Firebase (Identity Platform)

By default, Firebase projects are single-tenant. To enable multi-tenancy, you must turn on Identity Platform’s multi-tenant support:

1. **Enable Identity Platform**: In the Google Cloud Console for your Firebase project, enable **Identity Platform** if you haven't already. (This might involve enabling a Cloud API and accepting terms, since it's a Google Cloud service that extends Firebase Auth.)
2. **Allow Multi-Tenancy**: Navigate to the Identity Platform settings for your project:
   - Go to **Google Cloud Console > Identity Platform > Settings**.
   - Select the **Security** tab.
   - At the bottom, you should find a toggle or button to **“Allow tenants”**. Click this to enable multi-tenancy for the project ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=Enabling%20multi)). (In Firebase terms, this “Turns on” multi-tenant awareness.)
3. **Verify Enablement**: Once enabled, a new **Tenants** section or page should appear in the console. This confirms that your project now supports multiple tenants. You may receive a notice that each tenant will have separate configurations.

**Note:** Enabling multi-tenancy might require a Blaze (paid) plan, as it's part of the Identity Platform features. Ensure your Firebase project is on an appropriate plan or check the quotas for multi-tenant usage.

After enabling, Firebase’s Authentication service _“supports multi-tenancy, allowing you to create multiple tenants within a single Firebase project”_ ([
Solved: Multitenancy with Firebase (Is that possible?) - Google Cloud Community
](https://www.googlecloudcommunity.com/gc/Databases/Multitenancy-with-Firebase-Is-that-possible/m-p/637291#:~:text=Yes%2C%20it%20is%20possible%20to,users%2C%20authentication%20methods%2C%20and%20roles)). Each tenant will have its own set of users, sign-in methods, and configuration options, completely isolated from other tenants (this includes separate user UID namespaces, separate authentication provider credentials, etc.).

### Managing Tenants and Tenant-Specific Configuration

With multi-tenancy enabled, you can now create and configure individual tenants:

**1. Create Tenants:**

- Open the **Identity Platform > Tenants** page in the Cloud Console for your project.
- Click **“Add tenant”** (or a similar button to create a new tenant) ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=Creating%20a%20tenant%3A)).
- Enter a Name for the tenant (e.g., “Tenant A” for Organization A). The name is for your reference; once you save, an immutable **Tenant ID** (often a random string) will be generated by the system.
- Save the tenant. Repeat for each tenant you need (e.g., Tenant B, Tenant C, etc.).

Each tenant will be assigned a unique Tenant ID by Identity Platform ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=2)). You will use this Tenant ID in your code to direct authentication requests to the correct tenant.

**2. Tenant-specific Auth Settings:**

- For each tenant, you can configure allowed authentication methods. In the console, after selecting a tenant from the dropdown (the console UI usually has a tenant selector once multi-tenancy is on ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=Selecting%20a%20tenant%3A))), you can manage that tenant’s **Sign-in providers** similar to how you would in a normal Firebase project.
- For example, you can enable Email/Password for Tenant A, or enable Google Sign-In for Tenant B, etc., under each tenant’s settings. Providers and their credentials (like OAuth client IDs for Google or Facebook) can be set per tenant.
- Each tenant also has separate **users**. If you view the Authentication > Users list in the Firebase Console while a specific tenant is selected, you will see only that tenant’s users.

**3. Application Configuration for Tenants:**

Your application (frontend and possibly backend) needs to be aware of tenants. There are two main approaches:

- **Single Auth Instance switching tenants:** Use one Firebase Auth instance on the frontend, and set its `tenantId` property before each sign-in or sign-up operation to indicate which tenant to use.
- **Multiple Auth Instances:** Initialize multiple Firebase app instances (with the same config) but each attached to a different tenant. This is less common; the simpler approach is usually to switch the `tenantId` dynamically.

For most cases, using a single instance and setting the tenant as needed is sufficient. Firebase provides a property to do this on the client SDK:

**Setting the tenant in code (Firebase Web SDK):**

```js
import { getAuth } from "firebase/auth";

const auth = getAuth(); // your initialized Auth instance
auth.tenantId = "TENANT_ID_OF_CHOICE";
```

By assigning the desired tenant’s ID to `auth.tenantId` before a sign-in call, you ensure that the authentication action applies to that tenant ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=To%20sign%20in%20to%20a,not%20persisted%20on%20page%20reloads)). _Any future sign-in requests from this auth instance will include the tenant ID... until you change or reset the tenant ID_ ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=To%20sign%20in%20to%20a,not%20persisted%20on%20page%20reloads)). If `tenantId` is `null` or not set, auth calls go to the main project (no tenant context).

**Example:** If a user from Tenant A is logging in:

```js
auth.tenantId = "tenantA-id123"; // set Tenant A's ID (from console)
signInWithEmailAndPassword(auth, email, password);
```

This ensures that the email/password is checked against only Tenant A’s user pool, not global or other tenants.

If you have a multi-tenant app where the tenant is determined by the user’s context (for example, the URL `tenantA.yourapp.com` vs `tenantB.yourapp.com` or a user selection), you will use that to set the correct `tenantId` in the auth instance.

**4. Multi-Tenant Behavior:**

- A user authenticated under a tenant will have their ID token include the tenant information. The token’s payload has a field for `firebase` -> `tenant` (the tenant ID), which can be used on the backend to know the tenant context of the user.
- Users cannot sign in to another tenant without re-authenticating under that tenant (their credentials are scoped to their tenant).
- The Firebase Admin SDK allows tenant management as well. For instance, you can list or create users in specific tenants programmatically by obtaining a tenant-scoped auth instance on the server (not covered in depth here, but possible via `auth.tenantManager().authForTenant(tenantId)` in some SDKs).

By this point, we have multi-tenancy enabled and at least one tenant created. Next, we will configure OAuth settings like client IDs and redirect URIs, which apply to both single-tenant and multi-tenant scenarios.

---

## Configuring OAuth Clients, Redirect URIs, and Authorized Domains

Often, Firebase Authentication is used with OAuth providers (like Google, Facebook, GitHub) or with email link authentication that involves redirecting back to your application. Proper configuration of **OAuth client IDs**, **redirect URIs**, and **authorized domains** is crucial for these flows to work securely. In a multi-tenant environment, each tenant can have its own OAuth provider configuration, but there are also project-wide settings (like authorized domains) that need to be handled.

This section will guide you through:

- Setting up OAuth 2.0 client credentials (if needed) for providers in Firebase.
- Configuring the redirect URI that OAuth providers will use to return to your app.
- Ensuring your app’s domain(s) are whitelisted in Firebase for authentication operations.

### OAuth Client IDs and Secrets in Firebase

If you enable providers like Google, Facebook, Twitter, etc., via Firebase Authentication, some require entering **OAuth client credentials**:

- **Google**: By default, enabling Google sign-in in Firebase Console might auto-configure a Google OAuth client for your project. However, if you want to use a custom OAuth consent screen or multiple domains, you can specify a **Web Client ID** and **Web Client Secret** for Google sign-in in the Firebase console. This ensures the Google sign-in flow uses the specific OAuth client associated with your app.
- **Facebook, Twitter, GitHub**: These require you to register an OAuth app on their platforms and then supply the **App ID/Key** and **App Secret** to Firebase (under Authentication > Sign-in method > provider).

In Firebase Console, go to **Authentication -> Sign-in method**, and for each enabled provider:

- Click the provider (e.g., Google) and find the section for **Web SDK configuration (optional)** (for Google) or **OAuth redirect** info.
- For Google: You can enter a _Web client ID_ and _Web client secret_ obtained from the Google API Console. According to one explanation, if the Google OAuth flows are failing, you should ensure that _the same Google API project’s Client ID/Secret_ are entered here, and that the project IDs match ([angularfire - Firebase Google OAuth redirect error - Stack Overflow](https://stackoverflow.com/questions/39212980/firebase-google-oauth-redirect-error#:~:text=Google%27s%20error%20message%20includes%20a,Web%20client%20secret)). In other words, the OAuth client used by Firebase (which you can manage in **Google Cloud Console > APIs & Services > Credentials**) must have its details in sync with Firebase Auth settings.
- For other providers: Supply the required API Key/Secret that you obtained from registering your app with that provider.

**Why configure these?**  
Firebase can handle a lot of the OAuth dance for you, but misconfiguration can lead to errors like _“redirect_uri_mismatch”_ or _“unauthorized domain”_. By providing the correct client IDs and secrets and ensuring they correspond to your app’s authorized URIs, you let Firebase manage the OAuth flow on your behalf.

If you see errors from Google like _“The redirect URI in the request does not match the ones authorized for the OAuth client.”_, it often means the client ID being used by Firebase isn’t authorized for the domain or redirect. Double-check the following:

- The **Project ID** in Google Developers Console (for your OAuth client) matches your Firebase project’s ID ([angularfire - Firebase Google OAuth redirect error - Stack Overflow](https://stackoverflow.com/questions/39212980/firebase-google-oauth-redirect-error#:~:text=Google%27s%20error%20message%20includes%20a,Web%20client%20secret)).
- The **Web client ID** and secret from Google Developers Console are correctly entered in Firebase (Auth -> Sign-in method -> Google -> Web SDK configuration) ([angularfire - Firebase Google OAuth redirect error - Stack Overflow](https://stackoverflow.com/questions/39212980/firebase-google-oauth-redirect-error#:~:text=Google%27s%20error%20message%20includes%20a,Web%20client%20secret)). This ties Firebase Auth to use your specific OAuth client.
- The **Authorized redirect URIs** for that OAuth client include Firebase’s redirect handler (we discuss this next).

### Setting Authorized Redirect URIs

**Redirect URIs** come into play for OAuth-based sign-in methods (Google, Facebook, etc.) and email link sign-in. A redirect URI is the URL to which the external auth provider will send the user (often with an auth code or access token) after authentication. Firebase Authentication uses a standardized pattern for redirect URIs in web applications:

- When using Firebase’s frontend SDK, the redirect URI is usually:  
  **`https://YOUR_FIREBASE_AUTH_DOMAIN/__/auth/handler`**  
  By default, `YOUR_FIREBASE_AUTH_DOMAIN` is something like `yourproject.firebaseapp.com` (or your custom domain if you use one for auth).

For example, if your Firebase project ID is "myproj", the redirect URI might be `https://myproj.firebaseapp.com/__/auth/handler`. This is where Firebase listens for the OAuth provider's response.

**Configuring the redirect URI with providers:**

- **Google**: If you use a custom OAuth client, go to the Google API Console, find your OAuth 2.0 Client ID, and in its settings ensure the above URI (with your domain) is listed as an **Authorized redirect URI**. Google will only redirect to whitelisted URIs for security. In our earlier example error, the developer had to add `https://crudiest-firebase.firebaseapp.com/__/auth/handler` as an authorized redirect in Google Console ([angularfire - Firebase Google OAuth redirect error - Stack Overflow](https://stackoverflow.com/questions/39212980/firebase-google-oauth-redirect-error#:~:text=,)) ([angularfire - Firebase Google OAuth redirect error - Stack Overflow](https://stackoverflow.com/questions/39212980/firebase-google-oauth-redirect-error#:~:text=In%20my%20Google%20Developers%20Console,that%27s%20in%20the%20error%20message)).
- **Facebook/Twitter/GitHub**: Similarly, in the developer settings for those apps, add the Firebase auth domain (with `__/auth/handler`) as a valid OAuth redirect/callback URL. The Firebase Console often reminds you of the exact URL to add. For instance, Facebook might require `https://myproj.firebaseapp.com/__/auth/handler` in its OAuth settings for the app.
- **Email Link (Passwordless)**: When using email link sign-in, you will specify a **continue URL** (the link that the user clicks in the email) which must be whitelisted. Usually, you use the same auth domain or custom domain. Firebase will handle that link (again via the `__/auth/handler` if using Firebase-hosted domain or via dynamic links if configured).

**Multi-Tenant Note:** Each tenant can potentially have a different auth domain if you set up custom domains per tenant (this is advanced usage). By default, all tenants use the main project's auth domain. If you want a custom domain per tenant (so that redirects show a tenant-specific domain), you would configure multiple authorized domains (one per tenant) and use Identity Platform’s ability to host a custom domain for a tenant. Otherwise, using the main domain is fine.

Once configured, these redirect URIs ensure that external providers will successfully return to your application’s Firebase handler page, which then closes the loop and signs the user in.

### Adding Authorized Domains for Web OAuth Operations

Firebase restricts authentication operations (OAuth sign-in, email link sign-in, etc.) to authorized domains to prevent abuse. If you attempt to sign in from an unlisted domain, you'll get an "unauthorized domain" error.

**Authorized Domains setup:**

1. In the Firebase console, go to **Authentication** and then the **Sign-in method** tab.
2. Scroll to the section **Authorized domains**.
3. Add any domain that your application will use for authentication. This typically includes:
   - Your production domain (e.g., `myapp.com`).
   - Development or staging domains (e.g., `localhost` if testing locally, or a test subdomain).
   - The default Firebase Hosting domain for your project (e.g., `myproj.firebaseapp.com` and possibly `myproj.web.app`).
   - Any custom domain you've set up for Firebase Hosting or auth.
4. Click Save.

For example, to authorize localhost for development and a custom domain:

- Add `localhost` (and `127.0.0.1`) – these cover your local dev environment if you test the OAuth flow there.
- Add `yourapp.com` – your main site domain.
- The Firebase default domain might already be listed by default.

Make sure that the domain used in your redirect URIs is in this list. If using only the default domain for auth redirects, it should already be present. If you add a custom domain (like `auth.yourapp.com`) for handling sign-in, include that too.

**Troubleshooting Unauthorized Domain Errors:**  
If you encounter the error _“This domain is not authorized for OAuth operations for your Firebase project”_, it means the current host is not in the authorized list. The solution is to add that domain in the Firebase console:

- Go to Authentication > Sign-in method > Authorized domains.
- Add the domain and save ([How I solved Firebase Auth/unauthorized domain. Domain is not authorized error problem using the Vite development tool - DEV Community](https://dev.to/clericcoder/how-i-solved-firebase-authunauthorized-domain-domain-is-not-authorized-error-problem-using-the-vite-development-tool-2md7#:~:text=,console%20for%20your%20project)).
- Try the sign-in again.

Make sure to include the domain _without protocol or path_ (just the domain name). The Firebase console will handle subdomains if you add a root domain (in some cases you might need to add subdomains separately; e.g., adding `example.com` does not automatically allow `app.example.com`).

**Summary:** At this point, we have:

- Enabled needed OAuth providers in Firebase (possibly configured client IDs/secrets if required).
- Ensured the correct redirect URIs are set in those provider's configurations.
- Listed our app domains as authorized in Firebase to perform authentication.

This lays the groundwork so that when our React app initiates, say, a Google sign-in, Google knows to redirect back to our Firebase handler, and Firebase accepts the request from that domain. Now, let's move on to securing our backend API and handling secrets.

---

## Exposing APIs Securely and Generating/Handling Secrets

The backend API (our Spring Boot service) will be **exposed** to the internet to serve requests from the frontend. We need to ensure it is secured properly:

- Only authenticated users with valid tokens can access protected endpoints.
- Secrets (like service account keys or API keys) are handled safely and **not exposed** to the client or in the repository.

This section covers the secure API design and how to manage sensitive credentials.

### Secure API Architecture and Token Flow

As described in the introduction, the secure pattern is to use **Firebase ID Tokens** as the credential for API calls. This means our API endpoints will expect a bearer token and validate it. The general best practice as stated by Firebase is: _after a successful sign-in, send the user's ID token to your server via HTTPS, then have the server verify the token's integrity and authenticity, and use the token's claims (like `uid`) to identify the user_ ([reactjs - Firebase Auth, after logging a user from react client, how do I verify user is legitimate within my other api? - Stack Overflow](https://stackoverflow.com/questions/61828463/firebase-auth-after-logging-a-user-from-react-client-how-do-i-verify-user-is-l#:~:text=If%20your%20Firebase%20client%20app,in%20user%20on%20your%20server)).

**Why use Firebase tokens?** Firebase ID tokens are JWTs signed by Google (with its private keys) and can be verified using Google’s public keys. They are short-lived (usually ~1 hour), and can be refreshed by the client using a refresh token. By using these tokens:

- We avoid handling user passwords in our backend.
- We leverage Firebase’s secure token generation and verification process.
- We unify the auth system: the same login that works for frontend (Firebase) is accepted by backend.

**API Endpoint Protection Strategy:**

- **Authentication**: The backend will **verify the token** on each request to a protected endpoint. If the token is missing or invalid, the request is rejected (HTTP 401 Unauthorized).
- **Authorization**: Once authenticated, the backend can further check the user's privileges. For example, if an endpoint is tenant-specific, the backend can ensure the `tenantId` in the token (or in the request path) matches the data being accessed. If roles are used (via custom claims), the backend can check if `admin` claim is present for admin-only operations (if not, return 403 Forbidden).

All API communication should be over **HTTPS**. This prevents eavesdropping; an ID token sent over plain HTTP could be intercepted. Modern deployments (like Cloud Run or other hosting) will manage TLS for you. Ensure that your development environment also uses HTTPS for front-backend communication if possible (or at least be cautious with local testing).

We will implement the verification in the Spring Boot section. At a high level:

- The React app will attach the token: e.g., `Authorization: Bearer <id_token>` header.
- A Spring Security filter (or middleware) will parse this header, and if present, validate the JWT using Firebase’s Admin SDK.
- If valid, the filter passes the request to the intended controller; otherwise it blocks the request.

Diagram of a request handling:

```
Client (React + Firebase Auth) -- [HTTP GET /api/resource, Authorization: Bearer <ID_TOKEN>] --> Spring Boot API
Spring Boot API:
    - Intercept request -> Extract ID_TOKEN from Authorization header.
    - Verify ID_TOKEN (signature, expiration, audience) via Firebase Admin SDK.
    - If valid, identify user (e.g., get uid, tenant, claims).
    - (Optional) Check user roles/claims for this endpoint.
    - If all good, proceed to execute controller logic and return data.
    - If token invalid/expired, return 401; if lacks permission, return 403.
```

This ensures the API is not **“wide open”** – it’s only accessible with a valid token issued by _our Firebase project_.

### Service Accounts and API Credentials

To verify Firebase ID tokens and to perform certain admin actions (like creating custom tokens or managing users), the backend will use the **Firebase Admin SDK**. The Admin SDK needs credentials to authenticate with Firebase/Google services. This is typically done using a **service account**.

**Service Account Credentials:**

- In Firebase, go to **Project Settings > Service Accounts**. There you can generate a new private key for a service account (commonly the "Firebase Admin SDK default service account"). Download the JSON file – **this file is a secret** and contains a private key.
- Alternatively, in Google Cloud IAM, you can create a dedicated service account with the role **Firebase Admin** (or more granular permissions if needed, like just verifying tokens which might only need minimal permissions). Then generate a key for it.

The JSON key file will look like:

```json
{
  "type": "service_account",
  "project_id": "yourproject-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvg...",
  "client_email": "firebase-adminsdk-xxx@yourproject.iam.gserviceaccount.com",
  ... // other info
}
```

We will use this in our Spring Boot app to initialize Firebase Admin SDK. **Important:** Do not commit this file to source control. Keep it in a safe location and load it via environment variable or secure configuration (details on this in the secrets section).

**API Keys in Firebase Config:**

- Your Firebase web app config (often in `firebaseConfig` in the React app) contains an `apiKey`. This key is **not** truly a secret – it’s used to identify your project on Firebase and is okay to be visible in the client. Firebase API keys are not like server API keys; they cannot, by themselves, give access to your database or users without proper rules. (In fact, _“Don’t think of the API Key as a secret; it's not a private key, it's just an ID so the Firebase API knows who's accessing what project.”_ ([javascript - Is it safe to expose Firebase apiKey to the public? - Stack Overflow](https://stackoverflow.com/questions/37482366/is-it-safe-to-expose-firebase-apikey-to-the-public#:~:text=You%20guys%20aren%27t%20thinking%20about,you%20should%20be%20using%20GCP))).
- However, treat the Firebase API key with some care: do not hardcode it in multiple places unnecessarily, and restrict it in the Google Cloud Console if possible (for example, restrict usage to the Firebase services it’s meant for). But you **do not need to hide the Firebase config** on the frontend – it’s required for the app to connect to Firebase.

**Other Secrets (OAuth Secrets, etc.):**

- If you configured OAuth providers like Facebook, the secret keys for those are stored in Firebase and not exposed to the client. The client only gets an OAuth token which is fine.
- If your backend calls other third-party APIs or uses database credentials, those secrets should be kept out of the code and configured via secure means (env variables or a vault).

### Managing Secrets and API Keys Safely

Handling secrets properly is a critical part of secure application development. Here are best practices and how they apply to our scenario:

- **Never commit secrets to source control**: This includes service account JSON files, API keys for third-party services, etc. Use a `.gitignore` to exclude sensitive files (e.g., add the JSON key file there) ([API Keys Security & Secrets Management Best Practices - GitGuardian Blog](https://blog.gitguardian.com/secrets-api-management/#:~:text=,lived%20secrets)). Many breaches happen due to leaked keys in repos.
- **Use Environment Variables or Secret Management**: Instead of coding secrets in plaintext, store them in environment variables on the server or use a secrets manager. For example, you might set an environment variable `GOOGLE_APPLICATION_CREDENTIALS` that points to your service account JSON file path, or use something like Google Secret Manager to inject the key. Cloud platforms and CI/CD systems have mechanisms to supply secrets to your app at runtime ([API Keys Security & Secrets Management Best Practices - GitGuardian Blog](https://blog.gitguardian.com/secrets-api-management/#:~:text=,lived%20secrets)). This way, even if your code is public, the secrets come from a secure store.
- **API Key Exposure**: As noted, the Firebase `apiKey` is not a serious security risk by itself (exposing it doesn’t grant unintended access beyond possibly using your project’s resources, which your security rules protect) ([javascript - Is it safe to expose Firebase apiKey to the public? - Stack Overflow](https://stackoverflow.com/questions/37482366/is-it-safe-to-expose-firebase-apikey-to-the-public#:~:text=You%20guys%20aren%27t%20thinking%20about,you%20should%20be%20using%20GCP)). However, keys for other services (for example, a Stripe secret key or a custom API secret) _are_ sensitive. Those should strictly reside on the backend and never be sent to the frontend. If the frontend needs to perform an action with a third-party API, route it through your backend so you can keep the secret safe.
- **Rotate Keys if Compromised**: If you suspect a service account key or other secret leaked, revoke it (Firebase allows you to disable a service account key in IAM) and generate a new one. The Firebase Admin SDK will stop working if the key is revoked, so update your environment with the new key promptly.
- **Principle of Least Privilege**: Use service accounts with the minimal permissions your backend needs ([API Keys Security & Secrets Management Best Practices - GitGuardian Blog](https://blog.gitguardian.com/secrets-api-management/#:~:text=%2A%20Use%20,lived%20secrets)). For verifying ID tokens and managing custom claims, the Firebase Admin SDK service account (default one) is fine. But if you create your own, give it roles like “Firebase Authentication Admin” rather than Project Owner.
- **Don’t expose implementation details**: When your backend returns errors, avoid sending stack traces or hints that could help an attacker. For auth, just return a 401/403 without detail like “token expired” (you can log it internally).
- **Secure Communication**: Always use HTTPS for any API calls that include secrets or tokens (which should be all calls, essentially). This is non-negotiable for production.
- **CORS Configuration**: If your backend is separate from your frontend domain, set CORS rules to only allow the front-end origin in requests. This way, other domains cannot randomly make requests to your API with a user’s token (web browsers won’t send the request if CORS disallows). We will set this in Spring Boot security.
- **Short-lived vs Long-lived credentials**: Firebase ID tokens are short-lived (one hour). This is good practice, as even if one is stolen, it expires quickly. The refresh token is long-lived but it’s meant to be stored securely by the client (and only used to get new ID tokens). Make sure the refresh token is not accessible via JavaScript if possible (for example, in a web app, you might not have a refresh token unless using certain Firebase features, since the JS SDK handles it internally).
- **Logging and Monitoring**: Log authentication events on the backend (e.g., log when a token is rejected or a user with certain UID accesses a resource). Use Firebase Authentication logging and Cloud Monitoring to set up alerts for suspicious patterns (like many failed token verifications).

To summarize, **exposing APIs securely** means requiring valid auth tokens, validating them, and not leaking secrets. **Generating secrets** refers to creating things like service account keys or other secret tokens and doing so in a controlled manner (for instance, generating a random API secret for some internal use and storing it in Secret Manager, rather than keeping a default weak secret).

Next, we will implement the authentication and authorization logic in Firebase and our app (including custom claims for roles).

---

## Implementing Authentication and Authorization in Firebase

Now that we have the infrastructure set up (Firebase project with multi-tenancy, providers configured, and a plan for our secure API), let's implement the core authentication and authorization features. This involves two sides:

- On the **client side (Firebase Auth)**: handling user sign-up, sign-in, and ensuring we know the user's tenant and identity.
- On the **Firebase side**: optionally setting up custom claims for authorization.
- On the **backend side**: enforcing authorization rules (which we'll detail in the Spring section, but we outline the plan here as it relates to Firebase).

### Firebase Authentication Methods and Setup

In Firebase (Identity Platform), you have multiple methods to authenticate users:

- Email/Password
- OAuth providers (Google, Facebook, etc.)
- Phone number
- Anonymous (if enabled)
- Custom token (where you mint a token via Admin SDK)

For multi-tenancy, each tenant can have a different combination of these. For our purposes, let's assume:

- We enable **Email/Password** for basic login.
- Optionally, enable **Google OAuth** for convenience (this requires the config we did earlier).
- Users will register either via a sign-up form or an invitation (depending on your app’s logic). Self-service sign-up can be enabled per tenant.

**Setting up in Console:**  
Ensure under each tenant’s Authentication > Sign-in method, the methods you want are enabled. For example, under Tenant A, enable Email/Password (and possibly set Email link to off if not needed), and enable Google sign-in. Under Tenant B, maybe only Email/Password.

**Email/Password in Multi-tenant:**  
Each tenant's users are separate, but from the user's perspective, it’s the same process:

- A user provides email and password.
- Firebase will create an account under that tenant.

One thing to note: If the same email should be able to exist in different tenants, that’s allowed because identity is isolated per tenant. However, within a single tenant, emails must be unique.

**Implement Registration (if applicable):**  
Your app might have a “Sign Up” page where new users enter details. Using Firebase JS SDK:

```js
auth.tenantId = "<TENANT_ID>";
createUserWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed up successfully for the tenant
    const user = userCredential.user;
    // ... perhaps prompt email verification or profile setup
  })
  .catch((error) => {
    // Handle errors (e.g., email already in use, weak password)
  });
```

After sign-up, the user is usually auto-logged in (with a fresh ID token). You might want to send email verification depending on security needs (Firebase can send verification emails).

**Implement Login:**  
On login, similar code without the creation:

```js
auth.tenantId = "<TENANT_ID>";
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Logged in, you can get the user or token here
    const user = userCredential.user;
    // e.g., get token: user.getIdToken()
  })
  .catch((err) => {
    // Handle error (wrong password, user not found, etc.)
  });
```

For OAuth login (e.g., Google), you would also set `auth.tenantId` then do:

```js
auth.tenantId = "<TENANT_ID>";
const provider = new GoogleAuthProvider();
// Optionally, provider.addScope('profile'); etc.
signInWithPopup(auth, provider)
  .then(result => {
    // Google sign-in successful for this tenant.
    const user = result.user;
    // ...
  })
  .catch(err => { ... });
```

The main difference for multi-tenancy is ensuring the `auth.tenantId` is set appropriately _before_ calling the sign-in method. If not set, the sign-in might go to the default project user pool (which could fail if multi-tenancy is enforced).

**Authorization vs Authentication:**  
Authentication is verifying who the user is (which we just handled). **Authorization** is determining what the user can do. Out-of-the-box, Firebase Auth doesn't have user roles or groups, but we can implement that with **Custom Claims**.

### Custom Claims for Role-Based Access Control

Firebase allows you to set **custom claims** on user accounts via the Admin SDK. These claims are then included in the user's ID token (and refreshed token) and can be used to control access in various parts of your app:

- On the backend, you can check the token’s claims for roles like `admin: true` or `role: "moderator"`.
- In Firebase Security Rules (for Firestore/RTDB/Storage), you can also use custom claims to allow/deny certain operations to users with specific roles.

Implementing custom claims gives you a lightweight authorization mechanism without deploying a full external authorization system. _“Implementing custom claims-based authorization in Firebase boosts security by giving users specific permissions... using the Firebase Admin SDK to add claims to the user's ID token, letting you set access roles and privileges”_ ([How to implement a custom claims-based authorization in Firebase? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-a-custom-claims-based-authorization-in-firebase#:~:text=Implementing%20custom%20claims,resources%20based%20on%20set%20permissions)).

**Example Use Case:** Mark certain users as administrators of their tenant. They can access an admin-only API endpoint or perform certain management tasks.

**Setting a Custom Claim:**
You would typically set custom claims from a privileged environment (backend). For instance, using Node.js Admin SDK or Java Admin SDK in a secure context:

```js
// Node.js example (could be in a Cloud Function or a secure server)
admin
  .auth()
  .setCustomUserClaims(uid, { admin: true, tenantManager: true })
  .then(() => {
    // The claims have been set for the user
  });
```

This will attach `{ "admin": true, "tenantManager": true }` to the user's token payload on next issuance.

Using the Admin SDK in Java (Spring Boot could do this at some point):

```java
FirebaseAuth.getInstance().setCustomUserClaims(uid, claimsMap);
```

(where `claimsMap` is a Map like `{"admin": true}`).

**When are claims available?** Once set, the existing ID token a user has will **not** automatically have the new claim (because it’s already issued). The claim will appear:

- The next time the user’s ID token is refreshed (Firebase SDK auto-refreshes hourly, or you can force refresh by calling `user.getIdToken(true)` on client).
- If the user signs in again.

So, after setting claims, you might force a token refresh or ask the user to re-login to pick up new privileges.

**Using Custom Claims in Security (Backend):**
Our Spring Boot backend, after verifying the token, will have access to the decoded token’s claims. For example, if using the Firebase Admin SDK to verify, the result might be a `FirebaseToken` (in Java) which has `getClaims()`. If we added an `admin` claim:

```java
boolean isAdmin = Boolean.TRUE.equals(decodedToken.getClaims().get("admin"));
```

We can then allow or deny certain operations based on this flag. For instance, only admins can access a certain controller or perform a certain action.

We could implement this by:

- Adding a check in the filter or in the controller method (e.g., using Spring Security’s method security to require a role).
- Alternatively, mapping the Firebase token to a Spring Security `Authentication` with roles.

For simplicity, we might not fully integrate with Spring Security’s role hierarchy; we can just manually check in code.

**Using Custom Claims in Security Rules (if using Firestore, etc.):**
Even though our focus is a custom backend, note that if you have any Firebase Storage or Firestore usage, you can enforce that only certain users (with claims) can access certain data. In Firestore rules, for example:

```js
allow write: if request.auth.token.admin == true;
```

This would allow writes only if the custom claim `admin` is true on the user's token.

**Multi-Tenant and Claims:**
If you have multi-tenant, you might not need to encode the tenant in a claim (since Firebase already tracks tenant), but you may encode roles that are tenant-specific. For example, a claim `{ role: "admin", tenant: "tenantA-id" }` could be set, but that might be redundant since the token is anyway minted under a tenant. Instead, use the built-in tenant context and just have role claims.

It's often better to manage tenant context separately (the token's `firebase.tenant` is inherent). Focus claims on roles or permissions.

**Assigning Claims Workflow:**
You might decide that when a user signs up, they get a default role (like "user"). If you have an admin dashboard where an admin user can promote someone to admin, that action would trigger the Admin SDK to set a claim on that user's UID. In a multi-tenant app, you'd likely ensure one user per tenant is an admin, etc.

We will see how to retrieve these claims on the backend in the Spring Boot section. But keep in mind, the **Firebase Admin SDK is needed to set claims** – it can be done from a secure backend or Cloud Function. The client cannot directly give itself admin claims (that would be a huge security hole!). Only code with Admin privileges can assign them.

### Security Rules and Tenant Isolation

While our primary data will likely be handled by the Spring Boot API (which will have its own database or logic), many Firebase projects also use Firestore/Realtime DB or Cloud Storage. If you do:

- Use **Firebase Security Rules** to ensure tenant data is isolated. Typically, you would structure data by tenant ID (as shown in some data model diagram ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=Tenants%20,User%201))) and then write rules that only allow users from that tenant to read/write that tenant’s subcollection.
- For example, if Firestore has a document path like `/tenants/{tenantId}/users/{userId}`, a rule could be:

  ```js
  match /tenants/{tenantId}/data/{doc} {
    allow read, write: if request.auth != null
                      && request.auth.token.firebase.tenant == tenantId;
  }
  ```

  This ensures the Firebase Auth tenant matches the tenant segment in the data path.

- If you rely purely on your Spring Boot backend to interact with the database (bypassing Firebase client-side SDK for data), then security rules might not be in play. Instead, enforce tenant isolation in your backend logic (e.g., query filtering by tenant, verifying the token's tenant if present).

**Email Verification and Account Settings:**  
It’s generally a good idea to verify users' email addresses to prevent spam accounts. Firebase can send verification emails. You can enforce in the backend that `decodedToken.isEmailVerified()` is true before allowing certain operations.

**Multi-factor Authentication (MFA):**  
For advanced security, Identity Platform supports MFA. This might be beyond our scope, but just know it exists and can be enabled for users.

So far, we have our Firebase authentication system configured and ready: multi-tenant aware, with optional role claims for authorization. Next, let's integrate this on the frontend with React, and then on the backend with Spring Boot.

---

## Integrating Firebase Authentication with a React Frontend

In this section, we will connect everything on the client side. The React application will use Firebase Authentication to allow users to sign up, sign in, and sign out. It will handle multi-tenancy (by selecting or detecting the tenant and setting `tenantId` accordingly) and obtain ID tokens to communicate with the backend.

We will also implement basic UI flows: login form, possibly a registration form, and showing the user's status. Finally, we’ll cover how the React app should call the Spring Boot API with the auth token.

### Initializing Firebase in a React Project

First, add Firebase to your React project:

- Install Firebase SDK:

  ```bash
  npm install firebase
  ```

  (We assume using Firebase v9+ which uses modular import syntax. You can also use v8 with namespaced syntax; the concepts remain the same.)

- Get your Firebase config object from the Firebase Console:

  - In Project Settings > General, under "Your apps", find the configuration for your web app. It will be a JSON like:
    ```js
    {
      apiKey: "...",
      authDomain: "yourproject.firebaseapp.com",
      projectId: "yourproject",
      ... other keys ...
    }
    ```
  - **Important**: If using multi-tenancy, `authDomain` might be your default domain. If you plan to use a custom domain for auth, that should be reflected here once set up. Usually, you can keep using the default domain for the Firebase SDK config even if you have custom domains for frontends, as long as those domains are authorized (the SDK will still redirect to authDomain when needed).

- Initialize Firebase in your app (e.g., in a file `firebase.js` or at the top level of your app):

  ```js
  // firebase.js
  import { initializeApp } from "firebase/app";
  import { getAuth } from "firebase/auth";

  const firebaseConfig = {
    apiKey: "<YOUR-API-KEY>",
    authDomain: "<YOUR-AUTH-DOMAIN>",
    projectId: "<YOUR-PROJECT-ID>",
    // ...other config like storageBucket, appId, etc.
  };

  const app = initializeApp(firebaseConfig);
  export const auth = getAuth(app);
  ```

  This sets up the Firebase App and Auth instance. We export `auth` so we can use it in our React components or utility functions.

- (If you use context providers or state management for auth, you might wrap your app in an `AuthProvider` that uses Firebase, but that's an implementation choice.)

**Multi-Tenancy in Frontend:**
We have a single `auth` instance here. When a user from a specific tenant is about to log in or sign up, we will set `auth.tenantId = "<tenant-id>"`. One way is to determine the tenant on app load:

- If each tenant has a unique URL, parse `window.location.hostname` to figure out which tenant it is, and map that to the tenant ID.
- Or have the user select their tenant from a dropdown on the login page, and then set the tenantId accordingly when they submit.

Make sure to reset or change the tenantId if the user switches context (in most apps, a user will stay in one tenant context for their session).

### User Sign-Up and Sign-In (Email/Password & OAuth)

Let's implement the UI logic for sign-in and sign-out in React.

**Login Form (Email/Password) Example:**  
Assume we have a component with a form for email and password, and perhaps a way to specify tenant (like a subdomain or a select box).

```jsx
import React, { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase"; // our initialized auth

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [tenant, setTenant] = useState(""); // this could be tenant ID or name

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Set the tenantId before signing in
      auth.tenantId = tenant ? tenant : null; // assume tenant state holds the tenant ID string
      const userCred = await signInWithEmailAndPassword(auth, email, password);
      console.log("Logged in user:", userCred.user);
      // You might now redirect or fetch some user data
    } catch (err) {
      console.error("Login error:", err);
      alert(err.message);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      {/* Tenant input: could be a select if you have predefined tenants */}
      <input
        value={tenant}
        onChange={(e) => setTenant(e.target.value)}
        placeholder="Tenant ID"
      />
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
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
}
```

In a real app, you might not ask users to manually input a tenant ID. Instead, if each tenant uses a different subdomain or domain, you can map that. For example:

```js
// Determine tenant ID from hostname
const host = window.location.hostname;
if (host.includes("tenantA")) {
  auth.tenantId = "TENANT_A_ID";
} else if (host.includes("tenantB")) {
  auth.tenantId = "TENANT_B_ID";
}
```

Alternatively, use a subdirectory or ask user to choose their organization from a list.

**OAuth (Google) Sign-In Example:**  
You might have a button "Sign in with Google". On click:

```jsx
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const provider = new GoogleAuthProvider();
// if you want specific Google scopes: provider.addScope('https://www.googleapis.com/auth/drive');

auth.tenantId = tenantIdForThisUser;
signInWithPopup(auth, provider)
  .then((result) => {
    console.log("Google sign-in success:", result.user);
  })
  .catch((err) => {
    console.error("Google sign-in error", err);
  });
```

Firebase will handle redirect or popup flows. If using **redirect mode** instead of popup (some prefer redirect to avoid popup blockers), you'd call `signInWithRedirect(auth, provider)` and later handle the redirect result when the app loads (using `getRedirectResult`). In redirect mode, ensure your domain is properly in authorized domains and the OAuth redirect URI is correct (which we did in earlier sections).

**Sign-Out:**  
To log out:

```js
import { signOut } from "firebase/auth";
signOut(auth)
  .then(() => {
    // Sign-out successful
  })
  .catch((err) => console.error("Sign-out error", err));
```

This will clear the user’s session on the client. (The backend doesn't maintain a session for the user aside from the token, which expires automatically.)

**State Persistence:**  
Firebase Auth by default will keep the user logged in (using local storage) even after refresh, unless you configure otherwise. This is typically fine. When the app loads, you can listen to `onAuthStateChanged(auth, user => { ... })` to detect if a user is already logged in. If so, you might set some global state (like currentUser context). This is useful to conditionally show the UI (if user is null show login page, if not show main app). We'll omit detailed code for brevity, but it's a common pattern.

### Handling Multi-Tenant Logins on the Frontend

As discussed, you need to identify which tenant context the user is trying to log in to. Some patterns to implement this:

- **Subdomain per tenant**: e.g., `tenant1.myapp.com`, `tenant2.myapp.com`. You can deploy the same React app to respond to all those subdomains (via DNS wildcard and a check on `hostname`). Then in your React app initialization, pick the tenant based on `hostname`.
- **User-entered domain/tenant**: The user might type their company name or choose from a list on a landing page. For example, the app could start at a generic page where the user enters "tenant name: \_\_\_\_", then the app knows which tenant's ID to use.
- **Tenant-specific build**: Less ideal, but you could build separate frontends per tenant with tenantId hardcoded. This doesn't scale well if you have many tenants, though.

For simplicity, let's assume subdomain. So:

```js
// Example tenant mapping
const host = window.location.hostname;
let tenantId;
switch (host) {
  case "tenanta.myapp.com":
    tenantId = "TENANT_A_ID";
    break;
  case "tenantb.myapp.com":
    tenantId = "TENANT_B_ID";
    break;
  default:
    tenantId = null; // or some default
}
auth.tenantId = tenantId;
```

This code would run before any sign-in attempt. That way, the user is automatically working in the correct tenant.

**UI considerations**: Make it clear to the user which tenant they are accessing. Possibly display the tenant name/logo on the login screen.

### Storing Tokens and Calling Secure APIs from React

Once a user is logged in, Firebase Auth provides an ID token that we need to send to our backend API. How do we get the token and how do we include it in requests?

**Retrieving the ID Token:**
The Firebase user object (auth.currentUser) can always produce a fresh ID token:

```js
const user = auth.currentUser;
if (user) {
  const token = await user.getIdToken(/* forceRefresh */ true);
  console.log("ID Token:", token);
}
```

By passing `true` to getIdToken, we force a refresh (so we get the latest claims if any were updated, and maximize token lifetime). In practice, you might call getIdToken without forceRefresh to use a cached token until it's close to expiry, but for initial login or critical operations, refreshing is fine.

The token is just a string (JWT). We will now include this in our HTTP calls. If using **fetch** or **axios**, you attach it as an Authorization header:

For example, using fetch:

```js
fetch("https://api.myapp.com/secure-data", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
  .then((res) => res.json())
  .then((data) => {
    console.log("Secure data from API:", data);
  });
```

Or with axios:

```js
axios.get("https://api.myapp.com/secure-data", {
  headers: { Authorization: `Bearer ${token}` },
});
```

You should perform this retrieval and attachment for **every request** that needs authentication. In practice, you might intercept requests globally (if using axios, set a default header after login, or if using fetch, write a small wrapper that always adds the token). Just be careful to refresh the token if it's about to expire – the Firebase SDK can handle token refresh behind the scenes. If a token is expired, the backend will respond 401, and your frontend can then attempt to get a new token (Firebase usually already would have refreshed it if the user is still logged in).

**Important:** Do not store the ID token in long-term storage (like LocalStorage) with the intention to manage sessions yourself. Rely on Firebase to store the refresh token (which it does in local storage if persistence is enabled) and use `getIdToken` when needed. Storing the ID token persistently could be a security risk if XSS is a concern, because an attacker could grab it. It's short-lived anyway.

**Example: Getting token and calling backend (combining steps):**  
Suppose after logging in, you want to immediately fetch the user's profile data from your backend:

```js
const user = auth.currentUser;
if (user) {
  user
    .getIdToken()
    .then((token) => {
      return fetch("/api/profile", {
        headers: { Authorization: "Bearer " + token },
      });
    })
    .then((response) => {
      if (!response.ok) throw new Error("Auth failed or other error");
      return response.json();
    })
    .then((profileData) => {
      console.log("Got profile data:", profileData);
    })
    .catch((err) => {
      console.error("Error fetching profile:", err);
    });
}
```

Using the token in the header is straightforward. Make sure your backend’s CORS configuration allows the `Authorization` header and the origin of your front-end, otherwise the request might be blocked by the browser.

**Token Renewal and Session Persistence:**  
Firebase will automatically refresh the token in the background using the refresh token as long as the user is logged in. You typically don't need to manually handle refresh unless you specifically require the latest claims. The `onIdTokenChanged` listener can notify you whenever the token is refreshed (which could be hourly). If needed, you can use that to update something or re-fetch user roles.

**Testing the End-to-End Flow (before backend is ready):**  
As a quick test, you can call a dummy endpoint like:

```js
user.getIdToken().then((t) => console.log(t));
```

and then manually decode the token (for instance, using jwt.io or a library) to verify it contains the claims and the correct `firebase/tenant` etc. Also test that if you use a wrong tenantId (or none when required), sign-in fails appropriately.

Now our React app is set up to authenticate users and attach tokens to API requests. Next, we focus on the Spring Boot backend to accept and verify these tokens and secure the API endpoints.

---

## Securing a Spring Boot API Backend with Firebase Auth

We will now configure our Spring Boot application to use Firebase for authentication and authorization. The main tasks are:

- Initialize Firebase Admin SDK with our credentials.
- Set up a filter (or use Spring Security configuration) to intercept requests and verify the Firebase ID token from the `Authorization` header.
- Secure the endpoints so that only authenticated (and authorized) users can access them.
- Optionally, utilize roles from custom claims for authorization.

We assume you have a Spring Boot project (Gradle or Maven). Ensure you have the Firebase Admin SDK dependency in your build file. For example, in Maven:

```xml
<dependency>
  <groupId>com.google.firebase</groupId>
  <artifactId>firebase-admin</artifactId>
  <version>8.1.0</version> <!-- check for latest version -->
</dependency>
```

And possibly a Google API client dependency (though Firebase Admin brings what’s needed, older versions might require adding `com.google.http-client:google-http-client`).

### Setting Up Firebase Admin SDK in Spring Boot

**1. Service Account Key and Initialization:**

Place your service account JSON file in the Spring Boot project's resource directory (e.g., `src/main/resources/serviceAccountKey.json`). Alternatively, set an environment variable that points to it (like `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`).

During application startup, initialize Firebase:

```java
@Configuration
public class FirebaseConfig {

    @PostConstruct
    public void initFirebase() throws IOException {
        // Load the service account key JSON from the classpath
        try (InputStream serviceAccount =
                 new ClassPathResource("serviceAccountKey.json").getInputStream()) {
            FirebaseOptions options = FirebaseOptions.builder()
                    .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                    .build();
            FirebaseApp.initializeApp(options);
            System.out.println("Firebase Admin initialized");
        }
    }
}
```

This uses the JSON file to authenticate. If you're deploying on Google Cloud (App Engine/Cloud Run) and prefer using the default service account, you could instead do:

```java
FirebaseOptions options = FirebaseOptions.builder()
    .setCredentials(GoogleCredentials.getApplicationDefault())
    .build();
```

This would pick up credentials from the environment (Cloud Run’s service account or the env var if running locally).

**2. Spring Security Configuration:**

We will use Spring Security to intercept requests. In our security config, we’ll add a custom filter that checks the token after the built-in filters.

Example using the older WebSecurityConfigurerAdapter (Spring Boot 2.x way):

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.cors().and().csrf().disable() // enable CORS and disable CSRF for API (or configure appropriately)
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS).and()
            .authorizeRequests()
            .antMatchers("/public/**").permitAll()    // any public endpoints if you have
            .anyRequest().authenticated();

        // Add our custom JWT filter
        http.addFilterBefore(new FirebaseTokenFilter(), UsernamePasswordAuthenticationFilter.class);
    }

    // Possibly configure CORS if needed
    // e.g., @Bean CorsConfigurationSource corsConfigurationSource() { ... }
}
```

We ensure that:

- Sessions are stateless (we won't use HTTP sessions since auth is via token every time).
- All requests except explicitly public ones require authentication.
- We then insert our `FirebaseTokenFilter` to run before Spring’s default auth handling.

**3. Implementing the FirebaseTokenFilter:**

We create a filter that extends `OncePerRequestFilter` to run for each request:

```java
public class FirebaseTokenFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            // No token present, just continue. It will fail .authenticated() check if needed.
            // Alternatively, we could immediately reject here with 401.
            chain.doFilter(request, response);
            return;
        }
        String idToken = authHeader.substring(7); // remove "Bearer "

        try {
            // Verify the ID token with Firebase Admin SDK
            FirebaseToken decodedToken = FirebaseAuth.getInstance().verifyIdToken(idToken);
            // Token is valid. You can get the uid and claims if needed:
            String uid = decodedToken.getUid();
            Map<String, Object> claims = decodedToken.getClaims();
            String tenantId = decodedToken.getTenantId(); // should give tenant if present

            // Here we set up an authenticated user for Spring Security context if needed
            List<GrantedAuthority> authorities = new ArrayList<>();
            if (claims.containsKey("admin") && (Boolean) claims.get("admin")) {
                authorities.add(new SimpleGrantedAuthority("ROLE_ADMIN"));
            }
            // You can map more claims to authorities as needed.

            // Create an Authentication object
            UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(uid, /* credentials */ null, authorities);
            // Optionally store the token or user details in the authentication
            authentication.setDetails(decodedToken);

            // Set the authenticated user in context
            SecurityContextHolder.getContext().setAuthentication(authentication);
        } catch (FirebaseAuthException e) {
            // Invalid token or verification failed
            logger.error("Firebase ID token verification failed: " + e.getMessage());
            // You could short-circuit and send an error response here:
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid or expired token");
            return;
        }

        // Proceed with the request
        chain.doFilter(request, response);
    }
}
```

Let's explain the key parts:

- We grab the `Authorization` header and check for a "Bearer " token. If it's not there, we allow the filter chain to continue. Depending on requirements, you might want to immediately reject if no token for protected endpoints, but letting it continue to `.authenticated()` check also results in a 401 since no authentication is set.
- We extract the token string and call `FirebaseAuth.getInstance().verifyIdToken(idToken)`. This method will:
  - Verify the token's signature (using Google's public keys, which the SDK fetches and caches automatically).
  - Check token is not expired, issued for this project, etc.
  - If using multi-tenancy, **important**: By default, this might accept tokens from any tenant in the project. If you want to ensure only a specific tenant's token is allowed in this particular API instance, you could configure FirebaseAuth with a specific tenant or manually check `decodedToken.getTenantId()`. For example, if this API is only for Tenant A, verify that `tenantId.equals("TENANT_A_ID")` and otherwise reject.
- If verification fails (token invalid, expired, revoked), a `FirebaseAuthException` is thrown and we return a 401 to the client.
- If verification succeeds, we get a `FirebaseToken` (from Admin SDK), which includes `uid` (user’s unique ID) and `claims` (custom claims we set, as well as standard ones).
- We then create a `UsernamePasswordAuthenticationToken` with the user's UID as the principal (you could load a custom UserDetails by UID if you have a user service, but here UID is enough as identity). We also convert any relevant custom claims to Spring authorities (in the example, if `admin` claim is true, we add a ROLE_ADMIN authority).
- We set this Authentication into the `SecurityContext`. This means the user is now considered authenticated for the rest of the request handling.
- Downstream, in controllers, you can access `SecurityContextHolder.getContext().getAuthentication()` to get the uid or check roles (or use method security annotations if roles were set).
- The filter is set to run before the username/password filter (though we actually disabled form login entirely). Running it early ensures that by the time `.authenticated()` is checked, our context is populated.

This approach is essentially stateless JWT authentication in Spring Security, using Firebase as the JWT issuer. We have **successfully tied Firebase Authentication into Spring Security**.

To ensure it works, you can create a simple secured controller:

```java
@RestController
@RequestMapping("/api")
public class TestController {

    @GetMapping("/hello")
    public String hello(Authentication auth) {
        // Authentication will not be null if token was valid
        String uid = (String) auth.getPrincipal();
        return "Hello user " + uid;
    }

    @GetMapping("/adminOnly")
    public String adminOnly(Authentication auth) {
        if (auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"))) {
            return "Hello Admin " + auth.getName();
        }
        throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Not an admin");
    }
}
```

The `/api/hello` should return a greeting if a valid token is provided. The `/api/adminOnly` will check the roles set from custom claims.

**CORS Configuration:**
Because our React app likely runs on a different origin (e.g., http://localhost:3000 in dev or https://myapp.com in prod) than the API (maybe http://localhost:8080 or an API subdomain), we need to enable Cross-Origin Resource Sharing for the token to be accepted. In our SecurityConfig above, we called `http.cors()`. We should define a `CorsConfigurationSource` bean, for example:

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(Arrays.asList("http://localhost:3000", "https://myapp.com")); // allow frontend origins
    config.setAllowedMethods(Arrays.asList("GET","POST","PUT","DELETE"));
    config.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type"));
    config.setExposedHeaders(Arrays.asList("Authorization")); // if we needed to expose any
    config.setAllowCredentials(true);
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    return source;
}
```

Adjust the allowed origins to match your front-end domain(s). This configuration will allow the browser to make requests with the `Authorization` header. Without it, the browser will block the request (even though our server might accept it) due to CORS policy.

Now, with Spring Boot set up, let's verify the flow end-to-end:

- User logs in on React (for tenant X), gets ID token.
- React calls `/api/hello` with that token.
- Our filter in Spring Boot sees the `Authorization: Bearer ...` header, verifies the token via Firebase Admin:
  - If the token is issued by our Firebase project and not expired, `verifyIdToken` returns a `FirebaseToken`.
  - The filter then marks the SecurityContext as authenticated with the user's UID.
- The request proceeds to the controller, which sees an authenticated user and returns the data.
- If the token was missing or invalid, the filter returns 401. The frontend should handle that (maybe redirect to login if 401).

One more thing: **Tenant Enforcement**. If our backend is serving multiple tenants at once, we might not need to explicitly enforce tenant ID in the backend as long as data separation logic is elsewhere. However, if, say, the request URL contains a tenant identifier, we should check that it matches the token’s tenant to avoid a user from one tenant trying to access another tenant’s data by altering URL. For example, if an endpoint is `/api/tenantA/resource`, ensure the token’s tenant is tenantA. This could be done in the filter or in each controller. A simple approach in filter:

```java
String path = request.getRequestURI();
if (path.contains("/tenantA/") && !"TENANT_A_ID".equals(decodedToken.getTenantId())) {
    response.sendError(HttpServletResponse.SC_FORBIDDEN, "Wrong tenant");
    return;
}
```

This is rudimentary; a more dynamic solution is needed if you have many tenants and the tenant id in path or subdomain.

Since our design might rely on subdomains hitting potentially different backend instances or at least the front-end controlling tenant context, we might not include tenant ID in URLs. We might rely solely on the token’s tenant in backend to segregate anything.

### Protecting Endpoints and Role-Based Authorization in Spring

We have already demonstrated how to restrict endpoints to authenticated users and even how to check roles (custom claims) in the controller. We can strengthen this by:

- Using method-level security. We enabled `@EnableGlobalMethodSecurity(prePostEnabled = true)` in our security config (if not, we can). Then we can use `@PreAuthorize` annotations.
  Example:
  ```java
  @PreAuthorize("hasAuthority('ROLE_ADMIN')")
  @GetMapping("/adminData")
  public Data getAdminData() { ... }
  ```
  The `hasAuthority('ROLE_ADMIN')` will consult the GrantedAuthorities we set (which included ROLE_ADMIN for admin claim). This is cleaner than checking inside the method.
- We should ensure any non-public URL is protected. Our config already has `.anyRequest().authenticated()`, which covers that. If you add new endpoints and forget to restrict, that line catches it.

- If we have some endpoints that should be accessible by any logged-in user of a specific tenant only, we could incorporate that logic in the controller by comparing the requested resource's tenant with the token’s tenant. For instance:

  ```java
  @GetMapping("/tenant/{tenantId}/projects")
  public List<Project> listProjects(@PathVariable String tenantId, Authentication auth) {
      FirebaseToken token = (FirebaseToken) auth.getDetails();
      if (!tenantId.equals(token.getTenantId())) {
         throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Cross-tenant access not allowed");
      }
      // proceed to fetch projects for that tenant...
  }
  ```

  This assumes we saved the decoded token in `auth.setDetails()` as shown in the filter.

- If the entire backend is meant for one tenant, and you deploy separate instances per tenant, you might not need to check tenant each time (the instance can be configured with a fixed tenant). But in a single instance multi-tenant API, always validate that a user of Tenant A cannot access Tenant B’s data.

**Testing the Backend:**

- Try calling a protected endpoint without any Authorization header. You should get a 401.
- Call with `Authorization: Bearer <invalid or expired token>` – you should also get 401.
- Call with a valid token but manipulated (like an invalid signature) – 401.
- Call with a valid token from _another Firebase project_ – likely 401 or it might fail signature because wrong keys (the Admin SDK is tied to your project’s keys).
- If multi-tenancy is enabled, a token from a tenant of your project will pass signature, but if you want to reject tokens from other tenants at this API, implement that check.

Now the backend is effectively secure. The final pieces are about best practices and deployment.

---

## Best Practices for API Security and Secret Management

Throughout the guide, we have touched on several best practices. Here we compile and emphasize them to ensure our application remains secure and maintainable in the long run:

### Securing API Endpoints (HTTPS, CORS, and Rate Limiting)

- **Always use HTTPS**: This cannot be said enough. Ensure that both your frontend and backend are served over HTTPS in production. Firebase Hosting provides HTTPS by default. For the Spring Boot API, if using Cloud Run or other hosting, enforce HTTPS. This protects the ID tokens and any sensitive data in transit.
- **CORS (Cross-Origin Resource Sharing)**: Configure CORS on the backend to only allow requests from trusted origins (your front-end domains). We configured this in Spring Security. This prevents malicious websites from making requests to your API with a logged-in user's credentials (browser will not send the request if origin is not allowed).
- **Rate Limiting and Throttling**: Consider implementing rate limiting on the API to mitigate brute force or DDoS attacks. For example, if someone tries to hammer your authentication filter with random tokens, rate limiting can slow them down. Cloud Run and other services can integrate with Cloud Armor or similar to rate-limit. Or use a library like Bucket4J in Spring to rate limit.
- **Revoke Tokens if needed**: If a user’s account is compromised or an admin wants to force log out a user, Firebase allows revoking refresh tokens (Admin SDK `revokeRefreshTokens(uid)`). This will invalidate their session at next token refresh. Keep this in mind for account management.
- **Logging**: Log authentication failures on the backend (but not the full token!). For instance, log the UID of token if verification succeeds, or log the error message if it fails. Monitor these logs for unusual activity.
- **Test Auth Bypasses**: Ensure that no endpoints inadvertently bypass the auth filter. For example, double-check any configuration of Spring Security that `addFilterBefore` is correctly positioned. Verify that actuator or other built-in endpoints are either secured or disabled if they expose info.
- **Use App Check (Optional)**: Firebase offers App Check to ensure that only your authentic app can call certain Firebase resources. For a custom backend, App Check is less directly applicable, but you could use it for Firebase Storage/Firestore calls from client. It's an extra layer if needed (it adds attestation so that only requests from your app (web or mobile) succeed).
- **Content Security Policy on Frontend**: While not directly related to auth, adding CSP headers on your React app can mitigate XSS, which in turn helps protect the token in memory.

### Environment Variables and Secret Storage

- **Do not expose secrets in code**: The service account JSON, API secrets, etc., should not be checked into git or included in the frontend bundle. We used environment variables (or config files) for these on the server side. On the client side, the only "secret-like" thing is the Firebase apiKey which is safe as discussed.
- **Use a Secrets Manager**: In production, use cloud secret managers (e.g., Google Secret Manager, AWS Secrets Manager) to store things like the service account key or other secrets. You can then load them at runtime. Firebase has integration for Secret Manager with Cloud Functions, and for Cloud Run you can mount secrets as files or env vars.
- **Configuration Segregation**: Keep production credentials separate from development. Use different Firebase projects for dev vs prod if possible, so you don’t accidentally use a dev service account in prod. This also means separate API keys, etc. (You can utilize `.env` files and Spring profiles to switch configs.)
- **Encryption at Rest**: The service account JSON is sensitive; if it must reside on a disk, ensure it's in a secure location. If using container images, don't bake the secret into the image; mount it at runtime.
- **Principle of Least Privilege** (again because it's important): For example, if you only need to verify tokens and perhaps set custom claims, your service account might just need Firebase Auth Admin privileges. Don’t grant it Editor/Owner unless necessary. This way, even if the key leaked, damage is limited.

### Principle of Least Privilege and Key Rotation

- **Least Privilege for Firebase Services**: Limit which Firebase features are enabled. If your app only needs Firebase Auth (Identity Platform) and maybe Firestore, you can disable others (like if you’re not using Realtime DB or Storage, make sure they are secured or turned off to avoid any misuse).
- **User Roles**: We added custom claims for an admin role. Only grant such roles to users who need them. Implement an administrative interface carefully – ensure only existing admins can assign admin claims (to avoid escalation).
- **Rotate Secrets**: Have a plan to rotate secrets regularly. For example, the Firebase service account key – you might create a new one every 6 months and update your app to use it, then destroy the old one. This reduces the window of misuse if a key was compromised without your knowledge.
- **Audit and Alerting**: Set up Google Cloud audit logs to alert on things like new service account keys created, or if someone changes OAuth client settings. Also monitor Firebase Authentication metrics (like sudden spike in new accounts or sign-in failures).
- **Backup and Recovery**: Keep backup ways to access your system if something goes wrong. E.g., an emergency way to disable the auth requirement (maybe by deploying a variant of the backend) if Firebase itself has an outage – not usually needed, but just part of planning.

To summarize, building with Firebase and a custom backend can be very secure as long as you follow these practices. We leverage Google's security for identity (which is robust), and then enforce our own rules on the backend. The largest pitfalls to avoid are misconfigurations (like forgetting to restrict domain, or exposing a secret).

Finally, let's move on to deploying our applications.

---

## Deployment of Frontend and Backend Applications

After building the system, we need to deploy it in a production environment. We want our React frontend and Spring Boot backend to be accessible to users and to work together with Firebase Authentication seamlessly. This section outlines how to deploy each and what configurations might be needed post-deployment.

### Deploying the React Frontend (Firebase Hosting)

Firebase Hosting is an excellent choice for deploying single-page applications. It offers global CDN, HTTPS, custom domain support, and easy integration with Firebase services.

**Steps to Deploy on Firebase Hosting:**

1. **Build the React App**: Run the production build:

   ```bash
   npm run build
   ```

   This will create an optimized build (usually in a `build` or `dist` directory).

2. **Initialize Firebase Hosting (first time only)**:

   - Install Firebase CLI if not already: `npm install -g firebase-tools`
   - Login: `firebase login`
   - Init: `firebase init hosting`
     - Select your Firebase project.
     - Set `build` (or whichever folder has index.html) as the public directory.
     - Choose single-page app rewrite (yes for SPA, so that all routes serve index.html).
     - It will create a `firebase.json` and possibly a `.firebaserc`.

3. **Deploy**:

   ```bash
   firebase deploy --only hosting
   ```

   This will upload your static files to Firebase’s CDN. The CLI will give you a preview URL or use your configured domain.

4. **Custom Domain (optional)**:

   - If you want to use a custom domain (like `app.mycompany.com`), go to Firebase Hosting section in console, add custom domain, and follow steps to verify (you add a TXT DNS record) and set A records.
   - Once verified, Firebase will provision an SSL cert and serve your content on that domain.
   - Make sure to add this custom domain to the **Authorized domains** in Authentication settings as discussed before, so that Firebase Auth calls from that domain are allowed ([How I solved Firebase Auth/unauthorized domain. Domain is not authorized error problem using the Vite development tool - DEV Community](https://dev.to/clericcoder/how-i-solved-firebase-authunauthorized-domain-domain-is-not-authorized-error-problem-using-the-vite-development-tool-2md7#:~:text=,console%20for%20your%20project)).

5. **Multi-site / Multi-tenant**:
   - If each tenant had a separate domain, you could either set up multiple sites in Firebase Hosting (Firebase allows multiple hosting sites under one project, each with its own domain). But if the same app is used for all tenants and just detects the domain, you might not need multiple sites – one site with a wildcard domain could suffice (though official support for wildcard custom domains is limited; you typically must list each domain explicitly in Firebase Hosting).
   - Alternatively, you might deploy separate Firebase Hosting sites for each tenant if they have very different needs, but that complicates deployment. For most cases, one hosting site that handles all tenants via code logic is fine.

**Post-Deployment:**

- Test the login flow on the deployed site (on the firebaseapp.com domain or your custom domain). Ensure that OAuth redirects (e.g., Google sign-in) return to this domain correctly. If you get a redirect mismatch error, check that the domain is added in Google API console and Firebase Auth settings (we covered this).
- Test calling the backend from the deployed front-end. If there's any CORS issue, adjust the backend's allowed origins to include the production domain.

Firebase Hosting also can do **rewrites** to Cloud Functions or Cloud Run, but in our case we have a separate backend domain/service, so we don't necessarily need to route through Firebase Hosting. We can have the React app call the backend directly at its URL.

If you wanted, you could use Firebase Hosting rewrites to proxy API calls to your Spring Boot backend (for instance, if using Cloud Run, you could set up a rewrite so `/api/**` on the same domain proxies to the Cloud Run URL). This is an advanced config but can simplify CORS issues (because then the front-end and backend appear on the same domain to the client). This would be configured in `firebase.json` hosting settings. However, it's optional. CORS with proper configuration is fine too.

### Deploying the Spring Boot Backend (Cloud Run/App Engine)

For the Spring Boot application, several hosting options exist. Two common ones on GCP are **Cloud Run** (containerize and deploy) or **App Engine**. Cloud Run is a good choice for a stateless service like ours:

- It easily deploys Docker containers.
- It can scale to 0 (no traffic, no cost).
- We can set it to allow public unauthenticated access (since we handle auth) or use Cloud IAM (not needed here since we manage our own auth).
- It's HTTPS by default with a \*.run.app domain, and we can map custom domains.

**Deploying to Cloud Run:**

1. **Containerize the app**:

   - Add a `Dockerfile` at the root of your Spring Boot project (if one is not already present). For example:
     ```dockerfile
     FROM eclipse-temurin:17-jre-alpine  # use OpenJDK 17 JRE
     COPY target/myapp-0.0.1-SNAPSHOT.jar app.jar
     EXPOSE 8080
     CMD ["java", "-jar", "/app.jar"]
     ```
     Make sure the JAR path matches your build output. If using Gradle with bootJar, it might be `build/libs/yourapp.jar`.
   - (Alternatively, use Google Cloud Buildpacks which can build a container without a Dockerfile: `gcloud builds submit --pack image...`, but Dockerfile is straightforward.)

2. **Build and push the container**:

   - If you have Google Cloud CLI set up and a project, you can do:
     ```bash
     gcloud builds submit --tag gcr.io/yourproject/yourapp-image:v1 .
     ```
     This will build the image and push to Google Container Registry (or Artifact Registry).
   - Or manually build with Docker and push:
     ```bash
     docker build -t gcr.io/yourproject/yourapp:v1 .
     docker push gcr.io/yourproject/yourapp:v1
     ```

3. **Deploy to Cloud Run**:

   ```bash
   gcloud run deploy yourapp-service \
      --image gcr.io/yourproject/yourapp:v1 \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
   ```

   - We allow unauthenticated because we are not using Cloud Run's built-in auth (which is Google Accounts or IAM based); our JWT is from Firebase and we check it manually.
   - Choose the region closest to your users (and ideally same region as your Firebase project resources).
   - Cloud Run will output a URL, e.g., `https://yourapp-service-abc123.uc.r.appspot.com`. This is the base URL for your API.

4. **Set environment variables on Cloud Run**:

   - If you didn’t bake the service account JSON into the image, you can set an env var `GOOGLE_APPLICATION_CREDENTIALS` to a mounted secret. Cloud Run has a Secret Manager integration. For simplicity, you might have included the JSON in the image (not best practice) or uploaded it as a secret and then mount it.
   - Alternatively, if running on Cloud Run with the same project, consider not using a JSON key at all and instead let Cloud Run's service account have the needed permissions. Then use `GoogleCredentials.getApplicationDefault()`. In Cloud Run, the default service account is PROJECT_NUMBER-compute@developer.gserviceaccount.com (unless you change it). You could grant that service account the role `Firebase Authentication Admin`. Then `FirebaseApp.initializeApp()` with no credentials will use that. This avoids having any key in the container.
   - To set env vars: `gcloud run deploy ... --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/path/in/container/key.json` (and you'd have to ensure that key.json is present in container as a secret volume).

5. **Custom Domain for API (optional)**:

   - Cloud Run allows mapping custom domains via Cloud Run domain mappings. If you want something like `api.myapp.com`, you can set that up.
   - However, it's also fine to use the run.app URL and just configure your frontend to call that, as long as it's in authorized domains (though you don't need to add the Cloud Run domain to Firebase auth authorized domains because Firebase auth is only concerned with the domain where auth operations occur, which is the front-end domain).
   - If using a custom domain for API, you don't need to add it to Firebase authorized domains since the tokens are sent via header (the domain check is only for the web context of sign-in, not for token verification).

6. **App Engine Alternative**:

   - App Engine Standard for Java can also be used (just `gcloud app deploy`, but you'd have to adjust your app.yaml, etc.). App Engine automatically uses the default service account. But Cloud Run is more flexible with fewer gotchas (App Engine Standard Java has some restrictions and uses older Java by default). Cloud Run is likely the simpler path.

7. **Verify Backend is working**:
   - You can use a tool like curl or Postman:
     ```
     curl -H "Authorization: Bearer <token>" https://yourapp-service-...run.app/api/hello
     ```
     and see if you get "Hello user UID".
   - Or call from the deployed React app and check the browser console/network for responses.

**Scaling and Performance**:

- Cloud Run will scale out instances if traffic increases. By default, each instance can handle 80 concurrent requests. You might adjust memory/cpu if needed (e.g., if verifying tokens is CPU heavy – generally it's lightweight JWT signature check, should be fine).
- Cold starts: Cloud Run might spin down to zero. The next request will cold start (~ seconds delay). To reduce this, you could set a minimum instance to 1. This costs a bit more but ensures low-latency always.
- The Spring Boot app itself should ideally start fairly quickly. Using the latest Java and maybe native images (via GraalVM) could improve startup if needed, but that's advanced. For moderate use, it's fine.

**Security**:

- Ensure the Cloud Run service account has least privilege. If it only needs to verify tokens, it might not even need the Firebase Auth Admin role because verifying ID tokens does not require calling a Firebase endpoint – it's done with public keys. Actually, the Admin SDK might need to fetch the public keys or know project ID. It likely uses the credential to get project ID if not given. But you could probably even initialize without credentials by manually specifying project ID and using `FirebaseTokenVerifier` with public keys... that's too deep. Safer to provide credentials or ensure the environment provides project info.
- However, if you plan on using Admin SDK for other things like setting custom claims or user management in the future, then the service account definitely needs the permissions.

Now both frontend and backend are deployed:

- React app at, say, `myapp.web.app` (or custom domain).
- Spring Boot API at Cloud Run URL or `api.myapp.com`.

### Post-Deployment Configurations (Domains, Environment, Monitoring)

A few final tasks after deployment:

- **Domains & DNS**: If using custom domains, ensure DNS is set correctly. Verify SSL (for Firebase Hosting and Cloud Run custom domain, certificates should be provisioned automatically).
- **Environment Variables**: Double-check that production environment variables (Firebase config in React, service account or project IDs in backend) are correctly pointing to production services. For example, the Firebase config in React should be the production project (not some dev project), otherwise tokens won’t be accepted by the prod backend.
- **Authorized Domains**: We mentioned many times, but confirm that all domains involved are authorized in Firebase Auth:
  - The frontend domain(s) where users load the app.
  - If using any redirect in OAuth that goes through another domain, that too.
  - For email link sign-in, the link’s domain.
    (The backend domain does not need to be in authorized list since it’s not directly doing OAuth).
- **Monitoring & Logging**:
  - Set up Firebase Analytics or at least Monitoring to track sign-in events.
  - Check Cloud Run logs (each request and any errors from our logs or stack traces).
  - Optionally set up alerts for high error rates or for unauthorized attempts.
- **Testing end-user experience**:

  - Try a full sign-up -> email verification (if enabled) -> login -> data fetch cycle as a new user.
  - Try an OAuth login if enabled (Google sign-in popup should work on custom domain if configured properly).
  - Test multi-tenant: e.g., create a user in Tenant A and ensure you cannot use that user’s token on Tenant B's context (should be prevented either by tenant not matching or by being entirely separate backend contexts).

- **Scaling considerations**:
  - If expecting high load, consider using a caching layer for public keys. By default, Firebase Admin SDK caches Google's public keys and they rotate only once a day or so, so it's fine.
  - If using a lot of Admin SDK operations (not just verify), be mindful of Firebase usage limits (for example, if you started using it to fetch user data or update profiles, there are rate limits on those).
- **Secrets rotation drills**:
  - If you deployed using a service account key, simulate updating it: deploy a new version of the service with a new key (or better, switch to using Cloud Run's IAM identity to avoid keys).
  - Ensure that if something like environment variable changes (say you want to point to a new Firebase project for some reason) you know the steps to update config and redeploy.

By following these deployment steps, you have:

- A React app served over a fast CDN with Firebase.
- A Spring Boot REST API running on Google’s infrastructure, auto-scaling and secure.
- Both integrated via Firebase Authentication: tokens issued on the front-end are verified on the backend, all with no custom auth server code needed.

---

## Conclusion

We have successfully created a detailed walkthrough of building a secure, multi-tenant application using Firebase Authentication, a React frontend, and a Spring Boot backend. Let's recap the major points:

- **Firebase Authentication & Multi-Tenancy**: We enabled multi-tenancy in Firebase (Identity Platform) allowing isolation of users per tenant ([
  Solved: Multitenancy with Firebase (Is that possible?) - Google Cloud Community
  ](https://www.googlecloudcommunity.com/gc/Databases/Multitenancy-with-Firebase-Is-that-possible/m-p/637291#:~:text=Yes%2C%20it%20is%20possible%20to,users%2C%20authentication%20methods%2C%20and%20roles)). We learned how to create and manage tenants and ensure the client sets the correct tenant ID for auth operations.
- **OAuth Configuration**: We configured OAuth providers with proper client IDs and redirect URIs. We made sure to add our domains to Firebase’s authorized list to avoid domain mismatch errors ([How I solved Firebase Auth/unauthorized domain. Domain is not authorized error problem using the Vite development tool - DEV Community](https://dev.to/clericcoder/how-i-solved-firebase-authunauthorized-domain-domain-is-not-authorized-error-problem-using-the-vite-development-tool-2md7#:~:text=,console%20for%20your%20project)). This ensures third-party logins (e.g., Google) and email link flows work smoothly.
- **Secure API Design**: We adopted the practice of using Firebase ID tokens for authenticating API requests, sending them via HTTPS and verifying on the server ([reactjs - Firebase Auth, after logging a user from react client, how do I verify user is legitimate within my other api? - Stack Overflow](https://stackoverflow.com/questions/61828463/firebase-auth-after-logging-a-user-from-react-client-how-do-i-verify-user-is-l#:~:text=If%20your%20Firebase%20client%20app,in%20user%20on%20your%20server)). We stressed not exposing secrets, and storing keys securely.
- **React Integration**: On the front-end, we initialized Firebase, handled user sign-up/sign-in (with email/password and Google), and obtained the ID token to include in API calls. We accounted for multi-tenant context by setting the `tenantId` in the Firebase SDK ([Implementing Multi Tenancy with Firebase: A Step-by-Step Guide | KTree | Global IT Services Company](https://ktree.com/blog/implementing-multi-tenancy-with-firebase-a-step-by-step-guide.html#:~:text=To%20sign%20in%20to%20a,not%20persisted%20on%20page%20reloads)).
- **Spring Boot Integration**: On the backend, we used Firebase Admin SDK to verify tokens and integrated it with Spring Security. We wrote a custom filter to authenticate requests by validating JWTs ([Spring Boot REST api authenticating Firebase JWT tokens - Stack Overflow](https://stackoverflow.com/questions/68062611/spring-boot-rest-api-authenticating-firebase-jwt-tokens#:~:text=%2F%2FExtracts%20token%20from%20header%20String,e.toString)), and set up authorization rules using custom claims (roles). We ensured that only authorized users (e.g., admins with the claim) can access certain endpoints.
- **Best Practices**: We compiled best practices including using HTTPS, CORS configuration, least privilege for service accounts, and secure secret management ([API Keys Security & Secrets Management Best Practices - GitGuardian Blog](https://blog.gitguardian.com/secrets-api-management/#:~:text=,lived%20secrets)) ([javascript - Is it safe to expose Firebase apiKey to the public? - Stack Overflow](https://stackoverflow.com/questions/37482366/is-it-safe-to-expose-firebase-apikey-to-the-public#:~:text=You%20guys%20aren%27t%20thinking%20about,you%20should%20be%20using%20GCP)). We considered how to handle keys and credentials, and to monitor and update them.
- **Deployment**: We deployed the frontend on Firebase Hosting (with easy rollback and custom domain support) and the backend on Cloud Run (scalable container service). We configured environment variables and domains such that Firebase Auth continues to work in production. We tested the entire flow in a production-like environment.

By following this guide, an advanced developer can set up a robust authentication system with minimal friction, leveraging the strengths of Firebase for identity management and the flexibility of a custom backend for business logic. The resulting architecture is secure, scalable, and maintainable.

**Next steps** could include implementing refresh token handling (though Firebase SDK covers this), adding more fine-grained roles and permissions in custom claims, setting up unit and integration tests (for example, mock Firebase Admin SDK to test your filter logic), and perhaps integrating other Firebase services (like Firestore) for storing user data with security rules as an extra layer.

All code examples and configurations given are meant as a template and should be adapted to your specific project structure and needs. Security is an ongoing process: keep libraries up to date (e.g., Firebase Admin SDK, Spring Boot), and stay informed about Firebase updates (like new multi-tenancy features or Auth changes).

With this foundation, you can confidently develop and deploy a full-stack application that provides a seamless authentication experience to users while keeping their data safe and separate across multiple tenants.
