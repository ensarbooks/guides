# 1. Introduction

## Overview of Full-Stack Development

Full-stack development refers to building both the front-end and back-end components of an application. A _front-end_ deals with the user interface and user experience in the browser (often using HTML, CSS, and JavaScript), while a _back-end_ handles server-side logic, database interactions, and business rules. In a full-stack project, developers work on **all layers** of the application to deliver a complete product. According to AWS, _"Full stack development is the process of developing both the frontend and backend of applications... The frontend contains the user interface and code related to user interactions... The backend contains all the code required for the application to run, including integrations with data systems, communicating with other applications, and processing data."_ ([What is Full Stack Development? - Full Stack Development Explained - AWS](https://aws.amazon.com/what-is/full-stack-development/#:~:text=Full%20stack%20development%20is%20the,other%20applications%2C%20and%20processing%20data)). This integrated approach allows a team to build an application end-to-end in a cohesive manner ([What is Full Stack Development? - Full Stack Development Explained - AWS](https://aws.amazon.com/what-is/full-stack-development/#:~:text=Software%20developers%20require%20slightly%20different,in%20a%20single%20code%20base)).

Working as a full-stack developer requires knowledge of multiple technologies and the ability to design how different parts of the system communicate. It means being comfortable creating responsive UIs _and_ designing robust APIs or database schemas. Full-stack teams can be more efficient by reducing hand-offs between specialized front-end and back-end teams. However, they also must maintain clarity in how the components interact and ensure that **both** sides of the application meet security and performance standards.

In modern web development, a typical full-stack project might use a JavaScript framework like **ReactJS** for the client-side, a server-side framework like **Spring Boot** (Java) for the API, a database like **MySQL** for data storage, and cloud services (e.g. **AWS**) for deployment and infrastructure. This guide will use that technology stack as an example, illustrating how to build each layer and integrate them securely.

## Importance of ISO 27001 Compliance in Application Development

Security cannot be an afterthought in full-stack development. **ISO/IEC 27001** is an international standard for Information Security Management Systems (ISMS) that provides a framework for managing and protecting sensitive data. Compliance with ISO 27001 demonstrates that an organization follows best practices to secure information. For developers, this means incorporating security controls and processes throughout the software development lifecycle, not just in production. Following ISO 27001 guidelines helps ensure that from day one of the project, you are considering risks and protecting data properly.

In recent updates, ISO 27001 has put a stronger emphasis on application security. The 2022 revision of the standard explicitly includes controls related to secure software development. In fact, _"application security has become a crucial component of ISO 27001 compliance, particularly in the recently updated 2022 version"_ ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=Information%20security%20professionals%20are%20well,general%20insights%20and%20best%20practices)). This means organizations seeking compliance (or certification) must pay attention to how applications are designed, coded, tested, and deployed with security in mind. Traditional network perimeter security is not enough; ISO 27001 now expects security to be \*_“baked into every aspect of your software development process, from secure design principles right through to managing third-party code”_ ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=Incorporating%20application%20security%20measures%20into,party%20code)).

Following ISO 27001 in development leads to concrete practices such as enforcing secure coding standards, performing risk assessments for new features, controlling access to code and data, and ensuring proper logging and monitoring. These practices reduce the likelihood of vulnerabilities and data breaches. Moreover, many organizations and clients require ISO 27001 compliance (or the closely related **SOC 2** framework) as a condition of doing business, especially when building enterprise or financial applications. Adhering to ISO 27001 not only improves security but also provides a competitive advantage and trust signal, as it _"demonstrates an organization’s ability to secure its data"_ ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=Information%20security%20professionals%20are%20well,ISO%2027001%20compliance%2C%20particularly%20in)).

Throughout this guide, we will highlight how each step – from setting up the project, to writing code, to deploying on AWS – can be done in a way that supports ISO 27001 compliance. This includes referencing relevant controls (for example, secure coding corresponds to Annex A.8.28 in ISO 27001:2022), and showing how following best practices aligns with the standard. By the end, you should not only understand how to build a full-stack React/Spring Boot/MySQL application, but also how to do so in a manner that meets high security standards and is ready for ISO 27001 audits.

## Key Technology Stack: ReactJS, Spring Boot, MySQL, AWS

**ReactJS (Front-End):** React is a popular JavaScript library for building dynamic user interfaces. It allows developers to create reusable UI components and manage application state efficiently for single-page applications (SPAs). In our full-stack app, React will handle the client-side, rendering the views that users interact with in their web browser. We will use modern React features (such as functional components and hooks) to implement a responsive and secure front-end. React’s component-based architecture will help organize the front-end code and make it maintainable. Security-wise, we will need to use React carefully to avoid common issues like Cross-Site Scripting (XSS) by sanitizing any dynamic content and not exposing sensitive data in the front-end code.

**Spring Boot (Back-End):** Spring Boot is a Java-based framework that simplifies building robust back-end REST APIs and microservices. It comes with embedded servers and auto-configuration to get a backend service running quickly. We’ll use Spring Boot to implement the server-side logic of our application – handling HTTP requests, executing business logic, and interacting with the database. Spring Boot has excellent integration with **Spring Security**, which we will leverage for implementing authentication, authorization (like role-based access control), and other security features (such as CSRF protection and content security policies). The back-end will enforce security controls on data access, ensuring that only authorized users can perform certain actions, which is crucial for compliance.

**MySQL (Database):** MySQL is a widely-used open-source relational database. It will store the application’s data persistently. Designing the database schema securely and efficiently is an important part of the project. We will cover how to define tables and relationships for data integrity, as well as how to secure MySQL – for example by using least-privilege database users and enabling encryption in transit and at rest. Secure database practices like using prepared statements (to prevent SQL injection) and performing regular backups will be discussed in depth. MySQL will likely be deployed as a managed service on AWS (using Amazon RDS) to simplify management and enhance reliability.

**AWS (Deployment & Cloud Services):** Amazon Web Services will host our application. AWS provides cloud infrastructure and platform services that we will use for deployment and operations, such as Amazon EC2 for running the Spring Boot server, Amazon RDS for the MySQL database, Amazon S3 (and possibly CloudFront CDN) for hosting the React front-end, and IAM for managing access permissions. AWS is itself compliant with many security standards and offers tools to help build secure applications. (Notably, AWS operates under a **shared responsibility model**: AWS manages the security _of_ the cloud infrastructure, while you are responsible for security _in_ the cloud, i.e., your applications and data ([ISO 27001 Compliance: 2025 Complete Guide | StrongDM](https://www.strongdm.com/iso-27001#:~:text=controls,to%20maintain%20security%20standards%20for)).) We will ensure that we configure AWS services securely — for instance, using IAM roles instead of static credentials, applying security groups and network ACLs to limit access, enabling encryption for data storage (RDS and S3), and using AWS Certificate Manager for SSL/TLS certificates. Integrating CI/CD with AWS will also be covered, showing how we can automate deployment securely.

By combining these technologies, we get a modern tech stack suitable for building scalable web applications. The React front-end will communicate with the Spring Boot back-end via secure APIs (HTTPS requests), and the back-end will read/write data to MySQL. AWS will provide the environment in which all these components run and communicate. Each layer comes with its own best practices and potential pitfalls — which this guide will address step by step.

**Security & Compliance Focus:** At each step of using this tech stack, we will incorporate security best practices aligned with ISO 27001. For example, React will be set up to avoid common vulnerabilities in front-end code, Spring Boot will be configured to enforce security (using Spring Security for OAuth2/JWT), MySQL will be hardened (with access control and encryption), and AWS will be configured to protect resources (using IAM, VPC isolation, etc.). Logging, monitoring, and documentation requirements from ISO 27001 will be highlighted so that by the end, the project is not just functional, but also secure and compliant.

---

# 2. Project Setup and Architecture

Before diving into coding, it’s essential to set up the project structure and development environment properly. Good architecture and setup will make the application scalable, maintainable, and easier to secure. In this chapter, we will discuss how to organize the code (monolithic vs. microservices, monorepo vs. multiple repos), what tools to use for development and build, and how to establish a reliable CI/CD pipeline. We’ll also cover how these choices affect scalability and ISO 27001 compliance (for example, controlling access to the codebase and using CI/CD to enforce quality).

## Setting Up a Monorepo vs. Microservices Architecture

When starting a full-stack project, one architectural decision is whether to keep all code in a **single repository (monorepo)** or split it into multiple repositories (polyrepo), and whether the back-end will be a single monolithic service or multiple microservices. Each approach has pros and cons:

- **Monolithic Architecture:** A monolithic application is built as one unified unit (one deployable). All front-end and back-end code could even live in one project. This can simplify initial development and deployment – especially for smaller applications or teams – because there is a single codebase and build to manage. However, as the project grows large, a monolith can become hard to maintain or scale. Feature deployments are interdependent (one big deploy) and scaling requires scaling everything together ([ Microservices vs. monolithic architecture | Atlassian ](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith#:~:text=A%20monolithic%20application%20is%20built,on%20a%20number%20of%20factors)).

- **Microservices Architecture:** In a microservices approach, the application is broken into smaller, independently deployable services that communicate over network APIs. For example, you might have separate services for user management, orders, billing, etc. This allows each microservice to be developed, scaled, and deployed independently. Netflix’s architecture is a famous example, where they migrated from a monolith to “more than a thousand microservices” to support their scale ([ Microservices vs. monolithic architecture | Atlassian ](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith#:~:text=Netflix%20became%20one%20of%20the,thousands%20of%20times%20each%20day)). Microservices can make large applications more _manageable_, but come with added complexity (service orchestration, inter-service communication, eventual consistency, etc.). Deciding on microservices often depends on the size and complexity of the system. If you anticipate needing to scale different parts of the application differently or have separate teams working on different features, microservices may be beneficial. If not, a monolith may suffice initially.

- **Monorepo:** This is a source control strategy where _all_ code (perhaps multiple services or front-end and back-end) lives in one repository. _“A monorepo is a single centralized repository for all your application and microservice code... encompassing the entire codebase in one repository.”_ ([Benefits and challenges of monorepo development practices | CircleCI](https://circleci.com/blog/monorepo-dev-practices/#:~:text=A%20monorepo%20is%20a%20single,even%20datasets%20and%20configuration%20files)). The monorepo approach can simplify dependency management and code sharing, since everything is in one place. It encourages consistent coding practices across the stack and makes it easier to track changes that span front-end and back-end. For example, if a change in the back-end API requires a change in the front-end, a monorepo can have one commit that updates both together, keeping them in sync. It also simplifies CI/CD setup in some cases, as you can have one pipeline that builds and tests everything. However, monorepos require careful organization as the project grows to avoid confusion and slow build times. Tools like Nx or Lerna (for JavaScript) or Gradle multi-project builds (for Java) can help manage monorepos.

- **Polyrepo (Multiple Repositories):** Alternatively, you might keep the front-end in one repository and the back-end in another, or each microservice in its own repo. This is common in microservices architectures (each service is an independent project). It provides clear separation of concerns and access control (e.g., giving a team access to only the repo of the service they work on). However, it can introduce overhead in coordinating changes across repos and ensuring compatibility. Also, managing multiple repositories (with possibly different versioning and release cycles) can be complex as the number of services grows ([Benefits and challenges of monorepo development practices | CircleCI](https://circleci.com/blog/monorepo-dev-practices/#:~:text=With%20microservices%20architecture%20being%20a,NET%20to%20implement%20APIs)). With many repos, knowledge can become siloed (one team might not know changes in another’s repo), which can be a risk. There is also a risk that _"no one knows how to build and deploy the entire system"_ if knowledge is too scattered ([Benefits and challenges of monorepo development practices | CircleCI](https://circleci.com/blog/monorepo-dev-practices/#:~:text=Separate%20repositories%20introduce%20risk)).

For our example project, we might choose a **monorepo** containing two main folders: `/frontend` (for the React app) and `/backend` (for the Spring Boot app). This way, we can manage issues and features in one place and ensure front-end and back-end remain compatible. Within the back-end, we could still structure the code in a modular way (for example, using a layered architecture or even breaking into microservices later if needed). Many teams start with a monolithic back-end in a monorepo, then extract microservices over time as needed (this can be aided by frameworks like Spring’s modularization or by careful domain-driven design).

From a **compliance and security** standpoint, a monorepo can simplify enforcing certain policies: for example, you can apply the same code scanning tools and access controls to one repo. If using a private git repository, ensure **access control** is implemented (only authorized developers can access the code). ISO 27001 will require that your code repository has proper access permissions and possibly logging of changes (version control inherently logs commits and authors). If using multiple repos, you must manage access for each, which is more overhead. Regardless of repo strategy, make sure to follow the principle of least privilege – only grant repository access to those who need it (developers, CI service accounts, etc.) ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=Follow%20the%20principle%20of%20least,if%20their%20credentials%20are%20compromised)).

In summary, choose the architecture that fits the project’s size and team structure:

- _For a small-to-medium application:_ A monolithic back-end and monorepo are often simplest to start with.
- _For a large application or multiple independent teams:_ Microservices with possibly multiple repos might be considered, but you'll need robust DevOps practices to manage them.

We will proceed with a single Spring Boot service (monolithic back-end) and a React front-end, in a monorepo, as our example. We'll keep the design modular (e.g., separate layers or modules in Spring Boot for different domains) to ease any future transition to microservices if needed.

## Tools and Best Practices for Scalable Development

Building a scalable application requires using the right tools and following best practices from day one. Here are some key aspects and recommendations:

- **Version Control with Git:** Use Git for source control, which is the industry standard. Create a repository (e.g., on GitHub or GitLab or Bitbucket) for your project. Since we choose a monorepo, both front-end and back-end code will reside in this repo (e.g., in separate directories). Establish a branching strategy: for instance, a protected `main` (or `master`) branch where only reviewed code is merged, and feature branches for development. This ensures an organized workflow and traceability of changes. Tie Git commits to issue tracker IDs if possible, and write clear commit messages for audit trails (helpful for ISO 27001 to show change management).

- **Project Management & Issue Tracking:** Use a tool like Jira, Trello, or GitHub Issues to track features, bugs, and tasks. This not only helps team collaboration but also serves as documentation of changes and decisions (which is useful for compliance, demonstrating a controlled development process). For ISO 27001, you might need to show that changes are managed and approved – a ticketing system can provide that evidence.

- **Development Environment Setup:** Each developer should have a secure and standardized environment. This might involve:

  - Installing the correct Node.js version (for React) and Java JDK (for Spring Boot).
  - Using dependency management: **npm or Yarn** for JavaScript packages, **Maven or Gradle** for Java. We will use Maven or Gradle to manage Spring Boot dependencies and npm for React.
  - Setting up environment variables or configuration files for sensitive config (like API keys, DB passwords) so they are not hard-coded. Ensure that default dev configurations do not expose secrets and encourage use of a `.env` file (for React) and `application.properties` (for Spring) that can be overridden for production with secure values (we'll cover this more in deployment).

- **IDE and Code Quality Tools:** Encourage using good IDEs (VSCode for React, IntelliJ or VSCode for Java, etc.) with linters/formatters configured. For example, enable ESLint and Prettier for React to catch code smells and enforce a consistent style. For Java, use SpotBugs or SonarLint in the IDE to catch common bugs or security issues early. Consistent coding standards and automated formatting make the codebase maintainable as it grows.

- **Dependency Management and Updates:** Keep track of third-party libraries and their versions. Outdated dependencies can have vulnerabilities. It's a best practice to periodically review and update them. Using tools like Snyk, Dependabot, or OWASP Dependency-Check can automate alerts for vulnerable libraries. (This is also tied to ISO 27001 compliance – Annex A has controls for using security in development and managing vulnerabilities in components. Regular updates _"to mitigate security vulnerabilities, especially in libraries"_ ([Advanced Spring Boot Security: Implementing OAuth2, JWT, and Custom Authentication – Code Frosting](https://www.codefro.com/2024/08/29/advanced-spring-boot-security-implementing-oauth2-jwt-and-custom-authentication/#:~:text=,in%20libraries%20like%20Spring%20Security)) is considered a best practice.)

- **Code Structure:** Organize the repository clearly. For example:

  - `frontend/` for React app – inside which you might have `src/components/`, `src/services/` (for API calls), etc.
  - `backend/` for Spring Boot – you can follow a standard Maven structure (`src/main/java/...` with packages for controller, service, repository, model, etc.). If the back-end is large, consider a **layered architecture** (controllers -> services -> repositories) or even a modular approach (group by feature/domain).
  - Add a `README.md` at the root explaining how to build and run each part, so new developers or auditors can easily find instructions.
  - Use descriptive names and keep secrets out of the code (if any config files with secrets, add them to `.gitignore` so they aren't committed).

- **Secure Development Best Practices:** From day one, enforce secure coding guidelines. This includes things like:

  - Not logging sensitive information (no passwords or personal data in logs).
  - Input validation rules (we will implement later).
  - Output encoding to prevent XSS (relevant in front-end templates, etc.).
  - Using parameterized queries (we'll use ORMs which handle this, but be mindful if using raw SQL).
  - These practices should be documented in a developer guide or secure coding policy (which ISO 27001 would require – _“secure coding principles shall be applied to software development”_ ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=Research%20shows%20that%20developer%20security,apply%20to%20writing%20secure%20code))). Make sure the team is aware of them, possibly through a kickoff training session. Developer education is key; as the ISO standard notes, focusing on common weaknesses (like those in OWASP Top 10) helps prevent vulnerabilities early ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=%3E%20%20%20,)).

- **Automated Testing from the Start:** We will go in-depth on testing in a later chapter, but as part of project setup, configure the testing frameworks. For React, set up Jest and React Testing Library for unit tests. For Spring Boot, use JUnit and possibly integration test support (Spring Boot has testing starters to easily spin up the application context for tests). Having at least a basic test in each to verify the setup works (e.g., a dummy test that always passes or a simple health-check test) helps ensure CI is wired correctly. Also consider setting up linting tests (so CI fails if code style or simple static analysis finds issues).

- **Documentation and Configuration Management:** Keep track of configuration in a secure way. For example, maintain sample config files (like `.env.example` and `application-example.properties`) to show what variables are needed without actual secrets. Use a secure vault for real secrets in dev/test if possible (for instance, using AWS Secrets Manager or HashiCorp Vault, which we’ll discuss later). ISO 27001 compliance often requires controlling documentation – even config files can be considered documentation that should be managed. Using source control for config (with placeholders or encrypted values) ensures you have version history of config changes as well.

- **Continuous Integration (CI):** Set up a CI system that automatically builds and tests the application whenever changes are pushed. This could be done with services like GitHub Actions, GitLab CI, Jenkins, etc. We'll cover CI/CD in more detail, but early on, decide on the CI platform and create a basic pipeline definition. For example, a simple pipeline might install dependencies and run unit tests for both front-end and back-end. This helps catch integration issues early and enforces code quality. It’s easier to add security scans and deployment steps to an existing pipeline than to create one later under time pressure.

By following these best practices and using these tools, you set a strong foundation for development. This proactive approach is also aligned with ISO 27001’s emphasis on planning and control in development. The standard expects that you _plan_ for security – including selecting appropriate development environment controls and tools – as part of the project initiation ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=Phase%201%3A%20Planning%20and%20before,coding)). Document decisions like architecture choices and tool selections, as this documentation shows auditors that you have a considered process (and helps new team members understand the project).

## Git Repository and CI/CD Pipeline Overview

**Initializing the Git Repository:** Once the project structure (folders for front-end and back-end) is in place, initialize a git repository and push it to a remote (e.g., GitHub). Set up essential protections:

- Protect the main branch: require pull request reviews before merging, and perhaps CI passing status. This ensures no direct unchecked commits go into the main codebase (important for change control).
- Enable branch rules like requiring at least one approval (which aligns with having peer code reviews – a practice highly recommended for quality and security ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Code%20reviews%20are%20essential%20for,sensitive%20data%2C%20maybe%20you%20should))).
- If possible, enable signing of commits or at least tag releases for traceability.

**Continuous Integration (CI):** A CI pipeline automates building and testing your code on every commit or pull request. This helps maintain code quality and catches errors early. Outline of a typical CI pipeline for our stack:

1. **Checkout code** – the pipeline pulls the latest code from the repo.
2. **Set up environment** – e.g., install Node.js for front-end and JDK for back-end on the CI runner.
3. **Build Front-end** – e.g., `npm ci && npm run build` for the React app. Optionally, run front-end linters/tests: `npm run lint`, `npm run test`.
4. **Build Back-end** – e.g., `./mvnw clean verify` (if using Maven) to compile and run tests for the Spring Boot app. This will also ensure that the code meets quality checks (like failing the build if tests fail or if code coverage is below a threshold, if configured).
5. **Security Scans** – integrate security steps: for example, run **OWASP Dependency-Check** to scan for vulnerable dependencies in the back-end, or use a SAST tool to analyze code for known bad patterns. This can be done with plugins or separate steps. Some CI services have built-in security analysis (GitHub has CodeQL scanning, GitLab has SAST templates).
6. **Package Artifacts** – e.g., archive the built front-end static files (for deployment to S3) and the Spring Boot JAR (for deployment to EC2 or container). This ensures the outputs are ready to deploy.
7. **(Optional) Deploy to test environment** – In a CI stage or a separate CD pipeline, you might deploy automatically to a staging environment for further testing.

Using GitHub Actions as an example, a workflow YAML might define jobs for front-end and back-end in parallel. Each job would use appropriate runners (Ubuntu runner can handle both Node and Java). We would also configure secrets (like AWS credentials or keys) in the CI platform's secret store, not in code. **Never store sensitive credentials in the repository** – this is a critical compliance and security point. Instead, CI can inject them as environment variables for deployment steps if needed.

**Continuous Delivery/Deployment (CD):** Once CI ensures builds are good, CD takes over to deploy to environments:

- For example, upon merging to `main`, you might trigger a deployment to a **staging** environment on AWS. This could be automated via GitHub Actions or AWS CodePipeline. In staging, the team can perform more tests (including security tests like running a dynamic scanner).
- When ready to go live, a manual approval (change management) step can be used to deploy to **production**. This manual gate is often required in regulated environments. You would document who approved the deployment (for ISO 27001, keeping records of changes and approvals is important).

**AWS CodePipeline alternative:** AWS offers CodePipeline and CodeBuild services to implement CI/CD natively in the cloud. For instance, CodePipeline can watch a CodeCommit repository (or even GitHub) and trigger CodeBuild jobs to build/test and then a deployment action (like CodeDeploy to EC2 or CloudFormation changeset, etc.). For a monorepo with microservices, AWS suggests configuring separate pipelines per service, triggered by changes in specific paths ([Automatically detect changes and initiate different CodePipeline pipelines for a monorepo in CodeCommit - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automatically-detect-changes-and-initiate-different-codepipeline-pipelines-for-a-monorepo-in-codecommit.html#:~:text=This%20pattern%20helps%20you%20automatically,improved%20collaboration%2C%20standardization%2C%20and%20discoverability)). In our simpler case, one pipeline can handle both front-end and back-end. If going this route, ensure to follow AWS best practices, such as using IAM roles for CodeBuild with least privileges (only allow it to do what’s necessary, like upload artifacts or deploy).

**Scalability of CI/CD:** As the project grows:

- Ensure the pipeline remains efficient. For monorepo, you can optimize by only building what changed (though initially building both parts is fine, it’s not too heavy).
- The CI infrastructure should handle multiple developers pushing frequently. Cloud-based CI scales automatically usually, but watch out for queue times.
- Keep pipeline configurations in code (e.g., YAML in repo or CodePipeline definitions in CloudFormation) – this is Infrastructure as Code principle, making the CI/CD config auditable and versioned.

**Compliance Considerations for CI/CD:** ISO 27001 will expect that the deployment process is controlled:

- Only authorized individuals or automated processes should be able to deploy to production. Using CI/CD with role-based access (and logging) satisfies this. For example, in AWS CodePipeline, use IAM to restrict who can trigger or approve deployments.
- Maintain logs of deployments. CI tools usually log build and deploy steps; store those logs (e.g., in AWS CloudWatch or CI system) to demonstrate what was deployed when and by whom.
- Segregation of duties: It's a good practice to enforce that code authors are not the only approvers of their code deployment. Having peer review and a separate ops or tech lead approving production deploys adds to security. This can be implemented by code review requirement and manual approval steps.
- Secrets in CI: ensure the CI environment protects secrets (most managed CI solutions do, by encrypting them). Never output secrets in logs. This is part of secure pipeline configuration.

By setting up a robust CI/CD pipeline, you achieve several things: faster development feedback, higher quality releases, and a documented, repeatable deployment process. This aligns with ISO 27001 requirements for **change management and system development control** because every change is built, tested, and tracked automatically. As we build out the application, the CI/CD pipeline will be extended with more tests (including security tests) and deployment steps, which we will detail in later chapters.

---

# 3. Front-End Development (ReactJS)

In this chapter, we'll focus on the front-end aspect of the application using **ReactJS**. We'll cover how to set up a React project in a secure way, implement authentication and authorization on the client-side (working with OAuth2 and JWT tokens), securely integrate with the back-end API, validate user input, and follow best practices in component architecture. Even though much of security is enforced on the server, the front-end plays a critical role in protecting user data and providing a secure user experience (for instance, how it handles tokens, or sanitizes data to prevent XSS). Additionally, a well-structured front-end codebase is key to maintainability as the application grows.

## Setting Up a Secure ReactJS Environment

To get started, we'll initialize a new React application. One common approach is to use **Create React App (CRA)**, which bootstraps a React project with a lot of sensible defaults. Alternatively, one could use **Vite** for a faster build or frameworks like **Next.js** if server-side rendering is needed (though here we'll stick with a SPA approach). For our purposes, let's assume using CRA for simplicity:

```bash
npx create-react-app frontend --template cra-template-pwa
```

This command would create a React app in the `frontend` directory. We might use the PWA template (progressive web app) which includes a service worker setup; service workers can cache assets and improve performance, but we should be careful with them in terms of security (ensure they don't cache sensitive API responses unintentionally).

**Secure Configuration of React App:**

- **Node and NPM:** Ensure you are using a recent LTS version of Node.js for security and compatibility. Keep the `package.json` dependencies updated. Remove any unused dependencies which could present an attack surface.
- **Environment Variables:** CRA allows using a `.env` file for defining environment-specific variables (prefixing them with `REACT_APP_`). Ensure no secrets (like API keys or sensitive URLs) are committed in `.env`. For instance, the API base URL can be defined as `REACT_APP_API_URL="https://api.example.com"`. In production, you'll set this appropriately. It's crucial to remember that anything in the front-end code or variables is **visible to the end-user** (after build, variables get inlined). So, **do not put secret keys (like AWS secret keys, or DB credentials)** in React code. If you have to use an API key (say for a third-party service like Google Maps), restrict it via the service's settings (e.g., domain whitelisting) since it will be exposed.
- **HTTPS in Development:** When running the dev server (`npm start`), consider using HTTPS even locally. CRA allows an environment variable `HTTPS=true` to run the dev server over HTTPS. This helps catch any mixed-content issues early and ensures you're always testing with encryption. It also more closely mimics production where you'll use HTTPS. All API calls from React should be to `https://` endpoints as well. In production, our app will be served over HTTPS (we'll use AWS Certificate Manager for that).
- **ESLint and Strict Mode:** CRA comes with ESLint set up. Keep it enabled and possibly extend the config to include security linting rules (for example, there's an ESLint plugin for React security or you can integrate the ESLint rules from the OWASP JS Security guide). Also, React Strict Mode (enabled by default in CRA index) helps highlight potential issues (not security per se, but catches unsafe lifecycles, etc., which improves robustness).
- **Dependencies and Vulnerabilities:** Run `npm audit` after setting up to see if any dependency has known vulnerabilities. Fix or upgrade if so. CRA's template is usually up-to-date. Add a periodic `npm audit` (or use `npm audit fix`) step in development to ensure front-end deps remain secure.

**Folder Structure and Components:** Out of the box, CRA gives a basic structure. We should organize our React app logically:

- `src/components/` for presentational components.
- `src/pages/` or `src/views/` for page-level components (if using React Router).
- `src/services/` for things like API client code (e.g., a file `api.js` to encapsulate `fetch` or Axios calls).
- `src/context/` for Context API providers if using context for auth state.
- `src/utils/` for utility functions (like validators).
- Ensure that this structure prevents any one file from becoming too large or doing too many things (Single Responsibility Principle for components).
- If using TypeScript (which is recommended for large projects to catch type errors), set it up (`npx create-react-app frontend --template typescript`). It adds compile-time checking that can prevent certain bugs.

**Hardening the Development Setup:**

- **Browser Security Extensions:** During development, consider using a tool like the React Developer Tools extension for debugging, but also test with security-focused extensions (like an extension that blocks third-party scripts, or simulate disabled cookies) to see how your app behaves. This can reveal assumptions in code (e.g., if cookies are blocked, does auth break? If so, we may need better error handling).
- **CORS Configuration:** The dev server by default proxies API requests to avoid CORS issues if set in `package.json` (with `"proxy": "http://localhost:8080"` for example). For security, ensure that in production, the CORS settings on the back-end are configured to only allow the expected domain. We'll address this in the back-end, but from the front-end side, just be aware of CORS. During development, we might use a permissive setting, but for production, lock it down to the site’s domain (compliance note: restricting cross-origin access reduces risk of unauthorized use of your API).

**Initial Commit:** After setting up, commit the initial React app (without sensitive info). This baseline will serve as a checkpoint. From here, we'll start adding features like authentication.

## Implementing Authentication and Authorization with OAuth2/JWT

In a modern web app, authentication (logging users in) and authorization (restricting access based on user roles/permissions) are critical. We will implement an OAuth2/OIDC + JWT based authentication flow. The idea is:

- Users will log in through an OAuth2 process (which could involve our Spring Boot back-end as the auth provider or an external Identity Provider).
- Upon successful login, the user will obtain a **JWT (JSON Web Token)** that encodes their identity and roles.
- The React app will store this JWT securely (and not expose it to scripts) and attach it to API requests to authenticate with the back-end.
- The back-end will verify the JWT on each request to ensure the user is valid and has the required permissions.

**Choice of OAuth2 Flow:** For single-page applications (SPAs) like React, the recommended OAuth2 flow is **Authorization Code with PKCE (Proof Key for Code Exchange)**, _not_ the implicit flow. In older times, SPAs used the implicit flow to get tokens directly in the URL, but this has known security drawbacks. As an OAuth expert puts it, _"Implicit flow is no longer considered the best option for SPAs. Instead... use the Code Flow with PKCE because it’s more secure."_ ([Authorization Code Flow with PKCE (OAuth) in a React application | Mario Fernandez](https://hceris.com/oauth-authorization-code-flow-pkce-for-react/#:~:text=Now%20that%20you%E2%80%99ve%20learned%20about,love%20the%20argument%20by%20security)). PKCE allows the SPA to securely obtain an authorization code and then exchange it for tokens without needing a client secret (since public clients can’t safeguard a secret).

There are two main ways to implement auth in our scenario:

1. **Use an External Identity Provider (IdP):** e.g., Keycloak (self-hosted), Auth0, Okta, or AWS Cognito. These can handle user sign-up, login, and multi-factor auth, and provide JWTs. The React app would redirect the user to the IdP's login page (or use a hosted widget), and the IdP redirects back with the auth code which the React app exchanges for a JWT (via the IdP's OAuth2 endpoints). This is a robust approach and offloads a lot of security to well-tested services (and aligns with the best practice of using OpenID Connect ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=OpenID%20Connect%20,feature%20and%20dynamic%20client%20registration))).
2. **Use Spring Boot as the Auth server:** Spring Security can act as an OAuth2 Authorization Server (though as of Spring Security 5/6, the Authorization Server is a separate project). Alternatively, implement a simpler username/password login form in React that hits a Spring Boot `/login` API, which validates credentials (against a user DB) and returns a JWT signed by the server. This is a custom JWT auth approach.

For demonstration, we'll outline the second approach (custom JWT auth via our Spring Boot) as it's easier to illustrate end-to-end. But keep in mind, using a full OAuth2 Authorization Code flow with a proven IdP is recommended for production if possible (less custom code to secure).

**Client-Side Login Flow (custom JWT approach):**

- The user accesses the React app and is presented with a Login page (e.g., at route `/login`).
- The React app has a form for username and password. On submit, it sends a request to the back-end API endpoint (for example, `POST /api/auth/login`) with the credentials. This request must be sent over HTTPS (always).
- The back-end validates the credentials and, if valid, responds with a JSON containing a JWT (and possibly a refresh token if using them).
- The React app receives the JWT. Now, **how to store the token securely on the client?** The most secure way is to store it in an **HTTP-only cookie** with the `Secure` flag, so that it’s not accessible via JavaScript, mitigating XSS risk ([Securing Your React Apps: Best Practices](https://www.walturn.com/insights/securing-your-react-apps-best-practices-for-authentication-and-authorization#:~:text=Tokens%20,secure%20user%20authentication)). Alternatively, storing in memory (React state or a context) is okay for an SPA (it’s not persisted, so if the user refreshes the page, they’d have to log in again unless we use a refresh token or something). Storing in `localStorage` or a regular cookie accessible to JS is not recommended, because XSS could compromise the token. The best practice: have the back-end set an `HttpOnly` cookie on the login response containing the JWT. However, since our front-end and back-end might be on different domains, setting cookies requires correct CORS and cookie attributes (and the domain attribute possibly). Another approach is for the React app to receive the token and immediately store it in a cookie via client script with `document.cookie` with `HttpOnly` not possible (HttpOnly can only be set by server), so better to have server set it.

For simplicity, we can assume the JWT comes in response and React stores it using the **Web Storage API** initially, but with clear understanding of the risks. We will mitigate by using short-lived tokens and renewal flows:

- Use `localStorage` only if we implement proper XSS protections and possibly rotate tokens frequently. Many discussions favor cookies for security because _"Store the token in an http-only cookie, so nobody can access it. The JWT will then be sent on each request automatically"_ ([Most Secure/Best Practice for storing jwt on frontend : r/reactjs - Reddit](https://www.reddit.com/r/reactjs/comments/sivveh/most_securebest_practice_for_storing_jwt_on/#:~:text=Most%20Secure%2FBest%20Practice%20for%20storing,that%20will%20verify%20its%20integrity)), which helps against XSS. The downside of cookies is potential CSRF, but we can handle that.

Let's assume our back-end when provided credentials will return a JWT and a flag if it wants it stored as cookie. We might implement storing JWT in `localStorage` for now but we will ensure our front-end code is as XSS-free as possible (so that risk is low), and address CSRF by requiring the JWT as a Bearer token header (so a cookie would not be the only protection).

**Implementing Login Component (React):**
We create a component `Login.jsx`:

```jsx
import React, { useState } from "react";
import axios from "axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/auth/login`,
        { email, password },
        { withCredentials: true } // include this if server sets HttpOnly cookie
      );
      const token = response.data.token;
      // Store token securely
      localStorage.setItem("authToken", token); // or rely on HttpOnly cookie from server
      // Redirect or update app state to indicate user is logged in
      window.location.href = "/dashboard";
    } catch (err) {
      setError(
        "Login failed: " + (err.response?.data?.message || "Unknown error")
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Sign In</button>
    </form>
  );
}
```

This simplistic example uses axios to send a POST to the login API. Note `withCredentials: true` – this is needed if the server is on a different domain and is setting a cookie; it tells the browser to include cookies in the request and to accept cookies from the response. Our back-end will have to allow that via CORS settings (`allowCredentials`).

After successful login, we store the token. Using `localStorage` is shown here for illustration, but recall the security considerations:

- If we stored it in an `HttpOnly` cookie via server, we wouldn't call `localStorage.setItem` – the cookie is automatically stored by the browser, and we'd rely on it being sent in calls.
- If using `localStorage`, ensure the app is protected against XSS so that an attacker cannot run code to steal it. We'll talk about XSS prevention in a moment.

**Auth Context / State:** The app should know the user is logged in after this. Typically, you might store the user info in a React Context or global state (like Redux). For example, decode the JWT (it’s base64 JSON) to get user details (name, roles) and store those in a context state. A library like `jwt-decode` can parse the token. Or the back-end might provide user info in the login response as well. Storing the decoded info (not the raw token) in a React state is fine. But for security, avoid storing sensitive data like plaintext password (we never do that) or token in state if not needed – just keep token in memory or cookie and use it for API calls.

**Route Protection:** If using React Router for navigation, implement protected routes. For example:

```jsx
// Pseudocode for a PrivateRoute component:
<Route
  path="/dashboard"
  element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
/>
```

The `isAuthenticated` can be derived from the presence of a valid token (and maybe checking token expiry). You might write a function `isTokenValid()` to check if the JWT is not expired (by examining its `exp` claim).

For role-based authorization on front-end (e.g., only Admin sees a certain link), you can also use the token’s claims. For example, if the JWT contains `roles: ["ADMIN","USER"]`, store that in context and conditionally render admin features:

```jsx
{
  userRoles.includes("ADMIN") && <Link to="/admin">Admin Panel</Link>;
}
```

This is a **convenience** for the UI – actual enforcement of admin-only actions must happen on the back-end as well (never trust the front-end alone for security).

**Using OAuth2 Authorization Code with PKCE (alternative):** If we used an external IdP or Spring Authorization Server, the flow would differ:

- We’d redirect the user to the IdP’s auth URL (with `response_type=code`, `code_challenge` etc.). Possibly use an OAuth2 client library for React or just do `window.location.href = authUrl`.
- After user logs in at IdP, it redirects back to our app (say to `/callback`) with a `code`. We then have to exchange that code for tokens by making a back-end call. This can be done by our React app calling a proxy on our back-end or directly if CORS allowed. The back-end could handle the token exchange securely (because it can use client secret if needed) and then give the React app the JWT (or set cookie).
- This flow is more complex but more secure and avoids handling user passwords directly in our app. Many libraries like **OIDC Client** or frameworks like **NextAuth** for Next.js simplify it. In our manual approach above, we basically implemented a resource-owner password credentials flow (username/password directly) which is not OAuth2 recommended practice for third-party, but fine for first-party apps under certain conditions.

Given our approach, let's proceed with handling the token on the client now.

**Secure API Integration with JWT:**
Once logged in, the React app needs to include the JWT with each API call to protected endpoints. Usually, JWTs are sent in the HTTP Authorization header:

```
Authorization: Bearer <token>
```

We can configure axios to attach the token on all requests after login. For example:

```jsx
// Set token as default header for axios after login:
axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
```

Alternatively, for fetch:

```js
fetch("/api/data", {
  headers: {
    Authorization: "Bearer " + token,
  },
});
```

If using cookies (HttpOnly cookie scenario), the browser will include the cookie automatically in requests to the back-end domain, so you wouldn't manually add headers. But on the server, we'd need to read the token from cookie.

Make sure to **renew or logout** when token expires. JWTs typically have an expiration (`exp`). If we issued short tokens (say 15 minutes) and a refresh token, we'd need logic to use the refresh token to get a new JWT when the old one is near expiry or gets a 401. This logic can be in an axios interceptor: on receiving 401, attempt refresh (if refresh token cookie exists), else redirect to login. Due to time/space, we note this but won't detail fully. Just plan for token lifecycle, as compliance might require automatic logout after a period of inactivity.

**Preventing XSS and secure token handling:** As mentioned, storing the JWT in `localStorage` is common but can be dangerous if XSS vulnerabilities exist. We will mitigate this by:

- Avoiding any usage of `dangerouslySetInnerHTML` in React or inserting HTML from user input. React escapes content by default, which is good. We'll be careful to keep that default behavior.
- Using libraries or functions to sanitize any HTML if we ever need to display rich text from user (like if showing a comment that allows some HTML, which we likely won't).
- Not exposing the token unnecessarily. E.g., do not put the token in the DOM or in URLs. Keep it in memory or cookie. If we used cookie HttpOnly, XSS can't directly steal it. But if using localStorage, an XSS hole could call `localStorage.getItem('authToken')`. Thus, **most of all, we focus on preventing XSS**.

To illustrate XSS prevention: Suppose we display user’s name on a page after login. The name comes from the database. We ensure on backend that it’s a normal string without HTML. React will render it as text. If an attacker managed to put `<script>alert(1)</script>` as their name, React by default would not execute it; it would render it literally as text on the page (since React escapes it). If we accidentally used `dangerouslySetInnerHTML` to insert that name into the DOM as HTML, the script would execute. So we avoid using that method or any equivalent unless absolutely necessary (and if so, sanitize the input with a library like DOMPurify beforehand).

**Use of Security Headers in Front-End:** Some security protections are implemented via HTTP headers sent by the server that affect the front-end:

- **Content Security Policy (CSP):** This header can whitelist domains for scripts, styles, etc. We can configure our Spring Boot server to send a CSP header that disallows inline scripts and only allows scripts from our domain. This would greatly mitigate XSS (even if an attacker injects a `<script>` tag, the browser would block it by CSP). As per a best practice, _“configure your app to return a Content-Security-Policy header”_ ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Content%20Security%20Policy%20,tag%20in%20your%20HTML%20page)). We will implement a CSP in the back-end configuration later. On the React side, just ensure we do not violate it (like, if CSP disallows inline styles, we won't use any inline style attributes that are not allowed or we'll adjust CSP).
- **X-Content-Type-Options, X-Frame-Options, etc.:** These will also come from the server. The front-end just needs to be compatible (e.g., X-Frame-Options DENY means we can’t be embedded in an iframe, which is fine).
- **Service Workers Caution:** If using CRA's default service worker for a PWA, be mindful that caches might store API responses. Ensure sensitive data is not cached, or configure the service worker to avoid that. If uncertain, one might disable the service worker (i.e., not register it) to avoid complexity, unless PWA functionality is needed.

**OAuth2 Libraries:** Note that to implement OAuth2 login flows, there are libraries like `@azure/msal-react` (for Azure AD), `oidc-client` (generic), or Auth0's SDK if using Auth0. These can handle the redirect and token parsing for you, storing tokens in web worker memory or cookies. Using such libraries can reduce the chance of mistakes. The decision often comes down to whether you control the auth or use an external provider.

For our scenario, after implementing login and receiving the JWT, we will next integrate calls to secure APIs and handle user input on the front-end.

## Secure API Integration and Data Validation

The React front-end will communicate with the Spring Boot back-end via RESTful APIs (over HTTPS). Ensuring this integration is secure involves:

- Using HTTPS for all API calls (no plaintext HTTP).
- Including authentication tokens as discussed.
- Validating and sanitizing any data going in or out.
- Handling API responses and errors properly (avoiding leakage of sensitive info through the UI).

**API Client Setup:** It's good to centralize API calls in one place. For example, create an `api.js` that creates an axios instance:

```js
import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 5000,
});

// Attach the JWT token to each request if present
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export default API;
```

This way, throughout our React app we use `API.get('/items')` etc., and it automatically includes the bearer token. If using the cookie approach, we might not need to attach Authorization header manually (but we might still to be consistent; either is fine as long as back-end knows where to find the token).

**Input Validation on the Client:** Any forms or inputs in the UI should validate data before sending to the server. This improves user experience and reduces unnecessary load on the server, though it is not a substitute for server-side validation (which we will also implement for true security). For example:

- If we have a registration form, ensure the email looks like a valid email, password meets complexity rules, etc., in the front-end using regex or validation libraries.
- For numeric inputs or selections, ensure they’re within expected ranges.
- Use HTML5 form validation attributes (`required`, `minlength`, `pattern`, etc.) and additional JavaScript checks as needed.
- If the user tries to enter an extremely large value or a script in a text field, the front-end should catch it and prevent submission.

However, always remember an attacker can bypass front-end validation (e.g., by calling the API directly). The back-end must treat all input as untrusted. So why validate on front-end? Primarily for user convenience and to potentially catch mistakes early. It also can stop some obviously malicious input from ever reaching the server (like a very long string that could be a DOS attempt). But it's not foolproof if someone deliberately bypasses it.

**Preventing XSS in the Front-End UI:** XSS can also occur purely in the front-end if we inadvertently render data that came from an API or from user input unsafely. Example scenario: The back-end returns a JSON containing a username that happens to have malicious content (imagine a user named `"><script>alert('xss')</script>`). If our React app takes that and sets it directly as innerHTML somewhere, that script would run. To avoid this:

- Use React’s default rendering (curly brace syntax `{username}` in JSX) which escapes content.
- If for some reason you need to render HTML from server (like the server provides some HTML snippet), use `dangerouslySetInnerHTML` **only** with sanitized content. A library like DOMPurify can clean a snippet by removing scripts or dangerous tags. But as much as possible, design APIs to return structured data, not raw HTML. For example, if the server wants to format something, consider sending structured data or a markup like Markdown that can be safely converted using a library that escapes where needed.

**Handling API Errors:** When an API call fails (like a validation error from back-end, or a 401 Unauthorized, or 500 error), handle it gracefully:

- If it's a validation error (400 Bad Request), you might display messages near form fields. Do not show raw technical details to the user. For instance, the back-end might return `"error": "Invalid email format"`. Show that message but nothing more. Ensure any message displayed does not accidentally include malicious content (the back-end should control it, but to be safe, treat it as data and not HTML).
- If it's a 401/403 (Unauthorized/Forbidden), that likely means the user's session expired or they tried an action they don't have rights for. In case of 401, prompt re-login (maybe automatically redirect to login page and show "Session expired, please login again"). This ties into token refresh logic if implemented.
- If it's 500, log it (maybe send to some monitoring) but show a generic user-friendly error (like "An unexpected error occurred. Please try again later."). Do not expose stack traces or default error pages to the user – those can leak info. (Our back-end will be configured to not send stack traces in API responses for this reason.)

**Avoiding Sensitive Data Exposure:** The front-end should avoid exposing sensitive data in the browser beyond what is necessary. For example:

- If your back-end returns a user's profile including something sensitive like an access token or a personal identifier, think whether the front-end really needs to see it. Only fetch and store what you need for the UI.
- Do not keep sensitive data in global JavaScript variables longer than needed. For example, if you load user profile data, use state to display it, but you don't need to attach that data to the window object.
- Use browser storage wisely. We discussed JWT storage. Similarly, don't store other sensitive info in localStorage/sessionStorage or cookies unless absolutely required. If you do (e.g., perhaps you store some user preference that might be sensitive), consider encrypting it.
- When using cookies for session or tokens, always set them Secure (HTTPS only) and HttpOnly where applicable, to reduce theft risk. Also set `SameSite=Lax` or `Strict` for cookies so they are not sent cross-site (to mitigate CSRF; if our app is purely API with JWT, CSRF is less an issue, but if using cookies, `SameSite` is important).

**Example of Data Validation on Client:**
Suppose we have a form to create a new item in our app (e.g., a to-do item with a title and due date).
We might validate:

```jsx
if (title.length < 3) {
  setError("Title must be at least 3 characters.");
  return;
}
if (!title.match(/^[A-Za-z0-9 ]+$/)) {
  setError("Title contains invalid characters.");
  return;
}
```

This ensures no special chars (just an example). We also ensure required fields are not empty. On due date, ensure it's a valid date and not in the past (for example). By doing so, we give immediate feedback.

On the back-end, we will perform similar checks (maybe using Spring Boot's Bean Validation). That redundancy is fine and necessary for security.

**Front-end Role-Based Access Control (RBAC):** We touched on showing/hiding UI based on roles. For completeness:

- After login, decode the JWT (or have an API that returns user info including roles) and store roles in a context.
- Create a component like `<AdminOnly>` that takes children and displays them only if `roles.includes('ADMIN')`. Use this to wrap admin links or admin page components.
- This improves UX (normal users won’t even see links to pages they can’t access). However, it’s not a security control by itself – the back-end _must_ enforce checks. We will cover back-end RBAC in the next chapter.
- It’s also good to have an `Unauthorized` page or message if a user somehow navigates to a route they shouldn’t (perhaps by guessing the URL). The front-end can show a "403 Forbidden" page or redirect them away. This, again, is mainly UX because the server will also likely return 403 for the API calls.

**Preventing CSRF:** If we ended up using cookies for auth (say the JWT is in HttpOnly cookie), then we have to worry about CSRF (Cross-Site Request Forgery) because the browser will send that cookie automatically with requests, even if triggered by a malicious site. Solutions:

- Use **SameSite** cookies (Most modern cookies default to `SameSite=Lax` which prevents sending cookies on cross-site _submissions_ like forms or fetches from other sites, except for GET requests from links. `Lax` is usually enough for an API cookie that is only used via XHR/fetch because those are not simple navigations. If extremely paranoid, `Strict` could be used, but that might interfere with legitimate cross-site usage if any).
- Use anti-CSRF tokens: This involves the server generating a token and the client sending it back in a header. In a SPA scenario, we can store a CSRF token in a cookie (not HttpOnly) or in localStorage and send it as a custom header. Spring Security can use `CookieCsrfTokenRepository` to facilitate this, which places a `XSRF-TOKEN` cookie and expects a matching header. If we were using that, our axios calls would need to read the cookie and send the `X-XSRF-TOKEN` header. For example, _“if you’re using Angular or React, you will need to configure the CookieCsrfTokenRepository so JavaScript can read the cookie”_ ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=to%20add%20the%20Spring%20Security,starter%20as%20a%20dependency)). This is a bit beyond basic setup, but something to know. If we stick to stateless JWT in Authorization header, CSRF is not applicable because the token is not automatically sent by browser – our code attaches it.

Given our approach, we likely won't use server-managed session cookies, so CSRF risk is minimal. JWT in header is safe from CSRF by design.

**Example API Call with Validation:**
Let's say we want to create a new "project" via an API:

```jsx
async function createProject(name) {
  // Simple client validation
  if (!name || name.length < 1) {
    throw new Error("Project name cannot be empty");
  }
  if (name.length > 100) {
    throw new Error("Project name too long");
  }
  // (Server will also enforce maybe length <= 100)
  // API call
  const res = await API.post("/projects", { name });
  return res.data;
}
```

We wrap it so any component can call `createProject(name)` and handle the promise.

On the UI side, we call this in a try/catch and show feedback to user.

**Dependency Safety:** If using any third-party React components (say a rich text editor, or a date picker), verify their credibility and update frequency. Sometimes vulnerabilities can come through those (like an XSS flaw in a rich text editor). For ISO 27001, you'll need to manage third-party components as assets too – keep an inventory and monitor for patches ([Application security according to ISO 27001 | Invicti](https://www.invicti.com/white-papers/application-security-according-to-iso-27001-invicti-ebook/#:~:text=The%20ISO%20standard%20separates%20secure,open%20the%20door%20to%20attackers)) (that’s part of secure coding practices requirement, covering third-party and open source).

To summarize:

- The React front-end must securely handle user auth tokens (preferably via secure cookies or guarded storage).
- Validate and sanitize data on the client side to improve UX and reduce bad input, but always complement with server validation.
- Avoid dangerous practices that could introduce XSS or leak data.
- Use the browser’s security features (CSP, etc. configured from server) to add layers of protection.
- Use roles in front-end only to show/hide UI, but never rely on that for actual security enforcement.
- Always test the front-end for common issues (XSS, broken auth flows, etc.). You can use tools like browser dev tools to simulate attacks or run something like OWASP ZAP in proxy mode while using the app to see if it catches any weaknesses.

By building the front-end with these practices, we ensure that the client side of our app is not the weakest link. It complements the server-side security and gives a smooth, safe experience to users.

## Component-Based Architecture Best Practices

A well-structured React application is easier to maintain, extend, and secure. Component-based architecture is at the heart of React. Here are best practices and patterns to follow for organizing and writing React components, especially in a large application:

- **Reusability and DRY Principle:** Break your UI into small, reusable components. If you find the same chunk of JSX or logic being used in multiple places, abstract it into a separate component. For example, a form input with validation might be a reusable `<TextField>` component rather than writing the same markup in every form. Reusability reduces code duplication (Don't Repeat Yourself) and centralizes fixes – if a bug is found in a component, you fix it once. It also helps with security; for instance, if you have a component that displays user input, and you ensure it always escapes/sanitizes properly, using that everywhere avoids missing an XSS vector in a one-off piece of JSX.

- **Single Responsibility for Components:** Each component should ideally do one thing or render one specific piece of UI. This makes it easier to reason about and test. For example, a `UserProfileCard` component might solely be responsible for presenting a user's profile info, not fetching the data (data fetching could be done in a parent or via hooks). Keeping fetch logic separate from presentation allows you to test presentation with dummy data easily and to reuse that component with different data sources if needed.

- **Container vs Presentational Components:** This is a classic pattern where _container_ components handle data fetching and state management, and _presentational_ components simply render props. In modern React with hooks, the lines are blurred, but you can still segregate concerns. For example, you might have a component `UsersListContainer` that fetches a list of users from API and holds them in state, then renders `UsersList` passing the list as a prop. `UsersList` just takes `users` and maps to display rows. This way, if the data source changes (say, you now use a context or different endpoint), you only change the container. It also makes testing easier (you can test `UsersList` by giving it sample data without worrying about API calls).

- **Custom Hooks for Logic:** With React hooks, a great way to reuse logic is to create **custom hooks**. For example, `useAuth()` could be a hook that encapsulates login state, token handling, and provides functions like `login` and `logout`. Internally it might use `useState` and `useEffect`. Any component that needs auth info (like to know current user or to trigger login) can use this hook. This avoids repeating auth logic in multiple components. Similarly, `useFetch(url)` could be a generic data fetching hook that returns loading, error, and data state for a given URL. Hooks help keep components focused on rendering, while hooks handle the logic.

- **Performance Optimization:** Use React's optimization tools where appropriate:
  - `React.memo` for components that get the same props often and you want to avoid re-rendering (this is a pure component concept).
  - `useCallback` and `useMemo` hooks to avoid re-creating functions or values on every render when not necessary.
  - Lazy load components for routes (using `React.lazy` and `Suspense` for code splitting) so that large chunks (like an admin section) are not loaded until needed. This improves initial load and is good for user experience and somewhat for security (less code exposed upfront).
  - Avoid heavy computations in render; if needed, use web workers or move it to back-end if possible. Heavy computations can also be a performance security risk (if an attacker triggers a heavy operation in your UI, it can freeze the app, a sort of client-side DoS).
- **State Management:** As the app grows, consider a state management strategy:

  - React’s built-in Context API is good for global states like current user or theme. But for more complex interactions or a lot of shared state, a library like Redux or MobX might be useful. (Redux is common, but in modern React, a lot can be done with context + hooks without needing Redux for medium-sized apps.)
  - Whichever you choose, keep state minimal and scoped. For example, don't put every piece of state in a global store; local component state is fine if only that component or a small subtree needs it. This prevents unnecessary re-renders and complexity.
  - Ensure that sensitive state (like auth tokens) are managed carefully. If using Redux, avoid putting the raw JWT in Redux if the Redux devtools extension is enabled widely (in dev, someone could inspect it – but in production extension is not usually there, still caution).

- **Handling Lists and Keys:** When rendering lists of components from arrays, always provide a stable `key` prop. This is a basic React thing (to help it track elements). Use a unique identifier from data (like user ID). This prevents issues with item identity. It's not directly a security issue, but can cause UI bugs if keys are misused (which could conceivably cause wrong data to show if the list is manipulated).

- **Styling:** You can use CSS frameworks or CSS-in-JS. Ensure styles don't inadvertently cause security issues:
  - If using CSS-in-JS or styled-components, it's generally safe. Avoid injecting user data into style strings without sanitization, as theoretically could be exploited (e.g., if someone managed to input `background-image: url("javascript:...")` – though modern browsers mostly don't allow JS in CSS url).
  - If using a library like Material-UI (MUI) or Bootstrap, keep it updated to get security patches and avoid older versions that might have XSS issues in certain components.
- **Error Boundaries:** Implement an error boundary component at a high level to catch any render errors and display a friendly fallback UI (like "Something went wrong"). This prevents the entire app from crashing on an exception. It’s good for reliability. From a compliance perspective, it's part of ensuring high availability and graceful handling of failures (ISO 27001 also cares about availability).

- **Logging and Monitoring on Front-end:** While logging is mainly a back-end concern, front-end can also log (to console or to a monitoring service). For critical user actions or errors, consider sending logs to a service like Sentry. This is optional, but having front-end error monitoring helps detect issues (for example, if an XSS somehow got triggered or a certain browser has a problem). If you do send any data from front-end to a logging service, ensure it doesn't include PII or secrets (an error might accidentally include a user's input which could be sensitive; scrub or avoid that).

- **Accessibility and UX:** Good practices here also help security in indirect ways (accessible applications are easier to test and less likely to hide weird behaviors). Use semantic HTML, proper ARIA labels, etc.

- **Comment and Document Components:** Especially for complex components, include comments or use a tool like Storybook to document how components should be used. This reduces misuse that could cause bugs or security issues (e.g., a developer misusing a component prop might inadvertently bypass a security check that the component assumed they'd do).

Let's illustrate some of these with a short example:
Suppose we have to build a dashboard page that shows a list of projects and allows adding a new project. We might have:

- `<DashboardPage>`: Container component that uses a custom hook `useProjects()` to fetch projects from API and manage the list state. It provides functions like `addProject`.
- `<ProjectsList>`: Presentational component that takes `projects` array and renders it (maybe using a child `<ProjectCard>` for each).
- `<NewProjectForm>`: Component for the form to add a project (with internal state for the input, and calls `onCreate(name)` prop when submitted).

**NewProjectForm.jsx:**

```jsx
function NewProjectForm({ onCreate }) {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    if (name.trim().length < 1) {
      setError("Project name is required");
      return;
    }
    try {
      await onCreate(name.trim());
      setName(""); // reset form
    } catch (err) {
      setError(err.message || "Failed to create project");
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Project Name"
      />
      <button type="submit">Add Project</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}
```

This form ensures a non-empty name and delegates creation logic to a prop (which likely calls the API via context or parent state). This follows SRP: form deals with UI and validation, parent deals with data.

**ProjectsList.jsx:**

```jsx
function ProjectsList({ projects }) {
  return (
    <ul>
      {projects.map((proj) => (
        <ProjectCard key={proj.id} project={proj} />
      ))}
    </ul>
  );
}
```

Simple mapping to child component.

**ProjectCard.jsx:**

```jsx
function ProjectCard({ project }) {
  return (
    <li className="project-card">
      <strong>{project.name}</strong> - Created on{" "}
      {new Date(project.createdAt).toLocaleDateString()}
    </li>
  );
}
```

Note: We directly insert `project.name`. We trust that the back-end sanitized it or it's just a normal string. React will escape it anyway (if name had `<`, it will render as `<`). If we wanted to allow some HTML in name (unlikely for a name), we'd need to sanitize. But we assume names are plain. This is a presentational component with no logic.

**DashboardPage.jsx:**

```jsx
function DashboardPage() {
  const { projects, error, addProject } = useProjects(); // custom hook managing state
  if (error) return <div>Error loading projects: {error}</div>;
  if (!projects) return <div>Loading...</div>;
  return (
    <div>
      <h1>Your Projects</h1>
      <NewProjectForm onCreate={addProject} />
      <ProjectsList projects={projects} />
    </div>
  );
}
```

This container uses a hook (not shown here) that might do:

```jsx
function useProjects() {
  const [projects, setProjects] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    API.get("/projects")
      .then((res) => setProjects(res.data))
      .catch((err) => setError("Could not fetch projects"));
  }, []);
  const addProject = async (name) => {
    const res = await API.post("/projects", { name });
    setProjects((prev) => [...prev, res.data]); // update state
  };
  return { projects, error, addProject };
}
```

We would include error handling in `addProject` as well (and rethrow or set state error for the hook, which NewProjectForm catches).

This separation of concerns means:

- We can test `NewProjectForm` by simulating onCreate success/failure.
- We can test `ProjectsList` with sample data.
- `useProjects` could be unit tested by mocking API calls.
- If we want to add a feature like editing project name, we create a new component or extend ProjectCard with a form maybe, but it won't break the list or form components.

**Security Implications of Structure:**

- Because logic is well-contained, we reduce the chance of mistakes. For example, `addProject` ensures updating state in one place. If we had multiple places calling API for projects, we might forget one to handle an error or sanitize input.
- Reusable components (like an input field component that could include built-in XSS safe rendering or length limiting) ensure consistent security practices across the app.
- A clear structure also helps when performing a security review of the code. An auditor can see where data enters (API calls in hooks) and where it is displayed (cards, list). This traceability is good for verifying that all user-supplied data passes through appropriate checks.

**Coding Style and Linters:** Use a consistent coding style and have ESLint rules for things like:

- No unused variables (could indicate a logic mistake).
- No use of deprecated or dangerous APIs (there are ESLint plugins that warn on using `eval` or `innerHTML` etc.).
- Possibly use TypeScript to catch type issues (like treating a number as string which might break and cause unexpected errors).

In summary, component architecture best practices contribute indirectly to security by producing a more robust and maintainable codebase where it's easier to enforce and verify security measures. They also help meet ISO 27001's expectations around software development processes – code reviews are easier if the code is clean and modular, and secure coding guidelines (like input validation, error handling, etc.) can be consistently applied. A well-structured front-end is less likely to have hidden vulnerabilities and easier to fix if any are found.

---

# 4. Back-End Development (Spring Boot)

The back-end is the core of our application’s business logic and data handling. In our stack, the back-end is a **Spring Boot** application, which will expose a RESTful API and interact with the MySQL database. This chapter focuses on building the back-end in a secure manner. We will discuss secure API design, implementing authentication and role-based authorization using Spring Security with OAuth2/JWT, protecting the database access, and adding logging/auditing features aligned with ISO 27001.

Spring Boot is a powerful framework that comes with defaults and starters that make it easy to get started. However, security configurations and careful coding are needed to ensure the application is not vulnerable. We will use Spring Security to handle authentication and authorization, and adhere to best practices like hashing passwords, validating inputs, and proper exception handling.

## Secure API Design and Implementation

Designing a REST API involves deciding on the endpoints (URLs), request/response formats, and how clients will interact with the server. A secure API design ensures that:

- Endpoints are intuitive but do not reveal sensitive information.
- Data is validated and filtered on input and output.
- Only the necessary data is exposed to the client (principle of least privilege/data minimization).
- The API is consistent and uses proper HTTP methods (GET, POST, PUT, DELETE, etc.) with semantics that clients can rely on.

**Structuring Controllers and Routes:**
In Spring Boot, you'd typically create controller classes annotated with `@RestController` to define endpoints. For example:

```java
@RestController
@RequestMapping("/api/projects")
public class ProjectController {

    @Autowired
    private ProjectService projectService;

    @PostMapping
    public ResponseEntity<ProjectDto> createProject(@Valid @RequestBody CreateProjectRequest request) {
        ProjectDto created = projectService.createProject(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping
    public List<ProjectDto> listProjects(Authentication auth) {
        // auth will hold JWT details if needed to filter by user
        return projectService.listProjects(auth);
    }

    // ... other endpoints (get by id, update, delete) ...
}
```

Important points:

- We prefixed routes with `/api` to clearly delineate API endpoints (versus any other web content if it existed). This isn't mandatory, but a convention that helps, especially if later you host static front-end on the same domain (then `/api/*` can be routed to back-end).
- Using **DTOs (Data Transfer Objects)**: Notice `ProjectDto` and `CreateProjectRequest`. It's good practice not to expose your JPA entities directly as JSON, but use DTOs to control exactly what's serialized. This prevents accidentally leaking fields. For instance, your `User` entity might have a `passwordHash` field – if you return User directly as JSON, you might inadvertently send that hash to the client. With DTOs, you include only needed fields (e.g., user id, name, email, but not passwordHash). This is crucial for compliance (no leaking sensitive data) and follows **principle of least data**.
- Use `@Valid` on request bodies to trigger validation (with JSR 303 annotations on the request classes). For example, `CreateProjectRequest` can have `@NotBlank private String name;` and maybe `@Size(max=100)`. Spring will automatically return a 400 Bad Request if validation fails, with a message. We should customize the error handling to not expose too much info (by default it might include the field name and message; that’s usually fine).

**Input Validation (Server-Side):** As mentioned, using Bean Validation (`javax.validation`) is a great way to enforce rules. This covers basic checks (not null, string length, number ranges, pattern matching). For more complex logic, you can do manual validation in the service or controller. For example, if a combination of fields must be valid or a business rule like "a user cannot create more than 5 projects", implement that in service and throw a custom exception if violated.

**Output Filtering:** Ensure responses do not include sensitive information. When using Spring Boot with Jackson (for JSON), you can use annotations like `@JsonIgnore` on fields in your DTOs that should not be serialized. Or simply do not include that field in the DTO at all. Also be careful with error messages – e.g., if an exception occurs, by default Spring might return an error page or stack trace (depending on if it's a web app). For REST APIs, Spring Boot converts exceptions to JSON error responses usually (in `BasicErrorController`), but in production, make sure `server.error.include-stacktrace=never` (in application.properties) to avoid exposing stack traces. We likely will customize global exception handling with `@ControllerAdvice` to format errors in a consistent, non-leaky way.

**HTTP Methods and Idempotency:**

- Use GET for read operations (no side effects).
- Use POST for create operations (and perhaps for any action that isn't idempotent).
- Use PUT or PATCH for updates (PUT for full update, PATCH for partial).
- Use DELETE for deletions.
  And ensure these actually perform as expected (e.g., a GET should not modify data). This is more of a design principle, but it also ties into security: for example, enabling GET to delete something (just because it's easier) would be bad because web crawlers or prefetchers might accidentally trigger it. Moreover, if we rely on browser built-in CSRF protections, those often protect unsafe methods by default.

**Idempotency and Safe Methods:** For things like password reset endpoints, use POST and possibly a one-time token to ensure the action isn't repeated or forged.

**Resource Naming:** Use meaningful resource names in URLs (e.g., `/api/projects/{projectId}` for a single project). Avoid exposing internal identifiers if they are sensitive. Usually, numeric IDs or UUIDs are fine. But if your internal system uses something like an incrementing ID that could be guessed, consider using UUIDs or some random ID for externally facing identifiers to avoid enumeration attacks. If using numeric IDs, ensure authorization checks (so user A cannot request `/projects/3` if that belongs to user B – the back-end must check ownership).

**Rate Limiting and Throttling:** While not built-in to Spring Boot by default, consider how to prevent abuse. For example, someone could script hitting your login API repeatedly (brute force). Solutions include using an API gateway or filters to limit requests per IP, or using CAPTCHA (though for APIs it's tricky), or implementing account lockout after certain failed attempts. At minimum, log suspicious patterns (we'll discuss monitoring later). For ISO 27001, having controls against brute force (which is an attack on confidentiality) is important.

**Secure Coding in Implementation:**

- Use **prepared statements** for any raw SQL (if not using ORMs). Spring Data JPA or JDBC templates by default use prepared statements (with `?` placeholders) which prevents SQL injection by separating query from data ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,This%20involves%20adding)).
- Avoid constructing queries with string concatenation using user input. If using JPA and need dynamic queries, use parameter binding (or Spring Data repository query methods which handle it).
- Handle file uploads carefully (if any). We might not have file upload in this app, but if, ensure to check file type, size, and store it securely (preferably in S3 rather than on the server disk to avoid running out of space or malicious path).
- Use safe APIs for any system-level operations. For example, if the app ever needed to call an OS command (rare in our scenario), use `ProcessBuilder` with arguments separated, not building a shell command string (to avoid command injection).
- **Output Encoding:** If our API was returning HTML or if we had a web UI rendered by server (Thymeleaf, etc.), we'd need to encode outputs to prevent XSS. In a pure JSON API, the main thing is to make sure you're not inserting untrusted data into scripts or HTML on the server side. We are not doing server-side HTML, so not much risk of server XSS. But be mindful if any API takes HTML (maybe for rich text fields) – store it safely (sanitize or strip disallowed tags on server) so even if one client submits something malicious, it won't harm another client that fetches it.

**Error Handling and HTTP Status Codes:**

- Return appropriate status codes: 400 for bad requests (validation errors), 401 for unauthorized (not logged in), 403 for forbidden (logged in but not allowed), 404 for not found (e.g., requesting a resource that doesn't exist or not accessible to them but you don't want to reveal it exists), 500 for server errors, etc. This helps clients react accordingly and is a part of robust API design.
- In error responses, don't expose internal implementation. For example, an exception message like "NullPointerException at com.example.service.UserService line 45" should never reach the client. Instead, translate it to a user-friendly or at least neutral message (like "Internal server error").
- Logging of errors (we'll discuss in logging section) should record details for debugging, but the API should give minimal info to the user for security. For instance, for a login failure, a common debate: do we say "Invalid username or password" vs "Invalid password"? The former doesn't let attacker know if the username was valid. It's generally better to not reveal whether the username was correct (prevent user enumeration). Similarly, a 404 for a resource not found vs 403 can be used to not reveal existence. A practice: if user A requests resource 5 which belongs to user B, you might just return 404 (so as not to reveal that a valid resource exists at that ID) or a generic 403/404 message without details.

**Example of a Secure Endpoint Implementation:**
Let's consider registration:

```java
@PostMapping("/api/users")
public ResponseEntity<?> registerUser(@Valid @RequestBody RegisterRequest request) {
    userService.register(request);
    return ResponseEntity.ok().build();
}
```

The `register` method in service would:

- Validate if email is already taken; if so, throw a custom exception (maybe mapped to 400 or 409 Conflict).
- Hash the password before storing (using BCrypt).
- Possibly send a verification email (if we do email verification).
- Not log the raw password or send it anywhere.
- Return perhaps nothing or a success message. We wouldn't return the created user with password obviously.

Now, how do we ensure secure authentication and authorization in Spring Boot? That leads us into Spring Security configuration.

## Role-Based Access Control and Security Mechanisms

Spring Boot integrates with Spring Security to provide authentication and authorization. We will use **JWT (JSON Web Token)** as our authentication mechanism, meaning the back-end will validate a JWT on each request (sent by the client in the Authorization header as "Bearer token"). We also need to define user roles (like `ROLE_USER`, `ROLE_ADMIN`) and restrict endpoints based on those roles or authorities.

**Spring Security Setup:**
First, include the dependency:

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

The second one brings in JWT validation support (as a resource server).

We then configure security. In modern Spring Boot (2.7+ and 3.x), the recommended way is to use a `SecurityFilterChain` bean. For example:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthenticationConverter jwtAuthConverter; // converter to extract roles from JWT

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.csrf().disable() // disable CSRF because we use stateless JWT (no session cookies)
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/auth/**").permitAll()  // allow public auth endpoints (login, register)
                .requestMatchers(HttpMethod.GET, "/api/projects/**").authenticated() // must be logged in
                .requestMatchers(HttpMethod.POST, "/api/projects").hasRole("USER") // logged in users can create
                .requestMatchers("/api/admin/**").hasRole("ADMIN") // admin endpoints
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter))
            );
        return http.build();
    }
}
```

In this config:

- We disabled CSRF. Since our API is stateless (no session stored on server) and expects a token, CSRF protection is not needed. If we were using sessions/cookies, we would enable CSRF tokens to protect form submissions. The code comment notes why it's safe to disable here (stateless JWT usage).
- We use `.authorizeHttpRequests` to define access rules:
  - Auth endpoints (like login, register under `/api/auth/`) are open to all (`permitAll()`).
  - All GET requests to `/api/projects/**` require authentication (`authenticated()` means any logged-in user). We might allow read to public, but in this design, let's say you must be logged in to see projects (like your projects).
  - POST to `/api/projects` requires role USER (which normal authenticated users have). Actually `.hasRole("USER")` in Spring means it expects an authority "ROLE_USER" on the Authentication.
  - Admin endpoints under `/api/admin/` require admin role.
  - `.anyRequest().authenticated()` means everything else not matched explicitly must be authenticated (this is a safe default to ensure nothing slips through).
- We configure the app as an OAuth2 Resource Server with JWT. This means Spring Security will automatically:
  - Inspect the Authorization header for a Bearer token.
  - Validate the JWT (verify signature, expiration, etc.) using settings we provide (e.g., public key or shared secret).
  - If valid, create an `Authentication` object (of type `JwtAuthenticationToken`) with authorities extracted.
- We need to tell it how to extract roles from JWT. Often JWT might have a claim like "roles": ["ROLE_USER","ROLE_ADMIN"]. By default, Spring Security might not know to use that. The `JwtAuthenticationConverter` can convert JWT claims to GrantedAuthority list. For example, we could configure it:
  ```java
  @Bean
  public JwtAuthenticationConverter jwtAuthenticationConverter() {
      JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
      converter.setJwtGrantedAuthoritiesConverter(jwt -> {
          Collection<SimpleGrantedAuthority> authorities = new ArrayList<>();
          List<String> roles = jwt.getClaimAsStringList("roles");
          if (roles != null) {
              roles.forEach(role -> authorities.add(new SimpleGrantedAuthority("ROLE_" + role)));
          }
          return authorities;
      });
      return converter;
  }
  ```
  If our JWT includes "roles": ["USER"] for a normal user, this will create a GrantedAuthority "ROLE_USER". Spring's `.hasRole("USER")` matches that.

**JWT Generation** (Authentication process):
We have to create JWTs when users log in or register. We can use a library like **java-jwt** (JWT by Auth0) or Spring Security's OAuth2 Jose support. But simplest:

- Add dependency for JWT, e.g. `io.jsonwebtoken:jjwt` or use Auth0's `java-jwt`.
- When user passes credentials to `/api/auth/login`, our controller calls auth service:
  - Authenticate credentials (find user by username/email, use `BCryptPasswordEncoder.matches(raw, hashed)` to verify password).
  - If valid, generate JWT with claims: subject = username or user ID, issue time, expiration (maybe 15 minutes or 1 hour), and a claim for roles.
  - Sign it with a secret or private key. For example, using a symmetric secret in HS256 (ensure it's strong and kept out of code, maybe in application.properties or environment).
  - Return the JWT to the client (in JSON or as cookie).

We should store the password as a BCrypt hash. Spring Security provides `PasswordEncoder` interface; use `new BCryptPasswordEncoder()` to hash and verify.
Example:

```java
@Service
public class AuthService {
    @Autowired
    private UserRepository userRepo;
    @Autowired
    private PasswordEncoder passwordEncoder;
    @Value("${jwt.secret}")
    private String jwtSecret;

    public String login(String email, String password) {
        User user = userRepo.findByEmail(email)
            .orElseThrow(() -> new BadCredentialsException("Invalid email or password"));
        if (!passwordEncoder.matches(password, user.getPasswordHash())) {
            throw new BadCredentialsException("Invalid email or password");
        }
        // build JWT
        Algorithm alg = Algorithm.HMAC256(jwtSecret);
        String token = JWT.create()
                .withSubject(user.getId().toString())
                .withClaim("roles", user.getRoles()) // assume roles is a list of strings like ["USER","ADMIN"]
                .withIssuedAt(new Date())
                .withExpiresAt(Date.from(Instant.now().plus(1, ChronoUnit.HOURS)))
                .sign(alg);
        return token;
    }
}
```

(This uses Auth0 JWT library for example; `user.getRoles()` might need converting roles to short names without "ROLE\_" prefix depending on how we design it).
We would catch `BadCredentialsException` in a global exception handler to return 401.

Now, with this in place, Spring Security will automatically secure all endpoints except those we `permitAll()`. If a request comes without a valid JWT to a protected endpoint, it will respond with 401. If it comes with a valid JWT but lacking required role, it will respond 403.

**Protecting Sensitive Endpoints:**
We should double-check that any sensitive operations are properly restricted. E.g.:

- Only admin can delete users or view all users.
- Normal users can perform allowed actions on their own data but not others'.
- For resource ownership: Even if an endpoint is authenticated, within the handler, filter data by the current user. For example, `listProjects(Authentication auth)` should only return projects belonging to `auth.getName()` (if we set JWT subject to userId or email). We can get the current user's info via `Authentication auth` or a static helper `SecurityContextHolder.getContext().getAuthentication()`. The JWT's subject or a custom claim will give the user ID. Alternatively, after login we can store userID in a claim. Then:
  ```java
  String userId = auth.getName(); // by default might be the JWT subject
  return projectRepo.findByUserId(userId);
  ```
  Ensuring multi-tenant separation. If a user tries to access someone else’s resource by ID, the query returns nothing or we explicitly check and throw 404.

**Method-Level Security:** In addition to URL config, Spring allows method-level security with annotations:

- `@PreAuthorize("hasRole('ADMIN')")` above a method to restrict it. We have to enable with `@EnableMethodSecurity` in config. This is useful for service layer enforcement on top of controller (defense in depth).
- For instance, a service method `deleteProject(id)` could have `@PreAuthorize("@projectSecurity.isOwner(#id, authentication) or hasRole('ADMIN')")` which uses a custom Spring Expression to check if the current user is owner of that project or an admin. This ensures even if someone reached a method in an unintended way, the security is double-checked.

We might not need that if our controller endpoints already guard and we carefully fetch only allowed data. But it's a nice additional safeguard.

**Security Headers and HTTPS Enforcement:**
We should ensure the app is only accessible via HTTPS in production. If behind an AWS ALB or API Gateway terminating SSL, the Spring Boot app might see plain HTTP. We can enforce in Spring Security by requiring secure channel:

```java
http.requiresChannel(channel -> channel.anyRequest().requiresSecure());
```

This will redirect to HTTPS if a request comes via HTTP. If behind a proxy, need `X-Forwarded-Proto` handled (Spring Boot can if configured with `ForwardedHeaderFilter` or `server.use-forward-headers=true` when behind a known proxy).

Also, Spring Security by default adds some security headers:

- `X-Frame-Options: DENY` (prevents clickjacking by disallowing in iframes).
- `X-Content-Type-Options: nosniff`.
- `Cache-Control` on some error responses, etc.
  We might want to add Content Security Policy and HSTS:

```java
http.headers(headers ->
    headers.contentSecurityPolicy("script-src 'self'; object-src 'none';")
           .httpStrictTransportSecurity(hsts -> hsts.includeSubDomains(true).maxAgeInSeconds(31536000))
);
```

This would send a CSP header (disallowing any scripts not from our domain and disallowing plugins/objects) which helps mitigate XSS ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Content%20Security%20Policy%20,tag%20in%20your%20HTML%20page)). And HSTS to force clients to stick to HTTPS after first visit.

**Storing Secrets:** In our configuration above, we used a `jwt.secret` from properties. We must ensure this secret is strong and kept secret:

- In application.properties, do not commit real secret; use something like `${JWT_SECRET}` and supply via environment variable or Secrets Manager.
- If using asymmetric keys (RSA), store keystore securely.
- Limit who can access config. This is part of ISO compliance (control access to keys – maybe only ops team or use AWS Parameter Store).
- Regularly rotate secrets if possible (JWT secret rotation is non-trivial if stateless; might use a JWKS with multiple keys and rotate by adding new, phasing out old).

**Password Handling:** Use `PasswordEncoder` as mentioned. _Never store plaintext passwords._ Spring Security’s default is also to require a password encoder. If you try to authenticate without encoding, it might fail by default for safety ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Storing%20passwords%20in%20plain%20text,password%20encoding)). We use BCrypt which is recommended (strong hashing, with salt and multiple rounds) ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Storing%20passwords%20in%20plain%20text,password%20encoding)) ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Spring%20Security%20provides%20several%20implementations%2C,Pbkdf2PasswordEncoder)). Also consider setting a password policy:

- Enforce minimum length, complexity on registration (both front-end and back-end).
- Possibly check against a list of known leaked passwords (OWASP has lists, Troy Hunt's PwnedPasswords API etc., but that's more advanced).
- On password change, maybe invalidate all sessions/tokens (so old JWTs are no longer accepted – but stateless JWT can't be easily revoked unless we keep a blacklist or change a signing key, so trade-off; short expiration helps here).

**Session Management:** We're not using HTTP sessions since JWT is stateless. That’s good for scalability and avoids session fixation issues. Ensure `spring.session.store-type` is not something like `jdbc` unless needed (to avoid leftover sessions). Actually with stateless, Spring Security doesn't create sessions (especially if `.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)` is set in config).

**Auditing and Logging (within code):** Certain sensitive actions, like admin performing an action or multiple failed logins, could be logged or audited:

- We could use Spring Boot Actuator auditing, or simply log via SLF4J logger at INFO level "User X deleted project Y".
- For compliance, having an audit trail is useful. We'll cover more in logging section, but you might design the service methods to record these events (to DB or log).
- Use UUIDs for request tracing (Spring can propagate trace IDs if using Sleuth/Observability so each log can be correlated).

**Testing Security:** Write tests to ensure:

- Unauthorized access is blocked. E.g., use MockMvc to call an endpoint without auth header and expect 401.
- With a valid JWT of a user, they can access their resource.
- With a JWT of a normal user, try to access an admin endpoint and expect 403.
- Try a malicious input (like SQL injection attempt `' OR '1'='1` in a search parameter) and ensure it doesn't break the query (if using JPA repository, it's safe by default; if using plain JDBC, test that the parameter is handled).
- Ensure password hashing works: registration then login should succeed with the provided password.

All these add confidence that security is correct.

By configuring Spring Boot with Spring Security in this robust way, we fulfill a number of ISO 27001 controls:

- **Access control (A.9)**: We enforce that only authorized individuals (with correct role) can access certain functions ([Securing Your React Apps: Best Practices](https://www.walturn.com/insights/securing-your-react-apps-best-practices-for-authentication-and-authorization#:~:text=%2A%20Implement%20Role,side%20authorization%20checks)).
- **User authentication (A.9.4)**: We implement secure logon procedures, protect passwords by hashing, and manage sessions (or tokens in our case) securely.
- **Cryptography (A.10)**: We use secure algorithms (BCrypt, HS256 or RS256 for JWT) ([10 Spring Boot security best practices | Snyk](https://snyk.io/blog/spring-boot-security-best-practices/#:~:text=Storing%20passwords%20in%20plain%20text,password%20encoding)).
- **Secure system engineering (A.14)**: We built security into the design of the API endpoints and code (as this whole section demonstrates).

Next, we will ensure secure connection to the database and see how to integrate security in that layer.

## Secure Database Connectivity with MySQL

The back-end communicates with the MySQL database to store and retrieve data. We need to ensure this communication and the data access are secure:

- Use secure credentials and connections.
- Apply least privilege to the database user.
- Protect against SQL injection and other injection attacks.
- Handle errors from the DB gracefully.

**Database Credentials Management:**
In Spring Boot, DB creds are typically in `application.properties`:

```properties
spring.datasource.url=jdbc:mysql://db-host:3306/appdb?useSSL=true&requireSSL=true
spring.datasource.username=appuser
spring.datasource.password=somepassword
```

A few things here:

- **Never commit real passwords** in source control. Use placeholders and supply via environment variables or an external config. For instance, use `spring.datasource.password=${DB_PASSWORD}` and set `DB_PASSWORD` in the environment on the server or use Spring Cloud Config/Secrets Manager.
- The JDBC URL includes `useSSL=true` and `requireSSL=true` to enforce SSL/TLS for MySQL connection ([java - Connecting a springboot application with mysql server over ssl - Stack Overflow](https://stackoverflow.com/questions/63827838/connecting-a-springboot-application-with-mysql-server-over-ssl#:~:text=url%3A%20,cert.p12%26%20clientCertificateKeyStoreType%3DPKCS12%26%20clientCertificateKeyStorePassword%3D%7BKEY_STORE_PASSWORD%7D%20verifyServerCertificate%3Dtrue)). This ensures the data between the app and DB is encrypted, preventing eavesdropping (especially important if DB is separate from app server or in cloud where network could be shared). **Note:** With AWS RDS, one can enforce SSL and use AWS's CA certificate. The connection string might also include `verifyServerCertificate=true` and the truststore info. We saw a detailed example with keystore for client cert ([java - Connecting a springboot application with mysql server over ssl - Stack Overflow](https://stackoverflow.com/questions/63827838/connecting-a-springboot-application-with-mysql-server-over-ssl#:~:text=spring%3A%20datasource%3A%20url%3A%20,cert.p12%26%20clientCertificateKeyStoreType%3DPKCS12%26%20clientCertificateKeyStorePassword%3D%7BKEY_STORE_PASSWORD)) which is for client auth. In simpler scenarios, using MySQL’s provided cert for Amazon RDS (or CA-signed certs) and trust server certificate (or explicitly trust the CA) is recommended. The key is to avoid `useSSL=false`. Modern MySQL drivers require SSL by default unless disabled, which is good ([MySQL – Establishing SSL connection without server's identity ...](https://helpezee.wordpress.com/2019/07/02/mysql-establishing-ssl-connection-without-servers-identity-verification-is-not-recommended/#:~:text=MySQL%20%E2%80%93%20Establishing%20SSL%20connection,if%20explicit%20option%20isn%27t%20set)).
- Use a **dedicated DB user** for the application with minimal privileges. For example, if our app only needs to access `appdb`, create `appuser` with privileges only on that schema (and only SELECT/INSERT/UPDATE/DELETE on tables it needs, maybe EXECUTE if using stored procs, etc., but not global privileges). Do not use the MySQL `root` user or any admin user in the app. This way, if the app is compromised, the DB impact is limited ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=Follow%20the%20principle%20of%20least,if%20their%20credentials%20are%20compromised)).
- Ensure the DB user password is strong and rotated periodically. Also, in an ISO context, store it securely (maybe in AWS Secrets Manager and retrieve at startup, rather than plain in config).

**Connection Pooling:** Spring Boot by default uses HikariCP. It's fast and secure by default. Just ensure to size it right and perhaps turn on connection validation. But security-wise, not much to do except not expose the pool config info.

**SQL Injection Protection:**
As noted, using JPA (Hibernate) or Spring's JDBC templates with `?` placeholders ensures parameters are bound, not concatenated, preventing injection. If we do need to build dynamic queries (like optional filters), use JPA Criteria API or Spring Data JPA's method naming to avoid manual string building. If using native SQL queries (sometimes needed for complex queries), use parameters `:param` and set via `Query.setParameter`.
We already cited the importance of prepared statements ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,This%20involves%20adding)). Also use **Stored procedures** carefully: if using them, still pass inputs as parameters, not string concatenation within the proc. And restrict who can create/alter procs.

**Object-Relational Mapping (ORM) considerations:**

- If using JPA/Hibernate, be careful of the N+1 query issue (performance), but security wise ORMs are generally safe from injection if used properly.
- Use appropriate fetch strategies to avoid accidentally pulling too much data (could be performance issue or even security if lazy loading triggers undesired loads of related entities).
- If using Spring Data, methods like `findByEmail(String email)` are safe – Spring Data creates a prepared query behind scenes.

**Error handling in DB ops:**

- If a database error occurs (like unique constraint violation), catch it and translate to a meaningful response. For example, if register user with existing email triggers a SQLIntegrityConstraintViolationException, catch and throw a custom `EmailAlreadyUsedException` which returns a 400 with message "Email already in use." Do not expose the raw SQL error message (which might contain SQL or table info).
- Log technical details on server (for debugging) but return generic messages to clients.
- Also be mindful of timing and error differences – e.g., when checking login, to prevent user enumeration, ensure the response time is similar whether or not the user exists. We did "Invalid email or password" both cases. This is to not give a clue by timing or different message.

**Preventing Data Leakage:**

- Ensure that sensitive fields (like password hashes) are never selected in normal queries unless needed. If using JPA, annotate with `@JsonIgnore` on sensitive fields of entities if they could ever get serialized (like if using Spring Data REST, which we are not here, but that can auto expose repos in HAL+JSON).
- Principle of least privilege applies at query level too: don't fetch more columns than necessary in custom queries.
- If using multi-tenant (each user has own data), always include a tenant/user filter in queries (like `WHERE user_id = :currentUserId`). It's easy to rely on front-end to send correct ID, but back-end must enforce it. If you have repository methods, consider using Spring Security's @PostAuthorize or spec-based filtering.
- Use database encryption if needed for highly sensitive data (MySQL supports TDE in enterprise or you can encrypt at application level certain fields). For instance, if storing PII or secrets, maybe encrypt them in DB so even DB dumps are safe. That adds complexity (key management needed). For our case, not implementing that, but mention as compliance measure for e.g. credit card data (though that would also fall under PCI DSS separate from ISO).

**Database Auditing:**

- Possibly use MySQL logging/auditing to record certain statements, but that can be heavy. Alternatively, implement audit tables in app. For example, a table `project_audit` capturing project changes, with fields (project_id, action, timestamp, user_id). If needed by compliance (some standards require audit trails for critical data changes). ISO 27001 likes the idea of logging admin or high-risk actions, which can be done at app level.
- Use triggers for auditing carefully (they run with DB permissions, ensure they can't be misused to escalate privileges).

**Backup and Availability:**
While more of ops topic, mention:

- Ensure regular backups of the database (and test them) ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,using%20a%20trusted%20storage%20provider)) ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,in%20recovery%20scenarios%20when%20necessary)).
- For MySQL, using AWS RDS, enable automated backups and possibly multi-AZ for failover.
- ISO 27001 requires data backup (A.12.3) and also testing restores ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,in%20recovery%20scenarios%20when%20necessary)).
- Also, restrict backup file access. If backups are stored in S3, secure the bucket (no public access).
- If doing manual dumps, consider encrypting them before storage ([Best Practices for Handling Sensitive Data in MySQL Databases](https://aditya-sunjava.medium.com/best-practices-for-handling-sensitive-data-in-mysql-databases-4483fa0c339e#:~:text=sunjava,a%20secure%20location%2C%20ideally%20offsite)).

**Least Privilege on DB Server:**

- The DB itself should run with least OS privileges, and remote access to it should be restricted (firewall rules: only allow the app server's security group or IP to connect to MySQL port).
- If using AWS RDS, put it in a private subnet (no direct Internet access).
- For local dev, it's okay, but for production, ensure security groups (basically firewall) restrict MySQL port 3306.

**MySQL Hardening:**

- Remove default accounts or ensure they have strong passwords (the "root" should be locked down).
- Disable unused features or the "test" database.
- Ensure MySQL is up-to-date with latest patches (managed by AWS if using RDS or manually update if self-managed).
- Configure MySQL to use strong TLS (like enforce TLS1.2+, and use certificate validation).

**Example of a secure repository usage (Spring Data JPA):**

```java
@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {
    List<Project> findByOwnerId(Long ownerId);
}
```

We would use this in service:

```java
public List<ProjectDto> listProjects(Authentication auth) {
    Long userId = Long.valueOf(auth.getName()); // assuming JWT subject is userId
    List<Project> projects = projectRepo.findByOwnerId(userId);
    return projects.stream().map(proj -> toDto(proj)).collect(Collectors.toList());
}
```

This ensures user only gets their projects. If they somehow guess another ID, they'd have to call another method or endpoint which they don't have. If they try `GET /api/projects/999`, our controller might do:

```java
@GetMapping("/{id}")
public ResponseEntity<ProjectDto> getProject(@PathVariable Long id, Authentication auth) {
    Project proj = projectRepo.findById(id).orElseThrow(() -> new ResourceNotFoundException());
    Long userId = Long.valueOf(auth.getName());
    if (!proj.getOwnerId().equals(userId)) {
        throw new AccessDeniedException("Forbidden");
    }
    return ResponseEntity.ok(toDto(proj));
}
```

We manually check ownership. Alternatively, use @PreAuthorize with SpEL as mentioned:

```java
@PreAuthorize("#id == authentication.name or hasRole('ADMIN')")
@GetMapping("/{id}")
public ProjectDto getProject(@PathVariable Long id) { ... }
```

This requires the auth name to be userId (string) and admin override.

**Transaction Management:**
Use `@Transactional` on service methods to ensure data integrity. If one part fails, the whole transaction rolls back, preventing partial updates that could lead to inconsistent state (which can become a security issue if state checks fail because data is inconsistent).
E.g., if creating a project and adding an entry to another table fails, you don't want half data written.

**Logging DB Access:**
Maybe enable slow query log to identify performance issues (not directly security, but availability).
For security, could log at application level any direct SQL we manually run, but with ORMs it's not straightforward. Instead, ensure our app logs user actions which implies DB changes rather than logging the SQL itself.

By following these database security practices, we align with ISO 27001 controls on secure development (A.14) and access control (A.9) at the data layer. We prevent injection (which is a top OWASP risk) and protect data confidentiality and integrity in storage and transit.

Now that we've built a secure front-end and back-end and ensured secure DB usage, we move on to how to deploy this on AWS securely and integrate cloud services.

## Logging, Monitoring, and Auditing for ISO 27001

_(This was part of Back-end chapter but touches on the broader topic, which will be expanded in chapter 8. We include some back-end specific points here.)_

Implementing robust logging and monitoring in the back-end is crucial for detecting issues and fulfilling ISO 27001 requirements around event logging (A.12.4) and operational monitoring. From the perspective of the Spring Boot app:

- **Application Logs:** Use a logging framework (Spring Boot uses Logback by default) to log important events. At minimum, log errors/exceptions with stack traces (at ERROR level). Also log key security events at INFO or WARN level, such as authentication failures, excessive login attempts, or access denied events. Spring Security can log some of this by enabling a higher log level on its classes. You can also implement an `AuthenticationFailureBadCredentialsEvent` listener to log failed logins.
- **Audit Logging:** As discussed, if the application has critical actions (like changing a role, deleting data), log who did it and when. Example log: "INFO: User 5 deleted Project 42 at 2025-02-15T10:00:00". These logs could be needed in an audit trail. Make sure logs have timestamps and maybe the user ID or username performing the action. Using a **MDC (Mapped Diagnostic Context)** is helpful: you can configure a filter to put the authenticated username into the logging context for each request thread, then include `%X{username}` in log pattern, so every log line includes the user. E.g., `logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} [%X{traceId}] [%X{username}] %-5level %logger{36} - %msg%n`. This would include traceId (from Sleuth) and username from MDC if set. Spring Security can be configured to add username to MDC, or do in a filter once auth is done.
- **Protecting Logs:** Logs can contain sensitive information (like error stack traces that may have class names or even snippets of data). Ensure log files are stored securely (on disk with correct permissions or shipped to a secure log server). For ISO 27001, restrict log access to admins. Also consider log retention policies – keep logs as long as needed for audit (maybe 1 year) then archive or delete safely.
- **No Sensitive Data in Logs:** Be careful not to log secrets or personal data. For example, never log full passwords (even on failure). If you catch an exception that contains sensitive info, sanitize before logging (though exceptions usually don't contain passwords, but maybe a JDBC exception could show a connection string with password if misconfigured - avoid that by not putting password in JDBC URL). If you log requests or responses, ensure to mask things like credit card numbers or passwords. Logging libraries or custom filters can mask patterns (some use regex to replace digits in logs).
- **Monitoring:** Integrate with monitoring tools. For a Spring Boot app, actuators can expose metrics (like request counts, error counts, etc.). On AWS, you might use CloudWatch to collect application logs and metrics. Set up CloudWatch Alarms for certain conditions (like high error rate or repeated login failures). We will expand in chapter 8 about CloudWatch and ELK.
- **ISO 27001 Auditing:** The standard expects that important events (like login, admin actions) are logged and that logs are reviewed regularly ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=,long%2C%20or%20exhibiting%20unusual%20patterns)) ([MySQL Database Security Best Practices](https://www.percona.com/blog/mysql-database-security-best-practices/#:~:text=Log%20analysis%3A%20Regularly%20analyze%20your,sources%2C%20including%20your%20MySQL%20database)). It's good to have a process (maybe weekly log review or alerts hooking to email/Slack for serious issues). Also, maintain an **incident response log** if something is investigated (document timeline of events from logs).
- **Accountability:** Logging ties actions to user IDs, which supports accountability (who did what). This is crucial if something goes wrong, you can trace back. For instance, if data was deleted, logs should show which account initiated that request. Combined with secure authentication, you trust that log entry.

In our Spring Boot back-end, we might configure:

```properties
logging.level.org.springframework.security=INFO
logging.level.com.myapp=INFO
```

This will log security events like "Authentication success/failure". We might also manually log in service:

```java
logger.info("User {} created project {}", currentUserId, newProjectId);
```

One caution: ensure logs don't become a vector for injection. There are attacks where malicious input with special characters might break log format or trick someone reviewing logs (e.g., if someone enters a username like `]error[` to mess up bracket patterns). This is low risk but some advanced secure coding avoid directly concatenating untrusted input in logs. Using placeholders as above `{}` is fine as it handles it safely.

Finally, plan log backup/retention according to policy. Many orgs use a centralized SIEM (Security Info and Event Management) system to aggregate logs from app, DB, OS, AWS CloudTrail, etc., and set correlation rules. For our scope, ensuring the app logs to CloudWatch or a file that is shipped to a central location is enough.

We will address more in the Monitoring chapter.

---

With the back-end covered, we have a solid, secure server-side implementation. Next, we move to deploying this stack on AWS and using AWS services securely.
