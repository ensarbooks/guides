# Introduction to Azure AD B2C

Azure Active Directory B2C (Azure AD B2C) is a cloud-based **Customer Identity and Access Management (CIAM)** service for building consumer-facing applications. It provides identity as a service, allowing users to sign up, sign in, and manage their profiles in a secure, scalable way. Unlike regular Azure AD (for workforce identity), Azure AD B2C is designed for **external customers** and is a separate service built on the same technology ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20is%20a,spray%2C%20or%20brute%20force%20attacks)) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=Azure%20AD%20is%20built%20on,authentication%20needs%20of%20an%20app)). With Azure AD B2C, your application’s users can authenticate using **social accounts** (Google, Facebook, Microsoft, etc.), enterprise accounts, or local email accounts, all with **single sign-on (SSO)** across your applications ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Your%20customers%20can%20use%20their,to%20your%20applications%20and%20APIs)) ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=By%20serving%20as%20the%20central,up%20conversion)).

## Key Features of Azure AD B2C

- **Multiple Identity Providers**: Out of the box support for popular identity providers like **Google, Facebook, Microsoft Accounts**, Twitter (X), and any provider supporting OpenID Connect, OAuth2, or SAML ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=You%20can%20configure%20Azure%20AD,OpenID%20Connect%2C%20and%20SAML%20protocols)) ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=Azure%20AD%20B2C%20supports%20external,OpenID%20Connect%2C%20and%20SAML%20protocols)). This lets users log in with existing social or enterprise accounts, reducing friction.
- **Scalability and Security**: Azure AD B2C is highly scalable, capable of supporting millions of users and billions of authentications per day ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20is%20a,spray%2C%20or%20brute%20force%20attacks)). It automatically handles security threats such as DDoS attacks, password spray, and brute force attempts, so developers don’t need to build those protections from scratch ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20is%20a,spray%2C%20or%20brute%20force%20attacks)). **Multifactor authentication (MFA)** and threat detection are built-in features for enhanced security ([What is Azure AD B2C? - Petri IT Knowledgebase](https://petri.com/what-is-azure-ad-b2c/#:~:text=Use%20cases%20for%20Azure%20AD,validate%20secure%20transactions%20with)) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=Local%20add,that%20will%20contain%20the%20tenant)).
- **Standard Protocols & Tokens**: Supports industry standards like **OAuth 2.0, OpenID Connect (OIDC)**, and SAML for authentication flows ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Single%20sign,provided%20identity)) ([Technical and feature overview - Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/technical-overview#:~:text=Protocols%20and%20tokens)). Upon successful sign-in, Azure AD B2C issues **JWT security tokens** (ID token, Access token, Refresh token) that represent the user's identity and permissions ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=4.%20Upon%20successful%20sign,acquire%20a%20new%20access%20token)). These tokens can be used by your frontend and backend to authorize access to resources.
- **Custom Branding (White-label)**: Azure AD B2C allows full UI customization of the user experience. You can present a **branded sign-up or sign-in page** with custom HTML/CSS so that it seamlessly blends with your application's look and feel ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20is%20a,your%20web%20and%20mobile%20applications)). Every page (sign-up, sign-in, password reset, etc.) can be customized to provide a native-feeling experience to users.
- **Single Sign-On and Session Management**: Azure AD B2C acts as a central authentication authority for all your apps (web or mobile), enabling SSO across them. Once a user authenticates, they can access multiple related applications without re-authenticating, as long as the apps use the same B2C tenant ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=By%20serving%20as%20the%20central,up%20conversion)). Sessions are maintained via secure cookies in the user’s browser.
- **User Profile Management and Analytics**: It provides a directory to store user accounts and up to 100 custom attributes per user. You can collect profile data during registration or later (progressive profiling) and even integrate with external systems/CRM for storing user data ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20provides%20a,of%20truth%20for%20customer%20data)) ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20can%20facilitate,it%20sends%20to%20your%20application)). Azure AD B2C also offers analytics on sign-in activity and user behavior, helping you understand usage patterns ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=By%20serving%20as%20the%20central,up%20conversion)).
- **APIs and Custom Logic**: For advanced scenarios, Azure AD B2C can call your REST APIs during the authentication flow to apply custom business logic or integrate with external data sources. For example, you could call an API to validate a user-provided code, or to fetch loyalty program info during sign-in ([Technical and feature overview - Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/technical-overview#:~:text=You%20can%20integrate%20with%20a,with%20a%20RESTful%20service%20to)) ([Technical and feature overview - Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/technical-overview#:~:text=,user%27s%20identity%20within%20the%20application)). This extensibility is available via **Custom Policies** (described later) and **API connectors**.
- **Use Case Flexibility**: Azure AD B2C supports many application types – single-page apps (SPA), mobile apps, desktop apps, and server-side web apps. Any application that needs to **authenticate external users (customers, citizens, partners)** can use B2C for a robust identity solution. Typical use cases include consumer websites, e-commerce portals, citizen services portals, or multi-tenant SaaS platforms that want to offer social logins and self-service account management ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Any%20business%20or%20individual%20who,by%20IT%20administrators%20and%20developers)).

## Common Use Cases

- **Consumer Web Applications**: For example, an e-commerce site or a gaming platform can use Azure AD B2C to manage customer sign-ups and logins. Users can register with email or use their Facebook/Google account to log in, and the application offloads all password handling and user verification to Azure AD B2C.
- **Mobile Apps with Social Login**: A mobile app that wants quick onboarding can let users sign in with Google or Apple ID via Azure AD B2C. This provides a familiar login experience and eliminates the need to create yet another password.
- **Multi-Application Ecosystems**: If you have a suite of applications (web, mobile, API) that share the same user base, B2C provides a centralized identity service. Users sign in once and gain access to all applications (SSO). For instance, a company offering both a web portal and a REST API for customers can have a unified login through B2C, issuing tokens that work across the SPA and the API.
- **Applications Requiring Custom Identity Journeys**: Apps that need more than basic authentication — e.g., custom user onboarding steps, integration with legacy identity systems, conditional access policies, or user migration from an existing database — can leverage Azure AD B2C’s extensibility. Through custom policies, you can design complex sign-in flows, perform identity verification (like phone or email verification), and enforce custom attribute collection or validation during sign-up.
- **Security-Sensitive Services**: Apps in finance, healthcare, etc., where security and compliance are paramount, use B2C for its strong security posture. B2C supports **Multi-Factor Authentication** (e.g., SMS/OTP or authenticator app) and compliance standards. It can help meet regulations like GDPR by providing features for user consent, data export, and account deletion. (For instance, B2C has audit logs and can integrate with SIEM tools for monitoring sign-ins ([Monitor Azure AD B2C with Azure Monitor - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/azure-monitor#:~:text=Use%20Azure%20Monitor%20to%20route,gain%20insights%20into%20your%20environment)).)

**Note:** Azure AD B2C is typically used by developers and IT admins who need to add customer identity management to applications without building it from scratch. It allows you to focus on your app’s core functionality while outsourcing the heavy lifting of authentication, password security, and user management to a trusted cloud service.

---

# Azure AD B2C Setup

In this section, we’ll walk through setting up the Azure AD B2C tenant and configuration needed before coding our React application. This includes creating the B2C tenant, registering applications, defining user flows for common policies (like sign-up/sign-in), and preparing everything in the Azure portal.

## Creating an Azure AD B2C Tenant

**Azure AD B2C tenant** is a dedicated instance of the service that holds your user accounts, policies, and configurations. The first step is to create a tenant if you don’t have one already:

1. **Sign up for Azure**: You need an Azure subscription. If you don't have one, create a free Azure account ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=Prerequisites)).
2. **Create the Tenant**: In the [Azure Portal](https://portal.azure.com), search for **Azure AD B2C** and select **Create a resource** > **Azure Active Directory B2C** ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=4,page%2C%20select%20Create%20a%20resource)). Then choose **Create a new Azure AD B2C Tenant**.
3. **Provide Tenant Details**: Fill in the organization name (e.g., _Contoso B2C_), which will be the name of your B2C directory. Specify a **initial domain name** (this will be something like _contoso.b2c.onmicrosoft.com_ – it must be unique) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=7,directory%20page)). Select your country/region (this sets data residency; some regions support **data exclusivity** if needed) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=tenant.%20,your%20subscription%20from%20the%20list)). Choose your Azure subscription and resource group for billing linkage.
4. **Create and Link to Subscription**: Click **Create** to provision the tenant ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=8)). After creation, you should also **link your tenant to your Azure subscription** for billing (if not done automatically) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=,Favorite%20in%20the%20Azure%20portal)) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=You%20can%20link%20multiple%20Azure,B2C%20tenant%20to%20a%20subscription)). This ensures any usage (monthly active users beyond free tier, etc.) is associated with your subscription.
5. **Switch Directory**: Once created, switch to the new B2C directory in the portal (use the directory switcher at the top right). Now you will have a separate context where you can manage B2C settings ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=2,tenant%20that%20contains%20your%20subscription)).

**Tenant limits and considerations**: An Azure AD B2C tenant can contain up to 1.25 million objects (user accounts and app registrations) by default, expandable to 5 million by verifying a custom domain ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=,Learn%20how%20to%20%204)). You can create up to **20 B2C tenants per Azure subscription** (a limit enforce to prevent abuse) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=,limit%2C%20please%20contact%20Microsoft%20Support)). When the tenant is created, Azure automatically adds an application called `b2c-extensions-app` in it – this is used internally to store custom user attribute data, and you should not delete it ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=Note)).

## Registering Applications (App Registrations)

Next, you need to **register your applications** in the B2C tenant. In Azure AD B2C, **app registration** establishes a trust relationship between your application (such as the React SPA or a backend API) and the B2C identity provider. This provides a Client ID for your app and allows you to specify important settings like redirect URIs and permissions.

We will register two applications in B2C:

- The **React single-page application (SPA)** – for front-end client authentication.
- A **backend API** (if you have one) – to secure it and define scopes that the SPA can request. (If your app is purely front-end and calls no custom API, you may only need the SPA registration.)

**Register the SPA (React app):**

1. In your B2C tenant (Azure Portal, with the directory switched to the B2C tenant), go to **App Registrations** and click **New Registration**.
2. Enter a Name for the app (e.g., _ReactB2CClient_).
3. **Supported account types**: Choose **"Accounts in any identity provider or organizational directory (for authenticating users with user flows)"**. This setting is specific to B2C, allowing accounts from any configured identity provider ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=5,For%20example%2C%20spaapp1)).
4. **Redirect URI**: This is crucial. Select **Single-page application (SPA)** and enter the URI where your React app will run. During development, this is likely `http://localhost:3000` (if using webpack dev server) or similar. For production, it would be your deployed URL, e.g. `https://myapp.com` or a specific auth callback path if you use one (it must exactly match the redirect in code) ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=7,in%20the%20URL%20text%20box)). You can enter multiple redirect URIs if needed (e.g., one for dev, one for prod).
   - The redirect URI is where Azure AD B2C will **send authentication responses** (tokens or authorization codes) after a user completes the sign-in flow ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=The%20redirect%20URI%20is%20the,add%20the%20endpoint%20where%20your)). For SPAs using the OAuth2 Authorization Code flow with PKCE, B2C will redirect back to this URI with an authorization code.
   - **Important:** Redirect URIs must use **HTTPS** in production (localhost can be an exception) and are case-sensitive ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=The%20following%20restrictions%20apply%20to,redirect%20URIs)). Ensure the URI here exactly matches what your app expects.
5. **Permissions**: Under API permissions, Azure will by default include **openid** and **offline_access** for B2C. In the registration UI, you might see a checkbox to grant admin consent to these permissions – you can check it ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=8,and%20offline_access%20permissions%20check%20box)).
   - _Openid_ and _offline_access_ are standard scopes: **openid** allows user authentication and ID token issuance; **offline_access** allows issuing **refresh tokens** so the SPA can remain logged in without user interaction ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=OAuth%202,requiring%20interaction%20with%20those%20users)).
6. Click **Register**. After registration, note the **Application (client) ID** – a GUID. This will be used in your React app configuration to identify the B2C identity provider.

At this point, the SPA is registered as a **Public client** (since it's a browser app with no secret). Azure AD B2C knows about this application and will allow it to request tokens.

**[Optional] Register a Web API (for backend]:**

If your React app needs to call a protected backend API, you should also register that API in B2C:

1. Create another app registration, e.g., _MyApp-API_. For redirect URI, if it's a server API, you might not need to set a redirect (you can leave it blank or set to some URL if required for test).
2. Under **Expose an API** for the API registration, add a **Scope**. For example, define a scope name like `API.Access` or `API.Read`. This scope will represent a permission the API can grant to clients. Make sure to **save** and copy the full scope URI that gets generated (it will look like `https://<tenant-name>.onmicrosoft.com/<api-app-id-uri>/API.Access` if you set an Application ID URI for the API).
3. In the SPA app registration (ReactB2CClient), go to **API Permissions** and click **Add Permission**. Select **My APIs** and choose the API app you registered, then select the scope (permission) you defined (e.g., `API.Access`). Add it, and then **grant admin consent** for that permission so that users won’t be prompted for consent (in a B2C scenario, typically you as the developer pre-consent the API usage for your own app) ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=To%20enable%20your%20app%20to,the%20Azure%20AD%20B2C%20directory)) ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=,permissions%20to)).
4. Now the SPA is allowed to request an access token for the API’s scope.

**Important Settings in App Registrations:**

- In the SPA app's **Authentication** settings, ensure that the **Implicit grant** is **disabled** (unless you absolutely need it for legacy reasons). For MSAL.js 2.x (which we’ll use), implicit flow is not needed because we use the Authorization Code with PKCE flow ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=Note)). Implicit flow (granting tokens directly in the redirect without code) is older and less secure (no refresh tokens, tokens in URL). If you had to test user flows via the Azure portal’s “Run now”, you might temporarily enable implicit, but it’s recommended to keep it off in production ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=If%20your%20app%20uses%20MSAL,deploy%20your%20app%20to%20production)).
- If you use **Custom Domains** for your B2C tenant (so that the URLs are like `https://login.contoso.com` instead of `contoso.b2clogin.com`), you need to configure those, but that’s an advanced topic. Just note that if you set up a custom domain, your redirect URIs and app configurations should use that domain for consistency.

At this stage, we have our Azure AD B2C tenant ready and our application identities registered. Now we can configure user flows/policies for how users will sign up or sign in.

## Defining User Flows (Built-in Policies)

**User Flows** (also known as **Built-in policies**) are predefined authentication flows that manage user experience for common scenarios like sign-up, sign-in, profile editing, and password reset. Azure AD B2C provides these out of the box so you can configure an identity journey in minutes without writing code or XML. We will create a **Sign-up and Sign-in** user flow, which combines new user registration and returning user login in one experience (B2C will decide which path based on whether the user exists).

Steps to create a **Sign-up/Sign-in user flow**:

1. In the Azure AD B2C tenant portal, under **Policies**, select **User Flows** (or **User Journeys** in some UI) and click **+ New user flow** ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=3,and%20select%20Azure%20AD%20B2C)).
2. Choose the **Sign up and sign in** flow type (there are also separate templates for sign-up, sign-in, profile edit, password reset, etc., but the combined one is convenient) ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=5,and%20sign%20in%20user%20flow)). Choose the latest **Version** (generally "Recommended").
3. Give the user flow a **Name**. By convention, these names start with `B2C_1_` (for example: **B2C_1_signupsignin**). The name becomes part of the authority URL later.
4. **Identity providers**: Select which identity options to offer in this flow ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=8,at%20least%20one%20identity%20provider)).
   - Under **Local accounts**: choose Email or Phone signup if you want users to create accounts with email/phone and password. (Email is most common; phone can enable phone number authentication; or you can allow both email and phone.) If you choose "None" for local, then users _must_ use a social account to sign in (no local account option).
   - Under **Social identity providers**: you will see any external IdPs you have set up (e.g., Facebook, Google). Check the ones you want to allow. For a new tenant, you might first configure these IdPs under **Identity Providers** section (we cover this in the next section). If not configured yet, you can leave it and add later.
5. **User attributes and token claims**: Select which user information to collect during sign-up and which claims to include in the token. For example, you can collect **Display Name**, **Country**, etc., during sign-up. Attributes with checkmarks under "Collect" will be asked of the user (if not already existing). Attributes checked under "Return as claims" will be returned in the JWT token after authentication ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=signup%2C%20Phone%20signup%2C%20Phone%2FEmail%20signup%2C,Learn%20more)) ([User flows and custom policies in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview#:~:text=,Session%20management)). Common ones: Given Name, Surname, Email are usually collected/returned by default.
6. **Multifactor Authentication**: If you want MFA, expand that section. You can require users to perform MFA either **during registration or at sign-in**. Options typically include phone (SMS or phone call) for MFA. Enable it as required and choose whether to enforce it every time or only during certain risk events (if you have conditional access) ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=signup%2C%20Phone%20signup%2C%20Phone%2FEmail%20signup%2C,Learn%20more)). (Note: MFA in B2C can also be triggered via conditional access if you have premium licenses, see below.)
7. **Page customization**: Optionally, you can configure custom UI content for the pages in this flow (like using your own HTML templates for the sign-in page). If you plan to use the default Azure AD B2C pages for now, you can skip this here (you can always configure page customization later by editing the user flow).
8. **Create** the user flow.

Once created, you will see the user flow listed (e.g., _B2C_1_signupsignin_). You can click it to review settings or get the **Run now** endpoint for testing. The key detail is that this user flow defines an **endpoint/authority** for authentication:

For example:  
`https://<your-tenant-name>.b2clogin.com/<your-tenant-name>.onmicrosoft.com/B2C_1_signupsignin/v2.0/` … (and specific OIDC endpoints under that).

We will use this in our React app configuration as the authority for sign-in.

You may also want to create separate user flows for **Password Reset** and **Profile Edit**:

- **Password reset** flow (e.g., B2C_1_passwordreset): Allows users who forgot their password to reset it via email verification. You can integrate this by catching a specific error code in your app (AADB2C90118) and then triggering the password reset flow, or by providing a "Forgot Password" link that directly starts this flow ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Password%20reset%20error)).
- **Profile editing** flow (e.g., B2C_1_edit_profile): Allows logged-in users to update their profile attributes (name, etc.). You can invoke this from your app when the user clicks "Edit Profile".

For now, the **SignUpSignIn** flow is our primary focus since it covers initial authentication.

**Conditional Access (Advanced):** Azure AD B2C can also enforce **Conditional Access policies** if you have configured them (this requires Azure AD B2C Premium P1/P2 licenses). In the user flow setup, there’s an option "Enable conditional access policies" ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=9,Learn%20more)). Conditional Access can enforce MFA or block access based on risk, location, device compliance, etc., similar to enterprise Azure AD. This is advanced, but good to know if you have high security requirements.

## Custom Policies vs. User Flows (Overview)

Azure AD B2C offers **two ways to define user journeys**:

- **User Flows (built-in)** – which we just configured – are quick to set up through the portal and cover most common scenarios with configuration options ([User flows and custom policies in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview#:~:text=,policy%20editing%20experiences%20in%20minutes)).
- **Custom Policies** – which are fully configurable XML files that define every aspect of the identity experience ([User flows and custom policies in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview#:~:text=so%20you%20can%20create%20sign,policy%20editing%20experiences%20in%20minutes)) ([Azure Active Directory B2C custom policy overview | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/custom-policy-overview#:~:text=Custom%20policies%20are%20configuration%20files,to%20complete%20many%20different%20tasks)).

For an **advanced developer**, it's important to understand that **custom policies** exist and allow scenarios beyond the built-ins. Custom policies (also called Identity Experience Framework policies) can do things like:

- Integrate with **REST APIs** at various steps (for validation, data retrieval, etc.),
- Implement **complex account linkage** or custom multi-step journeys,
- Use **claims transformations** and custom validation on inputs,
- Support **external identity providers** that aren’t directly supported in the Azure portal UI,
- Provide more granular control over token contents, encryption, etc.

Custom policies are essentially a set of XML files (TrustFrameworkBase.xml, TrustFrameworkExtensions.xml, and relying party policy files) that you upload to the B2C tenant. They are powerful but also more complex to create and maintain (debugging can be more involved). Microsoft provides a **starter pack** with pre-built templates (for example: LocalAccounts, SocialAndLocalAccounts, with and without MFA) to get you started ([Azure Active Directory B2C custom policy overview | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/custom-policy-overview#:~:text=Custom%20policy%20starter%20pack)).

In this guide, we will focus on using **User Flows** for our implementation (since they are sufficient for many apps). We will cover Custom Policies in a later section (#5) for advanced scenarios like custom identity provider setups and custom journeys.

---

# React.js Application Setup

With Azure AD B2C configured, we can turn to the React application. Our goal is to integrate Azure AD B2C authentication into a React single-page app using **MSAL (Microsoft Authentication Library)**.

In this section, we’ll set up the project structure, install necessary dependencies, and establish best practices to prepare for implementing authentication. We assume the audience are advanced developers, so some basics (like how to create a React app) will be covered briefly for completeness, then we’ll dive into integration details.

## Project Structure and Tooling

**1. Initialize your React project** (if you don't have one already):

- You can use a tool like Create React App or Vite for quick setup. For example, using Create React App:
  ```bash
  npx create-react-app my-app
  cd my-app
  ```
  This will create a basic React application in the `my-app` directory with an entry point `src/index.js` and main component `src/App.js`. If you prefer TypeScript, you could do `npx create-react-app my-app --template typescript`. (If using Vite or Next.js, the setup will differ, but the integration of MSAL will be similar conceptually.)

**2. Install required dependencies** for Azure AD B2C auth:

- **MSAL for React and Browser**: Microsoft provides the `@azure/msal-react` package which is built on top of `@azure/msal-browser`. We'll use these to handle the auth flows in React. Install them via npm or yarn:
  ```bash
  npm install @azure/msal-browser @azure/msal-react
  ```
  This gives us MSAL React (which provides React context, hooks, and components for auth) and MSAL Browser (the core library handling browser OAuth flows) ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=Step%202%3A%20Install%20the%20dependencies)).
- **React Router** (if your app uses multiple pages/views): For our SPA, we likely want to protect certain routes. If not already added, install `react-router-dom`. MSAL React works with both React Router v5 and v6. The Microsoft sample currently uses v5, e.g., `npm install react-router-dom@5.3.3` ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=Install%20the%20react,command%20in%20your%20command%20shell)). For new projects, you may use React Router v6 which is the latest; MSAL React is compatible, but you'll implement route protection slightly differently (using hooks or wrapper components).
- (Optional) **UI library**: You may use a UI framework like Material-UI or Tailwind CSS for styling your app. This is not required for auth, but be aware when we integrate, our login button or form might use these. For example, you could install Material-UI (`@mui/material @emotion/react @emotion/styled`) or just plan to use Tailwind via CDN or configuration. In our guide, we will focus on auth logic, not CSS, but keep your UI framework in mind for integration.
- (Optional) **Bootstrap**: The Microsoft sample uses Bootstrap for quick styling ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=Install%20the%20Bootstrap%20for%20React,optional%2C%20for%20UI)). This is entirely optional and up to your preference.

**Project structure considerations**:

- **src/authConfig.js**: Create a module (e.g., `src/authConfig.js`) to hold configuration for MSAL (client ID, authority, etc.) ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=%2A%20src%2FauthConfig.js%20,tokens%2C%20and%20validate%20the%20tokens)). This keeps sensitive or config data in one place and separate from logic.
- **src/index.js(x)**: Your entry file will initialize MSAL and wrap the app in the necessary providers.
- **src/App.jsx**: Main app component. We will likely wrap our routes or main layout with MSAL's context provider here.
- **Auth Components**: We might create dedicated components or hooks for authentication status, e.g. a `<PrivateRoute>` component to protect routes, or use MSAL’s provided `<AuthenticatedTemplate>` and `<UnauthenticatedTemplate>` components.
- **UI Components**: e.g., `NavBar.js` to show login/logout buttons, and maybe placeholders for profile info when logged in, etc.

A possible structure:

```
my-app/
├── src/
│   ├── authConfig.js        # B2C configuration (client ID, policies, etc.)
│   ├── index.js             # App entry, MSAL Provider setup
│   ├── App.jsx              # App component, maybe sets up routes and layouts
│   ├── components/
│   │    ├── NavBar.jsx      # Navigation bar with sign-in/sign-out
│   │    ├── PrivateRoute.jsx# (optional) Helper for protected routing
│   │    └── ...other components
│   └── pages/
│        ├── Home.jsx        # Public or landing page
│        ├── Profile.jsx     # Example protected page showing user profile
│        └── ...other pages
└── ...
```

**Best Practices:**

- Keep configuration (client IDs, tenant name, policy names, API scopes) in a separate config file or in environment variables. Do not scatter them in your components.
- Do not include any **client secrets** in the React app – as a SPA, there is no secret (the app is public). All you need is the client ID and the sign-in policy/authority and scopes. The secrets (like an API's own secret or certificates) should only reside on secure backend if needed.
- Use **HTTPS** for local dev if possible, to closer mimic production and avoid any issues with cookies or redirects. (At least ensure your production will be HTTPS; B2C will refuse to redirect tokens to non-HTTPS URIs except for localhost).
- Plan for token storage: MSAL by default will store tokens in memory or sessionStorage. We'll discuss the implications in Security section, but as a best practice, we won't manually store tokens in localStorage where possible to minimize persistence of sensitive data ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=The%20choice%20between%20different%20storage,cached%20artifacts%20below%20for%20more)) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=We%20consider%20session%2Flocal%20storage%20secure,option%20instead)).
- Ensure your app is running on a **URL that is whitelisted in the B2C Redirect URIs**. If you run on localhost:3000 but only `http://localhost:5000` is registered, you’ll get a redirect_mismatch error (AADB2C90006) ([Error code reference - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/error-codes#:~:text=,web%20application%20%2C%20%206)). So keep those in sync as you develop.

## Integrating MSAL into the React App

Now we begin writing code to integrate Azure AD B2C into React. The MSAL library will handle the OAuth2 flow with Azure B2C endpoints. There are a few key steps:

1. Configure the MSAL **PublicClientApplication** instance with our B2C settings.
2. Wrap our app in the **MsalProvider** to provide the MSAL context to React components.
3. Use MSAL React components/hooks to initiate login, handle responses, and get tokens.
4. Protect routes or show/hide UI based on authentication state.

Let's go step-by-step:

**1. Configuration (authConfig.js):**

In **src/authConfig.js**, define the configuration object for MSAL. This includes:

- `auth.clientId`: The Application (Client) ID of your SPA registration in B2C.
- `auth.authority`: The authority URL of the B2C policy (which includes your tenant name and policy name).
- `auth.redirectUri`: The URL where MSAL will redirect back after login (must match what we registered).

For example:

```js
// src/authConfig.js
const B2C_TENANT_NAME = "<your-tenant-name>"; // e.g., contoso
const B2C_POLICY = "B2C_1_signupsignin"; // your user flow name
const B2C_DOMAIN = `${B2C_TENANT_NAME}.onmicrosoft.com`;

// The authority URL for B2C includes your tenant and policy:
export const b2cPolicies = {
  signUpSignIn: {
    authority: `https://${B2C_TENANT_NAME}.b2clogin.com/${B2C_DOMAIN}/${B2C_POLICY}`,
  },
  // (you could add other policies like password reset or edit profile here)
};

export const msalConfig = {
  auth: {
    clientId: "<your-client-id-guid>",
    authority: b2cPolicies.signUpSignIn.authority,
    redirectUri: "http://localhost:3000", // or your deployed site
    knownAuthorities: [`${B2C_TENANT_NAME}.b2clogin.com`],
    // knownAuthorities is used to specify trusted domains for B2C (to prevent phishing)
  },
  cache: {
    cacheLocation: "sessionStorage", // or "localStorage"
    storeAuthStateInCookie: false, // set to true if dealing with IE/Edge issues
  },
};

// You might also define the scopes for your API:
export const loginRequest = {
  scopes: ["openid", "offline_access"],
};
export const tokenRequest = {
  scopes: ["https://<your-tenant-name>.onmicrosoft.com/your-api/API.Access"],
  // replace with your API's scope URI if calling an API
};
```

This config object will be used to initialize MSAL. We include `openid` and `offline_access` in scopes by default (for ID token and refresh token). If we have a custom API, we prepare a `tokenRequest` with that API scope.

**2. Initialize MSAL and MsalProvider (index.js):**

In **src/index.js**, we'll import MSAL and set up the provider:

```jsx
// src/index.js
import React from "react";
import ReactDOM from "react-dom/client";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import App from "./App";
import { msalConfig } from "./authConfig";

const msalInstance = new PublicClientApplication(msalConfig);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <MsalProvider instance={msalInstance}>
    <App />
  </MsalProvider>
);
```

What this does:

- We create a `PublicClientApplication` with our config. This object (`msalInstance`) manages the authentication state, token cache, and all interactions with Azure AD B2C ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=,App%20instance%3D%7BmsalInstance%7D)).
- We wrap our `<App />` inside `<MsalProvider instance={msalInstance}>`. The `MsalProvider` is a context provider from MSAL React that will make the MSAL instance and authentication state available to all components in the app tree ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=,and%20its%20Pages%20child%20element)). Any component can then use hooks like `useMsal()` or components like `AuthenticatedTemplate` to access auth info.

It’s important that `MsalProvider` is high up (typically at root). Also, if you are using React Router, you might wrap the provider around the Router or vice versa depending on needs. For example, you could do:

```jsx
root.render(
  <BrowserRouter>
    <MsalProvider instance={msalInstance}>
      <App />
    </MsalProvider>
  </BrowserRouter>
);
```

This ensures routing and MSAL context are both available.

**3. App Component and Routing:**

In **App.jsx**, set up your routes and possibly UI layout. For example, using React Router v5:

```jsx
// App.jsx (assuming react-router-dom v5)
import React from "react";
import { Switch, Route } from "react-router-dom";
import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
} from "@azure/msal-react";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import NavBar from "./components/NavBar";

function App() {
  return (
    <div>
      <NavBar />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/profile" component={Profile} />
        {/* We will protect the Profile page in NavBar or using AuthenticatedTemplate */}
      </Switch>

      {/* Optionally, you can use AuthenticatedTemplate/UnauthenticatedTemplate to show different components or messages */}
      <AuthenticatedTemplate>
        {/* This content shows only when user is logged in */}
      </AuthenticatedTemplate>
      <UnauthenticatedTemplate>
        {/* This content shows only when user is NOT logged in */}
      </UnauthenticatedTemplate>
    </div>
  );
}
export default App;
```

If using React Router v6, you'd use `<Routes><Route ... /></Routes>` structure. The concept remains that certain routes (like `/profile`) require authentication.

**4. NavBar with Login/Logout:**

Create a component that shows a "Sign In" button when not signed in, and a "Sign Out" (and maybe user's name) when signed in. We can leverage MSAL React hooks:

```jsx
// components/NavBar.jsx
import React from "react";
import { useMsal, useIsAuthenticated } from "@azure/msal-react";

const NavBar = () => {
  const { instance, accounts } = useMsal();
  const isAuthenticated = useIsAuthenticated();

  const handleLogin = () => {
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error(e);
    });
  };

  const handleLogout = () => {
    instance.logoutRedirect().catch((e) => {
      console.error(e);
    });
  };

  const userName = accounts[0] && accounts[0].name; // MSAL stores account info after login

  return (
    <nav>
      {isAuthenticated ? (
        <div>
          <span>Welcome, {userName}!</span>
          <button onClick={handleLogout}>Sign Out</button>
        </div>
      ) : (
        <button onClick={handleLogin}>Sign In</button>
      )}
    </nav>
  );
};

export default NavBar;
```

Explanation:

- `useMsal()` gives us the MSAL instance and the array of signed-in accounts (for B2C, typically at most one account exists at a time) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=const%20LoginPage%20%3D%20%28%29%20%3D,%3D%20useMsal)).
- `useIsAuthenticated()` returns a boolean indicating if **any user** is currently signed in (i.e., a valid ID token is present in cache).
- If not authenticated, we render a **Sign In** button that triggers `instance.loginRedirect()`. This will start the redirect flow: it will navigate the browser to the Azure B2C sign-in page (constructed from the authority). We pass `loginRequest` which can include scopes for tokens we want (for example, if we need an access token for our API, we include that scope here) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=const%20initializeSignIn%20%3D%20%28%29%20%3D,loginRedirect%28%29%3B)). If we omit scopes, by default it will at least get an ID token; including API scopes will get an access token for those as well upon successful login ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=Microsoft%20has%20a%20tutorial%20on,must%20consent%20to%20when%20authenticating)).
- If authenticated, we show a welcome message (account info is available; the `name` claim is often in the ID token if you requested the profile scope or it's a default claim) and a **Sign Out** button. `logoutRedirect()` clears the cache and redirects to B2C to log out the user from the B2C session as well ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=Handling%20user%20signout)). We might also configure `postLogoutRedirectUri` in msalConfig if we want to redirect the user to a specific page after logout (otherwise, by default, MSAL will return them to the login page or the root) ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=We%20have%20a%20different%20method,then%20back%20into%20the%20app)).

**5. Handling the Redirect Response:**

When using redirect flow, after a user signs in on the B2C page, they will be redirected back to your app (to the redirectUri). At that point, MSAL needs to handle the URL that contains an authorization code (or tokens). The `MsalProvider` and `PublicClientApplication` are set up to handle this automatically:

- Under the hood, MSAL will parse the URL and exchange the authorization code for tokens (ID token, etc.) **in the background** (using a hidden iframe or via the redirect promise). This is why we don't see that in our code – MSAL’s **redirect handling** is automatic, as long as the app stays mounted.
- There is one thing to note: in older MSAL you had to call `handleRedirectPromise()` to process the redirect, but the MSAL React library does this for you internally when the provider is mounted. After processing, MSAL will store the tokens in its cache (in memory/sessionStorage as configured) ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=4.%20Upon%20successful%20sign,acquire%20a%20new%20access%20token)).
- Once processed, the `useIsAuthenticated` hook will flip to `true` and `accounts` will be populated, causing our components to re-render and show the logged-in state. This reactive model is very convenient.

**6. Protected Routes and Components:**

For pages that require login (say `/profile` route), you have a few options:

- Simply check `isAuthenticated` and conditionally render the content or redirect to home if not authenticated.
- Use MSAL’s `<AuthenticatedTemplate>` to wrap the protected component. `<AuthenticatedTemplate>` will render its children **only if** a user is authenticated ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=,src%2Fcomponents%2FPageLayout.jsx)). Conversely, `<UnauthenticatedTemplate>` renders only if no user is auth.
- Use a custom `PrivateRoute` component (common in React Router v5) that checks auth and redirects to login if not. With our approach, since login is a redirect to an external page, you might not do a redirect in the conventional sense (because the login page is not a route in our app but on B2C). Instead, if user is not authenticated and they try to access the protected page, you could trigger `loginRedirect()` automatically or show a message with a login button.

For example, using AuthenticatedTemplate:

```jsx
<Route path="/profile">
  <AuthenticatedTemplate>
    <Profile />
  </AuthenticatedTemplate>
  <UnauthenticatedTemplate>
    <div>Please sign in to view your profile.</div>
  </UnauthenticatedTemplate>
</Route>
```

However, note that if the user is not authenticated, the `<AuthenticatedTemplate>` will render nothing (so the route might appear blank). It might be better to handle at a higher level: e.g., in Profile component itself, if not authenticated, you call login or show a prompt.

**7. Testing the Login Flow:**

At this point, you can run your app (`npm start`) and click the "Sign In" button. What should happen:

- The browser will redirect to the Azure B2C sign-in page (you’ll see the URL change to yourtenant.b2clogin.com). The page will display the sign-in/sign-up UI (with options for email signup or social logins you enabled). It might show your custom branding if you configured any.
- Complete the sign-up or sign-in. For a new user, try creating an account; for a returning user, sign in with the credentials.
- After successful authentication, you should be redirected back to `http://localhost:3000` (or your redirectUri). The URL might have some query parameters or fragments momentarily as MSAL processes the token.
- MSAL will store the tokens and your app will re-render showing "Welcome, [User]!" and a Sign Out button (based on our NavBar logic). Congratulations, your React app is now authenticated against Azure AD B2C!

From here, we can move on to handling tokens (like calling an API with the access token) and other advanced features.

**Exercise:** _After completing the setup above, try adding a new component that displays the user's account information (e.g., their username or email). You can retrieve this from the `accounts[0]` object provided by MSAL (which contains user claims like username, object ID, etc.)._

---

# Authentication Implementation in React (Using Azure AD B2C)

Now that the basic integration is in place, let's dive deeper into the authentication flows and how to handle them securely in the React application. This section covers how the OAuth2 flow works with B2C, how to manage tokens and sessions on the client side, enabling multi-factor auth, and ensuring the auth process is robust.

## Understanding the Auth Flow (OIDC Authorization Code with PKCE)

Azure AD B2C uses **OpenID Connect** on top of OAuth2 for authentication. Our SPA uses the **authorization code flow with PKCE** (Proof Key for Code Exchange), which is the recommended approach for SPAs ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=Authorization%20code%20flow%20)) ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=To%20take%20advantage%20of%20this,js)). Here’s what happens step-by-step when a user signs in:

1. **User initiates sign-in** – e.g., by clicking the "Sign In" button in our React app, which calls `msalInstance.loginRedirect()` ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=const%20initializeSignIn%20%3D%20%28%29%20%3D,loginRedirect%28%29%3B)). MSAL constructs an authentication request to Azure AD B2C. This request includes:

   - The **authority** (our B2C endpoint with the policy, e.g., `.../B2C_1_signupsignin/v2.0`),
   - The **client ID** of our app,
   - The **redirect URI** to return to,
   - The requested **scopes** (openid, offline_access, and any extra like our API scope),
   - A randomly generated **PKCE code verifier** (and its hashed version, the code challenge),
   - A **state** parameter (to maintain session and prevent CSRF),
   - Possibly a **nonce** (to correlate the ID token).
     This is all handled by MSAL; we just invoked `loginRedirect()`.

2. **Redirect to Azure AD B2C** – The browser navigates to the Azure B2C tenant’s secure login page for our user flow. The URL includes the query params mentioned (client_id, scope, redirect_uri, etc.). If the user is not already signed in, they will see the sign-up/sign-in page we configured:

   - If it's their first time, they can sign up (enter email, create password, etc., or use a social login).
   - If returning, they sign in with existing credentials or via their social account.
   - Azure AD B2C handles verifying the password, or redirecting to the social provider (e.g., Google OAuth) if that is chosen ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=On%20the%20sign,for%20authentication%20with%20your%20application)). This can involve multiple steps (for example, if MFA is enabled, after password the user might get an OTP code).

3. **Token issuance (on Azure side)** – Once the user successfully authenticates and completes any additional steps (MFA, email verification, etc.), Azure AD B2C will issue an **authorization code** because we used code flow. This code is a short-lived one-time code.

4. **Redirect back with Authorization Code** – The browser is redirected to our React app’s redirect URI with the **authorization code** (typically in a query parameter `code=` if using standard, or MSAL might handle it via a hash). For example, we might see `http://localhost:3000/#code=XYZ...&state=...`. The `state` is used by MSAL to match the request and prevent CSRF.

5. **MSAL processes the code** – The MSAL library, upon the app loading this redirect URI, detects there's a code to be exchanged. It will **automatically exchange** the authorization code for tokens by making a hidden request to B2C's token endpoint ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=4.%20Upon%20successful%20sign,acquire%20a%20new%20access%20token)). It sends the code along with the PKCE code verifier, client ID, etc. (All of this is handled internally by `PublicClientApplication` when it sees the redirect response).

   Azure AD B2C validates the code and PKCE, and returns:

   - an **ID Token** (JWT) – contains user’s identity claims (name, emails, etc.) per OpenID Connect,
   - an **Access Token** (JWT) – if we requested any resource scope (like our API), this token grants access to that resource,
   - a **Refresh Token** – because we included `offline_access`, B2C issues a refresh token allowing the SPA to get new access tokens after the current ones expire, without user interaction ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=OAuth%202,requiring%20interaction%20with%20those%20users)).
     These tokens are returned to MSAL.

6. **MSAL caches the tokens** – MSAL stores the ID token and access token in its **token cache** (in memory, or in web storage depending on config). By default, MSAL.js v2 uses sessionStorage for SPA, meaning tokens persist for the session (tab) but not if the tab is closed ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=The%20choice%20between%20different%20storage,cached%20artifacts%20below%20for%20more)). It also stores the refresh token securely (note: refresh tokens for SPAs are also subject to certain limitations for security).
   MSAL now considers the user "logged in" and keeps track of the user account.

7. **App sees authenticated state** – After the redirect is handled, our React components (wrapped by MsalProvider) get updated context. The `useIsAuthenticated()` will return true, and `useMsal().accounts` will have the user’s account info. Our UI updates to show the user as signed in (welcome message, logout button, etc.). The app can now also call `acquireTokenSilent` to get access tokens for APIs as needed (likely the initial token is already acquired if requested).
8. **Subsequent token use** – The React app can call a protected API by attaching the access token in the `Authorization` header (we’ll cover this in the next section). If the access token expires, MSAL can use the refresh token to get a new one without requiring the user to log in again – this can happen behind the scenes, _silent_ to the user.
9. **Sign-out** – If the user clicks logout, we call `logoutRedirect()`. This clears the cache in MSAL (so no tokens in client storage) and redirects the user to Azure B2C’s logout endpoint. B2C will sign the user out of its session and finally redirect back to our app (to the postLogoutRedirectUri). At that point, our app should update to show them as logged out.

This flow ensures our app never directly handles the user's password – that is all on Azure AD B2C (or the social provider). We only ever see tokens. The use of authorization code + PKCE and refresh tokens allows long-lived sessions without exposing tokens in the URL or having a persistent secret in the SPA, aligning with OAuth best practices for SPAs ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=Authorization%20code%20flow%20)).

Diagrammatically, the flow is:

```
User -> [React App: clicks Login] -> [B2C: Sign-in page] -> (credentials) -> [B2C: issues auth code] -> [React App: receives code] -> [MSAL: exchanges code] -> [B2C: returns tokens] -> [React App: user logged in, tokens stored] -> [React App: accesses APIs with tokens]
```

## Secure Token Handling and Session Management

Now that we have tokens, proper handling on the client side is crucial:

- **Token Storage Location**: MSAL gives options for caching tokens in **memory, sessionStorage, or localStorage**. By default, it uses sessionStorage for SPAs, which is a good balance: tokens are not persisted if the tab is closed (which is more secure in case the data is left on a machine) but survive page reloads in the same tab ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=The%20choice%20between%20different%20storage,cached%20artifacts%20below%20for%20more)). Storing in **localStorage** would allow the user to open the app in a new tab and still be logged in without a fresh login (better UX) but introduces a higher risk if an attacker can run JS in the app (XSS vulnerability – they could potentially read localStorage) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=The%20choice%20between%20different%20storage,cached%20artifacts%20below%20for%20more)) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=We%20consider%20session%2Flocal%20storage%20secure,option%20instead)).
  - For advanced scenarios, MSAL can even encrypt tokens in localStorage (it uses AES-GCM encryption with a key stored in a session cookie to mitigate some risk) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=Starting%20in%20v4%2C%20if%20you,msal.cache.encryption)). But the general rule is: treat tokens in the browser as sensitive. If you have strong XSS protections, sessionStorage vs localStorage is less about security and more about user experience (persistence). Many developers stick with the default or memory for maximum safety.
  - **Recommendation**: Use sessionStorage (the default) or memory for token cache unless you explicitly need cross-tab persistence. And always guard your app against XSS attacks so that an attacker cannot inject script to steal tokens from storage ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=We%20consider%20session%2Flocal%20storage%20secure,option%20instead)).
- **Session Lifetime**: With B2C, there are a few "sessions" to consider:

  1. The **browser session with B2C** (B2C sets a cookie after you login, so if you go to the B2C login page again it knows you are already signed in and might not prompt for credentials).
  2. The **token session in the SPA** (how long the tokens in MSAL cache are valid).

  By default, ID tokens and access tokens in B2C might have lifetimes like 1 hour (this can be configured in B2C policies). The refresh token typically can last longer (days). MSAL will automatically use the refresh token to get a new access token when needed via `acquireTokenSilent()`. So a user can remain logged in for a long time without re-authenticating, as long as the refresh token is valid and the B2C session cookie is alive or refresh token is still accepted.

  If the user closes the browser (thus clearing sessionStorage and the session cookie is gone after some time), they may need to sign in again next time. However, B2C also supports "Keep me signed in" functionality in user flows which can prolong the Azure session.

- **Acquire Token Silently**: After initial login, whenever you need an access token (say to call an API), you should attempt to get it silently:

  ```js
  instance
    .acquireTokenSilent({ scopes: ["scope_uri"] })
    .then((response) => {
      const accessToken = response.accessToken;
      // call API with this token
    })
    .catch((error) => {
      if (error instanceof InteractionRequiredAuthError) {
        // This error means we need user interaction (e.g., login again or consent)
        instance.acquireTokenRedirect({ scopes: ["scope_uri"] });
      } else {
        console.error(error);
      }
    });
  ```

  MSAL will either return a cached token or use the refresh token to get a new one without bothering the user. If something prevents silent acquisition (e.g., the user revoked consent or the refresh token expired), we catch the error and can initiate an interactive flow (redirect or popup) again ([Using msal-react for React app authentication - LogRocket Blog](https://blog.logrocket.com/using-msal-react-authentication/#:~:text=We%20can%20initialize%20the%20authentication,thus%20preserving%20the%20current%20state)). In practice, for long-running apps, MSAL manages this well. Just ensure to request all needed scopes either at login or before calling the API, so that user consents to them.

- **Multi-tab scenario**: If you use memory or sessionStorage, each browser tab or window has its own MSAL state. Logging in one tab won’t automatically log in another. This is a security feature. If you want a smoother multi-tab experience, you might consider localStorage (with caution). Alternatively, you can implement a mechanism to share state (some advanced devs use BroadcastChannel API to broadcast login state to other tabs, or listen for storage events).
- **Logout and Cache Clearing**: When calling `logoutRedirect()`, MSAL will remove its cache entries (ID token, etc.) and redirect the user to B2C’s logout endpoint. B2C will clear its session cookie for that user. You should also clear any app state (e.g., Redux store data related to the user) on logout. After logout, the user should be like a fresh visitor. If they hit the app again, they might still have a refresh token in localStorage (if you stored it there, but if using sessionStorage it’s gone). Regardless, it's best to treat them as not authenticated and require login again.
- **Handling B2C-specific errors**: Sometimes, B2C might return an error after the redirect instead of a code (for example, if the user cancels the sign-in, or if they clicked "Forgot Password" which can be surfaced as an error code to trigger password reset). MSAL React will by default handle the typical ones. If using the redirect approach, the error might be in the URL and MSAL processes it. For instance, **AADB2C90118** is a code for "User clicked forgot password" in some flows. The MSAL library does not automatically handle launching the password reset flow; you have to catch this. The Microsoft samples show how to do it by checking the error in the redirect response and then calling `loginRedirect` with the password reset policy if that error is detected ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Password%20reset%20error)).
  - Advanced handling: MSAL has event callbacks (`msalInstance.addEventCallback`) where you can listen for login failure, etc., and inspect error codes. As an advanced dev, you might implement a handler to automatically trigger specific user flows (like password reset) or to display user-friendly messages.
- **Keep Alive and Inactivity**: B2C by itself doesn’t automatically log the user out of the SPA for inactivity. That is up to your app. If you require an auto-logout after X minutes of inactivity, you'd implement that by tracking user activity in the app and calling logout if timeout. Otherwise, the refresh token and session could keep them alive indefinitely (until refresh token expires or is revoked).

To summarize, **maintaining session** in the SPA is mostly handled by MSAL’s token cache and B2C’s cookies. The developer’s job is to ensure secure storage and to handle edge cases (like token expiration or required reauth) gracefully.

## Enabling and Handling Multi-Factor Authentication (MFA)

Azure AD B2C supports MFA in user flows and custom policies. Enabling MFA means that during sign-in or sign-up, the user must perform a second step (usually verifying a code sent to their phone or email).

In our **SignUpSignIn** user flow, we had an option to enable MFA (either **Optional** or **Required**). If you set it to **Required** for sign-in, then every sign-in the user will, after entering password, be prompted for a verification code (depending on methods allowed: typically SMS or phone call to a number they provide) ([Set up a sign-up and sign-in flow - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-sign-up-and-sign-in-policy#:~:text=signup%2C%20Phone%20signup%2C%20Phone%2FEmail%20signup%2C,Learn%20more)). If set to **Optional**, the user might be given the choice or you might enforce it via conditional access.

From the React app perspective:

- You do not need to write extra code to handle MFA. The **Azure B2C pages handle the MFA prompts** as part of the flow. It’s transparent to our app. Our app just sees a longer redirect time while the user completes MFA.
- When MFA is satisfied, the token issuance proceeds normally and the tokens we get are just like before, except they might have an MFA claim or strong authentication marker (not usually needed by the SPA to inspect).
- If the user cancels during MFA or fails it, B2C might return an error. For example, if user cancels the code entry, B2C could send an error code back (like AADB2C90091 for "user cancelled") ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=User%20canceled%20the%20operation)). MSAL might throw an error in that case, which you can catch and handle (perhaps treat as a login failure or give them another chance).
- If using **Conditional Access with MFA** (e.g., require MFA only for risky logins or certain locations), B2C will enforce that after the user enters password. Again, from the app’s view, it's just part of the redirect flow.

**Using Authenticator Apps**: B2C can also allow users to register an authenticator app (TOTP) or use email OTP as second factor, depending on user flow settings. With custom policies, you can be even more flexible. But regardless, it’s on the service side.

**Testing MFA**: If you enable MFA in the user flow, try logging in. After password, you should see a prompt to register a phone number and get a code. Ensure that works. After setup, subsequent logins will ask for the code. Our app will only complete login once the code is verified.

**Remembering MFA**: Azure AD B2C can "remember" the MFA for a specified number of days (configurable in user flow) so that the user isn't prompted every single time on the same device. This is something you can configure in the B2C policy (MFA settings). For instance, trust this device for 14 days, etc.

In summary, to **implement MFA**, enable it in B2C (either in user flow or via conditional access). The React app doesn't require code changes – just ensure the user flow is set to enforce MFA. The UX is handled by B2C's hosted pages. As an advanced scenario, if you wanted to do a completely custom MFA UX (e.g., custom policy invoking an API for phone verification), that would be part of custom policy and beyond the scope of front-end code.

**Note**: If you want to indicate in your UI that MFA is required or provide any specific messaging, you could do so around the login initiation. But generally, the user will see the message on B2C pages anyway.

---

# Custom Policies and External Identity Providers

Up to now, we used **Built-in User Flows** for authentication which cover many scenarios. However, advanced developers often need more flexibility than user flows provide. This is where **Custom Policies** come in. Additionally, integrating various external identity providers (social logins, enterprise logins) might require either simple configuration (for supported IdPs) or custom policies (for unsupported or complex scenarios).

## Custom Policies in Azure AD B2C

**Custom Policies** allow you to define completely custom user journeys by writing XML policy files. They leverage the **Identity Experience Framework (IEF)** under the hood of B2C. With custom policies, you can orchestrate identity experiences step by step: from user input, validation, federation to other IdPs, token issuance, etc. They are useful for scenarios like:

- Using identity providers that aren't directly supported in the Azure portal (for example, an OAuth2 IdP not listed, or a custom OIDC identity).
- Customizing the UI beyond what page templates allow, or hosting your own UI that interacts with B2C via REST APIs.
- Complex verifications: e.g., require user to verify an email via a code, then input additional info, call a REST API to validate that info, all in one flow.
- **Linking accounts**: e.g., allow a user to sign in with Google and link it to an existing local account so they can use either method for the same profile (requires custom policy logic to detect and merge accounts).
- Conditional logic: e.g., different behavior based on user attributes (maybe old users go through a migration process, new users go through normal sign-up).
- Integration with external systems: e.g., after sign-up, call a REST API to subscribe the user to a mailing list or to record something in CRM ([Technical and feature overview - Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/technical-overview#:~:text=You%20can%20integrate%20with%20a,with%20a%20RESTful%20service%20to)) ([Technical and feature overview - Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/technical-overview#:~:text=,permissions%2C%20audit%20databases%2C%20and%20more)).

**How Custom Policies Work**:

- They are defined as XML files. Key elements in the policy XML include:
  - **Claims schema**: define the claim types (pieces of data) that will be used (emails, names, custom attributes, etc.).
  - **User Journeys**: the high-level sequence of orchestration steps for an authentication flow.
  - **Technical Profiles**: the building blocks of steps – each technical profile can do things like interact with an IdP, validate input, issue tokens, call REST API, etc.
  - **Claims Transformations**: functions to manipulate or validate claims (e.g., regex checks, string concat, etc.).
  - **Content Definitions**: references to UI content (like which HTML page to show for a step).
  - **Relying Party policy**: the final policy that ties a user journey to an endpoint that the relying party (your app) uses.
- Microsoft provides a **starter pack** on GitHub with base policies for common scenarios ([Azure Active Directory B2C custom policy overview | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/custom-policy-overview#:~:text=Custom%20policy%20starter%20pack)). Typically, you pick a base (like SocialAndLocalAccounts) and then create an extension policy file where you make changes.

**Using a Custom Policy**:

- You upload the policy files in the Azure Portal (under Identity Experience Framework menu) or via Azure CLI/PowerShell.
- Once uploaded and enabled, each custom policy behaves similar to a user flow: it has a name and an endpoint (usually the policy ID becomes part of the authority URL).
- Your application can initiate the custom policy by using its name in the authority (just like we used B2C_1_signupsignin, you might use e.g., B2C_1A_CustomSignup).
- Everything else from app perspective is the same (it’s just an authority issuing tokens). The differences are in what happens on the B2C side.

**Example scenario**: Suppose you need to allow users to sign in with their GitHub account. Azure AD B2C does not list GitHub as a built-in IdP in the portal (at the time of writing). However, since GitHub supports OAuth2, you can add it via a custom policy. You'd create technical profiles for GitHub’s OAuth endpoints, specify how to get user info from GitHub, and then include that in your user journey. Then your policy could offer "GitHub" as an option on the sign-in page along with other providers.

Another example: Account linking – maybe a user signed up with email/password, later they want to also connect their Google account to the same login. A custom journey can handle that by, say, letting an authenticated user add a social login to their account (this involves reading the existing account, linking identities, etc., all doable in custom policy code). Microsoft has sample custom policies for account linkage ([Azure AD B2C account linkage - GitHub](https://github.com/azure-ad-b2c/samples/blob/master/policies/account-linkage/Readme.md#:~:text=Azure%20AD%20B2C%20account%20linkage,such%20as%20Facebook%20or%20AAD)).

**Complexity Warning**: Custom policies are powerful but can be complex and time-consuming to debug. Microsoft docs and community samples are essential resources. For advanced devs, consider using custom policies only if user flows cannot meet your requirements ([User flows and custom policies in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview#:~:text=Most%20of%20the%20common%20identity,full%20flexibility%20of%20custom%20policies)). Always start from the starter pack and modify; writing one from scratch is not recommended.

**Debugging custom policies**: Azure AD B2C provides logging via **Application Insights** for custom policy execution. You can enable it to trace each step of the policy and see errors in detail (like which technical profile failed) ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Troubleshooting%20with%20Application%20Insights)) ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=To%20diagnose%20problems%20with%20your,It)). There's also a Visual Studio Code extension that helps view the log traces to debug custom policies ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=new%20logs%20in%20Application%20Insights,is)).

For our React implementation, if we decide to use a custom policy instead of the built-in user flow:

- We would change the `authority` in `authConfig.js` to the custom policy’s name.
- Possibly adjust scopes or claims if our custom policy returns different things.
- The app code remains mostly the same; it's the service side that changed.

## Integrating External Identity Providers (Social Logins & Enterprise)

Azure AD B2C’s big advantage is easy integration of external identity providers. You can allow users to sign in with Google, Facebook, Microsoft accounts, LinkedIn, etc., without much custom code.

**Using built-in support (via User Flows)**:
Azure AD B2C directly supports many providers:

- Microsoft Account (MSA), Google, Facebook, LinkedIn, Twitter (now X), Amazon, GitHub, etc.
- Any OAuth2 or OpenID Connect provider (as a "generic" provider) – you provide the authorization and token endpoint URLs and mapping of claims.
- SAML identity providers (B2C can be a SAML SP to an IdP).
- Azure AD (multi-tenant or single-tenant) – this allows users from other Azure AD (work/school accounts) to log in.

To add, say, **Google** login:

1. Go to **Identity Providers** in B2C tenant settings.
2. Select Google (built-in template).
3. It will ask for a **Client ID** and **Client Secret** – these you obtain by creating credentials in Google Developers Console (OAuth 2.0 credential for a Web Application). You also specify the authorized redirect URI there, which would be in the form: `https://<yourtenant>.b2clogin.com/<yourtenant>.onmicrosoft.com/oauth2/authresp` ([Set up sign-up and sign-in with a Facebook account - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/identity-provider-facebook#:~:text=11,it%20On%20to%20make%20the)) (this is a generic callback in B2C that handles responses from IdPs).
4. Once you save the Google IdP in B2C, you can include it in a user flow. For instance, in the SignUpSignIn flow, check "Google" under Social Identity Providers.
5. Now, when users go to sign-in, they will see a "Sign in with Google" button. If they click it, B2C will redirect them to Google, do the OAuth dance, and back to B2C, then to your app. To the React app, it's seamless – it just receives tokens like any other login.

This process is similar for Facebook, Microsoft, etc., with different steps to create the app in each provider's developer portal and obtaining keys:

- **Facebook**: Create a Facebook Developer app, get App ID and App Secret, add Facebook as IdP in B2C with those ([Set up sign-up and sign-in with a Facebook account - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/identity-provider-facebook#:~:text=6.%20Select%20Settings%20,of%20Service%20URL%2C%20for%20example)) ([Set up sign-up and sign-in with a Facebook account - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/identity-provider-facebook#:~:text=4,App%20Secret%20that%20you%20recorded)). Also add B2C's auth callback URL in the Facebook app settings ([Set up sign-up and sign-in with a Facebook account - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/identity-provider-facebook#:~:text=11,it%20On%20to%20make%20the)).
- **Microsoft (Azure AD or Microsoft Account)**: There are options for Microsoft Account (personal MSA accounts) or Azure AD (work/school). For Azure AD, you might choose multi-tenant if you want any org to login, or single-tenant if only a specific Azure AD tenant's users. You would supply the client ID/secret of an app registered in that Azure AD.
- **Others**: Most OAuth/OIDC providers follow the same pattern – register app on provider's side -> configure IdP in B2C with the keys -> include in user flow.

**Custom Identity Providers via Custom Policy**:
If a desired IdP is not directly listed, B2C might not have a turn-key setup in the portal. You can often use the "Generic OpenID Connect" option in the portal if it’s OIDC. If it's a pure OAuth2 (not OIDC, e.g., Twitter which uses OAuth1.0a or an older OAuth2 that doesn’t supply OIDC metadata), you may need a custom policy. For example, **Twitter** (now X) was historically OAuth1, which required a custom policy. However, as of now B2C lists "X (Twitter)" as supported ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=You%20can%20configure%20Azure%20AD,OpenID%20Connect%2C%20and%20SAML%20protocols)), meaning they have a built-in approach.

**Linking Multiple Providers**:
Azure AD B2C can allow a user to sign up with one provider and later sign in with another if emails match, but out-of-the-box, those would be separate accounts unless you implement account linkage. By default:

- If a user signs up with email/password and also tries to sign in with a Google account of the same email, B2C will treat them as different accounts (because one is local, one is social).
- If you want a unified account, you need custom policy logic to link them. That might involve during sign-in, if the email matches an existing local account, prompt to link, etc. This is advanced and requires writing a custom policy or using a sample from Microsoft’s repository (they have an **account linkage** sample custom policy).

For our React app, enabling social providers doesn't change the React code. The only thing you might do is:

- Possibly display the different sign-in options on a custom page if you decide to embed B2C in an iframe or use a self-rendered UI. However, Microsoft strongly encourages using the hosted pages for security reasons.
- If using **MSAL’s loginRedirect** from React, by default it goes to the B2C page which shows all buttons. You can actually specify a hint to directly go to a specific IdP if you wanted (like skipping the B2C selection page and directly redirecting to Google). This can be done by adding a query parameter `&domain_hint=google.com` or `&idpHint=Google` depending on configuration ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=On%20the%20sign,for%20authentication%20with%20your%20application)). MSAL allows passing an `authority` that points directly to an IdP as well. But this is optional. If not specified, user will see all options and choose.

**Steps to test**:
After adding, for example, Facebook as above (with App ID/Secret):

- On the B2C sign in page, click "Facebook". It will redirect to Facebook’s OAuth. Sign in with Facebook. The first time, Facebook will ask you to consent to share info with the B2C app (like your email, profile pic).
- After consenting, it goes back to B2C, perhaps asks to create a username (if you configured local accounts as well, sometimes B2C might link a new social account to a local account by asking for an email; but typically B2C uses the social account's email as the account ID).
- Then you get into the app as a logged-in user. In your tokens, you will see claims like identity provider (it might have `idp: Facebook` in the token to indicate the source).
- The React app doesn’t need to care _which_ provider was used; it just knows the user is authenticated.

**External IdP error handling**:
If the user cancels on the external provider’s page, B2C will get an error and translate it to an error code back to your app (like AADB2C90273 if user cancels at IdP login) ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=,Learn%20more%20about%20%207)). MSAL might throw it as an error on redirect. You should handle these gracefully (maybe treat as cancelled login attempt, show a message or nothing). Typically, the user will just remain on the login page.

**B2C as Identity Provider for others**:
Not exactly our scope, but worth noting: You can also use Azure AD B2C as an IdP for other apps (SAML or OIDC). For instance, B2C can be used to sign into a Salesforce app via SAML. That is outside our direct implementation, but showcases the flexibility.

**Practical tip**: Always test each identity provider integration thoroughly. Each has its quirks (Facebook requires https redirect URIs unless localhost, Google requires enabling the API, etc.). Azure B2C documentation has specific guides for each provider (we saw the Facebook one for example) ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=You%20can%20configure%20Azure%20AD,OpenID%20Connect%2C%20and%20SAML%20protocols)) ([Add an identity provider - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/add-identity-provider#:~:text=You%20can%20add%20identity%20providers,providers%20to%20your%20%203)).

**Exercise:** _If you have enabled a social login (e.g., Google), test signing in with it. Then test signing in with a local account. Observe the user flow behavior. For a challenge, try enabling **Microsoft Account** login and see if you can get that working too. Check the ID token contents for `idp` claim to see which provider was used._

---

# Security Best Practices

Implementing authentication brings a lot of responsibility to maintain security. Azure AD B2C provides a secure backend, but how you use it in your React app and overall architecture matters. Here are important security best practices for an advanced implementation:

## Secure Handling of Tokens

- **Do Not Manually Persist Tokens in Insecure Storage**: Avoid writing code that stores tokens in plain localStorage, cookies, or other persistent storage with broad access. MSAL’s default in-memory/session storage approach is designed to mitigate token theft via XSS ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=The%20choice%20between%20different%20storage,cached%20artifacts%20below%20for%20more)) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=We%20consider%20session%2Flocal%20storage%20secure,option%20instead)). LocalStorage is vulnerable to JavaScript injection attacks – if an attacker can run script in your SPA (via XSS), they could retrieve tokens. If you must use localStorage (for multi-tab support), ensure your app is as hardened as possible against XSS (use CSP headers, input sanitization, etc.) ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=We%20consider%20session%2Flocal%20storage%20secure,option%20instead)). As MSAL docs say, **the real solution is preventing XSS** because if an attacker can run code, they could also just call the MSAL APIs to get a token anyway ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=,to%20XSS%20attacks%20see%20below)). Use frameworks and security libraries to sanitize any HTML if you render user input, and avoid `dangerouslySetInnerHTML` in React unless necessary.
- **Use HTTPS Everywhere**: Always host your app over HTTPS in production. The redirect URI must be HTTPS (except for localhost dev) ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=The%20following%20restrictions%20apply%20to,redirect%20URIs)). HTTPS ensures tokens and user data are not intercepted in transit. If you're calling APIs, ensure those calls are also HTTPS.
- **Configure CORS properly on your backend**: If your React app calls a custom API with the access token, that API should allow requests from your front-end’s origin (and not from random sites). This prevents other sites from silently using a logged-in session from a user’s browser to call your API (CSRF protection at the API level).
- **Use the Auth Code + PKCE flow**: We are using MSAL which by default uses PKCE for SPA. This is more secure than implicit flow because the tokens are not exposed in the URL and a stolen authorization code cannot be exchanged without the code verifier. The PKCE code is handled by MSAL internally, but it's good to know this is protecting your flow ([Register a single-page app in Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-register-spa#:~:text=Authorization%20code%20flow%20)).
- **Do not expose sensitive data in tokens**: When configuring what claims come in ID or Access tokens, stick to non-sensitive info. For example, it’s fine to have user’s name or an ID, but don’t put something like a password or security answers in a token. While tokens are meant to be read by your app or API, they can potentially be decoded by the client. The JWTs in a SPA are not 100% secret because the front-end has them. So only include what’s necessary.
- **Validate tokens on the server**: We’ll discuss this in backend, but ensure any token presented to your backend is validated (signature, issuer, audience, etc.). Don’t assume a token is valid just because it "looks like" a JWT. Always verify it using the Microsoft-provided public keys for your B2C tenant.
- **Avoid storing Refresh Tokens long-term on the client**: B2C’s refresh tokens for SPAs are already limited in scope and lifetime. MSAL will keep it in memory or session. You typically don't need to do anything special with refresh tokens. Just be cautious that if you were to persist MSAL’s cache to localStorage, that includes the refresh token. The compromise of a refresh token is more sensitive because it could potentially be used to get new access tokens for a longer period. MSAL’s encryption of cache in localStorage in v4 can mitigate persistence risk ([microsoft-authentication-library-for-js/lib/msal-browser/docs/caching.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/caching.md#:~:text=Starting%20in%20v4%2C%20if%20you,msal.cache.encryption)).
- **Logout and token revocation**: B2C doesn't provide a direct token revocation endpoint for SPAs (the refresh token can be revoked behind the scenes by B2C if user resets password or an admin disables account). But when a user logs out, B2C will invalidate the session cookie. If you want to be extra sure, you could enforce re-authentication by using the `'prompt': 'login'` parameter in login requests for sensitive operations (which forces user to enter credentials again even if they have a session).
- **Idle Timeout**: If your app has a requirement that after e.g. 15 minutes of inactivity the user should re-authenticate, implement that in the app by tracking user events. You might call `logoutRedirect()` after timeout, or better, redirect them to a session-expired page where they can click login again (which will use the existing Azure session or ask for login if session expired).

## Mitigating Common Threats

- **Cross-Site Scripting (XSS)**: This is the top threat for SPAs. If an attacker can inject script into your app (via a vulnerability), they could hijack the session or tokens. Use React’s intrinsic protections (it escapes content by default). Any time you use dangerouslySetInnerHTML or render user-provided content, be very careful. Consider using a Content Security Policy (CSP) header to restrict script sources and disallow inline scripts. Also, libraries like DOMPurify can sanitize HTML if you need to render it. MSAL itself is robust, but it can't prevent your code from XSS.
- **Cross-Site Request Forgery (CSRF)**: Our app mostly makes API calls using tokens in Authorization header (bearer tokens). CSRF is less of an issue for token-based auth than cookie-based auth, because an attacker’s site cannot easily steal your token and include it. However, CSRF could be an issue if your SPA calls some legacy endpoint that uses cookies. In that case, standard CSRF mitigations apply (anti-CSRF tokens). For our scenario, MSAL uses `state` in OAuth flow to protect the auth request from CSRF (so malicious sites can't inject responses).
- **Clickjacking**: Since our app might not have traditional login form (we redirect to B2C), clickjacking risk is lower. But you might still set `X-Frame-Options: DENY` or `Content-Security-Policy: frame-ancestors 'none'` on your app to prevent it being framed. Also note, the B2C pages themselves send CSP headers to avoid being framed (to prevent UI hijacking).
- **Password complexity and brute force**: Offloaded to Azure B2C. Azure AD B2C has strong password policies and lockout mechanisms, and Smart Detection for brute force or leaked credentials. As devs, we rely on those features (which is good - B2C is highly resilient to password attacks ([What is Azure Active Directory B2C? | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/overview#:~:text=Azure%20AD%20B2C%20is%20a,spray%2C%20or%20brute%20force%20attacks))). If you allow social logins, those providers handle their own security (and B2C will enforce MFA if configured regardless of IdP, up to a point).
- **Data Privacy (GDPR)**: If applicable, make sure to respect user data privacy. B2C allows users to retrieve and delete their data (there are APIs or through your app you can implement an account deletion which calls B2C Graph API to delete the account). Also, B2C can add a consent page if needed (custom policy) to ask users to agree to terms. If you route logs to external systems, be mindful (Azure warns that B2C logs contain personal data, so handle accordingly) ([Monitor Azure AD B2C with Azure Monitor - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/azure-monitor#:~:text=When%20you%20plan%20to%20transfer,appropriate%20technical%20or%20organizational%20measures)).
- **Monitoring and Alerts**: As part of security, monitor unusual sign-in activity. Azure AD B2C can send logs to Azure Monitor or Sentinel for analysis ([Monitor Azure AD B2C with Azure Monitor - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/azure-monitor#:~:text=Use%20Azure%20Monitor%20to%20route,gain%20insights%20into%20your%20environment)). For example, monitor for many failed sign-ins, or for tokens being used from unexpected locations (though that might be more Azure AD than B2C feature set; B2C is a bit limited in built-in risk analysis compared to enterprise AD).

## Compliance and Governance

- **Compliance Certifications**: Azure AD B2C is hosted on Azure, which complies with many standards (ISO, SOC, GDPR, etc.). If your app is in a regulated industry, you might need B2C’s documentation on compliance. Ensure you use features like data residency (select a region or use the **GoLocal** options if needed – e.g., store data in EU data centers for GDPR, or US only, etc.) ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=tenant.%20,your%20subscription%20from%20the%20list)).
- **User Consent and Privacy Policy**: When integrating social providers like Facebook or Google, you also have to adhere to their platform policies. E.g., Facebook requires you to have a privacy policy URL (which you input in the Facebook app settings) ([Set up sign-up and sign-in with a Facebook account - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/identity-provider-facebook#:~:text=important%20security%20credential,that%20their%20data%20be%20deleted)). Make sure your application has those pages (privacy policy, terms of service) because users might see them via the social login consent screens.
- **Admin accounts**: Protect your Azure AD B2C admin accounts. Use MFA on your Azure subscription login to not let someone maliciously alter your B2C settings.
- **Testing**: Regularly pen-test your application or use static analysis (linters) to catch any insecure code patterns.

In short, while Azure AD B2C gives you a secure auth foundation, you must use it correctly. Follow the principle of **least privilege** (request only the minimal scopes needed), and **defense in depth** (secure the client, the transport, the backend). Keep libraries up to date (MSAL updates often include improvements or fixes). And always assume any token or user data on the client can potentially be seen by the user or a malicious script, so handle accordingly.

---

# Debugging and Troubleshooting

Even with a solid setup, you might encounter issues during development or production. This section covers common problems and how to troubleshoot them in the context of Azure AD B2C and React.

## Common Issues and Error Codes

**Misconfiguration Errors**: These usually surface as error codes starting with `AADB2C` when the redirect back from B2C happens. Here are a few common ones:

- `AADB2C90006` or `AADB2C90007`: These indicate an issue with the redirect URI. _90006_ says the redirect URI provided in the request is not registered for the client ([Error code reference - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/error-codes#:~:text=%60AADB2C90002%60%20The%20CORS%20resource%20%27,6%20Sending)). _90007_ says the app has no redirect URIs registered ([Error code reference - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/error-codes#:~:text=authentication%20requests%20%20,request%20does%20not%20match%20client)). Solution: Double-check the **redirectUri** in your MSAL config matches exactly one of the Redirect URIs in the app registration. Also ensure you used the correct **application (client) ID** and tenant in your config. Even a trailing slash difference can cause this.
- `AADB2C90008`: The request does not contain a client ID. This would be unusual coming from MSAL (it always sends one), but it could happen if, say, the authority or config was wrong. Ensure the `clientId` is correctly set in msalConfig.
- `AADB2C90010`: Scope not provided. Make sure you requested at least "openid" or some scope. MSAL should include openid by default if you call `loginRedirect` without scopes, but if you customized something, keep it in mind.
- `AADB2C90011`: The client ID in the request does not match the one in the policy. This can occur if you have a custom policy that is tied to a specific client, or if you accidentally used the wrong policy in the URL. Usually not an issue with user flows.
- `AADB2C90012`: The scope provided is not supported ([Error code reference - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/error-codes#:~:text=%60AADB2C90011%60%20The%20client%20ID%20%27,does%20not%20match%20the)). Could mean you requested a scope that doesn't exist or wasn't correctly configured (e.g., a typo in the API scope, or forgetting to expose the API and grant permissions). Check the spelling and GUIDs.
- `AADB2C90118`: **Forgot password** error. This one is important – it’s not a misconfig, but a **signal**. This code is returned when a user clicks "Forgot your password?" on a sign-in page that is _not_ configured to handle password resets in-line ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Password%20reset%20error)). In older B2C user flows, the recommended approach was to catch this error in the app and then trigger the password reset flow. In MSAL, this can be caught in the redirect promise. The fix is either:
  - Use the built-in **Combined SignIn/SignUp** page with _self-service password reset enabled_, so that the "Forgot Password" link internally handles the reset ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Password%20reset%20error)) (no error thrown).
  - Or catch AADB2C90118 error and call `loginRedirect()` again but with the authority set to your password reset user flow. MSAL React sample does this: e.g.,
    ```js
    if (error.errorCode === "AADB2C90118") {
      const resetPasswordAuthority = b2cPolicies.resetPassword.authority;
      instance.loginRedirect({ authority: resetPasswordAuthority, scopes: [] });
    }
    ```
    After password reset completes, B2C will redirect with either a success (new password set, possibly an ID token if configured) or back to sign-in.
- `AADB2C90091`: User canceled an operation. This can happen if user closes the window or clicks cancel on a prompt (like cancel on forgot password, or cancel on a consent screen). It's generally an informational code. You might handle it by simply treating it as a no-op (user decided not to log in).
- `AADB2C90273`: User canceled at the identity provider selection or during a social login (like user hit "Cancel" on the Google consent screen) ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=completes,7%20error%20codes%20Azure%20Active)). Similar to above, you can treat it as a canceled login attempt.

**MSAL Library Errors**: These include things like timeouts or network issues:

- If MSAL cannot reach the B2C endpoints (network down, wrong authority URL), it will throw. Check console/network. Ensure no ad-blockers are interfering (some ad-block might block Microsoft domains).
- `InteractionRequiredAuthError`: This is thrown by `acquireTokenSilent` when it can't silently get a token (maybe no cached token or requires user interaction such as consent). If you see this in console, it might be expected (the library uses it to know when to fall back to interactive login). In your code, handle it by triggering `loginRedirect` or similar.

**UI and UX issues**:

- The login popup/redirect might not do anything if MSAL is not configured right. For instance, if you forgot to wrap in MsalProvider or you don't call the login function on button click properly. Use console.logs or MSAL's own logging to see if the function was invoked.
- If using popup (`loginPopup`), note that it can be blocked by browsers. MSAL's loginPopup opens a window. Ensure that call is triggered by a user action (click event), otherwise browser will block it. In our code, it is on button click, which is fine.

**Debugging tips**:

- **Enable MSAL Logging**: MSAL allows you to configure a logger with `msalInstance.setLogger` or in config. You can set it to `logLevel: LogLevel.Verbose` during dev to see detailed logs of each step. It will log to console by default.
- **Network Traces**: Use browser dev tools Network tab. During loginRedirect, you won't see the network calls in your app (since browser goes away to B2C), but you can use the browser devtools to preserve log and see the calls to `.../authorize` and `.../token`. After redirect, you can see the token request in the network tab (it’s usually a POST to your B2C `.../token` endpoint).
- **Use B2C "Run now"**: In Azure portal, under your user flow, there's a "Run user flow" feature where you can simulate the sign-in/sign-up page. If something is wrong with the user flow itself (say, it’s not accepting a social login because not configured), this helps isolate whether the issue is in Azure config or in your app.
- **Application Insights for B2C**: If you have a custom policy and set up App Insights, you can see logs of each step and technical profile executed, which is invaluable for debugging complex flows ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=To%20diagnose%20problems%20with%20your,It)) ([Troubleshoot custom policies and user flows in Azure Active Directory B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/troubleshoot#:~:text=Application%20Insights%20trace%20log%20details)). For user flows, there's less detail available but failure events might show up.
- **Azure AD B2C Logs**: B2C does emit sign-in logs that include basic info and error codes. In Azure Portal under your B2C tenant's Audit Logs or sign-in logs, you might see entries for failed or successful logins. The info is somewhat limited for B2C (compared to Azure AD), but it can confirm if a sign-in reached B2C and what error was generated.

**Specific scenario troubleshooting**:

- If after login, your app isn't showing as logged in: Check that `MsalProvider` is properly wrapping and that you call `useIsAuthenticated()` or `accounts` correctly. Possibly the redirect happened but maybe the app reloaded from scratch (which is fine, MSAL should still cache tokens). Try calling `msalInstance.getAllAccounts()` in console to see if it has an account. If not, maybe the redirect handling didn't occur. Ensure you are not manually removing the hash from URL before MSAL processes it (MSAL React actually handles this internally by using a hidden iframe for silent token, etc.).
- If the tokens are there but API calls fail with 401: Then it's likely an API or token validation issue, covered in backend section.

**Handling error display**:
For a polished app, you might want to catch errors and display user-friendly messages. For example, if login fails because of network, show "Unable to reach the authentication server. Check your connection." If fails due to misconfig (unlikely once in prod), maybe "Application configuration error, please contact support." For B2C specific ones:

- If user cancels (AADB2C90091), you might simply navigate them back to home or show "Sign in was canceled."
- If forgot password (AADB2C90118) triggers a second redirect to reset policy, after reset the user might return to sign-in. Possibly show "Password reset successful, please sign in with your new password." (This might require reading a query param that B2C can send, or you handle state accordingly).
- If a social IdP fails because of invalid client secret (that would actually show as an error on the B2C page, not making it to the app usually), you’d fix config. (E.g., if you mis-typed the Facebook secret, B2C might throw an error when trying to authenticate with Facebook – typically that error is shown on B2C's UI or as a general error code).

**Testing different scenarios**:

- Test an end-to-end sign-up, sign-out, sign-in again.
- Test password reset if enabled.
- Test login with each identity provider option.
- Test what happens if you try to access a protected route without being logged in (ensure your app either redirects to login or shows a message).
- Test token expiration: you can lower the access token lifetime in B2C (custom policy) to, say, 5 minutes for testing. Then keep the app open, call the API after 6 minutes, ensure MSAL fetches a new token (use console logging to see acquireTokenSilent happening).
- If you have roles or groups (B2C can have user groups and custom roles in claims), test that those claims come through and you handle them properly in UI (like role-based UI hiding admin sections, etc.).

**Support and Resources**:

- Azure AD B2C documentation and Microsoft Q&A forums are very helpful for error codes and scenarios (the error code reference doc lists many AADB2C codes and their meaning ([Error code reference - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/error-codes#:~:text=Error%20code%20Message%20Notes%20,0%7D%27%20has%20no%20registered))).
- Stack Overflow has many Q&As on Azure B2C errors. Often copying the error message into a search finds specific advice.
- Use the **Microsoft Authentication Library (MSAL) docs** for any nuances in the MSAL usage and advanced config (for instance, if dealing with IE11 or older browsers, there are known issues and needed config like `storeAuthStateInCookie`).
- In a pinch, you can also decode the JWT tokens on jwt.ms or jwt.io to inspect claims (like to see if certain claims are missing or to confirm token issuer and audience are correct).

**Troubleshooting Example**:
Suppose after login, your app tries to call the backend API and you get a 401 Unauthorized. First, check the network call:

- Is the Authorization header present and contains `Bearer <long_JWT>`? If not, your code to attach the token might be wrong.
- If the token is there, copy it and decode (on jwt.ms). Check the **aud** (audience) claim – it should match your API's Application ID URI or client ID. If it says something like `undefined` or is wrong, likely you requested wrong scope. Make sure you're using the scope in the form `https://tenant.onmicrosoft.com/api-name/ScopeName` as both exposed in B2C and requested in MSAL. Also ensure that the SPA registration has permission to that scope (granted in API Permissions) ([Configure authentication in a sample React SPA by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app#:~:text=To%20enable%20your%20app%20to,the%20Azure%20AD%20B2C%20directory)).
- Check the **iss** (issuer) claim – it should be your B2C tenant URL and policy, e.g., `https://<tenant>.b2clogin.com/<tenant>.onmicrosoft.com/v2.0/`. Your backend should treat that as acceptable issuer (we'll configure that).
- If everything about token looks right, then likely the backend is not configured to validate tokens correctly (like wrong issuer or missing openId config). We'll cover that next, but you’d adjust the backend config to accept tokens from your B2C.

---

# Advanced React Features Integration

In building a real-world React application with Azure AD B2C, you’ll also want to integrate the auth solution with your app’s state management, UI libraries, and ensure performance and maintainability. This section discusses how to use advanced React techniques alongside B2C auth.

## State Management (Redux or Context API) with Authentication

If your application uses **Redux** for global state or another state container (Mobx, Zustand, etc.), you might wonder how to integrate the authentication state. With MSAL React, much of the state (like user account info, token status) is encapsulated in its context. For many apps, using the hooks provided (`useIsAuthenticated`, `useAccount`, etc.) is sufficient. However, there are scenarios where you might want to sync MSAL state to your own state:

- You may want to store some user profile info in Redux (for instance, after login, you call a backend API to get extended profile or roles and store that in Redux).
- If not using `@azure/msal-react`, some apps dispatch Redux actions on login success/failure and manage auth in Redux entirely. (This can be done by using `@azure/msal-browser` events and then storing tokens in Redux store, but be careful to not expose tokens unnecessarily).

**Using React Context**: MSAL React is itself using Context API to provide auth state. If you need additional context, you could create your own AuthContext that wraps MSAL or provides convenience data:

- For example, an `AuthProvider` that uses MSAL hooks internally and provides things like `userName`, `userRoles`, etc., to the tree, so components can access more easily than assembling from MSAL themselves. But MSAL hooks already give a lot.
- You might want to provide a context for your API calls that includes the access token automatically.

**Redux approach**:

- Upon successful login (you can use the `MsalProvider` events or just after `loginRedirect` returns, though in redirect flow you don’t exactly get a callback unless you use `handleRedirectPromise` manually), dispatch an action like `LOGIN_SUCCESS` with user info.
- Store minimal info in Redux (like `state.auth.isAuthenticated = true` and maybe `state.auth.user = { name, id, ... }`). You usually would not store the token in Redux, especially if using Redux devtools (which could expose it). Instead, tokens remain in MSAL, and when you need to call an API, you can either call MSAL directly to get token or perhaps wrap the `acquireTokenSilent` call in a Redux thunk action.
- For example, you might have a thunk `fetchUserData` that does: call `acquireTokenSilent`, then call your API, then dispatch `USERDATA_LOADED` to store some profile from API in Redux.
- The benefit of Redux is if many components need to know something like “is user an admin?”, you might derive that from user’s roles claim once and store it in Redux, so all components can read it without each needing to parse the token or call MSAL hook.
- Another pattern is to subscribe to MSAL events. MSAL has an event system (e.g., `instance.addEventCallback`) where you get events for login success, token acquisition, etc. In that callback, you could dispatch Redux actions.

However, if your app is not already heavy on Redux, introducing it just for auth might be overkill. MSAL React covers the basics. The Context API is sufficient for many use-cases.

**Example**: If using Redux, you might have something like:

```js
// pseudo-code
const initialState = { isAuthenticated: false, user: null };
function authReducer(state = initialState, action) {
  switch (action.type) {
    case "LOGIN_SUCCESS":
      return { ...state, isAuthenticated: true, user: action.payload.user };
    case "LOGOUT":
      return { ...state, isAuthenticated: false, user: null };
    default:
      return state;
  }
}
```

And an action creator:

```js
function loginSuccess(user) {
  return { type: "LOGIN_SUCCESS", payload: { user } };
}
```

Then after MSAL finishes login, you call `dispatch(loginSuccess(msalAccount))`. The `user` could be {name: ..., jwt: ...} or some info. But again, storing the whole JWT might be unnecessary in Redux.

**Synchronization**: One challenge is if MSAL state changes outside of Redux (like user logs out via MSAL’s own method). But in our integration, we always call our `handleLogout` which could also dispatch Redux `LOGOUT`. If some other component calls MSAL directly, we might miss updating Redux. Typically, you'd centralize login/logout through your abstraction to keep in sync.

**Using user data/claims**:

- MSAL gives you the ID token raw or as claims. You can call `instance.getActiveAccount()?.idTokenClaims` to get a JSON of claims. Advanced dev might map this to a user model. For instance, you might extract `preferred_username` (often the email) or custom attributes.
- If you extended B2C schema with custom attributes (say "Role" or "LoyaltyId"), and configured the user flow to return them as claims, they will appear in `idTokenClaims`. You can then use them in the app (e.g., if claim `role = admin`, show admin menu).

**Guarding Routes**:
We mentioned `<AuthenticatedTemplate>` and similar. For complex apps, you might implement a higher-order component or wrapper to guard routes based on roles. For example:

```jsx
// A custom ProtectedRoute for v6
import { useIsAuthenticated } from "@azure/msal-react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {
  const isAuth = useIsAuthenticated();
  if (!isAuth) {
    return <Navigate to="/" replace />; // redirect to home or login page
  }
  return children;
}

// usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>;
```

For roles, you might have something like:

```jsx
function RoleProtectedRoute({ children, requiredRole }) {
  const { instance, accounts } = useMsal();
  const account = accounts[0];
  const idTokenClaims = account?.idTokenClaims || {};
  const roles =
    idTokenClaims["extension_Roles"] || idTokenClaims["roles"] || []; // depending on how roles are in token
  if (!roles.includes(requiredRole)) {
    return <div>Access Denied</div>; // or redirect
  }
  return children;
}
```

Then wrap a route with `<RoleProtectedRoute requiredRole="Admin">...</RoleProtectedRoute>`.

## UI Framework Integration (Material-UI, Tailwind CSS)

Using a UI framework does not drastically change how you implement authentication, but here are some considerations:

- **Material-UI (MUI)**: You might style the login/logout buttons with MUI `<Button>` components. For example, our `<NavBar>` could import MUI's Button and do `<Button variant="contained" onClick={handleLogin}>Sign In</Button>`. Also you can use MUI icons (maybe a Person icon next to user name). Ensure that these components update correctly on state change (they should, as our useIsAuthenticated hook triggers re-render).
  - If you use Material-UI’s theming or context, no conflict with MSAL's context – they can coexist.
  - You might have a modal from MUI (Dialog component) and in it you call `loginPopup` so user sees a popup login inside a modal. But actually loginPopup opens a new window, so the modal might just show a spinner and then wait for result. This is a design choice.
- **Tailwind CSS**: If using Tailwind, you'll have a bunch of utility classes. You can easily style the sign-in button with Tailwind classes (e.g., `className="bg-blue-500 text-white px-4 py-2 rounded"`). Tailwind doesn’t conflict with our logic either.
  - One thing with Tailwind: if you want to customize B2C pages to look like your Tailwind design, you could actually include Tailwind’s CDN in the custom page content. B2C user flows allow you to upload an HTML template for pages, which can include references to CSS frameworks. So you could use Tailwind classes in the HTML for B2C pages if you host the Tailwind CSS file. This way, the user sees a consistent style on the Azure-hosted pages as on your React app. That requires using **Page UI customization** in B2C (under User Flows > Page layouts). You’d upload an HTML file to blob storage (for instance) with your branding, include `<script src="...MSAL injector...">` and your CSS.
- **Responsive design**: Ensure your login button and any content is placed in a responsive manner in your nav. (Usually straightforward but if you have a hamburger menu etc., ensure it works when logged in vs out).
- **Customizing B2C pages**: If the default Azure AD B2C pages look too plain or off-brand, consider customizing them. There are two levels:
  - **Company branding**: You can add your logo and background, and tweak CSS via the user flow UI. Quick but limited changes (colors, etc.).
  - **Embedded HTML content**: As mentioned, upload completely custom HTML/CSS for the pages. The Microsoft docs "Customize the user interface with HTML templates" shows how to do that ([Customize the user interface with HTML templates - Azure AD B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/customize-ui-with-html#:~:text=Customize%20the%20user%20interface%20with,use%20Azure%20Active%20Directory%20B2C)). This is more advanced but yields a seamless experience. Just be aware that customizing too heavily requires maintenance (if B2C UI changes, your templates might need updates).
- **Testing UX**: Ensure that the transition to the B2C page and back is smooth. There will always be a full page redirect (unless you attempt to use popup). The user might see a short blank page during redirect. You can provide a better UX by:
  - Possibly showing a spinner or "Redirecting to login..." message right after the user clicks sign-in and before actually leaving your app. Since loginRedirect triggers a navigation, you might not have much time, but maybe set some state to show a loading overlay. It might only be visible for a second, but it’s fine.
  - Similarly, after redirecting back, MSAL might take a moment to process tokens. If your app can show a loading state, that helps. In practice, MSAL processes quickly, but if your app does heavy loading on start, it might not immediately show the logged-in UI.
  - You can create a **loading screen component** that checks `isAuthenticated` status. For example, initial mount, you don't know yet (actually useIsAuthenticated might return false until the redirect is processed). Possibly use `MsalProvider` with its own mechanism or call `handleRedirectPromise`. However, msal-react internally delays children rendering until redirect handling is done (I believe it does, by how it's designed). But if not, you could use something like:
    ```jsx
    const { inProgress } = useMsal();
    if (inProgress === "handleRedirect") return <LoadingSpinner />;
    ```
    The `inProgress` state from MSAL tells you if a login or acquireToken is currently happening.
- **Accessibility**: If using custom controls for login, ensure they are accessible (e.g., proper ARIA labels). B2C pages themselves have basic accessibility, but if you customize them, keep that in mind.

## Performance Optimizations

Integrating auth can impact performance if not managed:

- **Bundle size**: `@azure/msal-browser` is not tiny – it's a moderately sized library (perhaps a few hundred KB). To mitigate this:
  - Use code splitting: If the landing page of your app doesn’t require authentication, you could lazy-load the MSAL stuff. For example, only import and initialize MSAL when the user actually goes to login or a protected route. However, in most cases you need to know auth state from the start (to know whether to show login or content), so you'll likely load it upfront. It's usually acceptable for most apps, but be aware.
  - If using an alternative, MSAL is the official library. Other community libraries exist but they also wrap MSAL or older ADAL. Stick with MSAL for support and security.
- **Avoid excessive re-renders**: When using context and hooks, be mindful of render patterns:
  - The `AuthenticatedTemplate` and `UnauthenticatedTemplate` components internally subscribe to MSAL context and will re-render only when auth state changes – which is efficient.
  - If using `useMsal()` in many components, each of those components will re-render when MSAL state changes (e.g., on login). That's fine (only happens when login or logout happens). But don't put `useMsal()` in a deeply nested component that re-renders often for other reasons unless needed.
  - If you have heavy components that don’t care about auth, don’t use the auth context in them to avoid them re-rendering on login events.
- **Caching user data**: If on login you fetch additional data (e.g., user profile from your API), cache it appropriately so you don't fetch it on every render. Possibly store in Redux or Context and use memoization.
- **Parallelize token requests**: If on app startup you need multiple tokens (maybe one for an API, one for another API), MSAL can queue them. But try to request all needed scopes in one go if possible (less overhead).
- **Profile and Monitor**: Use React Developer Tools and browser performance tools to ensure that the presence of MSAL isn't slowing down your app. Typically, it won't unless misused. One scenario to watch: if you accidentally call `acquireTokenSilent` in a render loop (like not using useEffect properly), you could spam requests. Always call such functions in effects or event handlers, not every render.
- **Logging Impact**: Turn off verbose MSAL logging in production as it can be verbose. Use an appropriate log level or none in release builds.

**Large user base considerations**:

- If millions of users sign up, B2C can handle it, but your app listing those might not. So use pagination or server-side filtering for any UI that lists user accounts (if any in admin portal).
- B2C has a limit (50 million users per tenant with certain conditions ([Tutorial - Create an Azure Active Directory B2C tenant | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant#:~:text=,Learn%20how%20to%20%204))) so partitioning by tenants is needed if you ever reach that.

**Offline Support**:

- If your app needs to handle offline (no internet), obviously auth cannot happen offline. But you could allow the user to use cached data if token is still valid and just not try to call protected API until online. This is more of an app design decision (offline mode with limited functionality perhaps). MSAL cannot refresh tokens offline, but if token is not expired you could use it when back online.

**Mobile performance**:

- If this React app is a PWA or mobile wrapper, consider using MSAL's capabilities to work in webviews or with Auth redirect in mobile browser.

**Testing and QA**:

- Test in different browsers. MSAL supports all modern browsers, and even IE11 with some config. But if you need to support IE11, you must include some extra config (like `storeAuthStateInCookie: true`) due to its limitations ([Enable authentication in a React application by using Azure Active Directory B2C building blocks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-react-spa-app#:~:text=,the%20App%20and%20Pages%20components)).
- Test with slow network (simulate 3G) to ensure your loading spinners or messages appear.

**Memory usage**:

- MSAL's in-memory cache is small (just tokens and accounts). But if a user has many accounts (not common in B2C), it could store all. Not an issue typically.

**Upgrading MSAL**:

- Keep an eye on MSAL library updates (they do fix bugs that could impact performance or compatibility, e.g., improvements for newest React versions). Upgrading should be easy if you follow semver and test.

---

# Backend Integration

In most applications, authentication is not useful by itself; it serves to protect resources, typically via an API. In this section, we will discuss how to integrate our authenticated React front-end with a backend API (which could be built in Node.js, .NET, or any other technology). We will cover obtaining and using access tokens in the React app, validating them in the backend, and end-to-end communication.

## Calling Protected APIs from the React App

Our React app, after login, can acquire an **Access Token** for the backend API. The typical flow:

1. **Define the API scope** as we did in the B2C app registrations (e.g., `https://<tenant>.onmicrosoft.com/<api-name>/API.Access`).
2. **Include that scope in the login request or a subsequent token request.** For example, when calling `loginRedirect`, you can pass `{ scopes: [apiScope] }` so that the user consents to that scope during login. Alternatively, you can call `acquireTokenSilent({ scopes: [apiScope] })` after login to get the token.
3. MSAL returns an object with `accessToken` property.
4. **Use the Access Token in API calls**: Typically, in fetch or axios, set the `Authorization` header:
   ```js
   const token = response.accessToken;
   fetch('https://myapi.com/data', {
     headers: {
       'Authorization': `Bearer ${token}`
     }
   })
   .then(res => ...)
   ```
   This attaches the JWT access token. The API will see this and must validate it.
5. On the API side, if the token is valid and the user is authorized for that endpoint, it will respond with data. If not, it will return 401 or 403.

**Token acquisition example** (with MSAL hooks):
You can use the `useMsalAuthentication` hook from MSAL React to automatically handle acquiring a token for a given interaction. But a straightforward way:

```jsx
// Example of calling an API from a component
import { useMsal } from "@azure/msal-react";
import { tokenRequest } from "../authConfig"; // contains scopes

function DataFetcher() {
  const { instance, accounts } = useMsal();
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    if (accounts.length === 0) return;
    const account = accounts[0];
    // Acquire token silently for our API
    instance
      .acquireTokenSilent({
        ...tokenRequest,
        account: account,
      })
      .then((result) => {
        const accessToken = result.accessToken;
        // Now call API
        fetch("https://myapi.com/hello", {
          headers: { Authorization: `Bearer ${accessToken}` },
        })
          .then((res) => res.json())
          .then((data) => setData(data))
          .catch((err) => console.error("API call error", err));
      })
      .catch((err) => {
        console.error("Token acquisition failure", err);
        // Optionally handle InteractionRequired by redirecting user to login again
      });
  }, [instance, accounts]);

  if (!data) return <div>Loading data...</div>;
  return <div>Data from API: {JSON.stringify(data)}</div>;
}
```

In this snippet, we wait for a user account to exist, then get a token and call the API. The fetched data is stored in state and displayed.

**CORS**: If your API is on a different domain (likely), make sure it has CORS enabled to allow your React app's origin to call it. Set appropriate `Access-Control-Allow-Origin: https://yourapp.com` on the API responses.

**Refresh scenario**: If the token is expired or about to, `acquireTokenSilent` will automatically use the refresh token to get a new one. If the refresh token is also expired or not present (e.g., user hasn’t consented to that scope yet), it will throw an error requiring interaction. You might then do `instance.acquireTokenRedirect({ scopes: [apiScope] })` to prompt the user to login or consent. In practice, if you requested the scope during initial login, you won’t need an extra consent, and refresh should just work silently.

**Multiple APIs**: If you have multiple different APIs (with different App IDs), you can have multiple scopes. For example:

```js
const api1Scope = "https://tenant.onmicrosoft.com/api1/Read";
const api2Scope = "https://tenant.onmicrosoft.com/api2/ReadWrite";
instance.acquireTokenSilent({ scopes: [api1Scope, api2Scope] });
```

You can also get separate tokens for each (some prefer not to request too many in one token to keep token size small). It's fine to get separate tokens as needed.

Now that the front-end can call the API, let's ensure the **backend** accepts and validates the token properly.

## Backend API – Validating Tokens (Node.js example)

We’ll consider a Node.js (Express) backend first. The main task is to **validate the JWT** sent by the React app:

- Verify the token’s signature using Azure AD B2C’s public keys,
- Check the token has not expired,
- Check the issuer matches our tenant,
- Check the audience matches our API’s client ID or App ID URI,
- Possibly check certain claims (like ensure `scp` (scope) claim contains the expected scope like "API.Access").

Fortunately, there are libraries that simplify this:

- **passport-azure-ad**: A Passport.js strategy for Azure AD (works for B2C with some config). We saw code earlier using `BearerStrategy` from this library ([Enable authentication in your own Node.js web API by using Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-in-node-web-app-with-api#:~:text=%2F%2F%3Cms_docref_import_azuread_lib%3E%20const%20BearerStrategy%20%3D%20require%28%27passport,ms_docref_import_azuread_lib)) ([Enable authentication in your own Node.js web API by using Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-in-node-web-app-with-api#:~:text=%2F%2F,const%20app%20%3D%20express)).
- **jsonwebtoken (jwks-rsa)**: A more manual approach where you fetch the JWKS (JSON Web Key Set) from B2C and use it to verify the JWT using `jsonwebtoken` library. The JWKS URL for B2C is usually: `https://<tenant>.b2clogin.com/<tenant>.onmicrosoft.com/<policy>/v2.0/.well-known/openid-configuration`. Actually, that URL returns metadata which includes a JWKS URI. For a quick method, you can use `express-jwt` and `jwks-rsa` combo which can automatically fetch keys.

**Using passport-azure-ad (BearerStrategy)**:
We already saw an example setup:

```js
const passport = require("passport");
const BearerStrategy = require("passport-azure-ad").BearerStrategy;

const options = {
  identityMetadata: `https://${tenantName}.b2clogin.com/${tenantName}.onmicrosoft.com/${policyName}/v2.0/.well-known/openid-configuration/`,
  clientID: "<API-app-client-id>",
  issuer: `https://${tenantName}.b2clogin.com/${tenantName}.onmicrosoft.com/${policyName}/v2.0/`,
  // issuer is sometimes required but passport-azure-ad can derive it
  policyName: policyName,
  isB2C: true,
  validateIssuer: true,
  loggingLevel: "warn",
  passReqToCallback: false,
};

passport.use(
  new BearerStrategy(options, (token, done) => {
    // token is the JWT claims
    return done(null, {}, token);
  })
);

// Protect routes
app.use(passport.initialize());
app.get(
  "/hello",
  passport.authenticate("oauth-bearer", { session: false }),
  (req, res) => {
    console.log("User claims:", req.authInfo); // token claims are in req.authInfo
    res.send("Hello " + req.authInfo.name);
  }
);
```

Important in options:

- `identityMetadata` points to the OpenID Connect metadata for your B2C policy (which includes the JWKS URL) ([Enable authentication in your own Node.js web API by using Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-in-node-web-app-with-api#:~:text=%2F%2F,isB2C)).
- `clientID` is the _Application ID of your API_ (the one you assigned in B2C for the API). The library uses it as the expected audience.
- `issuer` or `issuerValidation` settings ensure the token was issued by your tenant & policy. Setting `validateIssuer: true` and providing either `issuer` or policy/tenant info will ensure it matches ([Enable authentication in your own Node.js web API by using Azure Active Directory B2C - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-in-node-web-app-with-api#:~:text=audience%3A%20config,passReqToCallback)).
- `policyName` and `isB2C` just help the library form things correctly for B2C.

Then, `passport.authenticate('oauth-bearer')` will automatically:

- Read the `Authorization: Bearer <token>` header,
- Validate the token (signature, issuer, audience),
- If valid, attach the decoded token to `req.authInfo` (and `req.user` possibly as empty {} as above),
- If invalid, respond with 401.

Now any route under that middleware is protected.

Make sure to send a 401 response for unauthorized, which Passport does by default if not authenticated.

**Using express-jwt and jwks-rsa**:
An alternative without Passport (maybe simpler if you don't use Passport for anything else):

```js
const jwt = require("express-jwt");
const jwksRsa = require("jwks-rsa");

const jwtCheck = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 10,
    jwksUri: `https://${tenantName}.b2clogin.com/${tenantName}.onmicrosoft.com/${policyName}/discovery/v2.0/keys`,
  }),
  audience: "<API-app-client-id>", // or the App ID URI of the API
  issuer: `https://${tenantName}.b2clogin.com/${tenantName}.onmicrosoft.com/${policyName}/v2.0/`,
  algorithms: ["RS256"],
});
app.get("/hello", jwtCheck, (req, res) => {
  res.send("Hello " + req.user.name);
});
```

This uses `express-jwt` to validate JWT using the JWKS. The `jwksUri` is typically something like `.../discovery/v2.0/keys` (which is given in B2C’s metadata). You supply the expected audience (your API’s id) and issuer (the B2C tenant/policy). If the token fails any check, a 401 is sent automatically by express-jwt.

**Validating in .NET (ASP.NET Core)**:
If your backend is in .NET Core, it's even easier with Microsoft.Identity.Web:
In Startup:

```csharp
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(options => {
         Configuration.Bind("AzureAdB2C", options);
         // options instance will have ClientId (Audience), Domain, etc from config
         options.TokenValidationParameters.NameClaimType = "name";
    },
    options => { Configuration.Bind("AzureAdB2C", options); });
```

And in appsettings.json you'd have:

```json
"AzureAdB2C": {
  "Instance": "https://<tenant>.b2clogin.com/",
  "Domain": "<tenant>.onmicrosoft.com",
  "TenantId": "<tenant GUID or domain>",
  "ClientId": "<API app client Id>",
  "SignUpSignInPolicyId": "B2C_1_signupsignin"
}
```

This will automatically set up JWT Bearer auth with the correct authority (which it forms as `https://tenant.b2clogin.com/tenant.onmicrosoft.com/B2C_1_signupsignin/v2.0`) and audience (clientId). Then, use `[Authorize]` on controllers or endpoints to protect them. The .NET middleware will validate tokens for you ([Enable authentication in a web API by using Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/enable-authentication-web-api#:~:text=%2F%2F%20Adds%20Microsoft%20Identity%20platform,options)).

**Validating roles/scopes**:
If your API defines multiple scopes or roles, you might want to enforce that. For example, if the token has `scp` claim `"API.Read"`, you might want certain endpoints to require that scope. In .NET, you can use policy: `[Authorize(Policy="RequiredScope")]` and configure a policy that checks the scope claim. In Node, you'd manually check `req.authInfo.scp` or `req.user.scp`.

**Testing the API**:

- Try calling the API without a token -> should get 401.
- Call with token but modified one character (invalid signature) -> 401.
- Call with a token for a different audience (maybe an ID token or a token from a different app) -> 401.
- Call with correct token -> 200 and expected response.

Use tools like Postman or curl to test your API with a token copied from the app (for manual verification).

**Handling token expiration**:

- If a token is expired, the API will reject it (401). The React app should then catch a 401, and possibly trigger a token refresh or re-login. Typically, if using refresh tokens correctly, the app should rarely send an expired token. But in long sessions or if the app was asleep (laptop in sleep mode, etc.), a token might expire without a silent refresh in time. In that case, on 401, a robust app might attempt to acquire a new token and retry once.
- If the refresh token is revoked (say user changed password, which invalidates refresh tokens), the app will eventually get an interaction required error when trying to get a new access token. Then you must send user to login again.

**On-Behalf-Of flow** (OBO):
If your React app calls an API, and that API in turn needs to call another downstream API (like Microsoft Graph), there's an OAuth2 flow called **On-Behalf-Of**. That’s beyond our direct scenario, but just to note: your API would take the access token from the client, and exchange it for a new token to call the next API, asserting it’s on behalf of the same user ([Request an access token in Azure Active Directory B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens#:~:text=Request%20an%20access%20token%20in,Of%20flow)). Azure AD B2C now supports OBO for its tokens (provided the required setup in app registrations). If you ever need that (say your API calls another microservice which also is protected by B2C, or an Azure AD protected resource), you would implement OBO in the backend.

## Deployment and Maintenance

Finally, once everything works, we need to deploy the system and plan for maintenance:

### Deploying the React Frontend

Options for hosting a React SPA include:

- **Azure Static Web Apps**: A great option that can also integrate with Azure Functions for API and has features for authentication. (However, Azure Static Web Apps authentication currently ties into Azure AD, not Azure AD B2C. So you might not use its built-in auth, but you can still host the SPA).
- **Azure Blob Storage + CDN**: You can upload the compiled `build` folder to an Azure Blob Storage container with static website enabled. Then use a custom domain and CDN if needed. This is cheap and serverless.
- **Azure App Service (Web App)**: You can host the static files on a Node/Express or .NET server or even on App Service as static files. If you already have an API, you might serve the SPA from the same server for simplicity (just host the files and have a catch-all route to serve index.html for client-side routing).
- **Others**: Of course, Netlify, Vercel, GitHub Pages, AWS S3, etc., can host the static site. Azure AD B2C will work from anywhere as long as the redirect URI is configured.

Make sure to set the correct production redirect URI in Azure AD B2C App Registration and perhaps adjust any environment variables (for example, maybe your B2C tenant name or policy name might be different between dev and prod if you use separate tenants).

**Building**: Run `npm run build` to get the optimized production build. Use that for deployment. Double-check that the msalConfig in production points to the correct stuff (maybe in dev you used a test B2C tenant and in prod you'll use a prod B2C tenant).

**Environment config**: You might store B2C config in environment files (e.g., .env) and use something like `REACT_APP_B2C_CLIENT_ID`. React will bake those in at build time. Ensure you don't commit secrets (though for SPA, clientId and policy are not secrets). If you have any admin or instrumentation keys, use environment injection in your pipeline or config files.

**Custom Domain**: If you use a custom domain for your website, ensure it’s added as a redirect URI. Also consider setting up a **custom domain for B2C** (e.g., auth.contoso.com instead of contoso.b2clogin.com) for a truly branded experience. Azure AD B2C allows custom domains if you bring a certificate. It's not required, but nice for user experience.

### Deploying the Backend API

If you have a Node.js API:

- Host it on Azure App Service (Linux or Windows) or Azure Functions (if it fits serverless model).
- Or containerize it and use Azure Container Instances or AKS if needed.
- Or if using .NET, an App Service or Azure Functions for .NET is straightforward.

**Configuration**: Store settings like B2C tenant name, policy, clientId (audience) in configuration (appsettings.json for .NET, environment vars for Node). These are not highly secret (except maybe client secret if API needs to call other APIs). Keep the client secret (for OBO or Graph API calls) safe in something like Azure Key Vault or App Service secrets.

**CORS**: Enable it to allow your front-end origin. In .NET, use `services.AddCors` to allow the domain. In Node, maybe use the `cors` package:

```js
const cors = require("cors");
app.use(cors({ origin: "https://myapp.com" }));
```

During dev, allow localhost:3000.

**Testing in production**: Do a smoke test after deployment: navigate to the site, attempt login, ensure redirect works (watch out for any domain differences), and that API calls succeed.

### Monitoring and Logging

Set up monitoring for both front-end and back-end:

- **Front-end**: Since it's static, you rely on Application Insights for front-end (by adding their JS SDK) to track if users encounter errors. Alternatively, track in Google Analytics or some error reporting service like Sentry. MSAL can be configured to send telemetry to Application Insights too (there is an option to capture events).
- **Back-end**: Enable Application Insights (for .NET, easy via instrumentation key; for Node, you can use the Application Insights Node SDK). This will capture request logs, and you can query failures (e.g., how many 401s are happening).
- **B2C Logs**: Azure AD B2C sign-in logs and audit logs should be monitored. You can configure **Azure Monitor Diagnostic Settings** to send B2C logs to a Log Analytics workspace, to Azure Storage, or to a SIEM (like Azure Sentinel) ([Monitor Azure AD B2C with Azure Monitor - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/azure-monitor#:~:text=Use%20Azure%20Monitor%20to%20route,gain%20insights%20into%20your%20environment)) ([Monitor Azure AD B2C with Azure Monitor - Azure AD B2C | Microsoft Learn](https://learn.microsoft.com/en-us/azure/active-directory-b2c/azure-monitor#:~:text=You%20can%20route%20log%20events,to)). This way, you can create alerts – for example, alert if there's a sudden spike in failed sign-ins (which could indicate an attack or outage), or if the number of users reaches certain thresholds.
- **Alerts**: Set up Azure alerts on B2C metrics if possible (B2C doesn't have many metrics, but you might rely on logs or the MAU count in Azure billing). Also, monitor the App Service metrics (CPU, memory) and the Application Insights for exceptions.

### Maintenance Considerations

- **Key Rotation**: Azure AD B2C will automatically rotate its signing keys periodically. Because we use the metadata URL or JWKS, our backend always fetches the current keys. So normally no manual intervention is needed. If you ever hard-coded a key (not recommended), you'd need to update it when B2C rotates (they rotate every few weeks typically).
- **Certificate Updates for Identity Providers**: If you integrated a SAML IdP or something that uses certificates, keep an eye on their cert expiry. For OAuth2 social logins, the client secret may expire (Facebook secrets do not typically expire, Google Client IDs usually do not expire). But if you regenerate secrets, update them in B2C.
- **User Management**: As an admin, you can manage users in the Azure AD B2C blade (create, delete, reset passwords). If your app needs an admin UI to manage users, you might use Microsoft Graph API for Azure AD B2C or the Azure AD Graph API (which is older) to programmatically manage B2C users. Ensure you have proper admin consent if you do that. This is beyond auth but part of maintenance (like user deletion on request, etc.).
- **Scaling**: B2C itself scales automatically. But ensure your chosen hosting for SPA and API scales to user load. The React app can be served via CDN which is easily scalable. The API, if on consumption plan or a scaled-out App Service, handle according to your needs. Use load tests to ensure JWT validation overhead is not a bottleneck (generally it's fast with caching keys).
- **Costs**: Azure AD B2C is billed by MAU (monthly active users) with some free tier (50k) and then per usage. Keep an eye on MAU in Azure Portal (it shows in B2C tenant overview). If you have sudden spikes in usage, your cost goes up linearly, but it's usually reasonable.
  - If you have multiple user flows, note that a user might count multiple times if they use multiple flows without sign-in in a month. However, currently B2C counts a unique user per month across all flows, so usually fine.
- **Updating Libraries**: Keep MSAL updated, as well as any backend libraries for JWT. Security patches in those can be critical.
- **Logging out across devices**: If a user changes their password or you want to force log out across all devices, Azure AD B2C can revoke refresh tokens. If you absolutely need global sign-out, you might consider in your app logic to check for some flag server-side (like store a "forceLogoutVersion" for a user in DB, and include that in token via custom claim, if mismatch then force login). This is complex but mentioning if needed for high-security environments.

- **New Features**: Azure AD B2C is part of "Microsoft Entra" now and evolving. Keep an eye on new features like Conditional Access, Identity Protection for B2C, custom policy improvements, etc., which you can adopt to improve security or user experience.
- **Documentation for Team**: For maintainability, document the setup: e.g., document the B2C tenant name, policies used, app registrations and their keys, etc., so if someone new joins the dev team or if you revisit in a year, you recall the configuration. Possibly script the setup (there are Azure CLI or Terraform modules for Azure AD B2C).
- **Testing Environment**: Usually you should have at least two B2C tenants: one for Dev/QA and one for Production, so you can test changes (like new user flows or custom policies) safely. Maintain them in parallel. Azure provides a way to export/import user flows (and custom policies you manage via files anyway). Ensure the app registrations exist in both and your app can switch depending on environment (e.g., using env variables as mentioned).

Finally, be mindful of the **user experience** during maintenance:

- If you ever need to change a user flow or custom policy in production, try not to disrupt logged-in users. Ideally, changes are backward compatible (for example, adding a new claim in token).
- If rotating an API scope or resource, you may need to update both front and back ends synchronously (like if you change the API's App ID URI).
- Communicate with users if any downtime for auth is expected (rarely needed, B2C is pretty much always available globally).

This concludes the deep-dive guide. With the above steps and considerations, an advanced developer should be able to implement and maintain a robust Azure AD B2C authentication system in a React application.

---

**Congratulations!** You have built a complete end-to-end solution with Azure AD B2C and React. You’ve learned how to set up a B2C tenant, configure user flows or custom policies, integrate MSAL into React for secure authentication, protect routes, call APIs with tokens, and enforce security best practices across the stack. Azure AD B2C takes care of the heavy lifting of identity management, and you focused on wiring it up correctly and securely in your app.

**Next Steps / Exercises**:

- Try implementing a **password reset** user flow in your application (add a "Forgot Password" link that triggers the reset).
- Experiment with a **custom policy**: for instance, try the starter pack for SocialAndLocalAccounts and modify it to display a custom UI. This will give you insight into the custom policy structure.
- Integrate an additional **social provider** (if you haven't already) like Twitter or LinkedIn and ensure the login process works for those.
- Implement a role-based authorization in the React app: assign a custom attribute or user flow that tags a user as "Admin", include that in the token, and then conditionally render admin components in React if the role is present.
- Load test your application (using a tool like Apache JMeter or k6) after deployment to see how it handles multiple simultaneous logins and API calls, and observe how B2C scales – this can build confidence for production load.

By following this guide and completing the exercises, you should be well-equipped to handle advanced scenarios and ensure a smooth, secure authentication experience for your users.
