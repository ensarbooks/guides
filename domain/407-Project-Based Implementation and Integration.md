# Project-Based Implementation and Integration

Now that we’ve discussed advanced techniques in each area, let's put it all together by building a simplified **enterprise application** as a learning exercise. Our example project will be a **Company Management System** that handles employees, departments, and projects. We will outline how to implement this system step-by-step, emphasizing the integration of C# backend logic, ASP.NET Core REST APIs, SQL Server via EF Core, and an Angular frontend. Throughout, we’ll apply the best practices we covered – from clean architecture and design patterns to performance optimizations and security.

## Architecture and Solution Setup

**Clean Architecture Layers**: We will structure the backend solution into distinct layers/projects for maintainability:

- **Domain Layer**: Contains core entities (business objects) and their logic. No external dependencies (no EF Core or ASP.NET here) – just plain C# classes defining Employee, Department, Project, etc., and possibly interfaces for persistence.
- **Application Layer**: Contains business logic and service interfaces. This is where we define use cases (e.g., handling a transfer of an employee to another department, or calculating project statistics). It may also define repository interfaces (e.g., `IEmployeeRepository`) that the domain/business logic will use to retrieve or save data.
- **Infrastructure Layer**: Implements the persistence and other technical details. Here we put the EF Core `DbContext` and repository classes that implement the interfaces from the Application layer. Could also include other services like email senders, file storage providers if needed.
- **API Layer**: The ASP.NET Core Web API project. It references the Application layer (to use business logic) and the Infrastructure layer (to configure it and its DI bindings). It hosts controllers that map HTTP requests to application layer calls, and formats responses (using DTOs).

This separation follows the **Dependency Inversion Principle** – inner layers (Domain/Application) do not depend on outer (Infrastructure/API). Only outer layers depend on inner layers. This makes it easier to test business logic (we can provide fake repositories), and allows swapping tech (for instance, replacing EF Core with another DB tech) with minimal changes to core logic.

**Entity Design (Domain Layer)**:

```csharp
public class Department
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<Employee> Employees { get; set; } = new();
}

public class Employee
{
    public int Id { get; set; }
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public int DepartmentId { get; set; }
    public Department Department { get; set; } = null!; // Navigation property

    public string FullName => $"{FirstName} {LastName}";
    // Business logic example: transfer employee to new department
    public void TransferToDepartment(int newDeptId)
    {
        DepartmentId = newDeptId;
        // (Optionally, add any business rules or events, e.g., logging transfer)
    }
}

public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public DateTime Deadline { get; set; }
    public List<Employee> TeamMembers { get; set; } = new();
}
```

We have a many-to-one between Employee and Department (Employee.DepartmentId foreign key), and a many-to-many between Employee and Project (TeamMembers property). EF Core will handle many-to-many via a join table automatically because we used a collection navigation on both sides (Employees have Projects, Projects have Employees). In Domain, we don’t necessarily include the join entity (EF will create it in the model).

**DbContext and EF Configuration (Infrastructure Layer)**:

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<Employee> Employees => Set<Employee>();
    public DbSet<Department> Departments => Set<Department>();
    public DbSet<Project> Projects => Set<Project>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        // Department-Employee one-to-many
        modelBuilder.Entity<Employee>()
            .HasOne(e => e.Department)
            .WithMany(d => d.Employees)
            .HasForeignKey(e => e.DepartmentId)
            .OnDelete(DeleteBehavior.Restrict);
        // Employee-Project many-to-many
        modelBuilder.Entity<Employee>()
            .HasMany(e => e.Projects)
            .WithMany(p => p.TeamMembers)
            .UsingEntity<Dictionary<string, object>>(
                "ProjectAssignment",  // name of join table
                j => j.HasOne<Project>().WithMany().HasForeignKey("ProjectId"),
                j => j.HasOne<Employee>().WithMany().HasForeignKey("EmployeeId"));
        // Add any necessary configurations, e.g., property lengths, indexes
        modelBuilder.Entity<Department>().Property(d => d.Name).HasMaxLength(100);
        modelBuilder.Entity<Employee>().Property(e => e.FirstName).HasMaxLength(50);
        modelBuilder.Entity<Employee>().Property(e => e.LastName).HasMaxLength(50);
        modelBuilder.Entity<Project>().Property(p => p.Name).HasMaxLength(100);
        modelBuilder.Entity<Project>().HasIndex(p => p.Deadline);
    }
}
```

In the above:

- We explicitly configured relationships (though EF could infer them via conventions, being explicit is fine for clarity).
- We named the join table "ProjectAssignment" and specified the foreign keys.
- Set some max lengths and an index on Deadline (imagine we may query projects by deadline often, indexing it for performance).
- We would also configure any seed data if needed (e.g., some initial departments) using `modelBuilder.Entity<Department>().HasData(new Department{Id=1, Name="HR"}, ...);` – and then ensure we add a migration for that.

**Repository Implementation (Infrastructure Layer)**:
We define repository interfaces in Application, for example:

```csharp
public interface IEmployeeRepository
{
    Task<Employee?> GetByIdAsync(int id);
    Task<List<Employee>> GetAllAsync();
    Task<List<Employee>> GetByDepartmentAsync(int departmentId);
    void Add(Employee employee);
    void Remove(Employee employee);
}
```

In Infrastructure:

```csharp
public class EmployeeRepository : IEmployeeRepository
{
    private readonly AppDbContext _context;
    public EmployeeRepository(AppDbContext context)
    {
        _context = context;
    }
    public Task<Employee?> GetByIdAsync(int id)
    {
        // Include Department and Projects if needed for rich data
        return _context.Employees
            .Include(e => e.Department)
            .Include(e => e.Projects)
            .FirstOrDefaultAsync(e => e.Id == id);
    }
    public Task<List<Employee>> GetAllAsync()
    {
        return _context.Employees
            .Include(e => e.Department)
            .AsNoTracking()  // no need to track for read
            .ToListAsync();
    }
    public Task<List<Employee>> GetByDepartmentAsync(int departmentId)
    {
        return _context.Employees
            .Where(e => e.DepartmentId == departmentId)
            .AsNoTracking()
            .ToListAsync();
    }
    public void Add(Employee employee)
    {
        _context.Employees.Add(employee);
    }
    public void Remove(Employee employee)
    {
        _context.Employees.Remove(employee);
    }
}
```

We would similarly implement `DepartmentRepository` and `ProjectRepository` as needed, or use generic patterns if we wanted to reduce repetition.

We might also create a `UnitOfWork` or just use the DbContext as the unit of work. Since our repositories have the context, we can call `await _context.SaveChangesAsync()` in a unit of work implementation or directly in the service that coordinates multiple operations.

**Service/Business Logic (Application Layer)**:
For instance, an `EmployeeService` could have a method to transfer an employee:

```csharp
public class EmployeeService
{
    private readonly IEmployeeRepository _empRepo;
    private readonly IUnitOfWork _unitOfWork;
    public EmployeeService(IEmployeeRepository empRepo, IUnitOfWork uow)
    {
        _empRepo = empRepo;
        _unitOfWork = uow;
    }
    public async Task<bool> TransferEmployeeAsync(int employeeId, int newDeptId)
    {
        var employee = await _empRepo.GetByIdAsync(employeeId);
        if (employee == null) return false;
        employee.TransferToDepartment(newDeptId); // domain logic updates DepartmentId
        // could check if newDeptId exists, etc., (that might involve DepartmentRepo)
        await _unitOfWork.SaveChangesAsync();
        return true;
    }
}
```

Here, `_unitOfWork.SaveChangesAsync()` would simply call context.SaveChangesAsync() under the hood to commit the transaction. The UnitOfWork might be part of a broader context or each repository call uses the same context which is injected (common if using one DbContext per request in DI).

**ASP.NET Core API Controllers (API Layer)**:
We create controllers to expose the functionality via HTTP endpoints. Example `EmployeesController`:

```csharp
[Route("api/[controller]")]
[ApiController]
public class EmployeesController : ControllerBase
{
    private readonly IEmployeeRepository _employeeRepo;
    private readonly IUnitOfWork _unitOfWork;
    public EmployeesController(IEmployeeRepository employeeRepo, IUnitOfWork unitOfWork)
    {
        _employeeRepo = employeeRepo;
        _unitOfWork = unitOfWork;
    }

    [HttpGet]
    public async Task<ActionResult<List<EmployeeDto>>> GetEmployees()
    {
        var employees = await _employeeRepo.GetAllAsync();
        // Map to DTOs
        var result = employees.Select(e => new EmployeeDto {
            Id = e.Id,
            FullName = $"{e.FirstName} {e.LastName}",
            DepartmentName = e.Department.Name
        }).ToList();
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<EmployeeDto>> GetEmployee(int id)
    {
        var e = await _employeeRepo.GetByIdAsync(id);
        if (e == null) return NotFound();
        var dto = new EmployeeDetailsDto {
            Id = e.Id,
            FirstName = e.FirstName,
            LastName = e.LastName,
            DepartmentId = e.DepartmentId,
            DepartmentName = e.Department.Name,
            ProjectIds = e.Projects.Select(p => p.Id).ToList()
        };
        return Ok(dto);
    }

    [HttpPost]
    public async Task<ActionResult<EmployeeDto>> CreateEmployee(CreateEmployeeDto createDto)
    {
        // Model binding and validation ensures createDto is valid as per data annotations
        var employee = new Employee {
            FirstName = createDto.FirstName,
            LastName = createDto.LastName,
            DepartmentId = createDto.DepartmentId
        };
        _employeeRepo.Add(employee);
        await _unitOfWork.SaveChangesAsync();
        // The employee.Id is now populated by the database
        var resultDto = new EmployeeDto {
            Id = employee.Id,
            FullName = $"{employee.FirstName} {employee.LastName}",
            DepartmentName = "" // we may do a lookup for Department name if needed
        };
        return CreatedAtAction(nameof(GetEmployee), new { id = employee.Id }, resultDto);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateEmployee(int id, UpdateEmployeeDto updateDto)
    {
        if (id != updateDto.Id) return BadRequest("ID mismatch");
        var employee = await _employeeRepo.GetByIdAsync(id);
        if (employee == null) return NotFound();
        // Update fields
        employee.FirstName = updateDto.FirstName;
        employee.LastName = updateDto.LastName;
        employee.DepartmentId = updateDto.DepartmentId;
        await _unitOfWork.SaveChangesAsync();
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteEmployee(int id)
    {
        var employee = await _employeeRepo.GetByIdAsync(id);
        if (employee == null) return NotFound();
        _employeeRepo.Remove(employee);
        await _unitOfWork.SaveChangesAsync();
        return NoContent();
    }
}
```

In the above:

- We used DTO classes (`EmployeeDto`, `EmployeeDetailsDto`, `CreateEmployeeDto`, `UpdateEmployeeDto`) for request/response shapes. This decouples the API contract from the internal Entity shape (e.g., we might not expose all fields directly).
- We return `NotFound()` (404) if an employee isn’t found, and `BadRequest()` (400) for an ID mismatch scenario.
- On create, we return `CreatedAtAction` with 201 status and Location header pointing to the new resource.
- On update/delete success, returning 204 No Content is a common pattern (the client can assume success with no additional body).

We should also add appropriate `[Authorize]` attributes if auth is required for these endpoints. For example, maybe only logged-in users can access them, or certain roles can create/update (depending on requirements). For now, assume any authenticated user can use them, but one could add `[Authorize]` on the class to require a valid token, and further `[Authorize(Roles="Admin")]` on certain methods if needed.

**Authentication & Authorization**:
We integrate JWT Bearer authentication:

- In `Startup` (or Program for .NET 6 minimal hosting), configure JWT:
  ```csharp
  services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
          .AddJwtBearer(options =>
          {
              options.TokenValidationParameters = new TokenValidationParameters
              {
                  ValidateIssuer = true,
                  ValidateAudience = true,
                  ValidateLifetime = true,
                  ValidateIssuerSigningKey = true,
                  ValidIssuer = "YourApp", // should match what you put in token
                  ValidAudience = "YourAppUsers",
                  IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("SuperSecretKey12345"))
              };
          });
  services.AddAuthorization();
  ```
- Create an `AuthController` with a `[HttpPost("login")]` that validates user credentials (for simplicity, maybe check against a hardcoded user or a table) and returns a JWT if valid:

  ```csharp
  [HttpPost("login")]
  public ActionResult<LoginResultDto> Login(LoginRequestDto loginDto)
  {
      // Validate username/password (this could check a Users table using UserManager if using Identity)
      if(loginDto.Username == "admin" && loginDto.Password == "Password123")
      {
          var tokenHandler = new JwtSecurityTokenHandler();
          var key = Encoding.UTF8.GetBytes("SuperSecretKey12345");
          var tokenDescriptor = new SecurityTokenDescriptor
          {
              Subject = new ClaimsIdentity(new[]
              {
                  new Claim(ClaimTypes.Name, loginDto.Username),
                  new Claim(ClaimTypes.Role, "Admin")
              }),
              Expires = DateTime.UtcNow.AddHours(1),
              Issuer = "YourApp",
              Audience = "YourAppUsers",
              SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
          };
          var token = tokenHandler.CreateToken(tokenDescriptor);
          var jwt = tokenHandler.WriteToken(token);
          return Ok(new LoginResultDto { Token = jwt });
      }
      return Unauthorized();
  }
  ```

  In production, you'd use ASP.NET Core Identity or another user store to verify credentials and retrieve roles, etc., but the above illustrates the JWT creation.

- Protect the other controllers by adding `[Authorize]` on class or specific endpoints, so that a valid JWT is required. For example:
  ```csharp
  [Authorize]
  [Route("api/[controller]")]
  [ApiController]
  public class EmployeesController : ControllerBase { ... }
  ```
  Now, any request to EmployeesController must include `Authorization: Bearer <token>` header with a valid token issued by our login.

**Global Exception Handling & Logging**:

- Use `app.UseExceptionHandler("/error")` in Startup to catch exceptions. We can have an `ErrorController` or simply use ExceptionHandler with a lambda to produce a ProblemDetails:
  ```csharp
  app.UseExceptionHandler(errorApp =>
  {
      errorApp.Run(async context =>
      {
          context.Response.StatusCode = 500;
          context.Response.ContentType = "application/json";
          var problem = new ProblemDetails
          {
              Status = 500,
              Title = "An unexpected error occurred.",
              Detail = "Please try again later or contact support.",
              Instance = context.TraceIdentifier
          };
          // Log the context.Error if needed (via an injected logger)
          await context.Response.WriteAsJsonAsync(problem);
      });
  });
  ```
  This ensures that any uncaught exceptions return a JSON problem rather than a blank 500 or HTML error page (especially since [ApiController] by default only handles model validation errors with 400).
- Logging: Configure `ILogger` in DI and use it in catch blocks or in the exception handler above to log details (like exception message, stack trace, etc.). Also log important actions, e.g., after saving changes for a user action (but be mindful of not logging sensitive info).

**Angular Frontend Setup**:

- Use Angular CLI to generate a new project (e.g., `ng new company-management`).
- Create models in TypeScript corresponding to our DTOs (e.g., `Employee`, `Department`, `Project` interfaces).
- Setup environment configuration: in `environment.ts` and `environment.prod.ts`, set the base API URL (e.g., `apiUrl: 'https://localhost:5001/api'` for dev).
- Generate services:
  - `EmployeeService` with methods to call API endpoints (`getEmployees()`, `getEmployee(id)`, `createEmployee(dto)`, etc.). Use Angular HttpClient.
  - Possibly `AuthService` to handle login (calls `/api/auth/login`, stores token).
- Use HttpInterceptor to attach JWT token to every outgoing request:
  ```typescript
  @Injectable()
  export class AuthInterceptor implements HttpInterceptor {
    constructor(private authService: AuthService) {}
    intercept(
      req: HttpRequest<any>,
      next: HttpHandler
    ): Observable<HttpEvent<any>> {
      const authToken = this.authService.getToken();
      if (authToken) {
        const authReq = req.clone({
          setHeaders: { Authorization: `Bearer ${authToken}` },
        });
        return next.handle(authReq);
      }
      return next.handle(req);
    }
  }
  ```
  Register this interceptor in `app.module.ts` providers:
  ```typescript
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ```
- Create Angular components for listing and editing:

  - `EmployeeListComponent`: On init, calls EmployeeService.getEmployees(), subscribes and stores list. Uses an \*ngFor to display employees (maybe showing name and department). Possibly include links or buttons to edit/delete.
  - `EmployeeEditComponent`: If editing existing, retrieve the id from route params, load employee (with department dropdown populated via DepartmentService). If creating new, it's similar but without id.
  - Similar components for Department and Project if needed.
  - A `LoginComponent` for the login form.
  - Perhaps a `DashboardComponent` as home page showing some stats (e.g., total employees, upcoming project deadlines, etc., which we could get from some aggregated endpoint or compute from data).

- **Routing**: Set up routes in `app-routing.module.ts`:

  ```typescript
  const routes: Routes = [
    { path: "login", component: LoginComponent },
    {
      path: "employees",
      component: EmployeeListComponent,
      canActivate: [AuthGuard],
    },
    {
      path: "employees/:id/edit",
      component: EmployeeEditComponent,
      canActivate: [AuthGuard],
    },
    {
      path: "departments",
      component: DepartmentListComponent,
      canActivate: [AuthGuard],
    },
    // ... maybe other routes
    { path: "", redirectTo: "employees", pathMatch: "full" },
    { path: "**", component: PageNotFoundComponent },
  ];
  ```

  Here, `AuthGuard` is a route guard we implement to check `AuthService.isLoggedIn()` (basically checks if token exists and not expired). If not logged in, redirect to `/login`.

- **State Management**: For a moderate app, using services with Observables may suffice. For instance, EmployeeService can hold a BehaviorSubject of employees list that components can subscribe to (especially if multiple components need that data). If demonstrating NgRx, we could set it up:

  - Define actions: LoadEmployees, LoadEmployeesSuccess, LoadEmployeesFailure, etc.
  - Reducer for employees state (holds list, loading flag, error).
  - Effect to call API on LoadEmployees and dispatch success/failure.
  - Components dispatch LoadEmployees on init, and use selectors to get employees from store.
  - This might be overkill for a tutorial, but it's how a large app would manage complex state. We’ll assume either approach is fine; given space, maybe skip detailed NgRx implementation here.

- **Error Handling on client**: If API returns validation errors (400 with details), display them in forms. If 401 occurs (maybe token expired), the interceptor could catch the 401 and redirect to login (or AuthGuard on any route change will do that).

  - Possibly use a notification service or Angular Material Snackbar to show error messages or success messages (e.g., "Employee saved successfully").

- **UI Layout**: Include a navigation bar with links to sections (Employees, Departments, Projects). That nav bar can also show "Logged in as [user]" and a Logout button. Logout would clear token and redirect to login.

**Testing Considerations**:

- Backend: write unit tests for Domain logic (Employee.TransferToDepartment) to ensure it behaves. Integration tests with an in-memory database for repository methods or even controller tests can be done using `WebApplicationFactory<T>` or similar in ASP.NET Core.
- Frontend: use Jasmine/Karma to test Angular services (mock HttpClient with HttpTestingController to simulate API responses). Also test components (with shallow rendering or DOM interaction via TestBed) to ensure they display data or react to service calls correctly.
- Use Postman or similar to manually test the API endpoints (especially the error cases, like not found, unauthorized).
- Use Angular's `ng serve` to run the dev server and test the whole app end-to-end in a browser. Possibly write e2e tests (Protractor or Cypress) to automate logging in and performing a few operations, verifying results on screen.

**Deployment Strategy**:

- Containerization: We could create a Dockerfile for the ASP.NET API and one for the Angular app (which can be a simple NGINX serving the built static files). Then use Docker Compose or Azure Web Apps to deploy.
- Ensure configuration for production: use environment variables for the JWT secret, database connection string, etc., not hardcoded.
- Database migrations: On first launch in prod, run `dbContext.Database.Migrate()` either in Startup or via a migration CLI to ensure DB is at latest version.
- Performance: In production, enable response caching for GET requests that are common (perhaps a list of departments could be cached for a minute since that doesn’t change often). Also ensure Angular is built with `ng build --prod` for optimization.

**Using the System**:

- When you navigate to the Angular app in browser, you get a login page (since not logged in, AuthGuard kicks you to `/login`). Enter credentials (which match what our AuthController expects, e.g., admin/Password123). If correct, Angular gets JWT and stores it (AuthService likely in localStorage).
- The AuthInterceptor now adds this JWT to every request. Angular router navigates to default route (employees list).
- The employees list component calls GET /api/employees, which the API verifies JWT, then returns list of employees (initially maybe none if DB empty, or seeded ones).
- You click "Add Employee", go to a form, fill details (name, choose a department from a dropdown that is populated via GET /api/departments), submit form (POST /api/employees). API creates, returns 201 with new ID. Angular maybe navigates back to list or to detail page, and shows success message.
- You test editing an employee (change department), deleting an employee, etc.
- Navigate to projects section, etc., verifying each works (and relationships reflect properly, e.g., removing an employee should perhaps remove from project team members via cascade or manual logic).
- Test security: try to use the app without logging in (should be redirected), or call APIs without token (should get 401).
- We should also test with a non-admin user if roles are used (in our Auth example, we always give Admin role to our test user; but if we had roles, we’d ensure role-based [Authorize] works, e.g., maybe only Admin can delete).

Throughout development, apply the performance and best practice notes:

- Use `AsNoTracking` on read-only queries to speed them up.
- Use includes to fetch related data in one go (we did for Department when listing employees).
- Index database columns used in filtering (we did index Deadline on Projects in case of queries by date).
- On Angular, use OnPush change detection in larger lists for efficiency, implement trackBy in ngFor loops for employees/projects listing:
  ```html
  <li *ngFor="let emp of employees; trackBy: trackByEmpId">
    {{emp.fullName}} ({{emp.departmentName}})
  </li>
  ```
  and in component:
  ```typescript
  trackByEmpId(index: number, emp: EmployeeDto) { return emp.id; }
  ```
- For large lists, consider pagination or virtual scroll. If employees could be thousands, the API should support paging parameters, and Angular UI implement an ngx-pagination or Material Paginator to request e.g., 50 at a time.
- Use lazy loading for any heavy Angular modules (not too critical in small app, but if we had an admin module with lots of extra dependencies, we’d lazy load as shown earlier).
- Security: confirm that Angular properly escapes any user input it displays. For example, if an employee name has `<script>` in it (someone maliciously entered that via API or DB), the Angular interpolation `{{emp.fullName}}` will render it harmlessly as text, not execute. We can test this by manually adding an employee with a name like `"<img src=x onerror=alert(1)>"` via API, and see that on UI it doesn't pop an alert, it just shows the string. Thanks to Angular's XSS protection.

**Wrap Up**:
By following this project through, we practiced:

- Designing a domain and mapping it to a relational DB using EF Core (with migrations to create tables).
- Implementing repository and service layers, applying OOP principles and patterns (like repository, unit of work).
- Exposing a REST API with proper HTTP usage (status codes, methods, routes, and secure it with JWT auth).
- Consuming that API in an Angular app, handling state, caching, and user interactions, with attention to performance and security on the client side.
- Testing and deployment considerations to ensure the system is robust in production.

This comprehensive example ties together all the advanced topics we've discussed, demonstrating how each piece (C#, ASP.NET Core, SQL/T-SQL, REST, Angular, EF Core) plays a role in an enterprise application. By building and iterating on this project, an advanced developer can deepen their expertise in full-stack development and be well-equipped to handle complex real-world applications.

## Testing and Deployment

No project is complete without proper testing and a solid deployment strategy. In this final section, we outline approaches for testing each part of the stack and discuss deployment considerations, including CI/CD pipelines and cloud hosting.

### Testing Strategy

**Unit Testing (Backend)**:

- **Domain Tests**: Write unit tests for domain entity logic. For example, test that `Employee.TransferToDepartment` updates the DepartmentId and perhaps logs an event (if we had events).
- **Service Tests**: Use mock repositories to test service methods. For the `EmployeeService.TransferEmployeeAsync`, supply a fake `IEmployeeRepository` that returns a known Employee, and a fake `IUnitOfWork` that tracks SaveChanges calls. Assert that it returns true when employee exists and false when not, that it calls SaveChanges once, etc. We can use a framework like Moq to create these mocks easily.
- **Controller Tests**: You can test controllers by mocking the repository/service dependencies. However, since controllers are thin, some teams skip direct unit tests on controllers and focus on integration tests.

**Integration Testing (Backend)**:

- Use the **WebApplicationFactory<TEntryPoint>** (from Microsoft.AspNetCore.Mvc.Testing) to spin up the API in memory with TestServer. Then use HttpClient to call endpoints and verify responses. We can use a test DB (like SQLite in-memory or the EF Core InMemory provider) configured for these tests:
  - For example, ensure that when you POST a new employee, a subsequent GET returns it.
  - Test authentication flows by obtaining a token from /login and then using it in Authorization header for subsequent calls.
  - Test error cases: GET /api/employees/999 returns 404, invalid model yields 400 with proper problem details, etc.
  - EF Core’s InMemory provider can simulate the DB, but be careful with relational constraints (it doesn’t enforce them like a real DB). Alternatively use a real localdb or SQLite to mimic real behavior.
- Also test EF Core queries against a real database for performance or correct translation if needed (not typical in automated tests, but maybe during development you run some load tests).

**Frontend Testing**:

- **Unit Tests**:
  - Service tests: use HttpClientTestingModule to mock backend calls. For example, in EmployeeService test, set up HttpTestingController to expect a GET and flush a sample response, then assert the service’s observable emits the mapped data.
  - Component tests: use Angular’s TestBed to create component with a stub service (provide a fake EmployeeService that returns known values). Test component logic (like after init it calls service and sets employees array, or clicking delete calls the service’s delete method).
  - Form validation tests: For a form component, set input fields, trigger validation, and assert form errors appear as expected.
- **End-to-End (E2E) Tests**: Use Protractor (default with Angular CLI) or Cypress to run the whole app against a test API (could be same in-memory API used in integration tests or a deployed test environment).
  - Write a test scenario: Login with valid creds, expect to navigate to employees list, click "Add Employee", fill form, submit, expect to see new employee in list.
  - Another scenario: Try to access a protected route without login, expect to be redirected to login.
  - These tests ensure the integration between Angular and API works and that the app functions from a user perspective.

**Performance Testing**:

- Use a tool like JMeter or Apache Benchmark for simple load testing on API endpoints. For example, simulate 100 concurrent GET /api/employees requests to see if our indexing and no-tracking yields good response times (and monitor SQL Server for scans).
- Test the Angular app with Lighthouse (built into Chrome DevTools) for performance best practices (bundle sizes, time to interactive, etc.). If any heavy part is flagged, consider lazy loading or code-splitting further, or using PWA techniques.

**Security Testing**:

- Attempt some basic pen tests:
  - XSS: Insert script as employee name via API, load UI to see if it executes (it shouldn’t, thanks to Angular).
  - CSRF: Because we use JWT in header, CSRF is not likely, but we can attempt to post from another domain (simulate via a tool) to ensure it fails due to missing token.
  - Ensure sensitive data (like our JWT secret) is not exposed anywhere (e.g., not sent to client, not logged).
  - Use OWASP ZAP or similar proxy to scan the API for common vulnerabilities.

### Deployment and CI/CD

**Continuous Integration (CI)**:

- Set up a pipeline (Azure DevOps, GitHub Actions, Jenkins, etc.) to build and test on each commit.
- Steps might include:
  1. Restore NuGet and NPM packages.
  2. Build the backend solution (`dotnet build`) and the Angular project (`ng build --prod`).
  3. Run backend tests (`dotnet test`) and frontend tests (`ng test --watch=false` for unit tests, maybe e2e tests with `ng e2e`).
  4. If all tests pass, produce artifacts: e.g., a Docker image or zip packages for deployment.

**Continuous Deployment (CD)**:

- If using Docker: create a multi-stage Dockerfile.
  - Stage 1: Use `node:14-alpine` to build Angular (copy package.json, run npm install, run ng build).
  - Stage 2: Use `mcr.microsoft.com/dotnet/sdk:5.0` to restore and build the .NET app and publish it (`dotnet publish -c Release -o /app/publish`).
  - Stage 3: Use `mcr.microsoft.com/dotnet/aspnet:5.0` as base, copy the publish output and also copy the Angular `dist/` output into `wwwroot` of the publish (if using the API to serve UI, e.g., if we use a fallback to serve index.html for any unknown route, making it a SPA).
    - Alternatively, serve Angular app separately via Nginx container or host on static hosting (like Azure Blob static website or GitHub Pages if no auth, but ours requires auth, so probably host with the API or on same domain for simplicity).
  - The result is one container running ASP.NET Core API (which could serve the Angular static files). This is a convenient deployment for small setups.
- On CI pipeline, after building and tests, build the Docker image and push to a registry.
- Then trigger deployment (CD):
  - If using Kubernetes, update the deployment (set image pull latest, etc.) or use Helm charts to rollout.
  - If using Azure Web App for Containers, you can point it to the registry image or use Azure DevOps release pipeline to deploy the image.
  - Alternatively, if not using containers:
    - Deploy the API to an Azure App Service (as a .NET app) and the Angular to Azure Static Web Apps or App Service as well.
    - Use GitHub Actions to deploy (there are pre-made actions for Azure).
- Ensure environment-specific configuration:
  - Use `ASPNETCORE_ENVIRONMENT` to load `appsettings.Production.json` with production DB connection and proper logging settings.
  - In Angular, the `ng build --prod` uses `environment.prod.ts` for API URL, etc., so ensure that's correct for deployed API.
  - Use user-secrets or environment variables for sensitive config (in container, pass as env var, and in Program.cs use `Configuration.GetConnectionString("DefaultConnection")` that picks it up).
- **Database migrations**: You can choose to have the API run `Database.Migrate()` on startup in production. This will apply any pending migrations automatically. This is convenient but be cautious if multiple instances start at once. Alternatively, run `dotnet ef database update` as part of deployment (ensuring the app offline or in maintenance during migrations if needed).
- **Monitoring**:
  - Use Application Insights or Serilog+Seq to capture logs and exceptions in production. For instance, Application Insights can be added via `services.AddApplicationInsightsTelemetry()` and configured with a key. It would capture request metrics, response times, exceptions, etc.
  - Angular can have Google Analytics or Azure AppInsights for front-end to track usage and any front-end errors (window.onerror).
  - Set up alerts: e.g., if any 500 errors spike or CPU on server is high, to notify the dev team.
  - Use a logging library to structure logs (Serilog to log JSON to files or console which container can output to a log aggregator).
- **Security & Patching**:
  - Keep dependencies up to date. For .NET, use Dependabot or manual upgrades for NuGet. Same for NPM packages. Our app uses widely-used libraries (Angular, EF Core, etc.) which regularly get updates. Plan periodic updates (e.g., Angular releases minor updates frequently; EF Core might not need as frequent).
  - Renew any secrets (JWT signing key, DB credentials) periodically. If using Azure, store them in Azure Key Vault or app settings rather than code.
  - Force HTTPS in production (most platform enforce it, but you can add `app.UseHttpsRedirection()` to be sure).
  - If deploying on a cloud VM or Kubernetes, ensure network security groups or ingress rules only expose needed ports, etc. Possibly separate the database into a private network.
  - Use Azure AD or other identity providers for production authentication if appropriate (to avoid managing passwords ourselves). But that’s an enhancement for real-world – our example uses a simple JWT for demonstration.

**Wrapping up Deployment**: At the end of this pipeline, we have:

- The database schema on the server (with seeded data if provided by migrations).
- The API running (with correct environment config, behind HTTPS).
- The Angular app served (either by the same API or via a static host) and able to communicate with the API (CORS configured if on different domain, etc.).
- Monitoring in place to catch issues, and the team is set up to improve and iterate.

With deployment done, the application is live and serving requests. The team should continuously gather feedback: performance metrics, error logs, and user feedback, to further optimize. Perhaps some pages are slow – then profile those DB queries or add caching. Maybe users want a feature – the clean architecture allows adding features without tangling concerns (maybe add a new Entity and corresponding UI, following similar patterns).

This completes our journey: from advanced development concepts to a deployed full-stack application. By following these steps and best practices, advanced developers can build **scalable, maintainable, and secure** full-stack systems with confidence.
