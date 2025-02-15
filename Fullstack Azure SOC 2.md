# Introduction to Technologies & SOC 2 Compliance

## Overview of ReactJS, Spring Boot, MySQL, and Azure

**ReactJS:** React is a popular **JavaScript library for building user interfaces** ([React | Meta Open Source](https://opensource.fb.com/projects/react/#:~:text=React%20is%20a%20JavaScript%20library,for%20building%20user%20interfaces)). It enables developers to create reusable UI components and manage application state efficiently. React's declarative nature makes it straightforward to design interactive UIs, and its component-based architecture encourages modular and maintainable code. By using React, developers can build rich single-page applications (SPAs) that provide a smooth user experience without full page reloads. Advanced features like the virtual DOM allow React to update UI components efficiently in response to data changes.

**Spring Boot:** Spring Boot is an **open-source Java-based framework used to create microservices and standalone web applications**. It is part of the Spring ecosystem and is designed to simplify the setup of new Spring projects. With Spring Boot's autoconfiguration and “starter” dependencies, developers can get a production-ready application off the ground quickly, without lengthy XML configurations. Spring Boot applications typically embed a web server (e.g., Tomcat or Jetty) and come with production-ready features like health checks and metrics via the Actuator module. This makes Spring Boot a strong choice for backend development, especially in a microservices architecture where each service is lightweight and specialized.

**MySQL:** MySQL is the world’s most popular **open-source relational database management system (RDBMS)**. It stores data in structured tables and supports SQL for querying and managing data. Known for its reliability, performance, and scalability, MySQL is used in many high-traffic applications (e.g., Facebook, Netflix). For developers, MySQL offers ACID-compliant transactions, strong consistency, and support for joins and complex queries. In our full-stack application, MySQL will serve as the primary datastore for persistent information. We'll interact with it through Spring Data JPA (an abstraction over Hibernate) in the Spring Boot backend, allowing us to perform CRUD operations using repository interfaces instead of hand-written SQL.

**Microsoft Azure:** Azure is a comprehensive **cloud computing platform** by Microsoft, offering infrastructure, platform, and software services on a global network of data centers. Azure manages and maintains the underlying hardware and networking, so developers can focus on building applications. It provides services for virtually every need – virtual machines, containers (AKS), databases (Azure Database for MySQL), identity management (Azure AD), monitoring (Azure Monitor/Application Insights), and more. We will leverage Azure to deploy our application in a secure, scalable manner. Azure has strong support for hybrid cloud scenarios and boasts the most industry certifications among cloud providers, making it a suitable choice for building compliant applications. Key Azure services we’ll use include Azure App Service (to host our web frontend and API), Azure Database for MySQL (a managed MySQL database), and Azure Key Vault (for secrets management).

## SOC 2 Compliance Requirements (Security, Availability, Confidentiality)

**SOC 2 Overview:** SOC 2 is a compliance standard established by the AICPA for service organizations to demonstrate that they properly manage customer data. It is built around five **Trust Services Principles**: **security, availability, processing integrity, confidentiality, and privacy**. Not all principles are required for every SOC 2 report – **Security** (also called Common Criteria) is the only mandatory principle, while the others are included as needed based on the organization's services. In this guide, we will focus on the **Security**, **Availability**, and **Confidentiality** principles, as they are most relevant to a full-stack application deployment on Azure handling customer data. (Processing Integrity and Privacy are important too, but might depend on specific data processing and personal data considerations beyond our scope.)

- **Security:** The security principle is about protecting the system against unauthorized access (both physical and logical). Compliance with this principle involves implementing measures such as access controls, two-factor authentication, encryption of data in transit and at rest, network firewalls, etc., to safeguard data and systems. For our application, this means we will enforce strong user authentication, proper authorization checks, secure coding practices (to prevent common vulnerabilities like XSS or SQL injection), and encryption for data storage and transfer. We will also need to maintain audit logs and monitoring to detect and respond to any unauthorized access attempts. The Security principle under SOC 2 includes over 30 criteria covering aspects of risk management, system components monitoring, and incident response.

- **Availability:** The availability principle ensures the system is **operational and accessible** as agreed or expected by customers. It covers whether the services are up and running and also includes disaster recovery and backup provisions. To comply, our application must have mechanisms for high availability (redundancy, failover, scalable infrastructure) and a disaster recovery plan (regular backups of the MySQL database, the ability to restore service after an outage). For example, **criteria A1.2** in SOC 2 availability is about having environmental protections, data backup processes, and recovery infrastructure to meet objectives. On Azure, we can utilize features like multiple instances behind a load balancer, auto-scaling, Azure's uptime SLA, and geo-redundant backups for the MySQL database to satisfy this principle.

- **Confidentiality:** The confidentiality principle is about protecting **sensitive information** from unauthorized disclosure. In practice, this involves encryption, strict access controls, and data masking as needed for any confidential data (e.g. customer secrets, business data, personally identifiable information). Our application should ensure that confidential data (like user credentials, personal details, or proprietary business data) is encrypted in the database, not exposed in logs, and only accessible to authorized roles in the system. For instance, **criteria C1.1** requires identifying and maintaining confidential information, and C1.2 requires its secure disposal when no longer needed. We will use Azure Key Vault for managing secrets (like encryption keys, database passwords) and ensure all network communication is over TLS. Additionally, role-based access control in both the application and Azure resources will help guarantee that only authorized personnel or services can access confidential information.

**Why SOC 2 Matters:** Adhering to SOC 2 guidelines is crucial for building customer trust and meeting industry requirements. It not only influences how we design and implement security controls in our app, but also how we document and maintain them. SOC 2 compliance will require us to **establish formal policies and procedures**. For example, we'll need an **Access Control Policy** defining how user and developer access is managed, a **Disaster Recovery Plan** outlining steps to recover from outages, and an **Incident Response Plan** detailing how to handle security incidents. Throughout this guide, we will highlight points that contribute to SOC 2 compliance, ensuring that by the end, we not only have a working full-stack application but one that is **“audit-ready”** with proper security and governance in place.

---

# Project Setup

In this chapter, we’ll set up the foundation of the project. This includes preparing the development environment, creating code repositories with proper version control strategies, and configuring continuous integration/continuous deployment (CI/CD) pipelines. By the end of this section, you will have a scaffold for your project where both the frontend (React) and backend (Spring Boot) can be developed and deployed in a structured, team-friendly way. We’ll also ensure that from the get-go, our setup aligns with SOC 2 best practices (for example, controlling access via Git and documenting our deployment processes).

## Setting Up the Development Environment

Before coding, make sure your development environment is ready with all necessary tools and prerequisites:

1. **Install Node.js and npm:** React is a JavaScript library, so you'll need Node.js (which includes npm, the Node package manager). Download and install the **LTS (Long Term Support) version of Node.js** from the official site. Verify the installation by running:

   ```bash
   node --version
   npm --version
   ```

   This guide assumes you have Node.js version 18.x or later. Having Node allows you to use tools like Create React App or Vite to bootstrap the frontend, and npm (or yarn) to manage JavaScript dependencies.

2. **Install Java JDK:** Spring Boot runs on Java. Install **JDK 17 (or later)**, since Spring Boot 3.x requires Java 17+. OpenJDK or Oracle JDK are fine; ensure the `JAVA_HOME` environment variable is set. Verify Java by:

   ```bash
   java -version
   ```

   You should see the installed version (e.g., "Java 17.0.x"). We will use Maven (and/or Gradle) for building the Spring Boot application, which typically comes with the Spring Boot initializer.

3. **Set up MySQL:** For development, you can install MySQL Community Server locally or run MySQL in a Docker container. Alternatively, use a lightweight option like MariaDB or an embedded database for initial development, then switch to MySQL for production. If installing MySQL locally, also install a MySQL client or admin tool (MySQL Workbench, TablePlus, or even the `mysql` CLI) to inspect the database. Create a database schema for your app (e.g., named `myapp_dev`) and a dedicated user (e.g., `myapp_user`) with a strong password and appropriate privileges on that schema. This mimics the principle of least privilege: the app's DB user should only have access to its own schema.

4. **Development IDE/Tools:** Choose your preferred IDE or text editors:

   - For React: **Visual Studio Code** is a popular choice, with useful extensions for React and JavaScript/TypeScript. Extensions like ESLint and Prettier help maintain code quality.
   - For Spring Boot: **IntelliJ IDEA** (Community or Ultimate) or **Eclipse** or **VS Code with Java extensions**. IntelliJ has excellent Spring integration and will help with things like code navigation and application configuration.
   - Install relevant plugins, such as the Azure Account extension if using VS Code (to interact with Azure services), or the Docker extension if you plan to containerize the app.

5. **Node/Java Project Generators:**

   - **Bootstrapping React App:** Use Create React App (CRA) or Vite to set up the initial React project structure. For example, with CRA you can run:
     ```bash
     npx create-react-app frontend --template redux-typescript
     ```
     This creates a React project in the `frontend` directory (we're using a template that includes Redux and TypeScript for an advanced setup; you can omit the template or choose another as needed).
   - **Bootstrapping Spring Boot App:** Use the Spring Initializr (start.spring.io) to generate a new Spring Boot project. Select **Maven** (or Gradle), Java, Spring Boot version 3.x. Add the following dependencies: Spring Web, Spring Security, Spring Data JPA, MySQL Driver, Spring Boot Actuator. You can also add OAuth2 Resource Server if available, or we can add it manually. Generate the project and download the zip. Unzip it into a directory named `backend` (for example). This gives you a Maven project with a ready-to-run Spring Boot application.

6. **Directory Structure:** If you’re using a single repository (monorepo) for both frontend and backend, arrange your directories like so:

   ```
   project-root/
     README.md
     frontend/   (React app)
     backend/    (Spring Boot app)
     infra/      (optional, for infrastructure-as-code scripts like Terraform or deployment manifests)
   ```

   Using a monorepo can simplify coordination (one place to commit code), but you could also use separate repositories for frontend and backend if that suits your team. Monorepo vs multi-repo is a matter of preference; a monorepo makes it easier to tag a single version that includes both front and back, whereas separate repos might align better if the frontend and backend are maintained by different teams or have different release cycles. In either case, ensure your **version control strategy** is clear (we discuss Git workflows next).

7. **Testing Tools:** Install any necessary testing frameworks:
   - For React: the project setup (CRA) includes Jest for unit tests. You might add React Testing Library for component testing.
   - For Java: JUnit and Mockito (Spring Boot includes JUnit by default). Ensure you can run `mvn test` successfully in the backend and `npm test` in the frontend.
   - Considering compliance, having automated tests (especially security tests) can be part of your control set (e.g., to ensure no critical vulnerabilities are introduced).

With these steps, your development environment is ready. We have separate development servers for frontend (`npm start` will run a dev server on, say, http://localhost:3000) and backend (`./mvnw spring-boot:run` runs the Spring Boot app on http://localhost:8080 by default). In development, you’ll likely deal with CORS (Cross-Origin Resource Sharing) issues when the React app calls the API; we will handle that in the coding sections.

Also note that at this stage, it's good to set up **source control ignore files** (`.gitignore`) for Node modules, build outputs, IDE config, etc., to avoid committing unnecessary files.

## Creating Repositories and Configuring Git Workflows

Using a **version control system** like Git is essential for collaboration, tracking changes, and maintaining a history of your project (also important for change management in compliance). We will create repositories for our code and set up a branching strategy.

1. **Initialize Git Repositories:**

   - If using a monorepo, initialize a single git repository at `project-root` (with `git init`), add all files, and make the first commit (e.g., "Initial commit: React and Spring Boot skeleton").
   - If using separate repos for `frontend` and `backend`, initialize each separately, or create them via GitHub/Azure DevOps and clone them. The separation can be beneficial if, for example, you want to deploy front and back independently or if they have different lifecycles. But it adds complexity in synchronizing changes. For this guide, we will assume a **single repository**, which simplifies the CI/CD setup (one pipeline can build and deploy both components).

2. **Remote Repository (GitHub or Azure Repos):** Create a remote repo on GitHub (or your preferred git hosting, e.g., GitLab or Bitbucket). If you use Azure DevOps, you can create a Project and use **Azure Repos** (which is basically git) within it. Once created, add the remote (e.g., `git remote add origin <repo URL>`) and push the main branch.

3. **Branching Strategy:** We recommend a **trunk-based development** approach for simplicity and speed, especially for a small team of advanced developers. This means using a main branch (often `main` or `master`) where all production-ready code lives, and developers create short-lived feature branches for changes. Feature branches are merged back into main via pull requests after review. Trunk-based development encourages continuous integration and avoids long-lived divergent branches. (An older model is GitFlow, with develop/release/hotfix branches, but GitFlow is considered more complex and “legacy” now, and can complicate CI/CD.)

   - Create a `main` branch (if not already `master` by default) for production-ready code.
   - Protect the `main` branch: require pull request approval for merges, and perhaps CI passing checks. This ensures code is reviewed (which is good for both code quality and compliance evidence).
   - Developers will branch from `main` to implement features or fixes (e.g., `feature/user-auth` or `bugfix/login-redirect`), then open a PR.
   - Optionally, maintain a `develop` branch if you want an integration branch, but with CI and small PRs, it's often fine to commit to main behind feature flags (for incomplete features).

4. **Git Hooks and Secrets:** Set up **pre-commit hooks** or **continuous integration checks** for linting and tests to enforce quality. For example, a pre-commit hook could run `npm run lint` and `mvn verify` to ensure no lint errors or failing tests are introduced. You can use tools like Husky (for Node) to manage Git hooks. Also, never commit secrets or credentials to the repository – we will use Azure Key Vault and environment configurations for that. Use a tool or Git hook (like a secret scanner) to detect and prevent committing secrets by accident.

5. **Documentation in Repo:** Create a `README.md` at the root of the repository. Document how to set up and run the app locally, the technologies used, etc. This is not only helpful for team onboarding but can serve as evidence of a well-documented process in an audit (e.g., showing that developers have instructions to follow security practices when running the app). Also consider maintaining a `CHANGELOG.md` to record notable changes per release (useful for tracking what changed for compliance and communication).

6. **Access Control in Git:** Ensure that only authorized developers have access to the repository (especially important for compliance). If using a platform like GitHub, use organization controls or GitHub teams to limit who can push to the repo. On Azure DevOps, manage project access through Azure AD groups. This ties into SOC 2 security – code is an asset and should be protected. Enforce 2FA on the Git platform accounts and consider using commit signing to verify authorship of commits.

At this point, your codebase is under version control, and the team workflow is established. All changes will be tracked, which is good for accountability. Next, we will integrate Continuous Integration and Continuous Deployment (CI/CD) to automate building, testing, and deploying our application.

## Setting Up CI/CD Pipelines in Azure DevOps or GitHub Actions

A robust CI/CD pipeline ensures that every code change is built, tested, and deployed automatically or with minimal manual steps. This not only speeds up development but is also crucial for SOC 2 (change management controls, reducing human error, and providing an audit trail of deployments). We will outline using Azure DevOps Pipelines and GitHub Actions (both are popular and can achieve similar goals). The choice often depends on your organization's ecosystem. For illustration, let's use **Azure DevOps** pipelines for a comprehensive enterprise-ready setup, but note how to do similar in GitHub.

**1. Azure DevOps Project Setup (if using Azure DevOps):** If you created a project in Azure DevOps and a repo there, navigate to Pipelines and create a new pipeline. Azure DevOps can detect a `azure-pipelines.yml` in your repo, or you can use the visual editor. We'll write a YAML pipeline as code for version control.

**2. CI Pipeline (Build and Test):** The first stage is continuous integration – build and test both frontend and backend on every push (or at least every PR and merge to main).

Create a file `azure-pipelines.yml` at the root of your repo with contents like:

```yaml
trigger:
  branches:
    include:
      - main # build main branch automatically; you can add others or PR triggers

jobs:
  - job: BuildAndTest
    displayName: "Build and Test Frontend and Backend"
    pool:
      vmImage: "ubuntu-latest" # Use a Microsoft-hosted Linux agent
    steps:
      - checkout: self

      - task: NodeTool@0 # Install Node.js on the agent
        inputs:
          versionSpec: "18.x" # Ensure we have Node.js (for building frontend)

      - script: |
          cd frontend
          npm install             # Install frontend dependencies
          npm run build           # Build the React app (production build)
        displayName: "Build Frontend"

      - script: |
          cd backend
          ./mvnw verify           # Build and run tests for backend (Maven wrapper)
        displayName: "Build & Test Backend"
        env:
          MAVEN_OPTS: "-Dmaven.test.failure.ignore=false"

      - task: PublishBuildArtifacts@1 # Save build outputs (optional, for CD)
        inputs:
          PathtoPublish: "backend/target/*.jar"
          artifactName: "backend-artifact"
      - task: PublishBuildArtifacts@1
        inputs:
          PathtoPublish: "frontend/build"
          artifactName: "frontend-build"
```

This YAML does the following:

- Checks out the code.
- Sets up Node.js and runs `npm install` and `npm run build` in the `frontend` directory, producing a production-ready build (static files in `frontend/build/`).
- Runs Maven in the `backend` directory to compile the code and run tests. The `verify` phase runs unit tests. We fail the pipeline if any test fails (ensuring code quality).
- Publishes build artifacts: the Spring Boot fat JAR (e.g., `myapp-0.0.1.jar`) and the compiled frontend static files. These artifacts can be used in a release pipeline or next stage for deployment.

In a real scenario, you might push the frontend files to a storage or CDN and the backend to an Azure service. We will handle deployment next.

With this pipeline, every commit triggers a CI build. You should see in Azure DevOps the logs of installation, compilation, and test results. This provides an audit trail of builds – e.g., you can show an auditor that all code is tested and built through an automated process, and if a build fails, it won't be deployed.

**3. CD Pipeline (Deployment):** We can define a second pipeline (or extend the above) to deploy our app to Azure. Let's consider two deployment targets:

- **Frontend**: Could be Azure Static Web Apps or an Azure Storage static site, or even served by the backend. For better separation, consider Azure Static Web Apps (which integrates well with GitHub Actions) or deploying the static files to an Azure Blob Storage with a CDN. However, to keep things straightforward, we might deploy the React build to Azure App Service as a separate site, or simply include it in the Spring Boot app (by copying files into `src/main/resources/static` so Spring Boot serves them). For an advanced setup, separate hosting is ideal.
- **Backend**: Azure App Service for Linux (with Java runtime) or Azure Kubernetes Service (if containerized). We’ll start with App Service for simplicity.

Let's say we use Azure App Service for both:

- Create an **Azure App Service** for the backend API (e.g., name: `myapp-backend`).
- Create another App Service or an **Azure Static Web App** for the frontend (e.g., `myapp-frontend`).
- Alternatively, use one App Service and serve the React files through Spring Boot (not ideal for large scale, but simpler initial deployment).

For now, assume **one App Service** that will serve the Spring Boot API. We'll handle the frontend by integrating it into the Spring Boot app (this avoids CORS in production and simplifies deployment – the React app can be built and packaged with the Spring Boot JAR). This approach means our CI pipeline should copy `frontend/build` into `backend/src/main/resources/static` before building the jar, so the jar contains the frontend. (This is a pattern some teams use: the React app becomes static resources served by Spring Boot).

If we choose that route, modify the pipeline slightly:

- Instead of publishing separate artifacts, copy the build output into backend and then build the jar:

```yaml
- script: |
    rm -rf backend/src/main/resources/static/*
    cp -R frontend/build/* backend/src/main/resources/static/
    cd backend
    ./mvnw package
  displayName: "Package Backend with Frontend"
```

This way, `target/myapp.jar` contains the frontend. Then deployment is just deploying that jar.

If instead deploying separately:

- Use Azure CLI or Azure DevOps tasks to upload `frontend/build` to a storage account (as static site) or to a second App Service.

For brevity, let's assume **packaging frontend into backend jar** approach for now. The pipeline would produce a single jar to deploy.

Now, deployment to App Service using Azure DevOps:

- In Azure DevOps, set up an Azure Resource Manager Service Connection (this connects the pipeline to your Azure subscription).
- Use the **Azure Web App Deploy** task:

```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: "<Your Service Connection name>"
    appType: "webApp"
    appName: "myapp-backend" # name of Azure App Service
    package: "backend/target/myapp.jar" # path to the JAR from the build
```

This will deploy the JAR to Azure (which essentially copies it and starts it since App Service will detect a Java SE app).

For a multi-stage YAML (CI then CD), Azure DevOps allows defining stages, for example:

```yaml
stages:
- stage: Build
  jobs:
    - job: BuildAndTest
      ... (steps as above)
- stage: Deploy
  dependsOn: Build
  condition: succeeded()
  jobs:
    - job: DeployToProd
      environment: 'production'  # Azure DevOps environment for approvals if needed
      steps:
        - download: current  # get artifacts from previous stage
          artifact: backend-artifact
        - task: AzureWebApp@1
          inputs:
            azureSubscription: 'MyAzureConn'
            appName: 'myapp-backend'
            package: '$(Pipeline.Workspace)/backend-artifact/myapp.jar'
```

You might configure **Approvals** on the Deploy stage (in Azure DevOps, if you set an Environment, you can require a manual approval before deployment). This is often a SOC 2 requirement: production deployments should be reviewed/approved. Alternatively, use branching protections (only certain people can merge to main which triggers auto deploy). Document your change management process clearly – e.g., "All production changes are deployed via pipeline X which requires PR review and approval from a tech lead."

**4. GitHub Actions (if using GitHub):** As an alternative, a GitHub Actions workflow YAML (in `.github/workflows/ci-cd.yml`) would have similar steps (checkout, setup Node, build, setup JDK, build). For deployment, GitHub has an official Azure WebApp action:

```yaml
- uses: azure/webapps-deploy@v2
  with:
    app-name: "myapp-backend"
    slot-name: "production"
    publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
```

You'd need to configure the publish profile secret from Azure (or use Azure login action with a service principal). The principles are the same. GitHub Actions also support environments and approvals.

**5. Running CI/CD:** Once configured, commit the pipeline YAML. If using Azure DevOps, the pipeline will run (or you might need to manually run the first time after setting it up). Make sure it passes. The result should be:

- On push to main, it builds and (optionally after approval) deploys to Azure.
- You should see your app running on Azure (though it might not do much yet until we develop features). You can verify the backend by hitting `https://<myapp-backend>.azurewebsites.net/actuator/health` (once we enable Actuator) or some test endpoint.
- If something fails (tests, or deploy), the pipeline stops and alerts the team.

**6. CI/CD and Compliance:** Our CI/CD setup helps with SOC 2 in multiple ways:

- **Automated Builds & Tests:** Ensures code quality and that security tests run on every change (reducing risk of introducing a vulnerability).
- **Traceability:** Every build and deployment is logged. We can trace which commit went into which deployment, and who approved it.
- **Segregation of Duties:** Developers merge code, but deployment can be gated by an approver in the pipeline, implementing a control so no single person can unilaterally push code to production without oversight.
- **Rollback Capability:** With pipelines, it's easy to redeploy a previous successful build if needed.
- **Infrastructure as Code:** The pipeline itself is code (in YAML), which is tracked and versioned. Any changes to deployment logic go through code review too.

Set up notifications for pipeline results (Azure DevOps can notify on Teams/Email on failures; GitHub can do email or integrate with Slack). Monitoring pipeline is also important: a failing build means no deployment, which could impact uptime if not noticed. But from a compliance perspective, failing builds stop bad code from going live – a safety mechanism.

Now that the project structure and DevOps pipeline are in place, we can dive into developing the frontend and backend features in the following chapters.

---

# Frontend Development with ReactJS

In this chapter, we'll build the frontend of the application using ReactJS. We'll focus on creating a well-structured project that can scale, implementing state management for complex data flows, and setting up secure authentication and API communication. The frontend is the user-facing part of our app, and it will communicate with the Spring Boot backend via REST APIs. We must also ensure the frontend is developed with security best practices in mind (e.g., handling JWTs securely, preventing XSS, etc.) to maintain our SOC 2 compliance posture on the client side.

## Project Structure and Architecture Best Practices

A clear project structure makes the codebase maintainable as it grows. We will structure our React app by feature, which is a common approach for large applications:

```
frontend/src/
├── components/        # Reusable UI components (buttons, form inputs, etc.)
├── pages/             # Page or view components, each corresponding to a route
├── services/          # API calls and integrations (e.g., Auth service, API client)
├── context/ or store/ # State management (if using Context API or Redux store)
├── hooks/             # Custom React hooks if needed
├── utils/             # Utility functions
└── App.js             # Main app component (routing setup)
```

Some best practices and patterns:

- **Keep components small and focused:** A component should ideally do one thing (e.g., a `UserList` component displays a list of users). This aligns with SOC2's emphasis on understanding the system – a clear component structure aids code reviews and security analysis.
- **Use functional components and Hooks:** We'll use React Hooks (e.g., `useState`, `useEffect`, `useContext`) for state and lifecycle management instead of older class components. Hooks lead to less verbose code and make it easier to share logic via custom hooks.
- **Routing:** Use `react-router-dom` for navigation between pages (if building an SPA). Define routes in a central location (often in `App.js` or a dedicated `Routes.js`).
- **Styling:** Use a consistent styling approach (CSS modules, styled-components, or a CSS framework like Tailwind or Material-UI). Ensure that whatever approach, you handle it consistently to avoid style conflicts. This is also a good place to note that using a UI component library that is well-tested can reduce front-end vulnerabilities (e.g., XSS from improper escaping) because the library components handle a lot for you.

Example snippet of a simple component and page:

```jsx
// File: src/pages/Dashboard.js
import React from "react";
import { UserList } from "../components/UserList";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      <UserList />
    </div>
  );
}
```

```jsx
// File: src/components/UserList.js
import React, { useEffect, useState } from "react";
import apiClient from "../services/apiClient";

export function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch users from backend API
    apiClient
      .get("/users")
      .then((response) => setUsers(response.data))
      .catch((error) => console.error("Failed to fetch users", error));
  }, []);

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name} - {user.email}
        </li>
      ))}
    </ul>
  );
}
```

In this example, `apiClient` is an Axios instance configured to call our backend (we'll set that up in the **Secure API consumption** section). The `UserList` component fetches data on mount and displays it. We would ensure that this list is only accessible to authorized users in the app (e.g., only an Admin can view all users) – that logic might be handled in the Dashboard page or via route protection.

**Architecture:** We might not need a complex flux architecture if the app is moderately sized, but for advanced scenarios, consider:

- **Container/Presentational pattern:** Where "container" components handle data fetching and state, and pass props to "presentational" components that just render UI. In our example above, `UserList` was both container (fetching data) and presentational. We could split it.
- **Atomic Design for components:** Having atoms, molecules, organisms in design system, etc., to create a consistent UI library.
- **TypeScript:** Strongly consider using TypeScript for an advanced project. It catches type errors early and makes the code more robust. Our structure can accommodate it (just use `.tsx` files and appropriate types for state and props).
- **Linting and Formatting:** Use ESLint with recommended React/JSX rules and perhaps a security plugin (eslint-plugin-security) to catch common issues. Prettier for consistent formatting.

By setting up the project structure and standards now, we ensure that as we implement features, the code remains clean. This also makes code reviews easier, which is beneficial not just for catching bugs but also for security reviews (a peer reviewer is more likely to notice a potential security issue if the code is well-organized).

## State Management (Redux, Context API)

For an advanced application, you will need to manage state that is shared across many components (e.g., the logged-in user's information, or a global notification system, etc.). There are two popular approaches:

- **Redux:** A powerful state management library that uses a single store, actions, and reducers. Redux is great for very complex state logic and debugging (with tools like Redux DevTools). However, it adds boilerplate.
- **Context API (with Hooks):** For moderate complexity, React's built-in Context API can be sufficient. Combined with the `useReducer` hook, you can get a Redux-like pattern without adding an external library.

We will demonstrate using the Context API for simplicity (and because Create React App with the Redux template might already set up Redux – if you went that route, you can stick with Redux).

**Using Context for Auth State:** We want to keep track of whether a user is logged in and their info/token. Let's create an `AuthContext`.

```jsx
// File: src/context/AuthContext.js
import React, { useState, useEffect } from "react";
import authService from "../services/authService";

export const AuthContext = React.createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // On mount, check if user is logged in (e.g., by checking a stored token or session)
    const storedUser = authService.getCurrentUser();
    if (storedUser) {
      setUser(storedUser);
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    const loggedInUser = await authService.login(credentials);
    setUser(loggedInUser);
    return loggedInUser;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

In this context provider:

- We initialize `user` to `null` and a `loading` state to track if we are checking the existing auth state (e.g., a token in local storage or cookie).
- `authService.getCurrentUser()` might look for a token in storage and return user info if token is valid (how we implement it depends on our auth approach, but maybe decode JWT or check existence).
- `login(credentials)` calls the backend (via `authService.login`, which would call our API endpoint like `/auth/login`) and returns user info + token. We then set it in context.
- `logout()` clears the token (via service) and resets context.

Wrap your app in `AuthProvider` in `index.js` or `App.js`:

```jsx
<AuthProvider>
  <App />
</AuthProvider>
```

Now any component can use `useContext(AuthContext)` to get the user and login/logout functions.

**Redux alternative:** If we chose Redux, we’d create slices for, say, `auth` and maybe other global state (e.g., an `alert` slice for notifications). Redux Toolkit greatly simplifies setting up a store with slices. For example:

```js
// authSlice.js (if using Redux Toolkit)
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import authService from "../services/authService";

export const loginThunk = createAsyncThunk(
  "auth/login",
  async (credentials) => {
    const user = await authService.login(credentials);
    return user;
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: { user: null, loading: false },
  reducers: {
    logout(state) {
      state.user = null;
      authService.logout();
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(loginThunk.rejected, (state) => {
        state.loading = false;
      });
  },
});
export const { logout } = authSlice.actions;
export default authSlice.reducer;
```

Then configure the store with this reducer and use `<Provider store={store}>` in `index.js`. Components would use `useSelector` and `useDispatch` to access state and dispatch actions.

Both approaches can achieve the needed functionality. For advanced devs, Redux gives more control and middleware (like redux-saga or redux-observable for complex async flows). Context is simpler and sufficient for many cases (especially given the use of a dedicated auth provider like MSAL which might manage its own state internally).

**Key point:** Whichever state management, ensure that sensitive data in state (like user tokens or personal data) is handled carefully:

- Do not store secrets in a way that can be easily read by malicious scripts. For example, **avoid storing JWTs in localStorage** due to XSS risk – it’s recommended to keep them in memory or in an HttpOnly cookie. We'll expand on this in the Auth section.
- If using Redux, consider using Redux Persist carefully. If you persist state to localStorage, do not persist the token or sensitive parts, or encrypt them. (However, an HttpOnly cookie approach would avoid this).
- When logging (like `console.log`), avoid printing sensitive info.

## Authentication and Authorization with OAuth2/OIDC

Authentication in a modern web app is often done via OAuth 2.0 and OpenID Connect (OIDC) if integrating with an external identity provider, or via a custom username/password system. Given our focus on security and SOC 2, using a proven identity solution is preferable to rolling our own. We will integrate with an OAuth2/OIDC provider for user authentication. This could be **Azure Active Directory (Azure AD)**, **Azure AD B2C**, **Okta**, **Auth0**, or another Identity Provider (IdP). For an Azure-focused solution, let's consider **Azure AD B2C** (which is good for customer-facing apps) or standard Azure AD if it's an internal app.

The typical OAuth2 Authorization Code flow with PKCE for a SPA looks like:

1. The user clicks "Login" in our React app.
2. The app redirects the user to the IdP login page (Azure AD, etc.) with a URL containing our app's client ID, requested scopes, redirect URI, and a PKCE code challenge.
3. The user signs in (possibly with multi-factor, etc., managed by IdP) and consents.
4. The IdP redirects back to our app’s redirect URI with an authorization code.
5. The React app (since it's a SPA and can't securely hold a client secret) uses PKCE to exchange that code for tokens (Access Token, ID Token, Refresh Token).
6. Tokens are then stored (in memory or cookie) and used for API calls (the Access Token, typically a JWT, is sent in `Authorization` header to our Spring Boot API).
7. The React app now knows the user's identity (from the ID Token) and can display user info and allow access to authorized parts of the app.

We can simplify by using a library. **MSAL (Microsoft Authentication Library) for React** is provided by Microsoft for Azure AD authentication and supports the PKCE flow out of the box. Alternatively, **OIDC Client** or **Auth0 SDK** for generic OIDC.

Let's outline using MSAL with Azure AD B2C:

- **App Registration:** In Azure AD B2C, register two applications as mentioned: one for the SPA (front-end) and one for the Web API (backend). The SPA registration will give a Client ID and specify redirect URIs (e.g., `https://localhost:3000`) and allow implicit or code flow. The API registration will define the scopes (e.g., "myapp.read", "myapp.write") that the SPA can request. Then, you **expose an API** in Azure AD (which essentially means define scopes). Grant the SPA permission to call the API. Generate a **client secret** for the API registration (which the Spring Boot backend will use to verify tokens or for calling graph API, etc., if needed).
- **MSAL Configuration in React:** Use the MSAL React library. Install with `npm install @azure/msal-browser @azure/msal-react`. Then configure it:

  ```jsx
  // File: src/authConfig.js
  import { PublicClientApplication } from "@azure/msal-browser";
  export const msalConfig = {
    auth: {
      clientId: "<SPA Client ID>",
      authority:
        "https://<tenant-name>.b2clogin.com/<tenant-id>/<B2C_Auth_Policy>/", // B2C specific authority (policy, etc.)
      redirectUri: "http://localhost:3000", // or your deployed site URL
      knownAuthorities: ["<tenant-name>.b2clogin.com"], // required for B2C
    },
  };
  export const msalInstance = new PublicClientApplication(msalConfig);
  ```

  Wrap your app with MsalProvider:

  ```jsx
  import { MsalProvider } from "@azure/msal-react";
  import { msalInstance } from "./authConfig";
  ...
    <MsalProvider instance={msalInstance}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </MsalProvider>
  ```

  Then use MSAL hooks for login:

  ```jsx
  import { useMsal } from "@azure/msal-react";
  ...
  const LoginButton = () => {
    const { instance } = useMsal();
    const login = () => {
      instance.loginPopup({ scopes: ["https://<your-api>/myapp.read"] })
        .catch(e => console.error(e));
    };
    return <button onClick={login}>Sign In</button>;
  };
  ```

  On successful login, MSAL will store the tokens in its internal cache (by default, in memory for SPAs – which is good). The `AuthProvider` we wrote can be integrated or we might rely on MSAL's context. MSAL React provides a hook `useIsAuthenticated` and `useAccount` to get user info.

- **Token Storage:** As noted, **never store tokens in localStorage** for SPAs due to XSS vulnerabilities. MSAL by default uses sessionStorage or memory for SPAs precisely to mitigate that. Another secure approach is storing the Access Token in a **HttpOnly cookie** (set by your backend during auth if doing a custom flow) so that JS cannot read it and it's automatically sent in requests. But that requires a backend component. Since we are using MSAL, it handles it in memory. The StackOverflow advice we saw: _"The preferred method is to store your JWT Token in memory: not in a cookie, and not in localstorage."_ aligns with this strategy.

- **Authorization (front-end side):** After login, you'll have an `accessToken` (JWT) with certain scopes or roles. You might decode the JWT on the client (it’s signed, so you can't alter it, but you can read claims). Based on claims like roles or permissions, you can conditionally render components. For example, if the JWT contains `roles: ["Admin"]`, show the admin menu. But always remember: front-end enforcement is just UX, real enforcement must happen in the backend. So, it's fine to show/hide buttons, but never rely on that to secure data (the API should check the token’s roles too).

- **Route Protection:** Use a `<PrivateRoute>` component or similar to guard routes:

  ```jsx
  // Example using MSAL's hook
  import { useIsAuthenticated } from "@azure/msal-react";
  import { Navigate } from "react-router-dom";

  function PrivateRoute({ children }) {
    const isAuthenticated = useIsAuthenticated();
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }
    return children;
  }
  ```

  Then in your routes config:

  ```jsx
  <Routes>
    <Route
      path="/dashboard"
      element={
        <PrivateRoute>
          <Dashboard />
        </PrivateRoute>
      }
    />
    <Route path="/login" element={<LoginPage />} />
  </Routes>
  ```

  So if not logged in, user is redirected to login page (or you could call MSAL login redirect directly).

**Implementing OAuth2/OIDC securely** gives us a few compliance benefits:

- We offload user authentication to a trusted Identity Provider (they handle password storage, MFA, account lockout policies, etc., which are all things auditors care about for security).
- We use standard libraries and flows (less custom security code that could have bugs).
- We keep tokens secure (memory or HttpOnly cookies) and use short-lived access tokens with refresh tokens (MSAL will handle token refresh under the hood).

If not using Azure AD, a similar approach with Auth0 or Okta would be done. For instance, Auth0 provides an SDK that does the PKCE flow and returns tokens.

We should also mention for completeness: the **backend (Spring Boot) will be configured to accept these JWT tokens** (see the backend section). Azure AD tokens will have a public key for validation and we can configure Spring Security with the issuer and audience so it knows how to parse them.

**Summary:** The React front-end will use an OAuth2 Authorization Code flow with PKCE for user sign-in, likely via a library like MSAL. The result is we get an ID token for identity (if needed) and an access token (JWT) that we will include in API calls. We'll manage the login state in our React context or MSAL's context, and ensure that no sensitive tokens are exposed to potential attackers (in memory only). This setup lays a strong foundation for a secure front-end authentication.

## Secure API Consumption (CORS, HTTPS, JWT Handling)

Now that our front-end can obtain a JWT access token after authentication, we need to use it to call the secure backend APIs. Here are the key considerations to consume the backend API securely:

- **Base URL and Environment Config:** Define the API base URL in a config file or environment variable. For example, in development it might be `http://localhost:8080/api`, and in production an Azure domain. If using Create React App, you can have a `.env.development` and `.env.production` with `REACT_APP_API_URL=` values. This prevents scattering base URLs in code and allows easy reconfiguration (and it keeps sensitive info like endpoint addresses out of code if needed).
- **CORS (Cross-Origin Resource Sharing):** During development, you'll access the API on a different origin (port 8080 vs 3000). The backend must allow the front-end origin. We'll configure Spring Boot to permit our dev origin for specific routes. In production, if we serve the React app and API from the same domain (e.g., same App Service), CORS is not an issue because the requests are same-origin. However, if frontend is on a different domain (like a static site on a CDN and API on api.myapp.com), we must enable CORS for that domain.

  - On the React side, if using a different domain for API, you will call the full URL in fetch/axios.
  - We will set appropriate CORS headers on the server. In Spring Boot, one can use the `@CrossOrigin` annotation on controllers or a global CORS config via a `WebMvcConfigurer` bean. We'll do it globally for our API endpoints.

  Example Spring CORS config (to be placed in backend code):

  ```java
  import org.springframework.context.annotation.Bean;
  import org.springframework.web.servlet.config.annotation.CorsRegistry;
  import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

  @Bean
  public WebMvcConfigurer corsConfigurer() {
      return new WebMvcConfigurer() {
          @Override
          public void addCorsMappings(CorsRegistry registry) {
              registry.addMapping("/api/**")
                      .allowedOrigins("http://localhost:3000", "https://myappfrontend.example.com")
                      .allowedMethods("GET", "POST", "PUT", "DELETE")
                      .allowedHeaders("Authorization", "Content-Type")
                      .allowCredentials(true);
          }
      };
  }
  ```

  This means any request to paths under `/api/` will accept requests from our front-end origin(s). We include `Authorization` in allowed headers so the JWT header isn't blocked. `allowCredentials(true)` if we were using cookies for auth (with JWT it's not needed unless using cookie).

- **HTTPS:** Always use HTTPS in production for all API calls. Azure App Service provides a free TLS endpoint (yourapp.azurewebsites.net is HTTPS by default). If using a custom domain, configure App Service or Azure Front Door with an HTTPS certificate. In development, it's okay to use http for localhost. But never send tokens over plain HTTP in production – that would violate the Security principle (encryption in transit is a must). We can enforce HTTPS in the App Service config and also code (Spring Boot can be set to `server.ssl.enabled=true` if you have a cert, or easier, just rely on Azure's TLS).

- **Including JWT in Requests:** When calling the API, include the JWT access token in the **Authorization header** as a Bearer token. For example, using Axios:

  ```js
  // src/services/apiClient.js
  import axios from "axios";
  import { msalInstance } from "../authConfig"; // if using MSAL
  const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:8080/api",
  });
  // Add a request interceptor to include the token
  apiClient.interceptors.request.use(
    async (config) => {
      const accounts = msalInstance.getAllAccounts();
      if (accounts.length > 0) {
        const account = accounts[0];
        const response = await msalInstance.acquireTokenSilent({
          scopes: [
            "https://<your-api>/myapp.read",
            "https://<your-api>/myapp.write",
          ],
          account: account,
        });
        const token = response.accessToken;
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  export default apiClient;
  ```

  Here we use MSAL to get the token (it will renew it if expired via `acquireTokenSilent`). We attach `Authorization: Bearer <token>` to every request. If not using MSAL, and you had your own AuthContext storing the token, you'd retrieve it from context and set the header.

- **Error Handling (401/403):** We should handle HTTP 401 (Unauthorized) or 403 (Forbidden) responses globally. If the backend says the token is invalid or expired (401), we might trigger a re-login. If 403, the user is authenticated but not allowed to do that action (we might show an error message). With Axios, we can add a response interceptor:

  ```js
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        // Token might be expired or invalid
        // Option: trigger a silent token refresh or redirect to login
        // For MSAL, you might call login again or clear state
        console.warn("Unauthorized, redirecting to login.");
        window.location.href = "/login"; // simple approach to re-auth
      }
      return Promise.reject(error);
    }
  );
  ```

- **Secure Data Handling:** When the data comes back from the API, be mindful of how you use it. React automatically escapes content in JSX, which protects against injection attacks by default. But if you dangerously set HTML, ensure the data is safe. Also consider content security policy (CSP) meta tags to restrict what external scripts or resources can load in your app, as an added security layer.

- **Preventing Sensitive Data Exposure in Frontend:** The frontend should never receive more data than necessary. For instance, if an API returns user objects, maybe it should not include sensitive fields (like a password hash or a security answer even if hashed). Ensure the backend only sends what's needed (principle of least privilege, again). This way, even if the front-end code has a bug or is tampered, the data exposure is limited.

- **Testing API Calls:** During development, use the browser's dev tools network tab to confirm:

  - The Authorization header is present in requests.
  - The requests to the API have status 200 and expected data.
  - No CORS errors (if you see CORS errors in console, adjust the backend CORS config accordingly).
  - If any request is going over http (inadvertently), fix it to https.

- **Audit Logging on Frontend:** While most logging for compliance is on backend, sometimes having some telemetry on the front-end is useful (e.g., using Application Insights in the front-end to track user behavior or errors). If using Application Insights, ensure no personal data or secrets are accidentally logged from the front-end. It's more of a privacy concern than security, but relevant if Privacy principle was in scope.

By following these steps, the React app will securely communicate with the Spring Boot API:

- We configured proper CORS so the dev environment works.
- We always use HTTPS in production.
- We attach JWTs to authenticate requests.
- We handle errors gracefully (which could also trigger user re-authentication if needed).

This covers the front-end development portion. The next chapter will focus on building out the backend services with Spring Boot, where we'll enforce the security on the server side (actually validating those JWTs and applying authorization rules) and implement the business logic and data access.

---

# Backend Development with Spring Boot

Now we turn to the backend, built with Spring Boot. The backend will expose RESTful APIs consumed by our React frontend. It will handle business logic, interact with the MySQL database, enforce security (authentication/authorization), and integrate with infrastructure (like logging and monitoring). We aim to structure the backend well (possibly as microservices or a modular monolith), implement secure endpoints with Spring Security and OAuth2, manage data using Spring Data JPA, and set up robust logging.

## Project Structure and Microservices Architecture

Our Spring Boot application can be organized in a standard layered architecture (which works whether you have one service or multiple microservices):

```
backend/src/main/java/com/yourorg/yourapp/
├── YourAppApplication.java        # Main class with main() to start Spring Boot
├── config/                        # Configuration classes (Security config, CORS, etc.)
├── controllers/ (or resources/)   # REST controllers
├── services/                      # Service classes (business logic)
├── repositories/                  # Repository interfaces for JPA
├── models/ (or entities/)         # JPA entity classes and possibly DTOs
└── util/                          # Utility classes (e.g., for logging or common helpers)
```

If splitting into microservices, you might have separate modules or projects for each service, each with a structure like above. For example, a `user-service`, `order-service`, etc. They could communicate via REST or messaging. However, microservices add complexity (service discovery, inter-service auth, etc.). If this is one cohesive application, a single service with modules is fine for now.

**Domain-Driven structure**: If the project is complex, consider organizing by feature/domain rather than purely layer. E.g., `com.yourorg.yourapp.user` package containing sub-packages for model, repo, service, controller related to user management. This can make it easier to eventually split into microservices.

**Microservices considerations:** For SOC 2, microservices can isolate data (e.g., a service that handles sensitive data can be locked down separately). But they require securing each service's communication. A simpler approach is a monolith behind an API. In this guide, we'll implement as a single Spring Boot app with clear module boundaries, which can later be separated if needed.

## Implementing Secure REST APIs with Spring Security & OAuth2

Security is a critical part of our backend. We will use **Spring Security** to secure our REST endpoints and integrate with our OAuth2 authentication mechanism.

**1. Add Spring Security and OAuth2 dependencies:** In `pom.xml`, ensure we have:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

Also, depending on the OAuth2 provider, we might add `spring-boot-starter-oauth2-client` if Spring Boot needed to act as a client (for calling other APIs), but for just validating JWTs, the resource server starter is enough. These will pull in Spring Security core and support for JWT validation.

**2. Configure Spring Security:** By default, Spring Security locks down all endpoints (requires authentication for all). We need to configure:

- How to authenticate (in our case, as a resource server that expects JWT bearer tokens).
- What authorization rules (which roles can access which endpoints).
- CORS and CSRF settings for stateless APIs.

Create a security configuration class, e.g., `SecurityConfig.java`:

```java
package com.yourorg.yourapp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .cors(Customizer.withDefaults())   // use our CorsConfiguration source (set elsewhere)
            .csrf(csrf -> csrf.disable())      // disable CSRF for APIs (using JWT, not cookies)
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/admin/**").hasRole("ADMIN")   // example: admin endpoints
                .requestMatchers("/api/public/**").permitAll()       // public endpoints (if any)
                .anyRequest().authenticated()                        // all other endpoints require auth
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(Customizer.withDefaults())  // validate JWT tokens on requests
            );
        return http.build();
    }
}
```

Let's unpack this:

- We enabled CORS (`cors()`) – it will use a bean of type `CorsConfigurationSource` if we define one, or globally applied config as per earlier `WebMvcConfigurer`. This ensures the Security filter chain knows to apply CORS.
- CSRF is disabled because we are not using cookies for auth (our API is stateless with JWT). CSRF protection in Spring is mainly to protect form login sessions; for JWT, it's common to disable it. (If we ever allowed cookies with session, we'd keep CSRF and use tokens).
- Authorization rules:
  - We say any URL under `/api/admin/` requires the user to have role `ADMIN`. Spring Security will look at the JWT's "roles" claims (which typically map to `ROLE_ADMIN` in Spring's context). Azure AD for instance might put roles in `roles` claim. We need to ensure those map – by default, Spring Security’s JWT converter may map `roles` claim to authorities like `ROLE_<value>`.
  - We allow `/api/public/**` without auth (e.g., health check or a status page).
  - All other endpoints need authentication (user must be logged in with a valid JWT).
- We configure this app as an **OAuth2 Resource Server** with JWT. This means Spring Security will:
  - Expect an `Authorization: Bearer <token>` header on incoming requests.
  - Verify the JWT’s signature and validity. We need to tell it the issuer or the public key.
  - If valid, it will set the `Authentication` in the security context with the user’s details (principle, authorities).

**3. JWT Validation Configuration:** In `application.yml` or `application.properties`, set the issuer or JWK set URI for our tokens. For example, if using Azure AD:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/<tenantId>/v2.0
          # alternatively, jwk-set-uri: https://<domain>/.well-known/openid-configuration/jwks
```

When you supply `issuer-uri`, Spring Security will automatically discover the token signing keys from the IdP’s metadata (as described in Spring docs). It will:

- Fetch the OIDC discovery document from Azure AD (`.well-known/openid-configuration` for your tenant).
- Get the JWKS (JSON Web Key Set) URL, fetch the public keys.
- Use them to validate signature of incoming JWTs (and cache them).
- Check the `iss` claim matches the issuer, and `aud` (audience) likely matches the client ID or API identifier you set. (If needed, you can configure the audience too.)

This means, with just those properties and the filter chain config above, **Spring Boot will handle JWT auth automatically**. If a request has a valid token, the request proceeds to controller; if not, it returns 401.

**4. Role/Scope Mapping:** Depending on the IdP, you might get user roles in a claim. Azure AD B2C can include custom roles or permissions in tokens, Okta might put groups, Auth0 could put scopes. Spring Security by default maps the JWT's `scope` or `scp` claims to authorities like `SCOPE_read`. But we want role-based. You might need a custom converter if roles are in a custom claim.
For example, to map an `roles` claim to Spring authorities:

```java
@Bean
public JwtAuthenticationConverter jwtAuthConverter() {
    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(jwt -> {
        Collection<GrantedAuthority> authorities = new ArrayList<>();
        List<String> roles = jwt.getClaimAsStringList("roles");
        if (roles != null) {
            for (String role : roles) {
                authorities.add(new SimpleGrantedAuthority("ROLE_" + role));
            }
        }
        return authorities;
    });
    return converter;
}
```

Then in the security config:

```java
.oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter())));
```

This ensures our `hasRole("ADMIN")` works if the JWT contains `"roles": ["ADMIN"]` for instance.

**5. Define REST Controllers:** Now implement our API endpoints. For example, a UserController:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping
    public List<UserDto> getAllUsers() {
        return userService.getAllUsers();
    }

    @GetMapping("/me")
    public UserDto getCurrentUser(Authentication auth) {
        // 'auth' will be a JwtAuthenticationToken if JWT, which we can cast or use directly
        String userId = auth.getName(); // default is sub claim or something unique
        return userService.getUserById(userId);
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public UserDto createUser(@RequestBody CreateUserRequest request) {
        return userService.createUser(request);
    }
}
```

Key points:

- `@RestController` makes it a REST endpoint returning JSON (because of Spring Boot's autoconfig of Jackson).
- We protect sensitive endpoints either via method-level security (`@PreAuthorize`) or via the config we did:
  - In config, we said `/api/users/**` requires auth (didn't specifically restrict to roles, except admin for certain pattern). We might want normal users to GET their own info but not others, etc. Fine-grained checks might be done in code using the Authentication object or using PreAuthorize with SpEL (Spring Expression Language).
  - E.g., `@PreAuthorize("#id == authentication.name or hasRole('ADMIN')")` on a method to allow the user or admin.
- The `Authentication auth` parameter is auto-injected by Spring to controllers – it holds the JWT details if needed.
- The service layer (UserService) would implement `getAllUsers`, etc., using `UserRepository` (JPA) to fetch from MySQL.
- Data transfer objects (DTOs): It's wise not to directly expose JPA entities to the outside, especially if they have sensitive fields or lazy relationships. Use DTOs to control what's sent. E.g., `UserDto` might have `id, name, email` but not `passwordHash`.

**6. Protecting Sensitive Endpoints:** Suppose we have an Admin endpoint:

```java
@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")  // all methods here require ADMIN
public class AdminController { ... }
```

This ensures only ADMIN role can access any method. We also should double-check that in our token issuance, only intended admin users get that role. With Azure AD, that could mean only users in a certain AD group, etc.

**7. Input Validation:** Use Spring's validation (JSR 303 annotations like @NotNull, @Email, etc.) on request payloads where appropriate. For example, in CreateUserRequest DTO:

```java
public class CreateUserRequest {
    @NotBlank
    private String name;
    @Email
    private String email;
    @Size(min=8)
    private String password;
    // getters, setters
}
```

Then in controller method, add `@Valid` and it will automatically return 400 Bad Request if validation fails:

```java
public UserDto createUser(@Valid @RequestBody CreateUserRequest request) { ... }
```

This is part of secure coding – never trust input. Validation can prevent some attacks (e.g., extremely long input that could cause DoS, or improper format that could break queries though with JPA that's handled).

**8. Exception Handling:** Implement a global exception handler (`@ControllerAdvice`) to translate exceptions to proper HTTP responses (e.g., EntityNotFound -> 404, AccessDenied -> 403 with a message). Spring Security will handle AccessDenied by default (forbidden returns 403). But customizing error messages (without revealing sensitive info) is user-friendly.

**9. Testing Security:** Write some tests for the security config if possible. Spring Security has test support where you can annotate a test method with `@WithMockUser(roles="ADMIN")` etc. Ensure that a non-authenticated request to a secure endpoint returns 401, and an authenticated one with insufficient role returns 403, etc. This contributes to evidence that security controls are working as intended.

At this point, our backend will:

- Accept a JWT on incoming calls and validate it (authentication).
- Enforce method/URL-level authorization.
- Expose only the needed data and operations.

This addresses the **Security** principle of SOC 2: we have strong access controls and authentication in place. Also, because we're using standard libraries and minimal custom auth code, we reduce the chance of security errors (and make it easier to update as libraries fix issues).

## Database Integration with MySQL using JPA/Hibernate

Next, we set up persistence with MySQL. We have MySQL running (locally or Azure) and a schema created for our app. We will use Spring Data JPA with Hibernate to interact with MySQL in an object-relational way.

**1. Configure Data Source:** In `application.yml`, configure database connection properties:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/myapp_dev?useSSL=false&allowPublicKeyRetrieval=true
    username: myapp_user
    password: <your_db_password>
  jpa:
    hibernate.ddl-auto: update
    show-sql: false
    properties:
      hibernate.format_sql: true
```

For local dev, `allowPublicKeyRetrieval=true` and `useSSL=false` might be needed. In Azure, you'll use `jdbc:mysql://<mysql-host>:3306/<dbname>?useSSL=true&requireSSL=true` (Azure requires SSL). We will externalize the password (and later in Azure, supply via environment variables or Key Vault). The `ddl-auto: update` tells Hibernate to auto-create/update tables based on entities – convenient for dev, but for production, you might use `validate` or explicit migrations. We'll use it in dev for quick start, but in a controlled environment, prefer running SQL scripts or using a migration tool for schema (for better change control).

**2. Define Entities:** Create JPA entity classes for each table. For example, a `User` entity:

```java
@Entity
@Table(name = "users")
public class User {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, unique = true)
  private String email;

  @Column(name = "password_hash", nullable = false)
  private String passwordHash;

  @Column
  private String role;  // e.g., "USER" or "ADMIN"

  // getters and setters
}
```

If using OAuth external, you might not store password at all (since Azure AD B2C holds it). But if we want to allow both or just to have a user table for reference, we might not use `passwordHash` except for service accounts. In an OAuth scenario, you might store users by their OAuth subject ID with no password.

Also define other entities relevant to your app (e.g., if it's an e-commerce example, `Order`, `Product`, etc.). Mark relationships with `@OneToMany`, `@ManyToOne` as needed. Ensure to use lazy loading appropriately to avoid performance issues.

**3. Create Repositories:** Spring Data JPA allows us to create repository interfaces that Spring implements at runtime. For `User`:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```

Now you can inject `UserRepository` into services and use methods like `findAll()`, `findById()`, `save()`, `deleteById()`, and our custom `findByEmail()` without writing implementation.

**4. Service Layer:** Write service classes to encapsulate business logic and coordinate between controller, repository, and other parts. E.g., `UserService`:

```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepo;

    public List<UserDto> getAllUsers() {
        List<User> users = userRepo.findAll();
        return users.stream().map(UserMapper::toDto).toList();
    }

    public UserDto getUserById(String userId) {
        // userId might be a string (from JWT `sub` claim).
        // If it's numeric id, convert. If using UUIDs, etc adjust type.
        Long id = Long.parseLong(userId);
        User user = userRepo.findById(id)
                     .orElseThrow(() -> new EntityNotFoundException("User not found"));
        return UserMapper.toDto(user);
    }

    public UserDto createUser(CreateUserRequest request) {
        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        // Hash the password before storing
        String hash = passwordEncoder.encode(request.getPassword());
        user.setPasswordHash(hash);
        user.setRole("USER");
        User saved = userRepo.save(user);
        return UserMapper.toDto(saved);
    }
}
```

We assume `passwordEncoder` (BCryptPasswordEncoder typically) is available, perhaps as a bean we define in a SecurityConfig. Since we might not actually use password (if external OAuth), the createUser might be only for initial admin seeding or not used.

Note: If using external IdP, user provisioning might happen either on the fly (first time JWT comes in, we create a local user record if needed) or manually.

**5. Input/Output Mapping:** Use mappers or directly in service to map entity to DTO. It's often helpful to keep DTO classes for responses (so you don't expose fields like passwordHash). For example, a simple mapper:

```java
public class UserMapper {
    public static UserDto toDto(User user) {
        UserDto dto = new UserDto();
        dto.setId(user.getId());
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        dto.setRole(user.getRole());
        return dto;
    }
}
```

No password in UserDto. Also, ensure not to expose internal IDs if not needed (maybe use a public identifier).

**6. Database Migrations:** It's recommended to use a tool like **Flyway** or **Liquibase** for managing database schema changes in a controlled way (especially in prod). For now, we rely on `ddl-auto: update` in dev. For production, we would:

- Include Flyway and have SQL migration scripts (in `src/main/resources/db/migration`).
- This ensures an audit trail of DB changes (which is good for compliance).
- It also forces us to be deliberate about altering schema (which may require approval in change management).

**7. Performance considerations:**

- Add appropriate indexes via JPA annotations or in SQL migrations (e.g., if you query `findByEmail` often, ensure an index on email).
- Monitor lazy vs eager loading: if a relationship is always needed, maybe eager load it to avoid N+1 queries.
- Use pagination for endpoints that return large lists (Spring Data JPA supports `findAll(Pageable)`).
- These affect availability (performance issues can make the service unavailable under load).

**8. Transaction Management:** Spring Data JPA methods by default are transactional for write operations. Service methods can be annotated with `@Transactional` if they do multiple operations as one unit. Ensure consistency (for example, if creating a user should also create a profile in another table, wrap in one transaction).

**9. Testing with MySQL:** For local dev, test the repository methods (you can write a Spring Boot test that loads the context and uses an in-memory H2 database to test JPA queries, or test against a local MySQL test schema). Ensuring your database code works as expected and handles error conditions (like unique constraint violation, which throws DataIntegrityViolationException, etc.) is important.

**10. MySQL in Azure:** When we later deploy to Azure MySQL, we might need to add a dependency for the MySQL driver (which we did via Spring Boot starter). Also configure SSL. We'll ensure to set `spring.datasource.url` via environment variables on Azure (never commit the production DB password in code or config).

This covers integrating MySQL. At runtime, our Spring Boot app will connect to the MySQL database, and thanks to Spring Data JPA:

- It will **automatically run schema generation** (if enabled) or migrations.
- We can easily query or update database entries through repository methods and custom JPQL queries if needed (e.g., `@Query` annotations for complex queries).
- The database credentials are abstracted in config which we will externalize for each environment (dev vs prod).
- We should also consider database connection pool settings if high load (Spring Boot uses HikariCP by default which is fine, but might tune pool size under heavy load).

One more note: Ensure **secure credentials** – in dev it's fine to use a local .env or application-local.properties with the password. In the code repo or any public place, do not include real passwords. For production, we will load them from Azure Key Vault or pipeline variables.

## Logging and Monitoring Best Practices

Implementing logging is not just about debugging; for SOC 2, logs are crucial for audit trails and detecting security incidents. We need to configure logging in Spring Boot and set up monitoring hooks.

**1. Logging Configuration:** Spring Boot uses Logback by default. Out-of-the-box, it logs to console. For production, we might log to both console and a file (Azure will capture console logs via App Service logging, and we can also send to Application Insights).

- Ensure the log format includes timestamp, log level, logger name, and perhaps the request ID or user (we can use MDC for that if needed for distributed tracing).
- Example logback pattern:

  ```
  %d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger - %msg%n
  ```

  We can put this in `src/main/resources/logback-spring.xml` to customize if needed.

- **Mask sensitive data**: If logging request details, avoid printing things like passwords or secrets. For example, never log the Authorization header or token. If you have debug logging for requests, consider a filter to mask or remove sensitive headers/fields.

- **Log levels:** Set appropriate levels. INFO for general events, DEBUG for detailed debug info (which you might enable in dev, off in prod), ERROR for exceptions. Avoid using DEBUG in production as it may log too much (and possibly sensitive internals). For security-sensitive events, like a login failure or access denied, consider WARN level so it stands out.

- **Audit Logging:** Consider explicitly logging security events. E.g., in your AuthService (if you had login), log a message when a user logs in ("User [email] logged in successfully from IP [x]"). For our OAuth flow, we rely on Azure AD for login, but our backend can log when it first sees a token or issues a new user record. Also log admin actions: if there's an endpoint to delete a user, log which admin did it. These logs serve as audit trails for compliance.

**2. Spring Boot Actuator:** Enable Actuator endpoints for health and metrics:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, metrics, loggers, httptrace
```

At minimum, `/actuator/health` and `/actuator/metrics` are useful. `/actuator/health` will show the status (and by default, will include database status, etc.). You might want to configure health details to be shown only on secure endpoints (by default, details are restricted to authorized or same network requests unless set otherwise). We might keep health simple ({"status":"UP"}) for unauthenticated calls (useful for Azure Load Balancer or uptime checks).

With Actuator, Spring Boot automatically collects lots of metrics (memory, CPU, HTTP request counts, etc.) and with the Micrometer library, these can be forwarded to monitoring systems. If using Azure Application Insights, there's a starter that can collect these too.

**3. Monitoring Integration:**

- **Azure Application Insights**: It's a powerful APM tool. You can integrate by adding the Application Insights Java agent or the `applicationinsights-spring-boot-starter`. E.g., add the agent to your App Service by setting `JAVA_OPTS` to include the agent JAR path. This will automatically instrument HTTP requests and dependencies (like outgoing HTTP or DB calls) and send data to an Application Insights instance. It also captures exceptions and logs if configured. According to Microsoft, you can enable Application Insights for Spring Boot via either a JVM argument or programmatically.
- If you install the Application Insights Azure extension in App Service, it might auto attach. Alternatively, manually: place the AI agent jar in your project and configure it.

- **Azure Monitor Logs**: If not using Application Insights, at least ensure the logs from the app (stdout or a file) are being collected. In Azure App Service, you can enable logging to Azure Blob or Log Analytics. In AKS, you'd ensure log aggregation (maybe via Azure Monitor for containers or ELK stack).
- We aim for centralized logs and metrics.

**4. Add Correlation IDs:** To trace a request from the front-end through the back-end logs, it's helpful to have a correlation ID (also useful in microservices to track a request across services). You could generate a unique ID per request at a filter level and put it in MDC (Mapped Diagnostic Context) so every log statement for that request includes it. Spring Cloud Sleuth is a project that does this (and also integrates with distributed tracing systems like Zipkin). If using Application Insights, it also correlates requests and dependencies automatically by passing trace-context headers.

**5. Example Logging in Controller:**

```java
@GetMapping("/{id}")
public ResponseEntity<UserDto> getUser(@PathVariable Long id, Authentication auth) {
    log.info("User {} requesting details for user {}", auth.getName(), id);
    UserDto user = userService.getUserById(id);
    if (user == null) {
        log.warn("User {} not found by request of {}", id, auth.getName());
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.ok(user);
}
```

This log line records _who_ requested _what_. The `auth.getName()` might be the username or user ID of the caller (depending how JWT is set; often it's the `sub` claim). This kind of logging is useful for audit: if an admin accesses a user's data, we have a log of it (satisfies confidentiality controls about access to sensitive data).

**6. Protect Logs:** Ensure log files or log stores are protected. In Azure, Application Insights data is secured by Azure RBAC (only authorized can query). If writing to files, ensure file permissions and rotate them (Logback can do rotation by size/date). You don't want logs to fill disk (especially in cloud). On App Service, if writing a lot, offload to blob storage.

**7. Monitoring Dashboards & Alerts:** After deploying:

- Set up an Application Insights dashboard to watch metrics like server response time, failure rate, memory usage.
- Configure Azure Monitor **Alerts**: e.g., if CPU > 80% for 5 minutes, alert ops; if memory near limit, if average response time spikes, or if any unhandled exceptions are logged (AI can alert on exceptions). This ties to SOC 2 **availability** and **security** (alert on anomalies).
- Also set up an uptime test: Azure Application Insights has an **availability test** that can ping your health endpoint every few minutes from various regions and alert if down.

**8. Plan for Log Retention:** SOC 2 often requires retaining logs for a certain period (say 90 days or more) for forensic purposes. Ensure your log solution retains data sufficiently (Azure defaults can be 90 days for AI, can be adjusted or archived to storage for longer).

With logging and monitoring in place, our backend is **production-ready** and we have the tools to detect issues and demonstrate to auditors that we monitor our system's security and performance actively. Spring Boot Actuator and Azure's monitoring complement each other to provide a complete picture (Actuator for local health checks, Azure Monitor for aggregated, historical data and alerts).

---

# Infrastructure & Azure Deployment

With the application (frontend and backend) developed and tested locally, we move on to deploying it to Azure. This chapter will cover how to set up the Azure infrastructure: hosting our application on Azure App Service or Azure Kubernetes Service (AKS), provisioning an Azure MySQL database, managing secrets with Azure Key Vault, and using Infrastructure as Code (Terraform/Bicep) to automate resource creation. We want our deployment to be repeatable and secure, aligning with the **Availability** and **Security** trust principles by leveraging Azure's built-in features for redundancy and protection.

## Setting up Azure App Service or AKS for Deployment

**Azure App Service (Web Apps):** This is a PaaS (Platform as a Service) offering that is well-suited for hosting web applications without worrying about managing servers. For our case:

- We can create one App Service for the combined application (since we packaged frontend + backend together in the Spring Boot JAR).
- Alternatively, if we had separated them: one App Service could host a Node.js app serving the React build, and another App Service (or Azure Spring Apps service) for the Spring Boot API. There's also **Azure Static Web Apps** which is optimized for SPAs + Azure Functions as backend. But since our backend is more complex, we'll stick to App Service.

Let's proceed with **Azure App Service** for the Spring Boot app:

1. Go to Azure Portal, create a **Resource Group** (e.g., "rg-myapp-prod").
2. Create **Azure App Service**:

   - Runtime: Use **Java 17** (Java SE) if deploying a jar. Azure will run it with something like `java -jar`.
   - Or choose **Docker** if we containerize the app (then we'd push a container).
   - Instance size: Start with a small one (e.g., B1 or S1 tier) for testing. For production, consider at least two instances (so an S1 with scale-out count 2) for high availability.
   - Set Linux as OS for Java (Windows works too, but Linux is common for Java).
   - Provide a name, e.g., `myapp-backend-prod` (it will form part of the URL `<name>.azurewebsites.net`).
   - Deployment: We will deploy via CI/CD, so no need to deploy from portal directly. Just create the service.

3. **Configuration of App Service**: After creation, go to **Configuration**:
   - Add environment variables for any Spring Boot config we need to override. For example:
     - `SPRING_DATASOURCE_URL` = the JDBC URL to the Azure MySQL (we'll create that next).
     - `SPRING_DATASOURCE_USERNAME` and `SPRING_DATASOURCE_PASSWORD` (though password we'll fetch from Key Vault ideally).
     - `SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_ISSUER_URI` if needed to point to the correct issuer (though we can also package that).
     - `APPLICATIONINSIGHTS_CONNECTION_STRING` if using App Insights (if the site extension isn't used).
   - Enable "HTTPS Only" to ensure no HTTP.
   - Under TLS/SSL, if using a custom domain, you'll upload certificates or use App Service Managed Certificate if domain is enabled.
   - Scale-out: set the app to have at least 2 instances for redundancy (optional for now, but in production we would).
   - Auto-Heal: Consider configuring auto-heal rules (App Service can restart the app if certain conditions, like memory leak or specific error patterns).
   - Backups: App Service can do backups of the site content. Our app is mostly stateless (state in DB), but backup could capture config. With infra as code, we might not rely on this.

**Azure Kubernetes Service (AKS):** Using AKS is more involved but offers greater control for microservices or custom deployments:

- You would containerize the React front-end (as static served by Nginx or an Azure Storage static site) and the Spring Boot backend (into a Docker image).
- Push images to **Azure Container Registry (ACR)**.
- Create an AKS cluster (with node pools across availability zones for HA).
- Write Kubernetes manifests or Helm charts for deploying the frontend and backend (Deployments, Services, Ingress for routing).
- Use Azure AD integration for AKS if possible (for ops authentication), and ensure network policies.
- For simplicity, we continue with App Service. But note that for scaling to very large loads or microservices, AKS might be considered in the future.

**Azure Spring Apps** (formerly Azure Spring Cloud) is another option specifically for Spring Boot microservices, but it's a specialized PaaS.

For now, let's assume the decision is to use **Azure App Service** for the Java backend (with integrated front-end). This is the quickest path to get our full stack running on Azure.

We will set up deployment from our CI/CD pipeline (Azure DevOps or GitHub Actions) to this App Service. We already put a deploy step in our pipeline YAML for Azure DevOps:

```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: "MyAzureConnection"
    appName: "myapp-backend-prod"
    package: "$(Pipeline.Workspace)/backend-artifact/myapp.jar"
```

This will upload the jar and start the app. In Azure DevOps, ensure the service connection has permission to the resource group.

After deployment, verify:

- Browse to `https://myapp-backend-prod.azurewebsites.net/` and see if the React UI loads (since we packaged it in the jar).
- Test an API endpoint (maybe via browser or Postman) to see if it returns expected data. If it requires auth, test after setting up Azure AD accordingly with a token.

**High Availability Note:** Azure App Service is inherently in one region (but can be zone-redundant on Premium plans). For higher availability across regions, one could deploy the app in multiple regions and use Azure Traffic Manager or Front Door to route traffic. That ensures even if one region goes down, the app is available (SOC 2 Availability). This is an advanced setup out of scope here, but planning DR (Disaster Recovery) is critical: we should document Recovery Time Objectives (RTOs) and Recovery Point Objectives (RPOs) for the app, and Azure features like multi-region deployment help achieve low RTO.

## Configuring Azure Database for MySQL

We need a production-grade MySQL in Azure. Azure offers **Azure Database for MySQL** in two flavors: Single Server (older) and Flexible Server (newer with better features). We'll use **Flexible Server** for more control and easier scaling.

Steps to set up Azure MySQL:

1. In Azure Portal, create **Azure Database for MySQL - Flexible Server**:

   - Choose the same resource group "rg-myapp-prod".
   - Give a server name (e.g., `myapp-mysql`). The full hostname will be `myapp-mysql.mysql.database.azure.com`.
   - Choose region (same as App Service ideally for latency).
   - Workload type: choose "Production" which defaults to higher availability (redundant).
   - Compute and storage: a small instance to start (e.g., 1 vCore, 5 GB) can be chosen. For production loads, choose appropriately. Ensure "Zone redundant HA" if available for high availability within region.
   - Administrator account: create an admin (e.g., `dbadmin`) and password. This is not our app user, but a server admin.
   - Authentication: MySQL only (no AD auth for MySQL currently).
   - Networking: If App Service and MySQL are in the same region, you can use **VNet Integration**. E.g., create a new Virtual Network and put MySQL in it, and enable VNet integration on App Service to that VNet. This way MySQL is not exposed publicly, improving security. If VNet integration is complex, at least enable "Allow public access from Azure services" and restrict to the App Service's outbound IP.

     - Azure MySQL flexible server allows choosing Public access vs Private VNet. For simplicity, we might allow public but then restrict allowed IPs.
     - After creation, find the App Service's outbound IP addresses (in its Properties). Then in MySQL server Networking, add firewall rules for those IPs (so only the App Service can connect).
     - Also add a rule for your dev IP temporarily if you need to connect directly for debugging.

   - Click create and wait for it to provision.

2. Once MySQL is up, in Azure Portal go to the server:

   - Create a new database (the equivalent of schema) via "Create database". Name it `myapp_prod` for instance.
   - We need to create a dedicated user for the app rather than using the admin:

     - Connect using admin (you can use Azure Cloud Shell with MySQL client or MySQL Workbench from your machine).
     - Run SQL:
       ```sql
       CREATE USER 'myapp_user'@'%' IDENTIFIED BY 'StrongPassword!';
       GRANT ALL PRIVILEGES ON myapp_prod.* TO 'myapp_user'@'%';
       FLUSH PRIVILEGES;
       ```
       This creates `myapp_user` that can connect from any host `%` (we rely on firewall to restrict), with only privileges on `myapp_prod` database.
     - Alternatively, in Flexible Server, they encourage using the admin and Azure AD for admin tasks. But it's best practice to have a limited user for the app.

   - Ensure SSL is required: By default, Azure MySQL requires SSL. Check the "SSL settings" — they should have Enforcement = Required. Azure MySQL provides a CA certificate if needed to connect. But the MySQL driver can also accept the server's certificate using `useSSL=true` in URL. We'll use `requireSSL=true` as well to ensure encryption.

   Azure Database for MySQL automatically encrypts data at rest using service-managed keys (FIPS 140-2 validated). If needed, you can bring your own key (BYOK) for encryption to meet certain compliance (Azure allows attaching a Key Vault key to MySQL). In transit, as mentioned, SSL is required (only allow TLS1.2+ connections). So by using Azure MySQL, we are addressing encryption at rest and in transit without extra effort.

3. Configure our Spring Boot app to use this database:

   - Set environment variables in App Service:

     - `SPRING_DATASOURCE_URL = jdbc:mysql://myapp-mysql.mysql.database.azure.com:3306/myapp_prod?useSSL=true&requireSSL=true&enabledTLSProtocols=TLSv1.2`
       - The `enabledTLSProtocols=TLSv1.2` ensures using TLS 1.2.
       - We might also add `&serverTimezone=UTC` to avoid timezone warnings.
     - `SPRING_DATASOURCE_USERNAME = myapp_user@myapp-mysql` (for Azure MySQL, the username often needs `@servername` suffix to login).
     - `SPRING_DATASOURCE_PASSWORD = <the password>` – but we'll likely store this in Key Vault instead of directly here.

   - If using Flyway for schema, we would also set `SPRING_FLYWAY_URL` similarly, but if not, the app on first run with `ddl-auto=update` will attempt to create tables. Azure MySQL user needs privileges to create tables (we gave ALL on that db, so it should work).

   - Test connectivity: You can use the Azure Cloud Shell to run `mysql -h myapp-mysql.mysql.database.azure.com -u myapp_user@myapp-mysql -p myapp_prod` to ensure the user can connect and the DB is reachable. Also, our pipeline integration tests could run against a staging DB to ensure config works, but let's assume direct.

**Summary of MySQL security on Azure:**

- **Encryption at Rest:** provided by Azure (FIPS 140-2 validated).
- **Encryption in Transit:** enforced TLS 1.2, we configure our app to use SSL.
- **Firewall:** Only App Service and perhaps dev IP allowed.
- **Least Privilege:** Using a specific DB user with limited scope.
- **Backups:** Azure MySQL does automated backups (with point-in-time restore capability). Ensure the backup retention meets our requirements (default might be 7 days, can increase up to 35). For SOC 2, having backups and the ability to restore meets part of Availability. Document your backup retention and test restoration process (maybe try a restore into a staging server to simulate).
- **Monitoring:** Enable Azure monitoring for MySQL (it can send metrics like CPU, connections, etc., to Azure Monitor). Set alerts if CPU, storage or connections get high (e.g., alert if CPU > 80% which might indicate heavy load or performance issue).
- **Scaling:** With Flexible Server, you can scale up vCores or storage fairly easily if needed (some downtime may be needed for vCore change if not HA). Also can add read replicas for scaling reads (and failover scenarios). Keep that in mind if expecting growth.

## Secrets Management with Azure Key Vault

Storing secrets (like the DB password, API keys, etc.) securely is paramount. Azure Key Vault is a cloud service for securely storing and accessing secrets, keys, and certificates. We'll use Key Vault to manage:

- Database credentials (password, possibly username).
- Any other secret values, e.g., an OAuth client secret if our backend needed one (not in our scenario since we only validate tokens).
- Perhaps the Application Insights instrumentation key (though that's not super sensitive, but still).
- Future secrets like third-party API keys, etc.

**1. Create a Key Vault:** In Azure Portal, create **Azure Key Vault** in our resource group:

- Name: e.g., `kv-myapp-prod`.
- Access policy: Since this is production, we might restrict access. But to allow our App Service to fetch secrets, we will use a Managed Identity.
- It's good to disable public access and use Private Endpoint for Key Vault in production, but that requires VNet integration. If not using private endpoint, ensure firewall rules to only allow Azure services (like our app).

**2. Store Secrets:** In Key Vault, add secrets:

- Secret Name: `DBPassword` (for example) with value = the MySQL password for `myapp_user`.
- You could also store `DBUser` and `DBUrl` to keep everything in vault, though those last two are not as sensitive. Often just the password is stored, and user/URL can be config.
- If we had any other secrets, store them similarly. E.g., `OauthClientSecret` if we needed to call another service, etc.

Key Vault secrets have versions; when updating a secret, it creates a new version. The Key Vault will always give the latest version unless you pin a version in the reference.

**3. Give App Service access to Key Vault:** Use Managed Identity:

- In the App Service settings, enable **System-Assigned Managed Identity** (under Identity menu, switch it on). This creates a service principal in Azure AD representing the app.
- In Key Vault Access Policies (if using Vault's policy model) or Azure RBAC (Key Vault can use Azure RBAC roles), grant the App’s identity **GET** permission on secrets.
  - With Azure RBAC: assign the role "Key Vault Secrets User" to the App Service's identity for that Key Vault.
  - With Access Policy (legacy method): add access policy for that identity and select "Get" and maybe "List" for secrets.
- Now the App Service can authenticate to Key Vault without any passwords (it uses its identity). This is more secure than storing a Vault key.

**4. Using Key Vault secrets in the App Service configuration:** Azure provides a neat integration:

- In App Service > Configuration, when adding a setting, you can reference a Key Vault secret by using a special syntax in the _Value_ field:
  ```
  @Microsoft.KeyVault(SecretUri=https://kv-myapp-prod.vault.azure.net/secrets/DBPassword/)
  ```
  This will tell App Service to fetch that secret from Key Vault and treat it as an environment variable value. The App Service's managed identity is used to authenticate to Key Vault automatically.
- So set `SPRING_DATASOURCE_PASSWORD = @Microsoft.KeyVault(SecretUri=https://kv-myapp-prod.vault.azure.net/secrets/DBPassword/)`.
- When the app runs, the environment variable will have the actual password from Key Vault. The nice thing is the password isn't stored in App Service config, only a reference, and even if someone had read access to the App Service config, they'd just see that reference.

You can do similar for other secrets:

- If we had `SPRING_DATASOURCE_USERNAME`, we might not bother to hide that (not sensitive), but we could.
- If using an App Insights instrumentation key, that could be a secret but it's often considered okay to be in config (though no harm in vaulting it).
- Certificates for custom domain maybe in Key Vault, etc.

**5. Spring Boot integration with Key Vault (optional):** Spring has an **Azure Key Vault Config Starter** which can automatically load all secrets as properties. But using the direct App Service reference as above might be simpler. If we had a need to dynamically load secrets at runtime or in code, we could use Azure SDK to call Key Vault from the app, but that adds complexity. Usually, you want the environment to provide the secrets.

**6. Verify Key Vault access:** There is a tool: from Azure Cloud Shell, you can use `curl` with the Managed Identity token to test, but easier: in App Service, use the **Console** (in Azure Portal, App Service > Console) which gives you a shell on the instance. Type `env` and see if `SPRING_DATASOURCE_PASSWORD` is set to the correct value (it might not show it if it's injected in process, but likely it will show a placeholder or actual value). Or deploy a test endpoint that prints a config value. If not accessible, check the identity and access policy.

**Compliance note:** Using Key Vault demonstrates strong control over secrets:

- Secrets are stored encrypted under the hood by Azure.
- Access can be audited (Key Vault logs secret retrievals).
- We can even require an approval or specific process to update a secret (Key Vault supports RBAC such that only certain individuals can update production secrets, and that can be part of change management).
- No hard-coded secrets in code or config = reduces risk of leakage (and is often a specific criterion in security checks).

## Infrastructure as Code with Terraform or Bicep

To ensure our infrastructure is reproducible and version-controlled (important for both engineering and compliance), we should define it as code. **Terraform** is a widely used tool for multi-cloud, and **Bicep** is an Azure-specific templating language. Let's outline using Terraform as an example (Bicep would be similar conceptually, just Azure only).

**Terraform setup:**

- You'd have `.tf` files describing resources. Possibly separate modules or files for each component (one for app service, one for MySQL, etc., or all in one).
- You maintain this in a separate repo (infrastructure repo) or a folder `infra/` in the monorepo.

For example, a Terraform config snippet:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-myapp-prod"
  location = "Central US"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "myapp-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "Linux"
  reserved            = true                # needed for Linux
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "app" {
  name                = "myapp-backend-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_ISSUER_URI" = "https://login.microsoftonline.com/<tenant>/v2.0"
    "SPRING_DATASOURCE_URL" = "jdbc:mysql://${azurerm_mysql_flexible_server.db.fqdn}:3306/myapp_prod?useSSL=true&requireSSL=true"
    "SPRING_DATASOURCE_USERNAME" = "myapp_user@${azurerm_mysql_flexible_server.db.name}"
    # Password omitted here; we'll use key vault reference below
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = var.appinsights_connection_string
    "AzureWebJobsStorage" = var.azurewebjobsstorage  # if any, typically for functions
  }

  site_config {
    always_on = true
    java_version = "Java|17"
  }
}
```

We would also have Terraform resources for:

- The MySQL server:

```hcl
resource "azurerm_mysql_flexible_server" "db" {
  name                = "myapp-mysql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  administrator_login          = "dbadmin"
  administrator_login_password = var.db_admin_password
  sku_name     = "Standard_B1ms"  # 1 vCore burstable, for example
  storage_mb   = 5120
  version      = "8.0"
  high_availability {
    mode = "ZoneRedundant"       # If available in region
  }
  # networking: either public with firewall or vnet
  public_network_access = true
  # if we had a vnet:
  # private_dns_zone_id = azurerm_private_dns_zone.mysql.id
}

resource "azurerm_mysql_flexible_server_firewall_rule" "appservice_access" {
  name                = "AllowAppService"
  mysql_server_id     = azurerm_mysql_flexible_server.db.id
  start_ip_address    = azurerm_app_service.app.outbound_ip_addresses[0]
  end_ip_address      = azurerm_app_service.app.outbound_ip_addresses[0]
}
```

Actually, App Service has multiple outbound IPs. In Terraform, `outbound_ip_addresses` might give a list; you would need to create a rule for each (could iterate). Alternatively, allow all Azure (less secure but easier): Azure MySQL has a flag `private_network_access = true` and then set `public_network_access_enabled = true` (if `false` means only private).

- Key Vault and secret:

```hcl
resource "azurerm_key_vault" "vault" {
  name                = "kv-myapp-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tenant_id           = var.tenant_id
  sku_name            = "standard"
  purge_protection_enabled = true

  access_policy {
    tenant_id = var.tenant_id
    object_id = azurerm_app_service.app.identity.principal_id
    secret_permissions = ["get", "list"]
  }
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "DBPassword"
  value        = var.db_password   # you supply via TF variable (and state should be protected!)
  key_vault_id = azurerm_key_vault.vault.id
}
```

Storing secrets in Terraform state is sensitive; usually you'd use Azure DevOps secure variable for `var.db_password` or use Terraform to only set it once. Another approach: create secret outside and just reference it in app settings.

- App Service Key Vault Reference isn't directly in Terraform as a resource (currently, as of provider 3.x, you might have to use azurerm_app_service.app_settings for that). The tricky part is referencing Key Vault in app settings via Terraform. One approach:
  - Instead of putting actual password, put the Key Vault reference syntax in Terraform:
  ```hcl
  app_settings = {
    "SPRING_DATASOURCE_PASSWORD" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_password.id})"
  }
  ```
  The `id` of secret includes the full URI. Actually, `azurerm_key_vault_secret.db_password.id` might be the Azure resource ID, but there's also `.vault_uri` or `.value` attributes. According to docs, `id` might not be the correct URL. Possibly:
  ```hcl
  "SPRING_DATASOURCE_PASSWORD" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault.vault.vault_uri}secrets/DBPassword/${azurerm_key_vault_secret.db_password.version})"
  ```
  But for latest version, you could omit the version for always latest:
  ```hcl
  "SPRING_DATASOURCE_PASSWORD" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault.vault.vault_uri}secrets/DBPassword)"
  ```
  Need to ensure format is correct (with trailing slash).
- If using Application Insights:

```hcl
resource "azurerm_application_insights" "insights" {
  name                = "myapp-insights"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

# then provide connection string to app settings
```

After writing Terraform configs, you'd:

- Run `terraform init`, `terraform plan`, and `terraform apply` to create resources. This could be done manually, or integrated in CI.
- You can integrate Terraform in Azure DevOps pipeline (using the Terraform Installer and CLI tasks) or in GitHub Actions (using `hashicorp/setup-terraform` action). This way, infra changes go through PRs and approvals too.

**Benefits for SOC 2:**

- **Change Management:** Infra as code means any change to infrastructure (opening a port, changing an instance size) is done via code changes, which can be reviewed and approved similarly to code changes.
- **Consistency:** You can replicate environments (Dev, QA, Prod) with the same config (just different parameters).
- **Disaster Recovery:** If we lost everything, we could re-run Terraform to recreate infra (though restoring data is separate). But it aids in DR plans.
- **Documentation:** The Terraform files serve as documentation of your cloud architecture (which an auditor might review to see if it's well-thought-out).
- **Least Privilege Principals:** We can see clearly in code what identities have what access (like the Key Vault access policy, etc.). And Terraform state can be stored securely (e.g., in Azure storage with access controls).

Given we have many components, it’s wise to use Terraform to glue them. If not using Terraform, Bicep or even Azure CLI scripts would be the alternative.

---

# Security & Compliance for SOC 2

Having built and deployed the application, we now focus explicitly on security and compliance measures relevant to SOC 2. This chapter covers how to implement access controls and encryption throughout the stack, how to ensure logging and auditing are in place, how to monitor the system for security and availability, and how to prepare documentation for SOC 2 audits. This is about turning our technical implementation into a compliant service through policies, procedures, and controls.

## Implementing Access Control & Encryption

**Access Control:**

- **Application-level access control:** We’ve already implemented role-based access in the application (ADMIN vs USER roles in Spring Security, and UI conditions in React). Make sure that for each critical function, you have decided who is allowed to do it and enforced it in code. For example, only admins can delete data or access other users' data. Regular users can only access their own data. This should be documented as an access control policy for the application. If using groups/roles from Azure AD, maintain those groups and memberships carefully (e.g., an "Admin" group in Azure AD whose members get admin role in JWT). Review these memberships periodically (SOC 2 requires periodic user access reviews – ensure people who have admin access still need it).
- **Azure resource access control:** Use Azure Role-Based Access Control (RBAC) to limit who on the engineering team can manage the resources. For instance, not everyone should have Owner access to the subscription. Perhaps developers have Contributor or Reader roles, and only lead engineers or DevOps have rights to production changes. Also, use separate Azure environments for dev/test and production with strict access separation. Document these roles and rights (this could be part of your _Access Control Policy_ for infrastructure).
- **Database access:** We set up a dedicated DB user for the app. Ensure that user only has necessary permissions (which we did by scoping to the single database). The admin user should not be used by the app and should be stored securely (Key Vault) and used only for admin tasks. If multiple apps or microservices, give each its own DB credentials. And consider enabling **Azure AD authentication for MySQL** (in preview or GA depending on Azure updates) which would allow using managed identities to auth to DB instead of password – that would be ideal as it eliminates a static credential.
- **Network access:** If possible, run the App Service and MySQL in a VNet with restricted inbound/outbound rules. As noted, we can restrict DB to only App Service IPs or VNet. Also ensure no other open endpoints. If we had any other services (like a Redis cache, etc.), similarly restrict. Use Azure Firewall or NSGs to control any subnet traffic. This network security is an extra layer beyond app authentication (defense in depth).
- **Least Privilege Principle:** Everywhere, assign the minimal rights:

  - The Key Vault access policy gave only secret get/list to the App, not key management or full control.
  - The App's managed identity could also be used to fetch secrets or maybe write logs somewhere, but don't over-provision it.
  - Within code, if there are different levels of admin (like superadmin vs support-admin), consider separating those roles too (maybe not needed here).
  - On the front-end, ensure that just because an admin can do X doesn't inadvertently allow other users via a client-side check bypass. We rely on backend check, but double-check all high-privilege operations do require the proper role on backend.

- **Admin Interfaces:** If we have any admin functionality (maybe not separate UI, but actions), protect them. Possibly implement additional security like IP whitelisting or MFA for admin actions. For example, if an admin deletes a user via API, perhaps require them to re-auth via Azure AD with MFA (Azure AD Conditional Access policies can enforce MFA for accounts in admin role or when accessing particular app).
- **Secrets in code:** Ensure no secrets in code repositories. We used Key Vault for app secrets. Also, ensure not logging secrets (like if a connection string with password accidentally gets logged; we should avoid that).
- **Encryption of data at rest:** We covered that Azure MySQL data is encrypted at rest automatically. If the app stores any files or data elsewhere, ensure those are encrypted too (e.g., if using Azure Blob Storage for file uploads, turn on encryption and maybe use a private container or SAS tokens). If we had extremely sensitive data, consider field-level encryption (the app encrypts certain data before storing in DB). For instance, if storing customer secrets, use something like Azure Key Vault to encrypt/decrypt specific fields so DB only sees ciphertext. That might be overkill for many apps but is an extra layer.
- **Encryption in transit:** Re-iterate that all communications are secure:
  - Frontend <-> Backend: HTTPS enforced (we set "HTTPS Only" on App Service).
  - Backend <-> Database: TLS enforced (we set requireSSL).
  - Backend <-> Key Vault: uses HTTPS by default (Azure SDK and MSI calls happen over TLS).
  - If any integration with third-party APIs, use HTTPS and validate certificates.
  - If any internal service calls (not in this app, but e.g., if multiple microservices calling each other), ensure they use TLS (in Kubernetes, consider mTLS for service mesh if needed).
- **Certificate Management:** Our App Service uses Azure's certificate for the azurewebsites.net domain. If using a custom domain, get an SSL certificate (Azure can provide a free one via App Service Managed Certificate, but those don’t support wildcard or certain features). Manage certificate renewal (Managed Cert auto-renews, or if custom, set reminders to renew or use Azure Key Vault certificate management). Downtime or using an expired cert would hit Availability and trust.
- **Sensitive Configuration:** Ensure certain features are disabled in production:
  - No H2 console open, no actuator endpoints like `/env` or `/beans` open (we only exposed health/metrics intentionally).
  - Check that `show-sql` is off so SQL statements (which might have data) aren’t logged.
  - Ensure any default accounts or test accounts are removed in prod. If we created a test admin user in database for convenience, remove it or disable it.

**Encryption Recap**: We have encryption at rest on DB, in transit everywhere, Key Vault for secrets (it itself uses HSMs for keys). If we needed to comply with specific encryption standards, we could even use customer-managed keys for MySQL, but that’s advanced and not always required unless client demands.

## Secure Logging and Auditing

We've touched on logging in the backend setup; here we'll emphasize the auditing aspect:

- **Audit Log Events:** Identify security-relevant events and ensure they are logged. For example:
  - Authentication events: If using our own auth, log successful and failed login attempts. In our OAuth case, Azure AD will have logs of logins (we can retrieve them from Azure AD audit logs). But our app can log when a token is rejected (if we want).
  - Authorization events: log if someone tries to access something they shouldn't (the Spring Security will throw 403; we can add an access denied handler to log "User X tried to access Y and was denied").
  - Data changes: for critical data, log the change. E.g., if an admin updates a user role or deletes something, log who did that. These logs might be needed to demonstrate to an auditor that you can trace "who did what". In a more advanced system, you might maintain an audit log in the database too for certain actions.
  - System changes: if the application config changes, or a new deployment (CI/CD should log the deployer or approver).
- **Log Storage & Analysis:** As part of compliance, ensure logs are retained. Using Azure Application Insights/Monitor, set retention to required policy (maybe 90 days or more). If needed, archive older logs to cold storage. Make sure logs are tamper-evident or at least restricted so they cannot be easily modified by an attacker who might want to cover tracks. In Azure, if someone compromises the app, they typically can't delete past AI logs. But a very sophisticated attacker in Azure could try to access the AI resource; keep its access separate (maybe only ops team has direct AI access).
- **Regular Log Review:** Compliance means not only storing logs but also reviewing them. Set up a process (maybe weekly) to review security logs (failed login attempts, error logs, etc.). Or better, set up alerts for anomalies (we already mention alerts for errors or perf, but also security: e.g., an alert if there are 5 failed login attempts for the same account in a short time could indicate an attack).
- **Database auditing:** Azure MySQL can produce audit logs of connections and queries (to some extent). It's not as straightforward as SQL Server's auditing, but you can enable the general query log and slow query log. For compliance, maybe not needed to log every query (performance overhead), but consider logging administrative actions on the DB.
- **Front-end auditing:** If needed, log user activities in the UI as well (like log to backend when certain sensitive pages are viewed or actions taken). But primarily, backend should log the final actions.

- **Time synchronization:** Ensure all logs use a consistent time source/timezone (usually UTC). Azure services use UTC. This is important when correlating events from different systems (Azure AD logs, App logs, etc.).

- **Protecting PII in logs:** If your app processes personal data, be careful not to log sensitive PII unnecessarily. For example, don't log full credit card numbers or passwords ever. If logging user info, maybe log user ID instead of name or email, unless needed. This is more of a privacy consideration (which is a SOC 2 principle if included).
- **Log integrity:** Key Vault logs and Azure AD logs are available in Azure (and can be exported to log analytics). You might consider enabling **Azure Monitor Diagnostic Settings** for App Service, Key Vault, MySQL to send logs into a central Log Analytics workspace. That way, you can run Kusto queries to analyze combined logs (and it serves as an archive).
- **Incident Response:** If something does go wrong (say an alert triggers or you find a suspicious log), have a plan (documented procedure) to respond. This typically includes investigating the logs, maybe disconnecting affected systems, patching, etc. Having runbooks for common scenarios (like suspect data breach, DDoS attack, etc.) is a plus for SOC 2.

We should demonstrate compliance by showing that:

1. We **monitor and log** all critical activities.
2. We **restrict log access** to appropriate team members (for example, only the DevOps or security officer can read all logs, developers might only see their environment logs).
3. We **retain logs** for a defined period and have a backup of them.
4. We have **alerts** to catch issues in real-time instead of waiting for an audit to find them.

## Monitoring and Alerting with Azure Monitor & Application Insights

Monitoring is partially covered in our infrastructure, but let's outline key components and how they tie to SOC 2:

- **Azure Monitor & Application Insights:** We enabled App Insights for APM. Azure Monitor encompasses App Insights (for app telemetry) and Log Analytics (for logs/metrics). We should ensure that:
  - All relevant metrics are being collected: server CPU, memory, response time, request rate, error rate.
  - We create an Azure Dashboard that shows the health of the system (maybe a dashboard with charts for those metrics and a pie for availability test) – useful internally and also to show auditors that we have a continuous eye on system health.
  - **Alerts:** Set up alerts on:
    - **Security:** As mentioned, e.g., alert on many 401s (could indicate someone repeatedly calling with invalid token). Or Azure AD itself can alert on risky sign-ins.
    - **Availability:** If the App Service goes down (you can alert on the availability test failure or if App Service HTTP 5xx spiking). Azure Monitor can send an alert if the App is stopped or if pings fail.
    - **Performance:** Alert on high response time (maybe P95 latency > X ms).
    - **Capacity:** CPU high, memory high, or if hitting any configured limit (like thread pool exhaustion).
    - **Dependencies:** If MySQL connection fails or is slow (App Insights tracks dependency calls if configured, which includes DB calls), alert.
  - Ensure alert notifications go to a team alias or PagerDuty, etc., so someone responds quickly (SOC 2 wants to see you can promptly detect and respond to incidents).
  - Also set up **Application Insights Smart Detection** which automatically flags anomalies (but now integrated into Alerts, you might have to enable them).
- **Azure Service Health:** Subscribe to Azure service health alerts for the region/services you're using. If Azure has an outage affecting MySQL or App Service in your region, you want to know immediately. This is part of availability monitoring.
- **Disaster Recovery Drills:** Monitor that backups are running. Perhaps simulate a failover: for example, MySQL flexible can restore to a point in time; try it in a non-prod to ensure the process works and you can meet your RTO (recovery time objective). Keep a runbook for DR and test it annually at least (some compliance frameworks strongly encourage DR tests).
- **Penetration Testing and Vulnerability Scans:** Though not monitoring in the Azure sense, it's relevant to security monitoring:
  - Perform periodic vulnerability scanning of your web app (you can use tools like OWASP ZAP or have a third-party do a pen test) and address any findings. For instance, scan the site for OWASP Top 10 issues. If using Azure, consider Azure Security Center (now Defender for Cloud) which might scan App Service configurations. There's also App Service vulnerability assessment (for container or code).
  - Dynamic scans can be integrated in pipelines or run regularly. Document that you do this as part of maintaining security.
  - Infrastructure scanning: Ensure all Azure resources follow security best practices. Azure Defender can alert if something misconfigured (like storage container open, etc.). For App Service specifically, ensure SSL, etc. Azure also has a SOC 2 compliance blueprint which lists recommended Azure controls; cross-check if possible.
- **Continuous Compliance:** Use tools or scripts that continuously check compliance controls. For example, use Azure Policy to enforce certain settings (Azure Policy could ensure "HTTPS Only" is true on App Services, or no public IP on DB, etc.). This prevents drift that could break compliance. It ties into the concept of **continuous compliance** where your system is always being checked against compliance requirements. Implementing Azure Policies for SOC 2 can be powerful (like ensuring all resources have tags (for inventory), or logs enabled, etc., which are often controls).
- **Automated Risk Alerts:** Some companies use SIEM (Security Information and Event Management) systems. You might feed logs to an Azure Sentinel instance for advanced threat detection (like Sentinel can correlate sign-in logs and app logs to spot a potential breach). If within scope, mention that security monitoring is in place at that level too.

**Summary:** We have a robust monitoring setup:

- Real-time metrics and logs via Azure Monitor.
- Alerts for quick detection of issues.
- Regular testing of controls (like DR, security scans).
- And the team is alerted and ready to respond (with documented procedures).

This satisfies the **Availability** criterion (monitoring system uptime and performance) and parts of **Security** criterion (monitoring for security incidents). It also covers some **Confidentiality** aspects indirectly by ensuring any breach attempt would be noticed.

## Preparing for SOC 2 Audits (Documentation, Policies, Risk Assessments)

Finally, beyond the technical implementation, SOC 2 compliance requires documenting what you've done and ensuring you have policies and processes governing the system.

Key documentation and processes to prepare:

- **Security Policies and Procedures:** As per SOC 2 best practices, have a set of written policies. Typically:
  - **Information Security Policy:** an overarching doc that states management's commitment to security and outlines the high-level approach (could reference sub-policies).
  - **Access Control Policy:** detailing how access (physical and logical) is granted, changed, revoked. For our system: describe how developers access Azure (e.g., via Azure AD with MFA), how production database access is restricted, how end-users access the app (only via OAuth with strong auth).
  - **Change Management Policy:** explain how code changes are managed (we use Git, PR reviews, CI/CD pipeline with approvals – this is a change management control).
  - **Incident Response Policy:** what we do in case of an incident (detection, who to notify, how to escalate, mitigation steps, post-mortem).
  - **Business Continuity and Disaster Recovery Plan:** outline RTO/RPO, backup strategy, roles and responsibilities if an outage occurs, communication plan to customers.
  - **Acceptable Use Policy:** for employees, how they should use company resources.
  - **Risk Assessment Procedure:** commit to regular risk assessments of systems (could be an internal audit or review every X months).
  - **Vendor Management Policy:** if we rely on third-party services (Azure, etc.), ensure we review their SOC reports, etc.
  - **Encryption Policy:** specify when we require encryption (e.g., data classified as confidential must be encrypted in transit and at rest, which we did).
  - **Logging and Monitoring Policy:** states that we log critical activities and review logs regularly.
  - Possibly a **Privacy Policy** if handling personal data (ties to confidentiality and privacy trust principle).

These policies should be **approved by management** (in SOC 2, they like to see top-level sign off) and communicated to all relevant staff.

- **Risk Assessment:** Perform a risk assessment for the system. Identify threats (e.g., data breach, downtime, insider threat, etc.) and document how our controls mitigate them. For example:

  - Risk: Unauthorized access to customer data – mitigated by strong authentication (OAuth via Azure AD), role-based access, network restrictions, monitoring.
  - Risk: Data loss – mitigated by daily backups, redundant DB, etc.
  - Risk: Website outage – mitigated by using Azure SLA-backed services, auto-scaling, monitoring and quick response.
  - This process helps ensure we didn't overlook something and we have rationale for our security measures.

- **Collect Evidence:** During a SOC 2 audit, auditors will ask for evidence of controls in action. It's good to start collecting evidence proactively:

  - **System Architecture Diagram** – to show auditors how data flows, where it's stored, and where controls are applied.
  - **Screenshots or exports** – e.g., Azure AD settings showing MFA enabled, a list of users and their roles (to show least privilege).
  - **CI/CD pipeline logs** – to show that every change goes through the pipeline with tests.
  - **Access reviews** – records that you reviewed user access on date X and removed Y users who left.
  - **Incident reports** – if any incidents occurred, document the incident and resolution, to show you follow your process.
  - **Policies and revision history** – show that policies are updated (say yearly).
  - **Training records** – If you have a team, make sure they underwent security training (SOC 2 often expects annual security awareness training for staff). At least note that all developers are aware of secure coding practices (maybe keep a confluence page of secure coding guidelines they've read).
  - **Audit logs** – you might need to show logs of certain events; ensure you can retrieve logs from, say, last 6 months easily.

- **Engage with auditors:** When time for actual audit:

  - Provide them read-only access to relevant Azure resources if they need to inspect configurations (some won't do this, but some might).
  - Be prepared to walk through a demo of controls (e.g., show how an unauthorized user cannot access something, and how an authorized user can, demonstrating the access control works).
  - Prepare a **Control Matrix** mapping each SOC 2 criterion to what control we have. E.g., CC6.1 (Logical access is based on least privilege) – we have Role-Based Access Control in app and Azure AD, documented in Access Control Policy, reviewed quarterly. Provide evidence of last review.
  - Tools like Vanta or Drata can automate evidence collection for SOC 2 by hooking into Azure, GitHub, etc., to check settings. Using them can ease the audit, but even if not, manual prep is okay.

- **Continuous improvement:** Show that you didn't just set up controls once. SOC 2 Type 2 requires operating effectiveness over time (typically 3-12 months period). That means you have to actually practice the policies. For example, if your policy says "we review firewall rules monthly", ensure you have calendar invites and logs of those reviews. If pipeline says "requires approval", ensure in practice every deployment had an approval and there's a record.

- **Scope of Audit:** Confirm which principles and systems are in scope. For instance, if this app is the product being certified, include all components (frontend, backend, DB, underlying Azure infra). Possibly the CI/CD pipeline environment is in scope too (since if compromised, code can be changed). So secure your CI/CD (use MFA on Azure DevOps accounts, protect pipeline secrets, etc., and maybe mention those in evidence).

To conclude this section, once all of the above is in place, your organization should undergo a **SOC 2 readiness assessment** (either internally or with a consultant) to identify any gaps. Then a SOC 2 auditor does the formal audit. Because we built with security and compliance in mind from the start, we expect the audit to go smoothly, with our strong controls addressing the **Security**, **Availability**, and **Confidentiality** principles of SOC 2.

---

# Final Testing & Deployment

With development complete and the system prepared for security and compliance, it's time for final testing and the go-live deployment. We'll conduct thorough testing (functional, performance, security) to ensure the system is robust. Then we'll use our CI/CD pipeline to deploy to production (which we've largely covered) and verify everything is working in the live environment. We'll also cover a go-live checklist to ensure nothing is missed during the launch, and what to monitor post-deployment.

## Load Testing, Security Testing, and Vulnerability Scanning

Before going live, perform the following tests:

**1. Load Testing (Performance Testing):**

- Use tools like **Apache JMeter**, **Locust**, **k6**, or Azure Load Testing service to simulate concurrent users and load on the system.
- Create test scenarios for key endpoints. For example, simulate 100 users logging in and fetching data from the dashboard simultaneously.
- Monitor the system during the test: Check App Service CPU, memory, instance count (auto-scale if set), DB CPU and query throughput, response times (App Insights metrics).
- Determine the max load the current configuration supports and ensure it meets your expected usage plus some headroom. If not, scale up resources (increase App Service plan or DB vCores) or optimize the code (e.g., add caching, tune DB queries).
- Identify performance bottlenecks: If the CPU is high on the app, perhaps the JSON serialization or a specific algorithm is slow. If DB is the bottleneck, maybe an index is missing or N+1 queries happening. Use Application Insights performance traces (it can show slowest requests and DB calls).
- Also test **peak load** and **soak test** (sustained load) to see if performance degrades over time (memory leaks, etc.).
- If the app uses a lot of memory or CPU at peak, consider enabling auto-scale on App Service (scale out to multiple instances based on CPU). We already plan multi-instance for HA, which helps throughput too. Test that the system works correctly in multi-instance mode (sessions are stateless due to JWT, so should be fine; if we had sticky sessions or caching, ensure those work in distributed scenario).

**2. Security Testing:**

- Conduct a **penetration test** or at least run a **vulnerability scanner** against the web app. OWASP ZAP is a popular open-source tool that can scan for things like SQL injection, XSS, etc. Since we used parameterized JPA and React auto-escaping, likely minimal issues, but it's important to confirm.
- Test authentication flows: ensure no way to bypass (try using an expired token, see that it's rejected with 401; try some injection in token if possible – likely not).
- Test authorization: try normal user token to access an admin API, should get 403. Try to retrieve another user’s data with a normal token by manipulating an ID in an API call, should be forbidden or at least not found (depending on logic).
- Check for common web vulnerabilities:
  - XSS: Our React should be safe by default, but if we ever do `dangerouslySetInnerHTML` or render user-provided content, ensure it's sanitized.
  - CSRF: Since our API is stateless JWT, CSRF is not a major issue for API calls (and we've disabled CSRF in Spring because we aren't using cookies for auth). If we had any form that posts to our API using cookies, we would need CSRF tokens.
  - SQL Injection: Using JPA and prepared statements by default, likely fine. If any dynamic queries or native SQL, ensure using parameters, not string concatenation.
  - Insecure Direct Object References: This is about one user accessing another’s data by guessing an ID. We must ensure checks in the backend (like `getUserById` only allows if `id == auth.getName()` or user is admin). These checks should be tested.
  - File uploads (if any feature of that sort): ensure we restrict file types, scan them, and don't allow path traversal.
  - Check headers: Use browser dev tools to see response headers. Ensure security headers like `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: deny` are set. Spring Security can add some by default (frame options, etc.). We might add these in a `WebSecurityConfigurer` if needed for completeness. E.g., `http.headers().contentSecurityPolicy("default-src 'self';");`.
  - Also ensure CORS in production is not too permissive. Ideally, if frontend and backend are same domain in prod, we could even disable CORS entirely (since not needed). Or restrict to the one expected domain.
- If possible, get an **independent security audit** or pen test and fix any findings.
- Additionally, run **Dependency Scanners**: Tools like OWASP Dependency Check or Snyk on the project to find vulnerable libraries. E.g., ensure no known critical CVEs in our dependencies (Spring Boot BOM largely covers that, but new vulns appear, so check).
- Also scan the container or host: If we containerized the app for AKS, scan the Docker image for vulnerabilities (Microsoft Defender for Cloud can do that in ACR, or use Trivy).
- For the database, ensure no test data or default accounts lingering. Also consider running some queries to ensure data is properly encrypted if needed (though encryption is transparent).

**3. Vulnerability Scanning (Ongoing):**

- Integrate dependency scan into CI: e.g., use GitHub Dependabot or OWASP Dependency Check plugin in Maven to alert of outdated libs.
- Use Azure Security Center (Defender for Cloud) which will continuously scan for misconfigurations or recommendations (like "enable advanced data security on your SQL" or "App Service should disallow TLS1.0", etc.). Many of those recommendations align with compliance. Review and address as appropriate.

**4. Fix and Re-test:** For any issues found, fix them:

- If performance issues: optimize code/queries or scale resources, then run load test again.
- If security issues: fix code/config (e.g., add missing header, fix auth logic, update a library), then rerun security scans to ensure it's resolved.
- Document these testing results as evidence that the system was tested and secured prior to launch.

At this stage, we should have confidence in system stability, performance, and security. Now it's time to actually deploy to production (if we haven't already with pipeline, but often teams do a "soft launch" or a final release to prod after sign-off).

## Automating Deployments with Azure Pipelines

Our CI/CD pipeline is ready to deploy, but for the final deployment (and future ones) let's ensure it's configured for a controlled release:

- If not done, set up a **production deployment stage** that requires an approval. Possibly a change record in your ITSM if required by org. The approver could be a lead or someone outside the dev team to enforce separation.
- The pipeline should pull artifacts from the last successful build (which we have).
- Before deploying to prod, consider deploying to a staging slot or environment:
  - App Service has **deployment slots** (e.g., a "staging" slot). We could deploy the new version there first, test it in staging (with perhaps production DB if safe, or a staging DB snapshot). Then use **Swap** to swap it into production with minimal downtime. Swap also warms up the new instance.
  - Using slots can also allow quick rollback (swap back if needed).
  - Alternatively, if we use separate staging environment, test there.
  - For simplicity, maybe we deploy directly but since our app is stateless, the downtime is just the time to start the new instance (a few seconds, which might be acceptable if done off-hours or with multiple instances rolling).
- In Azure DevOps, ensure to create a release or run the pipeline for production. Approve it, and track that it was deployed.

**Deployment steps:**

1. The pipeline (as defined) will deploy the JAR to App Service. You can watch logs in Azure DevOps or in Azure portal (App Service > Log Stream).
2. Once deployed, run smoke tests:
   - Access the health endpoint `/actuator/health` to see if it returns UP.
   - Access the app's main page in a browser, ensure it loads.
   - Try a basic functionality (maybe with a test user account in Azure AD) to see that the entire login flow and data fetch works in prod.
   - Check Application Insights Live Metrics to see if any errors during startup (exceptions in logs).
3. DNS and domain: If using a custom domain like `myapp.com`, ensure DNS CNAME is set to the Azurewebsites hostname and the custom domain is configured in App Service, with an SSL cert bound. This should be done before launch. If the domain was being used by a previous system, plan the cutover carefully (lower TTL, etc.).
4. Scalability: Ensure auto-scaling or manual scaling rules are in place as expected (maybe set to 2 instances). If using auto-scale, maybe initially keep manual to reduce variables, and set auto-scale policies to scale out on high load.

**Rollback plan:** If something goes wrong after deployment (e.g., a critical bug slipped or performance issue):

- Because we have CI, we can revert in Git to previous commit, run pipeline to deploy previous build.
- Or if we used deployment slots, just swap back.
- Or if issue is small, hotfix and deploy fix quickly (but ensure the fix goes through pipeline too).
- Communicate to stakeholders if any user impact happened, etc. (Incident response etc.)

## Go-live Checklist and Post-Deployment Monitoring

Use a checklist to ensure all tasks are done before and after going live:

**Before Go-live:**

- [x] **All tests passed** (unit, integration, load, security).
- [x] **Security review done** – no high vulnerabilities open.
- [x] **SOC 2 controls verified** – e.g., logging is capturing data, backups enabled, etc.
- [x] **Documentation ready** – runbooks, contact lists, architecture docs available.
- [x] **Team on standby** – developers, ops, security know the deployment time and are available in case of issues.
- [x] **Communication plan** – if this is a new product or major update, inform relevant users or internal teams of the deployment window. Possibly put up a maintenance page if needed (for zero-downtime, maybe no need).
- [x] **DNS configured** – if launching a new domain or switching DNS, ensure it’s prepared (but maybe not switched until confirmation post-launch).
- [x] **Scaling configured** – double-check production App Service and DB are scaled to expected capacity (not accidentally left at tiny size used in testing).
- [x] **Feature flags** – if any risky feature is behind a flag, decide to turn on or keep off initially.

**During Deployment:**

- [x] Monitor the deployment process and ensure no errors.
- [x] After deployment, run sanity checks (smoke tests as described).
- [x] If any critical issue found, decide to rollback or fix forward quickly.

**After Go-live (first 24-48 hours):**

- [x] Continuously monitor logs and metrics. Possibly have someone watch live metrics for an hour after launch to catch any pattern (like increasing memory usage).
- [x] Ensure the monitoring alerts are working (you might trigger a test alert to see if notifications received).
- [x] Check that data is flowing: e.g., new entries in DB look correct, logs are coming into App Insights.
- [x] Solicit feedback from some beta users if applicable to verify functionality.
- [x] No security alarms triggered (check Azure AD sign-in logs for unusual attempts, etc., just as due diligence).

**High Availability validation:**

- If you have two instances running, try stopping one via Azure portal to see if the app still works (it should, with one instance left; Azure will restart the stopped one automatically if always_on).
- If possible, simulate a DB failover (MySQL flex might not have easy manual failover unless geo-replica). But at least know the process if DB fails (Azure will handle host failure behind scenes if zone redundant).
- Check that backups of DB are running as expected (take a manual backup or ensure point-in-time-restore is enabled).

**Maintaining Compliance:**

- Now that live, ensure you continue to follow procedures. For example:
  - If a new developer is hired, follow the onboarding checklist: give them access to repo, maybe not prod, train them on security, etc.
  - If someone leaves, remove access promptly (Azure AD and any accounts).
  - Schedule recurring tasks: e.g., quarterly access review meeting, monthly log review, etc. Put them on calendar.

**Incident drills:** Even if not immediate, plan to do a disaster recovery drill perhaps a few weeks after launch (to not destabilize initial period but still fairly soon to validate).

- E.g., simulate DB outage by restoring backup to a new server and repointing app (in a test scenario).
- Or simulate an Azure region outage by deploying to second region (if that’s in plan) and failing over DNS.

Now the application is live, serving users, and we have confidence in its security and reliability. We also have processes in place to continually support and improve it.

---

# Maintaining & Scaling the Application

Launching is not the end; an application must be maintained and scaled over its lifetime. In this final chapter, we'll discuss best practices for maintaining performance, scaling to meet demand, ensuring high availability and disaster recovery, and continuously keeping the application secure and compliant with SOC 2.

## Performance Optimizations

Over time, usage patterns may change and new bottlenecks may emerge. Continuous performance tuning is important:

- **Monitoring Performance Metrics:** Use Application Insights dashboards to watch metrics like request duration, page load times (it can capture front-end performance if you use the JavaScript SDK), and database query performance. Identify any slow trends.
- **Optimizing Frontend:**
  - Use code splitting (lazy loading) to reduce initial bundle size. If using CRA, consider dynamic `import()` for heavy components or routes.
  - Leverage browser caching: ensure static files (JS/CSS) have far-future cache headers since their names include hashes on build. App Service static content can be configured with certain headers, or if served by Spring Boot, we can add caching headers for static resources.
  - Use a CDN for static assets if not already (Azure Front Door or Azure CDN can distribute the content globally, reducing latency for distant users).
  - Optimize images (use compressed formats, proper sizes).
  - Use performance best practices in React: avoid heavy computations in render, use `useMemo` and `useCallback` to memoize expensive calculations or components that don't need to re-render often. Use the React Profiler tool to spot unnecessary re-renders.
  - If the app has a lot of data, implement pagination or infinite scroll instead of loading huge lists all at once.
  - Possibly implement web socket or SignalR for real-time updates instead of polling (if that becomes a requirement), but that has implications on infra.
- **Optimizing Backend:**
  - If some API endpoints are frequently used and computationally heavy, consider caching their responses. Spring Cache (with something like Redis as a cache store) could be introduced. E.g., cache reference data that doesn't change often.
  - Analyze database queries: enable slow query log on MySQL (Azure allows configuration) to catch queries that are slow. Add indexes or query optimizations as needed. For example, if a certain search is slow, maybe introduce a full-text index or move to a different data store like Azure Search or Elasticsearch for that feature.
  - Make sure connections to DB are reused (HikariCP pool is by default good). Monitor connection pool metrics to ensure it's not exhausted; if so, increase pool size or reduce latency of queries.
  - Profile memory usage: ensure no memory leaks. The Actuator /heapdump or a APM tool can help if memory grows unexpectedly. Sometimes caching too much or holding large data in memory could cause GC issues.
  - Tune the JVM if needed: e.g., for large heaps, use G1GC, etc. On App Service, we can set JVM options in the configuration (we already might have something like `-Xmx` set by App Service by default based on instance size).
  - Evaluate if a move to asynchronous processing would help in some areas. For example, if a certain request triggers a long process (like sending emails, generating reports), you might offload that to a background job or Azure Function to not tie up the web thread.
- **Capacity planning:** Based on the load tests and usage trends, plan scaling. For instance:

  - If CPU usage regularly goes above 70% during peak hours, scale up (to a higher tier) or out (more instances) before it hits 90-100%.
  - Similarly for DB, if it's nearing I/O or CPU limits, consider scaling to a higher tier (more vCores, more memory).
  - Keep an eye on MySQL connections usage; Azure MySQL has a connection limit per tier. If we approach it (due to many App instances each with pool), may need to scale or optimize pool sizes.

- **New Features impact:** When adding new features, consider their performance impact from design time. E.g., adding a complex join query or a heavy front-end component, think about whether it will slow things down at scale.

- **Testing after changes:** For significant changes or optimizations, rerun performance tests to ensure improvement (or at least no regression).

## Handling High Availability and Disaster Recovery

High availability (HA) means the system is resilient to certain failures and has minimal downtime. Disaster Recovery (DR) means being able to recover from catastrophic failure (like region outage) within acceptable time.

For HA:

- We have multiple App Service instances (so if one VM goes down, others still serve). Azure App Service SLA for multi-instance is higher than single instance. Ensure **Always On** is enabled (it is by default for paid plans, to keep the app warm).
- Azure MySQL Flexible Server in Zone Redundant HA mode will automatically failover if the primary node fails (with a few seconds/minute of connection blip). This is good for most single-region HA. There's no transparent multi-region for MySQL (unlike Cosmos DB which is multi-master). So for region failure, see DR.
- If using a single region, one common DR strategy is to have frequent backups and the ability to restore in another region. Azure MySQL can do geo-restore of backups to another region, but that is not instant (it might take hours to spin up).
- For mission-critical, one might set up a **Geo-Replicated MySQL** (you can create a read replica in another region, which can be promoted to write if primary fails). This can reduce downtime if region fails, at cost of complexity.
- Similarly, for App Service, have a deployment in a secondary region (maybe kept in sync via pipeline or slots). It's possible to use Azure Traffic Manager or Front Door with a priority routing: primary region active, if it's down, failover to secondary. This requires the DNS at user side to switch or front door to detect and route accordingly.
- If DR requirement (RTO) is very low (minutes), then active-active or active-passive multi-region should be set up. If RTO can be a few hours, you might do manual failover: manually restore DB backup in secondary region, deploy app there and change DNS. This needs practice though.
- Document the DR plan: e.g., "If region X goes down, we will restore service in region Y within 4 hours. Steps: restore DB from backup or promote replica, swap Traffic Manager, etc." and assign roles who does what.
- Also consider **Azure Key Vault and other dependencies** in secondary region if needed (Key Vault should also have redundancy, though one can rely on cross-region access or create a secondary vault).
- Test failover at least annually to ensure procedures are fine-tuned.

- **Data Backup**: Check backups for MySQL: configure retention to, say, 14 days or more depending on RPO requirement. Also maybe perform logical backups (mysqldump) before major changes as an extra safety.
- If any user-uploaded data (like images) stored in storage, ensure that is geo-redundant (RA-GRS storage).
- Maintain some automation for recovery: e.g., have Terraform scripts for secondary region as well (maybe disabled normally, but ready to run).

**Business Continuity:** Think beyond IT: if a disaster happens, how will you communicate to customers? Have a communication plan for incidents (maybe an email or status page update). This is often part of SOC 2 (service commitments to customers regarding uptime, etc., and how you handle exceptions).

## Scaling Strategies with Kubernetes and Azure Functions

As usage grows or features expand, you may consider evolving the architecture:

- **Microservices with Kubernetes (AKS):** If the single Spring Boot application becomes too large (monolithic) or you need to deploy components independently (e.g., an authentication service, a billing service, etc.), breaking into microservices could help. AKS would allow deploying multiple Spring Boot services and manage them. We would then need an API gateway or at least coordinate endpoints. But microservices also add overhead (network calls, etc.), so do it only if justified (e.g., different scaling needs for different components or team development independence).
- With microservices, each can be scaled individually, which can be cost-efficient if one part is heavy and others are light. Also, easier to maintain codebase boundaries. But ensure to implement inter-service security (like all services validating JWTs as we did, or using an internal auth mechanism).
- If migrating to AKS:

  - Containerize each service with Docker.
  - Use Azure Container Registry for images.
  - Setup CI pipeline to build and push images.
  - Use infrastructure-as-code (Helm charts or Terraform) to deploy to AKS.
  - Achieve similar security (Azure AD Pod Identity to access Key Vault, etc.).
  - Use Kubernetes features for self-healing and auto-scaling (Horizontal Pod Autoscaler).
  - Use Istio or Azure Front Door for ingress and perhaps service mesh if needed.

- **Serverless with Azure Functions:** Some parts of the application might be better as serverless functions, for instance:

  - Scheduled jobs (clean-ups, report generation) could be Timer-triggered Azure Functions.
  - Processing queue messages (if we offload heavy tasks to a queue).
  - Or if the entire backend could be broken into functions for each endpoint (that's essentially the idea of an API built on serverless). Azure Functions can integrate with Azure Static Web Apps to serve an API.
  - Functions scale automatically based on demand and you pay per execution, which can be cost saving for spiky workloads.
  - However, migrating a stateful restful API to functions might require some re-architecture (each function is stateless and has cold start concerns).
  - Perhaps better for adjunct tasks rather than the core API which is fine on App Service or AKS.

- **Hybrid approaches:** You can mix these. E.g., keep core service on App Service/AKS, but use an Azure Function for sending emails (triggered by a queue when user signs up) to not block the main thread and to scale that separately.
- **Scaling Database:** As the app scales horizontally, the database can become a bottleneck. Strategies:
  - Upgrade MySQL to more vCores, or move to Hyperscale (if Azure offers a MySQL Hyperscale).
  - Read replicas to distribute read load (configure the app to send read-only queries to replicas).
  - In extreme scale, consider sharding (split data across multiple DB instances by user segments). But that is complex and only if necessary.
  - Evaluate if a NoSQL database fits some parts better (for example, if you have a new feature that stores high-volume semi-structured data, maybe use Azure Cosmos DB).
- **Cost Management:** Scaling up should be balanced with cost. Continuously watch Azure cost metrics. Use appropriate sizing (not over-provisioning too much, use auto-scaling to handle peaks).
- **Continuous Deployment Pipeline:** As you adopt new services (like AKS or Functions), extend your CI/CD to cover those. Perhaps have separate pipelines per microservice to deploy independently.

## Continuous Security Updates and Compliance Adherence

Maintaining compliance is an ongoing effort. We need to:

- **Apply Updates/Patches:** Keep dependencies updated. We should periodically update the React dependencies (especially if security fixes come out for React or any library like Redux or axios). Same for backend (keep Spring Boot updated to latest minor release, and security patches).
  - Subscribe to security advisories (e.g., Spring releases, Node security announcements).
  - Use Dependabot or Renovate to automatically create PRs for updates and test them.
  - The underlying platform (Azure) takes care of OS patching for App Service and managed MySQL. If on AKS, ensure to regularly update base images and cluster nodes (Azure occasionally upgrades AKS versions; schedule those).
- **Rotation of Secrets/Keys:** Have a schedule to rotate secrets like database passwords, or certificate renewals.
  - Azure Key Vault makes this easier (you can set an expiry on secrets and get reminded).
  - If you use any credentials (like perhaps a storage account key), rotate it periodically and update config.
  - Rotation ensures that even if a secret leaked unknown to us, it would eventually become invalid.
- **Continuous Monitoring:** Keep the monitoring alerts on. Consider adding new ones if new threats identified. Also ensure someone is assigned to respond to alerts at all times (on-call rotation).
- **Regular Audits:** Even outside of formal SOC 2 audits, perform internal audits. For example, every 6 months do an access review: check Azure AD user list, remove any that are no longer needed; review roles in Azure portal.
- **Training and Awareness:** Keep the team’s security knowledge up-to-date. New devs should get training on secure coding. The threat landscape evolves (e.g., new OWASP Top 10 items). Possibly have annual refresher training which can be evidence for SOC 2 "security awareness training" criterion.
- **Incident Response Drills:** Do drills (like simulate a breach scenario and see if team follows the runbook, and improve it).
- **Policy Updates:** Revise policies as the system changes. If we add a new microservice, update architecture diagram and maybe update policies (e.g., add that microservice to scope of access control policy).
- **Continuous Compliance Tools:** If using a tool like Drata, Vanta, or Azure's Regulatory Compliance dashboard, watch the controls status. Azure Security Center has a compliance blade that maps Azure configuration to various standards including SOC 2, giving you a score. Use that to identify any gaps (e.g., it might complain if something isn't encrypted or if logs not enabled somewhere).
- **Documentation of Changes:** Maintain records whenever you make significant changes to the system (for audit trail). E.g., if you apply a performance fix that changes a config, note it somewhere (in change management system). Our Git history and pipeline logs already provide a lot of that automatically.
- **Next SOC 2 Audits:** For a SOC 2 Type 2 audit (which covers a period), ensure you're collecting evidence throughout that period. By the time auditors come, you should have everything (log samples, meeting notes of risk assessments, etc.).

In essence, treat compliance as part of normal operations, not a once-a-year scramble. Many aspects (logging, monitoring, access control) we integrated from the start so they naturally produce evidence.

Finally, aim for a culture of security and reliability in the team. Encourage raising concerns if anyone spots a potential security risk or compliance issue. Address them proactively.

---

With all these steps, we have built a full-stack ReactJS + Spring Boot application on MySQL and Azure that is not only functional and scalable but also **SOC 2 compliant** in terms of security, availability, and confidentiality.

By following this guide, advanced developers can implement such a system step-by-step, embedding best practices at every stage – from coding to infrastructure to operations – resulting in an application that can pass rigorous security audits while serving users effectively.
