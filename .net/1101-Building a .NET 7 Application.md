# Building a .NET 7 Application – Advanced Step-by-Step Guide

This comprehensive guide covers the end-to-end process of building a modern application using .NET 7. It is structured for advanced developers and spans all crucial steps – from initial project setup to deployment, touching on databases, APIs, security, performance, testing, containerization, and advanced architectural patterns. Each section provides clear explanations, code snippets, and best practices (with references) to ensure a thorough understanding.

---

## 1. Project Setup

Building a robust .NET 7 application starts with a proper development environment and project structure. In this section, we install and configure .NET 7, set up the development tools (Visual Studio or VS Code), and create a new solution with a clean project structure.

### 1.1 Installing and Configuring .NET 7

Before coding, ensure .NET 7 SDK is installed on your machine:

- **Download .NET 7 SDK**: Visit the official Microsoft .NET website to download the .NET 7 SDK for your OS. Choose the SDK (not just the runtime) to get the development tools and runtime libraries.
- **Verify Installation**: After installation, verify by running `dotnet --version` in a terminal. You should see a version starting with 7 (e.g., _7.0.x_).
- **Environment Variables**: The installer usually configures PATH. If using a package manager (like **winget** on Windows), you can install via command line: `winget install Microsoft.DotNet.SDK.7`.

> **Note:** .NET 7 reached end-of-life in May 2024 (short-term support). It's still usable for learning or specific needs, but consider using .NET 8 (LTS) for long-term projects.

### 1.2 Setting up Visual Studio or VS Code

You can develop .NET 7 apps using **Visual Studio 2022** or **Visual Studio Code**, depending on preference:

- **Visual Studio 2022**: Ensure you have VS 2022 updated to the latest release. VS 2022 (17.4 and above) includes .NET 7 SDK support by default. If not, modify VS installation to add .NET 7 development tools. Use the **ASP.NET and web development** workload for web/API projects.
- **Visual Studio Code**: VS Code is a lightweight IDE and requires extensions:
  - Install the **C# extension** or **C# Dev Kit** in VS Code for rich C# IntelliSense and debugging.
  - Ensure the .NET 7 SDK is installed separately (as above).
  - You may also install the **NuGet Package Manager GUI** extension to manage NuGet packages easily.

Both IDEs support .NET CLI commands in an integrated terminal. Advanced developers often mix GUI and CLI for efficiency.

### 1.3 Creating a New Solution and Project Structure

Organizing your code into a solution with projects improves maintainability. We’ll create a solution and an ASP.NET Core Web API project:

- **Using .NET CLI**: Open a terminal (or VS Code terminal) in your development folder and run:

  ```bash
  dotnet new sln -n MyApp              # Create a new solution
  dotnet new webapi -n MyApp.Api       # Create a Web API project
  dotnet new classlib -n MyApp.Core    # (Optional) Core library for domain logic
  dotnet new classlib -n MyApp.Data    # (Optional) Data access library
  dotnet sln add MyApp.Api/MyApp.Api.csproj
  dotnet sln add MyApp.Core/MyApp.Core.csproj
  dotnet sln add MyApp.Data/MyApp.Data.csproj
  ```

  The `dotnet new webapi` command scaffolds a new Web API project with a default Controller (WeatherForecast) and required files. The class libraries `MyApp.Core` and `MyApp.Data` are optional and illustrate a layered architecture (e.g., Core for domain and Data for EF Core context).

- **Using Visual Studio**: In VS 2022, _File -> New -> Project_, choose **ASP.NET Core Web API** template, ensure .NET 7 is selected as the framework, and name the project _MyApp.Api_. To add class libraries, right-click the solution, _Add -> New Project_, choose Class Library (.NET 7) and name appropriately. Organize the solution into folders if needed (e.g., **src** for projects, **tests** for test projects).

**Project Structure Best Practices**:

- Keep the Web API project focused on API concerns (Controllers, Startup/Program configuration).
- Use a separate class library for business/domain logic (services, entities) if following Clean Architecture principles.
- Use another class library for data persistence (EF Core DbContext, migrations, repository implementations).
- Make sure to add references between projects appropriately (e.g., MyApp.Api references MyApp.Core and MyApp.Data).

After setup, your solution might look like:

```
MyApp.sln
 └── src/
     ├── MyApp.Api/       # ASP.NET Core Web API (controllers, Program.cs, etc.)
     ├── MyApp.Core/      # Core library (entities, interfaces, domain services)
     └── MyApp.Data/      # Data library (EF Core DbContext, migrations, repositories)
```

This separation follows the principle of keeping layers decoupled and makes unit testing easier.

---

## 2. Database Configuration

This section covers configuring **MySQL** (a relational database), **Redis** (an in-memory data store for caching), and **MongoDB** (a NoSQL database) in the .NET 7 application. We will install necessary NuGet packages and set up each data source, including Entity Framework Core for MySQL, caching with Redis, and using MongoDB’s C# driver.

### 2.1 Setting up MySQL

**MySQL Server**: Ensure you have access to a MySQL database. This could be:

- A local MySQL server (e.g., via MySQL Community Server or MariaDB).
- A Docker container running MySQL (which we will set up later in containerization).
- Cloud-hosted MySQL (AWS RDS, Azure Database for MySQL, etc.) – for development, local is sufficient.

**NuGet Packages for EF Core (MySQL)**:

- .NET doesn't include a MySQL EF Core provider by default, so we'll use the Pomelo EF Core provider (Pomelo.EntityFrameworkCore.MySql).
- In the MyApp.Data project (or MyApp.Api if putting everything together), install the package:
  ```
  dotnet add package Pomelo.EntityFrameworkCore.MySql
  ```
  This adds support for MySQL in Entity Framework Core. Pomelo is a popular open-source provider that supports EF Core up to the latest versions.

**Designing the DbContext**:

- Create a class (e.g., `AppDbContext`) inheriting from `DbContext`.
- Define `DbSet<T>` properties for each entity (model) that you want to store in MySQL.
- In the `OnConfiguring` or via `AddDbContext` in DI, configure MySQL:

  ```csharp
  // In MyApp.Data (Data library)
  public class AppDbContext : DbContext
  {
      public AppDbContext(DbContextOptions<AppDbContext> options)
          : base(options) { }

      public DbSet<Product> Products { get; set; }
      public DbSet<User> Users { get; set; }
      // ... other DbSets

      protected override void OnModelCreating(ModelBuilder modelBuilder)
      {
          base.OnModelCreating(modelBuilder);
          // Fluent API configuration (if any) goes here
      }
  }
  ```

  In Program.cs (startup):

  ```csharp
  var connectionString = builder.Configuration.GetConnectionString("MySqlConnection");
  builder.Services.AddDbContext<AppDbContext>(options =>
      options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));
  ```

  Here, `UseMySql` is an extension provided by Pomelo to configure MySQL with EF Core ([Tutorial: Connect to MySQL with Entity Framework Core in C# - MySqlConnector](https://mysqlconnector.net/tutorials/efcore/#:~:text=)). `ServerVersion.AutoDetect` will automatically figure out the MySQL server version to use the correct SQL dialect.

**Connection String**:

- Define a connection string in _appsettings.json_:
  ```json
  "ConnectionStrings": {
    "MySqlConnection": "Server=localhost;Database=myapp_db;User Id=myuser;Password=mypassword;"
  }
  ```
  Update with your server, database name, and credentials. EF Core will use this to connect.

**Applying Migrations**:

- Use EF Core migrations to create the MySQL database schema from your models:
  ```
  dotnet ef migrations add InitialCreate -p MyApp.Data -s MyApp.Api
  dotnet ef database update -p MyApp.Data -s MyApp.Api
  ```
  Here `-p` points to the project containing `DbContext` (Data) and `-s` points to the startup project (API). The `InitialCreate` migration will scaffold a database setup script for MySQL using the Pomelo provider.

**Testing the DB Context**: Once configured, you can test connecting to MySQL by injecting `AppDbContext` into a controller or a service and performing a simple query (e.g., count rows in a table). On running the application, ensure tables are created in MySQL.

### 2.2 Setting up Redis for Caching

**Redis Server**: For development, you can run Redis via Docker (`docker run redis`) or install it on your machine. We'll assume a local Redis instance running on default port 6379.

**NuGet Package for Redis Cache**:

- Install Microsoft’s Redis cache package:
  ```
  dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
  ```
  This provides an implementation of `IDistributedCache` using Redis via StackExchange.Redis.

**Configuring Redis Cache in Startup**:

- In Program.cs, register the distributed cache:
  ```csharp
  builder.Services.AddStackExchangeRedisCache(options =>
  {
      options.Configuration = builder.Configuration.GetConnectionString("RedisConnection");
      options.InstanceName = "MyApp_";  // prefix for cache keys (optional)
  });
  ```
  This tells .NET to use Redis as the backing store for the distributed cache interface ([Distributed caching in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/distributed?view=aspnetcore-9.0#:~:text=builder.Services.AddStackExchangeRedisCache%28options%20%3D,MyRedisConStr)). In _appsettings.json_, add:
  ```json
  "ConnectionStrings": {
    "RedisConnection": "localhost:6379"
  }
  ```
  You can also include password or other config if your Redis requires it.

**Using the Distributed Cache**:

- .NET’s `IDistributedCache` interface provides methods like `SetStringAsync`, `GetStringAsync` for basic usage.
- Example: Caching a query result (list of products) for 5 minutes:

  ```csharp
  public class ProductService : IProductService
  {
      private readonly AppDbContext _db;
      private readonly IDistributedCache _cache;
      public ProductService(AppDbContext db, IDistributedCache cache)
      {
          _db = db;
          _cache = cache;
      }

      public async Task<List<Product>> GetAllProductsAsync()
      {
          string cacheKey = "products_all";
          // Try get from cache
          var cached = await _cache.GetStringAsync(cacheKey);
          if (cached != null)
          {
              return JsonSerializer.Deserialize<List<Product>>(cached);
          }

          // If not in cache, fetch from database
          var products = await _db.Products.AsNoTracking().ToListAsync();
          // Cache the result
          var cacheEntryOptions = new DistributedCacheEntryOptions
          {
              AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
          };
          await _cache.SetStringAsync(cacheKey, JsonSerializer.Serialize(products), cacheEntryOptions);
          return products;
      }
  }
  ```

  In the above code, we inject `IDistributedCache` via DI and use it to cache the list of products. Distributed caches like Redis improve performance by avoiding repeated database hits, and data remains consistent across multiple server instances. Notice we used JSON serialization for storing complex objects as strings – alternatively, use `IDistributedCache.Set` with byte arrays or a library like StackExchange.Redis directly for more control.

**Cache Invalidation**: Remember to invalidate or update cache entries on data changes (e.g., after creating a new Product, remove or update the `"products_all"` cache). A stale cache can serve outdated data, so plan a strategy (time-based expiration as above, or explicit invalidation in CRUD operations).

### 2.3 Setting up MongoDB as a NoSQL Store

**MongoDB Server**: You’ll need a MongoDB instance. For development:

- Use the official MongoDB community server, or
- Run a Docker container: `docker run -d -p 27017:27017 mongo:latest` (this launches MongoDB on localhost:27017 without authentication by default).

**NuGet Package for MongoDB**:

- Install the MongoDB .NET driver:
  ```
  dotnet add package MongoDB.Driver
  ```
  This gives you MongoClient and related classes to interact with MongoDB.

**Connecting to MongoDB**:

- Use `MongoClient` to connect. A connection string might be `"mongodb://localhost:27017"` for a local server.
- Example initialization (could be in a service or repository):

  ```csharp
  public class MongoRepository
  {
      private readonly IMongoDatabase _database;
      public MongoRepository(IConfiguration config)
      {
          var mongoConnection = config.GetConnectionString("MongoConnection");
          var client = new MongoClient(mongoConnection);
          _database = client.GetDatabase("MyAppDb"); // database will be created if not exists
      }

      public IMongoCollection<BsonDocument> GetCollection(string name)
          => _database.GetCollection<BsonDocument>(name);
  }
  ```

  You can also define strongly-typed document classes (POCOs) instead of using `BsonDocument`. If you have a class `Order`, you can get a collection with `GetCollection<Order>("Orders")`. MongoDB will create the database and collection upon first use if they don't exist.

**CRUD Operations with MongoDB**:

- **Create/Insert**: Use `InsertOne` or `InsertMany` to add documents.
  ```csharp
  var ordersCollection = _database.GetCollection<Order>("Orders");
  var order = new Order { Id = Guid.NewGuid(), Item = "Book", Price = 29.99 };
  await ordersCollection.InsertOneAsync(order);
  ```
  This will insert a new document in the _Orders_ collection.
- **Read**: Querying can be done with the driver’s fluent API or LINQ. For example:
  ```csharp
  var allOrders = await ordersCollection.Find(Builders<Order>.Filter.Empty).ToListAsync();
  var expensiveOrders = await ordersCollection.Find(o => o.Price > 100).ToListAsync();
  ```
  If using `BsonDocument`, you can use filters like `new BsonDocument("Price", new BsonDocument("$gt", 100))`.
- **Update**: Use `UpdateOne`/`UpdateMany` with filters and update definitions:
  ```csharp
  var filter = Builders<Order>.Filter.Eq(o => o.Id, orderId);
  var update = Builders<Order>.Update.Set(o => o.Status, "Shipped");
  await ordersCollection.UpdateOneAsync(filter, update);
  ```
- **Delete**: Use `DeleteOne`/`DeleteMany` with a filter:
  ```csharp
  await ordersCollection.DeleteOneAsync(o => o.Id == orderId);
  ```

**Indexing in MongoDB**: It’s crucial to create indexes for fields you query often. For example, if you frequently query orders by `CustomerId`, create an index on that field:

```csharp
await ordersCollection.Indexes.CreateOneAsync(
    new CreateIndexModel<Order>(Builders<Order>.IndexKeys.Ascending(o => o.CustomerId))
);
```

This ensures efficient lookups (we’ll discuss performance more later).

**Use Cases for MongoDB**: In a typical app, relational data (with relationships, transactions) go to MySQL (using EF Core), whereas document-oriented or unstructured data might go to MongoDB. For instance, you might store logs, large text/searchable data, or user activity streams in Mongo, while core business data (users, orders, products) reside in MySQL.

### 2.4 Installing Necessary NuGet Packages Recap

By now, we have identified and installed several NuGet packages:

- `Pomelo.EntityFrameworkCore.MySql` for MySQL support in EF Core.
- `Microsoft.Extensions.Caching.StackExchangeRedis` for Redis distributed cache.
- `MongoDB.Driver` for MongoDB interactions.
- (Additionally, we might use `Microsoft.AspNetCore.Identity` if using Identity, or other packages for advanced scenarios.)

You can manage these via CLI or through Visual Studio's NuGet Manager. Keeping packages updated is important for security and performance fixes (NuGet will show updates when available).

---

## 3. CRUD API Development

With the database backends ready, we can design and implement the **CRUD API**. This involves defining a RESTful architecture, organizing the project into controllers, services, and repositories, implementing create, read, update, delete operations for each data source (MySQL via EF Core, Redis for cache, MongoDB), and adding exception handling, logging, versioning, and documentation.

### 3.1 Designing a RESTful API Architecture

A well-designed API adheres to REST principles:

- **Resources and URLs**: Identify resources (nouns) your API exposes, e.g., _users_, _orders_, _products_. Use plural nouns in URLs (e.g., `/api/products` for collection, `/api/products/{id}` for a single resource).
- **HTTP Methods**: Use standard methods for actions:
  - GET (read), POST (create), PUT/PATCH (update), DELETE (remove).
  - For example: `GET /api/products` returns list of products, `GET /api/products/{id}` returns a specific product.
- **Statelessness**: Each request should contain all information for the server to fulfill it (e.g., authentication token, request data) – no reliance on server memory of previous requests.
- **Status Codes**: Return appropriate HTTP status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error, etc.) to indicate outcome.
- **HATEOAS (Optional)**: Advanced REST includes hypermedia links, but this can be added later or omitted for simplicity in many APIs.

Design URLs to reflect hierarchy or relationships where appropriate (e.g., `GET /api/users/{id}/orders` for orders of a specific user).

> **Best Practice:** Keep the API versioned (we will cover versioning in section 3.5). Also ensure the API is documented (section 3.6) and uses consistent naming conventions for ease of use.

### 3.2 Implementing Controllers, Services, and Repositories

**Controller**: In ASP.NET Core, controllers handle incoming HTTP requests. Each controller typically corresponds to a resource (e.g., `ProductsController` for product-related endpoints). Controllers should remain thin – delegating business logic to services or other layers.

**Service**: A service (or business logic layer) contains core logic and orchestrates data access. For example, `ProductService` might contain methods to get products (using repository or DbContext), apply business rules, and coordinate caching with Redis.

**Repository**: A repository abstracts data access. For MySQL (EF Core), a repository for each aggregate or entity can encapsulate EF operations (like a `ProductRepository` wrapping `_dbContext.Products`). This helps apply the **Repository Pattern**, making data access swappable (for testing or if switching databases). A **Unit of Work** can coordinate multiple repositories, sharing a single DbContext transaction for atomic operations (more on this in section 9.1).

**Example Structure**:

```csharp
// Models (in MyApp.Core or MyApp.Api Models folder)
public class Product { public int Id { get; set; } public string Name { get; set; } ... }

// Repository Interface (in MyApp.Core)
public interface IProductRepository {
    Task<Product> GetByIdAsync(int id);
    Task<IEnumerable<Product>> GetAllAsync();
    Task AddAsync(Product product);
    Task UpdateAsync(Product product);
    Task DeleteAsync(int id);
}

// Repository Implementation (in MyApp.Data)
public class ProductRepository : IProductRepository {
    private readonly AppDbContext _db;
    public ProductRepository(AppDbContext db) { _db = db; }
    public async Task<Product> GetByIdAsync(int id) => await _db.Products.FindAsync(id);
    public async Task<IEnumerable<Product>> GetAllAsync() => await _db.Products.ToListAsync();
    public async Task AddAsync(Product product) { _db.Products.Add(product); await _db.SaveChangesAsync(); }
    public async Task UpdateAsync(Product product) { _db.Products.Update(product); await _db.SaveChangesAsync(); }
    public async Task DeleteAsync(int id) {
        var product = await _db.Products.FindAsync(id);
        if (product != null) { _db.Products.Remove(product); await _db.SaveChangesAsync(); }
    }
}
```

Above, `ProductRepository` uses EF Core’s DbContext directly. In a real app, you might inject `ILogger` for logging, or use a Unit of Work to commit changes.

**Registering Services and Repositories**:
In Program.cs, register these in the IoC container:

```csharp
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<IProductService, ProductService>();  // if you have a service layer
```

Use `AddScoped` for per-request lifetime for these dependencies.

**Controller Example**:

```csharp
[Route("api/[controller]")]
[ApiController]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    public ProductsController(IProductService productService) {
        _productService = productService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll()
    {
        var products = await _productService.GetAllProductsAsync();
        return Ok(products);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _productService.GetProductByIdAsync(id);
        if (product == null) return NotFound();
        return Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult> Create(ProductDto newProduct)
    {
        var created = await _productService.CreateProductAsync(newProduct);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    // ... PUT (update) and DELETE endpoints similarly
}
```

In the above:

- `[ApiController]` attribute enables automatic model validation and binding.
- We return DTOs (Data Transfer Objects) rather than EF entities directly (for decoupling and security).
- `CreatedAtAction` helps to return a 201 Created with a Location header to the new resource.

The controller is thin: it passes data to the service and returns appropriate HTTP responses.

### 3.3 Writing CRUD Operations for MySQL, Redis, and MongoDB

We have multiple data sources; typically:

- Primary data (e.g., **products, users, orders**) might be in MySQL (with EF Core and repositories as above).
- **Caching** of some frequently used data in Redis to speed up reads.
- Some data or features using **MongoDB**.

**MySQL (EF Core) CRUD Recap**:

- **Create**: `_dbContext.Add(entity)` + `SaveChangesAsync()`.
- **Read**: Use LINQ queries, `FindAsync` or `FirstOrDefaultAsync` for single items. Use `AsNoTracking()` when no update is needed (for performance).
- **Update**: Track the entity (query it, modify properties) and call `SaveChangesAsync()`. Or use `_dbContext.Update(entity)`.
- **Delete**: Remove the entity via `_dbContext.Remove(entity)` or direct `Remove` if you have the instance, then `SaveChangesAsync()`.

**MongoDB CRUD in context**: You might create a separate service or repository for MongoDB collections. For example, if using MongoDB for logging events, you could have:

```csharp
public class EventLogService {
    private readonly IMongoCollection<EventLog> _collection;
    public EventLogService(MongoRepository mongo) {
        _collection = mongo.GetCollection<EventLog>("EventLogs");
    }
    public Task LogEventAsync(EventLog log) => _collection.InsertOneAsync(log);
    public Task<List<EventLog>> GetEventsAsync(DateTime since) =>
        _collection.Find(e => e.Timestamp >= since).ToListAsync();
    // ... update and delete if needed
}
```

This demonstrates using the `MongoRepository` from earlier to get a typed collection and performing insert/query.

**Redis and CRUD**: Redis is usually not used for _permanent_ CRUD data storage (unless you use Redis as a primary DB which is less common in enterprise apps). Instead, consider Redis as a cache or transient storage:

- **Create/Update**: Setting a cache value (as shown in ProductService above with `_cache.SetStringAsync`).
- **Read**: Getting the cache value (`GetStringAsync`).
- **Delete**: Removing a cache entry if needed (via `_cache.RemoveAsync(key)` or simply letting it expire).

A practical strategy:

- On creating or updating an entity in MySQL, also update or invalidate the corresponding cache. For instance, if you have a cached list of products, clear that cache when a product is added or changed.
- Use Redis for storing ephemeral data like user sessions, feature flags, or frequently accessed reference data.

### 3.4 Exception Handling and Logging in the API

Robust applications include error handling and logging:

**Global Exception Handling**:

- Use ASP.NET Core’s middleware or filters for catching exceptions globally. E.g., add a middleware at the start of the pipeline:

  ```csharp
  app.UseExceptionHandler("/error");  // built-in middleware to handle exceptions
  ```

  You can create a controller or endpoint for `/error` to return a friendly error JSON. Alternatively, write a custom middleware to catch exceptions and log them.

- For unhandled exceptions, return a 500 status with minimal details (avoid exposing internals). Use `ProblemDetails` or a custom error model for client-friendly errors.

**Try-Catch in Services**:

- Wrap critical sections (like database calls or external calls) in try-catch to handle expected exceptions (e.g., DB update conflicts, null reference issues).
- For example:
  ```csharp
  try
  {
      await _productRepository.AddAsync(product);
  }
  catch (DbUpdateException ex)
  {
      _logger.LogError(ex, "Error adding product {@Product}", product);
      throw; // or return a Result indicating failure
  }
  ```
  Logging the exception with contextual info (the product data here) is helpful.

**Logging**:

- .NET uses `ILogger<T>` for logging. Use DI to get an `ILogger<ProductsController>` or `ILogger<ProductService>`.
- Log at appropriate levels:

  - `LogInformation` for routine events (e.g., "User {id} retrieved {count} products").
  - `LogWarning` for abnormal situations that aren’t errors (e.g., "Product {id} not found").
  - `LogError` for exceptions or errors.
  - `LogDebug/Trace` for detailed debugging info (usually turned off in production).

- You can configure logging providers in Program.cs. By default, console logging is enabled. You might add file logging or use third-party providers like Serilog or NLog for advanced logging (structured logs, sinks to files/DB).

**Example Logging Setup**:

```csharp
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
```

To log to a file, you might integrate Serilog:

```csharp
Log.Logger = new LoggerConfiguration()
    .WriteTo.File("logs/log.txt")
    .CreateLogger();
builder.Host.UseSerilog();
```

(After installing _Serilog.AspNetCore_ package.)

**Structured Logging**: Prefer structured logs (with named placeholders) over string concatenation. For instance:

```csharp
_logger.LogInformation("Created new product {@Product}", product);
```

This allows log providers to capture object data in a structured form (JSON, etc.), which is useful for querying logs in systems like ELK or Seq.

**Validation Errors**:

- ASP.NET Core automatically returns 400 Bad Request if model validation fails (with [ApiController]). The error response contains details about which fields failed validation. Customize as needed with `InvalidModelStateResponseFactory` if default is not suitable.

**Testing Error Handling**:

- Simulate errors (e.g., throw exceptions in a dev/test environment) to ensure your global error handler and logging work as expected. The API should not leak stack traces in production.

### 3.5 API Versioning

As your API evolves, supporting multiple versions is important so that existing clients don’t break when you introduce changes. .NET offers libraries for API versioning:

- Install Microsoft’s ASP.NET Core versioning library:
  ```
  dotnet add package Asp.Versioning.Mvc
  dotnet add package Asp.Versioning.Mvc.ApiExplorer
  ```
  These help define and query API versions.

**Configure API Versioning**:

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.ReportApiVersions = true;
    // e.g., clients can specify version via query string or header
    options.ApiVersionReader = ApiVersionReader.Combine(
        new QueryStringApiVersionReader("api-version"),
        new HeaderApiVersionReader("X-API-Version")
    );
});
```

In this setup:

- If no version is specified by the client, it assumes version 1.0.
- It reports supported versions in response headers (`api-supported-versions`).
- It reads version from either a query `?api-version=1.0` or a header `X-API-Version: 1.0` (you can also use URL segment versioning, like `/api/v1/products`).

**Annotating Controllers**:

- Apply `[ApiVersion("1.0")]` on controllers or specific actions to denote which version they belong to.
- Use conventions or attributes like `[Route("api/v{version:apiVersion}/[controller]")]` to include the version in the URL if using URL versioning.

**Versioning Strategy**:

- **URL Segment**: e.g., `/api/v1/products` vs `/api/v2/products`. Clear but means duplicating routes for new versions.
- **Query String/Headers**: e.g., `/api/products?api-version=2.0` or header. Keeps URL same but requires clients to specify version explicitly.
- **Content Negotiation (Media type)**: using `Accept` header with version parameter, less common for web APIs.

**API Versioning and Swagger**: The ApiExplorer package and Swashbuckle can integrate to show multiple versions in Swagger UI (we’ll see Swagger next).

**Deprecating APIs**: With versioning, you can mark older versions as deprecated (using attributes or in documentation), guiding users to upgrade. The `ReportApiVersions` option (true) will help clients see if they’re using a deprecated version (via response headers).

### 3.6 API Documentation with Swagger

Documenting the API is crucial for developers to understand how to consume it. **Swagger (OpenAPI)** is the standard for documenting RESTful APIs, and .NET integrates well with it via Swashbuckle.

**Setup Swagger (Swashbuckle)**:

- Install Swashbuckle:
  ```
  dotnet add package Swashbuckle.AspNetCore
  ```
- Configure in Program.cs:

  ```csharp
  builder.Services.AddEndpointsApiExplorer(); // if not already present
  builder.Services.AddSwaggerGen(c =>
  {
      c.SwaggerDoc("v1", new OpenApiInfo { Title = "MyApp API", Version = "v1" });
      // If using JWT auth, you can configure Swagger to use the Bearer token
      // c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme { ... });
      // c.AddSecurityRequirement(...);
  });
  ```

  This registers the Swagger generator that builds the OpenAPI specification from your controllers and models.

- Enable Swagger middleware:
  ```csharp
  if (app.Environment.IsDevelopment())
  {
      app.UseSwagger();
      app.UseSwaggerUI(c =>
      {
          c.SwaggerEndpoint("/swagger/v1/swagger.json", "MyApp API V1");
      });
  }
  ```
  This will serve the Swagger UI at `https://<host>/swagger` when in development. You might also enable it in staging or production behind authentication if needed.

**Using Swagger UI**:

- When you run the app, navigate to `/swagger` (or the exact path configured) to see the interactive documentation.
- All controllers and actions decorated with HTTP verbs will appear, with their parameters and response schemas.

**XML Comments** (optional but recommended):

- Enable XML comments in project settings (in _.csproj_):
  ```xml
  <PropertyGroup>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <NoWarn>$(NoWarn);1591</NoWarn>
  </PropertyGroup>
  ```
- Add summary comments to controllers and models. Then configure SwaggerGen to include them:
  ```csharp
  c.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, "MyApp.Api.xml"));
  ```
  This will enrich the Swagger docs with the comments.

**Result**: Swagger UI provides a quick way to test APIs and serves as up-to-date documentation. It shows available endpoints, required parameters, and example responses, reducing the guesswork for API consumers.

> **OpenAPI vs Swagger**: Technically, OpenAPI is the specification format (openapi.json), and Swagger refers to tools implementing that spec (like Swagger UI) ([ASP.NET Core web API documentation with Swagger / OpenAPI | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/tutorials/web-api-help-pages-using-swagger?view=aspnetcore-8.0#:~:text=The%20Swagger%20project%20was%20donated,not%20being%20released%20by%20SmartBear)). In practice, the term Swagger is still commonly used for the tooling.

---

## 4. Authentication and Security

Security is a critical aspect of any application. We will implement **JWT authentication** for securing the API, set up role-based access control (RBAC) for authorization, and discuss general security best practices including data encryption.

### 4.1 Implementing JWT Authentication

JSON Web Tokens (JWT) are a common way to secure APIs by issuing tokens to clients that must be presented on each request:

**Why JWT**: JWTs are stateless (server doesn’t keep a session per user; the token itself carries the user identity/claims) and widely supported. They are used in the Authorization header as a bearer token: `Authorization: Bearer <token>`.

**Setup JWT in ASP.NET Core**:

- Install JWT auth package:
  ```
  dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
  ```
- Configuration in Program.cs:

  ```csharp
  var jwtSettings = builder.Configuration.GetSection("Jwt");
  var key = Encoding.ASCII.GetBytes(jwtSettings["Key"]);

  builder.Services.AddAuthentication(options =>
  {
      options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
      options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
  })
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

  In the above:

  - We set the default auth scheme to JWT Bearer.
  - We define TokenValidationParameters to ensure the token’s issuer and audience are what we expect, the token hasn’t expired, and the signing key is valid.
  - The `IssuerSigningKey` is the symmetric key used to sign tokens (from configuration). This should be a long random secret (e.g., a 32+ char string). In production, store this securely (e.g., environment variable or Azure Key Vault).

- Add an `app.UseAuthentication();` call before `UseAuthorization()` in the HTTP pipeline:
  ```csharp
  app.UseAuthentication();
  app.UseAuthorization();
  ```
  This ensures ASP.NET Core will validate JWTs on incoming requests and set the `User` principal if valid.

**Issuing Tokens (Login)**:

- You need an endpoint for users to authenticate (e.g., `POST /api/auth/login` with username/password). In that endpoint, after verifying credentials (perhaps checking a MySQL database for user and hashing the password):

  ```csharp
  // assuming user is valid and we have their roles or claims
  var tokenHandler = new JwtSecurityTokenHandler();
  var key = Encoding.ASCII.GetBytes(jwtSettings["Key"]);
  var tokenDescriptor = new SecurityTokenDescriptor
  {
      Subject = new ClaimsIdentity(new[]
      {
          new Claim(ClaimTypes.Name, user.Id.ToString()),
          new Claim(ClaimTypes.Role, user.Role)  // include role claims if using roles
      }),
      Expires = DateTime.UtcNow.AddHours(1),
      Issuer = jwtSettings["Issuer"],
      Audience = jwtSettings["Audience"],
      SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
  };
  var token = tokenHandler.CreateToken(tokenDescriptor);
  string tokenString = tokenHandler.WriteToken(token);
  // return tokenString in response (and maybe user info)
  ```

  This uses the **System.IdentityModel.Tokens.Jwt** library to create a JWT with claims for the user’s identity and roles, an expiration, and signs it with the symmetric key.

- Store the `Issuer`, `Audience`, and `Key` in configuration (appsettings or environment). For example, in _appsettings.json_:
  ```json
  "Jwt": {
    "Key": "A_Long_Secret_Key_1234567890",
    "Issuer": "MyAppAuthServer",
    "Audience": "MyAppAudience"
  }
  ```

**Using [Authorize]**:

- Decorate controllers or actions with `[Authorize]` attribute to require a valid JWT. For example:
  ```csharp
  [Authorize]
  [HttpGet("profile")]
  public IActionResult GetProfile() { ... }
  ```
  This ensures only requests with a valid JWT (and meeting any policy/role requirements) can access. If a request has no token or an invalid token, it will get a 401 Unauthorized automatically by the framework.

**JWT Validation**:

- The JWT bearer middleware will validate token signature and claims on each request. If token is invalid (wrong signature, expired, etc.), request is rejected with 401.
- By default, if `[Authorize]` is used without roles/policies, any authenticated user is allowed. We cover roles next.

### 4.2 Role-Based Access Control (RBAC)

RBAC restricts parts of your API to certain users based on roles or permissions:

- **Assign Roles to Users**: This usually happens in your user management (for instance, a User entity has a Role property or a separate link table for roles).
- **Authorize by Role**:
  - Use `[Authorize(Roles = "Admin")]` on controllers/actions to only allow users in that role.
  - You can specify multiple roles: `[Authorize(Roles = "Admin,Manager")]` allows either role.
  - For more complex rules, use policy-based authorization (next).

**Example**: Protect an admin-only endpoint:

```csharp
[Authorize(Roles = "Administrator")]
[HttpPost("admin/task")]
public IActionResult RunAdminTask() { ... }
```

If a user’s JWT (specifically, their claims) does not include role "Administrator", the framework will return 403 Forbidden.

Under the hood, JWT’s claims should include a role claim (e.g., `"role": "Administrator"`). The JWT validation in .NET will map JWT roles to `ClaimsPrincipal.IsInRole()` automatically if configured correctly (the default maps the `"roles"` or `"role"` claim).

**Policy-Based Authorization**:

- Instead of roles, you can define policies. For example:
  ```csharp
  builder.Services.AddAuthorization(options =>
  {
      options.AddPolicy("RequireAdmin", policy => policy.RequireRole("Administrator"));
      options.AddPolicy("RequireEmployeeId", policy =>
          policy.RequireClaim("EmployeeId"));
  });
  ```
  Then use `[Authorize(Policy = "RequireAdmin")]` on endpoints. Policies can also use custom requirements, e.g., require a certain claim value, or even custom handlers (for advanced scenarios like checking a user owns a resource).

**Combining Authentication and Authorization**:

- First, the user must authenticate (valid JWT). Then authorization policies/roles are checked.
- 401 Unauthorized means the user isn’t authenticated (token missing or invalid).
- 403 Forbidden means they are authenticated but not allowed (token is valid but lacks required role or policy claim).

**Securing Swagger**:
If your API requires JWT auth, you might want to secure Swagger UI or at least allow entering a JWT. Swashbuckle can add a padlock icon where you input a JWT token to authorize requests in the UI.

**ASP.NET Core Identity (Optional)**:
In a full app, you might use ASP.NET Core Identity for user management which can issue cookies or tokens. In this guide, we focused on JWT without the Identity library for brevity (manually handling user auth). Identity can integrate with JWT or with cookie authentication for web apps.

### 4.3 Security Best Practices and Data Encryption

Beyond authentication and authorization, consider the following to harden your application:

- **HTTPS Only**: Always serve the app over HTTPS in production. ASP.NET Core templates enforce HTTPS by default and include HSTS. Ensure `app.UseHttpsRedirection();` is in your middleware pipeline.
- **Secure Headers**: Add security headers to responses (Content-Security-Policy, X-Content-Type-Options, etc.) using middleware or the `HeaderPolicyCollection` in ASP.NET.
- **Input Validation**: Although model binding and validation attributes catch a lot, always validate inputs, especially for SQL or NoSQL queries. Using parameterized queries or LINQ-to-EF protects against SQL injection inherently (EF Core will parameterize queries).
- **Output Encoding**: If returning HTML or integrating with frontends, guard against XSS by encoding outputs. In Web APIs that return JSON, this is less of an issue since you’re not directly injecting into HTML, but be cautious if you ever output to a browser.
- **Store Secrets Safely**: Never commit secrets (JWT signing keys, DB passwords) in source control. Use user secrets for development, environment variables, or secret managers in production (Azure Key Vault, AWS Secrets Manager).
- **Limit Exposure**: Only expose necessary endpoints and data. Hide implementation details. For example, don’t return stack traces to the client on errors (use generic error messages).
- **CORS**: If your API is consumed by web frontends on different domains, configure CORS (Cross-Origin Resource Sharing) to allow the specific origins. Use `builder.Services.AddCors()` and `app.UseCors()` accordingly, rather than allowing `*` in production.
- **Data Encryption**:
  - **At-Rest**: Use encryption for sensitive data in the database (if not using transparent disk encryption). For example, you might encrypt certain fields (like SSN) before saving to DB.
  - **In-Transit**: HTTPS covers in-transit encryption for API calls. For internal data flows (e.g., caching, service calls), if over a network, ensure encryption (Redis can be configured with TLS, MongoDB can use TLS).
  - ASP.NET Core’s **Data Protection API** can be used to encrypt data such as cookies, or any confidential payloads, with automatic key rotation.
- **Password Storage**: If your app manages user passwords, never store raw passwords. Use a strong hashing algorithm (ASP.NET Identity uses PBKDF2 by default which is strong). The OWASP guidelines recommend at least PBKDF2, bcrypt or Argon2 for password hashing.

- **Regular Updates**: Keep .NET and NuGet packages updated for latest security patches. For example, if a vulnerability is found in a library like Newtonsoft.Json or EF Core, update to patched versions.

- **Penetration Testing**: For advanced security, consider running static analysis or pen-testing tools (like OWASP ZAP or Burp Suite) against your API to catch common vulnerabilities (SQLi, XSS, etc.).

### 4.4 Implementing Data Encryption (Example)

To illustrate using the Data Protection API (useful for encrypting sensitive data before saving to DB or for things like encrypting query strings):

```csharp
// In Startup
builder.Services.AddDataProtection();

// In a service where you need to encrypt data:
public class SensitiveDataService
{
    private readonly IDataProtector _protector;
    public SensitiveDataService(IDataProtectionProvider provider)
    {
        _protector = provider.CreateProtector("MyApp.SensitiveData.v1");
    }

    public string ProtectData(string input)
    {
        return _protector.Protect(input);
    }
    public string UnprotectData(string protectedData)
    {
        return _protector.Unprotect(protectedData);
    }
}
```

This uses Microsoft's data protection, which handles key management and encryption. The `CreateProtector` string is a purpose, isolating different use-cases of data. You can now do:

```csharp
string enc = sensitiveDataService.ProtectData("secret info");
// store enc in DB
string dec = sensitiveDataService.UnprotectData(enc);
// use dec when needed
```

This encryption is symmetric but with rotating keys stored securely (in files or registry by default, or Azure Key Vault in cloud). It's preferable to writing your own encryption logic.

**Summary**: Security must be considered at every layer: transport (HTTPS), authentication (JWT), authorization (RBAC/policies), data storage (encryption and hashing), coding practices (avoid injection, validate inputs), and configuration (safe handling of secrets). Always follow the principle of **least privilege** – give minimal access necessary – and **defense in depth**, so that if one layer is breached, others still protect the system.

---

## 5. Performance Optimization

High performance is key for a scalable application. We will explore strategies for optimizing performance in our .NET 7 app, including caching with Redis, query optimization for MySQL (EF Core), indexing for MongoDB, and leveraging asynchronous and parallel programming.

### 5.1 Caching Strategies with Redis

We introduced Redis caching in section 2.2. Now let's delve deeper into caching strategies:

- **Cache Aside Pattern**: The code example in section 2.2 followed this pattern: check cache first, if miss then retrieve from DB and update cache. This is a common approach that keeps cache updated on-demand.
- **Background Caching**: For data that can be stale for a while, you might pre-populate cache at startup or via background jobs (e.g., using a Hangfire recurring job or hosted service that periodically refreshes certain keys).
- **Cache Invalidation**: Define how cached data will be updated. Options:
  - Time-based expiration (we set 5 minutes for products list).
  - Manual invalidation (after a data change, call `_cache.Remove("products_all")` for example).
  - Cache tags or versioning (not built-in in IDistributedCache, but some libraries allow grouping cache entries).
- **Sliding vs Absolute Expiration**: A sliding expiration extends the life of a cache entry if it's accessed frequently. Absolute expiration is a fixed time. .NET’s `DistributedCacheEntryOptions` supports both. Use sliding for things that should stay cached if in constant use.
- **Distributed Locking**: In rare cases, to prevent cache stampede (many requests all miss cache at once and flood the DB), you might implement a lock so only one request reloads the cache while others wait. This can be complex; often setting short expiration and perhaps using an in-memory cache as an additional layer can mitigate stampedes.

Monitor cache hit ratios in production. If cache hit is low, maybe the expiration is too short or cache keys are not used consistently.

### 5.2 Query Optimization in MySQL (EF Core)

Using EF Core with MySQL efficiently:

- **Efficient Queries**: Only fetch data you need:
  - Use LINQ projections to anonymous or DTO types to avoid pulling entire entities if not needed. Example: `_dbContext.Users.Select(u => new { u.Id, u.Name }).ToListAsync()`.
  - Use `.AsNoTracking()` for read-only queries to avoid the overhead of tracking (it’s slightly faster and uses less memory).
- **Filters and Pagination**: Filter at the database level (in LINQ) rather than in-memory. For large datasets, always apply filters (e.g., date ranges, user-specific data). Implement pagination for endpoints returning lists (using `.Skip().Take()` in EF which translates to SQL LIMIT/OFFSET).
- **Include vs Separate Queries**: EF Core allows `.Include()` to fetch related data. Overusing Include can lead to large joins (e.g., including a collection navigation property pulls a lot of data). Sometimes it's better to load related data on demand or use explicit separate queries. Tools like EF Core’s logging can show the SQL generated – watch out for N+1 query issues.
- **Compiled Queries**: EF Core 7 can compile queries for repeated use to improve performance slightly. This is an advanced scenario (via `EF.CompileQuery`).
- **Raw SQL**: For very complex queries or performance-critical paths, use raw SQL with `FromSqlInterpolated` or ADO.NET. Ensure to parameterize inputs (`FromSqlInterpolated` does this automatically).
- **DB Optimization**: Create indexes in MySQL for columns used in `WHERE` clauses or joins. For example, if your `Orders` table queries by `CustomerId`, ensure an index on that column. You can add indexes via EF Core’s Fluent API or migrations:
  ```csharp
  modelBuilder.Entity<Order>()
      .HasIndex(o => o.CustomerId);
  ```
- **Connection Pooling**: .NET uses connection pooling by default. Ensure your MySQL is tuned to handle the number of connections (increase `max_connections` if needed on the DB server).
- **Monitoring**: Use MySQL’s `EXPLAIN` for slow queries (you can capture the SQL via logging or use a profiler). If an EF query is slow, examine if it's doing what you expect (maybe it pulled too much data or missed an index usage).

### 5.3 Indexing Strategies in MongoDB

MongoDB requires careful indexing to perform well:

- **Identify Query Patterns**: Add indexes on fields that you frequently filter or sort by. For example, an index on `Order.Status` if you often get orders by status, or a compound index on `UserId` and `CreatedDate` if you often query user’s recent actions.
- **Unique Indexes**: For fields like email or username in a user collection, use a unique index to enforce uniqueness.
- **Avoid Table Scans**: Without an index, MongoDB will scan all documents in a collection which is very slow beyond small sizes. Use the Mongo shell or driver to ensure indexes are created at startup or via migrations (MongoDB doesn’t have migrations like EF, but you can run an initializer).
- **Index Impact**: Indexes speed up reads but slightly slow writes and use memory. Don’t index everything, only what makes sense for queries.
- **Use .Explain()**: You can call `.Find(filter).Explain()` in development to see how MongoDB query planner handles your query.
- **Aggregation Pipeline**: If using complex aggregations in Mongo, ensure fields used in `$match` at the beginning are indexed. The pipeline can use indexes for the initial match stage.

### 5.4 Asynchronous Programming

.NET 7 is highly optimized for async/await. All our database calls (EF Core, Redis, Mongo) have async versions and we used them. Key points:

- **Avoid Synchronous Blocking**: Do not use `.Result` or `.Wait()` on tasks – this can cause thread pool starvation. Always propagate async calls (controller actions should be `async Task<ActionResult>`).
- **ConfigureAwait**: Not typically needed in ASP.NET Core (it doesn’t capture context the same way as older frameworks). But in library code, you might use `ConfigureAwait(false)` to avoid deadlocks in non-web contexts.
- **Parallel Execution**: If you have independent operations, you can do them in parallel. For example, if on a dashboard endpoint you need to fetch data from MySQL, Redis, and Mongo simultaneously:
  ```csharp
  var productsTask = _productService.GetAllProductsAsync();    // MySQL call
  var statsTask = _statsCache.GetStatisticsAsync();            // Redis call
  var auditTask = _auditLogService.GetRecentLogsAsync();       // Mongo call
  await Task.WhenAll(productsTask, statsTask, auditTask);
  var products = productsTask.Result;
  var stats = statsTask.Result;
  var logs = auditTask.Result;
  ```
  Because these calls hit different systems (DB, cache, NoSQL), doing them in parallel can improve total response time, utilizing multiple threads/I/O operations concurrently. Ensure the systems can handle concurrent requests.
- **I/O vs CPU**: Async is great for I/O-bound work (network, disk). For CPU-bound tasks (e.g., heavy computation), consider using background worker or processing it on a separate thread so as not to block the request thread (look into `Task.Run` or better, use a background queue with something like `IHostedService`).

### 5.5 Parallel Processing

For CPU-bound parallel tasks, .NET offers data parallelism (via PLINQ or Parallel.ForEach) and multi-threading:

- **Parallel LINQ (PLINQ)**: If you have a collection and need to perform CPU-heavy computation on each element, you can use `.AsParallel()`:
  ```csharp
  var results = data.AsParallel()
                    .WithDegreeOfParallelism(Environment.ProcessorCount)
                    .Select(x => HeavyComputation(x))
                    .ToList();
  ```
  PLINQ partitions the work across threads. Use only for CPU-intensive tasks that are easily parallelizable.
- **Parallel.ForEach**: Similar to PLINQ but imperative:

  ```csharp
  Parallel.ForEach(items, item => ProcessItem(item));
  ```

  Be cautious with parallel tasks in a web app – too many threads can hurt performance rather than help if the server CPU is overwhelmed.

- **Async Streams**: C# `IAsyncEnumerable<T>` allows streaming data asynchronously (e.g., reading a large DB result chunk by chunk). This can reduce memory usage and start processing before all data is available. It's advanced, but good for certain scenarios (e.g., sending large responses in chunks or processing large files).

**Measuring Performance**:

- Use Application Insights or logging to measure response times for endpoints.
- Benchmark critical sections (use BenchmarkDotNet for micro-benchmarks if needed).
- Use profiling tools or perform load tests to identify bottlenecks. Often, the database is the first bottleneck; caching and query tuning give the biggest wins, whereas micro-optimizations in C# code give smaller improvements.

**Scaling Out**:

- Remember that to handle more load, you can scale vertically (a more powerful server) or horizontally (more instances behind a load balancer). Horizontal scaling requires statelessness; our use of distributed cache and JWT (stateless auth) means any instance can handle any request – which is good.
- Use caching and optimized queries to reduce load per request, but for truly high scale, plan for multiple app servers and a robust database cluster (or split databases by service if using microservices).

---

## 6. Unit Testing and Integration Testing

Testing ensures that your code works as expected and helps prevent regressions. We will write **unit tests** for individual components (services, etc.) and **integration tests** for the API endpoints interacting with the database.

### 6.1 Writing Unit Tests with xUnit or MSTest

**Testing Framework**: xUnit is a popular choice for .NET (also MSTest or NUnit can be used). We’ll use xUnit in examples.

- Create a test project (e.g., `MyApp.Tests`) using `.NET 7 xUnit Test Project` template or via CLI:

  ```
  dotnet new xunit -n MyApp.Tests
  dotnet add MyApp.Tests/MyApp.Tests.csproj reference MyApp.Core.csproj
  dotnet add MyApp.Tests/MyApp.Tests.csproj reference MyApp.Data.csproj
  ```

  Reference the projects you want to test (likely Core and Data, and maybe Api if some logic is there). You might not reference Api project if it's just controllers, which you test via integration tests instead.

- Add any needed test packages:
  - `dotnet add package Moq` for mocking.
  - (xUnit is already included by the template.)

**Example Unit Test** for a service:

```csharp
public class ProductServiceTests
{
    [Fact]
    public async Task GetAllProductsAsync_ReturnsProducts()
    {
        // Arrange
        var sampleProducts = new List<Product> {
            new Product { Id = 1, Name = "Test1" },
            new Product { Id = 2, Name = "Test2" }
        };
        // Create a mock repository
        var repoMock = new Mock<IProductRepository>();
        repoMock.Setup(r => r.GetAllAsync()).ReturnsAsync(sampleProducts);
        // Create a mock cache that returns null (to simulate cache miss)
        var cacheMock = new Mock<IDistributedCache>();
        cacheMock.Setup(c => c.GetStringAsync(It.IsAny<string>()))
                 .ReturnsAsync((string)null);
        // We can also mock SetStringAsync to do nothing
        var service = new ProductService(repoMock.Object, cacheMock.Object);

        // Act
        var result = await service.GetAllProductsAsync();

        // Assert
        Assert.NotNull(result);
        Assert.Equal(2, result.Count());
        Assert.Equal("Test1", result.First().Name);
        // Verify that data was saved to cache
        cacheMock.Verify(c => c.SetStringAsync(
            It.IsAny<string>(),
            It.IsAny<string>(),
            It.IsAny<DistributedCacheEntryOptions>(),
            It.IsAny<CancellationToken>()), Times.Once);
    }
}
```

In this test:

- We used **Moq** to create a fake `IProductRepository` and `IDistributedCache`.
- We set up the repository to return a list of products, and cache to return null for `GetStringAsync` and capture that `SetStringAsync` is called.
- We then assert the service returns the expected products and interacts with the cache appropriately.
- This test avoids any real database or Redis calls, making it a true unit test.

**Testing Controllers**: Instead of unit testing controllers by mocking `IProductService`, it might be more valuable to do integration testing (so you can test the whole pipeline). But for completeness, you could do:

```csharp
[Fact]
public async Task GetById_ReturnsNotFound_WhenProductDoesNotExist()
{
    // Arrange
    var serviceMock = new Mock<IProductService>();
    serviceMock.Setup(s => s.GetProductByIdAsync(42)).ReturnsAsync((ProductDto)null);
    var controller = new ProductsController(serviceMock.Object);
    // Act
    var result = await controller.GetById(42);
    // Assert
    Assert.IsType<NotFoundResult>(result.Result);
}
```

Here, we directly call the controller method as a normal method.

**MSTest or NUnit**: Similarly capable; choose one framework and be consistent. xUnit has a nice parallel test execution by default and a clean assertion library.

**Organization**:

- Group tests by system under test (class or method) and scenario.
- Use `[Theory]` and `[InlineData]` in xUnit for data-driven tests (e.g., test multiple inputs without duplicating code).
- Keep tests independent (no order dependency, and reset static/shared state between tests as needed).
- Use test fixture setup if creating expensive resources (like a InMemory database context).

### 6.2 Mocking Dependencies with Moq (or alternative)

We saw Moq usage. Some tips:

- **Setup**: `mock.Setup(x => x.Method(It.IsAny<Type>())).Returns(...);` for functions. For properties, you might use `mock.SetupGet`.
- **Verify**: Use `mock.Verify(x => x.Method(y), Times.Once)` to ensure a method was called expected times (important to test side-effects like caching or calls to external components).
- **Returning Task/Async**: Use `ReturnsAsync(value)` for async methods.
- **Exception Throwing**: You can do `mock.Setup(x => x.Method(...)).Throws(new Exception("fail"));` to test exception paths.

Alternative mocking frameworks include NSubstitute, FakeItEasy, or just manual fakes.

For EF Core, you can use the **InMemory Database** (Microsoft.EntityFrameworkCore.InMemory) for tests instead of mocking DbContext (EF contexts are complex to mock). Example:

```csharp
var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase("TestDb").Options;
using var context = new AppDbContext(options);
// seed data
context.Products.Add(new Product { Id = 1, Name = "P1" });
context.SaveChanges();
// use context in repository
var repo = new ProductRepository(context);
var products = await repo.GetAllAsync();
Assert.Equal(1, products.Count());
```

This is more like a lightweight integration test because it uses an actual in-memory DB. It's fast and avoids requiring a real MySQL for tests.

### 6.3 Integration Testing Strategies

Integration tests will run the full stack (or significant portions of it). For ASP.NET Core, a great approach is using the **WebApplicationFactory<T>** class to host the app in memory.

**Using WebApplicationFactory**:

- Add reference to `Microsoft.AspNetCore.Mvc.Testing` in the test project:
  ```
  dotnet add package Microsoft.AspNetCore.Mvc.Testing
  ```
- Write a test using it:

  ```csharp
  public class ProductsApiIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
  {
      private readonly HttpClient _client;
      public ProductsApiIntegrationTests(WebApplicationFactory<Program> factory)
      {
          // Optionally customize factory, e.g., use a test appsettings or replace services
          _client = factory.CreateClient();
      }

      [Fact]
      public async Task GetProducts_ReturnsOkAndData()
      {
          // Arrange: (seed database if needed, perhaps via factory.Services)
          // e.g., using var scope = factory.Services.CreateScope();
          //       var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
          //       db.Products.Add(new Product { ... }); db.SaveChanges();

          // Act
          var response = await _client.GetAsync("/api/products");
          // Assert
          response.EnsureSuccessStatusCode();
          var json = await response.Content.ReadAsStringAsync();
          // deserialize and assert data
          var products = JsonSerializer.Deserialize<List<ProductDto>>(json);
          Assert.NotNull(products);
      }
  }
  ```

  This uses the Program class (entry point of API) to spin up the server in-memory on a TestServer. You get a HttpClient to call your API endpoints as if they were live.

- You can configure the WebApplicationFactory in multiple ways:
  - Override configuration (to use a test database or mock external services).
  - For example, if you want the API to use the InMemory provider instead of MySQL during tests, one way is to add an environment variable or use WebApplicationFactory's `WithWebHostBuilder` to override `AppDbContext` registration to use InMemory DB.
  - Alternatively, provide a separate `appsettings.Test.json` where the connection string points to a test DB (like a locally running MySQL or SQLite).

**Test Database**:

- A common approach is to use a separate test database (like a localdb or SQLite) and run migrations at test start. But using EF Core InMemory or SQLite in-memory mode is faster and avoids external dependencies.
- Ensure isolation: for integration tests, you might reset the database between tests (or use a new DB per test by using a unique name or EnsureDeleted at start).

**Integration Test vs Unit Test**:

- Integration tests are slower (because they start more of the app, possibly hit database or network). Use them to cover things unit tests might miss, such as:
  - Correct wiring of DI (did we forget to register a service? Integration test will catch it when the call fails).
  - Routing and filters (does `[Authorize]` block an anonymous call? Integration test can verify a 401).
  - The actual data flow from HTTP request down to DB and back.
- Aim for a few happy path tests and a few error path tests for key endpoints. You don’t need to integration-test every tiny validation if unit tests cover that logic.

**Continuous Testing**:

- Include tests in CI pipeline. With `dotnet test` command, tests will run. The integration tests will need the environment (like any required config in place).
- Mark integration tests appropriately if you want to separate them (you can use traits or categories). Some teams run unit tests on each build and integration tests less frequently or in a nightly run due to their heavier nature.

**Mock External Dependencies**:

- If your service calls external APIs (like a payment service via HTTP), in integration tests you should mock those. Options:
  - Abstract the external calls behind an interface and inject a fake in tests.
  - Or use tools like **WireMock.Net** to simulate an external HTTP API.
- For databases, as discussed, use in-memory or local test instances.

**Clean Up**:

- WebApplicationFactory will dispose and shut down the server after tests (via IClassFixture).
- If using a real test database, ensure to clean up data between tests (perhaps re-create schema).
- Use the `Dispose` pattern or xUnit fixtures to handle any cleanup.

By combining thorough unit tests for logic and integration tests for end-to-end verification, you’ll gain confidence in your application’s correctness and stability. Aim for good coverage on critical business logic and APIs.

---

## 7. Containerization and Deployment

Deploying the application in a consistent environment is simplified by containerization. We will containerize the .NET 7 API along with MySQL, Redis, and MongoDB using Docker, orchestrate them with Docker Compose, and set up a CI/CD pipeline. Finally, we’ll discuss deploying to Kubernetes or cloud platforms.

### 7.1 Setting up Docker Containers for .NET 7 API, MySQL, Redis, and MongoDB

**Dockerizing the .NET API**:

- Create a `Dockerfile` in the root of MyApp.Api project:

  ```dockerfile
  FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
  WORKDIR /src
  COPY ["MyApp.Api.csproj", "./"]
  # Copy other project files if multi-project and restore
  COPY . .
  RUN dotnet publish -c Release -o /app

  FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS runtime
  WORKDIR /app
  COPY --from=build /app .
  ENV ASPNETCORE_URLS=http://+:5000
  EXPOSE 5000
  ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
  ```

  This is a multi-stage Dockerfile:

  - Uses .NET SDK 7 image to build and publish the app.
  - Then uses the lighter ASP.NET Core runtime image to run the app.
  - It sets the container to listen on port 5000. We'll map that to a host port via Compose.

- **MySQL, Redis, MongoDB Images**: Use official images:
  - MySQL: `mysql:8.0` (set environment `MYSQL_ROOT_PASSWORD` and volumes for data).
  - Redis: `redis:7` (for dev, no config needed; for prod, consider a config file or use Redis with persistence).
  - MongoDB: `mongo:6` (set no auth for dev or provide a username/password via environment and create a user).

**Docker Compose**: Create `docker-compose.yml` to define all services:

```yaml
version: "3.8"
services:
  api:
    build:
      context: .
      dockerfile: MyApp.Api/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__MySqlConnection=Server=mysql;Database=myapp_db;User Id=root;Password=Password123;
      - ConnectionStrings__RedisConnection=redis:6379
      - ConnectionStrings__MongoConnection=mongodb://mongo:27017
      - Jwt__Key=SuperSecretKeyForJwt123! # in real setups, use secrets
      - Jwt__Issuer=MyAppAuthServer
      - Jwt__Audience=MyAppAudience
    depends_on:
      - mysql
      - redis
      - mongo

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=Password123
      - MYSQL_DATABASE=myapp_db
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mysql_data:
  mongo_data:
```

This compose file:

- Builds the API from the Dockerfile.
- Sets environment variables for the API container, including connection strings that point to other services by their compose service name (Docker’s DNS will resolve `mysql`, `redis`, `mongo`).
- Exposes necessary ports to the host for local testing (5000 for API, others as needed).
- `depends_on` ensures containers start in order (though you might still need to handle retry logic in the API if, say, MySQL isn’t ready when API starts).
- Defines volumes for MySQL and Mongo to persist data outside the container.

**Running Compose**:

- In a terminal, run `docker-compose up --build`. This will build the API image and start all containers. You should then be able to access the API at http://localhost:5000 (which proxies into the container).
- Verify that the API can connect to MySQL (the first run might fail if MySQL isn't fully ready; in development, just restart the API container or use retry logic like a health-check and wait).

**Docker Ignore**:

- Create a `.dockerignore` to avoid copying unnecessary files (like `.git`, `bin/`, `obj/` folders) into the image context.

### 7.2 Writing Docker Compose Files for Multi-Container Setup

We covered one in 7.1, but some general tips:

- Use separate compose files or override files for different environments (e.g., `docker-compose.prod.yml` might use production images or add different env variables).
- In CI/CD, you might build images and push to a registry (DockerHub, GitHub Container Registry, AWS ECR, etc.) instead of using compose to build on server.
- For testing, you can run `docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d` where docker-compose.test.yml might spin up the app in a test mode, which can be used for integration tests (some teams do this to test the actual container image in CI).

**Ensuring Services Wait (Healthchecks)**:

- Docker Compose allows healthchecks. For example, you could add:
  ```yaml
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    interval: 10s
    retries: 5
  ```
  to the MySQL service, and then in API’s depends_on, specify `condition: service_healthy`. This way, Docker waits for MySQL’s health check to pass before considering the API up (but your API might still need retry if it starts before DB ready).

### 7.3 CI/CD Pipeline Setup (GitHub Actions, Azure DevOps, GitLab CI/CD)

Automating build, test, and deployment:

- **GitHub Actions**: If using GitHub, create a workflow file (e.g., `.github/workflows/ci.yml`):

  ```yaml
  name: CI
  on: [push, pull_request]
  jobs:
    build_and_test:
      runs-on: ubuntu-latest
      services:
        mysql:
          image: mysql:8.0
          env:
            MYSQL_ROOT_PASSWORD: Password123
            MYSQL_DATABASE: myapp_ci
          ports: [3306:3306]
          # health-check can be added here too
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-dotnet@v3
          with:
            dotnet-version: 7.0.x
        - name: Restore
          run: dotnet restore
        - name: Build
          run: dotnet build --no-restore --configuration Release
        - name: Run Tests
          run: dotnet test --no-build --verbosity normal
        - name: Build Docker image
          run: docker build -f MyApp.Api/Dockerfile -t myapp:ci .
        - name: Run Docker Compose (optional for integration tests)
          run: docker-compose up -d
      # ... possibly push to registry or other steps
  ```

  This is just a template. It:

  - Checks out code, sets up .NET 7.
  - Runs `dotnet test` (which could run integration tests; here we even started a MySQL service container for tests if needed).
  - Builds a Docker image.
  - You could add steps to login and push Docker image to a registry (using `docker login` and `docker push`). Using GitHub Packages or Docker Hub credentials stored as secrets in the workflow.

- **Azure DevOps**: Use Azure Pipelines YAML with similar steps (Azure DevOps has tasks for .NET build, test, docker).
- **GitLab CI**: Similar approach in `.gitlab-ci.yml`.

**Deployment Pipeline**:

- After building and pushing container images, you might have another job to deploy:
  - For Kubernetes: Use `kubectl` or an action like `azure/aks-set-context` (for AKS) then `kubectl apply -f k8s.yaml`.
  - For AWS: Use Amazon ECS or EKS actions, or AWS CLI to update services.
  - For Azure: Use Azure Web App for Containers or Azure Container Apps, which have their own deploy steps (e.g., Azure CLI action to push the image to Azure Container Registry and deploy).
- If not using containers in deploy, you could also deploy the built binaries:
  - e.g., use a self-hosted VM or cloud VM, and copy files or use an IIS deploy for Windows. But containerization often simplifies deploying across different environments.

**Continuous Integration** ensures every commit is built and tested. **Continuous Deployment** can automatically deploy certain branches (like main) to staging or production after passing tests.

For safety, implement approvals or manual triggers for production deploys, and deploy to staging automatically.

### 7.4 Deploying to Kubernetes or Cloud Platforms

**Kubernetes (K8s)**:

- Create Kubernetes manifests (YAML) for your deployment, service, configmaps, etc.
- For example, a Deployment for the API:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: myapp-api
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: myapp-api
    template:
      metadata:
        labels:
          app: myapp-api
      spec:
        containers:
          - name: api
            image: myregistry/myapp:latest
            ports:
              - containerPort: 5000
            env:
              - name: ConnectionStrings__MySqlConnection
                value: Server=mysql;Database=myapp_db;User Id=root;Password=Password123;
              # other env like Jwt keys, etc.
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: myapp-api-service
  spec:
    selector:
      app: myapp-api
    ports:
      - protocol: TCP
        port: 80
        targetPort: 5000
    type: LoadBalancer
  ```
  You would also have deployments for MySQL, Redis, Mongo or use managed services for those in production (e.g., use AWS RDS for MySQL instead of running MySQL in K8s, use Azure Cache for Redis, etc., to reduce ops overhead).
- Use a tool like **Helm** or **Kustomize** to manage these manifests for different env (like different values for DB passwords, etc.).
- In the CI/CD, after pushing images to a registry, use `kubectl` (with the kubeconfig of your cluster) to apply these manifests:
  ```
  kubectl apply -f k8s/deployment.yml
  ```
- Monitor the pods via `kubectl get pods` to ensure they run. Configure readiness and liveness probes for the API container (K8s can periodically hit a /health endpoint to ensure app is healthy, and restart it if not).

**Cloud PaaS**:

- If not using K8s, you can deploy the container directly:
  - **Azure Web App for Containers**: You can point it to the container image, or use Azure CLI: `az webapp create ... --deployment-container-image-name myregistry/myapp:latest`.
  - **Azure Container Apps** or **AWS App Runner**: These services run containers with minimal infrastructure management.
  - **AWS ECS (Fargate)**: Define a Task Definition JSON for the container, and use AWS CLI or CDK to update the service with the new image.
  - **Google Cloud Run**: Easy way to run containers on Google Cloud, with automatic scaling on request. Just deploy via gcloud CLI.

**Environment Configuration**:

- Use environment variables for configuration in containers (which we already did for connection strings, etc.). In Kubernetes, use ConfigMaps and Secrets for these values.
- Ensure sensitive values (DB passwords, JWT keys) are in Secrets and mounted as env vars, not in plain text in repo.

**Logging and Monitoring**:

- In containers, logs are written to stdout by default (the console). Setup your cluster or cloud to capture these (e.g., Azure App Insights, or cluster logging to Elastic stack or Azure Monitor).
- Use health probes as mentioned. Also consider distributed tracing (more in Advanced topics) for diagnosing issues in a distributed environment.

**Scaling**:

- Kubernetes can auto-scale based on CPU usage or custom metrics.
- In cloud offerings, enable auto-scaling or scale manually as needed.

Now your application is containerized and deployable consistently across environments, ensuring “it works on my machine” is less of a worry because every environment runs the same containers.

---

## 8. Advanced Topics

In this section, we explore advanced architectural patterns and technologies that can enhance the application: microservices, gRPC, event-driven architecture with messaging (RabbitMQ/Kafka), and observability through distributed tracing and centralized logging.

### 8.1 Microservices Architecture Considerations

Thus far, we built a **monolithic** application (all features in one deployable). As an application grows, you might consider a **microservices** approach: multiple smaller services, each focusing on specific business capabilities, communicating with each other.

**When to Microservice**:

- Microservices can be developed and deployed independently, and scaled individually. However, they add complexity in communication, data consistency, and deployment.
- Use microservices if parts of your application have distinct contexts, could be reused separately, or need to scale differently. For example, a separate _Order Service_, _Inventory Service_, _User Service_, etc., each with its own database (per the **database-per-service** pattern).

**Design Principles**:

- **Single Responsibility**: Each service owns a specific domain or feature (similar to bounded contexts in DDD).
- **Own Database**: Avoid sharing databases between services. If two services need data, they communicate via APIs or messaging. This ensures loose coupling.
- **Communication**: Use lightweight protocols (REST or gRPC) for sync communication, and messaging (RabbitMQ, Kafka, Azure Service Bus) for async communication and integration events.
- **Example**: In an e-commerce scenario, when an Order is placed in OrderService, it might publish an "OrderPlaced" event. InventoryService subscribes to that event to reduce stock, and PaymentService charges the customer. This way, services collaborate without direct coupling.

**Technologies**:

- .NET 7 is fully capable for microservices. You might create multiple ASP.NET Core projects (one for each microservice).
- Use **Ocelot** or YARP if you need an API Gateway to aggregate or route requests to microservices.
- Use **Consul** or **ETCD** or built-in DNS for service discovery (Kubernetes handles this with service names).
- **eShopOnContainers** is a great reference application by Microsoft that demonstrates .NET microservices with DDD, CQRS, and more.

**Challenges**:

- Transactions across services (distributed transactions) – often solved via eventual consistency or sagas, not 2-phase commit.
- Testing microservices – need to test each in isolation and as a whole.
- DevOps overhead – more services to deploy, monitor, and maintain.
- Start with a monolith until a clear need for microservices emerges (“MonolithFirst” approach). You can even **modularize** the monolith (e.g., using Clean Architecture, as below) so that splitting it into microservices later is easier.

### 8.2 Using gRPC alongside REST API

**gRPC** is a high-performance RPC framework that uses HTTP/2 as transport and Protocol Buffers (protobuf) for data serialization. .NET has first-class support for gRPC.

**Why gRPC**:

- Strongly-typed contracts via `.proto` files.
- Efficient binary serialization (Protobuf) – faster and smaller than JSON.
- Supports bi-directional streaming, making it great for real-time communication or chat, IoT, etc.
- Often used for internal service-to-service communication where performance matters (e.g., between microservices).

**Adding gRPC Service**:

- Add a new gRPC Service to the project:
  ```
  dotnet add package Grpc.AspNetCore
  ```
- Define a `.proto` file, e.g., `protos/order.proto`:

  ```proto
  syntax = "proto3";
  option csharp_namespace = "MyApp.Protos";

  service OrderService {
    rpc GetOrder (OrderRequest) returns (OrderReply);
    rpc StreamOrders (OrderStreamRequest) returns (stream OrderReply);
  }

  message OrderRequest { int32 orderId = 1; }
  message OrderReply { int32 orderId = 1; string status = 2; /* other fields */ }
  message OrderStreamRequest { string customerId = 1; }
  ```

- Configure the project to generate C# from proto. In the .csproj:

  ```xml
  <ItemGroup>
    <Protobuf Include="Protos\order.proto" GrpcServices="Server" />
  </ItemGroup>
  ```

  Installing Grpc.Tools (usually via the Grpc.AspNetCore meta package) allows build-time codegen for the defined messages and service base class.

- Implement the service:

  ```csharp
  public class OrderServiceImpl : OrderService.OrderServiceBase
  {
      private readonly IOrderRepository _orderRepo;
      public OrderServiceImpl(IOrderRepository orderRepo) { _orderRepo = orderRepo; }

      public override Task<OrderReply> GetOrder(OrderRequest request, ServerCallContext context)
      {
          var order = _orderRepo.Find(request.OrderId);
          OrderReply reply = new OrderReply { OrderId = order.Id, Status = order.Status };
          return Task.FromResult(reply);
      }

      public override async Task StreamOrders(OrderStreamRequest request, IServerStreamWriter<OrderReply> responseStream, ServerCallContext context)
      {
          // Stream all orders for a customer
          var orders = _orderRepo.GetByCustomer(request.CustomerId);
          foreach(var order in orders)
          {
              var reply = new OrderReply { OrderId = order.Id, Status = order.Status };
              await responseStream.WriteAsync(reply);
          }
      }
  }
  ```

- Register gRPC in Program.cs:
  ```csharp
  builder.Services.AddGrpc();
  ...
  app.MapGrpcService<OrderServiceImpl>();
  ```
  By default gRPC will listen on the same port as HTTP (but requires HTTP/2). If hosting on IIS/Azure Web Apps, additional config needed because gRPC uses HTTP/2 and some proxies might need config.

**Consuming gRPC**:

- A .NET client can be generated from the same proto (Grpc.Net.Client in .NET Core can call gRPC services).
- Other languages (Java, Go, Python, etc.) can use the proto to generate clients, since gRPC is language-agnostic and contract-first.
- You may choose to use gRPC internally (between services or for mobile apps) and still expose a public REST API for broader compatibility (since not all clients easily support gRPC, e.g., web browsers need gRPC-Web).

**gRPC vs REST**:

- gRPC is faster and has built-in code generation for messages and clients, but is not human-readable and not cacheable by HTTP proxies.
- REST+JSON is human-readable, easier for debugging, and widely used for public APIs.
- They can coexist: you can run both REST controllers and gRPC services in the same ASP.NET Core app (just need to ensure Kestrel is configured for HTTP/2 and endpoints don't conflict). Or split them into separate services.

### 8.3 Event-Driven Architecture with RabbitMQ/Kafka

**Event-driven architecture** decouples services by letting them communicate through events or messages:

- One component publishes an event (e.g., "UserRegistered", "OrderPlaced").
- One or many other components subscribe to these events and react accordingly.

This is implemented via **message brokers** like RabbitMQ (a popular open-source message queue), Apache Kafka (a distributed event log), or cloud services like Azure Service Bus or AWS SNS/SQS.

**RabbitMQ Example**:

- Add RabbitMQ client library:
  ```
  dotnet add package RabbitMQ.Client
  ```
- To publish an event:

  ```csharp
  var factory = new ConnectionFactory() { HostName = "localhost" };
  using var connection = factory.CreateConnection();
  using var channel = connection.CreateModel();
  channel.ExchangeDeclare(exchange: "UserExchange", type: ExchangeType.Topic);
  string message = JsonSerializer.Serialize(new { UserId = user.Id, Email = user.Email });
  var body = Encoding.UTF8.GetBytes(message);
  channel.BasicPublish(exchange: "UserExchange", routingKey: "User.Registered", basicProperties: null, body: body);
  ```

  This sends a message to the "UserExchange" with a routing key "User.Registered". Any queue bound to this exchange with a matching routing key pattern will receive it (publish/subscribe pattern).

- On the subscriber side (could be another service or the same app listening on a different thread):
  ```csharp
  channel.ExchangeDeclare("UserExchange", ExchangeType.Topic);
  var queue = channel.QueueDeclare().QueueName;
  channel.QueueBind(queue, "UserExchange", "User.Registered");
  var consumer = new EventingBasicConsumer(channel);
  consumer.Received += (model, ea) => {
      var body = ea.Body.ToArray();
      var message = Encoding.UTF8.GetString(body);
      // Process message (e.g., send welcome email)
      Console.WriteLine("Received event: " + message);
  };
  channel.BasicConsume(queue: queue, autoAck: true, consumer: consumer);
  ```
  RabbitMQ uses exchanges and queues: producers publish to exchanges, and consumers read from queues. Binding connects them.

**Kafka Example** (conceptually):

- Kafka deals with topics (similar to Rabbit exchanges).
- Use Confluent’s .NET client library to produce and consume messages. Kafka is partitioned and distributed, offering high throughput. It's often used for event streaming (lots of events, possibly persisted for long-term).

**Which to use?**:

- RabbitMQ is great for traditional message queue scenarios (task queues, pub-sub for events, complex routing).
- Kafka shines in streaming and when you need durability and high volume (it retains events for days, and consumers can replay).
- For enterprise systems, either could be the backbone of an event-driven architecture.

**Integrating into .NET services**:

- You might run a background worker in your API (using `IHostedService`) to listen for messages. But if adopting microservices, you likely have separate worker services dedicated to these tasks, not in the web API process.
- Ensure to handle message acknowledgments and error handling. You don’t want to lose messages; use retry or dead-letter queues for messages that fail processing.
- For idempotency: events might be delivered more than once in some systems, so design handlers to be idempotent (e.g., check if you already processed that message ID).

**Use Cases**:

- As mentioned, on user registration event, send an email via an EmailService.
- On order placed, publish event so InventoryService updates stock, AnalyticsService logs the sale, etc.
- Logging and metrics can also be sent via an event pipeline to be processed asynchronously, rather than blocking the main flow.

Using events can improve scalability (less direct coupling) and make the system more resilient (one part can go down, messages accumulate and will be processed when it’s up). It does add eventual consistency concerns – data changes are not immediately visible everywhere – but many large systems embrace that.

### 8.4 Observability with Distributed Tracing and Logging

Observability means you can understand the internals of your system from the outside – mainly through **logs, metrics, and traces**.

**Centralized Logging**:

- Instead of logging to console or files on each server, aggregate logs to a central system:
  - Use ELK stack (ElasticSearch, Logstash, Kibana) or Azure Monitor, AWS CloudWatch, etc.
  - Tools like Serilog have sinks for ElasticSearch. Or deploy a sidecar like Fluentd/Fluent Bit to ship logs.
- Structure logs (JSON format) for easier querying. e.g., log as JSON with fields like `eventId`, `userId`, etc.
- Use correlation IDs: for each request, assign a unique ID (GUID). Log this ID in all logs for that request (ASP.NET Core does this out-of-the-box with `RequestId` in the logging scope). It helps trace through logs for one transaction.

**Metrics**:

- Export metrics like request rate, error count, latency, memory usage. .NET has EventCounters and tools like App Insights or Prometheus integration.
- For example, track how many orders placed per minute, or current jobs in queue.

**Distributed Tracing**:

- In a microservices or complex environment, a single transaction might touch multiple services. Distributed tracing involves propagating a trace ID through calls so you can trace a user request across services.
- **OpenTelemetry** is the emerging standard. .NET has OpenTelemetry libraries that can automatically instrument HTTP client calls, gRPC calls, database calls, etc., capturing trace spans.
- Example: Use OpenTelemetry .NET SDK:

  ```csharp
  builder.Services.AddOpenTelemetryTracing(tracing =>
  {
      tracing.AddAspNetCoreInstrumentation()
             .AddHttpClientInstrumentation()
             .AddEntityFrameworkCoreInstrumentation()
             .AddJaegerExporter(); // send to Jaeger tracing system
  });
  ```

  With this, each incoming request creates a trace, and calls made via HttpClient or to EF Core will be recorded as child spans. The Jaeger exporter sends trace data to a Jaeger server (an open-source distributed tracing system).

- **Jaeger/Zipkin**: You can run Jaeger in Docker for local testing. Zipkin is another similar system. They provide UIs to view traces (timelines of calls). This helps pinpoint slow microservice calls or errors.
- **Trace Context Propagation**: If you call an external API, you might propagate `Traceparent` header (per W3C Trace Context standard) so that if that system also does tracing, it can join the trace. OpenTelemetry does this automatically for HttpClient in the same trace context.

**Example Scenario**:
A client calls `GET /api/orders/123`. In logs, we see:

- TraceID `abc123`, SpanID for API call.
- The API internally calls InventoryService via HTTP – the outgoing HttpClient call will have the same TraceID `abc123` and a new SpanID.
- InventoryService logs with the `abc123` TraceID.
- The API also perhaps queries the database – EF Core instrumentation logs a span for the SQL query, tied to `abc123`.
- If an error happens in any step, it's logged with the trace ID. Using Jaeger UI, you see a trace timeline: API -> InventoryService -> DB, with durations and any error flags.

This makes troubleshooting much easier in distributed systems where an error might cascade through services.

**High-Level Observability**:

- Set up alerts based on metrics (e.g., alert if 5xx errors > X per minute or if queue length too high).
- Dashboards: Create dashboards for key metrics (APM - Application Performance Monitoring tools like NewRelic, Dynatrace, or open source Grafana + Prometheus can be used).
- Regularly review logs for anomalies.

By implementing robust observability, you ensure that when (not if) issues occur in production, you can quickly diagnose and address them, maintaining reliability.

---

## 9. Best Practices and Design Patterns

Finally, we compile best practices and design patterns that underpin a maintainable, scalable .NET 7 application. We will cover the repository and unit of work patterns, dependency injection guidelines, Clean Architecture and Domain-Driven Design principles, and other tips.

### 9.1 Repository and Unit of Work Pattern

As mentioned in section 3.2, the Repository pattern provides an abstraction over data access, and Unit of Work (UoW) coordinates multiple repository operations into a single transaction.

**Repository Benefits**:

- **Abstraction**: Controllers or services deal with an interface (e.g., `IProductRepository`), unaware if data comes from EF Core, raw SQL, or an in-memory list. This decouples business logic from persistence.
- **Testability**: You can swap the real repo with a mock implementation in tests easily.
- **Consistent API**: Repositories can provide a uniform set of methods (Add, Get, Remove, etc.) for all aggregates, which can make switching out ORMs or data stores easier in the future.

**Unit of Work**:

- With multiple repositories, each might have its own DbContext instance if not careful. UoW ensures a single DbContext is used, so that SaveChanges covers changes across repositories.
- A simple UoW implementation:

  ```csharp
  public interface IUnitOfWork : IDisposable
  {
      IProductRepository Products { get; }
      IOrderRepository Orders { get; }
      Task<int> SaveChangesAsync();
  }

  public class UnitOfWork : IUnitOfWork
  {
      private readonly AppDbContext _db;
      public IProductRepository Products { get; }
      public IOrderRepository Orders { get; }
      public UnitOfWork(AppDbContext db, IProductRepository prodRepo, IOrderRepository orderRepo)
      {
          _db = db;
          Products = prodRepo;
          Orders = orderRepo;
      }
      public Task<int> SaveChangesAsync() => _db.SaveChangesAsync();
      public void Dispose() => _db.Dispose();
  }
  ```

  Here, `ProductRepository` and `OrderRepository` would use the shared `_db` context. Now a service can do:

  ```csharp
  using(var uow = _unitOfWorkFactory.Create()) {
      uow.Products.Add(product);
      uow.Orders.Add(order);
      await uow.SaveChangesAsync();
  }
  ```

  If any one of these operations fails to save, none are persisted (if SaveChanges is one transaction).

- In practice with DI, you might not explicitly need a UoW class if you manage transactions via DbContext. EF Core’s `DbContext` itself is a UoW: it tracks changes and on SaveChanges it commits all or nothing. However, if you want to ensure multiple repositories share one context in a single request, using a UoW or injecting the same context into all helps.

**When to use**:

- If your project is small, using DbContext directly in services might be fine and simpler. Repository/UoW patterns can add indirection but are very useful in large projects or domain-driven designs.
- Microsoft’s docs note that EF Core already implements a lot of repository/unit-of-work patterns for you, so adding another abstraction is sometimes redundant. Use your judgment; many projects still choose to implement them for the listed benefits.

### 9.2 Dependency Injection Best Practices

.NET Core has DI built-in. Some guidelines:

- **Service Lifetimes**:
  - Transient: new instance every time (use for lightweight, stateless services).
  - Scoped: one instance per scope (in web apps, per request). Use for services that hold data context like DbContext or business logic that should be consistent throughout a request.
  - Singleton: one instance for the app’s lifetime. Use for stateless services that are expensive to create or truly global (e.g., a memory cache, or a service interacting with a singletons like a file logger). Be careful with singletons that hold state – it’s shared across threads.
- **Avoid Captive Dependencies**: For example, a singleton service that depends on a scoped service is dangerous (the scoped will be created once and reused, effectively becoming a singleton or causing errors). This is usually detected by DI container as an error. Design lifetimes such that longer-lived services don't depend on shorter-lived ones.
- **Prefer Constructor Injection**: It’s the most straightforward method – require dependencies via the constructor. It makes it clear what a class needs and makes it easier to test (you can pass mocks).
- **Avoid Service Locator**: Don’t inject `IServiceProvider` and fetch services manually (that’s called service locator pattern, considered an anti-pattern because it hides dependencies). Let DI container do the work.
- **Register Interfaces**: Program to interfaces (e.g., register IProductRepository to ProductRepository). This allows swapping implementations (for testing, or if you change how it works).
- **Configure Services in Extension Methods**: If your Program.cs is getting long, create extension methods to group registration:
  ```csharp
  public static class ServiceCollectionExtensions {
      public static IServiceCollection AddMyAppServices(this IServiceCollection services) {
          services.AddScoped<IProductService, ProductService>();
          services.AddScoped<IProductRepository, ProductRepository>();
          // ... etc.
          return services;
      }
  }
  ```
  Then in Program.cs: `builder.Services.AddMyAppServices();`. This organizes code by responsibility.
- **Disposable Transients**: If you register a service as transient that implements IDisposable, it will **not** be disposed automatically (only scoped and singletons are disposed by container at end of scope/app). That could cause resource leaks. In such cases, either make it scoped or singleton as appropriate, or manage disposal manually.
- **Logging and Options**: .NET will inject ILogger<T> and IOptions<T> for you if configured. Use `IOptionsSnapshot` for scoped options that can change (like reloading config).
- **Verify Configuration**: In Program.cs, after building the app, you can use `app.Services.GetService<...>()` to ensure no required service is missing (this may throw if not found, which is good to catch early).

By following DI principles, your code becomes more modular, testable, and adheres to **Inversion of Control** (dependencies are injected, not constructed inside classes).

### 9.3 Clean Architecture Principles

Clean Architecture, popularized by Robert C. Martin (Uncle Bob) and also known as Hexagonal or Onion Architecture, emphasizes a separation of concerns and direction of dependencies:

- **Dependency Rule**: Source code dependencies can only point inward. Inner layers (Entities, Use Cases) know nothing about outer layers (UI, Infrastructure).
- **Layers** (from inner to outer):
  - **Entities/Domain**: Business objects, logic rules. Pure C# classes, no framework dependency.
  - **Use Cases/Application**: Coordinates between domain objects and what the application should do. Contains business rules implementations, might define repository interfaces (that domain needs to persist).
  - **Interface Adapters**: This layer converts data from the outside (DB, network) into a form the inner layers can use and vice versa. e.g., Repositories that implement domain interfaces, controllers converting DTOs to domain models.
  - **Infrastructure/Framework**: EF Core, Web frameworks, UI, any external agencies. This layer implements the contracts defined inward.

In practice with .NET projects:

- One project for **Domain** (entities, domain services, interfaces for repo).
- One project for **Application** (if separate, containing use case orchestrations, but often domain and application are combined in smaller apps).
- One project for **Infrastructure** (EF Core Data Context and Repos, Email senders, File access, external service implementations).
- One project for **API/UI** (controllers, views if any).

Our earlier structure (MyApp.Core, MyApp.Data, MyApp.Api) was a simplified Clean Architecture:

- MyApp.Core holds entities and interfaces (domain and some application logic).
- MyApp.Data is Infrastructure (EF Core, repository implementations).
- MyApp.Api is the Presentation layer (and it ties it all together).

**Benefits**:

- You can swap out infrastructure (e.g., change database) without touching business logic.
- You can unit test business logic in isolation (because it doesn’t depend on real DB).
- Code is organized by role, not by technology (contrast with traditional 3-layer where you might put all logic in one project and all data code in another – Clean Arch is similar but explicitly controls dependency direction).

**Example**:

- Domain: `Order` entity, `IOrderRepository`, `PlaceOrder` logic (maybe as a method or separate service).
- Infrastructure: `OrderRepository` (EF Core), `EmailService` (SMTP implementation).
- The Domain might also define an `IEmailService` interface if sending email is part of domain logic (or domain can publish an event and outer layer handles it).
- The API controller or Application service method invokes domain logic (maybe calls `order.Place()` which uses an injected repo to save and an injected email service to send confirmation).
- Thanks to DI, at runtime the concrete `OrderRepository` and `EmailService` (in infra) fulfill those interfaces.

**Domain-Driven Design (DDD)**:

- DDD aligns with Clean Architecture – focus on the domain model. Use **Ubiquitous Language** (terms that domain experts use reflected in class names, etc.).
- Break the system into **Bounded Contexts** – which can map to microservices or modules in a monolith.
- Inside each context, identify **Entities** (with identity, life cycle), **Value Objects** (immutable types defined by value, not identity), **Aggregates** (clusters of entities with a root that enforces invariants), **Domain Events** (to notify when something important in domain happens), and **Domain Services** (operations that don’t neatly fit into one Entity).
- Our example: In an Order context:
  - Entity: Order (with OrderItems as maybe entities or value objects).
  - Value Object: Money (for price), Address.
  - Aggregate: Order is the root, it ensures OrderItems are consistent (e.g., total price).
  - Domain Event: OrderPlaced event could be raised by Order aggregate.
  - Repository: IOrderRepository to save/load orders (ensuring only aggregate roots are directly accessed via repo).
- DDD encourages modeling complex business rules in the domain, rather than anemic models (just data holders). Methods on the entity (like `Order.AddItem(product, quantity)`) encapsulate invariants (like cannot add negative quantity).
- Use **Factory** methods or classes to create aggregates if creation logic is complex.
- Use **Specification** pattern for reusable business rules (though in .NET one might just use LINQ for querying).

Implementing DDD fully can be an extensive topic (often requiring deeper discussion on design). But applying even some concepts (rich domain model, clear bounded contexts, domain events) can greatly improve maintainability for complex projects.

### 9.4 Additional Best Practices and Patterns

A few more pointers and design patterns commonly used:

- **DTOs vs Entities**: Use Data Transfer Objects (DTOs) for interactions (in/out of API). Do not expose your EF Core entities directly to clients – this prevents over-posting attacks and hides internal fields. Use AutoMapper or manual mapping to translate between DTOs and domain models.
- **Validation**: Use both attribute-based validation for basic checks (required, range) and perhaps a Fluent Validation library for complex rules. Keep validation logic near the model it validates (Single Responsibility).
- **Error Handling Pattern**: Some use a Result<T> type to avoid throwing exceptions for flow control. E.g., `Result<Thing>` that has Success flag and Error messages. This can make the code more explicit about failure cases without exceptions overhead. But exceptions are fine for truly exceptional or unexpected errors.
- **Circuit Breaker / Retry**: When calling external services (including DB or message brokers), use patterns like Circuit Breaker and Retry (Polly library is great for this). E.g., if DB is down, a circuit breaker can fail fast after a few tries and then periodically test connection.
- **CQRS (Command Query Responsibility Segregation)**: Consider separating commands (writes) and queries (reads) if your read models differ from write models. This can mean different methods or even different data stores optimized for each. Full CQRS also often involves event sourcing, which is advanced – only use if needed.
- **Rate Limiting & Throttling**: In APIs, consider rate limiting to prevent abuse (could integrate with something like AspNetCoreRateLimit package or use cloud API management).
- **API Versioning Strategy**: Already covered, but ensure you document changes and have deprecation policies.
- **Documentation & Comments**: Maintain clear code comments especially for complex logic. Also produce external documentation for your API and architecture – it helps onboarding and maintenance.
- **Keep up with .NET**: .NET is evolving (as of writing, .NET 8 is around). New features (like built-in container support in .NET 7 SDK, or performance improvements) can simplify tasks. For example, .NET 7 introduced minimal APIs which can reduce boilerplate if appropriate for smaller services. Choose between minimal APIs vs controllers based on needs (controllers are still better for large apps with filters, etc.).
- **SOLID Principles**: Follow SOLID (Single Responsibility, Open/Closed, Liskov substitution, Interface segregation, Dependency inversion) as general guidance. We touched on DI (Dependency inversion), SRP (services and classes should have one reason to change).
- **YAGNI and KISS**: "You Ain't Gonna Need It" – don't over-engineer. Apply patterns as needed, but don't introduce unnecessary abstraction. Keep It Simple, make code readable and straightforward where possible.

Finally, always **review and refactor**. Regular code reviews catch issues early. Refactor mercilessly as you learn better ways or the requirements change. A clean, well-structured codebase with these best practices and patterns will be easier to extend and maintain, allowing your .NET 7 application to evolve gracefully over time.

---

**Conclusion:** We have walked through the entire journey of building a .NET 7 application. Starting from setting up the environment and project, configuring relational and NoSQL databases and caching, designing a RESTful API with robust security, optimizing for performance, testing thoroughly, containerizing for consistent deployments, and exploring advanced architecture and patterns. By following these steps and best practices, you can develop an enterprise-grade application ready for the modern cloud era. Happy coding with .NET 7!
