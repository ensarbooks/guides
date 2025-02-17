# Implementing Google Login Authentication with Firebase in React, NestJS, and PostgreSQL: A Step-by-Step Guide

## Introduction

In this guide, we’ll build a full-stack authentication system using **Firebase** (Google sign-in), a **React (TypeScript)** frontend, a **NestJS** backend, and **PostgreSQL** for data storage. We will configure Firebase for Google OAuth, implement the login flow in React with the Firebase SDK, secure the NestJS API by validating Firebase JWTs, and store user info (and roles) in PostgreSQL. Advanced topics such as multi-factor auth, session management, role-based access control, deployment, and testing strategies are also covered. This guide assumes you are an experienced developer and focuses on precise, technical steps.

**Table of Contents:**

1. [Firebase Setup and Google Authentication Configuration](#firebase-setup)
2. [Implementing the Authentication Flow in React (TypeScript)](#react-auth)
3. [Securing the NestJS Backend with Firebase Auth and JWT](#nestjs-backend)
4. [Integrating PostgreSQL for User Data](#postgresql-integration)
5. [Advanced Authentication Features](#advanced-auth)
6. [Deployment Strategies (Frontend & Backend)](#deployment)
7. [Testing Strategies](#testing)
8. [Best Practices for Security and Performance](#best-practices)

## 1. Firebase Setup and Google Authentication Configuration <a name="firebase-setup"></a>

### 1.1 Create a Firebase Project and Web App

1. Go to the **Firebase Console** and create a new project ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=First%2C%20let%E2%80%99s%20create%20a%20Firebase,then%20click%20on%20Create%20Project)). Give it a name (e.g., "MyAuthProject"). You can disable Google Analytics for now if not needed ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=via%20the%20Firebase%20console%20here,then%20click%20on%20Create%20Project)).
2. After creation, in your Firebase project console, add a new **Web App** (click the **Web icon**). Give it a nickname and register it ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=In%20the%20same%20Project%20Settings,click%20the%20Add%20App%20button)). This will provide you with Firebase SDK config values (API key, Auth domain, etc.). Copy this config object for later use in the React app ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=You%20will%20be%20provided%20some,it%20will%20be%20required%20later)).
3. Still in Project Settings, under **Service accounts**, click _Generate new private key_. This downloads a JSON file with credentials for the Firebase Admin SDK ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=,NestJS%29%20side)). **Keep this file secure** – we’ll use it in the NestJS backend for server-side verification. Add this JSON to your backend (e.g., save as `firebase-service-account.json` and _DO NOT_ commit it to source control).

### 1.2 Enable Google Sign-In in Firebase Auth

1. In the Firebase console, navigate to **Authentication > Sign-in method**.
2. Enable the **Google** sign-in provider and configure any required OAuth consent details. Simply toggling Google "Enabled" will suffice for basic setup ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=Now%20to%20enable%20the%20authentication%2C,and%20enable%20the%20Google%20authentication)). You may be prompted to specify a project support email.
3. _(Optional)_ In the same Authentication settings, check **Authorized domains**. Firebase usually adds your app's domain (and `localhost`) automatically when you set up the web app. If you plan to use a custom domain or deploying to e.g. Netlify/Vercel, ensure that domain is listed; otherwise, Google sign-in may be blocked by OAuth.

At this point, Firebase is configured to allow Google account logins for your project. We have: the frontend config (API keys, etc.), and backend service account credentials. Next, we’ll implement the client-side login.

## 2. Implementing the Authentication Flow in React (TypeScript) <a name="react-auth"></a>

With Firebase set up, we can use the **Firebase Web SDK** to handle the Google login on the frontend.

### 2.1 Install Firebase SDK and Initialize Firebase

- Install Firebase in your React project (assuming you have a React + TypeScript app created, e.g. with Create React App or Vite):
  ```bash
  npm install firebase
  ```
- Create a Firebase config file (e.g. `src/firebase.ts`) to initialize the SDK:

  ```ts
  // src/firebase.ts
  import { initializeApp } from "firebase/app";
  import { getAuth, GoogleAuthProvider } from "firebase/auth";

  // Your Firebase config values (from step 1.1)
  const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    appId: "YOUR_APP_ID",
    // ...other keys like storageBucket, messagingSenderId, etc.
  };

  // Initialize Firebase app and Auth service
  const app = initializeApp(firebaseConfig);
  export const auth = getAuth(app);

  // Set up Google Auth Provider
  export const googleProvider = new GoogleAuthProvider();
  googleProvider.setCustomParameters({ prompt: "select_account" });
  ```

  This code initializes Firebase and sets up a Google provider. The `prompt: 'select_account'` parameter ensures the Google OAuth popup always asks the user to choose an account (useful if they’re signed into multiple accounts) ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=export%20const%20auth%20%3D%20firebase)).

### 2.2 Implement Google Sign-In Flow

To trigger Google Sign-In, we use Firebase Auth’s `signInWithPopup` (or `signInWithRedirect`). Here we’ll use the popup method for simplicity:

- Create a React component or utility function for login, e.g. `LoginButton.tsx`:

  ```tsx
  import React from "react";
  import { auth, googleProvider } from "../firebase";
  import { signInWithPopup } from "firebase/auth";

  const LoginButton: React.FC = () => {
    const handleLogin = async () => {
      try {
        await signInWithPopup(auth, googleProvider);
        // Firebase handles the popup OAuth flow.
      } catch (error) {
        console.error("Google sign-in error", error);
      }
    };

    return <button onClick={handleLogin}>Sign in with Google</button>;
  };

  export default LoginButton;
  ```

  When the user clicks this button, a Google OAuth popup appears. After the user authenticates with Google, Firebase receives the ID token from Google and signs the user in to Firebase. Under the hood, Firebase creates a user session and stores a refresh token in local storage by default (so the user stays logged in even on page refresh) ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=useEffect%28%28%29%20%3D,)).

- Optionally, you can use Firebase UI components or the Google One-tap API, but those are beyond our scope. The `signInWithPopup` method is straightforward and sufficient for our needs.

### 2.3 Handling User State and Tokens in React

After sign-in, you’ll likely want to access the authenticated user’s info and token to interact with your backend:

- **Auth State**: Firebase provides an `onAuthStateChanged` listener to react to login/logout events. For example, in your top-level component (App.tsx), you can listen and store the user:

  ```tsx
  import { onAuthStateChanged } from "firebase/auth";
  import { auth } from "./firebase";

  const [currentUser, setCurrentUser] = useState<firebase.User | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
    });
    return unsubscribe; // cleanup listener on unmount
  }, []);
  ```

  This will update `currentUser` whenever the user logs in or out ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=useEffect%28%28%29%20%3D,)). The `user` object contains details like `displayName`, `email`, `photoURL`, etc., which you can use in your UI (e.g., show the user's name or profile picture) ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=const%20Home%20%3D%20%28,div%3E)).

- **Retrieve JWT (ID Token)**: To secure API calls to our backend, we need the Firebase **ID token** for the authenticated user. This token is a JWT issued by Firebase. You can get it with `user.getIdToken()`. For example:

  ```ts
  const idToken = await auth.currentUser?.getIdToken();
  // send this token in an Authorization header to the backend
  ```

  You might call this in a React effect or whenever you need to make an API request. Typically, you would include this token in requests as a **Bearer token** in the HTTP header:

  ```ts
  await fetch("/api/protected-resource", {
    headers: { Authorization: `Bearer ${idToken}` },
  });
  ```

  On subsequent requests, you can call `getIdToken()` again; Firebase will return a cached token if it's not expired, or automatically refresh it using the stored refresh token if it has expired. This ensures the user’s token stays valid. (Firebase tokens expire every 1 hour by default.)

- **Logout**: Use `auth.signOut()` to log the user out (this clears the session and local token) ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=%3Cdiv%20className%3D,div%3E)). On logout, `onAuthStateChanged` will fire with `null`, so you can redirect or update UI accordingly.

**At this stage**, our React app can let users sign in with Google via Firebase, and we can retrieve the Firebase **ID token** (JWT) for the logged-in user. Next, we’ll set up the NestJS backend to verify these tokens and secure the API.

## 3. Securing the NestJS Backend with Firebase Authentication and JWT Validation <a name="nestjs-backend"></a>

The backend will trust Firebase as the Identity Provider. The high-level flow is: the React app sends the Firebase ID token in an API request header, and NestJS will verify this token (using Firebase Admin SDK) and authorize the user. We’ll use NestJS’s **Passport** integration to create a custom JWT strategy for Firebase.

### 3.1 NestJS Setup and Firebase Admin Initialization

- Ensure you have a NestJS project set up (Nest CLI can generate one: `nest new my-app`). Install dependencies for authentication:

  ```bash
  npm install @nestjs/passport passport passport-jwt firebase-admin
  ```

  (`passport-jwt` will help extract the token from headers, and `firebase-admin` allows verifying Firebase tokens.)

- Add your Firebase service account credentials to the backend. One approach is to store the JSON file and load it. For example, place the JSON in the project (or provide via environment). You can use `FirebaseAdmin.initializeApp` with a credential.

- Create a file `firebase-auth.strategy.ts` (e.g., in an `auth/` or `firebase/` directory):

  ```ts
  // firebase-auth.strategy.ts
  import { Injectable, UnauthorizedException } from "@nestjs/common";
  import { PassportStrategy } from "@nestjs/passport";
  import { Strategy } from "passport-jwt";
  import { ExtractJwt } from "passport-jwt";
  import * as admin from "firebase-admin";
  import * as serviceAccount from "../firebase-service-account.json"; // your service account key

  @Injectable()
  export class FirebaseAuthStrategy extends PassportStrategy(
    Strategy,
    "firebase-auth"
  ) {
    constructor() {
      super({
        jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
        ignoreExpiration: false, // we will let Firebase handle expiration
        secretOrKey: "", // not used, we use Firebase to verify
      });
      // Initialize Firebase Admin SDK
      admin.initializeApp({
        credential: admin.credential.cert(
          serviceAccount as admin.ServiceAccount
        ),
      });
    }

    async validate(token: string) {
      try {
        // Verify the token with Firebase Admin SDK
        const decodedToken = await admin.auth().verifyIdToken(token, true);
        return decodedToken;
      } catch (err) {
        // Token invalid or revoked
        throw new UnauthorizedException(`Firebase auth failed: ${err.message}`);
      }
    }
  }
  ```

  Let’s break down what this does:

  - We use a Passport **JWT strategy** named `'firebase-auth'`. The strategy’s `jwtFromRequest` extracts the token from the `Authorization: Bearer <token>` header ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=super%28,defaultApp)). We don’t provide a `secretOrKey` because we aren’t manually verifying the JWT signature; instead, in `validate()` we call `admin.auth().verifyIdToken(token)`.
  - `admin.initializeApp` is called once with our credentials. After this, `admin.auth().verifyIdToken` will use Google's public keys to verify the token’s signature and expiry. Passing `checkRevoked=true` (the second parameter) ensures that tokens that have been revoked (e.g., via Firebase console or if the user session is invalidated) are rejected ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=const%20firebaseUser%3A%20any%20%3D%20await,throw%20new%20UnauthorizedException)).
  - If verification succeeds, `decodedToken` contains the user’s Firebase UID and other claims (like email, name, and any custom claims). We return it, and NestJS will attach it as `req.user`. If verification fails, we throw `UnauthorizedException` to block access ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=.auth%28%29%20.verifyIdToken%28token%2C%20true%29%20.catch%28%28err%29%20%3D,)).

  **Note:** Make sure to enable JSON import in your TypeScript config (set `"resolveJsonModule": true` in `tsconfig.json`) if you import the service account JSON directly ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=unauthorized%20exception%20is%20thrown)). Alternatively, read the JSON from an environment variable or file system for production security.

### 3.2 Auth Guard and Protecting Routes

Now we need to tell NestJS to use this strategy to guard routes. Nest provides **Guards** for this purpose. We can create a guard that uses our `'firebase-auth'` strategy:

```ts
// firebase-auth.guard.ts
import { Injectable, ExecutionContext } from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";

@Injectable()
export class FirebaseAuthGuard extends AuthGuard("firebase-auth") {
  // Optionally, override handleRequest to attach user or handle errors
  handleRequest(err, user, info) {
    if (err || !user) {
      throw err || new UnauthorizedException(info);
    }
    return user; // user is the decoded Firebase token
  }
}
```

This guard extends Nest’s built-in AuthGuard, telling it to use the `'firebase-auth'` strategy we defined ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=%40Injectable,boolean%3E%28%27public%27%2C%20%5B%20context.getHandler%28%29%2C%20context.getClass%28%29%2C)). By default, if the strategy returns a user (decoded token), the request is allowed; otherwise it throws an Unauthorized. You can attach this guard to routes or controllers to protect them.

- **Apply the Guard**: For example, suppose we have a `ResourcesController` with a protected route:

  ```ts
  // resources.controller.ts
  import { Controller, Get, UseGuards, Req } from "@nestjs/common";
  import { FirebaseAuthGuard } from "../auth/firebase-auth.guard";

  @Controller("resources")
  export class ResourcesController {
    @Get()
    @UseGuards(FirebaseAuthGuard)
    getResources(@Req() request) {
      const user = request.user; // this is the decoded token
      return `This is a protected resource for ${user.uid}`;
    }
  }
  ```

  By using `@UseGuards(FirebaseAuthGuard)` on the route, only requests with a valid Firebase ID token will reach the handler ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=constructor%28private%20readonly%20resourcesService%3A%20ResourcesService%29%20,)). If the token is missing or invalid, NestJS will automatically respond with 401 Unauthorized before calling `getResources`.

- **Global Guard (optional)**: You can also apply the guard globally (in your main.ts or using `APP_GUARD` provider) if most of your endpoints are secured. In that case, you’d need a way to allow some public routes (like a health check). One approach is to add a custom metadata decorator (e.g., `@Public()`) and check for it in the guard. The LogRocket example shows using `Reflector` to bypass auth if a route is marked public ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=%7D%20canActivate%28context%3A%20ExecutionContext%29%20,return%20super.canActivate%28context)), but for brevity we won't detail that here.

- **Accessing User Info**: The `request.user` object will contain fields from the Firebase token. For example, `user.uid` (Firebase UID), `user.email`, `user.name`, etc. Use these in your controller/service as needed. For instance, you might use `user.uid` to look up the full profile in PostgreSQL (next section). NestJS can also inject this via a custom decorator `@User()` if you write one, or simply use `@Req()` or `@AuthUser()` from some libraries.

At this point, our backend is secured by Firebase Auth. We have effectively federated authentication: Google -> Firebase -> our NestJS. We have **not** created our own JWTs; instead, we trust Firebase’s JWT. The token the React app sends is the same token we validate on the server ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=What%E2%80%99s%20happening%20here%3F%20The%20JWT,an%20unauthorized%20exception%20is%20thrown)). This simplifies our auth flow and leverages Firebase’s security.

Next, let's integrate PostgreSQL to store user data and support additional auth logic (like roles).

## 4. Integrating PostgreSQL to Store User Data and Additional Auth Logic <a name="postgresql-integration"></a>

Using Firebase for authentication does not eliminate the need for a database; often we want to store additional user information or maintain our own user records. We will use **PostgreSQL** as our database, which NestJS can communicate with via an ORM or query builder (e.g., TypeORM, Prisma, or Knex). PostgreSQL will hold user profiles, app-specific settings, roles, etc., complementing Firebase Auth’s basic profile.

### 4.1 Setting Up PostgreSQL and an ORM in NestJS

- **Database Setup**: Ensure you have a PostgreSQL database running. For local development, you might use Docker or a local install. Create a database (e.g., `myapp_db`) and a user with password that NestJS can use.
- **Connect NestJS to Postgres**: Use an ORM or database library. For example, using TypeORM:
  ```bash
  npm install @nestjs/typeorm typeorm pg
  ```
  Configure TypeORM in `app.module.ts` (or a dedicated DatabaseModule) with your connection details (host, port, username, password, database). For example:
  ```ts
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      url: process.env.DATABASE_URL, // or manually specify host, port, etc.
      entities: [User],             // your entities
      synchronize: true,            // auto-create tables in dev (disable in prod)
    }),
    TypeOrmModule.forFeature([User]), // to inject User repository in services
    ...
  ]
  ```
  Or if using Prisma, set up the Prisma schema and client similarly. The key is that NestJS can now read/write to your Postgres database.

### 4.2 User Model and Repository

Define a **User** entity/model representing the data you want to store for each user. For example, a TypeORM entity:

```ts
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  firebaseUid: string; // Firebase UID from the token

  @Column()
  email: string;

  @Column()
  name: string;

  @Column({ default: "USER" })
  role: string; // application role (e.g., USER, ADMIN)

  // Additional fields: avatar, etc.
}
```

This is just an example schema – adjust as needed. We mark `firebaseUid` unique, ensuring one record per Firebase user. We also store email and name for convenience, but note that those come from Firebase and can be updated there (if the user changes their Google account name, etc.). Keeping them in sync is an important consideration (discussed below).

Use a NestJS **Service** and **Repository** to interact with this User entity. For instance, a `UsersService` with methods like `findByFirebaseUid(uid)` and `createUserFromToken(decodedToken)`.

### 4.3 Synchronizing Firebase Auth with the Database

**When to create or update the user in Postgres?** There are a few strategies:

- **On First Auth Request:** A simple approach is to create the user in the database the first time you see a valid token for that UID. For example, in the `validate()` function of our auth strategy or in a guard, after verifying the token, you can use a UsersService to find or insert a user. Pseudo-code:

  ```ts
  // In validate() or after guard passes
  const { uid, email, name } = decodedToken;
  let user = await this.usersService.findByFirebaseUid(uid);
  if (!user) {
    // New user logging in for the first time
    user = await this.usersService.create({ firebaseUid: uid, email, name });
  }
  // Attach user to request (for controllers to use)
  request.userRecord = user;
  ```

  This way, the first time a user authenticates, we capture their info in Postgres. Subsequent requests find the existing record.

- **On Every Request (Update):** If you want to update user info (like email or name) each time they login, you could refresh those fields from the token. However, hitting the database for every request may be unnecessary overhead if that data rarely changes. You might choose to update occasionally or provide a user profile update endpoint.

- **Via Firebase Triggers:** An alternative advanced approach is to use Firebase Auth **webhooks or Cloud Functions** to sync users. For example, Firebase can trigger a Cloud Function on user creation or deletion. That function could call your NestJS backend (or write to the DB directly) to create or remove the user record. This decouples the creation from the request flow. According to one common practice, developers treat Firebase as the source of truth for auth and use external DB for extended profile data, syncing via background events ([When using Firebase Auth with Postgres, how do you ensure your User table is in sync with Firebase? : r/Firebase](https://www.reddit.com/r/Firebase/comments/189df13/when_using_firebase_auth_with_postgres_how_do_you/#:~:text=%E2%80%A2)) ([When using Firebase Auth with Postgres, how do you ensure your User table is in sync with Firebase? : r/Firebase](https://www.reddit.com/r/Firebase/comments/189df13/when_using_firebase_auth_with_postgres_how_do_you/#:~:text=2,Auth%20when%20an%20update%20occurs)). However, implementing a Cloud Function to call your server is extra complexity. In our case, doing it on first request as above is simpler and works well for most applications.

- **Keep Data in Sync:** If a user updates their profile (say, changes email via Google), you might not immediately know in your database. You could periodically update from token, or provide UI to let users update their profile in your app which then updates both Firebase (via Admin SDK) and your DB. Some developers choose to treat Firebase as just an identity provider and keep all authoritative profile info in Postgres, updating Firebase only for things like password changes ([When using Firebase Auth with Postgres, how do you ensure your User table is in sync with Firebase? : r/Firebase](https://www.reddit.com/r/Firebase/comments/189df13/when_using_firebase_auth_with_postgres_how_do_you/#:~:text=I%E2%80%99m%20sort%20of%20facing%20this,%E2%80%9Cin%20sync%E2%80%9D%20with%20my%20db)).

For our guide, we’ll assume a straightforward approach: create on first login if not exists, and maybe update basic fields if needed. The main point is **yes, you typically need a User table in Postgres in addition to Firebase Auth** (Firebase’s user store can’t hold arbitrary data except limited custom claims) ([When using Firebase Auth with Postgres, how do you ensure your User table is in sync with Firebase? : r/Firebase](https://www.reddit.com/r/Firebase/comments/189df13/when_using_firebase_auth_with_postgres_how_do_you/#:~:text=%E2%80%A2)).

### 4.4 Additional Authentication Logic

With both Firebase and your database in play, you can implement additional logic, for example:

- **Email Verification Enforcement**: Firebase tokens include an `email_verified` field. If you require verified emails, check `decodedToken.email_verified` in the backend and reject the request if false. You could also prevent unverified users from being created in your DB or mark them as unverified. Firebase can send verification emails out-of-the-box for email/password users; for Google sign-in, the email is already verified by Google.

- **Disabled/Banned Users**: You might maintain a flag in your DB for banned users. If a user is banned in your system, you can reject their requests even if Firebase token is valid. Firebase Admin SDK allows disabling a user as well (which would make `verifyIdToken` fail via `auth().verifyIdToken(..., true)` if the account is disabled or token revoked). For a belt-and-suspenders approach, check a `user.isBanned` in your DB on each request as well.

- **Multiple Login Methods**: If you later add other providers (email/password, Facebook, etc.), consider how to link those to the same user record. Firebase provides a UID per user that stays the same regardless of provider (if you use Firebase's linking). As long as you use Firebase UID as the key in your DB, it will work for any provider.

- **Custom Auth Flows**: You might have a scenario where you want to use Firebase Custom Tokens to authenticate from your server (for instance, if you allow API key auth or a legacy auth alongside Firebase). Firebase Admin can create custom JWTs that clients can use to sign in ([Create Custom Tokens | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/create-custom-tokens#:~:text=Create%20Custom%20Tokens%20,JWTs)). Those custom tokens result in a Firebase UID as well. Covering this is beyond scope, but know that it's possible if needed for server-to-server auth.

We now have a robust backend that uses Firebase for authentication and Postgres for user data. Next, we’ll explore advanced features like MFA and roles.

## 5. Advanced Authentication Features <a name="advanced-auth"></a>

### 5.1 Multi-Factor Authentication (MFA)

Multi-factor authentication adds an extra layer of security by requiring a second step (e.g., SMS code or TOTP) after the initial login ([Multi-Factor(MFA) Authentication in React JS using firebase - DEV Community](https://dev.to/hasnain01hub/multi-factormfa-authentication-in-react-js-using-firebase-ljo#:~:text=So%2C%20in%20July%202022%20Firebase,more%20layer%20to%20authenticate%20users)). Firebase supports MFA for SMS and TOTP (Time-based One-Time Password, like Google Authenticator) as of 2022. To implement MFA in our stack:

- **Enable MFA in Firebase**: In the Firebase console, under **Authentication > Sign-in method > Advanced**, enable multi-factor authentication (SMS or TOTP as needed) ([Multi-Factor(MFA) Authentication in React JS using firebase - DEV Community](https://dev.to/hasnain01hub/multi-factormfa-authentication-in-react-js-using-firebase-ljo#:~:text=4,section%20of%20your%20firebase%20project)). For SMS, you’ll need to set up a phone provider (Firebase may ask for a testing phone number setup or reCAPTCHA config for web).

- **Enroll Users with MFA**: Firebase will not automatically enroll users in MFA just by enabling it. You must write logic on the client to enroll a user’s second factor. For example, after a user signs in (primary factor), you can use the Firebase JS SDK to prompt for phone number verification:

  - Use `firebase.auth().currentUser.multiFactor.enroll` with a phone auth provider or TOTP authenticator. This involves sending an SMS and verifying it. The flow is a bit complex: you must get an SMS verification code and then call `enroll(secondFactorAssertion)`. (Due to complexity, refer to Firebase’s MFA docs for detailed code samples ([MFA Firebase & React Flow - Stack Overflow](https://stackoverflow.com/questions/69548183/mfa-firebase-react-flow#:~:text=I%20am%20trying%20to%20enroll,platform%2Fdocs%2Fweb%2Fmfa)).)
  - Alternatively, you can enforce that certain actions require MFA: e.g., before performing a sensitive action, require the user to complete a second-factor auth (`multiFactor.getSession()` and send an SMS, etc.).

- **MFA Sign-In Flow**: When MFA is enabled and a user has enrolled, the sign-in process changes. For example, with SMS MFA:

  1. User signs in with Google via `signInWithPopup`. Firebase recognizes the user has MFA enabled and does **not** complete sign-in automatically.
  2. Instead, you’ll get an `auth/multi-factor-auth-required` error from signIn, with a `Resolver` object.
  3. Use this resolver to prompt the user for the second factor (e.g., SMS code input). Firebase SDK provides methods to continue the sign-in with the code. Once verified, the user is fully signed in and the ID token now reflects MFA.

- **Backend Considerations**: The Firebase ID token will contain information about second factor auth if applicable. For most cases, you don’t need to do anything special on the backend; a valid token is a valid token. Just be aware that if you **require** MFA for certain operations, you should enforce that users have MFA. Firebase doesn’t put a specific claim like “mfa”: true in the token (it might include `amr` or `auth_time` claims though). You might have to keep track of MFA enrollment in your DB (if, for example, you want to only allow certain actions if MFA was used recently). This gets into advanced security policy territory.

In summary, enabling MFA means additional UI/UX work on the frontend and possibly logic to encourage or enforce MFA, but the backend verification remains the same – Firebase handles the heavy lifting of ensuring the token is only issued after MFA is satisfied.

### 5.2 Session Management

By default, our approach is **stateless**: the frontend holds a token and sends it with each request. This is suitable for SPAs and mobile apps. However, there are cases where you may want a more traditional session approach or optimize how sessions are handled:

- **Firebase Session Persistence**: The Firebase SDK by default uses long-term persistence (localStorage) for the logged-in user, meaning the user stays signed in across page refreshes. You can change this to session-only or none using `auth.setPersistence()` with `browserSessionPersistence` or `inMemoryPersistence` depending on your needs. For example, for higher security (on a public computer), you might use session persistence so that closing the tab logs the user out. For most apps, the default is fine.

- **Session Cookies (Firebase)**: Firebase provides a mechanism to exchange an ID token for a **session cookie** (HTTP only cookie) ([Manage Session Cookies | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/manage-cookies#:~:text=Google%20firebase,that%20rely%20on%20session%20cookies)). This is useful for traditional web apps where you want the server to manage sessions instead of the client storing tokens. The flow is: after sign-in on the client, send the ID token to a special backend endpoint (`/sessionLogin`). On the backend, use `admin.auth().createSessionCookie(idToken, { expiresIn })` to mint a session cookie and set it in a response cookie. Subsequent requests from that browser include the cookie, and you verify it with `admin.auth().verifySessionCookie` on the backend. The benefit is the token is stored in a secure, HTTP-only cookie (not accessible via JS, mitigating XSS attacks on the token) and can have a longer lifetime (up to 14 days) ([Manage Session Cookies | Firebase Authentication - Google](https://firebase.google.com/docs/auth/admin/manage-cookies#:~:text=Google%20firebase,that%20rely%20on%20session%20cookies)). The downside is increased complexity and it shifts to a stateful model (you might need a logout endpoint to clear the cookie, etc.). NestJS can easily handle this if you choose: you’d treat the cookie similar to how we did the header token (just extract from cookie and verify). The Firebase Admin SDK has a separate method for session cookies, but usage is analogous.

- **Maintaining Sessions Server-Side**: Another approach (less recommended for JWT-based auth) is to create your own server-side sessions (e.g., using express-session or storing session IDs in Redis). In this architecture, it’s usually unnecessary, since Firebase already provides a token-based session. Stateless JWT sessions scale better (no session store needed) ([Nestjs Firebase Login Integration | Restackio](https://www.restack.io/p/nestjs-firebase-login-answer-cat-ai#:~:text=Stateless%20Sessions)). But if you did use a server session, you could store the Firebase UID in the session store after verifying login, and then trust that session cookie on subsequent requests. This is more complex and not needed unless you have legacy requirements.

- **Token Refresh**: The Firebase client SDK automatically refreshes the ID token every hour using a hidden refresh token. If you go the session cookie route, you can set an expiration and require re-login or token refresh after a certain time (or implement silent refresh by re-authenticating the user with the refresh token, which Firebase can do for you).

- **Logout**: In a stateless scenario, logout is done client-side (`auth.signOut()` which also invalidates the refresh token in Firebase). In a stateful cookie scenario, you would also want a logout endpoint to clear the session cookie and possibly revoke the Firebase token. Firebase Admin can revoke tokens via `admin.auth().revokeRefreshTokens(uid)` which invalidates all tokens for a user issued before the revocation time.

**Bottom line**: For most SPA use cases, sticking with Firebase’s client-managed tokens (and our guard on backend) is sufficient. Just ensure you protect the token on the client (if not using cookies, the token is in JS memory or localStorage – which is vulnerable to XSS, so guard your app against XSS!). If your app has high security needs, consider using HttpOnly cookies via the session cookie approach and secure them properly (Secure, SameSite, etc.).

### 5.3 Role-Based Access Control (RBAC)

Many applications require different levels of access (roles like "USER", "ADMIN", etc.). We have a `role` field in our User table for this purpose. How do we enforce roles?

**Option 1: Use Firebase Custom Claims** – Firebase allows attaching custom claims to a user’s ID token via the Admin SDK. For example, you can set an `"admin": true` claim on certain users. This will include `admin: true` in the token payload, and our backend can check for it. Custom claims are set server-side:

```ts
await admin.auth().setCustomUserClaims(uid, { role: "ADMIN" });
```

The user would need to sign-out and sign-in (or refresh token) to get a new token with this claim. Once set, every ID token for that user will carry the role info. Our NestJS `decodedToken` would then have `decodedToken.role == 'ADMIN'`. We could then build a **RolesGuard** that checks `request.user.role` against allowed roles. For example, using a custom decorator `@Roles('ADMIN')` and guard logic to compare ([Integrating Firebase Authentication into NestJS with nestjs-firebase-auth - DEV Community](https://dev.to/alpha018/integrating-firebase-authentication-into-nestjs-with-nestjs-firebase-auth-55m6#:~:text=Then%2C%20use%20the%20,role%20validation%20for%20specific%20endpoints)) ([Integrating Firebase Authentication into NestJS with nestjs-firebase-auth - DEV Community](https://dev.to/alpha018/integrating-firebase-authentication-into-nestjs-with-nestjs-firebase-auth-55m6#:~:text=%40RolesGuard%28Roles,admin)). This approach means **no extra DB lookup** for roles on each request, since the role is embedded in the token. However, custom claims have size limits and are meant for small pieces of info like roles or flags ([When using Firebase Auth with Postgres, how do you ensure your User table is in sync with Firebase? : r/Firebase](https://www.reddit.com/r/Firebase/comments/189df13/when_using_firebase_auth_with_postgres_how_do_you/#:~:text=%E2%80%A2)). They are great for RBAC.

**Option 2: Use Database Roles** – Alternatively, use the role field from the Postgres User record. In the request handling, once you have `userRecord` (from DB), check `userRecord.role`. You can implement this check either in each service/controller (not ideal) or via a Guard/Interceptor. For instance, you can create a guard `RolesGuard` that checks `request.userRecord.role`. You would need a way to know which roles are allowed for a route (e.g., a custom decorator like `@Roles('ADMIN')`). This is similar to using custom claims but without embedding in the token. It does incur a DB call to fetch the user record (which we already do when attaching userRecord). Since we likely have the user’s DB record anyway from section 4.3, using it is fine.

**Which to choose?** If your roles are fairly static and you want to minimize DB calls, custom claims are neat. Firebase even has built-in checks for roles if using the Firebase-REST JWT verification, but since we are using Admin SDK, we can manually check. The Dev Community library example we saw uses custom claims extensively, setting roles and then using a guard to validate them ([Integrating Firebase Authentication into NestJS with nestjs-firebase-auth - DEV Community](https://dev.to/alpha018/integrating-firebase-authentication-into-nestjs-with-nestjs-firebase-auth-55m6#:~:text=enum%20Roles%20,ADMIN%27%2C%20USER%20%3D%20%27USER%27%2C)) ([Integrating Firebase Authentication into NestJS with nestjs-firebase-auth - DEV Community](https://dev.to/alpha018/integrating-firebase-authentication-into-nestjs-with-nestjs-firebase-auth-55m6#:~:text=%40RolesGuard%28Roles,admin)). On the other hand, using the DB is straightforward and keeps all user info in one place. You can even combine them: for example, set the custom claim when a user’s role changes in the DB. That way the token and DB are in sync.

**Implementing RBAC in NestJS**:

- Create a custom decorator and guard for roles. Quick example using DB approach:

  ```ts
  // roles.decorator.ts
  export const Roles = (...roles: string[]) => SetMetadata("roles", roles);

  // roles.guard.ts
  @Injectable()
  export class RolesGuard implements CanActivate {
    canActivate(context: ExecutionContext): boolean {
      const requiredRoles = this.reflector.get<string[]>(
        "roles",
        context.getHandler()
      );
      if (!requiredRoles) return true;
      const req = context.switchToHttp().getRequest();
      const user: User = req.userRecord;
      return user && requiredRoles.includes(user.role);
    }
  }
  ```

  Now you can use `@Roles('ADMIN')` on a controller method, and apply both `UseGuards(FirebaseAuthGuard, RolesGuard)`. This ensures the user is authenticated and has the required role. If using custom claims, the logic is similar but you might check `req.user.role` from the token instead.

- When assigning roles, if it’s done by an admin in your app, you would update the DB and possibly call `setCustomUserClaims` so that future tokens carry the role. Keep in mind, Firebase custom claims are limited to 1000 bytes total and adding too many or too large data can break the token.

- If you have hierarchical roles or permissions, you might integrate a library or design a more complex system of privileges. That goes beyond basic RBAC, but NestJS’s guard system will still be the enforcement point.

Now that we have covered building the system, let's discuss how to deploy both the frontend and backend and ensure everything works in production.

## 6. Deployment Strategies <a name="deployment"></a>

Deploying our full-stack application involves hosting the React frontend and the NestJS backend (with its Postgres database). We’ll discuss strategies and considerations for each:

### 6.1 Deploying the React Frontend (e.g., Vercel, Netlify)

Modern React apps (if built with CRA, Next.js, Vite, etc.) can be deployed as static assets or as an SPA. Since our authentication uses Firebase (which is client-side for front-end), we don’t need any special server processing for the React app. We can build and serve it on any static hosting.

**Options**:

- **Vercel**: Vercel is great for Next.js, but also supports static React apps. If using Create React App or Vite, you can simply run `npm run build` and then deploy. On Vercel, you can connect your GitHub repo and it will auto-build and deploy on push. You might need to specify the build command (`npm run build`) and output directory (`build/` for CRA) in the Vercel settings, but Vercel often detects CRA automatically ([How to Deploy a React Site with Vercel](https://vercel.com/guides/deploying-react-with-vercel#:~:text=Install%20the%20Vercel%20CLI%20and,correct%20settings%20for%20your)). With Vercel, your app will be hosted at `<your-project>.vercel.app` (you can add custom domain). Ensure that domain is added to Firebase Auth authorized domains as mentioned earlier.

- **Netlify**: Similarly, Netlify can watch your repo. Configure build settings (CRA is auto-detected usually) ([How to deploy React Apps in less than 30 Seconds - Netlify](https://www.netlify.com/blog/2016/07/22/deploy-react-apps-in-less-than-30-seconds/#:~:text=How%20to%20deploy%20React%20Apps,3%3A%20Redirect%20and%20rewrite%20rules)). Netlify will give you a `<project>.netlify.app` domain by default. Add it to Firebase authorized domains if using Google sign-in from there.

- **Other**: You can also use GitHub Pages (for static sites), Firebase Hosting (since we’re using Firebase anyway – Hosting would give you a free SSL and global CDN for the frontend), or any web server to serve the static files. Both Vercel and Netlify offer easy CI/CD which is why they’re popular.

**Environment Variables**: If you have any environment-specific settings in React (like `REACT_APP_API_URL` to point to your backend), set those in your hosting platform’s configuration (Vercel’s dashboard or Netlify’s UI). Note that the Firebase client config (API key, etc.) is not sensitive on its own – it’s safe to embed in the frontend ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=%2F%2F%20Initialize%20Firebase%20firebase)). But if you had other secrets (which you should not in frontend), ensure they are handled properly.

After deployment, test the React app’s login button. It should pop up Google and redirect back. Google might complain if the OAuth redirect is not allowed – but Firebase SDK uses a generic redirect URL on your own domain, which should be allowed as long as the domain is whitelisted in Firebase.

### 6.2 Deploying the NestJS Backend (e.g., AWS, Heroku, DigitalOcean)

For the NestJS server, we need to host a Node.js application and also have a connection to PostgreSQL. Common approaches:

- **Heroku (with Postgres add-on)**: Heroku is developer-friendly. You can push your NestJS app and use the free tier of Heroku Postgres for the database. Steps:

  1. Commit your code to a Git repo.
  2. Create a Heroku app (`heroku create`).
  3. Add Postgres: `heroku addons:create heroku-postgresql:hobby-dev`. This provisions a database; the connection URL is stored in `DATABASE_URL` config var ([Deploy nestjs with postgres database to heroku - Reddit](https://www.reddit.com/r/Nestjs_framework/comments/i68mt3/deploy_nestjs_with_postgres_database_to_heroku/#:~:text=Deploy%20nestjs%20with%20postgres%20database,with%20a%20value%20that)).
  4. Set other env vars: `heroku config:set NODE_ENV=production FIREBASE_SERVICE_ACCOUNT="$(< path/to/serviceAccount.json base64 or credentials )"` etc. For the Firebase credentials, you might store them as an environment variable. One strategy is to base64-encode the JSON and decode in your app. Or break out important fields into separate vars (not as convenient).
  5. Push to Heroku: Heroku will detect a Node.js app and install dependencies. Make sure you have a start script (`npm run start:prod` for example, which runs `node dist/main.js` after build). Heroku Node buildpack will run `build` script if present. Alternatively, you can use a Docker container on Heroku.
  6. Once deployed, your NestJS app will run on some dyno (web process). Ensure you’ve set the PORT config if needed (Nest by default uses 3000; Heroku provides `PORT` env var). In Nest, use `app.listen(process.env.PORT || 3000)`.
  7. The Firebase Admin SDK will need the service account. If you set it via env, parse it properly in your strategy. For instance, `credential: admin.credential.cert(JSON.parse(Buffer.from(process.env.FIREBASE_SERVICE_ACCOUNT, 'base64').toString('utf8')))` if you did base64.

- **AWS**: There are many ways on AWS:

  - _Elastic Beanstalk_: EBS can take your Node app and handle deployment. You’d upload the code or connect via CLI. It can also provision a database (or you use Amazon RDS for Postgres separately). EBS is basically a managed EC2 with some orchestration. It’s straightforward and similar to Heroku in concept.
  - _EC2 or Docker_: You can manually set up an EC2 instance, install Node, and run the Nest app (using PM2 process manager for example). Or better, create a Docker image for your NestJS app and run it on an EC2 or ECS (Elastic Container Service). ECS with Fargate allows running containers without managing VMs. You’d also set up an RDS Postgres for the database. This route gives more control (and complexity).
  - _Serverless (Lambda)_: NestJS can be made to run on AWS Lambda behind API Gateway, but it requires using an adapter (like nestjs-serverless package) and cold start times might be an issue. It’s an advanced deployment scenario and not as straightforward as above options.
  - _AWS App Runner_: A newer service that can directly deploy a web service from a container or source, which might simplify deploying a Nest container.

  For AWS, whichever method, ensure your environment variables (DB URL, Firebase creds, etc.) are configured. Also set up proper logging/monitoring (CloudWatch if on AWS). If using RDS for Postgres, put the DB connection info in your Nest config.

- **DigitalOcean**:

  - _Droplet (VM)_: You can treat a DO Droplet like an unmanaged server. SSH in, install Docker or Node, run your app. You’ll have to handle process management (Docker or PM2) and environment setup.
  - _App Platform_: DO’s App Platform is a PaaS similar to Heroku. You can point it to a GitHub repo. It can deploy a Node app and also add a managed Postgres database. Configuration is done via a `spec` or the web UI (specifying build command, run command, env vars, etc.). This is simpler than managing your own droplet.
  - _Kubernetes_: If you use DO’s Kubernetes service, you could deploy NestJS in a k8s pod with a Postgres pod or DO managed DB. This is likely overkill for many cases.

- **Firebase (for backend)**: Note, Firebase has Cloud Functions and Firebase Hosting, but NestJS is not designed to run on Firebase Functions without modification. It’s possible (by creating an Express server and using Firebase Functions), but beyond our scope. We mention this because sometimes one might ask "Why not host the API on Firebase too?" – you could use Cloud Functions or Cloud Run with a container if you want a Google-stack deployment.

**Domain and CORS**: If your frontend is hosted on one domain (say, `myapp.vercel.app`) and backend on another (say, Heroku’s `myapi.herokuapp.com` or a custom domain), configure CORS on your NestJS app. NestJS can enable CORS easily:

```ts
app.enableCors({
  origin: ["https://myapp.vercel.app"], // front-end origin
  credentials: true,
});
```

Since our auth token is in the header, we just need to allow the origin. (If we used cookies, we’d need `credentials: true` and proper sameSite.) Make sure to update allowed origins if you use custom domains.

**PostgreSQL in Production**: If using Heroku Postgres or DO DBaaS or RDS, use the provided connection URL. On Heroku, `DATABASE_URL` is set automatically ([Deploy nestjs with postgres database to heroku - Reddit](https://www.reddit.com/r/Nestjs_framework/comments/i68mt3/deploy_nestjs_with_postgres_database_to_heroku/#:~:text=Deploy%20nestjs%20with%20postgres%20database,with%20a%20value%20that)). In others, you may get separate host, user, pass that you combine or set individually. Use SSL if required by host (some managed DBs require SSL connection). Also run migrations or sync to ensure the User table exists in production.

**Firebase Settings for Production**: Nothing special needs to be done in Firebase for production, except maybe to add the production domain to Auth authorized domains as mentioned. The same Firebase project can be used for dev and prod, but many choose to have separate Firebase projects for dev vs prod environments (so as not to mix test users with real users, etc.). In that case, you’d have different config values for each. That’s a choice depending on your workflow.

### 6.3 Summary of Deployment Best Practices

- **Environment Variables**: Do not hardcode secrets. Keep service account JSON out of your repo. Use env vars or secret managers. Ensure your build process (CI/CD) supplies these to your app.
- **Build Optimizations**: For frontend, use production builds (minified, etc.). For backend, prune dev dependencies. If using Docker, use multi-stage builds to get a slim image.
- **Monitoring**: After deployment, set up logging and monitoring. Check Firebase Auth dashboard for any errors. Use application performance monitoring if needed (LogRocket on the frontend, or NestJS logs, etc.).
- **Scaling**: Both Vercel/Netlify and Heroku/AWS handle scaling differently. If expecting heavy usage, be mindful of rate limits. Firebase Auth can handle huge scale for logins, but your NestJS and DB need scaling (e.g., more dynos, horizontal scaling, connection pooling). Use load testing to identify bottlenecks.

Now, with deployment covered, let's plan how to test our implementation to ensure reliability.

## 7. Testing Strategies <a name="testing"></a>

Testing an authentication system is crucial to catch issues early. We should test components in isolation (unit tests), the integration between them (integration tests), and the end-to-end user scenario (E2E tests).

### 7.1 Unit Tests

- **Frontend Unit Tests**: Test React components and util functions. For example, you might mock the Firebase Auth module to test that your `LoginButton` calls `signInWithPopup` when clicked. Using Jest and React Testing Library, you can simulate events and assert outcomes. Since the actual Firebase SDK opens a popup, you’d mock that out. You can also test that your context or Redux state updates correctly when a user logs in (perhaps by simulating an `onAuthStateChanged` callback).
- **Backend Unit Tests**: Test NestJS services and guards in isolation. For instance:
  - Test the `UsersService` with a mock repository to ensure `create` and `findByFirebaseUid` work as expected.
  - Test the `FirebaseAuthStrategy.validate()` method by mocking `admin.auth().verifyIdToken`. You can simulate a valid token (return a decoded token object) and an invalid token (throw an error) and assert that it returns the user or throws `UnauthorizedException`. This ensures your strategy logic (especially any custom handling you add) works.
  - If you have a `RolesGuard`, test that given a context with a user of certain role and requiredRoles, it returns true/false appropriately. Use reflection to simulate metadata (Nest provides `Reflector` you can instantiate for tests).
- **Utilities**: If you wrote any helper functions (maybe for parsing tokens or managing cookies), write tests for those.

In unit tests, you will frequently **mock external dependencies** like the Firebase Admin SDK and database connections. You don’t want unit tests to actually connect to Firebase or Postgres. Use Jest spies or injection tokens to provide dummy implementations.

### 7.2 Integration Tests (Backend)

Integration tests involve testing the API endpoints and possibly the database together, to ensure the pieces integrate correctly. In NestJS, you can use `@nestjs/testing` package to create a testing module that includes your real modules but maybe with some overrides.

- A common approach: spin up a NestJS app in memory (or a test environment) and use **Supertest** to send HTTP requests to it. For example, test that when hitting `GET /resources` with a valid Authorization header, you get a 200 and the expected response, but with an invalid token you get 401. This effectively tests the guard + controller + strategy integration. You would likely **mock** the Firebase Admin verification in this context to return a known decoded token (to avoid calling Google in tests). One way to do this is to spy on `admin.auth().verifyIdToken` or, better, in your strategy file, abstract the admin call so you can inject a fake. If using the actual `firebase-admin` in tests, it might try to load credentials. Instead, provide a stub that returns a predetermined object for any token. For instance, in your TestingModule, replace the `FirebaseAuthStrategy` with a fake that just checks if token == "test-token" then returns a fake UID. This is similar to mocking JWT in Nest tests ([NestJS mock JWT authentication in e2e tests - Stack Overflow](https://stackoverflow.com/questions/57629191/nestjs-mock-jwt-authentication-in-e2e-tests#:~:text=Overflow%20stackoverflow,want%20to%20insert%20credentials)). Some developers choose to bypass auth in integration tests by using a special testing guard that always returns a user (especially if you want to focus on testing business logic beyond auth).

- Test with the database: You can use a **test database** (e.g., a separate PostgreSQL schema or an in-memory DB). Some use SQLite for simplicity if your ORM supports it, or spin up a Docker Postgres for tests. The idea is to run the real DB queries to ensure your TypeORM entities and queries work. This catches issues like mismatched column names or transaction logic, which pure unit tests might miss ([NestJS Integration and E2E Tests with TypeORM, PostGres, and JWT](https://firxworx.com/blog/code/nestjs-integration-and-e2e-tests-with-typeorm-postgres-and-jwt/#:~:text=This%20guide%20covers%20a%20basic,connectivity%2C%20and%20JWT%20for%20authentication)) ([NestJS Integration and E2E Tests with TypeORM, PostGres, and JWT](https://firxworx.com/blog/code/nestjs-integration-and-e2e-tests-with-typeorm-postgres-and-jwt/#:~:text=Regardless%20of%20where%20you%20stand,of%20an%20overall%20testing%2FQA%20strategy)). Just be sure to clean up data between tests (tear down or use transactions that roll back). For example, using TypeORM’s `synchronize` to create schema and then dropping after, or manually deleting from tables between tests.

- Integration test cases to consider:
  - Hitting a protected route without token -> expect 401.
  - Hitting with a malformed token -> 401.
  - Hitting with a valid token for a user that doesn’t exist in DB -> it should create the user and return success (and maybe check DB entry).
  - Hitting with valid token for a user that exists -> returns expected data from the controller/service.
  - If role-based route: token with insufficient role -> 403 (you might implement this as 403 Forbidden).
  - Multi-factor edge: (This is hard to simulate in integration test without actual Firebase) – but you could simulate a decodedToken that was MFA. Usually not needed to test separately.

The key is to test the interactions between your Nest guards, services, and DB. Tools like Supertest make it easy to simulate HTTP calls to the Nest app as if a client was calling it.

### 7.3 End-to-End Testing (E2E)

End-to-end tests go through the entire system – from the frontend UI to the backend and database. This usually involves a real browser environment.

- **Using Cypress or Playwright**: These are popular frameworks to automate a browser. You can write a test like:

  1. Launch the React app in a test environment (maybe on localhost or a staging site).
  2. Click the "Sign in with Google" button.
  3. Complete the Google login flow.
  4. Verify that upon redirect, the app shows as logged in (e.g., displays the user's name) and that protected data is fetched from the backend.
  5. Perhaps test that refreshing the page stays logged in, and that logout works.

  However, automating the **Google OAuth popup** is tricky. You might not want your test suite to actually depend on Google's UI. There are a few approaches:

  - Use a **Firebase Auth Emulator** for tests ([Connect your app to the Authentication Emulator - Firebase - Google](https://firebase.google.com/docs/emulator-suite/connect_auth#:~:text=Google%20firebase,For)). The Firebase emulator can simulate Google sign-in without real Google accounts. You can configure the emulator to auto-sign-in a test user. For example, set up the Auth emulator and use a special OAuth test token. This is advanced but doable – it allows you to bypass real Google interaction and instead get a known ID token for a fake user.
  - Alternatively, you could write E2E tests that **mock the authentication step**. For instance, start your frontend in a mode where it doesn’t actually call `signInWithPopup` but directly sets a fake user (for testing only). This requires adding test hooks in your code (not always ideal in production code).
  - Another approach: use Cypress tasks to talk to Firebase Admin SDK directly. For example, create a user via Admin SDK and generate a custom auth token or use the REST API to get an ID token, then inject that into the app (e.g., set localStorage with the token or start the app with that user pre-logged in).

- **API E2E**: If automating the UI is too brittle, consider at least an end-to-end test from the API perspective: Run the backend (perhaps against a test database), and simulate a real Firebase token. You can actually use the Firebase Admin SDK in tests to mint a **custom token** and then exchange it for an ID token (via Firebase Auth REST API or emulator). This gives you a fully valid JWT that your backend will consider legit. Then use a HTTP client to call your API with that token and verify the responses. This is more of an integration test, but at the system level including token generation.

- **Testing multi-factor**: Testing MFA in E2E would involve automating the second factor input. If using emulator, you can pre-configure an SMS code for a test phone. If not, it’s very complex to automate receiving a real SMS. Probably skip MFA in automated E2E, or test it manually.

- **Performance**: You might also simulate multiple users logging in concurrently or repeated requests to see how your system holds up (though this is more load testing than functional testing).

Remember to **clean up** after E2E tests – e.g., delete any test accounts created in Firebase (Firebase Auth emulator resets on restart, which is convenient in tests). For the database, use a separate test database or clear the records created.

Using a combination of these testing strategies ensures your auth system is solid. Unit tests give quick feedback on logic, integration tests verify the system components talking to each other (with some realistic aspects like database), and E2E tests ensure the _user’s perspective_ (clicking buttons, etc.) results in the intended outcome across the entire stack.

## 8. Best Practices for Authentication Security and Performance Optimization <a name="best-practices"></a>

Finally, let’s summarize some best practices to keep our authentication robust and efficient:

### 8.1 Security Best Practices

- **Secure Credentials**: Treat your Firebase service account JSON and PostgreSQL credentials as secrets. Use environment variables or secret management – never commit them to the repo. In Firebase, you can also restrict the service account’s permissions to only what’s needed (the default service account has broad Firebase project access, which is usually fine, but in high-security environments consider principle of least privilege).
- **Use HTTPS**: Always host your app and API over HTTPS. This is non-negotiable for security since tokens could be intercepted on an unsecured connection. Platforms like Vercel/Netlify/Heroku provide HTTPS by default on their domains. If using custom domains, ensure to set up TLS certificates.
- **Validate Tokens Properly**: We used `verifyIdToken(token, true)` which not only checks the signature but also whether the token has been revoked ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=const%20firebaseUser%3A%20any%20%3D%20await,throw%20new%20UnauthorizedException)). This is a good practice – if you ever need to invalidate a user session (e.g., user reported stolen account), you can revoke in Firebase and that token becomes unusable. Also handle the errors from verification correctly (we throw Unauthorized).
- **Limit Token Usage to Authorization Header**: Our design keeps the JWT in memory and sends it in a header, which is fine. If you were to store it in a cookie, mark it HttpOnly and Secure. If in localStorage, be mindful of XSS. Basically, protect the token from leaks. Also, never include the Firebase refresh token in any responses or expose it – Firebase SDK handles refresh tokens internally.
- **Short Session Duration**: Rely on Firebase’s 1-hour token expiry and automatic refresh. This limits the window if a token is stolen. If using session cookies, choose an appropriate expiration (maybe a day or week, not indefinite) and require re-login after expiry for safety ([How to refresh session cookie in nestjs - Stack Overflow](https://stackoverflow.com/questions/72857952/how-to-refresh-session-cookie-in-nestjs#:~:text=How%20to%20refresh%20session%20cookie,age%22%20attributes)).
- **Multi-Factor for Sensitive Accounts**: Encourage or enforce MFA for administrative or highly sensitive accounts. This greatly reduces risk of account takeover. You can even integrate checks such as refusing certain operations if `auth_time` (last login time in token) is older than X or if a recent second factor auth wasn’t done – similar to how Google sometimes asks re-auth before major actions.
- **Role and Access Management**: Implement least privilege – e.g., an admin token should be verified both by its claim and possibly double-check in DB that the user is still an admin. If an admin’s role is revoked in the DB, either also remove the custom claim or at least ensure your `RolesGuard` checks the DB so they can’t use an old token to act as admin. Keep your role logic centralized and avoid scattering role checks in multiple places.
- **Preventing Abuse**: Since Firebase handles the heavy auth, things like password bruteforce protection, IP throttling on login, etc., are largely managed by Firebase/Google. However, your backend endpoints might need rate limiting (e.g., to prevent someone from using a valid token to spam requests). Implement rate limit middleware or use a proxy (NGINX, Cloudflare) for basic rate limiting if needed.
- **Audit Logging**: Consider logging authentication events. Firebase has logs for sign-in events in their console. On your backend, you might log when a user record is created or when critical admin routes are accessed, along with the `uid` for traceability. For compliance or debugging, these logs help.
- **Keep Libraries Updated**: Security issues are occasionally found in libraries (Firebase SDK, NestJS, JWT libs). Keep an eye on updates and apply patches. For example, Firebase Admin keys rotate regularly; using the Admin SDK (as we do) handles that automatically by fetching Google’s public keys and caching them. If we manually handled JWT verification, we’d have to manage key rotation – thankfully not needed here ([How to authenticate Firebase users against your NestJS Backend ‍](https://medium.com/@frederik.hafemann/how-to-authenticate-firebase-users-against-your-nestjs-backend-daf8698848cb#:~:text=%E2%80%8D%20medium,token%20is%20signed%20using)).
- **Disable Unused Auth Providers**: Only enable providers you use (we enabled Google and possibly email in our setup). Disable others to reduce attack surface (e.g., if you’re not using phone auth, leave it off to avoid any chance of abuse via those endpoints).
- **Content Security Policy (CSP)**: On the frontend, implement a strong CSP to mitigate XSS, which in turn protects your JS and tokens. Also consider using a service worker to handle auth token header injection in requests (Firebase has a feature with service workers to automatically attach ID tokens to outgoing requests to your domain, which can be convenient and secure ([Leveraging Service Workers for Efficient Session Management with ...](https://medium.com/@jabronidude/leveraging-service-workers-for-efficient-session-management-with-firebase-auth-61dc09331e42#:~:text=Leveraging%20Service%20Workers%20for%20Efficient,in%20the%20header%20without))). This ensures even if your fetch/axios call forgets to attach token, the service worker does it. It also isolates the token from the JavaScript context.

### 8.2 Performance Optimization Tips

- **Reuse Firebase Admin instance**: Initializing the Firebase Admin SDK is expensive (loading keys, etc.). We did it once in the strategy constructor. Ensure you don’t call `admin.initializeApp` for every request. The `admin` object can be shared. If you have multiple modules needing it, set it up in a global module. The Admin SDK will cache Google's public signing keys and reuse them for token verification, making subsequent verifications fast (usually a few milliseconds).
- **Connection Pooling**: For Postgres access, use connection pooling (most ORMs do this by default). This avoids the overhead of connecting to the DB on every request. Too many connections can also hurt performance, so size your pool appropriately (common default is 10).
- **Cache User Data (if necessary)**: If your token contains all needed info (like name, email, role via custom claims), you might not need to hit the database for each request. In that case, you can avoid an extra DB query in your guard by relying on token content. However, if you need DB data (perhaps more up-to-date or extensive than token), consider caching frequently accessed user info in memory or a fast store like Redis. For example, you could cache the user record by UID for a few minutes to avoid hitting DB repeatedly in that timeframe. Be cautious with cache coherence (invalidate if something changes). This is an optional optimization – many apps won’t need it if the DB is properly indexed and the load isn’t extreme.
- **Efficient Data Loading**: If on a given request you need both the token verification and some DB data, do them in parallel if possible. In Nest, since our guard runs before controllers, typically you'd finish verification then in the controller use the DB. But you could also design a custom `AuthService` that returns combined info. Simpler is fine until a performance issue is observed.
- **Batch and Minimize External Calls**: The only external call in our flow is the Firebase token verification. As mentioned, this hits Google’s certs the first time, then it’s local (validation of JWT signature). So it’s quite fast. If you were calling other APIs in the auth pipeline, try to minimize those.
- **Load Testing**: Use a tool like JMeter or k6 to simulate many logins or API calls to see where the bottleneck is. For instance, if 1000 users log in simultaneously, Firebase can handle it, but can your server handle 1000 nearly concurrent verifyIdToken calls and DB inserts? Possibly yes, but testing will confirm. You might find you need to increase your Node server resources or DB CPU. Also, enable HTTP keep-alive so that repeated requests (which is common in an SPA calling APIs frequently) aren’t creating new TCP connections each time. Most frameworks including Nest enable keep-alive by default nowadays.

- **CDN for Static Content**: Ensure your static files (React bundle) is served via CDN (Netlify and Vercel do this by default). This doesn’t directly affect auth but provides a faster first load which indirectly makes the whole experience snappier.

- **Compress Responses**: Enable GZIP or Brotli compression on API responses if sending larger data. For auth responses, typically it’s small (JSON with some data), but if you have larger payloads behind auth, compress them to save bandwidth and time.

### 8.3 Maintenance and Monitoring

- **Monitor Authentication Metrics**: Firebase provides metrics like how many sign-ins, how many new users, etc. Use these to detect anomalies (e.g., a spike in sign-ins could indicate a potential abuse or just a popular day).
- **Logs**: Keep an eye on your backend logs for auth errors. For example, if you see a lot of “Firebase auth failed: Error: Firebase ID token has expired” it might indicate users with long sessions who didn’t refresh – maybe they have an issue or your refresh handling is broken. If you see “Firebase auth failed: invalid signature” constantly, could be someone trying to spoof tokens.
- **Regular Security Review**: As your application grows, review who has access to Firebase project, rotate service account keys if needed, and ensure old tokens are revoked (Firebase has a feature to revoke all user tokens by forcing password reset or via Admin SDK).
- **Update Dependencies**: We said it before but it’s worth repeating in maintenance – keep Firebase libraries updated. Firebase updates often include security patches or improvements (for example, reinforcing TLS pinning or token verification enhancements). Similarly, update NestJS and Passport packages to get latest fixes.

By adhering to these best practices, you can achieve a secure, high-performance authentication system. Our stack uses Firebase and Google Auth to avoid reinventing the wheel for login, while NestJS and PostgreSQL give us full control over backend logic and data. This hybrid approach (Firebase for identity, custom backend for data) is powerful and scalable when done right.

## Conclusion

In this guide, we walked through building a complete Google login authentication system with **React (TypeScript)**, **NestJS**, and **PostgreSQL**, leveraging **Firebase Authentication** for OAuth and identity management. We started from setting up Firebase and Google sign-in ([Firebase Google authentication with React - DEV Community](https://dev.to/mdamirgauhar/firebase-google-authentication-with-react-gop#:~:text=Now%20to%20enable%20the%20authentication%2C,and%20enable%20the%20Google%20authentication)), implemented the front-end login flow with the Firebase SDK, and secured our back-end by verifying Firebase JWTs in NestJS ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=const%20firebaseUser%3A%20any%20%3D%20await,throw%20new%20UnauthorizedException)). We integrated Postgres to persist user data and support features like roles and multi-factor auth. Along the way, we discussed advanced considerations like session management (using Firebase’s built-in capabilities or cookies) and role-based access control using custom claims or database checks. Deployment strategies were covered for both frontend and backend, including environment configuration and using cloud platforms like Vercel, Heroku, and AWS. We also outlined testing methodologies from unit tests to end-to-end tests to ensure the system works reliably under various scenarios. Finally, we summarized best practices for security (protecting tokens, enforcing MFA, using least privilege) and performance (caching, pooling, monitoring) to keep the authentication system robust, secure, and efficient.

By following this step-by-step guide, experienced developers should be able to implement a production-ready authentication system that provides a smooth login experience with Google, while maintaining high security standards and scalability. The combination of Firebase and NestJS gives us the best of both worlds: ease-of-use in auth and full flexibility in our application’s backend logic ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=We%E2%80%99ll%20create%20a%20simple%20application,the%20validity%20of%20the%20JWT)) ([Using Firebase Authentication in NestJS apps - LogRocket Blog](https://blog.logrocket.com/using-firebase-authentication-in-nestjs-apps/#:~:text=What%E2%80%99s%20happening%20here%3F%20The%20JWT,an%20unauthorized%20exception%20is%20thrown)). Happy coding, and secure authenticating!
