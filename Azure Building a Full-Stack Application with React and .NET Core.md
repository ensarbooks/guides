# Building a Full-Stack Application with React and .NET Core

Full-stack development with **React** (frontend) and **.NET Core** (backend) combines a dynamic UI with a powerful API. This guide provides a step-by-step roadmap for advanced developers to build a modern full-stack application using the latest stable versions of React and .NET Core. We’ll cover environment setup, frontend and backend development best practices, containerization with Docker, CI/CD pipelines, security, deployment to Azure, configuration management, performance optimizations, monitoring, and testing. Each chapter includes practical examples and adheres to industry best practices.

## 1. Setting Up the Development Environment

A proper development environment is crucial for productivity and consistency. To develop a React + .NET Core application, ensure you have the following tools installed and configured:

1. **Node.js and npm** – Install the latest LTS version of Node.js (which includes npm) from the official website. Node is required to create and run the React app and manage its dependencies ([Complete Guide to using ASP.NET Core with React](https://www.scholarhat.com/tutorial/aspnetcorewebapi/asp-dot-net-core-react#:~:text=First%2C%20we%20need%20to%20install,the%20following%20tools)).
2. **.NET SDK** – Install the .NET SDK (Ideally .NET 6, 7, or 8) from Microsoft's website. This includes the .NET CLI and runtime needed to build and run ASP.NET Core projects ([Complete Guide to using ASP.NET Core with React](https://www.scholarhat.com/tutorial/aspnetcorewebapi/asp-dot-net-core-react#:~:text=First%2C%20we%20need%20to%20install,the%20following%20tools)). Verify installation by running `dotnet --version` in a terminal.
3. **Code Editor/IDE** – Use an editor like **Visual Studio Code** (cross-platform) or an IDE like **Visual Studio 2022** (especially if on Windows) which has dedicated support for .NET and front-end development ([Complete Guide to using ASP.NET Core with React](https://www.scholarhat.com/tutorial/aspnetcorewebapi/asp-dot-net-core-react#:~:text=First%2C%20we%20need%20to%20install,the%20following%20tools)). Make sure to install relevant extensions (C# plugin for VS Code, etc.).
4. **Database** – (Optional) If you plan to use a local database, install **SQL Server Express** or **PostgreSQL**. Alternatively, use Docker to run a database container during development.
5. **Git** – Install Git for version control. This will be useful for managing code and setting up CI/CD.

**Project Structure**: Plan a structure for your code. A common approach is to keep front-end and back-end in separate directories within one repository (e.g., `/client` for React app and `/server` for .NET API). This separation helps in managing each side independently while enabling combined workflows like Docker Compose.

**Verify Tools**: After installation, verify each tool: run `node -v` and `npm -v` to check Node/npm, and `dotnet --info` to confirm .NET SDK. Once everything is set, you can proceed to create the projects.

## 2. Creating the React Frontend

With the environment ready, start by creating the React application. We will use modern React practices like **functional components with Hooks**, **TypeScript**, and a state management solution (Context API or Redux) to build a scalable frontend.

### 2.1 Initializing the React App

Initialize a new React project. The recommended way is using a scaffold tool that sets up a React app with a proper build configuration:

- **Create React App (CRA)**: Although CRA is a traditional choice, modern tools like **Vite** are now often preferred for better performance. In fact, the latest Visual Studio templates use Vite by default ([Create an ASP.NET Core app with React - Visual Studio (Windows) | Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/javascript/tutorial-asp-net-core-with-react?view=vs-2022#:~:text=Note)). For simplicity, we'll use CRA (with TypeScript) here:

  ```bash
  npx create-react-app client --template typescript
  ```

  This creates a React project named "client" with TypeScript support. (You can also use Vite: e.g., `npm create vite@latest client -- --template react-ts` for a similar outcome.) The CRA TypeScript template provides a ready-to-run app using `.tsx` files and includes type definitions ([Create React App and TypeScript: A Quick How-To | Built In](https://builtin.com/software-engineering-perspectives/create-react-app-typescript#:~:text=You%20can%20start%20a%20new,)).

- After creation, run the app to verify setup:

  ```bash
  cd client
  npm start
  ```

  This should start the development server on http://localhost:3000.

**Project Structure**: The React app structure will have a `/src` directory containing `index.tsx`, `App.tsx`, and other files. You can organize features into components and possibly sub-folders as the app grows. For advanced apps, consider a modular structure (by feature or route).

### 2.2 Modern React Practices (Hooks and TypeScript)

**Use Functional Components & Hooks**: Modern React encourages functional components with Hooks for state and lifecycle instead of class components. Hooks let you use React features (state, context, effects, etc.) without writing classes ([Introducing Hooks – React](https://legacy.reactjs.org/docs/hooks-intro.html#:~:text=Hooks%20are%20a%20new%20addition,features%20without%20writing%20a%20class)). For example, instead of a class with `this.state`, you use `useState` hook:

```jsx
import { useState, useEffect } from "react";

function ExampleComponent() {
  const [count, setCount] = useState(0); // state hook
  useEffect(() => {
    document.title = `Clicked ${count} times`;
  }, [count]); // effect hook runs on count change

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

Hooks make code more readable and avoid the complexity of `this` context in classes. They also enable sharing logic via **custom hooks**.

**TypeScript**: Using TypeScript in React helps catch errors early and makes the code more maintainable for large codebases. The CRA template already set up TypeScript. Ensure you define proper types for component props, state, and other structures. For example:

```tsx
type User = {
  id: number;
  name: string;
};

interface GreetingProps {
  user: User;
}

const Greeting: React.FC<GreetingProps> = ({ user }) => {
  return <h1>Hello, {user.name}</h1>;
};
```

Here we define a `User` type and a component `Greeting` that expects a `user` prop of that type. TypeScript will flag misuse (like missing properties or wrong types) at compile time, improving reliability.

**State Management**: For global or complex state, decide between the Context API and Redux:

- _Context API_: Built-in and good for passing down global data (like theme, user auth info) without prop drilling. It’s lightweight and ideal for **small to medium** state needs. Using the Context API with the `useContext` hook is straightforward but be mindful of performance (excess re-renders if not optimized). For simple cases, Context is often sufficient and has less overhead than Redux ([Redux vs. Context API: Choosing the Right State Management for Your React App / Blogs / Perficient](https://blogs.perficient.com/2024/12/11/redux-vs-context-api-choosing-the-right-state-management-for-your-react-app/#:~:text=Context%20API)) ([Redux vs. Context API: Choosing the Right State Management for Your React App / Blogs / Perficient](https://blogs.perficient.com/2024/12/11/redux-vs-context-api-choosing-the-right-state-management-for-your-react-app/#:~:text=Choosing%20between%20Redux%20and%20the,API%20is%20a%20simpler%20alternative)).
- _Redux_: A popular state management library useful for **large or complex application state**. It provides a single store, strict unidirectional data flow, and powerful devtools. Redux involves more boilerplate (actions, reducers) but excels at managing state that many parts of the app need and that changes frequently ([Redux vs Context API + React Hooks - which wins in performance?](https://stackoverflow.com/questions/73669777/redux-vs-context-api-react-hooks-which-wins-in-performance#:~:text=Redux%20vs%20Context%20API%20%2B,for%20their%20own%20specific%20niche)) ([Redux vs. Context API: Choosing the Right State Management for Your React App / Blogs / Perficient](https://blogs.perficient.com/2024/12/11/redux-vs-context-api-choosing-the-right-state-management-for-your-react-app/#:~:text=Choosing%20between%20Redux%20and%20the,API%20is%20a%20simpler%20alternative)). Modern Redux with the Redux Toolkit reduces boilerplate and uses immer for immutable updates.

**Choosing**: If your app is large-scale with complex interactions or requires advanced patterns (like undo/redo, time-travel debugging), Redux is a solid choice ([Should You Still Go with Redux in 2024? Exploring Alternatives and ...](https://medium.com/@kavandev1/should-you-still-go-with-redux-in-2024-exploring-alternatives-and-comparisons-1d39af077144#:~:text=Should%20You%20Still%20Go%20with,for%20large%20and%20complex%20applications)). For simpler apps, the Context API (possibly combined with the `useReducer` hook for reducer logic) can suffice with less setup. It’s common to start with Context and migrate to Redux if state management grows complicated.

**Example – Context Usage**: Creating a context for user authentication status:

```tsx
// AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from "react";

interface AuthContextType {
  user: string | null;
  login: (name: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<string | null>(null);
  const login = (name: string) => setUser(name);
  const logout = () => setUser(null);
  const value = { user, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
```

This uses Context to provide auth state and functions. In your app, wrap your component tree with `<AuthProvider>` and use `useAuth()` in components to access `user` or call `login/logout`.

**Best Practices**: Structure your React code into reusable components. Use Hooks like `useEffect` for side-effects (data fetching, subscriptions), `useContext` for global data, and `useReducer` for complex state logic within a component or context. Leverage TypeScript interfaces/types for component props and API response shapes. Keep components focused (single responsibility) and lift state up only when needed to share it. This will keep your React app organized and maintainable.

### 2.3 Building UI and Handling Data

With the base app ready, proceed to build the actual UI components and integrate data from the backend (to be built). A few guidelines:

- **Routing**: If your app is multi-page (single-page app with multiple views), use React Router. Set up a Router in `App.tsx` and define routes for your pages.
- **UI Libraries**: Consider using component libraries or design systems (Material-UI, Bootstrap, Ant Design, etc.) to speed up UI development.
- **API Calls**: Abstract your API calls into separate modules or hooks (e.g., create a `useApi` hook or a set of functions using `fetch`/Axios) to keep components clean. Configure the base URL of your API depending on environment (for development, it might be `http://localhost:5000`, in production an Azure URL).
- **Environmental Config**: Create `.env.development` and `.env.production` files for any environment-specific variables. For example, in `.env.development`:

  ```env
  REACT_APP_API_URL=http://localhost:5000
  ```

  In production, `REACT_APP_API_URL` might point to the live API. Remember that React will embed these at build time, so _never put secrets in these .env files_, only configuration like URLs or feature flags ([React Environment Variables: How To Use Them Securely](https://onboardbase.com/blog/react-env#:~:text=Since%20React%20is%20client,because%20they%20will%20be)). Also, ensure you add `.env*` to `.gitignore` if they contain any sensitive info (API keys, etc.) ([Leveraging Environment Variables in React: A Safe & Effective Guide - DEV Community](https://dev.to/shriharimurali/leveraging-environment-variables-in-react-a-safe-effective-guide-1p4j#:~:text=Never%20Commit%20,files%20pushed%20to%20public%20repositories)).

- **Testing (Frontend)**: Implement unit tests for React components using **Jest** and **React Testing Library**. These tools let you render components in isolation and simulate user interactions to verify output. (More on testing in Chapter 10.)

By the end of this stage, you should have a functional React application structure, with placeholder components or basic pages, ready to interact with a backend API. Next, we'll build the .NET Core backend to serve data to this React app.

## 3. Building the .NET Core Backend API

The backend will be a RESTful API built with ASP.NET Core. We will create a Web API project, implement endpoints, and include best practices like dependency injection (DI), authentication with JWT, and database integration using Entity Framework Core.

### 3.1 Initializing the ASP.NET Core Web API

Use the .NET CLI to create a new Web API project:

```bash
dotnet new webapi -n ServerApi
```

This will scaffold a new ASP.NET Core Web API in the `ServerApi` folder ([Complete Guide to using ASP.NET Core with React](https://www.scholarhat.com/tutorial/aspnetcorewebapi/asp-dot-net-core-react#:~:text=2,Core%20Project)). It comes with a sample WeatherForecast controller. Alternatively, you can create the project in Visual Studio (choose "ASP.NET Core Web API" template). Ensure **Use Controllers** is selected (for minimal APIs, you'd structure things differently).

**Project Structure**: Key parts of an ASP.NET Core API project include:

- `Program.cs` (or `Startup.cs` in older versions): where services are configured and the app is built.
- `Controllers/` folder: contains API controllers (each controller corresponds to a set of endpoints).
- `appsettings.json`: configuration file for settings like connection strings. Also `appsettings.Development.json` for environment-specific overrides.
- Models, DTOs, and other folders as needed (you may create folders for Services, Repositories, etc., to organize code).

Run the template project to verify it's working:

```bash
cd ServerApi
dotnet run
```

By default, it will serve on `https://localhost:5001` (and http on 5000). The template includes a WeatherForecast endpoint; you can test it via browser or curl.

### 3.2 Dependency Injection and Project Structure

**Dependency Injection (DI)**: ASP.NET Core has DI built-in. Services like the `DbContext` (for EF Core) or custom services will be registered in `Program.cs` (via `builder.Services.Add...` calls) and then injected into controllers or other services via constructor parameters. This promotes loose coupling and easier testing ([DbContext Lifetime, Configuration, and Initialization - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#:~:text=The%20preceding%20code%20registers%20,NET%20Core%20configuration)) ([DbContext Lifetime, Configuration, and Initialization - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#:~:text=public%20class%20MyController%20,readonly%20ApplicationDbContext%20_context)).

For example, to register a simple service:

```csharp
// Program.cs
builder.Services.AddScoped<IMyService, MyService>();
```

Now `IMyService` can be a custom interface and `MyService` its implementation. In a controller, you request `IMyService` in the constructor and ASP.NET will provide it from the DI container:

```csharp
public class MyController : ControllerBase {
    private readonly IMyService _myService;
    public MyController(IMyService myService) {
        _myService = myService;
    }
    // Actions use _myService...
}
```

The Web API template by default already registers some services (like controllers, swagger, etc.). Keep registration of services organized – you can create extension methods or separate static classes to group related registrations (for example, all services related to a feature).

**MVC Controllers**: By default, the template uses Controllers decorated with `[ApiController]` and attribute routing. For instance, `WeatherForecastController` might have `[Route("[controller]")]` which means the route is based on the controller name. You can define specific routes and HTTP verbs using attributes like `[HttpGet]`, `[HttpPost("actionName")]`, etc.

**Example Controller**: A simple controller could look like:

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase {
    private readonly IProductRepository _repo;
    public ProductsController(IProductRepository repo) {
        _repo = repo;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll() {
        var products = await _repo.GetAllProductsAsync();
        return Ok(products);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> Get(int id) {
        var product = await _repo.GetProductByIdAsync(id);
        if (product == null) return NotFound();
        return Ok(product);
    }

    // ... other actions (POST, PUT, DELETE) ...
}
```

Here, `IProductRepository` is injected via DI. The controller actions return HTTP responses (`Ok()`, `NotFound()`, etc.) with appropriate types.

**Separation of Concerns**: For maintainability, consider using a layered approach:

- Controllers handle HTTP and model binding.
- **Services** (or business logic layer) handle core logic.
- **Repositories** (data layer) handle data access (e.g., via Entity Framework).

This separation isn't strictly required, but it can help manage complex applications. You can inject a service into the controller instead of a repository directly, depending on your design.

### 3.3 Authentication and Authorization (OAuth2/JWT)

Securing the API is critical. We will implement **JWT (JSON Web Tokens)** based authentication, which is a common choice for SPAs. With JWT, the client (React app) will obtain a token (usually after a login API call) and then include that token in the Authorization header for subsequent API requests.

**Setting up JWT Authentication**: In ASP.NET Core, add the JWT Authentication handler in `Program.cs`:

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
// ... other service registrations ...

builder.Services.AddAuthentication(options => {
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options => {
    options.RequireHttpsMetadata = false; // in dev only, enable HTTPS in production
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = builder.Configuration["Jwt:Issuer"],       // e.g., "myapp"
        ValidAudience = builder.Configuration["Jwt:Audience"],   // e.g., "myapp_users"
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
    };
});

builder.Services.AddAuthorization();
// ...
var app = builder.Build();
// ...
app.UseAuthentication();
app.UseAuthorization();
```

This configuration sets up JWT bearer tokens as the default auth scheme. We specify validation parameters: the token’s issuer, audience, and a signing key (symmetric key for HMAC). These values (Issuer, Audience, Key) would be in _configuration_ (e.g., in _appsettings.json_ or environment variables) for security. We then ensure `UseAuthentication()` and `UseAuthorization()` are called in the middleware pipeline (order is important: they should come **before** mapping endpoints).

With this, any endpoint decorated with `[Authorize]` will require a valid JWT access token in the `Authorization: Bearer <token>` header of the request. The JWT middleware will validate the token (signature and claims) according to the parameters we set. If the token is missing or invalid, the request will be rejected with 401 Unauthorized.

**Token Issuance**: We need an endpoint to issue tokens. This could be an "AuthController" with a `[HttpPost] Login` action. For example:

```csharp
[AllowAnonymous]
[HttpPost("login")]
public IActionResult Login([FromBody] LoginModel model) {
    // Validate user credentials (e.g., check username/password against DB)
    // ...
    if (isValidUser) {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.UTF8.GetBytes(Configuration["Jwt:Key"]);
        var tokenDescriptor = new SecurityTokenDescriptor {
            Subject = new ClaimsIdentity(new[] {
                new Claim(ClaimTypes.Name, model.Username)
                // add more claims as needed, e.g., roles
            }),
            Expires = DateTime.UtcNow.AddHours(1),
            Issuer = Configuration["Jwt:Issuer"],
            Audience = Configuration["Jwt:Audience"],
            SigningCredentials = new SigningCredentials(
                new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
        };
        var token = tokenHandler.CreateToken(tokenDescriptor);
        string jwt = tokenHandler.WriteToken(token);
        return Ok(new { token = jwt });
    }
    return Unauthorized();
}
```

This uses `System.IdentityModel.Tokens.Jwt` to create a token. In practice, you might use a library or identity framework, but the above illustrates the concept. The React app would call this `login` endpoint with user credentials, get back the token, and store it (in memory or localStorage) to include in future requests.

**OAuth2**: If integrating with an external identity provider (Google, Azure AD, etc.), you'd use OAuth2 flows. In such cases, you might not manually issue JWTs but rather validate tokens from those providers. For example, Azure AD B2C or IdentityServer can handle issuing tokens. Given our scope, implementing JWT issuance in-app is sufficient for most needs, but be aware that **rolling your own auth requires careful security review**. Consider using **ASP.NET Core Identity** or third-party auth services if appropriate.

**Authorization**: Once authentication is in place, you can restrict access to endpoints:

- Use `[Authorize]` on controllers or specific actions.
- Use roles or policy-based authorization if needed (e.g., `[Authorize(Roles = "Admin")]` if you include role claims in JWT).
- For a public endpoint, use `[AllowAnonymous]`.

JWT is stateless (no server-side session), which fits well with SPAs. The server just needs the signing key to validate tokens ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=JWT%20,header%20and%20a%20bearer%20token)) ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=We%20recommend%20using%20OpenID%20Connect,tokens%20intended%20for%20API%20access)). Ensure you protect that key (don’t hard-code it; keep it in configuration such as environment variables or Azure Key Vault in production).

### 3.4 Database Integration with Entity Framework Core

For data persistence, integrate a database using **Entity Framework Core (EF Core)**. EF Core allows you to interact with a database using .NET classes (models) and LINQ queries, and it supports many providers (SQL Server, PostgreSQL, etc.).

**Choose a Database**: .NET Core works with many DBs. SQL Server is often used (with the `Microsoft.EntityFrameworkCore.SqlServer` provider). PostgreSQL is another excellent choice (use `Npgsql.EntityFrameworkCore.PostgreSQL` provider). Install the appropriate NuGet package for your database provider:

```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
```

(for SQL Server, for example).

**Define a Data Model and DbContext**:

- Create model classes representing your data (entities). For instance, a `Product` class with properties like `Id`, `Name`, `Price`.
- Create a subclass of `DbContext` (e.g., `AppDbContext`) that includes `DbSet<TEntity>` properties for each entity, and optionally override `OnModelCreating` for configurations.

Example:

```csharp
public class Product {
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    // Other properties...
}

public class AppDbContext : DbContext {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<Product> Products { get; set; }
}
```

**Register DbContext with DI**: In `Program.cs`, register the context with the connection string:

```csharp
string connStr = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connStr));
```

This tells EF Core to use SQL Server with the provided connection string. The `DefaultConnection` string would be defined in _appsettings.json_. For example, in _appsettings.json_:

```json
"ConnectionStrings": {
  "DefaultConnection": "Server=localhost;Database=MyAppDb;User Id=myuser;Password=mypassword;Trusted_Connection=False;"
}
```

During development, you might use a local SQL Server or a Dockerized DB. Ensure the connection string matches your setup. EF Core will manage the connection. By registering with DI, `AppDbContext` can be injected wherever needed (e.g., into a repository or directly into a controller, though direct injection into controllers is less common beyond simple scenarios).

**Migrations**: Use EF Core migrations to create the database schema from your models. Typical steps:

```bash
dotnet ef migrations add InitialCreate
dotnet ef database update
```

This will apply the migrations to the database (creating tables, etc.). Ensure `dotnet-ef` tool is installed (`dotnet tool install --global dotnet-ef`) and that your connection string is correct.

**Using the DbContext**: In a repository or service, inject `AppDbContext`. For example:

```csharp
public class ProductRepository : IProductRepository {
    private readonly AppDbContext _db;
    public ProductRepository(AppDbContext db) { _db = db; }

    public async Task<IEnumerable<Product>> GetAllProductsAsync() {
        return await _db.Products.ToListAsync();
    }
    public async Task<Product?> GetProductByIdAsync(int id) {
        return await _db.Products.FindAsync(id);
    }
    // ...other methods (Add, Update, Delete)
}
```

Then register this repository in DI (`builder.Services.AddScoped<IProductRepository, ProductRepository>();`). The controller can call into the repository, which uses EF Core to query the database. EF Core will translate LINQ to SQL queries and handle opening/closing connections.

EF Core uses **DbContext pooling** by default as scoped services. Each web request gets its own DbContext instance (scoped lifetime) ([DbContext Lifetime, Configuration, and Initialization - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#:~:text=The%20preceding%20code%20registers%20,NET%20Core%20configuration)) ([DbContext Lifetime, Configuration, and Initialization - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#:~:text=The%20final%20result%20is%20an,disposed%20when%20the%20request%20ends)). This is usually ideal: it aligns with unit-of-work per request, and changes are saved via `SaveChanges()`.

**Best Practices**:

- **Async DB Calls**: Always use async methods like `ToListAsync`, `FindAsync`, `SaveChangesAsync` to avoid blocking threads.
- **No Business Logic in Controllers**: Keep complex logic in services, not in the controller or directly in EF queries.
- **Validation**: Validate input (use Data Annotations or FluentValidation for model validation on DTOs).
- **Automapper**: Consider using AutoMapper to map between entity models and DTOs that you expose via API, so you don't leak internal schema or to shape data as needed.
- **Database Security**: Use parameterized queries (EF Core does this by default) to prevent SQL injection. Limit the exposure of sensitive data.

With EF Core set up, your API can now create, read, update, and delete data from the database. We have a basic full-stack: React frontend and .NET API backend. Next, we'll containerize these applications for consistent deployment.

## 4. Dockerizing the Application with Docker Compose

Containerizing your app ensures that it runs the same in any environment. We will create Docker images for both the React frontend and the .NET Core API, then use Docker Compose to run them together (along with a database container if needed). This simplifies deployment to Azure and other platforms.

### 4.1 Dockerizing the React Frontend

For a React app, the production deployment is usually a bundle of static files. We can use a **multi-stage Docker build** to first compile the React app, then serve it via a lightweight web server (like **nginx**).

Create a file `Dockerfile` in the React app directory (`/client`). An example Dockerfile for React:

```Dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with nginx
FROM nginx:stable-alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
# Copy a custom nginx config if you have one (optional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

In this Dockerfile:

- We use Node 18 in the first stage to install dependencies and build the app (running `npm run build` produces a production-ready static bundle in `build/` folder) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=%23%20Build%20Stage%20FROM%20node%3A18,RUN%20npm%20run%20build)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Exposes%20port%2080)).
- The second stage uses an nginx alpine image to serve those static files. We copy the build output into nginx's web root and then run nginx ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=FROM%20nginx%3Astable,g%22%2C%20%22daemon%20off)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)).
- We expose port 80 (the default nginx serving port).

This results in a small final image (only nginx and the static files, not the entire Node toolchain). It’s optimized for production use.

To build this image, you would run (from the `client` directory):

```bash
docker build -t myapp-frontend:latest .
```

This tags the image as "myapp-frontend:latest". (In Compose, we'll automate this.)

### 4.2 Dockerizing the .NET Core Backend API

In the ASP.NET Core project directory (`/ServerApi`), create a Dockerfile. .NET also benefits from multi-stage builds:

```Dockerfile
# Stage 1: Build and publish the .NET application
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ServerApi.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app

# Stage 2: Run the app using the runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app ./
EXPOSE 80
ENTRYPOINT ["dotnet", "ServerApi.dll"]
```

Explanation:

- We use Microsoft’s official .NET SDK image (for .NET 8) to compile the app ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=FROM%20mcr,source)) ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=,aspnetapp.dll)). We copy the csproj and run `dotnet restore` first (leveraging Docker layer caching so that if code changes but project file doesn’t, we don’t re-download packages on every build) ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=In%20the%20preceding%20Dockerfile%2C%20the,17%20Best%20practices%20for%20writing)). Then copy the rest and run `dotnet publish` to produce a release build.
- The final stage uses the lighter ASP.NET runtime image (no SDK) for running the app ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=FROM%20mcr,aspnetapp.dll)). We copy the published output from the build stage. We expose port 80 (inside the container the app will listen on default Kestrel port 80 unless configured otherwise). The entrypoint runs the DLL.

This yields a much smaller image than using the SDK image for runtime, and it's the recommended approach for containerizing .NET apps ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=The%20sample%20Dockerfile%20uses%20the,in%20Docker%20Hub%20by%20Microsoft)) ([Run an ASP.NET Core app in Docker containers | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-9.0#:~:text=The%20sample%20Dockerfile%20uses%20the,in%20Docker%20Hub%20by%20Microsoft)).

Build the image with:

```bash
docker build -t myapp-backend:latest .
```

(If your project has a solution and multiple projects, adjust paths accordingly in the Dockerfile COPY commands. The example assumes a single csproj in the directory.)

**Database Container** (Optional): If using SQL Server or PostgreSQL in Docker, you might not containerize the DB within the same image (you wouldn't put SQL Server inside your API container). Instead, you'll run a separate container for the database and network it with the API. For example, use the image `mcr.microsoft.com/mssql/server` for SQL Server or `postgres` for PostgreSQL, with environment variables for credentials.

### 4.3 Setting Up Docker Compose

Docker Compose allows defining multi-container applications. Create a `docker-compose.yml` at the root of your project (where you have both `client` and `ServerApi` directories):

```yaml
version: "3.8"
services:
  backend:
    build:
      context: ./ServerApi
      dockerfile: Dockerfile
    ports:
      - "5000:80" # Map host port 5000 to container's port 80 (ASP.NET Core)
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=${ConnectionStrings__DefaultConnection}
    depends_on:
      - db

  frontend:
    build:
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "3000:80" # Map host port 3000 to container's port 80 (nginx)
    depends_on:
      - backend

  db:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      SA_PASSWORD: "Your_password123"
      ACCEPT_EULA: "Y"
    ports:
      - "1433:1433"
```

In this Compose file:

- We define a **backend** service using the Dockerfile in `ServerApi`. It maps port 5000 outside to 80 inside (so our API is reachable at http://localhost:5000). We pass environment variables: here `ASPNETCORE_ENVIRONMENT=Development` (so the app can use the Development settings) and a connection string (demonstrating how to pass complex config via env vars, using the `__` double-underscore notation to map to config sections in .NET) ([Getting Started with Docker-Compose for ASP.NET Core and MSSQL](https://www.csharp.com/article/getting-started-with-docker-compose-for-asp-net-core-and-mssql/#:~:text=%7B%20,Warning)) ([Getting Started with Docker-Compose for ASP.NET Core and MSSQL](https://www.csharp.com/article/getting-started-with-docker-compose-for-asp-net-core-and-mssql/#:~:text=%7B%20services.AddControllers%28%29%3B%20services.AddDbContext)).
- The **frontend** service builds from the React app’s Dockerfile. It maps port 3000 outside to 80 inside. (In production you might use 80:80, but 3000 is chosen here to avoid conflicts with any dev server and to remind that it’s the frontend.) The frontend depends on backend, meaning it starts after the backend.
- A **db** service (example for SQL Server) is included, with a default SA password and the EULA acceptance required by MS SQL image ([Getting Started with Docker-Compose for ASP.NET Core and MSSQL](https://www.csharp.com/article/getting-started-with-docker-compose-for-asp-net-core-and-mssql/#:~:text=db%3A%20image%3A%20mcr.microsoft.com%2Fmssql%2Fserver%3A2019,%221433%3A1433)). This allows the backend to connect to "Server=db" (since in Compose, the service name becomes the hostname). Indeed, note in the connection string we used above, often you'd set it to "Server=db;Database=...;User=sa;Password=Your_password123;" in appsettings for it to connect to this containerized DB ([Getting Started with Docker-Compose for ASP.NET Core and MSSQL](https://www.csharp.com/article/getting-started-with-docker-compose-for-asp-net-core-and-mssql/#:~:text=%7B%20,Warning)).

With this setup, you can run:

```bash
docker-compose up --build
```

This will build images if not present and start all containers together ([Getting Started with Docker-Compose for ASP.NET Core and MSSQL](https://www.csharp.com/article/getting-started-with-docker-compose-for-asp-net-core-and-mssql/#:~:text=docker)). You should be able to navigate to:

- http://localhost:3000 for the React app (served by nginx container).
- http://localhost:5000 for the API (you can test the API directly to ensure it's running, e.g., GET http://localhost:5000/weatherforecast if using the default template endpoint).

The React app in production build may need to know the API URL. If it's a single-page app purely served by nginx, you might configure the base API URL as an environment variable at build time. For example, set `REACT_APP_API_URL` in the Dockerfile build ARG or docker-compose, and use it in your React code for API calls. Alternatively, since our setup puts them on the same host, you could configure a proxy or simply use relative paths if served from the same domain. (If served from different domains, handle CORS on the API – by default the template enables CORS for any origin in development; you’d configure it for production accordingly.)

**Docker Ignore**: Remember to have a `.dockerignore` file in each context (client and server) to avoid sending unnecessary files to the docker build (node_modules, bin/obj folders, etc.).

At this point, we have container images for the frontend and backend. We can run them locally with Compose and ensure everything works. Containerization also sets the stage for CI/CD and deployment.

## 5. Implementing CI/CD Pipelines (GitHub Actions & Azure DevOps)

Continuous Integration and Continuous Deployment (CI/CD) will automate building, testing, and deploying our application. We will outline using **GitHub Actions** (YAML-based workflows in GitHub) and mention **Azure DevOps Pipelines** as an alternative. Both can achieve similar end goals: build the code, run tests, package docker images, and deploy to Azure.

### 5.1 GitHub Actions for CI/CD

GitHub Actions allows you to define workflows in a YAML file (e.g., `.github/workflows/main.yml`) that run on GitHub’s hosted runners on certain triggers (push, PR, etc.). Here's a high-level example of what a CI/CD workflow might look like:

**Continuous Integration (CI) Steps**:

1. **Trigger** – e.g., on every push to main (or pull request).
2. **Checkout code** – use actions/checkout to get the repository code.
3. **Set up Node & .NET** – use actions/setup-node and actions/setup-dotnet to install the necessary toolchains.
4. **Install & Test Frontend** – run `npm ci` and `npm run test -- --watch=false` (for instance) in the `client` directory.
5. **Build Frontend** – run `npm run build` to produce the production build.
6. **Build & Test Backend** – run `dotnet restore`, `dotnet build`, and `dotnet test` for the .NET solution.
7. **Build Docker Images** – use Docker commands or the Docker Buildx action to build the frontend and backend images. Tag them, possibly with the commit SHA or a version.
8. **Push Docker Images** – push the images to a container registry (could be Docker Hub or Azure Container Registry). This requires auth (store credentials or use GitHub’s OIDC with cloud).
9. **Deploy** – use an action to deploy to Azure Web App (if using Web Apps for Containers) or other targets.

For example, a job might use the Azure Web App action:

```yaml
- uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
    publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
    images: myregistry.azurecr.io/myapp-backend:${{ github.sha }}, myregistry.azurecr.io/myapp-frontend:${{ github.sha }}
```

The above would tell Azure to update a web app with those container images (assuming the web app is configured for multi-container or using a compose). You would have set up the Azure publish profile secret and possibly use a multi-container configuration.

Another strategy is to build and push the images in the pipeline, and simply update the Azure App Service to use the new image tags.

**Parallel or Sequential**: Frontend and backend can be built in parallel jobs to speed up CI. However, for CD, you might want them in the same job for an atomic deploy.

**Example Workflow Snippet**:

```yaml
name: CI-CD

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Set up Node.js
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      # Set up .NET
      - uses: actions/setup-dotnet@v2
        with:
          dotnet-version: 8.0.x

      # Cache/restore npm packages (optional for speed)
      # - uses: actions/cache@v3 ...

      # Install and test frontend
      - name: Install Frontend Deps
        run: npm ci
        working-directory: client
      - name: Test Frontend
        run: npm run test -- --watch=false
        working-directory: client

      # Build frontend
      - name: Build Frontend
        run: npm run build
        working-directory: client

      # Build and test backend
      - name: Restore .NET
        run: dotnet restore
        working-directory: ServerApi
      - name: Build .NET
        run: dotnet build --no-restore -c Release
        working-directory: ServerApi
      - name: Test .NET
        run: dotnet test --no-build -c Release
        working-directory: ServerApi

      # Build Docker images
      - name: Build Backend Image
        run: docker build -t myapp-backend:${{ github.sha }} ./ServerApi
      - name: Build Frontend Image
        run: docker build -t myapp-frontend:${{ github.sha }} ./client

      # Log in to Azure Container Registry
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }} # stored as secret (SP credentials)

      - name: Push Images to ACR
        run: |
          docker tag myapp-backend:${{ github.sha }} myregistry.azurecr.io/myapp-backend:${{ github.sha }}
          docker tag myapp-frontend:${{ github.sha }} myregistry.azurecr.io/myapp-frontend:${{ github.sha }}
          docker push myregistry.azurecr.io/myapp-backend:${{ github.sha }}
          docker push myregistry.azurecr.io/myapp-frontend:${{ github.sha }}

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          slot-name: Production
          images: myregistry.azurecr.io/myapp-backend:${{ github.sha }}, myregistry.azurecr.io/myapp-frontend:${{ github.sha }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

This is a simplified example. It builds and tests everything, pushes images to Azure Container Registry (ACR), then instructs an Azure Web App to pull those images. The Azure login and publish profile secrets need to be configured in your GitHub repo. Alternatively, you could use Web App's continuous deployment from container registry without the deploy action (just push images and Azure will pick up latest if configured with "latest" tag and continuous deployment enabled).

**GitHub Actions vs Azure DevOps**: The above is GitHub Actions style. Azure DevOps uses a similar YAML approach or classic UI. The tasks in Azure DevOps would mirror these steps (e.g., use Docker@2 tasks to build and push images ([Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops#:~:text=steps%3A%20,%24%28tag)), AzureWebAppContainer@1 to deploy ([Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops#:~:text=,azureSubscription))). If your code is in Azure Repos, Azure Pipelines might be preferred, but for GitHub repositories, Actions are very convenient.

### 5.2 Azure DevOps Pipelines (Alternative)

If using Azure DevOps, you’d set up a pipeline in a `azure-pipelines.yml` file. It would have stages similar to above: build, test, push to registry, deploy. Azure DevOps has built-in tasks for many things:

- **DotNetCLI@2** to build/test .NET.
- **Npm@1** to install/test Node apps.
- **Docker@2** to build and push images (as seen in the snippet from MS docs, it can use `buildAndPush` command with a service connection to ACR ([Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops#:~:text=steps%3A%20,dockerRegistryServiceConnection%29%20tags%3A))).
- **AzureWebAppContainer@1** to deploy the container image to a Web App ([Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops#:~:text=,azureSubscription)).

For example, Microsoft’s documentation shows a YAML for building and pushing to ACR, then deploying to Web App for Containers in a stage ([Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops#:~:text=,14)). The Azure DevOps pipeline will require setting up a Service Connection for Azure, and storing secrets (like ACR credentials or using the built-in linkage when pushing to ACR via service connection).

**Environment Promotion**: In either system, you might have separate stages for **Staging** and **Production** deployments, with approvals in between. For instance, CI builds and pushes images, then you have a manual approval to deploy to production.

The key is automation: every commit/merge can trigger a build, run tests (to catch issues early), and if everything is okay, automatically deploy or at least prepare a deploy. This reduces errors and speeds up delivery.

We will now focus on deployment specifics and security considerations, which tie into CI/CD as well.

## 6. Security Best Practices for Full-Stack Applications

Security must be integrated at every stage of development. Here are important security practices for our React + .NET application:

### 6.1 Secure Development Practices

- **HTTPS Everywhere**: Serve both frontend and backend over HTTPS in production. ASP.NET Core project templates enable HTTPS by default and even include HSTS (HTTP Strict Transport Security) support ([Enforce HTTPS in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/enforcing-ssl?view=aspnetcore-9.0#:~:text=We%20recommend%20that%20production%20ASP,Core%20web%20apps%20use)). Ensure the web app is configured to **redirect HTTP to HTTPS** and use HSTS headers in production (ASP.NET Core’s `UseHttpsRedirection` and `UseHsts` middleware) ([Enforce HTTPS in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/enforcing-ssl?view=aspnetcore-9.0#:~:text=,HSTS%29%20headers%20to%20clients)). For development, .NET generates a dev certificate to use HTTPS locally; for production, use valid certificates (Azure Web Apps provide this via bindings).
- **CORS**: If the frontend and backend are served on different domains, configure CORS on the API to only allow the expected origin(s) and HTTP methods. Avoid broad `AllowAnyOrigin` in production – lock it down to your domain.
- **Input Validation**: Never trust client input. Use model validation on the API side (e.g., `[Required]`, `[MaxLength]` attributes or manual checks) and also validate on client (for better UX) but the server is the final gatekeeper. For any data that goes into a database, consider using parameterized queries or ORM (EF Core) to avoid SQL injection (EF Core by default parameterizes queries).
- **Output Encoding**: React by default escapes content in JSX, protecting against XSS in most cases. Don’t disable that unless necessary. If you render user-provided HTML, use libraries to sanitize it.
- **Authentication & Authorization**: As covered, use robust authentication (JWT with strong signing keys). Keep the JWT secret key truly secret – do not commit it; store in environment configuration (or Azure Key Vault). Enforce authorization rules on the API (don’t rely on UI to hide/show elements as the only protection). For example, even if the React app doesn’t show an "Admin" button to a non-admin user, someone could call the admin API – so the API must check roles/claims.
- **Avoid Sensitive Data in Frontend**: Do not embed secrets or private data in the React app. Remember, _anything in the React app (even in .env files) becomes public_. For instance, if you need an API key for a third-party service, consider proxying the call through your backend to keep the key hidden. Frontend env vars only help configure, not truly secure data ([React Environment Variables: How To Use Them Securely](https://onboardbase.com/blog/react-env#:~:text=Since%20React%20is%20client,because%20they%20will%20be)).

### 6.2 Protecting Secrets and Configurations

- **Config Files**: Use ASP.NET Core’s configuration system to your advantage. Keep sensitive config like connection strings out of source code (e.g., in _appsettings.json_ but even better in environment variables in production). Azure allows defining app settings which override appsettings.json values.
- **User Secrets (Development)**: During dev, you can use the Secret Manager (`dotnet user-secrets`) to store secrets locally outside of code.
- **Environment Variables (Production)**: Pass secrets (DB passwords, JWT signing keys, etc.) via environment variables in your Docker/azure settings. ASP.NET Core will automatically read `ASPNETCORE_ENVIRONMENT`, connection strings, etc., from environment if configured so ([Deploying Docker to Azure App Service - GitHub Enterprise Server 3.12 Docs](https://docs.github.com/en/enterprise-server@3.12/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=Create%20a%20personal%20access%20token,Managing%20your%20personal%20access%20tokens)) ([Deploying Docker to Azure App Service - GitHub Enterprise Server 3.12 Docs](https://docs.github.com/en/enterprise-server@3.12/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=az%20webapp%20config%20appsettings%20set,settings%20DOCKER_REGISTRY_SERVER_URL%3Dhttps%3A%2F%2Fghcr.io%20DOCKER_REGISTRY_SERVER_USERNAME%3DMY_REPOSITORY_OWNER%20DOCKER_REGISTRY_SERVER_PASSWORD%3DMY_PERSONAL_ACCESS_TOKEN)). In React, build-time env vars aren't secret; if you truly need a secret on frontend, you likely need a different approach because anything sent to the browser can be inspected.
- **Azure Key Vault**: For a higher level of security, consider using Azure Key Vault to manage secrets and have your app pull them at startup (there are providers to directly integrate Key Vault with ASP.NET Core configuration).

### 6.3 Hardening and Additional Measures

- **Least Privilege**: Give your app only the permissions it needs. For example, database user should have limited rights (not `sa` in production, but a user with just needed access).
- **SQL Injection & ORM**: If using raw SQL or Dapper, always parameterize queries. EF Core by default is safe from SQL injection if you use LINQ or parameterized raw SQL (via `FromSql`). Be cautious with any `ExecuteSqlRaw` calls.
- **Logging and Monitoring**: Implement logging (Serilog, etc.) to record important events, but avoid logging sensitive info (like don’t log passwords or full JWT tokens). In case of an incident, logs help trace issues.
- **Error Handling**: Don’t expose internal errors to end-users. In ASP.NET Core, ensure the Developer Exception Page is only in Development. In production, use `UseExceptionHandler` to catch exceptions and maybe return a generic error message. Similarly, handle frontend errors gracefully; don't show raw error objects to users.
- **Security Headers**: Add HTTP headers for security on both frontend and backend responses:
  - Use Content Security Policy (CSP) header to restrict resource loading (might be complex for SPAs, but consider it).
  - Ensure X-Frame-Options, XSS-Protection (for older browsers), Referrer-Policy, etc., are appropriately set. You can configure these in the web server (nginx) or via middleware in .NET. E.g., consider using the `NWebsec` middleware or similar to add security headers.
- **Packages and Updates**: Keep dependencies up to date. Security vulnerabilities are regularly found in NPM packages or NuGet packages; update frequently to incorporate patches. Remove unused dependencies to reduce attack surface.
- **Testing**: Perform security testing – e.g., try out some common attacks (XSS, SQL injection, CSRF) to ensure your app is not vulnerable. Use tools like OWASP ZAP or Burp Suite for security scanning.

By adhering to these practices, you significantly reduce the risk of breaches. Remember that security is an ongoing process, not a one-time setup.

## 7. Deploying Containerized Applications to Azure Web Apps

Now that we have our app containerized and CI/CD in place, let's deploy it to Azure. We will use **Azure App Service (Web Apps for Containers)** to host our Docker containers. Azure App Service can run single-container apps or multi-container apps using Docker Compose.

### 7.1 Preparing Azure Resources

**Resource Group**: Create an Azure Resource Group (e.g., via Azure Portal or CLI):

```bash
az group create --name MyAppGroup --location "Central US"
```

**Azure Container Registry (ACR)**: Although not strictly required (you could use Docker Hub), using ACR is convenient and secure for Azure deployments:

```bash
az acr create --resource-group MyAppGroup --name MyAppRegistry --sku Basic --admin-enabled true
```

(This creates a registry named MyAppRegistry.azurecr.io. `--admin-enabled true` gives you username/password for the registry to use in GitHub Actions or Azure DevOps if needed.)

Push your images to ACR (from CI or locally for initial test):

```bash
az acr login --name MyAppRegistry
docker tag myapp-backend:latest MyAppRegistry.azurecr.io/myapp-backend:latest
docker push MyAppRegistry.azurecr.io/myapp-backend:latest
# (repeat for frontend)
```

**Create Azure App Service Plan**: For Docker, use a Linux plan:

```bash
az appservice plan create --name MyAppPlan --resource-group MyAppGroup --is-linux --sku B1
```

(B1 is a basic tier; for production you might use B2 or higher tiers.)

### 7.2 Deploying to Azure Web App for Containers

**Single Container Deployment**: If you have only one container (e.g., you combine frontend and API into one image, or you're only deploying the API and serving frontend separately via CDN), you could use a single-container Web App. In our case, we have two containers. We have two approaches:

- Use **Multi-container (Compose)** deployment.
- Use two separate Web Apps (one for frontend, one for backend).

**Using Multi-Container with Docker Compose**:
Azure Web App for Containers on Linux can accept a docker-compose.yml (with some constraints). You can zip your `docker-compose.yml` and deploy it, or use Azure CLI to set it:

```bash
az webapp create --resource-group MyAppGroup --plan MyAppPlan --name MyAppWeb --multicontainer-config-type compose --multicontainer-config-file docker-compose.yml
```

Or you can set the compose via Azure Portal (under the Web App’s Docker Container settings). The compose file should reference images in a registry (ACR in this case, so ensure the Web App is configured with credentials to pull from ACR – which can be done by linking ACR or enabling Managed Identity).

Using the Compose approach, Azure will spin up both containers as defined. Ensure ports match (Azure Web App will route port 80 by default for HTTP traffic into the container network).

**Using Separate Web Apps**:
Alternatively, deploy backend and frontend to separate App Services:

- Backend: Create a Web App (Container) for the API:
  ```bash
  az webapp create --resource-group MyAppGroup --plan MyAppPlan --name myapp-backend --deployment-container-image-name MyAppRegistry.azurecr.io/myapp-backend:latest
  ```
  This creates a web app and deploys a specific container image ([Deploying Docker to Azure App Service - GitHub Enterprise Server 3.12 Docs](https://docs.github.com/en/enterprise-server@3.12/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=az%20webapp%20create%20%5C%20,name%20nginx%3Alatest)) ([Deploying Docker to Azure App Service - GitHub Enterprise Server 3.12 Docs](https://docs.github.com/en/enterprise-server@3.12/actions/use-cases-and-examples/deploying/deploying-docker-to-azure-app-service#:~:text=In%20the%20command%20above%2C%20replace,name%20for%20the%20web%20app)). You need to configure the app to use your ACR (you can do `az webapp config container set` with registry details if not using the `--deployment-container-image-name`).
- Frontend: Similarly:
  ```bash
  az webapp create --resource-group MyAppGroup --plan MyAppPlan --name myapp-frontend --deployment-container-image-name MyAppRegistry.azurecr.io/myapp-frontend:latest
  ```

Then, you'll have two URLs: e.g., myapp-backend.azurewebsites.net and myapp-frontend.azurewebsites.net. You’d configure the frontend to call the backend at the given URL. Optionally, set up a custom domain for each (or more commonly, use a single domain with path or subdomain separation).

If using separate apps, ensure CORS is configured on the API to allow the frontend’s domain.

**Environment Variables on Azure**:
In Azure Web App settings, configure any environment variables your containers need (under Application Settings). For instance, set `ASPNETCORE_ENVIRONMENT = Production`, `Jwt__Key` (for JWT secret), `ConnectionStrings__DefaultConnection` for DB, etc. Azure will inject these into the container. For ACR authentication, if using the `--deployment-container-image-name` approach, Azure will use the linked registry settings (which you may set with `az webapp config container set --name myapp-backend --docker-registry-server-url ... --docker-registry-server-user ... --docker-registry-server-password ...` or by linking via the portal). If the ACR is in the same subscription, you can use managed identity or an admin-enabled ACR as used.

**Database on Azure**:
If your DB is local (as in our Docker compose), you'll need to migrate to a cloud DB for production (e.g., Azure SQL Database or Azure PostgreSQL). Update the connection string in Azure settings accordingly. Azure Web App can use VNET integration to reach a DB in a private network if needed.

**Testing the Deployed App**:
Once deployed, test the endpoints:

- Access the frontend URL – you should see the React app.
- The React app should be able to communicate with the API (if CORS and URL configs are correct).
- Test a protected API call – ensure that your JWT auth works on Azure (the JWT secrets and config must be set properly as Azure app settings).

**Continuous Deployment**: If using CI/CD as configured, pushing to main (or a tagged release) can automatically build and push a new container, and then Azure Web App (if configured with "latest" or specific tag) can pull the update. Alternatively, your CI can call `az webapp restart` or re-deploy to trigger an update. Azure also supports connecting the web app to a GitHub Actions workflow (the action we used above essentially does that by deploying images).

**Scaling**: Azure App Service can scale out (multiple instances) even for container apps. If stateless (as our app should be), you can safely enable autoscaling to handle more load.

By deploying to Azure, we have our app live on the cloud. Next, we discuss managing different configurations for different environments (Dev, Staging, Prod) which is important in a CI/CD and cloud context.

## 8. Managing Environment Configurations (Dev, Staging, Prod)

Your application likely needs different settings for different stages (development, testing/staging, production). We should manage these configurations in a clean way:

### 8.1 Environment Variables & Config in React

**React**: At build time, React picks up environment variables from `.env.*` files. We can use:

- `.env.development` for local development settings.
- `.env.production` for production build settings ([Leveraging Environment Variables in React: A Safe & Effective Guide - DEV Community](https://dev.to/shriharimurali/leveraging-environment-variables-in-react-a-safe-effective-guide-1p4j#:~:text=In%20the%20root%20directory%20of,you%20can%20create%20files%20named)).
- Possibly `.env.staging` if you create a staging build.

For example, in `.env.production`:

```
REACT_APP_API_URL=https://myapp-backend.azurewebsites.net
```

and in `.env.development`:

```
REACT_APP_API_URL=http://localhost:5000
```

When you run `npm run build`, if `NODE_ENV` is `production` (which it is by default for the build script), CRA will use `.env.production`. When running `npm start`, it uses `.env.development`. This way, the frontend will call the correct API depending on environment.

Make sure not to commit any secrets in these .env files. In CI/CD, you could override or set env vars as needed. For example, in GitHub Actions, you might set `REACT_APP_API_URL` as an input to the build step for production.

If your staging environment is essentially an Azure deployment with a different API URL or endpoints, you might need to build a separate version or use runtime configuration. Since React is a static bundle, one pattern is to inject a configuration at runtime (for example, fetch a config JSON from the server on startup). This can allow one build to be deployed to multiple environments with different config. However, a simpler approach is to create separate builds for each environment if needed.

### 8.2 ASP.NET Core Configuration for Multiple Environments

ASP.NET Core handles this gracefully via the `ASPNETCORE_ENVIRONMENT` variable. By default, the template sets this to "Development" when running locally (through launchSettings.json). In Azure, it defaults to "Production" if not set.

**AppSettings**: You can have _appsettings.Development.json_, _appsettings.Staging.json_, _appsettings.Production.json_, etc. The `CreateBuilder` call automatically loads the main appsettings.json and then the environment-specific one based on `ASPNETCORE_ENVIRONMENT`. For instance, if env is "Staging", it will load appsettings.json then override with appsettings.Staging.json values ([Use multiple environments in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/environments?view=aspnetcore-9.0#:~:text=1.%20DOTNET_ENVIRONMENT%20%202.%20,DOTNET_ENVIRONMENT)).

Use this to your advantage:

- In appsettings.Development.json, you might have local dev settings (local DB connection, etc.).
- In appsettings.Production.json, production settings (production DB connection, prod logging settings).
- You can also use appsettings.Staging.json for a staging environment that mimics prod.

**Example**:

```json
// appsettings.json
{
  "Logging": { ... },
  "AllowedHosts": "*",
  "Jwt": {
    "Issuer": "MyApp",
    "Audience": "MyAppUsers"
  }
}
```

```json
// appsettings.Development.json
{
  "Jwt": {
    "Key": "DEV_ONLY_SECRET_KEY_123"
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyAppDev;User Id=dev;Password=devpass;"
  }
}
```

In production, you wouldn't store the real secret in a file; you'd use environment variables:

- Set `Jwt__Key` in Azure app settings (double underscore maps to nested config).
- Set `ConnectionStrings__DefaultConnection` in Azure as well (or use Azure's Connection Strings section which populates `ConnectionStrings:DefaultConnection`).

The app will combine these config sources. By default, environment variables override appsettings if they are set, which is convenient for sensitive values.

**Connection Strings in Azure**: If you use the Azure Portal’s Connection Strings blade, those become available in ASP.NET Core config too (as `DefaultConnection` in ConnectionStrings). Azure app settings also override appsettings.json automatically when `ASPNETCORE_ENVIRONMENT` is "Production".

**Managing per environment**:
In CI/CD pipelines, you can use separate config files or transforms:

- You might maintain separate YAML pipelines or workflow logic for different environments (with different variables).
- If using Azure DevOps release pipelines, you can substitute values in appsettings.json for different stages.

A typical approach:

- Keep generic config in appsettings.json and source control (non-secret).
- Use environment-specific JSON files or pipeline variables for environment-specific stuff.
- Use secrets storage for sensitive values.

**React vs .NET Config**: Note that for React, once built, the config is baked in. .NET can change config per deploy. If you need to change a React config (like API URL) without rebuilding, one technique is to have React app fetch from a `/config` endpoint on the API at runtime. But that's an advanced pattern; many simply rebuild React for each environment because frontend build is fast.

**Feature Flags**: For multi-environment deployments, consider feature flags. Azure App Configuration can serve feature flags that your app reads to enable/disable features without full redeploys.

In summary, design your configuration management so that you can deploy the same code to different environments with minimal friction, just by changing configuration. This ensures your dev/test/prod are as similar as possible (in terms of code), reducing bugs that appear only in one environment.

## 9. Performance Optimizations and Monitoring

Building a working app is one thing; ensuring it performs well and is observable in production is another. Let's cover optimizations for frontend and backend, and how to monitor the app using Azure Application Insights.

### 9.1 Frontend Performance Optimizations

**Production Build**: Always deploy the production build of React (minified, optimized). The difference is huge: a dev build might be 1.3 MB and take ~8 seconds on 3G, whereas a production build could be 534 KB and ~3.5 seconds ([Optimize React App Performance By Code Splitting](https://www.velotio.com/engineering-blog/optimize-react-app-performance-by-code-splitting#:~:text=The%20project%20is%20already%20configured,with%20a%20slow%203G%20connection)). Aim for fast load times (under 3 seconds on good connections) ([Optimize React App Performance By Code Splitting](https://www.velotio.com/engineering-blog/optimize-react-app-performance-by-code-splitting#:~:text=production%20bundle%20is%20much%20smaller%2C,with%20a%20slow%203G%20connection)).

**Code Splitting & Lazy Loading**: Implement code splitting for large apps. For example, use React.lazy and React Router's lazy loading for routes. This way, not all JS is loaded upfront. Code splitting can **significantly reduce initial bundle size**, improving load time and interactivity ([React app code splitting breaks apps. Solutions? - Support](https://answers.netlify.com/t/react-app-code-splitting-breaks-apps-solutions/113058#:~:text=React%20app%20code%20splitting%20breaks,It%27s%20certainly%20a%20best%20practice)). Load heavy components (charts, rich text editors, etc.) only when needed.

**Caching and CDN**: Host static assets (JS/CSS) on a CDN for global apps. Azure App Service can integrate with Azure Front Door or Cloudflare for CDN. Ensure that static files have far-future cache headers (the build output usually has hashed filenames, so it's safe to cache them long-term).

**Use Memoization**: In React, use `React.memo`, `useMemo`, and `useCallback` to avoid unnecessary re-renders of pure components or expensive calculations on each render. But use them judiciously (profile first to see bottlenecks).

**Avoid Heavy Operations on Main Thread**: If you have computations, consider Web Workers. Keep the UI thread free for user interactions.

**Optimize images**: If your app uses images, use proper sizes and possibly lazy load them. Use modern formats like WebP where supported.

**Profiling**: Use React DevTools Profiler to spot performance issues in rendering. Also run Lighthouse (in Chrome DevTools) on your deployed app to see suggestions (like eliminating render-blocking resources, minifying, etc.).

### 9.2 Backend Performance (ASP.NET Core)

ASP.NET Core is very fast out-of-the-box, but there are best practices to follow:

- **Asynchronous code**: Make all I/O operations async (database calls, HTTP calls, file reads). This allows the server to handle many concurrent requests efficiently. Blocking calls can lead to thread pool starvation and poor scalability ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=ASP,can%20work%20on%20another%20request)). Ensure your controller actions are async and return Task. This is especially important under load.
- **Pooling and Reuse**: The HTTP client, if you use one to call external APIs, should be reused (use HttpClientFactory). DBContext is already scoped per request by DI (reused within the request).
- **Database Optimizations**: Index your database tables properly for the queries you make. Use efficient queries (avoid N+1 query scenarios, use `.Include` in EF Core for related data as needed). Limit data fetched (e.g., don’t pull all columns if not needed, although EF Core by default materializes all properties of the entity – for large columns, you might use projections).
- **Caching**: Introduce caching for data that is expensive to fetch and does not change frequently. ASP.NET Core has MemoryCache for in-memory caching ([Caching in ASP.NET Core: Improving Application Performance](https://www.milanjovanovic.tech/blog/caching-in-aspnetcore-improving-application-performance#:~:text=Performance%20www,to%20implement%20various%20caching)), and you can also use distributed cache (Redis, etc.) if running on multiple instances. For example, cache results of a costly DB query for 1 minute if that’s acceptable. This can reduce load on the DB and improve response times ([ASP.NET Core Best Practices | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0#:~:text=Cache%20aggressively)).
- **Output Caching**: For certain GET endpoints that are hit often but don’t change per user, consider response caching (use `[ResponseCache]` attribute or middleware). This can let clients/proxies cache responses.
- **Minimize Middleware**: Only keep necessary middleware in the request pipeline. Each middleware adds a bit of overhead.
- **JSON Serialization**: The default System.Text.Json is fast. But you can optimize JSON size by using [JsonIgnore] on fields not needed in response, or using DTOs to shape data. Smaller responses = faster clients.
- **Pooling**: Use connection pooling for DB (EF Core does by default) and ensure your DB can handle concurrent connections or use a pooler like PgBouncer for Postgres.
- **Scale Up/Out**: Know when to scale. Azure App Service allows scaling up (more CPU/RAM) and out (more instances). If CPU-bound, scale up; if many concurrent requests (I/O bound), scaling out might be more effective.
- **Remove Debug Overhead**: Ensure things like detailed error messages or excessive logging are turned off or reduced in production as they can slow down throughput. Use logging at appropriate levels (Information or Warning for normal ops, Debug only when troubleshooting).

### 9.3 Monitoring with Azure Application Insights

Monitoring is essential to understand how your app performs in real-time and to diagnose issues. **Azure Application Insights** (part of Azure Monitor) is a great tool for this. It can collect logs, metrics, request traces, exceptions, and more from both your backend and frontend.

**Integrating App Insights in Backend**:

- Install the Application Insights SDK (Microsoft.ApplicationInsights.AspNetCore). In .NET 6/7/8, you just call `builder.Services.AddApplicationInsightsTelemetry();` with a connection string or instrumentation key ([Application Insights for ASP.NET Core applications - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/asp-net-core#:~:text=2.%20Add%20,cs%20class)).
- Provide the connection **Connection String** (preferred over instrumentation key now) from your Application Insights resource. E.g., in `appsettings.Production.json`, have:
  ```json
  "ApplicationInsights": {
    "ConnectionString": "<your AI connection string>"
  }
  ```
  The SDK will automatically pick this up when you initialize it ([Application Insights for ASP.NET Core applications - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/asp-net-core#:~:text=,from%20Application%20Insights%20Resource%20Overview)).
- This single line wiring auto-enables collection of HTTP requests, dependency calls (outgoing HTTP, SQL calls), exceptions, and logs ([Application Insights for ASP.NET Core applications - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/asp-net-core#:~:text=Application%20Insights%20can%20collect%20the,NET%20Core%20application)). It will send these to the Azure portal where you can see them in Application Insights blade.
- In Program.cs, after adding, you can also configure logging to use Application Insights (it already hooks into ILogger). For custom events or metrics, you can inject `TelemetryClient` and track events. But out-of-box, it tracks a lot: requests, responses, CPU usage, memory, etc.

**Frontend Monitoring**:

- Application Insights has a JavaScript SDK that you can add to your React app to track page views, AJAX calls, exceptions, etc., from the client side. You’d add the snippet or use npm package `applicationinsights-web`.
- Example:
  ```js
  import { ApplicationInsights } from "@microsoft/applicationinsights-web";
  const appInsights = new ApplicationInsights({
    config: {
      connectionString: "<your AI connection string>",
      enableAutoRouteTracking: true,
    },
  });
  appInsights.loadAppInsights();
  appInsights.trackPageView(); // Manually call if SPA
  ```
- This will report front-end errors and usage to the same App Insights (use a single resource for full-stack visibility). It can correlate requests from the front-end with back-end by operation IDs if configured properly.

**Azure Monitor and Alerts**:

- In Azure, set up **alerts** on Application Insights metrics. For example, alert if server response time avg > 2s for 5 minutes, or if exceptions rate spikes.
- Use the Performance tab in App Insights to see which API calls are slow and why (it can show SQL query times as dependencies).
- Use the Failures tab to see exceptions and failed requests.

**Logging**:

- Continue to use ILogger in .NET for structured logs. Those also flow to App Insights. You can search them with Kusto queries in the Logs tab (for example, query traces or customEvents).
- For front-end, console errors captured by the AI JS SDK appear as exceptions in Application Insights.

**Profiling**:

- App Insights can use an Azure Profiler (for apps on App Service) to take runtime profiles if enabled, which help in deep performance analysis.

**Application Map**:

- If your app calls other Azure services (SQL DB, storage, etc.), Application Insights can visualize an application map of components and call dependencies, which is useful for architecture overview and pinpointing slow points.

By actively monitoring and reviewing this telemetry, you can iteratively improve performance. For instance, if App Insights shows a particular query is slow, you can optimize that query or add an index. If the front-end has a high JavaScript error rate on a certain page, you can investigate those errors (maybe something not handled in code).

Remember to disable or reduce telemetry in local dev if you don't want noise (AI SDK usually doesn't send from dev unless configured, since connection string might be absent or you set `DisableTelemetry` when debugging).

Performance and monitoring go hand-in-hand: optimize, then verify via monitoring, and repeat. This ensures your app is not just functionally correct, but also fast and reliable.

## 10. Testing Strategies: Unit, Integration, and End-to-End Testing

Quality assurance through testing is crucial. We'll outline testing at different levels:

### 10.1 Unit Testing

**Backend Unit Tests**: Use a framework like **xUnit**, **NUnit**, or MSTest (xUnit is very popular with .NET Core). Unit tests should test individual components in isolation:

- **Services/Business Logic**: If you have services with logic, write tests for their methods. Use mocking (via a library like Moq) to simulate dependencies (e.g., repository or external service). This way, the test focuses only on the logic of that service.
- **Controllers**: It’s often unnecessary to unit-test trivial controller actions if they just call a service. Instead, focus on testing the service logic and maybe one test to ensure controller returns expected result for a given service behavior (using a mocked service).
- **Model Validation**: You can test that your Data Annotations work by creating model instances and using a ValidationContext to validate, or test that invalid models are handled as expected (though ASP.NET's model binding does this, integration tests might catch it).

Example (xUnit + Moq):

```csharp
public class ProductServiceTests {
    [Fact]
    public async Task GetProductReturnsNullIfNotFound() {
        // Arrange
        var repoMock = new Mock<IProductRepository>();
        repoMock.Setup(r => r.GetProductByIdAsync(It.IsAny<int>())).ReturnsAsync((Product)null);
        var service = new ProductService(repoMock.Object);

        // Act
        var result = await service.GetProductDetails(42);

        // Assert
        Assert.Null(result);
    }
}
```

This tests that our ProductService returns null (or maybe throws a specific exception, depending on design) when repository yields null.

**Frontend Unit Tests**: Using **Jest** (included with CRA) and **React Testing Library (RTL)**, you can write tests for React components:

- Render a component with given props, simulate user interactions (RTL's `fireEvent` or user-event library), and assert that the DOM output changes as expected.
- Mock external calls: For components that fetch data, you can mock `fetch` or axios using jest mocks or MSW (Mock Service Worker) in tests to provide controlled responses.

Example using React Testing Library:

```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import Counter from "./Counter";

test("Counter increments value on click", () => {
  render(<Counter initial={0} />);
  const button = screen.getByRole("button", { name: /increment/i });
  expect(screen.getByText(/Count: 0/i)).toBeInTheDocument();
  fireEvent.click(button);
  expect(screen.getByText(/Count: 1/i)).toBeInTheDocument();
});
```

This assumes a `Counter` component that displays "Count: X" and increments on button click.

Unit tests are fast and run in isolation, often on every build or in watch mode during development. They give you confidence that the smaller pieces work correctly.

### 10.2 Integration Testing

Integration tests verify the behavior of multiple components together – e.g., the API endpoints with the real database (or a test database). ASP.NET Core makes integration testing easier with the **WebApplicationFactory** in the `Microsoft.AspNetCore.Mvc.Testing` package, which can spin up the app in-memory for tests ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=WebApplicationFactory,Program.cs)).

**API Integration Tests**:

- Use WebApplicationFactory<Program> to create a test server, then use HttpClient to call your API endpoints as if from a client ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=The%20following%20test%20class%2C%20,Type%60%20header%20is)).
- You can use a test database (for example, configure the startup to use an in-memory database like InMemory provider or SQLite for testing). You might have to override configuration in the WebApplicationFactory (there are ways to do that by extending it and overriding ConfigureWebHost to inject a different DbContext or connection string).
- Then write tests like: making an HTTP GET call and asserting the status code and response content.

Example with xUnit:

```csharp
public class ProductsApiTests : IClassFixture<WebApplicationFactory<Program>> {
    private readonly HttpClient _client;
    public ProductsApiTests(WebApplicationFactory<Program> factory) {
        // Optionally customize factory to use a test DB
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetProducts_ReturnsOkAndList() {
        var response = await _client.GetAsync("/api/products");
        response.EnsureSuccessStatusCode();
        var data = await response.Content.ReadAsAsync<List<ProductDto>>();
        Assert.IsType<List<ProductDto>>(data);
        // Additional assertions on data if needed
    }
}
```

This will actually start the app (likely in a test environment), call the real pipeline (so controllers, DI, etc., all in play). It's a powerful way to test things end-to-end at the API level. If you don't want to hit a real DB, use InMemory DB or mock the repository by injecting a fake one in the DI for tests (which you can do by configuring the WebApplicationFactory to swap IProductRepository with a fake implementation that returns controlled data).

Integration tests ensure that your components (routing, controllers, DB code, etc.) work together correctly. They run slower than unit tests (since they boot up more stuff, possibly interact with file system or db), so have a moderate number of them focusing on key scenarios.

**Testing with Real Database**: Some teams run integration tests against a local test database or ephemeral containers (like starting a test Postgres container). This is fine, but make sure to reset state between tests (e.g., using a fresh DB for each test run or using transactions). Entity Framework’s InMemory provider is good for simple tests, but be cautious: InMemory is not a relational database and may not catch issues that a real relational db would (like missing relationships or queries that behave differently).

### 10.3 End-to-End Testing (E2E)

End-to-end tests (also called UI tests or functional tests) simulate a user using the application through the UI, ensuring the entire stack works. These tests will open a browser, click through the UI, and verify outcomes, interacting with both frontend and backend together.

**Tools**:

- **Cypress**: A JavaScript end-to-end testing framework that runs in the browser. Great for testing SPAs; you write tests in JS that interact with the app’s UI.
- **Selenium/WebDriver**: Language-agnostic but older style; you can use with frameworks like Selenium for C# or Python.
- **Playwright**: A newer Node.js (or .NET) library similar to Cypress with multi-browser support and great features.
- **Playwright for .NET** exists, so you could write E2E in C# if you prefer (the ASP.NET docs recommend Playwright for SPA testing ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=For%20testing%20SPAs%2C%20we%20recommend,which%20can%20automate%20a%20browser))).

**What to test E2E**:

- Critical user flows: e.g., user can log in, navigate to dashboard, create an item, see it reflected in list, log out.
- Form validations working end-to-end (client shows error, or server returns error and it's displayed).
- Basically scenarios that involve full system interaction.

**Example with Cypress** (JS):

```js
describe("Todo App", () => {
  it("allows adding a todo item", () => {
    cy.visit("http://localhost:3000");
    cy.get('input[name="new-todo"]').type("Buy milk{enter}");
    cy.contains("Buy milk").should("exist");
  });
});
```

This would start the app (assuming it's running or using cy.visit on a deployed URL), then simulate a user adding a todo, and finally verify that the new todo appears in the list.

For this to work in CI, you could launch your app in a test environment (maybe using docker-compose up with a test config) then run Cypress against it.

**Playwright (.NET)**:
You can use the Playwright NuGet and write tests in C# that open Chromium:

```csharp
using Microsoft.Playwright;
public class E2ETests {
  [Fact]
  public async Task CanRegisterAndLogin() {
    using var playwright = await Playwright.CreateAsync();
    await using var browser = await playwright.Chromium.LaunchAsync();
    var context = await browser.NewContextAsync();
    var page = await context.NewPageAsync();
    await page.GotoAsync("https://myapp-frontend.azurewebsites.net/");
    await page.ClickAsync("text=Register");
    // fill form...
    // assertions...
  }
}
```

This requires the app to be deployed or running for the test.

**Maintenance of E2E**: They can be flaky if not written carefully (timing issues, etc.). Use techniques like waiting for network idle or specific element to appear instead of arbitrary delays.

**Test Environments**: It's common to have a special environment (like a QA or staging environment) where E2E tests run against. For example, after a deployment to staging, run the E2E suite on it. In CI, perhaps spin up containers, then run E2E, then tear down.

**Coverage**: E2E tests complement unit/integration tests by catching issues those might miss (like mis-integrations between front and back, or build/config issues). But they are slower and harder to maintain, so have a smaller set of high-value scenarios.

### Bringing it all together:

- Run unit tests on every commit (fast feedback).
- Run integration tests in CI as well (they take a bit longer, but still do it for main branch at least).
- Perhaps run E2E tests on a nightly build or upon deployment to a test/staging environment, due to their longer runtime.

With a comprehensive testing strategy, you reduce regressions and ensure your full-stack app works as expected from the database all the way to the user interface.

---

By following this guide with structured chapters — setting up your environment, adhering to best practices in building both frontend and backend, containerizing your app, automating the pipeline, securing every layer, deploying to a scalable cloud service, managing configs, optimizing performance, and testing thoroughly — you will be able to build a robust, maintainable, and production-ready full-stack application using **React and .NET Core**.

Each step reinforced industry best practices and prepared the application for real-world usage, aligning with modern development and DevOps processes. Good luck with your full-stack development, and happy coding!
