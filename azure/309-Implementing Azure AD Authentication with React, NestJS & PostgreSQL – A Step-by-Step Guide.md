# Implementing Azure AD Authentication with React, NestJS & PostgreSQL – A Step-by-Step Guide

## Introduction

In modern applications, integrating **Azure Active Directory (Azure AD)** for authentication and authorization provides a robust and secure identity solution. This guide walks through building a **React** frontend (TypeScript) and a **NestJS** backend connected to a **PostgreSQL** database, all secured via Azure AD using **OAuth2** and **OpenID Connect** protocols. We will use Microsoft’s **MSAL** library for handling authentication on the client side, and NestJS’s **Passport** integration on the server side to validate JSON Web Tokens (JWTs) issued by Azure AD.

The topics covered include: registering and configuring an Azure AD application, setting up the React app with MSAL for login (and token acquisition), building a NestJS API that accepts Azure AD JWTs and implements **role-based access control (RBAC)**, storing user data, sessions, and roles in PostgreSQL, handling **multi-tenant** scenarios (allowing users from multiple Azure AD tenants), applying security best practices (proper token handling, protecting API routes), deploying the application (to Azure or via Docker containers), and testing/debugging common issues in the authentication flow. Each section provides clear steps, code examples, and explanations aimed at advanced developers, with an emphasis on production-ready configuration.

_Note:_ This guide assumes familiarity with the basics of React and NestJS. We focus on the integration specifics for Azure AD authentication. All code is in **TypeScript**, and we use **Markdown** headings, lists, and short paragraphs for clarity.

## 1. Understanding Azure AD, OAuth2, and OpenID Connect

**Azure AD** is Microsoft’s cloud identity provider, supporting industry-standard protocols **OAuth 2.0** for authorization and **OpenID Connect (OIDC)** for authentication. In essence, your application will redirect users to Azure AD to sign in, and Azure AD will issue tokens that your application can use to identify the user and authorize requests. Let’s clarify the key concepts and components:

- **OAuth2 vs OpenID Connect:** OAuth2 is a protocol for authorization (granting third-party apps access to user data), while OpenID Connect is an identity layer on top of OAuth2 for authentication (letting the app confirm user identity) ([Part 5: OpenID Connect (OIDC) with Azure AD | by Shoaib Alam](https://medium.com/@shoaib.alam/part-5-openid-connect-oidc-with-azure-ad-dfa34cf9c747#:~:text=OpenID%20Connect%20or%20OIDC%20is,all%20concepts%2C%20flows%2C%20endpoints%2C)). Azure AD implements both: your app uses OAuth2 flows to get tokens, and OIDC to get user identity details.

- **Tokens:** Azure AD issues **JWT bearer tokens** ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=The%20parties%20in%20an%20authentication,JWT)) that the React app and NestJS API will use. There are mainly two types of tokens in this flow ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Access%20tokens%20,granted%20by%20the%20authorization%20server)):

  - **ID Token:** Represents the user’s identity (contains user information like name, email, etc.). It is used in OIDC for user **authentication** (sign-in).
  - **Access Token:** Grants access to a protected resource (like your API). It contains **permissions (scopes)** that the client has been granted and is used for **authorization** when calling the backend API.
  - (Additionally, Azure AD can issue **Refresh Tokens** to obtain new tokens when the current ones expire ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=client%20application,get%20basic%20information%20about%20them)). MSAL handles refresh tokens automatically, so you typically won’t manage them manually in a SPA.)

- **Azure AD App Registration:** To use Azure AD, you must register your application in the Azure AD tenant. App registration gives you a **Client (Application) ID** (a unique GUID) and lets you configure authentication settings (allowed redirect URIs, supported account types, API permissions, etc.) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=Your%20client%20app%20needs%20a,based%20on%20the%20application%27s%20type)) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Redirect%20URI%20,client%20types%20use%20redirect%20URIs)). In a single-tenant app, only users from your organization can sign in; in a multi-tenant app, users from any Azure AD tenant can sign in (after consenting to your app). We’ll discuss multi-tenancy later.

- **Microsoft Authentication Library (MSAL):** Microsoft provides MSAL libraries for handling OAuth2/OIDC flows in applications. **MSAL** simplifies retrieving tokens and managing user sessions in the client, so you **don’t have to craft raw HTTP requests** to OAuth endpoints ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=We%20strongly%20advise%20against%20crafting,implementation%2C%20we%20have%20protocol%20reference)). We will use **@azure/msal-react** (built on **@azure/msal-browser**) on the React side, which implements the OAuth2 **Authorization Code flow with PKCE** under the hood (a secure flow suitable for SPAs). On the server, we’ll use the **passport-azure-ad** strategy for NestJS to validate incoming JWTs. Using these libraries is recommended for safety and ease ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=We%20strongly%20advise%20against%20crafting,implementation%2C%20we%20have%20protocol%20reference)).

**Authentication Flow Overview:** In this architecture, the flow works as follows:

1. **User Login (React & Azure AD):** The user clicks “Login” in the React app. MSAL redirects the user to Azure AD’s login page. After successful login (and consent if needed), Azure AD sends the user back to your app’s redirect URL with an **authorization code**. MSAL then exchanges this code for tokens (ID token for user info, and an access token for your API). The tokens are stored in the MSAL library (in memory or session storage).

2. **API Call with Access Token:** The React app now has an access token that proves the user’s identity and permissions. When calling your NestJS backend (for example, to fetch user profile or any protected data), the React app attaches the access token in the HTTP Authorization header: `Authorization: Bearer <token>`.

3. **Token Validation (NestJS):** The NestJS backend, on receiving a request with a Bearer token, uses a **Passport strategy** to validate the JWT. It checks the token’s signature (using Azure AD’s public keys), issuer, audience, and expiration. If the token is valid and not expired, the request is authenticated – the user’s identity (claims) is now available to the backend. The backend can then perform **authorization**: e.g., checking if the user’s role (from token claims or database) allows access to the requested resource.

4. **Access Granted/Denied:** If authentication or authorization fails, the API returns 401 Unauthorized or 403 Forbidden. If it succeeds, the API executes the requested operation and returns data to the frontend.

Throughout this process, Azure AD handles the heavy lifting of authenticating users (e.g., verifying passwords, 2FA, etc.) and issuing tokens. Our focus will be on configuring Azure AD correctly and writing our app to consume those tokens properly.

## 2. Azure AD Configuration – App Registration and Permissions

Before writing any code, we need to configure an **Azure AD application registration** that represents our frontend (and optionally our backend API). This involves a few steps in the Azure Portal:

### 2.1 Register the Application in Azure AD

1. **Create a new App Registration:** Sign in to the Azure Portal and go to **Azure Active Directory > App Registrations**, then choose **New registration**. Give the application a name (e.g., “MySaaSApp”) and specify who can use it:
   - For a single-tenant app (only your org): choose **Accounts in this organizational directory only**.
   - For a multi-tenant app (SaaS for any org): choose **Accounts in any organizational directory** ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-registration-to-be-multi-tenant#:~:text=By%20default%2C%20web%20app%2FAPI%20registrations,Accounts%20in%20any%20organizational%20directory)). (Multi-tenant means users from any Azure AD tenant can sign in after consenting ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-registration-to-be-multi-tenant#:~:text=If%20you%20offer%20a%20Software,their%20account%20with%20your%20application)).)
2. **Redirect URI:** Under **Redirect URI**, choose “Web” or “SPA” and enter your frontend URL that will handle logins (for development, e.g., `http://localhost:3000`). This must match exactly the URL your React app will use for MSAL redirect handling. Azure AD will redirect users here after sign-in.
3. **Finish Registration:** Click Register. Azure will assign an **Application (Client) ID** (copy this GUID, as you’ll use it in your React app configuration). Also note the **Directory (Tenant) ID** if your app is single-tenant (for multi-tenant, we will generally use `'common'` as tenant in the client, but you’ll still use the tenant ID on the backend for issuer validation).

Now you have an Azure AD app. Next, configure it for the tokens and permissions we need.

### 2.2 Configure Authentication and API Permissions

After registration, in the Azure AD portal for your app:

- **Enable ID Tokens and Access Tokens:** In the app’s **Authentication** blade, find the section for “Implicit grant and Hybrid flows” (if applicable) and ensure **ID tokens** and **Access tokens** are enabled. This allows the app to receive ID and access tokens in the SPA flow. (For authorization code flow with PKCE, these settings might not be explicitly required, but ensuring access token issuance is important.)

- **Expose an API (Define Scope):** If your app will provide a custom API (the NestJS backend), you should define a scope for it:

  1. In **Expose an API**, set an Application ID URI if not already set (or use the default which is `api://<client-id>`).
  2. Click **Add a scope**. For example, create a scope name “`API.Access`” (or “access_as_user”). Give admin consent description, and who can consent (choose “Admins and users” if users can consent to this scope). This defines a permission that clients (including your own SPA) can request to call the API ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=4,the%20permissions%20for%20your%20API)).
  3. Remove any default scopes you don’t need. By default, Azure AD might include the **Microsoft Graph** user.read permission for a new app. If you are not using Microsoft Graph in your app, remove it under **API permissions** to avoid unnecessary consent prompts and to **avoid token validation issues** (for example, having Graph permission can sometimes result in an access token with multiple audiences which could complicate validation) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=,Access%20token)).

- **API Permissions (for client app):** Now, if you created a custom scope above, you need to **grant your own client app access to it**. Under **API Permissions**:

  1. Click **Add a permission**, choose **My APIs** (if using the same app registration, it might be listed there), and select the scope you just created (e.g., `API.Access`). Add it as a **delegated permission**.
  2. Click **Grant admin consent** for your tenant (if you have admin rights), so that users won’t individually need to consent for your app’s own API. (In multi-tenant scenario, users from other tenants will see a consent screen unless their admin pre-consents – more on that later.)
  3. If you plan to call Microsoft Graph or other APIs, add the necessary delegated permissions as well. Otherwise, your custom scope is enough.

- **Client Secret (Optional):** For SPAs, you typically **do not use a client secret**, because the frontend code cannot securely hold a secret. If you were building a server-side app or a confidential client (like an API needing to call Azure AD), you would create a client secret or certificate. In our setup, the NestJS API will **not** directly call Azure AD to exchange tokens (it will only validate tokens), so we do **not** need a client secret for our main scenario. (However, if you wanted the backend to also act as an OAuth2 client – for example, to call Azure AD on behalf of the user or use client credentials – you’d generate a secret in **Certificates & Secrets** and use it server-side. We’ll omit that here.)

At this point, the Azure AD app is configured to issue ID tokens and access tokens for our own API. We have the **Client ID** (for MSAL in React), the **Tenant ID** (for building authority URLs and backend validation), and a defined **scope** (our API permission). We’re ready to set up the frontend.

## 3. Setting Up the React Frontend (TypeScript) with MSAL for Authentication

Our React application will use the **@azure/msal-react** library to integrate Azure AD authentication. MSAL will handle redirecting to Azure AD, processing the OIDC response, storing tokens, and providing authentication state to our React components. Let’s go step by step:

### 3.1 Initialize a React Project (if not already done)

If you don’t have a React app set up, create one with TypeScript. For example:

```bash
npx create-react-app my-app --template typescript
cd my-app
```

This will create a baseline React application in TypeScript. We will then install MSAL and configure it.

### 3.2 Install MSAL libraries

In your React project, install the MSAL packages:

```bash
npm install @azure/msal-react @azure/msal-browser
```

The `@azure/msal-react` package is the React wrapper, and `@azure/msal-browser` is the core library for browser-based auth. (The latter is a peer dependency that enables auth in SPA without a backend) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=The%20first%20package%20%E2%80%94%20%60%40azure%2Fmsal,without%20using%20a%20backend%20server)).

### 3.3 Configure MSAL and Wrap the App

Create an MSAL configuration and initialize the MSAL **PublicClientApplication** instance. A good place for this is in a file like `src/authConfig.ts` (or directly in your `index.tsx`/`App.tsx`). For example:

```tsx
// src/authConfig.ts
import { Configuration } from "@azure/msal-browser";

const tenantId = "<Your_Tenant_ID_or_common>"; // e.g., "contoso.onmicrosoft.com" or a GUID, or "common" for multi-tenant
export const msalConfig: Configuration = {
  auth: {
    clientId: "<Your_AzureAD_Client_ID>",
    authority: `https://login.microsoftonline.com/${tenantId}`,
    redirectUri: "http://localhost:3000", // must match Azure AD app's redirect URI
    postLogoutRedirectUri: "http://localhost:3000", // where to navigate after logout (optional)
  },
};
```

A few notes on this configuration:

- **clientId** is the Application (client) ID from Azure AD.
- **authority** is the URL of the Azure AD tenant or the common endpoint. For a single-tenant app, use your Tenant ID or domain in the URL (e.g., `https://login.microsoftonline.com/<tenant-id>`). For multi-tenant (our case if we selected “any org directory”), you typically use the `/common` endpoint to allow all tenants ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=To%20specify%20the%20audience%20in,common)). This authority URL points MSAL to the Azure AD endpoint for authentication.
- **redirectUri** is where the app will handle the response. In development it’s typically the local URL; in production, it will be your actual domain. It must exactly match one of the redirect URIs in Azure AD app registration.
- **postLogoutRedirectUri** is optional, it’s where Azure AD will redirect after a logout, often back to your homepage.

Now, initialize MSAL and wrap your application with the **MsalProvider** (which uses React Context to make authentication state available throughout the app):

```tsx
// src/index.tsx or src/main.tsx (depending on your setup)
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
  <MsalProvider instance={msalInstance}>
    <App />
  </MsalProvider>
);
```

We created a `PublicClientApplication` with our config, then used `MsalProvider` to wrap the `<App />` component ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=match%20at%20L188%20,MsalProvider)) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=import%20,browser)). This means any component in our app can now use MSAL hooks or components to respond to auth state.

### 3.4 Implementing the Login Flow

Next, in your React app interface, you need a way for users to sign in and sign out, and perhaps to display if they are authenticated. MSAL-react provides some convenience:

- **Hooks and Components:** You can use the `useMsal()` hook to get the MSAL instance and `accounts` info, and `useIsAuthenticated()` to get a boolean of auth status. There are also `<AuthenticatedTemplate>` and `<UnauthenticatedTemplate>` components that conditionally render children based on auth state (these can simplify showing a login button vs. logged-in content) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=In%20this%20article%2C%20we%20are,We%20will%20cover)) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=,26)).

For example, you might create a `LoginButton` component:

```tsx
import { useMsal } from "@azure/msal-react";

export const LoginButton: React.FC = () => {
  const { instance } = useMsal();
  const handleLogin = () => {
    instance.loginRedirect(); // Redirects to Azure AD
    // Alternatively, instance.loginPopup() to open a pop-up instead of full redirect
  };

  return <button onClick={handleLogin}>Sign In</button>;
};
```

This uses the `loginRedirect()` method to initiate the redirect flow ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=const%20initializeSignIn%20%3D%20%28%29%20%3D,loginRedirect%28%29%3B)). You could also configure it to request specific scopes if you want the access token for your API right away, e.g.:

```ts
instance.loginRedirect({ scopes: ["api://<your-client-id>/<scope>"] });
```

If you don't request the API scope on initial login, you can always acquire the token later (we’ll show that in the API call section).

After login, MSAL will handle the redirect back to your app (at `redirectUri`) and store the tokens. The user will now be considered “authenticated” in the context of MSAL.

To display user info or a logout button, you can use MSAL hooks:

```tsx
import { useIsAuthenticated, useMsal } from "@azure/msal-react";

const Navbar: React.FC = () => {
  const isAuthenticated = useIsAuthenticated();
  const { instance, accounts } = useMsal();

  const handleLogout = () => {
    instance.logoutRedirect();
  };

  return (
    <nav>
      {isAuthenticated ? (
        <>
          <span>Welcome, {accounts[0]?.username}!</span>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <button onClick={() => instance.loginRedirect()}>Login</button>
      )}
    </nav>
  );
};
```

Here, `accounts[0]` would contain the currently signed-in account (with username or email). We call `logoutRedirect()` to log the user out (which clears MSAL cache and redirects to Azure AD to sign out).

### 3.5 Calling the Protected API with the Access Token

Once the user is logged in, we want to call our NestJS API. Our API requires a valid access token in the header. With MSAL, obtaining the access token can be done in two ways:

- If you requested the API scope during the initial login (in `loginRedirect`), MSAL should have an access token in its cache already.
- If not (or if you need to refresh it), you use `instance.acquireTokenSilent` to get a token for a given scope.

Assuming we have defined a scope (e.g., `api://<client-id>/API.Access`), here’s how to retrieve the token and call the API:

```tsx
import axios from "axios";
import { useMsal } from "@azure/msal-react";

const fetchDataFromApi = async () => {
  const { instance, accounts } = useMsal();
  if (accounts.length === 0) {
    throw new Error("User is not logged in");
  }
  const account = accounts[0];
  // Request token for our API scope
  const response = await instance.acquireTokenSilent({
    account: account,
    scopes: ["api://<your-client-id>/API.Access"], // the scope for your API
  });
  const accessToken = response.accessToken;
  // Now call the API with the token
  const apiResponse = await axios.get(
    "http://localhost:4000/api/your-endpoint",
    {
      headers: { Authorization: `Bearer ${accessToken}` },
    }
  );
  return apiResponse.data;
};
```

Here we use `acquireTokenSilent` which will return a cached token if not expired or automatically refresh it using the hidden iframe/refresh token, without user interaction. If silent acquisition fails (e.g., if no refresh token or it’s the first time requesting that scope), you might need to fallback to `loginRedirect` or `acquireTokenPopup` for that scope which will prompt the user to consent. But in our case, since it’s our own API and we granted permission, silent should work after initial login.

The important part is attaching `Authorization: Bearer <token>` header in the API request. The backend will inspect this header for authentication.

**Protected Routes in React:** If your React app has client-side routing and you want to restrict certain routes to authenticated users, you can use the state from MSAL to conditionally render those routes. For example, using `useIsAuthenticated()` to decide whether to render a `<Route>` or redirect to login. MSAL’s `<AuthenticatedTemplate>` is another convenient way: any content inside it only renders if a user is signed in, whereas `<UnauthenticatedTemplate>` content shows only when not signed in ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=In%20this%20article%2C%20we%20are,We%20will%20cover)). This way, you can protect UI elements, but remember that real security is enforced in the backend (since front-end can be bypassed).

### 3.6 MSAL Configuration Tips (Advanced)

MSAL offers additional configuration options. For instance, the **cache** location (default is sessionStorage for SPAs, which is safer than localStorage to mitigate persistent XSS token theft). You can configure `cache: { cacheLocation: "sessionStorage", storeAuthStateInCookie: false }` if needed. Using sessionStorage means the user will need to log in again if they close the browser, but it’s more secure than localStorage ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=Storing%20JWTs%20in%20cookies%20configured,improves%20security%20by%20making%20it)). If you want “remember me” functionality, you might choose localStorage but be aware of the security trade-off.

Also, consider setting `authority` to the specific tenant ID if you want to restrict logins to a single tenant, or use `common`/`organizations` for multi-tenant. In multi-tenant scenarios, you may also want to add `prompt: "select_account"` or similar in the login request to ensure the user can choose or use their specific account.

At this point, our React app can log in users via Azure AD and acquire tokens. Next, we focus on the backend: validating those tokens and implementing authorization.

## 4. Building the NestJS Backend – Authentication and Authorization

Our NestJS backend will serve protected APIs and verify the Azure AD tokens presented by clients. We will use **Passport**, a popular authentication middleware, with the **passport-azure-ad** strategy (which knows how to validate Azure AD JWTs). NestJS has great Passport integration via the `@nestjs/passport` package.

### 4.1 Setting Up the NestJS Project

Initialize a NestJS project if you haven’t:

```bash
nest new my-api
```

Choose npm or yarn as you prefer. After installation, add the required auth packages:

```bash
npm install @nestjs/passport passport passport-azure-ad jsonwebtoken
```

- `passport-azure-ad` provides strategies for Azure AD (we will use the **BearerStrategy**, which validates JWT access tokens issued by Azure AD).
- `@nestjs/passport` integrates Passport into Nest.
- We also include `jsonwebtoken` (which is a dependency of passport-azure-ad or for potential direct JWT handling).

Now, let’s configure a **Passport strategy** in NestJS.

### 4.2 Azure AD Bearer Strategy for NestJS

Create a new file, e.g., `src/auth/azure-ad.strategy.ts`. We will implement a custom strategy by extending PassportStrategy with Azure AD’s BearerStrategy:

```ts
// src/auth/azure-ad.strategy.ts
import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { BearerStrategy, IBearerStrategyOption } from "passport-azure-ad";

@Injectable()
export class AzureADStrategy extends PassportStrategy(
  BearerStrategy,
  "azure-ad"
) {
  constructor() {
    super({
      identityMetadata: `https://login.microsoftonline.com/${process.env.AZURE_AD_TENANT_ID}/v2.0/.well-known/openid-configuration`,
      clientID: process.env.AZURE_AD_CLIENT_ID,
      issuer: `https://login.microsoftonline.com/${process.env.AZURE_AD_TENANT_ID}/v2.0`, // issuer URL base
      audience: process.env.AZURE_AD_AUDIENCE || process.env.AZURE_AD_CLIENT_ID,
      validateIssuer: true,
      loggingLevel: "info",
      passReqToCallback: false,
      // Other options: you could add scope here if you want to check a specific scope, etc.
    } as IBearerStrategyOption);
  }

  async validate(payload: any) {
    // This function is called after token is validated. 'payload' is the JWT claims.
    // Here you can implement additional validation or fetch user info from DB.
    return payload; // For now, we just return the token claims as the user object.
  }
}
```

Let’s break down the important parts of this configuration:

- **identityMetadata:** This is the URL to Azure AD’s OIDC metadata document for your tenant (or common). It includes the public keys for token signatures, issuer information, etc. We use the tenant ID here. If your app is multi-tenant, you have a choice: you could use a specific tenant (which means only tokens from that tenant are accepted), or use the `common` or `organizations` endpoint to accept tokens from any tenant. For multi-tenant acceptance, you might set `identityMetadata: https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration` and then set `validateIssuer: false` to allow multiple issuers. The Microsoft documentation notes that multi-tenant apps need to handle multiple issuer values ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=Multitenant%20applications%20must%20perform%20more,more%20information%2C%20see%20Validate%20tokens)). In our example, we use a specific tenant and `validateIssuer: true` (good for single-tenant or known tenants). We’ll discuss multi-tenant handling in a later section.

- **clientID:** The Azure AD client ID (GUID). This should match the token’s audience claim if the token is meant for this app. We load it from environment for security (never hard-code secrets or IDs in code for production).

- **issuer:** (Optional) The expected issuer URL of tokens. In Azure AD v2 endpoint, issuer will be `https://login.microsoftonline.com/{tenantId}/v2.0`. By specifying it, we ensure tokens from any other issuer are rejected. In multi-tenant (`common`) scenario, you might not set a fixed issuer but rather allow Azure’s common/organizations issuers and then check the token’s `tid` claim if needed. The strategy can be configured to accept multiple issuers if validateIssuer is false or through the metadata. Here we set it for single-tenant for illustration ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=identityMetadata%3A%20%60https%3A%2F%2F%24,loggingLevel)).

- **audience:** What audience the token must have. Often this is the client/application ID, or the App ID URI. In our case, since our SPA and API share the registration, the access token’s `aud` will likely be the client ID (unless a custom audience was set). We allow both by using an environment variable (some use `AZURE_AD_AUDIENCE` for API identifier). Commonly, setting audience to the client ID is enough ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=issuer%3A%20%60https%3A%2F%2F%24,validateIssuer)).

- **validateIssuer:** true/false to enforce the issuer match. We set true for security in single-tenant mode ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=%7D%2C%20settings%3A%20,scope%20of%20your%20azure%20AD)) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=issuer%3A%20%60https%3A%2F%2F%24,passReqToCallback)). If multi-tenant, you might set this to false, in which case any Azure AD issuer that matches the metadata endpoints will be allowed (you’d then manually check the `tid` claim in validate function to restrict if needed).

- **loggingLevel:** we set to 'info' (you can set 'warn' or 'error' to reduce verbosity, or 'info'/'verbose' for more detail during debugging). There’s also an option `loggingNoPII` – if set to false, it will include details in logs. In production, leaving `loggingNoPII` as true (default) is better to avoid sensitive info in logs.

- **passReqToCallback:** set to false because we don’t need the raw `req` in the validate callback. (If you wanted to access the request in validate, you’d set this true and adjust the validate signature).

- **scope:** (Optional) You can specify an array of scopes that the token must have to be considered valid. For instance, if you only want tokens that include your custom API scope, you could put `scope: ["API.Access"]` (the name of your scope). Our example omitted it, which means any valid token for this audience is accepted. Adding a scope requirement is an extra authorization check at the strategy level. If you expect the token to always have a specific scope, you can use it. (In our case, if the SPA requested our `API.Access` scope, the access token will have a `scp` claim containing it. We could validate that here.) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=loggingLevel%3A%20%27info%27%2C%20,scope%20of%20your%20azure%20AD)) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=loggingLevel%3A%20config,false%2C)).

The `validate(payload: any)` function is called once the token is verified. The `payload` is the JWT’s decoded claims (for example, it will include `oid` (object ID of user), `name`, `preferred_username` or `unique_name` (user email), `tid` (tenant ID), `scp` (scopes) or `roles` if any app roles were assigned, etc.). In the simple case above, we just return the payload, which will attach it as `req.user` in NestJS. Typically, here you might:

- Check if the user exists in your database, or create them if first login.
- Map token claims to a user object (e.g., find user by Azure AD `oid` and return a User entity).
- If using roles from DB, you might fetch the user’s roles here and attach to the user object.
- If you want to reject certain conditions (e.g., user not in your DB or disabled), you could throw an exception to deny access.

For example:

```ts
async validate(payload: any): Promise<User> {
  const { oid, name, preferred_username, tid } = payload;
  const user = await this.userService.findByAzureId(oid);
  if (!user) {
    // Optionally auto-register the user in our DB
    const newUser = await this.userService.create({ azureId: oid, name, email: preferred_username, tenantId: tid });
    return newUser;
  }
  return user; // return user entity (with roles etc.)
}
```

This would ensure `req.user` in controllers is a fully-fledged User object from our database. For brevity, we won’t implement the full userService here, but this is a common pattern.

Now we need to hook this strategy into Nest’s module system and protect routes.

### 4.3 NestJS Auth Module and Guard

NestJS uses guards to protect routes. Passport provides an **AuthGuard** class that wraps our strategy. Since we named the strategy 'azure-ad', we can use an `AuthGuard('azure-ad')`. We can either create a custom guard class or use the generic one directly in controllers.

First, set up an Auth module to provide the strategy:

```ts
// src/auth/auth.module.ts
import { Module } from "@nestjs/common";
import { PassportModule } from "@nestjs/passport";
import { AzureADStrategy } from "./azure-ad.strategy";

@Module({
  imports: [
    PassportModule.register({ defaultStrategy: "azure-ad" }), // register passport with our strategy as default (optional)
  ],
  providers: [AzureADStrategy],
  exports: [PassportModule, AzureADStrategy],
})
export class AuthModule {}
```

We import `PassportModule.register` to configure the default strategy. Now Nest knows about our AzureADStrategy.

In your main AppModule (or whatever module houses your controllers that need auth), import this AuthModule:

```ts
// src/app.module.ts
import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module'; // etc.

@Module({
  imports: [AuthModule, UsersModule, ...],
  controllers: [AppController, ...],
  providers: [AppService, ...],
})
export class AppModule {}
```

Now, in any controller, we can use the `AuthGuard('azure-ad')` to protect routes. For example:

```ts
// src/users/users.controller.ts
import { Controller, Get, UseGuards, Req } from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";

@Controller("users")
export class UsersController {
  @Get("me")
  @UseGuards(AuthGuard("azure-ad"))
  getMe(@Req() req) {
    // Only authenticated users with a valid token reach here
    return req.user; // this is the token claims or user object from validate()
  }
}
```

By using `@UseGuards(AuthGuard('azure-ad'))` on the route, NestJS will automatically invoke our AzureADStrategy to validate the token before entering the handler ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=export%20class%20AppController%20,)). If the token is missing or invalid, Nest will return a 401 Unauthorized response; the controller method won’t execute. If valid, `req.user` will contain the payload we returned in `validate()`.

We can also apply the guard globally (affecting all controllers) by using `app.useGlobalGuards(new (AuthGuard('azure-ad'))());` in main.ts or a custom provider. But typically, you might only protect certain routes or use a mix (global guard for most, plus allow an exceptions list for public routes). For simplicity, using `@UseGuards` per controller or route is clear.

**Testing the Setup (manually):** If you run your NestJS server (e.g., on `http://localhost:4000`) and try accessing a protected route without a token, you should get 401. If you attach the Authorization header with a valid Azure AD token (obtained via the React app/MSAL), you should get a response. We’ll integrate this with the frontend in end-to-end usage.

So far, we have a working authentication on the backend: Azure AD JWTs are accepted and verified. Next, we integrate a database to store user details, roles, etc.

## 5. Integrating PostgreSQL – Storing Users, Sessions, and Roles

Using a database is important for many reasons: you may want to persist additional user information (profile details, application-specific settings), implement your own roles/permissions, or track user sessions/logins. **PostgreSQL** is an excellent choice for reliability and relational data. We’ll use an ORM (TypeORM) with NestJS for simplicity in managing data.

### 5.1 Setting up TypeORM with NestJS and PostgreSQL

Install the necessary packages in the NestJS project:

```bash
npm install @nestjs/typeorm typeorm pg
```

The `pg` package is the PostgreSQL driver.

In your NestJS AppModule (or a separate DatabaseModule), configure TypeORM to connect to your Postgres database:

```ts
import { TypeOrmModule } from '@nestjs/typeorm';

// ... inside @Module imports array:
TypeOrmModule.forRoot({
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: Number(process.env.DB_PORT) || 5432,
  username: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASS || 'postgres',
  database: process.env.DB_NAME || 'myappdb',
  synchronize: true,  // auto-migrate entities; turn off in production and use migrations
  logging: false,
  entities: [__dirname + '/**/*.entity{.ts,.js}'],
}),
```

This uses environment variables for credentials (never store passwords in code; in dev you might use a .env file). The `synchronize: true` will automatically create database tables based on our entity classes – convenient for development, but in production consider using explicit migrations. We set `entities` path to include any file ending with `.entity.ts` or `.entity.js`.

Now, define some entities. Let’s create a `User` entity and a `Role` entity for RBAC:

```ts
// src/users/user.entity.ts
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToMany,
  JoinTable,
} from "typeorm";
import { Role } from "../auth/role.entity";

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  azureId: string; // Azure AD Object ID (sub/oid claim)

  @Column()
  email: string;

  @Column()
  name: string;

  @Column({ nullable: true })
  tenantId: string; // Azure AD Tenant ID (for multi-tenant scenarios)

  @ManyToMany(() => Role, (role) => role.users, { eager: true })
  @JoinTable({ name: "user_roles" }) // join table name
  roles: Role[];
}
```

```ts
// src/auth/role.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm";
import { User } from "../users/user.entity";

@Entity()
export class Role {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  name: string; // e.g., 'admin', 'user', 'manager'

  @ManyToMany(() => User, (user) => user.roles)
  users: User[];
}
```

Here, a `User` can have multiple roles and a `Role` can belong to many users (many-to-many relationship with a join table `user_roles`). We store the user’s Azure AD unique ID (`azureId` which corresponds to the `oid` claim in the token) and possibly the tenant ID (`tid` claim) if multi-tenant. We also store basic info like email and name for reference.

You might also want a separate table for “permissions” or a mapping of roles to permissions if doing fine-grained access control, but for this guide, roles are sufficient. (A comprehensive RBAC system might include tables for permissions and link roles to permissions ([Designing RBAC Permission System with Nest.js: A Step-by-Step Guide - DEV Community](https://dev.to/leapcell/designing-rbac-permission-system-with-nestjs-a-step-by-step-guide-3bhl#:~:text=,relationship%20between%20roles%20and%20permissions)), but we’ll keep it simpler.)

Now, import these entities in the TypeOrmModule. In your AppModule (or a dedicated Entities module):

```ts
imports: [
  // ... other modules,
  TypeOrmModule.forFeature([User, Role])
],
```

This makes repository providers for User and Role available via Nest’s DI (or you can use TypeORM’s Repository in services by injection).

### 5.2 Using the Database in Auth Flow

With the DB in place, how do we integrate it? One typical approach: in the **validate** function of our AzureADStrategy, we can use a UserRepository or UserService to find or create a User in our DB corresponding to the Azure AD identity. For example:

```ts
// Pseudocode modification in AzureADStrategy.validate:
async validate(payload: any): Promise<any> {
  const userRepo = /** inject repository via constructor in strategy class **/;
  const azureId = payload.oid || payload.sub;  // Azure AD Object ID (in v2 tokens it's 'oid')
  let user = await userRepo.findOne({ where: { azureId }, relations: ['roles'] });
  if (!user) {
    // Create new user record if first time seeing this Azure AD user
    user = userRepo.create({
      azureId,
      email: payload.preferred_username || payload.email || '',
      name: payload.name || payload.unique_name || '',
      tenantId: payload.tid || null
    });
    // Assign default roles if needed, e.g., everyone gets 'user' role:
    const defaultRole = await roleRepo.findOne({ where: { name: 'user' } });
    user.roles = defaultRole ? [defaultRole] : [];
    await userRepo.save(user);
  }
  // Optionally, update user's name/email if they changed in AD:
  // (user.name = payload.name, etc., then save)
  return user;
}
```

This way, `req.user` will be an instance of our User entity (with roles eagerly loaded). Then we can use Nest’s authorization mechanisms (like guards) to check `req.user.roles`. We’ll incorporate this in the RBAC section.

One important note: if you plan to use **session cookies** on the server side (instead of JWT for each request), you could store a session record in DB. However, in this JWT setup, we are stateless – we don’t use server sessions for API calls (the JWT itself is the credential each time). The mention of “sessions” could also refer to storing a refresh token or login session info. For example, if you had a longer user session concept, you might keep track of last login time or maintain an application session token. With pure JWT, that’s not needed on the server (the client manages it).

However, if you wanted to implement logout across devices or token revocation, you could keep a list of active JWT IDs or a blacklist in the DB and check against it on each request. That’s an advanced token revocation strategy (not required by default because JWTs expire and you might rely on expiration). We won’t implement that fully here, but it’s something to consider for complete session management.

Given our approach, storing the user and their roles is the primary use of PostgreSQL. We also have a Role table that can be managed via some admin interface or migration (you could insert roles like 'admin', 'user' initially).

We will now discuss RBAC implementation using those roles.

## 6. Advanced Authorization: RBAC (Role-Based Access Control) and Multi-Tenancy

With authentication in place, we move to **authorization** – determining what actions an authenticated user is allowed to perform. Two advanced requirements often arise: implementing role-based access control (RBAC) and supporting multi-tenant scenarios. Let’s address each:

### 6.1 Role-Based Access Control (RBAC)

RBAC means each user is assigned one or more roles (e.g., _User_, _Admin_, _Manager_), and permissions are granted to roles rather than individuals. We have set up a roles relationship in our database. We now enforce role checks in our NestJS application.

**Designing Roles and Permissions:** In our simple model, roles might be enough. In more complex systems, roles are often combined with granular permissions (for example, a “Document Editor” permission that can be assigned to roles). A typical RBAC schema might include separate tables for Users, Roles, Permissions, and join tables for User-Role and Role-Permission relationships ([Designing RBAC Permission System with Nest.js: A Step-by-Step Guide - DEV Community](https://dev.to/leapcell/designing-rbac-permission-system-with-nestjs-a-step-by-step-guide-3bhl#:~:text=,relationship%20between%20roles%20and%20permissions)). Our design above aligns with a simplified version (we have User, Role, and an implicit user_role join; we could introduce a Permission entity and a role_permission join if needed).

For our purposes, assume roles are sufficient to guard routes. For example, only users with the "admin" role can access certain admin APIs.

**Implementing a Roles Guard:** NestJS provides an example of using custom decorators and guards for roles ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=)) ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=export%20enum%20Role%20,user%27%2C%20Admin%20%3D%20%27admin%27%2C)). We can create a `Roles` decorator and a `RolesGuard` as follows:

```ts
// src/auth/roles.decorator.ts
import { SetMetadata } from "@nestjs/common";
export const ROLES_KEY = "roles";
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);
```

```ts
// src/auth/roles.guard.ts
import { CanActivate, ExecutionContext, Injectable } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { ROLES_KEY } from "./roles.decorator";
import { User } from "../users/user.entity";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(
      ROLES_KEY,
      [context.getHandler(), context.getClass()]
    );
    if (!requiredRoles) {
      return true; // no roles required for this route
    }
    const { user } = context.switchToHttp().getRequest<{ user: User }>();
    if (!user) return false;
    const userRoles = user.roles?.map((r) => r.name) || [];
    // Check if any of the user's roles is in the requiredRoles
    return requiredRoles.some((role) => userRoles.includes(role));
  }
}
```

We use `Reflector` to get metadata set by the `@Roles()` decorator on the route ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=match%20at%20L322%20canActivate%28context%29%20,context.getHandler%28%29%2C%20context.getClass)). If the route (or controller class) has `@Roles('admin')`, then `requiredRoles` will be `['admin']`. The guard then checks the `user` attached to the request and sees if that user’s roles include the required one. We assume `req.user` is an instance of our User entity, so `user.roles` is an array of Role objects; we map to their names for comparison.

To use this guard, you register it (e.g., in AuthModule providers) and then apply it either globally or to specific controllers. For instance, at a controller:

```ts
@Controller("admin")
@UseGuards(AuthGuard("azure-ad"), RolesGuard)
export class AdminController {
  @Get("reports")
  @Roles("admin") // only admin role can access
  getReports() {
    // ...
  }
}
```

Here we used both `AuthGuard('azure-ad')` and `RolesGuard`. The order can matter – typically you want the JWT AuthGuard to run first (authenticate and attach user), then the RolesGuard to authorize. In NestJS, multiple guards on a controller will all run; if any returns false, the request is denied. The RolesGuard will see `req.user` from the AuthGuard.

We could also make a combined guard or use `@UseGuards(RolesGuard)` at a higher level (even globally) if we ensure it always finds the Roles metadata (if none, it passes all as above). Alternatively, apply `RolesGuard` only on routes that have roles restrictions.

Also note, **Azure AD App Roles**: Azure AD itself has an app roles feature where you can define roles in the app registration and assign users or groups to those roles in the Azure AD tenant. If configured, Azure AD will include a `roles` claim in the token (an array of role names or IDs). We could leverage that instead of storing roles in our DB. For example, if our app registration has roles "Admin" and "User" and a user is assigned "Admin", the JWT’s `roles` claim might be `["Admin"]`. We could then simply read `payload.roles` in our strategy and map that to an internal roles list. This approach delegates role management to Azure AD (which might be desirable in enterprise scenarios). However, in a multi-tenant SaaS, app roles would need to be assigned in each tenant by that tenant’s admin, which might or might not be practical. For flexibility, we often maintain roles in the app database (plus it allows roles that are not global – e.g., tenant-specific roles).

Our guide proceeds with roles in the database. If you prefer Azure AD app roles, you could adjust by reading token’s roles claim in the guard or strategy (Azure AD roles appear in `payload.roles` for v2 tokens if configured, or `payload.roles`/`payload.wids` for group IDs).

**Assigning Roles:** How do users get roles in our DB? This could be done manually via database scripts, an admin UI, or by default (as shown, we gave every new user a "user" role by default). You might decide that any Azure AD user is a basic user, and then you promote some to admin through an admin interface. For demonstration, one could directly insert a role entry in the DB with name 'admin' and then manually link a user to that role via a database update or within code if you detect your user email is some known admin on first login. This is application-specific, so we’ll not elaborate too much – just ensure that in your `Role` table you have entries, and in `user_roles` join table appropriate mappings.

Finally, with the RolesGuard in place, our API endpoints can enforce RBAC. For example:

```ts
@Get('/users')
@UseGuards(AuthGuard('azure-ad'), RolesGuard)
@Roles('admin')
findAllUsers() {
  // Only admins can list all users
}
```

If a non-admin with a valid token hits this, RolesGuard will block it (return 403 Forbidden). If an admin hits it, it passes.

**Summary:** We stored roles in a DB and used a guard to enforce them – a typical approach in NestJS. In more sophisticated systems, roles might be hierarchical or combined with permissions, but the concept of checking a user’s roles from the DB remains (NestJS hint: you can store roles in DB or get from external provider ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=,from%20the%20external%20authentication%20provider)), which we demonstrated by pulling from DB).

### 6.2 Multi-Tenant Authentication Support

Multi-tenancy means our app can serve multiple organizations (tenants) with isolation. Azure AD multi-tenant setup allows users from different Azure AD directories to authenticate to our app (usually after an admin from their tenant consents). We have to consider a few things to fully support this:

**Azure AD App Registration for Multi-Tenant:** In section 2, if you chose “Accounts in any organizational directory” when registering, your app is _multi-tenant enabled_. Practically, this means:

- The **authority** in MSAL client was set to `/common` or `/organizations` (common allows both business and personal accounts if enabled; if only organizational accounts, `organizations` is used similarly). We used `common` in our msalConfig for multi-tenant. This lets users from any Azure AD attempt login.
- The first time a user from a different tenant logs in, Azure AD will show a **consent screen** asking them (or an admin) to consent to the permissions your app is requesting (like the `API.Access` scope). If the user is not an admin and your app requires admin-only permissions, login will fail until an admin grants consent. Otherwise, upon consent, Azure AD will create a **Service Principal** for your app in that user’s tenant and issue tokens ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=the%20Microsoft%20Entra%20admin%20center)). After consent, subsequent logins from that tenant users proceed without additional consent.

**Backend Validation for Multi-Tenant:** When tokens from various tenants come in, your backend needs to accept them. If you configured your Passport strategy with a specific `tenantId` and `validateIssuer:true`, it would only accept tokens from that one tenant (the home tenant). To accept others, you have a couple options:

- Use a common metadata endpoint and disable strict issuer validation. The `passport-azure-ad` strategy can be given `identityMetadata: https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration` and `validateIssuer: false`. This means it will accept tokens from any Azure AD tenant, as long as the token’s audience matches and the signing key is valid. The strategy will check that the token’s `iss` claim corresponds to some tenant’s endpoint and that the `tid` claim is present. The Azure docs mention that for multi-tenant, you should ensure the `iss` claim contains the tenant ID as well ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=Multitenant%20applications%20must%20perform%20more,more%20information%2C%20see%20Validate%20tokens)) (which is normally the case: iss = `https://login.microsoftonline.com/{tenantId}/v2.0`). Passport-Azure-AD likely does these checks internally.
- Alternatively, you could list allowed issuers if you only want to allow certain tenants.

For a true multi-tenant SaaS, you’d typically allow any, or any that have onboarded. You might want to restrict sign-ups to certain domains – that’s a business logic decision (like only specific partner tenants can use it). If so, you can enforce that in the validate function: e.g., check `payload.tid` against a whitelist of allowed tenant IDs stored in DB. If not allowed, throw an error to reject.

In our DB, we stored `tenantId` in User. We might also create a `Tenant` entity/table to track tenant-specific settings (like name, or whether they’re premium, etc.). On first user from a new tenant logging in, we could create a Tenant entry in DB. But that’s up to the application’s needs.

**Data Isolation:** Beyond authentication, multi-tenancy means ensuring that data belonging to tenant A is not accessible to tenant B. This typically involves scoping database queries by tenant. For instance, if you have an `Organization` or `Tenant` foreign key on your data tables, you would always filter by that based on the logged-in user’s tenant. If our `User` table has a `tenantId` field, any resource that belongs to a tenant can reference that. Our example is limited; you might imagine each `Project` or `Document` in the app has a tenantId, and any API fetching those ensures `item.tenantId === req.user.tenantId`.

This guide’s scope is mostly on auth, but keep in mind: to fully implement multi-tenant, incorporate the tenant context in your business logic. You might even include the tenant ID as part of JWT verification: e.g., a guard that checks `req.user.tenantId` against route parameters if needed or sets a query filter.

**Ensuring Unique Users per Tenant:** If the same person could log in from two different tenants (with separate accounts), you’ll get two user entries in your DB (since azureId will differ per tenant). That’s fine. If you want to treat them as separate or link them is another design consideration.

**Consent and Guest Users:** Azure AD has a concept of guest users (one tenant’s user invited to another). If a user is a guest in your app’s home tenant, they might appear with your home tenant ID but their actual home object ID. This can complicate things if not planned. A safer route is to go fully multi-tenant as above.

**Summary of Multi-Tenant Steps:** According to Microsoft’s guidelines, to convert to multi-tenant you:

1. Update app registration to multi-tenant,
2. use `/common` endpoint in auth,
3. handle multiple issuers in token validation,
4. implement user/admin consent logic ([node.js - MS OpenidConnect : Multitenancy on a nodejs web application - Stack Overflow](https://stackoverflow.com/questions/50695529/ms-openidconnect-multitenancy-on-a-nodejs-web-application#:~:text=0)). We’ve effectively touched each:
   - We set supported account types to “Any org directory” (done in Azure portal) ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-registration-to-be-multi-tenant#:~:text=By%20default%2C%20web%20app%2FAPI%20registrations,Accounts%20in%20any%20organizational%20directory)).
   - We used the common endpoint in MSAL config and in the strategy config we could use common with validateIssuer false ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-registration-to-be-multi-tenant#:~:text=1,7)).
   - We note the need to validate issuer differently (which passport-azure-ad mostly handles if configured correctly).
   - Consent: Usually just rely on Azure AD’s consent framework. If your app needs an **admin consent** for some permission, the user will be blocked until an admin grants it. You can provide an admin consent URL to them if needed (the portal provides a way or use the link: `https://login.microsoftonline.com/<tenant-id>/adminconsent?client_id=<app-id>`). But that’s outside of code – it’s an IT process.

From our code perspective, if we want to accept all tenants, we might adjust the strategy as:

```ts
super({
  identityMetadata: `https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration`,
  clientID: process.env.AZURE_AD_CLIENT_ID,
  audience: process.env.AZURE_AD_CLIENT_ID,
  validateIssuer: false,
  // ... other settings
});
```

This uses common metadata (which includes multiple issuer signing keys as needed) and skips strict issuer validation. We should still verify the token’s `aud` (clientID) and that `tid` claim exists. The library’s default for multitenant mode likely handles it ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=Multitenant%20applications%20must%20perform%20more,more%20information%2C%20see%20Validate%20tokens)). Always test this with a user from another tenant to ensure your backend accepts it. If not, adjust accordingly (for instance, sometimes setting `issuer: []` array of allowed issuers or turning off issuer check as done).

**Multi-Tenant Data example:** Suppose a user from tenant X and a user from tenant Y both call `GET /users/me`. Both will get their own profile. That’s fine. If there’s an endpoint like `GET /projects` that returns all projects, you must ensure it only returns projects of the user’s tenant. That could be done by scoping queries via `WHERE tenantId = :userTenantId`. You may incorporate the tenantId into JWT claims as well. In Azure AD tokens, `tid` is the tenant ID. We saved that in `User.tenantId`. So using `req.user.tenantId` is straightforward for filtering.

**Tenant-specific Roles:** In some apps, roles might be tenant-scoped (e.g., a user could be an "Admin" in their own tenant’s context but not for another tenant’s data). If using Azure AD app roles, those roles are actually assigned per tenant (each tenant’s admin assigns roles for their users for your app). If using our DB roles, we may need to associate roles with a tenant. That could be done by linking the UserRole join table with a tenant context or by namespacing roles per tenant. A simpler approach is to treat role names as global but enforce that, for example, tenant admins only have power over their tenant. We might not implement separate roles per tenant in code, but manage it via logic (like even if Role is "admin", the scope of that admin is inherently limited to their tenant’s data because of how we query data with tenant filter).

To conclude multi-tenancy: Our authentication and authorization system is designed to handle any number of tenants securely. Each request’s JWT indicates which tenant it’s from (`iss` and `tid`), and our system can accommodate that. We ensure that we validate tokens properly and isolate data by tenant in all queries. This allows scaling a single codebase and database to multiple client organizations (**SaaS model**).

## 7. Security Best Practices and API Protection

Security is paramount in authentication systems. We will highlight key best practices and how they apply to our implementation:

- **Never Trust the Client:** Always validate tokens on the server. We did this by using the Passport strategy to validate JWT signatures and claims. The token includes a signature that we verify using Azure AD’s public keys (passport-azure-ad handles retrieving the keys from the metadata endpoint). This ensures the token was indeed issued by Azure AD and not tampered with.

- **Validate Token Claims:** Besides signature, validate the **audience** (our app’s client ID or API identifier) to ensure the token is intended for us ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=issuer%3A%20%60https%3A%2F%2F%24,validateIssuer)), and the **issuer** to ensure it’s Azure AD (and if single-tenant, the correct tenant). The library does these. Also check **expiration** – library will reject expired tokens by default. If needed, also check `nbf` (not before) if present, but that’s usually handled. Ensure the token is an **access token** for the API (in our case, we accept tokens with our scope, which implies it’s an access token).

- **Use HTTPS Everywhere:** The frontend should only call the backend over HTTPS (especially when sending the Authorization header). Azure AD’s endpoints are HTTPS by default and should be used as such. In production, your React app and NestJS API must be served over TLS to prevent token interception.

- **Secure Token Storage (Frontend):** As discussed, storing tokens in browser local storage can expose them to JavaScript in case of XSS. MSAL by default keeps tokens in memory and/or sessionStorage. This limits persistence. For additional security, consider using **Hidden iframes or Refresh tokens** with **httpOnly cookies**. In a pure SPA, a common approach is to rely on short-lived access tokens (e.g., 1 hour) and silent renewal. If you need to persist login across sessions, MSAL’s refresh token (which is kept in memory or session storage) might not survive a full reload unless you choose localStorage. Another approach is a backend-for-frontend: your React app could delegate the OAuth flow to the server which then sets an httpOnly cookie. That, however, complicates the architecture and goes beyond our current setup.

  If using cookies, ensure they are **HttpOnly**, **Secure**, and ideally **SameSite=strict** to mitigate XSS and CSRF ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=Storing%20JWTs%20in%20cookies%20configured,improves%20security%20by%20making%20it)) ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=,for%20XSS%20attacks%20to%20succeed)). In our approach, since the token stays in the frontend context, we mitigate risk by not persisting it long and by protecting our app from XSS (next point).

- **Protect Against XSS and CSRF:**

  - **XSS:** Cross-Site Scripting could allow an attacker to run JS in your SPA and potentially steal tokens from memory or session storage. Mitigate XSS by sanitizing any dynamic content, using libraries or frameworks that auto-escape (React is generally safe by default, but be careful with `dangerouslySetInnerHTML` and such). Implement Content Security Policy (CSP) headers to restrict script sources. Also keep dependencies updated to avoid XSS vulnerabilities.
  - **CSRF:** If we were using cookies for auth tokens, we’d need anti-CSRF measures. In our design, the token is sent in header (Bearer), which is not automatically sent by browser to third-party sites, so CSRF is less of an issue. If you implement a session cookie approach, use SameSite=strict or anti-CSRF tokens.

- **Use JWT Best Practices:** JWTs should be short-lived and use appropriate signature algorithms (Azure AD uses strong algorithms like RS256, which is good). Do not accept **unsigned or weakly signed** JWTs. Also, do not assume JWTs are encrypted – they are just base64 encoded and signed. Anyone can decode and read the payload. Therefore, **never put sensitive data in the JWT** that you wouldn’t want the user or others to see. Azure AD’s tokens contain user info that’s fine to share with the client (like name, email), but nothing like a password. If you add custom claims from your side (via an API or something), consider that they will be visible.

- **Refresh and Logout:** Azure AD issues refresh tokens (if `offline_access` scope is granted) that MSAL can use. Ensure you handle logout properly: call `logoutRedirect()` or `logoutPopup()` so MSAL clears its cache and Azure AD ends the session (Azure AD will also clear its SSO cookie for that app). If a user logs out, make sure the frontend discards any stored tokens. On the backend, since we are stateless JWT, logout doesn’t directly affect the backend (the token will simply expire later). If immediate invalidation is needed (e.g., user clicks logout and you want to invalidate token), you can’t revoke a JWT easily. One strategy is to keep a server-side record: e.g., have a `session` table and include a session ID in JWT (Azure AD doesn’t allow custom claims easily, but you could map user->session in DB). For simplicity, relying on expiration is common. But you should educate that logging out of the app does not invalidate tokens that were already issued except by time. However, since our tokens are short-lived, the window is limited.

- **Least Privilege & Scopes:** Only request the minimal scopes from Azure AD that you need. In our case, we created a custom scope for our API. We did not request broad Graph permissions unnecessarily. This reduces what an attacker could do with a stolen token (they can only call our API, not Microsoft Graph or other APIs, because the token doesn’t have those scopes). Also, within our API, use roles/permissions to further restrict actions.

- **Monitoring and Logging:** In production, use logging to record important security events. For example, log authentication successes/failures (without sensitive token content) on the backend. Azure AD provides logs for sign-ins – monitor those for suspicious activity. On NestJS, you could add a middleware or extend the guard to log when a token is rejected (and why). However, avoid logging sensitive PII or full tokens. The Azure library by default does not log PII (unless you set `loggingNoPII: false` as we did for development; set it true in prod).

- **Regular Updates:** Keep MSAL and passport-azure-ad libraries updated to get security patches. These libraries are maintained by Microsoft and address vulnerabilities over time. Similarly, update NestJS and other dependencies to patch any known issues.

- **Enforce Strong User Security in Azure AD:** Leverage Azure AD features like **Conditional Access** and **MFA**. For instance, you can require multi-factor authentication for users to sign in, or conditional access policies (e.g., block sign-in from certain locations). These are configured in Azure AD and automatically apply – your app just gets the token after those requirements are satisfied. It greatly enhances security without extra code. Also, Azure AD can handle password policies, account lockout, etc., so your app doesn’t need to worry about that.

- **Key Management:** Azure AD takes care of rotating its signing keys. The `passport-azure-ad` library will automatically fetch the latest **OpenID Connect metadata** which includes the JWKS (JSON Web Key Set) for validation. This is great because if Microsoft rotates keys, your app will still accept the new signatures (it trusts the metadata endpoint). Ensure the `identityMetadata` URL is correct and uses `https://` (which it is). This way, you don’t hard-code any public keys or certificate thumbprints, avoiding maintenance.

By following these practices, our app is well-hardened. For example, using secure cookies would further improve security (by not exposing tokens to JS at all), but our trade-off was to keep the architecture simple (typical of an SPA + API). We mitigate that choice by focusing on XSS prevention.

## 8. Deployment Strategies (Frontend & Backend)

Deploying a full-stack application involves deploying the React frontend and the NestJS backend (and the PostgreSQL database). We will outline strategies for Azure and Docker, as well as general hosting considerations.

### 8.1 Preparing for Deployment

Before deploying, ensure a few things:

- You have appropriate **configuration for production**: e.g., different Azure AD settings if needed, turning off verbose logging, `NODE_ENV=production` for Nest (which disables certain debug features) ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=While%20there%27s%20technically%20no%20difference,environment)), and proper environment variables for database connection, client IDs, etc.
- The **frontend build** is optimized: run `npm run build` for React to produce minified static files.
- The **backend build**: compile NestJS TypeScript to JavaScript (`npm run build`, output in `dist/`). Ensure that the production environment is using the compiled code and that source maps are either disabled or handled properly.
- All necessary **environment variables** or config files are set on the server (like in Azure App Service or in Docker environment). This includes `AZURE_AD_CLIENT_ID`, `AZURE_AD_TENANT_ID` (if single-tenant) or any others used, database credentials, etc. You should not store secrets in the code repository – use environment configuration in the hosting platform ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=Before%20deploying%20your%20NestJS%20application%2C,ensure%20you%20have)).

### 8.2 Deploying the NestJS API

**Option 1: Azure App Service (PAAS)** – Azure App Service can host Node.js applications easily:

- Create an Azure App Service instance (Linux) for Node. You can use Azure CLI or portal. Choose a runtime that matches your Node version.
- Set environment variables in the App Service Settings (like DB connection string, client ID, etc.).
- Deploy your code. You can use CI/CD (GitHub Actions or Azure DevOps) or manual deployment via zip or VS Code Azure extensions. If using CI, build the Nest app (ts->js) and then deploy the `dist/` and `node_modules` (or the entire project if you build on the server – App Service can run `npm install` and `npm run build` if configured).
- Ensure the app is listening on the port provided by `process.env.PORT` (Nest’s default is 3000, but Azure sets a PORT env var). NestJS will pick up `process.env.PORT` if you pass it in listen. Alternatively, you can instruct Azure to redirect 80 to 3000.
- Also enable Azure App Service Logging for monitoring or hook up Application Insights for advanced logging.

**Option 2: Docker Container** – Containerizing the backend:

- Write a Dockerfile for NestJS. A basic example:

  ```Dockerfile
  FROM node:18-alpine
  WORKDIR /app
  COPY package*.json ./
  RUN npm install --only=production
  COPY dist ./dist
  CMD ["node", "dist/main.js"]
  ```

  This assumes you already built the Nest app (`dist` exists). Alternatively, a multi-stage Dockerfile can build the app:

  ```Dockerfile
  FROM node:18-alpine AS builder
  WORKDIR /app
  COPY . .
  RUN npm install
  RUN npm run build

  FROM node:18-alpine AS runner
  WORKDIR /app
  COPY package*.json ./
  RUN npm install --only=production
  COPY --from=builder /app/dist ./dist
  CMD ["node", "dist/main.js"]
  ```

  This results in a smaller image with only production dependencies and the built code. Docker ensures consistency across environments: your app will run the same inside the container as it did locally ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=Benefits%20of%20Dockerizing%20your%20NestJS,application)).

- Build and push the Docker image to a registry (Docker Hub or Azure Container Registry). For example:
  ```bash
  docker build -t myapp/nest-api:1.0 .
  docker push myapp/nest-api:1.0
  ```
- Deploy the container:
  - **Azure Web App for Containers:** you can point it to the image (if public Docker Hub or using Azure Container Registry with credentials) and it will run it. Set the environment variables in the App Service as usual.
  - **Azure Container Instances (ACI):** For a simple container (not much scaling, ephemeral), you can use ACI via Azure CLI.
  - **Kubernetes (AKS):** If you have more complex needs or multiple containers, deploying to an AKS cluster might be appropriate. That’s heavier and usually not needed unless you have a microservices architecture or high scale requiring orchestration.
- If using Docker, ensure to configure for scalability: e.g., you might want to run multiple replicas of the API container behind a load balancer for high availability. Azure App Service and AKS can handle that (App Service can do auto-scaling with multiple instances easily).

**Database (PostgreSQL):** Use a managed database service like **Azure Database for PostgreSQL**. Azure can host a Postgres instance for you; you just supply the connection string to your app. Managed DB ensures backups, reliability, and security patches. Alternatively, run Postgres in a container or VM, but managed is easier for production. Remember to set up firewall rules or VNet so your app can access the DB. On Azure, if App Service and DB are in same region, allow Azure services to connect or use VNet integration for tighter security.

### 8.3 Deploying the React Frontend

The React app is purely static (HTML, JS, CSS) after a build. Options to host:

- **Azure Storage Static Website**: You can upload the `build/` directory to an Azure Blob Storage container configured for static website hosting. This gives you a URL to the site. You might put it behind Azure CDN or custom domain. This is cost-effective and simple.
- **Azure App Service (as static site)**: You could also deploy the static files to an App Service configured for static content (or even use the same App Service as the API – serve the React build from NestJS or an Nginx). For instance, NestJS could serve static files using `Nestjs/ServeStaticModule` to serve the React `build` folder. That way, your API and frontend are on the same domain (which simplifies deployment and avoids CORS). If doing that, ensure to adjust Nest config to serve the frontend and catch-all route to index.html (so client-side routing works).
- **Azure Static Web Apps**: Azure has a service specifically for static frontends + optional Azure Functions. It integrates with GitHub for CI. However, since we already have a separate API, Static Web Apps might complicate integration (it expects to manage its own backend via Functions). You can still use it just for the static content and have it call your separate Nest API (with CORS).
- **Docker or other hosts**: Alternatively, containerize the React app with something like Nginx. E.g.,

  ```Dockerfile
  FROM node:16-alpine AS builder
  WORKDIR /app
  COPY . .
  RUN npm install && npm run build

  FROM nginx:alpine
  COPY --from=builder /app/build /usr/share/nginx/html
  # COPY a custom nginx.conf if you need to, else default is fine for serving /usr/share/nginx/html
  ```

  Then run this container on a service. But this is often overkill for pure static sites when storage/CDN is available.

**Environment config for React:** If your Azure AD settings differ between dev and prod (like you might use a different clientId or tenant for testing vs production), you need to supply those to React. Typically, one builds the React app with environment variables (like `REACT_APP_CLIENT_ID`) configured. Ensure at build time for production, you set the env vars (in CI or build pipeline). Alternatively, some people use a dynamic configuration by making the React app fetch a config JSON. But simplest: use the build environment. For example, in package.json scripts, you might do `CI=true REACT_APP_CLIENT_ID=abc REACT_APP_TENANT_ID=common npm run build`. In Azure Static Web Apps, you can set these variables.

**CORS:** If the frontend is hosted on a different domain than the API, you must enable CORS on the NestJS API to allow the frontend’s origin. We can do that in NestJS main.ts:

```ts
app.enableCors({
  origin: "https://myapp.frontend.com",
  allowedHeaders: "Content-Type, Authorization",
  credentials: false,
});
```

This will let the browser call the API from that origin. In development, we often use origin `http://localhost:3000`. In production, put your actual domain or use a regex if multiple. Keep it restrictive to known domains for security. If you serve frontend and backend on the same domain (e.g., backend at `/api` and frontend files on same host), you don’t need CORS – that’s simpler.

**Deployment Verification:** After deploying:

- Verify the React app loads and can redirect to Azure AD and back. Ensure the **redirect URI** used is updated in Azure AD app registration if your domain changed (for instance, add `https://myprodurl.com/auth/callback` or whatever is being used by MSAL).
- Verify the NestJS API is reachable at its URL, and that it can connect to the database (check logs for successful DB connection on startup).
- Test a full login flow in production: navigate to site, log in via Azure AD, get redirected back, and data from the API loads (e.g., call a test endpoint that returns user profile). If issues arise, check:
  - Azure AD reply URLs (redirect URIs).
  - CORS errors in console (if API calls failing).
  - Token validation failures in Nest logs (maybe the config for multi-tenant or audience is off).
  - Configuration mismatches (perhaps env vars not set correctly, etc.).

**Scaling Considerations:**

- The React app can be scaled via CDN easily since it's static.
- The API can be scaled by running multiple instances/containers. Azure App Service and AKS allow horizontal scaling. Because our app is stateless (no session stored in-memory that isn't shared), scaling out is easy – JWTs are independently verifiable by each instance.
- The database is a single instance (or a cluster if you use something like Azure Database hyperscale). If high load, ensure the DB is appropriately sized (vCores, memory) and consider read replicas if needed for heavy read load. Use connection pooling in the app (TypeORM’s default poolSize or PG pool; we set poolSize 10 in config as example ([Designing RBAC Permission System with Nest.js: A Step-by-Step Guide - DEV Community](https://dev.to/leapcell/designing-rbac-permission-system-with-nestjs-a-step-by-step-guide-3bhl#:~:text=database%3A%20%27nest,%5D%2C%20controllers%3A%20%5BAppController))). For most apps, the default is fine.
- Use a caching layer if needed. For example, if certain user data is frequently accessed and changes rarely, you might add Redis caching. Or if JWT validation performance is a concern, note that passport-azure-ad likely caches the openid keys. The validation itself is quick (just a crypto verify). No need for heavy caching there. But you might cache user roles from DB if that becomes a bottleneck (so that each request doesn't hit DB for user lookup – however, since JWT carries user info, an alternative is to put roles in token via app roles or custom claims, but that's not straightforward cross-tenant). DB caching is an optimization – measure first.

**Docker Compose for Dev/Prod:** If you prefer deploying using Docker Compose (like on a VM or server), you can define services for api, frontend, and db. For example:

```yaml
version: "3"
services:
  api:
    image: myapp/nest-api:1.0
    environment:
      - DB_HOST=db
      - DB_USER=postgres
      - DB_PASS=secret
      - DB_NAME=proddb
      - AZURE_AD_CLIENT_ID=...
      - AZURE_AD_TENANT_ID=...
    ports:
      - "4000:3000"
    depends_on:
      - db
  frontend:
    image: myapp/react-frontend:1.0
    ports:
      - "80:80"
  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=proddb
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

This would run all components together. In a production scenario, you might run such a compose on a Docker server or use Kubernetes. However, separating concerns (e.g., using a managed DB) is often safer.

### 8.4 Domain and HTTPS

If deploying both frontend and backend, consider using a custom domain. For example, `app.mycompany.com` for frontend and `api.mycompany.com` for backend, or even `app.mycompany.com` for both if served together. Use HTTPS certificates (Azure App Service can manage certificates or use Let's Encrypt). If using separate subdomains, ensure CORS and also consider setting a **Secure cookie** domain if you were using cookies.

Since the user specifically asked about Azure and Docker, the above covers those. If using other providers (AWS, GCP, Heroku, etc.), the principles are similar:

- On AWS, you might use S3 + CloudFront for static, ECS or Elastic Beanstalk or Lambda for backend, and RDS for Postgres.
- On Heroku, you could deploy the Node app (NestJS) easily and use Heroku Postgres, and deploy React as well (or use Heroku’s static buildpack). But in enterprise context, Azure is a good fit with Azure AD integration.

In summary, choose a deployment approach that fits your team’s expertise and the scale requirements. Azure App Service is a straightforward way to host both parts without container overhead. Docker is great for portability and when you want to ensure environment parity or use container orchestration.

## 9. Testing and Debugging the Authentication Flow

Proper testing ensures your auth system works and remains secure as you modify code. We cover different testing strategies and common issues with debugging tips:

### 9.1 Testing Strategies

**Unit Testing (Backend):**

- You can write unit tests for your NestJS guards and services. For example, test that `RolesGuard` correctly allows/denies access given a user with certain roles. You might create a fake `ExecutionContext` with a mock `req.user`.
- Test the AzureADStrategy’s `validate` method logic in isolation by calling it with a sample JWT payload to see if it creates/fetches a user correctly from a mocked repository.

However, the actual token validation (cryptographic) is part of the library – you wouldn’t unit test Azure’s code, but you might simulate it by calling `strategy.validate` directly with a known payload (bypassing the signature check). For example, if you want to test that a token with no `oid` claim is handled, you could call `validate({})` and expect perhaps an exception or certain behavior.

**Integration Testing (Backend):**

- Use Nest’s testing utilities (e.g., `@nestjs/testing` to create a testing module with the AuthGuard and a dummy controller) and Supertest to simulate requests. You can generate a dummy JWT that the strategy will accept. One tricky part: if using passport-azure-ad’s BearerStrategy, it will actually attempt to verify signature. One approach is to override parts of the strategy for tests (perhaps by using a custom provider that bypasses actual validation and just returns a static user object). Alternatively, for integration tests you might treat the auth as a black box and instead stub it: e.g., use Nest’s ability to override guards. For instance, in E2E tests, you could replace the `AuthGuard('azure-ad')` with a dummy guard that always returns true and sets `req.user` to a test user. This way, you can test your API endpoints without needing real Azure AD tokens each time.

Example of overriding guard in test:

```ts
import { ExecutionContext } from "@nestjs/common";
class DummyAuthGuard implements CanActivate {
  canActivate(ctx: ExecutionContext) {
    const request = ctx.switchToHttp().getRequest();
    request.user = {
      // ... mock user data, e.g., roles: [{name:'admin'}], tenantId: '...'
    };
    return true;
  }
}
```

Then in test module:

```ts
{ provide: APP_GUARD, useClass: DummyAuthGuard }
```

or override specifically the azure-ad guard token if registered.

This way, you can simulate authenticated requests easily. For testing the auth mechanism itself interacting with Azure AD, you might not do that in integration tests (that would be more like an end-to-end test requiring an actual Azure AD tenant which is complex and not usually run automated).

**Front-end Testing:**

- For React components, you can mock MSAL context. If you have logic depending on `useIsAuthenticated`, you can write tests that wrap the component with an `MsalProvider` using a fake MSAL instance. There’s MSAL React testing patterns, or you can simply abstract out logic that requires auth to a context and provide a mock value in tests.
- If you want to test the full login flow in a browser (end-to-end test), you could use a tool like **Cypress**. Cypress can handle the redirect to Azure AD by either:

  - Actually performing the login with a test account (you might store test credentials as environment variables and have Cypress input them into the Azure login form – although that exposes credentials and might not work if MFA is needed).
  - Or bypassing it by stubbing the network requests to Azure AD token endpoint (which is complicated).
    It's often easier to not test the actual Azure AD UI in automated tests. Instead, you might test that when the app receives a token (maybe by calling a certain MSAL function directly in test), it behaves correctly (e.g., showing logged-in state).

- Test the API calls from front-end: perhaps mock `fetch` or `axios` to ensure it includes Authorization header.

**Manual Testing:** Always do manual testing in a stage environment:

- Test logging in as a normal user (no special roles) and trying to access an admin-only API (should get 403).
- Test as an admin user to access admin API (200 OK).
- Test multi-tenant: if possible, create another Azure AD guest or a separate tenant user and try to sign in.
- Test token expiration: you can artificially shorten token lifetime for testing (Azure AD allows setting access token lifetime policies, or just wait 1 hour) to see if MSAL properly acquires a new one (MSAL’s default is to attempt silent refresh).
- Test logout and then using a previously acquired token (if you saved it) to call the API (should fail if token expired; if not expired, note that logout doesn’t revoke it – an area of potential improvement if needed).

**Performance Testing:** Not directly an auth test, but ensure your auth doesn’t bottleneck. For example, simulate multiple concurrent login requests to see if any part (like DB user creation) becomes slow under load. Azure AD can handle huge auth loads, so the main limiter might be your DB if thousands of new users sign up simultaneously. Use DB connection pooling and maybe limit how often you write new records (e.g., maybe queue them). For steady state with existing users, performance should be fine (a DB lookup by indexed azureId is very fast, and JWT verification is fast thanks to crypto libraries implemented in C++ under the hood).

### 9.2 Debugging Common Issues

Despite careful setup, you may encounter issues. Here are common ones and how to resolve them:

- **Issue: Login redirect works, but React app shows error like “interaction_in_progress” or doesn’t update state.**  
  **Solution:** Ensure you have wrapped your app in `<MsalProvider>` and that you are not calling loginRedirect twice. The error “interaction_in_progress” means MSAL is already handling a redirect or popup. This can happen if you call loginRedirect on page load automatically and also have something in a component. The fix is usually to call `instance.handleRedirectPromise()` (MSAL React does this internally if using MsalProvider). Also, ensure you have a route in React that can catch the redirect URI – MSAL will use the root by default, which your app should handle (the MSAL provider processes the hash and then removes it). If using React Router, ensure the router does not erroneously handle the hash. Usually, use BrowserRouter (with history) or HashRouter carefully.

- **Issue: Azure AD login page says “Error: AADSTS50011: The reply URL specified does not match...”.**  
  **Solution:** This means the redirect URI registered in Azure AD doesn’t match exactly what the app is using. Check the URL in the browser’s address bar when the error appears, and make sure that exact URL is in the Azure AD app’s Authentication > Redirect URIs list ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=,You%E2%80%99ll%20need%20it%20later)). Common mistakes: missing a trailing slash, using http instead of https, or wrong port in development. Fix the app registration and try again.

- **Issue: Got an access token in React, but API calls return 401 Unauthorized.**  
  Possible causes:

  - The token might not be sent at all. Check your network calls in browser dev tools to see if the Authorization header is present. If not, ensure you include it in the fetch/axios call exactly as `Authorization: Bearer <token>`.
  - CORS might be blocking the request before it reaches NestJS. Check the browser console for a CORS error. If present, configure NestJS to allow the origin and headers. Also check that the browser isn’t stripping the Authorization header due to a cross-origin issue (with proper CORS it shouldn’t).
  - The token is sent but the backend rejects it. Check NestJS logs (if you use a Logger in validate, or surround AuthGuard with try-catch). The passport-azure-ad library might not provide detailed logs by default. You can temporarily set `loggingLevel: 'info'` and `loggingNoPII: false` in the strategy config to see verbose logs (only in dev, as it might log user info) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=validateIssuer%3A%20true%2C%20passReqToCallback%3A%20false%2C%20loggingLevel%3A,scope%20of%20your%20azure%20AD)) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=constructor%28%29%20,validateIssuer)). If the log says “invalid signature” or “jwt audience invalid”, then likely the audience or issuer didn’t match what was expected. Make sure `clientID` and `audience` in strategy are correct. If the error says “Token is not active” or similar, check clock sync (Azure tokens have a few minutes of clock skew allowed, but if server time is way off, it can fail). Ensure your server time is correct (on Azure App Service it should be).
  - If using multi-tenant, and error indicates issuer invalid: maybe `validateIssuer` is true while token is from another tenant. The library might say something like "Invalid issuer". Setting `validateIssuer: false` or including `issuer` as an array of allowed issuers (the library supports an array for multi issuer) solves that ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=Multitenant%20applications%20must%20perform%20more,more%20information%2C%20see%20Validate%20tokens)).
  - Another cause: If your token is from the **v1 endpoint** (not likely if using MSAL which uses v2 by default). v1 tokens have different claims (aud might be the resource URI). Ensure you are using v2 (which MSAL does). If for some reason you used ADAL or something (older library), consider switching to MSAL.

- **Issue: acquireTokenSilent fails in MSAL (user gets stuck or a popup appears unexpectedly).**  
  **Solution:** This can happen if the token is expired and MSAL cannot refresh (maybe user’s session at Azure expired too). MSAL should automatically attempt a hidden iframe or refresh token. If using MSAL v2 and you have `offline_access` scope, a refresh token should be available. If it still fails, handle the error: MSAL will throw an error which you can catch and then call `instance.loginRedirect()` again to prompt login. This reauthentication might be needed if the user has been idle long enough.
  Also, check that the MSAL configuration has a `cacheLocation` that persists across page reload if you want silent to work after reload. By default sessionStorage means if user reloads the SPA, the MSAL state is lost and they would have to login again (though if still session cookie at Azure AD, loginRedirect will be silent). Setting cacheLocation to localStorage can keep tokens across reloads (with aforementioned risk). It's a trade-off.

- **Issue: Role-based guard not working – users with the right role still get 403.**  
  **Solution:** Check that `req.user` actually has the roles populated. Maybe your validate function isn’t returning the user entity with roles. If you forgot to load relations, `user.roles` might be empty. In TypeORM, if you didn’t use `{ eager: true }` or a join, then `roles` might not be there. We set eager: true on roles in User entity to auto-load roles ([Designing RBAC Permission System with Nest.js: A Step-by-Step Guide - DEV Community](https://dev.to/leapcell/designing-rbac-permission-system-with-nestjs-a-step-by-step-guide-3bhl#:~:text=export%20class%20User%20,id%3A%20number)). If not using eager, ensure to use `userRepo.findOne({..., relations: ['roles']})`.
  Also confirm that the RolesGuard is being applied after AuthGuard. In Nest, if you use `@UseGuards(AuthGuard, RolesGuard)`, the order in the annotation doesn’t guarantee execution order; all guards execute. But AuthGuard will populate user or throw if invalid, RolesGuard will then act. That should be fine.
  Also check that the role names in the token or DB match exactly what the @Roles decorator expects. Our RolesGuard checks `user.roles[i].name`. So if your roles in DB are lowercase but you put @Roles('Admin') with capital A, it won't match 'admin'. Perhaps normalize case or ensure consistency.
  Logging inside RolesGuard can help: log the `requiredRoles` and `userRoles` for debugging.

- **Issue: Multi-tenant user unable to log in because they get an error about consent (“need admin approval”).**  
  **Analysis:** This means your app is requesting permission that normal users can’t consent to (like reading directory data) or the tenant has user consent disabled. The error AADSTS**50020** or similar might appear. If it’s a needed permission, the admin of that tenant must grant consent. Provide them with the admin consent URL or use Azure AD’s Admin consent workflow (Azure AD can allow users to request admin consent which admin can approve in portal). If you don’t actually need that permission, remove it from Azure AD app. For example, if you accidentally added a Graph permission like User.Read.All, normal users can’t consent and admin must. Removing such requirement solves it. For our scenario, a user should be able to consent to "API.Access" if configured for user consent, which it is by default when you create a scope (we selected Admin and users can consent in step 4) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=,to%20add%20the%20scope%20configuration)).
  If user consent is disabled in their tenant entirely (some orgs do that for security), then an admin of that org must pre-consent for all users. They can do that by signing in to the URL: `https://login.microsoftonline.com/<tenant-id>/adminconsent?client_id=<app-id>` (which will show an admin consent prompt for the whole tenant). After that, any user in that tenant can sign in without individual consent prompts.

- **Issue: Azure AD claims missing something expected (like email is null in token).**  
  **Explanation:** Some claims are optional. For instance, Azure AD might not include `preferred_username` or `email` if not available or if not requested. In multi-tenant, if the user is from a different tenant, you might not get their email unless you added it as optional claim. You can configure **optional claims** in Azure AD app to get certain information in the token (like `email`, `given_name`, etc.) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=3,in%20Azure%20AD)). If you need those, set them in App Registration > Token configuration. Alternatively, call Microsoft Graph /userinfo endpoint after login to get user profile. But that requires Graph permission and an API call. Simpler is to include in token if possible.
  If `email` is missing, perhaps use `preferred_username` which is often the user’s UPN (often their email for org accounts, but not always). Or `name` for full name. In B2C scenarios, you might definitely configure these. In our context, enterprise users usually have these in the token by default.

- **Issue: Using the app on IE11 or older browser fails (maybe polyfill issues with MSAL).**  
  **Solution:** Ensure you include any necessary polyfills if older browser support is needed. MSAL might need Promise polyfill for IE. This is only relevant if supporting legacy browsers.

- **Issue: Timeouts or slow response from API on first call after a while.**  
  **Analysis:** Possibly the passport-azure-ad library fetching the metadata the first time (it caches after). The first validation might trigger a download of OpenID config and keys. This is usually quick (<100ms). But on a cold start, it could add a bit of latency. It’s generally fine. If on a very constrained environment without internet access, that’d be an issue (then you’d have to supply the metadata manually). On Azure, it can fetch it. If performance is a concern, consider eager loading the metadata at app startup (maybe by hitting a dummy validate).

- **Issue: Logging out from Azure AD (like sign-out) doesn’t fully sign out.**  
  Actually, Azure AD’s `logoutRedirect` will clear the token from MSAL and redirect to Azure AD sign-out, which clears the user’s session cookie for Azure AD (for that app). If the user was logged into Azure AD across multiple apps, Azure AD might keep a session if not specifically cleared. There's a concept of single sign-out. Azure AD attempts to sign out of all apps that user is logged into via front-channel if those apps have a logout URL configured. If you provided a logout URL in app registration (often same as redirect URI or a specific signout URI), Azure will send a GET to that URL (with an id_token_hint possibly) to notify the app to sign the user out. We didn't specifically handle that, but since our app is SPA, it's not as relevant. Just be aware that if a user signs out, their Azure AD session might still exist for other apps unless they did a full logout.

- **Issue: I want to test token validation without Azure** (for dev perhaps).  
  **Solution:** You can create dummy JWTs signed with test keys and modify your strategy in dev to trust those. But that’s complex and not needed if you can always get a token from Azure AD by login (which in dev is fine). If offline or to run integration tests, you might consider using a library like jsonwebtoken to sign a token with a known private key and configure passport-jwt with that key (instead of passport-azure-ad). But then you're not testing Azure integration. Usually, it's okay to test using actual Azure AD tokens in a dev environment (maybe register a separate app for testing if needed).

By systematically checking logs and the configuration on both the Azure side and the code side, you can resolve most issues. Azure AD provides specific error codes (AADSTSxxxx) which you can look up on docs for explanation. For example, AADSTS50011 is redirect mismatch, AADSTS70001something is usually about permission, etc. Use the Microsoft documentation and forums (Stack Overflow, MSDN) when encountering those codes – they often have known solutions.

## 10. Real-World Example Scenarios and Production Considerations

To put everything in context, let’s discuss a hypothetical real-world application and how it would use this setup, then final production tips:

**Scenario:** Imagine a SaaS platform called “Contoso Projects” that allows companies to manage projects and tasks. Contoso decides to use Azure AD for enterprise single sign-on. They make Contoso Projects a multi-tenant app because they have many client organizations. Each client’s employees will log in with their own corporate Azure AD credentials – no separate passwords for Contoso platform.

- **Multi-Tenant Azure AD:** Contoso registers the app as multi-tenant in their Azure AD (which acts as the "home" tenant). They define app roles: e.g., “Project Admin” and “Project User”. They choose to manage roles within the app for flexibility, but for demonstration, let’s say they also configure corresponding Azure AD app roles. When a new client (say Fabrikam Inc.) wants to use the app, an admin from Fabrikam goes through the consent process. After consenting, Fabrikam’s users can SSO into Contoso Projects. Each Fabrikam user upon first login is created in the Contoso DB with tenantId = Fabrikam’s tenant GUID. They might start with a default role of User. Fabrikam’s global admin can be flagged as a Project Admin in the Contoso app (Contoso might allow the first user from a tenant who is an Azure AD admin to become the default admin in-app as well). This way, multi-tenancy is achieved and each tenant has an admin.

- **RBAC in use:** Within Contoso Projects, the Project Admin role can create projects, invite other users (which might just be instructing them to log in or using Azure AD to send invites), etc. Our RBAC guard ensures only Admins can access admin endpoints. If Contoso doesn’t want to rely on Azure AD app role assignment (which would require each client’s Azure admin to assign roles to users in Azure AD), Contoso instead builds an in-app roles management: Project Admin (in-app) can elevate other users to admin within that tenant context. Our DB design supports that by linking roles to users per tenant.

- **API Protection & Usage:** Each API call from the single-page app includes the JWT. If a user tries to access another tenant’s data by modifying an identifier, the backend checks user.tenantId vs requested resource’s tenantId and denies if mismatch. This is additional to the basic RBAC but equally important for multi-tenant security. This prevents horizontal escalation between tenants.

- **Scale and performance:** Suppose Contoso Projects gets 100 client companies, each with 1000 users. That’s 100k users in the DB. Our approach will handle that easily: lookup by azureId is indexed and near O(1) operation, JWT verification is constant time. The volume of logins might spike at 9am Mondays when everyone logs in, but Azure AD can easily handle token issuance for many users simultaneously (millions of auths daily as per Microsoft ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=In%20addition%2C%20according%20to%20the,cannot%20be%20easily%20achieved%20otherwise))). Our backend might become CPU-bound if a ton of JWT validations happen concurrently – but this is quite efficient in Node (the crypto verify uses native code). Still, we would have multiple instances or robust hardware. Also, once logged in, tokens last an hour, so a user’s subsequent requests don’t incur re-auth overhead beyond checking the signature which is quick. DB calls for user info could be cached to reduce hitting the DB for each request (e.g., cache user roles in memory for token lifespan). If each API request decodes the JWT and uses the embedded info (like roles if we trust token or userId then fetch roles), that’s a minor overhead.

- **Monitoring in production:** Contoso would use Azure Application Insights or another logging solution to track errors (like unauthorized access attempts, etc.), monitor performance (maybe JWT verification or DB queries), and successes. They might also enable **audit logs**: e.g., log whenever an admin role is granted to someone (for compliance).

- **Optimized Configurations:** In production, they ensure:
  - `NODE_ENV=production` so NestJS and React run in prod mode (minimized, no sourcemaps or verbose errors) ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=)).
  - They disable any debug logging for auth libraries (no PII logs).
  - They set strict CORS rules (only allow domains that serve their app).
  - They regularly update the app with latest security patches (maybe dependabot for npm packages).
  - The tokens issued are the right size: If token becomes too large (e.g., if a user is in many Azure AD groups and groups claim is enabled, token might be big and hit header size limits – Azure AD addresses this by providing group overflow via Graph query, but it's a corner case). If needed, Contoso might opt to use just roles and not include groups in token to keep it lean.
  - They possibly use **HTTP caching** on static responses or CDN for static assets of React app.

**Case Study Reflection:** Many real companies use this pattern:

- Microsoft’s own line-of-business apps often use Azure AD for internal SSO with frameworks similar to Nest or Express.
- Multi-tenant SaaS like Office 365 itself is multi-tenant with Azure AD (though at a much bigger scale).
- A more comparable example: an app like **Slack enterprise login** can be integrated with Azure AD (via SAML/OAuth). Here we implemented OIDC. The approach is standard: use the identity provider for auth, rely on JWTs for session, have app-specific roles/permissions.

**Alternate Approaches:**

- If our NestJS API was to call Microsoft Graph on behalf of user (say to read their calendar), we could use the access token (with appropriate scopes) or use On-Behalf-Of flow with a client secret. That’s beyond our scope but Azure AD supports OBO flow ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=native%20%28desktop%29%20applications%20,on%20%28SSO)). Our app doesn’t do it but could if needed by obtaining Graph token or by configuring multi-scopes.
- If high security is needed, consider **Conditional Access** policies requiring compliant devices or specific conditions to allow tokens. The app can integrate with that seamlessly (Azure AD just won’t issue a token unless conditions met).
- If we needed to support external users without Azure AD, we could integrate Azure AD B2C (which is a separate scenario using local accounts or social logins). But that’s a different setup (with B2C tenants).
- We could also integrate multiple auth providers (say Google OAuth, etc.) but typically enterprise apps choose one (Azure AD here). If needed, using libraries like passport or custom logic you can accept tokens from multiple IdPs, but that complicates things.

**Production tips recap:**

- Load test your app with expected user counts.
- Keep an eye on Azure AD service health (rarely an issue, but if Azure AD is down, users can’t login – have a plan for that, maybe cached tokens will let already logged in users continue).
- Use Azure AD’s **identity governance** features if necessary (like if a user leaves company, their Azure AD account is disabled – our app will naturally reject their token once it expires or immediately if we validate `acct` claim status via Graph, but usually token just expires and they can’t get a new one because account disabled).
- Ensure your database backups and have a disaster recovery plan (because though Azure AD can auth, your app data is in Postgres – back it up).
- Consider compliance: if needed, log user login events (Azure AD logs them but you might need to surface them to tenant admins in-app).
- Provide user-friendly error messages: e.g., if a user from an unauthorized tenant tries to login, catch that and show a message like "Your organization has not been onboarded. Please contact support." Instead of a generic error. You can detect that scenario via error codes or by implementing a custom consent screen.

By following the steps in this guide, we’ve built a robust authentication system suitable for real-world production use, with Azure AD providing secure identity management, and our React/Node/Postgres stack enforcing authorization and storing app-specific data. This setup is **scalable, secure, and maintainable**, leveraging modern frameworks and cloud services.

---

**References:** This guide is informed by official documentation and best practices:

- Microsoft identity platform documentation on OAuth2 and OIDC ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Access%20tokens%20,granted%20by%20the%20authorization%20server)) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=We%20strongly%20advise%20against%20crafting,implementation%2C%20we%20have%20protocol%20reference)).
- Azure AD app registration steps and multi-tenant conversion guide ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-registration-to-be-multi-tenant#:~:text=1,7)) ([Convert single-tenant app to multitenant on Microsoft Entra ID - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory/develop/active-directory-devhowto-multi-tenant-overview#update-your-code-to-handle-multiple-issuer-values#:~:text=Multitenant%20applications%20must%20perform%20more,more%20information%2C%20see%20Validate%20tokens)).
- Usage of MSAL for React as detailed by Microsoft and community tutorials ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=The%20first%20package%20%E2%80%94%20%60%40azure%2Fmsal,without%20using%20a%20backend%20server)) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=Wrapping%20the%20app%20in%20the,component)).
- NestJS Authentication and Authorization patterns from the official docs and community examples ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=export%20enum%20Role%20,user%27%2C%20Admin%20%3D%20%27admin%27%2C)) ([Integrating Single Sign-On (SSO) with Azure Active Directory (Azure AD) | by Gnanabillian | Dev Genius](https://blog.devgenius.io/integrating-single-sign-on-sso-with-azure-active-directory-azure-ad-in-nestjs-210b07e7420d#:~:text=constructor%28%29%20,validateIssuer)).
- Security best practices for JWTs and SPAs ([Secure JWT Storage: Best Practices](https://www.syncfusion.com/blogs/post/secure-jwt-storage-best-practices#:~:text=,for%20XSS%20attacks%20to%20succeed)).
- Real-world performance and usage statistics of Azure AD ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=In%20addition%2C%20according%20to%20the,cannot%20be%20easily%20achieved%20otherwise)).
