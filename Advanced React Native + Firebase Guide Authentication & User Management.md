**# Advanced React Native + Firebase Guide: Authentication & User Management**

This guide provides a comprehensive, step-by-step walkthrough (200+ pages worth of material) for experienced React Native developers building an app with Firebase Authentication and robust user management. We’ll cover everything from initial setup to advanced features, with sample code and best practices. Each section is structured with clear steps, short paragraphs, and examples for easy scanning.

## 1. Project Setup

Before diving into coding authentication, we need to set up our React Native project with Firebase. This includes installing required packages, configuring Firebase for both Android and iOS, and handling sensitive config via environment variables.

### 1.1 Installing Dependencies

Begin by creating or using an existing React Native project (using React Native CLI for full native module access). Then install the Firebase SDK for React Native (we'll use **React Native Firebase** by Invertase, a widely used integration):

- Install the core Firebase app module and Auth module:

  ```bash
  npm install @react-native-firebase/app @react-native-firebase/auth
  # (or yarn add @react-native-firebase/app @react-native-firebase/auth)
  ```

  The `@react-native-firebase/app` package must be installed first as it initializes the Firebase native SDK ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=)). After that, installing `@react-native-firebase/auth` provides the authentication functionalities.

- If you plan to use Analytics, Crashlytics, etc., install those modules too (e.g. `@react-native-firebase/analytics`, `@react-native-firebase/crashlytics`). We will include these later as needed.

- Install provider-specific SDKs for social login:

  - Google Sign-In: `npm install @react-native-google-signin/google-signin` (for Google OAuth).
  - Facebook SDK: `npm install react-native-fbsdk-next` (for Facebook Login).
  - Apple Auth: `npm install @invertase/react-native-apple-authentication` (for Apple Sign-In).

  These libraries will be used in the Authentication section for social logins.

- After installing, link native modules (React Native 0.60+ does autolinking). For iOS, run `cd ios && pod install && cd ..` to install CocoaPods dependencies.

**Note:** If using **Expo**, you cannot directly use the native SDKs unless you eject or use the bare/managed workflow with config plugins. In a bare Expo or plain RN project, the above libraries work. In a pure managed Expo app, you’d rely on Expo’s Google/Facebook auth modules or EAS build with config plugins for the RN Firebase modules.

### 1.2 Configuring Firebase (Android & iOS)

Next, integrate your app with a Firebase project:

- **Create a Firebase project** in the Firebase console and add Android and iOS apps to it. This will generate platform-specific config files.

- **Android configuration:**

  1. Download the `google-services.json` file from Firebase console (Project Settings > Your Apps > Android) and place it under your RN project at `android/app/google-services.json` ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=certificate%20fingerprints%27%20on%20your%20app,in%20Firebase%20console)).
  2. Add the Google services Gradle plugin in your Android build config. Edit **`android/build.gradle`** and inside the `buildscript { dependencies { ... } }` block, add the classpath for Google Services if not present. For example:
     ```gradle
     buildscript {
         dependencies {
             // ... other classpaths
             classpath 'com.google.gms:google-services:4.4.2'  // Google Services plugin ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=buildscript%20,%2F%5C))
         }
     }
     ```
     _(Note: Use version compatible with your Gradle version. RN Firebase docs mention if RN ≤0.71, keep plugin ≤4.3.15 ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=dependencies%20,%2F%5C)).)_
  3. In **`android/app/build.gradle`**, apply the Google services plugin at the bottom of the file:
     ```gradle
     apply plugin: 'com.android.application'
     apply plugin: 'com.google.gms.google-services'  // Add this line ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=Lastly%2C%20execute%20the%20plugin%20by,file))
     ```
  4. Ensure your Android app’s package name matches what you registered in Firebase. If you need Google sign-in or phone auth, add the SHA-1 fingerprint in the Firebase console (you can generate SHA-1 by running `./gradlew signingReport` in the `android` directory) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=,your%20app%20in%20Firebase%20console)).

- **iOS configuration:**

  1. Download the `GoogleService-Info.plist` file from Firebase (Project Settings > Your Apps > iOS) and add it to your Xcode project. Place the file in the `ios/YourProject/` directory, then in Xcode right-click your project > “Add Files to [YourProject]…”, select the plist, and **check "Copy items if needed"** ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=,Xcode)). This ensures the config is bundled.
  2. Open your iOS App Delegate (usually `ios/YourProject/AppDelegate.m` or `.mm`). Import Firebase and configure it during app launch:

     ```objc
     #import <Firebase.h>  // add import

     - (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
         [FIRApp configure];  // initialize Firebase ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=Within%20your%20existing%20,the%20top%20of%20the%20method))
         // ... any other setup ...
         return YES;
     }
     ```

     This connects your iOS app to Firebase using the plist credentials.

  3. **Update CocoaPods for Firebase frameworks:** Recent Firebase iOS SDKs require using frameworks. In your **Podfile**, enable static frameworks:
     ```ruby
     use_frameworks! :linkage => :static
     $RNFirebaseAsStaticFramework = true  # RNFirebase specific flag ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=CocoaPods%20to%20use%20frameworks)) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=,%24RNFirebaseAsStaticFramework%20%3D%20true))
     ```
     Also, if your Podfile has Flipper enabled, disable it because Flipper + use_frameworks can conflict ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=%3E%20Notes%3A%20React,If)).
  4. Run `pod install` again after these changes. Then build the iOS app (`npx react-native run-ios`) to verify Firebase initializes without error.

- **Verify installation:** Rebuild the app on each platform. If configured properly, the native Firebase SDK will initialize using the included config files. You can test by calling a simple Firebase API (like `firebase.auth().currentUser`) or checking logs. On iOS, ensure the console shows no errors about missing plist, and on Android verify no errors about `google-services.json`. Once the core app module is working, you can proceed to use other Firebase services. At this point, the app module is ready, but no auth functions are called yet.

### 1.3 Setting up Environment Variables Securely

Managing API keys and config in a secure way is crucial. Hardcoding secrets (API keys, IDs) in the repository is a **bad practice** ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=One%20approach%20is%20to%20hardcode,this%20method%20has%20significant%20drawbacks)). For Firebase, the config files (plist/json) themselves are usually safe to include (they do not contain super-sensitive secrets, just project IDs and API keys). However, other sensitive values like API secret keys, or any config you wouldn't want exposed, should be handled via environment variables or secure storage:

- **Use a .env file and library:** Add a package like **react-native-config** or **react-native-dotenv** to load environment variables at build time. For example, `react-native-config` allows defining variables in a `.env` file and accessing them in native code and JS. This way, you can have separate `.env.development` and `.env.production` files and avoid bundling all configs in the app ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=environment%20variables%20to%20inject%20your,included%20in%20your%20final%20artifact)). Only the variables for the target environment will be included in the build artifact, reducing exposure of other environment’s secrets.

- **Do not commit secrets:** Make sure to **.gitignore** your `.env` files. A core rule is _never store plain text secrets in source control_ ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=One%20approach%20is%20to%20hardcode,this%20method%20has%20significant%20drawbacks)). If someone gains access to your repo, they shouldn’t find API passwords or private keys. Keep those in environment configs that are injected during CI/CD or development.

- **Example:** Create a `.env`:

  ```env
  API_URL=https://myapi.example.com
  GOOGLE_WEB_CLIENT_ID=abcd-1234.apps.googleusercontent.com
  ```

  Then use a library to access these in JS (e.g. `Config.API_URL`). Also, for iOS/Android native code (if needed, e.g. Google Maps API keys in manifest), react-native-config can automate injecting them.

- **Secure distribution:** In CI pipelines (discussed later), provide env vars through the CI secret store. For example, in GitHub Actions, add them as repository secrets and load into the build jobs. This ensures only authorized builds get the values.

By using environment variables, you ensure that each build (development, staging, production) can have its own Firebase config or API endpoints without bundling all configurations into the app. This technique reduces the risk of exposing non-production backends or keys to end-users ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=In%20a%20React%20Native%20app%2C,can%20dynamically%20import%20at%20runtime)) ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=environment%20variables%20to%20inject%20your,included%20in%20your%20final%20artifact)).

With the project properly set up and configured, we can move on to implementing authentication features.

## 2. Authentication

In this section, we implement various authentication mechanisms: basic email/password auth, OAuth logins (Google, Facebook, Apple), multi-factor auth, and even device biometrics. We assume you have enabled the relevant sign-in providers in Firebase console (Authentication > Sign-in method). Each method will include code samples and tips.

### 2.1 Email/Password Authentication

**Firebase Email/Password** sign-in is the fundamental auth method. It allows users to create an account with an email address and password and log in with those credentials.

**Enabling Email/Password:** In Firebase console, enable this provider under Authentication > Sign-in Method. No other setup is required.

**Implementing sign-up (registration):**
Use Firebase Auth’s `createUserWithEmailAndPassword(email, password)` method to register a new user account ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)) ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=Creates%20a%20new%20user%20with,an%20email%20and%20password)). For example:

```js
import auth from "@react-native-firebase/auth";

async function register(email, password) {
  try {
    const userCredential = await auth().createUserWithEmailAndPassword(
      email,
      password
    );
    // User registered successfully
    const user = userCredential.user;
    console.log("Registered new user:", user.uid);
    // (Optional) send email verification
    await user.sendEmailVerification();
  } catch (error) {
    if (error.code === "auth/email-already-in-use") {
      // Handle duplicate email
      console.warn("That email address is already in use!");
    } else if (error.code === "auth/invalid-email") {
      console.warn("That email address is invalid!");
    } else {
      console.error("Registration error:", error);
    }
  }
}
```

When called, this will create the user in Firebase Authentication and sign them in at the same time (the returned `user` will be logged in). It’s good practice to handle common errors (like email already in use, weak password, invalid email format).

**Implementing login:**
Use `signInWithEmailAndPassword(email, password)` to authenticate an existing user ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)):

```js
async function login(email, password) {
  try {
    const userCredential = await auth().signInWithEmailAndPassword(
      email,
      password
    );
    console.log("User logged in:", userCredential.user.email);
  } catch (error) {
    if (error.code === "auth/wrong-password") {
      alert("Incorrect password");
    } else if (error.code === "auth/user-not-found") {
      alert("No account found for this email");
    } else {
      console.error("Login error", error);
    }
  }
}
```

If successful, `auth().currentUser` will now be set to the logged-in user, and any auth state listeners will fire (more on that in State Management). On failure, Firebase throws an error with a specific code we can check (as shown above).

**Security tip:** Passwords are never stored or transmitted in plain text to your server. The Firebase SDK handles hashing and verification with Google’s back-end. Nonetheless, you should use HTTPS (which Firebase uses by default) and possibly enforce strong passwords (Firebase can enforce this via error on weak passwords by default).

**Email verification:** For added security, you might require users to verify their email. Firebase can send verification emails using `user.sendEmailVerification()`. We’ll cover the flow for email verification in **User Management** (section 3.3), but note you might call `sendEmailVerification` after registration and prompt the user to check their inbox.

At this point, you have basic email sign-up and sign-in working. Next, we broaden access with social logins.

### 2.2 Social Authentication (Google, Facebook, Apple Sign-In)

Offering social logins improves UX by allowing users to use existing accounts. Firebase Auth seamlessly supports OAuth providers like Google, Facebook, Apple, Twitter, etc. We’ll implement the three mentioned: Google, Facebook, and Apple.

**General flow:** For OAuth providers in React Native, the typical pattern is:

1. Use the provider’s SDK or OAuth flow to get an **ID token** or **auth token** for the user.
2. Pass that token to Firebase to sign in or link with Firebase credentials.

Firebase provides methods like `auth().signInWithCredential(providerCredential)` where `providerCredential` is built from the token you got. Each provider has a static method to create that credential (e.g. `GoogleAuthProvider.credential(idToken)`).

#### 2.2.1 Google Sign-In

**Setup:** In Firebase console, enable the Google provider in Auth > Sign-in method. On Android, ensure you have added your app’s SHA-1 fingerprint to Firebase settings; it’s required for Google sign-in to work on release builds ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=For%20bare%20React,on%20the%20Getting%20Started%20documentation)). Also, obtain the **Web Client ID** from the Firebase config (Firebase > Project Settings > General > Web SDK configuration). The Web Client ID is used on Android/iOS to authorize the OAuth token.

**Configuration:** Using the `@react-native-google-signin/google-signin` library:

- Initialize the Google Signin with the client ID. Do this once (e.g. at app startup):

  ```js
  import { GoogleSignin } from "@react-native-google-signin/google-signin";

  GoogleSignin.configure({
    webClientId: "YOUR_WEB_CLIENT_ID.apps.googleusercontent.com",
  });
  ```

  The `webClientId` is crucial (it should match the one in `google-services.json` under OAuth client type 3 – “Web client” ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=Before%20triggering%20a%20sign,client_type%3A%203))). If using iOS, also add the reversed client ID in your URL Types in Info.plist (the GoogleSignin library’s docs cover this).

**Google Login Flow:**

```js
import auth from "@react-native-firebase/auth";
import { GoogleSignin } from "@react-native-google-signin/google-signin";

async function onGoogleButtonPress() {
  // 1. Prompt Google Sign-In dialog
  await GoogleSignin.hasPlayServices({ showPlayServicesUpdateDialog: true });
  const userInfo = await GoogleSignin.signIn();

  // 2. Extract the ID token
  let idToken = userInfo.idToken;
  if (!idToken && userInfo.idToken === undefined && userInfo.user) {
    // some versions return token differently; adjust if needed
    idToken = userInfo.user.idToken;
  }
  if (!idToken) throw new Error("Google signin failed: No ID token");

  // 3. Create a Google credential with the token
  const googleCredential = auth.GoogleAuthProvider.credential(idToken);
  // 4. Sign-in with credential into Firebase
  return auth().signInWithCredential(googleCredential);
}
```

We call `GoogleSignin.signIn()` to handle the Google OAuth UI. This returns an object with the user’s Google info and tokens (the library handles the native Google Sign-In on Android and iOS). We then build a Firebase credential: `auth.GoogleAuthProvider.credential(idToken)` and use it to sign in to Firebase ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Google%20credential,idToken)). If successful, the user is authenticated with Firebase using their Google account.

After `await onGoogleButtonPress()`, you can proceed knowing `auth().currentUser` is set. For example:

```js
<Button
  title="Login with Google"
  onPress={() =>
    onGoogleButtonPress().then(() => console.log("Signed in with Google!"))
  }
/>
```

This pattern is exactly as shown in the RNFirebase docs ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=async%20function%20onGoogleButtonPress%28%29%20,signIn)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Google%20credential,idToken)). On Android emulators, ensure you use one with Google Play services. If you get an error like `DEVELOPER_ERROR`, double-check the SHA-1 and webClientId configuration; commonly this error means an OAuth config mismatch (wrong client ID or missing SHA fingerprint) ([Firebase Google Sign-in Problem on Android APK | by Kuray Ogun](https://freakycoder.com/react-native-notes-29-firebase-google-sign-in-problem-on-android-apk-4597e7e60973#:~:text=Firebase%20Google%20Sign,This%20is%20a)).

#### 2.2.2 Facebook Login

**Setup:** Enable Facebook provider in Firebase Auth methods. You’ll need a Facebook app ID. Follow React Native FBSDK setup (for `react-native-fbsdk-next`):

- Add your Facebook app ID and name in the iOS Info.plist and Android string resources as per FBSDK docs.
- On iOS, configure URL Types with `fb<APP_ID>` scheme; on Android, add a `<meta-data>` in AndroidManifest with the FB App ID.

Once set up, using the Facebook SDK to login and then Firebase:

```js
import { LoginManager, AccessToken } from "react-native-fbsdk-next";
import auth from "@react-native-firebase/auth";

async function onFacebookButtonPress() {
  // 1. Attempt Facebook login
  const result = await LoginManager.logInWithPermissions([
    "public_profile",
    "email",
  ]);
  if (result.isCancelled) {
    throw "User cancelled the Facebook login process";
  }

  // 2. Get the Facebook access token
  const data = await AccessToken.getCurrentAccessToken();
  if (!data) {
    throw "Something went wrong obtaining Facebook access token";
  }

  // 3. Create a Firebase credential with the token
  const facebookCredential = auth.FacebookAuthProvider.credential(
    data.accessToken
  );
  // 4. Sign-in to Firebase with that credential
  return auth().signInWithCredential(facebookCredential);
}
```

This uses Facebook’s LoginManager to show the login dialog. If the user consents, we retrieve an `AccessToken` from Facebook ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=async%20function%20onFacebookButtonPress%28%29%20,public_profile%27%2C%20%27email)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Once%20signed%20in%2C%20get,getCurrentAccessToken)). Then we pass that to Firebase: `FacebookAuthProvider.credential(token)` and sign in ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Firebase%20credential,accessToken)). After this, Firebase will treat the user as authenticated via Facebook.

You can call `onFacebookButtonPress()` on a button press similar to Google. If successful, the user is logged in (you can check `auth().currentUser.providerData` to see that it’s a Facebook account, etc.). On iOS, if you configured “Limited Login” (with limited data), the process is slightly different (requires an authenticationToken and nonce) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=,only)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Once%20signed%20in%2C%20get,getAuthenticationTokenIOS)), but the above covers the standard scenario.

#### 2.2.3 Apple Sign-In

**Setup:** Apple Sign In requires an Apple Developer account. You must:

- Enable “Sign in with Apple” capability in your Xcode project.
- In the Apple Developer portal, create a Services ID and an associated private key (used by Firebase to verify). In Firebase console > Auth > Sign-in method, enable Apple and provide the Services ID and key ID/team ID from Apple.

Using `@invertase/react-native-apple-authentication` (which wraps Apple’s auth):

```js
import { appleAuth } from "@invertase/react-native-apple-authentication";
import auth from "@react-native-firebase/auth";

async function onAppleButtonPress() {
  // 1. Start Apple Authentication
  const appleAuthRequestResponse = await appleAuth.performRequest({
    requestedOperation: appleAuth.Operation.LOGIN,
    requestedScopes: [appleAuth.Scope.FULL_NAME, appleAuth.Scope.EMAIL],
  });

  // 2. Ensure Apple returned a token
  const { identityToken, nonce } = appleAuthRequestResponse;
  if (!identityToken) {
    throw "Apple Sign-In failed - no identity token returned";
  }

  // 3. Create a Firebase Apple credential
  const appleCredential = auth.AppleAuthProvider.credential(
    identityToken,
    nonce
  );
  // 4. Sign in with Firebase
  return auth().signInWithCredential(appleCredential);
}
```

Here we call `appleAuth.performRequest` to prompt the system Apple Sign-In dialog ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=async%20function%20onAppleButtonPress%28%29%20,authentication%23faqs%20requestedScopes%3A%20%5BappleAuth.Scope.FULL_NAME%2C%20appleAuth.Scope.EMAIL)). The response contains an `identityToken` (JWT) and a `nonce` that our app provided. We then build an Apple Auth credential for Firebase with `auth().AppleAuthProvider.credential(token, nonce)` and use it to sign in ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Firebase%20credential,credential%28identityToken%2C%20nonce)). After this, the user is logged in to Firebase with their Apple ID.

**Important:** Apple requires that if you use Apple Sign-In, you must provide a way for users to revoke it and delete their account. Specifically, if a user deletes their Firebase account, you should revoke their Apple credentials. Firebase Auth provides `auth().revokeToken()` for this purpose (available for Apple provider) which you can call with the Apple OAuth authorization code if available ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=Apple%20also%20requires%20that%20the,API)) ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)). In practice, you would call Apple’s `getCredentialState` or keep the `authorizationCode` from the Apple sign-in response and call `auth().revokeToken(authorizationCode)` when deleting the user – this will revoke the Apple refresh token on Apple’s side, per Apple’s requirements.

All three social methods (Google, FB, Apple) ultimately result in a Firebase user. You can check `auth().currentUser.email` or `.displayName` etc. Often, you might want to link accounts (e.g., a user signed up with email and later wants to link Google). Firebase supports linking credentials via `currentUser.linkWithCredential(...)`, but that’s beyond our primary scope.

Now that we have multiple ways for users to authenticate, let’s add an extra layer of security with multi-factor auth.

### 2.3 Multi-Factor Authentication (MFA)

Multi-factor auth means the user must provide a second factor (like a phone OTP or authenticator code) in addition to their password. Firebase Authentication supports MFA (currently SMS as second factor) for Email/Password and federated accounts. Implementing MFA in a React Native app involves enrollment and sign-in flows:

**Enable MFA in Firebase:** You must enable Phone as a second factor in Firebase Authentication settings (in Firebase console under Authentication > Sign-in method, enable **SMS Multi-factor Authentication**) ([Add multi-factor authentication to your web app - Firebase - Google](https://firebase.google.com/docs/auth/web/multi-factor#:~:text=Google%20firebase,You%20should%20also%20enter)). This feature may require upgrading to Firebase’s Identity Platform (if prompted).

**2.3.1 Enrolling a second factor (Phone):**

1. **Prerequisite:** The user should be logged in with a primary factor and have a verified email ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=,See%20User%20interface%20is%20returned)) (Firebase requires email verification before adding MFA for email/password users).
2. **Get MultiFactor user:** Firebase provides a `multiFactor` property on the User. In RNFirebase, use `auth().multiFactor(user)` to get a `MultiFactorUser` instance ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=Begin%20by%20obtaining%20a%20MultiFactorUser,factor%20operations)).
3. **Initiate verification:** Call `multiFactorUser.getSession()` to get a session for enrollment ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=Request%20the%20session%20identifier%20and,to%20send%20a%20verification%20code)), then call `auth().verifyPhoneNumberForMultiFactor({ phoneNumber, session })` ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20session%20%3D%20await%20multiFactorUser,phoneNumber%2C%20session%2C)). This will send an SMS code to the provided phone number.
4. **Complete enrollment:** Ask the user to enter the SMS code. Then create a PhoneAuthCredential:
   ```js
   const cred = auth.PhoneAuthProvider.credential(verificationId, smsCode);
   const multiFactorAssertion = auth.PhoneMultiFactorGenerator.assertion(cred);
   await multiFactorUser.enroll(multiFactorAssertion, "My Phone"); // 'My Phone' is an optional display name for this factor ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20cred%20%3D%20auth,display%20name%20for%20the%20user)).
   console.log("MFA enrollment successful");
   ```
   This ties the phone number as a second factor to the user’s account. You can provide an optional name for the factor (useful if a user has multiple factors).

After enrolling, `user.multiFactor.enrolledFactors` would list the factors (like phone with UID and display name).

**2.3.2 Multi-factor Sign-In flow:**
When a user with MFA enabled tries to sign in (e.g., via `signInWithEmailAndPassword`), Firebase will throw a special error `auth/multi-factor-auth-required` after the first factor is validated ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=auth%28%29%20.signInWithEmailAndPassword%28email%2C%20password%29%20.then%28%28%29%20%3D,required%27%29)). The signIn call won’t automatically complete; we must handle the second factor:

1. Catch the `auth/multi-factor-auth-required` error:
   ```js
   let userCredential;
   try {
     userCredential = await auth().signInWithEmailAndPassword(email, password);
   } catch (err) {
     if (err.code === 'auth/multi-factor-auth-required') {
       const resolver = auth().getMultiFactorResolver(err);  // get resolver to continue MFA ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=Using%20the%20error%20object%20you,instance%20and%20continue%20the%20flow))
       // resolver.hints contains available second factors (e.g., phone numbers).
       const hint = resolver.hints[0];  // assume one phone factor
       // 2. Send OTP to that phone
       const mfaVerificationId = await auth().verifyPhoneNumberWithMultiFactorInfo(hint, resolver.session) ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=auth%28%29%20,setVerificationId%28verificationId));
       // Now prompt user for the SMS code:
       const code = await promptUserForCodeSomehow();  // implement UI for this
       // 3. Create assertion and complete sign-in
       const cred = auth.PhoneAuthProvider.credential(mfaVerificationId, code);
       const mfaAssertion = auth.PhoneMultiFactorGenerator.assertion(cred);
       userCredential = await resolver.resolveSignIn(mfaAssertion);  // completes the MFA sign-in ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20credential%20%3D%20auth))
     } else {
       throw err; // some other error (wrong password, etc.)
     }
   }
   ```
   We use `getMultiFactorResolver(error)` to obtain a `MultiFactorResolver` ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=Using%20the%20error%20object%20you,instance%20and%20continue%20the%20flow)). This resolver holds the `session` and the list of enrolled factors (hints).
2. **Selecting factor (if multiple):** If `resolver.hints` has more than one factor, you should prompt the user to choose (e.g., if they have 2 phone numbers). In our case, we assume one phone, so we directly use `hints[0]` ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=if%20%28resolver.hints.length%20,factors%20to%20the%20user)).
3. **Sending code:** We call `verifyPhoneNumberWithMultiFactorInfo(hint, session)` which sends the SMS ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=auth%28%29%20,setVerificationId%28verificationId)). It returns a `verificationId` similar to normal phone auth.
4. **Verify code:** Take the user’s input code, build a credential and then call `resolver.resolveSignIn(mfaAssertion)` ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20credential%20%3D%20auth)) to complete the sign-in. This returns a `UserCredential` like a normal login, and the user is now signed in.

From here on, the user is fully authenticated with two factors. Every subsequent sign-in will require the second factor again (unless you implement “remember this device” by using custom claims or other means, which is a more advanced concept).

**Tip:** The MFA flow can be complex in UI/UX, so ensure to guide the user (e.g., show “sending code to +123\*\*\*\*45”, then a screen to enter code). Also, handle errors like wrong code (`auth/invalid-verification-code`) or timeout.

Multi-factor auth significantly increases account security by preventing access with just a stolen password. Next, we will look at adding biometric auth for an even smoother login experience.

### 2.4 Biometric Authentication (Face ID / Fingerprint)

Biometric authentication (Face ID, Touch ID on iOS, or fingerprint/biometric unlock on Android) can be used to streamline the login process or secure the app. **Important:** Firebase itself does not natively support biometrics as an auth factor ([flutter - Can The App Include Biometric Login With Firebase? - Stack Overflow](https://stackoverflow.com/questions/64058218/can-the-app-include-biometric-login-with-firebase#:~:text=Firebase%20Authentication%20does%20not%20directly,not%20deal%20directly%20with%20those)). Instead, biometrics are used on the device to either _unlock stored credentials_ or _as an additional local check_ before letting the user access the app.

There are two primary use-cases for biometrics in our context:

**(a) Biometric unlock for stored credentials (password managers style):**  
We can store the user's email and password (or a Firebase custom token) securely in the device’s keystore after they log in the first time. On subsequent launches, use FaceID/TouchID to decrypt/retrieve those credentials and log in the user automatically, without them typing a password. This provides convenience without sacrificing much security (since the creds are protected by biometrics).

Steps to implement:

1. **After a normal login**, ask the user if they want to enable “Biometric Login” (optional but recommended UX). If yes, save their credentials securely:
   - Use a library like `react-native-keychain` or `expo-secure-store` to save the email/password or Firebase refresh token. For example, `react-native-keychain` can store credentials in Keychain/Keystore with device biometric protection (you can tag the item such that retrieval requires biometric auth).
   - **Never store plaintext password in AsyncStorage** or anywhere not secure. Use device secure storage APIs.
2. **On app launch**, check if credentials are saved. If yes, prompt the biometric authentication:
   - Using `react-native-keychain`: call `Keychain.getGenericPassword()` with options to require authentication. This will trigger Face ID/Touch ID or Android biometric prompt.
   - If the user passes biometrics, you get the decrypted credentials.
3. **Use credentials to authenticate:** With the email/password retrieved (for example), call `auth().signInWithEmailAndPassword(email, password)` programmatically. The user is logged in without manually entering anything, gated by biometrics.
   - Alternatively, you could store a Firebase custom auth token and use `signInWithCustomToken` to avoid storing the actual password. But that token might expire after 1 hour just like ID tokens, so storing password might be more reliable for long-term until user changes it.

This approach was suggested in a similar context for Flutter: storing email & password in secure storage on first login, then using `local_auth` to biometrically confirm and logging in with stored creds ([flutter - Can The App Include Biometric Login With Firebase? - Stack Overflow](https://stackoverflow.com/questions/64058218/can-the-app-include-biometric-login-with-firebase#:~:text=Assuming%20you%20are%20using%20Firebase,with%20email%20and%20password%20method)). The same concept applies in React Native.

**(b) Biometric lock for app (protecting logged-in session):**  
In this scenario, the user stays logged into Firebase (we don’t log them out), but we require biometric auth each time the app is opened (or after a period of inactivity) to access the app’s contents. This is more about app security than Firebase auth, but it’s worth mentioning:

- Implement this by using a state variable like `isAppLocked`. When the app launches or comes to foreground, if `isAppLocked` is true, show a screen or modal prompting for FaceID/TouchID (using e.g. `expo-local-authentication` or `react-native-biometrics` to simply prompt and verify identity).
- If the biometric check succeeds, set `isAppLocked = false` and allow access (render the main app screens).
- If it fails or the user cancels, keep the app locked or offer a fallback (perhaps a PIN or password if biometric fails).
- This method does not involve Firebase at all; it’s purely local. The Firebase session remains active in the background, but the UI is blocked by the biometric check.

This is useful if, for example, the user stays signed in but you want to ensure only they (not anyone who grabs their unlocked phone) can open the app.

**Firebase and biometrics:** Firebase has no direct API for biometrics, so either approach above is essentially “custom.” Approach (a) actually logs into Firebase, approach (b) just restricts UI. Many banking apps use approach (b) – user logs in once, stays logged in, but app is secured by biometric/PIN each time.

Be mindful of platform specifics:

- iOS Face ID will show a system dialog like “<AppName> wants to use Face ID” the first time. You need to have NSFaceIDUsageDescription in Info.plist.
- Android can use the newer BiometricPrompt. Libraries like `react-native-biometrics` or `react-native-fingerprint-scanner` wrap these.
- Always handle the case where biometric is not available or not enrolled (e.g., user hasn’t set up any fingerprint/face). Provide fallback (maybe use device PIN or prompt password).

In summary, **biometric auth** in RN + Firebase is achieved by secure credential storage and local device authentication ([Using biometric with firebase auth · invertase react-native-firebase · Discussion #4727 · GitHub](https://github.com/invertase/react-native-firebase/discussions/4727#:~:text=)) ([flutter - Can The App Include Biometric Login With Firebase? - Stack Overflow](https://stackoverflow.com/questions/64058218/can-the-app-include-biometric-login-with-firebase#:~:text=Assuming%20you%20are%20using%20Firebase,with%20email%20and%20password%20method)). It provides a fast login for returning users while keeping their credentials safe behind fingerprint or face recognition.

Now that we have a variety of authentication methods, let's look into managing users, roles, and sessions after they are logged in.

## 3. User Management

User management encompasses controlling what users can do (authorization), maintaining user profiles, and handling account changes like password resets or deletion. We will cover role-based access control (RBAC), session handling, profile updates/deletion, and secure flows for password reset and email verification.

### 3.1 Role-Based Access Control (RBAC)

RBAC is a strategy to restrict or allow access to parts of the app based on a user’s role (e.g., “admin”, “moderator”, “subscriber”, etc.). With Firebase, RBAC can be implemented using **Custom Claims** on Firebase Auth tokens or via security rules and Firestore data.

**Using Custom Claims:** Firebase Auth allows adding custom attributes (claims) to a user’s ID token via the Admin SDK. This is powerful for RBAC ([Control Access with Custom Claims and Security Rules - Firebase](https://firebase.google.com/docs/auth/admin/custom-claims#:~:text=Firebase%20firebase,implement%20various%20access%20control%20strategies)):

- You might have roles like `admin=true` as a custom claim on certain users. The Admin SDK (in a secure environment like Cloud Functions or server) can set this: `admin.auth().setCustomUserClaims(uid, { admin: true })`.
- These claims become part of the user’s ID token payload. You can then enforce access in Firebase Security Rules or in your app logic. For example, a Firestore rule could allow writes to an "admin" collection only if `request.auth.token.admin == true`.
- The official Firebase documentation states, _“The Firebase Admin SDK supports defining custom attributes on user accounts. This provides the ability to implement various access control strategies.”_ ([Control Access with Custom Claims and Security Rules - Firebase](https://firebase.google.com/docs/auth/admin/custom-claims#:~:text=Firebase%20firebase,implement%20various%20access%20control%20strategies)) and _“With custom user claims, you can give users different levels of access (roles)…”_ ([Introduction to the Admin Auth API - Identity Platform - Google Cloud](https://cloud.google.com/identity-platform/docs/concepts-admin-auth-api#:~:text=Cloud%20cloud,roles%29)). This means you can create roles like admin, editor, etc., and these are trusted because they’re set via the Admin SDK (users themselves cannot alter their token’s custom claims).

**Workflow to use custom claims:**

- When a user is promoted to a role (say you have an admin dashboard to toggle roles), call a Cloud Function or secure server that uses the Admin SDK to set the claim. e.g., `setCustomUserClaims(uid, {role: 'admin'})` or `{admin: true}`.
- On the client, after this change, you’ll want the user to have a refreshed token (the claim is added to new tokens, not existing ones). The user can re-log or you call `auth().currentUser.getIdToken(true)` to force refresh the token.
- Now `auth().currentUser.getIdTokenResult()` will include the custom claims. For example:

  ```js
  const tokenResult = await auth().currentUser.getIdTokenResult();
  console.log("User custom claims:", tokenResult.claims);
  ```

  You might see `{ admin: true }` in the claims.

- Use the claims in rules: In Firestore security rules, you could do:
  ```js
  allow write: if request.auth.token.admin == true;
  ```
  This ensures only admins (with that claim) can write. _(Make sure to also check `request.auth != null` to avoid undefined issues.)_

**Alternate approach – Firestore roles collection:** If you prefer not to use custom claims, you can keep a roles mapping in your database. For instance, a `/roles` or `/users` document that contains a field like `role: "admin"` or `isAdmin: true`. Then in rules, you could read that. However, reading user data in rules can be slower/complex, and it can be manipulated by client if not secured properly. Custom claims are safer for auth because they cannot be changed by the user and are faster in rules (available in the token directly) ([Control Access with Custom Claims and Security Rules - Firebase](https://firebase.google.com/docs/auth/admin/custom-claims#:~:text=Firebase%20firebase,implement%20various%20access%20control%20strategies)) ([Role-based authorization (RBAC) with Firebase Auth custom claims ...](https://medium.com/comsystoreply/role-based-authorization-rbac-with-firebase-auth-custom-claims-and-spring-security-6125c6fc7c4#:~:text=Role,RBAC%29%20with%20Spring%20Security)).

**Frontend usage of roles:** You can conditionally render UI based on role. E.g., if you fetched `tokenResult.claims.admin`, store that in state and show “Admin Panel” button only if true. Remember to update it when user re-logins or token refreshes.

In summary, define your role hierarchy, assign roles via custom claims using Admin SDK, and enforce with security rules and app logic. Firebase’s ability to attach custom attributes to user JWTs makes RBAC implementation straightforward and secure ([Control Access with Custom Claims and Security Rules - Firebase](https://firebase.google.com/docs/auth/admin/custom-claims#:~:text=Firebase%20firebase,implement%20various%20access%20control%20strategies)) ([Introduction to the Admin Auth API - Identity Platform - Google Cloud](https://cloud.google.com/identity-platform/docs/concepts-admin-auth-api#:~:text=Cloud%20cloud,roles%29)).

### 3.2 Handling User Sessions and Token Management

Managing user sessions in Firebase is mostly handled by the SDK, but understanding it helps to manage edge cases and security:

- **Token lifecycle:** When a user logs in, Firebase issues an **ID Token** (JWT) that is valid typically for 1 hour. The SDK will automatically refresh this token in the background using a **refresh token** so that the user’s session remains valid ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted)). This means you usually don’t have to manually handle token refresh – Firebase does it, ensuring `auth().currentUser` stays logged in across sessions, and `onIdTokenChanged` will fire when a new token is fetched.

- **Persistence:** By default, Firebase Auth on React Native (native SDK) persists the user session on the device (in secure storage). So closing and reopening the app will keep the user logged in (no need to re-enter credentials) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted)). We discuss persistence more in State Management section, but note that this is different from web where you can choose session vs local persistence. On RN, it’s effectively “local persistent” by default.

- **Session management:** If you need to force a user to re-authenticate (for sensitive actions or if you detect suspicious activity), you can use `reauthenticateWithCredential`. Firebase has a concept of **recent login**: certain operations (like changing email, or deleting account) require the user to have signed in recently (last 5 minutes by default). If not, those calls will throw `auth/requires-recent-login`. To handle that, prompt the user to re-enter password or redo social login:

  ```js
  const cred = auth.EmailAuthProvider.credential(user.email, password);
  await user.reauthenticateWithCredential(cred);
  // now retry the sensitive operation
  ```

  This ensures the user is indeed who they claim (important if someone left their app logged in and an attacker tries to change account email, for example).

- **Sign Out:** Calling `auth().signOut()` will clear the user session from the device. The user’s token is disposed and `currentUser` becomes null. Ensure your app’s state resets (navigate to login screen, etc.) on sign-out.

- **Token usage in APIs:** If you have your own backend server that needs to verify requests, you can send the Firebase ID token to that server (e.g., as an `Authorization: Bearer <token>` header). The server can then **verify the ID token** using Firebase Admin SDK or Firebase’s REST API to ensure the request is authenticated. This decouples auth from your backend logic and uses Firebase as the identity provider. It’s recommended to always verify on the backend if you rely on the identity for anything sensitive.

- **Custom sessions lengths:** By default, refresh tokens are long-lived and keep renewing ID tokens. If you want to force all users to re-log (for example, if you suspect a breach, or you revoked permissions), one approach is to **revoke refresh tokens** for a user from the Admin SDK (`auth().revokeRefreshTokens(uid)`). This will make existing tokens expire within an hour and the user will be kicked out (next token refresh will fail, making `currentUser` null). You might not need this often, but it’s good for emergency deauthorization of a user.

- **Multi-device sessions:** Firebase Auth doesn’t have a built-in session management UI for multiple devices. A user can log in on multiple devices and each will independently refresh tokens. If you need to implement “logout from other devices” or track active sessions, you’d have to manage that manually (e.g., store session records in Firestore and use security rules or cloud functions to invalidate tokens). That is beyond the default scope – by default, Firebase doesn’t limit concurrent sessions.

In summary, user session management with Firebase is mostly hands-off: the SDK persists and refreshes auth state automatically ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted)). As a developer, ensure to handle sign-outs, use reauthentication for sensitive actions, and optionally use token verification on your backend.

### 3.3 User Profile Management (Update, Delete, Profile Picture, etc.)

Managing a user’s profile involves updating properties like display name or photo, handling account deletion, and storing additional info.

**Firebase Auth User object:** Firebase Auth’s user has basic profile fields – `displayName`, `photoURL`, `email`, `phoneNumber`, etc. You can update some of these directly:

- `user.updateProfile({ displayName, photoURL })` – updates the user’s name and profile picture URL ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)).
- `user.updateEmail(newEmail)` – change email (will require recent login) ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)).
- `user.updatePassword(newPassword)` – change password (requires recent login) ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)).
- `user.updatePhoneNumber(cred)` – update phone number (cred obtained from phone auth verification) ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)).
- After certain updates like email change, the email may become unverified until re-verified. Firebase provides `user.sendEmailVerification()` to trigger verification emails ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=sendEmailVerification%28actionCodeSettings%3F%3A%20ActionCodeSettings%29%3A%20Promise)).
- If you want to update the email with verification (so the old email remains until confirmed), use `verifyBeforeUpdateEmail(newEmail)` which sends a verification link to the new email, and only updates the email in Firebase after the user clicks it ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)).

**Example – update display name:**

```js
if (auth().currentUser) {
  await auth().currentUser.updateProfile({ displayName: "John Doe" });
  console.log("Profile name updated!");
}
```

This will immediately update `auth().currentUser.displayName`. The change syncs to Firebase and any future token will contain the new displayName.

**Profile picture:** Firebase Auth’s `photoURL` is just a URL string. To let users upload profile images, you typically:

- Let user pick an image (using React Native Image Picker or similar).
- Upload the image to Firebase Storage (e.g., to a path like `/users/{uid}/profile.jpg`).
- Get the download URL of that image from Storage.
- Call `updateProfile({ photoURL: downloadUrl })` to save it in the Auth profile.

By doing this, `user.photoURL` will point to the image URL, and you can easily fetch it to display the avatar. Make sure your Storage security rules allow that read/write (we’ll cover security rules next).

**Deleting a user account:** Firebase provides `user.delete()` to delete the currently logged-in user ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)). As with email/password change, this operation requires recent login (otherwise you get `requires-recent-login`). After deletion, Firebase Auth no longer recognizes that user (their UID is freed up). You should also clean up any user data in your database at this point (Firebase will not automatically delete their Firestore/RTDB data or Storage files).

- _Example:_
  ```js
  try {
    await auth().currentUser.delete();
    // Signed-out locally as well
    console.log("User account deleted");
  } catch (error) {
    if (error.code === "auth/requires-recent-login") {
      // Re-auth then retry deletion
    }
  }
  ```
  If you have a Cloud Function listening for Auth user deletions, you can trigger cleanup there (see section 9.3).

**Email Verification flow:** Verifying a user’s email is often critical for certain apps. Here’s a secure flow:

- After sign-up, call `user.sendEmailVerification()`. This sends an email with a verification link.
- In Firebase console, you can customize the email template and set a **continue URL** (or specify one via `sendEmailVerification(actionCodeSettings)` which includes a URL that opens your app after verification).
- When the user clicks the link, Firebase marks the email as verified. If you set a continue URL to your app using a dynamic link, your app can catch that and confirm to user that their email is verified.
- You can enforce email verification by using Firebase Security Rules (e.g., only allow read/write if `request.auth.token.email_verified == true`) or in your app logic (only let verified users past a certain screen).

**Password Reset flow:** This is similar:

- Use `auth().sendPasswordResetEmail(email)` to send a reset link ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)). Firebase will email the user a link to reset their password.
- That link typically opens a web page where the user enters a new password. You can however configure it to redirect to your app (via custom URL scheme or Firebase Dynamic Links). If it redirects to the app, you can catch the oobCode (out-of-band code) and call `auth().confirmPasswordReset(code, newPassword)` to complete the reset in-app ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)). This is advanced; many apps simply use the default web flow for simplicity, which is fine.
- Ensure the email is entered is indeed a valid account – if not, Firebase still returns success (to prevent account enumeration). You might not want to disclose if an email is registered or not for security.

**Handling sensitive changes securely:** As mentioned, Firebase requires recent login for things like updateEmail, updatePassword, delete. Design your UI to possibly prompt re-authentication in these scenarios:

- e.g., “Please re-enter your password to confirm this action” then call `reauthenticateWithCredential` before calling `delete()` or others.

**User metadata:** Firebase tracks creation time and last sign-in time (`user.metadata`). This can be used for audit or display (e.g., “Member since Jan 2023”).

**Additional profile info:** Often the basic profile isn’t enough (you might want username, bio, etc.). The typical approach is to use a Firestore "Users" collection where each user has a document (keyed by their UID) containing extended profile info. You populate it at sign-up and read from it to display profiles. Make sure to secure this with rules (so users can only edit their own document, etc.). This is outside Auth per se, but common in user management.

**Apple Sign-In additional steps:** If using Apple, note that Apple provides the user’s name _only on first sign-in_. It’s recommended to capture it that first time (Firebase Auth will populate `displayName` on first sign-in with Apple if available). Also, as mentioned earlier, if a user deletes their account, you should revoke Apple credentials:

```js
const appleProviderData = auth().currentUser.providerData.find(
  (p) => p.providerId === "apple.com"
);
if (appleProviderData) {
  // You would need to have stored the Apple credential's authorizationCode at sign-in to use here
  await auth().revokeToken(appleAuthCode);
}
await auth().currentUser.delete();
```

`auth().revokeToken(authorizationCode)` revokes the Sign-in with Apple tokens ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)). Storing the `authorizationCode` securely at sign-in (perhaps in your DB, encrypted) is necessary because Apple doesn’t give it to you later. This is an Apple-specific requirement to keep in mind for user deletions.

To summarize, user profile management involves both Firebase Auth profile operations (simple fields) and potentially your own database for extra info. Leverage Firebase’s built-in functions for the common tasks (update email/password, etc.) and always handle the security (recent login) aspects properly.

### 3.4 Secure Password Reset and Email Verification Flows

We touched on these in profile management, but let’s compile best practices for password reset and email verification to ensure they are secure and user-friendly:

**Password Reset:**

- When `sendPasswordResetEmail` is called, Firebase sends a unique link to the user’s email. Ensure the email input is truly the user’s email (if user is logged in, you can pre-fill or use currentUser.email).
- The link contains an `oobCode` (one-time code) and usually directs to a Firebase hosted page where the user can set a new password. This link will expire after some time or once used.
- If you prefer a custom reset screen in your app:
  - Set up a Firebase Dynamic Link domain in your Firebase project.
  - In `sendPasswordResetEmail`, pass `actionCodeSettings` with your dynamic link as the URL and set `handleCodeInApp: true`.
  - In your app, handle the incoming dynamic link (using RN Firebase Dynamic Links or RN Linking). You’ll get the `oobCode` in the URL query.
  - Use `auth().verifyPasswordResetCode(oobCode)` to verify it’s valid (optional, also returns the email it’s for), then `auth().confirmPasswordReset(oobCode, newPassword)` to actually set the new password ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)).
  - After confirmation, you can prompt the user to log in with the new password (or log them in automatically by also calling `signInWithEmailAndPassword`).
- Make sure to provide user feedback: e.g. "We have emailed you a password reset link if an account exists."

- **Security:** The password reset link has a secure code; you don’t have to worry about intercept as long as the user’s email is secure. Encourage users to use a strong new password. The code can only be used once. Also, after a successful reset, any existing sessions (refresh tokens) for that user are revoked by Firebase for security, so the user will be logged out on other devices.

**Email Verification:**

- Call `sendEmailVerification` for new users or unverified users. You can do this automatically on sign-up or provide a button “Resend verification email” in the app.
- You can use actionCodeSettings here too, similar to reset. For instance, you might want the verification link to open the app. If so, set `url` to something like `myapp://emailVerify` (with your dynamic link setup).
- In the app, if you catch the link, call `auth().applyActionCode(oobCode)` to mark email as verified ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=)). Or simply rely on Firebase’s auto-detection: Actually, when the user opens the link, Firebase will verify and then if it goes back to your app, you can just refresh the user object (call `auth().currentUser.reload()` and then check `currentUser.emailVerified` becomes true).
- When email is verified, you might want to update UI or allow certain features. For example, perhaps only verified users can create content. You can enforce that in Firestore rules: `allow write: if request.auth.token.email_verified == true;` (the token has an `email_verified` claim that is true/false).

**Preventing abuse:**

- Both flows (reset and verify) should not be susceptible to account enumeration (Firebase’s default emails are generic enough). But do not add messages like “Email not found” on password reset – just say something like “If an account exists, you’ll get an email.”
- Rate limit the actions on the UI side to avoid spamming (e.g., user shouldn’t hammer "Resend email" infinitely – you could disable the button for a minute after sending).

By following Firebase’s built-in flows, you offload a lot of complexity. Always use the secure links (they have built-in protections) rather than creating your own less secure method. And ensure your app responds appropriately to the outcome (e.g., navigate user to login after password reset, etc.).

We have now covered how to authenticate users and manage their accounts. Next, let's focus on securing the system and following best practices.

## 4. Security Best Practices

Security is critical when dealing with authentication and user data. In this section, we discuss securing Firebase data with rules, preventing common vulnerabilities, and implementing logging/monitoring for security events.

### 4.1 Firebase Security Rules for Authentication & Database

Firebase Security Rules (for Firestore, Realtime DB, and Storage) are your first line of defense to protect user data. Even with a secure app, you must assume malicious actors could try to query your backend, so rules ensure that only authorized access is allowed.

**Authenticate all access:** By default, Firebase databases in locked mode allow only authenticated access. In Firestore rules, you might start with:

```js
// Firestore rules
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth.uid != null;
    }
  }
}
```

This rule means no one can read or write any document unless they are logged in (request.auth is not null) ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data

- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=The%20following%20Firestore%20rule%20example,your%20database%20contains%20a%20uid)). It’s a blunt rule, but a good starting point for an app where only authenticated users should use the database. The above snippet checks `request.auth.uid` which is the UID of the logged-in user making the request. This corresponds to “Checking if a user is authenticated” pattern ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=The%20following%20Firestore%20rule%20example,your%20database%20contains%20a%20uid)).

**Resource-specific rules:** Most apps require more granular rules. Common patterns:

- **User can only access their own data:** For example, you have a `users` collection with docs where the doc ID is the user’s UID. You want each user to read/write _only_ their own doc. A rule could be:
  ```js
  match /users/{userId} {
    allow read, write: if request.auth.uid == userId;
  }
  ```
  This ensures user X can’t read or write user Y’s profile. Another variant is if the document has an `ownerId` field:
  ```js
  allow read, write: if request.auth.uid == resource.data.ownerId;
  ```
  which achieves a similar effect (requires that the stored ownerId matches the authenticated user) ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=rules_version%20%3D%20%272%27%3B%20service%20cloud,)). This pattern – “document belongs to user” – is extremely common ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=it%20out%2C%20and%20only%20let,users%20see%20their%20own%20documents)) ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=rules_version%20%3D%20%272%27%3B%20service%20cloud,)).

- **Role-based rules:** If using custom claims for admin, you might have:

  ```js
  match /adminContent/{doc} {
    allow write: if request.auth.token.admin == true;
    allow read: if request.auth.token.admin == true;
  }
  ```

  This restricts access to only those with the admin claim ([Get started with Cloud Firestore Security Rules - Firebase](https://firebase.google.com/docs/firestore/security/get-started#:~:text=Firebase%20firebase,with%20Cloud%20Firestore%20Security%20Rules)).

- **Validated writes:** You can add conditions on data. For example, ensure a user can only set `userId` field equal to their UID (to prevent them from creating a record that pretends someone else is owner):

  ```js
  allow create: if request.auth.uid != null
                 && request.resource.data.userId == request.auth.uid;
  ```

  Or ensure they cannot elevate their role by writing a field:

  ```js
  allow update: if request.resource.data.role == resource.data.role;
  ```

  (so even if they try to include a new `role` field in their user doc update, rule rejects it).

- **Storage rules:** If you allow users to upload files (profile pics etc), use similar logic in Cloud Storage rules:
  ```js
  allow write: if request.auth.uid != null
                && request.auth.uid == request.resource.id;
  // for example, if your storage path is like /profilePictures/<uid>
  ```
  In Storage, `resource.id` might represent the filename. You can also use `request.auth.token` in Storage rules. For instance, to ensure the upload is under a folder named with their UID:
  ```js
  match /userUploads/{userId}/{fileName} {
    allow write: if request.auth.uid == userId;
    allow read: if request.auth.uid == userId;  // or more permissive if others can view
  }
  ```
  This prevents user A from uploading to user B’s folder or reading B’s files.

**Principle of least privilege:** Start with everything disallowed and open up only what’s necessary. E.g., an **admin** maybe can read/write all of a certain collection, but a normal user can only read some parts and not write, etc. Firestore rules allow function definitions and reusable conditions, which can help manage complex logic as your app grows.

**Testing rules:** Use the Firebase Rules Playground or the Emulator Suite to test scenarios. For example, test that an unauthenticated request to `/users/uid` is denied, test that a user can read their own doc but not another’s. There are unit test libraries (`@firebase/rules-unit-testing`) that let you simulate requests with certain auth contexts to ensure your rules are correct.

**Keep rules updated:** As you add features (like new collections), don’t forget to update rules for them. It’s easy to forget and accidentally leave data open. For instance, if you introduce a “posts” collection where users can write, define clearly: can users read others’ posts? Can they edit others’ posts? Write the rules accordingly.

In short, use Firebase Security Rules to enforce authentication and per-user access. For example, _“to build user-based and role-based access systems that keep your users' data safe, you need to use Firebase Authentication with Cloud Firestore Security Rules.”_ ([Get started with Cloud Firestore Security Rules - Firebase](https://firebase.google.com/docs/firestore/security/get-started#:~:text=Firebase%20firebase,with%20Cloud%20Firestore%20Security%20Rules)). By combining `request.auth` conditions with your data’s structure, you can prevent unauthorized reads/writes at the database level, even if someone tries to use stolen credentials or bypass your app.

### 4.2 Preventing Common Security Vulnerabilities

Beyond Firebase rules, consider general security best practices for your React Native app:

- **Secure API keys and secrets:** We covered not exposing secrets in the repo. Also, restrict your Firebase API key in Google Cloud to only allowed domains/package names. Though Firebase API keys are not secret (they can be embedded in the app), it’s a good practice to restrict usage to your app’s bundle ID to prevent misuse.

- **Use HTTPS everywhere:** All Firebase traffic is HTTPS by default. If you call any other APIs from your app, ensure you use `https://` endpoints. On iOS, update App Transport Security if needed to disallow insecure HTTP. Avoid accepting invalid SSL certificates.

- **Prevent Injection Attacks:** Traditional SQL injection isn’t an issue with Firebase since queries are structured and there’s no SQL. But if you use any form of dynamic queries or string interpolation (e.g., constructing a query string for a REST call), validate and sanitize inputs. Similarly, if you embed user-generated content in a WebView, sanitize it to prevent XSS (Cross-Site Scripting).

- **Local Data Security:** Avoid storing sensitive data in plain text on the device. Use Secure Store or Keychain for things like auth tokens (the Firebase SDK itself stores its refresh token securely). If you cache any personal info, consider encrypting it if ultra-sensitive.

- **Authentication flows:** Use Firebase’s secure methods instead of rolling your own. For instance, use Firebase phone auth for OTP instead of a custom SMS code solution; it comes with reCAPTCHA or safety net checks automatically to prevent abuse.

- **Limit failed attempts:** Firebase Auth will throttle excessive failed logins, but you can add UI logic to maybe lock out after certain attempts or add increasing delays between tries to counter brute force on passwords.

- **Email link safety:** If you use email link sign-in or send custom action links, treat them like passwords: they are one-time passcodes. Encourage users not to share them. Use short expiry for these links when possible.

- **Keep dependencies updated:** Security vulnerabilities are often discovered in libraries (even Firebase SDK) and fixed in updates. Stay up-to-date with patch versions of RN, Firebase, and any auth-related libraries. For example, older versions of `react-native-fbsdk` might have issues – using `react-native-fbsdk-next` (a maintained fork) is better. Update OpenSSL on Android if a vulnerability is reported (this usually comes via RN updates).

- **Device security features:** Encourage users to use device lock screen. Because if someone can open their phone, they might access the app if you don’t have an app lock. (This is more a user-level concern, but relevant for sensitive apps).

- **Don’t divulge too much info in errors:** For example, when logging in, an error “password incorrect” vs “user not found” could allow enumeration. Firebase by default says "email or password is invalid" (generic). Keep it that way on the UI.

- **Test as a malicious user:** Try using your app in unintended ways – e.g., call APIs out of sequence, or use a tool like Charles Proxy to intercept network calls from your app (during development) to see what someone could glean. Ensure sensitive data isn’t in those calls unencrypted.

- **Code tampering:** Since RN apps can be decompiled, avoid embedding any secrets or logic that trusts the client fully. Always enforce on the backend with rules or server checks. Assume an attacker could inspect your JS bundle. Don’t put admin passwords or anything in it (sounds obvious, but good to remember).

By covering these bases, you prevent most common vulnerabilities. The combination of **secure coding** on the app and **strict Firebase Rules** on the backend will protect against both casual misuse and more determined attacks.

### 4.3 Implementing Logging and Monitoring

Visibility into authentication events is important for security auditing and debugging. Firebase and other tools can help you monitor:

- **Firebase Authentication logs:** Firebase Auth itself logs events (sign-in, sign-out, errors) in the Firebase console (under Usage > Authentication). For more advanced logging, you can enable Cloud Logging for Firebase Auth (if using Google Cloud Identity Platform), but assuming standard Firebase, you have limited direct server-side logs. Instead, consider using Analytics to log auth events.

- **Analytics events:** Use Firebase Analytics to log custom events for security-significant actions:

  - e.g., `analytics().logEvent('login', { method: 'password' })` or method 'google', etc. Or `logEvent('sign_up', { method: 'email' })`. Firebase provides some predefined events like `login` that it might log automatically, but custom events can give you more detail ([Analytics | React Native Firebase](https://rnfirebase.io/analytics/usage#:~:text=Analytics%20automatically%20logs%20some%20events,this%20will%20be%20explained%20below)) ([Analytics | React Native Firebase](https://rnfirebase.io/analytics/usage#:~:text=function%20App%28%29%20,round%20neck%27%2C%20%27long%20sleeved)). Remember that Analytics events are not real-time for monitoring (they show up with some delay), but they’re useful for aggregate stats (like how many logins via Facebook per day, etc.).
  - You can also log an event for something like `password_reset_request` or `email_verify_click` if you handle those in-app.

- **Crashlytics for errors:** If there are critical sections (like a certain auth flow step) where an error should never happen, and if it does you want to know, you can log non-fatal errors to Crashlytics. For instance, if a certain OAuth callback fails, do:

  ```js
  import crashlytics from "@react-native-firebase/crashlytics";
  crashlytics().recordError(new Error("Google OAuth failed at step X"));
  ```

  Crashlytics will report this to the console. Crashlytics automatically captures app crashes, but you can also log custom keys and messages for context ([Crashlytics | React Native Firebase](https://rnfirebase.io/crashlytics/usage#:~:text=Use%20the%20,method)) ([Crashlytics | React Native Firebase](https://rnfirebase.io/crashlytics/usage#:~:text=,trace%20can%20still%20be%20sent)). For example:

  ```js
  crashlytics().setAttribute("userId", auth().currentUser.uid);
  crashlytics().log("User tried Facebook login");
  ```

  Then if a crash happens, you see that log in the crash report.

- **Realtime monitoring:** For critical systems, you might implement a simple admin panel that shows current users online, etc., by reading presence in the database. But for Auth, a better way is to use Cloud Functions triggers:

  - Create a function onAuth user creation/deletion (Auth trigger) to log these events. For example, log to Firestore an entry whenever a new user signs up (with timestamp, UID, provider) so you have an audit trail ([Firebase Authentication triggers - Cloud Functions](https://firebase.google.com/docs/functions/auth-events#:~:text=For%20example%2C%20you%20could%20send,a%20sample%20that%20does)). Similarly, log deletions or perhaps log sign-in events by using Callable functions (less reliable for sign-ins).
  - You could integrate with external monitoring: e.g., send an email/Slack alert when an admin user logs in or when many failed logins occur (though detecting many failed logins might require hooking into client side since Firebase Auth throttle is internal).

- **Performance Monitoring:** Firebase Performance Monitoring can track network calls latency, etc. It’s not directly security, but it can show if, say, the login call is taking unexpectedly long (which could hint at network issues or such).

- **Admin Analytics:** If you have critical admin actions in your app (only accessible by admin users), log those actions to a secure place. For example, if an admin deletes a post or bans a user via your app, you might log that action in an "adminActions" collection with who did what and when. This isn’t Firebase Auth per se, but part of security audit trails.

- **System health monitoring:** If your app uses Cloud Functions for some auth-related tasks (like sending welcome emails), monitor those functions (using Cloud Function logs or an uptime check) to ensure they succeed. Any failure in those could impact user experience/security (e.g., welcome email contains verification link – if it fails, users might not verify emails).

Finally, review your analytics and logs regularly. For example, if you notice a sudden spike in login errors or a strange time of many new accounts, that could indicate a problem (or an attack, like someone trying to mass-create accounts). Firebase has some protections (like phone auth will enforce SMS quota), but vigilance is key. As the Firebase blog says, _“security rules and monitoring help you govern how your users interact with the Firebase backend.”_ ([Get started with Cloud Firestore Security Rules - Firebase](https://firebase.google.com/docs/firestore/security/get-started#:~:text=Firebase%20firebase,with%20Cloud%20Firestore%20Security%20Rules)) ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data

- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=Checking%20if%20a%20User%20is,Authenticated)).

By implementing thorough logging and using Firebase/Google’s tools, you’ll be well-equipped to catch and debug security issues quickly.

## 5. State Management

Managing authentication state in a React Native app is crucial for a seamless user experience. We need to know when the user is logged in or not and respond in the UI (for example, show the login screen vs. the main app). We also want to persist the state so the user doesn’t log in every time they open the app.

### 5.1 Using Redux or Recoil (or Context) for Auth State

While Firebase Auth provides low-level state (through `auth().currentUser` and listeners), you often want to mirror this in your application state (for easier access and to trigger re-renders).

**Redux approach:**  
If your app already uses Redux for state management, you can create an `auth` slice of state. For example:

```js
// authReducer.js
const initialState = {
  user: null,
  loading: true, // to track initial state
};

export default function authReducer(state = initialState, action) {
  switch (action.type) {
    case "LOGIN":
      return { ...state, user: action.user, loading: false };
    case "LOGOUT":
      return { ...state, user: null, loading: false };
    case "SET_LOADING":
      return { ...state, loading: action.loading };
    default:
      return state;
  }
}
```

Then, when Firebase auth state changes, dispatch appropriate actions:

```js
auth().onAuthStateChanged((user) => {
  if (user) {
    dispatch({ type: "LOGIN", user: { uid: user.uid, email: user.email } });
  } else {
    dispatch({ type: "LOGOUT" });
  }
});
```

The `onAuthStateChanged` listener will be triggered whenever the user signs in or out, and even on app start (with the initial auth state) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=Listening%20to%20authentication%20state)) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=function%20App%28%29%20,user%2C%20setUser%5D%20%3D%20useState)). In fact, the first invocation is delayed until Firebase finishes checking persisted auth (which is why we often use a `loading` flag to not flicker the UI) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=It%20is%20important%20to%20remember,whilst%20the%20connection%20is%20established)).

With the above, your Redux store knows if `auth.user` is set or null. You can then conditionally render in your component tree based on that (e.g., in your root navigator, choose the AuthStack vs. AppStack depending on `user`).

**Recoil or Context approach:**  
Redux is robust but can be overkill if you only manage a small state. Recoil provides global state with atoms:

```js
// using Recoil
const authState = atom({
  key: "authState",
  default: { user: null },
});
```

And you can use `useRecoilState(authState)` in a context provider component that subscribes to Firebase. Or simply use React Context:

```jsx
const AuthContext = React.createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    const unsubscribe = auth().onAuthStateChanged((u) => {
      setUser(u);
    });
    return unsubscribe;
  }, []);
  return <AuthContext.Provider value={user}>{children}</AuthContext.Provider>;
}
```

Then consume `AuthContext` in components to know if there's a user. This approach is simpler and works fine for auth state.

**Why manage state, when we have `auth().currentUser`?** Because React needs to know when to re-render. `auth().currentUser` is just a value; it won't trigger re-renders by itself. By using an onAuthStateChanged subscriber and tying it to React state (like context or recoil or redux store), you cause the component tree to update when auth state changes, which is what we want (to show/hide screens appropriately).

**Example using context:**
In your app’s root:

```jsx
<AuthProvider>
  <NavigationContainer>
    {user ? <AppNavigator /> : <AuthNavigator />}
  </NavigationContainer>
</AuthProvider>
```

Where `user` comes from `AuthContext` (via `useContext(AuthContext)`). Initially, `user` might be null until Firebase loads the stored session, then it becomes non-null if a user is logged in ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=It%20is%20important%20to%20remember,whilst%20the%20connection%20is%20established)) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=function%20App%28%29%20,user%2C%20setUser%5D%20%3D%20useState)). You might show a loading spinner in between.

**Synchronization:** If you use Redux, ensure to unsubscribe the onAuthStateChanged when appropriate (though in a typical app, you set it once and it lives for app lifetime). RNFirebase’s listener will emit the initial state asynchronously (so you might want to show a splash or loading state until that fires – see `initializing` in RNFirebase example ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=It%20is%20important%20to%20remember,whilst%20the%20connection%20is%20established))).

**Edge cases:** Sometimes `onAuthStateChanged` might fire twice on app start (once with null, then with user) depending on how quickly persistence is loaded. The RNFirebase docs note that it _will trigger its initial state once a connection to Firebase is established_ ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=It%20is%20important%20to%20remember,whilst%20the%20connection%20is%20established)). That’s why they suggest an `initializing` flag to not render anything until the first state is received ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=established,whilst%20the%20connection%20is%20established)) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=%2F%2F%20Handle%20user%20state%20changes,false%29%3B)). We can implement that easily:

```js
const [initializing, setInitializing] = useState(true);
useEffect(() => {
  const unsubscribe = auth().onAuthStateChanged((user) => {
    setUser(user);
    if (initializing) setInitializing(false);
  });
  return unsubscribe;
}, []);
if (initializing) return <SplashScreen />;
```

This way, we don’t flash login screen before knowing if maybe user is already logged in.

**Managing additional user info:** If you store extra profile info in Firestore, you may also fetch that when auth state is ready. For instance, once `user` is non-null, you might query `firestore().doc('users/'+user.uid)` and store that in context/state as well. That gives you immediate access to profile fields like role, avatar, etc. You could even combine this with the auth state in a single Redux state object.

### 5.2 Persisting Authentication State Across App Reloads

**Firebase persistence:** As mentioned, the native Firebase SDK persists the user’s authentication state by default. _“The native Firebase SDKs provide this functionality using device storage, ensuring that a user’s previous authentication state between app sessions is persisted.”_ ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted)). This means if a user has logged in and then closes the app, when they reopen, `auth().currentUser` will still be set (and `onAuthStateChanged` will fire with that user).

For React Native (non-Expo), you typically don’t need to do anything extra to persist auth state. It uses the Keychain on iOS and SharedPreferences on Android to store the refresh token securely.

**However, if using the Firebase Web SDK in React Native (e.g., in an Expo app pre-SDK 40 or using `firebase/auth` directly),** you must configure persistence because the web SDK doesn’t know how to use React Native AsyncStorage by default. In such cases:

```js
import { initializeAuth } from "firebase/auth";
import { getReactNativePersistence } from "firebase/auth/react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(AsyncStorage),
});
```

This code (as seen in a StackOverflow question ([reactjs - How to persist Firebase User Auth on React Native/ - Stack Overflow](https://stackoverflow.com/questions/75669669/how-to-persist-firebase-user-auth-on-react-native#:~:text=getReactNativePersistence%2C%20initializeAuth%2C%20%7D%20from%20%22firebase%2Fauth%2Freact,firebase%2Ffirestore)) ([reactjs - How to persist Firebase User Auth on React Native/ - Stack Overflow](https://stackoverflow.com/questions/75669669/how-to-persist-firebase-user-auth-on-react-native#:~:text=export%20const%20db%20%3D%20getFirestore))) ensures the web SDK uses AsyncStorage to persist the session. Without it, an Expo app might not remember the user after restart, which is what the user in that post experienced (stuck on login screen offline because the auth state wasn’t persisted) ([reactjs - How to persist Firebase User Auth on React Native/ - Stack Overflow](https://stackoverflow.com/questions/75669669/how-to-persist-firebase-user-auth-on-react-native#:~:text=I%20have%20been%20trying%20to,as%20I%20have%20no%20connection)).

So if you use `@react-native-firebase/auth` (our case), it’s handled. If you used `firebase-js-sdk` in RN, do the above.

**Redux/State persistence:** Even though Firebase remembers the user, if you use Redux or similar to store user info, you might consider persisting that Redux state to avoid needing to fetch profile info again on app launch. But since `onAuthStateChanged` will fire quickly on launch, you can simply re-fetch anything needed.

Alternatively, use `redux-persist` to save the redux state (including auth slice) to AsyncStorage and rehydrate on load. If you do that, be careful: the persisted user info might be stale if the user was logged out externally. It might be safer to rely on Firebase and re-fetch. In any case, `auth().currentUser` is the source of truth.

**Persisting across reload vs. sign-out:** If the user explicitly signs out, you should clear any cached data (Redux state, AsyncStorage user data) since the next user might be different. Firebase will clear its persisted state on sign-out as well.

**Handling offline on start:** One tricky scenario – user is logged in, then goes offline, then opens the app. Firebase will load the last user from storage (so `currentUser` is not null), but it may not be able to refresh the token (since no internet). That’s okay; the user can still be treated as logged in locally and access cached data. But if they try to write to Firestore, the writes will be queued until online. As long as the token hasn’t expired (1h) or Firebase can use the refresh token when back online, it will sync. If the app stayed offline for long (token expired), Firebase will try the refresh when back online – if refresh token is still valid on server, it will succeed. Refresh tokens are long-lived, so likely fine. In short, being offline doesn’t immediately log the user out; they remain authenticated locally with cached credentials, as also noted in Firebase docs.

**Summary:** The heavy lifting of auth persistence is done by Firebase. Our job is to integrate that with app state. Many developers confirm that on RN, closing and reopening the app retains the user (they don’t need to log in each time) ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted)). That said, always test this on actual devices/emulators to confirm (some misconfiguration like using web SDK without persistence could break it).

To ensure a smooth UX:

- Show a splash/loading state until we determine auth state (we did via `initializing`).
- If user is logged in, navigate them to main content immediately (no login required each launch).
- If not, show login/signup.

Also, if implementing features like “Remember me” or “Keep me signed in”, note that Firebase by default keeps them signed in. If you ever want a “do not remember” (like not persisting after app close), you’d have to manually clear credentials or use `signOut` on app close (not typical on mobile). So generally, mobile apps keep users signed in unless they explicitly log out.

Now that we have state management in place, let's look at optimizing performance to make our app efficient and cost-effective.

## 6. Performance Optimization

While implementing authentication and user management, it's important to ensure our app is efficient. This means avoiding unnecessary Firebase reads/writes (to reduce latency and cost) and optimizing how we fetch user data.

### 6.1 Optimizing Authentication and User Data Fetching

**Minimize on-launch calls:** Thanks to persistence, you usually don't need to call `auth().currentUser` or any endpoint on launch to check auth; the SDK has it. Thus, avoid any redundant “check session” network call – not needed. Use the local state (onAuthStateChanged).

**Batch user data fetches:** If you need to load additional user info (say from Firestore) at login, try to batch or pipeline it. For example, instead of fetching user profile, then separately fetching user’s settings, combine them if they are in one document or use Firestore’s ability to get multiple docs in one go (use `.getAll()` or a single query if data is structured that way).

**Cache user profile in memory:** Once you fetch the user’s profile (like their preferences, friends list, etc.), keep it in an in-memory state (Redux/Context) so you don’t re-fetch it on every screen. If you navigate to different screens that need the user’s name or avatar, just read it from the global state instead of querying Firestore repeatedly. As one community tip says, _storing user data in the app state effectively reduces the number of reads from Firestore because you're not querying Firestore each time_ ([Does every user authenticated data count as a read from the ...](https://community.flutterflow.io/ask-the-community/post/does-every-user-authenticated-data-count-as-a-read-from-the-firestore-0qbqG2H9s5e0Qg1#:~:text=Does%20every%20user%20authenticated%20data,Firestore%20each%20time%20you)).

**Use Firestore listeners when appropriate:** If user data can change (like user updates profile from another device), you might set up a listener on the user document (`firestore().doc('users/uid').onSnapshot`) so your app state stays updated in real-time. This is great for responsiveness, but consider the cost: a listener will keep an open connection and fetch updates. If changes are rare, this is fine (and you get offline sync benefits). If you prefer not to listen constantly, you could fetch on important events (like after the user saves changes or when screen focuses).

**Optimize social login calls:** For Google/Facebook login, ensure you're not doing any extra unnecessary fetch. The code we wrote gets an ID token and logs in. That’s as few steps as possible. Some implementations might fetch user info from Google API after sign-in – you likely don’t need that if you only care about basic profile, since Firebase already has name/email from the token.

**Avoid polling:** Don’t poll Firebase in intervals to check something like auth status or user doc changes. Use the provided listeners (Auth has onAuthStateChanged, Firestore has onSnapshot). Polling would waste battery and read counts.

**Consider offline data:** Firebase Firestore by default caches data offline. If a user’s profile doc hasn’t changed, and you query it again, Firestore may serve it from cache quickly (and if online, also check server for updates). This caching is automatic. For heavy usage, you can increase cache size or use data bundles (a way to prefetch a bunch of data). Likely not needed for auth profile since that’s small.

**Use select fields (for Firestore):** If your user document is large but on a certain screen you only need one field, consider structuring your data to separate frequently needed info vs. rarely needed info. Firestore doesn’t natively support field masking in queries (except via the REST API or `select()` in certain client SDKs). But for example, you might keep user's public profile (name, photo) in one doc and private settings in another. Then a public profile fetch doesn’t bring all settings data. This is a form of denormalization. However, be cautious not to over-normalize and cause too many reads.

**Profile heavy operations as needed:** Use Firebase Performance Monitoring or your own timers to see how long certain operations take. If fetching user data is slow, maybe index improvements or data restructuring can help. But usually, fetching a single doc by ID is fast (and indexed by default as it’s a key lookup).

### 6.2 Reducing Firebase Reads/Writes (Minimizing Costs)

Even though Cloud Firestore can handle a lot, costs can build up if you are careless (especially in a large userbase). Some tips to reduce reads/writes:

- **Read from cache when possible:** Firestore’s offline persistence can serve reads from cache at no cost. If data hasn’t changed, you don’t need to re-read from server. By default, Firestore will still count a read if you call `.get()` while online (even if data same) because it has to check for updates. If you truly want to avoid any read, use state as a cache as discussed. For example, after login, we stored user profile in state so we didn’t hit Firestore every time we need the username (saving reads) ([Does every user authenticated data count as a read from the ...](https://community.flutterflow.io/ask-the-community/post/does-every-user-authenticated-data-count-as-a-read-from-the-firestore-0qbqG2H9s5e0Qg1#:~:text=Does%20every%20user%20authenticated%20data,Firestore%20each%20time%20you)).

- **Limit queries:** Only fetch what you need. If listing users or logs, use `.limit(n)` to not read thousands of docs if you only show 20 on screen. Implement infinite scroll or pagination to load more as needed.

- **Avoid uncontrolled listeners:** A listener on a busy collection (like `onSnapshot` on all “posts”) will keep pushing updates to the app and counting reads for each change. If your app doesn’t need real-time updates for that data, consider using one-time `.get()` calls or using Cloud Functions to aggregate changes rather than listening to raw data. In context of auth, this might be less of an issue, but if you had something like an admin monitoring panel that listens to all user sign-ins, that could be heavy.

- **Batch writes:** When making multiple writes, use Firestore batch or transactions. Batching 10 writes in one batch counts as 10 writes (so no cost saving in count) but it’s faster and more atomic. Where it can save cost is if you can do a **single write instead of multiple** by adjusting data model. E.g., instead of storing user’s 5 separate counters in 5 docs, store them in one doc if they are accessed together. Fewer document reads/writes that way.

- **Clean up old data:** This is more about cost management. If you have an "audit logs" collection and it grows huge, that’s a lot of data to query. Maybe archive or delete logs older than X days (depending on requirements) to reduce storage and reads needed.

- **Use analytics to identify heavy usage:** If you log events for every read or screen, you might find that a certain screen is causing 10 reads where it could be 2. Then refactor that screen’s data fetching. For instance, maybe it individually fetched 10 friend profiles – instead fetch them in one query or only fetch summary.

- **Minimize writes on auth triggers:** Sometimes, developers write to Firestore on every login (“user lastSeen = now”). This is fine in moderation but if your app has many logins, that’s a write per login per user. Evaluate if you really need that. If it’s for presence, consider using Realtime Database’s presence system which is optimized for that.

- **Use Cloud Functions to offload work:** For example, if upon user creation you need to set up 3-4 docs (profile, settings, stats etc.), doing it client side would be multiple writes that user waits for. Instead, one trigger in CF can create those docs in one go (still multiple writes, but it happens server-side without multiple round trips for the client). This is more about performance perceived by user.

- **Denormalize wisely:** Firestore encourages some denormalization (like duplicating data in multiple documents to avoid too many subqueries). But denormalization can increase writes (need to update multiple places) and storage. So balance it. For user data, one doc per user is usually fine (no need for heavy denormalization unless you have very high-scale requirements).

Remember, the biggest cost factors for Firestore are the number of reads and writes. So if you can cut down even a few per user per session by caching in state or not querying unnecessarily, it multiplies across many users. In one real example, a developer cut Firestore costs ~30% by implementing a simple in-app caching mechanism so that list data wasn't fetched repeatedly unnecessarily ([Firebase Firestore: Cut Costs by Reducing Reads - Medium](https://medium.com/better-programming/firebase-firestore-cut-costs-by-reducing-reads-edfccb538285#:~:text=Firebase%20Firestore%3A%20Cut%20Costs%20by,through%20a%20simple%20caching%20mechanism)) ([How to Prevent Firebase Runaway Costs - Daniel Llewellyn - Medium](https://danielllewellyn.medium.com/how-to-prevent-firebase-runaway-costs-a8b0dac79384#:~:text=Medium%20danielllewellyn,denormalisation%20strategies%20can%20also)).

As a concrete tip from the community: _“Storing user data in the app state effectively reduces the number of reads from Firestore because you're not querying Firestore each time you need that data.”_ ([Does every user authenticated data count as a read from the ...](https://community.flutterflow.io/ask-the-community/post/does-every-user-authenticated-data-count-as-a-read-from-the-firestore-0qbqG2H9s5e0Qg1#:~:text=Does%20every%20user%20authenticated%20data,Firestore%20each%20time%20you)) This emphasizes how a good state management strategy also benefits performance and cost.

Next, we'll focus on testing and debugging, which ensures our implementation works correctly and is easier to maintain.

## 7. Testing and Debugging

Thorough testing of authentication flows and having good debugging practices will save time and ensure a secure app. We will discuss unit/integration testing and common debugging tips for auth.

### 7.1 Writing Unit and Integration Tests for Authentication

**Unit testing components and logic:**

- If you have functions that aren’t directly the Firebase calls (e.g., form validation, or a Redux reducer handling auth actions), write plain Jest tests for those. For example, test that your `authReducer` returns the correct state given a 'LOGIN' action.
- For any util functions (like formatting a user name, etc.), test those similarly.

**Mocking Firebase for unit tests:**

- When writing unit tests for React components or functions that call Firebase Auth methods, you can mock the Firebase module. Jest allows creating manual mocks for `@react-native-firebase/auth` to simulate behavior. For instance, you could mock `auth().signInWithEmailAndPassword` to resolve with a fake user credential (or throw an error for wrong password). This way you test your component’s response to success or failure without actually hitting Firebase.
- Example with Jest mock:
  ```js
  jest.mock("@react-native-firebase/auth", () => {
    return () => ({
      signInWithEmailAndPassword: jest.fn((email, pass) => {
        if (email === "test@example.com" && pass === "correct") {
          return Promise.resolve({ user: { uid: "123", email } });
        } else {
          const err = new Error("Auth failed");
          err.code = "auth/wrong-password";
          return Promise.reject(err);
        }
      }),
      // ... mock other methods as needed
    });
  });
  ```
  Then your test can call your login function and expect a certain outcome.

**Integration testing with Firebase Emulator:**
For a more end-to-end test, use Firebase’s **Local Emulator Suite**, which includes an Auth emulator. The Auth emulator can mimic email/password signups, sign-ins, and even OAuth flows (with test credentials) ([Connect your app to the Authentication Emulator - Firebase](https://firebase.google.com/docs/emulator-suite/connect_auth#:~:text=Connect%20your%20app%20to%20the,For)). Benefits of the emulator:

- No real network calls; tests run offline and fast.
- No risk of messing up real user data or hitting usage quotas.
- You can create test scenarios, like pre-populating a user in the emulator and then trying to sign in.

How to use:

- Install Firebase CLI and run `firebase emulators:start --only auth` (maybe along with Firestore if needed).
- In your app (during tests or development mode), tell Firebase Auth to use the emulator:
  ```js
  if (__DEV__) {
    auth().useEmulator("http://localhost:9099");
  }
  ```
  This will direct all Auth calls to the local emulator at port 9099.
- Now, in your tests (or while running the app in dev), any signUp/signIn goes to emulator. The emulator by default allows any email/password (and you can even enable phone auth with a dummy SMS code flow).

You can script setup for integration tests:

- e.g., Before tests, hit the Auth emulator REST API to create a user (to test login).
- Then run your app logic to login that user, assert success.
- Or test sign-up: call your signUp function with new email/pass, then query emulator to see if user was created.

The Firebase Auth emulator supports many flows including email link, phone OTP, etc., with special predefined test phone numbers for automatic SMS codes (like +1 555-555-0000 always yields code '123456').

Using the emulator in a React Native Jest environment can be tricky (since it would require the emulator running during tests). Some developers might instead do this with Detox (for end-to-end on device) or a Node.js script using Firebase Admin SDK.

**End-to-end (E2E) testing:**
Consider using an E2E framework like **Detox** for React Native. You can write tests that simulate actual app usage:

- e.g., Launch app, tap "Login", enter email/password, tap submit, expect to see Home screen.
- Detox can interact with UI elements by testIDs. Combined with the Auth emulator, this becomes a true end-to-end test with no external dependency.
- Another route is Appium or other mobile testing tools. But Detox is popular for RN.

**Testing security rules:**
It’s also important to test that your security rules work as expected. Firebase provides the `@firebase/rules-unit-testing` package to simulate Firestore (and Auth context) to test reads/writes. For example, you can create a dummy user token with certain claims and attempt to read a doc in code, expecting an "allowed" or "denied". This is more of a backend test, but if you wrote complex rules for user data, it’s wise to test them. These tests run in Node (not in RN) typically.

**Automated CI for tests:**
Ensure your CI (like GitHub Actions) runs the unit tests. You can also set up the Firebase emulator in CI to run integration tests. The emulator can be started via CLI in a CI environment as well.

### 7.2 Debugging Authentication Issues

Even with tests, issues can arise when users start using the app on different devices and configurations. Here are tips for debugging:

- **Enable Debug mode for Firebase (if needed):** The RNFirebase library doesn’t have a single switch for verbose logging like the web SDK does, but you can often see a lot of info in Xcode/Android Studio logs. For example, on Android, you might add in `AndroidManifest.xml`:

  ```xml
  <application ... android:debuggable="true">
    <meta-data android:name="firebase_auth_log_level" android:value="DEBUG"/>
  </application>
  ```

  Or simply observe logcat for tags related to Firebase. On iOS, see the console for messages.

- **Common issues and resolutions:**

  **Google Sign-In DEVELOPER_ERROR on Android:** This is a frequent issue. It usually means the SHA-1 fingerprint or OAuth client ID setup is wrong ([DEVELOPER_ERROR , google sign in error on react native ... - Reddit](https://www.reddit.com/r/reactnative/comments/1cmabyr/error_developer_error_google_sign_in_error_on/#:~:text=Reddit%20www,the%20web%20client%20id)) ([Fixing DEVELOPER_ERROR in React Native SSO with Google in ...](https://serdarcevher.medium.com/fixing-developer-error-in-react-native-sso-with-google-in-android-without-firebase-d8782b801305#:~:text=,suffix%2C%20in%20the%20Google%20Cloud)). Ensure:

  - You added the SHA-1 of the **app signing certificate** (if using Play App Signing, use the one from Play console) to Firebase project.
  - You used the **Web client ID** in `GoogleSignin.configure`.
  - The reversed client ID in Info.plist matches that Web client ID.
  - If using multiple Firebase projects (dev/prod), ensure the google-services.json is correct for the build.
  - Sometimes, uninstalling the app and reinstalling (after these fixes) is needed because the OAuth consent screen might cache something.

  **Facebook login issues:**

  - If `LoginManager.logInWithPermissions` returns isCancelled immediately, check that your Facebook app config (ID, name) is correct in Info.plist and strings.xml and that the app is setup in Facebook’s dashboard for your bundle ID. Also, test the Facebook login process outside your app via the Facebook SDK to ensure the Facebook app or web is working.
  - On Android, make sure the Key Hash is set in your Facebook developer settings. You can get it by running `keytool` on your keystore or looking at logs – FBSDK will often log an error with the key that was expected. Add that in Facebook console.
  - If using limited login or issues with nonce, ensure you generate and pass nonce properly as per docs.

  **Apple Sign-In issues:**

  - On simulator, Apple Sign In might not work (if you’re not logged into an Apple ID on the simulator). Test on a real device.
  - If `appleAuth.performRequest` is not returning or Apple button does nothing, check that you enabled the capability in Xcode and that your Apple service ID & associated domains are set. Also, Apple Sign-In requires a real device to retrieve an identityToken in some cases.
  - If signIn works but Firebase throws an error, ensure you passed the `nonce` correctly when creating the credential (the same nonce you sent in the request). Also check your Firebase Apple provider setup (Service ID, key ID, etc.).
  - If `auth().signInWithCredential` for Apple fails with `auth/invalid-credential`, it’s likely an issue with the Apple JWT or the nonce mismatching – double-check those values.

  **Email/Password issues:**

  - `auth/user-not-found` or `auth/wrong-password`: These are straightforward – make sure you’re testing with a user that exists and password is correct. If you get user-not-found but you are certain the user exists, you might be pointing to a different Firebase project (like using the wrong GoogleServices-Info.plist or not having that user in this environment).
  - `auth/too-many-requests`: This can happen if test code rapidly calls login and fails – Firebase will throttle. If you hit this in development, wait a bit or use multiple test accounts.

  **Multi-factor debugging:**

  - Use the Auth emulator for MFA to simulate SMS without real phones. If using real phone, be mindful of SMS quotas.
  - The error messages for MFA flows are complex. Log out the `error.code` and full error to see what’s expected.
  - If resolver steps aren’t working, verify that `resolver.session` is being passed correctly. Also ensure on the console that multi-factor is enabled properly.

- **Device logs:** Always check device logs when debugging an auth issue:

  - Android: `adb logcat *:E ReactNative:V ReactNativeJS:V` (to see JS logs and errors). Or filter by `FirebaseAuth` or `GoogleService`.
  - iOS: run the app via Xcode and watch the debug console for any warnings/errors during auth flows.
  - Often, native SDKs print helpful warnings (e.g., GoogleSignIn might say "Unable to find GoogleService-Info.plist" or similar if config missing).

- **Network debugging:** For certain flows like email link or any web-based OAuth, sometimes it helps to intercept network calls. Using a proxy tool (Charles Proxy or Android’s network inspector) can show if requests are going out and responses. However, much of Firebase Auth is encrypted (and using secure web endpoints), so there's limited insight there.

- **Use emulator or test accounts in dev:** That way you can freely create/delete users without worrying about real user data. Also, you can test error scenarios (e.g., create a user, then try logging in with wrong password to trigger the error, see how your app reacts).

- **Edge case debugging:** Test scenarios such as:

  - The user signs in, then you revoke their account in Firebase console – what does the app do on next action? (It might get user disabled error).
  - The user changes password on another device – the current device’s token might become invalid at next use. Does the app handle a reauthentication prompt?
  - The user uses “Continue with Google” but cancels halfway – does your UI handle that gracefully (it should).

- **Consult error codes reference:** Firebase docs list all Auth error codes and their meaning. If you see an unfamiliar error code, refer to Firebase documentation or community forums. For example, `auth/account-exists-with-different-credential` means the email was already used with another sign-in method – you then may call `fetchSignInMethodsForEmail` and offer to link accounts. That’s a scenario to handle if you allow both email/password and Google for instance.

- **Use try/catch around async calls:** Always catch errors from `signIn`/`createUser`/`link` calls and log them (or at least handle them in UI). During development, logging full error objects to console can help identify misconfigurations (like error.message might have a URL to more info or a hint).

- **Monitoring in production:** Use Crashlytics to log unexpected errors. For example, you might log a non-fatal if a certain auth step fails in a way that shouldn’t (like `recordError` for an MFA failure flow that you thought was unreachable). Also, keep an eye on Firebase Auth usage in the console – if there’s a spike in anonymous users or errors, it may indicate an issue.

By systematically testing flows and using the above debugging methods, you can iron out most issues before users encounter them. And if something slips through, your logging and monitoring should catch it so you can fix it quickly.

Now that development and testing are done, let's discuss how to deploy the app and maintain it through CI/CD.

## 8. Deployment and Continuous Integration

Deploying a React Native app, especially with Firebase integration, involves building the app binaries and possibly setting up CI/CD pipelines for automated builds, tests, and releases. We’ll cover setting up a CI/CD pipeline and handling app updates and versioning.

### 8.1 Setting up CI/CD Pipelines for React Native apps with Firebase

A good CI/CD (Continuous Integration/Continuous Deployment) setup will automatically run tests and build your app for distribution whenever you push changes. We can use services like GitHub Actions, CircleCI, Bitrise, or others.

**Typical CI/CD stages:**

1. **Install Dependencies:** The CI runner will checkout your repository, then run `npm install` (and possibly `pod install` in ios directory).
2. **Run Tests:** Execute your unit tests (e.g., `npm test`). If any test fails, the pipeline stops (ensuring no broken code is deployed).
3. **Build the app:**
   - For Android: run `./gradlew assembleRelease` (to get an APK or AAB).
   - For iOS: run a script like `xcodebuild -workspace ios/YourApp.xcworkspace -scheme YourApp -configuration Release -archivePath YourApp.xcarchive archive` followed by `xcodebuild -exportArchive ...` to get an IPA. Or simpler, use **Fastlane**, which provides easier commands for building both platforms.
4. **Distribute the app:** After building, you can automatically distribute the binaries:
   - **Firebase App Distribution:** This service lets you upload APKs/IPAs to Firebase, and then invite testers (via their email) to download from Firebase. There’s a fastlane action and a Firebase CLI for this. For example, `firebase appdistribution:distribute <file> --app <AppID> --groups <tester group>` will upload it.
   - **App Store / Play Store:** For production releases, you might integrate fastlane or use platform-specific CLI. For Google Play, you can use the Google Play Developer API (fastlane supply, etc.), and for iOS, use fastlane deliver or the App Store Connect API to push TestFlight builds.
   - Many CI services have integrations with app stores or you can use fastlane match to handle code signing seamlessly in CI.
5. **Post-process:** Possibly upload source maps (for JavaScript error symbolication) to Sentry or Crashlytics, increment version numbers, etc.

**Integrating Firebase config in CI:**

- Remember to provide your `google-services.json` and `GoogleService-Info.plist` in the CI build. Since you likely don’t commit these (some do commit them, which is okay as they aren’t highly secret), ensure CI has them.
- One approach: Base64 encode the files and store as environment variables in CI. Then have a script in CI to decode and place them in the appropriate folders before build.
- Alternatively, use CI secret storage to store each file’s content. Or store them in a secure artifact store. The key is to not expose them in logs.

**Managing environment variants:**

- If you have separate Firebase projects for Dev/Prod, you might use different config files. Set up CI to use dev config on pushes to a dev branch, and prod config on main branch, etc.
- Use environment variables for any config differences as we set up earlier ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=environment%20variables%20to%20inject%20your,included%20in%20your%20final%20artifact)).

**Example (GitHub Actions):**

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with: { node-version: 16 }
      - name: Install JS dependencies
        run: npm ci
      - name: Install Pods
        run: |
          cd ios
          pod install --quiet
      - name: Run tests
        run: npm test -- --ci
      - name: Set up Android JDK
        uses: actions/setup-java@v1
        with: { java-version: 11 }
      - name: Decrypt Google Services
        env:
          GSERVICES_JSON: ${{ secrets.GOOGLE_SERVICES_JSON_DEV }}
          GSERVICES_INFO: ${{ secrets.GOOGLE_SERVICE_INFO_DEV }}
        run: |
          echo "$GSERVICES_JSON" | base64 -d > android/app/google-services.json
          echo "$GSERVICES_INFO" | base64 -d > ios/YourApp/GoogleService-Info.plist
      - name: Build Android Release
        run: cd android && ./gradlew assembleRelease
      - name: Build iOS Release
        run: |
          cd ios
          xcodebuild -workspace YourApp.xcworkspace -scheme YourApp -configuration Release -sdk iphoneos -archivePath $PWD/build/YourApp.xcarchive clean archive
          xcodebuild -exportArchive -archivePath $PWD/build/YourApp.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath $PWD/build/
      # (Assumes ExportOptions.plist is configured for App Store or Ad Hoc distribution)
      - name: Upload to Firebase App Distribution (Android)
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_SERVICE_ACCOUNT_TOKEN }}
        run: npx firebase appdistribution:distribute android/app/build/outputs/apk/release/app-release.apk --app YOUR_FIREBASE_APP_ID --groups testers
```

The above is illustrative. It checks out code, installs deps, runs tests, sets up environment (Java), decodes secret config files, builds both platforms, and uses Firebase CLI to distribute the Android APK. (iOS distribution could similarly use `firebase appdistribution:distribute` for the IPA).

If using **Fastlane**:

- You can have a `Fastfile` with lanes for Android and iOS builds, and even lanes for distribution. There’s a fastlane action for Firebase App Distribution (via plugin or directly hitting the API).
- Many find fastlane easiest for code signing on iOS (match to manage certificates and provisioning profiles) ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=Fastlane%20was%20originally%20an%20iOS,from%20CI%20and%20CI%20systems)) ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=The%20tricky%20part%20of%20going,share%20signing%20credentials%20between%20teams)). Ensure CI can access the repository or storage where match stores certs (usually encrypted in a git repo or in Google Cloud Storage).
- On Android, ensure you have the keystore in CI. Like config files, store the keystore file as a secret (Base64) and reconstruct it, and use env variables for the keystore password, alias, alias password.

**Continuous Deployment triggers:**

- You might set the pipeline to trigger on every push (for continuous integration testing).
- For deployment, maybe only on pushes to a release branch or when a tag is created.
- Or set up manual triggers for actual App Store deploy to avoid releasing on every commit.

**Public vs Private config:**

- Note that the Firebase config files (google-services) are generally fine to commit (they don't contain super-sensitive data, mainly identifiers). Many open source projects commit them. If your app’s users can use your Firebase backend freely if they have those, then your rules should mitigate abuse. But to be safe, some treat them as semi-secret. In CI, it's okay as long as your repo is private or you use secrets.

**Set up multi-environment projects:**
One medium article details using multiple GoogleService-Info.plist files for dev and prod and switching based on build configuration ([Setting Up CI/CD for React Native with GitHub Actions and Firebase ...](https://tudotechnologies.medium.com/setting-up-ci-cd-for-react-native-with-github-actions-and-firebase-app-distribution-86aa416e4beb#:~:text=Setting%20Up%20CI%2FCD%20for%20React,Actions%20and%20Firebase%20App%20Distribution)). This is advanced Xcode setup, but beneficial if you have separate firebase projects.

To sum up, a CI/CD pipeline will help automate building and distributing your app. Many have written guides on this, e.g., _“Setting up CI/CD for React Native with GitHub Actions and Firebase App Distribution”_ ([Setting Up CI/CD for React Native with GitHub Actions and Firebase ...](https://tudotechnologies.medium.com/setting-up-ci-cd-for-react-native-with-github-actions-and-firebase-app-distribution-86aa416e4beb#:~:text=Setting%20Up%20CI%2FCD%20for%20React,Actions%20and%20Firebase%20App%20Distribution)) and _“auto-generate a React Native app and send it to Firebase (Android) and TestFlight (iOS) using Fastlane and CircleCI”_ ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=In%20this%20article%2C%20you%20will,and%20how%20to%20configure%20circleCi)) ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=There%20are%20several%20solutions%20to,fixes%2C%20and%20sample%20configuration%20files)). These references echo the steps we've outlined, ensuring testers and users can get new versions quickly and reliably.

### 8.2 Handling Push Updates and App Versioning

**App versioning:**

- React Native apps have two version identifiers on each platform: the **JS bundle version** (you might control via package.json or manually), and the native version (Android `versionName` & `versionCode`, iOS `CFBundleShortVersionString` & `CFBundleVersion`).
- Each release, increment these properly. Users see the human-readable version (like 1.2.3) and app stores require monotonic build numbers (versionCode on Android, CFBundleVersion on iOS).
- If using CI, you can automate bumping the version. For example, have a step that reads the current version, increments the patch number, updates `android/app/build.gradle` and `ios/*/Info.plist` files. Fastlane has `incrementBuildNumber` for iOS and you can pass `--version-code` to gradle for Android.
- Keep your app’s version consistent with any in-app display or analytics (you might log the version in Analytics user properties for tracking).

**Push updates (over-the-air updates):**

- One approach is to use CodePush (by Microsoft App Center). CodePush allows deploying JS bundle and assets updates without App Store/Play Store. It’s great for quick patches. You integrate the CodePush SDK in your app. Then using their CLI, you push updates to their server, and the app will download them at runtime.
- Be mindful of store guidelines: Apple allows OTA updates for bug fixes but not for adding new features that circumvent review. Don’t abuse it.
- If you want to avoid third-party, Expo’s OTA update (if you were using Expo managed workflow) is another method, but since we are bare RN here, CodePush is the typical solution.
- Setting up CodePush:
  - Register app in App Center, get deployment keys.
  - Install `react-native-code-push` and configure in AppDelegate and MainApplication.
  - CodePush can be configured to check for updates on app start or resume.
  - Then on CI, after building or after merging to main, you could use `appcenter codepush release-react` to publish the update. This can be integrated in your CI pipeline as an additional step for staging or production.
- If using CodePush, still do regular store releases periodically, especially if native code changed or numerous changes have accumulated.

**Alternate approach:** If not using CodePush, just rely on frequent releases via the app stores. Perhaps use Firebase App Distribution or TestFlight for quick internal testing of fixes.

**Force updating users:**

- Over time, you might want to force users to upgrade (for instance, if a critical bug was fixed or a security issue). Implement a mechanism, such as:
  - Maintain a “minimum supported version” in Remote Config or Firestore.
  - On app launch, fetch this value and compare with app version. If app’s version is below minimum, prompt user to update (and possibly disable certain functionality).
  - This is important if you plan breaking changes. It’s more of an app maintenance concern.

**Push notifications (FCM):** Not to be confused with “push updates”. If by push updates the requirement meant push notifications, note:

- Firebase Cloud Messaging (FCM) can be used to send notifications to users. It requires setup of APNs on iOS and use of `@react-native-firebase/messaging`.
- But push notifications is a whole topic on its own and was not explicitly listed, so likely “push updates” referred to updating the app itself (via CodePush or store updates).
- If needed, you can integrate messaging and test sending auth-related notifications (like “Your account was logged in from a new device” security alerts).

**CI/CD for releases:** Ideally, tie version bumps and deployment together:

- For example, merging into a `release` branch triggers CI to bump version, build, and upload to TestFlight and Play Store internal testing. Then you or QA verify, then promote to production.
- Some teams even automate promotion if tests pass (continuous deployment), but with app stores, there’s often a review process (though Google allows automatic rollout if configured).

**Automating changelogs:** Use your commit history or PR descriptions to generate release notes. There are tools (like semantic release) that can parse commit messages to create a changelog. These can be fed into the App Store or Play Store on release.

**Monitor after deployment:** Once deployed, use Firebase Crashlytics to monitor if any crashes spiked (maybe a regression). Use Firebase Analytics events or user feedback to verify that the auth flows work in production as in testing.

By establishing a solid CI/CD and update strategy, your team can iterate quickly and deliver new features or fixes (like changes to auth logic or UI) to users with minimal friction. As one guide said, _automating the beta generation process and distribution via Fastlane and CI can drastically streamline releasing apps_ ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=In%20this%20article%2C%20you%20will,and%20how%20to%20configure%20circleCi)) ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=There%20are%20several%20solutions%20to,fixes%2C%20and%20sample%20configuration%20files)) – which is crucial for rapid development cycles.

## 9. Bonus: Advanced Features

Now we explore some advanced considerations and features to enhance our app: enabling offline capabilities for auth, using analytics/crash reporting to improve user experience, and extending functionality with Cloud Functions.

### 9.1 Offline Authentication Strategies

Supporting offline mode in an app means users can continue using some functionality without internet. For authentication, offline mode is limited but there are strategies to handle it gracefully:

- **Use Firebase’s offline persistence:** Firestore and Realtime DB both offer offline support (caching reads and queueing writes) ([Cloud Firestore | React Native Firebase](https://rnfirebase.io/firestore/usage#:~:text=Firestore%20provides%20out%20of%20the,server%20when%20they%20regain%20connectivity)). For instance, if a user is logged in and goes offline, they can still read any data that was cached and even write new data (which will sync when back online). As mentioned, Firebase Auth will keep the user’s session active offline – the user doesn’t get logged out just because there’s no connection.
- _“Firestore provides out of the box support for offline capabilities... uses a local database which synchronizes automatically with the server when connectivity is regained.”_ ([Cloud Firestore | React Native Firebase](https://rnfirebase.io/firestore/usage#:~:text=Firestore%20provides%20out%20of%20the,server%20when%20they%20regain%20connectivity)). Enable this (Firestore is enabled by default offline in RNFirebase; Realtime DB you have to call `database().setPersistenceEnabled(true)` if using it ([Offline Support - React Native Firebase](https://rnfirebase.io/database/offline-support#:~:text=Enabling%20Persistence,json))).

- **Allow login offline if credentials are known:** This is tricky. If a user is not logged in and has no internet, you cannot verify credentials with Firebase (no server connection). However, if the user had previously logged in on the device, Firebase may have a refresh token cached. If the token hasn’t expired, the SDK might consider `currentUser` valid (I believe Firebase requires at least one successful login; if app restarted offline, it still loads the last user). So if a user was logged in and they haven’t signed out, your app should treat them as logged in when offline (even if the token can’t be refreshed until online). This is beneficial – they can still use the app’s offline data. Just be careful to handle actions that require server (maybe queue them).
- If a user explicitly signed out, then offline they can’t sign back in until net is available. You can mitigate by an **“offline mode”** concept: E.g., allow the user to use the app in a limited read-only way if offline and not authenticated. Maybe store some public data offline that doesn’t require login.
- **Offline login via cache (not recommended for high security):** In some cases, developers implement a fallback where they hash the password and store it so that if offline, they can compare input hash to stored hash to “log in” the user locally. This might be acceptable for certain apps (especially if it’s more about convenience than security, and user explicitly opted for “remember me offline”). If you do this, **encrypt the stored password** strongly (or better, store a salted hash). Even then, it’s risky. Also, without connectivity, the user can’t truly be authenticated against server, so you should perhaps limit what they can do.
- If you have critical features (like a field service app where they must login daily but often are offline), consider an approach like:
  - On a successful login, store an encrypted token or the credentials (with user consent).
  - If offline and user tries to login with same credentials, allow access to offline data if the credentials match what’s stored. However, inform them that they are in offline mode and some features won’t be available until they connect.
  - As soon as internet is back, perform a real login to verify and sync any changes.
    This approach is advanced and must be carefully implemented to avoid security holes (you wouldn’t want someone to steal the device and get in offline because the credentials were stored).
- **Guest mode (offline usage without auth):** Another approach: allow certain features without any login. For example, let the user browse some content and mark favorites offline, then later when they create an account, sync that data. This avoids needing offline auth altogether.

- **Testing offline behavior:** Use emulator’s network conditioning or simply disable wifi/data on a test device. Test flows like app launch offline (if user was logged in prior) – the app should still show the main screen (since `auth().currentUser` is cached) and maybe indicate “offline mode” if needed. Test making a Firestore query offline – it should return cached data quickly. Also test writing data offline – the writes will succeed locally and then check that when you reconnect, they sync (Firebase will emit onSnapshot events when sync completes).

- **Limitations:** Actions like password reset obviously can’t be done offline. If the user tries, queue the request and show a message “Will send when back online” – but better to just disable those actions offline.
- **Design for intermittent connectivity:** The app might go online and offline frequently (subway rides, etc.). Use listeners to detect connection (NetInfo can tell you) and possibly use `firestore().enableNetwork()` / `disableNetwork()` if you want manual control (but not usually necessary). At least, inform the user with a banner “You are offline” so they know changes may not be up-to-date.

Offline support largely means leveraging Firebase’s local data capabilities ([Cloud Firestore | React Native Firebase](https://rnfirebase.io/firestore/usage#:~:text=Firestore%20provides%20out%20of%20the,server%20when%20they%20regain%20connectivity)) and building your UI to not hard-require immediate server responses. In terms of authentication, rely on cached auth state for already logged-in users. Perhaps consider a grace period if token expired while offline – you might allow them some offline usage and force login when back online.

### 9.2 Implementing User Analytics and Crash Reporting

Firebase offers **Analytics** and **Crashlytics** which are invaluable for understanding usage and stability.

**Firebase Analytics for user behavior:**

- Already, Firebase will log some events automatically (first_open, app_update, etc.) ([Analytics | React Native Firebase](https://rnfirebase.io/analytics/usage#:~:text=Analytics%20automatically%20logs%20some%20events,this%20will%20be%20explained%20below)).
- You should log custom events for important actions. For auth, examples:
  - `login` (with parameter `method: 'password'` or 'google', etc.) – so you can see how users authenticate mostly.
  - `signup` (param: method).
  - `logout` event when user signs out.
  - `reset_password` when a reset email is sent.
  - `mfa_enroll` when user enrolls a 2nd factor.
  - If your app has user roles or subscription levels, log an event or user property (e.g., `setUserProperty('role', 'premium')`).
- These analytics help product decisions (maybe you find that 70% users use Google login, so focus on that).
- They also help debugging flows – e.g., you can funnel from signup to first login to retention.
- Crashlytics can be linked with Analytics to log `App Exception` events for crashes.
- **Integration:** We need to add `@react-native-firebase/analytics` module. After installing and configuring (just like other RN Firebase modules), simply call `analytics().logEvent(name, params)` as needed. For example:
  ```js
  analytics().logEvent("login", { method: "google" });
  ```
  This gets sent to Firebase. In debug mode, use `adb shell setprop debug.firebase.analytics.app <package-name>` to enable verbose analytics logging on Android, so you can see events in logcat to verify.
- Analytics logs are not real-time in console; expect a few hours delay. But using DebugView (in Firebase console > Analytics > DebugView) you can see events from a development device live, which is great for verifying instrumentation.

**Crashlytics for crash reporting:**

- Add `@react-native-firebase/crashlytics` to the project. After installation, build the app so it registers with Crashlytics.
- On iOS, make sure to run the Crashlytics run script in Xcode build phases (RNFirebase should add it).
- Test Crashlytics integration by forcing a crash: call `crashlytics().crash()` in dev to see if it appears in Firebase console (it should within a few minutes under Crashlytics > Issues).
- Use Crashlytics to log non-fatal errors or custom keys:
  - `crashlytics().log("User reached Settings Screen");` – this will show up in crash reports timeline if a crash happens.
  - `crashlytics().setUserId(auth().currentUser.uid)` – sets the user ID for crash correlation. This is useful to see if a particular user always crashes, or to find crashes affecting many users (though user PII should not be logged in Crashlytics).
  - `crashlytics().recordError(error)` – if you catch an error that you don’t throw but want to report (e.g., a promise rejection that you handle but still want to know about). The stack trace will be sent to Crashlytics as a non-fatal error.
- Crashlytics can help identify issues in the wild that testing didn’t catch (especially platform-specific or weird edge cases).
- The combination of **Analytics + Crashlytics** can do things like: see if a crash happens right after a specific event (maybe “signup” event is always followed by a crash, indicating an issue in post-signup flow).
- Also consider using **Performance Monitoring** (`@react-native-firebase/perf`) to measure network call latencies, etc., if relevant. It’s less crucial for auth but could measure, say, how fast logins are or if some function is slow on certain devices.

**User analytics beyond Firebase:**

- If needed, integrate other analytics (Google Analytics via Tag Manager, or Amplitude, etc.) depending on stakeholder needs. But Firebase Analytics is usually sufficient and free.
- Ensure to comply with privacy laws: if in EU, you might need user consent for Analytics or an option to opt-out. Firebase Analytics provides options to not collect or to anonymize IP etc.
- Use **Remote Config** in conjunction with Analytics: e.g., you can create an experiment for different onboarding flows (A/B test social login button placements) and measure via analytics events which yields better conversion.

**Crash reporting beyond Crashlytics:**

- Sentry is a popular alternative for capturing JS errors (including non-crash errors). Crashlytics mainly catches native crashes (and some JS crashes if they result in app crash). For unhandled JS exceptions, you might want to integrate Sentry or a similar service for more detail (Crashlytics might show a generic "JavaScriptError" crash without stack unless you manually call recordError).
- You can actually combine: use Sentry for JS, Crashlytics for native. Or just Sentry for all – but since we already have Crashlytics with Firebase, using it plus adding some manual `recordError` on caught JS exceptions is a simpler addition.
- For example, globally catch JS exceptions:
  ```js
  const defaultHandler =
    ErrorUtils.getGlobalHandler && ErrorUtils.getGlobalHandler();
  ErrorUtils.setGlobalHandler((error, isFatal) => {
    crashlytics().recordError(error);
    if (defaultHandler) defaultHandler(error, isFatal);
  });
  ```
  This will send any uncaught error to Crashlytics, then let the app crash or handle as normal.

In conclusion, user analytics give insight into how the app is used and crash reporting tells you where it breaks. Both are essential for continuous improvement and for verifying that your authentication and user management flows are working well in production. They help answer questions like: Are users dropping off during sign-up? Is there a crash affecting certain login methods? With that data, you can iterate and fix issues proactively.

### 9.3 Firebase Cloud Functions for User Event Handling

**Cloud Functions** can extend your app by running backend code in response to Firebase events. For user management, some useful Cloud Function triggers and use-cases include:

- **Send welcome emails or perform post-signup tasks:**  
  Use the Auth trigger `functions.auth.user().onCreate(async (user) => { ... })` ([Firebase Authentication triggers - Cloud Functions](https://firebase.google.com/docs/functions/auth-events#:~:text=For%20example%2C%20you%20could%20send,a%20sample%20that%20does)). This fires whenever a new user is created (via any method). Inside, you could:

  - Send a welcome email (using an email service like SendGrid, Mailgun, or Firebase Extensions that handle email).
  - Create a Firestore document for the user (if you want to prepopulate something).
  - Set a custom claim (maybe mark first user as admin, or if email is from a certain domain give a role).
  - The Firebase docs example: _“you could send a welcome email to a user who has just created an account in your app.”_ ([Firebase Authentication triggers - Cloud Functions](https://firebase.google.com/docs/functions/auth-events#:~:text=For%20example%2C%20you%20could%20send,a%20sample%20that%20does)) and Cloud Functions Guide: _“when someone signs up, a Cloud Function can kick in to send a welcome email, set up user profiles, or link with other services.”_ ([How to use Firebase Cloud Functions to trigger an event on user sign-up? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-use-firebase-cloud-functions-to-trigger-an-event-on-user-sign-up#:~:text=Firebase%20Cloud%20Functions%20let%20developers,whenever%20a%20user%20signs%20up)). This is exactly what onCreate triggers allow.

  For instance:

  ```js
  exports.onNewUser = functions.auth.user().onCreate(async (user) => {
    const email = user.email;
    const uid = user.uid;
    // 1. Add a Firestore profile doc
    await admin.firestore().doc(`users/${uid}`).set({
      email: email,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      // any default fields
    });
    // 2. Send a welcome email via a third-party service (e.g. sendGrid)
    if (email) {
      await sendWelcomeEmail(email, user.displayName);
    }
  });
  ```

- **Clean up on user deletion:**  
  Use `functions.auth.user().onDelete(user => { ... })`. This triggers when a user is deleted. You can:

  - Remove their Firestore document and subcollections.
  - Delete their Storage files (like profile pictures).
  - Revoke any custom resources or subscriptions associated with them.
  - _Important:_ If you rely on this for cleanup, ensure your security rules prevent others from accessing those leftover data too. It’s a good safety measure though so your DB doesn’t grow with orphaned data.
  - Example:
    ```js
    exports.onUserDeleted = functions.auth.user().onDelete(async (user) => {
      const uid = user.uid;
      // Delete user Firestore doc
      await admin.firestore().doc(`users/${uid}`).delete();
      // Delete user storage folder
      const bucket = admin.storage().bucket();
      await bucket.deleteFiles({ prefix: `uploads/${uid}/` });
    });
    ```
    (Deleting files requires proper IAM permissions for the functions service account, but conceptually this is what you do.)

- **Custom authentication flows:**
  Cloud Functions can create **custom tokens** if you need to sign in users via custom mechanisms (like integrating with a legacy auth system or an enterprise login). The Admin SDK’s `createCustomToken(uid, claims)` can make a token that the app can use with `signInWithCustomToken`. For example, if you have your own server login, you verify user and then return a Firebase custom token to the app to use. This is advanced but useful for certain integrations.

- **Linking accounts automatically:**
  Suppose you want to auto-link a user’s anonymous account with their email once they sign up. You can handle that on client side, but you might also do checks on the backend (like merging data from an anon UID to the new UID by a function triggered on user create if there’s some reference connecting them).

- **Auditing and admin tasks:**

  - If you want to log every login attempt or security-sensitive action, Cloud Functions could be triggered via an HTTP call from the app (callable function) and then log to Firestore or external logging. For instance, whenever a user enables MFA, you could call a function to log that event for audit.
  - If you need to integrate with other systems on events – e.g., when a user signs up, notify your CRM or add them to a mailing list – Cloud Functions is the place to do it (Auth onCreate triggers or Firestore triggers if you log something there).

- **Periodic cleanup/maintenance:**
  Use Cloud Functions scheduled (cron) to do tasks like disabling or deleting inactive accounts (Firebase Auth has built-in user retention, but you might have your own criteria). The Admin SDK can list users, and you could remove those who haven’t logged in for X months (be careful with that approach though – always better to just disable rather than delete, or inform the user via email first).

- **Security with Cloud Functions:**
  One advantage: moving certain logic to backend can keep secrets out of client. For example, sending email via a third-party API might require an API key – do that in CF so the key isn’t in the app. Or verifying something like an invitation code: the app calls a CF with the code, CF checks a database and returns success or failure, preventing tampering on the client.

- **Firebase Extensions:**
  Firebase offers Extensions, which are pre-built Cloud Functions for common use cases, e.g., “Authenticate with Phone Number using SMS” (an alternative to standard phone auth), or “Send Welcome Email” extension, etc. Using an Extension can save coding. There’s one for sending email via SendGrid when triggered by Firestore or Auth events ([Firebase Authentication triggers - Cloud Functions](https://firebase.google.com/docs/functions/auth-events#:~:text=For%20example%2C%20you%20could%20send,a%20sample%20that%20does)) ([Sending emails using Firestore and Firebase Extensions - Invertase](https://invertase.io/blog/send-email-extension#:~:text=Sending%20emails%20using%20Firestore%20and,trigger%20along%20with%20Send)). Consider those if they fit your needs (they are basically Cloud Functions under the hood, but easier to install/configure).

To summarize, Cloud Functions let you react to user lifecycle events on the backend seamlessly. The _Firebase docs highlight that with custom backend code you can implement automated tasks like sending welcome emails or cleaning up after account deletion_ ([Firebase Authentication triggers - Cloud Functions](https://firebase.google.com/docs/functions/auth-events#:~:text=For%20example%2C%20you%20could%20send,a%20sample%20that%20does)) ([How to use Firebase Cloud Functions to trigger an event on user sign-up? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-use-firebase-cloud-functions-to-trigger-an-event-on-user-sign-up#:~:text=Firebase%20Cloud%20Functions%20let%20developers,whenever%20a%20user%20signs%20up)). This adds polish to your app:

- Users get a nice welcome message (increasing engagement),
- Your database stays clean,
- You can implement advanced flows like role assignment or integration with external services in a secure way.

---

That concludes the guide. We have covered project setup, implementing various auth methods, managing users and roles, enforcing security, managing state and performance, testing thoroughly, deploying via CI/CD, and leveraging advanced features like offline mode, analytics, and cloud functions.

By following these steps and best practices, you can develop a robust, secure React Native application with Firebase Authentication and provide a smooth experience for your users. Happy coding!

**Sources:**

- React Native Firebase docs – installation and setup ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=certificate%20fingerprints%27%20on%20your%20app,in%20Firebase%20console)) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=%2F%2F%20NOTE%3A%20if%20you%20are,%2F%5C%20%7D)) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=Lastly%2C%20execute%20the%20plugin%20by,file)) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=Download%20the%20%60GoogleService)) ([React Native Firebase | React Native Firebase](https://rnfirebase.io/#:~:text=Within%20your%20existing%20,the%20top%20of%20the%20method))
- RNFirebase Auth social login examples (Google, Facebook, Apple) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=async%20function%20onGoogleButtonPress%28%29%20,signIn)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Google%20credential,idToken)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Once%20signed%20in%2C%20get,getCurrentAccessToken)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Firebase%20credential,accessToken)) ([Social Authentication | React Native Firebase](https://rnfirebase.io/auth/social-auth#:~:text=%2F%2F%20Create%20a%20Firebase%20credential,credential%28identityToken%2C%20nonce))
- Firebase multi-factor auth documentation (RNFirebase) ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20session%20%3D%20await%20multiFactorUser,phoneNumber%2C%20session%2C)) ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20cred%20%3D%20auth,display%20name%20for%20the%20user)) ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=auth%28%29%20,setVerificationId%28verificationId)) ([Multi-factor Auth | React Native Firebase](https://rnfirebase.io/auth/multi-factor-auth#:~:text=const%20credential%20%3D%20auth))
- StackOverflow – Firebase doesn’t support biometrics directly; suggestion to store credentials and use device biometrics ([flutter - Can The App Include Biometric Login With Firebase? - Stack Overflow](https://stackoverflow.com/questions/64058218/can-the-app-include-biometric-login-with-firebase#:~:text=Firebase%20Authentication%20does%20not%20directly,not%20deal%20directly%20with%20those)) ([flutter - Can The App Include Biometric Login With Firebase? - Stack Overflow](https://stackoverflow.com/questions/64058218/can-the-app-include-biometric-login-with-firebase#:~:text=Assuming%20you%20are%20using%20Firebase,with%20email%20and%20password%20method))
- Firebase custom claims documentation (roles) ([Control Access with Custom Claims and Security Rules - Firebase](https://firebase.google.com/docs/auth/admin/custom-claims#:~:text=Firebase%20firebase,implement%20various%20access%20control%20strategies)) ([Introduction to the Admin Auth API - Identity Platform - Google Cloud](https://cloud.google.com/identity-platform/docs/concepts-admin-auth-api#:~:text=Cloud%20cloud,roles%29))
- RNFirebase user methods (updateEmail, updateProfile, etc.) ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=)) ([User | React Native Firebase](https://rnfirebase.io/reference/auth/user#:~:text=))
- RNFirebase auth methods (sendPasswordResetEmail, etc.) ([auth | React Native Firebase](https://rnfirebase.io/reference/auth#:~:text=))
- Firestore Security Rules patterns ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=The%20following%20Firestore%20rule%20example,your%20database%20contains%20a%20uid)) ([Firestore Rules Examples – Must-Know Patterns To Secure Your Data
- DEV Community](https://dev.to/jamalmoir/firestore-rules-examples-must-know-patterns-to-secure-your-data-bm1#:~:text=rules_version%20%3D%20%272%27%3B%20service%20cloud,))
- BAM Tech – managing env variables in RN (don’t commit secrets, use libraries) ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=One%20approach%20is%20to%20hardcode,this%20method%20has%20significant%20drawbacks)) ([Managing environment variables securely in React Native](https://www.bam.tech/article/managing-environment-variables-securely-in-react-native#:~:text=environment%20variables%20to%20inject%20your,included%20in%20your%20final%20artifact))
- RNFirebase Auth state persistence explanation ([Authentication | React Native Firebase](https://rnfirebase.io/auth/usage#:~:text=On%20web%20based%20applications%2C%20the,between%20app%20sessions%20is%20persisted))
- Reddit – caching user data in state reduces Firestore reads ([Does every user authenticated data count as a read from the ...](https://community.flutterflow.io/ask-the-community/post/does-every-user-authenticated-data-count-as-a-read-from-the-firestore-0qbqG2H9s5e0Qg1#:~:text=Does%20every%20user%20authenticated%20data,Firestore%20each%20time%20you))
- Medium – CI/CD with Firebase App Distribution (setup overview) ([Setting Up CI/CD for React Native with GitHub Actions and Firebase ...](https://tudotechnologies.medium.com/setting-up-ci-cd-for-react-native-with-github-actions-and-firebase-app-distribution-86aa416e4beb#:~:text=Setting%20Up%20CI%2FCD%20for%20React,Actions%20and%20Firebase%20App%20Distribution))
- Pleo Blog – automating RN apps to Firebase and TestFlight with Fastlane & CI ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=In%20this%20article%2C%20you%20will,and%20how%20to%20configure%20circleCi)) ([How to properly automate React Native applications with Fastlane?](https://pleodigital.com/en/blog/react-native-continuous-integration#:~:text=There%20are%20several%20solutions%20to,fixes%2C%20and%20sample%20configuration%20files))
- Firebase blog – using Cloud Functions on Auth triggers (welcome emails, etc.) ([How to use Firebase Cloud Functions to trigger an event on user sign-up? | Bootstrapped Firebase Guides](https://bootstrapped.app/guide/how-to-use-firebase-cloud-functions-to-trigger-an-event-on-user-sign-up#:~:text=Firebase%20Cloud%20Functions%20let%20developers,whenever%20a%20user%20signs%20up))
- Firebase docs – Cloud Firestore offline support ([Cloud Firestore | React Native Firebase](https://rnfirebase.io/firestore/usage#:~:text=Firestore%20provides%20out%20of%20the,server%20when%20they%20regain%20connectivity)).
