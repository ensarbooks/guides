# Secure .NET Core Development: A Comprehensive Guide

## Introduction

Building a modern web application requires not only functionality and performance but also **robust security**. This guide provides a step-by-step journey through developing a secure .NET Core application that is free of OWASP Top 10 vulnerabilities. Targeted at **advanced developers**, it covers best practices, coding guidelines, real-world case studies, and practical examples using .NET 6 and later. We will delve into topics such as secure authentication with OAuth2 and JWT, protecting APIs with rate limiting and CORS, preventing common attacks like SQL Injection, XSS, and CSRF, and leveraging security tools and testing methodologies to harden your application.

### Who Should Read This Guide

This guide is intended for experienced .NET developers, security engineers, and software architects who want to deepen their understanding of application security. It assumes familiarity with C# and ASP.NET Core fundamentals and focuses on **advanced security practices** and **secure coding techniques**.

### How to Use This Guide

The guide is structured like a book with clear chapters and an appendix:

- **Chapter 1:** Overview of OWASP Top 10 and how each risk pertains to .NET Core web apps.
- **Chapter 2:** Secure coding best practices and guidelines to avoid vulnerabilities.
- **Chapter 3:** Authentication and Authorization in depth (IdentityServer, JWT, OAuth2).
- **Chapter 4:** Securing APIs and microservices (rate limiting, CORS, secure headers).
- **Chapter 5:** Mitigation techniques for common vulnerabilities (SQL Injection, XSS, CSRF, etc.).
- **Chapter 6:** Handling sensitive data securely (encryption, hashing, secrets management).
- **Chapter 7:** Using security tools (SonarQube, OWASP ZAP, dependency scanning) in the SDLC.
- **Chapter 8:** Penetration testing strategies and automated security testing.
- **Chapter 9:** Real-world case studies of security failures and how to prevent them.
- **Chapter 10:** Conclusion – putting it all together in a secure development lifecycle.
- **Appendices:** Additional resources, checklists, and exercise solutions.

Each chapter includes **code samples**, practical examples, and **exercises** to reinforce learning. You are encouraged to try the exercises and refer to the appendices for solutions and additional references. Remember, security is a journey – use this guide as a reference and continually stay updated on emerging threats and best practices.

Let’s begin by understanding the foundation: the OWASP Top 10 vulnerabilities that plague web applications and how they specifically relate to ASP.NET Core.

## Chapter 1: Understanding the OWASP Top 10 in .NET Core

Security in web applications is often framed around common vulnerability categories. The **OWASP Top 10** is a renowned list that highlights the most critical web application security risks. In this chapter, we’ll overview each OWASP Top 10 category and discuss how .NET Core applications can be affected. This sets the stage for later chapters where we implement defenses against these risks.

### 1.1 What is the OWASP Top 10?

The OWASP (Open Web Application Security Project) Top 10 is a list of the ten most critical security risks to web applications. It is updated periodically (most recently in 2021) based on data about vulnerability prevalence and severity. The categories as of 2021 are:

1. **Broken Access Control** – Restrictions on what authenticated users are allowed to do are not properly enforced. Attackers can exploit flaws to access unauthorized functionality or data.
2. **Cryptographic Failures** – Sensitive data is not properly protected (e.g., passwords or credit card numbers not encrypted, weak encryption in use).
3. **Injection** – Untrusted data is sent to an interpreter as part of a command or query (SQL, OS commands, etc.), tricking the interpreter into executing unintended commands or accessing data without authorization.
4. **Insecure Design** – Flaws in design (at architecture or code level) that lead to security weaknesses (this is a broad category encouraging use of threat modeling and secure design patterns).
5. **Security Misconfiguration** – Security settings not defined or implemented correctly, such as leaving default configs, verbose error messages, or open cloud storage.
6. **Vulnerable and Outdated Components** – Using libraries, frameworks, or other software with known vulnerabilities can lead to compromise.
7. **Identification and Authentication Failures** – Weaknesses in authentication or session management (formerly “Broken Authentication”), such as improper handling of credentials, session IDs, or not using MFA.
8. **Software and Data Integrity Failures** – Assumptions related to software updates, critical data, and CI/CD pipelines not verified (e.g., not verifying integrity of plugins, using vulnerable deserialization).
9. **Security Logging and Monitoring Failures** – Absence of logging or monitoring, missing detection of breaches. This makes incident detection and response difficult.
10. **Server-Side Request Forgery (SSRF)** – The application can be tricked into making unintended requests to an internal or external resource, often leading to access of internal services.

> **Note:** Previous OWASP Top 10 versions (2017 and earlier) included categories like Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) explicitly. In the latest list, XSS is considered a subset of **Injection** (specifically, script injection), and CSRF is less prevalent due to frameworks having built-in protections ([why CSRF is removed from OWASP top 10, how to prevent CSRF on ...](https://stackoverflow.com/questions/48373904/why-csrf-is-removed-from-owasp-top-10-how-to-prevent-csrf-on-asp-net-mvc#:~:text=why%20CSRF%20is%20removed%20from,and%20some%20form%20of%20protections)) ([why CSRF is removed from OWASP top 10, how to prevent CSRF on ...](https://stackoverflow.com/questions/48373904/why-csrf-is-removed-from-owasp-top-10-how-to-prevent-csrf-on-asp-net-mvc#:~:text=,and%20some%20form%20of%20protections)). Nonetheless, we will cover XSS and CSRF thoroughly, as they remain important threats, especially if default protections are disabled or misconfigured.

### 1.2 OWASP Top 10 and ASP.NET Core

ASP.NET Core, by design, incorporates several security features to mitigate common vulnerabilities. For example, Razor pages automatically encode output to mitigate XSS, and the framework has built-in CSRF protection for form posts. However, secure defaults only go so far. Let’s briefly discuss each OWASP Top 10 risk in the context of a .NET Core application:

- **Broken Access Control:** In ASP.NET Core, this could occur if you forget to apply `[Authorize]` on sensitive endpoints or if you rely solely on client-side checks. It might also occur through insecure direct object references (IDORs)—for instance, if your application exposes an `/api/users/{userid}` endpoint and does not verify that the current logged-in user is allowed to access the requested `{userid}`. We’ll see later how to use policy-based authorization and proper checks to prevent this.

- **Cryptographic Failures:** .NET provides strong cryptographic APIs, but misuse is possible. Examples include storing passwords in plaintext or with a weak hash, using outdated algorithms (e.g., SHA1) for hashing, or not enforcing HTTPS. Even **hardcoding encryption keys** in code is a failure that can lead to sensitive data exposure. We will cover how to use robust cryptography (like AES encryption for data, and PBKDF2 for password hashing) in Chapter 6.

- **Injection:** A classic example is SQL Injection. If a .NET Core app uses string concatenation to build SQL queries (for instance, constructing a WHERE clause with user input), an attacker can inject SQL commands. Another injection vector is ORM misuse (though ORMs like Entity Framework reduce SQLi risk, improper use of `FromSqlRaw` or Dapper without parameters can still be dangerous). ASP.NET Core is also susceptible to other injections like LDAP injection or OS command injection if the app passes user input to system commands. We will demonstrate how using **parameterized queries** and ORMs can eliminate SQL injection risks ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Using%20Parametrized%20Queries)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=The%20query%20in%20our%20previous,would%20be%20written%20like%20this)), and how to validate inputs to prevent injection generally.

- **Insecure Design:** This is a broader concept. In .NET Core, insecure design might manifest as choosing to roll your own cryptography or authentication scheme without thoroughly understanding the pitfalls, or not designing for least privilege. For example, designing an app that requires running as an OS administrator or DB admin when it really only needs read/write on one database is insecure design. We will stress principles like _principle of least privilege_ throughout the guide to address this ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Remediation%3A%20The%20Principle%20of%20Least,Privilege)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=In%20the%20case%20of%20databases%2C,SQL%20code%20generated%20was%20this)).

- **Security Misconfiguration:** This can include leaving the app in **Development mode** on a production server (which might display detailed error pages and stack traces), not configuring HTTPS redirection or HSTS, using default application secrets or identity seeds, or failing to set the appropriate headers. .NET Core applications should be deployed with production settings (e.g., `ASPNETCORE_ENVIRONMENT=Production` which enables error handling middleware to hide errors, and can enable HSTS by default). We’ll learn how to properly configure the application (for example, using `app.UseHsts()` and tightening middleware settings) in Chapter 4 and Chapter 5.

- **Vulnerable and Outdated Components:** Using an outdated version of .NET or vulnerable NuGet packages can introduce risks. For instance, a vulnerability in a JSON library or a dependency injection container could be exploited if not patched. .NET developers must keep up with updates and use tools to scan for known vulnerabilities in dependencies. We will discuss dependency scanning tools (like OWASP Dependency Check and others) in Chapter 7. Regularly updating NuGet packages to patched versions is a simple yet critical practice ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=6)).

- **Identification and Authentication Failures:** ASP.NET Core’s identity system provides a robust framework for managing users and passwords, but developers might weaken it through misconfigurations. Examples include not enforcing a strong password policy, not hashing passwords properly (if using a custom auth scheme), or exposing authentication tokens in URLs. Another example is poor session management – e.g., not invalidating JWT tokens on password change or not using secure cookie flags for cookie-based auth. In Chapter 3, we’ll see how to implement secure authentication using IdentityServer and JWT, and how to configure things like account lockout and password hashing (the ASP.NET Core Identity uses PBKDF2 by default for hashing passwords with a salt and multiple iterations, which is good ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=On%20the%20other%20hand%2C%20several,hashing%20algorithms%20are%20safe))).

- **Software and Data Integrity Failures:** In .NET, one example could be not verifying the integrity of plugins or NuGet packages loaded at runtime. Another could be using the old BinaryFormatter to deserialize data from untrusted sources – this is a known risky practice as it can lead to remote code execution (which is why .NET 5+ has it obsolete and recommends not using it). We’ll address this by recommending safe alternatives (like System.Text.Json for known types, or better yet, avoid accepting serialized blobs from untrusted sources altogether). Also, protecting the integrity of CI/CD is important – e.g., ensure only trusted pipelines can deploy code, to prevent tampering.

- **Security Logging and Monitoring Failures:** Developers might not implement logging for security events (like login failures, odd input patterns) or might ignore setting up alerts. ASP.NET Core has logging frameworks (e.g., built-in logging, Serilog, etc.) that can be leveraged to record suspicious activities. Additionally, integrating with Application Performance Monitoring (APM) services or SIEMs can help detect attacks. We will cover in Chapter 8 how to plan monitoring and what to log (without logging sensitive data) to catch issues. Lack of monitoring was added to OWASP Top 10 because it’s seen that breaches often go unnoticed for weeks or months due to insufficient monitoring ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=Panera%20was%20alerted%20about%20the,was%20fixing%20the%20problem%20then)) ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=For%20example%2C%20some%20of%20the,points%2C%20including%20by%20phone%20number)) (as seen in some case studies).

- **Server-Side Request Forgery (SSRF):** While not as commonly discussed as XSS or SQLi, SSRF is relevant, particularly if your .NET application fetches data from other URLs (e.g., making HTTP requests based on user input). An insecure example is a feature that takes a URL from a user and downloads its content – an attacker could supply `http://localhost/admin` or an internal AWS metadata URL and trick the server into requesting internal services. We’ll learn how to mitigate SSRF by whitelisting domains, or using network controls. A famous case involving SSRF was the Capital One breach, where an SSRF vulnerability in an app behind a firewall allowed an attacker to access the AWS EC2 instance metadata and obtain credentials ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=The%20attacker%20gained%20access%20to,the%20data%20contained%20in%20them)).

This overview is just a teaser. In the following chapters, we will tackle each of these areas with concrete examples and solutions. For each vulnerability, we will demonstrate how to **identify, exploit (in a safe test scenario), and then fix or prevent** it in a .NET Core context.

**Exercise 1:** _Identify OWASP Categories_ – To ensure you understand the OWASP Top 10, consider a few scenarios and identify which OWASP category they belong to and why. For example:  
 a. A developer concatenates user input into a SQL query string and executes it.  
 b. An admin page is not protected by authentication, allowing anyone to access it if they know the URL.  
 c. The application uses an outdated version of a JWT library with a known vulnerability.  
 d. User passwords are stored in the database in plaintext.

_Write down your answers (the OWASP category for each scenario) and we’ll discuss them in the appendix._ (This exercise will help reinforce mapping real issues to the OWASP categories.)

---

## Chapter 2: Secure Coding Best Practices in .NET Core

Writing secure code is the frontline of defense against vulnerabilities. In this chapter, we compile a set of **best practices and secure coding guidelines** tailored for .NET Core applications. These are general recommendations that, when followed, significantly reduce the chances of introducing OWASP Top 10 vulnerabilities (and other security issues) into your application.

### 2.1 Validate All Inputs

**Never trust user input.** This is a cardinal rule. All external input – whether from users, APIs, or files – should be considered malicious until proven otherwise. .NET Core provides several mechanisms for input validation:

- **Model Validation:** Use data annotations (like `[Required]`, `[StringLength]`, `[Range]`, regular expression patterns, etc.) on your model properties. ASP.NET Core will automatically validate request data (for example, JSON in an API or form fields in MVC) against these annotations and provide validation errors. This prevents improper data from even reaching your business logic. Always check `ModelState.IsValid` in MVC controllers for form inputs.

- **Manual Validation:** For complex cases, manually validate and reject/fix bad input. For instance, if expecting an integer, try `int.TryParse()` and handle failure. If expecting one of a few known string values (e.g., a status like “low/medium/high”), ensure the input matches one of the allowed values (use an _allowlist_ of acceptable inputs) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Using%20Allowlists)).

  - Example:
    ```csharp
    string severity = userInput;
    var allowed = new[] { "Low", "Medium", "High", "Critical" };
    if (!allowed.Contains(severity))
    {
        return BadRequest("Invalid severity level.");
    }
    ```
    Using an allowlist (whitelist) ensures only expected values get through ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Using%20Allowlists)).

- **Length and Range Checking:** Always impose length limits on input fields (both client-side and server-side) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=9)) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=public%20IActionResult%20SubmitForm%28string%20input%29%20,%2F%2F%20Process%20input)). For example, if a username should be max 50 chars, enforce that. This not only prevents certain buffer overflow or performance issues but also is good for validation. Example:

  ```csharp
  if (input.Length > 100)
  {
      return BadRequest("Input is too long.");
  }
  ```

  Similarly, if expecting a numeric range (say 1-100), enforce that range.

- **Encoding and Character Checks:** If certain characters are not expected (e.g., no HTML should be in a name field), you can either reject input containing dangerous characters (`<`, `>` for HTML for example) or sanitize them (encode to safe equivalents). ASP.NET Core’s Razor will encode output, but if you’re processing input that shouldn’t contain certain content at all (like script tags), you might validate that upfront. For example:
  ```csharp
  if (userComment.Contains("<script", StringComparison.OrdinalIgnoreCase))
  {
      // Potential XSS attempt or unwanted input
      return BadRequest("Invalid input.");
  }
  ```
  However, generally, it’s better to _encode on output_ rather than blacklist inputs, because input filtering can be bypassed. We’ll discuss output encoding in the XSS section.

**Key Point:** Strong input validation helps prevent many attacks by stopping malicious data at the gate. For instance, proper validation (type checking, length checking) can mitigate SQL injection and XSS before we even get to specialized defenses ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Often%2C%20the%20methods%20in%20your,not%20an%20integer%20to%20fail)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=The%20good%20news%20is%20that,aren%27t%20assembled%20by%20string%20manipulation)).

### 2.2 Use Parameterized Queries and ORMs

A crucial best practice to prevent SQL Injection is: **never concatenate user input into SQL queries.** Instead, use parameterized queries or an ORM (Object-Relational Mapper):

- **Parameterized Queries:** If using `SqlCommand` or ADO.NET directly, always use parameters:

  ```csharp
  string unsafeUserInput = "O'Hara";
  string query = "SELECT * FROM Customers WHERE LastName = @lastName";
  using var cmd = new SqlCommand(query, connection);
  cmd.Parameters.AddWithValue("@lastName", unsafeUserInput);
  ```

  In this example, even if `unsafeUserInput` contains SQL special characters or malicious content, it will not break the query; the value is safely bound to the parameter, and the database treats it as data, not SQL code ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Parametrized%20queries%20avoid%20SQL%20injection,of%20the%20SQL%20query%20itself)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=After%20creating%20a%20new%20SqlCommand%2C,parameter%20using%20the%20AddWithValue%20method)). Parameterized queries ensure that user inputs do **not** alter the query structure.

- **ORMs (Entity Framework Core, Dapper, etc.):** High-level data access frameworks by default parameterize queries for you. For instance, with Entity Framework Core:

  ```csharp
  var customer = dbContext.Customers
                  .Where(c => c.LastName == unsafeUserInput)
                  .ToList();
  ```

  Internally, EF will translate that LINQ expression into a parameterized SQL query. This greatly reduces risk of injection. Be cautious with raw SQL methods in ORMs (like `FromSqlRaw` in EF Core); if you must use them, still supply parameters via interpolation that EF will parameterize (e.g., `FromSqlInterpolated`). Using an ORM not only improves productivity but also **decreases SQL injection risk** because queries aren't constructed via string manipulation in most cases ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=The%20good%20news%20is%20that,aren%27t%20assembled%20by%20string%20manipulation)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=means%20raw%20input%20values%20are,aren%27t%20assembled%20by%20string%20manipulation)).

- **No Dynamic SQL if possible:** Avoid scenarios where you construct dynamic SQL snippets (like building a WHERE clause dynamically from user input). If dynamic logic is needed (e.g., user can filter by multiple optional fields), use safe techniques (multiple parameters, or ORMs that handle expression trees). If absolutely needed, ensure any identifiers used (like column names) are from trusted sources or a fixed mapping (never directly from user input).

By following the above, you effectively mitigate injection attacks. Recall the earlier example: a vulnerable code concatenating input into a query could allow an attacker to append something like `'; DROP TABLE Users;--` to delete data ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=%60var%20query%20%3D%20,ORDER%20BY%20Published%20DESC)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=The%20string%20concatenation%20would%20result,in%20the%20following%20query)). Parameterization stops that entirely.

_(We will delve deeper into SQL Injection prevention in Chapter 5, including an example of exploiting a vulnerable query and then fixing it. But as a guiding principle: parameterize everything.)_

### 2.3 Avoid Hardcoding Secrets and Use Secure Storage

Hardcoding sensitive information in code is a serious mistake. This includes **passwords, API keys, connection strings, encryption keys**, etc. Best practices:

- **Configuration Files & User-Secrets:** Use appsettings.json or secrets management. For development, .NET Core has the [Secret Manager](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) tool to keep secrets out of code (stored in a user profile vault). For production, prefer environment variables or secure stores.

- **Environment Variables or Vaults:** Load secrets from the environment or a vault like **Azure Key Vault** or **AWS Secrets Manager**. .NET Core configuration can seamlessly pull from these sources. Example:

  ```csharp
  var builder = WebApplication.CreateBuilder(args);
  builder.Configuration.AddEnvironmentVariables();
  string dbConn = builder.Configuration["ConnectionStrings:DefaultConnection"];
  ```

  This way, the actual connection string can be set in the environment (or injected via CI/CD) rather than in code or appsettings.

- **Never commit secrets to source control:** This is more of a process guideline, but tools like **GitGuardian** or secret scanning should be used to ensure no secrets slip in commits.

- **Rotate Secrets:** If a secret (like a DB password) does leak, have a process to rotate it (change it) quickly. Use different secrets for dev, test, prod – don’t reuse them.

Avoiding hardcoded secrets means even if someone gets your source code, they don’t automatically get the keys to your production kingdom.

### 2.4 Use Strong Authentication and Authorization Practices

Authentication (identifying users) and authorization (controlling access) must be implemented carefully:

- **Use Proven Frameworks:** Don’t write your own authentication mechanism if you can use ASP.NET Core Identity or IdentityServer. They provide features like secure password storage (ASP.NET Core Identity uses salted PBKDF2 by default), account lockout, 2FA, etc. Rolling your own login system is error-prone.

- **Enforce MFA:** For sensitive applications, use Multi-Factor Authentication. If using IdentityServer4 or Azure AD, you can integrate MFA. At minimum, encourage users to use MFA if available.

- **Password Policies:** Enforce strong passwords (min length, complexity or passphrase), and use password attempt lockouts to prevent brute force. Also consider using password breach checks (e.g., haveibeenpwned API) to reject known compromised passwords.

- **Secure Session Management:** If using cookies for sessions, always set cookies with `HttpOnly` and `Secure` flags:

  - HttpOnly prevents JavaScript from accessing the cookie (mitigating some XSS impact) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Cookie%20No%20HttpOnly%20Flag)) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Reference%3A%20http%3A%2F%2Fwww)).
  - Secure ensures the cookie is only sent over HTTPS.
  - In ASP.NET Core, if you use the default cookie authentication, configure it like:
    ```csharp
    services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
            .AddCookie(options => {
                options.Cookie.HttpOnly = true;
                options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                options.Cookie.SameSite = SameSiteMode.Lax;
            });
    ```
    The above forces HttpOnly and Secure on cookies (SameSite is another important flag – we’ll discuss it in CSRF mitigation, but Lax or Strict helps mitigate CSRF by not sending cookies on cross-site requests).

- **Use JWTs carefully:** JSON Web Tokens are common for SPAs and mobile backends. Use strong signing keys (256-bit symmetric keys or RSA/ECDSA for asymmetric). Validate tokens on every request:

  ```csharp
  services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
          .AddJwtBearer(options => {
              options.TokenValidationParameters = new TokenValidationParameters {
                  ValidateIssuer = true,
                  ValidateAudience = true,
                  ValidIssuer = "https://yourdomain.com",
                  ValidAudience = "your-api",
                  ValidateIssuerSigningKey = true,
                  IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(Configuration["JwtSecretKey"])),
                  ClockSkew = TimeSpan.Zero // no tolerance on expiry
              };
          });
  ```

  The above ensures the JWT’s issuer and audience are what we expect and that the signature is valid (with our secret key). **Never disable signature validation or token expiration** – that would create a huge hole.

- **Principle of Least Privilege:** When designing authorization, give users the minimal access they need. Use role-based or policy-based authorization to restrict sensitive functionality. For example, an “Admin” role might have access to user management endpoints, while regular users do not:

  ```csharp
  [Authorize(Roles = "Admin")]
  public IActionResult GetAllUsers() { ... }
  ```

  If using claims, create policies:

  ```csharp
  services.AddAuthorization(options => {
      options.AddPolicy("CanDeleteOrder", policy => policy.RequireClaim("Department", "Sales"));
  });
  ```

  Then decorate actions with `[Authorize(Policy = "CanDeleteOrder")]`. This ensures even authenticated users must meet specific conditions to access that resource.

- **Avoid Identity & Access Control Pitfalls:** Common mistakes include: not logging out users properly, not invalidating JWTs when critical permissions change, exposing user IDs or tokens in URLs, etc. Also, implement **account lockout** on multiple failed login attempts to slow down brute force (ASP.NET Core Identity does this out-of-the-box).

We will cover a full implementation of authentication and authorization in Chapter 3, using IdentityServer4 (for OAuth2/OpenID Connect), JWTs, and ASP.NET Core Identity. There, you’ll see code samples for setting up an IdentityServer and protecting APIs.

### 2.5 Secure Error Handling and Logging

Error messages can inadvertently leak information that helps attackers:

- **Don’t reveal sensitive info in errors:** Stack traces or detailed error messages should never be shown to end-users. In .NET Core, ensure you run in Production mode (which by default shows a generic error page instead of the detailed developer exception page). For APIs, handle exceptions and return a generic message like “An error occurred” with maybe a correlation ID, but **do not return** the exception details. For example:

  ```csharp
  try {
      // some code
  }
  catch(Exception ex) {
      _logger.LogError(ex, "Unhandled exception processing request.");
      return StatusCode(500, "Internal Server Error");
  }
  ```

  In the above, we log the detailed exception internally, but the response to the client is generic ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=7)) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=catch%20%28Exception%20ex%29%20,)).

- **Remove or protect diagnostic pages:** Disable the Developer Exception Page on production. Also, secure any debugging endpoints (like if you had a health check or diagnostics endpoint, ensure they don’t divulge config values or stack traces to unauthenticated users).

- **Custom Error Handling Middleware:** It’s good to have a global exception handling middleware (or use `app.UseExceptionHandler(...)`) to catch any unhandled exceptions and return a safe response.

- **Logging:** Log important security events – log authentication attempts (success and failure), access denied events, input validation failures (could indicate someone trying to attack), etc. But **avoid logging sensitive data** (like full credit card numbers or passwords). Redact or hash them if needed. For example, don’t log user passwords ever (even if hashed, there’s no need to log). If you log JWTs or headers for debugging, be cautious as they might contain sensitive info.

- **Monitor logs:** Logging is only useful if someone reviews them. Use log monitoring tools or set up alerts for suspicious patterns (e.g., 50 failed login attempts in a short time, which could indicate a brute force attack).

Effective error handling thwarts attackers’ attempts to gather info (they often rely on error messages to learn about the system), and good logging practices ensure that if an incident occurs, you have data to understand and respond to it ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=SonarQube%20SonarQube%20is%20an%20automatic,Image%204)) ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=Add%20a%20new%20Sonar%20Service,in%20the%20SonarQube%20quality%20profiles)).

### 2.6 Secure Coding Checklist (Summary)

As a quick reference, here are **10 top secure coding practices** you should always keep in mind (many of which we discussed):

1. **Input Validation** – Validate _type, length, format, and range_ of all inputs. Reject or sanitize bad inputs ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=1)) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=9)).
2. **Parameterized Queries** – Use parameterized queries or ORMs for database access; never concatenate SQL commands ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=2)).
3. **No Hardcoded Secrets** – Keep secrets out of code; use configuration or vaults ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=3)).
4. **Encrypt Sensitive Data** – Encrypt confidential data at rest (in databases or files) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=4)), and use hashing + salting for passwords.
5. **Strong Authentication & AuthZ** – Use established frameworks, enforce least privilege, and protect session tokens ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=5,Authorization)).
6. **Keep Dependencies Updated** – Regularly update NuGet packages and .NET runtime to patch vulnerabilities ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=match%20at%20L176%206,Update%20Dependencies)).
7. **Proper Error Handling** – Don’t expose internal errors to users; log exceptions securely and handle them gracefully ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=7)).
8. **Use HTTPS Everywhere** – Enable TLS for all traffic to prevent snooping/tampering ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=match%20at%20L207%208,HTTPS)). Also use HSTS to enforce HTTPS.
9. **Limit Exposure** – Only expose the minimum necessary information in APIs (e.g., don’t return verbose data if not needed) and limit debug information. Also, limit input data size as an abuse prevention (to prevent gigantic payload attacks) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=match%20at%20L217%209,User%20Input%20Length)).
10. **Least Privilege** – Not just for users, but for the app’s own access. For example, the database account used by the app should have the minimum rights (e.g., it might not need to `DROP` tables, so don’t grant that) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=A%20great%20security%20practice%E2%80%94not%20only,your%20app%2C%20and%20nothing%20more)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=logins%20that%20can%20only%20do,SQL%20code%20generated%20was%20this)). Similarly, if running in a container or VM, give the app least OS permissions.

Following this checklist will address many of the common issues. Think of it as hygiene for your code – much like unit testing, security checks should be part of your development routine.

**Exercise 2:** _Secure Code Review_ – Take a simple insecure snippet of code and identify what's wrong and how to fix it. For example:

```csharp
public IActionResult Login(string username, string password) {
    // Insecure example for exercise
    var user = db.Users.SingleOrDefault(u => u.Username == username && u.Password == password);
    if(user != null) {
        HttpContext.Session.SetString("User", username);
        return Redirect("/AdminDashboard");
    }
    else {
        return Content("Invalid login");
    }
}
```

Identify at least three security problems in the above code (hint: think about how passwords are handled, session management, and any missing protections) and propose solutions or improvements. Write down your answers – we will discuss them in the appendix.

---

## Chapter 3: Authentication and Authorization in ASP.NET Core (IdentityServer, JWT, OAuth2)

Authentication and authorization are the gates that protect functionality and data in your application. In .NET Core, you have a rich set of tools to implement these features securely. This chapter focuses on implementing **robust authentication and authorization**, using modern standards like **OAuth2 and OpenID Connect** with **JWT (JSON Web Tokens)**, and leveraging frameworks such as **IdentityServer**. We’ll also cover how to integrate these tokens into your ASP.NET Core app and enforce authorization rules.

### 3.1 Authentication vs Authorization – A Primer

- **Authentication** is the process of verifying who a user is (login). In web apps, this often means verifying credentials (username/password, or external login like Google) and establishing an identity (issuing a token or cookie).
- **Authorization** is the process of verifying what an authenticated user is allowed to do. This is typically role/permission checks before allowing access to certain API endpoints or UI pages.

Modern architectures often separate these concerns. For example, you might have an **Identity Provider** (IDP) that handles authentication (e.g., IdentityServer or an OAuth provider), and your main application or API just handles authorization using tokens issued by that IDP.

### 3.2 Implementing OAuth2 and OpenID Connect with IdentityServer

**OAuth2** is an authorization framework that allows a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner (user) or by allowing the third-party app to obtain its own access token. **OpenID Connect (OIDC)** is an identity layer on top of OAuth2 that handles authentication (login) and user info. In simple terms: OAuth2 alone is about delegated authorization (e.g., “Service A can act on behalf of user on Service B”), while OpenID Connect adds _who the user is_.

**IdentityServer4/Duende IdentityServer** is a popular .NET library that implements OAuth2/OIDC. It acts as an Authorization Server. We can use IdentityServer to issue JWT tokens for our users after they login.

**Why use IdentityServer (or similar)?** It saves you from writing token issuance and validation logic from scratch and ensures compliance with standards.

#### 3.2.1 Setting up IdentityServer

Suppose we want to build a secure token service for our application. We’d install IdentityServer (for .NET 6+, Duende IdentityServer is the successor of the open-source IdentityServer4, but conceptually similar). In `Startup.cs` or the equivalent in .NET 6 minimal:

```csharp
services.AddIdentityServer()
    .AddInMemoryIdentityResources(Config.IdentityResources)
    .AddInMemoryApiScopes(Config.ApiScopes)
    .AddInMemoryClients(Config.Clients)
    .AddInMemoryApiResources(Config.ApiResources)
    .AddDeveloperSigningCredential(); // use a temporary signing key for dev
```

Here, we configure IdentityServer with in-memory stores for simplicity (in production, you might use a database or configuration files). We define:

- **IdentityResources**: standard OpenID Connect identity scopes like profile, email, etc.
- **ApiScopes**: define scopes (permissions) for APIs (e.g., `api.read`, `api.write`).
- **Clients**: define who can request tokens (could be our own web app, a SPA, mobile app, etc.), with their allowed flows and secrets.
- **ApiResources**: (optional in latest versions) group related scopes or APIs.

For example, in `Config.Clients` (often a static class):

```csharp
new Client {
    ClientId = "webclient",
    ClientSecrets = { new Secret("SuperSecretPassword".Sha256()) },
    AllowedGrantTypes = GrantTypes.Code, // Use Authorization Code flow (for web apps with front-channel)
    RedirectUris = { "https://myapp.com/signin-oidc" },
    PostLogoutRedirectUris = { "https://myapp.com/signout-callback-oidc" },
    AllowedScopes = { "openid", "profile", "api.read" }
}
```

This defines a client that will use the OAuth2 Authorization Code flow with OIDC (so it will get an identity token and access token). It can request the `openid` and `profile` scopes (for user identity) and `api.read` scope for our API.

We also define users (for testing, IdentityServer allows in-memory test users, but usually you'd connect to ASP.NET Core Identity or another user store). For brevity:

```csharp
.AddTestUsers(new List<TestUser> {
    new TestUser { SubjectId = "1", Username = "alice", Password = "P@ssw0rd" }
});
```

Finally, in the HTTP pipeline:

```csharp
app.UseIdentityServer();
```

This starts the IdentityServer middleware that will expose endpoints like:

- `/.well-known/openid-configuration` (metadata)
- `/connect/authorize` (for interactive user logins/consent – the start of Auth Code flow)
- `/connect/token` (for exchanging credentials or auth code for tokens)
- `/connect/userinfo` (to get user profile info if logged in)
- `/connect/endsession` (logout), etc.

We have essentially stood up an **Authorization Server**. Running the application now would allow clients to perform OAuth2 flows to get tokens. For example, a user would hit the authorize endpoint, login (via the test user or whatever user store), and IdentityServer would issue an **ID Token** (for authentication info) and/or **Access Token** (for API calls).

> IdentityServer uses a signing certificate to sign tokens. In dev we used `AddDeveloperSigningCredential()`, which generates a temporary key. In production, you’d use a persisted key or an X.509 certificate ([IdentityServer4 Integration with ASP.NET Core - Code Maze](https://code-maze.com/identityserver4-integration-aspnetcore/#:~:text=,in%20a%20production%20environment%3B)) so that tokens remain valid across deployments and are signed securely.

#### 3.2.2 Understanding OAuth2 Flows for .NET Apps

Depending on your application type, you choose an OAuth2 flow:

- **Authorization Code Flow (with PKCE for public clients):** Recommended for web applications (server-side) and SPAs. The client gets an auth code via the browser (after user login at IDP) and then exchanges it for tokens via a back-channel. This keeps the tokens off the URL. IdentityServer supports this flow.
- **Client Credentials Flow:** Used for service-to-service (no user). For example, a microservice authenticating to another microservice. IdentityServer can allow a client to directly get a token with only its own credentials (no user involved) ([IdentityServer4 Integration with ASP.NET Core - Code Maze](https://code-maze.com/identityserver4-integration-aspnetcore/#:~:text=So%2C%20we%20provide%20the%20,allowed%20scopes%20for%20the%20client)) ([IdentityServer4 Integration with ASP.NET Core - Code Maze](https://code-maze.com/identityserver4-integration-aspnetcore/#:~:text=information%20about%20the%20flow%20we,allowed%20scopes%20for%20the%20client)). We often use this for machine-to-machine API calls.
- **Resource Owner Password Credentials Flow (ROPC):** Allows exchanging user credentials (username/password) directly for a token. This is legacy and not recommended except maybe in trusted environments, because it requires the client to handle user passwords (though IdentityServer can support it, as shown in config using `AllowedGrantTypes = GrantTypes.ResourceOwnerPassword` for a client) ([IdentityServer4 Integration with ASP.NET Core - Code Maze](https://code-maze.com/identityserver4-integration-aspnetcore/#:~:text=So%2C%20we%20provide%20the%20,allowed%20scopes%20for%20the%20client)). It's better to use Authorization Code or device flow for interactive logins.
- **Implicit and Hybrid Flows:** These were used in older scenarios (Implicit for pure front-end apps, Hybrid for mixing server and client tokens). Implicit is generally not recommended now in favor of Authorization Code with PKCE (which is more secure for SPAs).

In our context, if we have an ASP.NET Core MVC app or Razor Pages app, it can act as an OAuth client to IdentityServer. If we have a separate API, that API will trust IdentityServer to validate tokens.

#### 3.2.3 Authenticating Users with IdentityServer (OpenID Connect in ASP.NET Core)

Once IdentityServer is configured and running, an ASP.NET Core web app can use OIDC to authenticate users. In Startup (or Program) of the web app:

```csharp
services.AddAuthentication(options => {
        options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = "oidc";
    })
    .AddCookie(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddOpenIdConnect("oidc", options => {
        options.Authority = "https://localhost:5001"; // IdentityServer URL
        options.ClientId = "webclient";
        options.ClientSecret = "SuperSecretPassword";
        options.ResponseType = "code"; // using auth code flow
        options.UsePkce = true;
        options.Scope.Add("openid");
        options.Scope.Add("profile");
        options.Scope.Add("api.read");
        options.SaveTokens = true; // save the tokens in the auth ticket (so we can use them later)
    });
```

This sets up the app to use a cookie for local login state and OIDC for challenges. Now, `[Authorize]` attributes in this app will automatically redirect unauthenticated users to IdentityServer’s login page. After login, the OIDC middleware will handle the callback, validate the ID token, establish a local user session (cookie), and save the access token (if any).

Developers can then retrieve the user’s claims (like name, email) via `User.Identity` and make calls to APIs using the saved access token if needed.

**Key security points:**

- The `Authority` is the trusted URL of the IDP; the middleware uses this to fetch configuration and signing keys, so it knows how to validate tokens.
- `UsePkce = true` ensures that even if this is a public client, the auth code exchange is secured with a proof key (to mitigate interception attacks).
- `SaveTokens = true` stores the JWTs in the cookie claim set. If this is a concern (it slightly increases cookie size and might be a risk if someone hijacks the cookie), you might store it server-side or fetch tokens on demand.

#### 3.2.4 Protecting APIs with JWT Bearer Authentication

If you have a separate Web API (e.g., a RESTful API serving data to your front-end), you likely want to secure it with JWT access tokens issued by IdentityServer (or any OAuth2 provider). In the API’s startup:

```csharp
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => {
        options.Authority = "https://localhost:5001"; // IdentityServer URL
        options.Audience = "api1"; // expected audience of the token (one of the ApiResources/Scopes)
        options.TokenValidationParameters = new TokenValidationParameters {
            ValidateIssuerSigningKey = true,
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true
        };
    });
```

With this, any incoming request to the API will require an `Authorization: Bearer <token>` header. The JWT middleware will:

- Validate the token’s signature (by fetching the signing keys from the authority’s discovery document automatically).
- Validate that the token is not expired and intended for this API (audience match).
- Create a `ClaimsPrincipal` for the user represented by the token.

Then you can use `[Authorize]` attributes or `HttpContext.User` in the API just as you would in an MVC app. If the token is missing or invalid, the request is denied with a 401.

**Pro Tip:** Scope-based auth – you can require certain scopes for certain endpoints. IdentityServer issues scopes in JWT as claims (often under `scope`). In ASP.NET Core, you could write a policy:

```csharp
options.AddPolicy("ApiRead", policy => policy.RequireClaim("scope", "api.read"));
```

Then:

```csharp
[Authorize(Policy = "ApiRead")]
[HttpGet]
public IEnumerable<Data> GetData() { ... }
```

This ensures the JWT must contain `scope: api.read` to access that endpoint. If a client app only had a token with `api.write` but not `api.read`, it would be denied. This is a form of permission enforcement.

#### 3.2.5 IdentityServer and ASP.NET Core Identity

In real applications, IdentityServer is often combined with ASP.NET Core Identity (which manages users, passwords, emails, etc.). IdentityServer can use ASP.NET Identity as its user store (so that when users login, it uses Identity’s user manager to verify password, etc.). Due to complexity, we won't show the full setup here, but know that:

- ASP.NET Identity stores hashed passwords (PBKDF2) and user details in a database.
- IdentityServer can be configured with `.AddAspNetIdentity<YourUser>()` to connect them.
- This way, when IdentityServer's login page is shown, it might actually be the typical ASP.NET Identity login UI.

The result is a robust system where IdentityServer (the auth server) delegates user validation to Identity (which is safe and battle-tested), and then issues tokens.

### 3.3 Working with JWT Tokens in .NET Core

Whether you use IdentityServer or a simpler JWT approach, understanding JWT usage is important.

**What is a JWT?** A JSON Web Token is a compact, URL-safe means of representing claims between two parties. It’s basically a JSON payload (claims about a user or client) that is signed (and optionally encrypted). For authentication, a JWT might include claims like `sub` (subject identifier for the user), `name`, `roles`, and `exp` (expiration time). The token is signed by the issuer (e.g., IdentityServer or another authority) so that the resource server (your API) can verify it hasn’t been tampered with.

**An example JWT (decoded):**

```json
{
  "iss": "https://localhost:5001",
  "aud": "api1",
  "sub": "1",
  "name": "alice",
  "scope": ["openid", "profile", "api.read"],
  "exp": 1700000000
}
```

This token says: issuer is our IDP, audience is "api1", it’s for user subject 1 (Alice), with scopes including `api.read`. The `exp` is a timestamp when it expires. This token would be signed with the IDP’s private key.

**Validating JWTs in .NET:** We typically rely on the JWT middleware as shown earlier. But if needed, you can manually validate using `JwtSecurityTokenHandler`. Example:

```csharp
var handler = new JwtSecurityTokenHandler();
var token = handler.ReadJwtToken(tokenString);
// (You could inspect token.Claims here)
var parameters = new TokenValidationParameters {
    ValidIssuer = "https://localhost:5001",
    ValidAudience = "api1",
    IssuerSigningKey = new SymmetricSecurityKey(Encoding.ASCII.GetBytes("your-256-bit-secret"))
};
SecurityToken validated;
var principal = handler.ValidateToken(tokenString, parameters, out validated);
```

This will throw if validation fails, or give you a `ClaimsPrincipal` if success. In real scenarios, you use the signing key (or a set of keys) that the issuer uses. With IdentityServer or other OIDC providers, usually we use their public key (for asymmetric RSA signatures) or a shared secret (for symmetric). The middleware can fetch it from discovery automatically if `Authority` is set.

**JWT Best Practices:**

- **Keep tokens short-lived.** Don’t issue access tokens valid for days. A common practice is 1 hour or less. This limits the window of misuse if stolen. If longer sessions are needed, use refresh tokens (we won't deep dive here, but refresh tokens allow obtaining new access tokens without re-login, and they can be revoked).
- **Use HTTPS.** Never transmit JWTs over plaintext. Even though the token is signed, if an attacker intercepts it, they can use it (it’s a bearer token – possession equals authority).
- **Store tokens securely on client side.** If you have a SPA, avoid storing JWT in plaintext local storage (vulnerable to XSS). Some recommend storing in an HttpOnly cookie, but then you must handle CSRF. Either approach has risks; a common compromise is to use the token in memory and rely on short expiration + refresh flow (with refresh token in HttpOnly cookie).
- **Validate at Audience and Issuer.** The middleware examples already show this – your API should ensure the token was meant for it (audience) and came from a trusted issuer.
- **Signature Algorithm choice:** Avoid `alg: none` (which means no signature – should never be accepted). If using symmetric signing (HMAC SHA256), ensure a strong secret key (at least 32 bytes). If using RSA/ECDsa, manage the keys properly (rotate if needed, etc.). IdentityServer uses RS256 by default which is secure.

### 3.4 Authorization in ASP.NET Core (Policies and Roles)

Once authentication (user login and identity establishment) is done (whether via cookie or JWT), the next step is to enforce authorization on actions.

**Role-based Authorization:** Simplest form, e.g.:

```csharp
[Authorize(Roles = "Admin")]
public IActionResult GetAllUsers() { ... }
```

The user must have a claim of type `role` (or `Roles` configured appropriately) with value “Admin”. If you use ASP.NET Identity, when a user is assigned a role, that will typically be present. If using JWTs, you might need to configure the token to include roles (for example, IdentityServer can include roles if you map the claims).

**Policy-based Authorization:** This is more flexible. As mentioned, you can define policies that might require certain claims or custom requirements:

```csharp
services.AddAuthorization(options =>
{
    options.AddPolicy("CanDeleteOrder", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim("Department", "Sales") &&
            context.User.IsInRole("Manager")));
});
```

This example policy requires that the user is in the Sales department _and_ is a Manager role. Then:

```csharp
[Authorize(Policy = "CanDeleteOrder")]
public IActionResult DeleteOrder(int orderId) { ... }
```

This will only allow users meeting that criteria.

You can also create policies that require claims with certain values, or even write a custom authorization handler for complex logic (like time-based access, or hierarchical permissions). For advanced cases, consider libraries like **PolicyServer** or custom solutions if you need attribute-level or record-level permissions – but those are beyond our scope.

**Default Authorization:** If you want all endpoints to require authorization by default, you can configure the auth middleware with a fallback policy:

```csharp
options.FallbackPolicy = new AuthorizationPolicyBuilder()
                              .RequireAuthenticatedUser()
                              .Build();
```

This would mean any endpoint that isn’t specifically marked `[AllowAnonymous]` will require an authenticated user. It’s often a good default for API applications.

**Resource-Based Authorization:** Sometimes you need to authorize based on a specific resource instance (for example, a user can edit their own profile but not others’). ASP.NET Core allows this by passing the resource to the `Authorize` attribute in policy, or more directly, by using within-code checks using the `IAuthorizationService`:

```csharp
var result = await _authorizationService.AuthorizeAsync(User, resourceItem, "PolicyName");
if (!result.Succeeded) {
    return Forbid();
}
// else proceed
```

Where `resourceItem` could be your data object, and your policy handler checks that the current `User.Identity.Name` matches, for example, `resourceItem.OwnerName`. This is how you would enforce record-level ownership checks.

### 3.5 Dealing with Identity Management: Sessions, Logout, etc.

**Sessions in Cookie Auth:** If you use cookie-based auth (like traditional ASP.NET Identity in MVC), the user’s login state is kept in a cookie. Logging out simply means removing that cookie (and possibly doing a sign-out on IdentityServer if using external login). Use `HttpContext.SignOutAsync()` to logout:

```csharp
await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
await HttpContext.SignOutAsync("oidc"); // if using OIDC, sign out of IdentityServer too
```

This ensures the cookie is cleared and the user is also logged out from the identity provider (if OIDC, the middleware knows to call the end session endpoint).

**JWTs and Logout:** If you use JWTs, “logging out” is trickier because the token on the client might just expire on its own. One cannot forcibly expire a JWT unless you maintain a server-side blacklist or the client discards it. Some approaches:

- Have short token lifetimes so that logout is not too significant (the token will expire soon anyway).
- Use refresh tokens: if user “logs out”, you can revoke the refresh token on server so they cannot get new tokens.
- If needed, keep a token blacklist on the API (e.g., store revoked token IDs) but this is typically not desired due to complexity.

**Concurrent Login control:** In some apps, you might want to invalidate old sessions when a user logs in somewhere else. With JWTs, this again needs custom logic (like a unique session ID claim that you track). With cookies and Identity, you can regenerate the security stamp and require validation. This is an advanced topic; for high-security apps, consider using the built-in **SecurityStamp** feature of ASP.NET Identity (it can sign out all sessions when a user’s security stamp changes, such as password reset or manually calling `UpdateSecurityStamp`).

**Account Lockout and Recovery:** Ensure you have flows for password reset (with secure tokens emailed to users), account lockout after too many failures (Identity does this by default: e.g., 5 failed attempts in 5 minutes could lock for 5 minutes). Encourage users to have unique emails or phone for recovery.

**Two-Factor Authentication:** If using Identity, enable 2FA via SMS or authenticator apps for accounts – this significantly improves security for user accounts by requiring a second step.

By properly implementing and configuring authentication/authorization, you cover OWASP categories like Broken Authentication and Broken Access Control directly. In fact, many real-world breaches happen due to these aspects being weak. With the above practices, your .NET Core app’s login and access control subsystem will be significantly hardened.

**Exercise 3:** _Implement a Basic OAuth2 Client_ – As a practical exercise, try setting up a minimal IdentityServer (or you can use a demo IdentityServer instance) and then configure an ASP.NET Core Web API to accept JWTs from that IdentityServer. Write a small client (could be a console app or use a tool like curl/Postman) to fetch a token (using client credentials or resource owner password for simplicity) and call the API with it. This will help you understand the flow end-to-end. Document the steps you took and any issues encountered (e.g., JWT validation errors) and how you resolved them. This hands-on experience is invaluable in mastering auth in .NET. (In the appendix, we will outline a sample solution for how to do this.)

---

## Chapter 4: Securing APIs and Microservices (Rate Limiting, CORS, and Secure Headers)

Modern applications often expose web APIs (for SPAs, mobile apps, or microservice architectures). This chapter focuses on securing those HTTP endpoints beyond just auth. We will discuss **rate limiting** to prevent abuse, configuring **CORS** correctly for cross-origin requests, and setting various **HTTP security headers** to harden your application’s responses.

### 4.1 Rate Limiting to Throttle Malicious or Excessive Requests

**Why rate limit?** To protect your application from denial-of-service (DoS) attacks or even accidental overload by clients. By limiting how many requests a single client (or IP or user) can make in a time window, you ensure fair usage and preserve resources.

ASP.NET Core introduced built-in **Rate Limiting Middleware** in .NET 7 ([Announcing Rate Limiting for .NET - Microsoft Developer Blogs](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=Announcing%20Rate%20Limiting%20for%20,to%20avoid%20overwhelming%20your%20app)) ([Rate limiting middleware in ASP.NET Core - Learn Microsoft](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=Rate%20limiting%20middleware%20in%20ASP,Apps)). For .NET 6 or earlier, you would use custom middleware or libraries (like `AspNetCoreRateLimit` package). We will illustrate using the .NET 7+ built-in approach, as it's more streamlined.

#### 4.1.1 Rate Limiting Basics

Common algorithms for rate limiting:

- **Fixed Window**: Allow N requests per time window (e.g., 100 requests per minute). Counter resets each window. ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=Fixed%20window%20limit)) ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=allowed%20to%20line%20up%20before,in%20the%20fixed%20window%20algorithm))
- **Sliding Window**: Similar to fixed, but a bit smoother by looking at a rolling time window to avoid burst at boundary issues ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=Sliding%20window%20limit)) ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=The%20sliding%20window%20algorithm%20is,weren%E2%80%99t%20any%20requests%20our%20limit)).
- **Token Bucket**: A bucket of tokens refills at a rate; each request consumes a token. Allows burst up to bucket size, then steadies out ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=Token%20bucket%20limit)) ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=To%20give%20a%20more%20concrete,unless%20requests%20take%20more%20tokens)).
- **Concurrency Limit**: Limit number of parallel requests executing at once (e.g., only 10 concurrent requests) ([Announcing Rate Limiting for .NET - .NET Blog](https://devblogs.microsoft.com/dotnet/announcing-rate-limiting-for-dotnet/#:~:text=Concurrency%20limit)).

The .NET middleware supports these via `AddFixedWindowLimiter`, `AddSlidingWindowLimiter`, `AddTokenBucketLimiter`, `AddConcurrencyLimiter` ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=The%20RateLimiterOptionsExtensions%20class%20provides%20the,extension%20methods%20for%20rate%20limiting)) ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=The%20AddFixedWindowLimiter%20method%20uses%20a,the%20request%20limit%20is%20reset)).

#### 4.1.2 Configuring Rate Limiting in .NET Core

First, install the package (if not already in Microsoft.AspNetCore.App): `dotnet add package Microsoft.AspNetCore.RateLimiting`.

Then in Program.cs:

```csharp
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.RateLimiting;

var builder = WebApplication.CreateBuilder(args);

// 1. Add the RateLimiter service
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("fixed", policy =>
    {
        policy.PermitLimit = 100;               // allow 100 requests
        policy.Window = TimeSpan.FromMinutes(1); // per 1 minute window
        policy.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        policy.QueueLimit = 2;                  // allow 2 extra requests to queue (beyond 100) before refusing
    });

    // You could configure other named policies or a default global one
    options.RejectionStatusCode = 429; // HTTP 429 Too Many Requests
});

// 2. Build app and enable rate limiting middleware
var app = builder.Build();

app.UseRateLimiter(); // add this before app.UseAuthorization() in pipeline

// 3. Apply the policy to endpoints
app.MapGet("/api/data", [EnableRateLimiting("fixed")] () => Results.Ok("Here is your data"));
```

In this example:

- We defined a policy named `"fixed"` with 100 requests/minute limit ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=builder.Services.AddRateLimiter%28_%20%3D%3E%20_%20.AddFixedWindowLimiter%28policyName%3A%20,QueueLimit%20%3D%202%3B)) ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=,12%20to%20OldestFirst)). If more requests come in that minute, they will be rejected with HTTP 429 (Too Many Requests). We allow a small queue of 2, meaning if at one moment there are a couple of extra requests, they wait briefly for the next window.
- We applied `[EnableRateLimiting("fixed")]` to a specific endpoint. You can also configure a global limiter with `options.GlobalLimiter` that applies to all requests, or use `RequireRateLimiting` on endpoints as shown in docs ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=app.MapGet%28,fixed)).

For example, global:

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(httpContext =>
    {
        // Partition by IP (could also use user id if logged in)
        var ip = httpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        return RateLimitPartition.GetFixedWindowLimiter(ip, key => new FixedWindowRateLimiterOptions
        {
            PermitLimit = 50,
            Window = TimeSpan.FromSeconds(30),
            QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
            QueueLimit = 0
        });
    });
    options.RejectionStatusCode = 429;
});
```

This uses a partitioned limiter by IP address, allowing 50 requests per 30 seconds per IP. Partitioning is powerful – it logically gives each unique key (like IP) its own rate counter.

**Important considerations:**

- Decide what to rate limit by: IP address is common, but in some cases you might have many behind one proxy – ensure to use X-Forwarded-For or similar if behind load balancers. Alternatively, limit by user account (if tokens are present).
- Rate limits should match your system capacity and typical usage. Too strict and you might throttle legitimate users; too lenient and it may not stop abuse.
- Provide helpful feedback: HTTP 429 with maybe a `Retry-After` header can hint clients when to retry.
- Some clients (like automated ones) respect `Retry-After`. You can set it via `options.OnRejected` event in the RateLimiterOptions to add headers:
  ```csharp
  options.OnRejected = (context, result) =>
  {
      context.HttpContext.Response.Headers["Retry-After"] = "60"; // retry after 60 seconds
      return new ValueTask();
  };
  ```

By applying rate limiting, you mitigate brute-force attacks (e.g., someone trying many passwords or tokens), scraping, and basic DoS from a single source. It’s an essential piece for public-facing APIs.

#### 4.1.3 Rate Limiting in Microservices

If you have multiple microservices, you might implement rate limiting at the gateway level (e.g., using an API Gateway like Azure API Management, Traefik, or Envoy). However, in-service rate limiting (as above) is still useful for defense in depth.

For internal APIs (service-to-service), you might not need rate limiting, except to catch accidental floods (bugs causing excessive calls). Typically, rate limiting is more for external facing endpoints.

**Real-World Note:** Many public APIs (Twitter, GitHub, etc.) have strict rate limits (like X requests per hour). They often use API keys or user tokens to associate the limits. In our context, you could partition by an API key or user account for a more fair limit than by IP (since IP could be shared). Implementing that requires looking at the request (maybe in `PartitionedRateLimiter` using a header or user claim as the key).

### 4.2 Configuring CORS (Cross-Origin Resource Sharing) Safely

**What is CORS?** Browsers enforce a “same-origin policy” which restricts scripts on one origin (domain/port) from making requests to a different origin. CORS is a protocol that allows a server to relax this restriction for certain trusted origins by including specific headers in responses.

If your .NET Core API is accessed by a web app running on a different domain (e.g., your API is at api.example.com and your frontend at app.example.com), you’ll need to enable CORS on the API to allow the app’s domain to call it.

However, configuring CORS incorrectly can lead to security issues. For instance, allowing all origins (`*`) for all requests might expose your API to requests from malicious sites, potentially enabling CSRF or other attacks in some scenarios.

#### 4.2.1 Enabling CORS in .NET Core

In Startup/Program:

```csharp
var MyAllowSpecificOrigins = "_myAllowSpecificOrigins";

builder.Services.AddCors(options =>
{
    options.AddPolicy(name: MyAllowSpecificOrigins,
        policy  =>
        {
            policy.WithOrigins("https://app.example.com", "https://admin.example.com")
                  .AllowAnyHeader()
                  .AllowAnyMethod();
                  // .AllowCredentials(); // if you need to support cookies/auth
        });
});
```

Then:

```csharp
app.UseCors(MyAllowSpecificOrigins);
```

This will add the appropriate CORS headers to responses for requests coming from the specified origins (the browser sends an `Origin` header, and the middleware will respond with `Access-Control-Allow-Origin: https://app.example.com` if it matches). We allowed any header and method for simplicity – you can lock those down too (e.g., allow only GET, POST if that’s all you use, etc., and only certain headers if you want to be restrictive).

**Never use `AllowAnyOrigin` in combination with `AllowCredentials`.** This is disallowed by the framework because it’s a big security risk (any site could send requests including credentials). If you need credentials (cookies or HTTP auth) to be sent in cross-site requests, you must specifically specify origins.

CORS **does not make your site more secure**, it actually _relaxes_ security to allow trusted sites. A common misconception is that enabling CORS protects something – it doesn’t; it simply controls which cross-origins are allowed. OWASP notes that "CORS is not a security feature, CORS relaxes security. An API is not safer by allowing CORS." ([Enable Cross-Origin Requests (CORS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cors?view=aspnetcore-9.0#:~:text=,earlier%20techniques%2C%20such%20as%20JSONP)). So, allow only the minimum origins that need access.

#### 4.2.2 Typical CORS Use Cases

- **Single Page Application + API:** The SPA hosted on `domainA.com` calls the API on `domainB.com`. CORS must allow `domainA.com` on the API. The SPA will likely use bearer tokens or cookies. If using cookies (not common for SPAs, but possible), you’d need to allow credentials in CORS and set `WithOrigins` to that specific domain (no wildcard).
- **Third-party integrations:** If you want to expose certain API endpoints to be usable via AJAX from any site (like a public JS SDK scenario), you might allow `*` for those particular resources (but carefully evaluate what they do).

#### 4.2.3 Common CORS Pitfalls

- Forgetting to include CORS middleware _before_ endpoints are mapped. The `UseCors` should typically come early (certainly before `UseEndpoints`). In minimal API setups, mapping with `[EnableCors]` filters or the like can also be used per endpoint.
- Not handling preflight (`OPTIONS`) requests. The CORS middleware automatically takes care of preflight (browsers send an `OPTIONS` request to ask what’s allowed). Ensure your app isn’t blocking OPTIONS (if you wrote a custom auth middleware, etc., be sure to let OPTIONS through or handle it idempotently).
- Overly broad origins. For example, `WithOrigins("https://*.example.com")` is not supported (no wildcard subdomains in the built-in method; you’d need to add a custom policy if you want that). Or using `AllowAnyOrigin()` for authenticated endpoints: if your API uses cookies for auth, `AllowAnyOrigin` could let malicious sites trigger your user’s actions (a kind of CSRF via XHR).
- Not understanding that CORS is only enforced by browsers. A malicious script or attack tool can always craft requests irrespective of CORS (they are not running in a browser context or they disable CORS). So, do not rely on CORS for security on the backend – enforce authentication and authorization on all requests. CORS is just for the browser’s protection of users. It is an important config for functionality (making your app work when domains differ), but not a security control on its own.

**CORS and OWASP:** While CORS is more of a configuration, misconfiguration can be an issue (fits under Security Misconfiguration in OWASP Top 10). For example, an API that unintentionally allows any origin could be abused by a malicious website to read data using a logged-in user’s session. So treat CORS configuration as part of your security review.

### 4.3 Setting Secure HTTP Headers

HTTP response headers can instruct browsers to enhance security. Some important headers and how to apply them in ASP.NET Core:

#### 4.3.1 Important Security Headers

- **Strict-Transport-Security (HSTS):** Informs browsers to only use HTTPS for future requests to your site. It prevents downgrade attacks and accidental http. For example: `Strict-Transport-Security: max-age=31536000; includeSubDomains`. In ASP.NET Core, you can enable this via `app.UseHsts()` (enabled by default in templates when in Production environment). You should only enable HSTS on sites that are exclusively HTTPS. Once a browser sees this header, it won’t attempt HTTP for the specified period (max-age, here 1 year). This is great for security, but be careful in development or on new domains (don’t turn it on until you’re sure all is HTTPS, because browsers will remember it).
- **Content-Security-Policy (CSP):** This header helps mitigate XSS by whitelisting content sources. For example, you might allow scripts only from your own domain and a trusted CDN, and disallow inline scripts. A simple example: `Content-Security-Policy: default-src 'self'; script-src 'self' https://trustedscripts.example.com; object-src 'none';`. A full CSP is complex to craft but very effective in preventing injected scripts from running, because the browser will block any script not allowed by the policy. We can set this header in ASP.NET Core, but it requires thoughtful configuration (possibly vary by page if needed). We will see how to set it via middleware or NWebSec.
- **X-Content-Type-Options:** Usually set to `nosniff`. This prevents browsers from MIME-sniffing responses away from the declared Content-Type. For example, if you serve a file as text, the browser won’t try to execute it as something else. It’s a simple header: `X-Content-Type-Options: nosniff`.
- **X-Frame-Options:** Controls whether your pages can be put in an iframe on other sites (clickjacking protection). Common values: `DENY` (no framing allowed), `SAMEORIGIN` (allow if the framing page is same site). Example: `X-Frame-Options: SAMEORIGIN`. CSP can also control framing via `frame-ancestors` directive nowadays (which is more powerful and the modern replacement).
- **X-XSS-Protection:** An old header related to IE/Edge XSS filter. Often set to `0` (to disable) or `1; mode=block`. Modern Chrome has removed support for it. It’s not very relevant if you have proper CSP and output encoding, but some scans still check for it. Setting `X-XSS-Protection: 1; mode=block` doesn’t harm (except perhaps on some older browsers). ZAP scanner tends to flag missing X-XSS-Protection as a medium finding ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=the%20configuration%20of%20the%20%E2%80%98X,header%20on%20the%20web%20server)) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=context.Response.Headers.Add%28%22X)).
- **Referrer-Policy:** Controls how much referrer info is sent when navigating from your site elsewhere or vice versa. A safer setting is `Referrer-Policy: no-referrer-when-downgrade` or `strict-origin-when-cross-origin`. This prevents leaking full URLs from HTTPS site to HTTP destinations, etc. It’s more privacy than strict security, but recommended.
- **Permissions-Policy (formerly Feature-Policy):** Allows you to control use of certain browser features/API by your site or if embedded. For example: `Permissions-Policy: geolocation=(), camera=()` to disable those. This is more relevant if you have embedded content or want to ensure your site isn’t inadvertently enabling features.

#### 4.3.2 Adding Headers in ASP.NET Core

You can always manually add headers in responses. For a simple approach without external libraries:

```csharp
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Frame-Options", "SAMEORIGIN");
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Xss-Protection", "1; mode=block");
    context.Response.Headers.Add("Referrer-Policy", "no-referrer-when-downgrade");
    // CSP might be too long to add here as string literal; consider using NWebSec for complex ones
    await next();
});
```

This middleware, placed early, will append these headers to every response (unless overridden elsewhere).

However, it's often better to use existing libraries or built-in methods:

- **UseHsts():** As mentioned, sets HSTS header for you (with some defaults, usually 30 days if not configured, or you can configure options for includeSubDomains, etc.). Only enable in production and for sites that are HTTPS.
- **NWebSec library:** This was a common library (still useful up to .NET 5; for .NET 6+, some features might not be maintained as actively since similar functionality can be done with built-in middleware). But NWebSec provides extension methods for many headers, making it convenient:
  ```csharp
  app.UseHsts(hsts => hsts.MaxAge(days: 365).IncludeSubdomains());
  app.UseXContentTypeOptions();
  app.UseXfo(xfo => xfo.Deny()); // or .SameOrigin()
  app.UseXXssProtection(options => options.EnabledWithBlockMode());
  app.UseReferrerPolicy(opts => opts.NoReferrerWhenDowngrade());
  app.UseCsp(csp => csp
      .DefaultSources(s => s.Self())
      .ScriptSources(s => s.Self().CustomSources("https://trustedscripts.example.com"))
      .ObjectSources(s => s.None())
  );
  ```
  This fluent API is from NWebSec (as shown in Scott Hanselman’s blog) ([Easily adding Security Headers to your ASP.NET Core web app and getting an A grade - Scott Hanselman's Blog](https://www.hanselman.com/blog/easily-adding-security-headers-to-your-aspnet-core-web-app-and-getting-an-a-grade#:~:text=app.UseHsts%28options%20%3D,opts.NoReferrerWhenDowngrade)) ([Easily adding Security Headers to your ASP.NET Core web app and getting an A grade - Scott Hanselman's Blog](https://www.hanselman.com/blog/easily-adding-security-headers-to-your-aspnet-core-web-app-and-getting-an-a-grade#:~:text=app.UseXContentTypeOptions%28%29%3B%20app.UseXXssProtection%28options%20%3D,opts.NoReferrerWhenDowngrade)). It’s very readable and ensures the syntax is correct (CSP strings can be tricky to get right with all quotes and semicolons).
- **Using Response Headers in Web.config (IIS):** If you host on IIS, you can also set headers in web.config (as Hanselman showed an example web.config section adding headers) ([Easily adding Security Headers to your ASP.NET Core web app and getting an A grade - Scott Hanselman's Blog](https://www.hanselman.com/blog/easily-adding-security-headers-to-your-aspnet-core-web-app-and-getting-an-a-grade#:~:text=%3CcustomHeaders%3E%20%3Cadd%20name%3D%22Strict,eval%27%20www.google.com%20cse.google.com)) ([Easily adding Security Headers to your ASP.NET Core web app and getting an A grade - Scott Hanselman's Blog](https://www.hanselman.com/blog/easily-adding-security-headers-to-your-aspnet-core-web-app-and-getting-an-a-grade#:~:text=cdn,none%27%3Bcamera%20%27none%27%3Bmagnetometer%20%27none%27%3Bgyroscope%20%27none%27%3Bspeaker%20%27self%27%3Bvibrate)). But in .NET Core, especially cross-platform, it's easier to handle in middleware or your code.

**Testing your headers:** After setting them up, test your site with tools like **Mozilla Observatory** or **SecurityHeaders.com**. These will give you a grade and point out missing headers or misconfigurations. The goal is often to get an A grade on these scans, which means you have most of the recommended headers.

For example, adding the headers we discussed often yields an A on securityheaders.com. Without them, you might get a C or D even if everything else is secure, because lacking these headers is considered a vulnerability (or at least a missed hardening opportunity).

#### 4.3.3 Cookie Security Flags

We touched on this in Chapter 3, but as part of headers/config, ensure cookies have:

- `HttpOnly`
- `Secure`
- `SameSite` attributes.

In .NET Core, when using cookie auth or even session, configure:

```csharp
services.AddSession(options => {
    options.Cookie.HttpOnly = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    options.Cookie.SameSite = SameSiteMode.Lax;
});
```

For authentication cookie:

```csharp
services.ConfigureApplicationCookie(options => {
    options.Cookie.Name = ".AuthCookie";
    options.Cookie.HttpOnly = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    options.Cookie.SameSite = SameSiteMode.Lax;
});
```

These ensure that the cookie (which isn’t a header but an HTTP attribute) is flagged appropriately:

- HttpOnly: JavaScript cannot read it, preventing XSS from stealing the session.
- Secure: Not sent in clear HTTP.
- SameSite: Controls cross-site sending. `Lax` means cookie is not sent on cross-site requests except top-level navigation (which is okay for most scenarios, and this setting helps mitigate CSRF for things like forms because the browser won’t send the cookie on a hidden POST from another site). `Strict` is even more restrictive (not sent at all cross-site, even if user clicks a link to your site – which can cause usability issues, like “remember me” cookies not sent if coming from an email link). `None` means cookie will be sent in all contexts (but then Secure must be true). Generally, Lax is a safe default for auth cookies now.

#### 4.3.4 Removing Identifying Headers

By default, ASP.NET Core no longer adds the `X-Powered-By` header (which used to show ASP.NET or version info) as older ASP.NET did. However, if hosting on certain servers, you might see a `Server` header (e.g., Kestrel might show “Kestrel” or IIS might show “Microsoft-IIS/10.0”). While removing these doesn’t necessarily improve security, it’s often done to not reveal information about your server stack (security by obscurity, minor benefit). If using Kestrel directly, you can’t easily remove the `Server` header without writing a middleware to strip it (which you can do). If using IIS, you can remove or mask it in web.config or IIS config.

In Hanselman’s example, they removed `X-Powered-By`, `X-AspNet-Version`, and `Server` headers using web.config in a Windows-hosted scenario ([Easily adding Security Headers to your ASP.NET Core web app and getting an A grade - Scott Hanselman's Blog](https://www.hanselman.com/blog/easily-adding-security-headers-to-your-aspnet-core-web-app-and-getting-an-a-grade#:~:text=%27none%27%3Bfullscreen%20%27self%27%3Bpayment%20%27none%27%3B%22%2F%3E%20%3Cremove%20name%3D%22X,Version%22%20%2F%3E%20%3Cremove%20name%3D%22Server%22)). In cross-platform, use a middleware:

```csharp
app.Use(async (ctx, next) => {
    ctx.Response.OnStarting(() => {
        ctx.Response.Headers.Remove("Server");
        return Task.CompletedTask;
    });
    await next();
});
```

This will remove the Server header just before the response is sent.

**Be cautious** that some hosting add their own header via reverse proxies (e.g., Azure might add some). Removing those might not be possible from the app side.

#### 4.3.5 Real World: Common Findings by Scanners

If you run OWASP ZAP or similar scanners (or even automated bug bounty scanners) against your app, some very common findings (if you haven’t set headers) include:

- Missing X-Frame-Options (usually Medium risk, easy fix by adding SAMEORIGIN) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=ZAP%20description%3A%20X,to%20protect%20against%20%E2%80%98ClickJacking%E2%80%99%20attacks)) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=app.Use%28async%20%28context%2C%20next%29%20%3D,Options%22%2C%20%22SAMEORIGIN%22%29%3B%20await%20next%28%29%3B)).
- Missing X-Content-Type-Options (Low risk, add nosniff).
- Missing CSP (Informational or sometimes High, depending on context, because CSP greatly helps against XSS).
- Missing HSTS (Medium if site is HTTPS, because you should enforce it).
- Missing `HttpOnly`/`Secure` flags on cookies (Medium risk) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Cookie%20No%20HttpOnly%20Flag)) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Reference%3A%20http%3A%2F%2Fwww)).
- Server info leakage via headers (Informational).
- If your app is purely API (no HTML), X-Frame-Options is less relevant (since you’re not framing an API typically), but scanners don’t always distinguish – still good to include.

By preemptively adding these headers, your application will fare much better in security reviews and, more importantly, will be more resilient to certain attacks (like clickjacking, XSS, protocol downgrade, etc.).

### 4.4 Additional API Security Practices

Beyond the big three above, a few more pointers for securing APIs and microservices:

- **Validation & Serialization:** When binding JSON input to models, ensure you have input validation (Chapter 2 covers this). Also, be mindful of over-binding – e.g., a client sending more fields than expected and them being updated. Use view models or DTOs that contain only what should be settable. This prevents an attack where an extra field (like "IsAdmin": true) in JSON might elevate privileges if your model had such a property and you inadvertently bind and save it.
- **Versioning and Deprecated Endpoints:** When deprecating endpoints, eventually remove them. Old endpoints left around might not have the latest security fixes.
- **Use HTTPS and up-to-date TLS:** This is obvious but must be stated. All microservice communication should also be encrypted (if not using service mesh that handles it, at least use TLS between services when possible, or a secure network).
- **Service Authentication:** Microservices should authenticate to each other – e.g., using client certificates or JWTs (client credentials flow). Don’t rely purely on network ACLs, especially in cloud environments – defense in depth says even internal APIs should ensure the caller is legitimate. Tools like Kubernetes mTLS (Istio) or IdentityServer issuing client tokens help.
- **Audit Logging:** Have your services log important access events and possibly trace IDs for tracking a chain of requests. This helps in forensic analysis if something goes wrong.
- **Graceful degradation under attack:** Rate limiting helps here. Additionally, have circuit breakers or fallbacks. If one service is being hammered, it could cause cascading failures. Patterns from the **Reactive Manifesto** or **Polly** library for resilience can help isolate failures so that one overloaded part doesn’t crash everything (this goes into availability, but availability is a security attribute too in terms of DoS).

By implementing the strategies in this chapter – rate limiting, proper CORS configuration, and secure headers – your .NET Core APIs and microservices will be far more robust against common web attacks and abuse patterns.

**Exercise 4:** _Harden a Web API_ – Take a simple ASP.NET Core Web API project (maybe an example project) and try to harden it:

1. Enable CORS so that only your test client (e.g., a React app at `http://localhost:3000`) can call it.
2. Add rate limiting such that any one IP can only hit the `api/values` endpoint 5 times per minute.
3. Add middleware to add security headers (at least HSTS, X-Content-Type-Options, X-Frame-Options).
4. Run the API (perhaps host it on `https://localhost:5001`) and use a tool like OWASP ZAP to scan it. Observe the difference in reported vulnerabilities before and after adding these protections.

Document what ZAP or Observatory reports. Are there any headers or issues you missed? Fix them and re-scan to see improvement. This exercise will give you practical insight into how these measures reflect in security scanning results (which is similar to what a pen tester or automated scan would catch).

---

## Chapter 5: Mitigating Common Vulnerabilities (SQL Injection, XSS, CSRF, etc.)

Now that we have covered general best practices, authentication/authorization, and API hardening, let's focus specifically on the **OWASP Top 10 vulnerabilities and their mitigation techniques** in .NET Core. We will go through the most prevalent ones (like SQL Injection, Cross-Site Scripting, Cross-Site Request Forgery) and show how to test for them and fix them. Many mitigations have been hinted at in earlier chapters, but here we consolidate and deepen the discussion around each vulnerability category.

### 5.1 SQL Injection (and Other Injection Flaws)

**The Vulnerability:** SQL Injection occurs when an application incorporates untrusted input into a SQL query without proper validation or escaping, allowing an attacker to alter the query’s structure ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=So%2C%20it%27s%20not%20unreasonable%20to,would%20have%20code%20like%20this)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=The%20string%20concatenation%20would%20result,in%20the%20following%20query)). Similar injection principles apply to other contexts: OS command injection (if you pass input to shell commands), LDAP query injection, etc.

**Impact:** An attacker can extract sensitive data, modify or destroy data (e.g., drop tables), or even escalate to executing OS commands via database (in some cases).

**Mitigation Techniques:**

- **Use Parameterized Queries:** This cannot be overstated. It is the primary defense. Example (bad vs good):

  ```csharp
  // BAD – vulnerable to SQL injection
  string query = $"SELECT * FROM Users WHERE Username = '{user}' AND Password = '{pass}'";
  // If user = admin'--  and any pass, the query becomes: SELECT * FROM Users WHERE Username='admin'--' AND Password='...'
  ```

  The `'--` would comment out the rest, effectively `SELECT * FROM Users WHERE Username='admin'`, which might log them in without checking password.

  ```csharp
  // GOOD – parameterized
  string sql = "SELECT * FROM Users WHERE Username = @user AND Password = @pass";
  using var cmd = new SqlCommand(sql, conn);
  cmd.Parameters.AddWithValue("@user", user);
  cmd.Parameters.AddWithValue("@pass", pass);
  ```

  Now no matter what `user` contains (even malicious SQL), it will be treated as a literal value for that parameter ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Parametrized%20queries%20avoid%20SQL%20injection,of%20the%20SQL%20query%20itself)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=After%20creating%20a%20new%20SqlCommand%2C,parameter%20using%20the%20AddWithValue%20method)).

- **ORM Usage:** ORMs like Entity Framework do this by default. However, caution if using raw SQL through ORM:
  - Use `FromSqlInterpolated` (EF Core) instead of `FromSqlRaw` when inserting parameters, or ensure you use proper `DbParameter`.
  - Dapper is a micro-ORM that encourages parameter usage (its API by design uses parameter placeholders).
- **Stored Procedures:** Historically, using stored procs was a recommendation. It can help if the stored proc internals don't concatenate inputs. But if a stored proc builds dynamic SQL unsafely, it's still injectable. So stored procs are not a panacea; parameterization remains key.

- **Validate Inputs (Defense in Depth):** E.g., if an ID is expected to be numeric, validate that before even using it in query. This doesn't replace parameterization, but it can stop obviously bad input early ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=Validating%20Input)). For example:

  ```csharp
  if(!int.TryParse(productId, out int pid)) return BadRequest("Invalid product id");
  db.Products.Find(pid);
  ```

  This way, an input like `1; DROP TABLE Products` is immediately rejected as not an int.

- **Least Privilege for DB Account:** We mentioned this earlier: The app's DB login should have the minimal rights necessary ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=A%20great%20security%20practice%E2%80%94not%20only,your%20app%2C%20and%20nothing%20more)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=,ORDER%20BY%20Published%20DESC)). If your app's queries never need to drop tables, don’t give it drop permissions. So even if injection occurs, the damage might be limited (e.g., maybe data read but not full destruction). For read-only scenarios, use a read-only account.

- **ORM Injection Note:** ORMs can have other injection-like issues if misused. E.g., an ORM that allows method like `context.Database.ExecuteSqlRaw($"UPDATE... {userInput}")` is just as dangerous as using `SqlCommand` incorrectly. Also watch out for NoSQL injection if using something like MongoDB – ensure queries are built properly (most drivers use JSON/BSON objects which are safer than string concatenation, but if you dynamically build JSON with user input, similar concept applies).

**Example:** Let’s simulate a simple vulnerable code and its fix:

```csharp
// Vulnerable
string search = HttpContext.Request.Query["q"];
string query = "SELECT * FROM Products WHERE Name LIKE '%" + search + "%'";
var cmd = new SqlCommand(query, conn);
var reader = cmd.ExecuteReader();
```

If `search` = `%' OR 1=1 --`, this query becomes `SELECT * FROM Products WHERE Name LIKE '%%' OR 1=1 --%'`. The `OR 1=1` causes all products to be returned (or potentially more destructive depending on context).

**Fix:**

```csharp
string search = HttpContext.Request.Query["q"];
string query = "SELECT * FROM Products WHERE Name LIKE @name";
var cmd = new SqlCommand(query, conn);
cmd.Parameters.AddWithValue("@name", "%" + search + "%");
```

Now, if `search` contained SQL wildcards or quote, it’s just part of the parameter value to match literally (except `%` which we intentionally added for wildcard search). No OR 1=1 injection is possible.

**Testing for SQL Injection:** During dev or testing, you can attempt basic SQLi strings in inputs (like `' OR '1'='1` or `'; DROP TABLE --`). Additionally, tools like **SQLMap** can automate injection testing. Always test on non-production data! If you use parameterization everywhere, SQLMap should not find an injection vector.

SQL injection is consistently in OWASP Top 10 (or the broader “Injection” category) because it's so dangerous. Yet as shown, the prevention in .NET is straightforward with proper coding.

### 5.2 Cross-Site Scripting (XSS)

**The Vulnerability:** XSS occurs when an application includes user-supplied input in a page without proper output encoding or validation, allowing the attacker to inject malicious JavaScript that runs in other users’ browsers ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=Cross,validating%2C%20encoding%20or%20escaping%20it)) ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=When%20other%20users%20load%20affected,validating%2C%20encoding%20or%20escaping%20it)). XSS can be:

- _Stored_: malicious script is stored on the server (in a database, etc.) and served to other users (e.g., a forum post containing a `<script>`).
- _Reflected_: script is in a link or request and reflected off the server (like an error message or search result that directly includes what was input). If a user is tricked into clicking such a link, their browser executes the injected script.
- _DOM-based_: the vulnerability is in the client-side JavaScript, which processes input from `document.location` or other sources insecurely.

**Impact:** XSS can hijack user sessions, deface websites, or redirect users. For instance, an attacker could steal cookies, allowing them to impersonate users. They could also perform actions on behalf of users (if the app relies only on cookies for auth, the script can silently make requests, a sort of CSRF via XSS). Basically, XSS is one of the most dangerous client-side issues.

**Mitigation Techniques:**

- **Output Encoding:** The primary defense. As the OWASP XSS prevention cheat sheet says: _encode everything by default unless you explicitly need unencoded HTML_. ASP.NET Core’s Razor engine by default encodes variables you output in views ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=HTML%20Encoding%20using%20Razor)) ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=Take%20the%20following%20Razor%20view%3A)). For example:

  ```csharp
  @foreach(var comment in Model.Comments) {
      <p>@comment.Text</p>
  }
  ```

  Even if `comment.Text` contains `<script>alert('xss')</script>`, Razor will output it as `&lt;script&gt;alert('xss')&lt;/script&gt;`, neutralizing it. This is automatic HTML encoding. **Never bypass it** by using `@Html.Raw` on untrusted data.

- **Context-specific Encoding:** If injecting data into attributes, JavaScript, or CSS contexts, appropriate encoding is needed ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=2,JavaScript%20encoding%20takes%20dangerous)) ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=characters%20for%20JavaScript%20and%20replaces,string%20ensure%20it%27s%20URL%20encoded)):

  - HTML attribute encoding (Razor does this if you put a var inside an attribute).
  - JavaScript encoding: If you absolutely must output user data into a script block, you should JSON-encode or JavaScript-encode it. e.g.:
    ```html
    <script>
      var username = "@JavaScriptEncoder.Default.Encode(user.Name)";
    </script>
    ```
    Or better: put the data in a `data-` attribute and read it in script (thus using HTML encoding which is handled, as suggested by Microsoft docs ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=JavaScript%20Encoding%20using%20Razor)) ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=%3Cdiv%20id%3D%22injectedData%22%20data))).
  - URL encoding: If putting untrusted data in URLs (e.g., query string parameters), use `UrlEncoder`.

- **Never mix untrusted data in HTML without encoding:** This includes not just script tags, but also avoiding to inject raw HTML from users (like a rich text field) unless you thoroughly sanitize it (which is hard; if needed, use a library like HTML Sanitizer to whitelist tags).

- **CSP (Content Security Policy):** Mentioned earlier, CSP is a powerful mitigating control. If you set a strict CSP (no inline scripts, only scripts from your domain or known sources, etc.), even if XSS occurs, the injected script might be blocked from executing or from doing anything useful (like it can't load an external script because CSP forbids it). CSP is a second line of defense and highly recommended. For example, requiring all scripts to have a nonce that your server generates means an attacker’s script injection without that nonce will fail.

- **Avoid dangerous APIs:** In older ASP.NET, `Response.Write` or manually building HTML was common; in Razor, minimize use of `HtmlString` or raw output. The Microsoft docs explicitly warn that `HtmlString` is not encoded ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=Warning)). Also on the client side, be careful with `innerHTML` assignment in JavaScript if it uses any data that may have come indirectly from user input; prefer `textContent` for inserting text.

- **Validate Input (for XSS):** This is tricky because you can’t filter all XSS (there are so many payload variations). However, if you have form fields that shouldn’t contain certain characters (like a username probably shouldn’t have `<` or `>`), you can reject those to reduce XSS chance. But be careful not to break legitimate cases (e.g., an address might need an ampersand or quotes). Encoding on output is more reliable than blacklisting input characters ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=This%20article%20applies%20primarily%20to,rendered%20in%20the%20user%27s%20browser)) ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=To%20prevent%20XSS%20attacks%2C%20web,information%2C%20see%20this%20GitHub%20issue)).

- **Libraries and Templates:** Use modern frameworks (Razor, or React/Vue on front-end which auto-escape by default) to your advantage. For instance, in React, data binding escapes HTML by default (unless you dangerously set HTML). The principle is consistent: auto-escape everywhere.

**XSS Example and Fix:**

Imagine a product review system where users can enter comments and other users see them.

- Vulnerable scenario: The developer stores the comments and when displaying, they do:

  ```csharp
  <div class="comment">@comment.Content</div>
  ```

  Actually, Razor will encode that – so Razor by default is safe. But if the developer got clever and allowed "HTML comments" or used `@Html.Raw(comment.Content)` to preserve formatting, then a user could input:

  ```html
  Great product! <img src="x" onerror="alert('XSS')" />
  ```

  This would pop an alert for any user viewing the review (the `onerror` triggers because `src=x` fails to load).

- Fix: Simply do not use Raw unless necessary. If wanting to allow some HTML, sanitize it (strip out `<script>` tags, `onerror` attributes, etc.). There are libraries like [Ganss.XSS](https://github.com/mganss/HtmlSanitizer) that can sanitize HTML input. Use them if you must accept HTML (like user-provided rich text content).

**Reflected XSS example:** Suppose you have a search page that takes a query parameter and shows “You searched for X”. If you do:

```csharp
<p>You searched for @Request.Query["q"]</p>
```

Razor encodes that, so you’d see actual `<script>` in the text if someone tried injecting. But if a developer mistakenly disabled encoding or in older ASP (if they did Response.Write(Request["q"])), an attacker could craft:

```
http://site/search?q=<script>stealCookies()</script>
```

When a user with an active session clicks that, it would execute on their browser, stealing cookies.

**Mitigation:** Don’t disable encoding. Also, you can use CSP to disallow inline scripts, so even if reflected, maybe the script won’t run. But best is not to have the XSS in the first place.

**Testing for XSS:** Use common payloads in form inputs or URL params, like:

- `"><script>alert(1)</script>` (see if an alert happens).
- Use browser developer tools to inspect if output is properly encoded (e.g., see `&lt;script&gt;` vs actual `<script>` in DOM).
- Tools: OWASP ZAP has XSS injection in Active Scan. There are also specialized XSS payload lists.

### 5.3 Cross-Site Request Forgery (CSRF)

**The Vulnerability:** CSRF (or XSRF) is an attack where an unauthorized command is transmitted from a user that the web application trusts. In simple terms, if a user is logged into your site, an attacker can trick their browser into making a request (GET or POST) to your site (using the user's session), without the user’s intention. E.g., the user visits malicioussite.com which has some JS or an image tag like `<img src="https://bank.com/transfer?amount=1000&to=attacker" />`. If the user is logged in to bank.com, their browser will include their session cookie with that request, potentially executing the transfer.

**Impact:** CSRF can perform state-changing actions on behalf of users (transfers, changing email, etc.) since the site only sees a valid request with a valid session. It cannot steal data directly (because the response goes to the user, not attacker), but if the action itself causes some change, that's done.

**Mitigation Techniques:**

- **Anti-forgery Tokens:** ASP.NET Core has built-in CSRF protection for POST forms. When you use `<form asp-antiforgery="true">` (or the default in Razor Pages), it emits a hidden field `__RequestVerificationToken` and also sets a same-named cookie. On form submission, the server verifies that the cookie and form field token match ([Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery?view=aspnetcore-9.0#:~:text=Synchronizer%20Token%20Pattern%20%28STP%29,a%20page%20with%20form%20data)) ([Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery?view=aspnetcore-9.0#:~:text=The%20token%20is%20unique%20and,view%20examples%20generates%20antiforgery%20tokens)). Only a page from your domain could have provided that token (because an external site cannot read the user’s cookie or generate a valid token). Use the `[ValidateAntiForgeryToken]` on controllers or Razor Page handlers to enforce this ([Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery?view=aspnetcore-9.0#:~:text=ASP,for%20working%20with%20antiforgery%20tokens)). In MVC, it's applied by default to any `[HttpPost]` action when using the auto-validate filter (AutoValidateAntiforgeryToken, which is in templates for any state-changing verb).

  So for any form:

  ```html
  <form asp-action="UpdateEmail" method="post">
    <input type="email" name="newEmail" />
    <input
      type="hidden"
      name="__RequestVerificationToken"
      value="@Antiforgery.GetTokens(HttpContext).RequestToken"
    />
    <button type="submit">Update</button>
  </form>
  ```

  If you use the Tag Helper or HTML Helper `@Html.AntiForgeryToken()`, they output that hidden field and cookie for you ([Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery?view=aspnetcore-9.0#:~:text=Explicitly%20add%20an%20antiforgery%20token,AntiForgeryToken)) ([Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery?view=aspnetcore-9.0#:~:text=In%20each%20of%20the%20preceding,similar%20to%20the%20following%20example)). Always include that in forms that modify data. The `[ValidateAntiForgeryToken]` will then validate it.

- **SameSite Cookies:** Modern approach leverages `SameSite` cookie attribute. If you set your auth session cookie as `SameSite=Lax` or `Strict`, the browser will not send it on cross-site requests (except some safe navigation cases in Lax). This mitigates CSRF because the malicious site cannot cause the user’s browser to send the cookie along with a cross-origin request. In .NET Core, cookies default to Lax which already covers most CSRF for typical POST forms (except if the user is tricked by a top-level navigation, but then they see the page – not silent).

  Note that anti-forgery tokens are still in use especially for login forms or if supporting older browsers. But SameSite is an additional built-in protection. In fact, OWASP removed CSRF from Top 10 partly due to frameworks using SameSite by default making it less common ([why CSRF is removed from OWASP top 10, how to prevent CSRF on ...](https://stackoverflow.com/questions/48373904/why-csrf-is-removed-from-owasp-top-10-how-to-prevent-csrf-on-asp-net-mvc#:~:text=why%20CSRF%20is%20removed%20from,and%20some%20form%20of%20protections)).

- **Check Referer/Origin header:** As a fallback, some apps check the `Origin` or `Referer` header of requests. If a request is supposed to be same-site (e.g., a form submission), then the Origin should be your domain. If it's absent or different, you can reject. This is not foolproof but in combination with tokens can be a useful check. Some frameworks do this check as well in their anti-CSRF implementation.

- **For APIs with JWT (no cookies):** If your API is purely stateless (e.g., uses JWT in Authorization header, not cookies), CSRF is generally not a concern. CSRF relies on browser automatically including credentials (like cookies or HTTP Basic auth). With JWT, the token is typically stored in JS (not recommended in cookies), and the external site cannot read the token from the user’s storage (assuming no XSS). However, if someone foolishly put JWT in a cookie, then it becomes CSRF-able. So, advice: _don’t put bearer tokens in cookies_. If you need to, then treat them like session cookies and defend accordingly (token + double-submit cookie etc.).
  For an SPA using cookies (some use-case to have a unified auth), then implement anti-forgery token similar concept: have the SPA get a CSRF token from server after login and send it in headers for subsequent requests (the server can validate against a value in cookie). Many frameworks (Angular, etc.) have this built-in if using cookie-based APIs.

**CSRF Example and Fix:**

Imagine a profile page with a form to update email:

```html
<form method="post" action="/profile/email">
  New email: <input name="email" type="email" />
  <button type="submit">Save</button>
</form>
```

And the corresponding action:

```csharp
[HttpPost]
public IActionResult Email(string email) {
    // update user email
}
```

If no anti-forgery is used, an attacker could send the user a link or auto-submit a form from evil.com:

```html
<form action="https://yoursite.com/profile/email" method="post">
  <input type="hidden" name="email" value="attacker@evil.com" />
</form>
<script>
  document.forms[0].submit();
</script>
```

When the user (logged in to yoursite) visits this, their browser posts to yoursite with their cookies, updating the email to attacker’s address.

**Fix:** In Startup, ensure `services.AddControllersWithViews(options => options.Filters.Add(new AutoValidateAntiforgeryTokenAttribute()));` is enabled (this is default in new projects). Then in the form view, add `@Html.AntiForgeryToken()` inside the form. Also ensure the cookie policy has SameSite Lax or Strict. With these, the above attack fails:

- The request from evil.com wouldn’t carry the anti-forgery token, so the server would reject it with 400.
- Additionally, if SameSite=Lax, a CSRF from a third-party context might not even send the cookie (if it’s not top-level navigation).

**Note on API CSRF:** If you have a pure REST API (no cookies, only tokens), CSRF is not directly a threat because browsers won’t automatically attach the bearer token from local storage or such (they can’t unless your JS does it, and an attacker’s site cannot call your JS due to CORS). But if you allow cross-origin requests widely and rely on cookie auth for an API, you have a problem (but then it’s basically a web app).

### 5.4 Broken Authentication and Session Management

We covered a lot in Chapter 3, but to recap specific failure modes:

- Passwords stored in database in plaintext or with weak hashing = huge risk (if DB compromised, all user passwords are known). **Mitigation:** Use strong hashing (e.g., ASP.NET Identity uses PBKDF2 with per-user salt and multiple iterations) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=On%20the%20other%20hand%2C%20several,hashing%20algorithms%20are%20safe)). Better, use a proven user management system (don’t DIY) so these are handled.
- No password policy or multi-factor = easier for attackers. Mitigation: enforce complexity or at least length (passphrases), encourage 2FA.
- Session IDs not rotating after login = session fixation risk. Mitigation: on successful login, call `HttpContext.SignInAsync` which will by default issue a new cookie (and the old one should be invalid – in Identity, they do a regenerate on login). Also, if you have a long-lived session cookie, consider regenerating it periodically or if privilege changes.
- Not logging out properly server-side. E.g., user hits “logout” but you just delete cookie on client; if someone stole the cookie, server still accepts it until expiry. Mitigation: if high-security, maintain a server-side session store or revocation list. Often not done in stateless JWT setups, but consider short expiration for JWT and revoking refresh tokens.
- Missing account lockout/brute force protection. Mitigation: Limit failed logins (e.g., 5 attempts then 5 min lock). Also possibly CAPTCHA after many failed attempts.
- Default credentials or predictable passwords (like admin/admin). Mitigation: obviously, change defaults and force admin to set strong password on first run.
- Exposed authentication endpoints lacking brute-force protection (like an open OAuth token endpoint with no lockout). Use rate limiting (like not letting one IP spam the token endpoint).
- Not using HTTPS for login or session – credentials can be intercepted. Mitigation: Always use TLS. HSTS ensures even if user types http, it goes https next time.

### 5.5 Broken Access Control (and Insecure Direct Object References)

Broken Access Control is a broad category. The core is users can act outside their intended permissions. Examples in .NET app:

- A regular user can access an admin page because the developer forgot `[Authorize(Roles="Admin")]`.
- An API does role checks in UI only, but not on the API route (client-side enforcement only, which is bypassable by directly calling API).
- Insecure Direct Object Reference (IDOR): e.g., `/api/order/12345` returns order data if you are that owner. But what if user changes URL to `/api/order/12346` (someone else’s order)? If no check that the order belongs to the user, that’s a data exposure. The fix is to enforce in code that the order’s OwnerId == current user’s id, otherwise deny.
- Not using user-specific keys in queries. For instance, `SELECT * FROM Orders WHERE OrderId = @id` – if id is global, any id will return an order. Instead, do `WHERE OrderId=@id AND UserId=@userId`.
- File access: If the app serves files and uses a filename from user input, broken access could allow path traversal (e.g., `?file=../../web.config`). Always validate and restrict paths (and ideally don’t take raw paths from user at all).

**Mitigations:**

- Use the framework’s authorization consistently (don’t roll your own, avoid “security by obscurity” where URL is hidden but not protected).
- Deny by default: require authorization on all endpoints unless explicitly public.
- For multi-tenant data: always filter by user or tenant ID in queries, based on the authenticated user’s identity.
- Test by logging in as a low-privilege user and attempting to access high-privilege functions (both via UI and by direct URL guessing or API calls). Automated test: use a tool like **OWASP Zap** or Postman with one user’s token to call another user’s resources.
- Ensure that disabled accounts or users who shouldn’t have access indeed cannot. For example, if a user is not an admin anymore, any cached privileges (like JWT claims) should be updated or invalidated.

In .NET, one convenient feature is **Resource-based authorization** as mentioned. If you find yourself writing `if (thing.OwnerId != currentUserId) return Forbid();` all over, you might centralize that logic in an AuthorizationHandler for a requirement like "SameOwner". But even without that, doing the check is what matters.

**Case in point:** The Panera Bread case we cited ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=For%20example%2C%20some%20of%20the,points%2C%20including%20by%20phone%20number)) ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=%E2%80%9CPanera%20Bread%20uses%20sequential%20integers,the%20entire%20database%2C%E2%80%9D%20Houlihan%20said)) is a classic broken access/IDOR. They had user info accessible via incrementing IDs with no auth check beyond being logged in. To fix that, they should have required authentication (maybe they did) _and_ ensured that one user can only fetch their own record (e.g., require the ID in URL to match the authenticated user’s ID, or better yet don’t use numeric IDs from user side at all, use the identity from token).

### 5.6 Security Misconfiguration

This is kind of a catch-all for things like:

- Using default keys, passwords, or config (e.g., leaving the default ASP.NET Identity secret key in appsettings, etc.).
- Debug configuration on production (showing error pages, having swagger open without auth in production, etc.).
- Not patching the system or platform (like running an old .NET Core runtime with known vulnerabilities, or letting the server OS be unpatched).
- Improper CORS config (allowing any origin as we discussed).
- Not enforcing TLS or having it misconfigured (like supporting old SSL versions, weak cipher suites).
- Leaving unnecessary services enabled (like the development Kestrel console or some diagnostic info endpoint).

**Mitigations:**

- Create deployment checklists. E.g., ensure `ASPNETCORE_ENVIRONMENT = Production` on the server, which by default triggers more secure settings.
- Remove or secure administrative endpoints (hangfire dashboard, health checks, etc.). Put them behind auth or IP allowlists.
- Regularly update NuGet packages and the .NET runtime. The .NET Core runtime occasionally has security updates (the app may need redeploy on new runtime patch).
- If using containers, don’t run as root in container if not needed; minimize attack surface in images (use Alpine or slim images).
- Use secure headers and options (which we covered in Chapter 4).
- Scan your application with tools (like a Nessus scan or other) to find common misconfigs (it might flag verbose server banners, old libraries, etc.).

A specific .NET example: The infamous `Web.Debug.config` transforms often left `<compilation debug="true">` on debug and false on release. In ASP.NET Core, debug show DeveloperExceptionPage. Always double-check that in production it’s not enabled:

```csharp
if (env.IsDevelopment()) {
   app.UseDeveloperExceptionPage();
} else {
   app.UseExceptionHandler("/Home/Error");
   app.UseHsts();
}
```

This pattern ensures no stack traces leak in prod.

Another: if you use swagger (Swashbuckle) in your API, by default it might be available to anyone at `/swagger`. In production, you probably want to either secure it (if it's sensitive) or disable it. Exposing your API spec publicly isn't a direct vuln, but it gives attackers more info easily (so it's recommended to restrict it to internal or require auth).

### 5.7 Using Components with Known Vulnerabilities

This one is straightforward: if your app uses a vulnerable version of a library, you’re at risk. For instance:

- Using a version of Newtonsoft.Json that had a known flaw in certain deserialization (just hypothetical).
- Using an outdated version of jQuery with known XSS issues.
- Or using .NET Framework or older .NET Core that is out of support and has unpatched issues.

**Mitigations:**

- Use tools like dependabot, OWASP Dependency Check, or Whitesource (like in Chapter 7) to identify vulnerable packages ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=,penetration%20testing%20on%20the%20websites)) ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=SonarQube%20SonarQube%20is%20an%20automatic,Image%204)).
- Keep an inventory of your components and their versions.
- Plan regular updates (e.g., allocate time each sprint to update NuGets).
- Pay attention to announcements (Microsoft security advisories for .NET, NuGet project release notes).
- If you absolutely cannot upgrade a component immediately, consider compensating controls. E.g., if a library has a vulnerability only exploitable by certain input, try to filter that input until you patch.

Example: A vulnerability in an image processing library that could be exploited by a malicious image -> if you can’t update library at once, maybe disable that feature or do extra validation on images to avoid the malicious trigger.

### 5.8 Insecure Deserialization

Although not as common in .NET Core (especially since BinaryFormatter is obsolete), this is worth a mention:

- **BinaryFormatter** in older .NET could be used to deserialize untrusted data leading to code execution. .NET Core marks it as obsolete. Avoid BinaryFormatter or LosFormatter. If you need binary serialization, use safe ones like protobuf-net or System.Text.Json for JSON.
- **JSON Deserialization issues:** If you deserialize JSON/YAML/XML from an untrusted source into objects, ensure the types are expected. In some frameworks, there were attacks via polymorphic deserialization (like sending type info to make the deserializer instantiate a dangerous type). System.Text.Json by default does not allow polymorphic type handling unless you opt-in. Newtonsoft.Json can be configured with TypeNameHandling which can be dangerous if not limited (it could allow an attacker to specify a type to deserialize into that has side effects).
- **ViewState/MAC**: In classic WebForms, an example: not setting ViewState MAC and an attacker forging it. In .NET Core, not applicable.

**Mitigations:**

- Don’t accept serialized blobs from users unless necessary. If needed, use secure formats (JSON with defined schema).
- If using JSON.Net and allowing type names, restrict the allowed types to a safe list.
- Update libraries like Newtonsoft if any known issues (for example, there was a well-known JSON.Net vulnerability with TypeNameHandling from 2017 if misconfigured).
- Use signing or encryption for any serialized data that travels between client and server (like cookies or hidden fields). ASP.NET Core Data Protection API is used for its own cookies and such.

### 5.9 Security Logging & Monitoring Failures

We discussed logging in Chapter 2 and 8. But to reiterate:

- Implement logging of important security events (logins, admin actions, etc.).
- Protect logs (they may contain sensitive info, so secure log storage).
- Monitor them using a SIEM or at least alerts for multiple failed logins, etc.
- Also consider enabling additional auditing in Identity (like track last login, etc., to detect anomalies).
- If using cloud, leverage services like Azure Application Insights or AWS CloudWatch for centralized logs and alerts.

If an incident happens, these logs are your only way to piece together what happened. Many breaches go undetected for months because nobody looked at logs or there were none. E.g., an attacker creates an admin account – was that event logged and flagged? If not, you wouldn’t know until much later.

### 5.10 Server-Side Request Forgery (SSRF)

We already covered SSRF in context of Capital One ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=The%20attacker%20gained%20access%20to,the%20data%20contained%20in%20them)). If your app fetches URLs based on user input:

- Do not allow internal addresses (like 169.254.169.254 AWS metadata, or localhost, or your internal microservice hosts). Validate the URL’s hostname/IP against an allow list or block private IP ranges.
- Use an external proxy with filtering if possible (some companies route all outgoing calls through a proxy that can filter or monitor).
- If the functionality is not needed, remove it (often SSRF exists in some generic HTTP fetch endpoint that isn’t critical).
- Use least privilege on any credentials on the server (Capital One’s issue was that the server had an IAM role with too broad permissions accessible via metadata).
- Example mitigation: If user can provide an image URL to upload from the web, instead of letting your server download it directly, consider having a safer approach or at least restrict to http/https and check content type.

### 5.11 Summary of Mitigations by OWASP Category

Let's summarize with a quick list mapping OWASP Top 10 (2021) to key mitigations in .NET Core context:

- **A1: Broken Access Control:** Use `[Authorize]` appropriately, implement role/claims checks, never trust client-side alone, enforce ownership checks at code level.
- **A2: Cryptographic Failures:** Always encrypt sensitive data at rest (use DPAPI or field-level encryption), use TLS, don’t transmit secrets in plaintext, secure password hashing (no plaintext passwords).
- **A3: Injection:** Parameterize queries, validate inputs, use ORMs, avoid dynamic eval or OS command execution with user input. Output encoding for XSS (which is injection of script into HTML). Use libraries to handle data safely.
- **A4: Insecure Design:** (This is broader) Do threat modeling, apply principles like least privilege, fail secure, etc. Don’t design workflows that circumvent security for convenience.
- **A5: Security Misconfiguration:** Harden environment (disable directory listing if serving files, use proper headers, update software, minimal features turned on).
- **A6: Vulnerable Components:** Keep dependencies updated, use tools to find known vulns, and have a patch process.
- **A7: Identification & Auth Failures:** Use robust frameworks for auth, secure session management (HttpOnly cookies, etc.), implement MFA, no default creds, protect against brute force (as in Sec.5.4).
- **A8: Software Integrity Failures:** Use signed packages, verify integrity of plugins (e.g., only load plugins from a secure source or check hashes). Protect CI/CD – e.g., ensure your build pipeline is secure so no one can inject backdoor in the code building process.
- **A9: Logging & Monitoring:** Ensure sensitive actions are logged, logs are kept safe, and alerts exist. E.g., send an admin alert if an unknown admin account is created or if there are too many 500 errors (could indicate attempted exploitation).
- **A10: SSRF:** Validate outbound requests, or disable unnecessary SSRF-prone features, and use network layer controls as backup.

**Exercise 5:** _Vulnerability Hunt_ – Take an intentionally vulnerable .NET Core application or a simple app you wrote and introduce a few vulnerabilities (or use a pre-made vulnerable app if available). For example:

- Introduce an XSS by outputting raw input.
- Introduce a SQL Injection by building a query unsafely.
- Remove [Authorize] on an admin action.
- Disable the antiforgery token validation on a form.

Then swap with a peer or simply run a scanner (like ZAP) and try to find and exploit these vulnerabilities. Document how you would exploit each (e.g., what input triggers the SQL injection to drop a table? what script can you inject for XSS?). Then, apply the fixes described in this chapter and retest to ensure the vulnerabilities are gone.

This will cement your understanding of these common issues and their fixes in a hands-on way.

---

## Chapter 6: Secure Handling of Sensitive Data (Encryption, Hashing, and Secrets Management)

Applications often deal with sensitive data: user passwords, personal information, financial data, etc. In this chapter, we will explore how to properly protect such data in .NET Core. This includes using **encryption** for data at rest, **hashing** for passwords, and managing secrets (like API keys or connection strings) securely.

### 6.1 Encryption Basics in .NET

**Encryption** is making data unreadable without a secret key. Use encryption for data that you need to retrieve in original form later (e.g., encrypting a credit card number to store, so you can decrypt when charging).

- **Symmetric Encryption:** Same key for encrypt and decrypt. .NET provides algorithms like AES (recommended), DES/3DES (outdated, do not use DES, 3DES is legacy), and others. AES in CBC mode with a random IV is common, or the newer AES-GCM (which also provides built-in integrity checking) ([.NET cryptography model - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/security/cryptography-model#:~:text=,This%20level%20is%20abstract)) ([.NET cryptography model - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/security/cryptography-model#:~:text=Going%20forward%2C%20this%20model%20of,the%20responsibility%20of%20the%20developer)). .NET has `Aes.Create()` to get an AES object. Example:

  ```csharp
  using var aes = Aes.Create();
  aes.Key = key;           // 32 bytes for AES-256
  aes.IV = iv;             // 16 bytes IV for AES
  var encryptor = aes.CreateEncryptor();
  using var ms = new MemoryStream();
  using var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write);
  using var sw = new StreamWriter(cs);
  sw.Write(plaintext);
  sw.Close();
  byte[] cipherText = ms.ToArray();
  ```

  This is similar to the code example in the DEV article ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=,ms%2C%20encryptor)) ([Top 10 Tips with Code Examples: How to Secure Your C# Application - DEV Community](https://dev.to/ssukhpinder/top-10-tips-with-code-examples-how-to-secure-your-c-application-ia7#:~:text=,)). The output `cipherText` you’d store alongside the IV (the IV can be public, it's not a secret, but must be unique per encryption). The key must be kept secret (in config or key vault).

  For decryption, you do reverse: `aes.CreateDecryptor()` and read from CryptoStream.

  AES-GCM (since .NET Core 3) is even easier using `AesGcm` class:

  ```csharp
  var aesGcm = new AesGcm(key);
  byte[] cipherText = new byte[plainBytes.Length];
  byte[] tag = new byte[16]; // authentication tag
  aesGcm.Encrypt(iv, plainBytes, cipherText, tag);
  ```

  AES-GCM gives you an auth tag to ensure the data wasn’t tampered. It’s recommended for new apps if you need authenticated encryption. Always either use an authenticated cipher mode (GCM) or include an HMAC with CBC encryption to prevent modifications (encrypt-then-MAC).

- **Asymmetric Encryption:** Public/private key (RSA, ECDsa). Use cases: exchanging keys securely, or digital signatures. If you need to, .NET has RSA in `System.Security.Cryptography`. Usually, you use RSA to encrypt a symmetric key, then use that symmetric key for bulk data (this is how TLS works under the hood). For most app needs, you rarely encrypt large data directly with RSA because it’s inefficient. You may use RSA to encrypt something small like a password or a token that only the server can decrypt with its private key.

- **Data Protection API:** .NET Core has a built-in data protection API (`Microsoft.AspNetCore.DataProtection`) primarily for protecting things like cookies, but you can use it for your own data. It manages key rotation and storage for you (by default, keys stored on disk, or you can configure Azure Key Vault, etc.). It’s mainly useful for protecting data that only _your app_ (or a set of apps sharing the same key ring) needs to decrypt. For example:

  ```csharp
  var protector = _dataProtectionProvider.CreateProtector("MyApp.Purpose.Strings");
  string cipherText = protector.Protect(sensitiveString);
  string plain = protector.Unprotect(cipherText);
  ```

  It uses AES + HMAC internally, and handles keys. This is great for things like connection strings in config that you want to encrypt, or maybe query parameters that you want to ensure not tampered.

- **File Encryption:** If you need to encrypt files, you could use the same AES routines reading/writing file streams. Or use OS-level encryption (e.g., Windows EFS) if appropriate.

**Key Management:** Encryption is only as good as the secrecy of your keys:

- Do not hardcode keys in source (we mentioned this in best practices). Keep them in config or better, in Azure Key Vault or AWS KMS. These services can either store keys for you or even perform cryptographic operations so the key itself never leaves the vault (e.g., Azure Key Vault can do encryption/decryption with stored keys).
- If using DataProtection, protect the key store. For example, in Azure, DataProtection can be configured to encrypt keys at rest with an X.509 certificate or key vault.
- Regularly rotate keys if possible. That can be complex (need to re-encrypt existing data or keep multiple keys for old vs new data), but at least have a strategy.

**Example scenario:** Storing credit card numbers for recurring billing. Instead of storing them in plaintext (never do that), you encrypt them with AES-256. The key is stored in Azure Key Vault. Your app, when needing to charge, pulls the key (or uses the vault to decrypt) and gets the number to pass to payment gateway. This way, even if the database is compromised, the attacker can’t get card numbers unless they also compromise the key vault (which is separate and hopefully strongly protected).

### 6.2 Hashing and Salting Passwords

**Hashing** is a one-way function. For passwords, we never want to decrypt – we just store a hash and compare hashes on login attempts.

- **Use strong, slow hashing algorithms for passwords:** As Code Maze article points out, MD5 and SHA1 are fast and now insecure for password storage ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=However%2C%20as%20more%20and%20more,use%20these%20for%20password%20hashing)) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=past%20became%20insecure,use%20these%20for%20password%20hashing)). We use algorithms like **PBKDF2**, **BCrypt**, **SCrypt**, or **Argon2** which are designed to be slow (to thwart brute force by making each attempt computationally heavy) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=,Argon2)) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=The%C2%A0BCrypt%2FSCrypt%20family%20of%20algorithms%20is,force%20attacks)).

  ASP.NET Core Identity uses PBKDF2 (HMACSHA256 by default in recent versions, 10k iterations by default). That is generally fine. If you roll your own, you can use `Rfc2898DeriveBytes` as shown by Code Maze to generate a hash:

  ```csharp
  byte[] salt = RandomNumberGenerator.GetBytes(16);
  string password = "userSupplied";
  // 10000 iterations, output 32-byte (256-bit) hash
  byte[] hash = Rfc2898DeriveBytes.Pbkdf2(Encoding.UTF8.GetBytes(password), salt, 10000, HashAlgorithmName.SHA256, 32);
  ```

  ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=var%20hash%20%3D%20Rfc2898DeriveBytes,salt%2C%20iterations)). You would store the salt and hash (and iteration count if you ever plan to change it).

  Then to verify:

  ```csharp
  byte[] hash2 = Rfc2898DeriveBytes.Pbkdf2(password, salt, 10000, HashAlgorithmName.SHA256, 32);
  bool isValid = CryptographicOperations.FixedTimeEquals(hash2, hash);
  ```

  Use `FixedTimeEquals` or similar constant-time comparison to avoid timing attacks on hash checking ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=var%20hashToCompare%20%3D%20Rfc2898DeriveBytes,iterations%2C%20hashAlgorithm%2C%20keySize)).

- **Salt**: The salt ensures that two users with same password have different hashes ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=Hashing%20Isn%E2%80%99t%20Enough%3A%20Password%20Salting)), and that precomputed rainbow tables for common passwords are ineffective without that salt. Always use a cryptographically random salt per password (16 bytes is common). .NET provides RNGcrypto service as shown.
- **Pepper (Application-level salt)**: Sometimes used as well – e.g., an additional secret value (not stored with the hash, but in code or config) that is used in hashing. This way, if DB is compromised, attacker still needs the pepper to crack hashes. But if app server is compromised, pepper might be found, so it's not foolproof. Many systems forego pepper if they trust the hashing strength, but it's an option.

- **Other data hashing:** Sometimes we hash data to create identifiers or fingerprints (e.g., hashing an email to get an ID that is not reversible but can be compared). For those, speed is fine (you might use SHA-256) since it's not about brute forcing. But careful: if it’s something like email, an attacker can brute force many possible emails (using known lists) to see which hash matches. So if you need non-reversible but also not guessable, consider HMAC (hash with a secret key). For instance, hashing user emails with a secret key (HMACSHA256) and using that as identifier means an outsider can’t enumerate emails without the key.

- **Storing other secrets:** If you store API keys or access tokens for users (like OAuth tokens), those should often be encrypted rather than plain. For example, you let users link their Twitter account and you store their OAuth token/secret – encrypt those in DB so that a DB leak doesn’t expose them.

**Storing Hashes Example:**

Suppose a user registers with password "P@ssw0rd1". We:

- Generate random 16-byte salt (e.g., `0xAB3CF8...`).
- Compute PBKDF2-SHA256 with 10000 iter -> outputs some 32-byte hash, e.g., `0x4F8A...`.
- Store in DB: UserId, Salt (in hex or base64), Hash (in hex/base64), and perhaps the iteration count and algo for future flexibility.
- On login attempt, retrieve user record by username, get salt, do same PBKDF2 on provided password, compare hash.
- If using Identity, it does all this for you and even supports multiple formats (if you upgrade from an older weaker format, Identity can mark the user and rehash with better algorithm on next login).

**Key stretching and future**: Over time, as computers get faster, you might increase iterations or move to Argon2 (which is memory-hard). .NET doesn't have Argon2 in the built-in, but there are libraries. Argon2 is winner of a recent Password Hashing Competition and is considered strong. But PBKDF2 is fine when used with high iterations.

### 6.3 Secure Storage of Secrets (Keys, Connection Strings, etc.)

**Problem:** Your app needs secrets (DB connection strings, encryption keys, third-party API keys). Storing them plainly in config files or code is risky (they could leak or be accessible if server is compromised or someone gains read access to the file system).

**Solutions:**

- **Azure Key Vault / AWS Secrets Manager / Hashicorp Vault:** External secret stores. They provide a secure storage and access control (often integrated with environment identity).
  - Azure Key Vault: you can give your app (if running in Azure) a managed identity and then load secrets from Key Vault at startup. E.g., using `builder.Configuration.AddAzureKeyVault(vaultUri, new DefaultAzureCredential());`. Then config keys from the vault appear like normal config. Key Vault also allows storing certificates and encryption keys (with optional HSM backing).
  - AWS Secrets Manager or Parameter Store: similar concept. There's AWS SDK for .NET to retrieve them.
  - These systems also have versioning and sometimes automatic rotation features (like database credentials rotation).
- **Environment Variables:** Better than putting in source code. Many deployment systems allow injecting env vars. .NET config can read env vars easily. The downside is if someone dumps env or logs environment, they could leak (but at least not in code repo).
- **User Secrets (during development):** .NET Core's Secret Manager is great for dev time (it stores secrets in a JSON in your user profile, not in the repo).
- **Encrypted configuration files:** You can encrypt sections of config on Windows using DPAPI with `dotnet user-secrets` or manually. But cross-platform that isn't straightforward. Instead, just use an external vault or environment injection for production.
- **No secrets in client-side code:** If you have an API key for third-party that must be used from client (like Google Maps API key), ensure it’s a public one that is intended to be exposed (and locked down by domain in Google's console). All other keys (like database or internal APIs) should never be in front-end code delivered to users.

- **Rotation:** Plan for how you'd update a secret if needed. For example, DB password change, how to update config without downtime. Some vaults allow multiple versions active for a while or atomic swaps.

**Configuration Example:**

In `appsettings.json`, you might put:

```json
"ConnectionStrings": {
  "MainDB": "Server=tcp:...;Database=Main;User Id=myuser;Password=PlainTextPassword;"
}
```

This is bad to commit. Instead:

- In source control or base config, maybe leave an placeholder or exclude it.
- In production, either:
  - Set environment variable `ConnectionStrings__MainDB` to the actual connection string (the double underscore `__` maps to nested config).
  - Or store in Azure Key Vault the secret "MainDB-ConnectionString", then load it such that `Configuration["ConnectionStrings:MainDB"]` is pulled from vault.

For smaller projects, environment vars or a separate secured config file on the server (with limited access permissions) might be fine. For enterprise, a vault is recommended.

**Encryption of sensitive fields in DB:**

- For certain fields like personal data, consider encrypting them in the database even if the DB is behind secure network. E.g., GDPR sometimes encourages encryption of personal data. If DB or backup is leaked, encrypted fields are safer.
- You can do field encryption at application level (like using AES before saving). But key management again is challenge – keys need to be somewhere.
- Some databases support Transparent Data Encryption (TDE) which encrypts entire DB at rest. This protects against someone stealing the physical DB files, but not against someone who queries the DB with proper access. Field-level encryption is more granular if needed to separate who can see what.
- If you do custom encryption, consider using well-tested libraries or approaches. Mistakes (like reusing IVs or using ECB mode) can undermine security.

### 6.4 Hashing Other Data & Digital Signatures

Beyond passwords:

- You might hash data to generate unique fingerprints (e.g., file hash to detect if file changed). Use SHA-256 or SHA-512 for collision resistance. .NET: `SHA256.Create().ComputeHash(bytes)` gives you the hash.
- If you need to ensure data integrity and also authenticity (i.e., verifying not only it didn't change but that it was produced by you), use HMAC. .NET: `HMACSHA256(key).ComputeHash(bytes)` produces a tag that only someone with the key can produce. This is how JWT signatures work (for JWT with symmetric key).
- Digital signatures with RSA or ECDsa can be used if you need to sign something and later verify (like issuing license tokens or such). .NET has classes like RSA.SignData / VerifyData.

**Example: Creating a secure reset password token:**
Instead of storing a reset token in DB, you could issue a token string that encodes user id and expiry and sign it with HMAC. The app can verify it without DB lookup. (This is similar to JWT idea.)

```csharp
var data = $"{userId}:{DateTimeOffset.UtcNow.AddHours(1).ToUnixTimeSeconds()}";
byte[] dataBytes = Encoding.UTF8.GetBytes(data);
byte[] sig = new HMACSHA256(key).ComputeHash(dataBytes);
string token = Convert.ToBase64String(dataBytes.Concat(sig).ToArray());
```

Then to verify, split the token into data and sig, recompute HMAC, check match and that timestamp not expired, etc. Alternatively, use JWT libraries to issue a token with claims and signing. But caution: rolling your own tokens can lead to mistakes, using a library (System.IdentityModel.Tokens or JWT) ensures proper format and signing.

### 6.5 GDPR, PCI, and Compliance Considerations

If you operate under certain regulations, you might have to implement specific data protection measures:

- **GDPR (EU data protection):** Requires data protection by design – encryption of personal data, ability to delete data (so keep track where you stored it, encrypted or not).
- **PCI-DSS (Payment Card Industry):** Very strict about card data: if storing PAN (card number), must be encrypted with strong encryption, and keys must be well protected (usually in HSM or KMS). Often, businesses choose not to store card data at all and use tokens provided by payment processors, to reduce scope of PCI compliance (outsourcing the storage).
- **HIPAA (Health info):** Also encourages encryption of PHI (protected health info) so that if a breach happens, encrypted data might exempt from breach notification if properly encrypted.

In .NET, nothing stops you from being compliant as long as you follow best practices as above. Sometimes using specialized third-party libraries or services is recommended for specific compliance (like a tokenization service for credit cards, etc.).

### 6.6 Summary

- Use **encryption** for any sensitive data that needs to be retrieved in plaintext later. Use AES (with secure mode and key lengths) and manage keys carefully (in vaults or secure store).
- Use **hashing** (with salt) for passwords so they can’t be reversed.
- Keep **secrets out of code**: use environment or vaults, and limit who/what can read them.
- Leverage .NET Core’s built-in cryptography which is industry-standard and vetted. Avoid writing your own low-level crypto (stick to library functions).
- When in doubt, refer to official guidelines: e.g., OWASP Cryptographic Storage cheat sheet, which echoes many of these points.

**Exercise 6:** _Implement and Break Encryption_ – This two-part exercise will solidify encryption understanding:

1. Write a small function to encrypt a piece of data (like a string message) with AES in CBC mode. Do it incorrectly on purpose (e.g., use a fixed IV or a weak cipher mode like ECB, or maybe no integrity check). Encrypt a message.
2. As an attacker (knowing the method), see if you can exploit the weakness. For instance, if ECB was used, see if patterns emerge (encryption of repetitive data shows pattern). Or if IV is constant, you might detect two identical plaintexts produce same cipher.
3. Then fix the implementation: use a random IV each time (and maybe output IV+ciphertext together), use AES-CBC with HMAC or AES-GCM for authenticity.
4. Decrypt and verify the data successfully with your fixed method. Ensure that if someone tampered with the ciphertext or IV, your decryption code detects it (e.g., HMAC validation fails).

This exercise will show how subtle choices in encryption can matter and reinforce using secure defaults.

---

## Chapter 7: Security Tools and Automation (Static Analysis, Scanning, and Dependency Checking)

A critical part of secure development is using tools to catch security issues early and often. In this chapter, we’ll explore various categories of security tools:

- **Static Application Security Testing (SAST):** analyzing source code or binaries for vulnerabilities (e.g., SonarQube, Roslyn analyzers).
- **Dynamic Application Security Testing (DAST):** running the app and scanning it (e.g., OWASP ZAP).
- **Software Composition Analysis (SCA):** checking dependencies for known vulnerabilities (e.g., OWASP Dependency Check, NuGet audit).
- **Infrastructure/Container Scanning:** (if applicable, scanning Docker images for vulns, etc.)
- **Continuous Integration (CI) integration:** how to include security checks in your pipeline.

By automating these, you can catch issues early in development and also ensure new vulnerabilities don't creep in over time.

### 7.1 Static Code Analysis with Roslyn Analyzers and SonarQube

**Roslyn Analyzers:** .NET has code analysis rules (some built-in, like CA warnings, and others via packages). There are specific security analyzers:

- Microsoft.CodeAnalysis.FxCopAnalyzers (some security rules included).
- Roslyn Security Guard (community analyzers for security, though not sure if it's up-to-date).
- DevSkim (Microsoft's tool, can integrate into VS Code, to spot insecure patterns).
- You can run these during build to get warnings if, say, you use `System.IO.Path.Combine(userInput)` incorrectly or if you call `GC.SuppressFinalize` incorrectly (some memory stuff which can be security relevant).

**SonarQube:** A popular tool that performs static analysis for many languages including C#. It detects code smells, bugs, and security vulnerabilities (like SQL injection, hardcoded credentials). SonarQube has a set of [Security Hotspots and Vulnerabilities rules](https://rules.sonarsource.com/) for C#.

Using SonarQube:

- You can run SonarQube server (or use SonarCloud SaaS) and integrate a Sonar scanner into your build (Maven, Gradle, or standalone Sonar CLI for .NET). Microsoft has SonarQube integration tasks for Azure DevOps.
- Sonar will produce a report; for example, it might flag:
  - “Use of weak cryptographic algorithm” if it sees `MD5.Create()`.
  - “Potential SQL Injection” if it detects string concatenation in SQL queries.
  - “Hardcoded secret” if a string looks like a password or API key.
- These findings can be reviewed and fixed by developers. Sonar can fail the build if quality gate not met (like if new vulnerabilities introduced).

From earlier references: SonarQube finds _bugs, vulnerabilities, code smells_ ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=SonarQube%20SonarQube%20is%20an%20automatic,Image%204)) ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=Add%20a%20new%20Sonar%20Service,in%20the%20SonarQube%20quality%20profiles)). It's a broad tool, not just security but code quality too.

**Setting up Sonar in CI:** Typically:

- In pipeline: build the project, then run sonar scanner with appropriate project key and connect to Sonar server. After analysis, Sonar UI will show issues.

**Limitations of SAST:** Static analysis can produce false positives or miss some context-based issues. But it's great for catching obvious mistakes (like the OWASP Top 10 variant, e.g., missing validation, open redirects, etc., if rules exist for them). It's also good at enforcing best practices consistently.

### 7.2 Dynamic Scanning with OWASP ZAP

**OWASP ZAP (Zed Attack Proxy):** This is a free DAST tool to find vulnerabilities in a running web app. It acts as a proxy to intercept and modify requests, plus has active scanners to attempt attacks (SQL injection payloads, XSS payloads, etc.).

**How to use ZAP:**

- You can use ZAP in GUI mode to explore the app (spider it to discover pages, then run active scan).
- Or in CLI/baseline mode in CI: OWASP provides a Docker image `owasp/zap2docker-stable` that can run a baseline scan and report alerts.
- Example, integrate in pipeline to run `zap-baseline.py -t https://yourapp` to spider and passively scan, and `zap-full-scan.py` for active scanning (which can alter data).
- There's also a ZAP API, and even a ZAP HUD in browser.

**What ZAP can find:**

- XSS (reflected/stored) by injecting scripts in parameters and checking if reflected.
- SQL injection (it will try some payloads and see if error messages or behaviors change). It's not as thorough as manual testing, but can catch basic issues.
- Missing security headers (it flags absence of CSP, X Frame Options, etc.) – as we saw in the DevReady blog, ZAP flagged those ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=X)) ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=ZAP%20description%3A%20X,to%20protect%20against%20%E2%80%98ClickJacking%E2%80%99%20attacks)).
- Directory indexing or known sensitive files (like .git folder accessible, backup files, etc.).
- Insecure cookies (missing HttpOnly/secure flags).
- CORS misconfig (if it finds `Access-Control-Allow-Origin: *` and maybe sensitive responses, etc.).
- Server errors (500s) which might leak info.

We saw earlier an example: ZAP flagged "Cookie Without HttpOnly Flag" and gave description ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Cookie%20No%20HttpOnly%20Flag)) and fix recommendation ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=Fix%3A)). This is exactly how ZAP presents issues (with risk level and some references).

**Using ZAP safely:** Active scanning will attempt attacks, which might create test entries or even drop tables if your app is truly vulnerable to such and ZAP triggers it. It's wise to run it against a test instance with test data. Also, be mindful if you have actions like "delete user" with simple GET, ZAP might call it during crawling (so use anti-CSRF tokens or confirm dialogues in your app for dangerous actions to avoid accidental triggered by scanner).

**Interpreting results:** ZAP may produce false positives too. E.g., it might think a page is vulnerable to XSS if it reflects input, but maybe you had encoding and it didn't notice. You verify manually.
Also, some findings might be low risk or intended (like it might flag "application error disclosure" if your API returns a stack trace on error – which is legit, you should fix that in prod).

**Other DAST:** Alternatives are Burp Suite (popular but not free for full version) or specific scanners for APIs (like APIsec or others). But ZAP is a solid, free choice.

### 7.3 Dependency Scanning and Updating (SCA)

Using components with known vulnerabilities (OWASP A6) is common, so **Software Composition Analysis** tools help. We touched:

- **OWASP Dependency Check:** an open source tool that scans project dependencies (NuGet, NPM, etc.) and compares against known CVE database.
  - It has a CLI or can be integrated via Jenkins/DevOps tasks.
  - It will output a report listing libraries and known issues. For .NET, it looks at packages.config or project file references.
- **dotnet list package --vulnerable:** .NET Core 2.1+ added this command which uses NuGet’s vulnerability database (powered by GitHub advisory DB). Running it will list any packages with known vulns and the severity.
- **NuGet client in Visual Studio:** VS has UI that will show a warning icon on packages that have known vulnerabilities and suggest upgrades.
- **Dependabot/GitHub:** If your code is on GitHub, enable Dependabot alerts – it scans your project files and notifies (and can even PR an update) if a dependency has a security update.
- **WhiteSource (now Mend):** A commercial SCA tool (free tier available for small projects or limited usage). The blog mentioned WhiteSource was used in a pipeline alongside Sonar ([Injecting security in CI/CD pipelines with SonarQube, WhiteSource, OWASP DC and OWASP ZAP – Azure DevOps – Ignite the code within](https://myownpicloud.wordpress.com/2020/08/01/injecting-security-in-ci-cd-pipelines-with-sonarqube-white-source-owasp-dc-and-owasp-zap-azure-devops/#:~:text=WhiteSource%20WhiteSource%20is%20used%20to,Image%206)). It scans and gives a report with suggestions to upgrade.

**Integrating SCA:**

- Ideally, your build should fail if a high severity vulnerability is detected in a dependency (unless you have a risk acceptance and suppress it).
- So you might run something like `dependency-check.bat` in CI and configure threshold.
- Or rely on GitHub alerts and make sure to address them before merging code.

**Example:** If you are referencing Newtonsoft.Json 11.x and a vulnerability is discovered in 11.x that is fixed in 12.x, these tools would alert you. Your action: test and update to 12.x. Or if can’t immediately, perhaps mitigate and note it.

Remember to check not only direct dependencies but also transitive (Dependency Check and others do that). NuGet’s own check covers transitives that have data in their advisory DB.

### 7.4 Other Security Testing (Penetration Testing & Fuzzing)

**Penetration Testing:** At some stage, a human or specialized team should test the app. The tools we discussed help prepare for that by catching low-hanging fruit. When pen testers come:

- They will try creative input combinations beyond what automated scanners do.
- They might test business logic flaws (something SAST/DAST can't easily find, like "can a normal user approve transactions by hitting an unlinked endpoint").
- They might review architecture (looking for how data flows, any obvious weak points).
- Ensure you provide them necessary access or accounts to test thoroughly.

From a developer perspective, it's good to do **self-pentesting** or peer review: e.g., try to break your own app like an attacker would:

- Use a proxy (ZAP or Burp) to modify requests (e.g., change user IDs in JSON payloads).
- See if you can bypass client-side validation by calling APIs directly.
- Try some known exploits (XSS payload, SQLi payload) even if you believe it's safe, just to verify nothing unexpected happens.
- Check the logs or responses for any info leak.

**Automated Security Testing in CI:** Beyond SAST/DAST, you can write your own integration tests for security aspects:

- E.g., write a test that ensures all your controllers have `[Authorize]` (using reflection to get controllers and checking attributes).
- Write an integration test that attempts an XSS: call an endpoint with some script tag and verify the response is encoded (perhaps by checking the response text does not contain `<script>`).
- If you have a regex path for input validation, fuzz it with a library (there are fuzzing libraries or just generate a bunch of random bad inputs to ensure your validation doesn't break or hang on certain patterns – ReDoS (regex denial of service) is something to watch out for with unbounded regex on user input).

**Continuous Monitoring:** If your application is live, consider using a Web Application Firewall (WAF) or intrusion detection:

- Azure has Application Gateway WAF that can block common attack patterns (based on rules like ModSecurity OWASP ruleset). AWS has AWS WAF. These are not foolproof but add a layer.
- You might get alerts if multiple attacks detected by WAF, etc., which can prompt deeper investigation.

### 7.5 DevSecOps Culture

Encourage a culture where developers, ops, and security work together:

- Use the tools but also educate team on why an issue is an issue. E.g., Sonar flags "Refactor this code to not log sensitive information" – devs should understand logging secrets is bad and not just suppress the warning.
- Keep dependencies lean to reduce attack surface.
- Ensure pipelines themselves are secured (a compromised CI could inject malware into your binaries).
- Use container image scanning if you deploy with Docker (e.g., Aqua Trivy or Clare can scan images for known vulns in OS packages).
- Use Infrastructure as Code scanning if using Terraform/ARM etc. (to catch misconfigs like open security groups).

**Tool Recap:**

- **SonarQube** – static code analysis, find security hotspots.
- **Visual Studio analyzers** – immediate feedback in IDE for common mistakes.
- **OWASP ZAP** – active scanning of running app.
- **Dependency Check/Dependabot** – alert on vulnerable libraries.
- **Sonar/WhiteSource** in CI – break build on known critical vulnerabilities.
- **Zap in CI** – possibly run baseline scan in a test stage (some teams do nightly DAST scans rather than every build due to time).
- **Custom scripts** – e.g., a script to ensure no "TODO: remove before prod" or "Hardcoded: password" strings remain.

**Exercise 7:** _Pipeline Security Automation_ – If you have access to a CI/CD environment (like GitHub Actions, Azure DevOps, or Jenkins), try to incorporate one of these tools:

- Add a step to run `dotnet list package --vulnerable` and fail if output contains "vulnerable".
- Or integrate OWASP Dependency Check (there's a GitHub Action for it).
- Or set up SonarCloud (free for open source) analysis on your repo.
- Intentionally introduce a vulnerable package (perhaps install an old version with a known flaw) and see if the pipeline catches it.
- Also, if possible, run OWASP ZAP in a pipeline against a deployed test instance and generate a report artifact.

This will give you experience in automating security tests, which is a key part of DevSecOps.

---

## Chapter 8: Penetration Testing and Automated Security Testing Strategies

In previous chapters, we've built up a fortress of defenses in our .NET application. But how do we verify that fortress holds against attack? This chapter discusses how to approach **penetration testing** – simulating attacks on your application – and how to incorporate security testing into your development lifecycle in an automated way.

### 8.1 Planning a Penetration Test

Whether you're doing it in-house or hiring external professionals, a pen test typically follows a structure:

1. **Reconnaissance:** Gather as much information as possible about the target application. This could include open ports, subdomains, API endpoints, technologies used (.NET Core version, etc.), and even leaked credentials (perhaps search public code repositories for mentions of your domain).
   - For a web app, recon can be as simple as browsing every page (including error pages) to see what info is revealed.
   - Use tools like Nmap for port scanning (to see if database or other ports accidentally open), and Google dorking ("site:yourdomain.com" searches for publicly indexed pages or sensitive info).
2. **Threat Modeling:** Based on recon, identify potential threat vectors. E.g., if the app uses JWT auth, threats: stolen token reuse, JWT forgery if weak signing key, etc. If it's e-commerce: threats like price manipulation, etc.
3. **Exploitation Attempts:** Systematically attempt exploits:
   - Input-based: SQLi, XSS, command injection, etc. (Often using automated scanners as part of this).
   - Authentication bypass: try default creds, weak creds, login response analysis (like user enumeration: does error say "wrong password" vs "user not found").
   - Access control: as we did, try accessing URLs or functions as the wrong user.
   - Business logic: e.g., apply a coupon multiple times, or change an order ID in a form submission to someone else's, etc.
   - API-specific: If there's an API, testing each endpoint with wrong methods or missing parameters, etc.
   - Client-side: Look at JavaScript for clues (maybe hidden admin functionality).
   - Also test the resilience: maybe a bit of load to see if any weird behavior (like sending a very large payload to see if it crashes - can indicate DoS or overflow).
4. **Post-Exploitation and Impact Analysis:** If an exploit is successful, see what you can do next. E.g., XSS -> can you steal an admin cookie? SQL injection -> can you dump user table? It's important to understand impact to prioritize fixes.
5. **Reporting:** Document vulnerabilities found, steps to reproduce, and recommendations to fix (which often align with what we've covered as mitigations).

As a developer prepping for pen test, it's good to do a mini version of these steps yourself (or with your team). There's also the OWASP Web Security Testing Guide which provides a comprehensive set of test cases.

### 8.2 Automated Security Testing in CI/CD

We've touched on automation in the previous chapter. To integrate security into CI/CD:

- Include linting/static analysis as part of build (fail build on high severity issues).
- Have nightly or weekly runs for heavier scans (like a full ZAP scan or dependency audit) if they are too slow for each build.
- If using containerization, use something like Trivy in pipeline to scan your Docker image for vulnerabilities (base OS packages, etc.).
- Set up QA environment to run DAST (some orgs have a dedicated “security test” stage in pipeline after deploy to QA).
- Use Smoke tests for security: e.g., after deployment, run a quick script that checks that the security headers are present, that HTTP is redirecting to HTTPS, etc. These can catch config mistakes (like someone deployed without HSTS or with debugging enabled).
- If you fix a security bug, write a regression test for it. E.g., you had an XSS in a feedback form, write an automated test that posts a script and verifies the output is encoded now (ensuring the fix stays in place).

### 8.3 Red Team vs Blue Team and Dev Involvement

If your company has a security team (blue team) and a testing team (red team), as a dev you should collaborate:

- Blue team might want you to add extra logging (like log all 5xx errors with details) to help detect attacks.
- Red team might share common findings so devs can proactively fix in future (like "hey, many of our apps forget to validate JWT audience, you should check that").
- Sometimes running **capture the flag** exercises or using deliberately vulnerable apps (like OWASP Juice Shop) internally can educate devs.

### 8.4 Real-time Protection and Monitoring

Pen testing is periodic, but also consider **real-time protections:**

- WAF: If a pen tester easily exploits something, a WAF could at least alert or block obvious patterns until fix deployed.
- Runtime Application Self-Protection (RASP): Tools/libraries that instrument the app to detect attacks in real time (for example, if someone tries to drop tables via input, it could detect that pattern in SQL query at runtime and stop it). This is more advanced and not widely used in .NET yet, but concepts exist.

- Monitoring: For example, set up alerts for:
  - Multiple failed logins (could be brute force).
  - Sudden spike in 500 errors (someone fuzzing or found a path causing errors).
  - New user account creation when it’s not expected (maybe an attacker made an admin account).

This blends into operational security, but developers can expose metrics or events to make this possible (like sending an event when an admin function is executed, which normally shouldn't happen often).

### 8.5 Case Study: Lessons from Past Incidents

We included case studies in Chapter 9, but tying to testing:

- Many breaches (like the ones we mention: ResumeLooters SQLi ([Millions of User Records Stolen From 65 Websites via SQL Injection ...](https://www.securityweek.com/millions-of-user-records-stolen-from-65-websites-via-sql-injection-attacks/#:~:text=,SQL%20injection%20and%20XSS%20attacks)), Panera IDOR ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=For%20example%2C%20some%20of%20the,points%2C%20including%20by%20phone%20number)), Capital One SSRF ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=The%20attacker%20gained%20access%20to,the%20data%20contained%20in%20them))) could have been found earlier with proper testing.
- E.g., an automated scanner or even a bug bounty researcher could find an open URL enumerating IDs (Panera case).
- SSRF might have been caught if someone internally thought to test the file upload URL with internal addresses (like a security test case).
- After hearing of these incidents, incorporate similar tests in your context. For example, after Capital One, many companies tested their apps for SSRF by trying to hit internal resources from any URL fetch functionality.

### 8.6 Tools Recap and Additional

- **Fuzzers:** Tools that automatically feed random data to find crashes or unexpected behavior. For .NET, there's not a built-in fuzzer, but you could use something like AFL (American Fuzzy Lop) on a native component, or write quick fuzz scripts for your input fields. Microsoft is working on Project OneFuzz (for Azure, mainly for native code though). Fuzzing might find things like RegexDenialOfService (if a regex catastrophically backtracks on certain input).
- **SAST Tools beyond Sonar:** Fortify, Veracode, Checkmarx are enterprise SAST tools. They might have more advanced data flow analysis. If in a corporate setting, you might use one of those via CI (upload code to their cloud or run their scanner).
- **DAST beyond ZAP:** Burp Suite Pro has more advanced scanning and fuzzing capabilities. Also tools like Arachni (for web) or Nikto (for server config).
- **SCA beyond dependency check:** We've mentioned dependency bots, also Snyk is a popular dev-friendly SCA (and does some static analysis too for code vulnerabilities).

**Remember**: No tool catches everything. Having multiple tools (defense in depth in testing too) helps. But also human review and testing is invaluable for logic issues that tools can't comprehend.

**Exercise 8:** _Attacker Mindset Drill_ – Pick one functionality in your application (say, the profile update feature). List all the ways it could be abused:

- What if someone changes the user ID in the request?
- What if they input a script in each field?
- What if they spam the endpoint 1000 times a minute?
- What if they try an extremely long value?
- What if they call it without being logged in?
- Can they call a different HTTP method on the same URL (maybe a GET that should be a POST)?

Try each of these scenarios (using a tool like Postman or ZAP to manipulate requests beyond what the UI allows). Document what happens. If any succeed in doing something unintended (e.g., you find a bug or a potential vulnerability), note it and then fix it. This exercise helps shift into an attacker's perspective and often reveals corner cases or bugs that might not be obvious during normal development.

---

## Chapter 9: Real-World Case Studies and Lessons Learned

Despite all precautions, history shows that even large organizations have suffered from security lapses. In this chapter, we will examine a few real-world security failures relevant to web applications and extract lessons that we can apply to our .NET Core development practices. Understanding how breaches happened helps ensure we don't repeat the same mistakes.

### 9.1 Case Study: The ResumeLooters Breach (2023) – SQL Injection & XSS

**What happened:** In 2023, a hacker group dubbed "ResumeLooters" targeted around 65 websites (mostly recruitment and retail sites) and stole millions of user records ([Millions of User Records Stolen From 65 Websites via SQL Injection ...](https://www.securityweek.com/millions-of-user-records-stolen-from-65-websites-via-sql-injection-attacks/#:~:text=,SQL%20injection%20and%20XSS%20attacks)) ([Millions of User Records Stolen From 65 Websites via SQL Injection ...](https://reg4tech.com/millions-of-user-records-stolen-from-65-websites-via-sql-injection-attacks/#:~:text=Millions%20of%20User%20Records%20Stolen,Millions%20of%20User%20Records)). They did this primarily through **SQL Injection and Cross-Site Scripting attacks**. They were able to extract data like names, emails, hashed passwords, and in some cases, resumes or other personal info. Some sites were also defaced or had malicious scripts injected (via XSS stored in database).

**How it happened:** Likely, these websites had input fields (perhaps job search or contact forms) vulnerable to SQL injection, which allowed the attackers to dump entire databases. Some sites might have allowed resume uploads or profile descriptions where XSS was possible, which the attackers could exploit to later deliver malware or phishing (via stored XSS on pages that recruiters would view).

**Lessons:**

- _SQL Injection is still a threat._ It consistently ranks in OWASP top risks ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=It%27s%20curious%20that%20many%20people,10%20OWASP%20security%20threats%20report)) and is not merely theoretical. As seen, a successful SQLi can lead to a complete compromise of user data. Our defense must be thorough: use parameterized queries everywhere and ORMs that are safe by default. We must never get complacent and think "our framework handles it" – validate that no dynamic SQL sneaks in. Code reviews should flag any raw SQL string concatenation.
- _XSS can escalate impact._ In ResumeLooters, after stealing data, they might have also left XSS payloads to further exploit anyone viewing that data. This reminds us to treat any user-supplied HTML or text as unsafe unless sanitized/encoded. Even in administrative backends, one user's data (if malicious) could be viewed by an admin – and if not properly encoded, execute in the admin's browser (who likely has powerful privileges, making that XSS potentially very damaging).
- _Regular testing:_ These attacks often hit multiple sites that likely used common software or had similar vulnerabilities. If those sites had undergone a security audit or used tools like ZAP actively, they might have caught these flaws before deployment.
- _Defense in depth:_ Even if one layer fails, others can mitigate damage. For example, had these databases stored passwords with strong hashes, the breach would expose hashes, not plaintext. Or if personal info was encrypted, the attackers would get ciphertext (unless they also got keys). Ensuring stolen data is less immediately useful adds a layer of protection (e.g., in one site breach, encrypted SSNs meant the attackers couldn't directly abuse them).

From a .NET perspective, applying our earlier recommendations (Chapter 5) on injection and XSS would directly prevent the vulnerabilities exploited by ResumeLooters.

### 9.2 Case Study: Panera Bread Data Leak (2018) – Broken Access Control

**What happened:** Panera Bread's website leaked millions of customer records (names, emails, addresses, last four of credit card, etc.) for about 8 months ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=Panerabread,earlier%20today%2C%20KrebsOnSecurity%20has%20learned)) ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=184%20Comments)). The data was available in plain text via an API endpoint on their site that required a customer ID. The customer IDs were sequential integers. An unauthenticated (or minimally authenticated) request to something like:

```
https://panerabread.com/api/GetCustomer?ID=123456
```

would return that customer's info. By incrementing the ID, an attacker could scrape the entire database ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=For%20example%2C%20some%20of%20the,points%2C%20including%20by%20phone%20number)) ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=%E2%80%9CPanera%20Bread%20uses%20sequential%20integers,the%20entire%20database%2C%E2%80%9D%20Houlihan%20said)). A security researcher discovered this and reported it, but initially Panera staff dismissed it as a likely scam and didn't fix promptly ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=security%20researcher%20Dylan%20Houlihan%2C%20who,back%20on%20August%202%2C%202017)) ([Panerabread.com Leaks Millions of Customer Records – Krebs on Security](https://krebsonsecurity.com/2018/04/panerabread-com-leaks-millions-of-customer-records/#:~:text=Panera%20was%20alerted%20about%20the,was%20fixing%20the%20problem%20then)).

**How it happened:** This is a classic **Insecure Direct Object Reference (IDOR)** – a type of Broken Access Control. The developers exposed an internal object (customer record) via an identifier that was easily guessable and did not enforce that the requesting user should only get their own record. Possibly, they intended it to be called after login and assumed no one would tinker with the IDs. But since it wasn’t locked down, any ID worked from anywhere.

**Lessons:**

- _Never trust client-side enforcement._ If they assumed "only the mobile app calls this and it will only call with the logged-in user's ID," that assumption is flawed. Always enforce on the server side: require authentication and check that the ID requested belongs to the authenticated user (or the user has rights to view it).
- _Use non-sequential IDs or GUIDs for references accessible by users._ If the API had used a random UUID for each customer (and that UUID is not guessable), it mitigates bulk enumeration. However, this is secondary to proper access control, because even a UUID, if not access-controlled, could be leaked or guessed by other means. But sequential integers are an invitation to scrape.
- _Heed security reports._ The fact that it remained exploitable for 8 months is a process failure. When the researcher reported it, they were initially brushed off. Organizations should have a clear process to handle vulnerability reports (bug bounty or at least a contact) and take them seriously. As a developer, if such a report comes in for your app, verify it ASAP rather than assume it's false.
- _Monitoring and rate-limiting:_ If Panera had monitoring, they might have noticed someone enumerating IDs (lots of requests in sequence). Having a rate limit (say, 100 requests per minute per IP) ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=options,QueueLimit%20%3D%202%3B)) ([Rate limiting middleware in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-9.0#:~:text=,12%20to%20OldestFirst)) and alerting on unusual access patterns could have detected or slowed the scraping. This doesn’t fix the vulnerability, but could mitigate mass exploitation.
- _Privacy by design:_ The leaked data included partial card numbers and PII. Under regulations like GDPR, such a leak is serious. The concept of _data minimization_ asks: did they need to expose that data via API at all? Perhaps not. Evaluate what data is exposed by your endpoints and consider filtering out or masking sensitive fields unless absolutely necessary.

In .NET terms, preventing this is straightforward: use `[Authorize]` on such an API and inside, use the user identity to fetch their data (ignore the provided ID or verify it matches). Or if admins can fetch arbitrary user by ID, ensure that endpoint is admin-only and still likely not expose it via client-side easily.

### 9.3 Case Study: Capital One Breach (2019) – Server-Side Request Forgery (SSRF) in the Cloud

**What happened:** A notable cloud security breach. Capital One had a misconfigured web application firewall (WAF) on AWS. An attacker exploited a **Server-Side Request Forgery (SSRF)** vulnerability in an application behind the WAF to trick it into making requests to AWS's internal metadata service (http://169.254.169.254) ([Capital One hack highlights SSRF concerns for AWS - TechTarget](https://www.techtarget.com/searchsecurity/news/252467901/Capital-One-hack-highlights-SSRF-concerns-for-AWS#:~:text=TechTarget%20www,access%20the%20AWS%20metadata)) ([Capital One incident (March 2019) - Cloud Threat Landscape](https://threats.wiz.io/all-incidents/capital-one-breach#:~:text=Capital%20One%20incident%20,exfiltrated%20from%20their%20AWS%20environment)). The metadata service returned temporary AWS credentials (IAM role credentials) for the web application’s server. The attacker then used those credentials to list and download data from Amazon S3 buckets (which contained ~100 million customer records) ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=The%20attacker%20gained%20access%20to,the%20data%20contained%20in%20them)) ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=metadata%20service%20via%20a%20SSRF,the%20data%20contained%20in%20them)).

**How it happened:** The compromised application accepted a parameter (perhaps a URL or some identifier) and made a server-side HTTP request without properly validating it. The WAF was supposed to block such attempts, but either it was misconfigured or the attacker found a way to bypass it. By exploiting SSRF, the attacker was able to access a service (metadata) that should have been off-limits to external users.

**Lessons:**

- _Validate outbound requests:_ If your app fetches URLs or resources given by user input, restrict them. In Capital One's case, they likely had an endpoint like "/export?url=<someurl>" which was intended to fetch an external resource. The fix would be to ensure the `url` parameter cannot point to internal IPs or hostnames. E.g., do a DNS lookup and block private ranges ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=when%20the%20infrastructure%20being%20targeted,explain%20this%20in%20more%20detail)) ([An SSRF, privileged AWS keys and the Capital One breach | by Riyaz Walikar | Appsecco](https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af#:~:text=When%20a%20web%20application%20hosted,itself%2C%20called%20the%20Metadata%20endpoint)).
- _Use IAM roles with least privilege:_ The AWS IAM role that the attacker obtained had broad access to S3 (including data they shouldn't have been able to access). Following least privilege, that web app's role should ideally only access the specific bucket/key it needed, not all data. In .NET on AWS, if using AWS SDK, ensure the IAM user/role used by the app has scoped permissions.
- _Metadata service protection:_ After this incident, AWS introduced IMDSv2 (Instance Metadata Service v2) which requires a session token, making such SSRF attacks harder ([AWS Shared Responsibility Model: Capital One Breach Case Study](https://www.appsecengineer.com/blog/aws-shared-responsibility-model-capital-one-breach-case-study#:~:text=Study%20www,The%20new%20service%20is)) ([AWS Shared Responsibility Model: Capital One Breach Case Study](https://www.appsecengineer.com/blog/aws-shared-responsibility-model-capital-one-breach-case-study#:~:text=To%20decrease%20the%20danger%20of,The%20new%20service%20is)). For Azure, there's a similar concept (Managed Identity endpoint). As developers, if we rely on these metadata, using the latest secure version is important. Also, one can configure network rules to block 169.254.169.254 except from trusted system processes.
- _WAF is not a silver bullet:_ Capital One had a WAF (ModSecurity) but it didn't prevent this. WAFs can help but cannot be solely relied on. Application code should not assume "the WAF will stop malicious input." We should code as if no WAF is there, implementing proper validation and authentication on all requests.
- _Logging and Alerting in Cloud:_ The attacker left traces (they posted the stolen data on GitHub gist which is how they were eventually caught). But internally, AWS CloudTrail logs showed unusual S3 access. Ensure that your cloud environment logging is enabled and that alarms are set for suspicious behavior (like large data exfiltration, or access using a role that normally is only used internally being used to list all buckets).

For a .NET developer, SSRF may not be a top-of-mind vulnerability, but this case shows it can be critical. If our .NET app calls `HttpClient.GetAsync(userProvidedUrl)`, we need to vet that URL. That could be as simple as checking `new Uri(url).Host` against an allowlist. Or disallow IP literals entirely if not needed.

### 9.4 Case Study: LinkedIn Password Leak (2012) – Cryptographic Failures

**What happened:** In 2012, LinkedIn was hacked and 6.5 million user password hashes were leaked (later it turned out much more were taken). The hashes were stored as unsalted SHA-1 ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=However%2C%20as%20more%20and%20more,use%20these%20for%20password%20hashing)) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=past%20became%20insecure,use%20these%20for%20password%20hashing)). SHA-1 is a fast hashing algorithm and without unique salts, many passwords were quickly cracked using rainbow tables and brute force.

**How it happened:** Attackers likely exploited some web vulnerability or gained access to LinkedIn's systems (exact initial vector isn't public), then dumped the user credential database. The main issue was not that the breach happened, but that the password storage was weak, making the breach much worse.

**Lessons:**

- _Use strong hashing for passwords:_ This incident (along with others like Adobe, RockYou, etc.) solidified that unsalted hashes (or encrypted passwords) are insufficient. We should use algorithms specifically designed for password hashing (e.g., PBKDF2, BCrypt, Argon2) with salt and a work factor that makes brute forcing impractical ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=,Argon2)) ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=PBKDF2%C2%A0is%20a%20popular%20key,force%20by%20adding%20extra%20complexity)).
- _Hash and salt ensures one user's password hash doesn't help crack another's._ LinkedIn didn't use salts, so identical passwords had identical hashes, allowing attackers to crack one and then know all users with that password.
- _Update aging algorithms:_ Even though 2012, SHA-1 was known to be not ideal for password storage (because it's fast). Today, SHA-1 is considered broken for collisions, but even before collision attacks, its use in password hashing was discouraged. The takeaway: if you're using an algorithm that's not the current best practice, plan to upgrade. For instance, if a .NET app from 2010 used SHA1 with salt, you should migrate users to PBKDF2 or BCrypt by re-hashing on login (ASP.NET Identity does this by having a Version in the password hash and upgrading on login).
- _Encryption vs Hashing:_ Some companies in the past stored passwords encrypted so they could email them in plaintext to users. This is a bad practice; hashing is preferred since you rarely need the actual password (just verification). If you think you need reversible encryption for a "password", it's likely not a user password but some other credential that might better be handled via a different workflow (like API keys).
- _Stolen hash usage:_ Even if hashes are not immediately cracked, there's risk. Attackers might use them in "Pass-the-hash" style attacks if the system allows that (not typical in web, but in some network auth scenarios). Or they could use hash for credential stuffing on other sites (some people reuse hash as a password elsewhere, unlikely, but plaintext password reuse is common, which is why cracking is done).

In .NET, thanks to ASP.NET Identity, we have a good default for password storage (PBKDF2 with 10000 iterations and salt). The key is to use those libraries and not invent our own weaker scheme. And if we are using older membership providers (like the old Membership in ASP.NET which used salted SHA1 by default), migrate to a stronger scheme.

### 9.5 Case Study: Equifax Breach (2017) – Using Vulnerable Components

**What happened:** Equifax, a major credit bureau, had a massive breach of ~147 million people's personal data. The root cause was a vulnerability in the Apache Struts 2 framework used in one of Equifax's web applications ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=It%27s%20curious%20that%20many%20people,10%20OWASP%20security%20threats%20report)) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=consistently%20ranked%20in%20the%20top,10%20OWASP%20security%20threats%20report)). The Apache Struts vulnerability (CVE-2017-5638) was a remote code execution bug via a malformed content-type header. Equifax had not updated the component even though a patch was available for months, and attackers exploited it to get into their systems and exfiltrate data.

**How it happened:** Equifax’s web app was using an out-of-date version of Struts with a known critical vuln. Attackers likely scanned for this known hole, found Equifax’s app, and used the exploit payload to execute commands on the server, thereby opening a backdoor or extracting data.

**Lessons:**

- _Keep dependencies updated:_ This is the poster child for "Using Components with Known Vulnerabilities". Equifax could have prevented this simply by updating the Struts library in a timely manner. In .NET, that means regularly updating NuGet packages (especially when security advisories come out). It also means staying on supported versions of .NET.
- _Inventory and patch management:_ Large organizations may have hundreds of apps; it's crucial to know which apps use what frameworks and have a process to roll out patches when a CVE is announced. Tools like dependabot, Snyk, or manual monitoring of Microsoft/OWASP feeds help. For example, if tomorrow a vuln in ASP.NET Core is found, apply the Microsoft patch or upgrade as soon as possible.
- _WAF or virtual patching:_ In some cases, a WAF could mitigate certain known attacks if you cannot patch immediately. After Struts vuln was announced, some WAF vendors provided rules to detect that exploit in traffic. Equifax’s WAF (if any) either wasn't properly configured or didn't catch it. So, while not reliable long-term, WAFs can provide a buffer.
- _Broader approach:_ This was a Java case, but .NET is not immune to similar issues. E.g., consider the 2019 deserialization vuln in JSON.NET if TypeNameHandling was misused, or a vuln in an image processing library. Or a vulnerability in the .NET Core runtime or Kestrel. We must apply security updates to runtime and libraries. Using managed services or cloud can shift some of this (e.g., Azure App Service automatically updates the underlying OS), but your app dependencies are your responsibility.
- _Post-exploit detection:_ Equifax didn't notice for a while. Regular scans (internal or external) could have found that their app was still vulnerable after patches released. Attackers often reverse-engineer patches, then exploit organizations that lag. Equifax was in that laggard group.

### 9.6 Synthesis of Lessons Across Cases

Let's synthesize major takeaways:

- **Input Validation & Encoding are non-negotiable:** SQLi and XSS (ResumeLooters) show catastrophic results if you don't properly handle input and output. Always validate and encode user data.
- **Access Control must be enforced server-side:** IDOR (Panera) demonstrates how oversight in auth can leak millions of records. Always check permissions on every request that accesses sensitive data.
- **Secure by Default Config:** Many issues (Panera, LinkedIn) could be mitigated by using secure defaults (random IDs or GUIDs for references, strong hash algorithms for passwords, etc.). Use frameworks (like ASP.NET Identity) that give secure defaults.
- **Defense in Depth:** In each case, think of a second layer that could have reduced impact. E.g., Panera if they encrypted sensitive fields in DB, at least addresses wouldn't be plain text. Equifax, if the database had been encrypted or segmented, maybe attackers would have harder time after RCE. ResumeLooters, if rate limiting on search fields, maybe they'd steal data slower or partial.
- **Monitoring and Response:** Several cases involved breaches going undetected (Panera 8 months, LinkedIn only realized after hashes on hacker forums, Equifax ~2 months to detect). Monitoring could have caught unusual activity. Also, having an incident response plan means once a vuln is known (Struts), you immediately respond (patch systems, look for signs of compromise).
- **Use of Tools:** Many of these could be caught by scanners:

  - A ZAP scan would likely catch the Panera vulnerability (as an "insecure object reference" or at least an excessive data exposure when spidering user accounts).
  - Dependency Check would have alerted on the Struts CVE.
  - A password audit tool would flag unsalted SHA1 in LinkedIn.
  - None of these remove the need for human diligence, but if your process includes these scans, you greatly reduce risk.

- **Security Culture:** Sometimes the knowledge of a vuln was present but not acted upon (Equifax had internal emails about patching Struts but didn't complete it in time; Panera had a researcher report and they ignored). A culture that prioritizes security issues as much as functional bugs is crucial. When a security concern arises, treat it with urgency.

### 9.7 How We Apply These Lessons to .NET Core Dev

Throughout our guide, we've actually addressed each of these:

- Parameterized queries and XSS prevention (addresses ResumeLooters tactics).
- Strict auth and claims checks (addresses Panera).
- SSRF validations, least-privileged cloud roles (addresses Capital One).
- Strong cryptography practices (addresses LinkedIn).
- Dependency scanning and timely updates (addresses Equifax).

By studying failures, we reinforce why each section of this guide matters. They are not hypothetical:

- The OWASP Top 10 categories are mapped to real incidents causing real damage.
- Our secure coding guidelines map to preventing those incidents.

**Exercise 9:** _Research a Breach_ – Choose a security incident not covered here, perhaps:

- Adobe 2013 breach (encrypted passwords but with hints stored plainly – leads to lesson on not storing password hints or using encryption where hashing should be).
- MySpace or RockYou breaches (plain text passwords – obvious lesson).
- TalkTalk 2015 (a UK ISP hack via SQLi in a legacy page).
- Any recent one affecting cloud (like a misconfigured storage leading to data exposure).
  Read about it and write down:
- What was the vulnerability?
- How could it have been prevented?
- Does our .NET app have similar functionality or risk? How do we mitigate it?

This helps you actively connect general practices to specific outcomes, making the security considerations less abstract.

---

## Chapter 10: Conclusion and Next Steps

We have journeyed through the landscape of secure .NET Core application development, covering everything from the fundamentals of the OWASP Top 10 to advanced topics like OAuth2 implementation and case studies of major breaches. By now, it should be evident that building a secure application is not a one-time task, but an ongoing process that spans design, coding, testing, and maintenance.

**Key Takeaways:**

- **Security is everyone’s responsibility:** As an advanced developer, you set the tone for security in your team. By following best practices (input validation, proper authentication, etc.), you not only secure your code but also set examples for others.
- **Use the framework features and libraries:** ASP.NET Core provides many security features out-of-the-box (Identity, Anti-forgery, Data Protection). Use them rather than reinventing wheels. Leverage community libraries (but keep them updated).
- **Think like an attacker:** Regularly step back and try to abuse your own application. This mindset helps reveal weaknesses in logic that automated tools might miss.
- **Automate where possible:** CI/CD integration of security tools will consistently catch issues that might slip through manual reviews. Automation is your baseline; manual pen-testing is your net for more complex flaws.
- **Stay informed:** The threat landscape evolves. New vulnerabilities (like the mentioned Struts or even something in .NET) emerge. Subscribe to security advisories (Microsoft Security Bulletins, OWASP news, etc.). Continuously educate yourself and your team. What is secure today might not be tomorrow’s standard.
- **Defense in Depth:** No single control is foolproof. Always imagine: "What if this layer fails?" and have another layer. For instance, if auth fails, ensure sensitive operations still require an additional check or cannot be performed too freely (rate limiting, auditing). If an SQL injection slips in, ensure the DB user has minimal rights, etc.
- **Secure design and threat modeling:** Before writing code, think about potential abuses of a feature. During design of a new module, perform a mini threat model: identify assets (sensitive data), entry points, threats, and mitigations. This way, you bake security in from the start, rather than patching later.
- **Performance vs Security:** There is often a balance (e.g., hashing passwords with more iterations adds server load). As advanced developers, find the sweet spot where the app remains performant but not at the cost of security. Usually, security measures have negligible impact on modern hardware for typical loads (like parameterized queries or hashing), and the cost of not doing them is far greater.
- **User Education:** Sometimes security issues involve the user (phishing, weak passwords). While largely out of scope for application code, consider adding user-facing security features: password strength meters, suspicious login alerts, etc., to help users protect themselves.
- **Incident Response:** Despite best efforts, incidents may occur. Have a plan: logging (Chapter 5 and 8) ensures you have data. Also, know how to invalidate sessions or rotate keys quickly if needed. In .NET, for example, if a breach of cookies is suspected, one can change the Data Protection keys so all current sessions become invalid (forcing re-authentication).

**Next Steps:**

- Apply what you've learned to your current projects. Maybe start with a security review sprint: run the tools, fix issues, improve configurations.
- Incorporate security requirements into your definition of done. A user story isn't done if it introduces an OWASP Top 10 vulnerability.
- Keep this guide as a reference. Each chapter stands as a checklist for a particular area (Auth, API hardening, etc.). Use the checklists and exercises with your team perhaps in security training sessions.
- Dive deeper into topics of interest:
  - If OAuth2 and OIDC are crucial for your work, delve into the official IdentityServer docs or OAuth RFCs.
  - If you're deploying on Azure/AWS, study their security best practices (Managed Identity, Key Vault, etc.) to utilize platform features.
  - Follow OWASP projects like the Cheat Sheet Series for specific technologies (.NET, JWT, etc.) for more nuanced advice ([why CSRF is removed from OWASP top 10, how to prevent CSRF on ...](https://stackoverflow.com/questions/48373904/why-csrf-is-removed-from-owasp-top-10-how-to-prevent-csrf-on-asp-net-mvc#:~:text=why%20CSRF%20is%20removed%20from,and%20some%20form%20of%20protections)).
  - Explore new .NET security features (for example, .NET 7/8 might have introduced further improvements like built-in JWT authentication in minimal APIs, etc., and .NET 6 introduced default anti-CSRF for SPA templates using cookies and SameSite).

Finally, consider the human aspect: encourage secure coding workshops, perform peer code reviews focusing on security, and cultivate a culture where reporting a potential security bug is welcomed, not shunned.

By combining knowledge (from guides like this), tools, and a proactive mindset, you can significantly reduce the risk of vulnerabilities in your .NET Core applications. Security is a journey, but every step you take strengthens the shield around your application and users.

**Appendices** (see below) provide quick reference sheets and answers to the chapter exercises, which you can use to test your understanding or to conduct training sessions.

---

## Appendices

### Appendix A: OWASP Top 10 Cheat Sheet

A quick reference mapping OWASP Top 10 (2021) to defenses:

- **A1: Broken Access Control:** Use proper `[Authorize]` attributes; implement server-side permission checks; avoid exposing internal IDs; use policy-based auth for fine-grain control; test all endpoints with an unprivileged account.
- **A2: Cryptographic Failures:** Always encrypt sensitive data in transit (TLS) and at rest if applicable; do not store passwords or keys in plaintext; use strong algorithms (AES, RSA, SHA-256 or better); rotate keys periodically.
- **A3: Injection:** Use parameterized queries (SQL, NoSQL, LDAP, OS commands via libs); avoid constructing queries/commands with string concatenation; sanitize inputs if parameters aren't available; use ORM or safe APIs.
- **A4: Insecure Design:** Perform threat modeling; use principles like least privilege, fail secure, defense in depth; use secure frameworks (avoid custom weak implementations); treat security as a design requirement.
- **A5: Security Misconfiguration:** Secure default configurations (disable debug, directory listing); use latest server/framework versions; restrict sensitive info in error messages; enable necessary security headers (CORS, CSP, etc. appropriately); segregate application components (so a compromise in one doesn't directly compromise all).
- **A6: Vulnerable and Outdated Components:** Maintain an inventory of components; subscribe to vulnerability feeds; update regularly; use tools to identify known vulns; prefer vendor-supported versions (LTS releases, etc.).
- **A7: Identification and Authentication Failures:** Use proven libraries for auth (ASP.NET Core Identity, OAuth servers); enforce password policies and 2FA; protect session tokens (HttpOnly cookies, etc.); implement account lockout and secure password reset; don't expose excessive info in login errors.
- **A8: Software and Data Integrity Failures:** Verify integrity of dependencies (use HTTPS for fetching, consider signature verification); lock down CI/CD (no unauthorized changes to build process); if using plugins/modules from users, sandbox or validate them; implement digital signing for critical data or updates.
- **A9: Security Logging and Monitoring Failures:** Log security-relevant events (logins, permission changes, errors); ensure logs are tamper-resistant and monitored; establish alerting on suspicious activities (multiple login failures, etc.); conduct regular log review or use automated log analysis.
- **A10: Server-Side Request Forgery:** For any functionality that fetches external URLs, validate inputs (allow only necessary domains or protocols); consider network segmentation (instances shouldn't reach internal networks unless needed); upgrade cloud metadata services to protected versions; and log outbound request details for anomaly detection.

### Appendix B: Secure Coding Checklist for .NET Core

Use this checklist during development and code review:

- [ ] **Input Validation:** All user inputs are validated (type, length, format). Reject obviously malformed data.
- [ ] **Output Encoding:** All variables in views are encoded by Razor by default (avoid `Html.Raw` unless content is safe). Any data inserted into `<script>` or attributes is properly encoded or retrieved safely.
- [ ] **Authentication:** Using ASP.NET Identity or equivalent? Passwords hashed (never plaintext). Session cookies have HttpOnly and Secure flags. Default login lockout enabled for brute force. Multi-factor auth available for sensitive accounts.
- [ ] **Authorization:** Every controller/API has `[Authorize]` as appropriate. No security-critical data is returned without verifying the user’s rights to it (object ownership checks in place). No client-side only admin restrictions (server always rechecks role).
- [ ] **Cryptography:** No custom crypto algorithms. Using AES for any needed encryption with random IVs and keys from secure store. Using PBKDF2 or other slow hashes for passwords. Random number generation via `RandomNumberGenerator` (not `System.Random`) for any security-sensitive randomness (e.g., tokens).
- [ ] **Error Handling:** Detailed exceptions are not shown to users. Generic friendly errors are. Stack traces and error IDs are logged internally. The application is not in debug mode in production.
- [ ] **Dependencies:** All NuGet packages are up-to-date. No package is flagged with known vulnerabilities (check with `dotnet list package --vulnerable`). Remove unused packages.
- [ ] **Secrets Management:** No secrets (API keys, connection strings, credentials) in source code or config files that get checked in. Using User Secrets for dev, and environment variables or Key Vault in production. Connection strings in production are encrypted at rest or stored securely.
- [ ] **Session Management:** Sessions or JWT tokens are invalidated on critical changes (password reset, logout). Consider setting short expiration for JWTs or sliding expiration for cookies. The `SameSite` attribute on cookies is appropriately set (Lax or Strict for session cookies).
- [ ] **HTTP:** HTTPS is enforced (UseHsts and UseHttpsRedirection enabled). No mixed content (ensure no HTTP links on pages). HSTS includes subdomains if applicable.
- [ ] **Security Headers:** X-Content-Type-Options=nosniff, X-Frame-Options (or CSP frame-ancestors) set to deny or sameorigin as needed, X-XSS-Protection (for legacy browsers) set, Content-Security-Policy defined (at least a basic one to disallow unexpected remote content).
- [ ] **CORS:** Not overly permissive. Only allowed origins configured. Credentials only allowed if necessary and with specific origins (no `AllowAnyOrigin` with credentials).
- [ ] **File Uploads:** If the app handles file uploads, files are scanned or validated for type. Store in a location not directly executable. Filename paths sanitized to prevent path traversal.
- [ ] **Deserialization:** No usage of BinaryFormatter or unsafe deserialization of user inputs. JSON deserialization not allowing type names from user.
- [ ] **Logging & Monitoring:** Sensitive personal data (PII) or passwords are not logged. Audit logs exist for important actions. Logs are protected from general access.
- [ ] **Extra for APIs:** Rate limiting in place for public endpoints (prevent abuse). Throttling or pagination for endpoints returning potentially large data sets (to avoid DoS via heavy queries).
- [ ] **Testing:** Security unit tests or integration tests pass (e.g., anti-forgery token check, role access tests). A run with a scanner (like ZAP or burp) has been done and any high findings addressed.

### Appendix C: Exercise Solutions (High Level)

_(Note: Solutions are brief since full detail is in earlier chapters.)_

**Exercise 1 (OWASP category identification):**
a. Concatenating user input into SQL -> **Injection** (SQL Injection) ([Preventing SQL Injection Attacks in .NET: A Guide](https://www.stackhawk.com/blog/net-sql-injection-guide-examples-and-prevention/#:~:text=So%2C%20it%27s%20not%20unreasonable%20to,would%20have%20code%20like%20this)).
b. Unprotected admin page -> **Broken Access Control** (no authorization check).
c. Outdated JWT library with vuln -> **Vulnerable Components** (Using components with known vulns).
d. Plaintext password storage -> **Cryptographic Failures** (previously Sensitive Data Exposure).

**Exercise 2 (Secure Code Review of Login snippet):** Issues:

- Storing plaintext password in DB (`user.Password` presumably), or comparing plaintext -> should hash passwords ([Hashing and Salting Passwords in C# - Best Practices - Code Maze](https://code-maze.com/csharp-hashing-salting-passwords-best-practices/#:~:text=However%2C%20as%20more%20and%20more,use%20these%20for%20password%20hashing)).
- Susceptible to SQL injection if using that style (though code not showing parameter usage).
- No account lockout on repeated tries, no MFA.
- Session fixation risk (should ideally regenerate session on login).
- Not using `PasswordSignIn` from Identity (reinventing wheel).
  Solutions: Use ASP.NET Identity which hashes passwords, include anti-forgery if needed for forms, add lockout, etc.

**Exercise 3 (OAuth2 client implementation):** This is complex but basic steps:

- Set up IdentityServer with in-memory config (like in Chapter 3 example).
- Protect an API with [Authorize] and JWT Bearer (pointing to IdentityServer).
- Use HttpClient or Postman to get token from IdentityServer (e.g., client credentials flow) and call API with it (set Authorization header).
- If issues: often due to misconfigured audience or authority (JWT validation fails). Ensure API expects the correct audience and that token contains that scope/audience.

**Exercise 4 (Harden Web API):** After enabling CORS for only localhost:3000, you'll find your JS app can call but others get blocked (test by curling from another origin with appropriate header).
Rate limiting: If you implemented like in Chapter 4, after 5 requests, subsequent get a 429.
Security headers: After middleware, use a tool or browser dev tools -> see HSTS, X-frame-options, etc., present.
ZAP scan: Before, ZAP would flag missing those headers. After, those particular alerts should disappear. If any remain (maybe CSP not set might be a medium risk), you can consider adding CSP.

**Exercise 5 (Vulnerability hunt scenarios):**

- Changing userID in a request: if you can fetch or modify others' data, that’s a Broken Access Control vulnerability (should fix by checking user context on server).
- Inputting `<script>` and seeing if it executes: if yes, site is XSS vulnerable. Fix by encoding output or sanitizing input ([Prevent Cross-Site Scripting (XSS) in ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-9.0#:~:text=1,HTML%20encoding%20and%20encodes%20double)).
- Spamming endpoint: if it leads to performance issues or user-specific actions being done repeatedly (like sending many emails), need rate limiting or better logic.
- Very long input causing crash or huge delay: might indicate a ReDoS if regex used, or memory issue. Use timeouts or length limits (Chapter 2).
- Calling without login: If that works for an endpoint that should require login, it's an access control bug (add [Authorize]).
- Using GET instead of POST: If state is changed via GET (which is unsafe), that’s a design flaw (enables CSRF easily). Should change to POST and protect with anti-forgery.

**Exercise 6 (Encryption implementation):**

- If done with a fixed IV or ECB mode: patterns emerge. For example, encrypting "AAAAAAAABBBBBBBB" with ECB would show two identical blocks for A and B. With CBC but fixed IV, encrypting same plaintext twice yields same ciphertext, which can leak that those operations had identical input.
- The fix: use random IV each time and either prepend it to ciphertext or store it alongside. Then you can decrypt. Test tampering: if you flip a byte in ciphertext and try to decrypt, with CBC you'll get garbled plaintext (HMAC would catch it if used).
- This shows need for integrity: simply decrypting doesn't tell you if ciphertext was modified. Adding an HMAC (or using AES-GCM) addresses that. So solution includes calculating HMAC of ciphertext+IV and verifying it before decrypting. If HMAC doesn't match, you refuse to decrypt (avoid padding oracle issues by verifying before decrypt).

**Exercise 7 (Pipeline automation):**

- If using `dotnet list package --vulnerable`: a sample output might list e.g. "Newtonsoft.Json 12.0.1 [Vulnerable: Moderate severity CVE-YYYY-... resolved in 12.0.3]". So you know to update.
- OWASP Dependency Check action would produce a report (HTML or SARIF) and you could see e.g. "jQuery-1.12.0.js : CVE-201X-... XSS vulnerability".
- SonarCloud: after running, you'll see issues in their dashboard. e.g., it might raise "Remove this hardcoded password" for something like `var pwd="12345";` or "Validate inputs before using in SQL command".
- ZAP baseline: would output something like "Medium: X-Frame-Options header not set" ([.Net Core Penetration Testing ](https://www.devready.co.uk/post/net-core-penetration-testing#:~:text=ZAP%20description%3A%20X,to%20protect%20against%20%E2%80%98ClickJacking%E2%80%99%20attacks)) before fix, and "PASS" after fix.
  If you introduced a vuln library, your pipeline should fail if you set it to (like WhiteSource can mark build unstable if new high vulns found). You then update the package and pipeline goes green.

**Exercise 8 (Attacker mindset drill on profile update):**
Example answers:

- Changing userID: if the profile update endpoint took an "id" param and you change to another user's id, does it update their profile? If yes, you found a Broken Access Control. Solution: don't take id from user at all (use the logged in user's).
- XSS in name field: after update, if you see your name with a script executed (maybe on the profile page or admin user list), that's a stored XSS. Fix: encode output on profile page and admin pages. Possibly also validate that name doesn't contain HTML.
- 1000 requests/min: maybe see if the server slows or if your account now has 1000 email change confirmations in your inbox. If it's causing issues, implement throttling (either limit how often a profile can be changed or a general rate limit).
- Extremely long value: If it crashes or hangs, likely a performance bug, possibly a regex issue if there's validation like `Regex.IsMatch(input)` that takes exponential time on certain input. Solution: use non-backtracking regex or limit length before regex.
- Call without login: if it works (profile updated anonymously), it's a big flaw. Add `[Authorize]`.
- GET vs POST: If the profile update can be triggered by just visiting a URL (GET), that's problematic (can be CSRFed easily by an attacker in an img tag). It should be POST only and protected by anti-CSRF token. Fix accordingly in ASP.NET by [HttpPost] and ValidateAntiForgeryToken.

**Exercise 9 (Research a breach):**
If someone researched Adobe 2013:

- Vulnerability: Attackers got into a backup system, stole ~152 million user records including encrypted passwords and password hints in plaintext. The encryption was unsalted 3DES on passwords, and hints gave clues, so many were cracked.
- Prevention: Not storing password hints (or encrypt them too), using stronger hashing (not reversible encryption) for passwords. Also, segmented network so an intrusion in one area doesn't yield full user DB.
- Apply to .NET app: don't store hints or any info that could help an attacker. If you must store security questions, treat them like passwords (hashed). Use one-way hashing, not reversible crypto, for user secrets.

This exercise answer will vary by breach chosen, but should draw parallels to one of OWASP categories and corresponding fixes.

---

_This concludes the 200+ page guide on secure .NET Core development. It's a comprehensive resource, but security is a vast field - always keep learning and stay vigilant._
