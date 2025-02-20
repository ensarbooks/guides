# Building a Full-Stack Spring Boot and React Application: Step-by-Step Guide

This guide provides a detailed walkthrough for advanced users to build a complex full-stack application using Spring Boot (Java) for the backend, React for the frontend (with Redux for state management), and MySQL for the database. We will cover backend REST API setup, database integration with CRUD operations, implementing authentication/authorization, creating the React frontend, integrating the frontend and backend, adding logging with Elasticsearch, containerizing with Docker, deploying on Kubernetes, and setting up CI/CD for automated deployment. Each section is structured with clear steps and best practices.

## Setting Up the Spring Boot Backend with REST APIs

1. **Initialize the Spring Boot project**: Use Spring Initializr or your IDE to create a new Spring Boot project. Include dependencies for Spring Web (for building RESTful APIs), Spring Data JPA (for database access), and MySQL Driver. This provides the essential libraries to create REST controllers and interact with MySQL.

2. **Define the domain model**: Create JPA entity classes for your data model. Annotate each with `@Entity` and define a primary key with `@Id` (and `@GeneratedValue` for auto-increment). For example, a `Product` entity might have fields id, name, price with corresponding getters/setters. Ensure the class and field names match your database table and columns, or use JPA annotations to map them ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=%40Entity%20public%20class%20Product%20,String%20name%3B%20private%20float%20price)) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=%40Id%20%40GeneratedValue%28strategy%20%3D%20GenerationType,return%20id%3B)).

3. **Create a repository interface**: For each entity, create an interface that extends `JpaRepository<Entity, ID>` (for example, `ProductRepository extends JpaRepository<Product, Integer>`). Spring Data JPA will automatically generate the implementation for common CRUD methods like `findAll()`, `save()`, `findById()`, and `deleteById()` so you don't have to write SQL or boilerplate code ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=import%20org)). This follows the repository pattern and simplifies data access.

4. **Implement service layer (optional)**: Although not strictly required, it's good practice to have a service layer. Create service classes (annotated with `@Service`) that inject the repositories (using `@Autowired`) and provide methods to handle business logic or transactions (annotate with `@Transactional` if needed). In simple CRUD apps, the service methods might just call the repository (e.g., `repo.findAll()` or `repo.save(entity)`) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=import%20org)) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=public%20void%20save%28Product%20product%29%20,save%28product%29%3B)). The service layer helps decouple controllers from data access and makes unit testing easier.

5. **Create REST controllers**: Implement controller classes annotated with `@RestController`. Use request mapping annotations to define API endpoints for each operation. For example, use `@GetMapping("/products")` to list all products, `@GetMapping("/products/{id}")` to get one by ID, `@PostMapping("/products")` to create, `@PutMapping("/products/{id}")` to update, and `@DeleteMapping("/products/{id}")` to delete. Spring's annotations like `@GetMapping`, `@PostMapping`, etc., map HTTP verbs to handler methods ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=hood,step%20by%20step)). Each method should call the service or repository to perform the action and return a result or status.

6. **Return proper responses**: When building REST APIs, ensure you return appropriate HTTP status codes and JSON responses. Spring Boot auto-converts return values to JSON using Jackson (which is included by default) ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=public%20record%20Greeting,)) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=This%20is%20the%20JSON%20representation,versa%2C%20automatically)). For example, a `List<Product>` returned from a controller will be serialized to JSON array in the response body ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=The%20first%20RESTful%20API%20is,a%20kind%20of%20retrieval%20operation)). Use `ResponseEntity` to customize the status and body if needed. For instance, return `ResponseEntity.ok(product)` when a product is found, or `ResponseEntity.notFound().build()` if an ID is not found ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=%40GetMapping%28,Product%3E%28HttpStatus.NOT_FOUND%29%3B)). This gives API consumers clear signals (200 OK, 404 Not Found, etc.).

7. **Run and test the API**: Run the Spring Boot application (e.g., using `mvn spring-boot:run` or your IDE). By default it will start on port 8080 ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=,CRUD%20start)). Test the endpoints using curl or Postman. For example, GET `http://localhost:8080/products` should return a JSON list of products (or an empty list), and POST `http://localhost:8080/products` with a JSON body will create a new product. Verify that CRUD operations behave as expected (creating returns 201/200, getting non-existent returns 404, etc.). At this stage, you have a basic RESTful backend.

**Best Practices & Tips**: Organize your code into packages (e.g., `controller`, `service`, `repository`, `model`). Use meaningful endpoint URLs (e.g., `/api/products` if prefixed with `/api`). Validate inputs and handle exceptions (you can use Spring's @ExceptionHandler or @RestControllerAdvice for global error handling). Also, enable Spring DevTools for hot reloading during development (optional).

## Connecting to MySQL and Implementing CRUD Operations

1. **Set up a MySQL database**: Ensure you have MySQL running and create a database/schema for your application (e.g., `myappdb`). You can use MySQL locally or via Docker. Create necessary tables either manually or let JPA create them (based on entities). For development, you might allow JPA auto-DDL (`spring.jpa.hibernate.ddl-auto`) to create tables, and for production use migrations (Flyway/Liquibase).

2. **Configure MySQL connection**: In `application.properties` (or `application.yml`), configure the datasource URL, username, and password for MySQL. For example:

   ```properties
   spring.datasource.url=jdbc:mysql://localhost:3306/myappdb
   spring.datasource.username=root
   spring.datasource.password=yourpassword
   spring.jpa.hibernate.ddl-auto=update
   ```

   This tells Spring Boot to connect to MySQL on localhost at schema `myappdb` with the given credentials ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=spring.jpa.hibernate.ddl)). The `ddl-auto=update` will auto-create/update tables based on entities (use `validate` or `none` in production to avoid unintended changes ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=application,with%20the%20following%20content))). When the app starts, you should see in logs that a connection to MySQL is established via Hibernate.

3. **CRUD repository usage**: With Spring Data JPA and MySQL configured, use the repository methods in your controller/service to perform database operations. For example, in a GET all products endpoint, call `productRepository.findAll()` which returns a `List<Product>` containing all records ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=The%20first%20RESTful%20API%20is,a%20kind%20of%20retrieval%20operation)). For getting one by ID, use `findById(id)` and handle the case when it returns empty (to return 404) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=%40GetMapping%28,Product%3E%28HttpStatus.NOT_FOUND%29%3B)). To create or update, use `save(entity)`, and for delete use `deleteById(id)`. Spring Data JPA implements these automatically ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=import%20org)), so you don't write any SQL – it follows best practices internally for common CRUD actions.

4. **Implement controller methods for CRUD**: Ensure each REST endpoint method uses the repository/service to interact with MySQL. For example:

   - **Retrieve list:** `@GetMapping("/products")` -> call `service.listAll()` (which might call `repo.findAll()`) and return the list. This will produce JSON like `[{"id":1,"name":"Product1","price":123.45}, ...]` ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=curl%20http%3A%2F%2Flocalhost%3A8080%2Fproducts)).
   - **Retrieve one:** `@GetMapping("/products/{id}")` -> call `service.get(id)` (which likely uses `repo.findById(id)`). If found, return it with 200 OK; if not, return 404 Not Found using `ResponseEntity` ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=%40GetMapping%28,Product%3E%28HttpStatus.NOT_FOUND%29%3B)).
   - **Create:** `@PostMapping("/products")` -> accept a JSON request body (Spring will bind it to a Product object), call `service.save(product)` (which uses `repo.save`), and return the saved object or a location URI. Typically return 201 Created with the new resource or 200 OK with the created entity.
   - **Update:** `@PutMapping("/products/{id}")` -> similar to create, but first check if the record exists (or simply call save which will update since the ID exists). Return 200 on success, or 404 if the ID doesn't exist.
   - **Delete:** `@DeleteMapping("/products/{id}")` -> call `service.delete(id)` (which does `repo.deleteById(id)`). Return 204 No Content on success, or 404 if id not found.

   Make sure to handle exceptions like `NoSuchElementException` for `findById().get()` calls ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=public%20ResponseEntity,Product%3E%28HttpStatus.NOT_FOUND%29%3B%20%7D)) or use `findById(id).orElseThrow()`. Each operation should log or print meaningful info (we will add proper logging later).

5. **Test CRUD functionality**: Restart the application after adding MySQL config and CRUD code. Use an API client to test each endpoint:

   - Creating an item should persist it in the MySQL database (verify via MySQL client or subsequent GET).
   - Updates should change the data in the database.
   - Deletions remove the data. Trying to get a deleted item should yield 404.
   - Check the console logs for any SQL errors or exceptions and fix accordingly (e.g., adjust entity mappings if needed).

6. **Database best practices**: Use meaningful transaction boundaries – in our simple example, each HTTP request is one transaction by default (managed by Spring). If using a service layer, annotate it with `@Transactional` to ensure atomic operations ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=import%20org)) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=public%20void%20delete%28Integer%20id%29%20,)). Also consider using DTOs to separate API layer from internal JPA entities (to avoid exposing all fields or to format data), but for a basic application returning entities directly is fine. Ensure proper indexing in the database for any frequently queried fields (the primary key is indexed by default).

By this stage, you have a Spring Boot application connected to MySQL with fully functional CRUD REST endpoints.

## Implementing Authentication and Authorization

With open CRUD endpoints, anyone could modify data. Next, introduce authentication and authorization to secure the backend. There are a few approaches (JWT tokens, OAuth2, or session-based auth). We will outline a JWT-based solution which is ideal for stateless REST APIs and modern SPAs.

1. **Add Spring Security**: Include the Spring Security dependency in your project (Spring Boot Starter Security). When you run the app now, Spring Security by default secures all endpoints with basic auth (you'll see a generated password in logs). We'll override this configuration.

2. **Configure Web Security**: Create a class that extends the Spring Security filter chain configuration (in Spring Boot 3+, you can use a `SecurityFilterChain` bean, or in earlier versions extend `WebSecurityConfigurerAdapter`). Annotate it with `@EnableWebSecurity`. In the security configuration, perform the following:

   - **Enable CORS and disable CSRF**: Since our frontend will be on a different origin (domain/port), enable Cross-Origin Resource Sharing so the browser calls are not blocked, and disable CSRF because we're not using cookies for auth in a stateless API ([JWT. How does JSON Web Token work in Java Rest API?](https://devopsi.pl/blog/how-does-json-web-token-work-in-java-rest-api/#:~:text=Having%20configured%20the%20authentication%20manager%2C,to%20set%20the%20following%20options)).
   - **Stateless session**: Configure the session management as stateless (`http.sessionManagement().sessionCreationPolicy(STATELESS)`) because we will not use HTTP sessions ([JWT. How does JSON Web Token work in Java Rest API?](https://devopsi.pl/blog/how-does-json-web-token-work-in-java-rest-api/#:~:text=a%20JWT%20token,to%20set%20the%20following%20options)).
   - **Endpoint security**: Define which endpoints are secured. For example, permit `POST /api/auth/login` and perhaps user registration endpoints to all (`permitAll()`), but require authentication for all other `/api/**` endpoints. You can also configure role-based access here (e.g., allow `GET /products` to anyone but restrict `POST/PUT/DELETE` to users with ADMIN role).
   - **Authentication provider**: Set up how users are loaded and passwords checked. This could be an in-memory user store for testing or a database of users. You might use `UserDetailsService` to load users and a password encoder (BCrypt) to verify passwords.
   - **JWT filter**: Add a custom filter in the security filter chain that will intercept requests and check for a JWT in the Authorization header. This filter should run **before** the default username/password authentication filter ([Spring Security JWT Tutorial | Toptal®](https://www.toptal.com/spring/spring-security-tutorial#:~:text=%2F%2F%20Add%20JWT%20token%20filter,class)), so it can authenticate the request by token. If the token is valid, create an `Authentication` object and set it in the security context.

3. **Implement JWT generation (Authentication)**: Create an authentication controller (e.g., `AuthController`) with a login endpoint (`POST /api/auth/login`). In this method, do the following:

   - Read the login credentials (username/password) from the request body.
   - Authenticate the user – you can use `AuthenticationManager` to authenticate, or manually load the user (via UserDetailsService) and check the password with a PasswordEncoder.
   - If authentication succeeds, generate a JSON Web Token. Use a JWT library (like io.jsonwebtoken Jwts, or Spring Security's Jwt APIs) to create a token signed with a secret key. Include claims such as username and roles, and set an expiration (e.g., 1 hour).
   - Return the JWT to the client, typically in a JSON response or in an `Authorization: Bearer <token>` header.
   - If credentials are invalid, return 401 Unauthorized.

4. **Implement JWT validation (Filter)**: In the custom filter that you added to the security config:

   - Extract the token from the `Authorization` header (it usually comes as "Bearer <token>").
   - Validate the token (verify signature with the secret key, and expiration date).
   - If valid, parse the token to get the user details (username, roles).
   - Load the user details (to double-check against user store if needed) and create an `UsernamePasswordAuthenticationToken` with these details and set it as authenticated.
   - Set this authentication into Spring Security's context. After this filter, Spring Security sees the user as authenticated and allows the request to proceed to the controller.
   - If the token is missing or invalid, the filter should not set an authentication, and Spring Security will block the request (or it will proceed to another filter which might reject it). You can customize an entry point to return 401 responses for unauthorized access.

5. **Test the secured endpoints**: Now, all protected endpoints require a valid JWT. First, obtain a token by calling the login API with valid credentials. Then, call the CRUD APIs with an `Authorization: Bearer <token>` header. You should get data if the token is valid and has necessary rights. Without a token or with an invalid token, you should get HTTP 401. This confirms that authentication is working.

6. **Authorization (roles)**: If your app has roles (e.g., ADMIN, USER), include those in the JWT or load them in the SecurityContext. You can then annotate controller methods with `@PreAuthorize("hasRole('ADMIN')")` or configure URL-based restrictions in the security config (e.g., `.antMatchers("/api/products/**").hasRole("ADMIN")`). Spring Security will then enforce that the JWT must belong to a user with that role for those endpoints. This is optional but important for real applications with permission differences.

7. **Alternate approaches**: Instead of JWT, you could use **OAuth2** if you want integration with an external identity provider (Google, Okta, etc.) or need an OAuth2 authorization code flow. Spring Security offers an OAuth2 client that can handle login redirects. Another approach is **session-based auth** (the traditional form login), where Spring Security creates an HTTP session and stores authentication there, using a JSESSIONID cookie. That would require enabling CSRF protection and might not be ideal for a separate SPA frontend. JWT is preferred for stateless interactions with a React app. If using OAuth2/OIDC (e.g., with Okta), you'd likely use OAuth2 Login and have your React app handle the redirect to the provider – this can be complex, so JWT with your own login is simpler for custom apps.

**Best Practices**: Use strong hashing for passwords (Spring Security's default is BCrypt). Keep the JWT secret safe (configure it in application properties and don't expose it). Set reasonable expiration and perhaps implement refresh tokens or re-login on token expiry. Also, enable HTTPS in production so that tokens are not intercepted. Log authentication events (log successful logins, and possibly suspicious failures). We have configured CORS and disabled CSRF because we rely on JWT for security instead ([JWT. How does JSON Web Token work in Java Rest API?](https://devopsi.pl/blog/how-does-json-web-token-work-in-java-rest-api/#:~:text=Having%20configured%20the%20authentication%20manager%2C,to%20set%20the%20following%20options)), which is a common setup for REST APIs. This security setup ensures only authorized users can access/modify the data.

## Creating the React Frontend with Redux for State Management

Next, build the frontend using React to provide a user interface for our application. We will use Redux for state management to handle complex state in a predictable way.

1. **Initialize the React app**: Use `create-react-app` (CRA) or Vite to bootstrap a new React project. For example, run `npx create-react-app myapp-frontend` (if using CRA) which sets up a React project with a development server. This will create a project structure with _src_ (for source code) and _public_ folders.

2. **Install Redux and related libraries**: In the React project, add Redux and the React-Redux bindings. The modern approach is to use Redux Toolkit. Install it with: `npm install @reduxjs/toolkit react-redux`. Redux Toolkit simplifies configuring the store and writing reducers. You might also install Redux Thunk (`npm install redux-thunk`) if you plan to handle async calls in traditional way (though Redux Toolkit has it included by default). If routing is needed, install React Router (`npm install react-router-dom`).

3. **Set up the Redux store**: Create a Redux store in your app. For example, create a file `src/store.js`. Using Redux Toolkit, you can use `configureStore({ reducer: rootReducer })`. Define your `rootReducer` by combining slice reducers or use Redux Toolkit's `createSlice` to make slices of state. For instance, create a slice for products:

   ```javascript
   import { createSlice } from "@reduxjs/toolkit";
   const productsSlice = createSlice({
     name: "products",
     initialState: { list: [], status: "idle" },
     reducers: {
       setProducts(state, action) {
         state.list = action.payload;
       },
       // other reducers like addProduct, updateProduct, etc.
     },
   });
   export const { setProducts } = productsSlice.actions;
   export default productsSlice.reducer;
   ```

   Do similar for user authentication state (e.g., `authSlice` to store current user/token). Combine these reducers in `configureStore`. Wrap your `<App />` in `<Provider store={store}>` in `index.js` so that React components can access the store.

4. **Build the UI components**: Plan your components structure. For a CRUD app, you may have components like `ProductList`, `ProductForm` (for create/edit), maybe `ProductDetails`, and authentication components like `Login`. Use React Router to define routes (e.g., `/login`, `/products`, `/products/:id/edit`). Each component will interact with the Redux store or local component state as needed.

   - **ProductList**: on mount, dispatch an action to fetch products from the backend, and select the `products.list` from Redux state to display. Use `useSelector` to get state and `useDispatch` to dispatch actions.
   - **ProductForm**: manage form state with local component state or Redux (for simplicity, local state for inputs, then dispatch an action on submit to save).
   - **Login**: have form fields for username/password, on submit dispatch an action to perform login (calling backend API).

5. **State management with Redux**: Redux will hold the global state, such as the list of products and the authentication info (e.g., current user or token). This centralizes application state in a single object and makes it predictable via pure functions (reducers) ([How to manage state in a React app using Redux. - DEV Community](https://dev.to/efkumah/how-to-manage-state-in-a-react-app-using-redux-5pc#:~:text=In%20this%20tutorial%2C%20you%20will,level%20component)). The typical data flow is: UI triggers an action (e.g., "FETCH_PRODUCTS"), a Redux thunk or saga performs the API call, then dispatches a success action with the data (e.g., "FETCH_PRODUCTS_SUCCESS"), which the reducer handles to update the state (store the fetched products). The UI subscribed to the store (via `useSelector`) will then automatically reflect the new state. This unidirectional flow makes it easier to manage and debug state changes.

6. **Implement asynchronous actions**: For calling the Spring Boot APIs, use `fetch` or a library like Axios (`npm install axios`). For example, to fetch products from the backend:

   ```javascript
   // Using Redux Thunk
   export const fetchProducts = () => async (dispatch) => {
     dispatch(productsLoading()); // set loading state if needed
     try {
       const res = await fetch("/api/products");
       const data = await res.json();
       dispatch(setProducts(data)); // store the list in Redux state
     } catch (err) {
       console.error("Failed to fetch products", err);
       // dispatch an error state or handle error
     }
   };
   ```

   You can call this `fetchProducts()` thunk in a React component by `dispatch(fetchProducts())` inside a `useEffect` hook when the component loads. Similar approach for create/update: call the appropriate backend endpoint then dispatch Redux actions (e.g., add the new product to state or update an existing one in state). Using Redux for state ensures the UI components always present the latest data and can react to loading or error states globally.

7. **Authentication on the frontend**: When the user logs in (through the login form component), call the backend auth API (`POST /api/auth/login`) with the credentials. On success, you'll get a JWT token (and possibly user info). Store the token in Redux state (e.g., in `auth.token`) and also perhaps in `localStorage` so it persists on refresh. Update the Redux auth state to reflect that the user is logged in (you might store the username/roles from the token as well). After login, redirect the user to the main app page (e.g., products list). Also, configure your Axios or fetch to include the JWT in the header for subsequent requests:

   - If using Axios, you can set a default header: `axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;`
   - Or for fetch, manually include in each request or create a wrapper function for requests that adds the header.
     This way, the backend will receive the JWT and authenticate the requests. Also implement a logout action that clears the token from state and storage.

8. **Connecting Redux with React components**: Use `useSelector` to get state slices (e.g., `const products = useSelector(state => state.products.list)`) and display the data in your JSX. Use `useDispatch` to dispatch actions (e.g., on form submit, dispatch `createProduct(newData)`). Redux will efficiently update only the necessary components when state changes. This is especially useful for larger apps where many components might need access to shared state (instead of passing props down many levels).

9. **UI/UX considerations**: Use a component library or custom CSS for styling. You might use React Bootstrap or Material-UI for a quick UI. Ensure to show loading states (e.g., when fetching data, show a spinner or "Loading..." text) and error messages (e.g., if a save fails). Also consider form validation feedback for better UX.

At this point, you have a React application that manages its state with Redux and is capable of performing actions and storing data. However, we need to actually integrate it with our Spring Boot backend APIs.

## Integrating the React Frontend with the Spring Boot Backend

With both backend and frontend set up, integration ensures they communicate properly.

1. **During development**: Run the React app (on its development server, usually at http://localhost:3000) and the Spring Boot app (at http://localhost:8080). By default, making an AJAX call from React to a different port (8080) will be blocked by the browser due to CORS. There are two ways to handle this in development:

   - **Use the CRA proxy**: If you created the app with Create React App, you can add a proxy. Open `package.json` of the React app and add: `"proxy": "http://localhost:8080",`. This will proxy any unknown requests from the React dev server to the Spring Boot server ([Use React and Spring Boot to Build a Simple CRUD App | Okta Developer](https://developer.okta.com/blog/2022/06/17/simple-crud-react-and-spring-boot#:~:text=To%20proxy%20from%20,app%2Fpackage.json)). For example, an API call to `/api/products` in development will actually be forwarded to `http://localhost:8080/api/products`. This eliminates CORS issues in dev and lets you call the API as if it's same host.
   - **Enable CORS on backend**: Alternatively, configure Spring Boot to allow requests from the React dev origin. You can do this by annotating your controller classes or methods with `@CrossOrigin(origins = "http://localhost:3000")`. Or define a global CORS mapping in your Security configuration (e.g., `http.cors()`) to permit the React app domain ([JWT. How does JSON Web Token work in Java Rest API?](https://devopsi.pl/blog/how-does-json-web-token-work-in-java-rest-api/#:~:text=Having%20configured%20the%20authentication%20manager%2C,to%20set%20the%20following%20options)). This way, even without the proxy, the browser will be allowed to call the API. In production, if frontend and backend are on the same domain or handled via an API gateway, CORS config may differ.

2. **Update API base URLs**: In your React app's code, ensure the API calls point to the correct URL. If using the proxy in development, you can just use relative URLs like `/api/products`. In production, if the frontend is served from a different domain, you might need the full URL. One approach is to set an environment variable for the API URL. For example, have `REACT_APP_API_URL` and use it: `fetch(process.env.REACT_APP_API_URL + "/products")`. Then you can configure this var for development (point to localhost:8080) and production (maybe an empty string if same domain, or a production URL). This avoids scattering host URLs in code.

3. **Build the React app for production**: When you are ready to integrate for production deployment, run `npm run build`. This creates an optimized `build` directory with static files (HTML, CSS, JS). You have a couple of options to serve these:

   - **Serve via Spring Boot**: Copy the build files into `src/main/resources/static` or configure Spring MVC to serve the React `index.html` on a certain path. Spring Boot will then serve the React app on requests (except those going to `/api/**` which your controllers handle). Matt Raible's tutorial, for example, packages the React app in the Spring Boot jar ([Use React and Spring Boot to Build a Simple CRUD App | Okta Developer](https://developer.okta.com/blog/2022/06/17/simple-crud-react-and-spring-boot#:~:text=Today%2C%20I%E2%80%99ll%20show%20you%20how,productive%20workflow%20for%20developing%20locally)). You might integrate the build into Maven so that `mvn package` also builds the React app and includes it ([Use React and Spring Boot to Build a Simple CRUD App | Okta Developer](https://developer.okta.com/blog/2022/06/17/simple-crud-react-and-spring-boot#:~:text=To%20proxy%20from%20,app%2Fpackage.json)).
   - **Serve via separate server**: Run the React app in a separate container (e.g., Nginx). In that case, your React app will call the Spring Boot API over the network. Ensure CORS is configured for the production domain. Also, if using a separate domain, you'll likely use an Ingress or load balancer to tie them together.

4. **Test end-to-end**: After either setting up proxy or enabling CORS, test the full flow:

   - Open the React app in the browser. The React app should fetch data from the Spring Boot API (e.g., the product list appears). You should see network calls in the browser's developer tools. If there's an error (like 401 Unauthorized due to security), ensure you obtain a JWT and include it. For testing, you might temporarily allow unsecured access to verify connectivity, then add the JWT header logic.
   - Try creating/editing data from the React UI and ensure it reflects in the database (and vice versa, changes in DB reflect when you refresh or re-fetch in UI).
   - Test the login: enter credentials in the React login form, submit, and ensure you receive a token and the app transitions to an authenticated state (perhaps show user info or enable admin features). Then test an action that requires auth (like adding a product) to see that the token is correctly being sent and accepted by backend (if token is missing or wrong, you should get a 401 from backend, which you can handle in React by redirecting to login).

5. **Logging and error handling**: Verify that errors are properly handled. For example, if the backend is down or returns an error, the React app should catch the fetch/axios error and display a message. On the backend, you can implement an `@ExceptionHandler` to return a JSON error response for exceptions (to avoid HTML error pages). Make use of browser dev tools and backend logs to diagnose any integration issues (like CORS errors, which will appear in browser console, or 401 errors if JWT is not set correctly).

6. **Synchronize configurations**: Ensure that any shared config (like API paths, port numbers, etc.) are consistent between front and back. Using relative paths and proxies helps. Also, double-check that the Spring Boot app's context path (if any) is considered. By default, Spring Boot serves at root ("/"), which matches our use of `/api/...`.

**Best Practices**: In a real deployment, you might put an API gateway or load balancer in front of the services. For example, serve React from Nginx or CDN and proxy API calls to the Spring Boot service. This way, both appear under one domain (which can simplify CORS). If you serve both on the same domain (e.g., React app at `/` and APIs under `/api` on the same host), you can avoid CORS entirely. Regardless, keep environment-specific settings (like API endpoint, OAuth client IDs, etc.) in config files or environment variables, not hard-coded.

Now your React frontend and Spring Boot backend are working together to provide a full-stack application. Next, we'll improve the backend with logging, and then move on to containerization and deployment.

## Implementing Logging for CRUD Operations and Sending Logs to Elasticsearch

Logging is crucial in a complex application for monitoring and troubleshooting. We will add logging to the backend and set up a pipeline to ship these logs to Elasticsearch, where they can be indexed and analyzed (often as part of the ELK stack: Elasticsearch, Logstash, Kibana).

1. **Add logging statements**: Use SLF4J (which Spring Boot includes) to log important events in your code. For example, in each controller method or service method for CRUD, add `logger.info("User {} created product {}", userId, productId)` after a creation, or `logger.info("Fetching all products")` when a list is requested. Also log warnings or errors appropriately (e.g., `logger.error("Product not found with id {}", id)` before throwing an exception). These logs will by default go to the console (stdout) and to any file if configured.

2. **Configure log format**: To send logs to Elasticsearch, it's best to format them as JSON. Spring Boot's default console logging is text-based. We can use **Logstash Logback Encoder** to log in JSON. Add the dependency:

   ```xml
   <dependency>
       <groupId>net.logstash.logback</groupId>
       <artifactId>logstash-logback-encoder</artifactId>
       <version>7.4</version>
   </dependency>
   ```

   (Use the latest version.) Then create or edit `logback-spring.xml` (in src/main/resources). Use a JSON encoder for the console or file appender:

   ```xml
   <appender name="JSON_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
       <encoder class="net.logstash.logback.encoder.LogstashEncoder" />
   </appender>
   <root level="INFO">
       <appender-ref ref="JSON_CONSOLE"/>
   </root>
   ```

   This will output logs in JSON format (with fields like timestamp, level, logger, message, etc.). You can add custom fields (like application name or environment) if needed.

3. **Set up Elasticsearch**: Ensure you have access to an Elasticsearch instance. It could be a local Elasticsearch (like running in Docker) or a cloud service. Note the URL and port (default ES runs on localhost:9200). Also determine an index name where logs should go, e.g., "myapp-logs". For production, one usually uses Logstash or Beats, but we'll show direct integration.

4. **Use an Elasticsearch log appender**: Instead of writing logs to file and having an external shipper, you can configure Logback to send logs directly to Elasticsearch. One way is using a community appender library like **logback-elasticsearch-appender**. Add its dependency:

   ```xml
   <dependency>
       <groupId>com.internetitem</groupId>
       <artifactId>logback-elasticsearch-appender</artifactId>
       <version>1.6</version>
   </dependency>
   ```

   This provides `ElasticsearchAppender` for Logback ([java - How to send Spring Boot logs directly into Elasticsearch server? - Stack Overflow](https://stackoverflow.com/questions/69692523/how-to-send-spring-boot-logs-directly-into-elasticsearch-server#:~:text=You%20could%20include%20the%20logback,file)). Configure it in `logback-spring.xml`:

   ```xml
   <appender name="ELASTIC" class="com.internetitem.logback.elasticsearch.ElasticsearchAppender">
       <errorHandler class="com.internetitem.logback.elasticsearch.ElasticsearchAppender$FailSilentlyErrorHandler"/>
       <url>http://localhost:9200</url>   <!-- Elasticsearch URL -->
       <index>myapp-logs</index>         <!-- Index name -->
       <type>logback</type>             <!-- document type, not used in ES7+ but keep for older compatibility -->
       <encoder class="net.logstash.logback.encoder.LogstashEncoder">
           <!-- optional: custom fields or settings -->
       </encoder>
   </appender>
   <root level="INFO">
       <appender-ref ref="ELASTIC"/>
   </root>
   ```

   This appender will send log events directly to Elasticsearch's REST API (HTTP POST to the specified URL/index). Each log event is a JSON document in the index. Make sure the Elasticsearch server is reachable from the app (network wise). If running ES in Docker, you might need to adjust host or use the container's network.

5. **Alternative: Logstash**: Another common approach is to send logs to Logstash. You could use Logstash TCP/UDP appenders. For example, `LogstashTcpSocketAppender` from the Logstash encoder library can send logs to a Logstash listener on a port ([Spring Boot send logs to ElasticSearch - Stack Overflow](https://stackoverflow.com/questions/77863602/spring-boot-send-logs-to-elasticsearch#:~:text=%3Cconfiguration%3E%20%3Cappender%20name%3D,%25blue%28%25msg%25n)). Then Logstash can funnel logs into Elasticsearch with more processing (e.g., parsing custom patterns). This is more flexible and robust (handles retries, etc.), but requires running a Logstash service and configuring it with a pipeline. For simplicity, direct-to-Elasticsearch (step 4) can work, but be mindful that network issues or ES downtime could block your app logging (the FailSilentlyErrorHandler in config helps avoid exceptions).

6. **Deploy and verify logging**: Restart the Spring Boot application with the new logging configuration. Trigger some CRUD operations (through the API or UI). Then check Elasticsearch:

   - Use Kibana (if available) or curl to query `http://localhost:9200/myapp-logs/_search?pretty=true` and see if documents are coming in. You should see JSON log entries with your messages and metadata.
   - Each log entry might have fields like `@timestamp`, `level`, `logger_name`, `message`, etc., and possibly thread info or custom fields you added. This structured log data can now be searched or visualized in Kibana (e.g., create a Kibana index pattern for "myapp-logs\*").
   - If logs aren't appearing, check the application stdout for errors related to the appender (maybe connection refused if ES not up). You can adjust logback config to also log to console for debugging.

7. **Logging best practices**: Log at appropriate levels (INFO for important lifecycle events, DEBUG for detailed troubleshooting info, ERROR for exceptions). Avoid logging sensitive data (passwords, tokens). Use MDC (Mapped Diagnostic Context) if you want to add contextual info (e.g., user ID) to all logs in a request; this is useful for tracing actions per user. In web apps, you can use a filter to put user id in MDC, and the log pattern to include `%X{userId}` ([Spring Boot send logs to ElasticSearch - Stack Overflow](https://stackoverflow.com/questions/77863602/spring-boot-send-logs-to-elasticsearch#:~:text=%3Cpattern%3E%25magenta%28%25d%7BHH%3Amm%3Ass.SSS%7D%29%20%25highlight%28%5B%25thread%5D%29%20%25,logs%3C%2Findex%3E%20%3C%2Fencoder%3E%20%3C%2Fappender)) for example. The logback encoder can include MDC data in the JSON output easily.

8. **Monitor logs**: With logs in Elasticsearch, you can set up Kibana dashboards or alerts. For instance, monitor for ERROR logs or unusual activity. Logging each CRUD operation with who did it and when, stored in Elasticsearch, creates an audit trail. This addresses both debugging needs and audit requirements.

By implementing logging and shipping logs to Elasticsearch, you can effectively monitor your application in production. This closes the loop on backend development. Now, we'll prepare the app for deployment by containerizing it.

## Using Docker to Containerize the Application

Docker will allow us to package the Spring Boot backend, React frontend, and even the MySQL database into containers for easy deployment and consistency across environments.

1. **Write a Dockerfile for the Spring Boot app**: In the Spring Boot project directory, create a file named `Dockerfile` with content to build a Docker image for the backend. A simple Dockerfile might be:

   ```Dockerfile
   FROM openjdk:8-jdk-alpine
   ARG JAR_FILE=target/*.jar
   COPY ${JAR_FILE} app.jar
   ENTRYPOINT ["java","-jar","/app.jar"]
   ```

   This uses a lightweight Alpine Linux with JDK 8 (you can use JDK 17 as well) as the base, copies the generated jar (from the Maven/Gradle build) into the image, and sets the entrypoint to run the jar ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=FROM%20openjdk%3A8,jar%22%2C%22%2Fapp.jar)). If your build produces a specific jar name, you can COPY that specifically instead of using ARG pattern.

   _Best practices_: Use a multi-stage build to minimize image size. For example, use `maven:3.8-jdk-17` image to build the app, then use a smaller JRE base image to run it. Also, consider running the app as a non-root user for security (create a user in Dockerfile and use `USER` instruction) ([Getting Started | Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker#:~:text=FROM%20openjdk%3A8,jar)).

2. **Build the backend image**: Ensure you've built the Spring Boot jar (`mvn package` to get `target/myapp.jar`). Then build the Docker image by running `docker build -t myapp-backend:1.0 .` (replace tag/name as desired). Docker will execute the Dockerfile, resulting in an image containing the app and Java runtime.

3. **Dockerize the React app**: You have two main options for the front-end:

   - **Option A: Serve via Nginx** – Create a Dockerfile in the React project that builds the app and serves it. Example:

     ```Dockerfile
     FROM node:18-alpine as build
     WORKDIR /app
     COPY package.json package-lock.json ./
     RUN npm install
     COPY . .
     RUN npm run build

     FROM nginx:1.21-alpine
     COPY --from=build /app/build /usr/share/nginx/html
     EXPOSE 80
     ```

     This multi-stage Dockerfile uses Node to compile the React app, then copies the static build files into an Nginx image. Nginx will serve the content on port 80. You might add an nginx config to route all requests to `index.html` (for SPA routing) except API calls (which could be proxied if needed, or just let the React client call the backend directly).

   - **Option B: Serve via Spring Boot** – Skip a separate container by adding the React build to the Spring Boot resources. If you followed an approach to embed React in Spring Boot (like copying build files to static or using Maven plugins), then the Spring Boot container will also serve the front-end. In that case, you only need one image (the backend) which includes the frontend resources. This simplifies deployment (one service instead of two) but isn't as scalable (front and back scale together).

   For a clean microservice separation, Option A is preferred: you'll have a backend container and a frontend container.

4. **Prepare a MySQL container (if needed)**: For development or simple deployments, you can run MySQL in a container as well. Use the official MySQL image:

   ```yaml
   services:
     db:
       image: mysql:8
       environment:
         - MYSQL_DATABASE=myappdb
         - MYSQL_ROOT_PASSWORD=example
         - MYSQL_USER=myapp
         - MYSQL_PASSWORD=mypassword
   ```

   Ensure your Spring Boot app's datasource URL and creds match what you configure (use env variables in Spring Boot container to override properties). In production, you might use a managed database service instead of a container, depending on needs.

5. **Use Docker Compose for local multi-container testing**: Create a `docker-compose.yml` that defines services for backend, frontend, and database (and perhaps Elasticsearch if you want). For example:

   ```yaml
   version: "3"
   services:
     backend:
       image: myapp-backend:1.0
       ports:
         - "8080:8080"
       environment:
         - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/myappdb
         - SPRING_DATASOURCE_USERNAME=myapp
         - SPRING_DATASOURCE_PASSWORD=mypassword
       depends_on:
         - db
     frontend:
       image: myapp-frontend:1.0
       ports:
         - "3000:80"
       depends_on:
         - backend
     db:
       image: mysql:8
       environment:
         - MYSQL_DATABASE=myappdb
         - MYSQL_ROOT_PASSWORD=example
         - MYSQL_USER=myapp
         - MYSQL_PASSWORD=mypassword
   ```

   This will start the MySQL database, then the backend (after DB is up), then the frontend. The backend waits on MySQL due to `depends_on` (though you might also need to handle retry logic for DB connection in the app). The frontend here is served on port 3000 (mapped to Nginx's 80). Adjust as needed. Bring everything up with `docker-compose up`. This is a convenient way to simulate the whole stack.

6. **Test containers**: Once all containers are up, test the app:

   - Visit the frontend (http://localhost:3000). It should fetch from backend (which is at `backend:8080` inside Docker network; if your React app was configured with the correct API URL or if served by Nginx, you may need to configure Nginx to forward API calls to the backend service).
   - Alternatively, you can expose the backend on 8080 and hit it directly from the browser or Postman to ensure it's working with the DB container.
   - Check logs of each container with `docker-compose logs` to debug any issues (like backend failing to connect to DB - might need to wait or the connection string must use the service name "db" as host, which we did in `SPRING_DATASOURCE_URL`).

7. **Containerization best practices**: Keep your images lean. For Java, prefer JRE-based images or tools like Jib (that can build optimized layers). For Node, cleaning up dev dependencies after build stage is good. Also, pin versions of images to avoid unexpected changes. Use Docker multi-stage builds to avoid shipping build tools in final image. Also consider security: update base images regularly, and use non-root users. For example, the Nginx Dockerfile can use `USER nginx` after copying files.

Now we have Docker images for all parts of the system. Next, we will see how to deploy these containers on Kubernetes for scaling and reliability.

## Deploying the Application with Kubernetes

Kubernetes (K8s) will orchestrate our Docker containers, allowing us to run and manage them in a cluster environment, with features like self-healing, scaling, and networking. We will create Kubernetes deployments and services for the backend and frontend (and a database if needed).

1. **Set up a Kubernetes cluster**: For testing, you can use a local cluster such as Minikube or Kind (Kubernetes in Docker) ([Getting Started | Spring Boot Kubernetes](https://spring.io/guides/gs/spring-boot-kubernetes#:~:text=You%20will%20also%20need%20a,kind)). Ensure you have `kubectl` installed and configured to talk to your cluster (`kubectl cluster-info` should show it running ([Getting Started | Spring Boot Kubernetes](https://spring.io/guides/gs/spring-boot-kubernetes#:~:text=You%20will%20also%20need%20a,kind))). For production, you might use a cloud provider's Kubernetes service (GKE, EKS, AKS, etc.).

2. **Container Registry**: If your K8s cluster is remote (not your local machine), push your Docker images to a registry that the cluster can pull from (Docker Hub, ECR, etc.). For local Minikube, you can often use local Docker or use Minikube's Docker environment to build inside it. Assuming images are accessible, note their names (e.g., `myrepo/myapp-backend:1.0`).

3. **Create Kubernetes manifests**: Write YAML files for Deployment and Service for each component:

   - **Backend Deployment**: A Deployment ensures a specified number of pods (instances) of the backend are running. Example `backend-deployment.yaml`:
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: myapp-backend
     spec:
       replicas: 2
       selector:
         matchLabels:
           app: myapp-backend
       template:
         metadata:
           labels:
             app: myapp-backend
         spec:
           containers:
             - name: backend
               image: myrepo/myapp-backend:1.0
               ports:
                 - containerPort: 8080
               env:
                 - name: SPRING_DATASOURCE_URL
                   value: jdbc:mysql://myapp-db:3306/myappdb
                 - name: SPRING_DATASOURCE_USERNAME
                   value: myapp
                 - name: SPRING_DATASOURCE_PASSWORD
                   value: mypassword
     ```
     This will run 2 replicas of the Spring Boot app, and define environment variables to connect to the database (assuming a service named `myapp-db` for DB).
   - **Backend Service**: To allow other pods or external clients to reach the backend, create a Service. Example `backend-service.yaml`:
     ```yaml
     apiVersion: v1
     kind: Service
     metadata:
       name: myapp-backend
     spec:
       selector:
         app: myapp-backend
       ports:
         - port: 8080 # service port
           targetPort: 8080 # container port
       type: ClusterIP
     ```
     This makes the backend available at `myapp-backend:8080` internally (ClusterIP). If you need external access (e.g., if front-end is outside cluster), you might use `NodePort` or `LoadBalancer` type.
   - **Frontend Deployment**: Similar approach for React (if using Nginx container):
     ```yaml
     kind: Deployment
     metadata: { name: myapp-frontend }
     spec:
       replicas: 1
       selector: { matchLabels: { app: myapp-frontend } }
       template:
         metadata: { labels: { app: myapp-frontend } }
         spec:
           containers:
           - name: frontend
             image: myrepo/myapp-frontend:1.0
             ports:
             - containerPort: 80
       ---
     kind: Service
     metadata: { name: myapp-frontend }
     spec:
       selector: { app: myapp-frontend }
       ports:
       - port: 80
         targetPort: 80
       type: LoadBalancer  # to expose externally
     ```
     This service as LoadBalancer will get an external IP (in cloud) or you can use NodePort on local cluster. Once exposed, users can access the React app via that IP. The React app will then make calls to the backend. Since the React app is inside cluster as well, it might call the backend via the internal service name. If the React code is still pointing to, say, `localhost:8080` it won't work in cluster. So ensure for production build, the React app's API calls point to the backend service name (e.g., change API URL to `http://myapp-backend:8080/api/...` or use relative paths if served together). If served separately, consider setting an environment variable during the Docker build for the API endpoint.
   - **MySQL Deployment/Service**: If not using an external DB, deploy MySQL to the cluster. Typically use a PersistentVolume for data. Kubernetes has a simpler way using StatefulSets for databases. But a quick setup:
     ```yaml
     kind: Deployment
     metadata: { name: myapp-db }
     spec:
       template:
         spec:
           containers:
           - name: mysql
             image: mysql:8
             env:
             - name: MYSQL_DATABASE  value: myappdb
             - name: MYSQL_ROOT_PASSWORD value: example
             - name: MYSQL_USER value: myapp
             - name: MYSQL_PASSWORD value: mypassword
             ports: - containerPort: 3306
     ---
     kind: Service
     metadata: { name: myapp-db }
     spec:
       ports: - port: 3306
       selector: { app: myapp-db }
       clusterIP: None  # headless, or could omit for ClusterIP
     ```
     In production, you'd use a PersistentVolumeClaim and possibly a StatefulSet to keep data between restarts.

4. **Apply the manifests**: Use `kubectl apply -f backend-deployment.yaml`, etc., for each file or combine them. Kubernetes will pull the images from the registry and start the pods. You can check status with `kubectl get pods` and `kubectl describe pod <name>` if something isn't running. If all goes well:

   - `kubectl get deployments` should show desired and available replicas matching (e.g., 2/2 for backend).
   - `kubectl get svc` should show the services. If the frontend service is LoadBalancer, check `kubectl get svc myapp-frontend -o json` for an IP (with Minikube, you use `minikube service myapp-frontend` to open it).
   - You might also generate YAML using kubectl itself for quick setups (e.g., `kubectl create deployment demo --image=springguides/demo --dry-run=client -o yaml > deployment.yaml`) ([Getting Started | Spring Boot Kubernetes](https://spring.io/guides/gs/spring-boot-kubernetes#:~:text=%24%20kubectl%20create%20deployment%20demo,o%3Dyaml)), then edit it. In our case writing custom YAML was straightforward.

5. **Access the application**: Navigate to the frontend's URL (for LoadBalancer, use the external IP; for NodePort, use the node IP and nodePort). The React app should load. It will request the backend API. If everything is configured right (API URL, service names, etc.), you should see the data. If not, use `kubectl logs <backend-pod>` to see if requests are hitting the backend or if there are CORS issues. It might be necessary to tweak CORS allowed origins to the domain of the frontend service.

6. **Scaling and self-healing**: You can scale the backend by changing `spec.replicas` in the Deployment or using `kubectl scale deployment myapp-backend --replicas=3`. K8s will launch more pods, and the service will load-balance between them. If a pod goes down, Deployment will recreate it. Similarly, you can scale the frontend if needed (less common, as it is mostly static files in Nginx).

7. **Ingress (optional)**: Instead of exposing frontend as LoadBalancer and backend separately, you could set up an Ingress controller (like NGINX Ingress or Traefik). An Ingress can route `http://myapp.example.com/` to the frontend service and `http://myapp.example.com/api/*` to the backend service. This provides a single entry point and cleaner URL structure. It also allows adding TLS easily. Ingress requires additional setup, but it's a common practice for production deployments.

8. **Logging on K8s**: Since we configured Elasticsearch (assuming it's accessible), our app should still be sending logs there. In Kubernetes, ensure network connectivity from the pod to ES (you might run ES as a separate service or use a hosted one). Alternatively, often in K8s one would use sidecar logging agents. But since we push directly to Elasticsearch, just verify logs are coming in. Kubernetes will also capture stdout logs; if you didn't push to ES, you'd rely on something like Fluentd to collect them. Our direct approach bypasses the need for a log collector.

9. **Monitor and optimize**: Use Kubernetes dashboards or CLI to monitor resource usage. Set resource requests/limits for pods to help scheduler and for stability (e.g., give the backend certain CPU/memory and set limits). Also configure liveness/readiness probes for the backend container (Spring Boot actuator health endpoint can be used) so K8s knows when the app is ready or if it needs restart.

At this point, your application is deployed on Kubernetes. It can handle more load by increasing replicas, and it's resilient to node/pod failures. The final step is to set up CI/CD to automate the build and deployment process.

## Setting Up CI/CD Pipelines for Automated Deployment

A CI/CD pipeline will automatically build, test, and deploy your application whenever you make changes, ensuring quick and reliable releases. We will outline using Jenkins as an example, but the principles apply to any CI/CD system (GitHub Actions, GitLab CI, etc.).

1. **Version Control Integration**: Ensure your code is in a git repository (e.g., on GitHub or GitLab). CI/CD is triggered by repository changes. For instance, a push to the main branch or a pull request can start the pipeline.

2. **Jenkins setup (or alternative)**: If using Jenkins, install Jenkins on a server or as a Kubernetes pod. Install necessary plugins (Docker, Kubernetes, etc., if needed). In Jenkins, create a Pipeline job that points to your repository. Alternatively, use Jenkins' Blue Ocean to create a pipeline. If using GitHub Actions, you'd create a YAML workflow in your repo (under `.github/workflows`). Both achieve similar tasks.

3. **Define pipeline stages**: Structure the pipeline into stages such as **Build**, **Test**, **Package**, **Dockerize**, and **Deploy**:

   - **Build and Test**: Checkout the repository code. In this stage, run the backend build (e.g., `./mvnw clean verify` if using Maven wrapper, or `mvn clean test`). This compiles the code and runs tests. Also, run frontend build/test if you have any (maybe run `npm install && npm run test -- --watch=false` for Angular or similar for React tests). Ensuring tests pass before proceeding is crucial.
   - **Package**: Package the application (e.g., `mvn package` to get the jar). And build the frontend (`npm run build`). Essentially prepare the artifacts needed for Docker images.
   - **Dockerize**: Use Docker to build images. In Jenkins, you might use a Docker pipeline plugin or just execute shell commands. For example:
     ```groovy
     stage('Docker Build') {
       steps {
         script {
           docker.build("myrepo/myapp-backend:${env.BUILD_NUMBER}")
           docker.build("myrepo/myapp-frontend:${env.BUILD_NUMBER}", "./frontend")
         }
       }
     }
     ```
     This assumes Docker daemon available to Jenkins (you might run Jenkins itself in Docker with access to host Docker, or use Kubernetes build agents). The above builds images and tags them with the build number (or you could use Git commit SHA).
   - **Push to Registry**: After building images, push them to Docker Hub or your registry:
     ```groovy
     stage('Push Images') {
       steps {
         script {
           docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials-id') {
             backendImage.push("${env.BUILD_NUMBER}")
             frontendImage.push("${env.BUILD_NUMBER}")
             // optionally push "latest" tag
             backendImage.push("latest")
             frontendImage.push("latest")
           }
         }
       }
     }
     ```
     This requires credentials (in Jenkins, you store Docker Hub creds and refer to them by ID). In GitHub Actions, you'd use actions like `docker/login-action` and `docker/build-push-action`.
   - **Deploy**: Once images are pushed, you can trigger a deployment. In Jenkins, one approach is using `kubectl` if Jenkins has access to the K8s cluster (you might configure `kubectl` on the Jenkins node, or use a Kubernetes plugin to deploy). For example:
     ```groovy
     stage('Deploy to K8s') {
       steps {
         sh 'kubectl set image deployment/myapp-backend backend=myrepo/myapp-backend:${BUILD_NUMBER} --record'
         sh 'kubectl set image deployment/myapp-frontend frontend=myrepo/myapp-frontend:${BUILD_NUMBER} --record'
       }
     }
     ```
     This updates the images in the existing deployments to the new version, causing Kubernetes to perform a rolling update. Alternatively, you can apply updated YAML manifests. If using GitOps (Argo CD or Flux), you might skip this stage and let the CD tool deploy the new image based on version changes.

4. **Continuous Deployment vs Manual approval**: For production, you might not want every commit to deploy immediately. It's common to deploy to a dev or staging environment automatically, and require a manual approval or tagging for production deployment. Jenkins pipelines and other CI tools allow adding input steps or gated promotions. Decide your workflow (e.g., auto-deploy to a test cluster, manual to prod).

5. **Setting up Jenkins specifics**: In Jenkins, create a Jenkinsfile in your repo that contains the pipeline script (as outlined above). Jenkins will use it on each build. Make sure to configure any needed credentials (Docker registry creds, possibly K8s credentials). You might use a Kubernetes service account token for `kubectl` or have Kubeconfig in Jenkins securely. Cloud-specific: if using GitHub Actions, your workflow would have similar steps using community actions for Maven, Node, Docker, kubectl, etc.

6. **Run the pipeline**: Test the pipeline by pushing a change (even a minor one). The CI should trigger:

   - It compiles and tests code (failing here stops the pipeline, which is good – it won’t deploy broken code).
   - If all tests pass, it builds the containers and pushes them.
   - Then it updates the Kubernetes deployment. Jenkins (or the CI system) should report success or any errors. Use those logs to fix pipeline issues.
   - After a successful deploy, verify on the cluster that the new pods are running (maybe with the new image tag). Also test the application quickly to ensure the new version is working.

7. **Notifications and monitoring**: Configure the pipeline to send notifications on failures or successes (Jenkins can email or Slack, GitHub Actions can post to Slack via webhook, etc.). This keeps the team informed of deployment status. Additionally, monitor the application (with tools like Prometheus, Kibana for logs, etc.) post-deployment to catch any runtime errors.

8. **CI/CD Best Practices**: Keep the pipeline script in version control (like Jenkinsfile or GitHub Actions yml) so it is maintained with code. Use descriptive stage names and echo important info (so logs are readable). Use ephemeral environments for testing if possible (like spin up a test application instance for integration tests). Also, ensure secrets (like passwords, tokens) in pipeline are protected (never log them, store in secure vaults or CI secret store). Automating the pipeline reduces human error and speeds up the release process ([Deploy a Spring-Boot Application in Kubernetes Pod using Jenkins CI/CD Pipeline | CloudIQ Tech](https://www.cloudiqtech.com/deploy-spring-boot-application-in-kubernetes-pod/#:~:text=To%20maximize%20the%20ease%20and,spring%20boot%20application%20in%20K8s)), which is crucial for agile development and DevOps practices.

By implementing CI/CD, every code change goes through the same build/test/deploy steps consistently. For example, our Jenkins pipeline automatically dockerizes the Spring Boot app and deploys it to K8s in one flow ([Deploy a Spring-Boot Application in Kubernetes Pod using Jenkins CI/CD Pipeline | CloudIQ Tech](https://www.cloudiqtech.com/deploy-spring-boot-application-in-kubernetes-pod/#:~:text=Create%20a%20Jenkins%20pipeline%20to,run%20it%20in%20a%20pod)). This means less manual work and faster iterations, allowing you to focus on coding while the infrastructure and pipeline handle the rest.

---

**Conclusion**: Following these steps, we've set up a robust full-stack application. We started from a Spring Boot REST API connected to MySQL and built it out with security (JWT auth). Then we developed a React frontend with Redux to manage state and integrated it with the backend. We added logging for observability, sending logs to Elasticsearch for monitoring. We containerized the application using Docker, making it easy to deploy anywhere. On Kubernetes, we deployed and exposed the app, leveraging the platform's scaling and management features. Finally, we automated the build and deployment using a CI/CD pipeline to ensure continuous delivery of new features. By adhering to best practices at each stage (like proper layering, security, and configuration management), the application is maintainable and scalable. You can further enhance this setup with advanced things like API gateways, service mesh, performance testing, etc., but this guide covers the end-to-end foundation for a production-grade full-stack system. Enjoy building and iterating on your application! ([Getting Started | Building a RESTful Web Service](https://spring.io/guides/gs/rest-service#:~:text=hood,step%20by%20step)) ([Spring Boot RESTful CRUD API Examples with MySQL database](https://www.codejava.net/frameworks/spring-boot/spring-boot-restful-crud-api-examples-with-mysql-database#:~:text=spring.jpa.hibernate.ddl))
