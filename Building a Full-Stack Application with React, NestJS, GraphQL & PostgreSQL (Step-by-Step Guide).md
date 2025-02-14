# Building a Full-Stack Application with React, NestJS, GraphQL & PostgreSQL (Step-by-Step Guide)

_This comprehensive guide walks through designing and developing a production-ready full-stack application using React (with TypeScript) for the frontend, NestJS for the backend, PostgreSQL for the database, and GraphQL as the API layer. We will cover everything from architecture and setup to advanced topics like performance tuning, security, and deployment. Each section provides practical steps, code snippets, and real-world best practices to help **advanced developers** build a robust Product Information Management (PIM) and dynamic pricing system._

## 1. Architecture Overview

In this chapter, we outline the overall architecture of the application and how each technology in the stack interacts with the others. Understanding the big picture will guide our implementation choices in subsequent steps.

### 1.1 Technology Stack and Roles

- **ReactJS (TypeScript)** – Frontend library for building a dynamic user interface. We use React with TypeScript for type-safe component development. The React app will communicate with the backend via GraphQL queries and mutations.
- **NestJS (Node.js with TypeScript)** – Backend framework to build a GraphQL API server. NestJS will use Apollo Server under the hood to handle GraphQL requests, and it structures our server-side logic into modules, services, and resolvers.
- **GraphQL (API Layer)** – Serves as a middleware between frontend and backend, defining a _single endpoint_ for queries and mutations. GraphQL allows the client to request exactly the data it needs and nothing more. This minimizes over-fetching and under-fetching of data, making our API efficient.
- **PostgreSQL** – Relational database for persisting application data. We design the schema to handle product information (PIM) and pricing details. PostgreSQL’s reliability and strong SQL capabilities make it suitable for complex queries and large datasets.

### 1.2 Component Interaction Flow

Let's visualize how these components interact in a typical request-response cycle:

```
Browser (React + TS app)
   ↳ [GraphQL Query/Mutation]
      ↳ NestJS GraphQL Server (Resolvers & Services)
         ↳ PostgreSQL Database (via ORM or Query Builder)
```

1. The **React frontend** sends a GraphQL query or mutation (for example, querying product details or submitting a price update) to the backend.
2. The **NestJS backend** receives the request at a single `/graphql` endpoint. NestJS uses GraphQL resolvers to process the query/mutation, executing business logic in service classes. Resolvers fetch or modify data by calling the database layer (using an ORM like TypeORM or Prisma, or query builder).
3. The **PostgreSQL database** executes the SQL query (e.g., fetch product info, update a price) and returns results.
4. The **NestJS server** packs the data according to the GraphQL schema and returns a JSON response.
5. The **React app** receives the data and updates the UI accordingly.

This unified GraphQL API approach means the client can fetch all needed data in a single round-trip, even if it comes from multiple tables or services. GraphQL acts as the contract between frontend and backend: the schema defines what data clients can request and how the data is structured.

### 1.3 Why GraphQL as Middleware?

Using GraphQL in the middle of our stack brings several advantages:

- **Exact Data Fetching**: The client queries exactly the fields it needs, avoiding the over-fetching that often happens with REST APIs. For example, the frontend can request a product's `name` and `price` without retrieving its entire record.
- **Single Endpoint**: All data interactions happen through a single `/graphql` endpoint. This simplifies client networking and avoids managing multiple REST endpoints for different resources.
- **Efficient Data Loading**: GraphQL can retrieve related resources in one request. For instance, fetching a product and its category and related price adjustments can be done in one query, rather than multiple REST calls. This results in fewer round-trips and faster load times.
- **Strong Typing**: GraphQL schemas are strongly typed. This aligns well with our use of TypeScript on both front and back end, providing end-to-end type safety. The schema serves as a single source of truth for what data is available and its form.
- **Real-Time Capabilities**: Although not covered in depth here, GraphQL supports subscriptions for real-time updates (e.g., price change notifications). This can be handy for live features in pricing or inventory.

In summary, GraphQL provides a precise, flexible API layer ideal for PIM systems where product data can be complex and varied ([Maximizing PIM Efficiency with GraphQL APIs](https://crystallize.com/blog/maximizing-pim-efficiency-with-graphql-apis#:~:text=GraphQL%20APIs%20provide%20precision%20and,what%20you%20need%2C%20nothing%20more)). By structuring our app around GraphQL, we ensure efficient data transfer and a frontend that can easily tailor requests to its needs, improving performance and developer productivity.

### 1.4 Module Overview

We will design the application in a modular way. The main components/modules include:

- **Product Module (PIM)**: Manages product information (names, descriptions, attributes, categories, variants).
- **Pricing Module**: Manages pricing logic (base prices, discounts, dynamic pricing rules, special offers).
- **Auth Module**: Handles authentication and authorization (user login, JWT issuance, roles/permissions).
- **Order/Cart Module** (optional, if extending to e-commerce): For completeness, a real app might include order management, but we will focus on PIM and pricing for this guide.
- **Frontend Modules**: On the React side, we might structure code by feature as well (e.g., Product pages, Pricing dashboard, Admin panel, etc.), using a routing mechanism if needed.

Each NestJS module will correspond to a domain area (e.g., Product, Pricing). This separation keeps code organized and maintainable. Modules in NestJS encapsulate providers (services), controllers/resolvers, and other components, making it easy to reason about features in isolation.

We'll explore each of these pieces in detail as we move forward. Next, let's get our development environment ready for building this application.

## 2. Setting Up the Environment

Before diving into coding, we need to set up our development environment with the necessary tools and project structure. This section covers installation of dependencies, project scaffolding, and best practices for organizing code in a full-stack TypeScript project.

### 2.1 Prerequisites

Ensure you have the following installed on your system:

- **Node.js (LTS version)**: The backend (NestJS) and development tools run on Node.js. Use the Long Term Support version for stability.
- **npm or Yarn**: A package manager to install dependencies. (NestJS CLI uses npm by default, but Yarn or pnpm can also be used.)
- **PostgreSQL**: Install PostgreSQL and ensure you can connect to a local database. Alternatively, use Docker to run a PostgreSQL container for local development.
- **NestJS CLI**: Install globally with `npm install -g @nestjs/cli`. This provides the `nest` command to scaffold and manage the NestJS project.
- **TypeScript**: Although installing NestJS will include TypeScript, it’s good to have the TypeScript compiler (`tsc`) globally available for other tooling.
- **React scaffolding tool**: We can use Create React App or Next.js for our React project. Since we plan to implement Server-Side Rendering (SSR) later for SEO, **Next.js** is a great choice (it has SSR built-in). Ensure you have `npx` available to use Next.js or CRA.

### 2.2 Project Structure

We will set up a **monorepo** style project using a single repository for both frontend and backend. This makes it easier to share code (like TypeScript types or GraphQL fragments) between them. An alternative is separate repos, but for a unified guide, monorepo is convenient:

- **root/** – Root folder of the project (possibly a Git repository).
  - **backend/** – NestJS project (we'll use `nest new backend` to generate this).
  - **frontend/** – React/Next.js project (we'll create this with `npx create-next-app` or similar).
  - **package.json** (optional at root if using a tool like Yarn Workspaces or Nx to manage monorepo).
  - **docker/** (optional: Docker compose files or Dockerfiles for containerization, if any).
  - **README.md** and configuration files (like `.eslintrc`, `.prettierrc` etc. at root if sharing config).

Each sub-project (frontend, backend) will have its own `package.json` and node_modules. This separation ensures clear boundaries: the backend is a Node service, the frontend is a separate Node app (Next.js) that ultimately builds static assets or runs a dev server.

**Organizing the NestJS backend**:
NestJS encourages a modular architecture. Inside `backend/src`, we might have:

- `app.module.ts` – The root module importing all feature modules.
- `modules/` (or feature-named folders like `product/`, `pricing/`, `auth/`) – each containing a module, service, resolver, and related files for that domain.
- `entities/` or `models/` – database models (if using TypeORM these are entity classes; if using Prisma, we will have a schema file).
- `dtos/` – data transfer objects, e.g., for GraphQL inputs or responses (though with GraphQL code-first, DTOs might be our GraphQL object types).
- `utils/` – utility functions, guards, interceptors, etc., if any custom ones are created (for example, a custom decorator for user roles, or an interceptor for logging).
- `main.ts` – NestJS entry file (bootstraps the application).

**Organizing the React frontend**:
In Next.js (if we use it), the structure is slightly opinionated:

- `pages/` – Next.js pages (each automatically becomes a route). We might have `pages/index.tsx`, `pages/products/[id].tsx`, etc.
- `components/` – Reusable UI components.
- `graphql/` – (optional) GraphQL queries/mutations definitions (if using a codegen or keeping them separate).
- `store/` – If using Redux, set up here; or if using React Query, we might not need a dedicated store directory.
- `utils/` – helper functions.
- `styles/` – styling (if using CSS modules or global CSS).
- Next.js handles SSR and webpack config out of the box. If using Create React App instead, we'd have a similar structure but might need additional setup for SSR (CRA doesn't support SSR without ejecting or additional libraries).

### 2.3 Setting Up NestJS (Backend)

Let's initialize the NestJS backend:

1. **Create NestJS Project**: In the root directory, run:
   ```bash
   nest new backend
   ```
   Choose your package manager when prompted. This creates a new NestJS project in the `backend` folder with a basic structure (module, controller, service).
2. **Install GraphQL & Tools**: We will use Apollo Server integration for NestJS. Install the GraphQL module and any ORM:
   ```bash
   cd backend
   npm install @nestjs/graphql @nestjs/apollo apollo-server-express graphql
   ```
   Also, install a PostgreSQL ORM or client. NestJS works smoothly with TypeORM or Prisma. For simplicity, let's use TypeORM:
   ```bash
   npm install @nestjs/typeorm typeorm pg
   ```
   The `pg` package is the PostgreSQL driver. If you prefer Prisma, you would install `@prisma/client` and `prisma` instead, but then you'd manage schema via Prisma Migrate – an advanced topic beyond this guide.
3. **Configure GraphQL Module**: Open `app.module.ts` and import the GraphQL module:

   ```typescript
   import { GraphQLModule } from "@nestjs/graphql";
   import { ApolloDriver, ApolloDriverConfig } from "@nestjs/apollo";
   // ... other imports

   @Module({
     imports: [
       GraphQLModule.forRoot<ApolloDriverConfig>({
         driver: ApolloDriver,
         autoSchemaFile: true, // code-first (generates schema from decorators)
         playground: true, // GraphQL Playground IDE (use false in production)
         context: ({ req }) => ({ req }), // if we need request for auth
       }),
       TypeOrmModule.forRoot({
         type: "postgres",
         host: "localhost",
         port: 5432,
         username: "postgres", // adjust to your local credentials
         password: "postgres",
         database: "pim_app",
         autoLoadEntities: true, // automatically load entities defined
         synchronize: true, // auto sync schema in dev (disable in prod)
       }),
       // ... import our feature modules (to be created)
     ],
     // controllers: [...], (for REST controllers if any)
     // providers: [...],
   })
   export class AppModule {}
   ```

   We configured GraphQL in **code-first** mode. `autoSchemaFile: true` tells Nest to generate the GraphQL schema (SDL) from our TypeScript decorators and classes. This means we'll define object types and resolvers using NestJS decorators (`@ObjectType`, `@Field`, `@Resolver`, etc.), and Nest will output a schema file (or in-memory schema) automatically. This approach ensures our TypeScript models and GraphQL schema stay in sync, avoiding manual SDL writing.

4. **Module Organization**: Create modules for **Product** and **Pricing** (and Auth):

   ```bash
   nest g module product
   nest g service product --no-spec
   nest g resolver product --no-spec
   ```

   The above commands (using Nest CLI generators) will create `product.module.ts`, `product.service.ts`, and `product.resolver.ts`. We passed `--no-spec` to skip creating test files for brevity. Repeat for `pricing` and `auth` modules:

   ```bash
   nest g module pricing
   nest g service pricing --no-spec
   nest g resolver pricing --no-spec

   nest g module auth
   nest g service auth --no-spec
   nest g resolver auth --no-spec
   ```

   Now our backend skeleton has modules for products, pricing, and auth. The CLI also auto-imports these modules into `app.module.ts` if everything is set up correctly.

5. **Configure TypeORM Entities**: In `product` module, we'll create an `entity` for Product (and Category, Variant, etc. as needed) under a new folder `product/entity/`. Similarly for pricing (maybe a Price or Offer entity). We will flesh out the database design in Section 3.

**Best Practice – Configuration**: You might have noticed we hardcoded DB config in TypeOrmModule above. In a real app, use a configuration service or environment variables. NestJS can load a `.env` or use `ConfigModule` to manage sensitive config:

```typescript
Imports: [
  ConfigModule.forRoot({ isGlobal: true }),
  TypeOrmModule.forRootAsync({
    useFactory: async () => ({
      type: "postgres",
      host: process.env.DB_HOST,
      // ...other options
    }),
  }),
  // ...
];
```

This way, we don't commit credentials to code. For this guide, we'll keep things simple, but remember to externalize config for any production deployment.

### 2.4 Setting Up React (Frontend)

Now, let's set up the React frontend. We opt for **Next.js** to leverage its SSR capabilities for SEO. Using Next.js (which is essentially React + Node for SSR) will make it straightforward to implement server-side rendering in Section 5. If SSR was not a concern, Create React App or Vite could be alternatives.

Steps to set up Next.js with TypeScript:

1. **Create Next.js App**: In the root (not inside backend), run:
   ```bash
   npx create-next-app@latest frontend --typescript
   ```
   This will scaffold a Next.js project in the `frontend` directory with TypeScript configured. If prompted, choose the options (you can say "no" to experimental features for now).
2. **Project Structure Overview**: The `frontend` folder will contain:
   - `pages/` – contains index page, api folder (for backendless API routes if needed), and `_app.tsx` (custom app component), `_document.tsx` (document markup).
   - `styles/` – global CSS and Home module CSS.
   - `package.json` – with scripts for dev, build, start, etc.
   - Next.js is already configured for SSR and supports environment variables via `.env.local`.
3. **Install UI and State Libraries**: Decide on state management. We might use **Redux** for global state (especially if multiple components need to share complex state) or **React Query (TanStack Query)** for remote data caching. We will demonstrate with React Query for GraphQL, as it can simplify data fetching and caching logic on the client.
   ```bash
   cd frontend
   npm install @apollo/client graphql    # Apollo Client for GraphQL requests
   npm install @tanstack/react-query    # React Query (optional, for data fetching management)
   ```
   We installed Apollo Client which will allow our React app to interface with the GraphQL API easily. React Query is optional but can integrate with Apollo or fetch calls to manage caching of requests. Alternatively, we could use Apollo Client's built-in caching and state management; Apollo Client itself can often replace the need for Redux in a GraphQL-heavy app.
4. **Configure Apollo Client**: In Next.js, we'll set up Apollo in a way that works with SSR. For example, create `frontend/lib/apolloClient.ts`:

   ```typescript
   import {
     ApolloClient,
     InMemoryCache,
     HttpLink,
     NormalizedCacheObject,
   } from "@apollo/client";
   import { useMemo } from "react";

   let apolloClient: ApolloClient<NormalizedCacheObject>;

   function createApolloClient() {
     return new ApolloClient({
       ssrMode: typeof window === "undefined",
       link: new HttpLink({
         uri: "http://localhost:3000/graphql", // our NestJS GraphQL endpoint
         credentials: "include", // include cookies if using auth
       }),
       cache: new InMemoryCache(),
     });
   }

   export function initializeApollo(initialState: any = null) {
     const _apolloClient = apolloClient ?? createApolloClient();
     // If your page has Next.js data fetching (getStaticProps, etc.), you can hydrate initial state here
     if (initialState) {
       _apolloClient.cache.restore(initialState);
     }
     // For SSG/SSR, always create a new Apollo Client
     if (typeof window === "undefined") return _apolloClient;
     // Create the Apollo Client once in the client
     if (!apolloClient) apolloClient = _apolloClient;
     return _apolloClient;
   }
   ```

   We will use this `initializeApollo` in a custom Next.js App or specific pages to ensure Apollo is available. The key is to point the URI to our NestJS backend. (Note: NestJS by default runs on port 3000; Next.js dev server runs on 3000 as well. So, either run them on different ports, e.g., NestJS on 4000, or configure differently. For this guide, assume NestJS on localhost:4000 and Next.js on 3000, to avoid conflict.)

5. **SSR and Apollo Integration**: Next.js supports SSR per page via `getServerSideProps`. Apollo has examples to pre-fetch data on server and send to client. We might set this up later in Section 5 when focusing on SSR. Initially, we can proceed with CSR (client-side rendering) to verify everything works, then add SSR.
6. **Verify Setup**: Run `npm run dev` in both `backend` and `frontend` folders.
   - NestJS should start on `localhost:3000` by default (we might change it to 4000 if port clash, via an environment or main.ts).
   - Next.js will start on `localhost:3000` (or 3001 if 3000 already taken).
   - Open the Next.js app in a browser (http://localhost:3000). See the default page. You can test a GraphQL query from the React side by modifying `pages/index.tsx` to call the backend (e.g., using Apollo Client to query a test resolver).
   - Also visit `http://localhost:4000/graphql` (or 3000 if not changed) to see the GraphQL Playground provided by Nest (if `playground: true`). You can test a simple query or the built-in `{ __schema { types { name } } }` to see the schema. Right now our resolvers return nothing (default), we will implement them later.

The environment is now ready. Next, we focus on designing the database schema for Product Information Management (PIM) and pricing data.

## 3. Database Design with PostgreSQL

A solid database design is the foundation of our PIM and pricing application. In this section, we design PostgreSQL tables (or entities) to store product information, product variants, categories, prices, discounts, and related data. We aim for a schema that is **normalized** enough to avoid data anomalies but also optimized for the queries we will need (e.g., fetching a product with its variants and current price efficiently).

### 3.1 Requirements for PIM Data Model

Our Product Information Management system should handle:

- **Products**: Each product has core information (name, description, SKU, etc.).
- **Attributes**: Additional details like specifications, brand, dimensions – these could be columns or a separate attribute table if we allow flexible attributes.
- **Categories**: Products can belong to one or multiple categories (for navigation and filtering).
- **Variants**: Many products have variants (same base product but different color, size, etc.). We need to model these so each variant has its own price, stock, etc., but they link to a parent product.
- **Media**: Images or media links for products (one-to-many relationship).
- **Pricing**: Base price for each product or variant, discount rules, special offers, and possibly historical pricing if we track changes.
- **Inventory** (if relevant, though not explicitly asked, but often tied with PIM).
- **Users** (for auth, e.g., admin users who manage the PIM, or customers if building a full system).

To support **dynamic pricing** and offers:

- We may have a table for discounts or promotions that apply to products (e.g., a percentage off during a sale, or volume pricing rules).
- We might have to store competitor pricing or demand data for dynamic pricing algorithms (this could be external inputs rather than DB tables for now).

### 3.2 Entity Design

Let's design a relational schema fulfilling above:

**Product** – represents a product model or family.

- `id` (PK)
- `name`
- `description`
- `sku` (stock-keeping unit, unique per product family if applicable)
- `category_id` (FK to Category, assuming one main category; if many-to-many, use join table)
- ... (other general fields)

**Category** – product categorization.

- `id` (PK)
- `name`
- `parent_category_id` (FK to self, for sub-category hierarchy if needed)

**ProductVariant** – if products have variants, each variant is a sellable unit.

- `id` (PK)
- `product_id` (FK to Product)
- `name` (or variant specific identifier, e.g., "Red - Large")
- `sku` (could be variant-specific SKU)
- `attributes` (could be a JSON column or link to separate tables for variant attributes like color, size)
- `price` (base price, though we might store this in a pricing table; at minimum keep a current price here for quick access)
- `stock` (if tracking inventory)

Alternatively, we could embed the variant concept into product itself by having optional fields for variant attributes if only one level of variant. But a separate table is more flexible.

**ProductAttribute** – optional table if we want to store arbitrary attributes (e.g., a key/value table).

- `id` (PK)
- `product_id` (FK)
- `name` (e.g., "color", "size", "weight")
- `value`

(This could also be done for variants: `ProductVariantAttribute` table linking variant to attributes like color=red, size=XL.)

**Media** – product images, etc.

- `id`
- `product_id` (FK to Product or maybe to ProductVariant if images tied to variants)
- `url`
- `type` (e.g., "image", "video")

**Price (Pricing)** – to handle dynamic pricing, we might separate pricing rules from product:

- `id`
- `product_id` or `product_variant_id` (if pricing can be at variant level; likely variant-level if variants exist)
- `base_price`
- `currency`
- possibly `valid_from` and `valid_to` for time-based pricing (if scheduling price changes)
- other fields for cost, markup, etc. if needed for dynamic strategy.

However, for simplicity, if base price is mostly static, keeping it in the ProductVariant might suffice. We can use a separate **Discount/Offer** table for special pricing conditions.

**Discount** – store active discounts or offers:

- `id`
- `product_id` or `category_id` or `apply_to_all` (some scope of what the discount applies to)
- `type` (e.g., "PERCENTAGE" or "FIXED_AMOUNT" off)
- `value` (e.g., 20 for 20% or $20 off)
- `start_date`, `end_date` (active period)
- `description` (e.g., "Black Friday Sale")

This allows multiple discounts, but the app logic will need to calculate final price combining base price and any applicable discount (ensuring not to stack conflicting promotions, etc.).

**User** – for authentication (admin or regular user if needed):

- `id`
- `email`
- `password_hash`
- `role` (e.g., "ADMIN" or "USER")

**PriceHistory** (optional advanced) – to keep track of price changes or competitor prices:

- `id`
- `product_variant_id`
- `old_price`, `new_price`
- `changed_at`
- Possibly `source` (like "MANUAL" or "COMPETITOR_SCRAPER")

For the sake of this guide, we will implement a simplified model focusing on **Product, ProductVariant, Category, Price (within variant or separate)** to address PIM and dynamic pricing basics.

### 3.3 Implementing Entities in NestJS (TypeORM)

We'll use TypeORM decorators to define these tables as classes in our NestJS application. This allows NestJS to auto-create the database schema (with `synchronize: true` for dev).

In `backend/src/product/entities/product.entity.ts`:

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from "typeorm";
import { ObjectType, Field, ID } from "@nestjs/graphql";
import { ProductVariant } from "./product-variant.entity";
import { Category } from "../../category/entities/category.entity";

@ObjectType() // GraphQL decorator to mark this class as a GraphQL type
@Entity()
export class Product {
  @Field(() => ID)
  @PrimaryGeneratedColumn()
  id: number;

  @Field()
  @Column()
  name: string;

  @Field({ nullable: true })
  @Column({ nullable: true })
  description?: string;

  @Field({ nullable: true })
  @Column({ unique: true, nullable: true })
  sku?: string;

  // Category relationship (many products to one category)
  @ManyToOne(() => Category, (category) => category.products, {
    nullable: true,
  })
  @JoinColumn({ name: "category_id" })
  category?: Category;

  @Field(() => [ProductVariant])
  @OneToMany(() => ProductVariant, (variant) => variant.product)
  variants: ProductVariant[];
}
```

In `backend/src/product/entities/product-variant.entity.ts`:

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
} from "typeorm";
import { ObjectType, Field, ID, Float } from "@nestjs/graphql";
import { Product } from "./product.entity";

@ObjectType()
@Entity()
export class ProductVariant {
  @Field(() => ID)
  @PrimaryGeneratedColumn()
  id: number;

  @Field()
  @Column()
  name: string; // e.g., "Red / Large"

  @Field({ nullable: true })
  @Column({ nullable: true, unique: true })
  sku?: string;

  @Field(() => Float)
  @Column("decimal", { precision: 10, scale: 2 }) // store currency with two decimals
  price: number;

  @Field({ nullable: true })
  @Column({ nullable: true })
  stock?: number;

  @ManyToOne(() => Product, (product) => product.variants, {
    onDelete: "CASCADE",
  })
  @JoinColumn({ name: "product_id" })
  product: Product;
}
```

In `backend/src/product/entities/category.entity.ts` (we can put Category under a separate module, or inside product module if simpler):

```typescript
import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from "typeorm";
import { ObjectType, Field, ID } from "@nestjs/graphql";
import { Product } from "./product.entity";

@ObjectType()
@Entity()
export class Category {
  @Field(() => ID)
  @PrimaryGeneratedColumn()
  id: number;

  @Field()
  @Column({ unique: true })
  name: string;

  @Field(() => ID, { nullable: true })
  @Column({ nullable: true })
  parentCategoryId?: number;

  @OneToMany(() => Product, (product) => product.category)
  products: Product[];
}
```

We decorated these with `@ObjectType` and `@Field` so they become part of the GraphQL schema automatically (code-first approach). For relationships:

- We did not directly expose a `Category` field on `Product` in GraphQL, but rather stored category in DB. We can add `@Field(() => Category, { nullable: true }) category?: Category` in Product class if we want GraphQL to return full category info when querying a product. Alternatively, use a `@ResolveField` in the resolver to fetch category on demand.
- We did expose `variants` on `Product` and `product` on `ProductVariant` for GraphQL because that helps fetching product with variants in one query.

**Note on GraphQL relations**: If we include `Product.variants` as a field, GraphQL can let us query a product and all its variants easily. But this can introduce the N+1 query problem – if we fetch many products and each product loads its variants, we should use joins or batch loading. We will address this in performance section (using `@ResolveField` or DataLoader to avoid multiple DB hits per product).

For **Pricing and Discounts**, we simplified by including `price` on `ProductVariant`. If we wanted a more complex pricing model:

- We could have a `Price` entity (with historical records or tiered pricing), but that complicates querying the "current price".
- We could also store fields like `discountPercent` or `discountPrice` on variant for a currently active discount, but a separate `Discount` entity is cleaner for multiple promotions.

As a simple approach: handle discounts in business logic (e.g., a service method that given a variant, checks if a discount entry exists in a `Discount` table and calculates final price). We can implement a `Discount` entity:

```typescript
@ObjectType()
@Entity()
export class Discount {
  @PrimaryGeneratedColumn() id: number;
  @Field(() => Float)
  @Column("decimal", { precision: 5, scale: 2 })
  value: number; // e.g., 10.00 for $10 or 15 for 15%

  @Field()
  @Column()
  type: "PERCENT" | "FLAT";

  @Column({ nullable: true })
  productId?: number;

  @Column({ nullable: true })
  categoryId?: number;

  @Field()
  @Column()
  startDate: Date;

  @Field()
  @Column()
  endDate: Date;
}
```

We might not expose `Discount` via GraphQL to clients except maybe for an admin UI. Instead, the GraphQL query for product price can incorporate discount logic and return an "effectivePrice".

However, designing GraphQL schema for pricing might involve a type like:

```graphql
type ProductVariant {
  id: ID!
  name: String!
  price: Float! # base price
  finalPrice: Float! # price after discounts (resolver calculated)
  discount: Discount # details of discount applied (if any)
  product: Product!
}
```

We can compute `finalPrice` in a resolver field by checking active discounts. We'll cover that in Section 7 (Optimizing Pricing & Offers).

**Ensure database constraints**: We added a few `unique: true` on SKU and category name. Also CASCADE delete on variant when parent product is deleted. We should consider indexes on foreign keys and any fields frequently filtered (like categoryId, productId in variant, etc.) for performance.

### 3.4 Example Data Model Summary

To solidify the design, here’s how an example product might be stored:

- **Product**: id=1, name="T-Shirt", description="Cotton tee", sku="TSHIRT-BASE", category_id=10 (say category 10 = "Apparel").
- **Category**: id=10, name="Apparel".
- **ProductVariant**:
  - id=101, product_id=1, name="T-Shirt Red - M", sku="TSHIRT-RED-M", price=19.99, stock=100.
  - id=102, product_id=1, name="T-Shirt Red - L", sku="TSHIRT-RED-L", price=19.99, stock=100.
  - id=103, product_id=1, name="T-Shirt Blue - M", sku="TSHIRT-BLUE-M", price=21.99, stock=50 (maybe blue is slightly more expensive).
- **Discount** (if a sale is on):
  - id=500, type="PERCENT", value=10, productId=1, startDate=2025-11-25, endDate=2025-11-30 (10% off this product for Black Friday week).

This structure can efficiently answer questions like:

- "Get product details along with all variants and their prices"
- "List products in a category"
- "Apply a discount to all variants of a product"

Now that the data model is in place, let's build out the NestJS backend with GraphQL resolvers to query and manipulate this data.

## 4. Building a NestJS Backend with GraphQL

In this section, we implement the backend logic: GraphQL schema (via code-first approach), resolvers for queries and mutations, and the supporting services. We also cover implementing authentication/authorization with NestJS (using JWT and Guards) and performance optimizations for the backend (like avoiding N+1 query issues and using efficient database queries).

### 4.1 Defining the GraphQL Schema (Code-First)

Using our entities from Section 3 as a starting point, our GraphQL schema will have types corresponding to those entities. Because we used NestJS GraphQL decorators (`@ObjectType`, `@Field`), much of the schema is auto-generated from the entity classes. However, we often define separate **DTOs** or GraphQL-specific types rather than exposing the entity classes directly, especially for inputs.

For example:

- **Queries**:
  - `products`: list all products or support filtering (e.g., by category).
  - `product(id: ID!)`: get a single product by ID.
  - `productVariants(productId: ID!)`: list variants of a given product (if not nested).
  - Possibly `categories` and `category(id: ID!)`.
  - If needed, `me`: get current user profile (to test auth).
- **Mutations**:
  - `createProduct(input: CreateProductInput!): Product`
  - `updateProduct(id: ID!, input: UpdateProductInput!): Product`
  - `createProductVariant(input: CreateProductVariantInput!): ProductVariant`
  - `updatePrice(variantId: ID!, price: Float!): ProductVariant` (for pricing updates)
  - `applyDiscount(input: DiscountInput!): Discount` (or maybe a mutation that affects product prices temporarily)
  - `login(credentials: AuthInput!): AuthPayload` (for authentication, returns JWT)
  - `register(userInput: UserInput!): User` (if we allow user registration)
- We might also have `deleteProduct`, `deleteVariant` etc., depending on needs.

**Input Types**: In GraphQL, we define input types for mutations:

```typescript
@InputType()
class CreateProductInput {
  @Field() name: string;
  @Field({ nullable: true }) description?: string;
  @Field({ nullable: true }) categoryId?: number;
}
```

Similar for `UpdateProductInput`, `CreateProductVariantInput` (with productId, name, price, etc.), and `AuthInput` (for login credentials).

**Resolver Map**: NestJS will auto-generate the schema from these types and our resolver method signatures. Typically:

- Query resolvers annotated with `@Query(() => ReturnType)`
- Mutation resolvers with `@Mutation(() => ReturnType)`
- Field resolvers with `@ResolveField` for relationships if needed.

Now, let's implement some key parts.

### 4.2 Implementing Resolvers, Queries, and Mutations

We'll focus on the Product and ProductVariant resolvers, as well as Auth resolver for login.

**Product Resolver (product.resolver.ts)**:

```typescript
import {
  Resolver,
  Query,
  Mutation,
  Args,
  ResolveField,
  Parent,
  Int,
} from "@nestjs/graphql";
import { Product } from "./entities/product.entity";
import { ProductService } from "./product.service";
import { CreateProductInput } from "./dto/create-product.input";
import { ProductVariant } from "./entities/product-variant.entity";
import { UseGuards } from "@nestjs/common";
import { GqlAuthGuard } from "../auth/gql-auth.guard"; // assuming we create a GraphQL guard for JWT

@Resolver(() => Product)
export class ProductResolver {
  constructor(private productService: ProductService) {}

  @Query(() => [Product])
  async products(): Promise<Product[]> {
    return this.productService.findAll();
  }

  @Query(() => Product, { nullable: true })
  async product(@Args("id", { type: () => Int }) id: number): Promise<Product> {
    return this.productService.findById(id);
  }

  @Mutation(() => Product)
  @UseGuards(GqlAuthGuard) // only authenticated users (e.g., admin) can create
  async createProduct(
    @Args("input") input: CreateProductInput
  ): Promise<Product> {
    return this.productService.create(input);
  }

  // Field resolver to get variants if not using direct relation
  @ResolveField(() => [ProductVariant])
  async variants(@Parent() product: Product): Promise<ProductVariant[]> {
    return this.productService.findVariants(product.id);
  }
}
```

**Explanation**:

- The `@Resolver(() => Product)` ties this resolver to the `Product` object type. The `product` and `products` methods are marked as `@Query`, making them available as GraphQL queries.
- The `createProduct` is a `@Mutation`. We've secured it with `@UseGuards(GqlAuthGuard)` – a guard we will create that validates JWT and sets `req.user`. This means only authenticated requests can invoke `createProduct` (authorization logic might further check if `user.role === ADMIN` inside the guard or resolver).
- The `@ResolveField` for `variants` is defined to resolve the `Product.variants` sub-field. Since we declared `variants: [ProductVariant]` in the Product entity and also have the relationship, one might think TypeORM can auto-load variants if we use eager relations. But often we disable eager loading to avoid performance issues. Instead, this approach manually fetches variants for a product when requested. This can prevent the N+1 problem when combined with batching (we could use DataLoader inside `findVariants` to batch requests for multiple products, see Section 8.3).

**Product Service (product.service.ts)**:
We should implement methods `findAll`, `findById`, `create`, `findVariants`. Using TypeORM repository:

```typescript
@Injectable()
export class ProductService {
  constructor(
    @InjectRepository(Product) private productRepo: Repository<Product>,
    @InjectRepository(ProductVariant)
    private variantRepo: Repository<ProductVariant>
  ) {}

  async findAll(): Promise<Product[]> {
    // Possibly use relations: ['variants'] if we want to load in one go.
    return this.productRepo.find({ relations: ["variants"] });
  }

  async findById(id: number): Promise<Product> {
    return this.productRepo.findOne({
      where: { id },
      relations: ["variants", "category"],
    });
  }

  async create(input: CreateProductInput): Promise<Product> {
    const product = this.productRepo.create({
      name: input.name,
      description: input.description || null,
    });
    if (input.categoryId) {
      product.category = { id: input.categoryId } as Category;
    }
    const saved = await this.productRepo.save(product);
    return saved;
  }

  async findVariants(productId: number): Promise<ProductVariant[]> {
    return this.variantRepo.find({ where: { product: { id: productId } } });
  }
}
```

For brevity, error handling (like what if product not found) is omitted, but you would typically throw exceptions (which Nest can map to GraphQL errors). Also, `createProduct` should perhaps handle variants in input if needed, but let's assume variants are created separately via another mutation.

**ProductVariant Resolver (could be in product.resolver.ts or separate)**:

```typescript
@Resolver(() => ProductVariant)
export class ProductVariantResolver {
  constructor(private productService: ProductService) {}

  @Mutation(() => ProductVariant)
  @UseGuards(GqlAuthGuard)
  async createProductVariant(
    @Args("productId", { type: () => Int }) productId: number,
    @Args("name") name: string,
    @Args("price", { type: () => Float }) price: number,
    @Args("stock", { type: () => Int, nullable: true }) stock?: number
  ): Promise<ProductVariant> {
    return this.productService.createVariant(productId, { name, price, stock });
  }

  // Possibly a mutation to update price
  @Mutation(() => ProductVariant)
  @UseGuards(GqlAuthGuard)
  async updatePrice(
    @Args("variantId", { type: () => Int }) variantId: number,
    @Args("newPrice", { type: () => Float }) newPrice: number
  ): Promise<ProductVariant> {
    return this.productService.updatePrice(variantId, newPrice);
  }
}
```

And corresponding service methods:

```typescript
async createVariant(productId: number, data: { name: string; price: number; stock?: number }): Promise<ProductVariant> {
  const variant = this.variantRepo.create({
    name: data.name,
    price: data.price,
    stock: data.stock ?? 0,
    product: { id: productId } as Product
  });
  return this.variantRepo.save(variant);
}

async updatePrice(variantId: number, newPrice: number): Promise<ProductVariant> {
  await this.variantRepo.update({ id: variantId }, { price: newPrice });
  return this.variantRepo.findOne({ where: { id: variantId } });
}
```

This allows an authorized user to create a variant for a product and update pricing.

**Category Resolver** (if needed, to query categories and maybe create them):

```typescript
@Resolver(() => Category)
export class CategoryResolver {
  constructor(
    @InjectRepository(Category) private catRepo: Repository<Category>
  ) {}

  @Query(() => [Category])
  async categories(): Promise<Category[]> {
    return this.catRepo.find();
  }
  @Mutation(() => Category)
  @UseGuards(GqlAuthGuard)
  async createCategory(@Args("name") name: string): Promise<Category> {
    const cat = this.catRepo.create({ name });
    return this.catRepo.save(cat);
  }
}
```

We should also consider ensuring category names unique etc., but that's okay for now.

With these resolvers, the GraphQL schema might look like (SDL form):

```graphql
type Query {
  products: [Product!]!
  product(id: Int!): Product
  categories: [Category!]!
}
type Mutation {
  createProduct(input: CreateProductInput!): Product!
  createProductVariant(
    productId: Int!
    name: String!
    price: Float!
    stock: Int
  ): ProductVariant!
  updatePrice(variantId: Int!, newPrice: Float!): ProductVariant!
  createCategory(name: String!): Category!
  login(authInput: AuthInput!): AuthPayload!
}
type Product {
  id: ID!
  name: String!
  description: String
  sku: String
  variants: [ProductVariant!]!
  # category: Category (if we add to object type)
}
type ProductVariant {
  id: ID!
  name: String!
  sku: String
  price: Float!
  stock: Int
  product: Product!
}
type Category {
  id: ID!
  name: String!
  parentCategoryId: ID
  products: [Product!]!
}
```

And input types:

```graphql
input CreateProductInput {
  name: String!
  description: String
  categoryId: Int
}
input AuthInput {
  username: String! # or email
  password: String!
}
```

Now, let's handle **authentication and authorization**.

### 4.3 Authentication and Authorization in NestJS GraphQL

For authentication, we will use JWT (JSON Web Tokens) with Passport.js integration in NestJS. NestJS provides a passport-jwt strategy that can validate a JWT on each request. In GraphQL context, we can't use the typical REST guard directly on a WebSocket or GraphQL request in the same way, but NestJS has a workaround via `GqlAuthGuard` (a custom guard that integrates with GraphQL's context).

**Setup AuthModule**:

- Install required packages: `npm install @nestjs/passport @nestjs/jwt passport passport-jwt bcrypt`.
- Create a User entity (for storing user credentials, e.g., an Admin user who can login to manage products).
- Configure Passport LocalStrategy for login (to validate username/password) and JWTStrategy for protecting routes.

**User Entity and Auth DTO**:

```typescript
// user.entity.ts
@ObjectType()
@Entity()
export class User {
  @Field(() => ID)
  @PrimaryGeneratedColumn()
  id: number;

  @Field()
  @Column({ unique: true })
  username: string;

  @Column()
  password: string; // hashed password, not exposed as Field for GraphQL

  @Field(() => String)
  @Column({ default: "USER" })
  role: string; // e.g., 'ADMIN' or 'USER'
}
```

No GraphQL field for password for security. Role is included if needed for authorization.

**AuthService** (auth.service.ts):

- A method to validate a user (username & password) by checking DB (with bcrypt compare).
- A method to generate JWT (sign with a secret).

```typescript
@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User) private userRepo: Repository<User>,
    private jwtService: JwtService
  ) {}

  async validateUser(username: string, pass: string): Promise<User | null> {
    const user = await this.userRepo.findOne({ where: { username } });
    if (!user) return null;
    const pwMatches = await bcrypt.compare(pass, user.password);
    return pwMatches ? user : null;
  }

  async login(user: User): Promise<{ access_token: string }> {
    const payload = { sub: user.id, username: user.username, role: user.role };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }

  async register(username: string, password: string): Promise<User> {
    const hash = await bcrypt.hash(password, 10);
    const newUser = this.userRepo.create({ username, password: hash });
    return this.userRepo.save(newUser);
  }
}
```

**LocalStrategy & JWTStrategy**:

```typescript
@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy) {
  constructor(private authService: AuthService) {
    super({ usernameField: "username" }); // by default expects username & password
  }
  async validate(username: string, password: string): Promise<any> {
    const user = await this.authService.validateUser(username, password);
    if (!user) throw new UnauthorizedException();
    return user;
  }
}

@Injectable()
export class JwtStrategy extends PassportStrategy(JwtStrategyBase) {
  // assume we imported as JwtStrategyBase from passport-jwt
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: "JWT_SECRET_KEY", // use .env in real app
    });
  }
  async validate(payload: any) {
    // attach user info to request (could fetch from DB if needed)
    return {
      userId: payload.sub,
      username: payload.username,
      role: payload.role,
    };
  }
}
```

We register these in AuthModule:

```typescript
imports: [
  PassportModule,
  JwtModule.register({ secret: 'JWT_SECRET_KEY', signOptions: { expiresIn: '1h' } }),
  TypeOrmModule.forFeature([User]),
],
providers: [AuthService, LocalStrategy, JwtStrategy, AuthResolver, GqlAuthGuard]
```

We include `AuthResolver` (GraphQL resolver for login and maybe register).

**AuthResolver (auth.resolver.ts)**:

```typescript
@Resolver()
export class AuthResolver {
  constructor(private authService: AuthService) {}

  @Mutation(() => AuthPayload)
  async login(@Args("authInput") authInput: AuthInput): Promise<AuthPayload> {
    const user = await this.authService.validateUser(
      authInput.username,
      authInput.password
    );
    if (!user) {
      throw new AuthenticationError("Invalid credentials");
    }
    const token = await this.authService.login(user);
    return { access_token: token.access_token };
  }

  @Mutation(() => User)
  async register(
    @Args("username") username: string,
    @Args("password") password: string
  ): Promise<User> {
    return this.authService.register(username, password);
  }
}
```

We assume `AuthPayload` is a GraphQL type defined as:

```typescript
@ObjectType()
class AuthPayload {
  @Field() access_token: string;
}
```

And `AuthInput` as earlier with username/password.

**GraphQL Guard**:
We need a guard that integrates with GraphQL. Typically:

```typescript
@Injectable()
export class GqlAuthGuard extends AuthGuard("jwt") {
  getRequest(context: ExecutionContext) {
    const ctx = GqlExecutionContext.create(context);
    return ctx.getContext().req;
  }
}
```

This tells the guard to extract the request from GraphQL context and then use the 'jwt' strategy on it (which expects a JWT in Authorization header as Bearer token).

We then use `@UseGuards(GqlAuthGuard)` on protected resolvers (like shown in ProductResolver for `createProduct`, etc.). When this guard passes, we can get `req.user` in our resolvers' context. In NestJS GraphQL, you can get the user by injecting context: e.g., define a custom decorator:

```typescript
export const CurrentUser = createParamDecorator(
  (data, context: ExecutionContext) => {
    const ctx = GqlExecutionContext.create(context);
    return ctx.getContext().req.user;
  }
);
```

Then in resolver: `@Mutation(() => Product) createProduct(@Args('input') input: CreateProductInput, @CurrentUser() user) { ... }`. This way you can use `user.role` to enforce authorization (like only admin can create).

For example:

```typescript
if (user.role !== "ADMIN") {
  throw new ForbiddenException("Only admins can create products");
}
```

This logic can also be put in a custom guard if desired.

**Authorization**: We've partially covered it:

- Use Guards to allow only authenticated calls.
- Use role checks either in guard or inside resolver to restrict certain actions (Authorization).
- For field-level auth, e.g., only certain users can see certain fields, GraphQL supports that via custom directives or just handle in code (not returning data if not allowed).

So far, our approach covers that only logged-in users with correct role can mutate data.

### 4.4 Avoiding N+1 Problems and Optimizing Database Access

GraphQL resolvers, if not careful, can lead to the N+1 query problem: e.g., fetching a list of products then for each product fetching variants triggers separate DB queries for each product (1 query for products + N queries for N products' variants). We should mitigate this:

- Use **join queries** in the ORM to retrieve related data in one go where appropriate.
- Use **DataLoader** pattern to batch requests for related data.

**Using Join/FETCH**: In `findAll()` we did `relations: ['variants']` which tells TypeORM to perform a JOIN and get variants in the same query for all products. This is the easiest fix if the data size is manageable and you always need variants with products. Alternatively, if not always needed, we could lazy load via resolvers but then use DataLoader.

**Using DataLoader**: DataLoader batches and caches requests within a single request cycle ([API with NestJS #28. Dealing in the N + 1 problem in GraphQL](https://wanago.io/2021/02/08/api-nestjs-n-1-problem-graphql/#:~:text=Solving%20the%20N%20%2B%201,problem%20with%20the%20DataLoader)). NestJS doesn’t have it built-in, but we can integrate manually or using community packages. The idea:

- Create a DataLoader for, say, variants by product IDs. It will collect all product IDs for which variants are requested, then perform one query to fetch all variants for those products, then return lists accordingly.
- Use request-scoped providers in NestJS so that each incoming GraphQL request gets its own DataLoader (ensuring caching per request).

Example DataLoader approach:

```typescript
@Injectable({ scope: Scope.REQUEST })
export class DataLoaderService {
  constructor(
    @InjectRepository(ProductVariant)
    private variantRepo: Repository<ProductVariant>
  ) {}

  public readonly batchVariants = new DataLoader<number, ProductVariant[]>(
    async (productIds: number[]) => {
      const variants = await this.variantRepo.findBy({
        product: In(productIds),
      });
      const variantsMap: Record<number, ProductVariant[]> = {};
      variants.forEach((v) => {
        if (!variantsMap[v.product.id]) variantsMap[v.product.id] = [];
        variantsMap[v.product.id].push(v);
      });
      return productIds.map((id) => variantsMap[id] || []);
    }
  );
}
```

Now in the `ProductResolver.variants` resolve field, instead of calling service directly, we use the DataLoader:

```typescript
@ResolveField(() => [ProductVariant])
async variants(@Parent() product: Product, @Context() ctx): Promise<ProductVariant[]> {
  return ctx.dataLoader.batchVariants.load(product.id);
}
```

We must ensure that `ctx.dataLoader` is populated. We can inject `DataLoaderService` in a guard or interceptor to attach it to context, or simpler, use the `context` option in GraphQLModule:

```typescript
GraphQLModule.forRoot({
  // ...
  context: ({ req, res }) => {
    return {
      req,
      res,
      dataLoader: req.locals.dataLoaderService, // one way, or manually instantiate DataLoaderService per request
    };
  },
});
```

A simpler approach is to fetch in one go via TypeORM as shown earlier, which works fine if it's not too heavy. For learning, we mention DataLoader because it's a known solution to GraphQL N+1 issues ([API with NestJS #28. Dealing in the N + 1 problem in GraphQL](https://wanago.io/2021/02/08/api-nestjs-n-1-problem-graphql/#:~:text=Solving%20the%20N%20%2B%201,problem%20with%20the%20DataLoader)).

**Query Complexity & Depth**: GraphQL endpoints can be abused by very deep or complex queries (clients asking for huge nested data or many items). We should safeguard:

- Limit the depth of queries (e.g., using plugins or manual checks).
- Limit the number of items returned (use pagination on list queries).
- Use NestJS's **Complexity** options: NestJS GraphQL has a plugin to estimate query cost. For instance, you can decorate fields with complexity values. In our case, if a field returns a list, you can define complexity as `@Field({ complexity: (options) => options.args.take * options.childComplexity })` etc. Example from NestJS docs:
  ```typescript
  @Query({ complexity: (options: ComplexityEstimatorArgs) => options.args.count * options.childComplexity })
  items(@Args('count') count: number) { ... }
  ```
  This multiplies the complexity by number of items requested.
- Use **Pagination**: For `products` query, in a real scenario, don't return all products without limits. Support args like `limit` and `offset` or cursor-based pagination. That mitigates massive queries.

For this guide, we'll assume manageable data sizes, but in practice, add those constraints.

### 4.5 Performance Techniques Summary

Summarizing some performance optimizations on backend:

- **Efficient Queries**: Use database joins or batch fetching to reduce number of queries ([API with NestJS #28. Dealing in the N + 1 problem in GraphQL](https://wanago.io/2021/02/08/api-nestjs-n-1-problem-graphql/#:~:text=Solving%20the%20N%20%2B%201,problem%20with%20the%20DataLoader)).
- **Indices**: Ensure database indices on search fields (like `product.category_id`, `variant.product_id`) for faster lookups.
- **Caching**: NestJS supports caching responses; however, with GraphQL, caching needs careful handling as mentioned. We might cache certain heavy queries (like a list of products) in memory or Redis. (Be cautious: in GraphQL, interceptors run per field, so naive caching could cache partial results incorrectly ([Caching | NestJS - A progressive Node.js framework](https://docs.nestjs.com/techniques/caching#:~:text=%23%20Auto)). Instead, implement caching in service layer or use query caching at the ORM level or using a library-specific cache.)
- **Concurrency**: The NestJS server can handle many requests, but Node is single-threaded per process. To scale on multi-core machines, run multiple NestJS instances (or use the cluster module) behind a load balancer. We discuss scaling more in Section 9.
- **Profiling**: Use logs or performance monitors to find slow queries. For example, TypeORM has a logging option to print queries and times. If a resolver is slow, check if it's doing more DB calls than expected.

With our backend implemented, next we focus on the frontend development, creating a React UI that interacts with this GraphQL API.

## 5. Frontend Development with ReactJS and TypeScript

The frontend is built with React and TypeScript, giving us a powerful and type-safe way to create user interfaces. In this section, we will develop the UI to manage products and pricing. We'll emphasize efficiency through reusable components, manage client-side state and server data, and implement Server-Side Rendering (SSR) to improve SEO for product pages.

### 5.1 Laying Out the UI Structure

Our application likely has the following pages or views:

- **Home Page**: Overview or dashboard (maybe a list of products or summary metrics).
- **Product List Page**: Displays a list of products (with ability to filter by category, search, etc.).
- **Product Detail Page**: Shows product information, variants, and pricing details. If admin, can edit; if general user, can just view.
- **Pricing Management Page** (optional): A page focused on adjusting prices or applying discounts.
- **Login Page**: For authentication (if needed for admin access).
- **Maybe Category Pages**: If presenting products to end-users by category.

Using Next.js, many of these will correspond to files in `pages/` directory:

- `pages/index.tsx` – could be home or redirect to products.
- `pages/products/index.tsx` – product list page.
- `pages/products/[id].tsx` – dynamic route for product detail.
- `pages/login.tsx` – login page.
- Possibly an API route for any serverless functions (but not needed since we have NestJS for backend).

We should also set up a layout component for consistent header/nav across pages. Perhaps a simple admin dashboard layout with navigation links (Products, Categories, etc.).

### 5.2 Reusable Components and UI Efficiency

To avoid repeating code, identify common components:

- **ProductCard**: A component to display a product summary (name, maybe image, price range).
- **ProductForm**: A form for creating/editing a product (with fields for name, description, category).
- **VariantTable**: Displays a table of variants for a product, with columns for variant name, price, stock, and maybe an edit button.
- **PriceEditor**: Component that allows editing price (for admin) inline or in a modal.
- **CategorySelector**: A dropdown or tree to pick a category for a product.
- **DiscountForm**: For adding a discount, if that’s a feature in UI.

Using TypeScript with React ensures these components have well-defined props interfaces, which helps catch mistakes at compile time.

Example: Define a type for Product (matching GraphQL type):

```typescript
// types.ts (frontend)
export interface Product {
  id: string;
  name: string;
  description?: string;
  sku?: string;
  variants: ProductVariant[];
}

export interface ProductVariant {
  id: string;
  name: string;
  sku?: string;
  price: number;
  stock?: number;
}
```

We might generate these types automatically using a GraphQL code generator (GraphQL Code Generator can take the schema or queries and produce TS types). But doing it manually for understanding is fine here.

**Building Product List Page**:
File: `pages/products/index.tsx`

```tsx
import { useQuery, gql } from "@apollo/client";
import Link from "next/link";

const PRODUCTS_QUERY = gql`
  query GetProducts {
    products {
      id
      name
      sku
      variants {
        id
        price
      }
    }
  }
`;

export default function ProductListPage() {
  const { data, loading, error } = useQuery(PRODUCTS_QUERY);

  if (loading) return <p>Loading products...</p>;
  if (error) return <p>Error loading products.</p>;

  const products = data.products;
  return (
    <div>
      <h1>Products</h1>
      <Link href="/products/new">
        <button>Create New Product</button>
      </Link>
      <ul>
        {products.map((prod: Product) => (
          <li key={prod.id}>
            <Link href={`/products/${prod.id}`}>
              {prod.name} – {prod.variants.length} variants
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

This uses Apollo's `useQuery` hook to fetch data from our GraphQL API. The query asks for all products with id, name, sku, and variant IDs and prices. We might just show number of variants for summary. Each product is linked to its detail page.

**Product Detail Page**:
File: `pages/products/[id].tsx`

```tsx
import { useRouter } from "next/router";
import { useQuery, useMutation, gql } from "@apollo/client";
import { useState } from "react";

const PRODUCT_QUERY = gql`
  query GetProduct($id: Int!) {
    product(id: $id) {
      id
      name
      description
      sku
      variants {
        id
        name
        price
        stock
      }
    }
  }
`;

const UPDATE_PRICE_MUTATION = gql`
  mutation UpdatePrice($variantId: Int!, $newPrice: Float!) {
    updatePrice(variantId: $variantId, newPrice: $newPrice) {
      id
      price
    }
  }
`;

export default function ProductDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const { data, loading, error } = useQuery(PRODUCT_QUERY, {
    variables: { id: Number(id) },
  });
  const [updatePrice] = useMutation(UPDATE_PRICE_MUTATION);

  if (loading) return <p>Loading product...</p>;
  if (error) return <p>Error loading product.</p>;
  if (!data.product) return <p>Product not found.</p>;

  const { product } = data;
  const [editingPriceId, setEditingPriceId] = useState<string | null>(null);
  const [newPrice, setNewPrice] = useState<number>(0);

  const handlePriceEdit = (variantId: string, currentPrice: number) => {
    setEditingPriceId(variantId);
    setNewPrice(currentPrice);
  };
  const handlePriceSave = async (variantId: string) => {
    await updatePrice({
      variables: { variantId: Number(variantId), newPrice: newPrice },
    });
    setEditingPriceId(null);
  };

  return (
    <div>
      <h1>Product: {product.name}</h1>
      <p>{product.description}</p>
      <h3>Variants:</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {product.variants.map((variant: ProductVariant) => (
            <tr key={variant.id}>
              <td>{variant.name}</td>
              <td>
                {editingPriceId === variant.id ? (
                  <input
                    type="number"
                    step="0.01"
                    value={newPrice}
                    onChange={(e) => setNewPrice(parseFloat(e.target.value))}
                  />
                ) : (
                  <>${variant.price}</>
                )}
              </td>
              <td>{variant.stock ?? "-"}</td>
              <td>
                {editingPriceId === variant.id ? (
                  <button onClick={() => handlePriceSave(variant.id)}>
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => handlePriceEdit(variant.id, variant.price)}
                  >
                    Edit Price
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => router.push("/products")}>Back to list</button>
    </div>
  );
}
```

This page fetches a single product by ID, displays details and a list of variants with an inline price editor. The `updatePrice` mutation is called with Apollo which will send the GraphQL mutation to NestJS. Apollo's cache should update the variant's price automatically because we returned the updated price and ID in the mutation (Apollo will merge it into the cache). If not, we might refetch the query after mutation or update cache manually, but Apollo usually can handle simple updates by ID.

We manage some local state for editing which variant's price is being edited.

**State Management**: We used Apollo for remote data. For local UI state (like which price is being edited), the component’s `useState` is fine. If the app grows more complex (e.g., a global cart state or multi-step flows), we could introduce Redux or context for shared state. However, Apollo Client itself can act as a state manager for remote data and even some local data through its cache and reactive variables. Many apps using GraphQL find they don't need Redux at all because Apollo covers a lot:

- Apollo's `InMemoryCache` caches query results, so if multiple components request the same product, it can serve from cache.
- We can also define local resolvers and fields in Apollo cache for client-only state.

**React Query**: If we weren't using Apollo, we could use React Query with fetch calls to GraphQL endpoints, but Apollo is more straightforward for GraphQL.

**Reusable Component Example**: Let's say `VariantTable` is a reusable component to display variants. We partially did that inline, but we could abstract it:

```tsx
// components/VariantTable.tsx
interface VariantTableProps {
  variants: ProductVariant[];
  onEditPrice?: (id: string, currentPrice: number) => void;
  onSavePrice?: (id: string, newPrice: number) => void;
}
const VariantTable: React.FC<VariantTableProps> = ({
  variants,
  onEditPrice,
  onSavePrice,
}) => {
  // similar table code, but calls onEditPrice/onSavePrice props
};
export default VariantTable;
```

Then in ProductDetailPage, use `VariantTable` and pass handlers. This decouples UI from logic.

**Styling**: We haven't covered much styling. We can use basic CSS for simplicity. Next.js by default supports CSS modules or global CSS. For a real app, a component library (like Material-UI or Ant Design) could speed up creating a polished UI. But since focus is on functionality, we'll keep styling minimal.

### 5.3 State Management with Redux or React Query

We touched on this above. Let's discuss when you'd use Redux:

- If the app requires complex state that is not just server data. For example, a multi-tab interface where some client state needs to persist across components (like unsaved form data or a wizard state).
- If multiple components need to respond to global events (like a websocket message or global notifications).
- Redux with Redux Toolkit can be used to manage such state in a structured way.

However, in modern React, context and hooks often suffice for simpler cases, and for server data, React Query or Apollo is preferred.

**React Query usage**: If not using Apollo, one could do:

```tsx
import { useQuery } from "@tanstack/react-query";
const { data } = useQuery(["products"], fetchProducts);
```

Where `fetchProducts` is a function that calls our GraphQL endpoint (using fetch or axios) and returns data. React Query handles caching, refetching, etc. But Apollo is specifically built for GraphQL and gives us the benefit of generating hooks via codegen if desired.

**Redux usage**: If we had Redux, we might have slices like productSlice, userSlice. The components would dispatch actions instead of directly calling mutations, and sagas or thunks would handle calling the GraphQL API, then store results in the Redux store. Apollo simplifies this by skipping the explicit store actions – the Apollo cache is the store for server data.

Given our app's nature (CRUD with GraphQL), Apollo is sufficient. We'll stick with it. We'll mention that if needed, Redux can be added but caution not to duplicate Apollo data in Redux (always choose one source of truth to avoid complexity).

### 5.4 Implementing SSR for SEO Enhancement

One of the requirements is SSR for SEO. React apps are traditionally client-side rendered (CSR), which can be problematic for SEO because search engine crawlers may not execute JS or may do so slowly. SSR ensures the page HTML is fully rendered on the server and delivered to the client, which is beneficial for SEO and performance ([A Comprehensive Guide to Server-Side Rendering in React](https://www.bairesdev.com/blog/server-side-rendering-react/#:~:text=performance%2C%20and%20an%20SEO,of%20components%20on%20the%20server)).

By using Next.js, we've already set the stage for SSR. Next.js will, by default for each page:

- Pre-render it on the server (either at build time for static pages or on each request for dynamic pages, depending on how we configure).
- Serve the HTML to crawlers and users, so content is indexed.

For SSR with data (like our product detail which needs product data from an API), Next.js provides two mechanisms:

- **getServerSideProps**: If a page exports this async function, Next.js will call it on each request (for that page) on the server. We can fetch data inside and return it as props. Then the page component receives those props and is rendered on server with data.
- **getStaticProps** (and getStaticPaths): For static generation at build time (or incremental static regeneration). Possibly for product pages if the product list is known at build time (not likely in an constantly updating store).

Given we have a dynamic PIM, SSR via getServerSideProps is apt for product pages so that search engines see the full product info.

Let's implement SSR for the product detail page:

```tsx
// Still in pages/products/[id].tsx, add below component export:
export async function getServerSideProps(context) {
  const id = context.params.id;
  // We can use Apollo Client on the server to fetch the product
  const apolloClient = initializeApollo();
  await apolloClient.query({
    query: PRODUCT_QUERY,
    variables: { id: Number(id) },
  });
  // Apollo cache now has the data. We pass it to the page via initial Apollo state.
  return {
    props: {
      initialApolloState: apolloClient.cache.extract(),
    },
  };
}
```

We had defined `initializeApollo` earlier to create a client instance. We call the query on server. The result is stored in Apollo's in-memory cache (in Node memory, just for this request). We extract that cache state and send it to the client as `initialApolloState`. Our custom `_app.tsx` (if configured to use Apollo) would use that to hydrate the Apollo cache on the client, so the client doesn't need to re-fetch the data.

We need to modify `pages/_app.tsx` to wrap with Apollo Provider and hydrate:

```tsx
// pages/_app.tsx
import { ApolloProvider } from "@apollo/client";
import { useApollo } from "../lib/apolloClient"; // assume we create a hook that uses initializeApollo with initialState

function MyApp({ Component, pageProps }) {
  const apolloClient = useApollo(pageProps.initialApolloState);
  return (
    <ApolloProvider client={apolloClient}>
      <Component {...pageProps} />
    </ApolloProvider>
  );
}
export default MyApp;
```

Here, `useApollo` calls `initializeApollo(pageProps.initialApolloState)` to get a client with the state, ensuring Apollo client cache is pre-filled with SSR data.

With this setup, when a user (or crawler) requests `/products/1`:

- Next.js runs `getServerSideProps` on server, Apollo fetches product 1 from NestJS GraphQL, gets data.
- Next.js renders `ProductDetailPage` on server with the data available (Apollo's useQuery might actually run on client side normally, but because the cache is already filled from SSR, it should find the data instantly).
- The HTML output contains the product name, description, etc., which is great for SEO (search engine sees the content without needing JS).
- The page is sent, browser loads it, React hydrates, Apollo is in sync with provided data.

**SEO benefits**: SSR ensures meta tags and content are present. We should also set appropriate `<head>` tags, like title and meta description, for each page. Next.js lets us do that via `next/head`. For example, in ProductDetailPage's component:

```tsx
import Head from "next/head";
// ...
<Head>
  <title>{product.name} - MyStore</title>
  <meta
    name="description"
    content={product.description?.substring(0, 150) || "Product details"}
  />
</Head>;
```

This way, each product page has a unique title and meta description which search engines index, improving SEO for product searches.

**Alternate approach**: If we weren't using Next.js, implementing SSR manually is complex (requires Node server to render React, e.g., using `ReactDOMServer.renderToString`). Next.js abstracts that for us. Given the user explicitly mentioned SSR for SEO, our use of Next.js addresses it. They likely expected mention of Next.js since it's a common solution (the Ahrefs article recommended Next.js for SSR).

### 5.5 Frontend Wrap-up

At this point, our frontend can:

- Fetch and display products and variants via GraphQL.
- Allow editing prices (with proper auth; note we didn't implement the auth token usage in Apollo yet).
- SSR for better SEO on product pages.

**Authentication in frontend**: To complete the loop, how does login work? We should have a login page:

- A form that calls the `login` GraphQL mutation with username & password.
- On success, gets a JWT (`access_token`).
- We then store that token (in a cookie or localStorage). For SSR considerations, storing in an HTTP-only cookie is good (set cookie via a response header?), or simply localStorage and include in Apollo client's auth header on each request.

Simplest approach: after login, store token in localStorage, and in ApolloClient, we set an auth link:

```typescript
import { setContext } from "@apollo/client/link/context";
// ...
const httpLink = new HttpLink({ uri: "...", credentials: "include" });
const authLink = setContext((_, { headers }) => {
  // get token from storage
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return {
    headers: {
      ...headers,
      Authorization: token ? `Bearer ${token}` : "",
    },
  };
});
const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
```

This attaches the JWT to every request. The NestJS JWT guard will then validate it. We included `credentials: 'include'` in case we use cookies instead (then you also set `cookie` header accordingly).

We should also handle logout (clear token).

Since focusing on the main theme, we'll assume the developer can handle these standard auth tasks.

With the frontend done, let's implement the domain-specific logic for PIM and dynamic pricing.

## 6. Product Information Management (PIM) Implementation

Now we focus on how to implement a scalable PIM system in our app. Many of the pieces are already laid out: a structured database for product data and a UI to manage it. In this section, we'll detail how to manage product information effectively, especially handling **product variations** and **categorization** which are central to a PIM.

### 6.1 Managing Products and Variations

Our system distinguishes between a "Product" (as a conceptual item or product family) and "Product Variants" (specific purchasable versions of the product). This is a common pattern in PIM: a product may have multiple variants (differing by attributes like size or color), and all share common information like description and category.

**Creating a Product**:
When an admin wants to add a new product:

1. They would fill a form (Product name, description, choose a category, maybe initial variants).
2. Submit via `createProduct` mutation.
3. The server creates a Product entry. If initial variants were allowed in the form, we'd also create those variant entries. If not, the admin can next go to a "Add Variant" form.

Our `createProduct` currently only takes basic fields, so after creating the product, the UI should navigate to that product's page where they can use `createProductVariant` to add variants.

**Ensuring unique fields**: The product SKU or variant SKUs should be unique if used. We set unique in DB for SKU. The service could catch duplicates and throw an error which GraphQL would return as an error message to the client.

**Variant Management**:
We should allow:

- Adding variants (with name, SKU, price).
- Editing variant details (price, stock, maybe name if needed).
- Removing a variant (maybe mutation to delete by id).
  Our backend can have a `deleteVariant(id)` mutation, and the frontend can call it (with a confirmation prompt).

**Listing and Searching**: As products grow in number, an admin UI should allow searching by name or SKU, and filtering by category or other attributes. We can implement GraphQL query arguments for `products` query, e.g., `products(categoryId: Int, search: String)`. The service would then apply a WHERE clause accordingly.

The database should have appropriate indexes (like an index on product name or use full-text search if needed for advanced search) but for now, simple filtering is fine.

**Categories**:

- We have Category entity and `createCategory` mutation. Admin can manage categories (create new, maybe delete or edit).
- The product creation UI should present categories. If categories are hierarchical, perhaps display as nested select options.
- In GraphQL, we can have a `category` field on product to query the category's name directly if needed.

**Bulk Operations** (advanced):
A robust PIM might need import/export or bulk edit. That might be out of scope here but worth noting as an advanced extension.

### 6.2 Handling Product Variations and Attributes

In our design, product variants are separate entries linked to a product. This covers many use-cases (like clothing with size/color variants). However, some products might have multiple dimensions of variation (size and color). Our `ProductVariant.name` currently might encode both ("Red - M"). A better approach is to have structured variant attributes:

- A `VariantAttribute` table that links a variant to an attribute like Color=Red, Size=M.
- A `ProductAttributeDefinition` possibly to define which attributes a product has (e.g., this product varies by Color and Size vs another by Material).

This can get complex (like how Shopify or others do variant options). For simplicity:

- We assume at most one combined variant descriptor (like our `name` covers it), or
- If needed, we extend GraphQL to allow providing attributes as part of variant creation input.

E.g., `CreateProductVariantInput` could include something like:

```graphql
input CreateProductVariantInput {
  productId: Int!
  attributes: [AttributeInput!]! # e.g., [{ name: "Color", value: "Red" }, { name: "Size", value: "M" }]
  price: Float!
  stock: Int
}
```

And the resolver would create a variant and store these attributes in a separate table.

Given complexity, we skip actual implementation, but mention the concept:

- To support multiple variant attributes, design a separate structure for variant attributes.
- Ensure that a combination of attribute values is unique for a given product (so no duplicate variant of same color/size).

### 6.3 Ensuring Scalability in PIM

Scalability considerations:

- **Large number of products**: Use pagination and filtering in queries (which we noted).
- **Many attributes**: If products have dozens of attributes, not all columns can be in one table (you'd exceed practical column counts or have sparse data). Instead a flexible key-value model (like `ProductAttribute` table or JSON field) is used. PostgreSQL's JSONB could store additional attributes. But that complicates querying/filtering (you then need JSON indexes).
- **Variants**: A product could have hundreds of variants (imagine a shoe with many sizes and widths). Our design can handle that as rows in ProductVariant table. We should index `product_id` in ProductVariant for performance (TypeORM does that by default for foreign keys).
- **Caching PIM data**: We might use a cache for frequently accessed product data, especially if it doesn't change often (like product details for fast page loads). E.g., a Redis cache where product data is cached as JSON for quick access. But any update must invalidate the cache.
- **CDN for media**: Product images should ideally be stored in a cloud storage and served via CDN, not directly from the database or NestJS. We would store only URLs in the DB as we planned.

### 6.4 Example Walkthrough

**Adding a new product example**:

- Admin goes to "New Product" page, enters "Smartphone X", description, selects category "Electronics".
- Submits -> GraphQL `createProduct(input:{...})` -> NestJS creates Product (id=42).
- UI navigates to product detail page for id 42, which is empty of variants.
- Admin clicks "Add Variant", enters variant details e.g., "128GB / Black", price $699, stock 50.
- Submit -> GraphQL `createProductVariant(productId:42, name:"128GB/Black", price:699, stock:50)` -> backend creates variant.
- UI shows the variant in the list. Admin adds more variants (256GB/Black, 128GB/Blue, etc.).
- The product page now lists all variants with their prices and stock.

**Editing product info**:

- If we allow editing product details, we would have a mutation like `updateProduct(id, input)` to change name/desc/category. We implement similar in resolver and service. The UI can show an edit form if needed (like a button "Edit Product Info").

**Category management**:

- Admin can add new categories via a form.
- To assign product to categories, either single category or multiple. We did single category field in product (category_id). For multiple categories, we'd need a join table Product_Categories.
- If multiple categories needed, adjust data model accordingly. But one main category is often fine for primary categorization (and others can be tags or additional categorization not implemented here).

Now that the PIM aspects are covered, let's focus on the pricing optimization part.

## 7. Optimizing Pricing and Offers

Dynamic pricing and effective management of discounts/offers is a key feature. We'll implement strategies to adjust prices based on certain rules and ensure our system can handle these changes efficiently.

### 7.1 Dynamic Pricing Strategies

**Dynamic Pricing** means prices can change based on various factors (time, demand, competition, etc.). Implementing this can range from simple rule-based adjustments to complex machine learning models. We'll outline a rule-based approach:

- Schedule-based: e.g., prices of all winter clothes drop by 20% in summer (time-bound discount).
- Stock-based: if inventory is high, lower the price to clear stock; if stock is low and demand is high, price might increase.
- Competitive pricing: if a competitor lowers their price, we might respond by lowering ours (requires external price feed, outside our scope).
- Personalized pricing: not applicable unless we have user data; skip for now.

Our system so far supports:

- Setting a price per variant.
- Defining discounts via a `Discount` entity (which we created conceptually).

To implement dynamic adjustments:

- We could run a background cron job (maybe using NestJS Cron or a separate microservice) that periodically checks conditions and updates prices or creates discount entries.
- For example, a cron that checks products with low stock and high views (assuming we track views) to raise price (like scarcity pricing), or checks time to apply scheduled sales.

In this guide, we'll keep it manual or simple:

- Admin can create a discount via UI (like "10% off on product 42 from date A to B").
- The system will calculate final price by applying active discounts on the fly when querying.

We will implement the logic in the GraphQL resolver for price:
Remember earlier, we considered adding `finalPrice` field to ProductVariant GraphQL type. Let's do that:

```typescript
@ResolveField(() => Float, { name: 'finalPrice' })
async getFinalPrice(@Parent() variant: ProductVariant): Promise<number> {
  // Check if there's an active discount for this product or variant
  const discounts = await this.discountRepo.find({
    where: [
      { productId: variant.product.id, startDate: LessThanOrEqual(new Date()), endDate: MoreThan(new Date()) },
      { categoryId: variant.product.category?.id, startDate: LessThanOrEqual(new Date()), endDate: MoreThan(new Date()) }
    ]
  });
  if (discounts.length === 0) return variant.price;
  // for simplicity, apply the first relevant discount
  const disc = discounts[0];
  if (disc.type === 'PERCENT') {
    return variant.price * (100 - disc.value) / 100;
  } else if (disc.type === 'FLAT') {
    return Math.max(0, variant.price - disc.value);
  }
  return variant.price;
}
```

We would need to inject `Discount` repository and have discount data. The above looks for any discount on the product or on the product’s category that is currently active (startDate <= now <= endDate). If found, and if percent, it reduces accordingly, if flat amount, subtracts value (not going below 0).

This logic executes whenever `finalPrice` field is requested in GraphQL. If performance is a concern (scanning discounts for each variant), we can optimize by caching active discounts in memory or ensure proper DB indexing (e.g., index on productId and date range in Discount table). Since typically number of active discounts is not huge, it's okay.

Alternatively, we could pre-calc final price and store it, but that adds complexity in keeping in sync.

**Example**:
Product variant price $100, there's a 10% off discount -> finalPrice returns $90.

If multiple discounts apply (rarely you'd allow stacking, might choose the best or stack sequentially depending on business rules), our simplistic approach picks first. Real systems might have a priority or not allow overlapping for same product.

### 7.2 Managing Discounts and Special Offers

We'll implement basic CRUD for Discount as well:

- A mutation `createDiscount(input)` to add a discount.
- Perhaps `removeDiscount(id)` to delete or mark expired.

`createDiscount` could be in a DiscountResolver:

```typescript
@Mutation(() => Discount)
@UseGuards(GqlAuthGuard)
async createDiscount(@Args('input') input: DiscountInput): Promise<Discount> {
  const disc = this.discountRepo.create(input);
  return this.discountRepo.save(disc);
}
```

And `DiscountInput` includes productId or categoryId, type, value, dates.

Then the admin UI can have a form to create a discount (e.g., pick product from dropdown or category, type=Percent, value=10, start=...).

When such a discount is active, our `finalPrice` resolver applies it.

We should also notify the frontend to use `finalPrice` field if we want to show discounted prices:
For example, on product page, show both original price and discounted price if applicable:
The GraphQL query for product variant could request both price and finalPrice:

```graphql
variants { id name price finalPrice }
```

Then in UI:

```jsx
<td>
  {variant.finalPrice < variant.price ? (
    <>
      <span style={{ textDecoration: "line-through" }}>${variant.price}</span>{" "}
      <span>${variant.finalPrice}</span>
    </>
  ) : (
    <span>${variant.price}</span>
  )}
</td>
```

This will strike-through original price if a discount is applied.

**Edge cases**:

- If a discount is category-wide, all products in that category get finalPrice adjusted.
- If two discounts apply (one category 10%, one product 5$ off simultaneously), our resolver picks the first match. We might refine to pick max discount or something.
- After discount period, finalPrice should automatically equal price (because discount query won't find an active one).
- Pricing in multi-currency: not addressed here; one could extend variant with currency or have a separate price table for currencies.

### 7.3 Real-time Price Updates (Advanced)

If we wanted changes to price to reflect in real-time on clients:

- We could use GraphQL subscriptions to notify frontends of price changes. For instance, when updatePrice mutation is called, publish an event that any subscribed client (maybe on a product detail page) receives and updates UI.
- NestJS GraphQL supports subscriptions (e.g., with WebSockets). Implementing it would require setting up a PubSub (Apollo has PubSub or use Redis pubsub).
- Out of scope for now, but worth noting as an advanced technique.

So far, we have covered how dynamic pricing can be implemented in our app in a basic form. Next, ensure the app is robust with performance optimizations and security best practices.

## 8. Performance Optimization & Security Best Practices

Building an advanced application means not only implementing features, but also ensuring it performs well under load and is secure against vulnerabilities. In this section, we discuss caching strategies, common security pitfalls to avoid, and specific GraphQL query optimizations.

### 8.1 Caching Strategies

Caching can significantly improve performance and scalability by reducing repetitive work:

- **Server-side caching**: Cache frequently requested data in memory or a fast store like Redis. For example, product list or category list changes rarely, so cache them. NestJS provides an easy caching module which can cache responses globally or per-route ([Caching | NestJS - A progressive Node.js framework](https://docs.nestjs.com/techniques/caching#:~:text=To%20reduce%20the%20amount%20of,to%20all%20endpoints%20globally)). However, as noted, caching GraphQL responses via the built-in interceptor is tricky ([Caching | NestJS - A progressive Node.js framework](https://docs.nestjs.com/techniques/caching#:~:text=%23%20Auto)), because resolvers are executed per field. Instead:
  - Cache at the service level: e.g., implement caching in `ProductService.findAll()` to return cached results if not stale. Use NestJS `cacheManager` to set/get cache by key (like `products_all`).
  - Cache at database/query level: Use a query result cache (TypeORM has query result caching where you can specify cache duration for certain queries).
  - Use an external cache: e.g., store JSON of product list in Redis, update it when products change.
- **Client-side caching**: Apollo Client already caches results. For example, if you query products list, then query product by id, Apollo can serve from cache if data is there. Utilize this fully:
  - Normalize cache: Apollo by default keys items by `id` if the GraphQL type has an `id` field. So queries are normalized. Ensure your `id` fields are consistent.
  - Use cache for optimistic UI: e.g., when updating price, Apollo can optimistically update the UI assuming success, making it feel snappy.
  - Implement HTTP caching for static assets (Next.js will handle caching of built assets automatically).
- **CDN**: If this were a public-facing app, use a CDN in front of your Next.js to cache SSR pages for certain time (if content doesn't change per user). Next.js also allows incremental static regeneration, which can be caching mechanism for pages that update periodically.

**Cache Invalidation**: Always consider how cache is cleared:

- If product data changes (new product or update), we should bust relevant caches. E.g., if we cached `products_all`, clear it after a new product is added.
- This can be done in the service function after saving to DB (just call `cacheManager.del('products_all')` for instance).

**Avoid Overcaching**: Some data like personalized info should not be cached publicly. Also, keep cache TTL reasonable to avoid serving stale prices during a sale, etc.

### 8.2 Security Best Practices

Security is critical. We address several layers:

**Authentication & Authorization**:

- We implemented JWT auth for mutations (and possibly for sensitive queries like viewing user info). Ensure the JWT secret is strong and kept secret. Use HTTPS in production so tokens aren’t intercepted.
- Implement role-based access control: e.g., only admin role can create/update products. We hinted at using `user.role` checks in resolvers.
- For GraphQL, one could also use schema directives for auth (advanced usage: e.g., `@auth(requires: ADMIN)` on schema fields, but with Nest it's often easier to use guards).

**Input Validation**:

- Ensure all inputs are validated to avoid bad data or attacks. NestJS has a ValidationPipe that can validate incoming args (if using class-validators on DTO classes). For example, ensure price is non-negative, names are not too long, etc.
- It prevents malicious input that could cause errors or overflow.

**Avoid Injection Attacks**:

- Because we use an ORM, it handles parameterization, so SQL Injection risk is low (never use string concat to build queries with user input).
- However, if using raw SQL, always parameterize inputs.
- GraphQL queries themselves aren't directly subject to injection the way string queries are, but be careful with any dynamic construction of queries.

**GraphQL Introspection and GraphiQL in production**:

- Turn off Playground (`playground: false`) and introspection in production environment. This prevents attackers from easily discovering your schema and types. Only enable it in dev.
- Apollo Server (and thus Nest’s GraphQL module) has an `introspection: false` option for production.

**Rate Limiting**:

- GraphQL endpoints can be abused with repetitive queries. NestJS has a built-in Rate Limiting guard (if using Fastify or express rate-limit). Consider rate-limiting unauthenticated requests to the GraphQL endpoint to mitigate brute force or spam.
- Also consider complexity limiting as discussed to avoid extremely expensive queries that could DOS the server (like querying a very deep nested structure or huge lists).

**Common Vulnerabilities**:

- **XSS (Cross-site scripting)**: Mostly relevant on the frontend. Since we use React, it escapes content by default. Only risk is if we dangerously set HTML from some source. For example, if product descriptions allow HTML, ensure to sanitize on server or use a library to render safely.
- **CSRF**: If using cookies for auth, be mindful of CSRF. However, if JWT is in Authorization header, CSRF is less of an issue (CSRF mainly targets cookies). Nest can enable CSRF protection if needed.
- **Directory Traversal/Path leaks**: Not much applicable because our server is API only. But if we had file upload for images, ensure to validate file paths, etc.
- **Misconfiguration**: Use Helmet (Nest has `Helmet` middleware) to set security headers on any API responses as needed.

**Encryption**:

- Store passwords hashed (we did with bcrypt). Never store plaintext passwords.
- If storing other sensitive data (like user emails), consider encryption at rest if necessary or at least in transit (HTTPS).
- JWT tokens should be stored securely on client (if in browser, localStorage is okay but can be accessed by JS; an HttpOnly cookie is safer from XSS, but then needs CSRF protection). We could also refresh tokens to limit damage if stolen.

**Testing Security**:

- Use tools or libraries to test for vulnerabilities. e.g., run `npm audit` for known vulnerable packages.
- Consider penetration testing or using OWASP ZAP to scan the running app for issues.

### 8.3 Optimizing GraphQL Queries

To maximize efficiency of GraphQL:

- **Use Aliases and Fragments (client-side)**: Not a server concern, but teaching devs to use GraphQL features to avoid duplicate data fetching. E.g., if two components need product data, better to query once and share via context or fragment.
- **Set Maximum Query Depth/Complexity**: We touched on complexity. NestJS can integrate Apollo's `costAnalysis` or manually define complexity as shown. For example, if we have a query that returns a list, we can annotate complexity. If a query is too expensive, Apollo server can reject it with an error instead of executing ([GraphQL + TypeScript - Complexity | NestJS - A progressive Node.js framework](https://docs.nestjs.com/graphql/complexity#:~:text=simpleEstimator%28,maxComplexity%29)).
  - The NestJS docs example shows using `@Query({ complexity: ... })` to calculate based on args (like count \* childComplexity). We can do similar on our `products` query if it accepted a `limit`.
- **Batching**: We implemented DataLoader which batches DB calls for N+1 fields. Ensure to use it on any heavy relationships. For instance, if we had to fetch product -> category name in a list of products, we could batch load categories by ids.
- **Pagination**: Always prefer queries that return paged results rather than everything. For example, if products query by default returned the first 20 and had arguments for offset, the client can gradually load more. This prevents a single huge query.
- **Avoid requesting too much data**: Educate frontend devs to only ask needed fields. This is a team policy thing. GraphQL gives power to the client, but in a controlled environment (you are building both client and server), ensure queries are optimized. For example, if a list page only needs product name and id, don't also fetch description and all variants until user goes to detail page.

### 8.4 Monitoring and Profiling

To maintain performance and security:

- Use monitoring tools (APM like New Relic, or even simple logs) to track response times of GraphQL queries and frequency. NestJS's logging can be enabled to see slow queries or use the built-in logger for key events.
- Set up health checks (NestJS Terminus can check database connectivity etc. ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=))) to ensure system is up.
- Profile the database: check query plans for heavy queries (use `EXPLAIN ANALYZE` in PostgreSQL for slow queries).
- Simulate high load (using tools like Artillery or JMeter) to see how the app scales. This might surface bottlenecks (like maybe the N+1 issue if DataLoader missing).
- Ensure the Node process has enough memory and look for memory leaks (tools or Chrome DevTools can connect to Node to profile memory). Common leaks could be if we accidentally keep large objects in memory (caches too large without eviction).
- For security, monitor logs for suspicious activities (multiple failed logins could indicate a brute force attempt – implement lockout or at least log them).

By following these practices, we help ensure the application remains performant and secure as it grows.

## 9. Deployment & Scaling

Developing locally is one thing, but deploying the application to a production environment and scaling it for many users is equally important. In this section, we cover setting up CI/CD, deploying to the cloud, and scaling both NestJS and PostgreSQL for high availability.

### 9.1 CI/CD Setup

Continuous Integration/Continuous Deployment (CI/CD) helps in automating tests and deployments:

- **Repository**: Your code should be in a version control system (e.g., GitHub/GitLab).
- **CI pipeline**: Use GitHub Actions, GitLab CI, or Jenkins to set up pipeline steps:
  1. **Install dependencies** for both frontend and backend.
  2. **Run tests** (if you have unit/integration tests; recommended to add for critical logic).
  3. **Build** the applications:
     - Backend: `npm run build` which produces a `dist/` folder (NestJS compiled to JavaScript).
     - Frontend: `npm run build` for Next.js, which outputs a `.next` folder with server-side render bundle and static files. Next.js can also export static pages if configured.
  4. **Run linting** and other static analysis (to maintain code quality).
  5. **Package artifacts**: possibly create a Docker image as part of CI.
- **CD**: Once pipeline passes, deploy:
  - If using a platform like Heroku or Vercel, you can push the code or the platform integrates with Git to auto-deploy.
  - For containerized deployment (common in advanced setups), push the Docker image to a registry and then update the running containers via Kubernetes or similar.

**Dockerization**:

- Create a `Dockerfile` for backend:
  ```Dockerfile
  FROM node:18-alpine
  WORKDIR /app
  COPY backend/package*.json ./
  RUN npm install --production
  COPY backend/dist ./dist
  EXPOSE 3000
  CMD ["node", "dist/main.js"]
  ```
  (In CI, we build dist first, or we can build inside Docker using multi-stage).
- For frontend (Next.js):

  - We can either use Vercel for deployment (optimal for Next.js, it handles SSR hosting).
  - Or Dockerize Next.js too:

    ```Dockerfile
    FROM node:18-alpine as builder
    WORKDIR /app
    COPY frontend/package*.json ./
    RUN npm install
    COPY frontend/. .
    RUN npm run build

    FROM node:18-alpine as runner
    WORKDIR /app
    ENV NODE_ENV=production
    COPY --from=builder /app/package*.json ./
    COPY --from=builder /app/.next ./.next
    COPY --from=builder /app/public ./public
    RUN npm install --only=production
    EXPOSE 3000
    CMD ["npm", "start"]
    ```

    This builds the Next app and then starts it (Next's start script will start an Express-like server for SSR).

- Ensure to configure environment variables in these images, e.g., DB connection strings for backend, so that in production it connects to the cloud DB not localhost.

**Environment configuration**:

- Use distinct config for dev vs prod. For NestJS, perhaps set `synchronize: false` in prod to avoid accidental schema sync (use migrations instead).
- Use a .env or better, a secrets manager, for DB passwords, JWT secrets, etc. CI/CD should inject these securely (most platforms allow setting env vars).

### 9.2 Cloud Deployment Strategies

There are several ways to deploy:

- **IaaS (Infrastructure as a Service)**: e.g., AWS EC2 or DigitalOcean Droplets. You get a VM and run Docker or Node processes. You manage more details like load balancing and scaling.
- **PaaS (Platform as a Service)**: e.g., Heroku, Render.com for backend, and Vercel for frontend. They abstract the infrastructure. For example, you can deploy NestJS on Heroku with the Dockerfile or buildpack; and Next.js on Vercel easily (Vercel is basically serverless for SSR, very convenient).
- **Container orchestration**: e.g., Kubernetes (on AWS EKS, Google GKE, or Azure AKS). Use this when you need fine-grained control and high scale. You'd define deployments for backend and maybe run frontend in a Node container or separate (or even use something like CloudFront+S3 for static if Next was static, but SSR needs a server).
- **Serverless**: NestJS could run in a serverless function environment (with some adaptation, Nest can be made to run in AWS Lambda, etc.). Next.js can export pages to serverless functions as well (e.g., Vercel architecture is serverless Lambdas for each page). Serverless is good for scaling to zero on low load, but might complicate stateful things (like DB connections – you might use a managed DB).

For a straightforward approach:

- Deploy PostgreSQL on a managed service (e.g., Amazon RDS, Heroku Postgres, Supabase, etc.) so you don't worry about installing DB on your server. Managed DB ensures automated backups, scaling vertical or read replicas easily.
- Deploy NestJS API on a service like Heroku or a Docker container on AWS Fargate or DigitalOcean App Platform. These can run your Node app and you can scale by increasing dynos or container count.
- Deploy Next.js on Vercel or as a Node app behind a CDN. If SEO is critical, Vercel is a good choice because it auto optimizes and you get global edge network.
- Setup environment variables on these platforms for anything like `DATABASE_URL`, `JWT_SECRET`, etc.

Make sure the frontend knows how to reach the backend:

- If both are on the same domain different paths (like example.com (frontend) and example.com/api (backend) behind a proxy).
- Or different subdomains (api.example.com and app.example.com), handle CORS: enable CORS in NestJS for the frontend domain. We can do that in main.ts:
  ```typescript
  app.enableCors({
    origin: "https://your-front-domain.com",
    credentials: true,
  });
  ```
  Since we might send cookies or auth headers, allow credentials.
- Next.js, if on Vercel, could use environment var NEXT_PUBLIC_API_URL to call the right URL.

### 9.3 Scaling NestJS and PostgreSQL

**Scaling NestJS (Horizontal Scaling)**:

- Once traffic grows, one instance might not suffice. You can scale vertically (give it more CPU/RAM) up to a point ([Deployment | NestJS - A progressive Node.js framework](https://docs.nestjs.com/deployment#:~:text=Vertical%20scaling%2C%20often%20referred%20to,some%20key%20points%20to%20consider)). But eventually, horizontal scaling (multiple instances) is needed ([How to Scale NestJS Applications: A Case Study of a High-Load Web Analytics Backend | HackerNoon](https://hackernoon.com/how-to-scale-nestjs-applications-a-case-study-of-a-high-load-web-analytics-backend#:~:text=horizontally%20by%20replicating%20the%20backend,on%20multiple%20servers)).
- If using a PaaS like Heroku, you can increase the number of dynos (instances) running your backend. Or in Kubernetes, increase replicas.
- You will need a load balancer to distribute requests to instances. In Kubernetes, it's handled by Service/Ingress. On Heroku, it's automatic with multiple dynos. On AWS, you might put an ELB in front of EC2 instances.
- NestJS is stateless by default (especially since sessions aren't used because we use JWT). So it's easy to have N instances. Just ensure they connect to the same DB and other shared resources.
- File uploads: if any, you can't rely on local disk in a multi-instance scenario. Use cloud storage for that.

**Clustering**:

- Node can fork multiple processes to utilize multiple CPU cores via the `cluster` module or PM2. NestJS can be started in cluster mode (there are articles about using cluster for NestJS to run one process per CPU). This is an alternative to multiple separate instances; on a single machine with 4 cores you could run 4 Nest processes. This improves throughput by parallelism. You still might eventually need multiple machines though.
- Clustering in Node shares the same port, so a master process distributes incoming requests to workers. It's an internal load balancer on the same machine. For example, `node --cpu-count=4 dist/main.js` using Node's cluster can do that. Nest's documentation or community recipes show how to do it. However, it won't scale beyond the machine or provide redundancy if machine goes down.

**Scaling PostgreSQL**:

- Vertical scaling: move to a bigger instance with more CPU/RAM, and possibly faster disk. This can handle more connections or bigger queries.
- Connection pooling: If we get a lot of short queries, the overhead of connecting can be an issue. Use a pooler like PgBouncer to manage connections. Many cloud DBs allow a high number of connections, but Node often keeps a pool of say 10 by default (TypeORM default). Tune pool size to not overload DB.
- Read replicas: If read traffic is heavy (e.g., lots of product queries), one primary can be strained. PostgreSQL can stream replicate to read-only replicas. We can then load balance read queries to replicas. NestJS TypeORM doesn't automatically do that, but you can configure replication in TypeORM's config (there's an option to provide an array of read replicas connection details). Then it will send reads to replicas and writes to primary.
- Caching at DB level: Using something like Redis as a cache for frequent reads can reduce direct DB load.
- Sharding: Typically not needed unless extremely large data (like millions of products beyond one server's capability). Sharding is complex; avoid unless necessary.
- Alternatively, consider **Postgres scaling solutions** like Citus (distributed Postgres) or Yugabyte (if really at huge scale, but those are advanced).

**High Availability**:

- Ensure DB is backed up and can failover. Managed DBs handle failover to a standby if primary fails (with some outage).
- Ensure NestJS instances are in multiple availability zones or at least can restart quickly if one crashes. Use process managers or orchestration that restarts crashed containers.
- Use health checks (as in NestJS Terminus) and have the load balancer remove instances that are unhealthy.

**Scaling the frontend**:

- Next.js on Vercel auto-scales by deploying to edge locations.
- If self-hosting Next.js, you can also run multiple instances behind a load balancer if needed.
- The static assets (JS, CSS) should be served via CDN or at least a caching layer.

### 9.4 Deployment Example

Let's illustrate a possible deployment using widely available services:

- **Database**: Hosted on Heroku Postgres (for example) or AWS RDS Postgres.
- **Backend**: Docker image deployed on AWS Elastic Container Service (ECS) with Fargate. We set it to run 2 tasks (instances) behind an Application Load Balancer. The ALB health-checks `/health` endpoint (which we implement via Terminus to return OK). If one instance fails, ECS replaces it.
- **Frontend**: Deployed on Vercel. It will communicate with the backend via the API URL (we set NEXT_PUBLIC_API_URL to the ALB URL). Vercel ensures global fast delivery.
- **CI/CD**: GitHub Actions workflow builds Docker and pushes to ECR (Elastic Container Registry) for backend, and triggers Vercel deploy for frontend.
- **Scaling**: ECS can auto-scale based on CPU usage or requests (via CloudWatch alarms). PostgreSQL on RDS can have a read replica and promote if master fails.
- **Domain**: Use a custom domain, say `myapp.com`. Point `api.myapp.com` to the ALB for backend, and root or `www.myapp.com` to Vercel (they provide aliases). Configure CORS so that Vercel domain or your domain is allowed to call the API.

This setup would allow the app to handle growing traffic and maintain uptime through redundancy.

## 10. Real-World Case Studies & Advanced Techniques

Finally, let's look at some real-world scenarios and advanced techniques to glean best practices, and discuss how to troubleshoot complex issues that may arise in such a full-stack application.

### 10.1 Lessons from High-Performing Applications

**Case Study: Shopify (PIM & GraphQL)** – Shopify, a major e-commerce platform, uses GraphQL for almost all client-facing APIs. Their PIM system handles millions of products. Key takeaways:

- GraphQL allows Shopify to provide a single flexible API for many clients (web, mobile, third-party apps). By using GraphQL, they've minimized bandwidth usage on mobile and improved performance for admin dashboards that need lots of data but only specific fields.
- They organize data by "Storefront API" and "Admin API", both GraphQL but with different permissions. In our app, we could similarly separate what customers see vs admin capabilities (though smaller scale).
- Shopify's GraphQL design suggests using **connections** (GraphQL edges/nodes) for pagination. Our app might eventually need that if lists grow huge.

**Case Study: Crystallize (Headless commerce + PIM)** – Crystallize is a headless commerce platform that touts GraphQL for PIM. According to their team:

- GraphQL made it easy to deliver fast storefronts by picking only needed data, and their system updates the GraphQL API in real-time as products change.
- They also highlight the importance of real-time updates and omnichannel consistency, which GraphQL subscriptions or on-demand queries facilitate.

**Case Study: Amazon (Dynamic Pricing)** – Amazon is famous for repricing products frequently (often every 10 minutes or so). While their scale is enormous and uses proprietary systems, the principle for us:

- **Automation**: Pricing changes are automated based on rules (inventory, competitor, season). We can gradually introduce automation; e.g., a script that scans for products not selling for 6 months and marks them 20% off.
- **Experimentation**: They A/B test prices to see effects. In our app, one could integrate with an A/B testing service or at least track sales vs price to find optimal prices (beyond our scope, but data collected could be analyzed).
- **Performance**: Changing millions of prices quickly is non-trivial; caching and efficient DB updates matter. For smaller scale, a single SQL to update many products (e.g., `UPDATE product_variant SET price = price * 0.9 WHERE category_id = X`) is faster than updating each item individually. So use SQL power for bulk operations.

**Case Study: High-Load NestJS Service** – The HackerNoon story we referenced described scaling a NestJS analytics service to handle millions of requests per day:

- They found that vertical scaling had limits and went with horizontal scaling by replicating the service on multiple servers. This is standard advice but the story guides that migrating to multiple instances was successful and cost-effective after some trial.
- They also mentioned trying microservices vs monolith trade-offs. For our app, we have a monolith (PIM + pricing in one service). In future, if one part becomes a bottleneck or needs separate scaling, one could split (e.g., move pricing to its own service if it involved heavy computation, or move search to a microservice using Elasticsearch).
- Logging and monitoring were key to identifying bottlenecks (in their case, maybe DB writes or data ingestion). In our case, monitor slow DB queries, etc.

**Case Study: Next.js SSR in Production** – Many companies (like Netflix, TikTok web, etc.) use Next.js for SEO-heavy pages:

- SSR can increase server load, but caching strategies (like static generation or caching rendered HTML) mitigate that. We might consider using Next.js Incremental Static Regeneration for product pages that don't change often – but if prices change dynamically, fully static might be tricky. However, we could regenerate pages every X minutes to update prices (the dynamic part then mostly handled client-side or via revalidation).
- Next.js 13 introduces App Directory and React Server Components which further optimize what loads on server vs client. That could reduce bundle sizes and improve performance.

### 10.2 Advanced Techniques and Future Improvements

A few advanced things we haven't implemented but are worth considering:

- **Microservices & Message Queues**: As app grows, you might split services (PIM, Pricing, Orders, etc.) into separate NestJS apps. They can communicate via events or queues (RabbitMQ or Kafka). For example, when an order is placed in an Orders service, it could send a message to PIM service to decrement stock. This decouples concerns but adds complexity. NestJS has a microservices module and support for various transport layers to build such architecture when needed.
- **CQRS and Event Sourcing**: NestJS supports a CQRS module (Command Query Responsibility Segregation). This is an advanced pattern where write logic (commands) and read logic (queries) are handled separately, possibly with different models. Useful if, say, writing data involves validations and events, but reading data can be optimized into simpler models or caches. If our product data had to be projected into different read models (like a denormalized view for fast search), CQRS could help.
- **GraphQL Federation**: If splitting backend into multiple GraphQL services, Apollo Federation allows composing them into one GraphQL gateway. If PIM and Pricing became separate microservices each with its GraphQL, a gateway could unify the schema. Right now, our app is small enough not to need that, but good to know if expansion happens.
- **Elasticsearch for Search**: For very advanced product search (especially text search on descriptions, or filtering on many attributes), integrating Elasticsearch or a search engine would improve performance. One could sync product data to ES and search there, then use GraphQL to fetch results (or even integrate via GraphQL).
- **AI/Machine Learning for Pricing**: Future pricing optimization might involve ML models predicting optimal price. Those could be integrated via a service call to a prediction API that suggests price changes. The app could then auto-update prices or suggest to admin. Not trivial to implement but something in vogue (AI-driven pricing, as seen in some references).
- **Testing & Quality**: Writing comprehensive tests for each resolver and component is an advanced best practice. Tools:
  - Use Jest (NestJS comes with it) to test services and resolvers (you can do integration tests hitting an in-memory GraphQL server or using a test database).
  - For the frontend, use React Testing Library to test components and perhaps Cypress or Playwright for end-to-end tests (simulate a user creating a product and seeing it appear, etc.).
  - Ensuring these tests run in CI will catch regressions early.

### 10.3 Troubleshooting and Debugging

Some complex issues that might occur and how to handle them:

- **GraphQL Errors**: If a resolver throws an exception (like a DB error or a custom `ForbiddenException`), the GraphQL response will have an `errors` field. Make sure to check those in the client. Apollo by default logs them. You can customize error formatting in Nest to hide internal details in production (so you don't leak stack traces).
- **Database Connection Issues**: If you see timeouts or "too many clients" errors from Postgres:
  - Check connection pool size vs DB max connections. Possibly use a pooler.
  - Ensure connections are closed (TypeORM pool does that automatically, but if using something like Prisma, ensure to destroy properly on shutdown).
  - For scaling, if many Nest instances each with pool of 10 connect to DB, you can exhaust connections. Use a global pooler or adjust.
- **Performance Degradation**: If requests become slow:
  - Profile if it's DB (enable query logging or slow query log on Postgres). Add appropriate indexes if a query is doing sequential scans on large tables.
  - Check memory/CPU on server, maybe need to scale up or out.
  - Look at logs: maybe some error is happening and causing retries or something.
  - Ensure DataLoader is working (e.g., if someone removed the `@ResolveField` approach and started calling DB in a tight loop).
- **Memory Leaks**: Node memory growing could be due to:
  - Too much cached data without eviction (if using in-memory cache).
  - Listeners not removed.
  - Large result sets kept in memory.
  - Use tools to snapshot heap and see objects. Perhaps in dev, use `--inspect` and Chrome DevTools to analyze.
- **Deployment Issues**:
  - Sometimes code works locally but not in production (could be environment differences). Always check environment variables in production logs.
  - If container fails to start, use the platform's logs (e.g., `docker logs` or Heroku logs).
  - Common mistakes: forgetting to run DB migrations on production DB, leading to schema mismatch. Use tools to manage that.
- **SEO Issues**: If after deploying SSR, Google still not indexing:
  - Check robots.txt and meta tags that might inadvertently block crawling.
  - Ensure SSR is truly happening (fetch as Googlebot using tools or check page source for content).
  - Possibly increase SSR cache or performance if pages time-out in rendering (unlikely unless extremely heavy pages).

### 10.4 Continuous Learning and Improvement

Tech stack updates:

- Keep an eye on updates to React (like new hooks or state management improvements), NestJS (new features, maybe improvements in GraphQL module), and PostgreSQL (new indexing features, etc.).
- Encourage code reviews and knowledge sharing in the team to enforce best practices (like preventing any raw SQL usage without careful review, or ensuring all new resolvers consider performance).
- Refactor when necessary: e.g., if product entity grows too large or pricing rules become too complex to handle inline, consider refactoring into smaller services or classes.

By learning from real-world examples and implementing advanced techniques carefully, we can make our full-stack application robust, high-performing, and maintainable in the long run.

### Conclusion

We've built a comprehensive full-stack application using React, NestJS, GraphQL, and PostgreSQL. We started with a high-level architecture, set up our development environment, designed a relational database for product info and pricing, implemented a GraphQL API with NestJS (including authentication and optimization strategies), and created a React frontend with SSR for SEO. We also covered critical aspects of performance, security, deployment, and scaling.

By following this step-by-step guide, an advanced developer should be equipped to create a production-ready application that manages product information and dynamic pricing efficiently, and be prepared to extend it with more advanced features and handle real-world scenarios. Each section of this guide aimed to provide not just instructions, but also reasoning behind choices and references to best practices, which is essential for making informed architectural decisions in your own projects.
