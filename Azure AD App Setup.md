# Azure AD

**Table of Contents**

1. **Introduction**
2. **Azure AD Application Registration**
   - 2.1 **Single-Tenant Application Registration**
   - 2.2 **Multi-Tenant Application Registration**
3. **Configuring Redirect URIs and Exposing APIs**
   - 3.1 **Redirect URIs and Platform Configurations**
   - 3.2 **Exposing an API (Defining Scopes)**
4. **Application Secrets and Certificate-Based Authentication**
   - 4.1 **Generating Client Secrets**
   - 4.2 **Using Certificates for Authentication**
   - 4.3 **Choosing Secrets vs. Certificates**
5. **Implementing OAuth 2.0 and OpenID Connect with Azure AD**
   - 5.1 **OAuth2 and OIDC Fundamentals**
   - 5.2 **Authorization Code Flow (with PKCE) for Web/SPAs**
   - 5.3 **ID Tokens vs. Access Tokens**
6. **Defining API Scopes and Permissions in Azure AD**
   - 6.1 **Creating and Configuring API Scopes**
   - 6.2 **Delegated vs. Application Permissions**
   - 6.3 **Consent (User Consent and Admin Consent)**
7. **Integrating Azure AD into Frontend (React) and Backend (.NET Core)**
   - 7.1 **Configuring Azure AD in a React SPA**
   - 7.2 **Configuring Azure AD in a .NET Core API**
   - 7.3 **Using Tenant ID and Client ID in Code**
8. **Implementing Authentication in the Frontend (React)**
   - 8.1 **Setting Up MSAL (Microsoft Authentication Library)**
   - 8.2 **Logging In and Acquiring Tokens**
   - 8.3 **Calling Secure APIs from React**
9. **Implementing Authentication and Authorization in the Backend (.NET Core)**
   - 9.1 **Enforcing Azure AD Authentication (JWT Validation)**
   - 9.2 **Protecting API Endpoints with [Authorize]**
   - 9.3 **Validating Scopes and Roles in API**
10. **Securing APIs with Azure AD**
    - 10.1 **Token Validation and Middleware**
    - 10.2 **Scope-based Authorization**
    - 10.3 **CORS and Cross-Origin Considerations**
11. **Troubleshooting Common Issues**
    - 11.1 **Authentication Failures and Error Codes**
    - 11.2 **Consent and Token Issues**
    - 11.3 **CORS Errors in SPAs**
    - 11.4 **Misconfigured Redirect URIs**
12. **Lifecycle Management and Best Practices**
    - 12.1 **Client Secret Expiration and Rotation**
    - 12.2 **Certificate Renewal and Rotation**
    - 12.3 **Monitoring and Auditing**
    - 12.4 **Security Best Practices**
13. **Conclusion**

---

## 1. Introduction

This guide is a comprehensive step-by-step tutorial for advanced developers on setting up an **Azure Active Directory (Azure AD)** application and integrating it into both frontend and backend applications. We will cover the entire process from registering an app in Azure AD to implementing OAuth2/OpenID Connect authentication flows, configuring scopes/permissions, and enforcing security in a React single-page app (SPA) and a .NET Core Web API. Along the way, we will incorporate **screenshots, diagrams, code snippets**, and troubleshooting tips. We’ll also highlight **best practices** such as secure secret management, certificate usage, and key rotation to ensure your Azure AD integration remains secure and maintainable over time.

Azure AD (now part of Microsoft Entra ID) provides centralized identity and access management for applications. By the end of this guide, you will have a working knowledge of how to:

- Register Azure AD applications in single-tenant or multi-tenant modes.
- Configure authentication parameters like redirect URIs and expose your own API scopes.
- Use **client secrets** and **certificates** for app authentication and understand when to use each.
- Implement **OAuth 2.0** and **OpenID Connect** flows to authenticate users and authorize access to APIs.
- Set up a React frontend to sign in users and call a protected .NET Core Web API with Azure AD tokens.
- Apply authentication and authorization checks in the backend API (using JWT bearer tokens from Azure AD).
- Secure the entire setup with best practices (least privilege, secret rotations, use of Key Vault, etc.) and troubleshoot common pitfalls.

Let’s begin with the cornerstone: registering your application in Azure AD.

---

## 2. Azure AD Application Registration

Before writing any code, you need to register your application in Azure AD. An **app registration** in Azure AD creates an identity configuration (an **Application object**) that lets Azure AD know about your app and what permissions or features it needs. This is required for Azure AD to issue tokens to your application. We will walk through registering two applications in Azure AD:

- A **frontend client** (React SPA).
- A **backend API** (.NET Core web API).

Typically, you register **one application per component**: one for the client (which will authenticate users and acquire tokens) and one for the API (which will accept tokens). In some scenarios, a single app registration can be used for both front and back end (when the app is purely server-rendered web app), but for SPA + API architecture, separate registrations are recommended for clarity and security.

During registration, Azure AD will assign a unique **Application (client) ID** to each app. You will also get a **Directory (tenant) ID** representing your Azure AD tenant. These IDs will be used in your application code/configuration later. _(After registration, the Azure portal’s Overview page for the app shows the **Application (client) ID** and **Directory (tenant) ID** ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=8,in%20your%20application%20source%20code)).)_

One key choice during registration is whether your app is **single-tenant or multi-tenant**. This determines who can sign in to your application:

### 2.1 Single-Tenant Application Registration

A **single-tenant** application is intended for use only within _your organization’s Azure AD tenant_. Only users (or guest users) in your Azure AD directory can access the app ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant)). This is common for line-of-business (internal) applications where you don’t need to allow access to users from other organizations. Azure AD refers to this option as "**Accounts in this organizational directory only**" (in the Azure portal registration UI).

**Steps to register a single-tenant app:**

1. **Open Azure AD App Registrations:** Log in to the [Azure Portal](https://portal.azure.com) and navigate to **Azure Active Directory** > **App registrations**. Ensure you have the right Azure AD tenant selected (use the directory switcher if you have multiple tenants) ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=1,at%20least%20an%20Application%20Developer)).
2. **Start New Registration:** Click **New registration** to create a new application entry ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=3.%20Browse%20to%20Identity%20,registrations%20and%20select%20New%20registration)).
3. **Name the Application:** Enter a friendly **Name** for your app (e.g., "My Company React Client" or "My Company API"). The name is for your reference and can be changed later; it does not affect functionality ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=4,app%20within%20the%20identity%20platform)).
4. **Supported Account Types:** Choose **“Accounts in this organizational directory only (Single tenant)”** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Accounts%20in%20this%20organizational%20directory,in%20your%20tenant)). This ensures only users in _your_ Azure AD tenant can sign in. (We’ll cover multi-tenant in the next section.)
5. **Redirect URI (optional):** For now, you can leave Redirect URI blank or set it later. We’ll configure redirect URIs in section 3.1.
6. **Register:** Click **Register** to create the application ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=6,URI%20in%20the%20next%20section)). After a moment, you will be taken to the app’s **Overview** page. Here, note down the **Application (client) ID** and **Directory (tenant) ID** – you will need these for your code configuration ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=8,in%20your%20application%20source%20code)).

   _Screenshot: After registering, the Overview page lists the application’s “Client ID” and “Tenant ID”, which uniquely identify your app in Azure AD ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=8,in%20your%20application%20source%20code))._

7. _(Repeat as needed)_: If you are setting up both a frontend and an API, create **two** app registrations. For example, register "My Company React Client" as a SPA client app (single-tenant) and "My Company API" as a web API (single-tenant). Each will get its own Client ID. We will configure their specific settings (redirect URIs, scopes, etc.) in upcoming sections.

**Explanation:** In a single-tenant scenario, the app trusts only the Azure AD instance of your organization. This is suitable for internal apps. Azure AD calls this a Line-of-Business application ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Often%20called%20a%20line,to%20provide%20to%20multiple%20organizations)). The benefit is simplicity – no other tenant’s admins or users can attempt to use your app. The downside is you cannot easily expand to other organizations without converting to multi-tenant (which is possible later if needed ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=6,select%20Help%20me%20choose%20option)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant))).

### 2.2 Multi-Tenant Application Registration

A **multi-tenant** application can be used by users from **other Azure AD tenants** (other organizations), not just your own. This is typical for software-as-a-service (SaaS) applications. When another organization’s user tries to sign in, Azure AD will prompt an admin in that org to consent to your app accessing their user’s data (if permissions require it). Multi-tenancy is enabled by choosing the option **“Accounts in any organizational directory”** or **“Accounts in any organizational directory and personal Microsoft accounts”** during registration ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=This%20type%20of%20app%20is,the%20widest%20set%20of%20customers)).

**Steps to register a multi-tenant app:**

1. **New Registration:** In **Azure AD > App registrations**, click **New registration**.
2. **Name:** Provide a name for the app (e.g., "Contoso SaaS App").
3. **Supported Account Types:** Select **“Accounts in any organizational directory (Any Azure AD directory - Multitenant)”** if you want to support Azure AD users from any org **or** select **“Accounts in any org directory **and** personal Microsoft accounts”** if you also want to allow Microsoft Accounts (MSA) like Outlook.com or Xbox accounts ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=This%20type%20of%20app%20is,the%20widest%20set%20of%20customers)). The latter option is the broadest audience, including both work/school accounts and personal accounts.
4. **Redirect URI:** (Optional at this point; can be added later in Authentication settings.)
5. **Register:** Click **Register** to create the multi-tenant app. Note down the **Client ID** as before. The **Tenant ID** for your own tenant is shown, but note that in a multi-tenant scenario, tokens could come from other tenants. We will typically use a special authority "common" or "organizations" in our code to handle multi-tenancy (discussed in section 7.3).

**Additional notes:** When an app is multi-tenant, it means it has one **application object** in its home tenant (your tenant where you registered it), but when users from other tenants consent to it, a corresponding **service principal** (enterprise app) is created in their tenant. You don’t necessarily see those, but it's how Azure AD represents the app in each tenant. The key point is to ensure that the sign-in and API permission flows (consent, etc.) are handled correctly for other tenants. We’ll discuss consent in section 6.3.

You can convert an existing single-tenant app to multi-tenant by changing the “Supported account types” in the app’s Authentication settings if needed ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=6,select%20Help%20me%20choose%20option)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant)), but it may require users in other tenants to consent. It’s often easier to decide up front.

With our app registrations in place, we can move on to configuring important settings like redirect URIs and exposing APIs.

---

## 3. Configuring Redirect URIs and Exposing APIs

After initial registration, two crucial configurations usually follow: setting up **Redirect URIs** (and other platform-specific settings) and **exposing APIs (scopes)** if your application provides an API. We will tackle each in sub-sections.

### 3.1 Redirect URIs and Platform Configurations

A **Redirect URI** (also known as reply URL) is the location where Azure AD will send authentication responses (tokens or authorization codes) back to your application. It’s essentially the URL in your app that Azure AD will redirect to after a user successfully signs in (or after other token flows). You must configure redirect URIs in Azure AD so that Azure knows which URLs are allowed – for security, Azure AD will only redirect to URLs you have registered.

**How to configure Redirect URIs:**

1. In the Azure portal, go to your app registration (e.g., your **Client SPA** registration). Under **Manage**, select **Authentication** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=1,App%20registrations%2C%20select%20your%20application)).
2. If you haven’t added a platform yet, click **“Add a platform”**. Choose the platform that matches your application type:
   - For a **React SPA** or any single-page application running in a browser, choose **Single-page application**.
   - For a traditional server-side web app (e.g., ASP.NET MVC), choose **Web**.
   - There are other options (Mobile, Desktop, etc.) as well, but we focus on SPA and Web here.
3. After selecting the platform:
   - **Redirect URIs:** Enter the URI where your app will handle the OAuth/OIDC response. For example, for a local React dev server you might put `http://localhost:3000` or `http://localhost:3000/auth-callback` (depending on your routing). For a deployed app, it would be your HTTPS URL, e.g. `https://myapp.com/auth-callback`.
   - If you selected **Single-page application** platform, the URI will be treated as a SPA redirect (with special CORS handling, see note below). If you selected **Web**, you can also specify front-channel logout URLs and implicit flow settings (for SPAs, Azure AD uses the Auth Code with PKCE flow by default).
4. **Implicit Grant Settings (for SPAs):** Under **Implicit grant and hybrid flows** (visible under **Web** platform in portal), you might see checkboxes for "ID tokens" or "Access tokens". In modern applications, for SPAs using MSAL.js 2.x, you do **not** need to enable implicit flow. Instead, use the Authorization Code flow with PKCE. If migrating from older implementations, you might have these enabled. (For new SPAs, you can leave them unchecked; MSAL will use the auth code flow.)
5. **Save** the changes.

**Redirect URI considerations:** Make sure the scheme/host/port exactly match what your app will use. For example, `http://localhost:3000` is different from `http://localhost:3000/` with a trailing slash in Azure AD’s eyes. Also, consider adding URIs for both development and production environments. Azure AD allows multiple redirect URIs; you might add one for local testing and one for the deployed site. Be cautious not to leave any unnecessary redirect URLs, especially broad ones, once in production (attackers could potentially intercept codes meant for a deprecated URL). As Microsoft docs note, it’s common to include local addresses for testing but not to expose them in production registrations ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=In%20a%20production%20web%20application%2C,registrations%20for%20development%20and%20production)).

**SPA Redirect URI Type:** In recent Azure AD (Entra ID) features, when you add a SPA redirect URI, Azure AD internally marks it as type "spa". This enables certain security measures. Specifically, Azure AD enforces **Proof Key for Code Exchange (PKCE)** for that redirect and blocks some flows that aren't appropriate for SPAs. If you attempt to use an OAuth flow in a SPA without properly adding a SPA redirect, you may encounter CORS errors. For example, using an auth code flow without the SPA redirect type can result in errors about missing `Access-Control-Allow-Origin` ([Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#:~:text=,the%20Microsoft%20Entra%20admin%20center)). Thus, always configure your SPA’s redirect URIs using the **Single-page application** platform type. (If you created your SPA registration before this feature existed, you can edit the manifest to set `replyUrlsWithType` to ensure it’s marked as SPA with `type`: `spa`.)

**Web URIs (Web Platform specifics):** If your application was a server-side web app, you’d use the **Web** platform. There you specify a redirect URI (e.g., `https://mywebapp.com/signin-oidc` for an OpenID Connect middleware). You can also specify a **Logout URL** (where Azure AD redirects after a user logs out, to properly end their session in your app). For SPAs, the logout redirect can be handled in code (MSAL provides a logout function that clears cache and can redirect). Additionally, under Web’s implicit flow settings, if you absolutely need to use implicit flow (legacy SPA), you’d check ID token or access token issuance. However, as mentioned, implicit flow is generally deprecated in favor of auth code + PKCE. Azure AD’s documentation explicitly recommends using the auth code flow with PKCE for SPAs instead of implicit ([Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#:~:text=application%20manifest%20editor%20in%20the,Microsoft%20Entra%20admin%20center)).

**Summary:** The redirect URI tells Azure AD where to send tokens. Always double-check this configuration if you get errors after login (many issues arise from mismatch between the URI in code vs. the one registered). We will see this again when we implement the client (React) – the library (MSAL) must be configured with the same redirect URI.

### 3.2 Exposing an API (Defining Scopes)

If your application includes a **Web API** (as our .NET Core API does), you need to configure that app registration to **expose API scopes**. By exposing an API and defining scopes (also known as **Delegated Permissions**), you declare to Azure AD and client apps “these are the permissions that can be granted/tokens that can be requested to access this API.” For example, you might define a scope called `API.Read` or `API.Write` that client applications can request in their access tokens. The API will then enforce these scopes to allow or deny calls.

Think of scopes as permission **names** that your API understands. A client can request one or multiple scopes when getting a token. Azure AD, upon user consent, will issue an access token with those scopes in the `scp` claim (or roles in the `roles` claim for application permissions, which we’ll discuss separately).

**How to expose an API and add scopes (in Azure Portal):**

1. In Azure AD, go to your **API’s app registration** (the one representing your backend API).
2. Under **Manage**, select **Expose an API**.
3. If this is the first time you’re exposing an API for this app, you’ll see an **Application ID URI** at the top. This is a unique identifier for your API in the format `api://<client-id>` by default. You can click **Set** to customize it. For instance, you could change `api://<GUID>` to `api://mycompany-api` if you prefer a friendlier URI, as long as it’s globally unique in your tenant. If you do change it, save the new URI. Otherwise, you can accept the default `api://{ClientID}` which is fine in most cases ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=1,Then%20enter%20the%20following%20information)).
4. Next, click **Add a scope**. A form will appear for defining a new scope. Fill in the details:
   - **Scope name:** Choose a name for the scope (no spaces, typically use dot notation or something descriptive). For example, `API.Read` or `Forecast.Read` (as in Microsoft’s example) ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=1,State%20is%20set%20to%20Enabled)). This name will appear in tokens (in the `scp` claim) if granted.
   - **Who can consent:** Choose **Admins and users** if both regular users and admins can consent to this scope, or **Admins only** if it’s a high-privilege scope requiring admin approval. For most general scopes, "Admins and users" is fine (it means a user can consent for themselves in single-tenant or the first user from an org can consent in multi-tenant if they have permissions). ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=1,State%20is%20set%20to%20Enabled))
   - **Admin consent display name / description:** A friendly title and description that an admin will see when consenting. E.g., _"Read access to Example API"_ and _"Allows the app to read data from Example API."_ Make these clear because admins in other tenants will read this to decide whether to trust your app. ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=2,State%20is%20set%20to%20Enabled))
   - **User consent display name / description:** Similar friendly text if a user consents for themselves. Often you can use the same wording (perhaps less technical). E.g., _"Read your data in Example API"_ etc. ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=3,State%20is%20set%20to%20Enabled))
   - **State:** Ensure it’s **Enabled** (it will be by default). This allows the scope to be used.
5. Click **Add scope** to save it. If everything is filled out correctly, you should now see your new scope listed in the “Exposed API” list for the app ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=7,the%20Expose%20an%20API%20pane)). For example, if you added `API.Read`, it might show as `api://<your-client-id>/API.Read` in the list.

_(Screenshot: In “Expose an API,” after adding a scope named `Forecast.Read`, it appears in the list with its properties ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=1,State%20is%20set%20to%20Enabled)).)_

Now your API app registration declares a scope that client apps can request. In our running example:

- The API app (e.g., "My Company API") might have a scope `API.Read` exposed.
- The client app (e.g., "My Company React Client") will later be configured to request the `API.Read` scope and will need permission to do so.

A **key concept**: When a client requests an access token for your API, it specifies the scope in the request. Azure AD then issues a token **for that API** with the `scp` claim containing that scope, provided the user (or admin) has consented to your app having that permission. The web API (your backend) must check the token’s scopes to decide if the call is allowed. We will cover implementing that check in section 9 and 10, but as a preview: if the token does not have the required scope, the API should reject the request (usually with HTTP 403 Forbidden). Azure AD itself doesn’t enforce scope in the token on the API’s behalf – it’s up to the API’s authorization logic. (However, Azure AD ensures that a token for your API **cannot have scopes your API didn’t define** and vice versa.)

In summary, _exposing an API_ is how you **define delegated permissions (scopes)**. Client apps will request these permissions and the user/admin will consent to them. Azure AD’s documentation emphasizes that a web API will only perform the requested operation if the access token it receives contains the required scopes ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=Once%20the%20API%20is%20registered%2C,receives%20contains%20the%20required%20scopes)).

We have set up one scope, but you can add multiple scopes if your API has different permission levels. For advanced cases, Azure AD also supports **App Roles** (which can be used for application permissions or to assign roles to users in enterprise apps). For example, you might define an app role "Admin" that only certain users can have via assignment. This is more for application permissions or role-based access inside the tenant. We will primarily use scopes in this guide, but app roles could be considered for more complex authorization (discussed briefly in 9.3).

Next, we need to allow our **client application** to access this scope. That means configuring the client’s registration with an **API permission** to this API. We will handle that in section 6 when discussing permissions and consent.

---

## 4. Application Secrets and Certificate-Based Authentication

Azure AD offers two main credential types for an application (when the app needs to prove its identity to Azure AD, such as in confidential client scenarios or when calling Azure AD protected resources on its own): **client secrets** (a string password) and **certificates** (public/private key pair). These are configured in the **Certificates & secrets** section of the app registration.

Even if your application is just a SPA and a backend API, you will encounter secrets/certs in a few contexts:

- If your backend API needs to call another Azure AD-protected API (like Microsoft Graph or another API), it might use its own credential (secret or cert) in a daemon scenario.
- If you create a server-side client (like a .NET service or daemon app) that uses client credentials flow, you’ll need a secret or certificate to authenticate it.
- For our React SPA and .NET API example, the SPA is a public client (no secret, because it runs in a browser and cannot keep secrets), and the API doesn’t need to log in to Azure AD (it just receives tokens). So strictly for SPA+API, you might not _need_ a secret. However, it’s common in development to generate a client secret for testing tokens, or if using tools like Azure CLI to get tokens for your API. Also, if your API is called by a non-interactive client, a secret/cert is required.

Regardless, understanding how to generate and manage these credentials is important. We also will cover best practices like **key rotation** in a later section.

#### 4.1 Generating Client Secrets

A **client secret** is essentially a password string that the application uses to prove its identity when requesting tokens from Azure AD (in flows like OAuth2 client credentials, or confidential client auth in general). In Azure AD App Registration:

- Navigate to **Certificates & secrets** for your app. Under **Client secrets**, click **“New client secret.”** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=1,Select%20Add))
- Provide a description (e.g., "Dev Secret 2025") – especially useful if you will have multiple secrets over time.
- Choose an expiration period. Azure AD limits secret lifetimes to at most **24 months (2 years)** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=3,after%20you%20leave%20this%20page)). You can choose 6 months, 12 months, 18, 24, or a custom (but if custom exceeds 24 it will be capped). Microsoft recommends using a shorter lifespan, e.g. **6-12 months**, to reduce risk ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=,Select%20Add)).
- Click **Add** to create the secret. Azure will now display the **secret value** _one time_. **Copy this value** and store it somewhere secure (like a password manager or Azure Key Vault). Once you leave the page, you cannot view the secret value again ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=months,after%20you%20leave%20this%20page)). If lost, you’d have to create a new secret.
- The secret will be listed with its name, creation date, and expiry. The **Secret ID** (also called key ID) is not the secret value; it’s an identifier (GUID) for reference. The value is what you use in authentication.

Use this client secret in your application’s configuration (for example, in a server-side app, you might put it in a configuration file or environment variable that MSAL uses). The client will present this secret when requesting tokens from Azure AD’s token endpoint, proving it is indeed the application that it claims to be.

**Security considerations for secrets:** Secrets are considered less secure than certificates. They are essentially passwords stored in configuration. _Never_ commit them to source code or expose them in client-side code. Treat them like any other production secret: use secure storage (Azure Key Vault, environment variables, etc.) and **rotate them regularly**. We will discuss rotation strategies in section 12.1. Azure AD now even allows an admin to set an app’s secrets policy (like forcing them to have short lifetime or disallow secrets in favor of certs) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)).

During development, a client secret is often used because it’s easy (just copy-paste) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)). But as you move to production, consider switching to a certificate for stronger security ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Sometimes%20called%20a%20public%20key%2C,platform%20application%20authentication%20certificate%20credentials)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)).

#### 4.2 Using Certificates for Authentication

Instead of a client secret, Azure AD apps can use a **certificate** credential. This involves generating or obtaining an X.509 certificate (which has a private key). You then **upload the public key** (certificate) in Azure AD, and the application holds the private key. When authenticating, the application signs a JWT or sends a signed assertion using its private key, and Azure AD verifies it using the public key.

**Adding a certificate to Azure AD App Registration:**

- Go to **Certificates & secrets** for the app. Under **Certificates**, click **“Upload certificate.”** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=1,Select%20Add))
- You need a certificate file in `.cer`, `.pem`, or `.crt` format (which contains the public key). This typically means you have generated a certificate and have both a public and private key. For example, you might create a self-signed certificate for this purpose, or use your organization’s certificate authority to issue one. Export the public part as a .cer file.
- Select the file and upload it ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=application,Select%20Add)). Azure will extract the info and show a thumbprint and other details if it’s successful. You do **not** get any secret value string here, since the secret is the private key which you keep separately (Azure never asks for your private key; it only stores the public portion).

Once added, the certificate will appear in the list with its thumbprint and expiration date. The app can now use that certificate to authenticate. For example, in a .NET app using Microsoft.Identity.Client (MSAL .NET), instead of providing a ClientSecret, you’d load the certificate from a store or file and configure the confidential client with it.

**Why use certificates?** Certificates are considered **more secure** than client secrets, because possession of the certificate’s private key can be more tightly controlled, and the private key can be stored in secure containers (like a hardware security module or Azure Key Vault) that make it harder to exfiltrate. Also, certificates can have lifetimes (often longer than 2 years, though you should still rotate them regularly). Microsoft’s guidance is to use certificates for production applications instead of secrets whenever possible ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Sometimes%20called%20a%20public%20key%2C,platform%20application%20authentication%20certificate%20credentials)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)).

In summary, a certificate adds security but also slightly more complexity (you must manage the certificate files or use Key Vault integration, etc.). We will revisit certificate usage in section 12.2 (key rotation and management).

#### 4.3 Choosing Secrets vs. Certificates

To decide between using a client secret or a certificate for your Azure AD app:

- **Use client secrets for:** development, testing, or low-risk scenarios where simplicity is needed and the client can’t easily use a certificate. Also acceptable for internal apps with short-lived secrets and good vaulting practices, but be mindful of the security risk.
- **Use certificates for:** production applications, especially those running on servers (web apps, background services) where you can securely store a certificate. Certificates greatly reduce the chance of credential leakage (for instance, an attacker who somehow reads your app’s config cannot directly see a plaintext secret if a cert is used; the private key would ideally be protected). Azure AD and security experts recommend certificates over secrets for any serious deployment ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)).

Keep in mind, not all application types can even use a secret: **Public client** applications (like our React SPA or mobile apps) cannot keep a secret safe (anything shipped to a user’s device or browser is essentially public), so Azure AD treats them as public clients – they are not allowed to use client_credentials flow by themselves. They always need a user context to get tokens (or use other means like proof of code exchange). So our **React frontend will not have a secret or certificate** at all. It will use user login + token flows. Our **.NET Core API** also does not need to present a secret to accept tokens. However, if our .NET API needed to call another API, it might need its own credential to perform the on-behalf-of flow or client credential flow – in that case we’d lean towards using a certificate.

**Summary:** A client secret is a simple string for app auth (easier but less secure), a certificate is a stronger credential (preferred for security). Whichever you use, treat them as sensitive credentials: store them securely and rotate them regularly (e.g., regenerate a new secret prior to expiry and update your apps to use it, or generate a new certificate when the old one expires or is compromised). Azure AD allows multiple active secrets/certs at once, so you can overlap during transitions.

---

## 5. Implementing OAuth 2.0 and OpenID Connect with Azure AD

With the app registered and configuration in place, let’s discuss how authentication actually happens. Azure AD is an **OpenID Connect (OIDC)** and **OAuth 2.0** provider. OIDC is an extension on top of OAuth 2.0 that adds identity (login) capabilities to OAuth’s authorization framework.

Understanding the flows will help debug issues and make the right implementation choices. We’ll focus on the **Authorization Code flow** (with PKCE for SPAs) for user login and obtaining tokens, since that is the recommended approach for web apps and SPAs connecting to APIs.

### 5.1 OAuth2 and OIDC Fundamentals

**OAuth 2.0** is an authorization protocol that allows a “client” application to obtain limited access (in the form of tokens) to a protected resource (like an API) on behalf of a resource owner (user). **OpenID Connect** builds on OAuth2 to provide authentication (issuing an ID Token that represents the user’s identity).

In an Azure AD context:

- Azure AD is the **Authorization Server (Identity Provider)** ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=Image%3A%20Diagram%20showing%20the%20OAuth,0%20roles)). It handles user authentication and issues tokens.
- The **Client** is your application (e.g., the React SPA or a server app) that needs tokens ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Client%20,client%20application%2C%20application%2C%20or%20app)).
- The **Resource Server** is typically your Web API (the protected resource that requires a token) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Resource%20server%20,or%20deny%20access%20to%20resources)).
- The **Resource Owner** is the user who owns the data or resource and is granting access (when user is involved, like delegated permission, the user is resource owner) ([OAuth 2.0 and OpenID Connect protocols - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols#:~:text=%2A%20Resource%20owner%20,user%20can%20consent)). In some flows (client credentials), there is no user – the app itself is the resource owner in a sense, or it's accessing on behalf of itself.

During an OAuth/OIDC **authorization flow**, the client interacts with Azure AD through certain endpoints (authorization endpoint, token endpoint) to authenticate the user and/or get tokens. Azure AD supports standard OAuth2 flows such as Authorization Code, Implicit (legacy, not recommended), Client Credentials, Device Code, etc., and OIDC for user sign-in.

**ID Token vs Access Token:**

- An **ID Token** is a JWT issued by Azure AD that contains information about the user (their identity) and is meant for the client. It’s issued as part of OIDC. The client (like our React app) uses the ID token to verify the user’s identity and establish a session. ID tokens are not meant to call APIs (they aren’t accepted by resource servers typically).
- An **Access Token** is a JWT (or opaque token in some cases) that grants access to a resource (like your API). It usually has a limited scope (the permissions) and audience (who it’s for). The client obtains an access token and includes it in requests to the API (usually in the HTTP Authorization header as `Bearer <token>`). The API then validates the token.

OpenID Connect basically says: in the Authorization Code flow, if you ask for the `openid` scope (and possibly `profile`, `email` scopes), Azure AD will include an ID token in the response. The presence of an ID token is what lets the client know “authentication successful, here’s who signed in.” Meanwhile, including other scopes (like your API’s scope) in the request will make Azure AD issue an access token for that resource.

**Basic OAuth2 Authorization Code Flow (with OIDC):**

1. **Authorization Request:** The client (React app) redirects the user to Azure AD’s **/authorize** endpoint with query parameters including:
   - client_id (identifies the app),
   - response_type (e.g., `code` for auth code flow, or `code id_token` in some hybrid cases),
   - scope (e.g., `openid profile api://.../API.Read` etc., i.e., what permissions we want),
   - redirect_uri (where to return after login),
   - state (random string to maintain state, prevent CSRF),
   - code_challenge (for PKCE, a hashed random value) and code_challenge_method if using PKCE (which SPAs must).
   - etc.
2. **User Login & Consent:** Azure AD shows a login screen (if not already signed in) for the user to enter credentials. If the user needs to consent to permissions (in multi-tenant or first time use), Azure AD will display a consent prompt listing the scopes the app requested (like “This app will be able to read your profile and read data from X API”). The user (or admin) consents.
3. **Authorization Response:** If successful, Azure AD redirects back to the **redirect_uri** with an **authorization code** (a one-time code) in the query string (and the original state for validation). If it was an implicit flow, tokens could be returned here instead, but we’re focusing on code flow.
4. **Token Request:** The client app now takes that authorization code and sends a back-channel request to Azure AD’s **/token** endpoint. This request includes:
   - grant_type=authorization_code,
   - code (the received auth code),
   - client_id & (for confidential clients) client_secret or client_assertion (for public SPA, no secret needed),
   - redirect_uri (must match what was used in step 1),
   - code_verifier (the plain PKCE value corresponding to the code_challenge in step 1, if PKCE was used).
5. **Token Response:** Azure AD validates everything and responds with tokens, typically: **id_token**, **access_token**, and **refresh_token** (if offline access was requested). In our scenario:
   - `id_token` (JWT) for the user’s identity, containing claims like name, email, oid (user’s object ID), etc.
   - `access_token` (JWT) that is intended for your API (with audience = your API’s App ID URI or client ID, and containing the `scp` claim with the scope like API.Read).
   - `refresh_token` (long-lived token that can be used to get new access tokens when the current one expires, without user interaction).
6. **Client Use of Tokens:** The React app can now consider the user logged in (establish session with ID token info) and can call the API by attaching the access token in requests.
7. **API Receives Token:** The .NET API receives the HTTP request with an `Authorization: Bearer <access_token>` header. The API’s authentication middleware (JWT Bearer) will validate the token: signature (using Azure AD’s public keys), issuer (Azure AD tenant), audience (matches the API’s identifier), and expirations. If valid, the user/principal is authenticated. The API then needs to check authorization, e.g., does the token have the required `scp` (scope) or perhaps an `roles` claim if using app roles. If yes, the API performs the requested action; if not, it returns 403. We’ll detail this in section 9 and 10.

This is the general flow. The good news is we rarely have to implement these steps manually. Instead, we use libraries:

- **MSAL (Microsoft Authentication Library)** in the client (for JS, .NET, etc.) which handles steps 1-5 for us. You rarely have to manually craft the /authorize or /token requests.
- **Middleware or library in the API** (like ASP.NET’s JWT Bearer authentication or Microsoft.Identity.Web) which handles validating tokens in incoming requests.

However, knowing these steps helps when something goes wrong (like a redirect URI mismatch causing an error in step 3, or an invalid scope causing no token issued, etc.).

**Why PKCE for SPAs?**  
Proof Key for Code Exchange (PKCE) is a mechanism to prevent authorization code interception. SPAs (public clients) cannot keep a client secret, so PKCE acts as a secure one-time secret. The SPA sends a hash of a secret (code_challenge) in step 1 and then the actual secret (code_verifier) in step 4. If an attacker intercepted the auth code in step 3, they couldn’t exchange it without the code_verifier. Azure AD requires PKCE for SPA redirect URIs by default ([Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#:~:text=,the%20Microsoft%20Entra%20admin%20center)), which is good.

### 5.2 Authorization Code Flow (with PKCE) for Web/SPAs

For modern web applications and SPAs with Azure AD, the **OAuth2 Authorization Code Flow with PKCE** is the recommended approach. Let’s break down specifics for our scenario:

- **React SPA**: It will use MSAL.js (or MSAL React) to perform an authorization code flow. Under the hood, MSAL will do a redirect or popup to Azure AD’s authorize endpoint. Because our app is SPA type, MSAL will include a PKCE challenge. Azure AD will return an auth code to our redirect URI, and MSAL will then exchange it for tokens (this happens via a hidden request, often using `fetch` or an iframe depending on library settings, since CORS is allowed for token endpoint when using SPA type redirect). The end result: MSAL gives us an ID token and access token in the browser. The tokens are usually stored in memory or session storage by MSAL (not in insecure cookies or localStorage if possible, though MSAL by default uses sessionStorage which is generally acceptable for tokens).
- **.NET Core Web App** (if we had one): It would likely use the server-side OpenID Connect middleware or MSAL .NET to do the code flow. In that case, a client secret would be used on the token request (because it’s a confidential client). But for our React SPA, no secret is used (only PKCE).

**Token version (v1 vs v2 endpoint):** Azure AD has two endpoint versions: v1 and v2. The app registrations we created (especially if we used scopes) operate on the v2 endpoint (the Azure AD **Microsoft Identity Platform** endpoint). By default, when you request tokens for custom scopes like `api://.../scope`, you’re using the v2 endpoint. If you see an issuer like `https://sts.windows.net/...` and scope in JWT is missing or using `roles` claim, that might indicate a v1 token. In our case, since we set **`accessTokenAcceptedVersion` = 2** (which is default for new app registrations or configurable in the manifest) and use scopes, we should get v2 tokens. A common problem is getting an unexpected v1 token – often fixed by ensuring the scope is requested correctly and that you’re using the v2 authorize endpoint (`https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize` vs older `oauth2/authorize`). MSAL libraries by default use v2.

Azure AD’s v2 endpoint issues tokens with an `scp` claim for scopes. V1 issues an `roles` claim for delegated permissions (and uses resource-specific consent). The presence of `scp` and an issuer containing `login.microsoftonline.com/{tenant}/v2.0` indicates a v2 token, which is what we want. We might mention this if troubleshooting a case where someone ends up with an issuer `sts.windows.net` (which is v1) – the fix is usually to use the v2 endpoint or set accessTokenAcceptedVersion in the app manifest.

**OpenID Connect scope:** One must include the `openid` scope in the auth request to get an ID token (and `profile` to get basic user info claims). MSAL will handle this if you specify you want an ID token or if you login with an OpenID scope. If ID tokens are not being returned when expected, ensure the app has "ID Tokens" enabled (for web apps) or the scopes include `openid` (for SPAs, MSAL includes it by default in login requests). If ID tokens are not enabled for the app, Azure AD would throw an error like _“the provided value for the input parameter 'response_type' isn't allowed for this client. Expected value is 'code'”_, meaning ID token implicit was not allowed ([OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#:~:text=6,checkbox)) ([OpenID Connect (OIDC) on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#:~:text=If%20ID%20tokens%20aren%27t%20enabled,error%20similar%20to)). For SPAs using code flow, this usually isn’t an issue, as MSAL will just request code+PKCE and then get an ID token in the token response.

In summary, the **auth code with PKCE flow** will be used by our React app to sign in users and get tokens for our API. We’ll rely on MSAL to handle it, which simplifies our job to basically configuring MSAL and calling the login function.

### 5.3 ID Tokens vs. Access Tokens

It’s worth reiterating the difference because it affects how you implement authentication vs. authorization:

- **ID Token:** proves the user’s identity to _your application_. It’s consumed by the client app. In a typical web app, the presence of a valid ID token means the user is authenticated, and you can create an app session for them. It often contains claims like name, email, `preferred_username`, and a unique ID (`oid` – object ID, or `sub`). In our case, the React app will get an ID token and could use it to display user info or store it in client state. The .NET API might never see the ID token (the API only cares about access tokens). _Important:_ ID tokens should not be used to call APIs; they are not meant for authorization to resources. They also usually have a short lifetime (often same as access token, but they cannot be refreshed by themselves except by redoing sign-in).
- **Access Token:** is a credential the client passes to the resource/API to access it. It usually has an `aud` (audience) claim equal to the API’s identifier (e.g., the client ID of your API or the Application ID URI) so that the API knows the token was indeed meant for it. It contains `scp` if issued for a user (delegated scenario) or `roles` if it’s an application token with app roles, and possibly other data like `oid` (user id) if delegated, etc. The .NET API will require a valid access token. The React app obtains this token via MSAL and attaches it to each request. Access tokens have an expiration (commonly 1 hour for Azure AD defaults). After expiration, the client should use a refresh token or silent re-auth to get a new one.

**Refresh Tokens:** Azure AD’s v2 endpoint supports returning a refresh token in SPA scenarios if you request the `offline_access` scope. MSAL can handle token refreshing for you under the hood (it uses an hidden iframe or refresh token in memory to get new access tokens without user interaction). We won't dive deep into refresh tokens here, but know that they allow long-lived sessions without forcing the user to log in frequently. They should be stored securely (MSAL handles this in memory or session storage for SPAs).

Now that we understand the protocol side, let’s start integrating these concepts into our actual applications – starting with ensuring our Azure AD registrations have the necessary **permissions** set up for the client to access the API.

---

## 6. Defining API Scopes and Permissions in Azure AD

In section 3.2, we _exposed_ a scope on the API app. Now we must allow the **client app** to use that scope. This is done by adding an **API permission** to the client app registration, linking it to the API’s scope. This process also ties into the consent framework of Azure AD.

### 6.1 Creating and Configuring API Scopes

_(This subsection recap: We already created a scope in 3.2 on the API. If you have not done so, do that first. In this example, assume we created a scope named `API.Read` on the API app.)_

After creating the scopes on the API app registration, they become available for client apps to reference.

### 6.2 Delegated vs. Application Permissions

When adding an API permission to a client, Azure AD will ask whether it's a **Delegated permission** or an **Application permission**:

- **Delegated Permission:** This is a permission that a client app is requesting on behalf of a signed-in user. It requires a user present (interactive or through refresh token) and the resulting access token will have an `scp` (scope) claim. Delegated permissions usually require user consent (or admin consent if the permission is high-privilege or if in a multi-tenant scenario where user cannot consent). In our React-to-API scenario, we use delegated permissions because the React app calls the API as the signed-in user. Azure AD will treat the access as the user’s context (the user’s identity is in the token via `oid` claim, etc.).
- **Application Permission:** This is used by a **daemon or server client** without a user. It represents the app calling the API as itself (e.g., a background service). These are often called **app roles** in the API registration. If we had defined an app role in the API (which appears under "App roles" in the registration, and marked as allowedMemberTypes = Application), then a client could request that as an application permission. The token in that case would carry a `roles` claim (not `scp`) and no user information (because it’s the app identity). Application permissions always require an admin consent, since they typically grant broad access (no user to constrain them). In our scenario, we likely don’t need any application permission unless we have a daemon client. So we will stick to delegated.

Given we defined a scope, that's a delegated permission by nature. Azure AD will not even show an application permission option for your API unless you define **app roles** for application usage ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=permissions%20you%20select%20in%20the,permissions%20selected%20for%20this%20example)). In the quickstart example, they note that _“Unless you've defined application roles for your web API, [the Application permissions] option is disabled.”_ ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=for%20this%20example)).

### 6.3 Consent (User Consent and Admin Consent)

**Consent** is the process where a user or admin grants the client app permission to access the specified resource (API) on the user’s behalf. In Azure AD:

- If a scope is marked "Admin and users can consent", a non-admin user can consent for themselves, but only within their own tenant. In a single-tenant app, when you first sign in, Azure AD might just grant consent silently because you are the owner, or it might prompt if you’re not an admin but the API requires admin? In our case, if both client and API are in the same tenant, and you (the developer/admin) are testing, you can pre-consent in the portal to avoid interactive prompts.
- In a multi-tenant app, the very first time a user from another tenant tries to sign in to the client that requests a certain API scope, that user will see a consent screen listing the permissions. If the scope is "Admins and users can consent", they (if regular user) can consent only for themselves – which in effect still allows them to get a token for that session. If the scope is admin-only, or if tenant policies prevent user consent, then an **admin must consent**. The user would see “need admin approval” and an admin in that tenant would have to grant consent for the org (via prompt or by doing it in portal using enterprise apps blade).

**Admin consent** typically means an administrator grants the permission for _all users_ in that tenant. This can be done via:

- The portal: In the **API Permissions** page of the _client app registration_, after adding permissions, an admin can click **“Grant admin consent for [TenantName]”** ([Protect and call an ASP.NET Core minimal Web API with Azure AD](https://markheath.net/post/secure-aspnet-core-web-api-azure-ad#:~:text=select%20,the%20permission)). This will pre-approve the listed delegated permissions for all users. After this, no user in that tenant will be prompted; tokens can be issued immediately.
- The consent screen: An admin user signing in interactively can accept a consent dialog that has an option “Consent on behalf of your organization”. That does the same tenant-wide consent.
- Azure AD Graph/PowerShell/CLI also has ways to grant consent.

For development in a single-tenant scenario, it's convenient to use the portal to grant consent upfront:

1. Go to the **client app registration** (e.g. "My Company React Client") in Azure AD.
2. Under **API Permissions**, click **Add a permission**. Choose **My APIs**, and select your API (e.g., "My Company API"). Then choose **Delegated permission** and check the scope(s) you want (e.g., `API.Read`) ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=4,My%20APIs%20in%20the%20sidebar)) ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=6,in%20user)). Add the permission. Now the permission will show up in the list as **"API.Read (My Company API)"** under Configured permissions, likely with a status "Not granted for <TenantName>".
3. If you are an admin, click the **Grant admin consent for <TenantName>** button. Confirm the prompt. Now the status will change to Granted (with your admin account and date) ([Protect and call an ASP.NET Core minimal Web API with Azure AD](https://markheath.net/post/secure-aspnet-core-web-api-azure-ad#:~:text=select%20,the%20permission)).
   - If you are not an admin, you can still add the permission, but you won't be able to grant for all. In that case, the first user who tries to sign in will get a prompt to consent just for themselves. In a dev/test environment, logging in with an admin or having an admin do this is easier.

At this point, your client is fully allowed to request tokens for that scope. No interactive consent prompt will appear for any user in _your_ tenant. In multi-tenant usage, other orgs’ admins would have to do similar for their users.

**Recap with our example:**

- API app "My Company API" has scope `API.Read`.
- Client app "My Company React Client" has permission to `My Company API / API.Read` (delegated). Admin consent is given in the home tenant.
- When our React app uses MSAL to login and request `API.Read`, Azure AD sees that the app is allowed and either doesn’t prompt at all (if already consented) or will show a prompt if needed (in another tenant scenario). After consent, Azure AD issues the access token with `scp: API.Read`.
- If we hadn’t configured this, the MSAL request for `API.Read` would fail saying the app is not authorized to request that scope, or the user would see a prompt for a permission that might say “(not granted)” which they might not be able to consent to. So this step is crucial.

**Also include Microsoft Graph or other APIs:** In many apps, you might also add permissions to Microsoft Graph (like User.Read) or others. The process is similar (under API permissions, add Microsoft Graph delegated perms, etc.). For completeness, the Microsoft quickstart example also added Graph permissions ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=In%20this%20quickstart%2C%20you%20provide,app%20access%20to%20Microsoft%20Graph)), but in our guide we focus on the custom API.

At this stage, we have completed the Azure AD portal configuration:

- App registrations for client and API (single or multi-tenant as needed).
- Redirect URIs set.
- API scopes defined.
- Client given permission to API scope (with consent handled).
- Credentials (secret/cert) generated if needed (though for our SPA + API, we likely only generated maybe a secret for testing or none at all for the SPA).

Now it’s time to use these in our applications.

---

## 7. Integrating Azure AD into Frontend (React) and Backend (.NET Core)

Next, we integrate the Azure AD authentication into our application code. We will start with the frontend (React SPA) and then the backend API.

### 7.1 Configuring Azure AD in a React SPA

To integrate Azure AD authentication in a React application, Microsoft provides the **MSAL (Microsoft Authentication Library) for JavaScript**. Specifically, there's an `@azure/msal-react` package which is a wrapper around `@azure/msal-browser` for easier React integration. MSAL will handle the details of interacting with Azure AD (redirects, token storage, etc.).

**Installation:** In your React project, install the MSAL libraries:

```bash
npm install @azure/msal-react @azure/msal-browser
```

This gives you React hooks and components (`msal-react`) and the core functionality (`msal-browser`).

**Configuration:** Create an MSAL configuration, typically in a file (e.g., `authConfig.js` or similar). This config includes your Azure AD **client ID**, the **authority** (Azure AD endpoint/tenant), and the redirect URI (and possibly other options).

For example, in `authConfig.js`:

```javascript
import { Configuration } from "@azure/msal-browser";

export const msalConfig = /** @type {Configuration} */ ({
  auth: {
    clientId: "YOUR-SPA-CLIENT-ID-GUID",
    authority: "https://login.microsoftonline.com/YOUR-TENANT-ID-or-common",
    redirectUri: "http://localhost:3000", // your redirect URI
  },
});
```

In the above:

- **clientId** is the Application (client) ID of your React SPA app registration ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=)).
- **authority** is the Azure AD authority to use. This typically is `https://login.microsoftonline.com/<TenantID>` for single-tenant (put your directory’s tenant ID or domain there) or `https://login.microsoftonline.com/organizations` (for multi-tenant business accounts) or `common` (to allow both AAD and Microsoft accounts) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=)) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=Microsoft%20docs%20learn)). For single-tenant, using your tenant ID or domain (like contoso.onmicrosoft.com) ensures only your users. For multi-tenant, `common` is common endpoint for all, or `organizations` to exclude personal MSAs ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=To%20specify%20the%20audience%20in,common)).
- **redirectUri** should match one of the URIs you added in Azure AD. For development, often `http://localhost:3000` (or wherever your React dev server runs). In production, your hosted URL. This is where the app will be redirected after login.

No client secret is used here, because this is a public client running in the browser. The authority URL includes the _tenant context_. If multi-tenant, `common` or `organizations` is used so that users from any tenant can log in. If single-tenant, using your specific tenant means the user _must_ be from your directory (if they try with another, it won’t sign them in).

Optionally, MSAL config can include other fields:

- e.g., `cache: { cacheLocation: "sessionStorage", storeAuthStateInCookie: false }` – controlling token cache location.
- But the basics above are the main required ones.

**Providing MSAL to React app:** In your React app’s entry point (e.g., `index.js` or `App.js`), you wrap your app with the MSAL provider:

```jsx
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import { msalConfig } from "./authConfig";

const msalInstance = new PublicClientApplication(msalConfig);

ReactDOM.render(
  <MsalProvider instance={msalInstance}>
    <App /> {/* Your main app component */}
  </MsalProvider>,
  document.getElementById("root")
);
```

This makes MSAL context available to your components. Now you can use hooks like `useMsal` or components like `AuthenticatedTemplate`/`UnauthenticatedTemplate` from `@azure/msal-react` to handle login logic.

We won't dive deeply into React code here, but a simple approach:

- Create a **login button** that calls `instance.loginPopup()` or `instance.loginRedirect()` (from `useMsal()` hook) with appropriate scopes.
- Manage the login state and retrieve tokens via `instance.acquireTokenSilent` or `acquireTokenPopup` for calling the API.

We know the needed **scope**: we defined (for example) `API.Read` on our API. In Azure AD, the full scope string would be `<Application ID URI>/<scope-name>`. If we left Application ID URI as default `api://<clientId>`, then the scope string might be `api://<API-CLIENT-ID-GUID>/API.Read`. Alternatively, Azure portal might also show a friendly permission name if within the same tenant. But in MSAL, we will specify scopes for token requests.

So in our React app, when calling the API, we might do something like:

```js
const request = {
  scopes: ["api://<YOUR-API-CLIENT-ID>/API.Read"], // the scope we want for the access token
};
const result = await instance.acquireTokenSilent(request);
// result.accessToken now holds a token to call the API
```

If silent token acquisition fails (e.g., first time or token expired with no refresh), MSAL will throw and we may need to call `instance.acquireTokenPopup(request)` or if using redirect flow, ensure that during login we asked for that scope.

Often, one can combine login and consent by calling `loginRedirect` or `loginPopup` with the API scopes included. For example:

```js
instance.loginRedirect({
  scopes: ["User.Read", "api://<API-CLIENT-ID>/API.Read"],
});
```

This would log in the user and also get consent for both Microsoft Graph User.Read (if needed) and our API’s scope in one go. After the redirect back, MSAL should have an access token for the API in its cache (or at least a refresh token to get it). Alternatively, you can login with just openid/profile and later call acquireToken for the API scope (which may cause a second redirect for consent if not yet granted).

For simplicity, you might:

- Call `loginRedirect({ scopes: ["openid", "profile", "api://.../API.Read"] })` on app start or when user clicks login.
- After redirect back, call `acquireTokenSilent({ scopes: ["api://.../API.Read"] })` to get the actual token (though MSAL might already have it).

**Using the token in API calls:** Once you have the `accessToken`, you attach it to HTTP calls. For example, using fetch:

```js
const token = result.accessToken;
const response = await fetch("https://localhost:5001/weather", {
  headers: { Authorization: `Bearer ${token}` },
});
```

Or if using Axios, set the Authorization header similarly.

We will set up our .NET API at `https://localhost:5001` (assuming it runs on 5001 for HTTPS by default) to accept this token.

**Recap for React:**

- Use MSAL React, configure with clientId, authority, redirectUri.
- Initiate login to get tokens (redirect or popup).
- On return, MSAL gives you access token.
- Use access token in API requests.

There are lots of nuances (like handling token expiration, using `AuthenticatedTemplate` to conditionally render UI when logged in, etc.), but this covers the gist needed for integration. The MSAL React library simplifies a lot: for example, it has `<MsalAuthenticationTemplate>` component that can protect routes or trigger login if user not authenticated.

Make sure you also handle **logout**: MSAL’s `instance.logoutRedirect()` can log the user out (it will clear local cache and redirect to Azure AD’s logout endpoint, which then can redirect back to a post-logout URL if configured).

### 7.2 Configuring Azure AD in a .NET Core API

For the ASP.NET Core Web API, we will use **Microsoft.Identity.Web**, a library that streamlines JWT bearer authentication with Azure AD. Microsoft.Identity.Web is essentially an extension over ASP.NET Core authentication that handles Azure AD configuration easily.

**Installation:** In your .NET Core Web API project (assuming .NET 6 or .NET 7 as of writing), install the NuGet package:

```
dotnet add package Microsoft.Identity.Web
```

This also brings in `Microsoft.AspNetCore.Authentication.JwtBearer` as a dependency.

**Configuration (appsettings):** We need to supply Azure AD settings to the API so it knows:

- The Tenant (issuer) to trust tokens from,
- The Client ID (audience) of itself (so it only accepts tokens for itself),
- The allowed scope or audience (though client ID usually covers that).

In **appsettings.json** (or you can use user-secrets or environment vars in production), include a section, e.g.:

```json
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "TenantId": "YOUR-TENANT-ID",
  "ClientId": "YOUR-API-APP-CLIENT-ID",
  "Audience": "api://YOUR-API-APP-CLIENT-ID"
}
```

The `"Audience"` field is sometimes used if your tokens use the api://<clientid> as the aud. In many cases, Azure AD v2 tokens will have aud = clientId or the App ID URI. Microsoft.Identity.Web might handle this automatically. (In Microsoft’s docs, they often omit Audience if using default scheme where audience = clientId is assumed.)

From our earlier quickstart snippet ([Quickstart: Protect an ASP.NET Core web API with the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-web-api-aspnet-core-protect-api#:~:text=2.%20Open%20,contains%20the%20following%20code%20snippet)), they had:

```json
"AzureAd": {
   "Instance": "https://login.microsoftonline.com/",
   "TenantId": "<tenant-id>",
   "ClientId": "<client-id>",
   "Scopes": "Forecast.Read"
}
```

Here "Scopes" was not needed for validation (it was more for downstream calls scenario). What’s needed is mainly tenant and client.

If your API is single-tenant, TenantId can be your tenant’s GUID. If multi-tenant, you might put `common` or leave it as a specific tenant but accept tokens from other tenants by validating issuers (Microsoft.Identity.Web has options for multi-tenant token validation like `ValidateIssuer` etc.). Simpler: If multi-tenant, you might still validate the token’s issuer is among a list of allowed ones (for instance, you may restrict to specific tenants that have onboarded).

For our context, assume single-tenant for simplicity.

**Configure authentication in code:** In your `Program.cs` (for minimal hosting model in .NET 6/7) or `Startup.cs` (older style), you add:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));
```

This single line will:

- Read the AzureAd config section,
- Set up JWT Bearer authentication,
- Configure the authority as `Instance + TenantId` (like `https://login.microsoftonline.com/<TenantId>/v2.0`),
- Configure the valid audience as the ClientId (or app ID URI),
- Enable token validation (signature, issuer, etc.) using Azure AD’s discovery keys.

In our example, since we used Microsoft.Identity.Web and provided TenantId and ClientId, it knows what to do. After this, we add the usual:

```csharp
app.UseAuthentication();
app.UseAuthorization();
```

in the pipeline (make sure these come before app.MapControllers or any endpoints execution).

Alternatively, without Microsoft.Identity.Web, one could manually do:

```csharp
.AddJwtBearer(options => {
    options.Authority = $"https://login.microsoftonline.com/{TenantId}/v2.0";
    options.Audience = "<API-CLIENT-ID or APP-ID-URI>";
    // etc (like validating issuer, etc.)
});
```

But the library saves time and also adds some additional features like easy integration with [RequiredScope] attribute.

**CORS:** Because our client is a SPA on a different origin (localhost:3000) than our API (localhost:5001), we must enable CORS (Cross-Origin Resource Sharing) in the API. So we add something like:

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSPA",
        policy => policy.WithOrigins("http://localhost:3000")
                        .AllowAnyHeader()
                        .AllowAnyMethod()
                        .AllowCredentials());
});
```

And in the pipeline:

```csharp
app.UseCors("AllowSPA");
```

This ensures the browser calls from the React dev server are allowed by the API.

Now our .NET API is set to only accept calls with a valid JWT access token from Azure AD. By default, simply adding `[Authorize]` on controllers or actions will enforce that the user is authenticated (token valid). But we might want to specifically ensure the token has the correct scope.

We’ll cover that in the next section. For now, at this stage:

- If we run the API, unauthenticated calls (no token) will get 401 Unauthorized by the middleware.
- Calls with a token will succeed authentication if token is valid (signature, not expired, etc.); then the [Authorize] attribute will allow into the action. If we have no further checks, any valid token for this API is accepted (even if it had only a subset of scopes). Many APIs might trust that Azure AD only issues tokens with at least one scope if the app is configured properly. But a best practice is to explicitly check the scope claim in the token.

We are ready to test an end-to-end: user logs in via React, gets token, React calls API with token, API validates and returns data.

Before that, let’s solidify how to implement authorization in the API (scopes/roles enforcement) and discuss securing the API.

### 7.3 Using Tenant ID and Client ID in Code

This section is a short note to emphasize how the **Tenant ID** and **Client ID** values we recorded from Azure AD are used in the code:

- In the **React app** configuration (msalConfig), the **Client ID** of the SPA app is used. The **Tenant ID** appears as part of the authority URL (if not using `common`). If multi-tenant, we might not explicitly put Tenant ID in code (using `common`), but if single-tenant, we set the authority to our tenant, effectively embedding the Tenant ID or domain.

  Example: `authority: "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47"` (where that GUID is Tenant ID) or a friendly domain like `contoso.onmicrosoft.com`. If multi-tenant, you might use `common` and then it will allow any tenant, but you might still restrict in API side if needed.

- In the **.NET API** config, the **Tenant ID** and **Client ID** of the API are provided in appsettings for Microsoft.Identity.Web. The Tenant ID tells the JWT middleware to only trust tokens from that tenant (for multi-tenant, one might have to configure it to accept multiple issuers). The Client ID is essentially the identifier for tokens (the API will accept tokens with aud = this client ID or associated App ID URI).

It’s important to ensure these IDs are correct, otherwise tokens will not validate:

- If ClientId mismatches, the token’s audience won’t match and the auth will fail.
- If TenantId mismatches, the issuer won’t match and auth will fail (unless you allow multi-tenant by disabling issuer validation, which you should do carefully if at all).

**Storing configuration securely:** In development, it’s fine to have these in the source (they are not secret). Indeed, a **Client ID and Tenant ID are not sensitive** – they are GUIDs that identify your app and directory, but they cannot be used to impersonate you (without the secret/cert). So it’s okay if these are public. Often front-end code has them visible (and it’s fine, they need to be there to redirect user to correct login). However, treat **Client Secret** or any credentials as highly sensitive (never put those in front-end code or commit to repository in plain text).

In production, you might still have Client ID and Tenant ID in config files or environment variables. They don't need vaulting (again, not secret), but sometimes to keep consistency, they might be kept alongside secrets in a config service.

Now that both front and back are configured, let's implement and verify the authentication/authorization behavior.

---

## 8. Implementing Authentication in the Frontend (React)

Building on the setup from section 7.1, we will outline the steps in the React app for authentication.

#### 8.1 Setting Up MSAL in React

- **MSAL Provider:** As shown, wrap your app in `MsalProvider` with an instance of `PublicClientApplication` configured with your credentials. This makes MSAL available throughout your React component tree.
- **Login Component or Hook:** You may create a component or use the provided `MsalAuthenticationTemplate`. For learning, let's do it manually:
  - Use the `useMsal()` hook from `@azure/msal-react` to get the MSAL instance and accounts.
  - If `accounts` array is empty, user is not logged in. Show a "Login" button.
  - On click of Login, call `instance.loginRedirect({ scopes: ["api://<API-ClientID>/API.Read"] })` or use a popup variant. Redirect is recommended for full redirect scenarios; popup can be good to avoid leaving the SPA, but can be blocked by browsers if not triggered by user gesture.
  - The scopes here include our API scope (and MSAL will automatically include "openid" and "profile").
- **Post Login:** After redirecting to Azure AD and back, the app will initialize again. MSAL will process the redirect and retrieve tokens. The `accounts` will now contain the signed-in user. You can get the account object or just display that the user is logged in (maybe show their username from account name).
- You might also call `instance.acquireTokenSilent({ scopes: ["api://.../API.Read"] })` here to ensure you have an access token handy. However, `loginRedirect` if called with scopes should have already acquired the token for those scopes. MSAL caches it.
- Use `AuthenticatedTemplate` and `UnauthenticatedTemplate` components (provided by msal-react) to easily render different UI for logged-in vs not logged-in states.

For example, in JSX:

```jsx
<AuthenticatedTemplate>
  <div>Welcome, you are logged in!</div>
  <button onClick={callApi}>Call API</button>
  <button onClick={logout}>Logout</button>
</AuthenticatedTemplate>
<UnauthenticatedTemplate>
  <button onClick={login}>Login</button>
</UnauthenticatedTemplate>
```

Where `login` calls `instance.loginRedirect` and `logout` calls `instance.logoutRedirect()`, and `callApi` triggers the API call with token.

#### 8.2 Logging In and Acquiring Tokens

As described:

- When `loginRedirect` is called, MSAL redirects user to Azure AD (with the parameters we discussed). After user enters credentials and consents (if needed), Azure AD redirects back to our redirect URI.
- MSAL's `handleRedirectPromise()` (internally in the library when using MsalProvider, it does this) processes the redirect and obtains the token.
- We now have an **ID token** and **Access token** stored in MSAL’s cache.

To manually get the access token (if needed):

```js
const { instance, accounts } = useMsal();
const request = {
  scopes: ["api://<API-ClientID>/API.Read"],
  account: accounts[0], // ensure we use the correct account
};
instance
  .acquireTokenSilent(request)
  .then((response) => {
    const accessToken = response.accessToken;
    // use the token
  })
  .catch((error) => {
    if (error instanceof InteractionRequiredAuthError) {
      instance.acquireTokenRedirect(request);
    }
  });
```

The above tries silent token acquisition (which will succeed if token is in cache and not expired). If it fails with interaction required, we fall back to redirect (or popup) to let user re-auth (maybe if additional consent needed or session expired).

In many cases, if you logged in with the scope initially, you won't need a separate acquireToken call because MSAL should already have an access token. But token will expire after ~1 hour. At that time, `acquireTokenSilent` will use the refresh token to get a new one. MSAL handles refresh token silently (since v2 endpoints allow CORS on token endpoint when using auth code + PKCE, or it uses hidden iframe if needed).

**Common Pitfalls:**

- Ensure the **redirectUri** in MSAL config exactly matches one in Azure AD. Otherwise, after login, Azure AD will fail to redirect or MSAL will ignore the response.
- If you see a browser error about CORS to login.microsoftonline.com on token request, that means the redirect URI is not marked as SPA. We discussed this: you must either use `Add a platform` -> SPA in Azure AD (which sets `type=spa`) ([Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#:~:text=,the%20Microsoft%20Entra%20admin%20center)). Without it, the token endpoint call from JavaScript is blocked by Azure AD.
- If you get an error like _AADSTS65001: No permission to access user/data as the user or something_, it likely means the API permission wasn’t granted. This would surface as an error during `acquireTokenSilent` or `loginRedirect` saying you need consent. The solution is to grant consent in portal (for dev) or let the user consent.
- If using `loginPopup`, some older browsers block it if not triggered by direct user action. Always tie it to a button click event.

#### 8.3 Calling Secure APIs from React

Now, to call our .NET API:
We have a button or some UI that triggers a fetch/axios call. Within that, ensure we have a token:

```js
const tokenRequest = {
  scopes: ["api://<API-ClientID>/API.Read"],
  account: accounts[0],
};
const response = await instance.acquireTokenSilent(tokenRequest);
const token = response.accessToken;
const apiResponse = await fetch("https://localhost:5001/weatherforecast", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
if (apiResponse.ok) {
  const data = await apiResponse.json();
  console.log(data);
} else {
  console.error("API call failed:", apiResponse.status);
}
```

_(This assumes your API has an endpoint like `/weatherforecast` that requires auth and returns JSON.)_

The **Authorization header** is critical – this is how the browser sends the token to the API. The string is exactly `"Bearer <access_token>"`. The API’s middleware will parse that.

If the token is missing or invalid, our API will return `401 Unauthorized`. If the token is valid but the user lacks a required scope/role, we might return `403 Forbidden` (if we implement scope checking manually).

A note on token storage security: MSAL by default keeps tokens in sessionStorage (which is in-memory per tab). This is relatively safe from other websites (as long as no XSS vulnerability in your app). Avoid storing tokens in localStorage long-term (persistent) as that’s more susceptible to XSS. Use the library’s defaults or configure it thoughtfully. Also, consider using HTTP-only cookies for tokens if doing server side, but in SPA context, MSAL is standard.

At this point, if everything is set up, your React app when logged in should be able to successfully fetch data from the protected API using the obtained token.

To logout, `instance.logoutRedirect()` will redirect to Azure AD logout endpoint (which clears Azure AD session cookie) and then back to a post logout URL (by default it uses your redirectUri, but you can configure one in Azure AD under Authentication “Front-channel logout URL” if needed). After logout, MSAL’s cache is cleared and the user is no longer authenticated in the app.

---

## 9. Implementing Authentication and Authorization in the Backend (.NET Core)

On the backend side, we’ve already configured JWT **authentication** via Microsoft.Identity.Web. Now we focus on **authorization** – controlling access to API endpoints based on the token’s contents (scopes or roles).

### 9.1 Enforcing Azure AD Authentication (JWT Validation)

Thanks to the `AddMicrosoftIdentityWebApi` configuration, **JWT validation** is automatically in place:

- The middleware will validate the token’s signature using Azure AD’s public keys (fetched from the discovery document). This ensures the token was indeed issued by Azure AD and not tampered with.
- It will validate the token’s **issuer** (by default, matches your tenant). So if a token from another tenant is presented and issuer is different, it might reject unless configured as multi-tenant. Microsoft.Identity.Web, by default, might accept `IssuerValidator` that checks if the issuer is any of the tenant IDs in the token’s `tid` claim that matches the configured one or certain allowed ones. If multi-tenant support is needed (like your API should accept tokens from other tenants because your SaaS allows multiple), you need to configure the TokenValidationParameters accordingly (e.g., set ValidateIssuer to false _only if_ you implement your own logic to validate).
- It will validate the **audience** (the token’s `aud` claim should match the API’s App ID). If we set the API’s ClientId in config, it uses that as the expected audience. If Azure AD issues the token with audience as the App ID URI, Microsoft.Identity.Web by default treats the clientId as valid, but it also populates a valid audience as clientId + maybe the URI. There’s a setting to add additional valid audiences if needed (like both the GUID and the api:// URI).
- It checks expiry (`exp`) and not-before (`nbf`) to ensure token is in valid time.

So simply by `[Authorize]` on controllers, we enforce that the caller has a valid Azure AD-issued token for our app ([Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles#:~:text=To%20protect%20an%20ASP,one%20of%20the%20following%20items)). If not, they get 401.

### 9.2 Protecting API Endpoints with [Authorize]

In ASP.NET Core, decorate your controllers or specific actions with the `[Authorize]` attribute (import from `Microsoft.AspNetCore.Authorization`). For example:

```csharp
[Authorize]
[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    [HttpGet]
    public IEnumerable<WeatherForecast> Get() { ... }
}
```

This will require the incoming request to be authenticated. If not, the framework returns 401 before hitting the action.

If you have some endpoints that should be public, you leave them without [Authorize] or explicitly mark as `[AllowAnonymous]`. Perhaps your API has a health check or public metadata endpoint that doesn’t require auth.

By default, [Authorize] without parameters will allow any authenticated user/token. It doesn’t check scope or role yet. It’s usually a good idea to at least check scopes. Otherwise, any token issued to your app, even with no specific scope (which normally doesn’t happen unless you allow the possibility of Azure AD issuing an access token with no delegated permission? Actually, in v2, if a user consented to no permissions, they wouldn't have a token at all. So practically, if they got a token, at least one scope is present, presumably the one they consented. So [Authorize] alone might be enough if you trust that the token having any scope is good enough. But it’s better to be explicit.)

### 9.3 Validating Scopes and Roles in API

**Scope validation:** We want to ensure the token has the scope `API.Read` (or whatever scope is needed for that endpoint). There are a few ways:

- **Manual check in code:** You can inspect the token claims. In ASP.NET, once authenticated, the `HttpContext.User` principal is set. The scopes in a v2 token appear as claims with type `"scp"` (a space-separated list of scopes in one claim) for user tokens. Microsoft.Identity.Web actually parses those and adds individual `Claim` for each scope with type `http://schemas.microsoft.com/identity/claims/scope`. It also does similar for roles (app roles appear in `"roles"` claim or `"scp"` if using graph or such).

  So you could do:

  ```csharp
  if (!HttpContext.User.HasClaim("http://schemas.microsoft.com/identity/claims/scope", "API.Read"))
      return Forbid(); // or Unauthorized
  ```

  in your controller, to enforce that scope.

- **Use [RequiredScope] attribute:** Microsoft.Identity.Web provides an attribute `RequiredScope` that you can put on controllers or actions to declaratively ensure a scope is present ([Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles#:~:text=You%20can%20verify%20the%20scopes,a%20key%20to%20the%20configuration)) ([Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles#:~:text=,access_as_user)). For example:

  ```csharp
  [Authorize]
  [RequiredScope("API.Read")]
  [HttpGet]
  public IEnumerable<WeatherForecast> Get() { ... }
  ```

  This will automatically check that the token’s scopes include "API.Read". If not, it will result in 403 Forbidden.

  `RequiredScope` can also accept multiple scopes (if any one of them suffices). And it can be configured via config (as shown in docs where it can pull from config setting if you want to avoid hardcoding) ([Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles#:~:text=For%20instance%20if%2C%20in%20appsettings,you%20have%20the%20following%20configuration)) ([Verify scopes and app roles protected web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-protected-web-api-verification-scope-app-roles#:~:text=using%20Microsoft)).

- **Policy-based Authorization:** You can define an authorization policy in `Startup/Program` like:
  ```csharp
  services.AddAuthorization(options =>
  {
      options.AddPolicy("RequireApiReadScope", policy =>
          policy.RequireClaim("http://schemas.microsoft.com/identity/claims/scope", "API.Read"));
  });
  ```
  Then use `[Authorize(Policy = "RequireApiReadScope")]` on the controller. This does effectively the same as RequiredScope attribute above.

Any of these methods are fine. `RequiredScope` is convenient since it's built-in and specifically meant for this scenario, coming from Microsoft.Identity.Web.Resource namespace.

For demonstration, if using `RequiredScope` from Microsoft.Identity.Web, ensure to import it:

```csharp
using Microsoft.Identity.Web.Resource;
```

It will only work if you have the authentication configured as per Microsoft.Identity.Web (which we do).

**App Roles / Application Permission validation:** If we had application permissions (daemon apps calling), we might also check `HttpContext.User.HasClaim("roles", "SomeAppRole")` or use `[RequiredScopeOrAppPermission]` attribute which Microsoft.Identity.Web offers to handle either scopes or app permissions in one go ([[Question] RequiredScope doesn't work (for web APIs called by ...](https://github.com/AzureAD/microsoft-identity-web/issues/1571#:~:text=these%2C%20you%20should%20be%20good)) ([RequiredScopeOrAppPermissio...](https://learn.microsoft.com/en-us/dotnet/api/microsoft.identity.web.resource.requiredscopeorapppermissionattribute?view=msal-model-dotnet-latest#:~:text=RequiredScopeOrAppPermissio,required%20by%20a%20web%20API)). For example, if an app calls your API using client credentials, the token will have a `roles` claim (with the app role name you defined) instead of `scp`. The API can check that. In our scenario, we are not doing that, but good to be aware for advanced cases.

**User Roles vs App Roles:** Azure AD can also put user’s directory roles or group claims in tokens, but by default it doesn’t unless requested (and requires additional config like group membership claims in the app registration). That’s not needed for our typical scenario of custom scopes. If you needed to only allow certain AAD groups or directory roles, that’s another layer (you’d parse `groups` claim or use Graph API to check user membership – out of scope for this guide).

For completeness, some choose to implement authorization at the API level by reading the `scp` in each call, but that can be repetitive. The attribute/policy approach is cleaner.

**Testing the API security:**

- Call the API without a token: should get 401. (Perhaps using curl or browser with no auth).
- Call with an invalid or expired token: 401 (or 403 if signature invalid, but generally treat as 401).
- Call with a valid token but missing the required scope: If you used only [Authorize], it would still allow if token is valid at all. But if we implemented [RequiredScope("API.Read")] and the token did not have API.Read, the attribute would fail and return 403 Forbidden. In our setup, the only way a token from Azure AD would lack the scope is if our client requested a different scope or none. Since our client specifically asks for API.Read, we should be fine.
- Call with a proper token (with API.Read): returns the data (200 OK).

The difference between 401 and 403: 401 is “unauthenticated” (no valid token); 403 is “authenticated but not authorized (doesn’t have needed permission)”. Our implementation should reflect that – [RequiredScope] tends to throw 403 when scope missing because the request _is_ authenticated, just not allowed for that scope.

### 10. Securing APIs with Azure AD

We already discussed much of API security, but let’s summarize best practices and additional considerations to ensure the API is secured:

#### 10.1 Token Validation and Middleware

By using the ASP.NET Core JWT bearer authentication middleware, we ensure:

- Tokens are validated automatically on each request.
- We don't have to manually call Azure AD to check tokens; the token is a self-contained JWT with signatures.
- The middleware will use Azure AD’s **OpenID Connect discovery document** (from `https://login.microsoftonline.com/<tenant>/.well-known/openid-configuration`) to get the signing keys and valid issuers. This happens at startup and cached, with periodic refresh. You don't have to supply the keys – it's handled.

This is a robust and standard approach. Always prefer using framework middleware over manually parsing tokens unless necessary. It’s less error-prone.

#### 10.2 Scope-based Authorization

Ensure you do implement scope or permission checks in the API. Without it, if a client somehow got a token (even for minimal scopes), they could call any endpoint that just had [Authorize]. This may be fine if your API only has one logical permission anyway. But often, you might have read vs write scopes. For example, maybe define `API.Read` and `API.Write`. You'd then require [RequiredScope("API.Write")] on POST/PUT actions, whereas GET actions might accept just API.Read.

We covered using [RequiredScope] attribute for ease. That essentially does:

```csharp
if (!context.User.Claims.Any(c => c.Type=="scp" && c.Value.Split(' ').Contains(requiredScope)))
 { context.Fail(); }
```

under the hood (conceptually).

For multiple required scopes (like the client needs to have both X and Y), you might enforce that in code or just design single scope that covers multiple actions.

**Least Privilege:** Design your scopes such that they give the minimum necessary access. E.g., a “read” scope that doesn't allow writing data. Only ask for what you need in the client. Users (and admins) will see the list of scopes when consenting – too many or too broad (like a wildcard) and they might hesitate. Granularity is good, but not too granular that it's unmanageable.

#### 10.3 CORS and Cross-Origin Considerations

We mentioned enabling CORS on the API. To reiterate:

- Because our React app runs on a different origin than the API, the browser will enforce same-origin policy. The API must send appropriate CORS headers to allow the cross-origin call.
- Using `.WithOrigins("http://localhost:3000")` in development is fine. In production, you'd allow your actual domain (and maybe not allow localhost).
- Consider using HTTPS in development for both front and back to avoid any issues (modern browsers might block tokens in localStorage or some cookies in http, but with pure fetch Bearer it's okay. Still, run API on HTTPS as shown).
- If you see CORS errors, ensure the `app.UseCors` is called before `UseAuthentication`/`UseAuthorization` or at least before the app endpoints. Order matters in ASP.NET pipeline.

Another note: CORS preflight (OPTIONS requests) – by default, our policy allowed any method, so preflight will succeed. We allowed credentials in policy, but actually in this scenario, we are not using cookies, so credentials are not needed; the Authorization header is not a credential per se for CORS, it's a header. We should allow that header (AllowAnyHeader does it). So it's fine.

#### Additional API Security (outside of Azure AD):

- **Throttling:** Consider rate limiting your API or requiring proper client-ids to avoid abuse. Azure AD tokens help ensure only authorized users call, but they don’t prevent DoS attacks with valid tokens or repeated calls.
- **Logging:** Use ASP.NET Core logging or Azure Application Insights to log authentication/authorization info. For example, log the `sub` or `oid` of callers, what endpoints, etc. Azure AD also logs sign-in attempts and token issues in Azure AD logs – use those for audit.
- **Validation:** If the API is extremely sensitive, you might add additional checks like ensure certain claims (maybe an 'appid' claim for the client id to ensure only your known client calls it – though if you trust the token, that should be fine. In AAD v2, the access token has an `azp` (authorized party) claim which is the client ID of the app that requested the token. If you want to be sure only your React app (with specific client id) can call, you could check `azp` or the `appid` claim. However, in delegated tokens, `azp` should be your client’s ID anyway. If someone somehow got a token for your API from another app, that would normally require that other app be authorized for your API in AAD (which you control). So not a common scenario, unless multi-tenant and another client somehow had the same user and permission, but still, you might want to trust any legitimate token.)

- **Use of API Gateways or APIM:** In some enterprise setups, the API might be behind Azure API Management or other gateways that do an extra JWT check (like APIM has a `validate-jwt` policy). That is optional since our API itself checks JWT. But in a defense-in-depth approach, APIM can also check the token and even enforce scopes at that level.

So far, we have a working secure system.

---

## 11. Troubleshooting Common Issues

Even with the correct setup, developers often run into some common issues when integrating Azure AD. Here are several and how to troubleshoot them:

### 11.1 Authentication Failures and Error Codes

- **Invalid_client or Unauthorized_client errors:** This can happen if the client app is not configured correctly. For instance, if you get `AADSTS650053: The application is configured for use by Microsoft Account users only. Please use the /consumers endpoint to serve this request.` or similar, it suggests a mismatch in who can log in. Check your **Supported account types** in app registration and the authority you’re using. E.g., if app is multi-tenant including personal accounts but you use common endpoint, etc. Ensure they align (for multi-tenant, `common` or `organizations` is fine; for single-tenant, use your tenant explicitly).
- **AADSTS50011: Redirect URI mismatch:** This error means the redirect URI in the request (like what MSAL sent, perhaps taken from your config) does not exactly match any of the redirect URIs in the app registration ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=A%20redirect%20URI%20is%20the,sends%20security%20tokens%20after%20authentication)). Check for typos, missing ports, HTTP vs HTTPS, trailing slashes. The error will usually show you the problematic redirect URI. Add it to Azure AD, or fix the one in the app.
- **AADSTS70001: Application with identifier X was not found in directory Y:** This often means the **Client ID** or **authority/tenant** is wrong. Maybe you used the wrong GUID or you are pointing to the wrong tenant. Verify the GUID in your code matches the Azure portal’s app's client id. If multi-tenant, ensure you used the correct domain in authority. If single-tenant but you accidentally used common in MSAL, Azure AD might try to find the app in a different context. Using the proper tenant ID in authority fixes it.
- **Tokens not being returned (no id_token or no access_token):** If you call MSAL with certain scopes and Azure AD returns an error or does not include a token:
  - If missing ID token, ensure **ID tokens** are enabled for the client (in Azure AD > Authentication, for Web platform, there's a checkbox "ID tokens"). For SPA, MSAL by default does code flow which always gives an ID token if `openid` scope is present. If something like `openid` was not requested, you might not get ID token (though MSAL usually does request it).
  - If missing access token for your API scope, ensure the scope string is correct and that **the client has permission** to that scope. If not, Azure AD might ignore the scope or return an error AADSTS65001 (saying not granted). The fix is to add the API permission and consent. If scope string is wrong (e.g., using the wrong API identifier or spelling), Azure AD might also ignore it.
- **Consent prompt appearing unexpectedly:** If you’re in your own tenant and you already granted consent, you shouldn’t see a prompt every time. If you do, it could be:
  - You’re requesting incrementally more scopes that weren’t consented yet. Azure AD will prompt when new permissions are requested.
  - Your token cache is being cleared or you always do login instead of using existing session.
  - In multi-tenant, a user from another tenant will see a prompt the first time (or if new permissions added later).
  - If using an incognito/private window, there's no session, so you may see the login and consent again.
- **“Need admin approval” error (AADSTS90094):** This means the user tried to consent to a permission that only an admin can consent to, or user consent is disabled. The message usually says _"User needs admin approval"_ and gives a URL an admin can visit to consent. To resolve:
  - As an admin of the tenant, either use that URL or go to Azure AD portal > Enterprise Applications > find your app > Permissions > Grant admin consent.
  - If you are the developer and it's your tenant, just grant consent in the app registration as described in 6.3.
  - If you expect to allow users to sign up from other orgs, you might need to provide a mechanism for their admin to pre-consent (like an admin onboarding flow).
- **Issuer validation errors in API:** If your API throws an error like _"IDX10205: Issuer validation failed. Issuer is <some GUID tenant>... "_ it means the token's issuer wasn't expected by the API. This can happen if someone from another tenant calls your API and your API config is single-tenant (only trusting your issuer). If your app is truly multi-tenant and you want to allow that, you need to configure the JWT options to allow multiple issuers. Microsoft.Identity.Web can toggle a flag to accept any issuer of an Azure AD (still verifying signature). See `MicrosoftIdentityOptions.AllowMultipleInstances` or using `ValidateIssuer = false` (with caution). Alternatively, enforce that only tokens from your tenant are accepted (which effectively makes your API single-tenant even if client is multi-tenant).

### 11.2 Consent and Token Issues

- If your client is not getting a token for the API (accessToken is null or error):
  - Double-check the scope name and API identifier in the code. It must match exactly what’s in Azure AD. For example, if your App ID URI is `api://abc-123-.../API.Read`, use that full string. If you named a custom URI like `api://myapi`, then scope is `api://myapi/API.Read`.
  - Ensure you used `.default` incorrectly or not. Sometimes MSAL uses `.default` scope to get all delegated perms that user has consented to. But if you explicitly want one scope, use that.
  - Check that the user actually consented. You can look in Azure AD > Enterprise Applications > [Your API] > Users and Groups > see if the user or "All Users" have the delegated permission. If not, no token will be issued for that scope until consent is given.
- If the token’s `scp` does not include what you expect:
  - Possibly the client asked for less/different scopes. Or the user is from a tenant where an admin limited the scopes. But usually Azure AD either gives or refuses, it doesn’t modify scopes silently (except if you request Graph scopes and some get dropped due to not granted).
  - In our scenario, if we requested only `API.Read` and we see the token's scp is exactly "API.Read", that's correct. If we saw nothing or "user_impersonation", note: In older Azure AD (especially v1 endpoint or default, a single scope often named user_impersonation is used by default for custom APIs if you used the default "Azure Resource Access" in v1. But we explicitly created a scope name, so it should appear).
- Another issue: **Access token has issuer sts.windows.net (v1)**. This could occur if the scope used was actually from an Azure AD v1 resource or if accessTokenAcceptedVersion in manifest for API was set to null or 1. If you accidentally used the v1 endpoint. The sign-in audience and endpoints might cause Azure to issue a v1 token. The user from Q&A had this issue because maybe they misconfigured the SPA as not using spa redirect, etc., which defaulted to an older flow. To fix, ensure `accessTokenAcceptedVersion` is 2 in the API’s manifest (or set in Expose an API blade if available), and always use /v2.0 endpoints (MSAL does by default). This ensures v2 tokens (with login.microsoftonline.com common as issuer) ([Implementing Azure AD Authentication - React App calling Web API through Azure API management (and with validate-jwt policy) - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/314819/implementing-azure-ad-authentication-react-app-cal#:~:text=But%20when%20I%20check%20in,0)).

### 11.3 CORS Errors in SPAs

- If the browser console shows an error like _“No 'Access-Control-Allow-Origin' header is present on the requested resource”_ when calling the token endpoint or your own API:
  - If it's token endpoint (login.microsoftonline.com), you likely missed marking the redirect URI as SPA in Azure AD, as mentioned earlier. Fix by updating redirect URI type ([Microsoft identity platform and OAuth 2.0 authorization code flow - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#:~:text=,the%20Microsoft%20Entra%20admin%20center)).
  - If it's your API, then you need to configure CORS properly. Make sure the API’s CORS policy matches exactly the origin (check that no trailing slash issues, http vs https, etc.). Also ensure the OPTIONS preflight is handled (if using attribute routing and .NET, by default it is). If not, you might need to allow OPTIONS method or use `[HttpOptions]` on controllers. The simplest is the AddCors policy like we did with .AllowAnyMethod which covers OPTIONS.
- If after deploying to production, say your domain is https://app.contoso.com for React and https://api.contoso.com for API, ensure to update the CORS allowed origins and the redirect URIs in Azure AD accordingly.

### 11.4 Misconfigured Redirect URIs

This is such a common issue it's worth double emphasis. Always ensure the **redirectUri in your MSAL config exactly matches one of the redirect URIs in Azure AD**. For example, if your app runs on `https://app.contoso.com` and you configured Azure AD with that, but your MSAL config has `https://app.contoso.com/` (with a trailing slash) or a different subdomain (www vs non-www), you'll get AADSTS50011 errors as mentioned. The fix is straightforward: align them. You can have multiple redirect URIs in Azure AD if needed (for dev vs prod, etc.), and then in code decide which one to use depending on environment.

**Tip:** During development, sometimes MSAL’s redirect might cause a blank page on return. This could be because your app isn't handling the redirect properly (maybe forgot to call `handleRedirectPromise`). Using the `MsalProvider` as shown should automatically handle it for you. Without it, one might need to call `msalInstance.handleRedirectPromise().then(...)` to process the response. The `MsalProvider` does that internally.

### Additional Troubleshooting Tools:

- Use **Browser Network traces**: See the requests to login.microsoftonline.com, check status codes. If the `/authorize` call returns an error, you'll see it in the query parameters on redirect to your redirect URI (like error=...). If the `/token` call returns error, MSAL usually catches and surfaces it in console or error object.
- Use **JWT viewers** (like jwt.ms or jwt.io) to inspect the tokens you receive. This can confirm if claims like `scp` and `aud` are what you expect.
- Azure AD **Sign-in logs** (in Azure AD portal under Monitoring) can show if a token issuance failed or succeeded for a user, with details and error codes.
- **Fiddler or Postman**: To test the API separately, grab an access token (maybe from MSAL or Azure AD's Graph Explorer or Postman OAuth2) and call the API with it. This helps isolate whether the issue is with the API or the client getting the token.

---

## 12. Lifecycle Management and Best Practices

Now that our system works, we need to plan for maintenance and security in the long run. Azure AD application integration is not a “set and forget” task; you must manage app credentials, monitor security, and update configurations as things evolve.

### 12.1 Client Secret Expiration and Rotation

If you used **client secrets**, remember they have an expiration (up to 24 months, often less as recommended) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=4,after%20you%20leave%20this%20page)). Azure AD will not automatically switch to a new secret; you must create a new one and update your apps to use it. If a secret expires and your app still uses it, authentication (for flows needing client auth) will fail, likely causing downtime.

**Best practice:** **Rotate secrets proactively before they expire** ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=)). For example, set a reminder 1 month before expiration to generate a new secret. Azure AD allows multiple active secrets, so you can have overlap:

1. **Generate a new secret** in Azure AD a few weeks before the old one expires ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=)). Add it to your app’s configuration (in addition to or replacing the old one, depending if your app can hold two).
2. **Deploy the updated configuration** to your application with the new secret. Ensure the app can authenticate with the new secret (test in a staging environment if possible) ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=,New%20Credentials)).
3. Once the new secret is confirmed working, you can **remove the old secret** from Azure AD (optional but recommended once it expires or immediately after switch) ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=)). Removing old credentials reduces risk of leaked credentials being used ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=)).
4. Always have at least one valid secret. If you remove the only secret accidentally, the app can’t auth until a new one is added.

To avoid human error, consider **automating secret rotation**. Azure AD doesn’t natively auto-rotate app secrets, but you can use Azure Key Vault and scripts:

- Use **Azure Key Vault** to store the secret, and perhaps an Azure Function or script that periodically generates a new client secret via Azure AD Graph/PowerShell, updates Key Vault, and informs the app (if the app reads from Key Vault or environment).
- Microsoft has guidance and samples on automating secret rotation ([Recommendations for protecting application secrets - Learn Microsoft](https://learn.microsoft.com/en-us/azure/well-architected/security/application-secrets#:~:text=Recommendations%20for%20protecting%20application%20secrets,management%20store%20that%20natively)).

Even better, switch to **certificate** auth to avoid short expirations. Certificates can be longer lived (though you should still rotate them too, see next).

### 12.2 Certificate Renewal and Rotation

If using **certificates** for app credentials, they typically have an expiry date as well (maybe 1 or 2 years if self-signed, or whatever your CA issues). Plan to renew before expiration:

- You can upload the new certificate’s public key to Azure AD _before_ the old one expires. Azure AD allows multiple certs, and will accept any that are valid. So overlap is key to zero downtime.
- If using Azure Key Vault with certificate auto-rotation (Key Vault can auto-renew certificates it manages), you can integrate that with Azure AD. However, Azure AD won’t fetch from Key Vault automatically; you’d still need a script to update the app registration with the new certificate. Azure AD’s Microsoft Graph API allows adding certificates, so you can script an auto-update when Key Vault rotates a cert ([How to Automatically Rotate Azure AD Application Certificates - Keytos](https://www.keytos.io/blog/pki/how-to-automatically-rotate-azure-ad-application-certificates.html#:~:text=How%20to%20Automatically%20Rotate%20Azure,new%20EZCA%20certificate%20is)).
- After adding the new cert, update your application to use the new certificate (private key). If your app loads a cert by thumbprint, you might load by new thumbprint or load all and let it pick valid one.
- Remove the old certificate from Azure AD once all apps no longer use it ([Procedure and the consequence when Rotating the keyCredentials in Azure Active Directory? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1427391/procedure-and-the-consequence-when-rotating-the-ke#:~:text=)).

**Key Vault integration:** Storing certificates (and secrets) in Azure Key Vault is highly recommended ([Recommendations for protecting application secrets - Microsoft Azure Well-Architected Framework | Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/security/application-secrets#:~:text=)). Key Vault can generate logs, handle storage securely, and manage access. Your app can pull the credential at startup. This way, updating the credential might not even require app code change if the app always looks up by a tag or version in Key Vault.

**Notifications:** Unfortunately, Azure AD doesn’t currently send proactive emails about app secret/cert expiry (as of now) ([Automation of Email Notification for Certificate Rotation?](https://learn.microsoft.com/en-us/answers/questions/384694/automation-of-email-notification-for-certificate-r#:~:text=Rotation%3F%20learn,possible%20as%20of%20right%20now)). You have to track it. Some third-party solutions or scripts can alert you. Keep an inventory of app credentials and their expiry.

### 12.3 Monitoring and Auditing

Monitor your Azure AD apps and sign-ins:

- Azure AD **Sign-in logs** will show who logged in to your app, when, and if any risky sign-ins occurred.
- **Audit logs** will show changes to app registrations (like who added a secret, who changed a setting).
- If suspicious behavior is noticed (like an app was granted more permissions by someone unexpectedly, or lots of failed logins), investigate and take action (maybe revoke credentials, etc.).

**Conditional Access:** For enhanced security, consider using Azure AD Conditional Access policies for your app. For example, require MFA for logins to the app, or limit access by IP/location. This can be done at the directory level (if you have Azure AD Premium). It adds another layer that doesn’t require app code changes.

**Principle of Least Privilege:** Only grant your app the minimum permissions it needs. We did this by creating specific scopes. Also, in the Azure AD registration, under "API permissions", remove default permissions that you don't need. Often a new registration might include the default "User.Read" for Microsoft Graph. If your app doesn’t use Graph, remove it, so that you’re not accidentally asking for it (and so consent prompts are cleaner).

**Regular Reviews:** Periodically (say every 6 or 12 months), review the app registration settings:

- Are there any outdated redirect URIs or credentials? Remove them.
- Check enterprise applications (service principals) – if multi-tenant, you might see many service principals in other tenants (you won't see them in your portal easily, but you can query via Graph).
- Ensure documentation of the setup is up-to-date so new team members can understand the configuration.

### 12.4 Security Best Practices

To summarize some best practices (many we’ve mentioned along the way):

- **Use HTTPS everywhere:** Ensure redirect URIs in production are HTTPS. Ensure tokens are only sent over HTTPS. This prevents token interception.
- **Do not expose secrets:** Never put client secrets in front-end code or in publicly accessible areas. For backend, store in environment variables or vaults, not in plain text in repo. If using a CI/CD, use secret variables.
- **Prefer Certificates or Managed Identity:** If your application is on Azure (like an Azure function or web app) and needs to call other Azure resources, consider using a **Managed Identity** instead of app client secrets. Managed Identity is a feature of Azure resources that automatically handles auth with Azure AD without you needing to maintain secrets. This might not apply for user login flows, but for backend-to-backend, it’s great.
- **Limit User Consent** (for enterprise scenarios): If you publish a multi-tenant app, malicious clients might try to trick users into consenting to rogue apps with the same name. Educate users or ideally use Verified Publisher for your app or Admin consent workflows.
- **Key Rotation**: As emphasized, rotate keys regularly and automate it if possible. It’s mentioned often because leaked credentials are a common breach vector.
- **Logging in the API**: Log token details in debug (avoid logging entire tokens in prod logs, but you can log claims like user ID, scope, etc.). This helps trace who did what.
- **Error Handling:** Handle errors gracefully on the frontend. If token acquisition fails, inform the user or redirect them to login again. On the API, if unauthorized, return a proper 401/403 with maybe a JSON error. Though not leaking info is also important; you might just return 401/403 without detail to avoid giving attackers clues.
- **Testing**: Test the scenario where a token is expired (simulate by changing system clock or using a short-lived token) to ensure your app can refresh properly. Test in different browsers and incognito to ensure no hidden dependency on existing session.
- **Documentation**: Document the Azure AD app setup within your project docs so future maintainers know the App ID, what secrets to update, etc., and the process to recreate if needed.

### 12.5 Lifecycle of an Azure AD App

It’s good to consider the **entire lifecycle** of your Azure AD app:

- **Creation**: We did this (portal or could be scripted). Use proper naming conventions (prefix with something, etc.) to identify in the tenant.
- **Development**: Use separate app registrations for dev/test vs production if needed. That way, you can have different redirect URIs, and if someone accidentally gets a prod secret they can’t use it on dev, etc. Azure AD tenants themselves could be separate for dev/prod, but often one tenant is fine with multiple apps.
- **Deployment**: Ensure when deploying your app, the necessary config (client IDs, etc.) are set correctly for that environment.
- **Maintenance**: As covered – rotating credentials, updating redirect URIs if your app URL changes (don’t forget that!), adding/removing permissions as features change.
- **Decommission**: If the app is no longer needed, remove its registration and credentials from Azure AD to reduce clutter and potential attack surface. Also remove any enterprise app entries in other tenants if applicable.

---

## 13. Conclusion

In this extensive guide, we covered the end-to-end process of integrating an application with Azure Active Directory for authentication and authorization. From registering applications (single-tenant for internal apps or multi-tenant for SaaS), to configuring redirect URIs and exposing API scopes, to implementing the OAuth 2.0 authorization code flow with PKCE in a React front-end, and protecting a .NET Core Web API with Azure AD JWT validation – all steps were detailed. We also addressed common troubleshooting scenarios and emphasized best practices such as principle of least privilege, secure credential management (favoring certificates and frequent rotation), and monitoring your integration for any issues.

By following a step-by-step approach:

- You set up the Azure AD **App Registrations** correctly (ensuring the Azure AD trust is established and configured).
- You implemented the client-side logic to **sign in users and acquire tokens** using MSAL (handling the OIDC/OAuth flow under the hood).
- You secured the server-side by **validating tokens and enforcing scopes/roles** in the Web API.
- You learned how to handle issues and maintain the solution securely over time.

Azure AD (Microsoft Entra ID) provides a robust platform for identity – leveraging it means you don’t have to manage user credentials in your app, and you instantly integrate with a broad ecosystem (including possibilities to extend to Microsoft Graph or other services with the obtained tokens).

As a final note, always keep your knowledge up to date with Azure AD’s evolving features. For example, new standards like **OAuth 2.1** or improvements in MSAL libraries may change some recommended practices. Microsoft’s documentation and community resources are very valuable (and we cited many along the way for reference). By adhering to the best practices and steps outlined in this guide, you can confidently implement enterprise-grade authentication and authorization in your applications with Azure AD.
