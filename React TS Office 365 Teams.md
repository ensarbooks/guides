**Introduction**  
This comprehensive guide walks you through building a **React + TypeScript** application that displays all Office 365 users and integrates deeply with Microsoft Teams. We’ll start from scratch – covering project setup, authentication with **Microsoft Entra ID** (formerly Azure AD) via MSAL, data retrieval from **Microsoft Graph API**, UI development with **Fluent UI**, and then deploy the app as a Microsoft Teams tab. Along the way, we’ll implement search and filtering, set up CI/CD pipelines, and discuss debugging and monitoring best practices. This guide is intended for advanced developers and is structured in a step-by-step format with code examples, screenshots, and diagrams for clarity.

# 1. Project Setup

Before coding the application, ensure your development environment is ready with the necessary tools: **Node.js**, **npm**, **TypeScript**, and a React project scaffold (using **Vite** or **Create React App**). In this section, we’ll install required tools and initialize a new React + TypeScript project.

## 1.1 Installing Node.js and npm

First, install **Node.js** (which includes npm). Many modern React toolchains require Node v18 or above. As of this writing, Vite requires Node.js **18+ or 20+**. Download the latest LTS version of Node.js from the official website and run the installer (on Windows/macOS) or use your package manager (on Linux). After installation, verify the versions:

```bash
node -v
npm -v
```

Ensure Node is at least v18. If not, update Node.js before proceeding. npm comes bundled with Node; you should see a version number for npm as well. npm will be used to install project dependencies and run scripts.

## 1.2 Setting Up TypeScript

TypeScript adds static typing to JavaScript, catching errors early and improving code maintainability. Create React App and Vite can both scaffold a React + TypeScript project without separate manual TypeScript setup. However, you may still want the TypeScript compiler available globally for linting or IDE intellisense. You can install it globally with:

```bash
npm install -g typescript
```

This isn’t strictly required if using a scaffold that includes TypeScript, but having the `tsc` command available can be useful (e.g., to quickly check type definitions). Verify TypeScript is installed by checking the version:

```bash
tsc -v
```

It should display the TypeScript version (e.g., 5.x). Now we’re ready to scaffold our React project.

## 1.3 Creating a React + TypeScript Project

You have two primary options to create a new React app: **Vite** (a fast, next-gen build tool) or **Create React App (CRA)** (the classic Facebook-supported toolchain). We’ll demonstrate using **Vite** for its superior performance and modern features, but note where CRA differs.

### 1.3.1 Using Vite

Vite offers a project creation command that sets everything up for you. In your terminal, run:

```bash
npm create vite@latest
```

This will launch an interactive prompt. You’ll be asked to enter a project name and select a framework and variant. For the framework, choose **React**, and for the variant, choose **TypeScript** (React + SWC is also an option, but we’ll use the default bundler). For example, if we name the project “o365-users”, you would:

1. Run `npm create vite@latest o365-users`
2. When prompted for a framework, select **React**.
3. When prompted for a variant, select **React + TypeScript**.

Vite will generate the project structure in a new folder (here, `o365-users`). The scaffold includes a `src` directory with key files like `main.tsx` (entry point), `App.tsx` (root component), an `index.html`, and configuration files like `tsconfig.json` and `vite.config.ts` ([How to build a React + TypeScript app with Vite - LogRocket Blog](https://blog.logrocket.com/build-react-typescript-app-vite/#:~:text=After%20processing%20the%20project%20information,generate%20the%20project%E2%80%99s%20folder%20structure)) ([How to build a React + TypeScript app with Vite - LogRocket Blog](https://blog.logrocket.com/build-react-typescript-app-vite/#:~:text=,file%20for%20any%20Vite%20project)). The structure will look roughly like this:

```
o365-users/
├─ src/
│  ├─ assets/         // images or static assets
│  ├─ App.tsx         // main App component
│  ├─ main.tsx        // ReactDOM rendering
│  └─ ... (other files)
├─ public/            // public static files (if any)
├─ package.json
├─ tsconfig.json
├─ vite.config.ts
└─ ...
```

Vite’s template already includes React and TypeScript configuration.

Now, install dependencies and launch the dev server:

```bash
cd o365-users
npm install
npm run dev
```

The Vite dev server will start and output a local URL (e.g. `http://localhost:5173`) ([How to build a React + TypeScript app with Vite - LogRocket Blog](https://blog.logrocket.com/build-react-typescript-app-vite/#:~:text=Running%20the%20application)). Open that in your browser to see the default React welcome page (Vite’s mascot or React logo). You now have a working React + TypeScript app! Press `Ctrl+C` in the terminal to stop the dev server when needed.

### 1.3.2 Using Create React App (Alternative)

If you prefer or require **Create React App**, you can use the TypeScript template as follows:

```bash
npx create-react-app o365-users --template typescript
```

This will create a new folder `o365-users` with a similar structure (using Webpack instead of Vite under the hood). After creation, run `npm start` to start the development server. The default port is 3000 for CRA (so `http://localhost:3000`). Both Vite and CRA approaches yield a React/TypeScript project ready for development.

**Note:** We’ll proceed with the Vite-based project for this guide, but the steps for integration with Microsoft Graph and Teams are applicable regardless of the build tool. Minor adjustments (like script names or config locations) will be noted where relevant.

## 1.4 Project Structure and Important Files

Before diving into coding, let’s note key files in the scaffold:

- **package.json** – Lists dependencies and scripts. Notably, you should see `"react"` and `"react-dom"`, and dev dependencies for TypeScript and possibly Vite.
- **tsconfig.json** – TypeScript compiler options. The default from Vite/CRA is fine, but ensure `jsx` is set to `react-jsx` and `strict` mode is true for best practices.
- **index.html** – The single HTML page into which our React app is injected. In Vite, this lives in the project root by default.
- **src/main.tsx** – Entry point that bootstraps the React app by rendering `<App />` into the DOM.
- **src/App.tsx** – The main React component. We will heavily modify this (or its children) to implement our UI.

At this point, we have a baseline React application running locally. Next, we’ll set up authentication with Azure AD and integrate Microsoft Graph API to fetch users.

# 2. Microsoft Graph API Integration

Our application needs to authenticate with Microsoft 365 and retrieve data (the list of users) from the **Microsoft Graph API**. The Graph API is the gateway to Microsoft 365 data (users, mail, Teams, etc.), and in our case we’ll call the `/users` endpoint to list all users in the organization. This section covers setting up an Azure AD app registration, using **MSAL.js** (Microsoft Authentication Library) in React for login, and calling Graph API endpoints with the acquired token.

**Overview of Authentication Flow:** When the user opens our app (whether standalone or in Teams), they need to sign in with their Microsoft 365 credentials. We’ll use **OAuth 2.0 Authorization Code Flow with PKCE** via MSAL. The React app will redirect or pop up a Microsoft login page, the user signs in, and MSAL obtains an **ID token** (for authentication) and an **access token** for Graph API. The access token (a JWT) is then used to call Graph’s REST endpoints. The diagram below illustrates this flow, where our **SPA** uses MSAL to acquire a token from Azure AD before calling Graph API ([React single-page application using MSAL React to authenticate users against Microsoft Entra External ID - Code Samples | Microsoft Learn](https://learn.microsoft.com/en-us/samples/azure-samples/ms-identity-ciam-javascript-tutorial/ms-identity-ciam-javascript-tutorial-1-sign-in-react/)):

Once authenticated, our app can call `https://graph.microsoft.com/v1.0/users` to get the user list. Let’s break the process into steps:

1. Register an app in Azure (to get a client ID and set permissions).
2. Install and configure MSAL in our React app.
3. Implement the login flow in React (sign-in and sign-out logic).
4. Acquire a token and call the Graph API to fetch users.

## 2.1 Registering an Azure AD Application (Microsoft Entra ID)

To allow our React app to authenticate users and call Graph, we must register it in **Microsoft Entra ID** (Azure AD). This gives us an **Application (client) ID** and enables us to specify permissions (like reading users).

**Step 1:** Open the [Azure Portal](https://portal.azure.com) and navigate to **Azure AD** (Entra ID) > **App registrations**. Click **“New registration”**. You will see a form like below ([image]()) where you provide details for the app registration.

- **Name:** Choose a name like “O365 User Directory App” – this is just a friendly identifier.
- **Supported account types:** If this app is only for your tenant (organization), choose **“Accounts in this organizational directory only”** (single-tenant) ([image]()). If it should work for multiple organizations, choose multi-tenant options ([entra-docs/docs/identity-platform/includes/registration/quickstart-register-app.md at main · MicrosoftDocs/entra-docs · GitHub](https://github.com/MicrosoftDocs/entra-docs/blob/main/docs/identity-platform/includes/registration/quickstart-register-app.md#:~:text=Supported%20account%20types%20Description%20Accounts,in%20your%20tenant)) ([entra-docs/docs/identity-platform/includes/registration/quickstart-register-app.md at main · MicrosoftDocs/entra-docs · GitHub](https://github.com/MicrosoftDocs/entra-docs/blob/main/docs/identity-platform/includes/registration/quickstart-register-app.md#:~:text=Accounts%20in%20any%20organizational%20directory,the%20widest%20set%20of%20customers)). For this guide, we’ll assume single-tenant (the Office 365 organization of your company).
- **Redirect URI:** Since this is a single-page app, we’ll configure this after selecting the platform. Leave it blank here for now (or you can set it if the UI allows).

Click **Register** to create the application. Once created, you’ll be taken to the app’s **Overview** page. Here, note the **Application (client) ID** and **Directory (tenant) ID** ([image]()). We will use the client ID in our React app configuration. The tenant ID is used if you want to restrict login to your organization’s Azure AD (in MSAL configuration, this can be part of the authority URL).

Next, we need to configure **Authentication** and **API permissions** for this app registration:

**Step 2: Authentication Platform Configuration:** In your app registration, go to **Authentication** in the sidebar. Add a platform for your app – choose **“Single-page application (SPA)”**. In the SPA settings, add your allowed **Redirect URI**. For development, this is likely `http://localhost:5173` (if using Vite’s default) or `http://localhost:3000` (CRA default), or wherever your dev server runs. Also add the production URL (we’ll have one after deployment, e.g., an Azure Web App or Static Web App domain). It’s important that the redirect URI exactly matches the URL where the app will be running and handling auth responses. Enable the checkbox **“Allow public client flows”** or specifically **“Allow authentication tokens in the browser”** if available (this setting might be automatically enabled for SPAs). Save these settings.

**Step 3: API Permissions:** By default, a new app registration has basic delegated permissions like **User.Read** for Microsoft Graph. Our goal is to list **all users** in the directory, which requires a higher permission. Specifically, we need **User.Read.All** (delegated) or **Directory.Read.All** for full directory access. We’ll use **User.Read.All** for this scenario, which allows reading all user profiles (but not other directory objects). In **API Permissions** for the app, do the following:

- Click **“Add a permission”**. Choose **Microsoft Graph** -> **Delegated permissions** (since our app will act on behalf of a signed-in user).
- Search for **User.Read.All** and select it. Also consider adding **User.ReadBasic.All** if you only need basic properties, but **User.Read.All** covers all user properties and is fine.
- The permission will be added, but note the status will show **“Not granted (admin consent required)”** for User.Read.All, because it requires admin consent. Click **“Grant admin consent for [Your Tenant]”** if you are an admin, to consent to this permission for your app. This step is necessary so that any user in your tenant can use the app without individually needing to be an admin (since the app will be retrieving all users). Ensure the status changes to **Granted**.

At this point, our Azure AD app registration is configured with a client ID, redirect URIs, and permissions to call Graph and read all users. We did not create a client secret because for a SPA we use **public client** flows (no secret needed, as the app can’t securely hold a secret). Now we can move on to our React code to utilize this registration.

## 2.2 Installing MSAL and Setting up Authentication

Back in our React project, we need to install the MSAL libraries and configure them with the Azure AD app details. We will use the official **MSAL for React** library (`@azure/msal-react`) which is a wrapper around the core `@azure/msal-browser` library, providing React context integration.

**Install MSAL packages:** In your project directory, run:

```bash
npm install @azure/msal-browser @azure/msal-react
```

This adds the libraries to your project. Next, create a configuration for MSAL in our app.

**MSAL Configuration:** Create a new file, e.g. `src/authConfig.ts` (or `.js`), to define the MSAL configuration object. Here’s an example configuration:

```tsx
// src/authConfig.ts
import { Configuration, LogLevel } from "@azure/msal-browser";

export const msalConfig: Configuration = {
  auth: {
    clientId: "<YOUR_CLIENT_ID>", // from Azure AD app registration
    authority: "https://login.microsoftonline.com/<YOUR_TENANT_ID>",
    redirectUri: "/", // redirect to base path (ensure this is in Azure AD redirect URIs)
  },
  system: {
    loggerOptions: {
      loggerCallback: (level, message) => {
        if (level === LogLevel.Error) {
          console.error(message);
        } else if (level === LogLevel.Info) {
          console.info(message);
        }
      },
      logLevel: LogLevel.Info,
    },
  },
};
```

A few points about this config:

- `clientId` is the Application (client) ID from the registration. Replace `"<YOUR_CLIENT_ID>"` with that GUID.
- `authority` is the URL of the Azure AD tenant or common endpoint. We use `https://login.microsoftonline.com/<tenant>` where `<tenant>` is either your tenant ID (from Azure portal) or a domain (like `contoso.onmicrosoft.com`). Using a specific tenant ID ensures only your org’s users can sign in; if you set `common` or `organizations` as the tenant, any work/school account can sign in (if multi-tenant).
- `redirectUri` can be set to the root (“/”) which means it will redirect to the index of your application. When running locally, this means `http://localhost:5173/` which we added in Azure AD. In production, we will also ensure the deployed domain is added.
- We also configure a simple logger to console for MSAL events (optional, but helps debugging).

Next, we initialize an MSAL instance and integrate it with React.

**Initialize MSAL and Wrap App:** In your `src/main.tsx` (entry file for React), we will create an instance of `PublicClientApplication` with the above config, and use `MsalProvider` to make it available to the React component tree. For example:

```tsx
// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import { msalConfig } from "./authConfig";

const msalInstance = new PublicClientApplication(msalConfig);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <App />
    </MsalProvider>
  </React.StrictMode>
);
```

Now our entire `<App />` is wrapped with MsalProvider ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=1.%20%60.%2Fsrc%2FApp.js%60%20,signed%20in%2C%20signin%20will%20be)), meaning any component can use authentication context and hooks provided by MSAL React.

## 2.3 Implementing Login and Logout in React

With MSAL configured, we need UI components and logic for signing in and out. MSAL React provides hooks like `useMsal` to get the MSAL instance and methods, and components such as `<AuthenticatedTemplate>` / `<UnauthenticatedTemplate>` to conditionally render UI based on login state ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=3.%20%60.%2Fsrc%2Fpages%2FHome.jsx%60%20,and%20token%20requests)). We’ll create a simple **Login button** that triggers the login flow, and a **Logout button** for signing out, plus ensure that upon login a token is acquired.

**Login Button Component:** Let’s create a component for login. We’ll use MSAL’s `useMsal` hook to get the PublicClientApplication instance, and call `loginPopup` (or `loginRedirect`) when the user clicks. We will request the necessary scopes (permissions) during login – at minimum the **User.Read** scope is often consented by default. However, since we need `User.Read.All`, and we’ve already granted admin consent for it, we can request it in the token acquisition silently. To keep things simple, we might just request **User.Read** on initial login (to get basic profile), and then request `User.Read.All` later when calling Graph. Alternatively, we can request **User.Read.All** upfront in the login to get the token in one go.

For clarity, we’ll perform login and then token acquisition in a separate step. Here’s a simple login component:

```tsx
// src/components/SignInButton.tsx (for example)
import { useMsal } from "@azure/msal-react";
import {
  InteractionType,
  InteractionRequiredAuthError,
} from "@azure/msal-browser";

export const SignInButton: React.FC = () => {
  const { instance } = useMsal();

  const handleLogin = async () => {
    try {
      await instance.loginPopup({
        scopes: ["User.Read"], // basic scopes; we will get broader scopes later
      });
      // loginPopup will handle redirects internally and return here when done
      console.log("Login successful!");
    } catch (err) {
      console.error("Login failed:", err);
    }
  };

  return <button onClick={handleLogin}>Sign In</button>;
};
```

This uses a popup flow (which is often better for SPAs than redirect, to avoid full-page reloads). If you prefer redirect, use `loginRedirect` and handle the redirect in a similar way (MSAL will redirect back to your app’s redirect URI and you’d call `instance.handleRedirectPromise()` on app start; MSAL React can also automatically handle redirects if you pass an `useMsalAuthentication` hook). The popup flow opens a new window for the user to log in, then returns control to the SPA.

**Logout:** Similarly, we can implement a logout button:

```tsx
export const SignOutButton: React.FC = () => {
  const { instance } = useMsal();
  const handleLogout = () => {
    instance.logoutPopup({
      postLogoutRedirectUri: "/", // redirect to home after logout
    });
  };
  return <button onClick={handleLogout}>Sign Out</button>;
};
```

Now, in our `App.tsx`, we can utilize MSAL React’s templates to show one of these buttons depending on whether a user is logged in:

```tsx
// src/App.tsx
import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
} from "@azure/msal-react";
import { SignInButton } from "./components/SignInButton";
import { SignOutButton } from "./components/SignOutButton";
import UsersList from "./components/UsersList"; // (we will create this to display users)

function App() {
  return (
    <div className="App">
      <h1>Office 365 User Directory</h1>

      <UnauthenticatedTemplate>
        <p>Please sign in to view the user directory.</p>
        <SignInButton />
      </UnauthenticatedTemplate>

      <AuthenticatedTemplate>
        <SignOutButton />
        <UsersList />
      </AuthenticatedTemplate>
    </div>
  );
}

export default App;
```

In the above snippet, when the user is not signed in, they see a prompt and the SignInButton. Once they sign in (the state changes), the AuthenticatedTemplate content is shown – a SignOut button and the `UsersList` component which will fetch and display users ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=3.%20%60.%2Fsrc%2Fpages%2FHome.jsx%60%20,and%20token%20requests)) ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=,of%20how%20to%20get%20the)). The MSAL provider internally keeps track of the authentication state.

## 2.4 Acquiring Access Token for Microsoft Graph

After a user signs in, we need an **access token** with the **User.Read.All** scope to call the Graph API. We can get this token using MSAL’s `acquireTokenSilent` method (which uses cached credentials or refresh as needed). If the scope wasn’t pre-consented or if an error occurs (like consent required), we might need to call `acquireTokenPopup` as a fallback to prompt the user.

We will implement the logic to get the token and call Graph in the `UsersList` component. For brevity, we will use the native `fetch` API to call Graph, but you can also use the official **Microsoft Graph JavaScript SDK**. Using direct HTTP calls is straightforward for our scenario.

**UsersList Component Implementation:**

```tsx
// src/components/UsersList.tsx
import React, { useState, useEffect } from "react";
import { useMsal } from "@azure/msal-react";

interface User {
  id: string;
  displayName: string;
  mail: string;
  department?: string;
  jobTitle?: string;
  // ... other user properties as needed
}

const UsersList: React.FC = () => {
  const { instance, accounts } = useMsal();
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      if (accounts.length === 0) return; // not logged in
      try {
        // Attempt to get token silently
        const response = await instance.acquireTokenSilent({
          scopes: ["User.Read.All"],
          account: accounts[0], // current signed-in account
        });
        const accessToken = response.accessToken;
        console.log(
          "Got Graph access token:",
          accessToken.substring(0, 15),
          "..."
        );

        // Call Microsoft Graph API /users endpoint
        const graphResponse = await fetch(
          "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,department,jobTitle",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        if (!graphResponse.ok) {
          throw new Error(`Graph API error: ${graphResponse.status}`);
        }
        const data = await graphResponse.json();
        setUsers(data.value); // Graph returns users in 'value' array
      } catch (err: any) {
        console.error(err);
        // If silent token acquisition fails (e.g., token expired or scope not consented), fallback to interactive
        if (err.name === "InteractionRequiredAuthError") {
          try {
            const response = await instance.acquireTokenPopup({
              scopes: ["User.Read.All"],
            });
            const accessToken = response.accessToken;
            const graphResponse = await fetch(
              "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,department,jobTitle",
              {
                headers: { Authorization: `Bearer ${accessToken}` },
              }
            );
            if (!graphResponse.ok) {
              throw new Error(`Graph API error: ${graphResponse.status}`);
            }
            const data = await graphResponse.json();
            setUsers(data.value);
          } catch (err2) {
            console.error(err2);
            setError(err2.message);
          }
        } else {
          setError(err.message);
        }
      }
    };

    fetchUsers();
  }, [instance, accounts]);

  if (error) {
    return <div>Error: {error}</div>;
  }
  if (!users.length) {
    return <div>Loading users...</div>;
  }

  return (
    <div>
      <h2>All Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <strong>{user.displayName}</strong> – {user.mail}
            {user.department && ` – ${user.department}`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UsersList;
```

Let’s break down what’s happening in `UsersList`:

- We use the MSAL hook to get the `instance` (PublicClientApplication) and the array of `accounts` (should contain the currently signed-in account).
- On component mount (and whenever `accounts` changes), we call `instance.acquireTokenSilent({ scopes: ["User.Read.All"] })` to get a token with the permissions to read all users. This call will succeed if we have a cached token or a refresh token, and if not it throws an `InteractionRequiredAuthError`.
- If successful, we get an `accessToken`. We then call Graph’s REST API: `GET /v1.0/users` with an Authorization header `Bearer <token>`. We also use `$select` to fetch only specific fields (displayName, mail, etc.) to limit payload. The Graph API returns a JSON with a `value` array of user objects.
- We save the users to state and render them in a list. If there is an error (e.g., no permission, network issue), we catch it and display an error message.
- If `acquireTokenSilent` fails due to needing user interaction (maybe first time consent), we use `acquireTokenPopup` as a fallback to show a consent prompt for the `User.Read.All` scope ([help using graph api : r/GraphAPI](https://www.reddit.com/r/GraphAPI/comments/1evz015/help_using_graph_api/#:~:text=https%3A%2F%2Flearn.microsoft.com%2Fen)). After that, we retry the fetch.
- We also handle basic loading state (if no users yet, show “Loading…”).

With this in place, when a user logs in, the UsersList component will automatically fetch all users from Graph. The list (likely unsorted) will include users’ display names and emails, and optionally departments and job titles as examples. You can adjust the fields and logic as needed.

**Graph API Permissions Note:** We are using the **delegated permission** `User.Read.All`. This means the signed-in user must have permission to read user data. By default, any user can read basic info of other users in the organization (unless restricted by policy), which is why this works. The admin consent we granted ensures the app has permission on behalf of users. If you wanted to absolutely ensure only admin can use this app, you could check the user’s role or use **app-only** permissions with client credentials, but that’s beyond our scope. For most cases, delegated `User.Read.All` with admin consent is sufficient to let non-admins read the directory via the app.

At this point, we have a working front-end that can authenticate and display users. Running `npm run dev` and logging in should show the list of all users in your Azure AD. The next step is to enhance the UI using Fluent UI to make it more professional and to add features like search and filtering.

# 3. UI Development with Fluent UI

To make our application look and feel consistent with Microsoft 365 experiences, we’ll use **Fluent UI React**, Microsoft’s official UI library for building web interfaces that blend with Office products. Fluent UI (formerly Office UI Fabric) provides a rich set of styled components (text, buttons, lists, etc.) and theming support. We will implement our user list and search using Fluent UI components.

## 3.1 Installing and Setting Up Fluent UI

Fluent UI for React can be installed via npm. We’ll use the Fluent UI v8 (also known as **@fluentui/react** package, which is the stable Office UI Fabric component library). Run:

```bash
npm install @fluentui/react
```

Additionally, to use icons or certain components, you may need the Fluent UI icons package:

```bash
npm install @fluentui/react-icons
```

(Though for basic usage, the core package is enough). After installing, we should apply the Fluent UI styling baseline. Fluent UI components use CSS-in-JS, but some components might require a theme provider. In Fluent v8, you can use components directly, but we might want to wrap our app in `Customizer` or apply a Fluent theme. For simplicity, we’ll use components out of the box.

Importing Fluent components is straightforward. For example:

```tsx
import { TextField, Stack, DetailsList, IColumn } from "@fluentui/react";
```

We will use **TextField** for search input, and **DetailsList** to render the list of users in a table format (with columns like Name, Email, Department). The `DetailsList` component provides built-in sorting, filtering, etc., but we can also handle filtering ourselves.

## 3.2 Building the Users List UI with Fluent UI

Instead of the simple `<ul>` list we used initially, let’s create a more polished table of users. We’ll use `DetailsList`, which expects an array of items and column definitions. We’ll transform our `users` state into that format.

First, define the columns for the list:

```tsx
// Inside UsersList component, before return:
const columns: IColumn[] = [
  {
    key: "column1",
    name: "Name",
    fieldName: "displayName",
    minWidth: 150,
    maxWidth: 200,
    isResizable: true,
  },
  {
    key: "column2",
    name: "Email",
    fieldName: "mail",
    minWidth: 200,
    maxWidth: 300,
    isResizable: true,
  },
  {
    key: "column3",
    name: "Department",
    fieldName: "department",
    minWidth: 100,
    maxWidth: 150,
    isResizable: true,
  },
  {
    key: "column4",
    name: "Job Title",
    fieldName: "jobTitle",
    minWidth: 100,
    maxWidth: 150,
    isResizable: true,
  },
];
```

The `fieldName` should match property names in our user objects. Now, we can render `DetailsList`:

```tsx
<DetailsList
  items={users}
  columns={columns}
  selectionMode={
    0
  } /* 0 = none, we’re not enabling selection of rows in this example */
  styles={{
    root: { maxHeight: 500 },
  }} /* set a max height if you want scroll */
/>
```

This will render a table with a header row (Name, Email, etc.) and each user as a row. The list is automatically scrollable if items exceed the container height. It also supports clicking column headers to sort (by default, sorts by the field, or you can control it).

Additionally, we want to add a **Search** feature. We can use Fluent UI’s **SearchBox** or simply a TextField for input. There is `SearchBox` component that provides a search icon and clear button by default. Let’s use it:

```tsx
import { SearchBox } from "@fluentui/react";

// In UsersList component state:
const [searchQuery, setSearchQuery] = useState("");

// In JSX, above the DetailsList:
<SearchBox
  placeholder="Search users..."
  value={searchQuery}
  onChange={(_, newValue) => setSearchQuery(newValue || "")}
  styles={{ root: { maxWidth: 300, marginBottom: 10 } }}
/>;
```

Now, we don’t want to show all users if a search query is entered – we want to filter the list. We can compute a filtered array of users based on `searchQuery`. For example:

```tsx
const filteredUsers = users.filter((u) => {
  const search = searchQuery.toLowerCase();
  return (
    u.displayName.toLowerCase().includes(search) ||
    (u.mail && u.mail.toLowerCase().includes(search)) ||
    (u.department && u.department.toLowerCase().includes(search))
  );
});
```

Then pass `filteredUsers` to `DetailsList` as items. This will dynamically show only those users matching the search text. Given that `users` might be large, this is a client-side filter. Alternatively, for very large directories, you might consider using Graph API’s `$search` query parameter on the `/users` endpoint to only retrieve matching users. Graph supports searching users by name or email via `$search="YOUR QUERY"` (with appropriate headers). But implementing server-side search would complicate the example (requiring API calls on each query). For now, client-side is fine assuming a manageable number of users or that the user will filter reasonably.

Update the JSX accordingly:

```tsx
<DetailsList items={filteredUsers} columns={columns} selectionMode={0} />
```

Now our UsersList component’s render might look like:

```tsx
return (
  <div>
    <Stack tokens={{ childrenGap: 10 }}>
      <h2>All Users</h2>
      <SearchBox ... />
      {filteredUsers.length > 0 ? (
        <DetailsList ... />
      ) : (
        <div>No users found.</div>
      )}
    </Stack>
  </div>
);
```

We wrapped in a Fluent UI `Stack` (a layout component that stacks children vertically with spacing). The `Stack` component is useful for layout in Fluent UI – here we just give some gap between the search box and list.

At this point, the UI is functional and styled with Fluent UI. The list has resizable columns, and the search box filters users.

## 3.3 Enhancing User Profile Display

Fluent UI also provides a **Persona** component that nicely displays a user’s avatar (photo or initials) along with their name and details ([Persona - Office UI Fabric JS](https://developer.microsoft.com/en-us/fabric-js/components/persona/persona#:~:text=Represents%20a%20person%2C%20complete%20with,initials%20can%20be%20shown%20instead)). As an optional enhancement, we could replace the simple text in the list with a Persona. For example, instead of just showing name in the list, we could use a custom `onRender` function for the Name column that returns a Persona component:

```tsx
import { Persona, PersonaSize } from "@fluentui/react";

// In columns definition for Name:
{
  key: 'column1', name: 'Name', fieldName: 'displayName', minWidth: 150, maxWidth: 250,
  onRender: (item: User) => (
    <Persona
      text={item.displayName}
      secondaryText={item.mail}
      size={PersonaSize.size40}
      imageInitials={item.displayName.split(' ').map(n => n[0]).join('')}
    />
  )
}
```

This will display each user as a Persona with their initials as an avatar (unless we fetch their actual photo separately). The Persona component can fetch images if provided an `imageUrl` (Graph has a `/photo/$value` endpoint for users, which we could call for each user’s photo – but doing that for all users might be heavy, so we might skip actual photos). The initials provide a nice colorful circle with the user’s initials by default.

For simplicity, the above approach suffices. We then might remove the separate Email column since email is shown as secondary text in Persona, or keep it if we want it separately. It’s up to design preferences.

We could also style the SignIn/SignOut buttons using Fluent UI’s `PrimaryButton` component for consistency, but that’s minor.

After these UI enhancements, our application should look like a mini version of a corporate directory: a search box, and a scrollable list of user profiles with names, emails, etc., all in a Fluent UI style.

# 4. Implementing Features: Search, Filtering, and Profile Views

We already added a basic **search** box that filters the list of users as the user types. Let’s recap and ensure it’s robust, and discuss adding a user **profile view** feature when a user is selected.

## 4.1 Search and Filtering Implementation

The search function we added listens to the `onChange` of the search box and updates the `searchQuery` state. This triggers a re-render and filters the `users` array. This approach is straightforward. For large data, consider debouncing the search input (waiting for the user to stop typing before filtering, to avoid too many re-renders). Fluent UI’s SearchBox doesn’t have built-in debouncing, but you can implement it with a `setTimeout` or a library like lodash if needed. For our case, it’s fine to filter as the user types.

We used `displayName`, `mail`, and `department` fields for filtering. You can extend this to other fields (jobTitle, etc.) depending on what’s important in your scenario.

If your tenant has thousands of users, fetching all and filtering client-side might be slow. In such cases, using Graph’s query parameters is better. For example, Graph supports queries like:

- `$filter` – e.g., `GET /users?$filter=startsWith(displayName, 'John')` to server-side filter names starting with John.
- `$search` – e.g., `GET /users?$search="John"` (with header `ConsistencyLevel: eventual`) to search across several fields (displayName, email, etc.). This requires the `User.Read.All` scope and is a relatively new feature for Graph.

Using those would require modifying our data fetch to be query-based per search input (and possibly adding a debounce to avoid calling Graph on every keystroke). This is an advanced optimization; for now, we assume a moderate user count or that the app is used by admins who will browse the list.

## 4.2 User Profile View Feature

It might be useful to view more details about a user or a profile card when clicking on a user in the list. We have a couple of ways to implement this:

- **Detail Panel**: When a user is clicked, open a Fluent UI **Panel** (a side pane) or **Dialog** showing that user’s details (maybe photo, phone, etc.).
- **Separate Page**: Use React Router to navigate to a user detail page (e.g., `/users/<id>`). This is feasible but in a Teams context (tab) might complicate navigation unless we use Deeplinks or tab navigation – so a modal/panel might be simpler.
- **Hover card**: Fluent UI has a **HoverCard** or we could integrate something like the Microsoft Graph Toolkit’s person card, but that’s another library.

We’ll implement a simple **Panel**. Fluent UI’s `Panel` component slides in from the side and can contain arbitrary content.

**Step 1:** Add state to track the selected user and a boolean for whether the panel is open:

```tsx
const [selectedUser, setSelectedUser] = useState<User | null>(null);
const [isPanelOpen, setIsPanelOpen] = useState(false);
```

**Step 2:** Modify `DetailsList` to handle item invocation (row click). We can use the `onActiveItemChanged` or `onItemInvoked` prop of DetailsList:

```tsx
<DetailsList
  items={filteredUsers}
  columns={columns}
  selectionMode={0}
  onItemInvoked={(item) => {
    setSelectedUser(item);
    setIsPanelOpen(true);
  }}
/>
```

This means when a row is clicked/activated, we set that user as selected and open the panel.

**Step 3:** Include the Panel in JSX:

```tsx
<Panel
  headerText="User Details"
  isOpen={isPanelOpen}
  onDismiss={() => setIsPanelOpen(false)}
  closeButtonAriaLabel="Close"
>
  {selectedUser && (
    <div>
      <Persona
        text={selectedUser.displayName}
        secondaryText={selectedUser.mail}
        size={PersonaSize.size72}
        imageInitials={selectedUser.displayName
          .split(" ")
          .map((n) => n[0])
          .join("")}
        styles={{ root: { marginBottom: 20 } }}
      />
      <p>
        <b>Department:</b> {selectedUser.department || "N/A"}
      </p>
      <p>
        <b>Job Title:</b> {selectedUser.jobTitle || "N/A"}
      </p>
      <p>
        <b>User ID:</b> {selectedUser.id}
      </p>
      {/* Add other fields as desired */}
    </div>
  )}
</Panel>
```

Now, when the panel is open, it shows a larger Persona with the user’s name and email and some additional info. We included the user’s Azure AD object ID for reference. You could also fetch more details dynamically here (for example, call Graph `/users/{id}` to get full profile including phone, address, etc. since our initial call used $select and might not have everything). But since we selected common properties in $select, we have enough to display a basic profile.

This feature enhances user exploration: you can search and then click a user to see details.

**Testing the UI:** At this stage, run the app and test signing in, searching for a user, and clicking their name. You should see a panel with their information. The UI should be clean and responsive. Fluent UI ensures that out-of-the-box components (like Persona, DetailsList) are responsive and accessible (keyboard navigation, etc.).

# 5. Teams Deployment (Creating a Teams Tab App)

Now that our React app is functional as a standalone web app, we want to **embed it in Microsoft Teams** as a custom app. Microsoft Teams supports custom tabs, which are basically iframes that load your web app within Teams ([Tabs in Microsoft Teams - Teams | Microsoft Learn](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs#:~:text=In%20this%20article)) ([Tabs in Microsoft Teams - Teams | Microsoft Learn](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs#:~:text=Tabs%20are%20client,see%20Teams%20JavaScript%20client%20library)). We will create a Teams app manifest to introduce our React app as a personal tab in Teams.

There are a few steps to deploying to Teams:

1. Hosting the app at an HTTPS URL (Teams requires https endpoint for content). We’ll cover hosting in the next section, but keep in mind the app must be accessible via the internet. For now, you can test using a tool like **ngrok** to expose your local dev server over HTTPS for Teams testing.
2. Creating a Teams app **manifest** (a JSON file) that describes the app (name, icons, domain, and tab configuration).
3. Packaging the manifest and icons into a zip, and uploading to Teams (either via the Teams client as a custom app or via the Teams Developer Portal).
4. Testing the app in Teams and ensuring authentication works inside the Teams context.

## 5.1 Preparing the App for Teams

There are a couple of considerations when running our app inside Teams:

- **Authentication in Teams**: Since our app uses MSAL and opens a popup for login, we need to ensure this still works within Teams (Teams desktop and web). By default, Teams might block content that opens new windows unless configured for authentication. However, MSAL’s loginPopup should work – it will open a browser window outside Teams for the user to authenticate. Another approach is to use Teams’ built-in authentication mechanisms (like the Teams JavaScript SDK and SSO). A full SSO integration is complex (requires adding the `webApplicationInfo` in manifest and exchange tokens), so we will rely on MSAL interactive login. This is fine, but users will have to sign in the first time, even if they’re already signed into Teams. For many scenarios this is acceptable.
- If we wanted to improve this, we could implement **Teams SSO** (Single Sign-On) which allows our app to silently get a token via Teams’ authentication, but that requires Azure AD app to have an **Application ID URI** and specific manifest changes (beyond our scope). We’ll proceed with our existing MSAL approach, which should prompt the user to login with Microsoft and then it will work (the user might only need to do this once, since MSAL will cache tokens).

## 5.2 Creating the Teams App Manifest

The Teams app manifest is a JSON file (typically named `manifest.json`) following the Teams schema (currently at version 1.20 as of 2025). This manifest defines how Teams should display and launch our app. Key sections include: **staticTabs**, **configurableTabs**, **bots**, **permissions**, **validDomains**, etc. For a simple personal tab app, we will focus on static tabs.

**Manifest Fields** (important ones for our scenario):

- `manifestVersion`: The schema version (use “1.20” for latest).
- `id`: A unique GUID for your Teams app (can use an online GUID generator to create one).
- `packageName`: A unique package identifier (reverse domain notation, e.g., “com.contoso.o365users”).
- `developer`: Information about you or your company (name, website, etc.).
- `name` and `description`: The name of your app (short and full descriptions).
- `icons`: Two image files (outline and color icons) for your app logo. You’ll need a 32x32 outline icon and a 192x192 (or 512x512) color icon.
- `staticTabs`: An array of tabs that are static (personal scope). We will add one entry here for our personal tab.
- `permissions` and `validDomains`: For our web content, we must list the domain where it’s hosted under `validDomains`. Also, since our app calls Graph API as the user, we might list `"Microsoft Graph"` under webApplicationInfo if doing SSO, but in our case MSAL covers it. We do not have a bot or messaging extensions, so we’ll leave those out or empty.

**Creating manifest.json**: Here’s a sample manifest (with placeholders to replace):

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.20/MicrosoftTeams.schema.json",
  "manifestVersion": "1.20",
  "version": "1.0.0",
  "id": "YOUR-GUID-HERE",
  "packageName": "com.yourcompany.o365users",
  "developer": {
    "name": "Your Name or Company",
    "websiteUrl": "https://yourcompany.com",
    "privacyUrl": "https://yourcompany.com/privacy",
    "termsOfUseUrl": "https://yourcompany.com/terms"
  },
  "name": {
    "short": "O365 Directory",
    "full": "Office 365 User Directory"
  },
  "description": {
    "short": "View all Office 365 users in a directory.",
    "full": "A Teams app that displays all users in the organization’s Office 365 directory, with search and profiles."
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "accentColor": "#0078D7",
  "staticTabs": [
    {
      "entityId": "userDirectoryTab",
      "name": "User Directory",
      "contentUrl": "https://<your-app-domain>/",
      "websiteUrl": "https://<your-app-domain>/",
      "scopes": ["personal"]
    }
  ],
  "permissions": ["identity", "messageTeamMembers"],
  "validDomains": ["<your-app-domain>"]
}
```

Let’s explain a few of these:

- **contentUrl**: The URL that will be displayed in the Teams tab canvas (iframe). This should be the fully qualified HTTPS URL of your deployed app. For development/testing, if using ngrok, it might be something like `https://abc123.ngrok.io/` (pointing to your local app). Make sure to include any path if your app isn’t at root. We use the root `/` because our React app is a single page. You can include a specific route if needed.
- **websiteUrl**: This is optional for personal tabs; it’s used if a user chooses “open in browser”. We set it to the same as contentUrl.
- **entityId**: Just an identifier for the tab (can be any string, often same as an ID or name).
- **scopes**: “personal” indicates this tab is a personal app (one user, in left sidebar of Teams). We’re not adding team or group chat scopes here.

The `permissions` array lists high-level platform permissions (not to be confused with Graph API permissions). “identity” allows the app to access user’s profile info and OAuth (for single sign-on scenarios), and “messageTeamMembers” might not be needed for us, but it’s often included by default. We could omit it if not using any messaging capabilities.

**Icons**: You need to provide the actual image files named `color.png` and `outline.png` as specified. The outline icon should be transparent background, simple white outline icon (32x32). The color icon is the full color logo (192x192 or 512x512). There are templates and guidelines in Microsoft’s documentation for Teams app icons. Prepare these and include them when packaging.

## 5.3 Packaging and Testing in Teams

Once manifest and icons are ready, package them into a ZIP file:

- The zip should contain `manifest.json`, `color.png`, and `outline.png` at the root (not inside any folder in the zip). The file names in the manifest must match exactly.

To test the app in Teams:

- **Using Teams Developer Portal:** The easiest way is to use the Teams Developer Portal (a GUI in Teams for managing apps). In Teams, go to **Apps** -> search for **Developer Portal** (or directly navigate to [https://dev.teams.microsoft.com/](https://dev.teams.microsoft.com/) and log in). In Developer Portal, you can import your manifest (or create a new app and fill in the details manually). If importing, just upload the zip. It will parse the manifest and show you the details. Ensure there are no validation errors (the portal will highlight any issues). You can then click **Preview in Teams** directly from Developer Portal to test it ([Teams Developer Portal's "Preview In Teams" button showing "App ...](https://learn.microsoft.com/en-us/answers/questions/962205/teams-developer-portals-preview-in-teams-button-sh#:~:text=Teams%20Developer%20Portal%27s%20,know%20what%20I%20am)).
- **Using manual upload:** Alternatively, download the zip and in the Teams client (if you have permission to upload custom apps), go to Apps -> **Upload a custom app** -> Upload for me or your org. Choose your zip. The app should appear in Teams (maybe as a personal app you can pin).

When you open the app in Teams (personal app, left sidebar), it will load the contentUrl in an iframe. You should see your React app’s UI appear inside Teams. If you are doing this locally via ngrok, ensure ngrok is running and the URL in manifest matches. If using a deployed Azure site (we’ll cover deployment next), use that URL.

Test the functionality inside Teams:

- Does the sign-in popup work? (In Teams desktop, clicking sign-in may open a separate system browser window for Azure AD login. After signing in, return to Teams – MSAL should complete and the app should show the data. In Teams web, it might open a new tab or window).
- After signing in, you should see the user list. The Graph calls should work since it’s the same domain and the token is valid (there’s nothing special needed because it’s still OAuth to Azure AD which is internet accessible).
- Try search and profile panel within Teams. They should work as in standalone.
- Check the UI scaling – sometimes the height of the tab needs to be managed. The Teams client by default might give a fixed height to your content. If your list is cut off, you might need to call the Teams SDK `app.initialize()` and `app.notifySuccess()` or use `microsoftTeams` javascript to adjust sizing. However, personal tabs generally auto-fit. We might ignore fine-tuning that here for brevity.

At this point, we have successfully integrated our app into Teams. We’ve effectively built a **Teams personal tab app**. If all tests out, the next step is to ensure our app is **hosted** online and then set up a CI/CD pipeline for continuous deployment.

# 6. Hosting & Deployment

To make the app available to users (and to Teams), we need to host it on a live web server with HTTPS. There are multiple ways to host a React app on Azure. We’ll discuss two popular options: **Azure App Service** and **Azure Static Web Apps**. Both can serve our React build, but they differ in setup and features.

Regardless of approach, we will first prepare our app for production by building it.

## 6.1 Preparing a Production Build

If using Vite, run: `npm run build`. This will create a `dist` directory with static files (HTML, JS, CSS, assets). If using CRA, `npm run build` creates a `build` directory similarly. These files can be deployed to any static server.

Be sure to set the correct homepage or base path if your app is not served from root. For Teams, we likely host it at root of a domain, so no special base path needed. If using Static Web Apps, the default is to serve from root of the domain.

Also, ensure any environment-specific config is handled. For instance, the Azure AD client ID and authority – in our example, we hardcoded them in authConfig. If you have separate dev vs prod Azure AD app registrations, use environment variables or separate config files. But to keep focus, we’ll assume one config.

## 6.2 Option 1: Deploy to Azure App Service (Web App)

Azure App Service can run an application with a Node server or serve static files. For a React SPA, the simplest approach is to treat it as a **static site**. We can either:

- Use App Service’s static site capability (Azure Blob Storage static website, not as straightforward via App Service),
- Or deploy a Node.js App Service that serves the files (with a simple Node/Express server or by configuring Oryx to serve static content).

A common approach: create an App Service (Linux) for Node.js, and when deploying, include an `azurewebapp.config` or configure it to run `npm run build` and then serve files from `build/`. However, a simpler path is Azure Static Web Apps (discussed next).

If you choose App Service:

1. **Create App Service**: In Azure Portal, create a **Web App** resource. Choose a name (this will form part of the URL, e.g., `o365directory.azurewebsites.net`). Choose runtime stack as Node 18 (so that the environment has Node for building, if needed). For region, pick something close to you.
2. **Deployment**: You can deploy by connecting App Service to your GitHub (via deployment center), or manually via tools like Azure CLI or VS Code Azure plugins. For instance, using Azure CLI, you could zip deploy:
   - Run `npm run build` locally, then `zip -r app.zip dist/*` (for Vite, zip the dist folder contents).
   - Use Azure CLI: `az webapp deployment source config-zip -g <ResourceGroup> -n <AppName> --src app.zip`. This will upload the zip and deploy. Azure will detect it's static and might serve it. If it doesn’t, you may need to add a web.config or configure static file serving. Another method: include a package like `serve` and have a start script (but that's more complex).

Alternatively, use an **Azure Storage static website** or **Azure Static Web App**.

## 6.3 Option 2: Deploy to Azure Static Web Apps

**Azure Static Web Apps (SWA)** is a service ideal for SPAs. It not only hosts static files globally, but also provides integration with GitHub Actions for CI/CD, custom domains, and even serverless APIs if needed. The workflow is typically:

- You push code to a branch (e.g., main) on GitHub.
- GitHub Action builds the app (runs `npm run build`) and deploys to SWA.
- SWA provides a `<your-app>.azurestaticapps.net` domain.

**Steps to create Static Web App:**

1. In Azure Portal, click **Create a resource** and search for **Static Web App**.
2. Provide a name, and choose your subscription and resource group.
3. Deployment: you’ll be asked to connect to GitHub and select your repository and branch, as well as build details. You can configure:
   - Build Preset: select **React** (since our app is a React SPA).
   - App location: usually "/" if the project root has the package.json.
   - Build output: "dist" for Vite (or "build" for CRA).
   - The workflow will be set up to run on pushes to the specified branch.
4. Azure will create the resource and set up a GitHub Actions workflow in your repo (check the `.github/workflows` folder). The workflow uses `Azure/static-web-apps-deploy@v1` GitHub Action to build and deploy ([Deploy a static HTML website from Github into Azure Static Web App](https://stackoverflow.com/questions/72601446/deploy-a-static-html-website-from-github-into-azure-static-web-app#:~:text=Deploy%20a%20static%20HTML%20website,secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_GRAY_CLIFF_62B10)) ([Azure Static Site Deployment with Environment Variables - Medium](https://medium.com/@jamescori/azure-static-site-deployment-with-environment-variables-8882c33bd426#:~:text=Medium%20medium.com%20%20,secrets)).
5. Once created, the first build will run. You can monitor it in GitHub Actions. After a few minutes, it should succeed and your app will be live. The portal will show you the generated URL (something like https://<random-name>.azurestaticapps.net). You can use that as the contentUrl in Teams manifest (update and re-upload if needed). ([Deploy a React app on Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react#:~:text=1,action%20is%20complete%20before%20continuing))

Azure Static Web Apps by default sets up environment with Node and runs `npm install` and build as configured ([Deploy a React app on Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react#:~:text=Create%20a%20repository)) ([Deploy a React app on Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react#:~:text=https%3A%2F%2Fgithub.com%2Fstaticwebdev%2Freact)). It’s very convenient as you don’t have to manually publish.

One consideration: **Auth and Graph in Static Web Apps** – our app uses client-side MSAL, which doesn’t require any server configuration, so it will run fine. If we needed to protect routes or use Azure Functions as API, SWA offers an authentication/authorization feature and easy function integration, but that’s beyond our need because we call Graph directly from the client.

Now, whether you used App Service or Static Web Apps, you should have a working URL serving your app. Test the URL in a regular browser (outside Teams) to ensure the production build works and you can log in (you might need to add the production URL to Azure AD app’s Redirect URIs if not done). Once confirmed, update the Teams manifest contentUrl to this production URL and redeploy the Teams app (in Developer Portal or via uploading updated manifest).

# 7. CI/CD: Automated Build and Deployment

To streamline updates to your app, set up Continuous Integration/Continuous Deployment. If using **Azure Static Web Apps**, as mentioned, GitHub Actions might already be configured by the Azure creation wizard ([Deploy a React app on Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react#:~:text=1,action%20is%20complete%20before%20continuing)). For **Azure App Service**, you can use **GitHub Actions** or **Azure DevOps pipelines** similarly.

## 7.1 GitHub Actions for Azure

If not already set up, let’s outline a simple GitHub Actions workflow to build and deploy to Azure. We’ll illustrate one for Azure App Service (since SWA would be created automatically). Suppose we have an App Service with name and we want to deploy via actions:

Create `.github/workflows/deploy.yml` in your repo:

```yaml
name: Build and Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: "18.x"

      - name: Install dependencies
        run: npm ci

      - name: Build project
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: build_artifact
          path: dist # or build if CRA
      # The above saves the built files as an artifact in the workflow (optional, for debugging)

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: "<your_app_service_name>"
          slot-name: "production"
          publish-profile: ${{ secrets.AzureAppService_PublishProfile }}
          package: ./dist
```

In the above:

- We use `azure/webapps-deploy` action to deploy. It needs a publish profile from Azure (you can get this from Azure Portal > App Service > Get Publish Profile, then add it as a secret in GitHub). Alternatively, use `azure/login` and `azure/webapp` actions.
- We assumed building outputs to `dist`. The deploy action can deploy the folder or a zip.

For **Azure Static Web Apps**, the action is different (Azure has `Azure/static-web-apps-deploy@v1` which is configured by the SWA creation wizard). You typically don’t need to write it manually; but if so, it looks like:

```yaml
- name: Build and Deploy
  uses: Azure/static-web-apps-deploy@v1
  with:
    azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_<ENV> }}
    repo_token: ${{ secrets.GITHUB_TOKEN }}
    action: "upload"
    app_location: "/"
    output_location: "dist"
```

Where the token secret is provided by Azure when you set up the SWA (the portal action creates it in your repo secrets).

## 7.2 Azure DevOps Pipeline (Alternative)

If using Azure DevOps, you would create a pipeline (YAML or classic) that does similar steps: check out code, npm install, npm build, then use Azure CLI or an Azure App Service Deploy task to push the build. The concepts are the same. Azure DevOps might be preferred in enterprise scenarios where code is in Azure Repos or where a more elaborate release process is needed.

Regardless of CI tool, the goal is to automate building the React app and deploying to the hosting service whenever code changes. This ensures your Teams app is always up to date for users without manual intervention.

With CI/CD in place, you can focus on development and simply push changes; the pipeline will update the Azure hosting, and since the Teams tab points to that hosted URL, users will see the updates (after a browser refresh).

# 8. Debugging & Monitoring

Building and deploying is half the battle; ensuring the app runs smoothly in production and diagnosing issues is the other half. In this section, we cover debugging techniques and monitoring strategies for our React + Graph + Teams application.

## 8.1 Debugging Common Issues

**Authentication Problems:** If users cannot log in, check the following:

- Are the redirect URIs correctly configured in Azure AD for the domain they are accessing? If the app is at `https://myapp.azurewebsites.net`, that exact URL (and path if any) must be in the app registration’s redirect URIs. Missing or incorrect URIs cause the login to fail or tokens to not be returned.
- If using Teams desktop, sometimes the popup might not come to the foreground. Users might need to alt-tab to see the login window. Ensure pop-up is not blocked. For Teams web (in-browser), the loginPopup might be blocked by default browser popup blocker. In such case, consider using `loginRedirect` in Teams (which will open the login in the same window – Teams might then open a browser window for auth and navigate back). MSAL React’s `MsalAuthenticationTemplate` can handle redirect flows in an iframe scenario if configured.
- If you see a blank page or an error after login redirect, check console logs. MSAL might log an error about “interaction in progress” or similar – ensure that MSAL’s redirect handling is properly integrated. (In our approach, we used popup to avoid dealing with redirect handling, which simplifies things).

**Graph API Errors:** If the user list is not showing:

- Open developer console (F12) in the context (if in Teams desktop, you can open devtools by clicking … in the top right of the tab and selecting **Developer Tools**). Look for network requests to graph.microsoft.com. If you see 403 Forbidden, it means the token did not have the right permissions or consent. Ensure admin consent for User.Read.All was granted. If 401 Unauthorized, possibly the token wasn’t sent or is expired – check the code that acquires token. Logging the error from `catch` as we did helps identify if it’s an MSAL error (like silent token failure).
- If the list is partially loading or you suspect paging issues (Graph returns only up to 100 users by default), check if the response includes `@odata.nextLink`. In a large directory, our code only fetches the first page. To get all users, implement pagination: loop while nextLink is present, accumulating results. This can be added if needed (be mindful that if your org has thousands of users, pulling them all to the client might be slow; you might instead implement a server function to query or require filtering).

**Teams-specific issues:** If the app works on its own but not inside Teams:

- Check **validDomains** in manifest. It must include the domain of your app (e.g., `myapp.azurewebsites.net` or the ngrok domain). If not, Teams will refuse to load it in iframe.
- If you get an error in Teams like “refused to connect” or a white screen, likely the domain is not allowed or the contentUrl is wrong. Update manifest and re-upload.
- If using ngrok for dev and it’s not working in Teams, ensure you started ngrok with `https` and included that domain in manifest, and consider that Teams may cache older manifest versions (remove previous test versions of the app from Teams to avoid conflicts).
- Authentication in Teams: If you want to debug token acquisition, you can add MSAL logging (we set logLevel Info). That might show messages in console about token cache, etc. You could also instrument events for MSAL (like an event callback on login). In Teams, because it’s an embedded webview, sometimes MSAL may treat it as a new session (especially in desktop). This means the user might have to login again even if they’re logged in elsewhere. We didn’t implement “single sign-on”, which would bypass that by using Teams context. That’s an advanced improvement if needed.

**Fluent UI issues:** Most Fluent UI components are straightforward, but if something isn’t appearing:

- Ensure you imported the component from `@fluentui/react`. Sometimes missing import leads to nothing rendering but no obvious error.
- If icons aren’t showing (like a search icon in SearchBox), it might need the icon font to be loaded. Fluent UI icons are usually loaded automatically when a component requiring them is rendered, but you can also explicitly import an icons bundle:
  ```tsx
  import { initializeIcons } from "@fluentui/react/lib/Icons";
  initializeIcons();
  ```
  call that once at app startup to ensure icons are available.

## 8.2 Performance Optimization

Our app is not very heavy, but a couple points:

- **Graph data caching**: We fetch the user list fresh on each load. You might cache it in memory or localStorage if the app is used frequently, to avoid repeated calls. Or implement a refresh mechanism (e.g., refresh every X minutes or on user request).
- **Paging**: If user count is huge, consider loading in pages (Graph allows `$top=500` max per request, and skip tokens via nextLink). You can implement an infinite scroll or “Load more” button if needed.
- **Bundle size**: Vite already code-splits and tree-shakes well. But including Fluent UI means a few hundred KB of styles/scripts. MSAL is also some size. In production build, check the network tab to ensure your app bundle is reasonable. If needed, you can lazy-load some components (React.lazy for components that aren’t needed initially, like perhaps the Persona or the Panel could be code-split). However, given modern bandwidth and the app’s scope, this is likely fine.

## 8.3 Monitoring and Logging

For a production app, you’ll want to know if users hit errors. Consider integrating **Application Insights** if using Azure:

- For React apps, Application Insights has a JavaScript SDK that can capture exceptions and telemetry. You’d add it to the app and it can send data to an Azure App Insights resource. This is especially useful if publishing to many users – you can see if errors occur that you didn’t catch.
- Alternatively, if using Azure Static Web Apps, you can attach Azure Monitor to the functions or front-end (but it’s static, so limited telemetry unless you integrate something).

At the very least, keep console logging around critical actions (perhaps behind a debug flag) for diagnosing issues when testing. MSAL’s built-in logging (as configured) can help track auth issues in console.

If something goes wrong in Teams and you only have a user report, instruct them how to press `Ctrl+Shift+I` to open dev tools in Teams (desktop) and check console for any errors to share with you. It’s a bit technical, but as an advanced developer you can parse those hints.

Also monitor performance – if the tab is slow to load, maybe fetch data after showing the UI (so that user sees the UI skeleton quickly). We did that with effect after login, which is fine. Ensure the Teams tab doesn’t hit any timeouts – Teams might time out if contentUrl doesn’t load within e.g. 30 seconds. Our app loads quickly, only network delay is Graph call which is usually quick.

**Graph API Monitoring:** If you suspect Graph issues, you can use the Graph Explorer tool to manually query your tenant with the same app (use the Graph Explorer logged in as a user to test /users or check what data comes). Also watch out for Graph throttling – if many people use this app simultaneously in a large tenant, Graph might throttle requests. In such case, implement some backoff or caching. Graph returns a `Retry-After` header if throttled.

Finally, update and version your app. If you significantly update the manifest (new scopes, new features), you might need to bump the manifest version and re-upload. For broad deployment in your org, you can publish the app to your tenant’s app catalog (via the Teams admin center). That way users can easily install it.

Throughout this process, keep security in mind. Our app exposes potentially sensitive directory info, so only deploy it in a context where that’s intended (internal company use). The Azure AD permission we used (User.Read.All) is an admin-level consent because normal users reading full profile of all users is considered high privilege. By granting that, you’ve allowed the app to be used by any signed-in user to read info on others. This is usually fine (like a GAL - Global Address List). But if your org has restrictions, consider limiting access to the Teams app (Teams admin can control who can install it).

**Logging out/in**: We provided a Sign Out button. This will clear MSAL cache for that user. If the user signs out, to sign in as a different user, they can then use sign in button. In Teams, typically the expectation is one user (the Teams user). Unless someone explicitly needs to switch accounts, sign out is rarely used. But good to have if the app might be used by guest accounts, etc.

# Conclusion and Next Steps

We’ve now built an end-to-end React application that authenticates with Azure AD, retrieves Office 365 user data via Microsoft Graph, and is embedded as a Teams personal tab. We used **TypeScript** for robustness, **MSAL.js** for authentication, **Microsoft Graph API** for data, **Fluent UI** for an elegant UI, and deployed on **Azure** with CI/CD to streamline releases. We also integrated it into Teams through an app manifest, making the solution feel like a native part of Teams.

From here, you can extend the app further: add filtering by departments or other attributes, allow exporting the user list, integrate with presence (Graph beta has presence info), or add group membership lookup. You could also explore making it a configurable tab for teams (so that it could show subset of users, e.g., members of that team – though that’s a different Graph query). The possibilities are broad when combining Microsoft’s identity and Graph capabilities with a custom app.

Remember to maintain the app – update dependencies periodically (for example, MSAL or Fluent UI updates), and watch the Microsoft Graph permissions; if your organization changes policies, the app might need adjustments.

This guide covered the primary aspects to empower you to create sophisticated enterprise web apps and deploy them in the Microsoft Teams ecosystem. Happy coding!

**Sources:**

1. Vite Official Documentation – Node.js version requirements and project creation
2. _LogRocket_ – Benefits of using Vite with React and TypeScript
3. Microsoft Learn – Azure AD app registration quickstart (permissions)
4. Microsoft Learn – Microsoft Graph API for listing users (permissions & usage)
5. Reddit Q&A – Explanation of Graph API permission setup for listing users ([help using graph api : r/GraphAPI](https://www.reddit.com/r/GraphAPI/comments/1evz015/help_using_graph_api/#:~:text=https%3A%2F%2Flearn.microsoft.com%2Fen))
6. Microsoft Docs – Teams Tabs overview (tabs in personal scope) ([Tabs in Microsoft Teams - Teams | Microsoft Learn](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs#:~:text=Tabs%20are%20client,see%20Teams%20JavaScript%20client%20library)) ([Tabs in Microsoft Teams - Teams | Microsoft Learn](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs#:~:text=There%20are%20two%20types%20of,meetings%20with%20a%20customizable%20experience))
7. Microsoft Docs – Teams App manifest schema (staticTabs contentUrl and scopes)
8. GitHub – MSAL React sample README (use of MsalProvider and templates) ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=1.%20%60.%2Fsrc%2FApp.js%60%20,will%20acquire%20an%20access%20token)) ([microsoft-authentication-library-for-js/samples/msal-react-samples/react-router-sample/README.md at dev · AzureAD/microsoft-authentication-library-for-js · GitHub](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/samples/msal-react-samples/react-router-sample/README.md#:~:text=,of%20how%20to%20get%20the))
9. Microsoft Learn – Deploy React app to Azure Static Web Apps (GitHub Actions integration)
