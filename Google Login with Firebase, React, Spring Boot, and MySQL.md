# Google Login with Firebase, React, Spring Boot, and MySQL – Step-by-Step Guide

## Introduction

This guide provides a comprehensive, step-by-step walkthrough for implementing Google Login authentication using Firebase in a React (TypeScript) application, with a Spring Boot backend and MySQL database. We will cover everything from setting up Firebase for Google OAuth, integrating Firebase Auth on the frontend, handling authentication state with React Hooks, securely managing tokens/sessions, verifying Firebase tokens in Spring Boot, storing user data in MySQL, and applying security best practices. We’ll also discuss deployment strategies and how to optimize the architecture for scalability and performance. This guide assumes you are an experienced developer familiar with React, Java/Spring, and relational databases, focusing on integration and best practices rather than basic concepts.

## Table of Contents

1. [Setting Up Firebase for Google Authentication](#setting-up-firebase-for-google-authentication)
2. [Integrating Firebase Auth in a React (TypeScript) Frontend](#integrating-firebase-auth-in-a-react-typescript-frontend)
3. [Implementing Auth Logic with Firebase SDK and React Hooks](#implementing-auth-logic-with-firebase-sdk-and-react-hooks)
4. [Securely Handling Tokens and Session Management](#securely-handling-tokens-and-session-management)
5. [Setting Up a Spring Boot Backend to Verify Tokens and Manage Sessions](#setting-up-a-spring-boot-backend-to-verify-tokens-and-manage-sessions)
6. [Configuring MySQL to Store User Data](#configuring-mysql-to-store-user-data)
7. [Security Best Practices for Authentication and Authorization](#security-best-practices-for-authentication-and-authorization)
8. [Deploying the React Frontend and Spring Boot Backend](#deploying-the-react-frontend-and-spring-boot-backend)
9. [Optimizing for Scalability and Performance](#optimizing-for-scalability-and-performance)

## Setting Up Firebase for Google Authentication

**1. Create a Firebase Project:** Start by creating a new project in the [Firebase Console](https://console.firebase.google.com). Give the project a name and follow the setup wizard (you can skip Google Analytics if not needed) ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=Start%20with%20a%20creating%20Firebase,3%20steps%20in%20this%20setup)) ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=)). Once created, you’ll be taken to the Firebase project dashboard.

**2. Register a Web App:** In your Firebase project’s overview, add a new app and choose the web platform (the **</>** icon). Provide an app nickname (e.g., "MyReactApp") ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=)). Firebase will then provide a configuration object containing keys like `apiKey`, `authDomain`, `projectId`, etc., which you’ll need for your React app. Copy this config for later use ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=Now%20after%20registering%20our%20app,will%20look%20something%20like%20this)). For now, you can skip adding Firebase Hosting if prompted.

**3. Enable Google Sign-In:** In the Firebase console, navigate to **Authentication** -> **Sign-in method**. Enable the **Google** provider and configure any required options (select a project support email, etc.) ([Firebase auth in a React app with TypeScript](https://davidschinteie.hashnode.dev/firebase-auth-in-a-react-app-with-typescript#:~:text=Initially%2C%20we%27ll%20need%20to%20activate,authentication%20through%20the%20Firebase%20console)). This allows Firebase to handle Google OAuth on your behalf. Ensure you add your app’s domain (e.g., localhost for development, and your production domain) to the list of authorized domains in the Authentication settings so that Google sign-in will work from those origins.

**4. (Optional) Set Up OAuth Consent Screen:** Although Firebase simplifies Google sign-in, it uses an internal OAuth client. If you need to customize the Google consent screen or branding, you can do so in the Google Cloud Console for the project (Firebase projects are also Google Cloud projects). This step is usually not required for basic functionality.

**5. Generate Service Account Credentials (for Backend):** To verify tokens and perform admin actions from Spring Boot, you’ll use Firebase’s Admin SDK. Go to **Project Settings** -> **Service Accounts** in Firebase, and click **Generate new private key**. This downloads a JSON file containing service account credentials. **Keep this file secure** and do not commit it to source control. You will use it in the Spring Boot application to initialize Firebase Admin. Move this JSON into your Spring Boot project (e.g., `src/main/resources/firebase-service-credentials.json`) or set an environment variable pointing to it. We will use this in a later section.

By completing these steps, Firebase is ready to handle Google logins for your app. Next, we’ll integrate Firebase into the React frontend.

## Integrating Firebase Auth in a React (TypeScript) Frontend

**1. Set Up the React Project:** If you haven’t already, bootstrap a React project with TypeScript. For example, using Create React App:

```bash
npx create-react-app my-app --template typescript
```

This will create a new React app in the `my-app` directory with TypeScript support. Alternatively, you can use tools like Vite or Next.js with TypeScript – the integration steps for Firebase will be similar.

**2. Install Firebase SDK:** In your React project, install Firebase:

```bash
npm install firebase
```

This brings in the Firebase JS SDK, which includes Authentication functions. (We will use the modular v9 SDK syntax, which uses tree-shakable imports.)

**3. Initialize Firebase in React:** Create a Firebase configuration file (for example, `src/firebase.ts` or `src/utils/firebase.ts`). Import the required Firebase functions and initialize the app with the config from the Firebase console. For clarity and security, it’s best to store your Firebase config in environment variables (especially if you use build tools like Vite or CRA). For example:

```typescript
// src/firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Your Firebase config object (replace with your values or use env vars)
const firebaseConfig = {
  apiKey: import.meta.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: import.meta.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.REACT_APP_FIREBASE_APP_ID,
};

// Initialize Firebase app and Authentication
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Prepare Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
```

In the above snippet, we used environment variables (prefixed with `REACT_APP_` for Create React App or `import.meta.env` for Vite) to inject the config values, which is a common practice ([Firebase auth in a React app with TypeScript](https://davidschinteie.hashnode.dev/firebase-auth-in-a-react-app-with-typescript#:~:text=const%20firebaseConfig%20%3D%20,VITE_FIREBASE_APP_ID%2C)). This avoids hardcoding secrets; although Firebase config is not highly sensitive (it’s okay if it’s exposed, as it’s needed in the client), using env vars allows different configs for dev/prod and keeps the code clean.

**4. Configure GoogleAuthProvider (Optional):** You can customize the GoogleAuthProvider if needed. For instance, to prompt the user to select an account every time (useful if multiple Google accounts are logged in), you can do:

```typescript
googleProvider.setCustomParameters({ prompt: "select_account" });
```

This step is optional; without it, Firebase will use the default Google sign-in behavior.

**5. Prepare the Auth UI Components:** In your React app, you’ll need a login interface. For example, create a `Login.tsx` component that renders a "Sign in with Google" button, and a `Home.tsx` component for post-login. We will implement the click handler logic in the next section. For now, ensure you have a basic routing (using React Router or conditional rendering) to show `Login` when no user is authenticated and `Home` (or the main app) when logged in.

By this stage, the React app is set up with Firebase. We have configured the Firebase Auth provider and prepared the groundwork to trigger Google sign-in and handle auth state.

## Implementing Auth Logic with Firebase SDK and React Hooks

Now we’ll implement the logic to authenticate users via Google and manage the auth state on the client side using React Hooks.

**1. Trigger Google Sign-In:** Using the Firebase Auth SDK, you can open a Google login pop-up when the user clicks the sign-in button. In your `Login` component (or a dedicated auth service file), call the `signInWithPopup` function with the Google provider. For example:

```typescript
// Inside Login component or an auth utility file
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../firebase"; // import the auth instance and provider

const handleGoogleSignIn = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    // Google sign-in successful. The signed-in user info can be obtained from result.user.
    console.log("Signed in user:", result.user);
  } catch (error) {
    console.error("Google sign-in error:", error);
    // Handle errors (ex: popup closed, network issues, etc.)
  }
};
```

In this snippet, `signInWithPopup(auth, googleProvider)` will open a pop-up window for the Google OAuth flow. If the user successfully signs in, Firebase gives us a `UserCredential` object from which we can get the authenticated user (`result.user`) ([Firebase auth in a React app with TypeScript](https://davidschinteie.hashnode.dev/firebase-auth-in-a-react-app-with-typescript#:~:text=%2F%2F%20Google%20Auth%20function%20const,googleProvider%20%3D%20new%20GoogleAuthProvider)). The user object contains details like `uid` (Firebase user ID), `displayName`, `email`, and `photoURL`. At this point, Firebase has also handled storing a refresh token for session persistence in the browser (so the user stays logged in on refresh). We should now update our app state to reflect that the user is logged in.

**2. Respond to Auth State Changes:** Firebase provides a listener `onAuthStateChanged` that notifies us whenever the user's sign-in state changes (login, logout, token refresh, etc.). We can use the React `useEffect` hook to subscribe to this auth state. For example, in a top-level component (like `App.tsx` or an AuthProvider context):

```typescript
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "./firebase";

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Listen for auth state changes
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setLoading(false);
    });
    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return currentUser ? (
    <Home user={currentUser} />
  ) : (
    <Login onGoogleSignIn={handleGoogleSignIn} />
  );
}
```

Here, we initiate the listener once on component mount. Initially, `currentUser` is null and we set a loading state. When Firebase calls our callback, we set the current user (this will be a `User` object if logged in, or null if logged out) and update loading. The component can then render either the logged-in view or the login screen accordingly. The `onAuthStateChanged` listener is crucial for maintaining session state: Firebase will automatically restore the user if there's a valid session (using the stored refresh token) when the app reloads. This means a returning user won't have to log in again every time; our listener will receive the user on app start if the session is still valid.

**3. Sign Out Functionality:** Implement a logout button that calls `signOut(auth)` from Firebase. For example, in the `Home` component:

```tsx
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

<button onClick={() => signOut(auth)}>Sign Out</button>;
```

Calling `signOut(auth)` will log the user out and trigger the `onAuthStateChanged` listener with `user = null`, updating our UI state accordingly.

**4. (Optional) Using Context for Auth State:** In a larger application, you may want to create a React Context to provide the `currentUser` and auth functions (`signIn`, `signOut`, etc.) to any component. This avoids prop-drilling the user object into deeply nested components. An `AuthProvider` component can wrap your app, manage the `onAuthStateChanged` logic, and use Context to expose auth data. Since this guide focuses on the overall integration, we won’t detail context implementation, but keep it in mind as a best practice for structuring your React app’s auth state.

With the above steps, our React app can initiate Google Login and react to authentication changes. The Firebase SDK handles the heavy lifting: after sign-in, it keeps the user’s ID token fresh and lets us know of changes. Next, we’ll see how to send this authentication information to our backend and manage sessions securely.

## Securely Handling Tokens and Session Management

Once the user is authenticated on the frontend, we need to communicate that to our Spring Boot backend to authorize API requests. Firebase issues **ID Tokens** (JWTs) for authenticated users. These tokens prove the user’s identity and can be verified by the backend. Here’s how to handle them securely:

**1. Retrieve the Firebase ID Token:** After a successful login, you can get the user's ID token via the Firebase SDK. The `User` object has a method `getIdToken()`. For example:

```typescript
const idToken = await result.user.getIdToken();
```

This token is a JSON Web Token (JWT) that includes the user's UID and other details. By default, Firebase ID tokens expire in 1 hour, but the Firebase client SDK will transparently refresh them as long as the user remains logged in. You can force a refresh (to get a fresh token) by calling `getIdToken(true)` ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=firebase%20,log%28idToken)), but typically this is not necessary unless you need the latest claims.

**2. Send the Token to Backend:** To authenticate API calls, the React app should include this ID token in requests to your Spring Boot server. The common approach is to use the `Authorization` header with a `Bearer` scheme. For example, if using `fetch` or Axios:

```typescript
// Example with fetch
fetch("/api/protected-resource", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${idToken}`,
  },
});
```

If you use Axios, you can set up an Axios interceptor to automatically attach the token from your state on every request to your API domain. The backend will then extract and verify this token for each protected endpoint (we’ll cover verification in the Spring Boot section).

**3. Token Storage on Client:** You might wonder where to store the ID token on the client. **Do not manually store the ID token in localStorage or cookies**; let Firebase handle it. Firebase stores a refresh token (and other auth state) in local storage or indexedDB under its own keys. This allows it to manage token renewal. Your code can always call `auth.currentUser.getIdToken()` when needed; the SDK will return a valid token, refreshing it if expired. If you manually store the token, it could become stale or present security issues. Instead, consider in-memory usage: for immediate subsequent requests, you can keep it in a variable or state, but for the most part just retrieve on demand.

**4. Session Management Strategies:** There are two primary ways to manage the session between the React app and Spring Boot:

- **Stateless JWT (Recommended):** Use the Firebase ID token on each request (no server-side session). This is a _stateless_ approach. The backend will treat each request independently, verifying the token’s signature and claims. This approach scales well and avoids maintaining session state on the server ([The Purpose of JWT: Stateless Authentication - jbspeakr.cc](https://www.jbspeakr.cc/purpose-jwt-stateless-authentication/#:~:text=Stateless%20authentication%20is%20essential%20for,said%20to%20simplify%20system%20landscape)). The downside is, if you want to revoke a user’s access, you’d have to implement token revocation (Firebase allows revoking tokens via the Admin SDK) or rely on token expiry.
- **Stateful Session (Alternate):** Exchange the ID token for a server session. For example, the client sends the token to a login endpoint, the backend verifies it and then creates an HTTP session (or issues its own JWT). Subsequent requests use a session cookie (e.g., JSESSIONID) or a custom JWT issued by the server. This can simplify things like immediate token revocation and integrate with Spring Security’s session management, but it adds complexity in a distributed environment (sessions need sticky load balancing or shared cache) and duplicates what Firebase already provides. For scalability and simplicity, many choose to remain stateless.

Firebase offers a middle-ground with **Session Cookies** in its Admin SDK: you can exchange an ID token for a long-lived session cookie, which is essentially a stateless JWT that you set in a cookie. This keeps the session on the client side (cookie) but allows persistent login without localStorage. However, implementing Firebase session cookies is beyond our scope; we will proceed with the stateless token approach for API calls.

**5. Secure Transmission:** Always send the token over HTTPS to prevent eavesdropping. If your React app and Spring Boot API are on different domains (or ports), configure CORS on the backend to allow the Authorization header. Avoid sending tokens in URL query parameters or local storage where they could be leaked or accessed by malicious scripts.

**6. Protecting Against XSS/CSRF:** If you use the recommended approach (Authorization header with token), the main threat is XSS (a script stealing your token). To mitigate this, avoid storing the token in localStorage where any XSS could grab it. Keeping it in memory (or letting Firebase manage it) limits exposure. If you use an HTTP-only cookie for session, you mitigate XSS (JS can't read the cookie) but then need to protect against CSRF (since browsers send cookies automatically). Using the Authorization header with a token from JS means you are not susceptible to CSRF by default (because an attacker’s site cannot read your token without XSS). In summary, the Firebase token + Authorization header approach is secure if your app is free of XSS vulnerabilities and served via HTTPS.

**Summary:** The React app, upon login, will obtain a Firebase ID token and include it with each API request (likely in an `Authorization: Bearer <token>` header). This approach is stateless and leverages Firebase’s secure token system. Next, we’ll set up the Spring Boot backend to accept and verify these tokens, ensuring only authenticated users can access protected resources.

## Setting Up a Spring Boot Backend to Verify Tokens and Manage Sessions

The backend will serve two main purposes: verify the authenticity of Firebase ID tokens (Google login credentials) and provide application-specific functionality (e.g., protected data, user profile storage, etc.). We will use Spring Boot with Spring Security to handle JWT verification and MySQL to store user data. Let’s go step by step:

**1. Initialize a Spring Boot Project:** Set up a Spring Boot project (using Spring Initializr or your build tool) with the following dependencies:

- **Spring Web:** for building REST APIs.
- **Spring Security:** to secure endpoints and handle authentication.
- **Spring Data JPA:** for interacting with MySQL (we’ll configure MySQL in the next section).
- **MySQL Driver:** JDBC driver for MySQL.
- You do _not_ need to include an OAuth2 client dependency or any Firebase-specific library for basic JWT verification, but including the **Firebase Admin SDK** can be helpful for certain tasks (like fetching additional user info or using custom Firebase features). We will include the Admin SDK to demonstrate both approaches.

**2. Add Firebase Admin SDK Dependency:** In your build file (Maven or Gradle), add the Firebase Admin SDK. For example, with Maven, add:

```xml
<dependency>
  <groupId>com.google.firebase</groupId>
  <artifactId>firebase-admin</artifactId>
  <version>9.1.1</version>  <!-- use the latest version -->
</dependency>
```

This SDK allows server-side verification of Firebase tokens and other admin operations.

**3. Configure Firebase Admin (Service Account):** Place the service account JSON (from Firebase setup) into the Spring Boot project (e.g., in `src/main/resources`). It’s a good practice to **load this via an environment variable** instead of hardcoding the path. For example, you can set an env var `GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/firebase-service-credentials.json` so that Firebase Admin SDK picks it up automatically. Alternatively, initialize it manually in code. One way is to create a configuration or service class that runs on startup:

```java
@Service
public class FirebaseInitializer {
    @PostConstruct
    public void initFirebase() throws IOException {
        // Load service account key
        InputStream serviceAccount = new ClassPathResource("firebase-service-credentials.json").getInputStream();
        FirebaseOptions options = FirebaseOptions.builder()
                .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                .build();
        FirebaseApp.initializeApp(options);
    }
}
```

This uses the service account JSON to initialize the default `FirebaseApp` instance ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=%40PostConstruct%20public%20void%20initializeFirebaseApp,credentials.json)). Once initialized, you can use `FirebaseAuth.getInstance()` in your app to verify tokens or fetch user info. (If you prefer not to deal with the JSON file, you can skip this if you use the JWT verification approach described next, but it’s useful to have FirebaseApp initialized for any admin operations or advanced features.)

**4. Set Up JWT Verification with Spring Security:** We will leverage Spring Security’s _resource server_ support to validate the Firebase ID tokens. Firebase tokens are JWTs signed by Google. Google also provides a set of public keys (JWKS) for verifying these tokens. Spring Security can be configured to treat our app as a resource server that accepts JWTs issued by Firebase.

Add the following to your Spring Boot `application.properties` (or better, `application.yml` for clarity):

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://securetoken.google.com/<your-firebase-project-id>
          jwk-set-uri: https://www.googleapis.com/robot/v1/metadata/jwk/securetoken@system.gserviceaccount.com
```

Replace `<your-firebase-project-id>` with the Firebase project ID you created ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=spring%3A%20security%3A%20oauth2%3A%20resourceserver%3A%20jwt%3A,id)). The `issuer-uri` and `jwk-set-uri` tell Spring Security to accept tokens from Firebase. The issuer URI ensures the token’s `iss` claim matches your project, and the JWK URI provides the public keys to validate the token’s signature. These URIs are standard for Firebase Auth tokens: all Firebase ID tokens have issuer `https://securetoken.google.com/<project-id>` and are signed by the `securetoken@system.gserviceaccount.com` keys.

Next, create a security configuration class (since Spring Security is on the classpath). For Spring Boot 2.x, extend `WebSecurityConfigurerAdapter` (note: in Spring Boot 3 / Spring Security 6, you’d use a SecurityFilterChain bean instead, but conceptually similar):

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
          .authorizeRequests()
            .antMatchers("/api/**").authenticated()   // secure all /api paths
            .anyRequest().permitAll()                // allow other paths (e.g., health check)
          .and()
            .oauth2ResourceServer().jwt();           // enable JWT authentication
    }
}
```

This security config says: any request to `/api/**` must be authenticated (i.e., must have a valid JWT in the header), while other requests are open (adjust these paths as needed for your application) ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=spring%3A%20security%3A%20oauth2%3A%20resourceserver%3A%20jwt%3A,id)) ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=%40Override%20protected%20void%20configure,oauth2ResourceServer)). The `.oauth2ResourceServer().jwt()` line activates the JWT filter using the properties we set. Spring Security will automatically:

- Read the `Authorization: Bearer ...` token from requests.
- Verify the token’s signature against the Google public keys.
- Check that the token’s issuer is correct and not expired.
- If valid, consider the request authenticated and set the security context with the user’s details (by default, the `uid` will be used as the username/principal).

We should also ensure stateless session management (to avoid creating an HTTP session for each request, since we are using tokens):

```java
http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
```

Add that to the `configure` method chain. This tells Spring Security not to use HTTP sessions to store security context between requests (each request is authenticated independently via the token). Stateless authentication aligns with using JWTs and allows the app to scale easily.

**5. Verify Firebase Tokens Manually (alternative):** The above configuration uses Spring Security’s built-in JWT support. Alternatively, you could skip configuring the resource server and instead, in each protected endpoint or a custom filter, manually verify the token using Firebase Admin SDK:

```java
String idToken = extractBearerToken(request);
try {
    FirebaseToken decodedToken = FirebaseAuth.getInstance().verifyIdToken(idToken);
    String uid = decodedToken.getUid();
    // Token is valid. You can set up a SecurityContext or proceed knowing the user's UID.
} catch (FirebaseAuthException e) {
    // Token invalid or expired
    throw new SecurityException("Invalid token");
}
```

This approach works, but it requires you to implement the extraction and verification logic. Using Spring Security’s `oauth2ResourceServer().jwt()` as shown is typically less code and ensures industry-standard validation (audience checks, etc., can be configured as needed). Under the hood, both approaches verify the JWT signature using Google’s public keys – so choose the one that fits your style. The Admin SDK approach gives you an immediate `FirebaseToken` object with decoded claims, and also allows fetching the full user record if needed (via `FirebaseAuth.getInstance().getUser(uid)`), whereas the Spring Security approach would require you to parse details from the JWT claims if needed.

**6. Testing the Setup:** At this point, your Spring Boot application should accept requests with a valid Firebase token. You can create a simple REST controller to test this. For example:

```java
@RestController
@RequestMapping("/api")
public class HelloController {
    @GetMapping("/hello")
    public String hello(Authentication authentication) {
        String uid = (String) authentication.getPrincipal();
        return "Hello, your UID is " + uid;
    }
}
```

With Spring Security’s JWT setup, the `Authentication` object will be a `JwtAuthenticationToken`. The `principal` is set to the `uid` (Firebase user ID) ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=%40GetMapping%20public%20ResponseEntity,getAuthentication)). So if you call this `/api/hello` endpoint from the React app with the Authorization header set, you should get a greeting with your UID. If the token is missing or invalid, Spring Security will return a 401 Unauthorized automatically.

**7. Managing User Sessions on Backend:** Since we are using a stateless approach, we are not creating server sessions. Each request is authenticated by token. This is ideal for scaling and microservices. If your application needs to keep track of user login sessions (for example, to record active users or to perform logout from server side), you can still implement that logic:

- You might store a record of "active JWTs" or login timestamps in a database if needed, or
- Use Firebase’s built-in mechanisms (Firebase allows you to revoke refresh tokens for a user, which will eventually force logout).
- However, in most cases, this isn’t necessary — the presence of a valid token is enough to consider the user “logged in”, and if you want to log them out, you instruct the client to remove its credential (which our React signOut already handles).

If you opted for stateful sessions (not recommended for most cases here), you would have an endpoint that exchanges the token for a session: the server would create a session and perhaps issue its own cookie. In that case, Spring Security could use a different filter chain (for example, treat the token as a credential in an authentication filter). This gets complex and is usually redundant given the capabilities of JWT. So we’ll stick to stateless JWT security.

**8. Role/Authority Mapping (Optional):** Firebase ID tokens can include [custom claims](https://firebase.google.com/docs/auth/admin/custom-claims) for roles/authorizations, or you can map user roles from your database. If you need role-based access on the backend, you could do something like: after verifying the token, load the user from DB (to get their roles) and attach authorities to the SecurityContext. With the resource server approach, you might implement a custom JwtAuthenticationConverter to map token claims to GrantedAuthority. For simplicity, this guide assumes all authenticated users are allowed if token is valid, and any app-specific authorization (like admin rights) can be handled via checks in your code (for example, checking a role field in the user database, see next section).

At this point, the Spring Boot backend is capable of authenticating incoming requests using Firebase tokens. Now we need to integrate MySQL to store user data and link it with these authenticated sessions.

## Configuring MySQL to Store User Data

We will use MySQL to store user-related data, such as user profiles or any application-specific info. The typical stack is Spring Data JPA for database operations and MySQL as the database. Let’s set that up:

**1. Install and Run MySQL:** Ensure you have a MySQL server running (locally or accessible remotely) and create a database for your application (e.g., `myapp_db`). Create a user with proper credentials for the app, or use root (not recommended for production).

**2. Spring Boot Database Configuration:** In `application.properties` or `application.yml`, add the MySQL connection settings and JPA configs. For example in `application.yml`:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/myapp_db
    username: myuser
    password: mypassword
  jpa:
    hibernate:
      ddl-auto: update # auto-create/update tables; use 'validate' or disable in production
    show-sql: true # to log SQL queries (optional)
```

Make sure the MySQL driver dependency is on the classpath (which we added earlier). Spring Boot will auto-configure a DataSource and an EntityManagerFactory using these properties ([A Guide to JPA with Spring | Baeldung](https://www.baeldung.com/the-persistence-layer-with-spring-and-jpa#:~:text=A%20Guide%20to%20JPA%20with,to%20define%20the%20DataSource%20configuration)).

**3. Define a User Entity:** Create a JPA entity class to represent users in your application. This will likely correspond to a table in MySQL where you store user info. For example:

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    private String uid;        // use Firebase UID as primary key

    private String name;
    private String email;
    private String profilePic;
    private Long lastLogin;

    // ... constructors, getters, setters ...
}
```

Here we’re using the Firebase `uid` as the primary key (a convenient unique identifier for users). We store the display name, email, profile picture URL, and last login timestamp as examples. You can extend this with any additional fields your app needs (roles, preferences, etc.). Using the Firebase UID as the key means we can easily retrieve the same user that logged in via Firebase.

**4. Create a User Repository:** Use Spring Data JPA to create a repository interface for the `User` entity:

```java
public interface UserRepository extends JpaRepository<User, String> {
    // JpaRepository provides CRUD operations by default.
    // You can add custom queries if needed, e.g., findByEmail.
}
```

This gives us basic database operations for the User table.

**5. Persisting Users on Login:** The typical flow is: when a user logs in via Google for the first time, our backend should create a corresponding `User` record in the database (if it doesn’t already exist). We have the user’s Firebase UID from the token (and we can get their name/email either from the token claims or by calling Firebase Admin SDK).

We can implement this in a couple of ways:

- **On-the-fly in a Request:** e.g., in a controller that requires authentication, check if `userRepository.existsById(uid)`; if not, fetch user details and save. This was illustrated in a similar context where after authenticating, the app pulled additional user info and saved a new record ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=UserRecord%20userRecord%20%3D%20FirebaseAuth)).
- **Dedicated Endpoint:** have the client call an endpoint like `/api/register` right after login, which the server uses to create the user in DB (this could carry additional info from client if needed, though in our Google login case, Google already provides name/email).

Using token claims: Firebase ID tokens contain some user info in the `firebase` claim (like email and whether it’s verified). However, Firebase might not include the display name/photo in the token by default for Google sign-in. To get those, you can either pass them from the client (from `result.user`) or call Firebase Admin `getUser(uid)` which returns a `UserRecord` with full profile. For example:

```java
UserRecord userRecord = FirebaseAuth.getInstance().getUser(uid);
User newUser = new User();
newUser.setUid(uid);
newUser.setName(userRecord.getDisplayName());
newUser.setEmail(userRecord.getEmail());
newUser.setProfilePic(userRecord.getPhotoUrl());
newUser.setLastLogin(userRecord.getUserMetadata().getLastSignInTimestamp());
userRepository.save(newUser);
```

This creates a User entry with data fetched from Firebase ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=UserRecord%20userRecord%20%3D%20FirebaseAuth)). You would run this logic if `userRepository.findById(uid)` returns empty (user not seen before). If the user exists, you might update certain fields like lastLogin timestamp or name (in case they changed their Google profile).

> **Advanced Note:** You might also consider storing only essential fields in MySQL (like our app-specific data) and rely on Firebase for auth-related data. However, having email and name in your DB is convenient for queries and avoiding extra calls to Firebase on each request. It’s a balance between duplication and ease of use. Storing them also lets you enrich user profiles with additional info beyond Google’s scope.

**6. Using the User Data:** Once users are stored, you can use `UserRepository` in your controllers or services to fetch the user’s data. For example, in a secured controller you could do:

```java
@GetMapping("/profile")
public ResponseEntity<User> getProfile(Authentication authentication) {
    String uid = (String) authentication.getPrincipal();
    User user = userRepository.findById(uid)
                    .orElseThrow(() -> new RuntimeException("User not found"));
    return ResponseEntity.ok(user);
}
```

This would return the user profile from MySQL for the authenticated user. Thanks to our Security config, `authentication.getPrincipal()` is the Firebase UID of the logged-in user ([spring-jwt-firebase/DIY.md at master · iethem/spring-jwt-firebase · GitHub](https://github.com/iethem/spring-jwt-firebase/blob/master/DIY.md#:~:text=%40GetMapping%20public%20ResponseEntity,getAuthentication)), so we can directly use it to find the user in the database.

**7. Database Schema and Migrations:** In development, using `hibernate.ddl-auto=update` will let Hibernate create the `users` table automatically. In production, you might use a migration tool or SQL script to create the table (with appropriate schema). For reference, the table might look like:

```sql
CREATE TABLE users (
  uid VARCHAR(128) PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  profile_pic VARCHAR(512),
  last_login BIGINT
);
```

Adjust lengths as needed. Ensure proper indexing (the primary key is indexed by default). If you expect to query by email or other fields, consider adding indexes there too.

By configuring MySQL and setting up the user entity, our backend can now persist user information and serve it as needed. We have essentially linked the Firebase-authenticated sessions with our application data via the UID. Next, let’s go over some security best practices to make sure our authentication system is robust.

## Security Best Practices for Authentication and Authorization

Implementing authentication involves handling sensitive data (tokens, personal info). Here are some best practices to follow in our Firebase-React-SpringBoot-MySQL stack:

- **Never Trust Client-side Data Without Verification:** Always verify the Firebase ID token on the server using either Firebase Admin SDK or JWT validation. Do not accept a UID or email from the client as proof of identity. Our setup above ensures the token is verified (signature and issuer) before trusting the user info ([java - Login with firebase + spring on backend - Stack Overflow](https://stackoverflow.com/questions/51202168/login-with-firebase-spring-on-backend#:~:text=1)).

- **Use HTTPS Everywhere:** Ensure both the frontend and backend are served over HTTPS in production. Tokens sent over plain HTTP can be intercepted. Also, configure secure cookies (if any) with the Secure flag.

- **Secure Token Storage on Client:** As discussed, avoid localStorage for tokens if possible due to XSS risk. If you ever store tokens, prefer HttpOnly cookies. In our approach, Firebase SDK handles storage securely. If you choose cookies for session, set the HttpOnly and SameSite attributes to restrict access and reduce CSRF risk ([security - Should JWT be stored in localStorage or cookie? - Stack Overflow](https://stackoverflow.com/questions/34817617/should-jwt-be-stored-in-localstorage-or-cookie#:~:text=So%20based%20on%20the%20above,reading%20it%20from%20the%20cookies)).

- **Limit Token Scope and Lifetime:** Firebase ID tokens by default expire after 1 hour, which is a reasonable balance between security and usability. The refresh token is used by Firebase to get a new ID token seamlessly. Do not extend the ID token lifetime on the Firebase side (even though custom tokens can be tweaked) unless absolutely necessary. Short-lived tokens limit the window of misuse if stolen.

- **Protect Endpoints with Proper Authorization:** We locked down `/api/**` to authenticated users. If you have different user roles (e.g., admin vs normal user), enforce that in the backend. For example, you might have an `isAdmin` flag in your `User` DB or a custom claim in Firebase. Check this in your controller or use method-level security (e.g., `@PreAuthorize("hasRole('ADMIN')")`) after wiring roles into the SecurityContext. Do not rely solely on UI to hide admin functionality; the backend should enforce it.

- **Validate Input Data:** Although not directly auth-related, ensure that any data coming from the client (even if authenticated) is validated to prevent injection attacks or malicious content. Using JPA with prepared statements helps avoid SQL injection. For any user-supplied content stored in DB, consider sanitizing or validating length/types.

- **Least Privilege for Service Account:** The Firebase service account JSON is powerful. If possible, restrict its permissions to only what's needed (though Firebase Auth tokens verification requires a service account from the same project – ensure you keep this file safe). Do not expose the content of this JSON. In production, prefer setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the credentials file location, so you don't have to include the raw JSON in the packaged app.

- **Regularly Update Dependencies:** Security issues are fixed over time, so keep Firebase SDK, Spring Boot, and other libraries up to date with patches.

- **Monitor and Rate Limit:** Watch for suspicious activities, such as multiple failed logins (though with Google login, Firebase handles account security), or an abnormal number of requests to your backend. Implementing basic rate limiting or using services to detect abuse can protect against brute force or DDoS attacks on your endpoints.

- **Use App Check (Optional):** Firebase offers App Check to ensure only your authentic app can interact with Firebase backend services. In our case, since we have our own backend, App Check isn’t verifying calls to Spring Boot, but could protect calls directly to Firebase (if any). This is more relevant if using Firebase database/storage; mentioning for completeness.

- **Backup and Secure Your Database:** Enable proper firewall rules so your MySQL is not publicly accessible. Use strong passwords for the DB user. Backup your user database regularly and encrypt backups if needed, as it contains personal data (names, emails).

By adhering to these practices, you help ensure that your login flow is not only functional but also secure against common threats. The combination of Firebase’s secure authentication and Spring Security’s robust authorization framework provides a solid foundation.

## Deploying the React Frontend and Spring Boot Backend

With development and testing complete, consider how to deploy both the frontend and backend for production use. There are a few approaches:

**1. Deploying the Frontend (React app):** Since the React app is a Single Page Application, you can deploy it as static files. Common options include:

- **Firebase Hosting:** Given we’re already using Firebase, you can use Firebase Hosting for the React app. Run `npm run build` to get a production build (which generates static files under `build/` or `dist/`). Then use the Firebase CLI to deploy those. You’ll need to add Firebase Hosting to your project and configure it (in `firebase.json`). Firebase Hosting can also proxy API calls to your Spring Boot server if configured, or you can just have the React app call your API domain directly.
- **Static File Hosting (Netlify, Vercel, AWS S3+CloudFront, etc.):** These services specialize in hosting SPAs. For example, Netlify or Vercel can directly deploy from your Git repo. AWS S3 with CloudFront can serve the files globally. Ensure you configure the web server for SPA routing (serve `index.html` for unknown routes).
- **Serving via Spring Boot:** Another approach is to bundle the React build into the Spring Boot app so both front and back are served from one server. You can do this by copying the build files into `src/main/resources/static` or using Maven plugins to build the React app during the Spring Boot build. Then Spring Boot will serve the React app at `"/"` and also serve APIs at `"/api"`. This simplifies deployment (one artifact to deploy) and avoids CORS issues entirely ([What's the best way to deploy a Spring Boot + React project? - Reddit](https://www.reddit.com/r/java/comments/iseggg/whats_the_best_way_to_deploy_a_spring_boot_react/#:~:text=Reddit%20www,deploy%20this%20JAR%20to%20heroku)). The drawback is you can’t easily scale frontend and backend independently, and the deployment process might be a bit more complex to set up initially.

Whichever method, ensure the environment config is set for production: e.g., use production Firebase project settings if different, and point the React app to the correct API URL (if not same origin).

**2. Deploying the Backend (Spring Boot app):** You have many options:

- **Cloud Platforms (Heroku, AWS, GCP, Azure):** Heroku is straightforward for Spring Boot (simply push code and it builds and runs). AWS Elastic Beanstalk or Google App Engine can also directly run a Spring Boot JAR with minimal configuration. Make sure to set your environment variables (DB credentials, Firebase creds path, etc.) on the server.
- **Containerization:** Dockerizing the Spring Boot app is a popular approach. You’d create a Docker image with the JDK and your application jar, then run that container on a service like AWS ECS, Google Cloud Run, Kubernetes, etc. For example, you might use a Dockerfile that extends an OpenJDK image, copies the jar, and sets entrypoint to `java -jar app.jar`. Ensure to also handle the MySQL instance (you might use a managed MySQL service or run MySQL as a container as well, but managed DB is easier for production).
- **Reverse Proxy and Domain:** When deploying, you might put a reverse proxy (like Nginx) in front of your Spring Boot app for SSL termination and to serve the React static files if needed. If frontend and backend are separate domains, configure CORS properly on Spring Boot (in SecurityConfig, you can enable `.cors()` and define allowed origins). If they share a domain (e.g., serving React from Spring Boot, or using subdomains), set appropriate CORS or use the same domain to avoid CORS altogether.

**3. Configuration in Production:** Remember to adjust configurations for production: disable `show-sql` and auto ddl in JPA (use proper migrations), use strong secrets, and point to production Firebase project if it differs. Also, ensure the Firebase Auth authorized domains include your production domain.

**4. Domain and OAuth Redirects:** If you use signInWithPopup, you’re mostly fine as long as the domain is authorized. If you ever use `signInWithRedirect`, you must configure the auth redirect URI in Firebase (usually just your domain). Popup is simpler for deployments because it just needs the domain on the whitelist.

**5. Testing After Deployment:** Once deployed, test the full flow in production:

- Navigate to the React app URL, click Google sign-in. The Google popup should show your production OAuth consent screen (if configured) and then redirect back.
- After login, try an API call that fetches user data. Ensure you get a response and not a CORS error or 401.
- Check your database to confirm the user record was created/updated properly on first login.
- Test logging out and logging in as a different user.

**6. Monitoring and Logging:** Set up logging (and log aggregation if possible) for the Spring Boot app to track any errors (like token validation failures or database issues). Also, monitor the performance of the application; enable any application performance monitoring if needed.

By carefully deploying both pieces and testing, you’ll have a working production setup. The frontend and backend can be scaled independently if needed (e.g., run multiple instances of Spring Boot behind a load balancer if you have high load; the stateless JWT auth will help scale without sticky sessions).

## Optimizing for Scalability and Performance

Finally, let’s discuss how this architecture can be optimized as your user base grows:

- **Stateless Backend for Horizontal Scaling:** We designed the backend to be stateless (no session memory per user) by using JWTs. This means you can run multiple instances of the Spring Boot app behind a load balancer, and any instance can handle any request, since authentication is self-contained in the token ([The Purpose of JWT: Stateless Authentication - jbspeakr.cc](https://www.jbspeakr.cc/purpose-jwt-stateless-authentication/#:~:text=Token)) ([Why JWT is Dangerous for User Sessions? | by Aditya Yadav](https://aditya003-ay.medium.com/why-jwt-is-dangerous-for-user-sessions-dd8eade705e6?source=rss------javascript-5#:~:text=Yadav%20aditya003,Stateless%20design%20simplifies%20horizontal%20scaling)). There’s no dependency on in-memory sessions. This greatly improves scalability – you can add more servers to handle more load without worrying about session replication.

- **Connection Pooling and Database Scaling:** Ensure your connection pool (HikariCP by default in Spring Boot) is tuned for your load – too few connections can throttle throughput, too many can overwhelm MySQL. Monitor connection usage. If read traffic grows, consider read replicas for MySQL and direct some read queries there (Spring can be configured for that). For write scalability beyond a single instance, more complex solutions like sharding or switching to a distributed database might be considered, but that’s usually far down the road. MySQL itself can handle a large number of users if properly indexed and if the data per user is not huge.

- **Caching Layer:** You can introduce caching for frequently accessed data to reduce database load. For example, if you often need to load user profiles, you could cache those in memory (e.g., using Spring Cache or a tool like Redis) to avoid hitting MySQL for every request. Since user data might change (like name or roles), use appropriate cache invalidation (maybe short TTLs or evict on updates).

- **Optimize Firebase Calls:** If you find yourself calling Firebase Admin SDK frequently (e.g., on every request to get user info), try to minimize that. It’s better to store needed info in MySQL as we did. If you need extra Firebase info (like custom claims), note that the JWT already carries custom claims so you wouldn’t need an extra call. Firebase Admin `verifyIdToken` is reasonably fast (it caches the public keys after first call), but relying on Spring Security’s JWT validation as we did is even more efficient (it’s just JWT library calls after keys are fetched). In high throughput scenarios, ensure the JWKs are cached – Spring Security does cache them by default.

- **Frontend Performance:** On the React side, build optimally for production (minified, chunked code). Use code splitting to avoid loading all pages’ code on first load. Utilize browser caching for static assets. A CDN (Content Delivery Network) for static files can drastically improve load times globally. Firebase Hosting and others provide CDN by default.

- **Load Balancing and CDN for Backend:** If your user base is global, consider deploying your backend in multiple regions or using a CDN for certain content. While dynamic API calls aren’t cacheable in a CDN by default, some public data or images could be. Also, using HTTP caching headers on GET responses (where appropriate) can reduce load (e.g., if user profile changes rarely, you could allow caching for a short period).

- **Asynchronous Work:** For any heavy operations on the backend triggered by user actions, use asynchronous processing or queues. Authentication itself is quick, but suppose upon first login you had to do extra work (like send a welcome email or process a large dataset), doing that asynchronously (via a message queue or separate thread) would prevent slowing down the auth flow.

- **Database Optimization:** As data grows, optimize queries and use indexes. For example, if you add a `last_login` field and plan to query users by last_login, index it. The current design mainly queries by primary key (UID) which is already optimal.

- **Monitoring and Auto-Scaling:** Use monitoring tools (like Spring Actuator, Prometheus/Grafana, New Relic, etc.) to keep an eye on memory, CPU, response times, DB performance. Set up auto-scaling rules if on cloud infrastructure (e.g., add more instances when CPU > 80%). This ensures your app can handle sudden spikes (like a surge of logins).

- **Security at Scale:** Enforce stricter quotas or rules as needed (for example, limit how often a single user can attempt logins to mitigate abuse, though Google also has its own protections). Also, consider periodic review of your Firebase security rules and Cloud project IAM to ensure minimal privileges as your project grows with possibly more team members.

- **Cost Considerations:** Firebase Auth is free for generous limits, but if usage grows significantly, ensure you’re on an appropriate Firebase pricing plan (Blaze plan for pay-as-you-go if needed). Similarly, MySQL hosting and outbound bandwidth for serving the React app or API have costs – optimize usage to keep things cost-efficient (e.g., unnecessary calls or very chatty clients might be optimized to reduce frequency).

In summary, the architecture presented is inherently scalable: using Firebase offloads authentication overhead, and using stateless JWTs means our backend can easily scale horizontally without session stickiness. MySQL can be scaled vertically (better hardware) or with replicas as needed for read-heavy scenarios. With proper optimization and monitoring, this stack can handle a large number of users while maintaining performance. And since we used established technologies (React for a snappy UI, Firebase for auth, Spring Boot for robust APIs), we benefit from their performance optimizations and best practices as well.

---
