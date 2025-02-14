# **Timesheet Application – A Comprehensive Full-Stack Guide (React + .NET Core + MySQL)**

## 1. **Introduction**

### **1.1 Overview of the Timesheet Application**

A timesheet application enables employees to record their work hours and submit them for management approval. The system typically supports features like time entry, editing entries, submitting for approval, and managers’ approval workflows. In our comprehensive guide, we’ll walk through building a **monolithic full-stack** timesheet application with a **React.js (TypeScript)** frontend, a **.NET Core** backend, and a **MySQL** database. We will cover everything from initial setup to deployment on **Azure**. The target audience is advanced developers who want a _complete implementation reference_ using **Visual Studio Code (VS Code)** and modern technologies.

### **1.2 Technology Stack and Tools Required**

- **Frontend:** React.js with TypeScript – for building a dynamic single-page application UI. We will use libraries like **Material-UI (MUI)** for UI components and possibly **React Hook Form** for form handling.
- **Backend:** .NET Core (latest version, e.g., .NET 8) – for implementing a Web API using **Entity Framework Core** (EF Core) for data access and **JWT (JSON Web Token) authentication** for security.
- **Database:** MySQL – a reliable open-source relational database to store user accounts, timesheet entries, approvals, etc.
- **Development Environment:** VS Code – with extensions for C# and Azure for efficient development. Node.js (with npm or yarn) and the .NET SDK will be needed on your machine.
- **Deployment:** Azure – we will use **Azure App Service** for the .NET Core API and **Azure Static Web Apps** or **Azure Blob Storage** for the React app, plus **Azure Database for MySQL** for the database.
- **Other Tools:** Git (for version control), GitHub Actions or Azure DevOps (for CI/CD), and MySQL Workbench or Azure Data Studio (for database management).

### **1.3 Project Setup Instructions**

Setting up the project involves preparing both development environments: one for React and one for .NET Core, and ensuring they can communicate. Below is a high-level plan:

1. **Install Prerequisites:** Ensure Node.js (which includes npm) is installed, and also install **yarn** (optional, as an alternative package manager). Install the latest **.NET Core SDK**. Set up **MySQL Server** (either install locally, use Docker, or use Azure for development).
2. **VS Code Extensions:** Install the **C# extension** (for .NET Core) and optionally the **Azure Account/Azure App Service** extensions. Also install **ESLint** and **Prettier** for code quality in React.
3. **Initialize Repositories:** You can keep frontend and backend in one repository (monorepo style) or separate repositories. For simplicity, we’ll assume a single repository with two main folders: `client` (React app) and `server` (ASP.NET Core API).
4. **Communication Setup:** We will configure CORS and perhaps a proxy for local development so that the React frontend (running on, say, `http://localhost:3000`) can call the .NET API (running on `http://localhost:5000`).
5. **Environment Variables:** Plan out environment variables for sensitive configs, such as the database connection string (for backend) and API base URL (for frontend). Use `.env` files and VS Code’s **dotenv** extensions to manage them for development, and plan for secure storage in Azure for production.

**Next steps:** We’ll dive into setting up the development environment in detail, then proceed to building backend and frontend step-by-step.

---

## 2. **Setting Up the Development Environment**

Before coding, we need to set up our development environment properly on your machine. We’ll cover Node.js/TypeScript for React, .NET Core, MySQL, and VS Code configuration.

### **2.1 Installing Node.js, npm (or yarn), and TypeScript**

- **Install Node.js:** Download and install Node.js from the official site (nodejs.org) – use the LTS version for stability. This also installs **npm** (Node Package Manager). Verify by running `node -v` and `npm -v` in a terminal.
- **Yarn (Optional):** Yarn is an alternative to npm. You can install it globally with `npm install -g yarn`. This guide uses npm or yarn interchangeably – use whichever you prefer for installing packages.
- **Install TypeScript:** Though Create React App will handle TypeScript setup, you might want the TypeScript compiler globally for other uses. Install it via npm: `npm install -g typescript`. Verify by `tsc -v` which should output the TypeScript version.

_Why TypeScript?_ – It adds static typing to JavaScript, improving developer productivity and code quality by catching errors at compile time. MUI (Material-UI) and many libraries provide type definitions for better IntelliSense in VS Code.

### **2.2 Setting up a React Project with TypeScript**

We’ll use Create React App (CRA) with a TypeScript template for quick setup:

1. **Create React App (CRA):** In your desired directory, run:
   ```bash
   npx create-react-app client --template typescript
   ```
   This creates a `client` folder with a React project pre-configured for TypeScript. (If using yarn: `yarn create react-app client --template typescript`).
2. **Project Structure:** CRA will give a standard structure (`src` for source files, `public` for static files). Open this project in VS Code (`code client`). If prompted “Required assets to build and debug are missing…”, click **Yes** to allow VS Code to set up launch configurations.
3. **Run the App:** Inside the `client` folder, run `npm start` (or `yarn start`). This should start the dev server at `http://localhost:3000` and open a browser showing the React welcome page. This verifies your React/TypeScript setup is working.

**VS Code Configuration for React/TypeScript:**

- Make sure to enable **TypeScript validation** and check that VS Code is using the workspace TypeScript version (Open Command Palette > “TypeScript: Select TypeScript Version” > choose “Use workspace version” if needed).
- Install VS Code plugins: **ESLint** (for linting), **Prettier** (for code formatting). A proper ESLint config (with TypeScript support) can be set up for code consistency.
- In `tsconfig.json` of the React project, ensure strict settings are enabled as recommended by MUI ([TypeScript - Material UI](https://mui.com/material-ui/guides/typescript/?srsltid=AfmBOopexk0Vf6IZzfmNq5dOuBQ2DP1ZUeWkaAcXtTJI5XyyHU50sZT3#:~:text=%7B%20,true%20%7D)) (CRA usually sets `"strict": true` already which includes strict type-checking flags).

### **2.3 Installing and Configuring .NET Core**

- **Install .NET SDK:** Download and install the latest **.NET Core SDK** (or .NET SDK if using .NET 6/7/8) from Microsoft’s website. On Windows, use the installer; on macOS, use the PKG; on Linux, use package managers (apt, yum, etc.). Verify installation by running `dotnet --version`.
- **VS Code C# Extension:** If not already installed, add the official **C# extension** (by Microsoft) in VS Code, which provides IntelliSense and debugging for .NET.
- **Create the .NET Core Project:** We will create an **ASP.NET Core Web API** project in a `server` directory. Use the .NET CLI:
  ```bash
  dotnet new webapi -o server
  ```
  This scaffolds a new Web API project (`-o server` creates a folder named server). The template includes a basic controller (WeatherForecast) which we can remove later.
- **Restore and Run:** Navigate to `server` folder and run `dotnet run`. The API should start (by default on `http://localhost:5000` or `http://localhost:5241` for newer HTTPS). You should see output in the console confirming it’s running and now listening on some URLs. At this point, it’s likely running with a self-signed dev certificate for HTTPS – we can skip certificate warnings for now or use HTTP for simplicity during development.
- **Project Structure:** The key files/folders: `Program.cs` (entry point, configures web host and services), `appsettings.json` (configuration, will include DB connection strings, JWT settings, etc.), `Controllers/` (Web API controllers).

### **2.4 Setting up MySQL Database**

For development, you can use a local MySQL server or run one in Docker. We’ll outline a local installation:

- **Install MySQL:** Download **MySQL Community Server** (preferably MySQL 8.x) for your OS and run the installer. Choose a **Developer Default** setup on Windows which includes MySQL Server, Workbench, etc. On Linux, use `apt-get install mysql-server` or similar.
- **Secure Setup:** During installation, set a **root password** (remember it) and allow MySQL to run on default port 3306. You may also create a dedicated user for the app later.
- **MySQL Workbench (Optional):** Install MySQL Workbench to easily run SQL queries and manage the database schemas. Alternatively, VS Code has a MySQL extension or you can use the Azure Data Studio with the MySQL extension.
- **Create Database:** Launch a MySQL client (Workbench or `mysql` CLI) and create a database for the timesheet app: `CREATE DATABASE TimesheetDb;`. Also create a user if not using root in development:
  ```sql
  CREATE USER 'timesheet_user'@'%' IDENTIFIED BY 'StrongPassword!';
  GRANT ALL ON TimesheetDb.* TO 'timesheet_user'@'%';
  ```
  (Using `%` allows connections from any host – for development it’s fine, but in production, restrict host or use Azure’s managed identity/security.)

We’ll integrate MySQL with EF Core in the backend setup (next section) using the **Pomelo EF Core MySQL provider**, as Microsoft’s Oracle MySQL provider is not as up-to-date. Pomelo’s provider is open-source and widely used.

### **2.5 Configuring Environment Variables**

Managing secrets and environment-specific settings is critical:

- **Backend (.NET):** In development, you can use the `appsettings.Development.json` file to store the MySQL connection string and JWT secrets, but avoid hardcoding sensitive info. Instead, use **User Secrets** (for local development) or environment variables. For example, run `dotnet user-secrets init` in the `server` project, then `dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;Database=TimesheetDb;User Id=timesheet_user;Password=StrongPassword!"`. Similarly set a JWT signing key (`Jwt:Key`) and issuer (`Jwt:Issuer`). The code will read these from config.
- **Frontend (React):** Create a `.env` file in `client` for development, e.g.,
  ```env
  REACT_APP_API_URL=http://localhost:5000   # base URL for API calls
  ```
  React’s CRA exposes any vars prefixed with `REACT_APP_` to the app. Later, for production, we’ll configure environment settings in Azure or in the CI/CD pipeline.

### **2.6 Verifying the Setup**

At this point, ensure:

- The React app (`npm start`) runs and can be opened in a browser (http://localhost:3000).
- The .NET API (`dotnet run`) starts without errors and you can fetch data from a default endpoint (like GET /WeatherForecast which returns sample data in the template) by opening `http://localhost:5000/WeatherForecast` in a browser or using curl.
- MySQL is running and accessible (try connecting via Workbench or using `mysql -u timesheet_user -p`).

If all the above work, you have a solid foundation to start development. Next, we’ll proceed to develop the **.NET Core backend API**.

---

## 3. **Backend Development – .NET Core API**

In this section, we’ll build the monolithic API using .NET Core. “Monolithic” here means one Web API project encompassing all needed areas (as opposed to microservices). We will incorporate **Entity Framework Core** for database operations, define our data models, handle authentication and authorization via JWT, and implement business logic like timesheet submission and approval.

### **3.1 Setting up a New .NET Core Project**

We already created the `server` project using `dotnet new webapi`. Let’s refine it:

- **Project Cleanup:** Remove the sample `WeatherForecast` classes and controller – we’ll add our own controllers. Confirm `server.csproj` has necessary references (we will add EF Core and JWT related packages soon).
- **Enable Nullable Reference Types:** In the project file or in a Directory.Build.props, ensure `<Nullable>enable</Nullable>` and `<ImplicitUsings>enable</ImplicitUsings>` are set (usually by default in new templates). This helps catch null-related issues at compile time.
- **Run the Project:** Just to ensure nothing’s broken after cleanup, run `dotnet run` again and ensure the app starts (though we removed the only controller, the app is essentially doing nothing but still listening).

### **3.2 Creating a Monolithic Architecture**

We will keep this API simple and monolithic. All features (auth, timesheet, approvals) will live in this single project, but we’ll structure it cleanly:

- **Folders:** Create folders like `Models` (for data models/EF entities), `Data` (for EF Core DbContext and migrations), `Controllers` (for API controllers), `Services` (for business logic services, optional), and `Dtos` (for data transfer objects if needed). This layered approach keeps code organized.
- **Onion Architecture (optional):** If you prefer separation, you could have separate class libraries for Domain (entities), Infrastructure (EF Core context, migrations), etc., but to keep it straightforward, we’ll do all in one project with folders.

### **3.3 Implementing Entity Framework Core with MySQL**

EF Core will handle database interactions via models and a DbContext. Steps to set it up:

1. **Add EF Core Packages:** Use Pomelo’s MySQL EF Core provider:
   ```bash
   dotnet add package Pomelo.EntityFrameworkCore.MySql
   dotnet add package Microsoft.EntityFrameworkCore.Design
   ```
   Pomelo provides compatibility with MySQL, and the Design package is needed for migrations tooling.
2. **Create a Data Context:** In `Data` folder, create `TimesheetContext.cs`:

   ```csharp
   using Microsoft.EntityFrameworkCore;
   using YourNamespace.Models;
   using Pomelo.EntityFrameworkCore.MySql.Infrastructure;

   public class TimesheetContext : DbContext
   {
       public TimesheetContext(DbContextOptions<TimesheetContext> options) : base(options) { }

       public DbSet<User> Users { get; set; }
       public DbSet<TimesheetEntry> TimesheetEntries { get; set; }
       public DbSet<TimesheetApproval> TimesheetApprovals { get; set; }
       // ... other DbSets as needed

       protected override void OnModelCreating(ModelBuilder modelBuilder)
       {
           base.OnModelCreating(modelBuilder);
           // Fluent API configurations if needed (e.g., relationships, constraints).
       }
   }
   ```

   Note: We’ll define `User`, `TimesheetEntry`, etc. in the Models section next.

3. **Configure Connection String:** In `appsettings.json`, add:
   ```json
   "ConnectionStrings": {
     "DefaultConnection": "Server=localhost;Database=TimesheetDb;User=timesheet_user;Password=StrongPassword!;TreatTinyAsBoolean=true"
   }
   ```
   (The `TreatTinyAsBoolean=true` is a MySQL quirk if using `TINYINT(1)` as bool. Alternatively, just use BIT or proper bool types in migrations.)
4. **Configure EF Core in Program.cs:**  
   In `Program.cs`, inside the `var builder = WebApplication.CreateBuilder(args);` section, add:
   ```csharp
   var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
   builder.Services.AddDbContext<TimesheetContext>(options =>
       options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));
   ```
   The `UseMySql` extension comes from Pomelo’s package; `ServerVersion.AutoDetect` will figure out the MySQL version. If you prefer not to AutoDetect, specify like `ServerVersion.Create(new Version(8,0,31), ServerType.MySql)` for MySQL 8.0.31, but AutoDetect usually works well.
5. **Enable Migrations Tool:** Run `dotnet tool install --global dotnet-ef` to ensure the EF Core CLI is available. Verify with `dotnet ef --help`. If you installed the SDK correctly, sometimes it’s already available.

### **3.4 Designing Models and Database Migrations**

We will create the data models as C# classes, then generate EF Core migrations to create the database schema. Some key models for a timesheet app:

- **User:** Represents an employee or manager. Fields: `Id, FullName, Email, PasswordHash, Role (e.g., Employee/Manager/Admin)`. If using Identity, you could integrate ASP.NET Core Identity, but for brevity, we’ll create a simplified user model and handle auth ourselves (since we target JWT and perhaps custom roles).
- **TimesheetEntry:** Represents a daily or weekly entry of hours. Fields: `Id, UserId, Date, HoursWorked, Description, Status (Pending/Approved/Rejected), CreatedAt`. Possibly a link to an approval record.
- **TimesheetApproval:** Represents an approval record. Fields: `Id, TimesheetEntryId, ManagerId, ApprovedOn, Status (Approved/Rejected), Comments`. Or, you might simplify and just have a field on TimesheetEntry for manager’s decision and use this table for history.

Create these classes in the `Models` folder. Example `TimesheetEntry.cs`:

```csharp
public class TimesheetEntry
{
    public int Id { get; set; }
    public int UserId { get; set; }
    public DateTime Date { get; set; }
    public decimal HoursWorked { get; set; }
    public string Description { get; set; }
    public TimesheetStatus Status { get; set; }  // an enum for Pending, Approved, Rejected
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public User User { get; set; }  // navigation property
}
public enum TimesheetStatus { Pending, Approved, Rejected }
```

And `User.cs`:

```csharp
public class User
{
    public int Id { get; set; }
    public string FullName { get; set; }
    public string Email { get; set; }
    public byte[] PasswordHash { get; set; }  // store hashed passwords
    public string PasswordSalt { get; set; }  // if using a salt (or use Identity library)
    public string Role { get; set; }  // e.g., "Employee" or "Manager" etc.

    public List<TimesheetEntry> TimesheetEntries { get; set; }
}
```

We keep it simple: storing PasswordHash and Salt if we implement custom auth, or we might decide to integrate ASP.NET Identity for user management (which brings a lot of tables and complexity, so many prefer a custom lightweight approach for JWT).

Now, run **EF Core Migrations**:

```bash
dotnet ef migrations add InitialCreate
```

This should produce a `Migrations` folder with a migration class that has `Up` and `Down` methods, creating tables for our models. Check the migration code to verify it matches your intent (correct table names, column types, foreign keys, etc.). Then apply the migration to the database:

```bash
dotnet ef database update
```

This executes the migration against the database specified in the connection string, creating tables. If everything is set correctly, the **TimesheetDb** should now have tables like `Users`, `TimesheetEntries`, etc. (You can verify via MySQL Workbench). EF Core also creates a `__EFMigrationsHistory` table to track applied migrations.

### **3.5 Implementing Authentication and Authorization (JWT)**

For our API, we want to secure endpoints so only authenticated users can access them, and certain endpoints (like approvals) only accessible by managers. We’ll use **JWT (JSON Web Tokens)** for stateless auth: the client (React) will log in, get a JWT, store it, and send it in the `Authorization` header for subsequent requests. The server will validate the JWT and set the user context for authorization. Steps:

1. **Add JWT Authentication Packages:**

   ```bash
   dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
   dotnet add package System.IdentityModel.Tokens.Jwt
   ```

   These provide JWT handling capabilities.

2. **Configure JWT in Program.cs:**  
   Define some settings in `appsettings.json`, e.g.:

   ```json
   "Jwt": {
     "Key": "YourSuperSecretKeyHere",
     "Issuer": "TimesheetApp",
     "Audience": "TimesheetAppUsers",
     "ExpireMinutes": 60
   }
   ```

   The Key should be a long random string (in production, store securely). Issuer and Audience are identifiers to validate the token. Now in `Program.cs` builder configuration:

   ```csharp
   using Microsoft.AspNetCore.Authentication.JwtBearer;
   using Microsoft.IdentityModel.Tokens;
   using System.Text;
   //...
   var jwtSettings = builder.Configuration.GetSection("Jwt");
   var key = Encoding.UTF8.GetBytes(jwtSettings["Key"]);

   builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
       .AddJwtBearer(options =>
       {
           options.TokenValidationParameters = new TokenValidationParameters
           {
               ValidateIssuer = true,
               ValidateAudience = true,
               ValidateLifetime = true,
               ValidateIssuerSigningKey = true,
               ValidIssuer = jwtSettings["Issuer"],
               ValidAudience = jwtSettings["Audience"],
               IssuerSigningKey = new SymmetricSecurityKey(key)
           };
       });
   ```

   This registers JWT Bearer authentication. We enable validation for issuer, audience, lifetime, and signature, using the symmetric key (which is derived from our secret key). Now the app knows how to validate incoming JWTs.

3. **Issue JWTs (Login Endpoint):**  
   Create an `AuthController` with a `[HttpPost("login")]` action. Steps inside `login`:

   - Validate user credentials (check email/password against the database). For password handling, if we stored hash, we’d hash the input password and compare. For simplicity, you might initially store plaintext for testing but **that’s not recommended for real apps**. Instead, use a strong hash (e.g., PBKDF2 or bcrypt).
   - If valid, create a JWT token:
     ```csharp
     var tokenHandler = new JwtSecurityTokenHandler();
     var tokenDescriptor = new SecurityTokenDescriptor
     {
         Subject = new ClaimsIdentity(new[] {
             new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
             new Claim(ClaimTypes.Name, user.FullName),
             new Claim(ClaimTypes.Role, user.Role)  // include role claim
         }),
         Expires = DateTime.UtcNow.AddMinutes(int.Parse(jwtSettings["ExpireMinutes"])),
         Issuer = jwtSettings["Issuer"],
         Audience = jwtSettings["Audience"],
         SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
     };
     var token = tokenHandler.CreateToken(tokenDescriptor);
     string tokenString = tokenHandler.WriteToken(token);
     ```
     Return this `tokenString` to the client (usually in a JSON like `{ token: "..." }`).
   - In addition to the token, you might return some user info (like name, role) so the client can store that in its state. But sensitive info should remain in the token claims or fetched via an API.

4. **Authorization:**

   - Apply `[Authorize]` attribute on controllers or actions that require auth. For example, our `TimesheetController` (which will handle CRUD on timesheet entries) should be `[Authorize]` so only authenticated users can call it.
   - For role-specific, you can use `[Authorize(Roles = "Manager")]` on e.g. `ApprovalsController`, so only JWTs containing “Manager” in their `Roles` claim can access ([JWT Validation and Authorization in ASP.NET Core - .NET Blog](https://devblogs.microsoft.com/dotnet/jwt-validation-and-authorization-in-asp-net-core/#:~:text=So%2C%20a%20roles,to%20APIs%20and%20work%20immediately)). We added the role claim above when issuing the token.
   - Ensure in Program.cs we also have `app.UseAuthentication(); app.UseAuthorization();` in the correct order in the HTTP pipeline (Authentication must come before Authorization). The template might already have Authorization in place, just add Authentication accordingly. For .NET 8 minimal APIs, you’d call `app.UseAuthentication()` manually.

5. **Testing Auth:**
   - Try registering a test user manually in the database or create a register endpoint (optional). If manual, hash a password or temporarily adjust code to not require hashed password just to test token issuance.
   - Call `/login` via a tool like Postman: POST with JSON `{ "email": "user@example.com", "password": "password123" }`. You should get back a token if credentials are correct.
   - Call a protected endpoint, e.g., GET `/api/timesheets` with `Authorization: Bearer <token>` header. If the token is valid and not expired, the call should succeed; if missing or wrong, you get 401 Unauthorized by default.

By implementing JWT auth, we decouple the client and server auth concerns: the server only checks tokens and never manages sessions or cookies, making it ideal for SPA backends.

### **3.6 Creating API Endpoints for Timesheet CRUD Operations**

Now with auth in place, let’s create endpoints for core timesheet functionality. We’ll likely have:

- **Timesheet Entries:**

  - `GET /api/timesheets` – list timesheet entries for the logged-in user (if role is Employee) or maybe all entries to approve (if role is Manager). We might differentiate by role or have separate endpoints.
  - `GET /api/timesheets/{id}` – get a specific entry (with appropriate authorization: employees can fetch their own, managers can fetch if it’s under their purview).
  - `POST /api/timesheets` – create a new timesheet entry (employee records their hours for a date). This will include data like date, hours, description. Set status to Pending by default, and associate with the logged-in user’s ID.
  - `PUT /api/timesheets/{id}` – update an existing entry (if it’s still pending and belongs to the user, allow edit; if already approved/rejected, might block edits).
  - `DELETE /api/timesheets/{id}` – possibly allow deletion if pending.

- **Approvals (Manager actions):**
  - `GET /api/approvals/pending` – manager fetches all pending timesheets to approve (likely filtered to the team they manage; how we determine that is app-specific. Perhaps any manager can see all for simplicity, or the User model could have a ManagerId or department grouping).
  - `POST /api/approvals/{timesheetId}` – to approve or reject a timesheet. We can accept a payload like `{ "approved": true, "comments": "Looks good." }` or `{ "approved": false, "comments": "Please correct date." }`. The API will then update the TimesheetEntry status to Approved or Rejected, record who approved it (manager’s user id, from token), and perhaps create a record in TimesheetApproval table.

We will create **TimesheetController** and **ApprovalController** (or combine logically). Use `[ApiController]` and route like `[Route("api/[controller]")]`. Add `[Authorize]` at class level to ensure all actions require a logged-in user, and add specific `[Authorize(Roles="Manager")]` on approval actions if needed.

Inside these controllers, use dependency injection to get `TimesheetContext`. For example:

```csharp
public class TimesheetController : ControllerBase
{
    private readonly TimesheetContext _db;
    public TimesheetController(TimesheetContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetMyEntries()
    {
        // get user ID from token:
        int userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier).Value);
        var entries = await _db.TimesheetEntries
                               .Where(t => t.UserId == userId)
                               .ToListAsync();
        return Ok(entries);
    }

    [HttpPost]
    public async Task<IActionResult> CreateEntry(TimesheetEntryDTO dto)
    {
        int userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier).Value);
        var entry = new TimesheetEntry
        {
            UserId = userId,
            Date = dto.Date,
            HoursWorked = dto.Hours,
            Description = dto.Description,
            Status = TimesheetStatus.Pending,
            CreatedAt = DateTime.UtcNow
        };
        _db.TimesheetEntries.Add(entry);
        await _db.SaveChangesAsync();
        return CreatedAtAction(nameof(GetMyEntries), new { id = entry.Id }, entry);
    }
    // ... other actions (PUT, DELETE)
}
```

We use a DTO (`TimesheetEntryDTO`) for incoming data to avoid binding the EF entity directly. The `CreatedAtAction` returns HTTP 201 with a Location header by convention.

For Approval in a Manager controller:

```csharp
[Authorize(Roles = "Manager")]
[Route("api/[controller]")]
[ApiController]
public class ApprovalsController : ControllerBase
{
    private readonly TimesheetContext _db;
    public ApprovalsController(TimesheetContext db) { _db = db; }

    [HttpGet("pending")]
    public async Task<IActionResult> GetPendingEntries()
    {
        var pendingEntries = await _db.TimesheetEntries
                                      .Where(t => t.Status == TimesheetStatus.Pending)
                                      .Include(t => t.User)
                                      .ToListAsync();
        return Ok(pendingEntries);
    }

    [HttpPost("{timesheetId}")]
    public async Task<IActionResult> Decide(int timesheetId, ApprovalDecisionDTO decision)
    {
        var entry = await _db.TimesheetEntries.FindAsync(timesheetId);
        if(entry == null) return NotFound();
        if(entry.Status != TimesheetStatus.Pending)
            return BadRequest("Timesheet already processed.");

        entry.Status = decision.Approved ? TimesheetStatus.Approved : TimesheetStatus.Rejected;
        _db.TimesheetEntries.Update(entry);
        // Optionally record in TimesheetApprovals table:
        _db.TimesheetApprovals.Add(new TimesheetApproval {
            TimesheetEntryId = timesheetId,
            ManagerId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier).Value),
            Status = decision.Approved ? TimesheetStatus.Approved : TimesheetStatus.Rejected,
            Comments = decision.Comments,
            ApprovedOn = DateTime.UtcNow
        });
        await _db.SaveChangesAsync();
        return Ok();
    }
}
```

Here `ApprovalDecisionDTO` might have `{ bool Approved; string Comments; }`. We ensure only pending entries can be approved/rejected once. After decision, if needed, notify the employee via some mechanism (maybe the frontend will fetch updated status).

**Important:** Enforce that a manager cannot approve their own timesheet if that scenario exists (if a user is both employee and manager). That could be done via additional checks: e.g., if `entry.UserId == managerId`, disallow.

### **3.7 Implementing Business Logic for Approval Workflows**

The core logic lies in the ApprovalsController above. Some additional business rules or enhancements:

- **Prevent Multiple Approvals:** If using a separate TimesheetApproval table, you can ensure one entry doesn’t get two approval records (e.g., mark TimesheetEntry as processed). We handled by status check.
- **Hierarchies:** If managers can only approve their team’s timesheets, we need a way to identify which entries a manager should see. This could be done by adding a field like `ManagerId` or `Department` to User, and then filtering pending entries by that. For simplicity, our example shows all pending to any manager. In a real scenario, you’d implement proper scoping.
- **Email Notifications (optional):** We won’t cover it in depth, but in a real app, upon approval or rejection, you might send an email to the employee. This could be done by integrating an email service or using Azure Logic Apps, etc.

Testing the workflow:

- Have an employee user with a pending timesheet, have a manager user call the approval endpoint. Ensure the status changes and an approval record is created.
- Ensure that unauthorized users (like an employee trying to call the manager endpoints) get a 403 Forbidden due to the role requirement.

### **3.8 Unit and Integration Testing for API Endpoints**

For a robust implementation, write tests for your API:

- **Unit Tests:** Test components like services or controllers in isolation by mocking dependencies. For example, you could have a service method `ApproveTimesheet(int timesheetId, int managerId, bool approve, string comments)` and test its logic (by passing a fake repository or an in-memory context). Use **xUnit** and **Moq** for .NET. e.g., using xUnit’s `[Fact]` and asserting expected outcomes.
- **Integration Tests:** Use the **WebApplicationFactory** or in-memory TestServer provided by ASP.NET Core to run the whole stack in memory. You can seed a test database (like using an in-memory DB or a test container database) and then make HTTP calls to your controllers. ASP.NET Core’s **Microsoft.AspNetCore.Mvc.Testing** simplifies starting the app in tests. Write tests for critical paths:
  - Login returns JWT for valid credentials, and 401 for invalid.
  - Authorized access: calling a protected endpoint with token works (200 OK), without token -> 401.
  - Role restrictions: an employee JWT calling approval endpoint -> 403 Forbidden.
  - CRUD: creating a timesheet returns 201 and actually persists, updating changes fields, etc.

Integration tests help ensure that our Web API behaves correctly with all middleware (auth, etc.) in place. They simulate real requests and can cover more ground than unit tests alone. However, maintain a balance (don’t over-test trivial things in integration, as they are slower).

So far, we’ve built and tested the backend. Keep the API running for the next part – we’ll develop the React frontend to interact with these endpoints.

---

## 4. **Frontend Development – React with TypeScript**

With the backend ready, we switch to implementing the frontend in React (TypeScript). The focus will be on creating a user-friendly UI for timesheet entry and approval using modern React libraries (e.g., Material UI for layout and controls, React Router for navigation, state management with React Query or Redux Toolkit, form handling, and calling the REST API with Axios).

### **4.1 Setting up a New React Project with TypeScript**

We already created the React project (in section 2.2). If not done, ensure the project is up to date and running:

- Navigate to the `client` directory and open in VS Code.
- Clean up initial files: remove or repurpose `App.css`, `App.tsx`, etc., as needed.
- Install necessary packages for our stack:
  - **React Router:** for single-page navigation – `npm install react-router-dom` (TypeScript types included by default in v6).
  - **Axios:** for HTTP requests – `npm install axios`.
  - **Material UI (MUI):** `npm install @mui/material @emotion/react @emotion/styled`. (MUI requires emotion as peer deps).
    - Alternatively, **Ant Design**: `npm install antd` – either library provides a set of components; we’ll proceed with MUI in examples.
  - **State Management:** If using **React Query** – `npm install @tanstack/react-query`. For **Redux Toolkit** – `npm install @reduxjs/toolkit react-redux`. We can use either; React Query is excellent for server state (data fetching), whereas Redux might be used for global UI state or if caching is more custom. Possibly, we use both: React Query for data and Redux for auth state.
  - **React Hook Form + Yup (for forms):** `npm install react-hook-form` and `npm install yup @hookform/resolvers` for schema validation. This simplifies building forms with validation. Alternatively, one can use Formik; Hook Form is lighter-weight and works smoothly with MUI.
  - **Date library:** Consider installing date-fns or moment if dealing with date formatting for timesheets. MUI has a date picker that may require an adapter (like `npm install @mui/x-date-pickers @mui/x-date-pickers-pro date-fns` if needed).
  - **JWT Decode (optional):** `npm install jwt-decode` if we want to decode JWT on client (to get user info from token). Not strictly necessary because we often store user info separately.

After installing, restart `npm start` to ensure no breakage from new dependencies.

### **4.2 Creating Reusable UI Components (Layout and Forms)**

Set up the basic structure of the app:

- **App Component & Routing:** Use React Router to define pages: Login, Register (if needed), Timesheet Entry page, Timesheet List page, Approval Dashboard, etc. Example in `App.tsx`:

  ```tsx
  import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
  import Layout from "./components/Layout";
  import LoginPage from "./pages/LoginPage";
  import TimesheetPage from "./pages/TimesheetPage";
  import ApprovalsPage from "./pages/ApprovalsPage";
  import RequireAuth from "./components/RequireAuth"; // component to protect routes

  function App() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/timesheets" />} />
          <Route path="/login" element={<LoginPage />} />
          {/* Protected routes: wrap with RequireAuth */}
          <Route element={<RequireAuth />}>
            <Route path="/timesheets" element={<TimesheetPage />} />
            <Route path="/approvals" element={<ApprovalsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }
  export default App;
  ```

  Here, `RequireAuth` would check if the user is logged in (perhaps by checking context or Redux store for a valid token) and either render the child routes or redirect to `/login`. We’ll implement auth management soon.

- **Layout Component:** Create a component for common layout (e.g., a responsive drawer or navbar that has links to different sections, like “My Timesheets” and “Approvals” if the user is a manager). This could use MUI’s `<AppBar>` and `<Toolbar>` for a top bar, and conditional rendering of navigation items based on role.
- **Theme:** Optionally set up a MUI theme for consistent styling (colors, typography). With TypeScript, extend the theme if needed to include custom palette, etc. (This might be advanced usage; MUI’s default theme can suffice initially).
- **Reusable Form Components:** If multiple forms (login form, timesheet entry form), you might create generic input components wrapping MUI’s. For example, a `TextField` component that already integrates with React Hook Form’s `register` function and shows validation errors. MUI’s `<TextField>` works well with Hook Form via the `error` and `helperText` props.

**Material UI Example:** A simple responsive app bar:

```tsx
// in Layout.tsx
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth"; // custom hook to get auth state

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Timesheet App
          </Typography>
          {user ? (
            <>
              <Button color="inherit" onClick={() => navigate("/timesheets")}>
                My Timesheets
              </Button>
              {user.role === "Manager" && (
                <Button color="inherit" onClick={() => navigate("/approvals")}>
                  Approvals
                </Button>
              )}
              <Button
                color="inherit"
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
              >
                Logout
              </Button>
            </>
          ) : (
            <Button color="inherit" onClick={() => navigate("/login")}>
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <main style={{ padding: "1rem" }}>{children}</main>
    </>
  );
};
```

Wrap routes inside `<Layout>` if you want the bar on every page.

### **4.3 Implementing Authentication and Session Management (Frontend)**

We need to coordinate with our backend’s JWT auth. The flow:

- **Login Page:** Provides a form (email & password). On submit, calls the backend `/login` API via Axios. If successful, we get a JWT. We then **store the JWT** on the client (likely in **localStorage** or a cookie). We also update the app state to mark the user as logged in.
  - _Security note:_ Storing JWT in localStorage is common and simple, but can be susceptible to XSS. Another approach is to store it in an HTTP-only cookie (set by the server) to mitigate XSS, but then CSRF protection is needed. Since we’re writing a reference guide, we’ll use localStorage for simplicity, but caution the reader: _for high-security apps, consider HTTP-only cookies or secure storage_.
- **Auth Context or Redux:** We need a global way to know if the user is logged in and who they are. We can do this via React Context or Redux. For an advanced dev audience, **Redux Toolkit** might be already familiar, but for demonstration we might use React’s Context API with a `AuthProvider`. Alternatively, use React Query’s concept of caching the “current user”.
  - Let’s outline a simple context: `AuthContext` provides `{ user, token, login, logout }`. When `login` is called (with email/password), it will do the API call and store the token (in localStorage and context state). It might decode the JWT to get user info like role, or the API could return user data alongside token. Many APIs do: e.g., `{ token, user: { name, email, role } }`. That saves decoding on the client.
  - On app startup, the context’s `useEffect` can check localStorage for a token, and if present and valid (maybe decode to see if expired), consider the user logged in and populate state.
  - `logout` would remove the token from storage and reset state.
- **Axios Configuration:** To call protected endpoints, Axios must include the JWT in headers. We can set up an Axios instance with an **interceptor** that attaches the `Authorization: Bearer ...` header to each request if a token is present. This way, we don’t manually attach token for every call. For example:
  ```tsx
  import axios from "axios";
  const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:5000",
  });
  // Request interceptor to add JWT
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
  export default api;
  ```
  Also handle response interceptor to catch 401s (if token expired, maybe logout or refresh, but we may not implement refresh tokens in this guide for brevity).
- **Protecting Routes:** As shown, a `RequireAuth` component (could be implemented using `<Outlet />` and context). It checks if `user` exists; if not, redirect to `/login`. Also possibly display a loading indicator while checking auth state on first load.
- **Role-based UI:** Show/hide certain navigation links or page content based on `user.role`. For example, only show the Approvals page link if `user.role === 'Manager'`. Also on ApprovalsPage component itself, you could protect via logic or simply rely on backend protection (if a non-manager navigates, the API calls will 403, and you can handle that gracefully).

**Session persistence:** By using localStorage for the token, we maintain the user’s session even after a page refresh (the context/provider on load will retrieve the token). If using Redux, you might integrate something like Redux-Persist. With Context, an effect to load token is fine.

### **4.4 Consuming .NET Core APIs using Axios**

Now the core of the frontend: using Axios to call our API endpoints and displaying data. Let’s outline key pages:

- **LoginPage:**
  - Form with fields for email and password (use MUI TextField and a Button).
  - Use `useForm` from React Hook Form for managing form state and validation (e.g., require both fields). Example:
    ```tsx
    const {
      register,
      handleSubmit,
      formState: { errors },
    } = useForm<LoginFormData>();
    const { login } = useAuth();
    const onSubmit = async (data: LoginFormData) => {
      try {
        await login(data.email, data.password);
        navigate("/timesheets");
      } catch (err) {
        setErrorMessage("Invalid credentials");
      }
    };
    return (
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="Email"
          {...register("email", { required: true })}
          error={!!errors.email}
          helperText={errors.email && "Email is required"}
        />
        <TextField
          type="password"
          label="Password"
          {...register("password", { required: true })}
          error={!!errors.password}
          helperText={errors.password && "Password is required"}
        />
        <Button type="submit" variant="contained">
          Login
        </Button>
        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      </form>
    );
    ```
    The `login` context function will call Axios:
    ```tsx
    // in AuthProvider or so:
    const login = async (email, password) => {
      const response = await api.post("/api/auth/login", { email, password });
      const { token, user } = response.data;
      localStorage.setItem("token", token);
      setAuthState({ user, token });
    };
    ```
    We assume our API returns both token and user info. If not, we could decode token (jwt-decode) to extract info like role, but it’s easier to return user.
- **TimesheetPage (for employees):**
  - Two parts: a form to add a new entry, and a list/table of existing entries.
  - Use **React Query** or **Axios with useEffect** to fetch the list of timesheets for the current user. If using React Query:
    ```tsx
    const { data: timesheets, refetch } = useQuery("timesheets", async () => {
      const res = await api.get("/api/timesheets");
      return res.data;
    });
    ```
    React Query will manage caching and loading state. Alternatively, use a `useEffect(() => { api.get(...).then(setTimesheets) } , [])` and manage loading manually with useState.
  - Render the list: perhaps use MUI’s `<Table>` component to show date, hours, status, and maybe an edit/delete button for pending entries.
  - The **entry form**: fields for date, hours, description. Use React Hook Form again for this sub-form. On submit, do `api.post('/api/timesheets', data)` then on success either refetch the list (if using React Query, call `refetch` or have an automatic invalidation on success with React Query’s `useMutation`). If using local state, simply append to list.
  - Validation: require a date, require hours (and numeric). You can use Yup with Hook Form to enforce e.g., hours > 0. Use `yup.object({ hours: yup.number().positive().required(), ... })` and integrate via `resolver: yupResolver(schema)` in useForm config.
  - Provide user feedback: show a success message or clear the form on success; show an error alert if the API call fails.
- **ApprovalsPage (for managers):**
  - Display a list of pending timesheets requiring approval. Similar to above, fetch via `api.get('/api/approvals/pending')`.
  - Render maybe in a table with employee name, date, hours, description. Perhaps allow clicking a row to see details. For each entry, have Approve/Reject buttons.
  - On Approve or Reject click, call the API: `api.post('/api/approvals/{id}', { approved: true, comments: "..." })`. For UI simplicity, maybe a dialog pops up to enter an optional comment, then confirm.
  - After action, update the UI: remove that entry from the pending list (you could refetch the pending list, or just filter it out from state). Also perhaps show a toast/snackbar saying "Timesheet approved!" or "Rejected and employee notified" etc.
  - If managers also should see all timesheets or filter by employee, that could be an extension. In our scope, focusing on pending list and action.

**Integration between Frontend and Backend:**

- Ensure that the API URL is correctly set (via `REACT_APP_API_URL`). If you run frontend on port 3000 and backend on 5000, CORS must be configured on the backend to allow requests from 3000. We will cover CORS in section 5, but if you already encounter CORS errors, a quick fix in dev is to proxy calls via React’s proxy setting or just enable CORS for localhost in .NET.
- Test the end-to-end: register a user (maybe via a quick API call or make a registration page if desired), login through the UI, ensure you get to TimesheetPage upon successful login, add an entry, see it appear in list. If possible, create a second user with Manager role and use them to login and see the approval list.

### **4.5 Managing Application State with React Query or Redux**

We touched on this but let’s clarify state management choices:

- **Authentication State:** Best handled in a context or Redux store. Given advanced devs often are comfortable with Redux, we could set up a simple Redux slice for auth:

  ```js
  // authSlice.js (pseudo-code)
  const authSlice = createSlice({
    name: "auth",
    initialState: { user: null, token: null },
    reducers: {
      setCredentials: (state, action) => {
        state.user = action.payload.user;
        state.token = action.payload.token;
      },
      clearCredentials: (state) => {
        state.user = null;
        state.token = null;
      },
    },
  });
  export const { setCredentials, clearCredentials } = authSlice.actions;
  export default authSlice.reducer;
  ```

  Then in a Redux store (configureStore) include this slice. The `login` function would dispatch `setCredentials({ user, token })`. The `<RequireAuth>` can get state via `useSelector(state => state.auth.user)` etc.  
  But if the project is not complex, context might suffice.

- **Server Data State (Timesheets, Approvals):** This is where **React Query** shines, as it provides caching, loading states, and automatic refetch on certain conditions. We could also use **RTK Query** (part of Redux Toolkit) which offers similar features integrated with Redux. Either is fine.  
  For demonstration, assume React Query:
  - Wrap your app in `<QueryClientProvider client={queryClient}>` in `index.tsx` (after creating a `queryClient = new QueryClient()`).
  - Use `useQuery` for GET requests and `useMutation` for POST/PUT. For example, in TimesheetPage:
    ```tsx
    import { useQuery, useMutation } from "@tanstack/react-query";
    const timesheetsQuery = useQuery(["timesheets"], () =>
      api.get("/api/timesheets").then((res) => res.data)
    );
    const createEntryMutation = useMutation(
      (newEntry) => api.post("/api/timesheets", newEntry),
      {
        onSuccess: () => timesheetsQuery.refetch(), // refetch list after adding
      }
    );
    // timesheetsQuery.data contains the list, timesheetsQuery.isLoading indicates loading
    ```
    React Query manages an internal cache key `'timesheets'` and will prevent unnecessary refetch if data is fresh, etc..
  - If using Redux instead: you can store timesheets in Redux store and update via actions. This is more manual work (writing reducers to handle loading, success, fail). RTK Query can reduce that boilerplate.
  - Both approaches are valid; since audience is advanced, they might choose what fits. The key is to avoid doing heavy lifting with just useState if multiple components need the data or if caching is beneficial.

**Note:** _React Query vs Redux_ – They serve different purposes: React Query is for **server state** (data fetched from APIs, which can be stale or need sync) while Redux is for **client state** (UI state, global toggles, etc.). In our app, timesheet data is clearly server state, so React Query is appropriate. Auth status can be seen as global client state, which Redux or context suits. We leverage both tools for what they do best.

### **4.6 Implementing Timesheet Entry Form, Validation, and Submission**

We already discussed the timesheet entry form in 4.4, but let’s detail the user experience and best practices:

- **Date Selection:** Use a date picker component for ease. If using MUI, you can leverage `DatePicker` from `@mui/x-date-pickers`. After installing `@mui/x-date-pickers` and a date library (like date-fns), wrap the app with LocalizationProvider in index.tsx:
  ```tsx
  import { LocalizationProvider } from "@mui/x-date-pickers";
  import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
  // ...
  ReactDOM.render(
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <App />
    </LocalizationProvider>,
    document.getElementById("root")
  );
  ```
  Then in the form:
  ```tsx
  import { Controller, useForm } from "react-hook-form";
  import { DatePicker } from "@mui/x-date-pickers";
  const { control, handleSubmit, register } = useForm();
  // ...
  <Controller
    name="date"
    control={control}
    defaultValue={null}
    rules={{ required: true }}
    render={({ field }) => (
      <DatePicker
        label="Date"
        {...field}
        renderInput={(params) => (
          <TextField
            {...params}
            error={!!errors.date}
            helperText={errors.date && "Required"}
          />
        )}
      />
    )}
  />;
  ```
  The `Controller` is used because the DatePicker isn’t a simple input and we need to integrate it with react-hook-form.
- **Hours Input:** Could be a number input. Use `type="number"` on TextField or use MUI’s `TextField` with `InputProps` to allow only numeric. Validation via rules: `{ required: true, min: 0.1, max: 24 }` (assuming hours > 0 and maybe <= 24 for a day).
- **Description:** A multiline TextField for description of work done, optional or required based on business rule.
- **Submit Button:** Make sure it’s disabled while submitting to prevent duplicate submissions. `useForm` provides `formState.isSubmitting` to indicate if a submission is in progress, useful to show a spinner on the button.
- **Handling Submission:** The form’s onSubmit will call our mutation or API. Provide feedback: if success, maybe reset the form (`reset()` function of useForm) and show a success message (“Entry added”). If error, show error.
- **Form Layout:** Use a `<Stack>` or `<Box>` from MUI to space out fields, making it responsive. Possibly grid or paper card around it for better aesthetics.

This form and list combination essentially fulfill the “My Timesheets” page. The employee can add new entries and see their status. They might also edit or delete while pending: implementing edit would require selecting an entry to populate form or a modal to edit it. For brevity, one could skip edit and only allow delete or updating hours before submission.

### **4.7 Building the Project Manager Dashboard for Approvals**

The ApprovalsPage is effectively the manager’s dashboard:

- Show summary counts: e.g., number of pending timesheets. Possibly cards like “Pending: X, Approved Today: Y, Rejected Today: Z”. This is optional; can provide a quick overview using small Card components or just text.
- List pending timesheets (as detailed in 4.4).
- If the manager has a lot of entries, implement filtering (by employee, by date range). This can be additional form controls that filter the data on client-side or via API query params. For example, a dropdown of employees (you’d need an API to get employees list) to filter pending by that employee. For now, assume manageable volume where a simple list is fine.
- Possibly also list recently approved timesheets (for record). Or allow switching views: pending vs all. This can be a toggle or tabs (MUI `<Tab>` component to toggle between “Pending” and “All”). “All” could call a different endpoint (maybe GET /api/timesheets with a query param or a different action for managers that returns everything).
- Use MUI components to make it look like a dashboard: maybe a `Container` with some spacing, a heading “Timesheet Approvals”, etc.

When an approval action is taken:

- We already covered API call and removing from list.
- Consider optimistic UI: we might remove the entry from UI immediately before API responds, then if API fails, push it back. But given the operation is quick, it’s fine to wait for success then refetch or update list.
- Use a dialog for confirmation: When clicking Approve or Reject, open a dialog (`Dialog` component) that asks “Confirm Approve this timesheet?” and optionally input a comment for rejection. If approve, comment might not be needed. This improves UX by preventing accidental clicks.

### **4.8 Frontend Testing (Unit Tests for Components)**

While building the frontend, consider testing:

- Use **React Testing Library (RTL)** and **Jest** for component tests. For example, test that the Login form calls the login function when submitted with valid data, and displays errors when fields are empty (simulate user typing and clicking).
- Test that a protected route redirects to login if not authenticated (this can be done by rendering `<RequireAuth>` with context not providing a user, and using RTL’s `history` to check navigation).
- Snapshot tests for components like Layout to ensure UI doesn’t drastically change unexpectedly.
- If time permits, integration tests using **Cypress** to run the whole app with a fake backend or actual backend. With the app running (maybe in a test environment), Cypress can automate a browser: log in, add a timesheet, verify it appears, log out, etc. End-to-end tests are highly beneficial in catching issues in the integration between frontend and backend. (For advanced devs, this might be something they set up themselves; we highlight it as continuous improvement in section 8).

Now that the frontend is built, we will ensure it connects to the backend securely via CORS and any required configurations, then move on to deploying the application on Azure.

---

## 5. **Integrating React and .NET Core**

This section addresses how to integrate the frontend and backend seamlessly, especially regarding cross-origin resource sharing (CORS), authentication state management across the two, and any nuances in connecting the React app to the .NET API.

### **5.1 Setting up CORS Policies**

Since our React app runs on a different origin (http://localhost:3000) than the API (http://localhost:5000) during development, the browser will block requests unless CORS is enabled on the API. We need to configure .NET Core to allow our frontend.

In the ASP.NET Core backend:

- **Add CORS services** in Program.cs:
  ```csharp
  var MyAllowSpecificOrigins = "_myAllowSpecificOrigins";
  builder.Services.AddCors(options =>
  {
      options.AddPolicy(name: MyAllowSpecificOrigins,
          policy  =>
          {
              policy.WithOrigins("http://localhost:3000")
                    .AllowAnyHeader()
                    .AllowAnyMethod();
          });
  });
  ```
  This creates a policy named `_myAllowSpecificOrigins` which allows the origin of our React dev server. We allow any header (so Authorization header passes through) and any method (GET, POST, etc.). In production, you might allow only specific methods, but generally API will support various methods.
- **Use CORS** in the HTTP pipeline:
  ```csharp
  var app = builder.Build();
  app.UseCors(MyAllowSpecificOrigins);
  // ...other middleware like app.UseAuthentication(); app.UseAuthorization(); app.MapControllers();
  ```
  Place `UseCors` before `UseAuthentication`/`UseAuthorization` to ensure preflight requests (OPTIONS) are handled properly and don’t interfere with auth middleware ordering ([Enable Cross-Origin Requests (CORS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cors?view=aspnetcore-9.0#:~:text=builder.Services.AddCors%28options%20%3D,policy)).
- This global policy will apply to all endpoints. We could also use `[EnableCors("MyPolicy")]` on controllers if we wanted selective enabling. But typically, in a SPA scenario, we allow the whole domain of the frontend.
- Verify CORS works: If you try calling an API from React without this, you’d see a CORS error in the browser console. After enabling, those errors should disappear and network calls succeed, with appropriate `Access-Control-Allow-Origin` headers coming from the API.

**Development convenience:** Alternatively, React’s package.json can specify `"proxy": "http://localhost:5000"` so that CRA’s dev server proxies API calls to backend, avoiding CORS issues in dev. However, configuring CORS is good for readiness in production and clarity.

### **5.2 Connecting Frontend with Backend APIs**

With CORS in place, the integration mostly involves using the correct URLs and handling the authorization token as discussed. Some pointers:

- **Base URL Config:** Ensure that the Axios baseURL or fetch calls in React use the correct base (for dev, likely `http://localhost:5000` or the proxy approach, for prod, it will be an Azure URL). By using environment variables (`REACT_APP_API_URL`), we can easily swap this for production builds.
- **Testing Endpoints from Frontend:** Test each API call from the React application to ensure the expected data flows correctly:
  - Login: enters credentials on UI, after submission, check via React dev tools that auth state is set and localStorage has token, and that the app navigates to the protected route.
  - Fetch timesheets: after login as employee, ensure the network call to `/api/timesheets` returns data (you might need to have seeded data or allow adding new entries and then they appear).
  - Approve: as manager user in UI, approve an entry, ensure the API call is made with status 200 and the UI updates (the entry disappears from pending list).
- **Common Pitfalls:**
  - If the JWT is not sent, likely the Axios interceptor isn’t set or the token isn’t in storage. Use browser devtools > network to inspect the request headers.
  - If you get 401 on every request, possibly the JWT validation in .NET fails – check that the token from login is indeed included and not expired. Also, the `Issuer` and `Audience` in token must match those expected by API. If you use the same values in config for both issuing and validating, this should be fine.
  - If a user logs out, ensure to remove the token. If they log in as a different user, the old token should not remain.

### **5.3 Handling Authentication State Between Frontend and Backend**

This refers to maintaining the user’s logged-in session:

- Our backend is stateless (no sessions, just token validation on each request). The frontend holds the token, so _frontend is the source of truth for auth state_. This means:
  - The user’s “session” lasts as long as the token is valid and present on client. If the token expires (we set it to 60 minutes in config), any further API calls return 401. We should handle that – perhaps auto logout or refresh logic. A simple approach: when Axios interceptor catches a 401, we can redirect to login with a message “Session expired, please log in again.” For a more advanced approach, implement refresh tokens: issue a long-lived refresh token in an HttpOnly cookie and short-lived JWTs, but this complicates the flow and is not necessary for an initial implementation.
- **Persisting Login:** As mentioned, store token in localStorage and on app load, retrieve it. Also store user info (maybe in localStorage too as JSON). Alternatively, on app load if token exists but no user info, call an endpoint like `/api/auth/me` that returns current user based on token. This verifies token and provides fresh data. Many apps do this to verify that the token is still valid and get any updated user info.
- **Logout Flow:** On logout button click (in Layout component earlier), we do:
  - Remove token from localStorage.
  - Clear global state (AuthContext or Redux store).
  - Redirect to login (or homepage which then goes to login if no user).
  - On the backend, since we use JWTs, there’s no server-side session to clear. However, one consideration: if using refresh tokens or if wanting immediate invalidation, you might have a token blacklist or track a token ID server-side, but again, that’s beyond a basic JWT usage.
- **Role-based Rendering:** Ensure that if a user is not a manager, they cannot even manually navigate to /approvals route. The `RequireAuth` could check user role if we pass a required role prop. Or simply, on ApprovalsPage, use `useAuth` and if `user.role !== 'Manager'`, perhaps show a message or redirect. Even if they somehow see the page, the API calls would fail (403) so security is not compromised, but user experience would be confusing.
- **Edge Cases:**
  - If token expires while user is on app, their next API call fails. We should catch 401 and handle gracefully – perhaps show a message “Session expired, please log in” and then logout.
  - If user’s role changes (not likely in our scenario at runtime), their token would not reflect new role until re-login (since role is in token claims). This is acceptable.
  - If the backend is down, show an error to user “Server is unreachable, try again later” by catching Axios network errors.

By properly managing the token on client and verifying on server, we keep the auth flow robust and secure.

At this point, we have a fully functional application running locally. Next, we’ll tackle how to deploy this application to Azure.

---

## 6. **Deployment on Azure**

Deploying to Azure involves publishing the .NET Core API to Azure App Service (or Azure Container), the React app to Azure Static Web Apps (or a storage blob or App Service), and setting up a MySQL database in Azure. We also consider CI/CD pipelines for automated deployment.

### **6.1 Setting up Azure App Services for Hosting the Backend**

**Azure App Service** is a platform for hosting web applications (supports .NET, Node, etc.) as a managed service. We’ll host our .NET Core API here.

Steps to deploy the .NET Core API:

1. **Azure Account & Subscription:** Ensure you have an Azure subscription. Log in to Azure Portal (portal.azure.com).
2. **Create a Resource Group:** (Optional but good practice) In Azure, create a Resource Group (e.g., “TimesheetAppRG”) to contain all related resources (App Service, DB, etc.).
3. **Create App Service (Web App):** In Azure Portal, create a new resource: _Web App_. Choose a name (globally unique, e.g., “timesheet-api-username”), runtime stack = .NET (choose the version, e.g., .NET 8), and OS (Windows or Linux). Linux with .NET is common for new apps. Choose a pricing plan (start with Free or a low-tier for testing).
   - Alternatively, you can create via Azure CLI:
     ```bash
     az webapp create --resource-group TimesheetAppRG --plan MyPlanName --name timesheet-api-username --runtime "DOTNET|8-lts"
     ```
     (This assumes an App Service Plan "MyPlanName" created via `az appservice plan create`).
4. **Configure Settings:** Once Web App is created, go to its settings:
   - Under _Configuration_, add connection strings and environment variables. For example, add a Connection String named `DefaultConnection` with your MySQL connection (we’ll set up MySQL in Azure in section 6.4). Mark it as type MySQL or Custom (Azure treats connection strings specially – in .NET, these can be accessed via `Configuration.GetConnectionString` automatically if named "DefaultConnection"). Also add the JWT settings (Key, Issuer, etc.) as app settings if needed (matching names in appsettings). Note: Azure App Service environment variables override appsettings, and `Configuration["Jwt:Key"]` will fetch from these if set.
   - If using appsettings.Production.json, you can deploy that, but easier is to rely on Azure config for secrets.
5. **Publish the App:** There are multiple ways:

   - **VS Code Azure Extension:** If you installed Azure App Service extension, you can right-click on the project folder or use the command palette: "Azure App Service: Deploy to Web App...", then select your subscription and the created Web App. It will build and deploy your app.
   - **GitHub Actions:** Azure can generate a GitHub Actions workflow to build and deploy on push to main. In the Azure Portal Deployment Center for your web app, choose GitHub and have it setup the workflow. The YAML (similar to [49]) will checkout code, setup .NET, build and publish, then use `azure/webapps-deploy` action with your publish profile secret. You’ll need to store the publish profile from Azure (download from the web app Overview blade) as a GitHub secret `AZURE_WEBAPP_PUBLISH_PROFILE`. The sample GitHub Actions YAML in [49] shows how to structure it – building, then deploying via the publish profile credentials.
   - **Manual Publish:** You can run `dotnet publish -c Release` locally, then use Azure CLI or portal to zip deploy. For instance:
     ```bash
     dotnet publish -c Release -o publish_output
     az webapp deploy --resource-group TimesheetAppRG --name timesheet-api-username --src-path publish_output
     ```
     Or use `az webapp deployment source config-zip` with a zip of the publish_output.

   Using CI/CD (GitHub Actions) is recommended for an “advanced” workflow – it ensures every push can deploy, and you maintain Infrastructure as Code.

6. **Verify API on Azure:** After deployment, go to `https://<yourapp>.azurewebsites.net/api/timesheets` (for example) in the browser or use curl. It might show an authentication error if no token – meaning it’s running. Or deploy a version with at least an open endpoint (like health check) to verify. Azure App Service logs can be viewed in the portal (Log Stream) if something goes wrong (like startup failure due to misconfig).

### **6.2 Deploying the React Frontend to Azure Static Web Apps**

Azure Static Web Apps is a service specifically for hosting SPAs and static sites, with global distribution and integrated CI/CD (GitHub Actions). Alternatively, one can use Azure Storage as a static site or host it on an App Service as well (using something like create-react-app’s build output). We’ll use Static Web Apps (SWA):

Steps:

1. **Azure Static Web App (SWA) Creation:** In Azure Portal, create a Static Web App. Choose “Other” or specifically React as the framework if prompted (the build will be done via GitHub Action normally). Provide the GitHub repository and branch, and specify the folder where the app lives (`client` if monorepo). Azure will add a GitHub Actions workflow to build the React app (runs `npm install && npm run build`) and deploy it. In creation:
   - App artifact location: `client/build` (that’s where CRA outputs the static files).
   - API location: (optional, if we had an Azure Functions API or something – not in our case because our API is separate). We can leave it or set to none.
   - The Action will then build and deploy your app on push.
   - The result will be a SWA with a domain like `https://nice-name-xyz.azurestaticapps.net`.
2. **Alternate: Azure Storage Static Site:** If not using SWA, you could upload the `build` directory to an Azure Blob Storage static website or even serve the files from the .NET app (but mixing concerns is less ideal). With storage: create a Storage Account, enable static website hosting, upload files. However, SWA provides free SSL and easier CI/CD for SPAs.
3. **Configuration:** After deploying React app, you need it to communicate with the API. If your API is at `https://timesheet-api-username.azurewebsites.net`, the React app should call that. Ensure `REACT_APP_API_URL` is set accordingly during build. With Static Web Apps, you define any environment variables in the SWA configuration (if using Azure DevOps pipeline or in workflow file). Alternatively, you might hard-code the production API URL in your app, but that’s not flexible. The SWA action allows specifying `env: STATIC_WEB_APP_API_TOKEN` for Azure Functions backends, but for our external API, just ensure the base URL is known to the frontend.
   - If both the SWA and the API were under the same domain (SWA can proxy to Azure Functions or other APIs if configured with routes), but that’s advanced usage. More straightforward: treat them as separate, and the React app will call the Azure Web App domain for API.
   - **CORS in Production:** Update the CORS policy on the .NET API to allow the SWA’s domain (e.g., `https://nice-name-xyz.azurestaticapps.net`) in addition to localhost. Or set `WithOrigins("*")` temporarily if you want to allow all (not recommended for production security, but many internal APIs might allow all origins if they expect only specific clients anyway). Better to list the known domain(s).
4. **Custom Domain (optional):** If you have a custom domain, you could map it to both the SWA and the API app. That’s beyond scope, but Azure allows binding custom domains with managed certificates.

**CI/CD Pipeline for SWA:** When SWA resource is created via Azure portal with GitHub link, the GitHub Actions YAML is added to your repo (under `.github/workflows`). It will look something like:

```yaml
- uses: actions/checkout@v3
- uses: actions/setup-node@v3
- name: Build And Deploy
  run: |
    npm install
    npm run build
  env:
    STATIC_WEB_APP_API_TOKEN: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
```

Azure automatically sets the token secret. This action will auto-deploy any changes in the client folder to the SWA.

### **6.3 Configuring CI/CD Pipelines (GitHub Actions or Azure DevOps)**

We touched on GitHub Actions. Let’s summarize:

- **GitHub Actions for API:** Use the official Azure Web App deploy action. Or use **Azure DevOps** pipelines if the organization uses that, but the principle is similar: build .NET, publish artifact, then use an AzureWebApp task to deploy.
- **GitHub Actions for Static Web App:** It’s mostly automated by Azure. If doing manually: after build, you could use Azure CLI to upload or use Azure REST API. The provided GitHub Action is easier.
- **Environment Separation:** Possibly have separate dev/test/prod environments with different Azure resources and branches. That adds complexity but advanced devs may have multi-stage pipelines. Start with a single production environment triggered on main branch push. Use app settings for differences (like API URL).
- **Secrets Management:** Use GitHub Secrets or Azure Key Vault to store secrets like JWT signing key or DB passwords if needed in pipeline (for example, if pipeline seeds database or runs migrations). Typically, we avoid pushing secrets in code or config.

**Continuous Deployment Verification:** After setting pipelines, do a test commit (like change a UI text) and push to main. The GitHub Actions should trigger, build, and deploy both backend and frontend. Check Azure to see if changes reflect.

### **6.4 Setting up MySQL Database on Azure**

Azure offers **Azure Database for MySQL** (both single server and flexible server options). For a production scenario, we’d use that to avoid hosting MySQL ourselves.

To set up:

1. **Create Azure Database for MySQL:** In Azure Portal, create a new Azure Database for MySQL (select flexible server if available, as single server may be legacy). Choose a name, region, admin username and password. Choose a compute tier (Basic for dev).
2. **Networking:** For ease, allow public access from Azure services and maybe your local IP (so you can manage remotely). If using flexible server, you can put it in same VNet as App Service for better security.
3. **Configure DB:** Once created, get the connection string info. It will have a server name like `yourserver.mysql.database.azure.com`. The admin user is like `admin@yourserver` (for single server) or just `admin` (for flexible with hostname separate).
   - Create the `TimesheetDb` schema in this server. Azure’s MySQL lets you connect with tools. For quick route, use the Azure Cloud Shell or MySQL Workbench locally:
     ```
     mysql -h yourserver.mysql.database.azure.com -u admin@yourserver -p
     CREATE DATABASE TimesheetDb;
     CREATE USER 'timesheet_user'@'%' IDENTIFIED BY 'StrongPassword!';
     GRANT ALL ON TimesheetDb.* TO 'timesheet_user'@'%';
     ```
     (Alternatively, use the admin user in connection string and skip creating a separate user to simplify.)
4. **Configure App Service to use Azure MySQL:** Update the connection string in App Service settings. Use the format Azure expects: e.g.,
   ```
   DefaultConnection = Server=yourserver.mysql.database.azure.com;Database=TimesheetDb;User=timesheet_user@yourserver;Password=StrongPassword!;SslMode=Required;
   ```
   (Adding `SslMode=Required` because Azure MySQL requires SSL by default for connections). Azure Portal has a Connection Strings section – since this is MySQL, you might also flip it to “MySQL” type which might set some environment variables like `MYSQLCONNSTR_DefaultConnection`. .NET’s config builder does read those with special prefixes.
5. **Apply EF Migrations on Azure DB:** Our application on startup can auto-apply migrations (you can call `context.Database.Migrate()` in Program.cs if you want code-first auto updates). If not, you can run `dotnet ef database update` manually pointing to Azure (maybe by setting connection string env var locally then running). Or even better, incorporate migration step in CI/CD (like a script step to run `dotnet ef database update` against the Azure DB). But careful: running migrations from a build agent might need firewall access to DB. Simpler for now: after deploying API, do a one-time `update-database`.
   - Alternatively, use Azure Data Studio or MySQL Workbench to run the SQL from the migration .sql script.
6. **Test DB Connection:** The .NET API logs (App Service > Log Stream) will show if it connects or any errors. If it can’t connect, check firewall settings on Azure MySQL (maybe add App Service’s outbound IP). If it connects but invalid login, check username format (Azure requires @server suffix for user in connection string). Once EF runs, the tables should be in the Azure MySQL. Check with Workbench to see if tables created.

Now the backend is connected to an Azure MySQL, and the connection string is stored securely in Azure (not in code). The fronted calls the backend, which interacts with the DB – full cloud operation.

### **6.5 Monitoring Logs and Performance**

Azure provides several tools:

- **App Service Logging:** Enable Application Logging (Filesystem) for quick debugging in Azure (this can be done in Azure Portal > Web App > App Service Logs, then use Log Stream to view). You can also integrate Serilog or other logging frameworks to log to console, which App Service can capture.
- **Application Insights:** Highly recommended for production. It’s an Azure service to monitor performance, exceptions, requests, etc. You can enable it in the Web App (there’s an option “Enable Application Insights” that might have been offered when creating the app, or can be done after by linking an App Insights resource). Then add the Application Insights SDK to the .NET app. For example, add `Microsoft.ApplicationInsights.AspNetCore` package and do `builder.Services.AddApplicationInsightsTelemetry();`. This will automatically collect incoming request metrics, dependency calls (like to MySQL), exceptions, etc., which you can view in Azure Portal. It’s very useful for advanced troubleshooting.
- **Performance Monitoring:** App Insights has a Performance tab to see which requests are slow, and even Application Map to see if DB calls are slow.
- **Front-end Monitoring:** Static Web Apps doesn’t have built-in monitoring like App Insights by default. But you can use Google Analytics or Azure Application Insights via the JavaScript SDK if needed to track page views, etc.

**Scaling Considerations:** If heavy load is expected:

- Scale up the App Service Plan (e.g., more CPU/memory or enable autoscale).
- Azure MySQL: choose appropriate tier (Basic is for dev/test, not performance). Use General Purpose or Memory Optimized for production loads.
- Static Web App: it auto-scales globally (it’s CDN-based for static files). If using a different approach (like hosting React in App Service), ensure compression and caching is on.

We’ve deployed and set up monitoring, covering the full lifecycle. Next, we’ll discuss adding advanced features and optimizations beyond the basic functionality.

---

## 7. **Advanced Features and Optimization**

Beyond the core implementation, advanced requirements often include role-based access control, performance enhancements (caching), comprehensive logging, and supporting localization & accessibility.

### **7.1 Implementing Role-Based Access Control (RBAC)**

Our app already distinguishes roles (Employee vs Manager) in a basic way: through JWT claims and `[Authorize(Roles="...")]` in the API and conditional UI in frontend.

For more complex RBAC:

- You might introduce more roles (Admin, etc.), or even dynamic roles/permissions (like using Policy-based authorization in ASP.NET Core). For example, you could define a policy "CanApproveTimesheets" and have `[Authorize(Policy="CanApproveTimesheets")]` instead of just roles, which could allow more granular control (e.g., maybe only senior managers can approve over a certain hour limit, etc.). ASP.NET Core’s policy system allows you to write custom handlers that check claims or other data.
- If using **ASP.NET Core Identity**, you’d get built-in management of roles and users. Identity would bring in tables like AspNetUsers, AspNetRoles, etc., but since we did custom, continuing custom is fine.
- **Front-end RBAC:** If the application grows (say an admin page to manage users), you might want a centralized definition of what each role can see/do in the UI. Perhaps an object mapping roles to allowed routes or menu items. For a handful of roles, simple checks suffice.
- **Testing RBAC:** Write tests to ensure an Employee JWT cannot call manager endpoints (we did logically and can test via integration tests with a token without the claim). Also test that a Manager sees only allowed UI options.

### **7.2 Caching and Performance Improvements**

Possible performance enhancements:

- **Backend Caching:** Use in-memory caching for frequent reads, such as reference data or queries that don’t change often. For example, if managers repeatedly fetch the same pending list and the list is heavy, caching that result for a short interval could help (though pending list changes when approvals happen). Or caching user info in memory so you don’t query DB for user on every request (we haven’t been doing that explicitly yet, but if some endpoints need to load user details for each call, caching them for a few minutes can save DB calls). Use `IMemoryCache` via dependency injection and cache data appropriately.
  - We could implement a caching in the service layer, e.g. `GetPendingTimesheets()` could try retrieving from cache first. For distributed cache (multi-instance app), Azure Cache for Redis could be used, but that’s overkill for small scale.
- **Frontend Performance:**
  - Use React’s production build which does tree shaking and minification. Ensure source maps are off for production (or restricted). The Static Web Apps action by default does production build. Check Lighthouse or browser audits to see if there are any obvious improvements (like large bundle size – if so, consider code splitting by lazy loading some pages).
  - Use caching on client: our React Query already caches data. Also, enabling browser caching for static files (SWA should auto-assign caching headers with content hashes).
  - Virtualize long lists if needed (not needed unless hundreds of timesheets in one view – then could use `react-window` or similar for performance).
- **Database Indexing:** Ensure the MySQL database has proper indexes. EF Migrations by default will create primary keys and foreign keys. But if you query by `UserId` often in TimesheetEntries, an index on that column is beneficial. You can use EF’s Fluent API or annotations to add indexes. For example:
  ```csharp
  modelBuilder.Entity<TimesheetEntry>()
      .HasIndex(t => new { t.UserId, t.Status });
  ```
  This might help for queries where you filter by user and status (like an employee filtering only pending).
- **Load Testing:** It might be wise to test the app with a load test (e.g., JMeter or Azure Load Testing) to identify bottlenecks. This is beyond coding, but an advanced step.

### **7.3 Logging and Error Handling Best Practices**

We did some basic error handling (return 401, 403 etc. appropriately). To further improve:

- **Global Exception Handling:** In ASP.NET Core, use `app.UseExceptionHandler("/error")` to catch unhandled exceptions and return a standard response (possibly JSON with an error message and correlation ID). Or write a custom middleware as referenced in [56], which catches exceptions and logs them. The idea is the API should never crash without a controlled response.
  - For example, wrap all controller logic in try-catch might be tedious, better to rely on a global handler. We can create `ExceptionHandlingMiddleware` (like in [56], which logs and returns a generic error) or use the built-in exception handler middleware:
    ```csharp
    if (!app.Environment.IsDevelopment())
    {
        app.UseExceptionHandler("/error"); // in production, forward to a generic error handler
    }
    ```
    Then create an ErrorController with `[Route("/error")]` that returns a generic message from `ProblemDetails`.
- **Structured Logging:** Use Serilog or similar to log structured data (like user id, action performed, etc.). For instance, log an information entry when a timesheet is submitted: “User 5 submitted timesheet 123 for 8 hours on 2025-02-13.” This creates an audit trail.
  - Serilog can direct logs to console (which Azure picks up) or to files, or even to Azure Application Insights directly. But built-in Microsoft.Extensions.Logging also can send to Application Insights if configured.
- **Frontend Error Handling:**
  - Use Error Boundaries in React for any uncaught errors in the component tree to avoid a white screen. Create an ErrorBoundary component that catches errors and displays a friendly message.
  - Handle promise rejections from Axios: we did with try/catch around each call. Possibly add a global error interceptor to catch any unhandled errors and maybe show a toast “An error occurred”.
  - Logging front-end errors: Could send them to a logging endpoint or third-party (Sentry, etc.) if needed.
- **User Feedback:** Ensure that any error that happens (e.g., failing to load data due to network) is conveyed to the user in a friendly manner. E.g., show a message “Failed to load timesheets, please check your connection or try again” instead of just a blank table.

### **7.4 Implementing Localization and Accessibility**

**Localization (i18n):**  
If the app needs to support multiple languages (English, Spanish, etc.), plan for internationalization:

- On the frontend: Use libraries like **react-i18next** or **react-intl**. For example, react-i18next provides a hook to load translations and a `<Trans>` component or `t` function to translate keys. You’d create JSON files for each language. The advanced developer likely knows about this, but we mention: structure your UI text to be translatable, e.g., instead of hardcoding “Login”, use `t('login')`.
- Provide a language switcher if needed. Or detect browser language. For right-to-left languages, ensure MUI supports (it does if configured).
- The backend might also need localization (for example, if sending emails or error messages that should be in user’s language). ASP.NET Core has localization support (resource files, IStringLocalizer). But likely, most text is on the UI side. Perhaps the approval comments or descriptions are user-entered so they remain as entered.

**Accessibility (a11y):**  
Ensure the app is accessible:

- Use semantic HTML elements where possible (MUI components under the hood use proper roles, but we should verify with tools).
- Use ARIA attributes if needed for custom controls. For instance, the approval buttons should have aria-label like “Approve timesheet for John Doe on 2025-02-13” to give context to screen readers, or ensure the context is clear via surrounding text.
- All form inputs have labels (MUI’s TextField associates label properly).
- Contrast of text and background meets WCAG guidelines (MUI default theme mostly does, but custom colors should be checked).
- Tab order should be logical (the layout code should reflect logical ordering, which usually it does).
- Test with a screen reader or at least using keyboard navigation (ensure you can navigate with Tab, activate buttons with Enter/Space, etc.). Use `aria-*` attributes to improve where default semantics aren’t enough.
- Tools: use Lighthouse or Axe browser extension to audit accessibility. They will point out missing alt attributes, etc.

By addressing localization and accessibility, we make the app usable to a broader audience and compliant with standards.

We have now covered enhancements that an advanced implementation might consider. Finally, we’ll cover testing and maintenance strategies.

---

## 8. **Testing and Maintenance**

Building the app is one milestone; ensuring its quality and maintainability long-term is another. We’ll discuss testing strategies (unit, integration, end-to-end) and how to maintain the project with continuous improvements.

### **8.1 Writing Unit Tests for Backend and Frontend**

**Backend (ASP.NET Core) Unit Tests:**

- Use xUnit (or NUnit/MSTest) for writing tests. The typical approach is to test services and maybe controllers in isolation using mock dependencies. Since we somewhat kept logic in controllers, one might refactor to have a service layer that controllers call, to make it easier to unit test the logic without spinning up MVC.
- Example test: Testing the `ApproveTimesheet` logic. Could instantiate a fake `TimesheetContext` – you can use an in-memory database provider for EF Core for tests (UseInMemoryDatabase). Seed it with a pending timesheet, then call the function to approve, then assert the status changed and an approval record created.
- Use **Moq** library to mock any interfaces (if you had an interface for email sender, etc.).
- Also test validation logic: if `ApproveTimesheet` is called on an already approved entry, does it throw or return appropriate error? You’d simulate that in a test.
- Test the Auth Controller’s login: possibly by mocking a `IUserRepository` that returns a known user for given credentials, then assert that a token is returned. (Though issuing a token involves using actual JWT library – you might just ensure the structure of response).
- For any custom utilities, test them.

**Frontend (React) Unit Tests:**

- Use Jest and React Testing Library (RTL).
- Write tests for components: e.g., **LoginPage**:
  - render it with a dummy AuthContext provider that has a mock `login` function. Simulate user typing into email and password fields (using RTL’s `fireEvent.change` or `userEvent.type`) and clicking submit. Then assert that `login` was called with correct values. Also test required field validation: submit with empty fields should show error messages and not call `login`. This ensures our form validation works.
- **TimesheetPage**:
  - We might mock the data fetching hook. If using React Query, one way is to wrap in a QueryClientProvider with a special test QueryClient that’s configured with initial data. Or abstract the data fetching into a custom hook (like `useTimesheets`) which can be mocked.
  - Alternatively, mount the component and intercept the Axios call via MSW (Mock Service Worker) to return fake data. This is integration-test like, but done in Jest environment.
  - Ensure that when clicking "Add Entry" button, if hours is negative, an error appears (test validation).
- **ApprovalsPage**:
  - Simulate clicking approve on a pending item and ensure the item is removed from list (you might inject a mock context or service that simulates that).
- **Redux slices**: if using Redux, test reducers: dispatch an action and check new state.
- Snapshots: Use `renderer.create` (from react-test-renderer) to create snapshots of components for baseline UI (less critical but can catch accidental changes).

**Test execution**: Run `dotnet test` for backend tests. Run `npm test` for frontend (which uses Jest by default to watch tests). In CI, these should run on every push; ensure pipelines run tests before deploy, and if tests fail, do not deploy.

### **8.2 Setting Up Automated End-to-End Testing**

While unit/integration tests cover logic, end-to-end (E2E) tests ensure the whole system works from the user’s perspective:

- Use **Cypress** or **Playwright**. For a React app, Cypress is popular for E2E in JS. Playwright has a .NET version as well that could integrate with testing the web app, as the MS docs hint.
- **Cypress Setup:** Add Cypress to dev dependencies (`npm install cypress --save-dev`). Write tests that run the app (you can run against a deployed test environment or run local – but local requires starting the dev servers, which Cypress can manage via `start-server-and-test` or concurrently).
  - Example test:
    - Visit the login page,
    - type valid credentials (you might need to seed the database or have a known user; perhaps run against a local instance with known seed data, or directly manipulate DB in test).
    - Click login,
    - assert redirect to /timesheets,
    - assert that the page shows "No entries" initially (if none).
    - Fill the form to add timesheet, submit, assert the entry appears in the list.
    - Log out, assert redirect to login.
  - Another test: login as manager, go to approvals page, approve an entry, ensure it disappears.
- **Headless vs headed**: In CI, you run Cypress in headless mode. Configure GitHub Actions to run `npm run build` then `npm ci` then `npx cypress run` (if you have a server, you might start it with the backend stubbed or using the actual backend in a staging slot).
- Alternatively, use Playwright .NET to write a C# test that launches a browser, navigates to the React app and performs actions. The benefit is you can integrate with the backend more easily within the same test code if needed. But using the same language as the frontend for E2E (JS for Cypress) can be simpler.

E2E tests catch integration issues like mismatched API responses and UI expectations, CORS issues, etc., that unit tests might miss. They can be flaky if not written carefully, so ensure proper waiting for elements and stable test data.

### **8.3 Continuous Improvement Strategies**

Maintenance of the project includes:

- **Code Reviews:** All changes going into main should be code-reviewed by peers. This ensures consistency with best practices and catches potential issues early.
- **Refactoring:** As new features get added, continuously refactor to avoid code smells (duplicated code, too large functions, etc.). For example, if you find TimesheetPage and ApprovalsPage share logic to render a list of entries, factor that into a component.
- **Dependency Updates:** Regularly update NuGet packages and npm packages to get security patches and improvements (be cautious with major version changes). Tools like Dependabot (GitHub) can automate PRs for updates. Run tests after updates to catch breakages.
- **Monitoring and Feedback:** Use monitoring (App Insights) to see if any errors occur in production that weren’t caught. Also gather user feedback (maybe managers want an export to Excel feature, etc.) and plan those enhancements.
- **Performance Tuning:** If usage grows, profile the application. Perhaps add an index, or move heavy operations to background jobs. For instance, if approval should trigger an email, using a queue and background worker would be better than making the user wait.
- **Security Audits:** Ensure OWASP top 10 are considered – e.g., JWT is properly secure, password storage is hashed (we should ensure using a strong hash algorithm, at least use something like BCrypt via a library, or ASP.NET Identity which handles it), validate inputs (EF Core parameterizes queries by default which prevents SQL injection; but e.g., if you ever do raw SQL, use parameters). Also consider adding anti-forgery if using cookies, but with JWT it's not needed.
- **Documentation:** Maintain good documentation for the project. This guide can serve as documentation, but also have a README with setup steps, environment setup for new developers, etc.
- **Automate Repetitive Tasks:** For example, automating database migrations on deployment, or nightly jobs (like archiving old timesheets) if needed using Azure WebJobs or Functions.

Finally, encourage a culture of writing tests for new features (Test-Driven Development if possible), which for advanced devs can be a natural part of development. This ensures each new feature comes with tests guarding against regression.

---

By following this guide from setting up the project, through development steps, to deployment and maintenance, an advanced developer should have a **complete implementation reference** for a Timesheet application using **React, .NET Core, and MySQL** on Azure. The application is structured with best practices in mind, ensuring clarity, security, and scalability.

Now, let’s briefly recap our implementation with references to the sources that informed our best practices and choices:

- We set up the TypeScript React project and VS Code environment ([TypeScript - Material UI](https://mui.com/material-ui/guides/typescript/?srsltid=AfmBOopexk0Vf6IZzfmNq5dOuBQ2DP1ZUeWkaAcXtTJI5XyyHU50sZT3#:~:text=%7B%20,true%20%7D)), ensuring strict type checking for quality.
- Configured EF Core with MySQL using Pomelo library, enabling us to connect to MySQL effectively.
- Implemented JWT authentication in .NET, following recommended validation parameters (issuer, audience, lifetime, signing key).
- Used `Authorize` attributes to enforce role-based security easily ([JWT Validation and Authorization in ASP.NET Core - .NET Blog](https://devblogs.microsoft.com/dotnet/jwt-validation-and-authorization-in-asp-net-core/#:~:text=So%2C%20a%20roles,to%20APIs%20and%20work%20immediately)).
- Used Axios interceptors in the frontend to include auth tokens, as commonly done for JWT auth.
- Chose React Query for data fetching due to its strengths in caching and syncing server state.
- Enabled CORS in ASP.NET Core to allow the React app to communicate with the API ([Enable Cross-Origin Requests (CORS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cors?view=aspnetcore-9.0#:~:text=builder.Services.AddCors%28options%20%3D,policy)).
- For Azure deployment, followed Microsoft’s guides to publish the .NET app and configured CI/CD with GitHub Actions.
- Emphasized using Application Insights for logging and monitoring in .NET, as per Azure’s guidance.
- Ensured we considered accessibility, aligning with React’s support for standard HTML and ARIA for accessible rich internet apps ([Accessibility – React](https://legacy.reactjs.org/docs/accessibility.html#:~:text=React%20fully%20supports%20building%20accessible,by%20using%20standard%20HTML%20techniques)).

With these practices and references, the timesheet application is robust and ready for production use, while also being maintainable and extensible for future requirements.
