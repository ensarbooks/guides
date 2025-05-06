# Building a Udemy-like Video Streaming Platform with React.js & NestJS

This guide provides a comprehensive, step-by-step walkthrough for advanced developers to build a **Udemy-like video streaming application**. We will use **React.js** for the frontend and **NestJS** for the backend, covering everything from initial setup to deployment. Each chapter dives into a key aspect of the project, with detailed steps, code examples, and best practices.

**Table of Contents:**

1. [Project Setup](#project-setup)  
   1.1 [Monorepo Structure or Separate Projects](#monorepo-structure-or-separate-projects)  
   1.2 [Configuring TypeScript, ESLint, and Prettier](#configuring-typescript-eslint-and-prettier)  
   1.3 [Database Setup (PostgreSQL or MongoDB)](#database-setup-postgresql-or-mongodb)

2. [Authentication & User Management](#authentication--user-management)  
   2.1 [Implementing JWT Authentication](#implementing-jwt-authentication)  
   2.2 [OAuth Integration (Optional)](#oauth-integration-optional)  
   2.3 [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)

3. [Course Creation & Management](#course-creation--management)  
   3.1 [Course and User Models](#course-and-user-models)  
   3.2 [Instructors: Creating and Managing Courses](#instructors-creating-and-managing-courses)  
   3.3 [Video Upload and Storage (AWS S3, Cloudinary, Firebase)](#video-upload-and-storage-aws-s3-cloudinary-firebase)  
   3.4 [Course Pricing and Monetization](#course-pricing-and-monetization)

4. [Video Streaming & Playback](#video-streaming--playback)  
   4.1 [Adaptive Streaming with HLS/DASH](#adaptive-streaming-with-hlsdash)  
   4.2 [Building a Custom Video Player (React Player or Video.js)](#building-a-custom-video-player-react-player-or-videojs)  
   4.3 [Secure Video Streaming (Signed URLs, DRM)](#secure-video-streaming-signed-urls-drm)

5. [Payment Integration](#payment-integration)  
   5.1 [Integrating Stripe](#integrating-stripe)  
   5.2 [Integrating PayPal (Alternative)](#integrating-paypal-alternative)  
   5.3 [Handling Purchases, Refunds, and Subscriptions](#handling-purchases-refunds-and-subscriptions)

6. [Reviews & Ratings](#reviews--ratings)  
   6.1 [Implementing a Review System](#implementing-a-review-system)  
   6.2 [Moderation and Content Management](#moderation-and-content-management)

7. [Performance Optimization](#performance-optimization)  
   7.1 [Caching Strategies with Redis and CDN](#caching-strategies-with-redis-and-cdn)  
   7.2 [Frontend Performance: Lazy Loading and Code Splitting](#frontend-performance-lazy-loading-and-code-splitting)  
   7.3 [Database Indexing and Query Optimization](#database-indexing-and-query-optimization)

8. [Security Best Practices](#security-best-practices)  
   8.1 [Protecting Against XSS and CSRF](#protecting-against-xss-and-csrf)  
   8.2 [Securing API Endpoints (Auth Middleware & Guards)](#securing-api-endpoints-auth-middleware--guards)  
   8.3 [Rate Limiting and DDoS Protection](#rate-limiting-and-ddos-protection)

9. [Deployment & Scaling](#deployment--scaling)  
   9.1 [Deploying the Frontend (Vercel, Netlify, AWS Amplify)](#deploying-the-frontend-vercel-netlify-aws-amplify)  
   9.2 [Deploying the Backend (AWS, DigitalOcean, Heroku)](#deploying-the-backend-aws-digitalocean-heroku)  
   9.3 [CI/CD Pipeline Setup (GitHub Actions/GitLab CI)](#cicd-pipeline-setup-github-actionsgitlab-ci)  
   9.4 [Scaling Considerations and Cloud Infrastructure](#scaling-considerations-and-cloud-infrastructure)

10. [Testing & Debugging](#testing--debugging)  
    10.1 [Unit and Integration Testing with Jest](#unit-and-integration-testing-with-jest)  
    10.2 [End-to-End Testing with Cypress](#end-to-end-testing-with-cypress)  
    10.3 [Debugging Common Issues (Frontend & Backend)](#debugging-common-issues-frontend--backend)  
    10.4 [Monitoring and Logging (Sentry, Datadog, ELK)](#monitoring-and-logging-sentry-datadog-elk)

Let's get started with the project setup!

---

## Project Setup

In this chapter, we will initialize our project environment. We’ll use a **monorepo** structure to house both the frontend (React) and backend (NestJS) together, which simplifies development and sharing code between the two. If you prefer separate repositories, you can adapt these steps accordingly. We will also configure TypeScript for a consistent development experience, and set up linting/formatting tools (**ESLint** and **Prettier**) to maintain code quality. Finally, we'll prepare our database (either PostgreSQL or MongoDB) to store application data.

### 1.1 Monorepo Structure or Separate Projects

**Monorepo vs. Multi-Repo:** A monorepo keeps frontend and backend code in one repository, easing code sharing and coordination. Tools like Nx or Yarn Workspaces can help manage a monorepo efficiently. Nx, in particular, is a powerful toolkit for monorepos that supports both React and NestJS and can optimize builds and testing for large projects. If you use separate repos, you can still follow the steps but maintain two codebases.

- **Using Nx (Optional but Recommended):** Nx provides generators and build tools for a unified repo. To use Nx:

  1. **Install Nx CLI:** `npm install -g nx` (you can also use `npx nx` without global install).
  2. **Create a workspace:** Run `npx create-nx-workspace@latest my-org` and follow the prompts. Choose **React** as the preset for the frontend app, and select **Vite** or CRA as the builder. Nx will create an initial React app (often in `apps/` directory).
  3. **Add NestJS app:** Once the workspace is ready, add a NestJS application by running `nx g @nx/nest:app api` (where "api" is the name of the backend app). Nx will scaffold a NestJS project under `apps/api`.
  4. **Verify structure:** You should have a structure like:
     ```
     my-org/
       apps/
         ui/    (React frontend)
         api/   (NestJS backend)
       libs/    (shared libraries, if any)
       package.json (workspace root)
       tsconfig.base.json (shared TypeScript config)
     ```
     With Nx, both apps share configurations and can easily reference shared code. Nx also helps with running both servers concurrently and setting up testing.

- **Using Yarn Workspaces or Lerna:** As an alternative, Yarn workspaces (or npm workspaces) and Lerna can organize a monorepo. The idea is similar: have a root `package.json` with workspaces pointing to `frontend/` and `backend/` directories. Each project is a separate package. Yarn will install dependencies for both together. This approach requires manual setup of scripts for running both projects. Nx, on the other hand, comes with a lot of this pre-configured.

- **Separate Repositories:** If you opt out of a monorepo, initialize two separate projects: one for React and one for NestJS. For example:
  - Create a React app (you can use Create React App: `npx create-react-app udemy-clone-front --template typescript`, or Vite, or Next.js if desired).
  - Create a NestJS app: `nest new udemy-clone-back` using Nest CLI.
  - You’ll manage them separately, but ensure to sync API contracts (e.g., using a shared API specification or client library).

**Installing NestJS CLI:** If you haven't installed NestJS CLI globally, do so with `npm i -g @nestjs/cli`. This allows using the `nest` command to create and manage Nest projects.

**Directory Setup:** For the purposes of this guide, we'll assume a monorepo using Nx (for clarity). However, each step will still apply if you use separate projects. You may need to run commands in the respective project directories.

### 1.2 Configuring TypeScript, ESLint, and Prettier

Both React (frontend) and NestJS (backend) use **TypeScript**, which provides static typing for easier maintenance and fewer bugs. We will ensure TypeScript is properly configured, and set up **ESLint** and **Prettier** for code linting and formatting.

**TypeScript Configuration:**

- **Shared Config (Monorepo):** If using Nx or a monorepo, you likely have a base TypeScript config (like `tsconfig.base.json`) and project-specific configs extending it. Verify that the `compilerOptions` are suitable. Key settings include:
  - `target` (ES2017 or later for modern JS),
  - `module` (commonjs for Node backend, ESNext or something appropriate for frontend bundler),
  - `strict: true` for strict type checking,
  - `esModuleInterop: true` and `allowSyntheticDefaultImports: true` to ease importing CommonJS modules,
  - For NestJS, `emitDecoratorMetadata` and `experimentalDecorators` should be true (needed for Angular and Nest decorators).
  - For React, JSX setting should be enabled (`jsx: react-jsx` if using React 17+ JSX transform).
- **Frontend tsconfig:** Ensure paths to include `src/` and appropriate typings. Create React App or Vite templates usually come with a good tsconfig. If using Nx, it's pre-configured.
- **Backend tsconfig:** NestJS application has a `tsconfig.json` and a `tsconfig.build.json` for compilation. Check that the outDir is `dist/` and sourceMap is true (for debugging).

**ESLint Setup:**

ESLint helps catch code issues and enforce style. We want a unified style across frontend and backend if possible.

- **Installing ESLint:** Many scaffolding tools include ESLint. NestJS has an ESLint config by default. For React, CRA also sets up ESLint. If not, install it: `npm i -D eslint` and relevant plugins.
- **Common Configuration:** Consider using a single ESLint config that works for both. You might create a root `.eslintrc.json` with base rules, and then override settings in `apps/ui/.eslintrc.json` and `apps/api/.eslintrc.json` for React and Nest respectively (for example, React might need React-specific lint rules, NestJS might need Node rules).
- **TypeScript ESLint:** Install `@typescript-eslint/eslint-plugin` and `@typescript-eslint/parser` to lint TypeScript code. Also include recommended configs:

  ```json
  // Example .eslintrc.json fragment
  {
    "extends": [
      "eslint:recommended",
      "plugin:@typescript-eslint/recommended",
      "plugin:prettier/recommended"
    ],
    "parser": "@typescript-eslint/parser",
    "plugins": ["@typescript-eslint"]
  }
  ```

  You might use separate extends for React (`plugin:react/recommended`, etc.) in the frontend config.

- **Prettier Integration:** We will use Prettier for formatting, and integrate it with ESLint to avoid conflicts. Install Prettier and the ESLint Prettier plugin: `npm i -D prettier eslint-config-prettier eslint-plugin-prettier`.  
  Create a basic `.prettierrc` (or `prettier.config.js`) in the root, for example:
  ```json
  {
    "semi": true,
    "singleQuote": true,
    "printWidth": 100
  }
  ```
  In ESLint config, extending `"plugin:prettier/recommended"` ensures Prettier rules override conflicting ESLint rules. This way, running ESLint will report formatting issues which Prettier can fix.

**Running Lint and Format:**

- Add npm scripts to package.json for convenience:
  - `"lint": "eslint . --ext .ts,.tsx --fix"` (this will lint all files and auto-fix where possible),
  - `"format": "prettier --write \"**/*.{ts,tsx,js,json,md}\""` to format various file types.
- Run `npm run lint` and `npm run format` regularly or set up a pre-commit hook (using Husky) to enforce style on commits.

**Note:** A monorepo approach can share a single ESLint/Prettier config, which avoids duplication and ensures consistency across the frontend and backend projects. If you encounter issues where ESLint doesn't pick up the correct parser for React vs Node, you can specify `overrides` in the config to target specific folders with different settings.

### 1.3 Database Setup (PostgreSQL or MongoDB)

A robust application needs a database. In our case, we may choose a relational database like **PostgreSQL** (with an ORM such as TypeORM or Prisma) or a NoSQL database like **MongoDB** (with Mongoose). We will outline steps for both:

**Option A: PostgreSQL with TypeORM (or Prisma)**

1. **Install Database Server:** For local development, you can install PostgreSQL directly or use Docker. If using Docker, a simple approach is:

   ```bash
   docker run --name udemy-postgres -e POSTGRES_USER=udemyuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=udemy_db -p 5432:5432 -d postgres:14
   ```

   This runs a Postgres container with a database `udemy_db` on port 5432. Remember the credentials for your app config.

2. **Install TypeORM and NestJS integration:** Nest provides `@nestjs/typeorm` package. In the NestJS app, install TypeORM and the Postgres driver:

   ```bash
   npm install @nestjs/typeorm typeorm pg
   ```

   This will add TypeORM support and the `pg` driver for PostgreSQL. (Alternatively, if you prefer Prisma, you would set up Prisma client and schema instead.)

3. **Configure TypeORM:** In your NestJS app, typically in `app.module.ts`, import the `TypeOrmModule`. For example:

   ```typescript
   import { TypeOrmModule } from "@nestjs/typeorm";

   @Module({
     imports: [
       TypeOrmModule.forRoot({
         type: "postgres",
         host: "localhost",
         port: 5432,
         username: "udemyuser",
         password: "mypassword",
         database: "udemy_db",
         entities: [__dirname + "/**/*.entity{.ts,.js}"], // paths to entity classes
         synchronize: true, // auto-create tables in dev; disable in prod
       }),
       // ... other modules
     ],
   })
   export class AppModule {}
   ```

   This sets up a connection to the Postgres database. The `synchronize: true` option auto-generates database tables from your entities each time you run the app (convenient for development, but use migrations or disable in production for safety).

   _If using Prisma_, you would instead run `npx prisma init` to set up Prisma schema, configure the database URL in `.env`, and use Prisma's client in NestJS via a custom provider or NestJS Prisma module.

4. **Define Entities:** Create entity classes for core concepts (User, Course, Video, Enrollment, etc.) using TypeORM decorators:

   ```typescript
   import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from "typeorm";
   @Entity()
   export class Course {
     @PrimaryGeneratedColumn()
     id: number;

     @Column()
     title: string;

     @Column("text")
     description: string;

     @ManyToOne(() => User, (user) => user.courses)
     instructor: User;

     // ...other columns like price, etc.
   }
   ```

   Similarly define a `User` entity, `Video` entity (if separate from Course, representing each lecture video), `Enrollment` entity (linking users to courses they purchased), etc. We'll flesh these out in later sections.

5. **Test Connection:** Run the NestJS application (`npm run start` or `nx serve api` if using Nx). The console should show TypeORM connecting and (if `synchronize` is true) creating tables. If any errors occur (e.g., connection refused), check the database credentials and that the DB server is running.

**Option B: MongoDB with Mongoose**

1. **Install MongoDB Server:** You can install MongoDB locally or use Docker. Docker example:

   ```bash
   docker run --name udemy-mongo -p 27017:27017 -d mongo:5
   ```

   This runs MongoDB on default port 27017 without authentication (fine for dev; for prod, set up user and password).

2. **Install Mongoose and NestJS Mongoose Module:**

   ```bash
   npm install @nestjs/mongoose mongoose
   ```

   This adds the NestJS Mongoose module to integrate Mongoose (MongoDB ODM).

3. **Configure Mongoose:** In `app.module.ts`:

   ```typescript
   import { MongooseModule } from "@nestjs/mongoose";

   @Module({
     imports: [
       MongooseModule.forRoot("mongodb://localhost:27017/udemy_db"),
       // ... other modules
     ],
   })
   export class AppModule {}
   ```

   Provide the connection string to your MongoDB. If credentials are needed: e.g., `'mongodb://user:pass@host:27017/dbname'`. The NestJS Mongoose module will handle connecting at app startup.

4. **Define Schemas and Models:** Instead of TypeORM entities, define Mongoose schemas. For example, create a `schemas/course.schema.ts`:

   ```typescript
   import { Schema, Prop, SchemaFactory } from "@nestjs/mongoose";
   import { Document } from "mongoose";

   @Schema()
   export class Course extends Document {
     @Prop({ required: true })
     title: string;

     @Prop({ required: true })
     description: string;

     @Prop({ type: Number, required: true })
     price: number;

     @Prop({ type: String, ref: "User" })
     instructorId: string;
     // ...
   }
   export const CourseSchema = SchemaFactory.createForClass(Course);
   ```

   Similarly define `User` schema, etc. In the module (e.g., a CourseModule), register the schema:

   ```typescript
   @Module({
     imports: [
       MongooseModule.forFeature([{ name: Course.name, schema: CourseSchema }]),
     ],
     providers: [CourseService],
     controllers: [CourseController],
   })
   export class CourseModule {}
   ```

   Now you can inject the Mongoose model in services using `@InjectModel(Course.name)`.

5. **Test Connection:** Run the NestJS app. You should see a successful connection to MongoDB in the logs. No tables to create (MongoDB is schemaless), but ensure no errors.

**ESLint/Prettier for Database Entities/Schemas:** If using TypeORM, you might want to separate entity definitions into their own folder. Ensure your linting covers those files too. If using Prisma, the schema file is separate (`schema.prisma`), and doesn't go through ESLint.

**Conclusion of Setup:** By now, we have:

- A project structure (monorepo) with React and NestJS apps.
- TypeScript configured on both sides.
- ESLint and Prettier ensuring code quality.
- A database running (Postgres or Mongo) and connected to our NestJS app.

We are ready to implement features like authentication, course management, and more. Next, we'll tackle authentication and user management.

---

## Authentication & User Management

User authentication is a critical part of our application, enabling users to sign up, log in, and access protected resources. We’ll implement **JWT-based authentication** for stateless API security, and discuss **OAuth** options for social logins if needed. We’ll also set up **Role-Based Access Control (RBAC)** to differentiate between **students** and **instructors** (and possibly admins), ensuring that only authorized users can perform certain actions (e.g., only instructors can create courses).

### 2.1 Implementing JWT Authentication

**Why JWT?** JSON Web Tokens (JWT) allow stateless authentication. The server issues a signed token after verifying user credentials, and the client (frontend) stores this token (typically in localStorage or a secure HTTP-only cookie). On subsequent requests, the token is sent (usually in the Authorization header) and the backend verifies it to authenticate the user. This eliminates the need to store session state on the server.

**NestJS Authentication Overview:** NestJS leverages the Passport library to streamline auth. We will use the `@nestjs/passport` and `@nestjs/jwt` modules to implement JWT auth. The high-level steps are:

1. Create an **AuthModule** and a **UsersModule** in NestJS.
2. Use **Passport JWT Strategy** to validate JWTs.
3. Create a login route to issue JWTs, and a guard to protect routes by requiring a valid JWT.

Let's implement step by step.

**Step 1: Install auth packages.** In the NestJS backend, install the required packages for authentication:

```bash
npm install --save @nestjs/passport @nestjs/jwt passport passport-local passport-jwt
npm install --save-dev @types/passport-local @types/passport-jwt
```

This includes Nest wrappers for Passport, and Passport strategies for local (username/password) and JWT.

**Step 2: Generate Modules and Services.** Use Nest CLI (or manually create files):

```bash
nest g module auth
nest g service auth
nest g controller auth
nest g module users
nest g service users
nest g controller users
```

These will scaffold basic classes. In a monorepo or Nx, ensure to run these in the backend app directory (e.g., `apps/api`).

We'll need a **User model**. If you have a User entity (TypeORM) or schema (Mongoose) from the setup, we will use that. Otherwise, for demonstration, let's create a simple User model for now. For example, define a `User` interface or class:

```typescript
// users/user.entity.ts (for TypeORM, otherwise a class/interface)
export enum Role {
  Student = "student",
  Instructor = "instructor",
  Admin = "admin",
}

export class User {
  id: number;
  email: string;
  password: string; // hashed password
  roles: Role[];
}
```

In a real app, this would be an Entity with decorators or a Mongoose schema. We also define a Role enum for RBAC.

**Step 3: UsersService – managing users.** Implement basic user lookup in the UsersService. For now, it might just have an in-memory array or use TypeORM repository:

```typescript
@Injectable()
export class UsersService {
  private users: User[] = [
    {
      id: 1,
      email: "alice@example.com",
      password: "hashedpw1",
      roles: [Role.Instructor],
    },
    {
      id: 2,
      email: "bob@example.com",
      password: "hashedpw2",
      roles: [Role.Student],
    },
  ];
  async findByEmail(email: string): Promise<User | undefined> {
    return this.users.find((u) => u.email === email);
  }
  async findById(id: number): Promise<User | undefined> {
    return this.users.find((u) => u.id === id);
  }
}
```

Later, we will replace this with real database calls (e.g., using a UserRepository if TypeORM, or `UserModel` if Mongoose).

**Step 4: AuthService – validating users and generating JWT.** In `AuthService`, write a method to validate user credentials and another to generate JWT token:

```typescript
@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService // provided by @nestjs/jwt
  ) {}

  async validateUser(email: string, pass: string): Promise<any> {
    const user = await this.usersService.findByEmail(email);
    if (user && user.password === pass) {
      // NOTE: compare hashed in real app
      const { password, ...result } = user;
      return result; // return user data excluding password
    }
    return null;
  }

  async login(user: any) {
    const payload = { sub: user.id, roles: user.roles, email: user.email };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
```

This service checks a user’s email/password (here we’re not hashing for brevity, but you must hash passwords in production). If valid, it signs a JWT containing the user's ID and roles. The `JwtService` comes from NestJS JWT module which we'll configure next.

**Step 5: Configure JWT Module.** In `AuthModule`, import `JwtModule` with a secret:

```typescript
@Module({
  imports: [
    PassportModule,
    JwtModule.register({
      secret: "myjwtsecret", // move to env in real app
      signOptions: { expiresIn: "1h" },
    }),
    UsersModule,
  ],
  providers: [AuthService],
  controllers: [AuthController],
})
export class AuthModule {}
```

Use a strong secret from an environment variable in practice. Set token expiration (here 1 hour).

**Step 6: Implement LocalStrategy (for login).** We use `passport-local` to verify username/password:

```typescript
@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy) {
  constructor(private authService: AuthService) {
    super({ usernameField: "email" }); // by default passport-local expects 'username'
  }
  async validate(email: string, password: string): Promise<any> {
    const user = await this.authService.validateUser(email, password);
    if (!user) {
      throw new UnauthorizedException();
    }
    return user;
  }
}
```

Register this in AuthModule providers (and ensure to import `PassportStrategy` and `Strategy` from passport-local).

**Step 7: Implement JWT Strategy (for guarding routes).** This will validate JWTs on protected endpoints:

```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(PassportJwtStrategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: "myjwtsecret",
    });
  }
  async validate(payload: any) {
    // payload contains data we signed (sub, roles, etc.)
    return { userId: payload.sub, email: payload.email, roles: payload.roles };
  }
}
```

Here `PassportJwtStrategy` is imported from `passport-jwt`. We extract token from the Authorization header (`Bearer <token>`). The `validate` method returns the data to attach to the request (as `req.user`). Register this in AuthModule providers as well.

**Step 8: AuthController – login and signup routes.** Create endpoints for login (and optionally signup):

```typescript
@Controller("auth")
export class AuthController {
  constructor(private authService: AuthService) {}

  @UseGuards(AuthGuard("local")) // use Passport local strategy for this route
  @Post("login")
  async login(@Request() req) {
    // If AuthGuard('local') passes, req.user will be set
    return this.authService.login(req.user);
  }

  @Post("register")
  async register(@Body() dto: RegisterDto) {
    // implement user creation (hash password, save to DB)
    // for now, just a placeholder
    return { message: "User registered (stub)" };
  }
}
```

The `AuthGuard('local')` automatically calls our LocalStrategy to validate credentials. On success, it attaches the user to `req.user`, which we then pass to AuthService.login to get a JWT. The response will be `{ access_token: "jwt..." }`. On the React side, we'll call this endpoint and store the token.

**Step 9: Protecting Routes with JWT Guard.** For any authenticated route (like fetching user profile, enrolling in a course, creating a course, etc.), use `AuthGuard('jwt')`:

```typescript
@Controller("courses")
export class CoursesController {
  constructor(/* ... */) {}

  @UseGuards(AuthGuard("jwt"))
  @Get()
  findAllCourses() {
    // Only authenticated users can hit this
    // For example, return list of courses (some might be free or previewable)
  }

  @UseGuards(AuthGuard("jwt"))
  @Post()
  createCourse(@Body() dto: CreateCourseDto, @Req() req) {
    // Only authenticated (and specifically instructors - we'll handle that via roles) can create
    const user = req.user; // set by JwtStrategy validate()
    // ... create course with user as instructor
  }
}
```

We will refine authorization using roles in the RBAC section. For now, the JWT guard ensures only logged-in users with a valid token can access these endpoints. NestJS makes it easy to secure endpoints with such guards as middleware.

**Frontend Integration (Login Flow):** On the React side, create a login page where the user enters email and password. On form submit, call the backend `POST /auth/login` endpoint with the credentials (e.g., using `fetch` or Axios). If successful, you will get an `access_token` in JSON. Save this token:

- E.g., `localStorage.setItem('token', data.access_token);` (simplest approach).
- Alternatively, set a cookie (if you adjust the backend to set HttpOnly cookies, but that complicates CSRF handling; JWT in localStorage is common for single-page apps, but be mindful of XSS).

Then include this token in the `Authorization` header for subsequent API calls:

```js
axios.get("/courses", { headers: { Authorization: `Bearer ${token}` } });
```

We will manage global auth state in React (perhaps using Context or Redux, beyond scope here).

**Password Hashing:** Ensure that in your final implementation, you hash user passwords (e.g., using bcrypt). The validation in AuthService should use `bcrypt.compare(password, user.passwordHash)`.

**JWT Refresh Tokens (Optional):** For better security, you might implement refresh tokens to avoid long-lived JWTs. This involves issuing a second token with longer expiry and a mechanism to refresh the access token. Given the scope, we'll stick to access tokens only.

At this point, we have a working JWT authentication system:

- Users can register (sign up) and login.
- We issue JWTs for login.
- Protected routes require the JWT.

Next, we'll consider OAuth options for social logins.

### 2.2 OAuth Integration (Optional)

If you want users to log in using Google, Facebook, or other OAuth providers (common for modern apps), NestJS can integrate Passport strategies for OAuth (e.g., `passport-google-oauth20`).

**Setup for Google OAuth (example):**

1. Install the strategy: `npm install passport-google-oauth20 @types/passport-google-oauth20`.
2. Create a GoogleStrategy class extending `PassportStrategy` similar to above, configure with client ID/secret and callback URL.
3. Use `AuthGuard('google')` in a controller route to redirect to Google OAuth consent page.
4. Handle the callback route to get the profile, then either create or find a user in DB, and then issue a JWT for them.

Due to length, we won't do detailed steps here, but the outline is:

- e.g., `@Get('google') @UseGuards(AuthGuard('google'))` on a route will redirect.
- Then `@Get('google/callback') @UseGuards(AuthGuard('google'))` will handle the callback where `req.user` contains Google profile info. Here you’d log the user in (JWT issuance).

Implementing OAuth can enhance user convenience, but ensure to still handle linking accounts and security. This guide will proceed with JWT as the primary auth method for simplicity.

### 2.3 Role-Based Access Control (RBAC)

Our application has different user roles with distinct permissions:

- **Student:** Can purchase courses, watch videos, write reviews.
- **Instructor:** Can create courses, upload content, view their students.
- **Admin (optional):** Can manage the platform, moderate content.

We need to enforce that, for example, only an **Instructor** can create a new course, and only the **owner of a course** or an **admin** can edit it. This is where RBAC comes in.

**Approach to RBAC:** We will use a **Roles Guard** in NestJS to check user roles against required roles on each route. NestJS provides a way to implement custom guards and decorators for roles ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=Finally%2C%20we%20create%20a%20,package)).

**Step 1: Define Roles Enum (we did this above)** – we have a `Role` enum with values like 'student', 'instructor', 'admin'. This can be in a shared file (e.g., `users/role.enum.ts`).

**Step 2: Create a Roles decorator:** This will allow us to annotate routes with required roles.

```typescript
import { SetMetadata } from "@nestjs/common";
import { Role } from "./role.enum";
export const ROLES_KEY = "roles";
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);
```

This uses `SetMetadata` to attach roles metadata to the route handler.

**Step 3: Implement RolesGuard:** A guard that reads the required roles and compares with the user’s roles:

```typescript
import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { ROLES_KEY } from "./roles.decorator";
import { Role } from "./role.enum";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) {
      return true; // no roles required for this route
    }
    const { user } = context.switchToHttp().getRequest();
    if (!user) return false;
    // Check if the user's roles include any of the required roles
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

This guard uses NestJS `Reflector` to retrieve the roles metadata we set with the `@Roles` decorator on the route ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=%40Injectable,private%20reflector%3A%20Reflector%29)) ([Authorization | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/authorization#:~:text=%5D%29%3B%20if%20%28%21requiredRoles%29%20,user.roles%3F.includes%28role%29%29%3B)). If the route requires no roles, it's public or just needs authentication. If roles are required, it ensures the logged-in user (`req.user` from JWT) has at least one of those roles.

**Step 4: Apply RolesGuard:** There are a couple of ways:

- **Globally:** In your `AppModule`, you could provide it as a global guard:
  ```typescript
  providers: [
    {
      provide: APP_GUARD,
      useClass: RolesGuard,
    },
  ];
  ```
  This way, RolesGuard runs for all requests. However, you would combine it with the JWT AuthGuard or incorporate authentication in it.
- **Locally on Controllers/Routes:** Use both `@UseGuards(AuthGuard('jwt'), RolesGuard)` and the `@Roles(...)` decorator on specific routes.

For clarity, we'll use the second approach on specific routes:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Post('courses')
createCourse(...) { ... }
```

This ensures the user is logged in (JWT guard) and an Instructor (RolesGuard checks roles). We can also stack roles, e.g., `@Roles(Role.Admin, Role.Instructor)` if either can access.

**Attaching Roles to Users:** When a user registers, by default assign them a 'student' role. We may allow upgrading to instructor via an application or admin action. For now, assume that we mark certain users as instructors manually (or provide an endpoint to become instructor, which is beyond scope).

**Frontend Consideration for Roles:** The React app should be aware of the user’s role after login (since the JWT contains roles). We can decode the JWT on the client side (careful: do not trust it fully on client, but for UI logic it's fine) to know if the user is instructor or student and show/hide certain UI elements (like "Create Course" button). Alternatively, have an API `/auth/profile` that returns user info including roles, which the React app calls after login to get authoritative data.

At this point, our auth system supports:

- JWT login and protected routes.
- Role-based access to certain features.

Next, we will move to course creation and management, where we'll apply these auth mechanisms.

---

## Course Creation & Management

This chapter focuses on the core feature: instructors creating courses, and students viewing/enrolling in courses. We will design the data models for courses and related entities, implement features for instructors to manage their content, handle video uploads to a storage service, and consider course pricing.

### 3.1 Course and User Models

Before writing endpoints, let's refine our data model for courses:

- **User**: represents a student or instructor (or admin). Key fields: `id, name, email, passwordHash, roles, etc.`.
- **Course**: represents a course. Key fields:
  - `id`
  - `title`
  - `description` (text, possibly long)
  - `price` (number, could be 0 for free or some currency amount)
  - `instructorId` (relation to User who created it)
  - `thumbnail` (URL to an image)
  - `language`, `level` (optional metadata)
  - `createdAt`, `updatedAt` timestamps
- **Video (Lecture)**: Each course contains multiple video lectures. We can model videos as a separate entity that links to Course.
  - Fields: `id, courseId, title, videoUrl (or storage key), orderIndex, duration, etc.`
- **Enrollment/Purchase**: A join entity linking User (student) and Course to indicate the student has bought/enrolled in the course. Fields: `id, studentId, courseId, purchaseDate, etc.`.
- **Review**: We'll cover in the Reviews section, but mention it here: `id, courseId, studentId, rating, comment, createdAt`.

If using TypeORM (Postgres):

- Define these as @Entity classes with relations (`ManyToOne`, `OneToMany`).
- Use repositories or TypeORM query builder in services to manage them.
  If using Mongoose:
- Define schemas and use Mongoose models in services.

**Example Entity (TypeORM) for Course:**

```typescript
@Entity()
export class Course {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column("text")
  description: string;

  @Column("decimal", { precision: 10, scale: 2, default: 0 })
  price: number;

  @Column({ default: false })
  published: boolean;

  @ManyToOne(() => User, (user) => user.courses, { eager: true })
  instructor: User;

  @OneToMany(() => Video, (video) => video.course)
  videos: Video[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

**Example Schema (Mongoose) for Course:**

```typescript
@Schema({ timestamps: true })
export class Course extends Document {
  @Prop({ required: true })
  title: string;

  @Prop({ required: true })
  description: string;

  @Prop({ type: Number, default: 0 })
  price: number;

  @Prop({ default: false })
  published: boolean;

  @Prop({ type: mongoose.Schema.Types.ObjectId, ref: "User" })
  instructorId: string;
}
export const CourseSchema = SchemaFactory.createForClass(Course);
```

We would also have a VideoSchema etc., but let's proceed with the logic.

### 3.2 Instructors: Creating and Managing Courses

**Instructors create courses:** We want an API endpoint where an instructor can create a new course (with basic info initially, like title, description, price). They might then upload videos to it (handled in next section). Possibly, instructors can also update their course details or publish/unpublish courses.

**Endpoint Design:**

- `POST /courses` – Create a new course. **Auth:** Instructor only.
- `PUT /courses/:id` – Update course details (only instructor of that course or admin).
- `POST /courses/:id/videos` – Upload a new lecture video to the course (instructor only).
- `GET /instructor/courses` – List courses for the logged-in instructor to manage.
- `GET /courses` – List all published courses (for students to browse).
- `GET /courses/:id` – Get details of a specific course (if published or if owner viewing).
- Possibly endpoints for deleting a course, etc.

We will implement some of these.

**Create Course (Backend):**

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Post('courses')
async createCourse(@Body() createCourseDto: CreateCourseDto, @Req() req) {
  const user = req.user;  // from JwtStrategy
  // Assuming we have a CourseService with a method to create
  return this.courseService.createCourse(user.userId, createCourseDto);
}
```

The `CreateCourseDto` might include title, description, price, etc. The service will:

- Validate the data (you can use class-validator decorators on DTO).
- Create a new Course entity and save it, associating the instructor (userId from JWT).

**CourseService.createCourse example:**

```typescript
async createCourse(instructorId: number, dto: CreateCourseDto): Promise<Course> {
  const instructor = await this.usersRepo.findOne(instructorId);
  if (!instructor) throw new Error('Instructor not found');
  const course = this.courseRepo.create({
    ...dto,
    instructor,
    published: false  // start as draft
  });
  return this.courseRepo.save(course);
}
```

If using Mongoose, similar logic but use `new this.courseModel(dto)`.

**Update Course:**
To allow instructors to edit, say `PUT /courses/:id`:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Put('courses/:id')
async updateCourse(@Param('id') id: string, @Body() dto: UpdateCourseDto, @Req() req) {
  const courseId = parseInt(id);
  await this.courseService.updateCourse(req.user.userId, courseId, dto);
  return { message: 'Course updated' };
}
```

In `courseService.updateCourse(instructorId, courseId, dto)`, ensure the course exists and belongs to that instructor (unless the user is admin). For example:

```typescript
async updateCourse(userId: number, courseId: number, dto: UpdateCourseDto) {
  const course = await this.courseRepo.findOne({ where: { id: courseId }, relations: ['instructor'] });
  if (!course) throw new NotFoundException('Course not found');
  if (course.instructor.id !== userId) {
    throw new ForbiddenException('You are not the instructor of this course');
  }
  Object.assign(course, dto);
  await this.courseRepo.save(course);
}
```

Admins could be allowed to edit any course (so you might allow Role.Admin too).

**Listing Courses (Instructor view):**
Endpoint `GET /instructor/courses`:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Get('instructor/courses')
async getMyCourses(@Req() req) {
  const userId = req.user.userId;
  return this.courseService.findByInstructor(userId);
}
```

This would return courses where `course.instructor.id = userId`. In SQL, ensure an index on instructorId for fast lookup. In Mongo, ensure an index on instructorId field as well.

**Listing Courses (Public):**
For the main marketplace, `GET /courses` could return all published courses (maybe with basic info). Public, but you might still allow logged-in to call it:

```typescript
@Get('courses')
async listCourses(@Query('search') search: string) {
  return this.courseService.findAllPublished(search);
}
```

We can implement search by title, etc., but for now just return all courses with `published: true`. Ensure not to return unpublished courses to students.

**Course Details:**
`GET /courses/:id` – return course info. If the course is published or if the requesting user is the instructor or a student who purchased it, allow. Otherwise if it's a draft and not their course, deny.

**Important:** These are basic implementations. In a full app, you'd likely structure controllers and services by domain (CourseController, InstructorController, etc.). Also, error handling and validation should be robust.

### 3.3 Video Upload and Storage (AWS S3, Cloudinary, Firebase)

Video content is the heart of the platform. We need a way for instructors to upload videos for their courses. Storing videos directly on our server’s file system is not recommended for scalability. Instead, we will use cloud storage:

- **AWS S3** (Amazon Simple Storage Service): Scalable object storage. We can upload videos to S3 and serve them via CDNs.
- **Cloudinary** or **Firebase Storage**: Alternatives that also offer easy uploads and in Cloudinary’s case, on-the-fly processing.

We'll illustrate using **AWS S3** with **pre-signed URLs** approach, which is common:

- The client (React) requests an upload URL from our backend for a specific file.
- The backend (NestJS) uses AWS SDK to generate a pre-signed URL that allows the client to upload directly to S3.
- The client then `PUT`s the file to S3 using that URL.
- We save the video metadata (like the S3 key or URL) in our database.

This approach keeps the heavy file transfer off our server (client uploads directly to S3) and is secure because the URL is short-lived and specific to that file.

**Setting up AWS SDK:**  
Install AWS SDK v3 (modular) or v2. For v3:

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-presigned-post
```

For simplicity, we can also use AWS SDK v2:

```bash
npm install aws-sdk
```

We'll outline with v2 for brevity.

**Configuration:**  
Store AWS credentials (Access Key, Secret, region, bucket name) in environment variables. For example, in a `.env` file (and use `@nestjs/config` to load them).

**Generating a Pre-signed Upload URL (Backend):**  
Create an endpoint `GET /courses/:id/upload-url?filename=...&contentType=...` for instructors to get a URL for uploading a video to a specific course.

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Get('courses/:id/upload-url')
async getUploadUrl(
  @Param('id') courseId: string,
  @Query('filename') filename: string,
  @Query('contentType') contentType: string,
  @Req() req
) {
  const userId = req.user.userId;
  // Verify this course belongs to the user
  await this.courseService.ensureInstructorOwnership(userId, +courseId);
  // Generate S3 pre-signed URL
  const uploadKey = `courses/${courseId}/${Date.now()}_${filename}`;
  const url = await this.fileService.getPresignedUploadURL(uploadKey, contentType);
  return { uploadUrl: url, key: uploadKey };
}
```

In the above:

- `ensureInstructorOwnership` would throw if the course isn't owned by that user.
- We generate a unique key for the file (perhaps include courseId and timestamp).
- `fileService.getPresignedUploadURL` encapsulates AWS S3 logic.

**AWS S3 Presigned URL Generation (using AWS SDK v2):**

```typescript
import AWS from "aws-sdk";
AWS.config.update({
  accessKeyId: process.env.AWS_KEY,
  secretAccessKey: process.env.AWS_SECRET,
  region: process.env.AWS_REGION,
});
const s3 = new AWS.S3();

@Injectable()
export class FileService {
  private readonly bucket = process.env.AWS_S3_BUCKET;

  async getPresignedUploadURL(
    key: string,
    contentType: string
  ): Promise<string> {
    const params = {
      Bucket: this.bucket,
      Key: key,
      Expires: 60, // URL valid for 60 seconds (adjust as needed)
      ContentType: contentType,
      ACL: "private", // files should be private by default (we'll generate viewing URLs later)
    };
    return s3.getSignedUrlPromise("putObject", params);
  }
}
```

This returns a URL that allows an HTTP PUT with the specified content type. We mark files as private since we don't want arbitrary public access; we'll use signed URLs or CloudFront for delivering them (discussed in 4.3).

**Client-side upload (React):**  
On the frontend, when an instructor selects a video file to upload:

1. Call the backend to get upload URL:
   ```js
   const res = await axios.get(`/courses/${courseId}/upload-url`, {
     params: { filename: file.name, contentType: file.type },
     headers: { Authorization: `Bearer ${token}` },
   });
   const { uploadUrl, key } = res.data;
   ```
2. Use the returned `uploadUrl` to PUT the file directly to S3:
   ```js
   await fetch(uploadUrl, {
     method: "PUT",
     body: file,
     headers: { "Content-Type": file.type },
   });
   ```
   This uploads the file to S3. If successful (status 200), the file is now in the bucket at the given key.
3. Save the video record in database:
   After upload, we should inform our backend that the video is ready. We can call another endpoint like `POST /courses/:id/videos` with the `key` and maybe title/duration:
   ```js
   await axios.post(
     `/courses/${courseId}/videos`,
     { title: videoTitle, key: key, duration: videoDuration },
     { headers: { Authorization: `Bearer ${token}` } }
   );
   ```
   The backend will create a Video entity with the S3 key. Duration can be obtained via a library or by reading video metadata on the client before upload.

**Handling Video Transcoding:** If we want HLS streaming (multiple quality levels), one approach is to let the instructor upload the raw video, and then have a background job or AWS service convert it to HLS playlist and segments. This can be complex; services like AWS Elastic Transcoder or AWS MediaConvert can do this automatically upon upload. For simplicity, we might skip transcoding here and assume the instructor provides a ready MP4 that we will stream (with the option to add HLS conversion later).

**Alternate approach with Cloudinary:** Cloudinary allows client-side upload via their library, and can auto-convert videos and provide streaming URLs. If using Cloudinary, you might not need your own presigned logic; instead, use their upload widget or API. Similar with Firebase Storage (use Firebase SDK on client directly).

**Video Storage Summary:** Our approach using S3 presigned URLs means:

- The server does not handle the video bytes (just generates a one-time credential).
- The upload is secure (only valid for a short time, and tied to our credentials) ([Uploading objects with presigned URLs - AWS Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html#:~:text=Uploading%20objects%20with%20presigned%20URLs,upload%20without%20requiring%20another)).
- We store video references (S3 keys) in our DB to retrieve later.

Next, we'll discuss streaming those videos (playback) in Section 4.

### 3.4 Course Pricing and Monetization

Monetization features include setting course prices, handling free courses, and potentially implementing promotions or coupons. Here we'll focus on basics:

- Each course has a `price`. If price > 0, it requires purchase to access full content.
- If price = 0, it's a free course (any logged-in user can access).
- Students purchase courses via payments (we'll detail payments in Chapter 5).
- Once purchased, an entry in an Enrollment or Purchase table is created.

**Displaying Prices (Frontend):** On the course list and detail pages, show the price. Possibly format it as $XX. If implementing multiple currencies or localized pricing, that's more advanced (out of scope).

**Free Previews:** Often platforms allow a few lectures as free preview even for paid courses. This could be implemented by marking certain video lectures as `preview: true` which can be accessed without purchase. For now, we won't dive deep, but keep it in mind (maybe one video of each course could be previewable to entice students).

**Instructor Revenue:** If we were to implement instructors earning money, we might need to track purchases per instructor to calculate payouts, etc. That gets complex with tax and so on, but not needed for the functioning of the app. We'll assume platform handles it outside our scope.

**Setting Price:** The instructor, when creating or editing a course, should be able to set the price. Possibly from a predefined set (like $19.99, $29.99, etc.) to standardize pricing, or any value. We should validate this input (non-negative, maybe caps).

**Changing Price:** If an instructor changes the price after some purchases, it won't affect those who already bought. But new students see new price. This is acceptable.

**Course Publishing:** We have a `published` flag in our Course. The workflow might be:

- Instructor creates course (published = false by default). They upload content, etc.
- When ready, they set published = true (perhaps via an endpoint or in the update).
- Only published courses show up in public listing or search.
- Unpublished courses can only be seen by the instructor (and perhaps admins). Students cannot enroll in an unpublished course.

We should implement an endpoint to publish:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Instructor)
@Post('courses/:id/publish')
async publishCourse(@Param('id') courseId: string, @Req() req) {
  await this.courseService.publish(+courseId, req.user.userId);
  return { message: 'Course published' };
}
```

In CourseService.publish:

```typescript
async publish(courseId: number, instructorId: number) {
  const course = await this.courseRepo.findOne({ where: { id: courseId }, relations: ['instructor'] });
  if (!course) throw new NotFoundException();
  if (course.instructor.id !== instructorId) throw new ForbiddenException();
  course.published = true;
  await this.courseRepo.save(course);
}
```

After publishing, students can find and purchase the course.

**Summary:** Course creation and management endpoints allow instructors to:

- Create a new course (draft).
- Upload videos to it.
- Edit details.
- Publish the course.
  Students will in turn:
- View published courses.
- View details (perhaps including a curriculum outline, instructor info).
- Purchase a course (to be covered next).
- After purchase, access the videos.

Now that courses and content can be created and stored, let's tackle how to stream those videos to students efficiently and securely.

---

## Video Streaming & Playback

Delivering a smooth video playback experience is crucial. In this chapter, we'll implement video streaming using adaptive streaming protocols (HLS or DASH), incorporate a video player in the React frontend, and ensure the videos are delivered securely to prevent unauthorized access or piracy.

### 4.1 Adaptive Streaming with HLS/DASH

**What is adaptive streaming?** Traditional video (MP4) might be served as a single file, which can cause buffering if the user's bandwidth is limited. **HLS (HTTP Live Streaming)** and **DASH (Dynamic Adaptive Streaming over HTTP)** are protocols that break video into small chunks and allow switching between different quality levels on the fly. This means the player can adjust the quality based on internet speed, providing a better experience (less buffering). HLS is widely used and works by serving a playlist (M3U8 file) that lists video segment files.

**HLS vs DASH:** HLS is an Apple format, widely supported especially on Safari and iOS. DASH is an MPEG standard, more widely used in DRM contexts. For simplicity, we can use HLS since many open-source players support it.

**Generating HLS Streams:** We have videos uploaded (possibly as MP4). To get HLS, we typically need to transcode them into multiple bitrates and create segments. There are a few approaches:

- Transcode offline using FFmpeg (maybe as part of an upload processing step).
- Use a cloud service (AWS MediaConvert, or Cloudinary can do it if you upload there).
- Use on-the-fly transcoding (less common, heavy load on server).

For an MVP, we might skip actual multi-bitrate and just serve the MP4 directly. However, let's outline HLS in case:

- An FFmpeg command can produce HLS segments and a master playlist. For example:  
  `ffmpeg -i input.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8`  
  (This would create index.m3u8 and segment files).
- Doing this for multiple quality levels (different resolutions/bitrates) yields multiple playlists and a master playlist with each variant.

This is complex to integrate fully here, so assume we prepare an HLS stream for each video. Perhaps the instructor could upload in multiple qualities or we use a background job.

**Serving Video Segments:** If we have HLS files (M3U8 and .ts segment files) stored in S3, we can serve them through CloudFront or via pre-signed URLs similarly. A more straightforward route is:

- Use the frontend player to request the M3U8 playlist from our backend or directly from S3 (if public or using signed URL).
- The player will then fetch segments sequentially.

If not using HLS, a single MP4 can be progressively downloaded, but won't adapt quality.

Given advanced nature, we'll assume we want to use HLS for streaming. We will:

- Either pre-generate HLS for each video.
- Or use a library on server to do it on request (not recommended for scale).

**Backend for streaming:**
We could create an endpoint to get a video URL:
`GET /courses/:courseId/videos/:videoId/stream` which returns a signed URL (with limited time) to the video file (or to an HLS playlist) in S3.

Simpler: We could store videos as private and generate a CloudFront signed URL or an S3 signed URL when a student requests a video. Alternatively, proxy the stream through our backend (which can check auth then stream bytes).

**Secure Access Check:** Ensure the requesting user has purchased the course (or it's free/preview):

```typescript
@UseGuards(AuthGuard('jwt'))
@Get('/courses/:courseId/videos/:videoId/stream-url')
async getVideoStreamUrl(@Param('courseId') courseId: number, @Param('videoId') videoId: number, @Req() req) {
  const userId = req.user.userId;
  // Check if course is purchased by this user or user is instructor of it
  const hasAccess = await this.courseService.checkAccess(courseId, userId);
  if (!hasAccess) throw new ForbiddenException('No access to this course');
  // Get video info
  const video = await this.videoService.getVideo(videoId);
  if (!video || video.courseId !== courseId) throw new NotFoundException();
  // Generate a signed URL to the video file or playlist
  const streamUrl = await this.fileService.getPresignedDownloadURL(video.s3Key, 60);
  return { streamUrl };
}
```

Here, `getPresignedDownloadURL` would generate a URL to GET the object (different from upload):

```typescript
async getPresignedDownloadURL(key: string, expiresInSeconds: number): Promise<string> {
  const params = { Bucket: this.bucket, Key: key, Expires: expiresInSeconds };
  return s3.getSignedUrlPromise('getObject', params);
}
```

Set a short expiry (maybe a few minutes) so that the URL cannot be reused long-term or shared widely.

The frontend can call this endpoint when the user opens a course player page, get the `streamUrl`, and then feed that to the video player.

### 4.2 Building a Custom Video Player (React Player or Video.js)

On the frontend, we need a video player component to actually play the course videos. There are two popular approaches:

- **React Player**: A React component that supports many URL types (YouTube, Vimeo, as well as HLS if you include the right file). It's easy to use but less customizable than Video.js for some needs.
- **Video.js**: A robust JavaScript video player library that can be integrated into React (either via a React wrapper or manually). It has plugins for HLS (although modern Video.js supports HLS by default via `videojs-http-streaming`).

Let's use **Video.js** for example, as it has good HLS support and UI controls.

**Setup Video.js:**  
Install video.js and any needed plugins:

```bash
npm install video.js
```

For HLS, Video.js 7+ has HLS support built-in via M3U8 handling. (On platforms where HLS is not natively supported, video.js will use its tech to play it.)

**Create a VideoPlayer component:**

```jsx
import React, { useEffect, useRef } from "react";
import videojs from "video.js";
import "video.js/dist/video-js.css";

function VideoPlayer({ srcUrl }) {
  const videoNode = useRef(null);
  const playerRef = useRef(null);

  useEffect(() => {
    if (videoNode.current) {
      // initialize Video.js player
      playerRef.current = videojs(videoNode.current, {
        controls: true,
        preload: "auto",
        autoplay: false,
        responsive: true,
        fluid: true, // make it responsive
        sources: [
          {
            src: srcUrl,
            type: srcUrl.endsWith(".m3u8")
              ? "application/x-mpegURL"
              : "video/mp4",
          },
        ],
      });
    }
    return () => {
      // cleanup on unmount
      if (playerRef.current) {
        playerRef.current.dispose();
      }
    };
  }, [srcUrl]);

  return (
    <div className="video-container">
      <video
        ref={videoNode}
        className="video-js vjs-default-skin vjs-big-play-centered"
      />
    </div>
  );
}

export default VideoPlayer;
```

This component takes a `srcUrl` which can be an HLS playlist or an MP4 file. We detect `.m3u8` to set the MIME type for HLS. Video.js will handle adaptive streaming and quality switching.

**Using the VideoPlayer:**  
In a CoursePlayer page (React), you might:

```jsx
const CoursePlayer = ({ courseId }) => {
  const [videoUrl, setVideoUrl] = useState(null);
  const [videos, setVideos] = useState([]); // list of lectures
  const [currentVideo, setCurrentVideo] = useState(null);

  useEffect(() => {
    // fetch course details including video list
    axios.get(`/courses/${courseId}`).then((res) => {
      setVideos(res.data.videos);
      setCurrentVideo(res.data.videos[0]); // play first video by default
    });
  }, [courseId]);

  useEffect(() => {
    if (currentVideo) {
      // get a streamable URL for this video
      axios
        .get(`/courses/${courseId}/videos/${currentVideo.id}/stream-url`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          setVideoUrl(res.data.streamUrl);
        });
    }
  }, [currentVideo]);

  return (
    <div>
      <h2>{/* Course title */}</h2>
      {/* maybe a list of lecture titles to click and setCurrentVideo */}
      {videoUrl && <VideoPlayer srcUrl={videoUrl} />}
    </div>
  );
};
```

This structure shows how we'd retrieve a secure URL for the video just in time for playback. The URL might expire in a minute, but once the player has loaded the playlist/segments, it's fine (for continuous playback, ensure expiration is not too short, or generate for each segment via CloudFront signed cookies – advanced topic).

**Alternate Player: ReactPlayer**  
ReactPlayer (npm package `react-player`) can play HLS if you include `import 'react-player'` and provide the .m3u8 URL. The usage is:

```jsx
<ReactPlayer url={videoUrl} controls playing={false} />
```

It will automatically use the appropriate player. However, to ensure HLS works across browsers, sometimes including `hls.js` library or using Video.js is preferred.

**Playback Controls and UI:**  
Video.js provides a default skin with play/pause, timeline, volume, fullscreen, etc. We might want to list video lectures on the side, show the course title, etc., to mimic the Udemy classroom experience.

**Quality and Streaming:**  
If using HLS with multiple renditions, Video.js will automatically allow quality switching (either manually in settings if you include a quality selector plugin, or automatically adapt). There are plugins like `videojs-http-source-selector` or similar to allow user to pick quality.

### 4.3 Secure Video Streaming (Signed URLs, DRM)

Preventing piracy and unauthorized sharing of content is important for a paid course platform. Several measures can be implemented:

**1. Signed URLs (Short Expiry):** We already touched on this. By generating pre-signed URLs for video files when a student requests them, we ensure:

- The URL is tied to our credentials and expires quickly.
- Even if someone shares that URL, it will soon become invalid, reducing risk of mass sharing.

AWS S3 pre-signed URLs and CloudFront signed URLs are common methods. We used S3 pre-signed for simplicity. In production, a better way is to use **CloudFront** (CDN) with signed cookies or signed URLs for video content:

- CloudFront can serve content from the S3 bucket.
- You set CloudFront to require signed requests (with a key pair).
- Your backend generates a signed URL or cookie for authorized users.
- The video player then can fetch all segments via that CloudFront URL as long as the cookie or URL is valid.

This offloads the traffic to CloudFront (which is global CDN) and not directly to S3. For our guide, using S3 URLs is sufficient to convey the idea.

**2. DRM (Digital Rights Management):** DRM provides a higher level of protection by encrypting video content and requiring license servers to decrypt. Examples: Widevine, PlayReady, FairPlay. Implementing DRM is complex:

- The video must be encrypted (either during transcoding or at rest).
- License server infrastructure must be in place to give decryption keys to authorized clients.
- The player must support DRM (e.g., using an HTML5 Encrypted Media Extensions (EME) via a library or certain video players).

Services like AWS MediaPackage or a platform like Mux can handle DRM for you. Given the complexity, many e-learning startups start with signed URLs and move to DRM if piracy becomes a huge issue.

For our advanced guide, we'll mention DRM but focus on achievable measures:

- **Token-based authorization**: The signed URL approach is a form of this.
- We could also implement a simple **watermarking** approach, like overlaying the user's email on the video via the player (to discourage screen recording sharing). But that's more of a deterrent than prevention.

**Example: Cloudinary or Mux**: Using these services, they provide their own URL-based protections or domain whitelisting.

In summary, **signed URLs for each video request** are our primary anti-piracy mechanism in this implementation. It ensures only users who have access can get a valid link to the content ([Integrate AWS S3 with NestJS for private and public files storage | Adarsha Acharya](https://www.adarsha.dev/blog/aws-s3-nestjs#:~:text=,will%20no%20longer%20be%20valid)). This, combined with the need to log in, is usually sufficient at early stages. For full DRM, one would integrate a service or use browser DRM APIs.

**Backend Checkpoints for Security:** Always verify:

- The user requesting the video has indeed purchased or has access.
- Use short expiry for URLs (and maybe tie them to user IP if possible, though S3's signed URL can't easily lock to IP without CloudFront).
- Log access if needed (so you can monitor unusual patterns).

Now that we have content creation and streaming in place, let's integrate payments so students can purchase courses.

---

## Payment Integration

Monetizing courses requires a payment system. We will integrate **Stripe** for handling payments (credit/debit cards, etc.), as Stripe is a developer-friendly, popular solution. We’ll also briefly mention PayPal integration as an alternative. Key aspects include:

- Accepting one-time payments for courses.
- (Optionally) handling subscriptions (if we had recurring membership or subscription plans).
- Handling refunds.
- Ensuring secure payment processing (we should never store raw card info on our server; use Stripe’s tokens or checkout).

### 5.1 Integrating Stripe

**Why Stripe?** Stripe provides an API to create payment sessions and securely handle card data. We can use Stripe Checkout (a pre-built page) or Stripe Elements (to build custom form). For a smooth start, Stripe Checkout or Payment Links allow offloading most complexity to Stripe.

However, to integrate with our system (like knowing which user bought which course), we'll likely use Stripe's API for one-time payments:

- Create a **PaymentIntent** or **Checkout Session** for a course purchase.
- Redirect the user to Stripe's hosted payment page or collect card details in the app and confirm the payment via API.
- Upon success, Stripe will notify us via **webhooks** or the return of the session, so we can fulfill the purchase (grant course access).

**Backend Setup for Stripe:**

1. Install Stripe SDK for Node: `npm install stripe`.
2. Configure Stripe secret key in an environment variable (STRIPE_SECRET_KEY).
3. Create a Stripe module/service in Nest to interact with Stripe APIs.

**Creating a Checkout Session (Server-side):**  
We can create an endpoint like `POST /purchase` where the frontend sends which course is being bought, and then we create a Stripe Checkout Session:

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, { apiVersion: '2022-11-15' });

@Post('purchase')
@UseGuards(AuthGuard('jwt'))
async purchaseCourse(@Body() body: { courseId: number }, @Req() req) {
  const course = await this.courseService.findById(body.courseId);
  if (!course) throw new NotFoundException('Course not found');
  if (course.price <= 0) {
    throw new BadRequestException('Course is free or invalid price');
  }
  const user = req.user;
  // Create a Stripe Checkout Session
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    customer_email: user.email,  // so Stripe can prefill or associate
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: {
          name: course.title,
          description: `Course by ${course.instructor.name}`
        },
        unit_amount: Math.round(course.price * 100), // Stripe expects cents
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: `${FRONTEND_URL}/payment-success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${FRONTEND_URL}/course/${course.id}`,
    metadata: {
      courseId: course.id,
      userId: user.userId
    }
  });
  return { checkoutUrl: session.url };
}
```

This uses Stripe's hosted checkout. The `success_url` is where Stripe will redirect after payment, and we include the session ID in the URL for verification. We also store metadata (courseId, userId) in the session for later reference.

**Frontend flow (Stripe Checkout):**

- User clicks "Buy Course".
- We call `POST /purchase` with courseId, get back `checkoutUrl`.
- We redirect `window.location = checkoutUrl`.
- The user completes payment on Stripe's site, then is redirected to our success page.

**Handling the success redirect:**  
On the success page (e.g., `/payment-success` route in React), we can grab the `session_id` from URL and call our backend to verify:

```typescript
@Get('payment/verify')
async verifyPayment(@Query('sessionId') sessionId: string) {
  const session = await stripe.checkout.sessions.retrieve(sessionId);
  if (session.payment_status === 'paid') {
    // Mark enrollment in DB
    const courseId = session.metadata.courseId;
    const userId = session.metadata.userId;
    await this.courseService.enrollStudent(courseId, +userId);
    return { status: 'success' };
  } else {
    return { status: 'pending' };
  }
}
```

Alternatively, use **Stripe Webhooks**: Stripe can send an HTTP POST to an endpoint on our server when events occur (like `checkout.session.completed`). This is more reliable for server-side processing:

- Expose an endpoint `/webhook` that Stripe calls.
- Verify the signature (Stripe signs webhook requests).
- On receiving a `checkout.session.completed` or `payment_intent.succeeded` event, look up the session or intent, get metadata, and fulfill the order (enroll the student in the course).

Using webhooks means even if the user closes the window at an odd time, our server still gets notified and can grant access.

Stripe's docs outline that process, and it's recommended for production to use webhooks for guaranteed fulfillment.

**Enrolling Student (granting access):**  
When payment is confirmed:

```typescript
async enrollStudent(courseId: number, userId: number) {
  // e.g., create an Enrollment record
  const enrollment = this.enrollmentRepo.create({ course: { id: courseId }, student: { id: userId } });
  await this.enrollmentRepo.save(enrollment);
}
```

If using Mongo, similar but with a relational logic replaced by storing courseId and userId in a collection.

Later, when a student tries to access a course video or content, we'll check this enrollment exists to authorize.

**Stripe Subscriptions:** The question mentions subscription models. If we wanted, we could create subscription products in Stripe (like monthly membership to access all courses, or subscription to a course’s new content). That involves:

- Using `mode: 'subscription'` in the checkout session and specifying a price ID for a recurring plan in Stripe.
- Handling webhook events like `invoice.payment_succeeded` to grant ongoing access.

For simplicity, our model is one-time purchase per course (like Udemy’s model). Subscription (like "Netflix style access to all courses for $X/month") can be an extension.

**Testing Stripe Integration:** Use Stripe test mode (the default with your test API keys). Stripe provides test card numbers (e.g., 4242 4242 4242 4242) to simulate successful payment. Test various scenarios:

- Successful payment (should grant access).
- Failed payment (user should not get access).
- Canceled checkout (no changes).

**Security:** We do not expose our Stripe secret to frontend. All creation of sessions is on backend. The frontend only gets a redirect URL or uses Stripe.js with a client secret in more custom flows. This protects against misuse. Also, using Stripe means we are not storing any card info on our servers, reducing PCI compliance scope.

### 5.2 Integrating PayPal (Alternative)

If we want to offer PayPal as a payment option, we would integrate PayPal's API similarly:

- PayPal has an SDK for creating an order and capturing it.
- We could have an endpoint that creates a PayPal order (with course info and price).
- The frontend can redirect the user to PayPal or use the PayPal buttons SDK to handle it.
- On approval, PayPal calls our success callback or we query PayPal to capture the payment.
- Then mark enrollment as done.

PayPal integration is a bit different (and their sandbox/testing is separate). Given time, one might choose one system to implement first (Stripe tends to be easier for card payments). Many platforms eventually support both (some users prefer PayPal).

For this guide, it's fine to rely on Stripe. Just note that adding PayPal would involve:

- Creating a PayPal developer app to get client ID and secret.
- Using their checkout or smart payment buttons on frontend.
- An endpoint to capture the order.

### 5.3 Handling Purchases, Refunds, and Subscriptions

We covered purchases. Let's talk about **refunds** and **subscriptions** a bit more.

**Refunds:**

- With Stripe, you (as the platform owner) can initiate refunds via Stripe Dashboard or API. If you want to allow users to refund themselves (maybe a 30-day refund policy), you could create an endpoint that calls Stripe's refund API:
  ```typescript
  await stripe.refunds.create({ payment_intent: <id> });
  ```
- You would need to store the Payment Intent or Charge ID associated with a purchase to refund it. Stripe's webhook events or storing `session.payment_intent` from Checkout can give you that.
- Also mark in your DB that the enrollment is revoked if refunded.

For simplicity, we might handle refunds manually or not include in first version. But advanced users might script automated refunds triggered by support requests.

**Subscriptions:**

- If implementing a subscription model (for example, a subscription that grants access to all courses, or a subscription for a series of content), you'd use Stripe's Subscription APIs.
- Create Products and Prices in Stripe (monthly, yearly).
- The user subscribes via a Checkout or portal, and Stripe handles recurring charges.
- Webhook events inform you of new subscription, cancellation, failed payments, etc.
- Your system would have to mark the user as having an active subscription and allow access accordingly (maybe skip individual purchases if subscription active).

This is a bigger design decision: subscription vs one-time purchase. Udemy primarily does one-time purchases per course, which is what we implemented. Subscription models (like Coursera Plus or Udemy’s personal plan) require different logic but can be layered on (maybe an `isSubscriber` flag on user).

**Admin Fees and Payouts:** Not requested, but in a real platform, you might only pay instructors a portion of revenue. That would involve tracking payments and calculating payouts. Stripe Connect could be used to pay instructors directly (Stripe can split payments or send payouts). That is outside our scope but worth noting.

**Testing Payment End-to-End:**

- Use test mode to simulate a user buying a course. After success, ensure the user can now access the course videos (the enrollment check passes).
- Try to access without buying – should be forbidden.
- Test multiple courses, ensure each purchase grants access to that specific course.

Now that payments are integrated, students can purchase courses and get access. Next, we implement the review and rating system for feedback and quality signals.

---

## Reviews & Ratings

A review system allows students to rate courses and leave feedback, which helps others decide on courses and gives instructors feedback. We will implement a basic reviews and ratings feature:

- Students can leave a rating (e.g., 1 to 5 stars) and a comment on a course they have purchased.
- We will calculate an average rating for each course.
- Include moderation tools to manage inappropriate content (likely by an admin user or simple filters).

### 6.1 Implementing a Review System

**Data Model:**

- **Review** entity: fields like `id, courseId, studentId, rating (number 1-5), comment (text), createdAt`.
- Composite index on (courseId, studentId) to ensure one review per course per student (perhaps).
- We might allow updating a review or just one-time submission.

**Submit Review API:**
We need an endpoint for a student to submit a review after taking a course:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Student)
@Post('/courses/:id/reviews')
async submitReview(@Param('id') courseId: number, @Req() req, @Body() dto: CreateReviewDto) {
  const userId = req.user.userId;
  // Verify user purchased this course
  const enrolled = await this.courseService.isEnrolled(courseId, userId);
  if (!enrolled) throw new ForbiddenException('You must purchase the course to review it');
  // Create review
  return this.reviewService.createReview(userId, courseId, dto);
}
```

`CreateReviewDto` would have `rating` and `comment`. Use class-validator to constrain rating between 1 and 5, comment length, etc.

**ReviewService.createReview:**

```typescript
async createReview(userId: number, courseId: number, dto: CreateReviewDto) {
  // If we want to prevent multiple reviews, check if exists:
  const existing = await this.reviewRepo.findOne({ where: { course: {id: courseId}, student: { id: userId } } });
  if (existing) {
    // Optionally allow update:
    existing.rating = dto.rating;
    existing.comment = dto.comment;
    return this.reviewRepo.save(existing);
  }
  // Otherwise create new
  const review = this.reviewRepo.create({
    rating: dto.rating,
    comment: dto.comment,
    course: { id: courseId },
    student: { id: userId }
  });
  return this.reviewRepo.save(review);
}
```

If using Mongoose, similar logic with `ReviewModel`.

**Average Rating Calculation:**
When a new review is added, update the course's average rating and review count. Two ways:

- Compute on the fly when needed (each time you show course details, aggregate reviews).
- Store in Course entity fields `rating` and `ratingCount`, update them whenever a review changes.

For simplicity, update and compute when a review is created or updated:

```typescript
async updateCourseRating(courseId: number) {
  const reviews = await this.reviewRepo.find({ where: { course: {id: courseId} } });
  const avg = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length;
  const course = await this.courseRepo.findOne(courseId);
  course.rating = avg;
  course.ratingCount = reviews.length;
  await this.courseRepo.save(course);
}
```

Call `updateCourseRating` at the end of createReview. In SQL, this could be done with a single query using AVG and COUNT.

**Displaying Reviews:**

- `GET /courses/:id/reviews` to list reviews for a course (with maybe pagination if many).
- Or include a few recent reviews in the course details response.

E.g.:

```typescript
@Get('/courses/:id/reviews')
async listReviews(@Param('id') courseId: number, @Query('page') page: number = 1) {
  return this.reviewService.findByCourse(courseId, { page });
}
```

The service might use repository to find with skip/take for pagination.

On the React side, show average rating (stars) on course tile and detail page. Show a list of reviews with user name, rating, comment, date. Possibly allow sorting (most recent, highest, etc.).

**Permissions:**

- Only students who bought the course can post a review (we enforced that).
- A student can edit their review (we allowed update).
- A student should not review a course they haven't bought.
- An instructor should not review their own course (we may check and prevent that if needed).
- If a user gets a refund, you might want to remove their review or at least mark it (this depends on policy).

### 6.2 Moderation and Content Management

User-generated content like reviews can include inappropriate language or spam. We should have some moderation strategy:

- **Automated filters:** We can integrate a library or simple keyword filter to reject or flag reviews containing profanity or hate speech.
- **Manual moderation:** An admin interface where admin users can view all reviews and remove ones that violate guidelines.

**Basic approach:** Add a `flagged` or `approved` field to Review.

- New reviews could default to `approved = false` and require manual approval (this might deter user engagement due to delay).
- Or `approved = true` by default, but allow reporting.

For now, let's say admin can remove a review:

```typescript
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.Admin)
@Delete('/reviews/:id')
async deleteReview(@Param('id') reviewId: number) {
  await this.reviewService.delete(reviewId);
  return { message: 'Review deleted' };
}
```

The service would remove and then update course rating counts.

**Reporting Mechanism:** We could allow users to "report" a review. That's more UI and tracking. Given the advanced scope, let's assume an admin just monitors.

**Displaying Reviews Safely:** Use proper escaping on frontend (React does by default) to avoid XSS if someone put script in a review. Possibly use a library to strip HTML from comments if you allow some formatting.

**Instructor responses:** Sometimes instructors respond to reviews. That could be another model (comments on reviews), but we’ll skip as it’s extra.

**Star Rating UI:** On frontend, you might use a star component for user to select rating, and a textarea for comment. When displaying, show stars filled for rating, etc.

**Verification:** If anonymity is a concern, you could show reviewer's name partially (like "John D." if privacy needed). But in courses, usually full name or username is fine.

**Summary:** The reviews system encourages quality and helps rating courses. We implemented:

- Posting a review (with access control).
- Calculating average ratings.
- Possibly an admin deletion for moderation.

Next, let's ensure the app performs well by exploring performance optimizations.

---

## Performance Optimization

Performance is key for a good user experience and scalability. We will address caching, front-end optimizations like lazy loading, and database optimizations.

### 7.1 Caching Strategies with Redis and CDN

**Server-side Caching (NestJS with Redis):**  
To improve response times for data that doesn't change frequently (e.g., course catalog, course details, etc.), we can introduce caching.

NestJS has a built-in cache module (`@nestjs/cache-manager`). By default it caches in-memory, but we can configure it to use **Redis** for distributed caching (so that multiple instances of our server share the same cache).

**Enabling CacheModule (Simple):**

```typescript
import { CacheModule } from '@nestjs/cache-manager';
@Module({
  imports: [
    CacheModule.register({
      ttl: 5, // seconds by default (set globally)
      max: 100, // maximum number of items in cache (for in-memory store)
    }),
    // ... other imports
  ],
})
```

This sets up a basic cache. We can then use `@UseInterceptors(CacheInterceptor)` on controllers or methods to cache their responses automatically. By default, the cache key is based on the request URL.

Example:

```typescript
import { CacheInterceptor, CacheTTL, CacheKey, UseInterceptors } from '@nestjs/common';

@UseInterceptors(CacheInterceptor)
@Get('/courses')
@CacheKey('all_courses')
@CacheTTL(60)
async listCourses() {
  return this.courseService.findAllPublished();
}
```

This will cache the result of `listCourses` for 60 seconds under the key 'all_courses'. Subsequent requests within that time return the cached result.

**Using Redis as Cache Store:**  
To use Redis, first install a Redis client adapter for cache-manager. NestJS docs suggest `@keyv/redis`.

```bash
npm install @keyv/redis
```

Then:

```typescript
import { createKeyv } from '@keyv/redis';
@Module({
  imports: [
    CacheModule.registerAsync({
      useFactory: () => ({
        store: createKeyv('redis://localhost:6379'), // your Redis URL
        ttl: 60,
      }),
    }),
    // ...
  ],
})
```

Now, the cache is stored in Redis. This means if you run multiple server instances (behind a load balancer), they share the cache.

Be mindful of cache invalidation: if data changes (like a new course added), you should clear relevant cache keys. The `cache-manager` provides methods to access the cache in services if needed (via `CacheService` injection).

**CDN for Static Assets:**  
All static assets (images, maybe the React build if not using a specialized host, videos) should be served via a CDN for faster global delivery:

- If using Vercel/Netlify, they handle CDN for your static front-end assets.
- For videos, as discussed, consider CloudFront or Cloudflare. This offloads traffic from your server.

**CDN for API responses:** Not typical to CDN-cache API JSON, because it's dynamic and requires auth. But some public, unauthenticated endpoints (like a public list of courses) could be cached at CDN level (with appropriate headers, like setting Cache-Control). Not needed if we have server-side caching + fast server response.

**Client-side Caching:**  
We can use browser caching for static resources (set long cache headers on images, scripts, etc., which build tools often do by fingerprinting filenames). This way returning visitors load faster.

**Cache Invalidation Strategy:**

- **Time-based (TTL):** As above, set a TTL. This is simple but stale data might be served. Acceptable for things like course list (if a new course is published it might appear 1 minute later).
- **On-demand:** When data changes, purge the cache. For example, after a new review is added, we could purge the cache for course details or recalc rating. With `cache-manager`, you can do `cacheManager.del('cache_key')`. If using CloudFront, you can call an API to invalidate cache paths.

**Redis for other performance aspects:**  
We could also use Redis for:

- Session store (if we used sessions instead of JWT).
- Rate limiting (though NestJS throttle by default uses an in-memory or in-process store, which can also use Redis for distributed rate limiting if needed).
- Task queues or job scheduling (beyond scope here, but for video processing or sending emails in background, etc).

### 7.2 Frontend Performance: Lazy Loading and Code Splitting

As our React app grows with many pages (Home, Course list, Course detail, Player, Profile, Admin dashboard, etc.), we should apply code splitting so that users don't have to download a huge JS bundle for the entire app on first load.

**Code Splitting with React.lazy:**  
React provides `React.lazy()` and `<Suspense>` to split code at component level. Also, if using a routing library (react-router), we can lazy load routes.

Example using React Router:

```jsx
// Instead of importing all pages at top:
const CoursePage = React.lazy(() => import('./pages/CoursePage'));
const HomePage = React.lazy(() => import('./pages/HomePage'));
...
<Routes>
  <Route path="/" element={
    <Suspense fallback={<div>Loading...</div>}>
      <HomePage />
    </Suspense>
  } />
  <Route path="/course/:id" element={
    <Suspense fallback={<div>Loading...</div>}>
      <CoursePage />
    </Suspense>
  } />
  ...
</Routes>
```

This ensures that `CoursePage` code is loaded only when that route is accessed. The fallback shows while loading.

This dramatically reduces initial bundle size – the user downloads only what's needed for the first screen, improving load time. It’s proven to improve performance by avoiding loading code the user may never need upfront.

**Lazy loading components:**  
Within a page, if there's a heavy component that isn't visible immediately, you can lazy load that too. For example, the video player component might only load when user enters the course player page, etc.

**Bundle Analysis:** Use tools like webpack-bundle-analyzer to see what's in your bundle. Ensure large libraries (video.js, for instance) are only included when needed.

**Performance for video content:**  
We covered adaptive streaming. Additionally, use preview thumbnails or low-quality previews for videos if listing many videos (but in courses, we usually only play one at a time in detail page, so it's fine).

**UI Performance:**

- Use React dev tools to identify unnecessary re-renders.
- Use memoization (`React.memo`, `useMemo`, `useCallback`) for expensive calculations or components to avoid re-render.
- Virtualize long lists (if you had thousands of courses or reviews, use a library like react-window to only render visible items).
- Use throttle/debounce on search inputs or any frequent events.

**Use a CDN for front-end assets:**  
We already said static assets (like images, maybe video thumbnails) can be on S3/CloudFront or a service. React build files if deployed on Vercel/Netlify are handled for you.

**HTTP caching on frontend:**  
Set caching headers for API responses that can be cached. E.g., the list of courses (could be cached for 1 minute on client by sending `Cache-Control: max-age=60`). But since our client is likely single-page app using fetch, the caching would need us to implement or rely on HTTP cache. Often, caching at client for API isn't done heavily (some use SWR or react-query for caching in memory between page navigations).

**Use of service workers:**  
We could use a service worker for offline support or caching. Possibly out-of-scope, but a PWA approach can cache content so the app loads even offline (at least the pages the user visited).

### 7.3 Database Indexing and Query Optimization

A poorly optimized database can slow the app as it scales. Key points:

- **Indexes:** Ensure common query fields are indexed.

  - For Postgres/TypeORM: define indexes either via `@Index()` decorator on entity fields or direct SQL. E.g., index on `Course.published` (for listing published courses), `Course.title` if searching by title (maybe use full-text search for search).
  - Index on foreign keys: `Video.courseId`, `Enrollment.courseId`, `Enrollment.studentId`, `Review.courseId` etc. Most ORMs will automatically index foreign keys, but check.
  - For sorting queries by date or name, ensure those columns are indexed if large data.
  - Multi-column index if needed (like an index on (courseId, studentId) for enrollment to quickly check if a user is enrolled in a course).

- **Query patterns:**

  - Use query builders or repository methods that allow you to select only needed columns (to reduce data transfer).
  - Avoid N+1 query problems: e.g., if fetching courses with instructor info, use `.join()` or proper ORM relations to fetch in one query instead of looping.
  - For analytical queries (like top courses by sales), consider caching or maintaining summary tables rather than heavy runtime aggregation.

- **Pagination:** Always paginate queries that can return lots of rows. For example, if we had 10,000 courses, don't fetch all at once for a list page. Use `LIMIT 20 OFFSET ...` or keyset pagination for better performance.

- **Use ORM features:** TypeORM and others allow using caching at query level too (`find({ cache: true })` etc.), but since we integrated a cache system, that might suffice.

- **Monitoring DB performance:** Enable logging of slow queries and analyze them. Add indexes as needed.

- **NoSQL considerations:** If using MongoDB:
  - Create indexes on fields used in queries (like `Course.published`, `Review.courseId`, etc.) using `@Index()` decorator in schema or via code on startup.
  - Be mindful of $lookup (joins in Mongo) as they can be heavy; often better to embed some data or handle join logic in app if needed. But in our design, relations like course->videos we can fetch via separate queries rather than join in DB.
  - Use Mongo's aggregation framework for computing averages (like average rating) if needed, or do in app for smaller scale.

**Redis caching for DB queries:** We discussed using Redis with NestJS caching which can reduce load on DB by serving from cache for repeated queries.

**CDN for database content?** Not applicable directly. But if we expose some data as static JSON (not likely here), CDN could cache it. More relevant for static sites.

**Load testing:** As an advanced user, you might simulate load (using tools like JMeter or k6) to see how the application holds up with many concurrent users, and profile slow spots.

**Scale database:** If expecting high traffic:

- For Postgres: consider read replicas for heavy read load, and direct read queries to replicas.
- For Mongo: scale via sharding if needed (overkill for our case unless millions of docs).
- Consider using a managed DB service to not worry about config.

Now that performance is handled, let's ensure security best practices are followed end-to-end.

---

## Security Best Practices

Security must be considered at every layer, especially when dealing with user data and payments. We will outline measures to protect against common vulnerabilities like XSS, CSRF, SQL injection, and ensure our APIs are secured.

### 8.1 Protecting Against XSS and CSRF

**Cross-Site Scripting (XSS):**  
XSS occurs when malicious scripts are injected into webpages, potentially stealing user data or performing actions on behalf of the user. In our app:

- **Stored XSS**: e.g., a user could try to insert `<script>` tags in a review or course description.
- **Reflected XSS**: maybe via query parameters if not handled.

**Mitigation in React:** React by default escapes content in JSX. So if a review comment contains `<script>`, when we render `{comment}` in React, it will not execute, it will display as text. This is a big safety feature. Only if we use `dangerouslySetInnerHTML` would we expose ourselves—so avoid using that with unsanitized data.

**Sanitizing User Input:** For fields like course descriptions, if instructors can include HTML content (say for rich text), we should sanitize it on server side to remove script tags or dangerous attributes. Libraries like DOMPurify (for browser or node) can do this.

**Content Security Policy (CSP):** Setting a CSP header can mitigate certain XSS by restricting what domains scripts can load from, etc. If using NestJS with Helmet, it can help set some CSP headers ([Helmet | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/helmet#:~:text=Helmet)).

**XSS in Backend (Templates):** Not directly relevant since our backend returns JSON, not HTML. If we were rendering templates, we'd use a templating engine that escapes by default.

**Cross-Site Request Forgery (CSRF):**  
CSRF is when an attacker tricks a logged-in user's browser to make a request (like form submission) to our site, using their credentials (cookies). Since we're using JWT in Authorization header and not cookies for auth, CSRF risk is lower (CSRF mainly targets cookie-based auth because browser auto-sends cookies).

However, if we did store JWT in an HttpOnly cookie (some apps do for convenience), then we would need CSRF protection tokens.

In our architecture:

- We use localStorage for JWT, and we manually attach it to requests. An attacker page cannot read our localStorage (due to same-origin policy) and cannot directly trigger our API with Authorization header without our JS (unless XSS, which is separate).
- So CSRF is mostly mitigated by using token in header instead of cookie.

If we had any state-changing endpoints accessible via GET (we don't; we use proper verbs), or if we accept cookies for auth, we should implement a CSRF token system (e.g., Nest has no built-in but can use `csurf` package with express).

**Other headers via Helmet:** Helmet sets various headers:

- X-XSS-Protection (though modern browsers ignore it).
- X-Content-Type-Options: `nosniff` (prevents MIME type sniffing).
- X-Frame-Options: `DENY` or `SAMEORIGIN` (prevents clickjacking by disallowing iframes embedding your site).
- etc.

We should enable helmet in main.ts:

```typescript
import helmet from "helmet";
app.use(helmet());
```

This will apply a broad set of protections ([Helmet | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/helmet#:~:text=Helmet)).

### 8.2 Securing API Endpoints (Auth Middleware & Guards)

We have already placed JWT guards on sensitive endpoints. To recap and add:

- All state-changing or sensitive reads should require authentication (and appropriate role). E.g., creating courses, posting reviews, viewing purchased content.
- Public endpoints (course list, course detail) remain public (with caution that no private data is leaked).

**Never trust client-side auth only:** Always enforce on backend. Even if the UI hides a "Create Course" button for non-instructors, an attacker could call the API directly. But our guard will prevent action due to role check.

**Validate Inputs (to prevent SQL Injection):** Using an ORM (TypeORM / Mongoose) and parameterized queries by default protects against SQL injection (or NoSQL injection). But if you write raw SQL or queries, use parameter binding (`query("... where name = $1", [name])` rather than string concatenation).

**Use class-validator for DTOs:** This ensures inputs meet expected format and possibly prevents malicious input (like extremely long strings, or incorrect types that could cause issues). Also, it provides a consistent error response.

**Rate-limiting (Brute force protection):** Mentioned earlier, use NestJS Throttler on sensitive routes like login to prevent brute force password attempts or other abuse. For example, apply `@Throttle(5, 60)` on login route to allow max 5 attempts per minute from one IP. We can also apply globally:

```typescript
imports: [ ThrottlerModule.forRoot({ ttl: 60, limit: 100 }) ], // as example
```

This would limit each IP to 100 requests per minute on all endpoints by default. Adjust based on usage. We might skip applying globally to not hamper legitimate usage like loading many course assets, but login and similar should definitely be limited. We can also exclude static file routes.

**Authentication Middleware:** We have used Nest guards. Alternatively, one could apply a global middleware to extract JWT, but Nest guards are simpler in our case.

**Communication Security:** Ensure the app is served over HTTPS always, especially because we handle tokens and possibly user info. If deploying on platforms like Vercel/Heroku, they provide HTTPS by default. If self-hosting, get TLS certificates (Let's Encrypt, etc.).

**Secure Password Storage:** We said this but to reiterate: never store plaintext passwords. Use bcrypt (with a salt). NestJS has a bcrypt library or you can use `bcryptjs`. Usually, do `bcrypt.hash(password, 10)` for storing, and `bcrypt.compare(inputPassword, storedHash)` for verifying.

**JWT Secret Management:** Use a strong secret (random string 32+ chars) and keep it in environment variable, not in code. Rotate if needed (this is advanced; rotating JWT secrets means invalidating existing tokens unless you handle multiple).

**Expiration and Refresh:** Our JWT expires in 1h. This limits the window if stolen. For better security, implement refresh tokens with short access token life, but that adds complexity (storing refresh token in cookie etc.). At least with 1h tokens, a user might need to log in again after expiry, or we implement a refresh endpoint that reissues a token if the old one is valid and not expired by much.

**SQL Injection Specifics:** If using TypeORM repository methods, passing parameters is safe. If using QueryBuilder, use `.setParameters`. We should avoid manually concatenating any user input into queries. If we absolutely need raw queries, use parameter binding (the TypeORM docs and Nest docs on database cover this).

### 8.3 Rate Limiting and DDoS Protection

**Rate Limiting:** As above, use NestJS Throttler or a gateway/proxy (like Nginx or Cloudflare) to limit request rates. The NestJS Throttler we added is straightforward for basic protection against brute force or spam requests.

To set throttle globally:

```typescript
providers: [
  {
    provide: APP_GUARD,
    useClass: ThrottlerGuard,
  },
];
```

and config as shown. Or use `@Throttle()` on specific routes (like login, signup).

**DDoS Protection:** A determined DDoS (distributed attack) is hard to handle at application level if it saturates your network. Typically:

- Use a service like Cloudflare or AWS Shield which can absorb or mitigate DDoS. Cloudflare can act as a proxy and has DDoS protection even on free tier for many attacks.
- Ensure your server can scale (auto-scaling groups, etc.) if under load, but for large DDoS only a CDN/proxy layer helps.

**Resource Limits:** Use proper timeouts and limits on incoming requests:

- For example, set payload size limit (Nest by default might allow up to some size; if we expect video uploads, but we offloaded to S3, so our APIs shouldn't accept huge bodies).
- If enabling file upload endpoints (like if we allowed uploading images for course thumbnail), use Nest's file upload with limits on file size.

**Helmet and Other Best Practices:** We've applied Helmet for headers like HSTS (force HTTPS), frameguard (no clickjacking) etc. According to Nest docs, Helmet sets these protective headers and improves security ([Helmet | NestJS - A progressive Node.js framework](https://docs.nestjs.com/security/helmet#:~:text=Helmet)).

**Logging and Monitoring for security:** Have logs of important actions (logins, payment attempts, etc.) and monitor for suspicious activity (like many failed logins). This can be done by analyzing logs or integrating with something like Sentry or Datadog to set up alerts.

**Dependency updates:** Keep your dependencies (React, Nest, etc.) updated to get latest security fixes. Use tools like `npm audit` to catch known vulnerabilities in packages.

By applying these practices, we mitigate a wide range of security issues:

- XSS: React escaping + Helmet CSP.
- CSRF: use JWT in header or use csurf if needed for cookies.
- SQL injection: use ORM properly.
- Authentication: robust JWT handling, strong password hashing.
- Rate limiting: throttle brute force attempts.
- DDoS: external services + throttle to some extent.

Next, we'll cover deploying our application and scaling it to handle real-world traffic.

---

## Deployment & Scaling

With the application built and secured, the final steps are deploying it to a production environment and setting up continuous delivery. We'll cover deploying the React frontend and NestJS backend, different hosting options (Vercel, Netlify, AWS, Heroku, etc.), and how to set up CI/CD pipelines. We will also touch on scaling considerations, like containerization and load balancing.

### 9.1 Deploying the Frontend (Vercel, Netlify, AWS Amplify)

**Deploying React on Vercel:**  
Vercel is optimized for frontend frameworks and static sites. If your React app is a single-page app (built with CRA or Vite), it's essentially static assets after build.

- Install Vercel CLI (`npm i -g vercel`) or use their web UI.
- Ensure your project is in a git repository.
- On Vercel dashboard, create a new project, link it to your repo (GitHub/GitLab/Bitbucket).
- Vercel will auto-detect a React app and set up the build (`npm run build`) and publish the `build/` directory.
- It provides a domain (e.g., myapp.vercel.app) and you can add a custom domain.
- On each push to main (or a specified branch), it auto-deploys (CI/CD built-in).

**Deploying on Netlify:**  
Netlify is similar for static sites:

- On Netlify, create a site from Git, configure build command and publish directory.
- For CRA: build command `npm run build`, publish directory `build`.
- It also auto-deploys on new commits.
- Netlify offers forms, functions, etc., but for our use we mostly serve static files.

**AWS Amplify (Console):**  
AWS Amplify Console can connect to your repo and deploy the frontend as well:

- It sets up a pipeline triggered by git pushes.
- It's a bit more manual than Vercel/Netlify in UI, but provides similar outcomes.

All these options provide CDN backing and SSL automatically.

**Serving via S3/CloudFront:**  
Alternatively, you can build the React app and manually upload the files to an S3 bucket configured to host a static site, then front that with CloudFront for CDN. AWS Amplify essentially automates a lot of this.

**Environment Variables:**  
If your frontend needs environment variables (like API base URL), with React (CRA) those need to be embedded at build time (using `REACT_APP_` prefix or similar). With Vite, use `import.meta.env`. Vercel and Netlify allow setting env vars in settings which they inject during build.

**Domain Setup:**  
Point your domain's DNS to the provided domain (or use their nameservers). For example, with Netlify you get a `.netlify.app` domain, but you can add a custom domain and they set up DNS and certificates.

**Testing production build locally:** Always good to run `npm run build` and serve it (like using `serve -s build`) to ensure it works, before deploying.

### 9.2 Deploying the Backend (AWS, DigitalOcean, Heroku)

For NestJS backend, we have multiple routes:

- **Heroku:** Easiest for beginners, supports Node apps out of the box.
- **AWS (EC2 or ECS or Elastic Beanstalk):** More setup but powerful. Elastic Beanstalk can deploy Node apps with minimal fuss, or use a container.
- **DigitalOcean Droplet or App Platform:** Droplet means you manage a VM, App Platform is more PaaS like Heroku.

Let's outline a simpler PaaS route (Heroku) and a container route:

**Deploying NestJS to Heroku:**

1. Create a Heroku app (`heroku create app-name`).
2. Add Heroku Postgres add-on if using Postgres (Heroku gives a DATABASE_URL).
3. Set environment variables in Heroku (e.g., JWT_SECRET, Stripe keys, etc.) via `heroku config:set`.
4. Push code to Heroku: Heroku will detect Node.js and run `npm install` and `npm run build` (if `build` script exists) then `npm start`. Ensure your `package.json` has a start script like `"start": "node dist/main.js"`.
5. Heroku opens port from env var `PORT`, Nest by default uses 3000. Modify main.ts to use `process.env.PORT` if available:
   ```typescript
   const port = process.env.PORT || 3000;
   await app.listen(port);
   ```
6. After deploy, check logs `heroku logs -t` to debug if needed. Then test the API endpoints.

Heroku free tier had limitations (and recently removed free dynos), so might need a paid dyno now.

**Deploying via Docker (AWS or others):**

- Create a Dockerfile for NestJS. Example:
  ```Dockerfile
  FROM node:18-alpine
  WORKDIR /app
  COPY package*.json ./
  RUN npm install --production
  COPY . .
  RUN npm run build
  CMD ["node", "dist/main.js"]
  ```
  This builds the app inside the container.
- Build the image: `docker build -t udemy-backend .`
- Test run: `docker run -p 3000:3000 udemy-backend` to ensure it works.
- Now push this image to a registry (Docker Hub, ECR, etc.).
- AWS: You could use ECS (with Fargate) to run the container, or Elastic Beanstalk which can directly build and run container.
- DigitalOcean: Has an App Platform where you can give it a Dockerfile or just the Node app.
- Alternatively, a simpler way: use **Railway.app** or **Fly.io**, which can deploy Docker or Node apps easily with minimal config.
- If using Docker in production, consider multi-stage build to reduce image size (build on one stage, copy dist to a slim node image).

**Reverse Proxy / Nginx:** If deploying Nest on a VM or container, you might put Nginx in front to serve as reverse proxy, handle SSL (if not handled by cloud load balancer), and possibly serve the React static files. In our case, we likely host frontend separately, so backend can just be API.

**Connecting Frontend and Backend:**

- CORS: Ensure that your NestJS has CORS enabled for requests from your frontend domain. E.g., in main.ts:
  ```typescript
  app.enableCors({ origin: "https://yourfrontenddomain.com" });
  ```
  Or origin: '\*' for simplicity (but better to restrict to known domain).
- In production, the frontend will call the backend via an URL (e.g., if hosted separately, maybe an API subdomain). For local dev it was likely http://localhost:3000, but in prod maybe https://api.yoursite.com. Make sure to update the frontend config to use the correct base URL. Often using an environment variable in the build for API URL.
- If using the same domain (e.g., serving frontend and backend from same origin), that simplifies things (no CORS needed). Some deploy strategies put the frontend in an S3/CloudFront and use a subpath for API on same domain via CloudFront behaviours or Nginx. But that's advanced; easier is separate subdomains.

**Scaling Backend:**

- If using Heroku, you can scale vertically (bigger dyno) or horizontally (multiple dynos) and Heroku will load balance.
- If using AWS ECS or Kubernetes, you define tasks/pods and can scale out more instances behind a load balancer.
- Ensure statelessness: Our app is stateless (especially using JWT, not session). So scaling horizontally is fine; any instance can handle a request. If we used in-memory cache or throttler, we should ensure those use Redis so that instances share state. (We configured cache with Redis and could also configure Throttler with Redis for global rate limiting.)

**Database Scaling:** For more users, move to managed databases (Heroku Postgres, AWS RDS, etc.). They can scale and provide backups. Could also use connection pooling service if many connections (like PGbouncer).

**Logging & Monitoring in Prod:**

- Use a service like Papertrail or LogDNA to collect logs from Heroku or container logs.
- Or integrate Nest's logger to output JSON and aggregate with ELK stack (ElasticSearch, Logstash, Kibana) if self-managed.

**Scheduled Jobs / Cron:** If needed (not in scope, but e.g., send emails, cleanup) consider using Nest Schedule or separate worker service.

Now the application is deployed. Let’s automate the process with CI/CD.

### 9.3 CI/CD Pipeline Setup (GitHub Actions/GitLab CI)

Continuous Integration/Continuous Deployment (CI/CD) ensures that tests run on each commit and deployments happen automatically. We will outline a GitHub Actions pipeline as an example, which could build and test both frontend and backend, and then deploy.

**GitHub Actions Workflow:**
Create a file `.github/workflows/main.yml` in your repo:

```yaml
name: CI CD Pipeline

on:
  push:
    branches: [main] # adjust to your main branch

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        include:
          - part: frontend
          - part: backend

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm install
        # If monorepo, this installs both, maybe use separate if needed

      - name: Build ${{ matrix.part }}
        run: |
          if [ "${{ matrix.part }}" == "frontend" ]; then
            npm run build --prefix frontend  # assuming frontend folder
          else
            npm run build --prefix backend
          fi

      - name: Run tests
        run: |
          if [ "${{ matrix.part }}" == "frontend" ]; then
            npm test --prefix frontend -- --watchAll=false
          else
            npm run test --prefix backend -- --watchAll=false
          fi

      - name: Deploy Backend (Heroku)
        if: matrix.part == 'backend'
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "your-heroku-app-name"
          heroku_email: "your-heroku-email"

      - name: Deploy Frontend (Netlify)
        if: matrix.part == 'frontend'
        uses: nwtgck/actions-netlify@v1.2.3
        with:
          publish-dir: frontend/build
          production: true
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

This example uses a matrix to do frontend and backend in parallel. It installs, builds, tests both. Then uses:

- A Heroku deploy action (needs API key secret) to deploy backend.
- A Netlify deploy action (needs site ID and auth token) for frontend.

Alternatively, if using Vercel, you might skip deploying via actions and rely on Vercel's git integration which auto-deploys.

If using Docker and AWS, the steps would differ:

- Build Docker image, push to ECR.
- Maybe use AWS CLI or ECS action to update service.

**Testing Stage vs Deploy Stage:** You might separate the workflow into jobs or have an approval step for deployment (in GitHub Actions can use environments with required approvals).

**GitLab CI/CD:** Similarly, a `.gitlab-ci.yml` can be set up with runners to do builds and use their CD features.

**CI for Pull Requests:** Usually, CI runs tests on PRs to ensure quality before merge. Deployment typically triggers only on main branch merges.

**Cypress integration:** If using Cypress for e2e, you can set up a job to spin up the app and run Cypress tests in CI as well, possibly using GitHub Actions service containers for DB or so.

**Notifications:** Setup Slack or email notifications for deploy status if needed.

The key is to automate everything: commit -> tests -> deploy. This reduces manual errors and speeds up iteration.

### 9.4 Scaling Considerations and Cloud Infrastructure

**Scaling Web Servers:**

- Horizontal scaling: run multiple instances of the NestJS backend. This might be behind a load balancer (Heroku does this automatically if you scale dynos; AWS would use an ELB).
- Ensure session state is not in-memory if any (we use JWT so it's fine).
- Use a shared cache and database which we have.

**Microservices vs Monolith:** NestJS can be split into microservices if needed (for example, a separate service for payments or video processing). But to start, a monolith is simpler. If scaling team or complexity, could break out services.

**Using Node Cluster mode:** Nest can run in cluster mode to utilize multiple CPU cores on one machine. This is another way to scale on a single VM (e.g., using PM2 or the `cluster` module). Or simply run multiple container instances.

**Serverless option:** We could deploy NestJS as serverless functions (each endpoint as a lambda via Nest's serverless support) but this is advanced and not necessary unless wanting to reduce server management.

**Scaling Database:**

- Use a larger DB instance if needed.
- Add read replicas to offload read-heavy queries (modify app to use different connection for read vs write).
- Optimize queries as discussed.

**Scaling Media Delivery:**

- Offload videos to CloudFront CDN to handle many concurrent streams.
- Possibly use HLS which is chunked and easier to distribute.
- Monitor S3/CloudFront costs; video can incur bandwidth costs.

**Background Jobs Infrastructure:**
If you need to process videos (transcoding) or send emails, consider a job queue (BullMQ with Redis, for example) and separate worker processes. For instance, uploading a video could enqueue a "transcode" job.

**Monitoring & Alerts:**

- Set up CloudWatch alarms or similar for high CPU/memory, or error rate.
- Use uptime monitoring to get alerted if API or site goes down.

**Cost Considerations:**

- Use free tiers or low-tier instances while starting. E.g., Heroku Eco dyno (low cost), free Postgres small, Cloudinary free for video up to some limits.
- As usage grows, plan costs for S3/CloudFront (video heavy).
- Optimize content (maybe limit video size/quality to what's needed, to control egress costs).

**Documentation and Maintenance:**

- Document your environment setup for new developers.
- Use Infrastructure as Code (like Terraform) if the setup gets complex (especially on AWS) to replicate environment easily.

Now, with deployment and scaling covered, one major piece remains: testing and debugging, to maintain reliability as the project grows.

---

## Testing & Debugging

Testing ensures our application works as expected and prevents regressions. Debugging techniques help diagnose issues during development and production. We will cover unit and integration tests using **Jest** (and **Supertest** for end-to-end API tests), how to set up **Cypress** for front-end end-to-end tests, and methods for debugging common problems in both NestJS and React. We'll also discuss monitoring tools like Sentry for error tracking.

### 10.1 Unit and Integration Testing with Jest

**NestJS Testing with Jest:**
NestJS comes with Jest configured out of the box for unit tests and integration (end-to-end) tests ([Testing | NestJS - A progressive Node.js framework](https://docs.nestjs.com/fundamentals/testing#:~:text=,environment%20for%20easily%20mocking%20components)). Upon generating a module or controller via CLI, Nest created a basic test file (e.g., `app.controller.spec.ts`).

**Unit Testing example (Service logic):**  
Suppose we want to test the `CourseService.createCourse` method. We can write a test that uses a mocked repository.

```typescript
import { Test, TestingModule } from "@nestjs/testing";
import { CourseService } from "./course.service";
import { getRepositoryToken } from "@nestjs/typeorm";
import { Course } from "../entities/course.entity";
import { Repository } from "typeorm";

describe("CourseService", () => {
  let service: CourseService;
  let repo: Repository<Course>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CourseService,
        {
          provide: getRepositoryToken(Course),
          useValue: {
            create: jest.fn(),
            save: jest.fn().mockResolvedValue({ id: 1, title: "Test Course" }),
          },
        },
      ],
    }).compile();

    service = module.get<CourseService>(CourseService);
    repo = module.get<Repository<Course>>(getRepositoryToken(Course));
  });

  it("should create a course", async () => {
    const dto = { title: "Test Course", description: "Desc", price: 0 };
    const userId = 42;
    // Assuming createCourse calls repo.create and repo.save
    await service.createCourse(userId, dto);
    expect(repo.create).toHaveBeenCalledWith({
      ...dto,
      instructor: { id: userId },
      published: false,
    });
    expect(repo.save).toHaveBeenCalled();
  });
});
```

This uses Nest TestingModule to provide a fake repository (we supply a useValue with jest mocks) so the service can be tested in isolation. We then verify that repository functions were called correctly.

**Integration (end-to-end) Testing NestJS:**  
Nest can instantiate the whole app with an in-memory server for e2e tests, using Supertest to simulate HTTP calls.

A typical e2e test (see `test/app.e2e-spec.ts` that Nest creates):

```typescript
import * as request from "supertest";
import { Test } from "@nestjs/testing";
import { INestApplication } from "@nestjs/common";
import { AppModule } from "../src/app.module";

describe("CourseController (e2e)", () => {
  let app: INestApplication;
  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();
    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it("/courses (GET) should return array", () => {
    return request(app.getHttpServer())
      .get("/courses")
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });

  afterAll(async () => {
    await app.close();
  });
});
```

This launches the entire AppModule (with all controllers). Typically, you might use a test database or SQLite in-memory for these tests to run without affecting dev/prod DB. You can set env like NODE_ENV=test and configure TypeORM to use sqlite in that case.

**Front-end Testing with Jest and React Testing Library:**
Create React App (and similar) often come with Jest setup and RTL (React Testing Library). Write tests for components:

```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import LoginForm from "./LoginForm";

test("calls onSubmit with email and password", () => {
  const handleSubmit = jest.fn();
  render(<LoginForm onSubmit={handleSubmit} />);
  fireEvent.change(screen.getByPlaceholderText(/email/i), {
    target: { value: "test@example.com" },
  });
  fireEvent.change(screen.getByPlaceholderText(/password/i), {
    target: { value: "secret" },
  });
  fireEvent.click(screen.getByRole("button", { name: /login/i }));
  expect(handleSubmit).toHaveBeenCalledWith({
    email: "test@example.com",
    password: "secret",
  });
});
```

This ensures the form collects input and calls the prop properly.

We should also test critical logic like:

- Authentication context (if using one).
- Utility functions.
- Possibly use MSW (Mock Service Worker) to simulate API responses in front-end tests for components that fetch data.

**Running tests in CI:** We would run `npm test -- --watchAll=false` for both front and back as shown in the CI step. All tests should pass before deployment.

### 10.2 End-to-End Testing with Cypress

While Jest + Supertest tests our API, and Jest + RTL tests our components, **Cypress** can automate a browser to test actual user flows:

- E.g., Launch the web app, fill login form, click, verify that it navigates to dashboard, etc.
- It can also call backend or use seeded database to set up scenarios.

Setting up Cypress:

1. Install: `npm install cypress --save-dev`.
2. Initialize: `npx cypress open` (to scaffold structure).
3. Write tests in `cypress/e2e` folder, e.g., `course_spec.cy.js`:
   ```js
   describe("Course purchase flow", () => {
     it("allows a user to buy a course and access it", () => {
       // Start from home page
       cy.visit("http://localhost:3000");
       // Login
       cy.get("input[name=email]").type("student@example.com");
       cy.get("input[name=password]").type("password123");
       cy.get("button").contains("Login").click();
       // After login, should show courses
       cy.contains("All Courses");
       // Click first course
       cy.get(".course-card").first().click();
       cy.contains("Buy Course").click();
       // This might redirect to Stripe; for test, maybe use a test stub if possible.
       // Alternatively, you could simulate purchase by calling an API stub or skip actual payment in test.
       // After "purchase", suppose we simulate by directly marking enrollment in DB for test.
       // Then:
       cy.contains("Start Learning").click();
       cy.url().should("include", "/learn");
       cy.contains("Video Player");
     });
   });
   ```
   This is a high-level idea; dealing with Stripe in e2e is complex (Stripe has test mode but integration in Cypress might require using their test card entry which might or might not be feasible directly due to cross-domain).
   Perhaps for testing purchase flow, it's acceptable to stub the payment step or test it in integration tests separately.

Cypress can run headlessly in CI with `cypress run`. For that, the app (frontend and backend) must be running. In CI, one approach:

- Start backend (maybe with test config) in background (e.g., `npm run start:ci`).
- Start frontend (or serve the built one) on a port.
- Then run cypress targeting those.

This can be resource-intensive, so sometimes e2e tests are run on merges, not every commit.

### 10.3 Debugging Common Issues (Frontend & Backend)

Even with tests, issues will arise. Some common issues and how to debug:

**Backend Debugging:**

- **NestJS Exceptions:** If an endpoint returns 500, check Nest logs. By default, Nest logs errors to console (with stack trace) and returns a generic 500 to client. In dev mode, enable detailed errors or use `app.useGlobalFilters(new AllExceptionsFilter())` to handle and log.
- **Source Maps:** Ensure `sourceMap: true` in tsconfig so that stack traces reference TypeScript line numbers when debugging.
- **Logging:** Use `console.log` or Nest's Logger (`this.logger.log()`) in services to trace values. In development, it's fine to sprinkle console logs or use a debugger.
- **Node Debugger:** You can run NestJS with `node --inspect-dist/main.js` or in TS directly with `ts-node --inspect`. Then attach VSCode or Chrome Node DevTools to step through code.
- **Postman/Thunder Client:** Test the API endpoints manually. Often, replicating a failing request in Postman helps inspect what's wrong (headers, data, etc.).
- **Database issues:** If queries not working, enable query logging in TypeORM (`logging: true` in config) to see the SQL in console. Or use a DB client to inspect data.

**Frontend Debugging:**

- **Browser DevTools:** Use console and network panels. If an API call fails (network 4xx or 5xx), see the response and error message from backend.
- **Console errors:** If UI isn't behaving, check console for React errors (like state update on unmounted component, etc.).
- **React DevTools Profiler:** If performance issues, see what re-renders often.
- **Breakpoints:** You can put `debugger;` in your React code or set breakpoints via browser devtools sources panel to step through.
- **CORS errors:** If you see CORS error in console, adjust the backend CORS settings or proxy correctly.
- **Build issues:** If production build doesn't work, use source maps (if generated) or add logging. Possibly differences in environment (maybe env vars not set).
- **Testing in multiple browsers:** Check if an issue is browser-specific (maybe something works in Chrome but not Safari due to HLS support, etc.).

**Synchronization issues:** E.g., video not loading: check if the token is passed, or if the signed URL expired. Maybe adjust expiry or the logic to fetch new URL if needed (we might add logic to refresh video URL every X minutes for long videos).

**Memory leaks or heavy usage in frontend:** Use the Performance tab in devtools to take heap snapshots if suspect a leak.

**Common issues:**

- Logging in but Authorization header not attached on subsequent requests -> likely forgot to attach or lost token (check how state is managed).
- JWT expiration causing 401 and user not handled -> ensure to catch 401 in frontend, redirect to login or refresh token.
- Video playback issues: maybe content type issues, check that the Content-Type header is correct (video/mp4 or application/x-mpegURL) when serving.
- Stripe webhooks not received: ensure the endpoint is accessible publicly (for local testing, use `stripe listen` proxy or similar).
- Inconsistent environment config: a bug only in prod could be due to differences (like using HTTP instead of HTTPS somewhere, or a third-party key only working on certain domain).

Logging is your friend: instrument both client and server with logs at key points and review them.

### 10.4 Monitoring and Logging (Sentry, Datadog, ELK)

Once in production, we want to know when things break (uncaught exceptions) or performance issues happen.

**Sentry (Error Tracking):**

- Sentry can capture exceptions from both frontend and backend.
- Frontend: install `@sentry/react` and initialize with your DSN. For example:
  ```js
  import * as Sentry from "@sentry/react";
  Sentry.init({
    dsn: "https://<key>.ingest.sentry.io/<project>",
    tracesSampleRate: 0.1,
  });
  ```
  This will catch JS errors and report to Sentry, with stack trace and even Redux state if configured.
- Backend: install `@sentry/node` and initialize in main.ts:
  ```typescript
  import * as Sentry from "@sentry/node";
  Sentry.init({ dsn: "https://...", tracesSampleRate: 0.1 });
  app.useGlobalFilters(new SentryFilter()); // custom filter to send exceptions to Sentry
  ```
  Or use NestJS Sentry community module for easier integration.

Sentry also can do performance tracing to see slow requests or components.

**Datadog/NewRelic (APM):** These services provide deeper metrics (like CPU, memory, response times, DB query times).

- They often require an agent or instrumentation in code.
- If high budget/need, integrate their Node APM for backend and Real User Monitoring (RUM) for front.

**ELK Stack (Elastic Log monitoring):**

- You might send all logs to ElasticSearch for analysis. For example, use Winston logger in Nest to send logs to a file or directly to ELK.
- Or use a hosted solution (Elastic Cloud, Logz.io, etc.).
- With structured logs (JSON), you can create dashboards of errors or key events.

**Uptime Monitoring:** Use Pingdom, UptimeRobot, or health checks to alert if API or site is down.

**Analytics:** For frontend usage and conversion, Google Analytics or similar can be integrated to see user behavior (e.g., funnel from visiting course to purchasing).

**Example: Logging an error to Sentry in backend:**

```typescript
try {
  // some code that throws
} catch (error) {
  this.logger.error(error.message, error.stack);
  Sentry.captureException(error);
  throw error; // rethrow after logging
}
```

Though if a global filter is set, it might catch unhandled ones.

**Alerting:** Set up Sentry alerts (email/slack) for high-severity errors (e.g., payment failures or 500 errors).

**Periodic Review:** Check your monitoring dashboards regularly, or set up weekly reports (some services email summaries of errors).

**Debugging Production Issues:**

- Reproduce locally if possible with similar data.
- If not, use logs/metrics from production to narrow down. Possibly add more logging around suspected area and redeploy temporarily to catch the issue.
- Use feature flags to turn off problematic features if needed while investigating (for advanced setups).

---

This concludes our step-by-step guide. You have now built a Udemy-like platform with robust features, optimized performance, and a scalable, secure architecture. By following these chapters, you have set up the project, implemented authentication and course management, integrated video streaming and payments, allowed reviews, optimized performance, secured the application, and prepared it for deployment and scaling. Happy coding and best of luck launching your online learning platform!
