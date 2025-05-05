# Advanced Azure AD Application Integration Guide (React SPA & Spring Boot API)

**Introduction**  
This comprehensive guide walks through the end-to-end process of setting up Azure Active Directory (Azure AD) for a React single-page application (SPA) and a Spring Boot REST API. It is written for advanced developers and covers everything from app registration in Azure AD to implementing OAuth2/OIDC authentication in code. We will create an Azure AD application, configure redirect and web URIs, expose API scopes, generate secrets, and then use the tenant and client IDs in both a React front-end and Spring Boot back-end. Along the way, we’ll discuss OAuth2/OpenID Connect flows, security best practices, and production deployment considerations. The guide is structured with clear sections and step-by-step instructions, including code snippets, so you can follow along and integrate Azure AD authentication seamlessly.

## 1. Creating an Azure AD Application (App Registration)

**Step 1 – Access Azure AD:** Log in to the Azure Portal and navigate to **Azure Active Directory > App Registrations**. You will need appropriate permissions (e.g., Azure AD Application Administrator) to create a new app registration.

**Step 2 – Start New Registration:** Click **“New registration”**. On the registration form, enter a **Name** for your application (e.g., “MyAdvancedApp” for a combined app, or you can create separate registrations for front-end and back-end as discussed below).

**Step 3 – Choose Supported Account Types:** Select who can use the application (the _sign-in audience_). Azure AD offers several options ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=This%20type%20of%20app%20is,the%20widest%20set%20of%20customers)):

- **Single tenant (Accounts in this organizational directory only):** Only users in your Azure AD tenant can access (commonly used for line-of-business internal apps) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Accounts%20in%20this%20organizational%20directory,in%20your%20tenant)).
- **Multitenant (Accounts in any Azure AD directory):** Users in any organization’s Azure AD can consent to use the app (typical for SaaS applications) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Accounts%20in%20any%20organizational%20directory,to%20provide%20to%20multiple%20organizations)).
- **Multitenant + Personal Microsoft Accounts:** Allows any Azure AD user _and_ personal Microsoft accounts (Live/Xbox/Outlook) to use the app ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=This%20type%20of%20app%20is,the%20widest%20set%20of%20customers)).
- **Personal Microsoft accounts only:** Rarely used for enterprise scenarios.

Choose the option that fits your scenario. For example, if this application is only for your company, choose single-tenant; if it’s a SaaS app for multiple organizations, choose multitenant.

**Step 4 – Redirect URI (optional at this stage):** For now, you can leave **Redirect URI** blank (we will configure redirect URIs in detail later) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=6,URI%20in%20the%20next%20section)). If you are only registering the API (which doesn’t require an interactive login), you don’t need to specify a redirect URI at all ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=3,user%20is%20logged%20in%20interactively)). If you are registering a client app (like the React SPA) you will later add a redirect URI for it.

**Step 5 – Finish Registration:** Click **Register**. After a moment, the new app will be created. You’ll be taken to the app’s **Overview** page, which shows important identifiers:

- **Application (client) ID:** The unique GUID for your app registration ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=When%20registration%20finishes%2C%20the%20Microsoft,in%20the%20Microsoft%20identity%20platform)). This is the **Client ID** used by apps to identify this application in authentication flows.
- **Directory (tenant) ID:** The GUID for your Azure AD tenant (also found in Azure AD Overview). This is needed for tenant-specific configurations (like forming the authority URL) ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=Application%20,specifies)).

Make note of these IDs. _(Tip: You can always return to this Overview page to copy them. The client ID and tenant ID will be used in your React and Spring Boot configurations.)_ Azure also creates a **Service Principal** for this app (under **Enterprise Applications**), but that’s managed automatically.

**Using Separate Registrations for SPA and API:** In many architectures, you will create **two** app registrations – one for the front-end client (React SPA) and one for the back-end API (Spring Boot). This separation is recommended for security and clarity. The client app will represent the user-facing application that requests tokens, and the API app will represent the resource (your API) that accepts tokens. Azure AD allows one app registration to have both client and API settings, but separating them offers better control (e.g. you don’t need to expose the API’s secret to the front-end). In this guide, we assume two registrations:

- **“MyAdvancedApp-SPA”** (client app): Configured as a public client (no secret), with SPA redirect URI.
- **“MyAdvancedApp-API”** (API app): Configured to expose scopes, possibly with a client secret or certificate if needed for server-to-server calls.

Azure AD supports linking these two apps via permissions. In fact, Microsoft’s guidance is to register both a client and a web API and then grant the client access to the API’s scopes ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=To%20grant%20a%20client%20application,to%20have%20two%20app%20registrations)). We’ll cover exposing scopes and granting access in a later section.

**Assigning Ownership (optional):** After creating the app, you can assign additional **Owners** under the app’s **Owners** blade. Owners are users who can manage the app registration. For production apps, ensure at least two owners (for resiliency) and keep this list updated ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Assign%20application%20owner)).

**(Optional) Branding & Properties:** Under **Branding & Properties**, you can set a logo, home page URL, and other info. Providing a meaningful name and logo is recommended, especially if users will see consent screens or the app in their app launcher ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Branding)). Also add a terms of service and privacy statement URL for compliance ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Privacy)).

**Result:** You have now registered an Azure AD application. You should have the **Client ID** (Application ID) and **Tenant ID** on hand. Next, we’ll configure redirect URIs and any necessary URLs for authentication.

## 2. Configuring Redirect URIs and Web URIs

After app registration, the next critical step is configuring **redirect URIs** (also known as reply URLs). A redirect URI is the location Azure AD will send authentication responses (tokens or authorization codes) to after user sign-in ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=A%20redirect%20URI%2C%20or%20reply,specified%20in%20the%20login%20request)). It’s a cornerstone of OAuth2/OIDC security – Azure AD will only redirect to URLs you have explicitly registered to prevent token leakage to malicious sites ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=For%20security%20reasons%2C%20the%20authentication,URLs%20configured%20for%20the%20application)).

**Platform Configuration:** In Azure AD, redirect URIs are configured per application **Platform**. Go to your app’s **Authentication** blade. Click **“Add a platform”** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=1,App%20registrations%2C%20select%20your%20application)). You’ll see options like **Web**, **Single-page application (SPA)**, **Mobile/Desktop**, etc. Choose the appropriate platform for your client or server:

- For a **React SPA** (running purely in a browser with no back-end code for auth), choose **Single-page application**.
- For a traditional **Web** app (such as a server-rendered Spring Boot MVC app), choose **Web**.
- For our **Spring Boot API** (which is not a public client and doesn’t sign users in via browser), we typically do _not_ need to add a redirect URI at all (since it won’t handle interactive logins) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=3,user%20is%20logged%20in%20interactively)). The API will receive tokens from the SPA via authorization headers.

**Adding a Redirect URI for React SPA:** When you select **Single-page application**, you can input the URI. For development, this is often a localhost address. For example, if your React dev server runs at `http://localhost:3000`, you might use `http://localhost:3000` or a specific route like `http://localhost:3000/auth-callback`. Enter the URI and click **Configure**. If you have multiple environments (dev, staging, prod), you can add multiple redirect URIs. Common practice is to include:

- The local development redirect (e.g., `http://localhost:3000` or `http://localhost:3000/login/oauth2`).
- The production redirect (e.g., `https://myapp.contoso.com/auth-callback`).

**Adding a Redirect URI for Web (if needed):** If your Spring Boot app was handling user login (e.g., using Spring Security OAuth client), you’d add a **Web** platform and specify the redirect URI (e.g., `https://myserver.com/login/oauth2/code/azure` if using Spring Security’s default OAuth2 login endpoint). In our scenario (React as front-end), the Spring Boot API is not handling interactive logins, so you likely won’t configure a Web redirect for the API app registration. (The API will instead be secured by tokens issued to the SPA.)

**Redirect URI Restrictions:** Azure AD enforces some rules on redirect URIs ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=,for%20some%20localhost%20redirect%20URIs)) ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=,%29%20%2C)):

- URIs **must be HTTPS** for web and SPA apps in production (HTTP is allowed only for `localhost` during development) ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=,for%20some%20localhost%20redirect%20URIs)).
- Wildcard URI patterns are _not_ allowed (except in some specific multi-tenant cases for certain Microsoft applications) – you must specify the exact domain and path. Avoid using wildcards like `*.myapp.com` ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=,web%20agent%2C%20you%20may%20use)).
- The redirect URI is case-sensitive and must match exactly what the application will request ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=%2A%20Redirect%20URIs%20are%20case,path%20of%20your%20running%20application)).
- You can configure **at most 256 redirect URIs** for single-tenant or multi-tenant apps (100 if personal Microsoft accounts are allowed) ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=Accounts%20being%20signed%20in%20Maximum,manifest%20is%20set%20to%20AzureADandPersonalMicrosoftAccount)), so manage them wisely. Remove any URIs you no longer need to reduce attack surface ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=,URIs%20on%20a%20regular%20basis)).
- **No fragment (`#`)** or certain special characters are allowed in the URI. Query parameters in redirect URIs are only permitted for single-tenant or multi-tenant _work/school_ account apps, not if personal Microsoft accounts are allowed ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=Query%20parameters%20are%20allowed%20in,with%20work%20or%20school%20accounts)).
- For SPAs, Azure AD uses the OAuth2 Authorization Code Flow with PKCE (Proof Key for Code Exchange) by default (implicit flow is disabled by default for new SPA registrations due to security). Ensure **“Implicit grant”** settings for access tokens or ID tokens are unchecked unless you specifically need them (most modern apps should use the code flow).

After adding the redirect URI, Azure will display it under the platform settings. If you selected **SPA**, Azure AD automatically marks your app as a public client (no client secret required) and enables the OAuth2 code flow + PKCE for that redirect. If you selected **Web**, you have additional options such as enabling the **ID token** and **access token** implicit flows (historically used for hybrid SPA apps) – leave those off unless needed.

**Web URIs vs Redirect URIs:** In Azure AD’s Authentication settings, you might also encounter fields like **Logout URL** (for Web platform) or the older **Home page URL** in Branding. A **Logout Redirect URI** (front-channel logout URL) is where Azure AD will redirect the user’s browser after a sign-out is initiated from Azure AD. If you want Azure AD to notify your app on logout, set this URL (for example, your app’s post-logout page). This is optional, but for completeness in a production app you might set `https://myapp.contoso.com/logout` as the logout URL in the Web platform settings.

**Multiple Redirect URIs and Environments:** You can and should register separate redirect URIs for each environment (dev, test, prod). _Never_ include development URIs in the production app registration that end-users use. It’s better to create separate app registrations for prod and dev, or at least remove dev URIs when deploying to prod ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=In%20a%20production%20web%20application%2C,registrations%20for%20development%20and%20production)). For example, you might have “MyApp-Dev” with `localhost` URIs and “MyApp-Prod” with the real domain URIs. This prevents accidental exposure of tokens to unintended endpoints.

**Summary:** At this point, the client app registration (React SPA) has a configured redirect URI. Azure AD will only send authentication responses (like authorization codes or tokens) to this URL after login ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=A%20redirect%20URI%2C%20or%20reply,specified%20in%20the%20login%20request)). If the user attempts login and the redirect doesn’t exactly match one on the list, Azure AD will throw an error (AADSTS50011) rejecting the request ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=For%20security%20reasons%2C%20the%20authentication,URLs%20configured%20for%20the%20application)).

For the API app registration, typically no redirect URI is needed (since it doesn’t directly handle logins). Now we proceed to configuring the API permissions (scopes) that the API will expose.

## 3. Exposing APIs and Setting Application Scopes

For a secure API, you need to define what permissions (scopes) client applications can request on it. In Azure AD, this is done in the **“Expose an API”** section of your app registration (for the API app). Here you will set the **Application ID URI** and define **scopes** that represent various permissions.

**Step 1 – Set the Application ID URI:** Navigate to your API app registration in Azure AD (e.g., “MyAdvancedApp-API”). Under **Expose an API**, the first thing to configure is the **Application ID URI**. This is a URI that uniquely identifies your API in the Azure AD ecosystem. By default, Azure AD suggests an ID URI in the form `api://<client-id>` (where `<client-id>` is the GUID of your app) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=1)). You can use this default or change it to a more user-friendly URI (like `api://myapp.company.com`), as long as it’s unique in your tenant or globally if multi-tenant.

- Click **“Set”** or **“Add”** next to Application ID URI if not already set. If using the default, just accept and save it ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=1)). If customizing, use a URI format you control (it doesn’t need to be an actual internet URL, but using a domain you own is a good practice). For example, `api://myadvancedapp-api` or `api://contoso.com/myapp`.

> _Note:_ The Application ID URI forms the prefix for scope names in tokens ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=2,Select%20Save)). If you leave it as `api://<GUID>`, your scope identifiers will be like `api://<GUID>/<ScopeName>`. If you set a custom URI, scopes will be `api://custom-uri/ScopeName`. Either is fine; some prefer custom URIs for clarity.

**Step 2 – Define Scopes:** After setting the App ID URI, click **“Add a scope”**. You’ll provide:

- **Scope name:** A short string to identify the permission (e.g., `API.Read`, `API.Write`, or a more descriptive name like `Employees.Read.All`). Scope names are often in the format _resource.operation_._level_ ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Field%20Description%20Example%20Scope%20name,only%20access%20to%20Employee%20records)). For example, for an employee records API: `Employees.Read.All` for full read access ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Field%20Description%20Example%20Scope%20name,only%20access%20to%20Employee%20records)).
- **Who can consent:** Choose whether **Admins and users** can consent to this scope, or **Admins only** ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Scope%20name%20The%20name%20of,only)). If a scope grants high-privilege access, you might require admin consent only. For user-facing basic scopes, allowing users to consent is convenient.
- **Admin consent display name & description:** End-user won’t see these if user can consent, but an Azure AD admin reviewing the scope during consent will see them. Provide a clear description (e.g., “Read access to employee records”) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Admin%20consent%20display%20name%20A,access%20to%20all%20Employee%20data)).
- **User consent display name & description:** If users can consent, provide a friendly description they will see on the consent screen ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=User%20consent%20display%20name%20A,access%20to%20your%20Employee%20data)). E.g., “Read your employee records.”
- **State:** Enabled or disabled. Leave it **Enabled** (enabled means the scope is active) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=by%20the%20scope,Enabled)).

For example, you might add a scope called **`API.Access`** with “Admin and users” consent, and descriptions like “Access the Advanced API”. Or more granular scopes: `Data.Read`, `Data.Write`, etc., depending on your needs.

Click **Add scope** to save it ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=State%20Whether%20the%20scope%20is,Select%20Add%20scope)). You can add multiple scopes if your API has different permission levels.

**Step 3 – (Optional) App Roles:** In addition to OAuth2 scopes, Azure AD app registrations allow **App Roles** (sometimes used for role-based access control). App roles can be assigned to users or client apps and appear in tokens’ `roles` claims. If your API will use roles (e.g., “Admin” vs “User” roles), you can define them under **App roles** in the API app registration ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Assign%20app%20role)) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Display%20name%20The%20name%20of,role%2C%20and%20then%20select%20Apply)). This is optional and slightly different from scopes:

- **Scopes** are typically used for delegated permissions (when a client app acts on behalf of a user).
- **App Roles** can be used for **application permissions** (client credentials flow) or to assign user roles for an app. In a delegated scenario, user roles can also be conveyed via groups or roles claim if configured.

For our purposes (React SPA calling API on behalf of user), defining scopes is usually sufficient. We won’t dive deep into app roles, but just know they exist for certain advanced scenarios (for example, if your API should allow background services to call it with an application identity, you’d create app role permissions that require admin consent).

**Step 4 – Expose scopes in API code (awareness):** The scopes you define in Azure AD are mainly enforced by Azure AD during token issuance (consent) and by your API when validating tokens. In your Spring Boot API, you will check the token’s scopes (or roles) to authorize access to various endpoints. For example, you might require the `API.Read` scope to access a GET endpoint. We’ll show how to enforce that in Spring Security later. Azure AD doesn’t automatically enforce scope usage in your API; it issues the scopes in the token, and it’s up to your API to check them. Azure documentation suggests designing scopes with proper granularity and checking them in the incoming token before performing the action ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20If%20you%27re%20securing,before%20making%20any%20authorization%20decisions)) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=platform%2C%20carefully%20think%20through%20the,before%20making%20any%20authorization%20decisions)).

**Step 5 – Pre-authorize a client application (optional):** A nice Azure AD feature is **Authorized client applications**. In the **Expose an API** section, after adding scopes, you’ll see an option to **“Add a client application”** and pre-authorize it for specific scopes ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=6,the%20opportunity%20to%20decline%20consent)). This means if you trust a particular client app (by Client ID), you can allow it to call your API without requiring the user to consent. This is useful in single-tenant scenarios to avoid the consent prompt for your own app.

For example, add the Client ID of your React SPA app and select the scopes (like `API.Access`) to authorize ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=users%20won%27t%20have%20the%20opportunity,to%20decline%20consent)). This will embed in the API’s manifest that “SPA app <id> is allowed these scopes.” Now, when a user signs in on that SPA, Azure AD will not ask for consent for those scopes (since it’s pre-approved). Use this only for first-party clients you control. In a multi-tenant scenario or for third-party clients, you cannot pre-authorize beyond your tenant.

**Granting API Permissions to the Client App:** Now that the API (resource) defines scopes, you need to grant the client application access to those scopes. This can be done in two ways:

- As mentioned, pre-authorize in the API registration (no user consent needed).
- **OR** (and especially in multi-tenant or when pre-auth isn’t used) – add an **API permission** in the client app registration.

For completeness, here’s how to configure the latter:

1. Go to the **Client app registration** (SPA) in Azure AD.
2. Under **API Permissions**, click **“Add a permission”**.
3. Choose **“My APIs”** (since the API is in the same tenant) ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=client%20application%20,API)). You should see your API (e.g., “MyAdvancedApp-API”) in the list. Select it.
4. Select the **delegated permissions (scopes)** you want to grant. You will see the scopes you created (e.g., `API.Access` or `Employees.Read.All`). Check the boxes for the needed ones and add the permission.
5. After adding, if your scope required admin consent (or if you’re in your own tenant as admin), click **“Grant admin consent for [Tenant]”** so that users won’t see a consent prompt. This will consent on behalf of all users in the tenant for those permissions.

At this point, your client app knows about the API’s scopes. It can request tokens for those scopes, and Azure AD will issue them if consent is granted. The relationship between the client and API registration is established: the client has permissions to call the API ([Web API app registration and API permissions - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis#:~:text=To%20grant%20a%20client%20application,to%20have%20two%20app%20registrations)). Think of the client app asking “Can I get a token to call X API with Y scope?”, and Azure AD will check if permission is granted.

**Visualization – Client & API permissions:**

- _API app_ (MyAdvancedApp-API) exposes scope “API.Access”.
- _Client app_ (MyAdvancedApp-SPA) has permission to “MyAdvancedApp-API/API.Access”.
- When a user signs in via the SPA, the SPA will request an access token for that scope. Azure AD sees the SPA is allowed that scope (via admin consent or pre-auth) and includes it in the access token’s `scp` claim.
- The access token’s audience (`aud`) will be your API’s App ID URI or client ID, and the `scp` will include “API.Access” indicating the granted permission. Your API must verify both audience and scope.

We will ensure in Spring Boot that the token’s audience matches our API and that the required scope is present before allowing the request.

## 4. Generating and Managing Client Secrets and Certificates

If an application needs to prove its identity (for example, a server-side application or a daemon service), you must create a credential for it. Azure AD supports two main credential types for app registrations:

- **Client Secrets** (a generated secret string a.k.a. application password).
- **Certificates** (public key credentials uploaded to Azure AD, where your app holds the private key).

For a **React SPA**, no secret is used (SPA is a public client). For a **Spring Boot API**, if it only needs to validate incoming tokens, it doesn’t strictly require a secret. However, if the Spring Boot app needs to call other Azure AD-protected APIs (like Microsoft Graph or another API) or if it needs to perform the OAuth **client credentials flow** (acting as its own identity), then it would need a client credential (secret or certificate). We will create a secret for completeness, assuming our Spring Boot application might need to identify itself to Azure AD (for example, to fetch tokens in a non-user context or to perform on-behalf-of flow).

**Creating a Client Secret:**

1. In your Azure AD app registration (usually the back-end API app if needed, or any confidential client), go to **Certificates & Secrets**.
2. Under **Client secrets**, click **“New client secret”**.
3. Provide a description (e.g., “Spring Boot API Secret – 2025”) for tracking.
4. Choose an expiration period. Azure AD allows at most 24 months for a secret ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=3,after%20you%20leave%20this%20page)). You can choose 6 months, 12 months, 18, 24, or a custom shorter period. It’s **recommended to use a short-lived secret** and rotate it regularly ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=,after%20you%20leave%20this%20page)). For production, consider using 6 or 12 months and have a rotation process.
5. Click **Add**. Azure will generate the secret value **one time** and display it. **Copy this value immediately** and store it somewhere secure (like a password manager or Key Vault). **You will not be able to see the secret value again once you leave this page** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=months,after%20you%20leave%20this%20page)). (If lost, you’d have to generate a new secret.)

The secret value is a long random string. This is essentially the “password” that your application (client) will use to authenticate with Azure AD in flows like OAuth2 authorization code (for web apps) or client credentials. The secret is associated with a **Client ID** – together they form the credentials for the app.

**Security Best Practices for Secrets:** Microsoft deems client secrets **less secure** than certificates ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Client%20secrets%20are%20considered%20less,that%20are%20running%20in%20production)). If possible, use a certificate for production systems ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=You%20can%20add%20certificates%2C%20client,CA%29%20where%20possible)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Sometimes%20called%20a%20public%20key%2C,platform%20application%20authentication%20certificate%20credentials)), because:

- Secrets are strings that could be checked into code by mistake or stolen from config.
- Certificates (private keys) can be safeguarded more robustly and often have hardware protection options.
- Azure AD certificates can be longer-lived or automatically renewed via enterprise processes.

However, secrets are easier to use during development. If you use a client secret:

- **Never embed the secret in client-side code** or expose it in a React app – treat it like a password (only use it on secure server side) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=password%20credentials%20%28client%20secrets%29,and%20regularly%20rotate%20your%20credentials)).
- Do not commit secrets to source control. Use environment variables or secure stores to supply them to your application runtime ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)).
- Consider storing secrets in **Azure Key Vault** and fetching at runtime, or use **Azure Managed Identities** so you might not need a secret at all ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=password%20credentials%20%28client%20secrets%29,and%20regularly%20rotate%20your%20credentials)).
- Plan to **rotate** the secret regularly. Azure AD will show the expiration date; you should add a new secret before the old one expires and update your app to prevent downtime.

**Using a Certificate Instead of Secret (Optional):** You can upload an X.509 certificate (public key) in Azure AD under **Certificates & Secrets > Certificates** ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=1,Select%20Add)). Your application would hold the private key. This is more secure because the private key can be in a key vault or HSM. Azure AD will accept the certificate’s thumbprint as a valid credential when your app presents a signed JWT (client assertion). Advanced setups often use certificates, especially for long-running services, because they eliminate storing a plain text secret and can be automated with Key Vault. Azure AD’s best practices explicitly state to favor certificates over secrets for confidential clients ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=You%20can%20add%20certificates%2C%20client,CA%29%20where%20possible)) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)).

**Multiple Secrets and Auto-Rotation:** Azure AD allows having multiple client secrets active simultaneously. This is useful for rotation – you can add a new secret while the old one is still valid, update your apps to use the new secret, then remove the old secret. There are also Azure AD PowerShell/CLI and Microsoft Graph API methods to create secrets, which you can integrate into automation or DevOps pipelines (beyond scope for this guide).

**Summary:** At this point, if needed, you have a client secret for your app (likely the Spring Boot API app registration, since our React SPA won’t use it). Keep the secret value securely. In production, lean towards certificate credentials or managed identities for better security ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)).

We now have all the Azure AD configuration in place: app(s) registered, redirect URIs set, scopes defined, and a client credential ready. Next, we’ll see how to use the **Tenant ID**, **Client ID**, and scopes from these registrations in our application code.

## 5. Using Tenant and Client IDs in React and Spring Boot Applications

With Azure AD configured, developers need to plug in the relevant identifiers into their applications. The key pieces of information we have from Azure AD are:

- **Directory (Tenant) ID** – the Azure AD tenant identifier (GUID).
- **Application (Client) ID** – the identifier for the app registration(s) (GUID). We have one for the SPA and one for the API.
- **Client Secret or Certificate** (if a confidential client is used, e.g., Spring Boot API).
- **OAuth 2.0 Endpoints** – such as the **Authority URL** (issuer) and the **scope strings** we defined.

Here’s how each is used:

**Tenant ID and Authority:** The **Authority** is the URL that the app will use to authenticate users. It typically includes the Azure AD endpoint and your tenant. For example, `https://login.microsoftonline.com/<TenantID>/` is a common authority URI. In code or config, you’ll often combine this with the path for the v2.0 endpoint (if using Microsoft Identity Platform v2) – e.g. `https://login.microsoftonline.com/<TenantID>/v2.0`. The `<TenantID>` can be your tenant’s GUID or a domain name (like `contoso.onmicrosoft.com` or a verified custom domain). You can also use special aliases:

- `common` – allows sign-in from any Azure AD tenant or Microsoft account (multi-tenant endpoint).
- `organizations` – allows sign-in from any Azure AD tenant (no personal accounts).
- `consumers` – allows only personal Microsoft accounts.

For a single-tenant app, you’ll typically use your specific Tenant ID (or tenant domain) in the authority. This ensures the app only accepts users from your tenant. For a multi-tenant app, your client might start with authority `common` (to direct to a generic endpoint) until a user logs in, then the token will be issued by that user’s tenant.

In our **React app (SPA)**, when configuring MSAL, we will specify the tenant in the authority (or use `common` if we want to allow any tenant). In our **Spring Boot API**, we will use the tenant in the issuer URL for token validation.

**Client IDs:** The Client ID uniquely identifies the application. In the **React SPA**, the MSAL library needs to know the Client ID of the SPA app registration to request tokens for it ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=Initialize%20the%20MSAL,the%20Microsoft%20Entra%20admin%20center)) ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=const%20msalConfig%20%3D%20,navigateToLoginRequestUrl%3A%20true)). In the **Spring Boot API**, if using Azure AD Spring Boot Starter or verifying tokens, we will configure the expected audience as the API’s Client ID or App ID URI ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)).

- In React, the Client ID is public (it’s fine to embed in the front-end config). It’s used to initialize the MSAL.js library so Azure knows which app is calling.
- In Spring Boot, the Client ID might be used to explicitly validate the token’s `aud` claim, ensuring the token was intended for _your_ API.

**Tenant ID in Code:** The tenant ID in front-end code is often indirectly used as part of the authority URL. For example, MSAL can be configured with: `authority: "https://login.microsoftonline.com/<TenantID>"`. In the back-end, the tenant ID appears in the token issuer (`iss` claim). We will set the expected issuer to include our tenant ID, so that Spring Security only accepts tokens issued by _our_ Azure AD tenant ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=%60idp.example.com%2F.well,is%20referred%20to%20as%20a)).

**Example – MSAL Configuration (React):** When we integrate MSAL into React, we’ll create a config object:

```javascript
const msalConfig = {
  auth: {
    clientId: "<SPA-Application-Client-ID>", // GUID from Azure AD for SPA
    authority: "https://login.microsoftonline.com/<TenantID>/", // Authority with tenant
    redirectUri: "http://localhost:3000", // Your redirect URI
  },
  cache: {
    cacheLocation: "sessionStorage", // or localStorage
    storeAuthStateInCookie: false,
  },
};
```

This example shows where the Client ID and Tenant ID go in a typical MSAL setup ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=const%20msalConfig%20%3D%20,navigateToLoginRequestUrl%3A%20true)). If our app were multi-tenant, we could use `common` in place of `<TenantID>` in the authority. If single-tenant, using the Tenant ID (or tenant primary domain) ensures only our tenant’s users can sign in ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=Authority%20Optional%20The%20identity%20provider,should%20return%20the)). The `redirectUri` must exactly match one of those configured in Azure.

**Example – Spring Boot Configuration:** In Spring, using Azure’s starter, we might configure:

```yaml
spring:
  cloud:
    azure:
      active-directory:
        profile:
          tenant-id: <Tenant-ID> # Your tenant GUID
        credential:
          client-id: <API-Application-Client-ID>
          client-secret: ${API_CLIENT_SECRET}
        app-id-uri: api://<API-Application-Client-ID> # or custom App ID URI
```

In a plain Spring Security (without Azure starter), we can use properties:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/<TenantID>/v2.0
          audience: <API-Application-Client-ID>
```

Here:

- `issuer-uri` points to the Azure AD tenant’s v2.0 issuer. Spring will use OIDC discovery to get signing keys ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=the%20,and%20subsequently%20validate%20incoming%20JWTs)).
- `audience` is the expected audience (the API’s client ID or URI). This ensures the JWT’s `aud` claim matches our API ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)). (This `audience` property is supported in newer Spring Security to automatically validate the `aud` claim).

If not using the `audience` property, one can manually validate the `aud` in a custom JWT filter or use the Azure AD starter’s `app-id-uri` config which does the same ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)).

**Tenant ID Usage in Spring Boot:** By using the `issuer-uri` that contains the tenant ID, Spring’s JWT decoder will only trust tokens from that tenant. It fetches the OpenID Connect metadata from `https://login.microsoftonline.com/<TenantID>/v2.0/.well-known/openid-configuration` to get the JWKS (keys) and issuer details ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=%60idp.example.com%2F.well,a%20%20213%20Authorization%20Server)). This means if a token from a different tenant or an untrusted source comes in, the issuer check will fail and the token will be rejected.

**In Summary:**

- **React**: Use _Client ID_ and _Tenant ID_ (in authority URL) in MSAL config. Also specify the _scope_ (which includes the API’s App ID URI and scope name) when requesting tokens. The _Tenant ID_ can be hard-coded or configured (for single tenant), or use `'common'` if multi-tenant support is intended (with appropriate considerations).
- **Spring Boot**: Use _Tenant ID_ in the issuer URL and _Client ID/App ID URI_ as the expected audience. Also use _Client Secret_ (if acting as confidential client for outbound calls).

Next, we will delve into the authentication flow (OAuth2 and OpenID Connect) and how these pieces come together during a user sign-in and API call.

## 6. Implementing Authentication with OAuth2 and OpenID Connect

Azure AD is an OpenID Connect (OIDC) identity provider and OAuth2 authorization server. Our React SPA and Spring Boot API will use the OAuth2 **Authorization Code flow with PKCE** (Proof Key for Code Exchange) to authenticate users and obtain tokens. Let’s break down how the authentication works and how to implement it:

**Authorization Code Flow with PKCE (for SPA):**

1. **User Initiates Sign-in:** The React app (via MSAL library) redirects the user to Azure AD’s authorization endpoint (`https://login.microsoftonline.com/<TenantID>/oauth2/v2.0/authorize`) with parameters including the client ID, requested scopes, redirect URI, and a PKCE code challenge.
2. **User Authenticates:** The user enters credentials (or uses SSO if already logged in). Azure AD shows a consent screen if the user/admin hasn't consented to the requested scopes.
3. **Authorization Code Issued:** After successful login (and consent), Azure AD directs the browser back to the specified redirect URI with an **authorization code** (a one-time short-lived code) in the URL query.
4. **MSAL Exchanges Code for Tokens:** MSAL (running in the React app) catches the redirect, extracts the code, and sends a background request to Azure AD’s token endpoint (`/oauth2/v2.0/token`) including the code, client ID, redirect URI, and the PKCE code verifier. Because this is a SPA (public client), no client secret is sent – the PKCE code verifier secures the exchange. Azure AD validates everything and responds with:
   - an **ID Token** (JWT) – contains user identity information (subject, name, email, etc) in OIDC standard claims.
   - an **Access Token** (JWT) – authorizes access to the requested resource (in our case, the API scope).
   - a **Refresh Token** – long-lived token that can be used to get new access tokens when the current one expires (MSAL manages this if applicable; for SPA with code+PKCE in v2 endpoint, a refresh token is often provided and MSAL stores it in memory or session storage).
5. **Tokens Stored & User Authenticated:** MSAL stores the tokens (ID token and access token) in its cache (browser storage as configured). At this point, the React app considers the user “logged in” and typically uses the ID token info to greet the user or store profile info.

All of this is handled by the MSAL library, so as a developer, you mostly call MSAL APIs and handle success or error responses. The main interactive piece is initiating the login redirect or popup.

**OpenID Connect and ID Token:** OIDC is an extension on OAuth2 that provides the ID token, which represents user authentication. MSAL will request the `openid` and `profile` scopes by default to get an ID token (which is why in Azure AD’s “API permissions” for the client app, you often see **User.Read** or other Microsoft Graph delegated perms automatically added – those allow basic profile reading, but strictly `openid profile` are OIDC scopes that any Azure AD app can use without special config). The ID token’s primary use is to get the user’s identity (e.g., name, oid, emails) without another API call. **Important:** The ID token should only be processed by the client app. Never send the ID token to your API – the API doesn’t need it (the API uses the access token). And never trust the ID token for authorization decisions on the API side; use the access token for that.

**Access Token:** The access token issued for our custom API will have:

- an **audience (`aud`)** of the API’s App ID URI or client ID (meaning “this token is intended for that API”) – our Spring Boot should verify this.
- a **scope (`scp`)** claim listing the permissions (e.g., “API.Access”) granted ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=const%20accessTokenRequest%20%3D%20,account%3A%20account%2C)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=.acquireTokenSilent%28accessTokenRequest%29%20.then%28function%20%28accessTokenResponse%29%20,error%20instanceof%20InteractionRequiredAuthError%29)).
- the issuing authority (`iss`) which includes our tenant ID (e.g., `https://sts.windows.net/<tenant>` for v1, or `https://login.microsoftonline.com/<tenantID>/v2.0` for v2 tokens).
- **OID (object ID)** of the user, tenant ID (`tid`), perhaps group or role claims if configured, etc.

The React app will attach this access token in the **Authorization header** of HTTP requests to the Spring Boot API: `Authorization: Bearer <access_token_jwt>`.

**Spring Boot API – Token Validation (OAuth2 Resource Server):**  
When the API receives a request with a Bearer token:

1. Spring Security will intercept the request. It will check for the `Authorization: Bearer ...` header.
2. It will validate the JWT. Using the configured **issuer URI**, Spring’s OAuth2 Resource Server auto-downloads the signing keys (public keys) from Azure AD’s JWKS endpoint ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=Where%20,and%20subsequently%20validate%20incoming%20JWTs)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=It%20achieves%20this%20through%20a,deterministic%20startup%20process)). It validates the token’s signature, expiration, issuer (`iss`), and audience (`aud`) against what we configured ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)).
3. If valid, the token’s claims are mapped to a Spring Security **Authentication** object. By default, Spring will take the `scp` claims from the token and turn each scope into an authority prefixed with `SCOPE_`. For example, scope `API.Access` becomes authority `SCOPE_API.Access`. If the token contains an OIDC **roles** claim (app roles), those might be prefixed with `ROLE_` if using Azure’s starter library. The exact mapping can be customized, but out-of-the-box, you get `SCOPE_{scopeName}` authorities.
4. You can then use Spring Security annotations to authorize. For example, `@PreAuthorize("hasAuthority('SCOPE_API.Access')")` on a controller method will only allow calls with that scope ([java - Spring boot ressource server with azure ad - Stack Overflow](https://stackoverflow.com/questions/74834378/spring-boot-ressource-server-with-azure-ad#:~:text=http%20.authorizeHttpRequests%7B%20authorize%20,oauth2.jwt%28Customizer.withDefaults%28%29%29)) ([java - Spring boot ressource server with azure ad - Stack Overflow](https://stackoverflow.com/questions/74834378/spring-boot-ressource-server-with-azure-ad#:~:text=authorize%20)). Or more generally, you might simply require any authenticated token for most endpoints and optional specific scopes for sensitive ones.

If token validation fails (token missing, expired, wrong audience, invalid signature, etc.), Spring Security will return an HTTP 401 Unauthorized automatically. If the token is valid but lacks a required authority, it will return 403 Forbidden.

**User Info Flow (optional):** In some cases, after obtaining an access token, the SPA might call a Microsoft Graph API to get user profile (especially if more detail or to confirm login). With Azure AD, an ID token often suffices for basic profile (it contains username, email, etc., if requested via claims or by including `profile` scope). For simplicity, we won’t integrate Microsoft Graph here, but advanced apps can combine Graph calls (requiring Graph scopes and consent) to fetch details like user’s manager, photo, etc.

**Refreshing Tokens:** MSAL automatically handles token refresh. The access tokens from Azure AD by default last **1 hour** (for v2 endpoints, and a refresh token lasts 24 hours for SPAs) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20pattern%20for%20acquiring%20tokens,access%20and)). MSAL will try `acquireTokenSilent` to use a cached token or a refresh token to get a new access token without user interaction ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20pattern%20for%20acquiring%20tokens,access%20and)). If that fails (e.g., refresh token expired or revoked, or no session), MSAL will require a user interaction (pop-up or redirect) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20silent%20token%20requests%20to,to%20acquire%20tokens)). As a developer, you typically call `acquireTokenSilent` before an API call; MSAL will return a valid token or throw an exception that you handle by calling `loginRedirect` or `loginPopup` again if needed ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=.acquireTokenSilent%28accessTokenRequest%29%20.then%28function%20%28accessTokenResponse%29%20,accessToken)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=.acquireTokenSilent%28accessTokenRequest%29%20.then%28function%20%28accessTokenResponse%29%20,Call%20API%20with%20token)).

**Authentication Flow Summary (step-by-step):**

- **Step 1:** _User visits the React app._ If not already authenticated, the app shows a “Login” button.
- **Step 2:** _User clicks Login._ MSAL uses `loginRedirect()` (or `loginPopup()`) to start the auth flow. The browser navigates to Azure AD.
- **Step 3:** _Azure AD prompts for credentials and consent._ User logs in. Azure AD returns an auth code to the React app’s redirect URI.
- **Step 4:** _React app (MSAL) processes redirect._ MSAL exchanges the code for tokens (ID & access). The user is now authenticated in the app (MSAL provides user info from ID token).
- **Step 5:** _React calls the Spring API._ It includes the access token in the Authorization header.
- **Step 6:** _Spring Boot API receives request._ The Spring Security filter validates the JWT (issuer = Azure AD with our tenant, audience = our API). Token is valid and contains scope “API.Access”.
- **Step 7:** _API authorizes the request._ The endpoint or security config ensures the required scope is present. If yes, the controller executes (for example, returns some protected data).
- **Step 8:** _React app receives API response._ Data is displayed to the user.
- **(Later)** _Token expires._ MSAL either transparently uses refresh token or prompts user to sign in again if needed. The cycle continues as long as the session is active.

This flow implements OAuth2 for delegated user access and OIDC for user identity. It’s secure because the sensitive operations (auth and token issuance) happen on secure redirects and back-channel calls with PKCE, and because the API validates every request’s token.

**Libraries and Standards:** We heavily rely on the **Microsoft Authentication Library (MSAL)** for the client and **Spring Security** for the server, so we don’t have to manually implement protocol details. This is aligned with best practices: _“Don’t program directly against protocols like OAuth2 and OIDC, use supported libraries”_ ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Use%20modern,to%20securely%20sign%20in%20users)). MSAL and Spring Security take care of token caching, validation, and adherence to standards.

Now that we understand the flow, we can implement the code in our React and Spring Boot projects.

## 7. API Security Considerations and Best Practices

Securing an application with OAuth2/OIDC involves more than just the basic flow. Advanced developers should consider various security best practices to protect tokens, user data, and the integrity of the authentication system. Here are key considerations and best practices:

- **Use HTTPS Everywhere:** Ensure that all redirect URIs and endpoints are served over **HTTPS** in production ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=,https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient)). This prevents token interception. (Azure AD will not allow non-https redirect URIs except for localhost development) ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=,for%20some%20localhost%20redirect%20URIs)).

- **Avoid Wildcard Redirects:** Do not use wildcard (`*`) redirect URI patterns ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=,calling%20back%20to%20your%20app)). Always specify exact allowed URLs. Wildcards can introduce security holes by allowing unintended redirection.

- **Maintain Redirect URI Ownership:** Only use redirect URIs in domains you control (so you can ensure they remain secure). Keep DNS records up to date for those domains ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20Manage%20your%20redirect,URIs)). Regularly **review and remove** any redirect URIs that are not needed ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=,URIs%20on%20a%20regular%20basis)).

- **No Implicit Flow (unless needed):** The OAuth2 implicit flow (where tokens are returned in the redirect URI fragment) is deprecated for most scenarios due to security issues. Use Authorization Code flow with PKCE instead (which MSAL does by default). In Azure AD app settings, **do not enable** the implicit grant checkboxes for access token or ID token unless you have a legacy reason ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20If%20your%20app,list%20of%20app%20registration%20owners)).

- **Least Privilege Scopes:** Define and request the **minimal scopes** necessary for the app’s functionality ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Make%20sure,permissions%2C%20see%20this%20permissions%20reference)). Do not request overly broad permissions (like `User.Read.All` for Graph or a custom `*.All` scope) unless absolutely required. If your API has multiple operations, consider splitting into fine-grained scopes so clients can request only what they need ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Make%20sure,permissions%2C%20see%20this%20permissions%20reference)).

- **Consent and Permissions:** If a scope is high-privilege, mark it **admin consent required** (in Expose an API) so that only administrators can grant it ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Scope%20name%20The%20name%20of,only)). This prevents end-users from accidentally granting too much power to a client. On the client side, be transparent about what permissions the app asks for – use clear description fields in Azure AD for consent prompts.

- **Validate Tokens on API Side:** Do not assume tokens are valid – always validate signature, issuer, audience, and expiration in the API. Use the well-known Azure AD public keys (libraries handle this). Only accept tokens from the expected Azure AD tenant (or tenants). This prevents malicious tokens from other sources being accepted.

- **Validate **Audience** and **Scopes**:** Your API should check that the token’s audience (`aud`) is either your API’s Client ID or App ID URI, and that the token contains the scope (`scp`) required for the endpoint ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)). Spring Security and Azure’s libraries can enforce this automatically (as we configured with `audience` or `app-id-uri`) ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)). This ensures the token presented is truly meant for your API and has the right permissions. If using custom validation, be cautious to do these checks.

- **Never Trust the Client with Tokens:** The React app should never try to manipulate or inspect the access token beyond storing and sending it. For example, _do not attempt to parse JWT in the JavaScript front-end to make authorization decisions_ – the token could be tampered with if not validated, and its content could change (or be encrypted in the future) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20DO%20NOT%20look,to%20validate%20the%20access%20token)). Only the API (which has the token validation setup) should interpret token claims. The client can use the ID token for display (which MSAL already validated), but treat access tokens as opaque from the client’s perspective, simply a credential to present to the API ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20DO%20NOT%20look,to%20validate%20the%20access%20token)).

- **Protect Secrets and Credentials:** As emphasized, never embed client secrets in front-end code. Even in back-end code, avoid directly hardcoding secrets. Use environment config or Azure Key Vault to load them securely ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)). Better yet, if running on Azure, consider using a **Managed Identity** for the app to acquire tokens for Azure resources without any secret at all ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)). Also, limit who has access to the Azure AD app registration’s management – monitor the list of owners and restrict it ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20If%20your%20app,list%20of%20app%20registration%20owners)).

- **Token Lifetime & Refresh:** The default settings in Azure AD (v2) give refresh tokens with a 24-hour lifetime for SPAs ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=token%20is%20found%20or%20the,see%3A%20Acquiring%20an%20Access%20Token)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20silent%20token%20requests%20to,to%20acquire%20tokens)). Long refresh tokens in a browser can be a risk if XSS or malicious code runs. Make sure to guard against XSS in your SPA to protect the MSAL cache. If security policies require, you can configure conditional access or custom policies to adjust token lifetimes (though Azure AD moved to more preset lifetimes for consistency).

- **Single-Sign-On (SSO) and Session Security:** If your app is part of a suite, leveraging SSO means if a user is already signed in to Azure AD (for example in another tab to Office 365), MSAL can silently sign them in (via an invisible iframe or `ssoSilent` in some MSAL versions). This improves UX. However, be aware of **Conditional Access** and **third-party cookie** issues – browsers blocking third-party cookies can interfere with silent token renewal ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20silent%20token%20requests%20to,to%20acquire%20tokens)). MSAL’s design (silent -> if fail, interactive) accounts for this, but testing in various browsers is wise.

- **Logging and Monitoring:** In production, monitor your application’s authentication and authorization events. Azure AD provides sign-in logs, and you can integrate with Azure AD Audit logs to track consent grants, token issuance, etc. On the application side, log important security events (but never log sensitive data like actual tokens or passwords). Also consider using **Application Insights** or other monitoring to detect unusual patterns (e.g., multiple 401s that could indicate token issues).

- **Error Handling and User Experience:** Ensure your front-end can handle token expiration gracefully (e.g., prompt user to sign in again if needed). Catch MSAL exceptions such as `InteractionRequiredAuthError` which indicates that silent renewal failed and you need user interaction (MSAL throws this, which you can catch and then call `loginRedirect`) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=%2F%2F%20Acquire%20token%20silent%20success,error%20instanceof%20InteractionRequiredAuthError%29)). Also handle the case where Azure AD might require MFA or conditional access – the MSAL redirect will handle it, but your UI should not break during the process.

- **API Design for Security:** In your Spring Boot API, besides JWT validation, enforce **authorization rules** for each endpoint. Use method-level security (`@PreAuthorize`) or configure `HttpSecurity` to restrict URLs by scope/role. For example, you might require `SCOPE_API.Write` for POST/PUT requests. This ensures even if a user has a token, they can only use it for allowed operations.

- **CORS (Cross-Origin Resource Sharing):** Since a React app (on say `localhost:3000` or a domain) will call an API on another domain, configure CORS on the Spring Boot API to allow the front-end origin. Ensure you only allow the necessary origins and headers (Authorization). Spring Boot can be configured with a CORS filter or using `@CrossOrigin` on controllers for the specific domain of your front-end. This doesn’t directly affect OAuth, but it’s necessary for the browser to accept responses.

- **Prevent CSRF (for OAuth flows):** When using MSAL, CSRF is generally not a concern for the implicit parts because we are not using cookies for auth (the token is in Authorization header). But if your Spring Boot app had endpoints that modify state and also used cookies, ensure to use Spring’s CSRF protection. In our token-based scenario, CSRF is less relevant since cookies aren’t used for API auth.

- **Use MSAL and Spring Security Updates:** Keep the MSAL library updated to the latest version – it is actively maintained for security improvements. The same goes for Spring Security and Azure spring libraries. These ensure you get the latest fixes and features (for example, enforcement of audience validation in newer Spring versions was an enhancement for security ([The latest on Azure Active Directory integration](https://spring.io/blog/2021/01/13/the-latest-on-azure-active-directory-integration#:~:text=In%20OAuth%202,server%20sample%20project%20for%20details)) ([The latest on Azure Active Directory integration](https://spring.io/blog/2021/01/13/the-latest-on-azure-active-directory-integration#:~:text=In%20OAuth%202,server%20sample%20project%20for%20details))).

- **No ROPC in Production:** The Resource Owner Password Credentials flow (where you’d collect user passwords in the app to exchange for token) is **highly discouraged** except in legacy scenarios ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=unless%20explicitly%20required,the%20valid%20scenario%20here)). It bypasses many security features (MFA, federated IdPs) and should not be used in our context (and MSAL doesn’t use it by default). Always prefer interactive or at least confidential client flows with proper redirects.

In short, follow the principle of **defense in depth**: Azure AD provides a secure token service, but you must use it correctly – restrict who can access what, validate everything, protect secrets, and use proven libraries instead of custom solutions ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Use%20modern,to%20securely%20sign%20in%20users)). By adhering to these best practices, you significantly reduce the risk of common vulnerabilities in OAuth integration.

## 8. Deployment and Management of the Azure AD Application in Production

Deploying an application that uses Azure AD involves not only deploying the code (React build and Spring Boot app) but also managing the Azure AD app registrations across environments. Here are considerations and steps for a smooth deployment and ongoing management in a production environment:

**Separate Azure AD App Registrations for Environments:** It’s often wise to have distinct app registrations for dev, test, and production. This prevents test configurations (like redirect URIs pointing to localhost or test URLs) from existing in the production app registration ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=In%20a%20production%20web%20application%2C,registrations%20for%20development%20and%20production)). For example, you might have “MyApp-Dev-SPA” & “MyApp-Dev-API” and “MyApp-Prod-SPA” & “MyApp-Prod-API”. Each has its own client IDs, redirect URIs, and secrets. Your code can be configured (via environment variables) to use the appropriate IDs and endpoints for each environment.

**Configuration Management:** In your CI/CD pipeline or configuration files, parameterize the following per environment:

- Tenant ID (in case you use separate Azure AD tenants for testing vs prod – some organizations have a dev Azure AD and a separate prod Azure AD).
- Client IDs (for SPA and API).
- Client Secret (for the API, in secure storage).
- Redirect URIs (for SPA, though these are mostly front-end config and Azure AD config).
- Scope names/values (likely the same name but with different client ID/URI prefixes per environment).

Using environment-specific config ensures your app will request the right scope (which includes the API’s App ID URI GUID, which will differ between dev and prod).

**Automating App Registration Setup:** In enterprise settings, manually clicking around the portal for each environment can be error-prone. Consider automating Azure AD app creation and configuration using:

- **Infrastructure as Code (IaC):** Tools like Terraform (with the AzureAD provider) or Bicep/ARM templates. These can create app registrations, set secrets, redirect URIs, and expose scopes. _Note:_ Not all aspects of app registration have full ARM support, so Terraform or the Azure CLI/PowerShell might be more straightforward.
- **Azure CLI / PowerShell:** Azure CLI command `az ad app create` and `az ad app update` can script creation of apps, adding redirect URIs (`--web-redirect-uris`, `--enable-public-client` for SPA, etc.), and adding secrets. Similarly, PowerShell (AzureAD or Microsoft Graph modules) can script these tasks.
- **Microsoft Graph API:** The Azure AD app registration (Application and ServicePrincipal objects) can be manipulated through Graph API. Microsoft provides Graph endpoints to create an application, add passwordCredentials (secrets), add permission scopes, and even grant admin consent. This is advanced but powerful for full automation. For example, a deployment script could check if an app registration exists, create one if not, or update existing one’s settings.

By automating, you can version control the configuration of your identity settings and ensure consistency between environments.

**Key Vault for Secrets:** In production, never leave the client secret in plain text on the server or in config files. Use **Azure Key Vault** to store the secret and have your Spring Boot app fetch it at startup (Azure provides integration and libraries for this). Alternatively, use environment variables set in your deployment environment (ensuring only ops team/DevOps pipeline knows the value). If using Azure App Service or Kubernetes, use their secret management features (e.g., App Service application settings are encrypted at rest, or Kubernetes secrets). Rotate the secret periodically (Key Vault can even generate new secrets and Azure AD can have multiple secrets as noted).

**Using Certificates in Prod:** If you switch to a certificate credential for the API app, deploy the certificate securely. For instance, store the PFX in Key Vault and load it in Spring Boot at runtime. Azure Key Vault has a feature to directly integrate with Azure AD app (Workload Identity Federation), but that’s advanced – it allows an app running in Azure to authenticate to Azure AD via a token from Key Vault or other identity, avoiding secrets entirely ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=If%20you%27re%20using%20an%20Azure,Azure%20Resource%20Manager%20service%20connections)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Federated%20identity%20credentials%20are%20a,secrets%20using%20workload%20identity%20federation)). This might be overkill for many apps, but it’s available.

**Enterprise Policies:** If your company requires Conditional Access (e.g., MFA always, or allowed locations, etc.), work with your Azure AD admin to create policies that exclude service accounts or adjust for your app if needed. For example, if the API uses client credentials, you might need a policy to allow it (since no interactive login is involved, MFA doesn’t apply). Azure AD has the concept of **Enterprise Applications** for each service principal – in the Enterprise Applications blade, you can assign users, groups, or even restrict the app to certain users. By default, if “Users can consent to apps” is on, any user can use a multi-tenant app. For internal single-tenant apps, you might not worry about this, but for multi-tenant, consider enabling **Admin consent workflow** in Azure AD to control external access.

**Monitoring and Logging in Production:**

- **Azure AD Sign-in Logs:** Monitor these for your app’s sign-ins. You can filter by application to see successful and failed logins, errors, etc. This can catch issues like users from unexpected tenants trying to access (for multi-tenant apps), or errors due to misconfiguration.
- **Azure AD App Audit Logs:** If someone modifies the app registration (e.g., adds a new secret, changes a redirect URI), Azure logs that. Review these logs for unauthorized changes.
- **App Logs:** On the Spring Boot side, log authentication events (Spring Security can output a log when a JWT is validated, or you can add a filter to log principal details). But again, don’t log the token itself.

**Scaling Considerations:** Azure AD can handle high scale for auth, but be mindful of token caching in MSAL. MSAL by default stores tokens in session or local storage in the browser – which is fine per user. Spring Boot, using Spring Security, by default does not cache tokens between requests (it will parse/validate each time; the library caches the keys from Azure AD so that’s efficient). If your API sees huge traffic, ensure the `issuer-uri` discovery call is done once (it is, by Spring Boot at startup) so it doesn’t fetch metadata repeatedly. Azure AD’s JWKS (keys) are cached and only refetched when the signing keys rotate (which is rare). So overhead is low.

**Testing in Production Environment:** Always test the full login flow in an environment as close to prod as possible. Common issues to catch:

- Missing or incorrect redirect URI (AADSTS50011 errors).
- CORS issues between SPA and API.
- Scope consent issues (maybe admin consent needed).
- Token validation errors due to audience or issuer mismatch (e.g., if you accidentally used the wrong tenant in config, you’d see 401 errors and logs like “Invalid issuer or configuration” in Spring Boot).

**Admin Consent for Multi-Tenant Apps:** If your app is multi-tenant and you expect external organizations to use it, the onboarding involves an admin of the other org consenting to your app’s permissions. Microsoft provides an **admin consent URL** (e.g., `https://login.microsoftonline.com/{otherTenantID}/adminconsent?client_id=<YourAppId>...`). Document this process if relevant. It’s beyond just deploying, but it’s part of managing who can use the app. For single-tenant, this doesn’t apply.

**Managing App Registration Lifecycle:** The app registration is an Azure AD object like any other resource. Manage it like code:

- Keep track of app registration settings in documentation or scripts.
- If decommissioning the app, delete the app registration to reduce clutter and security risk.
- If transferring ownership, update the Owners list. Remove employees who leave from the Owners.

**Updates to the App Registration:** If you need to add a new scope or change a redirect URI, that is a breaking change for clients. In production, adding a new redirect URI is safe (it doesn’t break existing ones), but removing one or changing the App ID URI will potentially break existing tokens or client trust. Plan such changes carefully and coordinate deployment of code and Azure AD changes. Azure AD now allows editing an App ID URI, but if you do, tokens issued after will have new audience – your API validation would need to allow both old and new during a transition, possibly.

**High-Level Deployment Steps Recap:**

1. Deploy Azure AD app registrations (via portal or script) for prod, with correct settings (no localhost URIs, actual domain, production secret or certificate).
2. Configure your React app’s production build to use prod Azure AD settings (prod tenant, client ID, redirect URI).
3. Configure your Spring Boot app (via application-prod.yaml or environment) with prod Azure AD settings (issuer URI with prod tenant, client ID, secret, allowed audiences).
4. Deploy the React app (e.g., to Azure Storage Static site or Azure App Service or other hosting) at the URL that matches the redirect URI.
5. Deploy the Spring Boot app (e.g., to Azure App Service, Azure Spring Apps, AKS, VM, etc.) and ensure its URL matches any expected App ID URI if needed (though not strictly required to match domain).
6. Test the login flow in prod environment – it should redirect to Azure AD, log in, redirect back, and the React app should call the API successfully with a valid token.
7. Monitor logs and adjust any settings as needed.

By following these deployment considerations, you ensure that your integration with Azure AD remains robust, secure, and maintainable as the application moves to production and beyond.

## 9. Integration Example: React SPA with Azure AD (Using MSAL)

Now, let’s implement the client-side integration in our React application using **MSAL (Microsoft Authentication Library) for JavaScript**. This will cover setting up the MSAL provider, logging in the user, acquiring access tokens, and calling the protected API.

**Prerequisites:** You should have the **@azure/msal-browser** (or **@azure/msal-react**) package installed. For example, run: `npm install @azure/msal-browser` (and `@azure/msal-react` if using the React wrapper).

**MSAL Configuration:** In your React app, create a config (e.g., `authConfig.js`):

```javascript
import { PublicClientApplication } from "@azure/msal-browser";

export const msalConfig = {
  auth: {
    clientId: "<YOUR-SPA-CLIENT-ID>", // Application (client) ID of the SPA app ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=const%20msalConfig%20%3D%20,navigateToLoginRequestUrl%3A%20true))
    authority: "https://login.microsoftonline.com/<YOUR-TENANT-ID>/", // Azure AD tenant authority
    redirectUri: "http://localhost:3000", // The redirect URI you set in Azure AD ([Initialize MSAL.js client apps - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-initializing-client-applications#:~:text=const%20msalConfig%20%3D%20,navigateToLoginRequestUrl%3A%20true))
    postLogoutRedirectUri: "http://localhost:3000", // Where to navigate after logout (optional)
    navigateToLoginRequestUrl: true, // If true, will redirect back to where login was initiated
  },
  cache: {
    cacheLocation: "sessionStorage", // or "localStorage" for persistent caching
    storeAuthStateInCookie: false, // set true if dealing with IE/edge issues
  },
};

// Create MSAL instance
export const msalInstance = new PublicClientApplication(msalConfig);
```

Replace `<YOUR-SPA-CLIENT-ID>` with the client ID GUID of your React app registration, and `<YOUR-TENANT-ID>` with your tenant ID (or “common” if multi-tenant, or tenant domain name). This configuration will initialize MSAL with the basics: who the app is (clientId), who it trusts (authority/tenant), and where it should return after login (redirectUri). The MSAL instance will automatically handle caching tokens in sessionStorage.

**Providing MSAL to React:** If using `@azure/msal-react`, you can wrap your app in an **MsalProvider** in `index.js`:

```jsx
import React from "react";
import ReactDOM from "react-dom";
import { MsalProvider } from "@azure/msal-react";
import App from "./App";
import { msalInstance } from "./authConfig";

ReactDOM.render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <App />
    </MsalProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
```

This makes the MSAL instance available throughout the component tree.

**Logging in the User:** You can choose a **popup** or **redirect** method for user sign-in. A popup keeps the user on the same page and opens a separate window for Azure AD; a redirect will navigate away to the Azure AD login page and then come back. Both are supported by MSAL. We will use redirect in this example for simplicity (and fewer popup blockers issues).

In your main component (or a dedicated Login component), trigger login:

```jsx
import React from "react";
import { useMsal } from "@azure/msal-react";

function LoginButton() {
  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error(e);
    });
  };

  return <button onClick={handleLogin}>Sign In</button>;
}
```

Here, `loginRequest` is an object defining scopes you want during login. You might define it as:

```javascript
export const loginRequest = {
  scopes: ["openid", "profile", "<YOUR-API-APP-ID-URI>/<SCOPE-NAME>"],
};
```

For example, if your API App ID URI is `api://12345-abcde-...` and scope name is `API.Access`, the scope string to request is `"api://12345-abcde-.../API.Access"`. Including `openid` and `profile` is good practice to get an ID token with user info ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=const%20accessTokenRequest%20%3D%20,account%3A%20account%2C)). If you need refresh token (MSAL v2 gives one by default for code flow), including `offline_access` scope would request that, but MSAL React might handle it implicitly.

When `loginRedirect` is called, MSAL will save the state and redirect the browser to Azure AD. After authentication, Azure AD will redirect back to the redirectUri. MSAL will then process the response. Using `MsalProvider`, the library will automatically handle the redirect promise behind the scenes (in earlier MSAL usage without the React wrapper, you would call `msalInstance.handleRedirectPromise()` on page load to handle the auth code exchange).

**Checking Authentication State:** The MSAL React library provides hooks like `useIsAuthenticated()` or `useAccount` to check if a user is logged in. Alternatively, after login, you can check `instance.getAllAccounts()` to see if an account is present.

For example:

```jsx
import { useIsAuthenticated } from "@azure/msal-react";
function App() {
  const isAuthenticated = useIsAuthenticated();

  return (
    <div>
      {isAuthenticated ? <span>Welcome!</span> : <LoginButton />}
      {isAuthenticated && <DataFetcher />}
    </div>
  );
}
```

If authenticated, we display a welcome and maybe a component that fetches data; if not, show the login button.

**Acquiring Access Token for API Calls:** Once the user is logged in (meaning MSAL has an ID token and probably an access token if we requested scopes on login), we need to ensure we have an access token when calling the API. MSAL will have cached the token for `<YOUR-API-APP-ID-URI>/<SCOPE>` if it was included in the `loginRedirect` scopes. If not, or if you need to call additional scopes later, you use `acquireTokenSilent` or `acquireTokenPopup`.

For example, to call the API, we can do:

```jsx
import { useMsal } from "@azure/msal-react";
import axios from 'axios';

function DataFetcher() {
  const { instance, accounts } = useMsal();

  const callApi = async () => {
    const account = accounts[0]; // assuming one account signed in
    if (!account) return;
    try {
      const response = await instance.acquireTokenSilent({
        scopes: ["<YOUR-API-APP-ID-URI>/<SCOPE-NAME>"],
        account: account
      });
      const accessToken = response.accessToken; ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=.acquireTokenSilent%28accessTokenRequest%29%20.then%28function%20%28accessTokenResponse%29%20,and%20send%20an%20interactive%20request))
      console.log("Acquired token:", accessToken);
      // Call API with the token
      const apiResponse = await axios.get("http://localhost:8080/your/api/endpoint", {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      console.log("API data:", apiResponse.data);
    } catch (err) {
      if (err instanceof InteractionRequiredAuthError) {
        // Token silent request failed (perhaps expired and no refresh token or need consent)
        instance.acquireTokenRedirect({
          scopes: ["<YOUR-API-APP-ID-URI>/<SCOPE-NAME>"]
        });
      } else {
        console.error(err);
      }
    }
  };

  React.useEffect(() => {
    callApi();
  }, []);

  return <div>Loading data...</div>;
}
```

In this snippet, we attempt to silently get an access token for our API scope ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20pattern%20for%20acquiring%20tokens,access%20and)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=.acquireTokenSilent%28accessTokenRequest%29%20.then%28function%20%28accessTokenResponse%29%20,error%20instanceof%20InteractionRequiredAuthError%29)). MSAL will:

- Check cache for a non-expired token for that scope ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20pattern%20for%20acquiring%20tokens,access%20and)).
- If not found or expired, use the refresh token to get a new one (if possible) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=When%20this%20method%20is%20called%2C,access%20and)).
- If that fails (e.g., refresh token expired or no session), it throws an `InteractionRequiredAuthError` ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20silent%20token%20requests%20to,to%20acquire%20tokens)).

We catch that specific error and call `acquireTokenRedirect` to prompt the user to login again or consent. This flow ensures minimal user disruption. In practice, if your initial login already consented to the API scope (which it did if you included it), you typically won’t need a second interaction unless the user’s session is gone after many hours.

Using **axios** or **fetch** to call the API is straightforward: just set the `Authorization` header with the `Bearer <token>`. The API endpoint (here `http://localhost:8080/your/api/endpoint`) should be one of your protected routes in Spring Boot.

**Logout:** You should implement a logout that clears MSAL and redirects the user to Azure AD’s sign-out. MSAL provides `instance.logoutRedirect()` or `logoutPopup()`. This will clear the MSAL cache and redirect to Azure AD sign-out endpoint, which in turn can log the user out of Azure AD (or just end the session for your app depending on config). We set `postLogoutRedirectUri` so after Azure AD sign-out, it comes back to our site.

**Recap of React Integration:** We configured MSAL with our app IDs, triggered login, acquired tokens, and used those tokens in API calls. The heavy lifting (token caching, silent refresh, PKCE, etc.) is handled by MSAL. Our job was mostly to configure and call the right methods. We also need to handle UI transitions (logged-in vs not, loading states for API calls, error messages if something goes wrong). With the above structure, once the user is logged in, any call to `DataFetcher` will automatically attach a valid token (refreshing it if needed). If the token expires after an hour, the next call triggers MSAL to use the refresh token or require login again, as described.

Finally, let’s move to the server side to complete the picture.

## 10. Integration Example: Spring Boot API with Azure AD (Using Spring Security)

Now we will set up the Spring Boot back-end to **accept and validate Azure AD-issued tokens** and secure the API endpoints. We assume a Spring Boot application using Spring Security 5+.

**Prerequisites:** Include the required Spring Security dependencies. In `build.gradle` or `pom.xml`, ensure you have:

- Spring Boot Starter Security (`spring-boot-starter-security`).
- Spring Security OAuth2 Resource Server (`spring-boot-starter-oauth2-resource-server`).
- (Optional) The Azure Spring Boot Starter for Azure AD if you prefer that approach (`com.azure.spring:spring-cloud-azure-starter-active-directory` for latest version as of early 2025).

For our example, we will show the standard Spring Security configuration which uses the OAuth2 Resource Server support.

**Application Properties (application.yml):** Configure Spring Security to know the Azure AD issuer and audience. For instance:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/<YOUR-TENANT-ID>/v2.0
          audience: <YOUR-API-CLIENT-ID>
```

Let’s break that down:

- `issuer-uri` is the base URL of the token issuer. Azure AD’s documentation says for the v2 endpoint, the issuer will be `https://login.microsoftonline.com/<TenantID>/v2.0` (there is a common metadata URL, but at runtime tokens have tenant-specific issuers) ([java - Spring boot ressource server with azure ad - Stack Overflow](https://stackoverflow.com/questions/74834378/spring-boot-ressource-server-with-azure-ad#:~:text=EDIT%3A)) ([java - Spring boot ressource server with azure ad - Stack Overflow](https://stackoverflow.com/questions/74834378/spring-boot-ressource-server-with-azure-ad#:~:text=I%27ve%20changed%20the%20issuer,id%7D%2Fv2.0)). By providing issuer-uri, Spring will auto-configure JWT validation by fetching the OIDC discovery document from Azure AD ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=the%20,and%20subsequently%20validate%20incoming%20JWTs)).
- `audience` is the expected audience claim. Setting this property (supported in Spring Security 5.5+) means the JWT’s `aud` must contain this value or validation will fail. We set it to our API’s client ID (GUID). According to Spring’s documentation, it will accept the token if any of the `aud` values matches this configured audience.

Alternatively, instead of `audience`, if using Azure’s starter:

```yaml
spring:
  cloud:
    azure:
      active-directory:
        client-id: <YOUR-API-CLIENT-ID>
        app-id-uri: api://<YOUR-API-CLIENT-ID> # The App ID URI configured in Azure ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=credential%3A%20client))
```

The Azure starter internally sets up the equivalent checks (it knows the client ID and app ID URI and will validate that the token’s audience matches one of those) ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)).

**Security Configuration Class (if needed):** If you include Spring Boot Starter Security and the above properties, you may not need much custom config – Spring Boot will auto-configure a JWT decoder based on issuer-uri and secure all endpoints by default (requiring authentication). However, for finer control (e.g., to open some endpoints or to require specific scopes), you can add a class:

```java
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
          .authorizeHttpRequests(authz -> authz
                .antMatchers("/public/**").permitAll()   // allow public endpoints if any
                .antMatchers(HttpMethod.GET, "/admin/**").hasAuthority("SCOPE_API.Read")  // example scope check
                .antMatchers(HttpMethod.POST, "/admin/**").hasAuthority("SCOPE_API.Write")
                .anyRequest().authenticated()  // everything else requires authentication
          )
          .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> {
                     // (Optional) you could add a custom converter to handle roles vs scopes here
                })
          );
        return http.build();
    }
}
```

This configuration:

- Permits any requests to `/public/**` without a token.
- Requires the scope `API.Read` for GET requests to `/admin/*` and `API.Write` for POST to `/admin/*` (assuming those are the scope names we chose; prefix `SCOPE_` is automatically added by Spring Security to each scope in the token).
- All other endpoints simply require any authenticated JWT.

If you want to enforce a single scope for the whole API, you could do `.anyRequest().hasAuthority("SCOPE_API.Access")` instead.

Note: The string `"SCOPE_API.Read"` is how Spring represents a scope claim of `"API.Read"` by default ([java - Spring boot ressource server with azure ad - Stack Overflow](https://stackoverflow.com/questions/74834378/spring-boot-ressource-server-with-azure-ad#:~:text=http%20.authorizeHttpRequests%7B%20authorize%20,oauth2.jwt%28Customizer.withDefaults%28%29%29)). Spring Security’s default **JwtAuthenticationConverter** looks at `scp` claim for Azure AD (and `scope` for other providers) and prefixes each entry with `SCOPE_`. If Azure AD issues roles (in `roles` claim because we assigned app roles to user or client), Spring (by default) might not include them unless you customize. The Azure starter automatically maps Azure AD app roles to Spring authorities as well (with prefix `ROLE_` typically). For simplicity, we stick with scopes.

**Testing the API Security:** With this setup, let’s say we have a controller:

```java
@RestController
public class HelloController {
    @GetMapping("/hello")
    public String hello(@AuthenticationPrincipal Jwt jwt) {
        String username = jwt.getClaim("preferred_username");
        return "Hello, " + username + "! Your token is valid.";
    }
}
```

When the React app calls `GET /hello` with the access token:

- Spring Security filters check the JWT. It’s from `login.microsoftonline.com/tenant/v2.0` (issuer matches), audience matches our client ID, signature is valid, not expired -> passes.
- The request is authenticated; our config says `.anyRequest().authenticated()` so `/hello` is allowed (no specific scope needed in this example).
- The controller method can get the JWT details. We inject `Jwt jwt` to get token claims easily. We respond with a hello message.

If a call comes in without a token or with an invalid token:

- Spring Security will throw an authentication exception and return 401 before hitting the controller.

If a call comes with a valid token but lacks a required scope for that endpoint:

- Spring’s authorization will throw access denied and return 403.

**Cross-Origin Resource Sharing (CORS):** To allow the React app (different origin) to call the API, enable CORS. One quick way in Spring Security config is:

```java
http.cors().and()... // enable Spring Boot CORS support with defaults
```

And define a `CorsConfigurationSource` bean to allow the specific origin:

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("http://localhost:3000"));  // front-end origin
    config.setAllowedMethods(List.of("GET","POST","PUT","DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    config.setExposedHeaders(List.of("WWW-Authenticate")); // if you want to expose any headers
    config.setAllowCredentials(true);
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    return source;
}
```

Without proper CORS, the browser will block the front-end’s request even if the token is valid, so this is important for local development and production (update the allowed origins to your production front-end URL).

**Using Azure Spring Boot Starter (alternative):** Instead of manually configuring, you could use Azure’s starter which simplifies some of this. For example, after including `spring-cloud-azure-starter-active-directory`, your `application.yml` might be:

```yaml
spring:
  cloud:
    azure:
      active-directory:
        tenant-id: <TenantID>
        client-id: <API-ClientID>
        client-secret: <API-Secret> # if API needs to call other APIs
        app-id-uri: api://<API-ClientID>
```

And then in your security config you might use Azure’s provided classes:

```java
http.apply(AadResourceServerHttpSecurityConfigurer.aadResourceServer()); ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=Exception%20))
```

This one-liner (from Azure SDK) sets up JWT validation with Azure AD defaults ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=http,)). By default it secures all API endpoints. You can still add `.authorizeHttpRequests` after that to customize. The advantage is Azure’s library will automatically handle the authority and audience validation using the provided `tenant-id` and `app-id-uri` ([Spring Boot Starter for Microsoft Entra developer's guide - Java on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/spring-boot-starter-for-azure-active-directory-developer-guide#protect-a-resource-serverapi#:~:text=spring.cloud.azure.active,URI%3E%60%20values%20described%20previously)). It also can handle multi-tenant scenarios by not hardcoding tenant if needed (though usually you specify one). The downside is adding another dependency, but it may provide extras like integration with Azure AD groups or roles easily.

**On-Behalf-Of Flow (advanced scenario):** If your Spring Boot API needed to call another downstream API (say, Microsoft Graph) using the user’s identity, you would implement OAuth2 On-Behalf-Of (OBO) flow. Azure AD’s OBO allows your API to exchange the incoming user’s access token for a new access token for another resource (with consented permissions). This requires your API app registration to be configured with permission to call that other API and use its **client secret** to request the token. The Azure spring starter has utilities for OBO, and without it, you’d manually call Azure AD’s token endpoint with grant_type `urn:ietf:params:oauth:grant-type:jwt-bearer` etc. This is beyond our current scope but worth noting for advanced systems where one API calls another on behalf of the user. Azure’s documentation has a sample for this ([The latest on Azure Active Directory integration](https://spring.io/blog/2021/01/13/the-latest-on-azure-active-directory-integration#:~:text=On%20Behalf,server)).

**Testing End-to-End:** Now, with React and Spring Boot set up, test the whole flow:

- Run Spring Boot on `localhost:8080`. Ensure it’s picking up the config (check logs – Spring will log something like “Configured OAuth2 Resource Server to secure with issuer ...”).
- Run the React dev server on `localhost:3000`.
- Open the app in a browser. Click Sign In. You should be redirected to Microsoft login, then back.
- Open developer console network tab and trigger the API call (if not automatic). You should see the request to `http://localhost:8080/your/api/endpoint` with status 200 and data returning (assuming your API is running and that endpoint exists and is annotated properly). If you see a CORS error, fix the CORS config. If you see 401, check the access token and Spring Boot logs – possibly audience or issuer mismatch (make sure tenant ID and client ID are correct in both React and Spring). If 403, likely a missing scope – ensure the token has the scope and the security config matches it.

**Conclusion:** The Spring Boot API now successfully validates Azure AD JWTs and authorizes requests based on scopes. We used Spring Security’s built-in resource server support to do heavy lifting (as recommended by Spring and Microsoft) rather than manually validating tokens. This completes the integration: the React SPA obtains a token from Azure AD and the Spring Boot API accepts it to secure resources.

---

By following this guide, you have:

- Registered Azure AD applications for your front-end and back-end,
- Configured redirect URIs and exposed an API with scopes,
- Secured your client with MSAL and your server with Spring Security,
- Implemented OAuth2 Authorization Code flow with PKCE and OpenID Connect in a robust manner,
- Applied security best practices (least privilege, secure secret handling, etc.),
- And set up your environment for deployment and maintenance.

This provides a solid, enterprise-grade authentication setup. Azure AD (now part of **Microsoft Entra ID**) will handle the identity and access management, letting you focus on your application’s functionality. Always keep security in mind: regularly update libraries, rotate secrets or use certificates, and monitor your system. With this in place, you can extend the solution (for example, adding role-based authorization with app roles or group claims, integrating with CIAM/B2C for external users, etc.) as needed, knowing the foundation is secure and well-structured. Happy coding!

**References:**

- Microsoft Identity Platform Documentation – App registrations and configuration ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=This%20type%20of%20app%20is,the%20widest%20set%20of%20customers)) ([Quickstart: Register and expose a web API - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis#:~:text=Scope%20name%20The%20name%20of,only)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=3,after%20you%20leave%20this%20page)) ([Quickstart: Register an app in the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app#:~:text=,after%20you%20leave%20this%20page))
- OAuth2 and OIDC specifications and Azure AD implementation guidelines ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=A%20redirect%20URI%2C%20or%20reply,specified%20in%20the%20login%20request)) ([Redirect URI (reply URL) best practices and limitations - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url#:~:text=For%20security%20reasons%2C%20the%20authentication,URLs%20configured%20for%20the%20application)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20pattern%20for%20acquiring%20tokens,access%20and)) ([Acquire a token to call a web API (single-page apps) - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-spa-acquire-token#:~:text=The%20silent%20token%20requests%20to,to%20acquire%20tokens))
- Spring Security Official Docs – OAuth2 Resource Server JWT configuration ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=jwt%3A%20issuer)) ([OAuth 2.0 Resource Server JWT :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html#:~:text=the%20,and%20subsequently%20validate%20incoming%20JWTs))
- Azure AD Best Practices – Managing secrets, redirect URIs, and permissions ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Protect%20and,and%20regularly%20rotate%20your%20credentials)) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20%20Make%20sure,permissions%2C%20see%20this%20permissions%20reference)) ([Best practices for the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/identity-platform-integration-checklist#security#:~:text=Image%3A%20checkbox%20DO%20NOT%20look,value%2C%20or%20attempt%20to%20parse)).
