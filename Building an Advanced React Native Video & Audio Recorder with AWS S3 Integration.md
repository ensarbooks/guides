# Building an Advanced React Native Video & Audio Recorder with AWS S3 Integration

This guide provides a comprehensive, step-by-step walkthrough for advanced developers to build a React Native application that **records video and audio** and **uploads them to AWS S3**. We will cover project setup, implementing recording features, managing files, integrating with AWS S3 (including secure uploads with progress tracking), performance optimizations, testing, deployment, and security best practices. The guide is structured with clear sections and sub-sections, including code snippets, best practices, and references to documentation for further details.

**Table of Contents:**

1. [Project Setup](#project-setup)
   - [Installing React Native CLI or Expo](#installing-react-native-cli-or-expo)
   - [Configuring Dependencies and Project Structure](#configuring-dependencies-and-project-structure)
   - [Setting up TypeScript](#setting-up-typescript)
2. [Audio & Video Recording](#audio-video-recording)
   - [Handling Permissions (iOS & Android)](#handling-permissions-ios--android)
   - [Video Recording with **react-native-camera**](#video-recording-with-react-native-camera)
   - [Audio Recording with **react-native-audio-recorder-player**](#audio-recording-with-react-native-audio-recorder-player)
   - [Configuring Recording Settings](#configuring-recording-settings)
   - [Building the Recording UI](#building-the-recording-ui)
3. [File Storage & Management](#file-storage--management)
   - [Saving Recordings Locally](#saving-recordings-locally)
   - [Displaying Recorded Files in the App](#displaying-recorded-files-in-the-app)
   - [Handling Large Media Files Efficiently](#handling-large-media-files-efficiently)
4. [AWS S3 Integration](#aws-s3-integration)
   - [Setting Up AWS S3 Bucket and IAM Roles](#setting-up-aws-s3-bucket-and-iam-roles)
   - [Installing & Configuring AWS SDK (Amplify) for React Native](#installing--configuring-aws-sdk-amplify-for-react-native)
   - [Securely Handling API Keys & Authentication](#securely-handling-api-keys--authentication)
   - [Implementing File Uploads with Progress](#implementing-file-uploads-with-progress)
   - [Error Handling and Retry Logic](#error-handling-and-retry-logic)
5. [Enhancements & Optimizations](#enhancements--optimizations)
   - [Media File Compression Before Upload](#media-file-compression-before-upload)
   - [Background Uploads](#background-uploads)
   - [Encrypting Files for Security](#encrypting-files-for-security)
   - [Optimizing App Performance](#optimizing-app-performance)
6. [Deployment & Testing](#deployment--testing)
   - [Debugging and Logging Best Practices](#debugging-and-logging-best-practices)
   - [Running Tests (Unit, Integration, UI)](#running-tests-unit-integration-ui)
   - [Deploying to App Store and Google Play](#deploying-to-app-store-and-google-play)
7. [Security Best Practices](#security-best-practices)
   - [Protecting S3 Uploads & Preventing Unauthorized Access](#protecting-s3-uploads--preventing-unauthorized-access)
   - [Securing API Endpoints and Authentication](#securing-api-endpoints-and-authentication)
   - [Data Privacy Considerations](#data-privacy-considerations)

---

## Project Setup

Before diving into coding, we need to set up our React Native project and ensure all required tools and libraries are installed. This section covers choosing between React Native CLI and Expo, structuring the project, managing dependencies, and configuring TypeScript for type-safe development.

### Installing React Native CLI or Expo

**Choosing a Development Environment:** React Native offers two main ways to start a project:

- **React Native CLI (Bare Workflow):** Gives full control over native iOS/Android projects. Best for advanced use cases where you need custom native modules (like the camera and audio libraries we’ll use) or want to integrate closely with native code.
- **Expo (Managed Workflow):** Eases setup by abstracting native configurations and comes with many features out-of-the-box. However, using custom native modules not supported by Expo can be tricky (Expo has its own camera/audio modules, but here we specifically want `react-native-camera` and other libraries which might require the bare workflow or an EAS development build).

For this guide, we will use the **React Native CLI** approach to have maximum control and to easily integrate the third-party native modules. (It’s possible to use Expo with custom development builds, but that adds complexity; advanced developers can adapt these steps to Expo if desired.)

**Prerequisites:** Ensure you have Node.js and a package manager (npm or Yarn) installed. For React Native CLI, you also need to install Android Studio (for Android SDK/emulator) and Xcode (for iOS, on macOS). Detailed environment setup is available in the official React Native docs. Make sure you have the **React Native CLI** (`npx react-native`) available or install it via `npm i -g react-native-cli` if needed.

**Initializing the Project:** Use the React Native CLI to bootstrap a new project. You can include a TypeScript template if you plan to use TypeScript (recommended for an advanced project). For example, to create a new project named **RecorderApp** with TypeScript:

```bash
npx react-native init RecorderApp --template react-native-template-typescript
```

This will create a new directory `RecorderApp` with the standard React Native structure. If you're not using TypeScript, you can omit the template flag:

```bash
npx react-native init RecorderApp
```

<details>
<summary>Using Expo (alternative)</summary>

If you prefer Expo for quick setup, you can initialize with:

```bash
npx create-expo-app RecorderApp
```

Expo projects come pre-configured, but to use `react-native-camera` or other native libraries, you might need to eject or use Expo’s dev client. In this guide, we continue with the CLI (bare) project.

</details>

**Running the Blank App:** After installation, navigate into the project directory and run on your target platform:

```bash
cd RecorderApp
npx react-native run-android   # for Android
npx react-native run-ios       # for iOS (on macOS, with a simulator or device)
```

This should launch a basic “Hello World” app, confirming your environment is set up correctly. Keep this development server running as we add features.

### Configuring Dependencies and Project Structure

Our app will use several libraries for recording and uploading. Let’s add the necessary dependencies:

- **Camera access:** `react-native-camera` (often imported as `RNCamera`) for video recording and picture taking. This library provides a `<RNCamera>` component to access the camera and supports video capture.
- **Audio recording:** `react-native-audio-recorder-player` for recording and playing audio files. This library simplifies audio recording on both iOS and Android with a consistent API.
- **File handling:** We will use React Native’s built-in file system via the camera/audio libraries. For additional file management, we can use packages like `react-native-fs` or the modern `react-native-file-access`. We will also use `@react-native-async-storage/async-storage` for storing metadata (like file list) locally.
- **AWS S3 integration:** To communicate with AWS, we’ll use **AWS Amplify** (which includes Storage APIs for S3). Alternatively, one could use AWS SDK directly or third-party S3 upload libraries; we choose Amplify for its ease of use in React Native.
- **File compression:** `react-native-compressor` for compressing video/audio files before upload (to save bandwidth and storage).
- **Background upload:** `react-native-background-upload` to handle uploading of large files in the background (so the upload isn’t halted if the app is minimized).
- **Video playback (optional):** `react-native-video` for playing back recorded videos in the app (useful when listing recordings).
- **Additional utilities:** `@react-native-community/netinfo` (to check connectivity before upload), etc., as needed.

Install the required packages via npm or Yarn:

```bash
yarn add react-native-camera react-native-audio-recorder-player @react-native-async-storage/async-storage aws-amplify react-native-compressor react-native-background-upload react-native-video
```

_(If using npm, replace `yarn add` with `npm install --save`.)_

After installing, don’t forget to install iOS pods for native modules:

```bash
cd ios && pod install && cd ..
```

This links the native modules for iOS. On Android, autolinking (RN 0.60+) should handle the integration. The `react-native-camera` and other native modules will be linked automatically. Verify that the installation steps from each library’s documentation are followed (e.g., `react-native-camera` might require some Gradle configuration as noted in its docs).

**Project Structure:** Organize your project for clarity and scalability:

- Create a `src/` directory to hold your source code.
- Inside `src/`, organize further into modules, e.g.:
  - `components/` for presentational components (if any UI components are separate).
  - `screens/` for screen components (e.g., `RecordScreen.tsx` and `PlaybackScreen.tsx`).
  - `services/` for utility modules (e.g., `awsService.ts` for AWS upload functions).
  - `hooks/` for any custom React hooks (e.g., a hook to use the audio recorder).
  - `utils/` for helper functions (e.g., a helper to request permissions).
- Keep platform-specific code (if any) separated using `.ios.tsx` or `.android.tsx` file naming, or within `Platform` checks in code.

**Example Structure:**

```
RecorderApp/
├── android/
├── ios/
├── src/
│   ├── screens/
│   │    ├── RecordScreen.tsx
│   │    └── PlaybackScreen.tsx
│   ├── components/
│   │    └── RecordButton.tsx
│   ├── services/
│   │    └── awsService.ts
│   ├── hooks/
│   │    └── useAudioRecorder.ts
│   └── utils/
│        └── permissions.ts
├── App.tsx
└── ... (config files, etc.)
```

This is just one way to structure; adjust as needed for your preferences. The key is to separate concerns (UI, business logic, services) so the app remains maintainable as it grows.

### Setting up TypeScript (Optional but Recommended)

TypeScript helps catch errors early and provides better documentation through types. If you started with the TypeScript template, much is already set up:

- A `tsconfig.json` is generated with default React Native settings.
- Files are `.tsx` or `.ts` instead of `.js`.

If you started with a JavaScript template and want to add TypeScript:

1. **Add TypeScript Dependencies:** Install TypeScript and type definitions:
   ```bash
   yarn add -D typescript @types/react @types/react-native
   ```
2. **Add a tsconfig:** Create a `tsconfig.json` in the project root with appropriate settings. For RN, a typical tsconfig includes `"jsx": "react-native"`, and allows JSX in `.tsx` files.
3. **Rename files:** Change your entry file (`App.js`) to `App.tsx`. Rename other JS files in `src` to `.tsx` or `.ts` as appropriate. Update any imports accordingly.
4. **Run the app:** The Metro bundler should pick up the new configuration. If you run into any type errors, fix them or adjust the tsconfig.

TypeScript will help especially when using AWS Amplify and other libraries by providing IntelliSense for methods and catching wrong usage.

**Note:** All code snippets in this guide will be given in TypeScript/JSX for clarity.

Now that the project is set up and our tools are in place, let's move on to implementing audio and video recording features.

---

## Audio & Video Recording

Recording audio and video are core features of our app. We will use **`react-native-camera`** (RNCamera) for video recording, and **`react-native-audio-recorder-player`** for audio recording. In this section, we’ll cover how to request the necessary permissions, configure the recorder settings (quality, format, etc.), and build a simple UI to start/stop recordings and save the output.

### Handling Permissions (iOS & Android)

Accessing the device camera and microphone requires explicit user permission on both Android and iOS.

- **iOS Permissions:** You must add usage descriptions to the app’s **Info.plist** file for any privacy-sensitive resource. Open `ios/RecorderApp/Info.plist` and add:

  ```xml
  <key>NSCameraUsageDescription</key>
  <string>This app requires access to the camera to record videos.</string>
  <key>NSMicrophoneUsageDescription</key>
  <string>This app requires access to the microphone to record audio.</string>
  ```

  If these keys are missing, iOS will crash the app when you attempt to access the camera or microphone, with an error stating the Info.plist must contain those keys ([Xcode: Missing Info.plist key for NSCameraUsageDescription](https://stackoverflow.com/questions/44690075/xcode-missing-info-plist-key-for-nscamerausagedescription#:~:text=NSCameraUsageDescription%20stackoverflow,the%20app%20uses%20this%20data)). Ensure the description string explains why you need the permission, as this is shown to the user.

- **Android Permissions:** In `android/app/src/main/AndroidManifest.xml`, include:

  ```xml
  <uses-permission android:name="android.permission.CAMERA" />
  <uses-permission android:name="android.permission.RECORD_AUDIO" />
  <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
  ```

  (The storage permission is needed if you plan to save video files to external storage or share to gallery. If you only use app-internal storage, you might not need WRITE_EXTERNAL_STORAGE on newer Android versions, but it's common to include for media apps.)

  At runtime, **Android API 23+ (Marshmallow and above)** also requires prompting the user for these permissions. The `react-native-camera` library can automatically prompt for camera/audio permission on Android if configured via its props (we'll see this next). Alternatively, you can use `PermissionsAndroid` API or a library like `react-native-permissions` to request permissions in JavaScript. For simplicity, we'll use RNCamera's built-in prompts for camera and microphone.

- **App Launch Checks:** It’s a good practice to check and request permissions before attempting to record. This can be done on component mount: e.g., using the `PermissionsAndroid.request()` for Android, and for iOS, the first access triggers the system prompt based on Info.plist entries. You might also handle the case where a user previously denied permission and needs to be guided to enable it from settings.

**Example (Android runtime permission request for microphone):**

```ts
import { PermissionsAndroid, Platform } from "react-native";

async function requestAudioPermission() {
  if (Platform.OS === "android") {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
      {
        title: "Microphone Permission",
        message: "This app needs access to your microphone to record audio.",
        buttonPositive: "OK",
      }
    );
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  }
  return true; // iOS automatically handles via Info.plist prompt
}
```

We will integrate permission checks in our recording components next.

### Video Recording with **react-native-camera**

The **`react-native-camera`** library (RNCamera) provides a `<RNCamera>` component that displays a camera preview and methods to capture photos or videos. First, integrate the camera view into our app’s UI, then implement recording logic.

**Installation Note:** By now you should have installed `react-native-camera` and run pod install. If using RN <0.60, manual linking would be required, but for modern versions, autolinking suffices. Ensure you have added the required permissions as above.

**Camera Preview Component:** Create a screen (e.g., `RecordScreen.tsx`) that will contain the camera preview and controls:

```tsx
// src/screens/RecordScreen.tsx
import React, { useRef, useState } from "react";
import { View, TouchableOpacity, Text, StyleSheet } from "react-native";
import { RNCamera } from "react-native-camera";

const RecordScreen: React.FC = () => {
  const cameraRef = useRef<RNCamera>(null);
  const [isRecording, setIsRecording] = useState(false);

  const startVideoRecording = async () => {
    if (cameraRef.current && !isRecording) {
      try {
        setIsRecording(true);
        // Start recording with optional settings
        const promise = cameraRef.current.recordAsync({
          quality: RNCamera.Constants.VideoQuality["720p"], // or "480p", "1080p", etc.
          maxDuration: 60, // limit to 60 seconds for example
          mute: false, // include audio
          // You can add other options like videoBitrate, codec for iOS, etc.
        });
        if (promise) {
          const data = await promise; // Wait for stopRecording to be called
          console.log("Video recorded at: ", data.uri);
          // data.uri is the file path of the recorded video in cache
          // You might want to save this URI to state or AsyncStorage for later use
        }
      } catch (e) {
        console.error("Video recording error:", e);
      } finally {
        setIsRecording(false);
      }
    }
  };

  const stopVideoRecording = () => {
    if (cameraRef.current && isRecording) {
      cameraRef.current.stopRecording();
      // This will trigger the promise above to resolve with the video data
    }
  };

  return (
    <View style={styles.container}>
      <RNCamera
        ref={cameraRef}
        style={styles.preview}
        type={RNCamera.Constants.Type.back} // use rear camera
        flashMode={RNCamera.Constants.FlashMode.auto}
        captureAudio={true} // enable audio recording with video
        androidCameraPermissionOptions={{
          title: "Camera Permission",
          message: "We need permission to use your camera",
          buttonPositive: "OK",
          buttonNegative: "Cancel",
        }}
        androidRecordAudioPermissionOptions={{
          title: "Audio Permission",
          message: "We need permission to use your microphone",
          buttonPositive: "OK",
          buttonNegative: "Cancel",
        }}
      />
      <View style={styles.controls}>
        {isRecording ? (
          <TouchableOpacity onPress={stopVideoRecording} style={styles.button}>
            <Text style={styles.buttonText}>Stop Recording</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity onPress={startVideoRecording} style={styles.button}>
            <Text style={styles.buttonText}>Record Video</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  preview: { flex: 1 },
  controls: {
    position: "absolute",
    bottom: 20,
    alignSelf: "center",
  },
  button: {
    backgroundColor: isRecording ? "red" : "blue", // pseudo-code: change style if recording
    padding: 15,
    borderRadius: 5,
  },
  buttonText: { color: "#fff", fontSize: 16 },
});

export default RecordScreen;
```

In this code:

- We use a functional component with `useRef` to hold the camera reference (so we can call `recordAsync()` and `stopRecording()` on it).
- The UI shows the camera preview full-screen, and a button below it that toggles between “Record” and “Stop”.
- When “Record” is pressed, we call `recordAsync()` on the camera ref. We pass some **RecordOptions** such as quality and maxDuration. The `recordAsync` returns a Promise that resolves when recording stops (either via reaching maxDuration or when we call `stopRecording()`). We await that promise to get the `data` which includes the `uri` of the recorded video file ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=takeVideo%20%3D%20async%20%28%29%20%3D,recordOptions)).
- We log the file path (`data.uri`). The video is saved in the app’s cache directory by default ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=interface%20RecordResponse%20%7B%20%2F,codec%3A%20VideoCodec%5Bkeyof%20VideoCodec)). You might move it or upload it directly from that path.
- We handle errors in recording with try/catch and ensure the `isRecording` state is updated accordingly.
- We provided `androidCameraPermissionOptions` and `androidRecordAudioPermissionOptions` to let RNCamera auto-handle the permission prompt on Android. (On iOS, the Info.plist entries we added will trigger the system prompt when needed.)

**Recording Implementation Notes:**

- The camera `type` is set to back camera; you could allow switching to front camera if desired (using `RNCamera.Constants.Type.front`).
- `captureAudio:true` ensures audio is captured with video. If you only wanted silent video, set it to false.
- The `quality` option uses a preset (e.g., "720p"). RNCamera supports various resolutions or even a specific width/height. Using a preset ensures it's device-appropriate.
- We set a `maxDuration` to auto-stop after 60 seconds as a safety (you can remove this or adjust as needed).
- On iOS, you could specify `codec` in options if you want a specific video codec (e.g., H264 vs HEVC), but using the default is fine.
- When `stopRecording()` is called, it **fulfills the promise** from `recordAsync` ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=stopRecording)), allowing us to proceed with the video file.

RNCamera also provides events like `onRecordingStart` or `onRecordingEnd` if needed, but the above approach is straightforward.

**After recording** a video, we now have a video file (likely in a path like `file:///data/.../Caches/Camera/...mp4` on device). We should save the URI for later use (to upload or display). We will discuss storing and managing these files in the next section.

### Audio Recording with **react-native-audio-recorder-player**

For audio, we will use the **`react-native-audio-recorder-player`** library. This library allows recording audio (usually to an M4A or MP3 file) and playing it back. Unlike video (which we did with a UI preview), audio recording doesn’t need a preview UI – we typically just show a timer or levels and a record/stop button.

**Setting up the Audio Recorder:** We will integrate audio recording in perhaps the same screen or a separate screen/component. For clarity, let's assume a separate AudioRecorder component or maybe extend our RecordScreen to handle both modes (video/audio). Here, we'll outline just the audio part in isolation:

```tsx
// Inside RecordScreen or a separate AudioRecordScreen component
import AudioRecorderPlayer from "react-native-audio-recorder-player";

// ... within a component:
const audioRecorderPlayer = useRef(new AudioRecorderPlayer()).current;
const [isRecordingAudio, setIsRecordingAudio] = useState(false);
const [recordTime, setRecordTime] = useState("00:00");
const [audioRecordFile, setAudioRecordFile] = useState<string | null>(null);

const startAudioRecording = async () => {
  try {
    const audioPath = Platform.select({
      ios: "audio_record.m4a", // iOS will save in Documents by default
      android: undefined, // Android will save in Cache by default if undefined
    });
    const result = await audioRecorderPlayer.startRecorder(audioPath);
    // Optionally, listen to progress. The library provides a callback for recording progress:
    audioRecorderPlayer.addRecordBackListener((e) => {
      const currentTime = audioRecorderPlayer.mmssss(
        Math.floor(e.currentPosition)
      );
      setRecordTime(currentTime);
      return;
    });
    setIsRecordingAudio(true);
    console.log("Recording audio at path: ", result);
    // `result` is the path of audio file, e.g., file:///.../audio_record.m4a
  } catch (error) {
    console.error("Audio recording error", error);
  }
};

const stopAudioRecording = async () => {
  try {
    const result = await audioRecorderPlayer.stopRecorder();
    audioRecorderPlayer.removeRecordBackListener();
    setIsRecordingAudio(false);
    setRecordTime("00:00");
    setAudioRecordFile(result);
    console.log("Audio recorded and stored at: ", result);
  } catch (error) {
    console.error("Stop record error", error);
  }
};
```

And the UI for this might be a button similar to video:

```jsx
{
  isRecordingAudio ? (
    <TouchableOpacity onPress={stopAudioRecording} style={styles.button}>
      <Text style={styles.buttonText}>Stop Audio</Text>
    </TouchableOpacity>
  ) : (
    <TouchableOpacity onPress={startAudioRecording} style={styles.button}>
      <Text style={styles.buttonText}>Record Audio</Text>
    </TouchableOpacity>
  );
}
<Text>{recordTime}</Text>;
```

In the above code:

- We create an `AudioRecorderPlayer` instance. We use `useRef(...).current` to avoid re-creating it on every render.
- On `startRecorder`, we optionally pass a file path. If no path is given on Android, it records to a default path (likely in cache or files directory, often an `.mp3` file in cache). On iOS, if no path, it might default to a temp, so sometimes specifying ensures consistency. We choose `.m4a` for iOS (common AAC format) and let Android default (which uses `.mp3` in cache).
- `startRecorder` returns the file path of the recording file (we log it). We also set up a listener with `addRecordBackListener` which provides updates on the recording state. We use it to update a timer display (`recordTime`) every few milliseconds. The library provides a helper `mmssss` to format milliseconds to mm:ss.
- After calling `startRecorder`, the user is recording. We set `isRecordingAudio=true` to update the UI.
- On `stopRecorder`, the promise resolves with the path of the file saved. We remove the listener, reset state, and save the `result` (file path) in `audioRecordFile` for later use (like to play or upload).
- The recorded audio file will typically be in the app’s cache (on Android, something like `/CacheDir/Audio/xxxxx.mp3`) or in Documents (on iOS, if we named it `audio_record.m4a`, it likely saved in Documents by default with that name, or in cache if not).
- **Permissions:** The microphone permission we handled earlier covers audio. On Android, ensure RECORD_AUDIO was granted. On iOS, the first call to startRecorder will trigger the system permission prompt if not already granted.

**Audio Recording Implementation Notes:**

- `react-native-audio-recorder-player` handles the low-level native recording. It uses AVAudioRecorder on iOS and MediaRecorder on Android internally. The default output is `.m4a` (AAC) on iOS and `.mp3` on Android. You can also supply a custom path with extension to influence this (as we did for iOS).
- We could configure audio bitrate or channels by using a custom path with specific encoding, but the library doesn’t expose a lot of custom settings directly (it's meant to be simple). For most cases, default quality is fine (it typically uses 44100 Hz, stereo).
- We show a basic timer UI. You could also show audio amplitude (the library provides `e.currentMetering` in the callback if enabled).
- If needed, we can allow recording multiple audio snippets and storing each file path.

At this point, we have the ability to record video and audio files. Next, let's address storing these files and listing them, before we move to uploading.

### Configuring Recording Settings

**Video Settings:** We briefly touched on some options for `RNCamera.recordAsync`:

- `quality`: sets the resolution/quality of the video. Possible values include `"480p"`, `"720p"`, `"1080p"`, `"4:3"` etc, as defined in `RNCamera.Constants.VideoQuality`. Use presets for simplicity; they map to device-supported resolutions.
- `videoBitrate`: an optional number specifying video bit rate in bits per second. Higher bitrates improve quality at the cost of larger file size. If not set, the camera will choose a reasonable default. For example, you might set `videoBitrate: 5 * 1000 * 1000` (5 Mbps) for 1080p video.
- `maxDuration` / `maxFileSize`: to limit recordings. We used `maxDuration`. `maxFileSize` (in bytes) can ensure the file doesn’t exceed a certain size.
- `mute`: if true, records video without sound.
- `orientation`: you can lock orientation of the recorded video (but usually you let it follow device orientation).
- `codec` (iOS only): specify the codec (H.264, HEVC, JPEG etc). For instance, `RNCamera.Constants.VideoCodec.H264` if you want broad compatibility.

These options are documented in the RNCamera docs ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=interface%20RecordOptions%20,string%3B%20videoBitrate%3F%3A%20number%3B%20fps%3F%3A%20number)). Choosing the right settings is a balance between quality and file size. For our purposes, 720p with default bitrate is a good default that balances clarity with not being too heavy.

**Audio Settings:** `react-native-audio-recorder-player` doesn’t expose many settings directly. The default sample rate is typically 44100 Hz and bit rate around 128kbps for MP3 on Android, and M4A on iOS (which uses AAC). If higher quality is needed, one might have to use a different library or native module. However, for voice recordings or even music, the default is usually sufficient. If needed, you could record raw PCM with another library, but that’s beyond our scope.

One setting we _can_ control is the output format via the file extension. For example, using `.wav` extension on iOS might yield a WAV file (large size but lossless), while `.m4a` gives a compressed AAC. We will stick to `.m4a/.mp3`.

**Storage Paths:** For both video and audio, you can specify the storage path:

- By default, RNCamera saves videos in the app cache directory (`Caches/Camera` on iOS, cache on Android). This is fine for temporary storage. We can move it if we want it persistent or accessible outside the app (like gallery).
- The audio recorder, by default, on Android writes to something like: `<App Cache>/sound.mp3` (with a random file name). On iOS, if we provide a simple name like `hello.m4a`, it actually saves in `Documents` (the library code appends `file://` and uses `DocumentDirectoryPath` on iOS). We provided `'audio_record.m4a'` for iOS, which the library will interpret correctly as a file in Documents (since it adds `file://` and uses RNFS).

You can always move files after recording to a desired location. For example, using `react-native-fs` to move from cache to document directory or to an external storage (Android). But be mindful of storage permissions if moving to external on Android (scoped storage rules on Android 10+ require using MediaStore API or similar for gallery access).

**Summary of Best Practices for Recording Settings:**

- Use a reasonable quality to avoid huge files. For example, 720p video for most cases, unless high definition is needed.
- Set limits (`maxDuration` or manual UI control) to prevent extremely long recordings which could produce very large files.
- Inform users of remaining time or file size if possible (advanced: you could estimate file size as recording progresses by bit rate \* time).
- Monitor recording status via callbacks to update UI (like we did with audio timer, and you could do with video too, though RNCamera doesn't give a time callback, you'd use a timer in JS if needed).
- Test on multiple devices; older devices may handle high resolution poorly or have different performance.

### Building the Recording UI

We partially built the UI in the above code snippets: a simple interface with a preview (for video) and buttons to control recording. Let’s consider the overall UI/UX and how to integrate both audio and video recording features in the app:

One approach is to have a **tabbed interface or segmented control**: one for video recording, one for audio recording. For example:

- **RecordScreen** could contain two tabs: "Video" and "Audio". In "Video" tab, show the camera preview and video record controls. In "Audio" tab, show an interface to record audio (perhaps just a big microphone icon button and a timer).
- Alternatively, have separate screens: VideoRecordScreen and AudioRecordScreen, and a simple menu to navigate between them.

For simplicity, let's assume a single screen with a toggle:

```jsx
<View style={styles.modeToggle}>
  <Button
    title="Video Mode"
    onPress={() => setMode("video")}
    disabled={mode === "video"}
  />
  <Button
    title="Audio Mode"
    onPress={() => setMode("audio")}
    disabled={mode === "audio"}
  />
</View>;
{
  mode === "video" ? <VideoRecorderView /> : <AudioRecorderView />;
}
```

Where `<VideoRecorderView>` is essentially the JSX we wrote using `<RNCamera>` and `<AudioRecorderView>` is the JSX for audio recording.

**Design considerations:**

- **Video UI:** In our example, the video preview takes up the full screen. The record/stop button is overlaid. We might want to show a recording timer on the UI when recording (e.g., a red blinking dot with elapsed time). We can implement that by starting a timer when video recording starts (just a JS interval that updates a state counter every second).
- **Audio UI:** We only have the microphone icon or button and a timer. We could also visualize audio levels (VU meter) if desired, but that requires additional work (the library provides `currentMetering` which could be used to draw a simple bar or so).
- **Buttons and Icons:** For a polished app, use icons (like a record icon, stop icon). You can use `react-native-vector-icons` or any icon library to show a circle for record, square for stop, etc.
- **User feedback:** When recording starts, give clear indication (change button color to red, show “Recording...” text, maybe disable switching mode until they stop, etc.) When stopped, confirm that it saved (maybe briefly show a toast or so "Saved to library" if you implement saving to gallery or just "Recording saved").

- **Permissions UX:** The first time the user hits record, the app will prompt for permissions. Ensure the UI is ready to handle the user possibly denying permission (e.g., the camera view might not show if no permission). RNCamera has a prop `permissionDialogTitle` and `permissionDialogMessage` for iOS as well (older versions) but those might not be needed if Info.plist is set. You can handle the case `RNCamera.Constants.CameraStatus` to see if authorized, and display a message or request if not.

Now we have a functional UI and the ability to record audio and video. The next step is to deal with the recorded files: storing them, listing them, and preparing for upload.

---

## File Storage & Management

After recording, our app will produce media files (video and audio). We need to decide how to store these files locally and how to manage potentially large files. This section covers saving recordings, listing them in the UI, and best practices for handling large media on a mobile device.

### Saving Recordings Locally

When a recording is finished, we typically obtain the file path of the saved media:

- For video (RNCamera): `data.uri` (e.g., `"file:///data/user/0/com.recorderapp/cache/Camera/12345.mp4"` on Android or similar on iOS).
- For audio (AudioRecorderPlayer): `result` from `stopRecorder()` (e.g., `"file:///storage/emulated/0/Android/data/com.recorderapp/cache/12345.mp3"` on Android, or a path in Documents on iOS).

By default, these are in the app’s sandbox (not visible to user’s gallery). That’s fine for our use (we will upload them to S3, not necessarily save to public gallery). If you **do** want them accessible in gallery or by other apps, you would have to move them to a public directory and use platform APIs to add to media library (beyond our scope).

For managing these files within the app:

- **Save metadata:** You can keep an in-memory list (state) of recorded items during a session. But if you want the list to persist across app launches, you should save references (like file names, paths, durations, type) to persistent storage. **AsyncStorage** is a good option for storing a list of file records (as a JSON string, for example).
- **Do not store large file binary in AsyncStorage.** AsyncStorage is meant for small data (a few MB at most). On Android it has a default limit (~6MB per app) ([Increase Android AsyncStorage Size in React Native - Code Daily](https://www.codedaily.io/tutorials/Increase-Android-AsyncStorage-Size-in-React-Native#:~:text=The%20iOS%20AsyncStorage%20implementation%20has,size%20of%20AsyncStorage%20is%206MB)). So we will only store the URI or path (string) in AsyncStorage, not the file content.
- **Use a file system library if needed:** React Native’s built-in `CameraRoll` (for images/videos to photos app) or `react-native-fs` can help move or copy files if needed. We might not need to move files unless we want a custom location.

**Example: Storing and retrieving file list in AsyncStorage:**

Let's say we maintain a list of recordings in AsyncStorage under a key `'recordingsList'`. Each item could be an object like `{ type: 'video'|'audio', uri: string, date: number, duration: number }`.

```ts
import AsyncStorage from "@react-native-async-storage/async-storage";

const saveRecordingInfo = async (newItem) => {
  try {
    const jsonValue = await AsyncStorage.getItem("recordingsList");
    const list = jsonValue ? JSON.parse(jsonValue) : [];
    list.push(newItem);
    await AsyncStorage.setItem("recordingsList", JSON.stringify(list));
  } catch (e) {
    console.error("Failed to save recording info", e);
  }
};
```

We would call `saveRecordingInfo` after stopping a recording. For example, after stopping video:

```js
await saveRecordingInfo({
  type: "video",
  uri: data.uri,
  date: Date.now(),
  duration: actualDuration,
});
```

The `duration` we might have to measure manually (RNCamera doesn’t return duration, but we know maxDuration or we can track with a timer). For audio, the library can provide duration in the stop callback if we track `recordSecs`.

**Loading the list on app start:** in a component (like in a useEffect of a list screen), do:

```js
const loadRecordings = async () => {
  const jsonValue = await AsyncStorage.getItem("recordingsList");
  const list = jsonValue ? JSON.parse(jsonValue) : [];
  setRecordingsList(list);
};
```

This way, users can see their past recordings even after restarting the app (as long as the actual files still exist at the stored path).

**Managing File Lifecycle:** Consider when to delete local files:

- If your app uploads the file to S3, you might want to remove it from local storage to free space (especially videos which can be large). However, deleting immediately after upload might be risky if the user expects to re-play it in the app or if upload needs verification.
- A strategy: mark an item as "uploaded" in your metadata, and offer a way to delete it from the device if space is needed or after confirmation. Or automatically purge old recordings after some time if already uploaded.
- Ensure you have permission to delete (within your app sandbox you do). Use a library like `react-native-fs` to unlink files.

For now, we'll keep all files and let the user manage (or just accumulate). But be mindful that many video files can eat up storage quickly. Monitoring total storage used by recordings and alerting the user might be a good enhancement.

### Displaying Recorded Files in the App

To enhance user experience, the app should list the recorded files and allow playback:

- For each video recording, show a thumbnail or at least the filename or timestamp. You can generate thumbnails from video using `react-native-create-thumbnail` or `react-native-compressor`'s utility to create a thumbnail, or simply show an icon with the date.
- For audio recordings, list with an icon and name/time.

**UI Implementation:** Create a component or screen (e.g., `PlaybackScreen` or integrate in Record screen a scrollable list below controls):

```tsx
// Example snippet for listing recordings (could be in a separate screen)
import { FlatList, Image } from "react-native";
// ... inside a component:
<FlatList
  data={recordingsList}
  keyExtractor={(item, index) => index.toString()}
  renderItem={({ item }) => (
    <View style={styles.listItem}>
      {item.type === "video" ? (
        <Image source={{ uri: item.uri }} style={styles.thumbnail} /> // this might not directly show thumbnail, might need to use a lib
      ) : (
        <Image
          source={require("../assets/audio_icon.png")}
          style={styles.thumbnail}
        />
      )}
      <Text>
        {item.type.toUpperCase()} - {new Date(item.date).toLocaleString()}
      </Text>
      {/* Maybe a play button */}
      <Button title="Play" onPress={() => playItem(item)} />
      {/* If not uploaded yet, show upload button or status */}
      {!item.uploaded && (
        <Button title="Upload" onPress={() => uploadItem(item)} />
      )}
    </View>
  )}
/>;
```

In the above pseudo-code:

- We use a `FlatList` to render each recording.
- If it's a video, we attempt to show an `<Image>` with `uri`. This might work if the video file is accessible as an image (some platforms might show first frame). Often, this won't display because it's not an actual image; to get a thumbnail you might need to use a library to extract one. Alternatively, use a <Video> component in paused mode as thumbnail (but that’s heavy). For simplicity, one could just use a static icon for video as well.
- A play button uses a `playItem` function:
  - For video: you can navigate to a video player screen or use `react-native-video` component to play it.
  - For audio: you can use the same `AudioRecorderPlayer` to play (it has `startPlayer(uri)` method).
- An upload button will trigger upload to S3 (we will implement the upload logic in the AWS section). The `item.uploaded` flag (which we'd add in metadata once uploaded) can help indicate if already uploaded.

**Playing Videos with `react-native-video`:** This library can play video given a file URI. For example:

```jsx
<Video source={{ uri: item.uri }} style={styles.videoPlayer} controls={true} />
```

This would show a video player with controls (play/pause, seek) for the given video file.

**Playing Audio with AudioRecorderPlayer:** We already have the instance; we can do:

```js
await audioRecorderPlayer.startPlayer(item.uri);
audioRecorderPlayer.addPlayBackListener((e) => {
  // update UI with e.currentPosition / e.duration if needed
});
```

And a stop function similarly:

```js
audioRecorderPlayer.stopPlayer();
audioRecorderPlayer.removePlayBackListener();
```

The audio lib makes it easy to reuse for playback as well.

### Handling Large Media Files Efficiently

Recording video especially can produce large files. Even a 1-minute 720p video might be tens of MB. Here are strategies to handle them efficiently:

- **Avoid loading entire file into memory:** When uploading or playing, use streaming. For example, AWS Amplify’s Storage.put will take a Blob or file path directly, so you don’t need to read the whole file into JS memory. Similarly, `react-native-video` streams from file. Never attempt to base64 encode the file or use `require()` on it, as that would load it fully in RAM and likely crash for large videos.

- **Use caching and temp storage wisely:** The default of saving to cache is actually good because if the app cache is cleared by the OS, it frees space. However, that means if the app is killed by system and cache cleared, recordings could vanish. If that’s a concern, consider moving important files to a more permanent directory (Documents on iOS, or app’s files dir on Android). `react-native-fs` can get you paths for DocumentDirectoryPath, etc.

- **Monitor storage:** If users can record multiple videos, you may want to show how much space recordings are using and possibly restrict length or number of recordings. Since this is an advanced guide, you might integrate with device APIs to get available disk space and warn if low.

- **Consider compression:** We will discuss compression in the Enhancements section, but compressing videos can drastically reduce file size (with some quality loss), making uploads faster and using less device storage.

- **Multipart uploads:** AWS S3 has a multipart upload feature for large files. If using Amplify or the AWS SDK, they automatically use multipart for files over 5 MB, which means the file is split and uploaded in parts, reducing memory pressure and improving resilience. This happens under the hood (we'll cite this in the AWS section).

- **Threading/Background:** If the user leaves the app during an upload, by default the upload might pause (since the JS thread might be suspended). Using background upload (discussed later) can handle this. For recording, if the app goes background while recording, typically recording stops or pauses (especially video recording will stop if the app goes inactive because camera view is not active). It's tricky to record video in background (not allowed by OS for privacy). Audio can continue in background if you configure audio session properly on iOS (for voice recording category) and request background audio permission. That level of detail is beyond scope, but keep in mind limitations: video recording requires foreground; audio recording can be background if you set allowed background modes for audio.

**Summary:** Treat media files carefully: keep them either in cache (and risk them being cleared eventually) or move to safe location, and ensure you don’t unnecessarily duplicate them (to save space). Clean up files that are no longer needed (e.g., after successful upload if you decide so).

Now that we have local file management in hand, let's proceed to the core integration with AWS S3 for uploading these recordings to the cloud.

---

## AWS S3 Integration

Uploading the recorded media to the cloud allows the content to be stored persistently and accessed remotely. AWS S3 (Simple Storage Service) is a great choice for storing such files. In this section, we cover how to set up an S3 bucket and appropriate permissions, integrate AWS Amplify (or AWS SDK) into the React Native app, handle credentials securely, perform file uploads with progress monitoring, and implement error handling with retries.

### Setting Up AWS S3 Bucket and IAM Roles

**AWS Account & S3 Bucket:** Ensure you have access to an AWS account:

1. Log in to the AWS Console and go to the S3 service.
2. Create a new bucket (e.g., name it `my-recorder-uploads`). Choose a region close to your users or where your account is based (we’ll use this region in the app config).
3. For simplicity, you can keep the bucket private (no public access), as we intend to use authenticated requests to upload and (if needed) retrieve. AWS by default blocks public access on new buckets, which is good for security.
4. Note the bucket name and region.

**IAM User or Role for Access:** Our app will need credentials to upload to S3:

- One approach is to create an IAM User with programmatic access that has permission to put objects to the S3 bucket. Then embed the access key and secret in the app (not ideal security-wise, we'll address later).
- A better approach is to use AWS Amplify with Amazon Cognito Identity Pool, which can grant temporary credentials to the app. The Amplify CLI can set this up: it creates an Identity Pool and IAM roles that allow that identity to access the S3 bucket (with certain permissions). This way, you don’t embed long-term keys in the app.
- If you use Amplify CLI: run `amplify init` in your project, then `amplify add storage` and follow prompts to create a bucket. Amplify will create a file `aws-exports.js` in your project with all details (bucket name, region, Cognito pool, etc.) and you can directly use Amplify’s `Storage` API.
- If not using Amplify CLI, you can manually create a Cognito Identity Pool in the AWS console, attach an IAM role that has S3 PutObject permission on your bucket. Then use `Auth` from Amplify or AWS SDK to get credentials. (This is advanced configuration; using Amplify's defaults is simpler.)

**Minimal IAM Policy for S3:** If you choose to create an IAM user manually, an example policy to allow uploads might be:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-recorder-uploads",
        "arn:aws:s3:::my-recorder-uploads/*"
      ]
    }
  ]
}
```

Attach this to the user or role. But be cautious: embedding those keys in-app means if someone decompiles the app, they have access. At _minimum_, never commit keys to source control and consider using environment variables or a server to distribute temporary credentials.

We will proceed with the assumption of using **AWS Amplify** for integration, as it abstracts a lot of this and follows best practices (the Amplify scenario uses Cognito under the hood, which is more secure).

### Installing & Configuring AWS SDK (Amplify) for React Native

We already installed `aws-amplify`. Amplify is a high-level library that includes Auth, API, Storage, etc. We will use the Storage module.

**Configuration:** When using Amplify in React Native, you typically have a configuration file. If you used Amplify CLI to add storage, you should have `src/aws-exports.js` with configurations. If not, you can manually configure Amplify:

Example `aws-exports.js` (if manually writing):

```js
const awsmobile = {
  aws_project_region: "us-east-1",
  aws_cognito_identity_pool_id: "us-east-1:xxxxxx-xxxx-xxxx-xxxx-xxxxxxxx", // if using Cognito
  aws_cognito_region: "us-east-1",
  aws_user_pools_id: "us-east-1_XXXXXXXXX", // if using user pools (optional)
  aws_user_pools_web_client_id: "XXX", // if using user pools (optional)
  aws_storage_bucket: "my-recorder-uploads",
  aws_storage_region: "us-east-1",
  aws_storage_defaultAccessLevel: "public", // or "private"/"protected"
};
export default awsmobile;
```

The above is similar to what Amplify CLI would produce. The **Access Level** is worth noting:

- `"public"` means content is publicly accessible (no authentication needed to get the object if you know the URL). In Amplify, "public" allows unauthenticated identities to read/write if policy allows.
- `"protected"` means only authenticated users can read, but anyone (even guest) can write? Actually Amplify defines:
  - public: read/write by all (if identity pool unauth role has access),
  - protected: read by all authenticated users, write by owner only,
  - private: read/write by owner only.
- We'll treat our uploads as either public or protected. For personal recordings, "private" would make sense (only that user can access). But to keep it simple, we might use public or protected and not delve deep into user management.

**Initialize Amplify:** In your app entry (App.tsx or a separate config file called in index.js), configure Amplify:

```js
import Amplify from "aws-amplify";
import awsconfig from "./src/aws-exports";
Amplify.configure(awsconfig);
```

This should be done before using any Amplify APIs. After configuration, Amplify’s Storage module knows about our S3 bucket.

_(If not using Amplify config and using raw AWS SDK: you would do something like AWS.config.update with region and credentials. But as mentioned, we proceed with Amplify for ease.)_

Now we can use Amplify’s Storage API to upload files. Amplify also handles things like refreshing credentials if using Cognito.

### Securely Handling API Keys & Authentication

Security is crucial when integrating AWS:

- **Do NOT hardcode Access Key/Secret in the app code.** This is easily extracted. If using Amplify with Cognito, you only have the identity pool ID which by itself is not a secret.
- If using an IAM user approach (not recommended for production), at least store the keys in a secure way (e.g., use environment variables and some obfuscation, or fetch them from a secure server). However, assume any determined attacker with the APK could retrieve them. With those keys, they could potentially read/write to your S3 bucket outside the app.
- **Preferred approach:** Use Amazon Cognito Identity Pools for unauthenticated or authenticated identities. This gives temporary, limited-privilege credentials to the app. The `aws-exports.js` approach above likely uses a Cognito Identity Pool (`aws_cognito_identity_pool_id`). The IAM role attached to that identity pool should have permissions only for the S3 bucket (and perhaps with some object key restrictions).

**Authentication:** If your app requires user login (say, using Cognito User Pools or any auth), you can integrate that with Amplify Auth. For our scenario, maybe this is a utility app without user accounts – then you might use the Identity Pool's "unauthenticated guest" credentials to allow uploads. Amplify supports that (if you enable unauth access in the identity pool).

- If using unauth, ensure the unauth role has only the needed permissions.
- If using auth (user must sign in), then the auth role can have broader access (still only to their content ideally).

**Protecting Secrets:** Amplify will store tokens/credentials in React Native’s AsyncStorage under the hood. That’s generally fine. Just make sure not to log sensitive info. The actual S3 upload will be signed with those credentials.

**Network Security:** The uploads to S3 should be done over HTTPS by default (Amplify uses HTTPS endpoints). AWS endpoints support HTTPS and you should ensure it's not downgraded.

**CORS (if using presigned URLs in a web context):** Not needed in React Native (no browser), but if ever generating a presigned URL and using `fetch` to PUT, since RN is not subject to browser CORS, it's okay. If this were a web app, you'd configure CORS on the bucket for web uploads.

At this stage, with Amplify configured, we can implement the actual file upload functionality in our app.

### Implementing File Uploads with Progress

We will use **Amplify Storage** to upload. The Amplify Storage module provides the `Storage.put` method for uploading files to S3. It can take a **File Blob or a file path** (React Native can often use the URI string directly, Amplify will handle it by using React Native fetch under the hood). We will also use the progress callback to update UI.

**Uploading a video or audio file:**

```ts
import { Storage } from "aws-amplify";

// fileUri: the local file path (string) we got from recording
// key: the name to use in S3 (you can include folder paths if desired)
async function uploadFile(fileUri: string, fileType: "video" | "audio") {
  const fileExtension = fileUri.split(".").pop(); // e.g., 'mp4' or 'm4a' or 'mp3'
  const fileName = fileUri.split("/").pop(); // take the last part of path as file name
  const s3Key = `${fileType}/${Date.now()}_${fileName}`;
  // We prefix with type/ and timestamp to avoid name collisions and organize by type.

  try {
    console.log(`Uploading ${fileUri} to S3...`);
    const response = await Storage.put(s3Key, {
      // We need to pass the file data here. Amplify accepts:
      // For React Native: either a Blob, or a URI with special handling.
      // We'll use fetch to get the blob from the file URI.
      level: "private", // or 'public' or 'protected' depending on your use case
      contentType: fileType === "video" ? "video/mp4" : "audio/m4a", // adjust if mp3
      progressCallback(progress) {
        const percent = Math.round((progress.loaded / progress.total) * 100);
        console.log(`Upload progress: ${percent}%`);
        // We can update state to show a progress bar or percentage text
        setUploadProgress(percent);
      },
    });
    console.log("Upload successful: ", response.key);
    // Mark the file as uploaded in our stored list, perhaps update AsyncStorage
    await markFileAsUploaded(fileUri, response.key);
  } catch (err) {
    console.error("Upload failed", err);
    // handle retry or error UI
  }
}
```

The above code is a conceptual illustration. A few important things:

- We generate an `s3Key` which is the object key in the S3 bucket. We include subfolder by type and timestamp to keep it unique. You could also use UUIDs.
- `Storage.put(key, file, options)` is typically how Amplify works. But in React Native, if we pass the `fileUri` string directly, Amplify might attempt to auto-detect and upload. However, in some cases, you need to convert the URI to a Blob. The Amplify docs suggest using `fetch` to get the blob from the file URI:
  ```js
  const response = await fetch(fileUri);
  const blob = await response.blob();
  await Storage.put(key, blob, { contentType: 'video/mp4', progressCallback... });
  ```
  We saw this approach in the instamobile example. This ensures Amplify knows the data. (Amplify v4+ can accept a file URI string on React Native by internally converting it, but let's assume we might need to do it manually for reliability.)
- The `progressCallback(uploadProgress)` gives loaded and total bytes. We compute a percentage and log it or set state. This way we can show a progress bar in the UI.
- We set `level: 'private'` meaning the file will go to a user-specific protected area if using Cognito (if not using Cognito, 'private' vs 'public' might not matter beyond possibly prefixing the key differently).
- `contentType` is important so that S3 knows what type of file it is (especially if you will access it via web or need to play it from S3 directly).
- On success, `Storage.put` returns an object with the key (and maybe some other info). We log the key. We could store the S3 key in our file list metadata (e.g., mark the local file entry with `s3Key` and `uploaded=true`).
- In case of an error, we catch it and can decide to retry or show a message. Amplify might throw different errors (network issue, credentials issue, etc.).

**Progress Display:** In our state, we might have something like:

```ts
const [uploadProgress, setUploadProgress] = useState<number | null>(null);
const [uploadStatus, setUploadStatus] = useState<
  "uploading" | "done" | "error" | null
>(null);
```

We update these in the uploadFile function accordingly. The UI could show a progress bar or spinner when `uploadStatus==='uploading'`. Once done, maybe show a checkmark.

**Multiple Uploads:** If uploading multiple files (say user recorded several before hitting an upload action), you could upload in sequence or parallel. Parallel uploads of large files might strain bandwidth/memory, so maybe queue them.

**Large Files and MultiPart:** As noted, Amplify will automatically use S3's multipart upload for large files (>5MB). This means even if the file is 100MB, it will upload in chunks, and the progress callback will reflect chunk progress. This is efficient and you don't need to manage it manually.

**Alternate Approach - AWS SDK v3:** Another way is to use `@aws-sdk/client-s3` and call `PutObjectCommand`. However, this can be tricky in React Native due to needing a polyfill for buffer, and you would still have to manage progress events manually. Amplify simplifies those details.

### Error Handling and Retry Logic

Even with the best code, network issues or other errors can cause uploads to fail. We need to handle these gracefully:

- Always wrap upload calls in try/catch (as above).
- If `err` is something like a network error, you might inspect it and decide to retry immediately or after some backoff. For example, you can implement an exponential backoff: wait 1s, then 2s, then 4s, etc., up to some limit, and retry the upload.
- Amplify's `Storage.put` might not have built-in retry for certain errors, so manual retry could be needed. (It likely retries internally for multipart parts but let's assume we manage our own logic at a high level.)
- If the app goes offline mid-upload, Amplify will throw. You can listen for network status via `NetInfo` from `@react-native-community/netinfo` to delay uploads until connection is back.

**Example Retry Pseudocode:**

```js
async function uploadWithRetry(fileUri, fileType, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await uploadFile(fileUri, fileType);
      // if successful, break out of loop
      setUploadStatus("done");
      return;
    } catch (err) {
      if (attempt < retries) {
        console.log(`Upload attempt ${attempt} failed, retrying...`);
        await new Promise((res) => setTimeout(res, attempt * 2000)); // wait 2s, 4s, ...
      } else {
        console.log("All retries failed.");
        setUploadStatus("error");
        // maybe keep the item marked as not uploaded so user can retry manually
      }
    }
  }
}
```

We can call `uploadWithRetry(item.uri, item.type)` for each item.

**Handling specific errors:**

- 403 Forbidden from S3: means credentials are not allowed to that bucket/key. Check IAM policies or if credentials expired (Amplify should refresh if expired).
- 413 Entity too large: file might exceed some service limit (unlikely for S3 if under 5GB in one put; Amplify splits anyway).
- Network timeouts: could happen on very slow networks. Possibly handle by smaller chunk or just rely on S3 multipart.

**Cancellation:** If user wants to cancel an upload in progress, Amplify’s `Storage.put` doesn't provide a straightforward cancellation token. In that case, using the lower-level AWS SDK with abort controller or using `react-native-background-upload` (which we discuss later) might be needed. For simplicity, we won't implement cancellation here, but note it's a limitation.

**Cleaning up partial uploads:** S3 multipart uploads, if interrupted, can leave partial parts. AWS S3 has lifecycle rules to abort multi-part uploads after X days automatically. Not a big issue for a few user files, but something to know.

Now that uploading is handled, let's discuss further enhancements and optimizations that an advanced app might implement.

---

## Enhancements & Optimizations

At this stage, we have a working app that can record audio/video, save them, and upload to S3. Next, we'll explore additional features and improvements:

- Compressing media files to reduce upload size.
- Uploading in the background so the user isn't stuck on the app during a long upload.
- Encrypting files for added security.
- General performance optimizations for the app’s runtime and user experience.

Each enhancement is optional but can significantly improve the app depending on use case.

### Media File Compression Before Upload

**Why compress?** Raw recorded videos can be large. For instance, a minute of 720p video might be ~50MB. Many times, such high quality isn't necessary or can be compressed further with minimal perceptible loss. By compressing:

- Uploads are faster (uses less bandwidth).
- Storage costs on S3 are lower (smaller files).
- Downloads for playback are faster if users will retrieve them.

**Video Compression Libraries:** There are a few libraries:

- [`react-native-compressor`](https://www.npmjs.com/package/react-native-compressor): Compresses images, videos, audio similar to WhatsApp quality. Also offers background upload capability.
- [`react-native-video-compress`](https://github.com/chengsam/react-native-video-compress): Another that provides video compression to MP4 with options for bitrate, quality.
- Using native FFmpeg through [`react-native-ffmpeg`](https://github.com/tanersener/react-native-ffmpeg) (powerful but adds a large binary ~10MB and complexity of FFmpeg commands).
- Server-side compression: Alternatively, upload raw and let a server compress, but that means user uploads a big file, so it defeats the purpose for bandwidth.

We will use **react-native-compressor** for demonstration, as it also can compress audio if needed:
Install it (we already did). It might require linking (autolink should do, plus pod install, which we did).

**Compress before upload:** The workflow would be:

1. After recording, but before upload, call the compression function on the file.
2. Get a new compressed file path.
3. Upload that instead.
4. Optionally, delete the original large file to save space, once the compressed one is confirmed good.

**Example using react-native-compressor:**

```js
import { Video, Audio } from "react-native-compressor";

async function compressVideoFile(originalPath: string): Promise<string> {
  try {
    console.log("Compressing video...", originalPath);
    const compressedPath = await Video.compress(
      originalPath,
      { compressionMethod: "auto" }, // 'auto' chooses WhatsApp-like settings
      (progress) => {
        console.log("Compression progress: ", progress);
      }
    );
    console.log("Video compressed to:", compressedPath);
    return compressedPath;
  } catch (e) {
    console.error("Video compression error", e);
    return originalPath; // if compression fails, fall back to original
  }
}
```

The `react-native-compressor` API above:

- `Video.compress(inputFile, options, callback)` returns a promise with the path of the compressed video.
- We used `compressionMethod: 'auto'` which tries to mimic WhatsApp's algorithm (good balance).
- The `progress` callback gives a number from 0 to 1 (percentage) which we log or could use to update UI. Compression can be time-consuming, so consider showing a loader.
- The output path on Android is typically a new file in cache (e.g., `.mp4` in cache or files directory). On iOS, similar.
- After compression, we get `compressedPath`. That is what we will provide to `uploadFile`.

**Audio Compression:** Audio files recorded as M4A (AAC) or MP3 are usually already compressed. You could compress audio by re-encoding to a lower bitrate MP3 or AAC. The `react-native-compressor` has an `Audio.compress` but audio sizes are smaller, so this is less critical unless you need to shrink long recordings or convert WAV to MP3.

**Trade-offs:** Compression uses CPU and battery. On older devices or very long videos, this might take a while and potentially overheat if not careful. Test how it performs and consider providing the user an option to upload original vs compressed.

**When to compress:**

- Option 1: Compress immediately after recording (blocking UI until done, or show “processing”).
- Option 2: Compress on the fly during upload (some libraries allow streaming compress while uploading, but that's complex).
- Option 3: Compress only when on cellular vs WiFi (maybe skip compression if on WiFi and user doesn’t mind, compress on cellular to save data).
- Option 4: Always compress in background after recording while user can still record next (multi-threading would be needed or just schedule it).

For simplicity, you might call `compressVideoFile` inside your `uploadFile` function before actually uploading:

```js
const pathToUpload = fileType==='video' ? await compressVideoFile(fileUri) : fileUri;
await Storage.put(s3Key, /* blob from pathToUpload */, { ... });
```

Thus, you compress only when uploading. Alternatively, call it right after recording and update the local list to point to the compressed file.

### Background Uploads

In a mobile app, it's important to handle the scenario where the user leaves the app while an upload is in progress. By default, if the app goes to background, the JavaScript thread may be suspended and any ongoing upload might pause until the app comes back to foreground. On iOS, there's a short grace period for network tasks to finish when app goes background, but not enough for large videos (iOS might allow ~30 seconds, after that the app is frozen). On Android, background execution is more lenient but not guaranteed unless a Foreground Service is used.

**Solution:** Use a native background upload mechanism. The library **`react-native-background-upload`** (by Vydia) is a popular choice. It offloads the upload to native background tasks on both Android and iOS, meaning the upload can continue even if the app is minimized or the screen is locked.

To use it:

- We've installed it. For iOS, ensure `Background Modes -> Background fetch` or `Background transfer` is enabled in Xcode if required (the library docs mention adding capabilities).
- The library works by performing an HTTP POST/PUT. So it doesn't directly integrate with Amplify; instead, you'd either hit your own upload server or use S3 pre-signed URLs.

**Using Pre-Signed URLs for S3:** One way is:

1. Get a pre-signed URL for your S3 bucket (your backend or an AWS Lambda could generate this, or even Amplify Storage has a `Storage.get(key, { expires: X, download: false })` which might give a URL).
2. Use `react-native-background-upload` to upload the file to that URL with method PUT.

However, since this is complex to integrate with Amplify in one step, an easier approach:

- Amplify Storage does not natively support background (as it runs in JS). So consider using background-upload library directly with S3 REST API.
- The library can also upload to any HTTP endpoint. AWS S3 PUT Object can be done via a signed URL or via the AWS SDK with credentials. Without a server, you could try constructing the AWS authorization header yourself, but that's not trivial.

If we imagine an **advanced scenario**: We have an AWS Lambda that can generate a pre-signed URL for a given key. Our app requests that first, then uses background-upload to PUT the file. This way, the heavy lifting is done by background-upload.

For brevity, let's illustrate usage of react-native-background-upload (not fully wiring with S3, but conceptually):

```js
import Upload from "react-native-background-upload";

async function uploadInBackground(fileUri: string) {
  const fileName = fileUri.split("/").pop();
  const destUrl = await getPresignedUrlFromServer(fileName); // your implementation
  const options = {
    url: destUrl,
    path: fileUri.replace("file://", ""), // the library might need a file path without scheme
    method: "PUT",
    type: "raw", // since we are doing direct PUT of binary
    headers: {
      "Content-Type": "video/mp4", // or appropriate
      // If your presigned URL requires any specific headers (usually it includes them in query params, so not needed here)
    },
    notification: {
      enabled: true,
      autoClear: true,
      onProgressTitle: "Uploading...",
      onCompleteTitle: "Upload finished",
      onErrorTitle: "Upload error",
    },
  };

  Upload.startUpload(options)
    .then((uploadId) => {
      console.log("Background upload started with ID:", uploadId);
      Upload.addListener("progress", uploadId, (data) => {
        const percent = Math.round(data.progress);
        console.log(`Background Upload Progress: ${percent}%`);
      });
      Upload.addListener("error", uploadId, (data) => {
        console.log(`Background Upload error: ${data.error}`);
      });
      Upload.addListener("completed", uploadId, (data) => {
        console.log("Background Upload completed");
        // maybe mark file as uploaded
      });
    })
    .catch((err) => {
      console.error("Unable to start background upload", err);
    });
}
```

Key points:

- `react-native-background-upload` can show notifications on Android while uploading (via `notification` options). On iOS, it uses URLSession background tasks which allow upload to continue for longer (still, iOS may impose time limits but it's the best you can do).
- We had to get a `destUrl`. This implies some backend logic. For completeness, if using AWS Amplify with Auth, an alternative is to use AWS S3 multipart copy but that’s too complex; better to stick to presigned.
- The `path` we give is the local file path. We strip `file://` as the library expects a raw path.
- `type: 'raw'` indicates we are sending the raw file. The library also supports `multipart` if posting as form-data, but for S3 PUT, raw is correct.
- We add listeners for progress, error, completion.
- If user closes the app completely (swipes it away), on iOS the upload may still continue, but you won't get events in JS (app is closed). On Android, if app process is killed, the upload might stop unless it's a foreground service (this library uses WorkManager on Android I believe). The library doc says it's the only RN uploader with background support on both platforms.

**When to use background upload:**

- If your app expects users to possibly leave mid-upload often (e.g., uploading large videos).
- If uploads are very large (hundreds of MB) that user wouldn’t reasonably keep app open for.
- If you promise the user they can navigate away and it’ll still upload.

If the files are small or medium (few MB), maybe normal upload with a notice "Keep app open until upload completes" is acceptable, as background complexity is high.

### Encrypting Files for Security

Security of data is paramount, especially if the recordings may contain sensitive information. There are multiple layers where encryption can be applied:

1. **In-Transit Encryption:** Data is encrypted during upload via HTTPS (TLS). AWS Amplify/SDK uses HTTPS by default, fulfilling this. We should enforce using `https://` endpoints (Amplify does).
2. **At-Rest Encryption on S3:** S3 can automatically encrypt stored objects (Server-Side Encryption). You can enable default encryption on the bucket (AES-256 or AWS KMS managed keys). It's good to enable this so even if someone got the raw S3 storage, they can't read files without the key. AWS now enables SSE-S3 by default on buckets.
   - You can also specify in the upload request that you want SSE (e.g., adding `x-amz-server-side-encryption: AES256` header or as option in SDK).
   - We should check our IAM policies to ensure they allow only encrypted uploads. AWS Foundational security advises ensuring SSE is enabled.
3. **Client-Side Encryption:** This means encrypting the file _before_ uploading, so that even AWS (and anyone with access to the bucket) cannot read it unless they have the decryption key. This is the highest level of security: "encrypt your data before it ever leaves your device" ([amazon web services - Aws S3 encryption. Why use it? - Server Fault](https://serverfault.com/questions/931326/aws-s3-encryption-why-use-it#:~:text=With%20that%20said%2C%20if%20you,free%20to%20do%20so%2C%20right)). Implementing this means:

   - You generate a symmetric key (e.g., using crypto libraries) on the device or retrieve a public key from server.
   - Encrypt the file (this could be done using libraries like `react-native-crypto` or native code or using AWS SDK client encryption libs).
   - Upload the encrypted file to S3.
   - To play/download, you'd need to decrypt it on the client after downloading from S3.

   This is doable but complex. If you require this, consider using AWS S3 client-side encryption SDK or a simpler approach like encrypting the file bytes with AES using a key.
   For example, you could use `react-native-fs` to read the file as base64, use a JavaScript crypto library to encrypt the base64 string, then upload the encrypted data. But encrypting large videos in JS could be slow (native would be better).

   Given our advanced developer scope, we at least note that for maximum security (think sensitive voice or video data), client-side encryption ensures privacy even if cloud credentials leak ([amazon web services - Aws S3 encryption. Why use it? - Server Fault](https://serverfault.com/questions/931326/aws-s3-encryption-why-use-it#:~:text=With%20that%20said%2C%20if%20you,free%20to%20do%20so%2C%20right)).

**Practical steps for encryption:**

- **Enable S3 SSE:** In the AWS Console for S3, enable "Default Encryption" with AES-256 or AWS-KMS for the bucket. That way, any file uploaded (even from our app) is encrypted at rest by AWS. This doesn't require code changes (unless your bucket policy requires the header).
- **Use KMS for more control:** If using AWS KMS keys, you can specify a key and even have more control (like audit access to that key). But that requires adding a header or Amplify config to use KMS key-id.
- **Client encryption option:** Possibly out-of-scope to implement fully here, but one could do:
  - Use a library like `crypto-js` (for AES encryption in JS) if file is not huge (crypto-js can handle base64 of a few MB, but a 50MB video might be too slow).
  - Or do chunk encryption to not load entire file in memory.
  - Or use native encryption modules.

**Weighing needs:** If the content is not extremely sensitive and you trust AWS's SSE, that is usually sufficient and much easier. Many apps rely on SSE-KMS (managed by AWS) as a robust security measure (especially since now S3 auto-encrypts new objects by default).

**API Keys protection:** Also recall that by using Cognito, we avoid storing long-term API keys in the app. If you had to, you might encrypt them or use AWS SDK's feature to retrieve credentials via Amazon Cognito anyway.

### Optimizing App Performance

Performance considerations in such an app include:

- UI rendering performance: The camera preview can be performance intensive. Use `PureComponent` or functional components with memo if the UI around the camera re-renders often. We kept it simple, but for example, avoid re-rendering the `<RNCamera>` while recording is ongoing (that could cause issues). We managed state in a way that toggling recording doesn't unmount the camera, which is good.
- Use `useCallback` for functions like `startVideoRecording` if passing them to components, to prevent unnecessary re-renders of child props.
- Large state objects: We only store URIs and small info, which is fine. We avoid storing actual file data in state.
- **Memory usage:** By not reading files into JS memory, we keep memory usage low. If you ever have to manipulate the file (like for encryption or other processing), try to do it in streams or native modules to avoid OOM on large files.
- **Background threads:** Recording itself runs on device hardware codecs, not the JS thread, so it's okay. But our compression uses native code (FFmpeg or similar via that library) which will consume CPU. It's not on JS thread, but it will tax the device; possibly do compression when the device is connected to power or allow user to cancel it if taking too long.
- **Throttle progress updates:** If you find progress callbacks (upload or compression) are calling setState too frequently (like many times per second), throttle them to maybe update UI 2-4 times a second to reduce render load.
- **Batch operations:** If uploading many files sequentially, ensure one finishes (or a couple concurrently) rather than all at once which could saturate the network and slow the device.
- **Offline handling:** If offline, maybe queue the upload and not even attempt until network is available (store in AsyncStorage a "pending uploads" list).
- **Release resources:** When the user navigates away from the recording screen, stop the camera preview (you can unmount RNCamera or call `pausePreview()` ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=pausePreview)) to free camera for other apps). Also, if audio recording not in use, release it (the library doesn't need explicit release, but ensure `stopRecorder()` called).
- **Battery usage:** Video recording and uploading are heavy on battery. Inform the user or manage when to do these tasks (perhaps allow uploads only on WiFi or with battery > X%, depending on use case).

- **Testing performance:** Use profiling tools. React Native has a performance monitor, and Xcode Instruments or Android Profiler can show CPU/memory usage of your app during recording and uploading. This can catch any obvious inefficiencies.

By implementing these optimizations and being mindful of resource usage, you ensure the app runs smoothly even as it handles intensive tasks.

---

## Deployment & Testing

With features implemented, we must rigorously test the application and then prepare it for deployment on both iOS App Store and Google Play Store. This section outlines debugging techniques, writing tests (unit/integration/UI) to verify functionality, and best practices for releasing the app.

### Debugging and Logging Best Practices

During development, you'll encounter issues (permission problems, crashes, failed uploads, etc.). Good debugging practices include:

- **Logging:** We used `console.log` and `console.error` in many places. In development, these show up in Metro console or device logs. For a more robust solution, consider integrating a logging library or service (like Sentry for crash reporting, or React Native Debugger/Flipper for viewing logs). Ensure to remove or tone down verbose logs in production builds to avoid performance issues or leaking sensitive info.
- **React Native Debugger/Flipper:** Flipper is an extensible debugging platform for RN apps. It can show logs, network requests, performance, database, etc. If Amplify is making network calls, you can inspect them via Flipper's network plugin to ensure requests are correct.
- **Inspecting device logs:** For Android, use `adb logcat` to see native logs as well, which might show camera errors or other native module issues. For iOS, use Xcode > Devices & Simulators > see logs, or run via Xcode to see console.
- **Debugging permissions:** If camera or mic isn't working, check that permissions are granted. On Android, `adb shell pm grant <package> android.permission.CAMERA` can force grant for testing. On iOS, if you accidentally denied and want to test again, you must reset permissions (via Settings or uninstall app).
- **Handling native errors:** `react-native-camera` might throw errors if something is wrong (like "Camera is not running"). Catch and log those, possibly show user an alert to reopen camera.
- **Profiling performance:** Use Xcode Instruments for iOS (Time Profiler, Energy Log) to see if any method is hogging CPU. Use Android Profiler (in Android Studio) to check memory during video recording, etc.
- **Network debugging:** If upload fails, you might log the error. Amplify error might contain an HTTP response. Check if it's a 401 (not authorized) or other code. Use AWS CloudWatch (if using Cognito, failed auth can log there) or S3 logs if enabled to debug server-side issues.

- **Edge case testing:** Try unusual scenarios: record video then immediately stop app, does it save? What if no internet and user hits upload? Does the app crash if upload called with no connection (Amplify should throw nicely, which we catch)? Also test long recordings (does a 10 minute audio recording still work? Does a 500MB video actually upload? maybe not in one go without tuning, but test boundaries).

By thoroughly debugging, you'll iron out many issues before users see them.

### Running Tests (Unit, Integration, UI)

**Unit Testing:** Focus on testing the non-UI logic:

- Functions like `saveRecordingInfo`, `uploadFile` (maybe mock Storage.put), `compressVideoFile` (could be tricky to actually run in test, better to mock the compressor module).
- Use Jest as it comes with React Native projects. You might need to mock native modules such as `react-native-camera` because they can't run in a Node environment. For example, create a file `__mocks__/react-native-camera.js` to export a dummy component ([Testing · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/tests#:~:text=To%20test%20a%20component%20which,the%20root%20of%20your%20project)).
- Test that after recording (simulate calling the functions) the AsyncStorage is updated properly, etc.

**Integration Testing:** This might involve launching the app and simulating flows:

- You can use **React Native Testing Library** to render components and simulate button presses. For instance, render `<RecordScreen>` in a test, simulate a press on "Record Audio", then simulate a press on "Stop Audio", and assert that `audioRecordFile` state is not null afterwards. However, since that uses a native module, you'd have to mock `audioRecorderPlayer.startRecorder` to immediately return a path, etc.
- Or use Detox for end-to-end: Detox can automate the app on a simulator. You could script: press "Record Video", wait X seconds, press "Stop", then press "Upload", and then verify some success message. This requires the app to be in debug mode with Detox integrated.

**UI Testing:** Visually verify on devices:

- Test on different device types (small screen, large tablets) to ensure the camera preview and buttons layout nicely.
- Test on both platforms - there might be platform-specific issues (e.g., Android might need handling of back button, or differences in file URI format).
- If possible, test on a physical iOS device – camera and mic behavior sometimes differ from simulator (the simulator has no camera input, it will just show a blank or test pattern for RNCamera; the audio may not record on simulator either. So real devices are needed for full test of recording).
- For iOS, test that you have provided Info.plist usage descriptions correctly; run a build for release and ensure no permissions issues.
- Test background upload by initiating an upload and then minimizing the app; on Android, see if it completes (logcat or notification), on iOS, see if it completes (maybe check the file appears in S3 or debug logs on next open). This can be tricky to automate, but manual testing is key.

**Automated vs Manual:** For an advanced app, setting up a CI pipeline for tests would be ideal. You can run Jest in CI easily. Detox can run on a CI (like GitHub Actions with macOS runners) to do some flows on iOS/Android emulator.

**Mocking AWS:** In unit tests, you might not actually hit AWS. Use jest mocks for `Storage.put` to simulate a resolved promise or progress callback. Amplify might need a little setup to not actually try to reach the network.

**Testing uploading to AWS (Integration):** Possibly create a test environment S3 bucket and actually try an upload from a dev build, ensuring the file arrives and is intact (download and play it from S3 to confirm).

**Edge Cases to Test:**

- Very short recordings (less than a second).
- Hitting stop immediately after start (did we handle if `recordAsync` promise might not have settled? Our code awaited promise after stop, which should be fine).
- User denying permission and then trying to record.
- Network down and coming back during an upload.
- Cancel upload (if not implemented, at least it should not crash anything).
- Multiple recordings in a row (does each new recording get a new file or overwrite? RNCamera will generate a new file each time; audio library overwrote because we gave same file name on iOS in example - maybe use unique name each time to avoid overwriting audio. On Android we left undefined so it auto-creates unique. So adjust iOS audio logic to use unique name too, e.g., use Date.now in name.)
- App being killed mid-recording (likely the file is lost or not saved properly; not much can be done, but see if partial file exists and handle it or just discard it on next launch).

By covering these tests, you'll gain confidence in the app's reliability.

### Deploying to App Store and Google Play

Finally, to release the app to users:

**App Store (iOS):**

- Ensure all App Store requirements are met:
  - Provided usage descriptions for camera/microphone (we did; Apple will reject if not ([Your app will be rejected from the AppStore unless you add ...](https://community.intercom.com/mobile-sdks-24/your-app-will-be-rejected-from-the-appstore-unless-you-add-nscamerausagedescription-and-nsmicrophoneusagedescription-to-your-info-plist-6591#:~:text=,plist))).
  - Icons and launch screens are set up.
  - No mention of private APIs or prohibited content.
- Use Xcode to archive the app:
  - In Xcode, increment the version and build number.
  - Product -> Archive, then validate and upload to App Store Connect.
- On App Store Connect, fill in app information, upload screenshots (you might take screenshots of your recording UI, etc.), and then submit for review.
- Apple review: They will test the app, ensure it asks for permissions correctly and functions. They might record a short video and see if it works. Make sure the app doesn’t crash and provides some user guidance if needed (e.g., if no permission, we should ideally show a message instead of just doing nothing).
- If using background modes (like audio recording in background, etc.), list them in your Entitlements and explain usage to Apple (they are strict about background audio usage, e.g., if you allow audio recording with screen off, they want a justification).

**Google Play (Android):**

- Generate a signed APK/AAB:
  - Create a signing key (if not already) via Android Studio or `keytool`.
  - Set up gradle to sign the release build with that key.
  - Generate the release AAB (Android App Bundle) which is now the preferred upload format.
- Test the release build on a device (sometimes Proguard can cause issues with native libs – e.g., ensure you added Proguard rule for background-upload as noted in its docs).
- Create a Google Play Developer account if not done, then create a new app listing.
- Upload the AAB, add content descriptions (it will ask if your app uses camera/mic and for what – be truthful, it will likely mark it as requiring those features).
- Add screenshots, descriptions, etc.
- Submit for review (usually faster than Apple’s process).

**Beta Testing:** Consider using TestFlight (for iOS) and Internal Testing track (for Android) to distribute the app to a few testers (or your team) before public release. They might find issues you missed.

**Deployment Configurations:**

- Remove any debug code or test endpoints.
- Ensure Amplify is pointing to production resources (or if you used a dev S3 bucket, either switch to prod bucket or have it configurable).
- Monitor logs post-release. If you integrated something like Sentry, you'll catch any runtime errors users face.

**App Updates:** Plan how to roll out updates if needed. If a critical bug in recording arises, be ready to fix and push an update.

**Security in Deployment:**

- Make sure the S3 bucket has proper CORS (if any web usage) and correct policies. If it's meant to be private, double-check that (use AWS IAM Policy Simulator or try accessing an object via URL to see if it's blocked).
- Possibly set up server-side monitoring: AWS CloudWatch can log S3 access or Amplify Auth usage anomalies.

**Privacy and Compliance:**

- Because the app records user content, ensure your app listing has a privacy policy (both stores require one if the app collects user content).
- If targeting regions with data protection laws, mention how data is stored (S3, possibly region, encryption etc).
- If minors could use the app, consider restrictions or compliance like COPPA (if applicable).

By following these steps, you'll successfully package and release your app to users.

---

## Security Best Practices

Security should be considered at every step of development, but let's summarize specific best practices relevant to our React Native recorder app, especially around uploading to S3 and handling user data.

### Protecting S3 Uploads & Preventing Unauthorized Access

**S3 Bucket Access Controls:**

- Keep the bucket **private**. Do not enable public read or write unless absolutely necessary. AWS provides block public access settings that should be on to prevent accidental exposure.
- Use IAM roles/policies to scope access. For example, if using Cognito identity pool, configure the role so that:
  - It can only access the specific bucket (as we did in our policy example).
  - Optionally, if using authenticated users, you can restrict each user's access to only their own folder (S3 supports policy conditions like `${aws:userid}` in the key).
- If not using Cognito and using one set of credentials in app (not ideal), at least restrict those credentials to only allow `PutObject` and perhaps only in a certain prefix (you could have a common prefix for app uploads).
- Consider **Server-Side Encryption** mandatory. Enable bucket default encryption (SSE-S3 or SSE-KMS). This means if anyone somehow got the raw storage they still can’t read the data. Many organizations require this.
- Monitor your bucket: Turn on S3 server access logging or AWS CloudTrail for object-level API calls. This way, if something suspicious happens (e.g., a flood of download attempts), you are aware.

**Preventing Unauthorized Uploads:**

- If you used unauthenticated access (guest), note that technically anyone with the app (or decompiled app) could use those credentials. If someone extracted your Cognito identity pool ID, they could abuse it to get credentials and upload unwanted data. Mitigate by:
  - Setting bucket lifecycle rules to maybe delete unrecognized files or scan them.
  - Or requiring authentication (users must log in, so you at least know which user did what).
  - Or validating content on the server side if possible.
- Another technique: use pre-signed URLs that your server issues only for specific actions (then an attacker would have to request from your server which you could authenticate or rate-limit).

**Data Validation:** If your app allows upload, ensure the content is what you expect:

- Perhaps restrict file sizes in the app (no one should upload a 5GB file unexpectedly).
- The server side (if any) could also enforce size or type limits (S3 bucket can have an object policy restricting max size via Lambda trigger, or simply rely on app restriction).
- Validate file type if important (e.g., ensure videos are .mp4, not some other possibly dangerous file - though on S3 it's just bytes, but if you later serve them publicly, you don't want someone uploading HTML or something that could be malicious if interpreted incorrectly).

### Securing API Endpoints and Authentication

If your app communicates with any API or backend besides direct S3:

- Use proper authentication (e.g., if using a custom backend to get pre-signed URLs or to list user files, protect those endpoints with Auth tokens).
- Use HTTPS for all network calls (which includes S3 and any API).
- Do not expose sensitive information through endpoints. For example, if you have an endpoint to list all user’s files, ensure it checks the identity of the requester (don’t allow an attacker to query others' files).
- Implement rate limiting or abuse detection on any endpoints that could be spammed (like a misbehaving client repeatedly asking for presigned URLs or uploading too frequently).

For Amplify, if you use **Auth (Cognito User Pools)**:

- Enforce strong password policy, multi-factor auth if appropriate, and email/phone verification as needed.
- Validate user emails if they will be used in S3 key naming to avoid any injection (probably not applicable here).
- Keep Cognito tokens duration reasonable and secure (Amplify handles storing them, but you might want to adjust token refresh periods based on your security needs).

**Secure Storage of Keys/Tokens:**

- The app will inevitably store Cognito identity ID and tokens in AsyncStorage (Amplify does that). This is on the device and could be extracted if device is rooted. For extremely sensitive apps, consider using an encrypted storage (there are libraries for RN to store sensitive data in Keychain/Keystore rather than plain AsyncStorage).
- However, media files themselves likely not super secret on device (they recorded them so it's already on device in plain form).

**Least Privilege Principle:**

- The app’s AWS credentials should have the least privileges it needs. For example, it probably doesn’t need to `ListBucket` on the entire bucket if your design is such that the app always knows the key names (but we included it for listing in our policy). If you can, limit it to only `PutObject` and maybe `GetObject` on specific key patterns.
- If you implement delete functionality (user can delete recording from cloud), then include `DeleteObject` for those keys, but otherwise don't.

### Data Privacy Considerations

Our app deals with user-generated content (potentially personal videos/audio). Consider the following to protect user privacy:

- **User Consent:** Make sure the user explicitly grants permission for camera/microphone (we do via system prompts). If you record audio/video in background (not in our scenario, but if), you must notify the user (in many jurisdictions, recording without indicator is illegal; iOS provides the red bar/icon when mic is in use).
- **Privacy Policy:** Clearly state what you do with the recordings. If they are just stored to the user’s own S3, say that. If any data is shared or used for analytics, disclose it.
- **Deleting Data:** Provide a way for users to delete their recordings, both locally and on cloud. If a user uninstalls the app, any uploaded files remain in S3 unless you have server logic to delete them after some time. You may consider implementing a retention policy (e.g., auto-delete after X days if that makes sense) or an in-app "Delete from cloud" button per file.
- **Handling Sensitive Info:** If recordings might capture sensitive info (faces, voices), ensure that they are not accessible by other users. Our approach using private S3 objects achieves that (each user has their own space).
- If you allow sharing a recording (not in scope, but possible extension), be careful to generate a controlled URL (like a short-lived presigned URL) rather than making the object public permanently.
- **Compliance:** If targeting global audience, think of GDPR (EU) or other regulations. Users might request their data be deleted. Since data is on S3, you'd have to delete their files if requested. Having a structured way to list and remove all of a user's files is part of compliance (Amplify Storage list can get all keys for a user if they used a particular prefix).
- **Logging and Metadata:** Avoid sending any recording content or user info in logs. E.g., our logs print file paths – those might contain a user identifier if we include one in path, so be cautious if uploading logs to a service.
- **Encryption (again):** If especially sensitive (e.g., health or legal data), client-side encrypt to ensure even if cloud is breached, content is safe. We discussed this earlier.

- **On-Device Privacy:** The recordings on the device are in app storage, not accessible to other apps (unless the device is rooted or someone connects via USB and device allows browsing app storage). For extra safety, one could store in encrypted form on device as well, but that is rare for media due to complexity. iOS by default encrypts app sandbox when device is locked (if the app data protection is default), so that's some level of on-device encryption.

By following these practices, you reduce the risk of unauthorized access or leaks and align with security standards. Remember that security is an ongoing process: keep dependencies updated (e.g., if AWS SDK has a security fix, update it), and respond to new threats as they emerge.

---

## Conclusion

In this guide, we covered the end-to-end process of building a React Native app with advanced features:

- We set up the project with the right tools and libraries.
- Implemented video recording via `react-native-camera` and audio recording via `react-native-audio-recorder-player`, handling permissions appropriately for both Android and iOS.
- Managed the recorded files locally, storing them and preparing them for upload.
- Integrated AWS S3 using Amplify, enabling uploads of large files with progress tracking and handling errors robustly.
- Added improvements like media compression to save bandwidth, background upload capability for better UX, and optional encryption for security.
- Discussed how to test the app thoroughly and deploy it to app stores.
- Emphasized security and privacy best practices to protect user data and credentials throughout the process.

By following the steps and code examples provided, you should be able to implement a production-grade solution for capturing audio/video in a React Native app and storing it on AWS S3. Use the code snippets as a starting point, and refer to the cited resources for deeper understanding of specific topics or troubleshooting.

**References:**

- React Native Camera Documentation – explains usage of RNCamera for capturing media ([Work in progress · React Native Camera](https://react-native-camera.github.io/react-native-camera/docs/api#:~:text=takeVideo%20%3D%20async%20%28%29%20%3D,recordOptions)).
- React Native Audio Recorder Player Documentation – shows how to start and stop audio recordings, including permission notes.
- AWS Amplify Storage Documentation – example of uploading with progress monitoring and using the library in React Native.
- Instamobile Tutorial on S3 Uploads – practical example of integrating Amplify in a React Native app.
- React Native Compressor – library for media compression, used to compress video files similarly to WhatsApp ([react-native-compressor - npm](https://www.npmjs.com/package/react-native-compressor#:~:text=const%20result%20%3D%20await%20Video,)).
- React Native Background Upload – library that enables uploading files in the background on iOS/Android.
- AWS Security Blog – best practices like blocking public access and enabling encryption on S3.
- ServerFault discussion on S3 encryption – stresses the importance of client-side encryption for sensitive data ([amazon web services - Aws S3 encryption. Why use it? - Server Fault](https://serverfault.com/questions/931326/aws-s3-encryption-why-use-it#:~:text=With%20that%20said%2C%20if%20you,free%20to%20do%20so%2C%20right)).
- AsyncStorage documentation and limits – notes on using AsyncStorage for small data only (around 6MB on Android) ([Increase Android AsyncStorage Size in React Native - Code Daily](https://www.codedaily.io/tutorials/Increase-Android-AsyncStorage-Size-in-React-Native#:~:text=The%20iOS%20AsyncStorage%20implementation%20has,size%20of%20AsyncStorage%20is%206MB)).

Using these references and following the structured approach in this guide, you can build and scale a robust media recording and upload application. Happy coding!
