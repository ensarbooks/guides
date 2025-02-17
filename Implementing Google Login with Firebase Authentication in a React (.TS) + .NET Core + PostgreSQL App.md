# Implementing Google Login with Firebase Authentication in a React (.TS) + .NET Core + PostgreSQL App

**Table of Contents**

1. [Introduction & Setup](#introduction--setup)
   - 1.1 [Overview of Firebase Authentication with Google Login](#overview-of-firebase-authentication-with-google-login)
   - 1.2 [Setting up a Firebase Project & Google Sign-In](#setting-up-a-firebase-project--google-sign-in)
   - 1.3 [Setting up PostgreSQL and .NET Core Backend](#setting-up-postgresql-and-net-core-backend)
   - 1.4 [Creating a React TypeScript App](#creating-a-react-typescript-app)
2. [Frontend Implementation (React & TypeScript)](#frontend-implementation-react--typescript)
   - 2.1 [Integrating Firebase Authentication SDK](#integrating-firebase-authentication-sdk)
   - 2.2 [Firebase Context and Authentication Hooks](#firebase-context-and-authentication-hooks)
   - 2.3 [Managing Authentication State (Context API)](#managing-authentication-state-context-api)
   - 2.4 [Login, Logout, and Google Auth Flows](#login-logout-and-google-auth-flows)
   - 2.5 [Protecting Routes with Authentication Guards](#protecting-routes-with-authentication-guards)
3. [Backend Implementation (.NET Core & PostgreSQL)](#backend-implementation-net-core--postgresql)
   - 3.1 [Initializing a .NET Core Web API Project](#initializing-a-net-core-web-api-project)
   - 3.2 [Configuring PostgreSQL with Entity Framework Core](#configuring-postgresql-with-entity-framework-core)
   - 3.3 [JWT Authentication with Firebase ID Tokens](#jwt-authentication-with-firebase-id-tokens)
   - 3.4 [User Management Endpoints (Login, Register, Update)](#user-management-endpoints-login-register-update)
   - 3.5 [Session Management in PostgreSQL](#session-management-in-postgresql)
4. [Security Best Practices](#security-best-practices)
   - 4.1 [Protecting API Keys and Environment Variables](#protecting-api-keys-and-environment-variables)
   - 4.2 [Server-side Token Validation & Authorization](#server-side-token-validation--authorization)
   - 4.3 [Protecting Sensitive Routes & Data](#protecting-sensitive-routes--data)
   - 4.4 [Refresh Tokens and Persistent Sessions](#refresh-tokens-and-persistent-sessions)
5. [Optimizations and Enhancements](#optimizations-and-enhancements)
   - 5.1 [Performance Improvements](#performance-improvements)
   - 5.2 [Error Handling and Logging](#error-handling-and-logging)
   - 5.3 [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
   - 5.4 [Multi-factor Authentication (MFA) and Extra Security](#multi-factor-authentication-mfa-and-extra-security)
6. [Testing and Debugging](#testing-and-debugging)
   - 6.1 [Unit Testing Authentication Flows](#unit-testing-authentication-flows)
   - 6.2 [Integration Testing Secure API Endpoints](#integration-testing-secure-api-endpoints)
   - 6.3 [Debugging Common Authentication Issues](#debugging-common-authentication-issues)
7. [Deployment & Scaling](#deployment--scaling)
   - 7.1 [Deploying the React Frontend (Firebase Hosting/Vercel)](#deploying-the-react-frontend-firebase-hostingvercel)
   - 7.2 [Deploying the .NET Core Backend (Azure/AWS/DigitalOcean)](#deploying-the-net-core-backend-azureawsdigitalocean)
   - 7.3 [CI/CD Pipeline Setup](#cicd-pipeline-setup)
   - 7.4 [Scaling for High-Traffic Applications](#scaling-for-high-traffic-applications)
8. [References](#references)
9. [Appendices](#appendices)

---

## Introduction & Setup

In this guide, we will build a full-stack application with **Google Login** using **Firebase Authentication** on the frontend and a **.NET Core** (C#) backend with a **PostgreSQL** database. We will cover everything from initial setup to deployment, with an emphasis on **advanced techniques** and **best practices** for security and scalability. By the end, you will have a deep understanding of integrating Firebase Auth (Google Sign-In) into a React/TypeScript app and securely communicating with a .NET backend that uses JWT verification and persists user data in PostgreSQL.

### Overview of Firebase Authentication with Google Login

**Firebase Authentication** provides a secure and easy way to handle user authentication, supporting various identity providers like Google, Facebook, email/password, and more. For Google login specifically, Firebase acts as an OAuth2 wrapper, managing the Google sign-in flow and returning a **Firebase ID token** (a JWT) that represents the authenticated user. This token can then be used to identify and authenticate the user in requests to our backend services ([How to implement Firebase Authentication with OAuth providers? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-firebase-authentication-with-oauth-providers#:~:text=1.%20Google%20Sign,firebase%2Fauth)).

**Key concepts:**

- _Firebase Project_: A container for our app's Firebase config and services. We will create a Firebase project to enable Authentication.
- _Google Sign-In Method_: In Firebase, Google Sign-In is an **OAuth2** based login. We must enable the Google provider in our Firebase project so users can sign in with their Google accounts.
- _Firebase ID Token_: After a successful Google login, Firebase issues an ID token (JWT) for the client. This token includes the user's identity (Google UID mapped to a Firebase UID, email, etc.) and is signed by Firebase. It lasts about 1 hour by default.
- _Backend Verification_: The backend (our .NET API) must verify incoming Firebase ID tokens to ensure they are valid and not tampered with. Firebase provides methods or standards (like using JWT libraries with Google's public keys or Firebase Admin SDK) to verify tokens ([How to integrate Firebase Authentication with a custom backend? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-integrate-firebase-authentication-with-a-custom-backend#:~:text=Step%205%3A%20Verify%20Firebase%20ID,Token%20in%20Backend)). Once verified, the backend can trust the user's identity and perform authorized actions (e.g., read/write to a database).
- _PostgreSQL Integration_: We will store persistent user data (e.g., profile info, application-specific settings, or session info) in a PostgreSQL database. This can include mapping Firebase user IDs to database records.
- _JWT-based Auth Flow_: We will implement a JWT authentication flow where the React app includes the Firebase ID token in requests (usually via an HTTP `Authorization: Bearer <token>` header). The .NET backend will validate this token on each request. We may also establish our own session/refresh token logic for longer sessions, but initially the Firebase token itself serves as the auth token.

Overall, the architecture looks like this (in words):

1. The user clicks "Login with Google" in the React app.
2. Firebase Authentication SDK opens a Google OAuth login popup. The user signs in with Google.
3. Firebase provides the React app with an **ID token** (and a refresh token behind the scenes) for the authenticated user.
4. The React app receives the ID token and stores the user’s auth state (for example, in React Context). It can also send this token to the .NET backend with API requests.
5. The .NET backend receives the token, verifies it’s issued by our Firebase project and not expired or revoked. If valid, the backend trusts the user’s identity (e.g., user ID, email in the token).
6. The backend can then create or update a user record in PostgreSQL (for example, storing user profile info or tracking the login) and respond to the frontend with protected data.
7. The user stays logged in. Firebase SDK will automatically refresh the ID token using the refresh token when needed, keeping the session alive. On logout, the Firebase SDK will clear the session on the client, and we can also inform the backend to invalidate any stored sessions if necessary.

This flow leverages Firebase’s secure authentication system while allowing our backend to maintain its own data and additional security (like server-side session records or roles). We get the best of both worlds: easy social login via Firebase **and** a robust custom backend with full control over data and authorization logic.

### Setting up a Firebase Project & Google Sign-In

Before writing any code, we need to configure Firebase for our application and enable Google login:

**1. Create a Firebase Project:**

- Go to the **Firebase Console** and click "Add project". Enter a project name and follow the steps to create the project (you can disable Google Analytics for now if not needed). Wait for the project to be provisioned ([Firebase auth in a React app with TypeScript](https://davidschinteie.hashnode.dev/firebase-auth-in-a-react-app-with-typescript#:~:text=1,Project)).
- Once created, you'll be taken to the project dashboard.

**2. Register a Web App in Firebase:**

- In the Firebase console, click the **Settings cog -> Project settings**. Under "Your apps", select the web icon (</>) to add a web app.
- Give it a nickname (e.g., "ReactWebApp") and register it. Firebase will provide you with a configuration object containing keys like `apiKey`, `authDomain`, `projectId`, etc. You can also set up a Firebase Hosting site now or later, but it's optional for development.
- **Important**: This config object is used by the frontend to initialize Firebase. It's safe to include in the frontend code (it's not secret), but we will still not hard-code it in multiple places. We'll store it in an environment variable or a config file.

**3. Enable Google Sign-In Provider:**

- In your Firebase project console, navigate to **Authentication -> Sign-in method**.
- You will see a list of sign-in providers. Enable **Google**. You might be prompted to specify a project support email (this is used for sending auth emails, etc., choose an email from your Google account).
- Keep the default settings for Google sign-in. By enabling it, Firebase allows OAuth using Google for this project ([How to integrate Firebase Authentication with a custom backend? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-integrate-firebase-authentication-with-a-custom-backend#:~:text=1,like%20Google%2C%20Email%2FPassword%2C%20Facebook)). Ensure the status for Google is set to "Enabled" in the console.

Now our Firebase project is ready to handle Google logins. Next, we'll set up the backend environment.

### Setting up PostgreSQL and .NET Core Backend

Our backend will be a **.NET Core Web API** that uses a PostgreSQL database. We assume you have the following tools installed on your development machine:

- **.NET SDK** (6.0 or 7.0) – for creating and running the .NET project.
- **PostgreSQL** server – either installed locally or running in a Docker container. Alternatively, you can use a service like ElephantSQL or Azure Postgres for testing, but local is fine.
- **psql** client or a DB administration tool (like pgAdmin or DBeaver) to run SQL commands or inspect the DB (optional but useful).

**1. Install and Run PostgreSQL:**

- If not already set up, install PostgreSQL (e.g., via the official installer or using Docker). On macOS/Linux, you can use `brew` or apt-get, etc.
- Make sure PostgreSQL is running. Create a new database for this project (e.g., `google_auth_demo`). Also create a user (or use the default `postgres` user) with a password and grant it access to the database.
- Take note of the connection details (host, port, database name, username, password). Typically, for local dev: host=`localhost`, port=`5432`, db=`google_auth_demo`, user=`postgres`, password=`yourpassword`.

**2. Create a .NET Core Web API Project:**

- Open a terminal and run:
  ```bash
  dotnet new webapi -n FirebaseAuthDemo.Api
  ```
  This uses the "Web API" project template. It will create a new folder `FirebaseAuthDemo.Api` with a .NET project inside.
- Alternatively, you can use Visual Studio/VS Code to create a new ASP.NET Core Web API project with the above name.
- The template includes an example WeatherForecast controller which we can remove later. For now, restore packages and ensure it builds:
  ```bash
  cd FirebaseAuthDemo.Api
  dotnet build
  ```

**3. Add Entity Framework Core and Npgsql (PostgreSQL) packages:**

We'll use **Entity Framework Core** as an ORM to interact with PostgreSQL, for ease of data access and migrations.

- Install the Npgsql EF Core provider:
  ```bash
  dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
  ```
- Install the main EF Core package (though the template might include it already):
  ```bash
  dotnet add package Microsoft.EntityFrameworkCore
  ```
- Also, add `Microsoft.AspNetCore.Authentication.JwtBearer` (for JWT auth later):
  ```bash
  dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
  ```
- And Firebase Admin SDK if we plan to use it (optional for verifying tokens, but we may not need it with pure JWT approach):
  ```bash
  dotnet add package FirebaseAdmin
  ```
  (We'll discuss when the Firebase Admin SDK is useful in the backend.)

**4. Configure the Database Context:**

- In the .NET project, create a folder `Models` and add a `User.cs` file for a user entity, and possibly a `Session.cs` if we plan to track sessions. For example, our `User` model could look like:
  ```csharp
  public class User
  {
      public string Id { get; set; }       // will store Firebase UID (string)
      public string Email { get; set; }
      public string DisplayName { get; set; }
      public DateTime CreatedAt { get; set; }
      public DateTime LastLogin { get; set; }
      // Additional fields as needed, e.g., roles, profile info, etc.
  }
  ```
  We choose `Id` as string because Firebase UIDs are strings (for Google sign-in, it's a Google user ID under the hood). We could also use GUIDs or int IDs for our own system, but using the Firebase UID directly as primary key simplifies user mapping.
- Create a `AppDbContext.cs` in a `Data` folder:

  ```csharp
  using Microsoft.EntityFrameworkCore;
  using FirebaseAuthDemo.Api.Models;

  public class AppDbContext : DbContext
  {
      public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
      public DbSet<User> Users { get; set; }
      // If we implement sessions or other entities, add DbSet for them too.
  }
  ```

- In `Program.cs` (or `Startup.cs` if using older .NET Core template), configure the DbContext in the service container:

  ```csharp
  builder.Services.AddDbContext<AppDbContext>(options =>
      options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
  ```

  Ensure you have a connection string in appsettings.json or user secrets. For example, in _appsettings.json_:

  ```json
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=google_auth_demo;Username=postgres;Password=yourpassword"
  }
  ```

  (Replace with your actual connection settings. For security, in production you'd not put the password in plain text here, but in the dev environment it's okay or use Secret Manager.)

- Run EF Core migrations to create the database schema:
  ```bash
  dotnet tool install --global dotnet-ef  # if not installed
  dotnet ef migrations add InitialCreate
  dotnet ef database update
  ```
  This should create the `Users` table in your PostgreSQL database.

At this point, we have a basic .NET backend ready, connected to PostgreSQL, and a table for users. We haven't implemented any controllers or auth logic yet – that will come in Section 3 when we integrate Firebase JWT verification and define our API endpoints.

### Creating a React TypeScript App

Now, let's set up the React frontend that will use Firebase Authentication:

**1. Create the React App (TypeScript):**

We will use Vite (or Create React App) for a quick setup. Vite is faster and modern, so let's use that:

```bash
# Using npm
npm create vite@latest google-auth-demo-client --template react-ts
# OR using yarn
# yarn create vite google-auth-demo-client --template react-ts

cd google-auth-demo-client
npm install  # install dependencies
```

This will scaffold a React project in TypeScript. If you prefer Create React App:

```bash
npx create-react-app google-auth-demo-client --template typescript
```

Either method gives a starting point with React + TypeScript.

**2. Project Structure:**

Inside the React project, you'll have a `src` directory. We will work mainly in `src/` for our app code. Plan for the following key files/folders:

- `src/firebase.ts` – to initialize Firebase.
- `src/contexts/AuthContext.tsx` – to create a React Context for auth state.
- `src/components/Login.tsx` – a login page or component with a Google Sign-In button.
- `src/App.tsx` – main app component (will include routing).
- `src/ProtectedRoute.tsx` – a component or function to protect routes (like a PrivateRoute).
- Possibly `src/pages/Profile.tsx` or other pages to demonstrate a protected resource.
- We will also manage routing (using **react-router**). Install React Router:
  ```bash
  npm install react-router-dom
  ```
  We'll use v6 which is the latest major version.

**3. Install Firebase SDK:**

Add Firebase to the React app:

```bash
npm install firebase
```

This installs the Firebase JS SDK (v9+ which uses a modular API).

**4. Firebase Configuration:**

From earlier, we have the Firebase config values (apiKey, authDomain, etc.). We should not directly hardcode them in our code. Instead, use environment variables. In React (with Vite or CRA), environment variables can be placed in a `.env` file. For example, create a `.env` (for CRA use prefix `REACT_APP_`, for Vite use `VITE_` prefix):

```
VITE_FIREBASE_API_KEY=YOUR_API_KEY
VITE_FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID=YOUR_SENDER_ID
VITE_FIREBASE_APP_ID=YOUR_APP_ID
```

Make sure to replace the placeholders with actual config from the Firebase console. (These values are not extremely sensitive by themselves but treat them carefully and _never commit real keys to a public repo_.)

**5. Initialize Firebase in React:**

In `src/firebase.ts`, initialize the Firebase app and get the Auth instance:

```ts
// src/firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Setup Google Auth Provider (we'll use this in our login function)
export const googleAuthProvider = new GoogleAuthProvider();
```

Here we export `auth` (the Firebase Auth instance) and `googleAuthProvider` which we'll use to trigger Google sign-in.

We are now ready to implement the frontend logic for authentication.

---

## Frontend Implementation (React & TypeScript)

With our React app set up and Firebase configured, we will implement the front-end functionality for authentication. This includes connecting to Firebase Auth, managing user state, handling login/logout UI, and protecting certain routes from unauthenticated access.

### Integrating Firebase Authentication SDK

**Importing and Initializing Firebase:** We already created `firebase.ts` with initialization. We should import `auth` from that file wherever we need to use Firebase Auth. The Firebase SDK provides functions to sign in, sign out, and listen to auth state changes.

**Sign in with Google:** Firebase provides a pre-built Google OAuth flow. We will use the pop-up method in our React app for a smooth UX. The SDK function `signInWithPopup(auth, provider)` handles the OAuth handshake in a popup window and returns a Promise with the user credentials if successful ([How to implement Firebase Authentication with OAuth providers? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-firebase-authentication-with-oauth-providers#:~:text=1.%20Google%20Sign,firebase%2Fauth)). Under the hood, Firebase uses the GoogleAuthProvider we set up.

For example, a simple login function using the SDK:

```ts
import { signInWithPopup } from "firebase/auth";
import { auth, googleAuthProvider } from "./firebase";

async function signInWithGoogle() {
  try {
    const result = await signInWithPopup(auth, googleAuthProvider);
    // The signed-in user info:
    const user = result.user;
    console.log("Google sign-in successful. User:", user);
    // You can also get an ID token:
    const token = await user.getIdToken();
    console.log("Firebase ID Token:", token);
    return { user, token };
  } catch (error) {
    console.error("Error during Google sign-in", error);
    throw error;
  }
}
```

This code triggers the Google login popup and, after the user authenticates, we get a `user` object which includes profile info (display name, email, etc.) and a method to get the ID token. We will use such a function in our React components (likely via context or a custom hook for auth).

**Signing out:** Similarly, Firebase SDK provides `signOut(auth)` to log the user out:

```ts
import { signOut } from "firebase/auth";
signOut(auth).then(() => {
  console.log("User signed out");
});
```

**Firebase Auth State Persistence:** By default, Firebase Auth persists the user's session in local storage, so they remain logged in even after refresh (until explicit sign out or token expiration beyond refresh). The default is "local" (permanent until sign out). This is fine for our use; we want persistent login. (Firebase also supports "session" or "none" persistence if needed.)

We will let Firebase handle token refresh automatically. The SDK uses the refresh token to get new ID tokens every hour, so the user stay authenticated without having to log in again each hour. (Firebase refresh tokens **do not expire on a time basis** – they only become invalid if the user is disabled, deleted, or password changed, etc. ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=Refresh%20tokens%20don%27t%20expire%20after,on%20managing%20user%20sessions%20says)).)

### Firebase Context and Authentication Hooks

To avoid prop-drilling user state through our component tree, we'll use React Context to provide authentication state (current user, loading status, etc.) to the entire app. This way, any component can access the auth info (like whether the user is logged in and their data) via a context hook, and we can protect routes easily.

**Creating AuthContext:**

Let's create `AuthContext.tsx` in `src/contexts`:

```tsx
import React, { useEffect, useState, useContext, createContext } from "react";
import { User } from "firebase/auth";
import { auth } from "../firebase"; // our initialized auth
import { onAuthStateChanged } from "firebase/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
}

// Create context with default (null as we will provide real context in provider)
const AuthContext = createContext<AuthContextType | null>(null);

// Custom hook to use the AuthContext
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Listen for auth state changes (login/logout)
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  // Google login function
  const loginWithGoogle = async () => {
    setLoading(true);
    // (We will implement this using signInWithPopup as shown earlier)
    try {
      // signInWithPopup returns user credentials; Firebase will handle updating auth state
      await signInWithPopup(auth, googleAuthProvider);
      // After this, the onAuthStateChanged listener will be called and update state.
    } catch (err) {
      console.error("Google login error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    await signOut(auth);
    // onAuthStateChanged will handle updating user to null
  };

  const value: AuthContextType = { user, loading, loginWithGoogle, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

A breakdown of this context provider:

- We use `onAuthStateChanged(auth, callback)` to subscribe to Firebase Auth events. This callback runs whenever the user's sign-in state changes (on login, logout, or token refresh) ([React + Firebase: A Simple Context-based Authentication Provider - DEV Community](https://dev.to/dchowitz/react-firebase-a-simple-context-based-authentication-provider-1ool#:~:text=Firebase%20offers%20us%20to%20register,about%20the%20current%20authentication%20situation)) ([React + Firebase: A Simple Context-based Authentication Provider - DEV Community](https://dev.to/dchowitz/react-firebase-a-simple-context-based-authentication-provider-1ool#:~:text=function%20CurrentUser%28%29%20,firebase.User%20%7C%20null%3E%28null)). It provides a `firebaseUser` (of type `User` from Firebase Auth) or `null` if signed out. We set our local `user` state accordingly and set `loading` to false once we have the initial state.
- We manage a `loading` state to indicate if we are still checking the initial auth state (useful to show a spinner while verifying if the user is already logged in when the app loads).
- We provide `loginWithGoogle` and `logout` functions as part of the context, which our components can call (e.g., the Login button will call `loginWithGoogle`, a Logout button in UI will call `logout`).
- We used the earlier sign-in logic inside `loginWithGoogle` (calling `signInWithPopup`). Note: We could have directly returned the user or token, but since we have the global listener, we just rely on that to set the user.
- The `useAuth()` hook simplifies consuming the context.

Now, wrap our application with `AuthProvider`. In `src/main.tsx` (if Vite) or `src/index.tsx` (if CRA), do:

```tsx
// index.tsx or main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "./contexts/AuthContext";

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
```

This ensures any component inside `<App>` can access the AuthContext via `useAuth()`.

**AuthContext in action:** Anywhere in our component tree, we can now do:

```tsx
const { user, loading, loginWithGoogle, logout } = useAuth();
```

to get the current auth state and actions. For example, in a NavBar component, we might show "Logout" button if `user` exists, or "Login" if not.

### Managing Authentication State (Context API)

The approach above leverages React Context to hold the `user` object returned by Firebase Auth. Let's discuss why this is beneficial:

- **Single Source of Truth:** The Firebase Auth service already keeps track of whether the user is signed in. By listening to it once in a context provider, we avoid having to manually pass user info through props or query Firebase in multiple components. It centralizes auth logic.
- **Reactivity:** When `onAuthStateChanged` triggers, we call `setUser`, causing any components using `user` from context to re-render with the new value (logged in or out). This means our UI will react immediately to login/logout events.
- **Global Availability:** With context, any route or component can check `user` to decide what to render. For instance, a `Profile` page can use `const { user } = useAuth();` to get the logged-in user's info or redirect if not present.

We should ensure that initially, while Firebase is checking the stored credentials (which happens very quickly on app load), we show a loading indicator. In our `AuthProvider`, we started `loading` as `true`. The `onAuthStateChanged` callback will fire even if the user is already logged in from a previous session (with the existing user or null) ([React + Firebase: A Simple Context-based Authentication Provider - DEV Community](https://dev.to/dchowitz/react-firebase-a-simple-context-based-authentication-provider-1ool#:~:text=Firebase%20offers%20us%20to%20register,about%20the%20current%20authentication%20situation)). Once it fires the first time, we set loading to false. So components can use `loading` to decide whether to show a spinner or not. We used this in our `PrivateRoute` logic (coming next) to avoid flickering content.

### Login, Logout, and Google Auth Flows

Now let's implement the UI for logging in and out, and tie everything together:

**Login Page/Component:**

We can create a component `Login.tsx` which shows a "Sign in with Google" button. When clicked, it will call our context's `loginWithGoogle` function.

```tsx
// Login.tsx
import React from "react";
import { useAuth } from "../contexts/AuthContext";

const Login: React.FC = () => {
  const { loginWithGoogle, loading } = useAuth();

  const handleGoogleSignIn = async () => {
    try {
      await loginWithGoogle();
      // After login, Firebase will handle redirect if using popups. We might want to navigate to home page.
      // If using react-router, you can use useNavigate to redirect to protected page on success.
    } catch (error) {
      console.error("Login failed", error);
      // display error to user if needed
    }
  };

  return (
    <div className="login-page">
      <h2>Welcome, please sign in</h2>
      <button onClick={handleGoogleSignIn} disabled={loading}>
        {loading ? "Signing in..." : "Sign in with Google"}
      </button>
    </div>
  );
};

export default Login;
```

Here we disable the button if `loading` is true (to prevent multiple clicks while the popup is open or auth state is being determined). When `loginWithGoogle` resolves, our context will update `user`. We likely want to redirect to a protected page after login. If using React Router, we could do something like:

```tsx
const navigate = useNavigate();
...
await loginWithGoogle();
navigate("/dashboard");
```

Alternatively, we might conditionally redirect inside the component if `user` is already logged in (so the login page is not shown to logged-in users). For simplicity, assume the router handles that (we will set up a route guard next).

**Logout:**

Wherever we have a UI for an authenticated user (like a Navbar or Profile page), we can provide a logout button:

```tsx
const { logout } = useAuth();
<button onClick={() => logout()}>Logout</button>;
```

This will call Firebase `signOut`, and our context will then set `user` to null via the `onAuthStateChanged` handler, automatically updating the UI to a logged-out state.

**Getting Firebase ID Token:** In many cases, our React app will need to call the backend API to fetch or update data after login. To authenticate these API calls, we must include the Firebase ID token in the request headers. How to get the ID token on the client:

- Firebase `User` object (from `auth.currentUser` or from the signIn result) has a method `getIdToken()`. We can call `await user.getIdToken()` at any time to get a fresh token. By default, if the current token is older than a certain threshold (e.g., nearing expiration), `getIdToken()` will automatically refresh it using the refresh token.
- We might want to attach an interceptor to all API calls to include this token. For example, if using `fetch` or axios, ensure to retrieve the token and send it.

A simple example using fetch:

```ts
async function callSecureEndpoint() {
  const token = await auth.currentUser?.getIdToken();
  const res = await fetch("https://localhost:5001/api/protected", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await res.json();
  console.log(data);
}
```

However, doing this manually for each call is repetitive. A more advanced approach is to set up a global Axios interceptor or a fetch wrapper that automatically adds the `Authorization` header if `auth.currentUser` exists.

For now, remember: **any call to our .NET API that needs authentication must send the Firebase ID token** in the headers (usually under `Authorization: Bearer ...`). The backend will validate this token as we’ll see in Section 3.3.

### Protecting Routes with Authentication Guards

We want certain parts of our React app to be accessible only to logged-in users (for example, a dashboard or profile page), and redirect users to login if they are not authenticated. This is commonly implemented with **Protected Routes** (or Private Routes).

Using React Router v6, there are a couple of ways to do this. One clean way is to create a `PrivateRoute` component that wraps child routes.

**PrivateRoute component:**

```tsx
// PrivateRoute.tsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./contexts/AuthContext";

interface PrivateRouteProps {
  children: JSX.Element;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    // While checking auth state, we can render a loading indicator
    return <div>Loading...</div>;
  }

  if (!user) {
    // Not logged in, redirect to login page
    return <Navigate to="/login" replace />;
  }

  // If user is logged in, render the protected component
  return children;
};

export default PrivateRoute;
```

Usage in routing: Suppose we use React Router's `<Routes>`:

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "./ProtectedRoute";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Home from "./pages/Home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Home />} />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
```

In this setup:

- Visiting `/profile` will render `<PrivateRoute>` first. That component checks `user`. If not logged in, it redirects to `/login`. If logged in, it renders the `<Profile />`.
- The `replace` prop in `<Navigate>` is used so that the navigation history is replaced, preventing the user from going "back" to the protected page after being redirected.
- For the login route, we might also want to prevent logged in users from seeing it (e.g., if already logged in and they manually go to /login, perhaps redirect to home). We can implement that logic inside the Login component or have a similar guard for public routes.

The context's `loading` state ensures that we don't incorrectly redirect while the auth status is still being determined on app startup. If `loading` is true, we just display "Loading..." (one could show a spinner). Once Firebase tells us if there's a user or not, `loading` becomes false and then we either redirect or show the child.

This approach is confirmed in practice: the PrivateRoute pattern is commonly used to wrap protected content ([Building a Firebase Authentication and Private Route System in a React App - DEV Community](https://dev.to/jps27cse/building-a-firebase-authentication-and-private-route-system-in-a-react-app-5203#:~:text=const%20PrivateRoute%20%3D%20%28,%3D%20useContext%28AuthContext)) ([Building a Firebase Authentication and Private Route System in a React App - DEV Community](https://dev.to/jps27cse/building-a-firebase-authentication-and-private-route-system-in-a-react-app-5203#:~:text=return%20%3CNavigate%20to%3D)). It ensures unauthorized users can't see protected pages.

**Protecting component rendering**: Even outside of routing, you might conditionally render parts of a component based on auth. For instance:

```tsx
{
  user ? (
    <button onClick={logout}>Logout</button>
  ) : (
    <Link to="/login">Login</Link>
  );
}
```

This can be done anywhere using `useAuth()` to tailor the UI.

At this stage, our frontend is capable of:

- Signing in with Google via Firebase.
- Maintaining auth state in a global context.
- Restricting access to certain routes when not logged in.
- Logging out and clearing state.

Next, we will implement the backend to accept the Firebase token and authorize requests, as well as provide APIs for user data.

---

## Backend Implementation (.NET Core & PostgreSQL)

The backend is responsible for providing secure endpoints that our frontend can call to get or modify data (e.g., user profile, app data), while validating that the user is authenticated (via the Firebase ID token) and authorized for the specific action. We will now implement:

- JWT validation in .NET using Firebase tokens.
- Controllers for auth (if needed) and for a sample protected resource.
- Saving user info to PostgreSQL when needed (e.g., on first login).
- Handling sessions or refresh tokens on the server side if we choose to maintain our own sessions.

### Initializing a .NET Core Web API Project

_(This part was covered in Section 1.3: setting up the .NET project and EF Core. We assume the project is created and database configured.)_

We have a `User` model and `AppDbContext` ready. Let's implement a controller for user-related operations, and set up authentication in the .NET app.

**Configure JWT Bearer Authentication:**

In `Program.cs` (for .NET 6+ minimal hosting model) or `Startup.cs` (for .NET 5 and earlier), we need to configure the JWT authentication scheme to accept Firebase tokens.

Add the following in the service configuration (Program.cs before `builder.Build()`):

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
// ... (other services like AddDbContext, etc.)

string firebaseProjectId = "<YOUR_FIREBASE_PROJECT_ID>";
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = $"https://securetoken.google.com/{firebaseProjectId}";
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = $"https://securetoken.google.com/{firebaseProjectId}",
            ValidateAudience = true,
            ValidAudience = firebaseProjectId,
            ValidateLifetime = true
        };
    });
```

Let's break down what this does:

- We add JWT Bearer Authentication to the ASP.NET Core pipeline. This means the app will inspect the `Authorization` header of incoming requests for a bearer token.
- `options.Authority` is set to `https://securetoken.google.com/<projectId>`. This is a special URL for Firebase Auth. By setting Authority and valid issuer/audience, we are essentially telling ASP.NET to trust tokens issued by Firebase for our project ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=services%20.AddAuthentication%28JwtBearerDefaults.AuthenticationScheme%29%20.AddJwtBearer%28options%20%3D,ValidateIssuer%20%3D%20true)) ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=ValidIssuer%20%3D%20%22https%3A%2F%2Fsecuretoken.google.com%2Fmy,)).
- When a token comes in, the JwtBearer middleware will:
  - Validate the token's signature against Google's public keys (it knows how to retrieve the public signing keys because we pointed to the Google securetoken domain as the authority).
  - Check that the token's issuer (`iss` claim) matches `https://securetoken.google.com/<projectId>` and the audience (`aud` claim) matches our project ID ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=options.Authority%20%3D%20%22https%3A%2F%2Fsecuretoken.google.com%2Fmy,id%22%2C%20ValidateAudience%20%3D%20true)).
  - Check the token hasn't expired (`exp` claim and `ValidateLifetime`).
- If all checks out, the token is considered valid and the user is authenticated. The claims from the token will be available in `HttpContext.User` in the API. If the token is invalid or missing, requests to protected endpoints will be rejected with 401 Unauthorized automatically.

With this, we **do not necessarily need the Firebase Admin SDK** to verify tokens manually. The above configuration uses standard JWT validation. (Under the hood, it likely fetches the signing keys from a well-known URI like `https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com` which is what Firebase uses for token signing.)

> **Note:** The `firebaseProjectId` is the Project ID found in your Firebase project settings (usually the same as the one in your Firebase config). It is critical to set the correct project ID, otherwise the tokens will fail audience/issuer validation.

Now, also ensure to enable authentication in the HTTP pipeline:

```csharp
var app = builder.Build();
// ... (if any middleware like app.UseCors, etc.)
app.UseAuthentication();
app.UseAuthorization();
```

The `UseAuthentication()` call must come before any endpoint handling (and before `UseAuthorization()`) ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=public%20void%20Configure,)). This enables the JWT middleware to actually validate tokens on incoming requests.

**Creating Controllers/Endpoints:**

Let's create an `AuthController` to handle login on the backend if needed. In many cases, we might not need a separate login endpoint because the client already has the token. But we may want an endpoint to exchange the ID token for, say, a session cookie or to simply verify it and get user info. Also, we might want an endpoint to handle additional user registration logic.

For example, an endpoint that the client calls right after login to ensure the user exists in our database and get a session response:

```csharp
// Controllers/AuthController.cs
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _db;
    public AuthController(AppDbContext db) { _db = db; }

    // This endpoint could be called by the frontend after a successful Google login, with the ID token in Authorization header.
    [HttpPost("login")]
    [Authorize]  // Requires a valid Firebase token
    public async Task<IActionResult> PostLogin()
    {
        // The [Authorize] attribute plus JWT Bearer config ensures this is called only if token is valid.
        // We can retrieve the user's UID and other claims from the token:
        var uid = User.FindFirst("user_id")?.Value; // Firebase JWT uses "user_id" for UID
        var email = User.FindFirst(System.Security.Claims.ClaimTypes.Email)?.Value;

        if (uid == null)
            return Unauthorized("No user ID in token");

        // Check if user exists in our DB
        var user = await _db.Users.FindAsync(uid);
        if (user == null)
        {
            // Create new user in DB if first time
            user = new User
            {
                Id = uid,
                Email = email,
                DisplayName = User.FindFirst(System.Security.Claims.ClaimTypes.Name)?.Value,
                CreatedAt = DateTime.UtcNow,
                LastLogin = DateTime.UtcNow
            };
            _db.Users.Add(user);
        }
        else
        {
            // Existing user, update last login time
            user.LastLogin = DateTime.UtcNow;
            _db.Users.Update(user);
        }
        await _db.SaveChangesAsync();

        // Optionally, generate a session token or return some info
        // For now, we just return user profile info as confirmation
        return Ok(new {
            uid = user.Id,
            email = user.Email,
            displayName = user.DisplayName,
            lastLogin = user.LastLogin
        });
    }
}
```

A few things to note in this example:

- We used `[Authorize]` on the controller action, which means the request must have passed authentication. Thanks to our JWT setup, that means it had a valid Firebase token ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=Then%20add%20auth%20into%20the,controller%20endpoint%20like%20so)).
- In the body, `User` (a property of ControllerBase) is the `ClaimsPrincipal` representing the authenticated user. Firebase tokens include a number of claims:
  - `user_id` claim holds the Firebase user UID (this is the unique identifier we want, corresponds to `firebase.auth().currentUser.uid`).
  - `email` claim (and `email_verified`) if the user has an email (Google accounts do).
  - `name` (or it might be in `firebase:name` claim depending on setup) – in the .NET claims principal, it might map differently.
  - We used `ClaimTypes.Email` and `ClaimTypes.Name`. In JWT, the Google token likely has these mapped via the JWT middleware. (We might need to inspect the token structure; but `Firebase JWT` typically has `name`, `email`, `picture` etc. as custom claims. The JWT middleware might or might not automatically map them to standard ClaimTypes.)
- We find or create a user in the database using the `uid` as primary key.
- We update `LastLogin` each time.
- We return some user info. We could also issue a custom JWT or session cookie here if we wanted our own token, but since we can just use the Firebase token for subsequent requests, this might not be necessary. Some setups might return a custom JWT if the backend wants to have its own shorter token or include additional claims (like roles).

**Protecting Other Endpoints:**

Now, any other controller we create for application data can use `[Authorize]` to secure it. For example, a `ProfileController` or any resource controller can have `[Authorize]` on class or specific actions. Inside, you can use the `User` claims to know who is calling.

For demonstration, let's say we have a simple `ProfileController` that returns the user's profile (from our DB) and allows updating it:

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]  // All actions require auth
public class ProfileController : ControllerBase
{
    private readonly AppDbContext _db;
    public ProfileController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetProfile()
    {
        var uid = User.FindFirst("user_id")?.Value;
        if (uid == null) return Unauthorized();
        var user = await _db.Users.FindAsync(uid);
        if (user == null) return NotFound("User not found");
        return Ok(new {
            uid = user.Id,
            email = user.Email,
            displayName = user.DisplayName,
            createdAt = user.CreatedAt,
            lastLogin = user.LastLogin
        });
    }

    [HttpPut]
    public async Task<IActionResult> UpdateProfile([FromBody] UpdateProfileRequest req)
    {
        var uid = User.FindFirst("user_id")?.Value;
        if (uid == null) return Unauthorized();
        var user = await _db.Users.FindAsync(uid);
        if (user == null) return NotFound("User not found");
        // Example: allow updating display name
        user.DisplayName = req.DisplayName;
        _db.Users.Update(user);
        await _db.SaveChangesAsync();
        return Ok("Profile updated");
    }
}

public class UpdateProfileRequest
{
    public string DisplayName { get; set; }
}
```

This shows typical usage:

- Ensure the user is authenticated.
- Use their UID from the token to fetch their data.
- Perform the requested operation if authorized (here any logged-in user can update their own profile name).
- We don't allow changing sensitive fields like email via this route because that should be done via Firebase (for Google login, email won't change arbitrarily).

**Testing the Auth Flow (manually):**

At this point, we have:

- Frontend that can log in and obtain an ID token.
- Backend that will accept a request with `Authorization: Bearer <idToken>` and verify it.

We should test one cycle:

- Start the .NET project (`dotnet run`) – ensure it listens on say `https://localhost:5001` (default for HTTPS).
- Use Postman or curl: get a Firebase ID token from the client (maybe log it in console as we did, or use the Network tab to see a request). Or incorporate a quick call after login to the `AuthController.PostLogin`.
- When the React app logs in, call `fetch('/api/auth/login')` with the token. Since we likely are on different domains (React dev server on 3000 and API on 5001), we must handle CORS. Make sure to enable CORS on the .NET side for your React app origin (e.g., in Program.cs: `app.UseCors(x => x.AllowAnyHeader().AllowAnyMethod().WithOrigins("http://localhost:3000"));`). For simplicity, you can allow any origin during development.
- The /login endpoint in our example returns user info. That confirms the token was accepted.
- Now calls to `/api/profile` get and put should also work with that token.

We may find that `User.FindFirst("user_id")` works because Firebase includes a claim "user_id". If not, the claim could be "sub" (subject) which often also contains the uid in Google tokens, or we might retrieve by `User.Identity.Name`. In the Firebase JWT, the `sub` claim is the UID, and many JWT libraries map `sub` to the NameIdentifier claim. So `User.FindFirst(ClaimTypes.NameIdentifier)` might give the UID in some cases ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=)). To be safe, we could check both.

For example:

```csharp
var uid = User.FindFirst("user_id")?.Value ?? User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
```

We could also inspect `User.Claims` collection in a debugger to see what's present.

### JWT Authentication with Firebase ID Tokens

We’ve essentially covered this in the previous sections, but let's recap and ensure clarity on JWT auth:

- **Why JWT (JSON Web Tokens)**: Firebase ID tokens are JWTs signed by Google. JWT is a standard that allows stateless authentication – the token itself contains the user info (claims) and a signature. The server can validate the signature (with no database lookup) and trust the data inside the token.
- **Verification Process**: The .NET `AddJwtBearer` setup uses the `Authority` to fetch the signing keys (which rotate periodically) and caches them. On each request with a token, it uses those keys to verify the token’s signature. It also checks the token's claims for issuer (to ensure it came from our Firebase project) and audience (to ensure the token was meant for our project). This is all done by Microsoft’s token handler automatically ([Setting up API authentication using Firebase JWT tokens in ASP.NET Core 3.1. · GitHub](https://gist.github.com/edijer/9eb3759b9cc92f2a9cac62154b16ee60#:~:text=options.Authority%20%3D%20%24,ValidateIssuer%20%3D%20true)).
- **No need for manual validation on each endpoint**: Because we use `[Authorize]` and JWT Bearer middleware, we don't have to manually call Firebase Admin SDK's `VerifyIdTokenAsync` in every controller. The middleware has already done it before the controller logic runs. If the token was invalid, the request would never reach our controller (ASP.NET would have returned 401).
- **Using Firebase Admin SDK vs JWT library**: An alternative approach could be to use the Firebase Admin SDK for .NET (the `FirebaseAdmin` NuGet and calling `FirebaseAuth.DefaultInstance.VerifyIdTokenAsync(idToken)`). While that works, it introduces an extra dependency and requires a service account key. It's typically used if you need additional Firebase admin features. But if your only goal is to verify the token, the JWT approach is efficient. Even Firebase’s docs encourage using a JWT library in languages where Admin SDK might not be necessary ([Verify ID Tokens | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/verify-id-tokens#:~:text=Verify%20ID%20tokens%20using%20a,can%20still%20verify%20ID%20tokens)). So our approach is aligned with best practices.

One more thing: If you plan to accept both Firebase tokens and perhaps other tokens (like your own JWTs) in the same API, you can configure multiple authentication schemes. But in our case, we stick to Firebase tokens.

### User Management Endpoints (Login, Register, Update)

**Login Endpoint:** We created `AuthController.PostLogin` that essentially acts as a "register if new" and "login" endpoint. In some applications, you might not even need this if the client can directly use the Firebase token for all calls. However, it can be useful to have an explicit login endpoint to perform first-time initialization. It can also be a place to create a server-side session or issue a custom token.

**Register Endpoint:** If we were supporting email/password via Firebase, we could have a similar flow. But since Google Sign-In handles its own account creation (there's no separate "register with Google" – the first Google login essentially creates the Firebase user), our register logic is just "create DB record if not exists", which we did in PostLogin.

If we wanted to allow non-Google users (email/password through Firebase), we'd use Firebase Auth REST API or Admin SDK on backend or call from frontend. Since our focus is Google, we won't digress into email registration.

**Update User Details:** We showed an example in `ProfileController.UpdateProfile` for updating a display name in our DB. If you wanted to allow updating the email or password, that's tricky because for Google accounts you typically cannot change the Google email from Firebase (the Google account email is what it is). For email/password accounts, you'd use Firebase's own methods (like `updateEmail` on the client or Admin SDK).

One might allow linking accounts, etc., but those are advanced auth scenarios beyond this guide's core.

Our user management in summary:

- Keep the user table in sync with Firebase accounts on login.
- Possibly provide an admin endpoint to list users or something (which would require elevated privileges, perhaps with custom claims for admin, see RBAC section).
- Provide user profile GET/PUT for the user to manage their info.

**Session Management in PostgreSQL:**

This deserves its own discussion, bridging into the next subsection too, as it overlaps with security best practices.

### Session Management in PostgreSQL

So far, our approach is stateless: every API call from the frontend includes the Firebase token. This is fine and often desirable (stateless servers scale easily). However, the prompt explicitly mentions "Storing and managing user sessions securely in PostgreSQL". This implies a scenario where we want to track sessions server-side. There are a couple of reasons to do this in an advanced app:

- **To implement manual logout on server side**: With pure JWT, if a token is not expired, there's no way to invalidate it except at the client or by Firebase revoking it (which requires using the Admin SDK to revoke refresh tokens). If we keep track of sessions (for example, store refresh tokens or a session ID in DB), we can forcibly terminate sessions (e.g., user logs out from all devices, or admin revokes access).
- **For refresh token rotation**: We might want to issue our own refresh tokens and short-lived access tokens to have more control (though Firebase already provides short-lived ID token + long-lived refresh token).
- **Audit logging**: Tracking when and from where users have logged in.

How can we implement session storage?

- One approach: store Firebase refresh tokens in the database when a user logs in. Firebase gives a refresh token when the user first signs in (accessible via `userCredential.user.refreshToken`). The client typically doesn't expose it after initial sign-in, but it is stored in local storage by the SDK. If we wanted, we could capture it on login and send it to the backend. However, **security caution**: A refresh token essentially allows generating new ID tokens. If an attacker steals it, they can impersonate the user indefinitely (until revoked). Storing refresh tokens in DB should be done in a hashed/encrypted form.
- Alternatively, create our own session token: For example, upon login, generate a random session ID or JWT, store it in a `Sessions` table with userId and expiration, and return a cookie to the client. But that starts to duplicate what Firebase does.

In an advanced scenario, we might do the following for maximum security:

- When user logs in on the frontend, call backend /auth/login with the ID token _and_ possibly device info.
- Backend verifies token, creates user if needed.
- Backend generates a secure random **session identifier** (or even a JWT signed by backend) and stores a record in a `UserSessions` table with: sessionId, userId, refreshToken (if using Firebase's), createdAt, lastSeenAt, maybe an IP or user-agent string, and an expiration.
- Backend sets an HTTP-only cookie with this sessionId or token for the client to use on subsequent requests (so the frontend doesn't manually attach Authorization header, instead cookie is sent automatically). This cookie approach can protect from XSS since it's http-only, but requires same-site or CSRF protection for requests.
- On subsequent requests, backend looks up session in DB (or if it's a JWT, it might contain the data but then we lose easy revocation).
- If using Firebase refresh tokens: The backend could periodically use the refresh token (via Admin SDK or REST call) to get a new ID token for long-lived sessions, or instruct the client to do so.
- When user logs out, backend deletes the session record from DB (and client deletes cookie).
- If user tries to use a deleted session (cookie present but not found in DB), the backend rejects and asks re-login.

This is complex and may be overkill if Firebase's own system suffices. But since the guide asks for advanced coverage, it's worth describing.

For our application, to keep it simpler, we can implement a `UserSessions` table with minimal info:

```csharp
public class UserSession {
    public int Id { get; set; }
    public string UserId { get; set; }  // foreign key to User.Id
    public string RefreshToken { get; set; }  // store securely (maybe encrypted)
    public DateTime CreatedAt { get; set; }
    public DateTime? RevokedAt { get; set; }
    public string DeviceInfo { get; set; }
}
```

We then:

- On login (AuthController): save `user.RefreshToken` (which we can get from the Firebase token by decoding? Actually, ID token doesn't contain refresh token. We would need the client to send the refresh token explicitly if we want it. The Firebase JS SDK doesn't expose refresh token via `getIdToken()`. We can only get it from `user.refreshToken` property of the user object, which is not officially in types but does exist.)
- For demonstration, let's skip storing refresh token, but we'll store a session record:
  ```csharp
  _db.Sessions.Add(new UserSession {
      UserId = uid,
      CreatedAt = DateTime.UtcNow,
      DeviceInfo = Request.Headers["User-Agent"].ToString()
  });
  await _db.SaveChangesAsync();
  ```
- Possibly return a session ID to the client. Or if using cookies, we'd set it.

However, in practice, it's often enough to trust Firebase's token rotation and not manage refresh tokens manually, unless building a very custom solution.

So, summarizing Session management:

- **We can track active sessions in Postgres**: each login creates a session record. We can use this for auditing and manual invalidation.
- **Server-side Token validation**: Already covered – always validate the token signature and claims. This ensures no session can bypass authentication.
- **Secure storage**: If storing refresh tokens or any sensitive token in DB, treat it like storing passwords (hash or encrypt them, as they are essentially secrets).
- **Cleanup**: Maybe set up a job to delete old sessions or those marked revoked.

In our guide scope, we will not implement full session tokens, but it's good to note how advanced systems can utilize the DB for session management beyond the stateless JWT.

---

## Security Best Practices

Security is paramount when dealing with authentication. Now that we have the basic functionality working, let's review and implement best practices to harden our application on both client and server sides.

### Protecting API Keys and Environment Variables

**Firebase API Key Exposure:** The Firebase config `apiKey` is included in the frontend code. It's important to understand that this API key is _not_ a secret key in the way an API secret is. It's used to identify your Firebase project on the client. It’s okay if it's public (and it will be, since frontend code can be viewed). However, **do not** check your entire Firebase config into a public repository if possible, and do not confuse this API key with server secrets. Use environment variables (which we did with Vite) to manage it, and restrict its usage in the Firebase console:

- In the Firebase console under Project Settings -> General -> Your apps, you can set authorized domains. Make sure only your dev domains (localhost) and production domain are listed. This prevents others from using your config from unauthorized origins.
- You cannot restrict the API key to certain API calls (like some Google Cloud API keys) because Firebase API keys are generic, but Firebase security rules and the auth system itself protect data.

**Environment Variables:** On the backend, keep sensitive info out of source code:

- Connection strings (with DB password) should be in configuration files that are not committed (like using `dotnet user-secrets` in development, and environment variables in production).
- Firebase Admin SDK (if used) requires a service account JSON. **Do not** include this in source code. Instead, load it from a secure location (file not in repo, or better use Google Application Default Credentials in cloud environment). Our solution didn't require it, but if we did custom operations (like setting custom claims or revoking tokens), we would need service account credentials.
- When deploying to services like Azure, use the platform's secret management to store these values.

**Securing .env files:** If you use a .env file for local dev (both frontend and backend), add those files to `.gitignore` so they aren't accidentally committed.

**Frontend Build Secrets:** If you deploy the React app, remember that any variables you embed will be visible to users. So only embed what’s necessary (again, Firebase config is fine, but nothing like an admin password, which you should never have on frontend anyway).

### Server-side Token Validation & Authorization

We've configured JWT validation, but let's reiterate best practices around it:

- **Always verify on the server**: Never trust any user info (like email or UID) coming from the client without verification. Our approach of requiring the token and validating it ensures we rely on Firebase's secure authentication. The line in Firebase docs is: _“after a successful sign-in, send the user's ID token to your server and verify it”_ ([Verify ID Tokens | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/verify-id-tokens#:~:text=Verify%20ID%20Tokens%20,the%20integrity%20and%20authenticity)) – which is exactly what we do.
- **Use built-in JWT validation**: This reduces risk of mistakes. We set the expected issuer and audience, so tokens from other projects or tampered tokens are rejected. This also covers checking token expiry automatically.
- **Validate HTTPS usage**: Ensure your backend is served over HTTPS in production. The ID token should never be sent over plaintext HTTP, or it could be intercepted. (During local dev, https://localhost is okay; if using http locally for simplicity, that's fine on localhost).
- **Leverage [Authorize] attributes**: We applied `[Authorize]` to our protected endpoints. This is declarative security. You can also create custom authorization policies (for example, require certain claims or roles) using `AddAuthorization` in ConfigureServices. For instance, if we had an "admin" claim, we could do:

  ```csharp
  options.AddPolicy("AdminOnly", policy => policy.RequireClaim("admin", "true"));
  ```

  Then use `[Authorize(Policy = "AdminOnly")]` on certain routes.

- **Principle of least privilege**: Only require auth where needed. Public endpoints (like a public info page) should not be behind auth. Conversely, everything that modifies user data or accesses personal data must require auth.

- **Token Revocation**: Consider how to handle if a user's account is compromised or if they should be forcefully logged out. Firebase allows revoking tokens by invalidating the refresh token for a user (via Admin SDK). If you suspect stolen tokens, you can use `FirebaseAuth.DefaultInstance.RevokeRefreshTokensAsync(uid)` to invalidate further use (the current ID token will expire within the hour and the user will be forced to reauthenticate) ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=Refresh%20tokens%20don%27t%20expire%20after,on%20managing%20user%20sessions%20says)) ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=)). In our DB, if we had stored refresh tokens, we could delete them to revoke access.

### Protecting Sensitive Routes & Data

Beyond auth, consider authorization at a data level:

- Our ProfileController allowed a user to fetch and update their own data by looking up by UID. We should ensure one user cannot access another user's info. Because we always use the UID from the token (which is the current user), it's safe. Do not trust an ID that comes from the client (even if they pass an ID in the request body or params, you should validate that it matches the authenticated user's ID when appropriate).
- If you have multi-user data (say an admin can access others, or a shared resource), apply proper checks. For example, if implementing an endpoint to get a list of all users, restrict it to admins (maybe by checking a custom claim or a role in DB).
- Avoid sending back more data than necessary. For instance, our profile returns email, displayName. If there were sensitive fields (like an internal role or tokens), we wouldn't send those to the client unnecessarily.

**CORS (Cross-Origin Resource Sharing):** If your frontend and backend are on different domains, configure CORS on the backend to only allow the origins you trust (your front-end URL). This prevents other websites from invoking your API with a user's credentials (important if you ever use cookies or if the token is accessible). In development, we allowed localhost. In production, set it to your domain. Example in .NET:

```csharp
app.UseCors(policy =>
    policy.WithOrigins("https://yourapp.com")
          .AllowAnyHeader()
          .AllowAnyMethod()
          .AllowCredentials());
```

`AllowCredentials()` if you use cookies; if only using Authorization header, credentials are not needed.

**Rate limiting and spam protection:** Authentication endpoints (like login) should possibly have rate limiting to prevent brute force. With Google login via Firebase, the brute forcing is on Google side (which has its protections). But if you have other auth methods (e.g., password), consider using Firebase's built-in protections or your own rate limit on the API if needed.

### Refresh Tokens and Persistent Sessions

Let's discuss refresh tokens and session persistence specifically:

- **Firebase Refresh Tokens**: As noted, Firebase ID tokens last 1 hour. The Firebase SDK on the client will automatically use the refresh token to get a new ID token when needed (this happens behind the scenes, typically before the old one expires, or when you call `getIdToken(true)` manually to force refresh ([How to integrate Firebase Authentication with a custom backend? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-integrate-firebase-authentication-with-a-custom-backend#:~:text=2.%20Retrieve%20User%20Token%3A%20,))). So from a client perspective, as long as they don't close the app for longer than the refresh token is valid (which is essentially forever unless revoked), they stay logged in.
- **Refresh Token Expiration**: Firebase refresh tokens, by default, do not expire on a time basis ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=Refresh%20tokens%20don%27t%20expire%20after,on%20managing%20user%20sessions%20says)). They remain valid until one of the conditions (user disabled/deleted, account change) occurs, or until you revoke them manually ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=But%20you%20can%20revoke%20the,tokens%20for%20more%20on%20that)). This means a user who logged in once can come back days or weeks later and still be logged in (which is user-friendly).
- **Security of Refresh Tokens**: These are stored in the browser (local storage or indexedDB by Firebase). XSS attacks could potentially steal them, which is why you must guard against XSS. One best practice is to use the Firebase **session cookies** feature for web apps: you can exchange an ID token for a long-lived HTTP-only session cookie via the Admin SDK ([Manage User Sessions | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/manage-sessions#:~:text=Google%20firebase,when%20one%20of%20the)). That cookie acts similar to a refresh token but is HttpOnly, mitigating XSS risk. Implementing that would mean the client after login calls the server, the server uses Admin SDK to create a session cookie from the ID token, sets it in response. Then client can rely on that cookie for auth. This is advanced, so as an exercise, know it's possible.
- **Our approach**: We'll rely on the default token/refresh mechanism. If the user closes the tab and reopens, Firebase will retrieve the saved refresh token and get a new ID token (onAuthStateChanged will fire accordingly).

- **Persistent login**: Achieved via refresh tokens as above. To further ensure persistence after, say, a server restart, since we are stateless JWT, nothing on server is lost anyway. If we had a session table and our own session tokens, we might want to also implement refresh for those (like rotating our JWTs, etc., but we won't go that far here).

**Storing Session in DB**:

- If we implement the sessions table, we can mark sessions as active. But we should also have a plan to clear old sessions (for example, if we consider a session expired after X days of inactivity, we should prune those).
- If security policy requires, we could expire refresh tokens after a time. Since Firebase doesn't expire them by time, we could enforce our own rule: e.g., after 30 days, require full re-login (you can achieve this by revoking on Firebase side or by not accepting old session entries).

### Optimizations and Enhancements

Having a functional product is step one; optimizing it for performance, maintainability, and extra features is step two. Let's explore some enhancements and improvements we can add.

#### Performance Improvements

**Frontend Performance:**

- _Lazy loading Firebase:_ The Firebase SDK is modular, but it's still a chunk of code. If auth is needed on almost all pages, loading it upfront is fine. Otherwise, consider code-splitting Firebase-related code. For example, if the landing page doesn't require auth, only load firebase/auth when the user navigates to login or when needed.
- _Minimize re-renders:_ Using context and a single state for `user` helps, but be mindful that every time `user` changes, any component using `useAuth()` re-renders. This is expected for login/logout events (which are infrequent). Just avoid putting huge components inside context provider that might rerender often. Our context is at top, so it's fine.
- _Batch state updates:_ If you had more state in AuthContext (like roles, etc.), update them in one `setState` call if possible to avoid multiple re-renders.

**Backend Performance:**

- _Database Indices:_ Ensure `User.Id` (UID) is primary key or indexed for fast lookup. For sessions, index by `UserId` as well if you often query by user.
- _Connection Pooling:_ .NET and Npgsql handle pooling by default. Ensure you're not opening too many connections. Our usage with EF Core is fine.
- _Minimize external calls:_ We did not introduce extra external calls on backend (like to Firebase Admin every time) thanks to JWT verification offline. If we were calling Firebase for each request, that would be slower. So we chose the optimal approach.
- _Caching:_ In some cases, you might cache user data after the first DB lookup. E.g., once you verify a token and get user from DB, you could cache the user info in memory or a distributed cache for subsequent requests within a short time window to avoid repeated DB hits for the same user. But careful: user info could change (like roles), so cache invalidation strategy is needed. For high throughput systems, this could help.
- _Batching requests:_ If the client needs to call multiple endpoints on load (for profile, for settings, etc.), consider providing a combined endpoint or use GraphQL. Not directly related to auth, but improves perceived performance.
- _Serving Static Content:_ If you eventually serve the React app from the .NET server, use response compression and proper caching for static files.

#### Error Handling and Logging

Robust error handling makes debugging and maintenance much easier:

**Frontend:**

- In our `loginWithGoogle` function, we catch errors and `console.error`. In a real app, you might show a user-friendly message. Firebase errors have codes (e.g., popup_closed_by_user, network-request-failed, etc.). Handle common ones to guide the user (maybe they blocked the popup, etc.).
- For protected routes, if an API call returns 401 (unauthorized) perhaps because token expired or backend didn't accept it, you should handle that. The Firebase token might have expired if the user was idle and refresh failed. In such case, prompt them to login again. You can use an interceptor to catch 401 responses globally and do something (like redirect to /login).
- Use try/catch around API calls and inform the user when something goes wrong (while also possibly logging to an external service for serious errors).
- Logging: For advanced debugging, you could integrate a client-side logging tool or use console logs liberally in dev. But remove or lower the verbosity in production.

**Backend:**

- Use a logging framework (the default `ILogger` in ASP.NET Core). Log important events:
  - Log when a login endpoint is hit, maybe info level "User X logged in".
  - Log warnings for suspicious activities (e.g., if an invalid token is received repeatedly, log it).
  - Log errors with stack traces for unexpected exceptions (like DB failures).
- Implement global exception handling middleware or use the built-in Developer Exception Page in dev. In production, ensure unhandled exceptions don't leak sensitive info. By default, .NET Core does not include stack trace in production responses, which is good.
- Return proper HTTP status codes: e.g., 401 for unauthorized, 403 for forbidden (if user is authenticated but not allowed), 400 for bad inputs, 500 for server errors, etc. Our examples mostly returned 401/404 appropriately.
- Validate request bodies on update endpoints (in UpdateProfile, we should validate that DisplayName is not too long or empty, etc., to avoid bad data).
- Consider using FluentValidation or DataAnnotations for model validation on inputs, and return errors accordingly.

**Monitoring**: In production, use monitoring tools (Application Insights, etc.) to keep track of authentication metrics – e.g., number of logins, errors, etc.

#### Role-Based Access Control (RBAC)

In many applications, not all authenticated users are equal—some might be "admin" or have specific roles/permissions. Firebase Authentication by itself doesn't have roles, but we can implement it:

**Using Firebase Custom Claims:**
Firebase allows assigning custom claims to a user via the Admin SDK. For instance, you can set a `admin:true` claim on certain users ([How to implement a custom claims-based authorization in Firebase? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-a-custom-claims-based-authorization-in-firebase#:~:text=Step%203%3A%20Define%20Custom%20Claims)) ([How to implement a custom claims-based authorization in Firebase? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-a-custom-claims-based-authorization-in-firebase#:~:text=,)). Once set, any new ID token the user obtains will contain that claim. This is a powerful way to embed roles in the JWT that the backend will receive.

How to set a custom claim:

- Use the Admin SDK in a secure environment (your server or a Cloud Function) to call `FirebaseAuth.SetCustomUserClaimsAsync(uid, new { role = "Admin" })` or similar.
- Once set, you might need the user to re-login or refresh their token to get the new claim.

If we go this route, our .NET JWT validation will include those claims in `User.Claims`. For example, there might be a claim `role: Admin`.

We would then enforce it:

- In .NET, configure `TokenValidationParameters.RoleClaimType` and `.NameClaimType` if needed. By default, it might not map "role" to ClaimsIdentity.Role. We can do:
  ```csharp
  options.TokenValidationParameters = new TokenValidationParameters {
      // ... existing settings
      RoleClaimType = "role"
  };
  ```
  Then we can use `[Authorize(Roles = "Admin")]` on controllers, which will check the "role" claim ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=ValidIssuer%20%3D%20%22https%3A%2F%2Fsecuretoken.google.com%2Fmy,)) (if the JWT middleware maps it properly).
- Alternatively, skip the above and just manually check claims: e.g.,
  ```csharp
  if (User.Claims.Any(c => c.Type == "role" && c.Value == "Admin")) { ... }
  ```
  or use policy:
  ```csharp
  options.AddPolicy("AdminOnly", policy => policy.RequireClaim("role", "Admin"));
  ```
  then `[Authorize(Policy="AdminOnly")]`.

**Using Database Roles:**
Another approach is to store roles/permissions in your database (e.g., a column in Users or a separate table if many-to-many roles). Then:

- When a request comes, you have the user UID, you fetch the user's roles from DB. This could be done on each request (which is a performance hit) or cached. Or done at login time and stored in a session token.
- For example, your `User` table could have an `IsAdmin` boolean or a `Role` string. In the login process or in a custom JWT, you could include that. If not using custom JWT, you'd check in each relevant endpoint.

One way is to combine approaches: when user logs in, set a Firebase custom claim for role from the database. But to set a custom claim, you need admin privileges. Our backend could do it since we have the Admin SDK and service account. This would sync Firebase token with DB roles, but custom claims might take a few minutes to propagate.

For advanced RBAC (like fine-grained permissions), you might maintain it entirely in your backend logic.

**Client-side usage:** If you have roles, you may also use them on the client to conditionally render admin UI. But never rely solely on client-side checks for security (the server must enforce it).

For example, if `user` in context has a claim `role: admin`, you could show an "Admin Panel" link. But still, the admin API endpoints should verify the user is admin on the server side.

**Summary**: Implementing RBAC involves:

- Determining how to store/assign roles (Firebase custom claims or DB).
- Propagating that info to the token or fetching it in requests.
- Using `[Authorize(Roles="...")]` or policies in .NET to protect endpoints.
- Providing an interface to assign roles (maybe an admin page where an admin can designate another user as admin, which would call a function on backend to set custom claim or update DB).

#### Multi-factor Authentication (MFA) and Extra Security

Multi-factor authentication adds an additional layer (like an OTP code or push notification) on top of password or primary login. With Google sign-in, the user might have 2FA on their Google account (like Google prompt or SMS) – if so, they will complete that during Google login. We don't have to implement anything special to support that; it's handled by Google.

However, Firebase Authentication itself introduced multi-factor support for SMS in late 2020, but it's only available if you upgrade to **Identity Platform** (a paid service) ([Firebase Authentication with multi-factor authentication - Stack Overflow](https://stackoverflow.com/questions/52886244/firebase-authentication-with-multi-factor-authentication#:~:text=From%20March%2012%2C%202020%2C%20It,authentication%20to%20your%20web%20app)) ([Firebase Authentication with multi-factor authentication - Stack Overflow](https://stackoverflow.com/questions/52886244/firebase-authentication-with-multi-factor-authentication#:~:text=4)). If using that, you could enforce that after a user logs in (with email/password, or even possibly Google?), they have to also pass an SMS code.

Given our use-case (Google login), typically you wouldn't add an extra MFA on top of Google login via Firebase _within the app_. If you needed MFA, you'd rely on the Google Account's MFA.

For completeness: if we had email/password auth and wanted MFA, we could:

- Enable MFA in Identity Platform,
- The front-end would then use Firebase's MFA enrollment and verification APIs (like `multiFactor()` methods).
- Or do something like send an OTP and verify it before marking user as fully authenticated.

This gets complex and is beyond the scope for now. We simply acknowledge:

- MFA improves security by requiring a second factor (something the user has).
- It's highly recommended for sensitive applications or admin accounts.

**Additional Security Layers:**

- **Email Verification**: If using email/password, ensure the user’s email is verified. Firebase can send verification emails. For Google, emails are usually verified by default (Google provides verified email).
- **Monitoring and Alerts**: Monitor for suspicious login patterns (many attempts, logins from new locations, etc.) and possibly alert users (Google does some of this on their own).
- **Secure Data Storage**: On the server, secure sensitive fields. For example, if storing refresh tokens, consider encryption. If storing any personal user data, ensure your DB and backups are encrypted.
- **Regular updates**: Keep Firebase SDK, .NET, and all libraries up-to-date for latest security patches. Also update your Firebase project settings as needed (e.g., if any vulnerability discovered, Google will update something).
- **Content Security Policy (CSP)**: On the front-end, implement CSP headers to mitigate XSS by only allowing scripts from trusted sources. Also consider other OWASP front-end security practices (like sanitizing any data that might be rendered, though with React's default escaping, you're relatively safe from XSS unless you dangerously set HTML).
- **Preventing CSRF**: If you move to using cookies for auth, implement CSRF tokens or SameSite cookie attributes to protect endpoints like logout or others from cross-site requests. With our approach (token in header), CSRF is less of an issue because an attacker from another site cannot read the token from JS (if using httpOnly cookie they can send but not read, if using local storage token, an XSS would be needed to get it which is a different threat).

---

## Testing and Debugging

With functionality and security in place, we need to test our implementation thoroughly and be equipped to debug issues that arise. We'll cover strategies for testing both on the client and server, as well as common issues and how to resolve them.

### Unit Testing Authentication Flows

**Front-end Unit Tests:**

For React components and hooks, you can write tests using Jest and React Testing Library.

- Test the `AuthContext` provider: You can simulate various auth states by mocking Firebase Auth functions. For example, you might mock `onAuthStateChanged` to call its callback with a fake user or null and ensure that context `user` value changes accordingly.
- Test components like `PrivateRoute`: You can render it with a dummy child and a mocked context value. For example, wrap PrivateRoute in a context provider with `user=null` and ensure it navigates to login (you might need to use `MemoryRouter` for routing context in tests).
- Test the login flow: This is tricky as it involves the popup. Instead, you might abstract the `loginWithGoogle` function to be injectable or mockable. Perhaps test that clicking the button calls `loginWithGoogle` and that `loginWithGoogle` when resolved triggers a navigation. Many will treat this as an integration test rather than pure unit, because it spans context and routing.
- If using a library like Cypress for end-to-end, you can simulate a login by actually clicking and going through the Google OAuth (there are ways to stub it, or in a testing environment, use Firebase Auth emulator which can simulate the sign-in without actual Google accounts).

**Back-end Unit Tests:**

You can use xUnit or NUnit for testing controllers and services in .NET.

- **Testing JWT validation**: Instead of trying to generate a real Google token, you might bypass the actual [Authorize] and test the logic inside. One approach is to unit test your services (like a hypothetical service method that takes a UID and does DB operations). But to test the authentication attribute itself, that's more of an integration test.
- For controllers, one strategy is to create a fake `ClaimsPrincipal` with the needed claims and attach it to the controller's `User` property, then call the action method directly. For example, in a test, do:
  ```csharp
  var controller = new AuthController(...);
  controller.ControllerContext = new ControllerContext {
      HttpContext = new DefaultHttpContext {
         User = new ClaimsPrincipal(new ClaimsIdentity(new [] {
             new Claim("user_id", "testuid"),
             new Claim(ClaimTypes.Email, "test@example.com")
         }, "TestAuth"))
      }
  };
  var result = await controller.PostLogin();
  Assert.IsType<OkObjectResult>(result);
  ```
  This bypasses JWT validation and directly injects a user context.
- You should also test scenarios like "new user gets created in DB", "existing user gets updated", etc., by seeding an in-memory database (use `UseInMemoryDatabase` option for EF Core in tests).
- Test the ProfileController: similar approach, ensure that without auth (or with a missing claim) it returns Unauthorized, with proper claims it returns expected data.

**Edge cases to test:**

- Token expired scenario: You could simulate it by using an expired token (if you have one) or by mocking the JwtBearer events. But easier is an integration test (coming next).
- Malformed token: ensure the API returns 401.
- User not in DB (first login) vs in DB (subsequent login).
- Concurrent logins (same user logging in from two devices) – should both create sessions? Our code would create duplicate DB entries in that case. Maybe we allow that and have multiple session records.

### Integration Testing Secure API Endpoints

Integration testing means testing the system end-to-end or at least multiple layers together:

**Using Firebase Auth Emulator:**
Firebase offers an Authentication Emulator which you can run locally. This emulator can create test users and generate tokens. A great advantage is that it can produce a Firebase ID token that your backend will accept, without needing real Google accounts.

- Start the Auth emulator (via Firebase CLI or as part of the Firebase emulators suite).
- Create a fake Google user in the emulator or simply use an email/password test account.
- Sign in via the emulator (there's a REST API or Admin SDK can create custom tokens for emulator).
- Get an ID token and call your local API with it.

However, an easier approach if not using emulator:

- Use the real Firebase, but in a test environment (maybe a separate project). You can use Firebase Admin SDK in your test code to mint a custom token or verify an ID token. Actually, Admin SDK can create a custom token which then can be exchanged for an ID token via REST. This is complex for a test.

Alternatively:

- Use a tool like **Postman**: Manually do the Google OAuth (or use Firebase Auth REST API to login with a test Google account) and get back an ID token, then call your endpoints.
- Or use a library to simulate JWTs: Because our backend trusts any JWT signed by Google (with appropriate issuer/audience), we could cheat in integration tests by generating a JWT signed with our own key but skipping signature validation. One could disable `ValidateIssuerSigningKey` in the TokenValidationParameters for tests and just supply any token with correct claims. But that's not a true integration test of the production behavior.

**Automated Integration Test Example (with WebApplicationFactory in ASP.NET Core):**

You can spin up the API in memory and send HTTP requests to it using a test client:

- Use `Microsoft.AspNetCore.Mvc.Testing.WebApplicationFactory<Startup>` to create a test server.
- Override the authentication: For instance, you could create a fake authentication handler that automatically authenticates requests (to bypass actual JWT). For example, in the test Startup configuration, replace JWT bearer with a dummy scheme that accepts a preset user. Microsoft docs have examples of testing with a fake scheme.
- Then use `HttpClient` to call the endpoints and verify responses.

While this won't test the actual JWT validation logic (since we bypassed it), it tests that once authenticated, the endpoints work.

To test actual JWT path, you'd need a valid token:

- Possibly fetch one at runtime from Firebase: There are REST endpoints for Firebase Auth, or we can use the Admin SDK to verify our approach:
  - Use Google APIs client to fetch a custom token.
  - Exchange custom token for ID token via `signInWithCustomToken` endpoint.
  - Use resulting ID token in test calls.

Given time, many might just test with a dummy scheme or focus on unit tests for logic, and assume JWT middleware works as it's a library feature.

**Front-end Integration/E2E:**

- Use Cypress or Selenium to run the app in a browser:
  - Test the login UI: click "Sign in with Google". Doing a real Google login in an automated test is tricky (you'd need to input Google credentials or have a stub).
  - Alternatively, if using Firebase emulator auth, you could embed a custom login method in test mode (like a special button to auto-login a test user without Google flow, only in test environment).
  - Test that after login, protected page content is visible, and if not logged, redirect occurs.

### Debugging Common Authentication Issues

Even with everything set up, you might run into issues. Here are some common ones and how to address them:

**1. Google popup blocked / not opening:** Browsers may block the sign-in popup if it's not triggered by a user gesture. Ensure the login function is called in a button onClick handler (which we did). If you see nothing when clicking, check browser console for popup blocker warnings. Also, ensure no double-click issues or that you call `signInWithPopup` only once.

**2. Firebase config errors:** If `initializeApp` is given wrong config, you might see errors like "auth/invalid-api-key" or "auth/domain-config-required". Make sure the API key and authDomain match what's in Firebase console. Also, ensure the domain you are running the app on (e.g., localhost) is in the authorized domains in Firebase console; otherwise, you'll get an error when trying to sign in.

**3. onAuthStateChanged not firing or user null:** If after sign-in you don't get a user, possibly the signInWithPopup didn't resolve, or the Auth instance might be different (make sure you use the same `auth` from initialization everywhere; using two different Firebase app instances can cause confusion). Also, check if there are any errors in the sign-in promise.

**4. Token not sent to backend:** If your API calls are not including the token, ensure you are actually retrieving it and setting the header. If using fetch, remember to include `{ credentials: 'include' }` if using cookies, and proper headers if using Authorization. For axios, set default Authorization header after login.

**5. CORS errors:** If the browser console shows CORS errors (e.g., "No Access-Control-Allow-Origin header"), then your backend didn't allow the frontend origin. Fix the CORS policy on backend to allow the dev origin (and in production, allow the production origin).

**6. 401 Unauthorized from backend:**

- Check the Authorization header format. It should be `"Bearer <token>"`. If you forget "Bearer", the JWT middleware won't pick it up.
- Check the token itself: decode it at jwt.io to see claims. Is the `aud` matching your Firebase project ID? (It should). Is `iss` correct? (Should be "https://securetoken.google.com/yourproject"). If not, you might have a token from a different project or an error.
- Check backend logs: We can enable logging for JWT events. For example, in AddJwtBearer, we can add:
  ```csharp
  options.Events = new JwtBearerEvents {
      OnAuthenticationFailed = ctx => {
          Console.WriteLine("Token failed validation: " + ctx.Exception.Message);
          return Task.CompletedTask;
      },
      OnMessageReceived = ctx => {
          Console.WriteLine("Token received: " + ctx.Token);
          return Task.CompletedTask;
      }
  };
  ```
  This can help see if token is being received and if there's a specific error (like signature validation failed or audience mismatch).
- Ensure the system clock of the server is correct. If the server time is far off, `ValidateLifetime` might reject tokens as expired/not yet valid. (This usually isn't an issue in modern environments, but worth noting).

**7. Multiple [Authorize] policies not working:** If you try to use roles or multiple schemes, ensure you configured them correctly. For roles, the claim type must match.

**8. Firebase Admin issues:** If you attempted using FirebaseAdmin and had trouble, double-check the service account JSON and environment. But since we stuck to JWT, less likely.

**9. Database issues:** If user creation fails, see error (maybe constraint issues, etc.). Use migrations properly. Also ensure your DB is running.

**10. Logout issues:** If the user clicks logout but remains logged in: maybe you didn't actually call `signOut(auth)` or the state didn't update. Check that the AuthContext is handling logout. If using cookies for session, ensure cookie is cleared.

**Debugging Tools:**

- Browser DevTools for network requests (see if the auth header is present, see responses).
- Postman to simulate requests with tokens (you can paste the Firebase token into Postman Auth header to test).
- Firebase console has a "Users" section to see registered users; check if your Google login created a user there (it should). This helps confirm the frontend is indeed connecting to the correct project.
- Logging on server as mentioned.
- Use `jwt.io` or similar JWT decoder to inspect token contents quickly during dev.
- If using emulator, use its UI to observe events.

---

## Deployment & Scaling

Finally, after development and testing, we need to deploy the application to a production environment and ensure it can scale to meet demand. We will discuss deploying both the React frontend and the .NET backend, setting up CI/CD pipelines, and considerations for scaling.

### Deploying the React Frontend (Firebase Hosting/Vercel)

**Firebase Hosting:**
Since we already use Firebase for Auth, an easy choice is Firebase Hosting for the React app:

- In Firebase console, add Firebase Hosting to your project (if not already).
- Install Firebase CLI (`npm install -g firebase-tools`), login (`firebase login`).
- Inside your React project directory, run `firebase init hosting`. Follow prompts: use existing project, specify `build` folder as the public directory (since CRA or Vite build output goes to `build` or `dist`; for CRA it's `build`, for Vite default is `dist` - adjust accordingly). Configure as SPA app (yes to single-page app rewrite).
- Build your app: `npm run build`. This produces a production build.
- Deploy: `firebase deploy --only hosting`. It will upload the static files to Firebase CDN. After deploy, you'll get a Firebase subdomain (like `your-project.web.app`) and if configured, a custom domain.

Firebase Hosting is global and fast, and your app will be served securely over HTTPS. It also supports HTTP/2, etc., out of the box. Since our app calls an API on another domain (the .NET backend), ensure you have configured CORS on the backend to allow the Firebase hosting domain.

**Vercel (or Netlify):**
Alternatively, you can use Vercel or Netlify which are great for React apps:

- Push your code to GitHub.
- On Vercel dashboard, create a new project linked to the GitHub repo. It auto-detects React (or you can specify build command `npm run build` and output directory `build` or `dist`).
- Set environment variables in Vercel for the Firebase config (like VITE*FIREBASE_API_KEY, etc. if using Vite, or REACT_APP*... if CRA).
- Deploy. Vercel will provide a domain and you can add custom domain if you have one.
- Vercel also supports automatic deployments on git push, making it easy to continuously deploy front-end changes.

**Environment Config in Prod:**
Make sure you set the correct Firebase config for production if it differs (usually same project for simplicity). Also, update any API URLs. In development, you might call API at `http://localhost:5000`. In production, your API might be at a different URL (like an Azure/AWS domain). You can use environment variables for the API base URL and configure them in the build.

For example, in React .env: `REACT_APP_API_URL=https://api.yourdomain.com`. Use that in fetch calls.

**Security on Hosting:**

- Enable HTTPS only (Firebase does by default).
- Optionally, set up CSP meta tags or headers in hosting config.
- If using service workers or any caching, ensure tokens are not cached in browser incorrectly (but since tokens are in headers, caching static assets is fine).

### Deploying the .NET Core Backend (Azure/AWS/DigitalOcean)

You have many options to host a .NET Core API and a PostgreSQL database in production. We'll outline a few:

**Azure App Service + Azure Database for PostgreSQL:**

- Create an App Service for Linux, choose a .NET runtime. Or use a container (App Service can also run Docker containers).
- Publish your .NET app to Azure (via Visual Studio Publish wizard or GitHub Actions or Azure DevOps pipeline).
- Azure provides a Connection Strings configuration where you can put your connection string. You can also set environment variables like `ConnectionStrings__DefaultConnection` via the Azure Portal, which your app will use.
- For the database, Azure has a managed PostgreSQL service. Provision one, and update the connection string accordingly. Ensure the App Service can reach the DB (set up VNet or allow Azure services in DB firewall).
- Also set environment variables for any secrets (like if you use Firebase service account for some reason, you'd store that differently, maybe in Key Vault).
- Ensure your app is configured for production: e.g., ASPNETCORE_ENVIRONMENT = "Production" (so detailed error pages are off).
- The .NET app will be accessible at some URL (like `https://yourapp.azurewebsites.net`). Make sure your Firebase Authorized Domain includes this if you call Firebase from server (not needed for verifying tokens).
- If using Azure, consider Application Insights for monitoring.

**AWS (Elastic Beanstalk or ECS or Lambda):**

- Elastic Beanstalk can host .NET apps easily; you upload the published output or even the project and AWS handles deployment.
- Alternatively, build a Docker image for the .NET API and run it on AWS ECS (Fargate) or even AWS Lambda (with a tool like AWS Lambda .NET, but that's advanced).
- Use Amazon RDS for PostgreSQL as the database.
- AWS Amplify or S3+CloudFront could serve the React app (if not using Firebase Hosting).
- Setup environment variables in the EB environment or ECS Task Definition for config.

**DigitalOcean (Droplet or App Platform):**

- On a simple VM (droplet), you can Dockerize the app or run it directly. You'd have to manage Nginx or Caddy as a reverse proxy to handle TLS (if not using Kestrel's built-in TLS, though you can).
- DO App Platform supports Docker and might even directly support .NET apps.
- Use DO Managed PostgreSQL for the database.

**Dockerizing the App:**
A modern approach: create a Dockerfile for the .NET API:

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:7.0-alpine AS runtime
WORKDIR /app
COPY ./publish-output ./  # after building and publishing your app
ENV ASPNETCORE_URLS=http://+:80
ENV ConnectionStrings__DefaultConnection=${ConnectionStrings__DefaultConnection}
# (Environment variables can be passed in via docker run or Kubernetes secrets)
ENTRYPOINT ["dotnet", "FirebaseAuthDemo.Api.dll"]
```

And one for build if needed, etc. Then you can run this container anywhere. Ensure to use secure ways to supply DB password (like secrets or env vars in the orchestrator).

**PostgreSQL deployment:**

- If self-hosting DB, be cautious about backups, replication, etc. A managed DB is often safer (less DevOps overhead).
- Ensure the DB is not open to the world; allow only the app server to talk to it (use firewall rules or security groups).
- Set a strong password for the DB user.
- Apply latest patches to Postgres.

**Domain and SSL:**

- For the API, it's good to have it on a custom domain (api.yourapp.com). Use something like Let's Encrypt for SSL if not already provided by the platform. Azure/AWS often provide a default certificate on their subdomain; for custom domains, you'd manage TLS (Azure has easy certificate binding, AWS you can use Certificate Manager + CloudFront or ALB).
- The React front-end if on Firebase gets a free SSL on the `.web.app` domain; for custom domain, Firebase can also provide a certificate via Let's Encrypt integration.

**Setting up Backend environment for Firebase:**

- Although we didn't heavily use Firebase Admin, if in future you do (for sending FCM messages or extra auth admin tasks), you'd need to provide service account creds. Typically, on Google Cloud (Firebase is Google Cloud under the hood), the recommended way is to deploy your .NET API on Cloud Run or GKE and attach a service account. But on Azure/AWS, you'd store the service account JSON in a secure place and load it. Or simply rely on REST APIs with the API key for limited stuff.
- In our case, no need as we just trust JWTs.

### CI/CD Pipeline Setup

To automate deployments, set up CI/CD:

**GitHub Actions (for example):**

- For the React app: Use a workflow that triggers on push to main (or when ready to deploy). Steps:
  1. Checkout code.
  2. Install Node, npm ci.
  3. Build the app (`npm run build`).
  4. Deploy: If using Firebase Hosting, use the Firebase Action which requires FIREBASE_TOKEN (generate via `firebase login:ci`). If using Vercel, you might rely on Vercel's Git integration rather than GitHub Action. For Netlify, there's a deploy action or use their linking.
  5. Alternatively, deploy to an S3 bucket + CloudFront, etc., if doing manually.
- For the .NET API: Another workflow:
  1. Checkout, setup .NET.
  2. Build and run tests (`dotnet build`, `dotnet test`).
  3. Publish the app (`dotnet publish -c Release -o publish-output`).
  4. (Optional) Build Docker image (`docker build -t yourapp:latest .`).
  5. Deploy: If Azure Web App, use the Azure WebApp action (needs credentials set in secrets). If Docker, push to Container Registry and then trigger a deployment (like update Kubernetes or notify App Service or ECS, depending on setup).
  6. Alternatively, use FTP/SSH for a simple server (not ideal for CI).
- Use secrets in GitHub Actions for sensitive data (like API keys for deploy, or connection strings if needed).

**Azure DevOps or others**: Similarly, set up pipelines to build and deploy. Azure DevOps has tasks for Azure WebApp, etc.

**Testing in CI**: You can also run the integration tests as part of pipeline. Perhaps have a step to start a test Postgres (use Docker to run `postgres:alpine` for example, set connection string to it) and run your tests.

**Notifications**: Have the CI/CD send notifications on failures (email or Slack) so you know if a build or deploy fails.

### Scaling for High-Traffic Applications

Designing for scale ensures that as your user base grows, the application remains responsive and stable.

**Scaling the Frontend:**

- Firebase Hosting and CDNs in general handle scaling automatically. Firebase Hosting can serve a very high number of concurrent requests, with assets cached globally.
- If using Vercel/Netlify, they also scale transparently for static sites.
- So the main concern is the backend and the database.

**Scaling the .NET Core API:**

- .NET Core APIs can scale out (multiple instances behind a load balancer). If using Azure App Service, you can enable autoscaling (scale out by CPU or other metrics).
- If using containers, you might deploy to Kubernetes or an auto-scaling group in AWS ECS.
- Because we used JWTs statelessly, any API instance can handle any request (no session affinity needed). This is good for horizontal scaling.
- One caveat: if we had implemented a session store or something, multiple instances need to access a common session store (like the PostgreSQL we planned or a distributed cache). In our design, the session info is in Postgres, so all instances can query it. If we used in-memory session, that would break in multi-server scenario (so we avoid that).
- Monitor CPU, memory of app instances. Crypto (JWT signature checking) is quite efficient, but heavy usage might increase CPU – ensure instances are scaled timely.
- Use caching strategies if needed: e.g., if certain user data is read often and rarely changes, an in-memory cache or distributed cache can reduce DB load. But be cautious to not cache stale auth info.
- Consider using a reverse proxy or API gateway for features like request throttling, caching, or SSL offload. Azure API Management or AWS API Gateway could front your API if needed (though not required).

**Scaling the PostgreSQL database:**

- The database is a stateful service and often a bottleneck. Strategies:
  - Choose the right instance size (CPU, RAM) for your expected load.
  - Enable connection pooling and set max connections wisely. Too many connections can harm performance; use a pooler like PgBouncer if needed.
  - If read traffic heavy, consider read replicas for Postgres (available in cloud providers) and direct read-only queries to replicas. But with our simple app, reads/writes are both low volume (just user info).
  - Use indexing (already did for UID) to make queries fast. Our queries are simple primary key lookups, which is fine.
  - If you eventually accumulate lots of session logs or audit logs, consider archiving old data out of the main tables to keep them slim.
  - Monitor DB metrics: CPU, disk I/O, connections, slow queries. Optimize queries if needed (maybe not an issue here).
  - In extreme scale cases, you might consider sharding or moving some data to NoSQL, but that’s beyond our scope.

**Handling spikes in auth traffic:**

- Firebase Authentication itself (the Google side) can handle large volumes of sign-ins. But if you expect a spike (like thousands of users logging in at once):
  - Your backend verifying tokens might see a spike. The JWT validation library will cache the Google public keys and reuse them, so that's fine. The processing of each token is usually milliseconds. 1000 logins at once should be okay on a moderately sized server, but you can scale out.
  - Database writes (creating many new users at once) – ensure that is optimized (maybe use batch insert if ever needed, although usually users trickle in).
  - Use queue or backoff for expensive tasks triggered on login (for example, if on login you do heavy computations or third-party calls, consider offloading those to background tasks to not slow the login response).

**Client-side concurrency:**

- If many users are connected, our front-end being static has no problem. But consider using something like Firebase Firestore or Realtime DB if you needed real-time updates with many clients – that’s another topic.

**Logging and Monitoring in Production:**

- Use monitoring tools to watch for increased latency or error rates. E.g., Application Insights (Azure) can track response times for each API call. If auth verification starts slowing (maybe if public key retrieval fails and times out?), you'd catch it.
- Set up alerts for high error rates (e.g., if > 1% of requests are 500s or 401s unexpectedly).

**Load Testing:**

- Before going live, run a load test. Tools like JMeter or Locust or Azure Load Testing can simulate many users hitting your login and API endpoints. This can reveal bottlenecks.
- Focus on scenarios like: X logins per second, or Y concurrent profile fetches.
- Ensure the system can handle it within acceptable response times (< some milliseconds).

**Graceful degradation:**

- If the database goes down or is overloaded, our API would fail. Have a plan: perhaps queue writes, or show a maintenance message to users, etc. It's good to handle DB connection exceptions gracefully (return a friendly error).
- If Firebase service is down (rare, but it could happen or network issues), users might not log in. The app should handle it (maybe show "Login temporarily unavailable, try again later").

**Scaling team and process** (just a note):

- As an advanced project, maintain code quality. Use linting and formatters for front-end (ESLint, Prettier) and tools like StyleCop or SonarQube for backend.
- Write documentation (like this guide!) for future developers, because advanced systems can be hard to grasp.

---

## References

- Firebase Documentation: **Authenticate Using Google with Firebase** – Official guide for adding Google Sign-In on web ([How to implement Firebase Authentication with OAuth providers? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-firebase-authentication-with-oauth-providers#:~:text=1.%20Google%20Sign,firebase%2Fauth)).
- Firebase Documentation: **Verify ID Tokens** – How to verify Firebase ID tokens on backend (includes info on using JWT libraries) ([How to integrate Firebase Authentication with a custom backend? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-integrate-firebase-authentication-with-a-custom-backend#:~:text=Step%205%3A%20Verify%20Firebase%20ID,Token%20in%20Backend)) ([Verify ID Tokens | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/verify-id-tokens#:~:text=Verify%20ID%20Tokens%20,the%20integrity%20and%20authenticity)).
- Stack Overflow: _"Firebase - Verifying that API requests have a valid ID token in .NET 5"_ – Discussion and answers on integrating Firebase Auth with ASP.NET Core JWT validation ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=services%20.AddAuthentication%28JwtBearerDefaults.AuthenticationScheme%29%20.AddJwtBearer%28options%20%3D,ValidateIssuer%20%3D%20true)) ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=ValidIssuer%20%3D%20%22https%3A%2F%2Fsecuretoken.google.com%2Fmy,)).
- GitHub Gist: _"Firebase JWT tokens in ASP.NET Core 3.1"_ – Example of JWT Bearer configuration for Firebase (Authority, Audience setup) ([Setting up API authentication using Firebase JWT tokens in ASP.NET Core 3.1. · GitHub](https://gist.github.com/edijer/9eb3759b9cc92f2a9cac62154b16ee60#:~:text=options.Authority%20%3D%20%24,ValidateIssuer%20%3D%20true)).
- Firebase Documentation: **Managing Sessions** – Explains refresh token behavior and how to manage session length ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=Refresh%20tokens%20don%27t%20expire%20after,on%20managing%20user%20sessions%20says)).
- Stack Overflow Answer by Frank van Puffelen – Notes that Firebase refresh tokens don't expire unless certain events occur (and how to revoke them) ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=Refresh%20tokens%20don%27t%20expire%20after,on%20managing%20user%20sessions%20says)) ([Is there a way to set an expiry on Firebase refresh tokens? - Stack Overflow](https://stackoverflow.com/questions/65728180/is-there-a-way-to-set-an-expiry-on-firebase-refresh-tokens#:~:text=)).
- Dev.to Article: _"React + Firebase: Context-based Authentication Provider"_ – Demonstrates using React Context and `onAuthStateChanged` for global auth state ([React + Firebase: A Simple Context-based Authentication Provider - DEV Community](https://dev.to/dchowitz/react-firebase-a-simple-context-based-authentication-provider-1ool#:~:text=Firebase%20offers%20us%20to%20register,about%20the%20current%20authentication%20situation)) ([React + Firebase: A Simple Context-based Authentication Provider - DEV Community](https://dev.to/dchowitz/react-firebase-a-simple-context-based-authentication-provider-1ool#:~:text=,constrived%29%20example)).
- Dev.to Article: _"Building a Firebase Authentication and Private Route System in React"_ – Guide on protecting routes using React Router v6 and Firebase Auth ([Building a Firebase Authentication and Private Route System in a React App - DEV Community](https://dev.to/jps27cse/building-a-firebase-authentication-and-private-route-system-in-a-react-app-5203#:~:text=const%20PrivateRoute%20%3D%20%28,%3D%20useContext%28AuthContext)) ([Building a Firebase Authentication and Private Route System in a React App - DEV Community](https://dev.to/jps27cse/building-a-firebase-authentication-and-private-route-system-in-a-react-app-5203#:~:text=return%20%3CNavigate%20to%3D)).
- Firebase Blog / Medium: _"Role Based Access Control with Firebase Custom Claims"_ – Explains using custom claims for roles ([How to implement a custom claims-based authorization in Firebase? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-a-custom-claims-based-authorization-in-firebase#:~:text=Step%203%3A%20Define%20Custom%20Claims)) ([How to implement a custom claims-based authorization in Firebase? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-implement-a-custom-claims-based-authorization-in-firebase#:~:text=,)).
- Stack Overflow: _"Firebase Authentication with Multi-Factor Auth"_ – Indicates MFA (SMS) requires Cloud Identity Platform (paid) ([Firebase Authentication with multi-factor authentication - Stack Overflow](https://stackoverflow.com/questions/52886244/firebase-authentication-with-multi-factor-authentication#:~:text=From%20March%2012%2C%202020%2C%20It,authentication%20to%20your%20web%20app)) ([Firebase Authentication with multi-factor authentication - Stack Overflow](https://stackoverflow.com/questions/52886244/firebase-authentication-with-multi-factor-authentication#:~:text=4)).

_(All references were accessed for information and code examples relevant to this implementation.)_

## Appendices

**Appendix A: Firebase ID Token Contents**  
A Firebase Google login ID token is a JWT typically containing claims such as:

- `iss` (Issuer) – `https://securetoken.google.com/<projectId>`
- `aud` (Audience) – `<projectId>`
- `sub` (Subject) – Firebase UID (same as `user_id`)
- `user_id` – Firebase UID
- `email` – User's email
- `email_verified` – true/false
- `name` – User's display name
- `picture` – URL of user profile photo
- `auth_time` – Timestamp of when user signed in
- `exp`, `iat` – Expiration and issued-at times
- Possibly others like `firebase` (contains sign-in provider info).  
  Understanding these helps in extracting needed info on backend. For example, `user_id` is the primary key for our Users table, and `email` we store as well. If `email_verified` is false (unlikely for Google provider), you might restrict certain actions.

**Appendix B: Using Firebase Admin SDK in .NET**  
If one wanted to use Firebase Admin SDK (for example, to set custom claims or to verify tokens manually), you'd do:

```csharp
FirebaseApp.Create(new AppOptions() {
    Credential = GoogleCredential.FromFile("path/to/serviceAccountKey.json")
});
FirebaseToken decoded = await FirebaseAuth.DefaultInstance.VerifyIdTokenAsync(idToken);
string uid = decoded.Uid;
```

This gives you a `FirebaseToken` object. However, as discussed, for normal auth flows, this isn't necessary when using JWT middleware ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=Since%20I%20have%20the%20ID,however%20it%20is%20not%20necessary)) ([c# - Firebase - Verifying that API requests have a valid ID token in .NET 5 - Stack Overflow](https://stackoverflow.com/questions/68094840/firebase-verifying-that-api-requests-have-a-valid-id-token-in-net-5#:~:text=FirebaseToken%20decodedToken%20%3D%20await%20FirebaseAuth,Uid)). But the Admin SDK is useful for admin tasks like creating users, revoking tokens, etc.

**Appendix C: Example .env Setup**  
For clarity, here's what a `.env` might look like for our React app (using Vite):

```env
VITE_FIREBASE_API_KEY="AIzaSyD...yourkey"
VITE_FIREBASE_AUTH_DOMAIN="yourproject.firebaseapp.com"
VITE_FIREBASE_PROJECT_ID="yourproject"
VITE_FIREBASE_STORAGE_BUCKET="yourproject.appspot.com"
VITE_FIREBASE_MESSAGING_SENDER_ID="1234567890"
VITE_FIREBASE_APP_ID="1:1234567890:web:abcdefg12345"
VITE_API_URL="https://api.yourdomain.com"  # custom API base URL
```

And for the .NET app (if using user secrets or Azure config):

```
ConnectionStrings__DefaultConnection=Host=...;Port=...;Database=...;Username=...;Password=...
FirebaseProjectId=yourproject  (if we externalize this instead of hardcoding in code)
```

Make sure to substitute your real values.

**Appendix D: Postman Testing Example**  
To test with Postman:

1. Obtain an ID token. E.g., after login, copy it from browser console or network.
2. In Postman, create a request to `https://yourapi.com/api/profile` (or login).
3. Under Authorization tab, choose "Bearer Token" and paste the ID token.
4. Send the request. You should get a 200 OK with data if everything is set up. If you get 401, token might be wrong or expired.

**Appendix E: Useful Commands Summary**

- `dotnet new webapi -n ProjectName` – create new Web API project.
- `npm create vite@latest clientapp --template react-ts` – create new React+TS app.
- `dotnet ef migrations add Init` / `dotnet ef database update` – create and apply EF migrations.
- `firebase init hosting` / `firebase deploy` – deploy frontend to Firebase.
- `openssl jwt -in token -noverify -text` – (if OpenSSL is available) decode a JWT for debugging. (Or use jwt.io web).
- `firebase login:ci` – get a token for CI deployment.
