# Building a .NET Core Blog Application: A Step-by-Step Guide

**Introduction:**

This comprehensive guide walks through creating a **blog application** using modern .NET technologies and best practices. We'll use **.NET Core** (ASP.NET Core) for the Web API, implement **Clean Architecture** to separate concerns, apply the **CQRS** pattern with **MediatR** for in-memory messaging, integrate **Entity Framework Core** with **PostgreSQL** for data persistence, secure the application with **JWT authentication** and role-based **authorization**, and finally containerize the app with **Docker** and set up basic **CI/CD**. Along the way, we cover writing tests and optimizing performance (caching, pagination). This guide is aimed at **advanced .NET developers** and is structured as a professional resource with clear steps, code snippets, and best practices.

---

## 1. Project Setup and Architecture

Building a robust application starts with a solid foundation. In this section, we set up the project and apply **Clean Architecture** principles to organize our code. We will create a solution with multiple projects (layers) and configure essential services like Dependency Injection and Middleware.

### 1.1 Setting Up the Solution Structure

**Clean Architecture** (also known as Hexagonal or Onion architecture) encourages separating an app into layers (or **projects** in .NET) with clear responsibilities. The typical layers we will use are:

- **Domain** – Holds core entities and domain logic.
- **Application** – Contains business logic, use cases, interfaces, and DTOs. This layer implements CQRS handlers (commands/queries) and is independent of external frameworks.
- **Infrastructure** – Implements details like data access (EF Core), external services, file system, etc. This layer depends on **Application** (and Domain) to fulfill contracts.
- **API (Presentation)** – The ASP.NET Core Web API project. It depends on the **Application** (to execute commands/queries) and **Infrastructure** (for DI registration). It exposes endpoints to clients.

Clean Architecture ensures that **inner layers (Domain, Application) do not depend on outer layers** (Infrastructure, Presentation). Outer layers can depend on inner layers, but not vice versa ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=entire%20solution,shaped%20by%20following%20the%20Domain)) ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=independently%20from%20outer%20layers%20and,specific%20purpose%20is%20to%20communicate)). This dependency rule creates a resilient, testable system. In an ideal design, the Domain layer has no dependencies and contains only entities, value objects, and domain services or rules ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=itself%20implies,shaped%20by%20following%20the%20Domain)). The Application layer coordinates the domain to implement use cases (such as creating a blog post or adding a comment) and defines interfaces that the Infrastructure will implement (e.g., repository interfaces for data access). By keeping the **Domain** and **Application** layers free of infrastructure concerns, we can more easily maintain and evolve the software ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=application%20development,resilient%20and%20flexible%20software%20architectures)).

**Step 1:** Create a new solution and projects for each layer. Using the .NET CLI, you might do:

```bash
dotnet new sln -o BlogApp
cd BlogApp

# Create Class Library projects for Domain, Application, Infrastructure
dotnet new classlib -n BlogApp.Domain
dotnet new classlib -n BlogApp.Application
dotnet new classlib -n BlogApp.Infrastructure

# Create the ASP.NET Core Web API project for the Presentation layer
dotnet new webapi -n BlogApp.API

# Add projects to the solution
dotnet sln add BlogApp.Domain/BlogApp.Domain.csproj \
             BlogApp.Application/BlogApp.Application.csproj \
             BlogApp.Infrastructure/BlogApp.Infrastructure.csproj \
             BlogApp.API/BlogApp.API.csproj

# Add project references to establish layer dependencies
dotnet add BlogApp.Application/BlogApp.Application.csproj reference BlogApp.Domain/BlogApp.Domain.csproj
dotnet add BlogApp.Infrastructure/BlogApp.Infrastructure.csproj reference BlogApp.Application/BlogApp.Application.csproj
dotnet add BlogApp.API/BlogApp.API.csproj reference BlogApp.Application/BlogApp.Application.csproj
dotnet add BlogApp.API/BlogApp.API.csproj reference BlogApp.Infrastructure/BlogApp.Infrastructure.csproj
```

In the above setup:

- **BlogApp.Domain** has no dependencies (contains only domain models/entities).
- **BlogApp.Application** references Domain.
- **BlogApp.Infrastructure** references Application (and transitively Domain) to implement interfaces defined in Application.
- **BlogApp.API** (the Web API) references both Application and Infrastructure so it can call into Application logic and register Infrastructure implementations via DI.

This enforces the intended layering: _Domain <- Application <- Infrastructure <- API_. The **outer layers depend on inner layers, never the opposite** ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=itself%20implies,shaped%20by%20following%20the%20Domain)).

### 1.2 Domain Layer – Entities and Core Logic

The **Domain layer** defines the core data structures of the blog. For a blog application, typical domain entities might include:

- `Post` – representing a blog post (with properties like Id, Title, Content, Author, CreatedDate, etc.).
- `Comment` – a comment on a post (with Id, PostId, Author, Content, Timestamp, etc.).
- `Category` – a category or tag for posts.
- `User` – (if implementing users in the domain; alternatively, user info might be external if using Identity).

Domain entities are usually simple **POCO** classes. They can include basic validation or behaviors, but heavy business logic can also be encapsulated in domain services or in the Application layer. Ensure your domain classes are **persistence-ignorant** – they should not directly depend on EF Core or any data access details ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=When%20you%20use%20relational%20databases,simplified%20persistence%20into%20your%20database)) ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=From%20a%20DDD%20point%20of,and%20the%20Infrastructure%20Ignorance%20principles)). This means, for example, avoid `[Key]` or other EF attributes in this layer; instead, configure those in the Infrastructure (via EF Fluent API or configurations).

**Example – Domain Entity (Post):**

```csharp
namespace BlogApp.Domain.Entities
{
    public class Post
    {
        public Guid Id { get; private set; }
        public string Title { get; private set; }
        public string Content { get; private set; }
        public string AuthorId { get; private set; }   // e.g., user ID string
        public DateTime CreatedAt { get; private set; }
        public DateTime? LastModifiedAt { get; private set; }

        // Navigation properties for relationships
        private readonly List<Comment> _comments = new();
        public IReadOnlyCollection<Comment> Comments => _comments.AsReadOnly();
        public Category? Category { get; private set; }
        public Guid? CategoryId { get; private set; }

        // Constructors
        private Post() { /* For EF Core and serialization */ }

        public Post(string title, string content, string authorId, Guid? categoryId = null)
        {
            Id = Guid.NewGuid();
            Title = title;
            Content = content;
            AuthorId = authorId;
            CreatedAt = DateTime.UtcNow;
            CategoryId = categoryId;
        }

        // Domain behavior example
        public void UpdateContent(string newContent)
        {
            Content = newContent;
            LastModifiedAt = DateTime.UtcNow;
        }

        public void AddComment(string commentText, string commenterId)
        {
            var comment = new Comment(commentText, commenterId, this.Id);
            _comments.Add(comment);
        }
    }
}
```

This domain model is a plain C# class with no EF or infrastructure concerns. The `Post` class ensures integrity (for instance, only way to add a comment is via `AddComment` method which ensures the comment is linked to this post). All data required for persistence is present, but we haven't yet touched how to persist it – that will come in the Infrastructure layer.

### 1.3 Application Layer – Application Logic and CQRS Setup

The **Application layer** is where we organize **business logic** into use cases. Here we will introduce **CQRS (Command Query Responsibility Segregation)** and MediatR, but first, let's outline what goes into Application:

- **DTOs and ViewModels:** Data transfer objects if needed (e.g., `PostDto`, `CommentDto` for sending data to clients).
- **Interfaces:** Abstractions that the Application layer uses (for example, `IPostRepository`, `IUnitOfWork`, interfaces for external services or file storage if needed). These interfaces will be implemented in Infrastructure.
- **CQRS Commands & Queries:** Classes representing operations (commands to change state, queries to retrieve data) and their corresponding **Handlers**.
- **Validation**: You can include input validation logic, e.g., using FluentValidation for validating commands, or simple guard clauses inside handlers.

We'll delve deeper into CQRS in section 2, but in summary, **CQRS** means separating write operations (commands) from read operations (queries). Each command or query is handled by a dedicated **handler**. Using MediatR, we can dispatch these requests in-memory.

**Example – Application Interfaces:**

```csharp
namespace BlogApp.Application.Common.Interfaces
{
    public interface IPostRepository
    {
        Task<Post?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
        Task AddAsync(Post post, CancellationToken cancellationToken = default);
        // Other relevant methods like Update, Delete, List, etc.
    }

    public interface IUnitOfWork
    {
        Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    }
}
```

Here we define a repository interface for posts and a unit-of-work interface. The Application layer will use these interfaces. The **Infrastructure layer** will provide concrete implementations (e.g., using EF Core). This abstraction insulates our core logic from the details of data access ([Implementing the Repository and Unit of Work Patterns in an ASP.NET MVC Application (9 of 10) | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application#:~:text=The%20Repository%20and%20Unit%20of,Work%20Patterns)) ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=Repository%20patterns%20are%20intended%20to,simulating%20access%20to%20the%20database)). It also makes it easier to unit test the Application layer by mocking these interfaces.

**Important:** Some developers argue that with EF Core you don't always need a custom repository/unit-of-work because `DbContext` itself provides these patterns ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=Using%20a%20custom%20repository%20versus,using%20EF%20DbContext%20directly)). EF Core's `DbSet<TEntity>` can be considered a generic repository and `DbContext` as a unit-of-work. However, abstracting them via interfaces can still be useful for decoupling and testing ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=match%20at%20L286%20Repository%20patterns,simulating%20access%20to%20the%20database)). We'll implement these patterns as per our design, acknowledging that EF Core under the hood is already a unit-of-work.

### 1.4 API Layer – ASP.NET Core Project Setup

The **API layer** is the ASP.NET Core Web API project (BlogApp.API). Initially, it's a basic template with WeatherForecast, etc. We will configure it to use our Application layer.

**Program.cs Configuration:**

In .NET 6 and above (including .NET 7/8), the template uses the minimal hosting model. We'll register services and middleware in `Program.cs`. Key steps:

1. **Configure Services (Dependency Injection):** Register our Application and Infrastructure services (like DbContext, MediatR, repository implementations, etc.).
2. **Configure Middleware (HTTP Pipeline):** Use routing, authentication, authorization, exception handling, etc.
3. **Map Controllers or Endpoints:** We will use controllers for a structured API.

**Dependency Injection:** ASP.NET Core has a built-in IoC container that supports registering services with lifetimes (Transient, Scoped, Singleton) ([Dependency injection in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-9.0#:~:text=ASP,between%20classes%20and%20their%20dependencies)). We will use this to inject our dependencies. For example, we will register `IPostRepository` to its implementation, `IUnitOfWork` to an EF Core implementation, etc. This way, controllers or handlers can request these interfaces via constructor injection. DI promotes loose coupling and easier testing (we can swap implementations) ([Implementing the Repository and Unit of Work Patterns in an ASP.NET MVC Application (9 of 10) | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application#:~:text=The%20repository%20and%20unit%20of,driven%20development%20%28TDD)).

**Setting up DI in Program.cs:**

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

// 1. Add Controllers (since we're using MVC/Web API)
builder.Services.AddControllers();

// 2. Register Application services (if any) - e.g., MediatR, etc.
// (We'll cover MediatR in detail later, but for example)
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(BlogApp.Application.AssemblyMarker).Assembly));

// 3. Register Infrastructure services (Database, Repositories, etc.)
builder.Services.AddDbContext<BlogDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddScoped<IPostRepository, PostRepository>();
builder.Services.AddScoped<IUnitOfWork, EfUnitOfWork>();

// 4. (Optional) configure Swagger for API documentation in development
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 5. Build the app
var app = builder.Build();

// Configure middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage(); // Show detailed error pages in dev
    app.UseSwagger();
    app.UseSwaggerUI();
}
else
{
    app.UseExceptionHandler("/error"); // Global error handler in production (we can implement a controller for /error)
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseRouting();

// (Later we'll add Authentication & Authorization middleware here)

app.UseAuthorization();

app.MapControllers();

app.Run();
```

In the above snippet, note how we register DbContext and repository implementations. The `AddDbContext` call registers our EF Core context as a **scoped** service by default (scoped per HTTP request). Our repository and unit-of-work are also registered as scoped, so they share the same DbContext instance within a request. This is important to ensure all database operations in a single request use the same context (and therefore the same transaction). According to Microsoft, a scoped lifetime is recommended for DbContext in web apps to tie it to the request, which aligns with the unit-of-work pattern ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=The%20repository%20instance%20lifetime%20in,your%20IoC%20container)).

**Middleware Configuration:** By default, the template adds `UseRouting()` and `UseEndpoints` (or in this case `app.MapControllers()` which implicitly does endpoint routing). We also add `UseDeveloperExceptionPage()` in development for detailed error info, and `UseExceptionHandler` in production for a generic error handler. We will refine error handling later.

We include `UseAuthorization()` (and later will add `UseAuthentication()`) when we implement JWT authentication (section 5).

**Controllers Setup:** We will create controllers for our blog endpoints (Posts, Comments, Categories, etc.) in the API project. Initially, ensure the API project has the required NuGet packages and references:

- It should reference the Application and Infrastructure projects.
- Add `Microsoft.AspNetCore.Authentication.JwtBearer` (for JWT auth, covered later).
- Add `FluentValidation.AspNetCore` if using FluentValidation for model validation (optional advanced step).
- Ensure `MediatR.Extensions.Microsoft.DependencyInjection` is added to use `AddMediatR`.

We will postpone writing the controllers until we implement the CQRS handlers in the next sections, but you might create stubs like `PostsController`, `CommentsController` with `[ApiController]` and `[Route("api/[controller]")]` attributes. Each controller action will typically call `MediatR` to send a command or query and return the result.

At this point, our solution structure is in place. We have laid out the projects and prepared the API for further development. Next, we implement the CQRS pattern with MediatR in the Application layer.

---

## 2. Implementing CQRS with MediatR

**CQRS (Command Query Responsibility Segregation)** is a pattern where write operations (commands) are separated from read operations (queries) for clearer design and potential scalability benefits. With CQRS, **commands** modify state and **queries** retrieve state, and they are handled by different logic. We will use **MediatR**, a popular .NET library that implements the **Mediator pattern**, to dispatch these commands and queries within our application.

### 2.1 Understanding Commands vs. Queries

In CQRS:

- A **Command** is an operation that **changes state** (e.g., creating or editing a blog post). Commands typically **do not return data** (or might return a simple status or identifier) – their main purpose is side effects on the system (database changes, etc.).
- A **Query** is an operation that **reads data** without changing state (e.g., retrieving a list of posts or a post by ID). Queries return data and have **no side effects**.

MediatR models these with the `IRequest<T>` interface (or `IRequest` for void) and `IRequestHandler<TRequest,TResponse>` for handlers. We'll define our commands/queries as classes implementing `IRequest<T>` and their handlers implementing `IRequestHandler`.

According to best practices, **Commands should encapsulate all the data needed to perform the action**, and **Queries contain parameters needed to fetch data**. For example, a "CreatePost" command might contain Title, Content, AuthorId, CategoryId, etc. A "GetPosts" query might contain filters or pagination info.

_Why MediatR?_ MediatR decouples the sender of a request from its handler. Instead of our controllers or UI knowing about the service or method to call, they simply send a request (command/query) to the mediator. The mediator finds the appropriate handler and invokes it. This leads to a clean separation where the application logic is in the handlers, and the controllers are thin. It also helps with open/closed principle: adding new operations doesn't require modifying existing ones, just adding new request/handler pairs.

MediatR also supports pipelines (behaviors) that can be used for cross-cutting concerns (like logging, validation, etc.) in a central way.

**MediatR Benefits:** As DevLeader notes, _"MediatR facilitates the decoupling of software components, managing interactions between different parts of an application in an elegant and maintainable manner"_ ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=MediatR%20is%20a%20,an%20elegant%20and%20maintainable%20manner)). It allows objects to communicate indirectly through the mediator, reducing direct dependencies between them ([C# Clean Architecture With MediatR: How To Build For Flexibility | by Dev Leader | Dev Leader](https://medium.devleader.ca/c-clean-architecture-with-mediatr-how-to-build-for-flexibility-eeaeb16c3ddb#:~:text=MediatR%20is%20a%20,an%20elegant%20and%20maintainable%20manner)).

### 2.2 Adding MediatR to the Project

To use MediatR, install the NuGet package `MediatR.Extensions.Microsoft.DependencyInjection` in the Application (or API) project. We typically register MediatR in the API's startup, but it needs to know about our handlers which reside in the Application layer.

We already added a line in Program.cs:

```csharp
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(BlogApp.Application.AssemblyMarker).Assembly));
```

Here, `AssemblyMarker` is just any type in the Application assembly (we can create an empty static class for this) to help MediatR discover handlers in that assembly.

This single line tells MediatR to scan the Application assembly for any classes implementing `IRequestHandler<,>` and automatically register them. Thus our handlers will be picked up.

### 2.3 Defining Commands and Queries in the Application Layer

Let's define some command and query classes for our blog application. We will create a folder like `Application/Blog/Posts/` for grouping related commands and queries (this is optional but helps organize by feature).

**Examples:**

- **CreatePostCommand** – to create a new blog post.
- **UpdatePostCommand** – to edit an existing post.
- **DeletePostCommand** – to delete a post.
- **GetPostByIdQuery** – to retrieve a single post by ID.
- **ListPostsQuery** – to list posts, possibly with filtering or pagination.
- Similarly, commands/queries for Comments and Categories as needed.

**CreatePostCommand and Handler:**

```csharp
// Command
public record CreatePostCommand(string Title, string Content, string AuthorId, Guid? CategoryId) : IRequest<Guid>;

// Handler
public class CreatePostCommandHandler : IRequestHandler<CreatePostCommand, Guid>
{
    private readonly IPostRepository _postRepo;
    private readonly IUnitOfWork _unitOfWork;

    public CreatePostCommandHandler(IPostRepository postRepo, IUnitOfWork unitOfWork)
    {
        _postRepo = postRepo;
        _unitOfWork = unitOfWork;
    }

    public async Task<Guid> Handle(CreatePostCommand request, CancellationToken cancellationToken)
    {
        // Validate or transform input (could also use validators outside)
        var newPost = new Post(request.Title, request.Content, request.AuthorId, request.CategoryId);
        await _postRepo.AddAsync(newPost, cancellationToken);
        await _unitOfWork.SaveChangesAsync(cancellationToken);
        return newPost.Id;
    }
}
```

Here, `CreatePostCommand` is an **immutable record** carrying the required data. The handler uses the repository to add a new Post domain object and commits via UnitOfWork. It returns the `Guid` of the created post as the result.

**GetPostByIdQuery and Handler:**

```csharp
public record GetPostByIdQuery(Guid PostId) : IRequest<PostDto?>;

public class GetPostByIdQueryHandler : IRequestHandler<GetPostByIdQuery, PostDto?>
{
    private readonly IPostRepository _postRepo;
    private readonly IMapper _mapper; // if using AutoMapper for mapping to DTO

    public GetPostByIdQueryHandler(IPostRepository postRepo, IMapper mapper)
    {
        _postRepo = postRepo;
        _mapper = mapper;
    }

    public async Task<PostDto?> Handle(GetPostByIdQuery request, CancellationToken cancellationToken)
    {
        var post = await _postRepo.GetByIdAsync(request.PostId, cancellationToken);
        if (post == null) return null;
        // Map domain Post to PostDto (which might include comments, etc.)
        return _mapper.Map<PostDto>(post);
    }
}
```

This Query returns a `PostDto` (which we'd define in Application layer to shape the data for presentation). We assume an `IMapper` (like from AutoMapper) is injected to map Domain to DTO. If not using AutoMapper, you can manually map properties.

**Commands vs Queries Return Types:** Notice `CreatePostCommandHandler` returns `Guid` (the new ID) – a command can return something simple or even a full DTO, but often it's just an acknowledgment or new ID. `GetPostByIdQueryHandler` returns a `PostDto` (or null if not found).

The difference between commands and queries is also conceptual:
_"Commands ... often return void or a result indicating a command result. In contrast, queries fetch data ... returning a read-only response without side effects."_ ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=Commands%20in%20MediatR%20represent%20operations,without%20causing%20any%20side%20effects)).

### 2.4 Implementing Handlers and Validators

We have seen simple handler implementations. Let's discuss **validation**. We want to ensure invalid data doesn't make it to our core logic or database. We can validate in multiple ways:

- Using **Data Annotations** on our command DTOs (e.g., `[Required]` on Title).
- Using **FluentValidation** library to write more complex validation rules and integrate it with MediatR pipeline or ASP.NET ModelState.
- Manual validation in handlers (less ideal for repetitive rules).

For a professional approach, let's use **FluentValidation**. Install `FluentValidation.AspNetCore` and `FluentValidation.DependencyInjectionExtensions`. We can create validators for our commands:

```csharp
using FluentValidation;
public class CreatePostCommandValidator : AbstractValidator<CreatePostCommand>
{
    public CreatePostCommandValidator()
    {
        RuleFor(c => c.Title)
            .NotEmpty().WithMessage("Title is required")
            .MaximumLength(200).WithMessage("Title is too long (200 char max).");
        RuleFor(c => c.Content)
            .NotEmpty().WithMessage("Content is required");
        RuleFor(c => c.AuthorId)
            .NotEmpty().WithMessage("AuthorId is required");
    }
}
```

We then need to hook this into the pipeline. One way is to use MediatR's pipeline behaviors. For example, create a `ValidationBehavior<TRequest,TResponse>` that runs all validators for a request before the main handler executes:

```csharp
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : class, IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;
    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }
    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)
    {
        if (_validators.Any())
        {
            var context = new ValidationContext<TRequest>(request);
            var validationResults = await Task.WhenAll(
                _validators.Select(v => v.ValidateAsync(context, cancellationToken))
            );
            var failures = validationResults.SelectMany(r => r.Errors).Where(f => f != null).ToList();
            if (failures.Count != 0)
                throw new ValidationException(failures);
        }
        return await next();
    }
}
```

Then register this behavior with MediatR in Program.cs:

```csharp
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
builder.Services.AddValidatorsFromAssembly(typeof(BlogApp.Application.AssemblyMarker).Assembly);
```

Now, whenever a command/query is sent via MediatR, the validation behavior will run first, throwing an exception if any rules fail. We can catch that exception globally to return a 400 Bad Request with details (we'll handle that in error handling).

If not using FluentValidation, ensure to validate fields in the handler or controller and return appropriate errors.

### 2.5 Using MediatR for In-Memory Communication

With everything set up, how do we use MediatR in practice? In our controllers (or any part of the API layer), we inject `IMediator` (or `ISender`) and call `Send` with a request.

**Example – PostsController using MediatR:**

```csharp
[ApiController]
[Route("api/[controller]")]
public class PostsController : ControllerBase
{
    private readonly IMediator _mediator;
    public PostsController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpPost]
    public async Task<IActionResult> Create(CreatePostCommand command)
    {
        // The command will be automatically bound from request body (JSON) because it matches our action parameter
        Guid newPostId = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetById), new { id = newPostId }, null);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<PostDto>> GetById(Guid id)
    {
        var result = await _mediator.Send(new GetPostByIdQuery(id));
        if (result == null) return NotFound();
        return Ok(result);
    }

    // ... other actions (Update, Delete, etc.)
}
```

In the Create action, we send the CreatePostCommand. MediatR will find the `CreatePostCommandHandler` we wrote and execute it. The handler returns the new post's ID, which we use to return a 201 Created response with the URI of the new resource. In the GetById action, we send a query and return the data or 404 if not found.

Our controller does **not directly depend on any service or EF Core** – it only knows about MediatR and the request/response types. This decoupling means the controller logic is very minimal and all heavy lifting is in the Application layer.

MediatR works **in-memory**, meaning it simply invokes the handler within the same process. It's not a queue or service bus (though it could be extended to use those if needed). It's great for decoupling and organizing code within a monolith or microservice.

To summarize this section, we've set up MediatR and created command/query handlers implementing CQRS. We saw how **commands modify state** and **queries fetch state** ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=Commands%20in%20MediatR%20represent%20operations,without%20causing%20any%20side%20effects)), and how to dispatch them with MediatR. We also integrated validation via pipeline behaviors. Next, we will integrate the database using Entity Framework Core and PostgreSQL to persist our blog data.

---

## 3. Database Integration with Entity Framework Core and PostgreSQL

Now that our architecture and CQRS framework is in place, we need to persist data. We will use **Entity Framework Core (EF Core)** as our ORM and **PostgreSQL** as the database. In this section, we will configure EF Core to use Npgsql (the .NET data provider for PostgreSQL), create database **Migrations**, and implement the Repository and Unit of Work patterns in our Infrastructure layer.

### 3.1 Configuring EF Core with PostgreSQL

**Adding EF Core and Npgsql:** In the Infrastructure project, add the EF Core packages and Npgsql provider:

- `Microsoft.EntityFrameworkCore` (the base EF Core library).
- `Microsoft.EntityFrameworkCore.Relational` (for relational DB capabilities, may be included by base in recent versions).
- `Npgsql.EntityFrameworkCore.PostgreSQL` (the EF Core provider for PostgreSQL).
- `Npgsql` (the ADO.NET driver for PostgreSQL).

Using Package Manager Console or dotnet CLI:

```bash
dotnet add BlogApp.Infrastructure package Microsoft.EntityFrameworkCore.Design
dotnet add BlogApp.Infrastructure package Microsoft.EntityFrameworkCore
dotnet add BlogApp.Infrastructure package Npgsql.EntityFrameworkCore.PostgreSQL
```

(We include `EFCore.Design` to enable migrations commands in CLI or PMC).

**DbContext Setup:** In the Infrastructure layer, create a `BlogDbContext` class inheriting `DbContext`. This will coordinate EF Core.

```csharp
using Microsoft.EntityFrameworkCore;
using BlogApp.Domain.Entities;

namespace BlogApp.Infrastructure.Persistence
{
    public class BlogDbContext : DbContext
    {
        public BlogDbContext(DbContextOptions<BlogDbContext> options) : base(options) { }

        public DbSet<Post> Posts => Set<Post>();
        public DbSet<Comment> Comments => Set<Comment>();
        public DbSet<Category> Categories => Set<Category>();
        // ... and so on

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            // Fluent API configurations (if any complex configurations needed)
            // Example: modelBuilder.Entity<Post>(entity => { ... });
        }
    }
}
```

The `DbSet<T>` properties will let EF Core know about our entity classes. We should also consider configurations:

- Use `OnModelCreating` to configure relationships, keys, constraints if they are not by convention. For instance, ensure `Post.Id` is the key (by convention it is, since it's named Id).
- Configure cascading deletes or indexes as needed.
- If our domain classes used value objects or owned types, we'd configure those here.

**Connection String:** In the API project's **appsettings.json**, add a connection string for PostgreSQL:

```json
"ConnectionStrings": {
  "DefaultConnection": "Server=localhost;Port=5432;Database=BlogAppDb;User Id=postgres;Password=YourPassword;Pooling=true;"
}
```

Use your PostgreSQL credentials. The format is standard: `Host` (or Server), `Port`, `Database`, `Username`, `Password`. We will ensure this is used in the `AddDbContext` call we did earlier.

**Registering DbContext:** In Program.cs, we used:

```csharp
builder.Services.AddDbContext<BlogDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
```

This ties the `BlogDbContext` to the Postgres database using Npgsql. The `UseNpgsql` extension comes from the Npgsql EF Core provider package ([Using EFCore with Postgres | NimblePros Blog](https://blog.nimblepros.com/blogs/using-ef-core-with-postgres/#:~:text=You%20also%20need%20to%20update,code%20will%20look%20like%20this)). This single line configures the connection. (Make sure to have `using Npgsql.EntityFrameworkCore.PostgreSQL;` or the appropriate using for extension methods).

As the NimblePros blog notes, adding references to Npgsql and the EF Core provider is required, then you replace the default (like SQLite or InMemory) with `UseNpgsql` in your options ([Using EFCore with Postgres | NimblePros Blog](https://blog.nimblepros.com/blogs/using-ef-core-with-postgres/#:~:text=As%20the%20Clean%20Architecture%20template,PostgreSQL)). In our case, since we created from scratch, we directly used `UseNpgsql`.

**Verify configuration:** At this stage, if you run the application (e.g., via `dotnet run` or Visual Studio), EF Core will attempt to connect to the database. If the database doesn't exist or tables are missing, you'll get an error. We need to create the database schema via **Migrations**.

### 3.2 Creating Migrations and Applying Schema Changes

Entity Framework Core's Code First Migrations will help us create the database schema from our model definitions.

**Step 1:** Enable migrations in the Infrastructure project (where DbContext is). In PMC, select BlogApp.Infrastructure as the Default Project (or use CLI with `--project` flag) and run:

```
dotnet ef migrations add InitialCreate --startup-project ../BlogApp.API/BlogApp.API.csproj --output-dir Persistence/Migrations
```

Explanation:

- `--startup-project` points to the API project which holds the appsettings and where EF will get the connection string and other runtime services.
- `--project` (implicitly by running in Infrastructure directory or specifying) is the project containing DbContext.
- `--output-dir` specifies where to put the migration files (organized under Persistence/Migrations here).

This should scaffold a migration class representing the initial database creation (based on our DbSets and model). It will have `Up` method creating Posts, Comments, Categories tables with the appropriate schema.

Check the migration code to ensure keys and relationships look correct (adjust if needed by adding configurations or data annotations in the Domain model, then regenerating migration).

**Step 2:** Apply the migration to the database:

```
dotnet ef database update --startup-project ../BlogApp.API/BlogApp.API.csproj
```

This will connect to the database and execute the migration, creating the schema. After this, your PostgreSQL database should have the tables.

If you prefer, you can also use the `Database.EnsureCreated()` approach for simpler projects (which creates the database automatically if it doesn't exist, without migrations). However, for a professional app, Migrations are recommended to evolve the schema over time.

**Tip:** In development, you might use `EnsureCreated` for quick setup, but migrations are better for maintaining production databases and tracking changes.

### 3.3 Implementing Repository and Unit of Work Patterns

Our Application layer defined interfaces `IPostRepository` and `IUnitOfWork`. Now in Infrastructure, we implement these using EF Core.

**Repository Implementation (PostRepository):**

```csharp
using BlogApp.Application.Common.Interfaces;
using BlogApp.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace BlogApp.Infrastructure.Repositories
{
    public class PostRepository : IPostRepository
    {
        private readonly BlogDbContext _context;
        public PostRepository(BlogDbContext context)
        {
            _context = context;
        }

        public async Task<Post?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default)
        {
            return await _context.Posts
                         .Include(p => p.Comments)      // include comments (if needed)
                         .Include(p => p.Category)      // include category
                         .FirstOrDefaultAsync(p => p.Id == id, cancellationToken);
        }

        public async Task AddAsync(Post post, CancellationToken cancellationToken = default)
        {
            await _context.Posts.AddAsync(post, cancellationToken);
        }

        // Additional methods like Update, Delete, etc.
        public void Update(Post post)
        {
            _context.Posts.Update(post);
        }
        public void Remove(Post post)
        {
            _context.Posts.Remove(post);
        }
    }
}
```

This uses the EF `BlogDbContext` under the hood. Note that we do not call `_context.SaveChanges()` here – that's the job of the Unit of Work (so that multiple operations can be committed together).

**Unit of Work Implementation (EfUnitOfWork):**

```csharp
using BlogApp.Application.Common.Interfaces;
namespace BlogApp.Infrastructure
{
    public class EfUnitOfWork : IUnitOfWork
    {
        private readonly BlogDbContext _context;
        public EfUnitOfWork(BlogDbContext context)
        {
            _context = context;
        }
        public async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
        {
            return await _context.SaveChangesAsync(cancellationToken);
        }
    }
}
```

This is a thin wrapper around DbContext.SaveChangesAsync. It allows our Application layer to call `_unitOfWork.SaveChangesAsync()` without directly depending on EF’s DbContext, thus honoring the dependency inversion. It also makes it easier to swap implementations or mock the behavior in tests if needed.

As per Microsoft’s guidelines, the **Unit of Work** pattern is basically to share a single context across repositories and commit once ([Implementing the Repository and Unit of Work Patterns in an ASP.NET MVC Application (9 of 10) | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application#:~:text=Later%20in%20the%20tutorial%20you%27ll,use%20these%20classes%20without%20interfaces)). Our setup ensures a single `BlogDbContext` is injected into both the repository and unit-of-work (since both are scoped and resolved per request).

We should register these in DI (already done in Program.cs):

```csharp
builder.Services.AddScoped<IPostRepository, PostRepository>();
builder.Services.AddScoped<IUnitOfWork, EfUnitOfWork>();
```

This means whenever a `CreatePostCommandHandler` (for example) needs an `IPostRepository`, it gets a `PostRepository` with the same DbContext instance as the `EfUnitOfWork` it also gets injected. This is key for the pattern to work correctly.

**Transactions:** By default, EF Core will wrap SaveChanges in a transaction if multiple operations are pending. If you have multiple SaveChanges calls per request (not common if using UoW), you might need explicit transactions. But if all changes in a single request are done through one context and one SaveChanges at the end, it’s atomic.

**NoRepository Alternative:** As noted, EF DbContext already implements repository and unit-of-work patterns internally ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=Using%20a%20custom%20repository%20versus,using%20EF%20DbContext%20directly)). One could skip writing custom repositories and directly use `BlogDbContext` in handlers (via DI). However, introducing the repository interface decouples the persistence implementation from the application logic and can **facilitate testing with in-memory or fake implementations** ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=match%20at%20L286%20Repository%20patterns,simulating%20access%20to%20the%20database)). For advanced scenarios (like DDD aggregate rules, complex queries), a repository can also encapsulate those operations (for instance, a method `GetPostsByCategory(categoryId)` could be in the repository).

Our approach strikes a balance, showing the patterns in action. Keep in mind to avoid overly generic repositories that just duplicate what DbContext does. Each repository should be tailored to aggregate roots (e.g., Post is an aggregate root containing Comments) and provide meaningful methods for that aggregate.

### 3.4 Ensuring EF Core Configurations and Conventions

Before moving on, double-check that EF Core configurations align with your needs:

- **Table names and column names**: By default, EF will use DbSet property name or class name as table name (pluralization conventions were removed by default in EF Core). If you want to enforce snake_case naming (common in PostgreSQL), you might use modelBuilder conventions or manual configuration.
- **Relationship mappings**: Ensure the one-to-many from Post to Comments is recognized. Since we have `Post._comments` list and `Comment` likely has a `PostId`, EF should hook it up by convention. If not, we can explicitly configure `modelBuilder.Entity<Comment>().HasOne(c => c.Post).WithMany(p => p.Comments).HasForeignKey(c => c.PostId)`.
- **Cascade deletes**: By default EF might set cascade delete on required relationships. For example, deleting a Post might delete its Comments. Decide if that’s desired. You can configure `OnDelete` behavior in Fluent API if needed.
- **Indexes**: Consider adding indexes via annotations or Fluent API for commonly queried fields (like Post.CreatedAt if sorting by date, or CategoryId if filtering by category).
- **Value conversions**: If using any PostgreSQL-specific types (JSON, Array, etc.), ensure to configure via EF if necessary.

Finally, consider seeding some initial data (optional). EF Core migrations support data seeding via `modelBuilder.Entity<>().HasData()` ([CQRS and MediatR in ASP.NET Core - Building Scalable Systems - codewithmukesh](https://codewithmukesh.com/blog/cqrs-and-mediatr-in-aspnet-core/#:~:text=protected%20override%20void%20OnModelCreating)) ([CQRS and MediatR in ASP.NET Core - Building Scalable Systems - codewithmukesh](https://codewithmukesh.com/blog/cqrs-and-mediatr-in-aspnet-core/#:~:text=modelBuilder.Entity)). You could seed a couple of Category records or a default admin User, etc., in the initial migration for convenience.

At this stage, our Infrastructure layer is complete: we have EF Core connected to PostgreSQL, a DbContext, migrations for schema, and repository/UoW implementations. Next, let's build the Web API endpoints to expose our blog functionality.

---

## 4. Building APIs for the Blog Application

With the backend logic in place (CQRS commands/queries, EF Core integration), we can now create the **API endpoints** for clients to interact with the blog system. In this section, we will develop **CRUD endpoints** for blog posts, comments, and categories, and discuss API versioning, validation, and error handling strategies.

### 4.1 Designing the Controllers and Routes

We will have at least three controllers:

- `PostsController` – manage blog posts (create, update, delete, get one, get list).
- `CommentsController` – manage comments (perhaps adding a comment to a post, deleting a comment).
- `CategoriesController` – manage categories (create, list, etc., if needed for organizing posts).

For each controller:

- Use the `[ApiController]` attribute (this enables automatic ModelState validation and other conveniences).
- Base route as `api/[controller]` which will become `api/posts`, `api/comments`, etc.
- Return appropriate HTTP status codes:
  - 200 OK for successful GET or PUT.
  - 201 Created for successful creation (POST).
  - 204 No Content for successful deletion.
  - 400 Bad Request for validation errors (ModelState errors or thrown ValidationException from our pipeline).
  - 401 Unauthorized or 403 Forbidden for auth issues (when we add auth).
  - 404 Not Found for missing resources.
- Support optional features like **pagination** for listing posts (we can use query parameters `?page=1&pageSize=10` or similar).
- Later, we'll consider adding versioning.

We already sketched `PostsController` earlier. Let's flesh it out and similarly for comments:

**PostsController Implementation:**

```csharp
[ApiController]
[Route("api/[controller]")]
public class PostsController : ControllerBase
{
    private readonly IMediator _mediator;
    public PostsController(IMediator mediator) { _mediator = mediator; }

    // POST: api/posts
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreatePostCommand command)
    {
        // If using [ApiController], it auto-checks ModelState and returns 400 if invalid.
        var newPostId = await _mediator.Send(command);
        // Return 201 with location of new resource
        return CreatedAtAction(nameof(GetById), new { id = newPostId }, null);
    }

    // GET: api/posts/{id}
    [HttpGet("{id}")]
    public async Task<ActionResult<PostDto>> GetById(Guid id)
    {
        var post = await _mediator.Send(new GetPostByIdQuery(id));
        if (post == null) return NotFound();
        return Ok(post);
    }

    // GET: api/posts  (optionally with ?page etc.)
    [HttpGet]
    public async Task<ActionResult<List<PostDto>>> GetAll(int page = 1, int pageSize = 10)
    {
        var posts = await _mediator.Send(new ListPostsQuery(page, pageSize));
        return Ok(posts);
    }

    // PUT: api/posts/{id}
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(Guid id, [FromBody] UpdatePostCommand command)
    {
        if (id != command.PostId)
            return BadRequest("ID in URL and body do not match.");
        await _mediator.Send(command);
        return NoContent();
    }

    // DELETE: api/posts/{id}
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(Guid id)
    {
        await _mediator.Send(new DeletePostCommand(id));
        return NoContent();
    }
}
```

Things to note:

- In Update, we ensure the route ID matches the command’s Id to avoid confusion.
- We return `NoContent` on Update and Delete (common practice when no response body is needed).
- We introduced a `ListPostsQuery` for pagination. You'd implement `ListPostsQueryHandler` to fetch a page of posts (e.g., via `_postRepo` with Skip/Take in EF). Also consider returning total count or pagination metadata (you could define a response model like `PagedResult<PostDto>` with properties Results + TotalCount).
- We used `[FromBody]` explicitly for clarity, but with [ApiController] it's implied for complex types in POST/PUT.

**CommentsController Implementation:**

For comments, we might consider that adding a comment is logically a sub-resource of posts. We could design the route as `POST /api/posts/{postId}/comments` instead of a separate top-level comments endpoint. This is a design decision. For simplicity, let's create a CommentsController but use the route to reflect the relationship:

```csharp
[ApiController]
[Route("api/posts/{postId}/[controller]")]
public class CommentsController : ControllerBase
{
    private readonly IMediator _mediator;
    public CommentsController(IMediator mediator) { _mediator = mediator; }

    // POST: api/posts/{postId}/comments
    [HttpPost]
    public async Task<IActionResult> AddComment(Guid postId, [FromBody] AddCommentCommand command)
    {
        if (postId != command.PostId)
            return BadRequest("PostId mismatch.");
        var newCommentId = await _mediator.Send(command);
        return CreatedAtAction(nameof(Get), new { postId = postId, id = newCommentId }, null);
    }

    // GET: api/posts/{postId}/comments/{id}
    [HttpGet("{id}")]
    public async Task<ActionResult<CommentDto>> Get(Guid postId, Guid id)
    {
        var comment = await _mediator.Send(new GetCommentQuery(postId, id));
        if (comment == null) return NotFound();
        return Ok(comment);
    }

    // DELETE: api/posts/{postId}/comments/{id}
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(Guid postId, Guid id)
    {
        await _mediator.Send(new DeleteCommentCommand(postId, id));
        return NoContent();
    }
}
```

This illustrates nested routing. We ensure the comment’s PostId is taken from the URL for consistency. The commands `AddCommentCommand`, `GetCommentQuery`, `DeleteCommentCommand` would be defined similarly to others (with handlers using repository to manipulate comments, probably via the Post aggregate).

**CategoriesController:**

Likewise, a simple controller to manage categories (like list all categories, create a category, etc.) can be created if needed for the blog.

### 4.2 API Versioning

As our API grows, supporting versioning is a best practice so that changes can be introduced without breaking existing clients. For advanced scenarios, you might use the **Microsoft ASP.NET Core API Versioning** library.

To use it:

- Install `Microsoft.AspNetCore.Mvc.Versioning`.
- In `Program.cs`, add:
  ```csharp
  builder.Services.AddApiVersioning(options =>
  {
      options.AssumeDefaultVersionWhenUnspecified = true;
      options.DefaultApiVersion = new ApiVersion(1, 0);
      options.ReportApiVersions = true;
  });
  ```
- Decorate controllers or actions with `[ApiVersion("1.0")]` and use route tokens like `"/api/v{version:apiVersion}/[controller]"` in Route attributes to expose versioned routes.

However, if our blog API is small and under our control, we might not need multiple versions immediately. We'll design with versioning in mind (e.g., the URL could include `/v1/` if needed). The code above enables basic versioning with querystring or header by default, or URL if specified. For simplicity, we might skip actual multiple versions in this guide.

But if implementing, you might have controllers in namespaces or with attributes for v1 and future v2, etc., side by side.

**Best Practice:** If you foresee breaking changes, set up versioning early. Otherwise, at least plan your routes such that adding version prefix later is possible (like not hard-coding versionless routes everywhere in clients).

### 4.3 Validation and Error Handling in the API

We already integrated validation via FluentValidation for commands. With `[ApiController]`, any data annotation validation errors on action parameters (like required fields missing) will automatically produce a 400 response with details, without us writing any code.

For FluentValidation errors (thrown as `ValidationException` in our pipeline), we should handle them. One approach: a custom error-handling middleware or the `UseExceptionHandler` we set up to catch exceptions and shape error responses.

**Global Error Handling:** We can write a middleware that catches exceptions and returns an appropriate `ProblemDetails` JSON (which is the standardized error format in ASP.NET Core).

Example global exception handling middleware:

```csharp
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
        context.Response.ContentType = "application/json";
        var contextFeature = context.Features.Get<IExceptionHandlerPathFeature>();
        if (contextFeature != null)
        {
            Exception ex = contextFeature.Error;
            // Set specific status codes for known exceptions
            if (ex is ValidationException)
            {
                context.Response.StatusCode = StatusCodes.Status400BadRequest;
                var problem = new ValidationProblemDetails(((ValidationException)ex).Errors.ToDictionary(
                                    err => err.PropertyName,
                                    err => new string[] { err.ErrorMessage }))
                {
                    Type = "https://httpstatuses.com/400",
                    Title = "One or more validation errors occurred.",
                    Status = StatusCodes.Status400BadRequest
                };
                await context.Response.WriteAsJsonAsync(problem);
            }
            else
            {
                // Log the exception (not shown here)
                var problem = new ProblemDetails
                {
                    Title = "An unexpected error occurred!",
                    Status = StatusCodes.Status500InternalServerError,
                    Detail = app.Environment.IsDevelopment() ? ex.ToString() : null
                };
                await context.Response.WriteAsJsonAsync(problem);
            }
        }
    });
});
```

This is placed before `app.UseRouting()` typically (or configured via `UseExceptionHandler` as shown). What it does:

- If a `ValidationException` is caught, returns HTTP 400 with a `ValidationProblemDetails` containing the errors (mapping property names to error messages).
- For any other exception, returns a generic 500 with maybe the stack in dev.

Now, our API will send back clear errors for validation issues (e.g., missing Title will result in a 400 with that info) and hide internal exceptions from the user (just show generic message, but you should log the details on server).

**Additional Error Handling:** We also consider 404s for not found (we already do that in controllers), 401/403 will be handled by [Authorize] (the framework will handle those responses if not authenticated/authorized).

### 4.4 Putting It All Together – Testing the API Endpoints

At this point, it’s good to manually test the API (or write integration tests which we'll cover later). Run the API (F5 or `dotnet run`) and use a tool like **Postman** or **curl** to try endpoints:

- `POST /api/posts` with a JSON body:
  ```json
  {
    "title": "Hello World",
    "content": "This is my first post",
    "authorId": "user123",
    "categoryId": null
  }
  ```
  Should return 201 Created. Check the Location header or try GET.
- `GET /api/posts/{id}` for the ID returned above, should return the post data (likely in our `PostDto` shape).
- `PUT /api/posts/{id}` to update a post (with JSON body containing the updated content and the same id).
- `GET /api/posts` to list posts (we might have implemented it to return just a subset or all).
- `POST /api/posts/{id}/comments` to add a comment to a post.
- `DELETE /api/posts/{id}` to delete a post (then GET should return 404 after deletion).

Also test validation:

- Send an empty body to `POST /api/posts` – should get 400 with validation errors (Title required, etc.).
- Send a malformed GUID etc., the model binding might catch it as 400.

All basic CRUD should now be functioning. The API is nearly complete. Next, we focus on securing it with authentication and authorization.

---

## 5. Authentication and Authorization

Most blog applications require user accounts, authentication, and roles (e.g., admin vs regular user). We will implement **JWT authentication** for our API and demonstrate **role-based authorization** for certain endpoints (for example, only an admin or the post author can delete a post).

### 5.1 Implementing JWT Authentication

**JSON Web Tokens (JWT)** are a common way to authenticate APIs in a stateless manner. The idea is that after a user logs in (perhaps via a separate identity service or endpoint), the client gets a JWT, which it includes in the `Authorization: Bearer <token>` header of requests. The server validates the token on each request, and if valid, the request is authenticated.

For our guide, we'll assume an external identity system or a simple custom login that issues tokens. We focus on configuring the API to **accept and validate JWTs**.

**Setup JWT Bearer in ASP.NET Core:**

1. **Add JWT Authentication services** in Program.cs:
   ```csharp
   using Microsoft.AspNetCore.Authentication.JwtBearer;
   using Microsoft.IdentityModel.Tokens;
   // ...
   var builder = WebApplication.CreateBuilder(args);
   // ... (other service registrations)
   builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
       .AddJwtBearer(options =>
       {
           options.TokenValidationParameters = new TokenValidationParameters
           {
               ValidateIssuer = true,
               ValidateAudience = true,
               ValidateLifetime = true,
               ValidateIssuerSigningKey = true,
               ValidIssuer = builder.Configuration["Jwt:Issuer"],
               ValidAudience = builder.Configuration["Jwt:Audience"],
               IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
           };
       });
   ```
   In your configuration (appsettings.json or user secrets), you need to provide `"Jwt": { "Issuer": "...", "Audience": "...", "Key": "a very long random secret key" }`. The **Key** is the symmetric secret your server uses to sign tokens (in a real scenario, a secure, ideally 256-bit key). The parameters here ensure the token's issuer and audience match what we expect and that the signature is valid ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=JWT%20,header%20and%20a%20bearer%20token)) ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=,is%20known%20as%20delegated%20authorization)). `ValidateLifetime` will ensure the token hasn't expired.
2. **Enable Authentication Middleware**: In the request pipeline (Program.cs), add `app.UseAuthentication();` **before** `UseAuthorization()`. This ensures that on each request, ASP.NET will attempt to decode and validate the JWT from the headers and set the `User` (ClaimsPrincipal) if successful.

3. **Protect Endpoints**: Use `[Authorize]` attribute on controllers or actions that require login. For example, on PostsController, we might put `[Authorize]` on all actions by decorating the controller class (so all actions require auth), except maybe GET for public blogs if desired. Or we can allow viewing posts without login but require login for create/update/delete.

If we need an endpoint for login (issuing JWTs), we could implement one in a separate AuthController. However, that's outside scope (could use Identity or manual token issuing).

**How JWT works (brief):** A JWT is a base64-encoded token with a header, payload, and signature. When the server receives it, the `JwtBearerHandler` will decode it using the signing key (for symmetric HS256 signing) and validate claims. If valid, the user’s claims (like user ID, roles, etc.) are available in `HttpContext.User`. This is done for each request, so it’s stateless (no session on server). Microsoft’s default JWT handler can manage this easily, as long as the token is properly issued and the server has the key to validate.

From the Microsoft docs: _"JWT bearer authentication is commonly used for APIs... The identity provider issues a JWT on successful authentication, which can be sent to other servers to authenticate. A JWT is self-contained (claims about user's identity/permissions)."_ ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=JWT%20,header%20and%20a%20bearer%20token)).

### 5.2 Managing User Roles and Permissions

**Role-Based Authorization:** Once authentication is in place and we have user identities, we can restrict certain actions to certain roles or to the resource owner.

For example, in a blog:

- Only **admins** or **the author of a post** should be able to delete or edit that post.
- Only logged-in users can create comments; perhaps any logged-in user can comment, but only admins can delete any comment, while regular users can only delete their own comment.

We will use ASP.NET Core's built-in role-based authorization for this.

If using ASP.NET Identity or another system, a JWT can include a claim like `roles: ["Admin"]` or similar. The JWT handler will map that to `User.IsInRole("Admin")`.

**Applying role policies:**

- Decorate controllers or actions with `[Authorize(Roles = "Admin")]` to allow only users with that role. For example, to restrict deletion of posts to admins:

  ```csharp
  [Authorize(Roles = "Admin")]
  [HttpDelete("{id}")]
  public async Task<IActionResult> Delete(Guid id) { ... }
  ```

  This means if the JWT does not have role "Admin", the framework will automatically return 403 Forbidden for that request ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)).

- You can specify multiple roles: `[Authorize(Roles = "Admin,Moderator")]` means user must be in either Admin or Moderator role ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)).

Alternatively, for more complex logic (like author can delete their own post, or Admin can delete any), role alone isn't enough. You could use **policy-based authorization** where you write an authorization handler that checks the resource. For simplicity, one could check inside the action:

```csharp
// Inside Delete action
var post = await _mediator.Send(new GetPostByIdQuery(id));
if (post == null) return NotFound();
if (User.Identity?.Name != post.AuthorId && !User.IsInRole("Admin"))
    return Forbid(); // 403 if not author or admin
await _mediator.Send(new DeletePostCommand(id));
return NoContent();
```

Here we assume the JWT contains a NameIdentifier or Name claim that we set to user ID.

**Registering Roles:** If we had a user registration system, roles would be assigned there. In ASP.NET Core Identity, you'd call `AddRoles<IdentityRole>()` during setup ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=builder.Services.AddDefaultIdentity)). But if our tokens already have roles, we don't need Identity on the API, just trust the token's claims.

**Summary of Authorization:** We use `[Authorize]` attribute to enforce authentication and optionally specify roles or policies. It's declarative and ensures only allowed users reach the action's code ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)). Role checks can also be done imperatively via `User.IsInRole` or claims checks if needed.

From Microsoft docs: _"Role-based authorization checks are declarative – the developer embeds them in code against controllers or actions. For example, `[Authorize(Roles = "Administrator")]` on a controller limits access to only users in that role."_ ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)).

### 5.3 Testing Authentication & Authorization

After configuring, test the following:

- Without any token, calls to protected endpoints should result in 401 Unauthorized.
- With an invalid or expired token, also 401.
- With a valid token but lacking necessary role, should get 403 Forbidden on endpoints that require a specific role.
- With valid admin token, should be able to perform all actions.
- With valid normal user token, can perform allowed actions (like create post if we allow any authenticated user to create, or create comment, etc.), but get 403 on disallowed ones (like deleting someone else's post if we coded that check).

At this point, the application has a full authentication and authorization setup. The next steps cover containerization and deployment.

---

## 6. Dockerization and Deployment

Deploying our application in a consistent environment is important for production. We will containerize the application using **Docker** and also set up a **docker-compose** for running the app and the database together. Additionally, we discuss setting up a simple CI/CD pipeline (e.g., with GitHub Actions) to build and deploy the app.

### 6.1 Creating Dockerfiles for the Application

We'll create a Docker image for the ASP.NET Core API. .NET provides official base images for runtime and SDK.

**Dockerfile for BlogApp.API:**

In the API project folder, create a file named `Dockerfile` (no extension). A common approach is to use a **multi-stage build** to minimize final image size:

```Dockerfile
# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj files and restore as distinct layers
COPY BlogApp.Domain/BlogApp.Domain.csproj BlogApp.Domain/
COPY BlogApp.Application/BlogApp.Application.csproj BlogApp.Application/
COPY BlogApp.Infrastructure/BlogApp.Infrastructure.csproj BlogApp.Infrastructure/
COPY BlogApp.API/BlogApp.API.csproj BlogApp.API/
RUN dotnet restore BlogApp.API/BlogApp.API.csproj

# Copy the rest of the source code
COPY . .
WORKDIR /src/BlogApp.API

# Build and publish the app (release mode, to out folder)
RUN dotnet publish -c Release -o /app/out

# Stage 2: Run
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/out ./
ENTRYPOINT ["dotnet", "BlogApp.API.dll"]
```

Explanation:

- Uses the .NET 8 SDK image to build. We copy project files and run `dotnet restore` first to utilize caching (so that changes in code don't invalidate restoring packages).
- Then copy all code and run `dotnet publish`, which produces compiled output in `/app/out`.
- Second stage uses a lighter **ASP.NET Core runtime** image (no SDK). It copies the published output and sets the entrypoint to run the .dll.
- We expose no ports here; we rely on docker-compose to publish ports.

This Dockerfile defines how to build the container image. It results in a final image that is relatively small (only the runtime plus our app). Each command like `FROM`, `WORKDIR`, `COPY`, `ENTRYPOINT` has specific roles ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20,of%20the%20container%20to%20App)) ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20next%20command%2C%20,ends%2C%20the%20container%20automatically%20stops)):

- `FROM` sets the base image (the environment like .NET runtime) ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20,of%20the%20container%20to%20App)).
- `WORKDIR` sets working directory inside container ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20,of%20the%20container%20to%20App)).
- `COPY --from=build` copies files from the build stage's output to the final image ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20,of%20the%20container%20to%20App)).
- `ENTRYPOINT` defines the process that will run when the container starts (our web API) ([Containerize an app with Docker tutorial - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container#:~:text=The%20next%20command%2C%20,ends%2C%20the%20container%20automatically%20stops)).

Make sure to adjust .NET version tags (if using .NET 7, use appropriate tags). The example above uses .NET 8.

### 6.2 Docker Compose Configuration

We'll use **docker-compose** to run our API container and a PostgreSQL container together, so it's easy to start the whole stack with one command for development or testing.

Create a `docker-compose.yml` file at the solution root:

```yaml
version: "3.9"
services:
  api:
    build:
      context: .
      dockerfile: BlogApp.API/Dockerfile
    ports:
      - "5000:80" # map host port 5000 to container's port 80
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=db;Port=5432;Database=BlogAppDb;Username=postgres;Password=YourPassword
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=YourPassword
      - POSTGRES_DB=BlogAppDb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
```

Explanation:

- We define two services: **api** and **db**.
- **api** uses the Dockerfile to build the image (context is the root, we specify the path to Dockerfile). It publishes container's port 80 to host's 5000 (so we can browse http://localhost:5000).
- We set environment variables:
  - `ASPNETCORE_ENVIRONMENT=Development` (so it uses development settings, shows swagger etc., you can change as needed).
  - Connection string is provided via environment with `ConnectionStrings__DefaultConnection` (this is how hierarchical config in appsettings is passed: section\_\_key). We point it to `Host=db` which is the hostname of the db service in compose ([Docker: Adding PostgreSQL to .Net Core - Part 2 - IntelliTect](https://intellitect.com/blog/docker-postgresql/#:~:text=is%20just%20the%20name%20we,send%20it%20straight%20toward%20the)), and the credentials as per db service env.
- `depends_on: db` ensures the db container starts before the api (though we might still need to handle retry logic in the app if db isn't immediately ready).
- **db** uses official Postgres image. We set a volume to persist data, and environment vars for user, password, and database name.
- We open port 5432 for convenience (in a real server, maybe not needed to expose outside).
- Define a named volume `pgdata` to persist database between runs.

With this file, a developer (or CI pipeline) can run `docker-compose up --build` and the whole app will come up. The .NET API will connect to the "db" service thanks to Docker's internal DNS ([Docker: Adding PostgreSQL to .Net Core - Part 2 - IntelliTect](https://intellitect.com/blog/docker-postgresql/#:~:text=is%20just%20the%20name%20we,send%20it%20straight%20toward%20the)).

We should ensure the app uses the connection string from env when in a container. Our Program.cs was using `builder.Configuration.GetConnectionString("DefaultConnection")`. This will pick up from appsettings by default. But because we provided an environment variable, by default ASP.NET will also consider environment variables (with that naming convention) as configuration. The `ConnectionStrings__DefaultConnection` will override the appsettings value. So it should work automatically.

**Testing docker-compose:** You can test locally by running the compose command. Check that the app can indeed talk to the database (the first run might fail if the app tries to connect before Postgres is ready; if so, consider adding retry logic or use a wait-for script. Simpler: configure EF to retry on failure).

### 6.3 Setting up CI/CD with GitHub Actions

Now that Dockerization is done, we can automate building and deploying this container. Let's outline a simple GitHub Actions workflow for CI (Continuous Integration) and possibly CD.

**GitHub Actions Workflow (ci-cd.yml):**

```yaml
name: CI-CD

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    env:
      IMAGE_NAME: your-dockerhub-username/blogapp-api
    steps:
      - uses: actions/checkout@v3

      - name: Set up .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: "8.0.x" # adjust for your .NET version

      - name: Restore dependencies
        run: dotnet restore BlogApp.API/BlogApp.API.csproj

      - name: Build
        run: dotnet build --no-restore -c Release BlogApp.API/BlogApp.API.csproj

      - name: Run Tests
        run: dotnet test --no-build -c Release

      - name: Build Docker Image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: BlogApp.API/Dockerfile
          push: false
          tags: ${{ env.IMAGE_NAME }}:latest

      - name: Push to DockerHub
        uses: docker/build-push-action@v4
        with:
          context: .
          file: BlogApp.API/Dockerfile
          push: true
          tags: ${{ env.IMAGE_NAME }}:latest
        env:
          DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
          DOCKERHUB_PASSWORD: ${{ secrets.DOCKERHUB_PASSWORD }}
```

Explanation:

- Trigger on push to main (adjust as needed).
- It checks out code, sets up .NET, restores, builds, and tests the application.
- Uses the `docker/build-push-action` GitHub Action to build the Docker image. We do it in two steps: first just build (and optionally load it to run tests inside container if needed), then push. Or we could combine, but here shown separate for clarity.
- We use secrets for Docker Hub credentials (you'd set those in your GitHub repo settings).
- This pushes an image tagged as `latest` to Docker Hub (or any registry). You could also tag with the Git commit or version.
- If deploying to a server, you might then use SSH or other actions to pull the image on the server and run `docker-compose up -d` or deploy to a Kubernetes cluster, etc. That part depends on your environment (could be AWS ECS, Azure Web App for Containers, etc.).

For **Azure DevOps**, a similar pipeline can be created with YAML, or using their classic pipeline. But describing both would be lengthy; the steps are analogous: use a build agent, .NET CLI tasks, then Docker tasks.

By setting up CI/CD, each commit gets validated (build & tests) and the artifact (Docker image) is produced. This greatly enhances reliability and speed of deployments.

### 6.4 Deployment Considerations

When deploying:

- Use environment variables for sensitive config (like actual DB password, JWT secrets) instead of putting them in images or code.
- Consider using **Docker secrets** or orchestrator secrets for production.
- If deploying via docker-compose on a server, ensure to use strong passwords and maybe not expose DB port publicly.
- Use a reverse proxy or cloud load balancer if needed (or configure the container to use HTTPS with certificates).

For scaling, one could run multiple instances of the API container behind a load balancer. Because we used a stateless JWT auth and a shared database, scaling horizontally should be fine. Caching (next section) might need consideration if using in-memory cache in multiple instances (maybe use distributed cache like Redis in that case).

We have now containerized and set up an automation pipeline. Finally, let's cover testing and performance optimization to ensure our application is robust and fast.

---

## 7. Testing and Performance Optimization

Quality and performance are crucial for any application. In this final section, we discuss writing **unit tests and integration tests** for our application and techniques to improve performance such as **caching** and **pagination**.

### 7.1 Writing Unit and Integration Tests

**Unit Tests:** We want to test our Application layer logic in isolation:

- For command handlers, we can supply fake repository and unit-of-work implementations (or use in-memory DB with a real repository, depending on what we want to test).
- Use a testing framework like **xUnit** or **NUnit**. .NET typically uses xUnit by default in templates.
- We can create a test project `BlogApp.Tests` (or separate ones like BlogApp.UnitTests and BlogApp.IntegrationTests).

For example, to test `CreatePostCommandHandler`:

- We can create a fake repository that just collects added posts in memory (implementing `IPostRepository`).
- A fake unit-of-work that maybe just returns 1 on SaveChanges.
- Run the handler's Handle method with a sample command and assert that:
  - The returned Guid is not empty.
  - The fake repository now contains a post with the given title, etc.
  - Perhaps ensure that SaveChanges was called (could track via a flag in fake UoW).

Alternatively, we could use an in-memory EF Core database. EF Core has an `InMemoryDatabase` provider (Microsoft.EntityFrameworkCore.InMemory) which can be used for testing. Or use SQLite in-memory. That way, we use the real PostRepository and real DbContext but targeting an in-memory DB so no actual PostgreSQL needed. This tests more of the integration between repository and EF but might be considered an integration test.

**Integration Tests:** These tests ensure the whole system or large parts of it work together:

- We can spin up the Web API in memory using the **WebApplicationFactory** provided by Microsoft.AspNetCore.Mvc.Testing ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=and%20pages%2Fviews%20are%20found%20when,TestServer)).
- Then use an HttpClient to call the API endpoints, possibly with a test database or the in-memory database.

For integration testing with a real database, one approach is to use **Testcontainers** (a library to run a throwaway PostgreSQL container for tests) or just use the EF InMemory provider for a simpler approach.

Using **WebApplicationFactory** is powerful: it boots up the actual Startup (Program) of our API in a test server. We can override configurations (like use a test DB) by providing a custom WebApplicationFactory or using environment config.

The Microsoft documentation suggests referencing the Mvc.Testing package and perhaps separating integration test project to have access to internal classes if needed ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=,TestServer)) ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=,Microsoft.NET.Sdk.Web)).

Here's a simple example using WebApplicationFactory and InMemory EF for integration tests:

```csharp
public class PostsApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    public PostsApiTests(WebApplicationFactory<Program> factory)
    {
        // Create a factory that uses a different DB for testing
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Remove the real DbContext registration
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<BlogDbContext>));
                if (descriptor != null) services.Remove(descriptor);
                // Add in-memory database
                services.AddDbContext<BlogDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }

    [Fact]
    public async Task CreatePost_ReturnsCreated()
    {
        var newPost = new { title = "Test Post", content = "Hello", authorId = "user1" };
        var response = await _client.PostAsJsonAsync("/api/posts", newPost);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        // The Location header should contain the URI of new resource
        var location = response.Headers.Location;
        Assert.NotNull(location);

        // We can GET that location to verify the post exists
        var getResponse = await _client.GetAsync(location);
        Assert.Equal(HttpStatusCode.OK, getResponse.StatusCode);
        var postDto = await getResponse.Content.ReadFromJsonAsync<PostDto>();
        Assert.Equal("Test Post", postDto.Title);
    }
}
```

This uses xUnit (`[Fact]`) and the web factory. It switches the EF Core to InMemory for tests so we don't require an actual Postgres. Each test can run in isolation with a fresh DB (since we can give a unique DB name or ensure to clear it between tests).

Integration tests like above cover the full stack from controller to DB. They give confidence that the wiring (DI, routes, filters, etc.) is correct. But they're slower than unit tests, so we do a mix: unit tests for logic, integration for overall.

**Unit vs Integration separation:** It's wise to separate them (perhaps by project or at least by naming conventions) ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=Separate%20unit%20tests%20from%20integration,Separating%20the%20tests)), so you can run unit tests frequently and integration tests maybe in CI or when needed.

### 7.2 Performance Optimization: Caching

To ensure the blog API performs well under load, consider introducing caching for expensive or frequent read operations:

- **In-Memory Caching:** Using `IMemoryCache` to store results of queries that don't change often (e.g., list of posts or a post detail) can reduce load on the DB for repeated requests ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)). We might use it for something like `GetPostById` – after retrieving from DB once, store it in cache so subsequent requests (within a short time) return faster.

- **Distributed Caching:** If you have multiple API instances or want to persist cache beyond a single process restart, use a distributed cache (e.g., Redis or SQL Server distributed cache). But that adds complexity. In-memory is fine if one instance or sticky sessions in a web farm ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=the%20IMemoryCache%20.%20,requests%20to%20the%20same%20server)).

Let's consider a simple scenario: we cache posts list and post details. We can implement caching in the Query handlers or via a decorator. For example, a pipeline behavior that caches query responses based on the query parameters as key. Alternatively, inside `GetPostByIdQueryHandler`:

```csharp
public class GetPostByIdQueryHandler : IRequestHandler<GetPostByIdQuery, PostDto?>
{
    private readonly IPostRepository _postRepo;
    private readonly IMemoryCache _cache;
    // ... constructor

    public async Task<PostDto?> Handle(GetPostByIdQuery request, CancellationToken token)
    {
        string cacheKey = $"Post_{request.PostId}";
        if (_cache.TryGetValue(cacheKey, out PostDto? cachedPost))
        {
            return cachedPost;
        }
        var post = await _postRepo.GetByIdAsync(request.PostId, token);
        if (post == null) return null;
        var dto = _mapper.Map<PostDto>(post);
        // Set cache with appropriate expiration
        _cache.Set(cacheKey, dto, TimeSpan.FromMinutes(5));
        return dto;
    }
}
```

You would register IMemoryCache in DI (`builder.Services.AddMemoryCache();`). This method caches each post for 5 minutes. If a post is updated or deleted, you should invalidate the cache for that post (e.g., after an UpdatePostCommand or DeletePostCommand, remove the cache entry if exists).

Alternatively, one could rely on the fact that the post will eventually update after 5 min; for a blog that might be acceptable, or use shorter expiration.

For list of posts (which might change when new posts are added), you could also cache the result of `ListPostsQuery` (with keys maybe including page number).

Caching dramatically reduces DB hits for read-heavy scenarios: _"Caching can significantly improve performance by reducing the work required to generate content... caching works best with data that changes infrequently and is expensive to generate."_ ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)). Blog posts are typically read much more often than written, making them good candidates for caching.

**Note:** Always consider cache invalidation strategy. Using absolute expiration or sliding expiration is important so stale data doesn't live forever ([In-Memory Caching in ASP.NET Core for Better Performance](https://codewithmukesh.com/blog/in-memory-caching-in-aspnet-core/#:~:text=Performance%20codewithmukesh,longer%20than%20the%20sliding)). In our example, 5 minutes caching is a simple strategy.

### 7.3 Performance Optimization: Pagination and Query Tuning

**Pagination:** We briefly mentioned it – for endpoints returning lists (like list of posts or comments), do not return huge datasets in one go. Use `Skip`/`Take` (or in SQL terms OFFSET/FETCH) to implement pagination. We did that with `ListPostsQuery(page, pageSize)`.

Ensure that page size has an upper limit to prevent clients from asking for everything at once (e.g., max 100 per page). This protects the API and DB.

Example in repository (if we add such method):

```csharp
public async Task<List<Post>> GetPostsAsync(int page, int pageSize)
{
    return await _context.Posts
                  .OrderByDescending(p => p.CreatedAt)
                  .Skip((page - 1) * pageSize)
                  .Take(pageSize)
                  .ToListAsync();
}
```

Also consider if the client needs total count (for showing number of pages). You might provide an endpoint or include an extra field. EF can do `.CountAsync()` for total count, but doing that on every list request doubles the queries. You could cache the count or accept slightly out-of-sync counts.

**Query optimization:** With EF Core, be mindful of performance:

- Include only necessary related data. We used `.Include(p => p.Comments)` for GetById to get comments. That's fine if we need them. If comments are large or not always needed, make it optional or separate call.
- Use AsNoTracking for read-only queries to avoid tracking overhead if not needed (especially for queries that retrieve a lot of data and you won't modify it).
- Ensure proper indexing in database on commonly filtered columns (EF migrations can create indexes via Fluent API or `[Index]` attribute).
- Avoid N+1 query issues: e.g., if you had to load many posts and then their comments separately in a loop, better include or adjust queries to fetch in one go.

**Logging and Monitoring:** For performance, also set up logging of slow queries or use application performance monitoring to catch bottlenecks. But that’s beyond the code – more of an ops concern.

### 7.4 Additional Best Practices and Final Notes

- **Security:** Apart from auth, ensure to handle any sensitive data carefully. Use HTTPS (our container example didn't explicitly show it, but typically you'd run behind an HTTPS proxy or terminate TLS at a load balancer).
- **Middleware Order:** Ensure `UseAuthentication` is before `UseAuthorization`, and that `UseCors` (if needed) is correctly placed to allow front-end apps to call.
- **Data Protection:** If using Identity or something, configure data protection for consistent key rings in Docker, etc.
- **Scalability:** The app is built with scalability in mind (CQRS can scale read/write parts independently if needed, and the layering helps with maintainability). If needed in future, one could separate the reads to a separate service or use read replicas of the database.
- **Documentation:** Use Swagger (which we enabled) to document the API. That helps others integrate with your API.
- **CI Pipeline Enhancements:** In CI, one can also run integration tests (maybe using docker compose to bring up services and run tests against them). Our example was basic, but you can expand it.

This marks the end of our step-by-step guide. We started from a blank slate and went through setting up a Clean Architecture in .NET, implementing CQRS with MediatR, integrating EF Core with PostgreSQL (applying repository and UoW patterns) ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=match%20at%20L286%20Repository%20patterns,simulating%20access%20to%20the%20database)), building a rich Web API with proper layering and practices, securing it with JWT auth and role-based authorization ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)), containerizing the app with Docker, and setting up CI/CD. We also touched on testing and performance tuning, which are critical for a production-ready system.

By following this guide, an advanced developer should have a blueprint for constructing a robust, scalable blog (or similar) application in .NET Core. The principles and patterns used here can be applied to many other domains and projects, providing a clean separation of concerns and a maintainable codebase. Happy coding!

**Sources:**

1. Faris Karcic, _"A Developer's Guide to CQRS Using .NET Core and MediatR"_, _DZone/Slideshare_, Jun. 22, 2020 – Discusses combining Clean Architecture with CQRS for a scalable .NET project ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=entire%20solution,shaped%20by%20following%20the%20Domain)) ([A Developer's Guide to CQRS Using .NET Core and MediatR | PDF](https://www.slideshare.net/slideshow/a-developers-guide-to-cqrs-using-net-core-and-mediatr/250928602#:~:text=independently%20from%20outer%20layers%20and,specific%20purpose%20is%20to%20communicate)).

2. **Microsoft Documentation**, _"Repository and Unit of Work Patterns"_, by Tom Dykstra – Explains how these patterns abstract data access for testing and maintainability ([Implementing the Repository and Unit of Work Patterns in an ASP.NET MVC Application (9 of 10) | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application#:~:text=The%20repository%20and%20unit%20of,driven%20development%20%28TDD)) ([Implementing the Repository and Unit of Work Patterns in an ASP.NET MVC Application (9 of 10) | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application#:~:text=Later%20in%20the%20tutorial%20you%27ll,use%20these%20classes%20without%20interfaces)).

3. **Microsoft Docs**, _"Dependency injection in ASP.NET Core"_ – Confirms that ASP.NET Core's built-in DI container supports a variety of lifetimes and patterns for loose coupling ([Dependency injection in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-9.0#:~:text=ASP,between%20classes%20and%20their%20dependencies)).

4. Sarah Dutkiewicz, _"Using EFCore with Postgres"_, NimblePros Blog, Apr 14, 2023 – Guide on switching a Clean Architecture template to use Npgsql, with details on adding the provider and connection strings ([Using EFCore with Postgres | NimblePros Blog](https://blog.nimblepros.com/blogs/using-ef-core-with-postgres/#:~:text=As%20the%20Clean%20Architecture%20template,PostgreSQL)) ([Using EFCore with Postgres | NimblePros Blog](https://blog.nimblepros.com/blogs/using-ef-core-with-postgres/#:~:text=services.AddDbContext)).

5. **Microsoft Docs**, _".NET Microservices: Infrastructure Persistence Layer Implementation"_ – Notes that EF Core is based on Unit of Work and Repository patterns, and custom repositories add an abstraction mainly for testing and domain purity ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=Using%20a%20custom%20repository%20versus,using%20EF%20DbContext%20directly)) ([Implementing the infrastructure persistence layer with Entity Framework Core - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-implementation-entity-framework-core#:~:text=match%20at%20L286%20Repository%20patterns,simulating%20access%20to%20the%20database)).

6. DevLeader, _"C# Clean Architecture with MediatR: Build for Flexibility"_, Feb 6, 2024 – Describes how MediatR implements the Mediator pattern to decouple components in Clean Architecture ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=MediatR%20is%20a%20,an%20elegant%20and%20maintainable%20manner)) and provides examples of commands vs. queries usage ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=Commands%20in%20MediatR%20represent%20operations,without%20causing%20any%20side%20effects)) ([C# Clean Architecture with MediatR: How To Build For Flexibility](https://www.devleader.ca/2024/02/06/c-clean-architecture-with-mediatr-how-to-build-for-flexibility/#:~:text=%2F%2F%20Command%20public%20class%20UpdateOrderCommand,)).

7. **Microsoft Docs**, _"Configure JWT Bearer Authentication in ASP.NET Core"_ – Explains JWT basics and how the JwtBearer handler validates tokens and uses claims for authz ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=JWT%20,header%20and%20a%20bearer%20token)) ([Configure JWT bearer authentication in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0#:~:text=,is%20known%20as%20delegated%20authorization)).

8. **Microsoft Docs**, _"Role-based authorization in ASP.NET Core"_ – Shows usage of [Authorize] with roles to restrict access in controllers ([Role-based authorization in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles?view=aspnetcore-9.0#:~:text=%5BAuthorize%28Roles%20%3D%20,)).

9. **Microsoft Docs**, _"Integration tests in ASP.NET Core"_ – Recommends using WebApplicationFactory and separating integration tests, also covers Microsoft.AspNetCore.Mvc.Testing benefits ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=and%20pages%2Fviews%20are%20found%20when,TestServer)) ([Integration tests in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-9.0#:~:text=,Microsoft.NET.Sdk.Web)).

10. **Microsoft Docs**, _"Cache in-memory in ASP.NET Core"_ – Highlights performance gains from caching and the basic usage of IMemoryCache ([Cache in-memory in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory?view=aspnetcore-9.0#:~:text=Caching%20can%20significantly%20improve%20the,never%20depend%20on%20cached%20data)).
