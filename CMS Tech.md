# Overview of Technologies

To build a modern CMS (Content Management System) with advanced capabilities, we leverage a stack of cutting-edge technologies. Each component serves a specific role in the architecture:

## GraphQL

GraphQL is a query language for APIs and a runtime that fulfills those queries with your data. Unlike REST which has fixed endpoints, GraphQL allows clients to request exactly the data they need in a single request ([GraphQL | A query language for your API](https://graphql.org/#:~:text=GraphQL%20is%20a%20query%20language,and%20enables%20powerful%20developer%20tools)). It uses a **strongly-typed schema** to describe available data, enabling introspection and validation. Key GraphQL concepts include:

- **Schema & Types**: Defines object types (e.g., `Post`, `User`) and their fields, queries, and mutations.
- **Queries & Mutations**: Clients send queries to fetch data and mutations to modify data, specifying precisely which fields they want.
- **Resolvers**: Functions on the server that fetch the data for each field in a query.
- **Overfetching/Underfetching Elimination**: Because clients ask for what they need and nothing more, GraphQL avoids the overfetching of data typical in REST ([GraphQL | A query language for your API](https://graphql.org/#:~:text=GraphQL%20is%20a%20query%20language,and%20enables%20powerful%20developer%20tools)). This leads to efficient network usage and optimized performance on diverse clients (web, mobile, etc).
- **Multiple Data Sources**: GraphQL can unify data from multiple backends (databases, microservices, etc.) under one API. It provides a consistent interface even if the underlying data comes from different sources ([GraphQL Overview](https://www.apollographql.com/docs/graphos/get-started/concepts/graphql#:~:text=GraphQL%20provides%20a%20powerful%20layer,into%20a%20single%2C%20consistent%20API)).
- **Tooling**: The introspective nature of GraphQL enables rich tooling (playgrounds, IDE autocompletion, schema documentation) and techniques like caching and persisted queries.

GraphQL’s flexibility makes it ideal for a CMS, where frontends (websites, apps) may each request different subsets of content. For example, a blog CMS can expose a GraphQL API so that a mobile app can fetch smaller images and minimal fields, while a desktop site can request full content in one round trip. We will deep dive into GraphQL's usage in the CMS throughout this document, including schema design, integration with Node.js, and performance considerations.

## Node.js

Node.js is a JavaScript runtime built on Chrome’s V8 engine, designed for server-side development. It allows running JavaScript on the server, enabling **full-stack JS development** using one language for both client and server ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=%E2%9C%A8%20What%20is%20Node,between%20frontend%20and%20backend%20tasks)). Node’s key characteristics:

- **Event-Driven, Non-Blocking I/O**: Node uses an event loop and asynchronous, non-blocking I/O model. This lets it handle many concurrent connections efficiently without multithreading, which is ideal for I/O-heavy workloads like web APIs ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=1.%20Asynchronous%20and%20Non,requests%20simultaneously%20without%20performance%20bottlenecks)). In a CMS context, Node can handle many simultaneous client requests for content without thread-per-request overhead.
- **High Performance**: Powered by V8, Node executes JS code quickly. Its single-threaded nature (with background threads for I/O) means you avoid context-switch overhead and can achieve near real-time performance for applications like chats or real-time editing in a CMS ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=2,streaming%20services%2C%20or%20gaming%20platforms)).
- **NPM Ecosystem**: Node has a massive ecosystem of libraries on **npm**. For our stack, this means access to frameworks like Express (web server), Apollo Server (GraphQL server), Mongoose (MongoDB ORM), and many others to accelerate development ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=4,and%20plugins%20to%20accelerate%20development)).
- **Scalability**: Node apps can scale horizontally by running multiple instances (processes or containers) behind a load balancer. It also supports clustering (running multiple worker processes on a multi-core machine) to utilize all CPU cores. Node’s lightweight concurrency model handles spikes effectively ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=1.%20Asynchronous%20and%20Non,requests%20simultaneously%20without%20performance%20bottlenecks)).
- **JSON-native**: Using JavaScript on the server is convenient when working with JSON, which is the data format for MongoDB and also how GraphQL responses are typically formatted. This synergy reduces impedance mismatch and processing overhead.

In our CMS, Node.js will serve as the platform for implementing the application backend and GraphQL API. We will use Node to define the CMS’s business logic, GraphQL schema/resolvers, and interact with the database and cache.

## OpenResty

OpenResty is a fully-fledged web application server based on Nginx, augmented with Lua JIT (Just-In-Time) compilation for scripting capabilities. Essentially, OpenResty turns Nginx into a powerful platform where developers can run Lua code at the web server layer (['openresty' tag wiki - Stack Overflow](https://stackoverflow.com/tags/openresty/info#:~:text=By%20taking%20advantage%20of%20various,capable%20to%20handle%2010K%2B%20connections)). Important points about OpenResty:

- **Nginx Core**: It bundles the standard Nginx core with many third-party modules. So it inherits Nginx’s high-performance event-driven architecture and can handle thousands of connections with low memory usage.
- **Lua Scripting**: OpenResty’s hallmark is the `lua-nginx-module`, which allows embedding Lua scripts into Nginx configuration. This means you can write dynamic request-handling logic directly in the web server (for tasks like custom authentication, caching logic, request transformations) without needing to proxy to an application server for every task (['openresty' tag wiki - Stack Overflow](https://stackoverflow.com/tags/openresty/info#:~:text=By%20taking%20advantage%20of%20various,capable%20to%20handle%2010K%2B%20connections)).
- **Non-Blocking I/O**: It leverages Nginx’s event model to perform non-blocking I/O with not just HTTP clients but also with backend services (like databases, other APIs) from within the server (['openresty' tag wiki - Stack Overflow](https://stackoverflow.com/tags/openresty/info#:~:text=OpenResty%20aims%20to%20run%20your,MySQL%2C%20PostgreSQL%2C%20Memcached%2C%20and%20Redis)). For example, OpenResty can directly query Redis or MySQL using Lua libraries, handling responses asynchronously.
- **Use Cases**: Commonly used as a **high-performance API gateway, load balancer, or web cache**. In our stack, OpenResty can serve as a reverse proxy in front of the Node.js GraphQL server – handling SSL termination, caching of certain content, request routing, and possibly serving static files. Because it’s essentially Nginx, we can also use it to enforce web-layer security (rate limiting, IP blocking) and improve performance via techniques like microcaching.
- **Performance**: By running logic within Nginx, OpenResty avoids context switching to an application server for certain operations. Lua is lightweight and the integration is efficient, meaning we can build extremely high-throughput systems (OpenResty has been shown to handle 10k+ concurrent connections on modest hardware) (['openresty' tag wiki - Stack Overflow](https://stackoverflow.com/tags/openresty/info#:~:text=By%20taking%20advantage%20of%20various,capable%20to%20handle%2010K%2B%20connections)).

We will explore how to configure OpenResty for our CMS – for example, to cache GraphQL query results for a few seconds to boost performance on repeated requests, or to serve a pre-rendered HTML page from cache. Its installation and integration details follow in later sections.

## MongoDB

MongoDB is a popular NoSQL, document-oriented database that stores data in flexible, JSON-like documents. It eschews the rigid tables-and-rows schema of SQL databases for a more flexible document model:

- **Document Store**: Data is stored as BSON (binary JSON) documents within collections. Each document can have an arbitrary structure, which can evolve over time (fields can be added/removed easily). This fits a CMS where content items may have varying fields or nested structures. For example, a “Post” document can have a field that’s an array of comments (embedded documents).
- **Schema Flexibility**: MongoDB documents have “optional schemas” – you can enforce structure at the application level or via schema validation rules, but the DB itself doesn’t require a fixed schema ([MongoDB - Wikipedia](https://en.wikipedia.org/wiki/MongoDB#:~:text=MongoDB%20is%20a%20source,like%20documents)). This flexibility speeds up development, as we can adjust content models without heavy migrations (useful in agile content iteration).
- **JSON-native & JavaScript**: Being JSON-like means it aligns well with Node/GraphQL, which use JSON formats. Also, MongoDB’s query language uses JSON-style syntax, and it supports running JavaScript on the DB (though that’s less common in modern usage).
- **Powerful Querying**: Supports rich queries, indexing, aggregation pipeline for data analytics, and text search. We can query inside nested structures, which suits complex CMS content (like find all posts where any comment author is “Alice”).
- **High Availability**: MongoDB has built-in replication; a **replica set** is a group of mongod processes that keep copies of the same data, providing redundancy and automatic failover ([Replication - MongoDB Manual v8.0](https://www.mongodb.com/docs/manual/replication/#:~:text=Replication%20,provide%20redundancy%20and%20high%20availability)). If the primary database server goes down, a secondary can take over, ensuring the CMS stays online.
- **Scalability**: For scaling writes and very large data, MongoDB supports **sharding** – partitioning data across multiple servers. Each shard holds a subset of the data, and a router directs queries to the appropriate shard. Sharding, combined with replication, allows the database to handle high throughput and huge data sizes by distributing load ([Sharding - MongoDB Manual v8.0](https://www.mongodb.com/docs/manual/sharding/#:~:text=Sharding%20,sets%20and%20high%20throughput)). In a global-scale CMS, shards could be used to distribute content by region or content type.
- **Use in CMS**: We might use MongoDB to store content entries (articles, pages, user profiles, etc.). Its ability to store complex objects and arrays directly is convenient. For instance, a single content document can include an array of tags or an embedded sub-document for an author profile.

We will cover the installation of MongoDB, data modeling for a CMS, and how to integrate it with Node (using libraries like Mongoose or the official driver). Also, we’ll see how to manage migrations/updates in a schemaless world and ensure performance with proper indexing.

## Redis

Redis is an in-memory data structure store, often used as a cache, message broker, or ephemeral database. It holds data in memory (with optional disk persistence), which makes it extremely fast (sub-millisecond data access). Key features of Redis relevant to our stack:

- **Data Structures**: Redis is more than a plain key-value store. It supports strings, hashes, lists, sets, sorted sets, bitmaps, and more as values. This allows usage like caching HTML fragments, storing session data, counters, queues, pub/sub channels, etc. For example, we could use a Redis list as a queue for background jobs (like sending notifications when content is published), or a hash to cache assembled page data.
- **Caching**: A primary use-case. Because it’s in-memory, Redis is often placed as a cache in front of a database. In our CMS, we might cache the results of expensive GraphQL queries or frequently accessed data (e.g., site settings, top 10 posts) in Redis to avoid frequent database reads. Redis can automatically evict least used entries when memory is full (configurable eviction policies) to make space, making it suitable for caching use.
- **High Throughput**: It can perform a huge number of operations per second (on the order of 100k+ ops/sec even on moderate hardware), which is essential for high-traffic systems. If our CMS experiences a spike in traffic, cached data in Redis can be served very quickly compared to recomputing from the DB each time.
- **Pub/Sub and Streams**: Redis has a publish/subscribe feature useful for real-time features. For example, if the CMS had a live editing feature or notifications, Redis channels could broadcast changes to multiple subscribers (though more relevant to real-time collab than content serving). Streams (a log data structure) can help in event sourcing or activity feeds.
- **Persistence & Durability**: While primarily in-memory, Redis can persist data to disk via snapshots (RDB) or an append-only log (AOF). For a pure cache, persistence might be turned off (for performance), accepting data may be lost on restart. For a message queue or critical data, you’d enable persistence.
- **High Availability**: Redis can be configured in a primary-replica setup and use **Redis Sentinel** for automatic failover. Sentinel monitors the primary and replicas; if the primary fails, Sentinel will promote a replica to primary and direct clients to it ([Understanding Redis High Availability: Cluster vs. Sentinel - Medium](https://medium.com/@khandelwal.praful/understanding-redis-high-availability-cluster-vs-sentinel-420ecaac3236#:~:text=Medium%20medium,replica%20architecture)). Redis also offers a Cluster mode which shards data and provides partition tolerance and failover.
- **Use in CMS**: Besides query caching, Redis could store user session tokens (if our auth is stateful), rate-limiting counters (to throttle abusive clients), or even content that’s computed at runtime (like personalized recommendations) for quick retrieval.

We will detail how to install and configure Redis, and how to integrate it with Node.js (using a Node Redis client) to cache GraphQL responses or other data. We’ll also discuss strategies for cache invalidation in a CMS (e.g., when content is updated, ensuring the cache is updated or cleared).

## AWS (Amazon Web Services)

AWS is our cloud platform of choice for deploying the CMS. It is the world's most comprehensive and widely adopted cloud platform, offering over 200 fully featured services from data centers globally ([What is AWS? - Cloud Computing with AWS - Amazon Web Services](https://aws.amazon.com/what-is-aws/#:~:text=Services%20aws,services%20from%20data%20centers%20globally)). For our purposes, AWS provides the infrastructure (virtual machines, networking, storage) and managed services to run the CMS at scale. Key AWS elements we will use or consider:

- **Compute**: We can use **EC2** (Elastic Compute Cloud) virtual machines to run our Node.js servers, OpenResty, MongoDB, etc., or use **EKS** (Elastic Kubernetes Service) to run containers in a managed Kubernetes cluster. Another option is **AWS Lambda** for serverless functions, but since our stack includes specific server components, we focus on VM or container approaches.
- **Networking**: **VPC (Virtual Private Cloud)** allows isolation of our resources. We’ll create a VPC with subnets (possibly public subnets for load balancers and private subnets for application servers and databases). Security Groups (firewall rules) control traffic – e.g., allow web traffic to the OpenResty/Node servers, but keep MongoDB accessible only from the app servers. AWS’s global infrastructure (multiple regions and AZs) lets us deploy a highly available architecture.
- **Storage & Database**: We might use AWS **EBS** volumes for persistent storage on EC2 (for MongoDB data if self-hosted). Alternatively, AWS offers **DocumentDB** (a MongoDB-compatible managed database) and **ElastiCache** for Redis as managed services. Using those can offload maintenance, but we’ll outline both managed and self-managed approaches.
- **Scaling & HA**: AWS provides **Auto Scaling Groups** for EC2 (automatically add/remove instances based on load), and managed load balancers (**ELB/ALB**). For example, we can put an Application Load Balancer in front of our OpenResty or Node instances to distribute traffic and handle SSL. Auto Scaling can ensure that if traffic increases, new instances launch (with our app Docker container perhaps) to handle the load, and scale down when idle. We’ll discuss how to configure these for the CMS.
- **AWS Services for CI/CD & Monitoring**: We can use **CodePipeline/CodeBuild** or GitHub Actions for CI/CD, **CloudWatch** for logs and metrics, **CloudFront** as a CDN for caching static content, etc. In this guide, we will primarily focus on core deployment, but will mention these where relevant (e.g., CloudWatch for monitoring, CloudFront in scaling).
- **Terraform on AWS**: While not an AWS service, Terraform will interface heavily with AWS APIs to provision resources. This gives us a repeatable infrastructure definition.
- **Cost and Usage**: AWS is pay-as-you-go. We should design the architecture to be cost-efficient (e.g., use appropriate instance types, auto-scaling to zero in dev, use spot instances if suitable for non-critical batch, etc.). We’ll highlight best practices to keep the cloud costs reasonable while maintaining performance and reliability.

AWS provides the backbone on which we’ll deploy our containerized CMS. In the Deployment section, we will walk through best practices of provisioning AWS resources for the stack, setting up networking, and deploying the application using services like EC2, EKS, etc.

## Rancher

Rancher is an open-source container management platform that simplifies deploying and running Kubernetes clusters anywhere (on any cloud or on-prem) ([What is Rancher? | Rancher](https://ranchermanager.docs.rancher.com/#:~:text=Rancher%20is%20a%20Kubernetes%20management,anywhere%20and%20on%20any%20provider)). In our stack, we consider Rancher as a tool to manage our Docker containers and Kubernetes clusters with greater ease and visibility. Key points about Rancher:

- **Multi-Cluster Kubernetes Manager**: Rancher can **provision Kubernetes clusters** on providers (like create an EKS cluster on AWS or spawn VMs and install Kubernetes on them), or it can **import existing clusters** ([What is Rancher? | Rancher](https://ranchermanager.docs.rancher.com/#:~:text=Rancher%20is%20a%20Kubernetes%20management,anywhere%20and%20on%20any%20provider)). This allows a unified control plane for all your clusters. For example, you might have a dev K3s cluster and a prod EKS cluster both managed via one Rancher interface.
- **Unified Authentication & RBAC**: Rancher adds centralized authentication and Role-Based Access Control on top of Kubernetes. This means you can manage user access to all clusters in one place ([What is Rancher? | Rancher](https://ranchermanager.docs.rancher.com/#:~:text=Rancher%20adds%20significant%20value%20on,cluster%20access%20from%20one%20location)). For an organization, that simplifies granting developers or ops personnel the right permissions.
- **UI and UX**: Rancher provides a friendly web UI to view your workloads, nodes, monitoring dashboards, logs, and more. This can be easier for teams to adopt versus purely CLI-based Kubernetes management.
- **App Catalog & Integrations**: Rancher integrates with Helm (through its Application Catalog) making it easy to deploy common applications (like logging or monitoring stacks) on clusters ([What is Rancher? | Rancher](https://ranchermanager.docs.rancher.com/#:~:text=It%20then%20enables%20detailed%20monitoring,automatically%20deploy%20and%20upgrade%20workloads)). It includes **Fleet** for GitOps-style continuous delivery (which can automatically deploy updates to clusters from Git repos) ([What is Rancher? | Rancher](https://ranchermanager.docs.rancher.com/#:~:text=It%20then%20enables%20detailed%20monitoring,automatically%20deploy%20and%20upgrade%20workloads)). This means if we adopt GitOps, Rancher can continuously apply the latest config changes to our CMS deployments.
- **Monitoring and Logging**: Rancher can deploy a **Prometheus** and **Grafana** stack for monitoring clusters with a few clicks ([Monitoring and Alerting - Rancher](https://ranchermanager.docs.rancher.com/integrations-in-rancher/monitoring-and-alerting#:~:text=Prometheus%20lets%20you%20view%20metrics,and%20how%20to%20enable)). It can also ship logs to external systems. This out-of-the-box support saves time in setting up observability.
- **Why Rancher for our CMS**: We plan to containerize the Node.js app, OpenResty, etc. Using Kubernetes ensures scalability and resilience. Rancher will help manage that Kubernetes cluster on AWS, handling aspects like upgrades and node management. It’s particularly useful if our infrastructure spans multiple environments (e.g., dev cluster vs prod cluster) or even multiple cloud providers.
- **Rancher vs DIY Kubernetes**: While one could use EKS or Kubernetes directly, Rancher adds a layer of convenience and multi-cluster capability. It’s very useful for advanced deployments where you might need to orchestrate multiple Docker services (web, API, DB) and want a single pane of glass to operate them.

In this guide, we will illustrate how to set up Rancher on AWS (itself running on a Kubernetes cluster) and then use it to deploy our CMS stack. We will also cover how Rancher’s features (like load balancer services, persistent volumes, etc.) fit into the deployment and scaling of the CMS.

## Terraform

Terraform is an open-source **Infrastructure as Code (IaC)** tool by HashiCorp that allows you to define and provision cloud infrastructure using a declarative configuration language (HCL). It's a critical part of our tech stack for automating and versioning the setup of all the AWS resources and services we need. Key aspects of Terraform:

- **Infrastructure as Code**: Instead of clicking around in AWS console, you write `.tf` files describing resources (servers, networks, databases). Terraform then creates those resources in the correct order, and can modify or destroy them as the code changes. This ensures consistency across environments and enables source control for infrastructure.
- **Cloud Agnostic**: Terraform supports multiple providers (AWS, Azure, GCP, and many others). In our case we focus on AWS, but it's possible to use the same tool to provision, say, DNS records in Cloudflare or infrastructure on another cloud if needed. This multi-cloud capability is useful if our CMS needs resources outside AWS too ([Introduction to Terraform and Infrastructure as Code | NextLink Labs](https://nextlinklabs.com/resources/insights/terraform-infrastructure-as-code#:~:text=DevOps%20in%20making%20provisioning%20new,a%20company%27s%20cloud%20operation%20strategy)).
- **Execution Plan**: Terraform has a plan/apply workflow. You write config, run `terraform plan` to see what changes it will make, then `terraform apply` to enact them. This prevents unintentional changes.
- **State Management**: Terraform keeps a state file of the resources it created. This state can be stored locally or remotely (e.g., in an S3 bucket) for collaboration. It’s important to lock state in teams to avoid concurrent changes.
- **Examples for our CMS**: We will use Terraform to codify:
  - VPC, Subnets, Route Tables, etc (network setup).
  - Security Groups (firewall rules).
  - EC2 Instances or an EKS Cluster for running our containers.
  - Possibly RDS (if we were using a SQL DB) or other managed services. For MongoDB/Redis, if we self-host on EC2 or containers, Terraform still provisions the underlying instances or EBS volumes.
  - Autoscaling groups and Load Balancers (for scaling and HA).
  - IAM roles and policies (for instance permissions, etc.).
- **Repeatability & Environment parity**: With Terraform, we can create identical dev/staging environments with the same config. For example, the same Terraform scripts could set up a staging VPC and cluster that mirrors production, simply by changing variables (like a prefix or number of instances).
- **Collaboration**: The infrastructure config lives in code, which can be code-reviewed and versioned. This reduces configuration drift and ensures everyone knows the expected infrastructure state.

We will provide step-by-step Terraform usage: writing configuration files for the needed AWS resources, running Terraform commands, and applying best practices (like using variables, remote state, and modules for reusability). An example from Rancher’s quick start shows using Terraform to create an EC2 instance and security group for Rancher server ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=1,git%20clone%20https%3A%2F%2Fgithub.com%2Francher%2Fquickstart)) ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=6.%20Run%20)), exemplifying how Terraform automates AWS setup. By the end, you’ll have a code-defined AWS environment ready for the CMS deployment.

## Docker

Docker is an open platform for developing, shipping, and running applications using containerization. Containers package an application and its dependencies into a lightweight, portable unit that can run uniformly across environments. Docker is foundational to our stack for several reasons:

- **Environment Consistency**: With Docker, we can ensure the CMS app, whether running on a developer’s machine, a test server, or in production on AWS, has the **same environment** (same OS libraries, Node version, etc.). This “works on my machine” problem is greatly reduced.
- **Isolation**: Each service (Node.js API, OpenResty, MongoDB, Redis) can run in its own container with defined resource limits and not interfere with others. For instance, we can run multiple Docker containers on a single EC2 instance (like Node container, Redis container, etc.) without them conflicting on dependencies.
- **Immutability & Versioning**: Docker images capture the application at a point in time (including code and runtime). We can version these images (via tags) and roll back if needed. Deployments become simply distributing new images and running containers, which is much faster and less error-prone than configuring servers manually.
- **Scaling & Management**: Containers start quickly and can be easily replicated. Using Kubernetes (with Rancher) or Docker Compose/Swarm, we can scale out additional containers of our Node app to handle load. Docker also makes it easier to deploy microservices or service-oriented architectures.
- **Docker Hub & Base Images**: We can leverage base images like `node:lts-alpine` (a slim Node.js Linux distribution), `openresty/openresty` (official OpenResty image), `mongo` and `redis` images provided by the community. This saves time in setup – e.g., the official MongoDB container comes with the server ready to run.
- **Integration with CI/CD**: Docker fits well with CI/CD pipelines: build an image, test it, and deploy that image. It's atomic and reproducible.

In our CMS project, we will containerize the Node.js GraphQL API server and possibly the OpenResty server as separate services. MongoDB and Redis might also run as containers for dev/testing, though in production we might use managed services or dedicated instances. We will show how to write Dockerfiles (for custom images), how to use Docker Compose for local development to bring up the whole stack, and how these containers are deployed to AWS (either on raw EC2 or within an EKS cluster).

Docker enables us to **“build once, run anywhere”** – package the CMS application and run it in various environments consistently ([Get Docker | Docker Docs
](https://docs.docker.com/get-started/get-docker/#:~:text=Docker%20is%20an%20open%20platform,developing%2C%20shipping%2C%20and%20running%20applications)). This will be evident as we move through development to deployment in the upcoming sections.

---

Now that we have an overview of each technology, the following sections will guide you through setting up each component, integrating them in a cohesive CMS architecture, deploying to AWS, scaling, monitoring, securing, troubleshooting, and following best practices at each step.

# Installation and Setup

In this section, we provide detailed step-by-step instructions to install and set up each component of the tech stack. By the end of this section, you will have a development environment with GraphQL, Node.js, OpenResty, MongoDB, Redis, and necessary tools (Docker, Terraform, Rancher) installed and configured. We will also prepare the AWS environment for deployment.

**Assumptions/Prerequisites**: We assume you have a machine (or VM) with a Unix-like OS (e.g., Ubuntu 20.04+) and you have administrative (sudo) rights on it. For Windows users, using WSL2 or Docker Desktop’s integrated WSL2 backend is recommended for a Unix-like environment, or adapt the commands to Windows equivalents (PowerShell commands for package installation, etc.).

Let's proceed with each component:

## 1. Install Node.js (LTS) and Set Up a GraphQL Project

**Node.js Installation**: For stability, we use the LTS (Long-Term Support) version of Node.js.

1. **Use Node Version Manager (Optional)**: If you prefer, install Node Version Manager (nvm) to easily switch Node versions. On Linux/Mac, you can install nvm via the project’s instructions. For brevity, we’ll use the NodeSource repository method.
2. **Add NodeSource APT repository (Ubuntu/Debian)**: NodeSource provides up-to-date Node binaries. Run the following command to add the NodeSource repo for Node.js LTS (replace `18.x` with the desired major version if needed):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   ```
   This script will add the NodeSource signing key and repository to your system ([how to install a latest version of Nodejs on Ubuntu? - Stack Overflow](https://stackoverflow.com/questions/74879973/how-to-install-a-latest-version-of-nodejs-on-ubuntu#:~:text=The%20current%20LTS%20version%20can,y%20nodejs)).
3. **Install Node.js**: After adding the repo, install Node.js and npm:
   ```bash
   sudo apt-get install -y nodejs
   ```
   This installs Node.js (which includes npm, the Node package manager).
4. **Verify Installation**: Check the versions:
   ```bash
   node -v
   npm -v
   ```
   You should see Node’s version (e.g., v18.x.x) and npm’s version.
5. **Global vs Local Packages**: It’s best to avoid using `sudo npm install -g` for global packages unless necessary. We will install project-specific packages locally within the project directory using npm or yarn.

**GraphQL Project Setup**: Now that Node is installed, let’s scaffold a basic Node.js project for our CMS backend. 6. **Create a Project Directory**: Choose a directory for your project and initialize it:

```bash
mkdir cms-backend && cd cms-backend
npm init -y
```

This creates a `package.json` with default values. 7. **Install GraphQL and Server Library**: For GraphQL in Node, a popular choice is Apollo Server. We’ll use Apollo Server (which runs an Express under the hood) as it’s well-documented. Install Apollo Server and the GraphQL JS library:

```bash
npm install apollo-server graphql
```

This adds dependencies to your project. 8. **Create a simple GraphQL server**: Create a file `index.js` (or `server.js`) and add a minimal Apollo Server example:

```js
const { ApolloServer, gql } = require("apollo-server");
// Example type definitions (schema)
const typeDefs = gql`
  type Query {
    hello: String
  }
`;
// Example resolvers
const resolvers = {
  Query: {
    hello: () => "Hello, CMS World!",
  },
};
// Create and start the Apollo Server
const server = new ApolloServer({ typeDefs, resolvers });
server.listen({ port: 4000 }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

This defines a trivial schema with one query and starts the server on port 4000. 9. **Run the GraphQL Server**: Use Node to start it:

```bash
node index.js
```

You should see a log indicating the server is ready at `http://localhost:4000/`. Open that URL in a browser – Apollo Server’s playground interface appears where you can run `{ hello }` query to test. 10. **Project Structure**: As you proceed, you’ll expand this project with your CMS schema, resolvers, and integration with MongoDB/Redis. It’s good to organize code by feature (e.g., have separate files for type definitions and resolvers, and maybe a folder for database models). For now, we have a working baseline.

_Node and GraphQL are now set up._ We have a simple Node server running GraphQL. Next, we will set up the database and cache.

## 2. Install MongoDB

We’ll install MongoDB Community Edition for development. In production, you might use a managed service or run Mongo in a replica set, but for now a single-node Mongo is sufficient.

### Option A: Install MongoDB Locally (Ubuntu)

1. **Import MongoDB public GPG key**:
   ```bash
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   ```
   (Use the appropriate key for the version you want, e.g., 6.0 which is current stable at this time).
2. **Add MongoDB APT source**:
   ```bash
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   ```
   This assumes Ubuntu 20.04 (focal). Adjust the distribution if on a different version (e.g., bionic for 18.04, jammy for 22.04).
3. **Install the packages**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y mongodb-org
   ```
   This will install the MongoDB server (`mongod`), client (`mongo` shell), and tools.
4. **Start MongoDB service**:
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod  # to start on boot
   ```
   Check status with `systemctl status mongod`. The service should be active (running).
5. **Verify Connectivity**: Run the Mongo shell to ensure it connects:
   ```bash
   mongo
   ```
   By default, it connects to `mongodb://127.0.0.1:27017`. You should get a prompt (`>`). You can run `db.serverStatus().version` to see the version, then type `quit()`.
6. **Enable Authentication (optional for dev)**: By default, MongoDB allows connections without auth only on localhost. It’s recommended to enable access control (create users and require auth) even in dev, to mirror production. To do this, you would edit `/etc/mongod.conf` to set `security.authorization: enabled` and create an admin user. (For now, if just local and secure, you might skip, but be mindful for real deployments).

MongoDB is now running locally. It stores data under `/var/lib/mongodb/` by default.

### Option B: Run MongoDB in Docker (Alternative)

If you prefer not to install directly, you can use Docker:

- Ensure Docker is installed (we will cover Docker in a later step, but if you followed out of order, skip ahead to Docker installation).
- Run:
  ```bash
  docker run -d --name mongodb -p 27017:27017 -v mongo-data:/data/db mongo:6.0
  ```
  This pulls the MongoDB image and runs it, exposing it on the host port 27017 and using a named volume for data persistence. Verify with `docker logs mongodb` and ensure it started. You can then connect using the Mongo shell on the host or from another container.

For continuing the setup, we will assume MongoDB is accessible at least on `localhost:27017`.

## 3. Install Redis

Similarly, we can either install Redis directly or use Docker.

### Option A: Install Redis Locally (Ubuntu)

1. **Install from APT**: Redis is available in Ubuntu’s repository. Install it with:
   ```bash
   sudo apt-get install -y redis-server
   ```
2. **Secure Binding (Optional)**: By default, the Redis config (`/etc/redis/redis.conf`) may bind to `127.0.0.1` which is fine (only local access). Ensure it’s not binding to `0.0.0.0` (which would expose it).
3. **Set a Password (Optional)**: For development, you might not need a password locally, but it’s good practice to require one. In the config file, find the line `# requirepass foobared` and set a strong password by uncommenting and changing `foobared`. Then restart Redis. When `requirepass` is enabled, Redis will reject any command from unauthenticated client ([Redis security | Docs](https://redis.io/docs/latest/operate/oss_and_stack/management/security/#:~:text=When%20the%20requirepass%20setting%20is,sending%20the%20AUTH%20command))】.
4. **Start Redis**: It likely started automatically. Check with:
   ```bash
   systemctl status redis
   ```
   or simply try the CLI: `redis-cli ping`. It should return `PONG`.
5. **Test Data**: Run `redis-cli` to get a Redis prompt. Try:
   ```
   SET test "hello"
   GET test
   ```
   It should return "hello". Type `exit` to quit.

### Option B: Run Redis via Docker

- If Docker is available, one can run:
  ```bash
  docker run -d --name redis -p 6379:6379 redis:7-alpine
  ```
  This will run a Redis container accessible on the host port 6379. Note that by default this has no password and binds to all interfaces in the container (which we mapped to host port, so essentially accessible to host). It’s fine for local, but in production we’d restrict network access.

Now we have a Redis instance for caching and a MongoDB instance for data, both running and accessible.

## 4. Setup AWS CLI and Credentials

Before we can deploy anything to AWS or use Terraform effectively, we should set up our AWS account credentials and CLI:

1. **AWS Account**: Ensure you have an AWS account created. Sign up at AWS if you haven’t. Also, it’s recommended to create an IAM user for yourself rather than using the root account.
2. **IAM User and Access Key**: In the AWS console, create an IAM user with programmatic access. Assign appropriate permissions (for initial setup, you might use AdministratorAccess policy, but for production use least privilege). Generate an **Access Key ID and Secret Access Key** for this use ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=,and%20cluster%20in%20Amazon%20AWS))】.
3. **Install AWS CLI**: While not strictly needed for Terraform, having AWS CLI is useful for quick sanity checks. Install AWS CLI v2:
   - On Linux: you can use pip (`pip install awscli` if you have Python) or download the binary. On Ubuntu, you might do:
     ```bash
     sudo apt-get install awscli
     ```
     (Though this might give v1; alternatively use pip or the official installer for v2).
   - Verify with `aws --version`.
4. **Configure AWS CLI**: Run:
   ```bash
   aws configure
   ```
   Enter your Access Key ID, Secret Key, default region (e.g., `us-east-1` or your preferred region), and default output format (you can use `json`). This stores credentials in `~/.aws/credentials` file. Terraform can reuse these credentials by default.
5. **Create an AWS Key Pair (for EC2)**: If you will directly SSH into EC2 instances, create an SSH key pair in AWS (via AWS console or `aws ec2 create-key-pair`). Save the private key (`.pem`) in a secure location. For Terraform, you might need the key name to provision EC2 that you can SSH into.
6. **AWS Resource Setup Note**: At this point, we haven’t created any AWS resources. We’re just preparing credentials. We will use Terraform next to define and launch infrastructure. However, you may want to ensure your account has default limits that suit your plan (e.g., some accounts might have very low default vCPU limits). For a small test, defaults are fine.

## 5. Install Terraform

Terraform will orchestrate AWS resources for us:

1. **Download Terraform**: Go to the [Terraform download page](https://www.terraform.io/downloads.html) and get the appropriate package for your OS. For Linux 64-bit:
   ```bash
   wget https://releases.hashicorp.com/terraform/1.5.6/terraform_1.5.6_linux_amd64.zip
   unzip terraform_1.5.6_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```
   (Replace version number as needed for the latest release).
2. **Verify**: Run `terraform -v`. You should see the version and confirmation that it's installed.
3. **Terraform Setup**: No additional configuration needed, but you might create a directory for your infrastructure code, e.g., `infrastructure/` in your project.
4. **AWS Provider**: We will write Terraform config soon. By default, Terraform reads AWS credentials from `~/.aws/credentials` (which we set up) or environment variables. Ensure that the AWS CLI configure step was done. Alternatively, set environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (and optionally `AWS_DEFAULT_REGION`) in your shell. For sensitive information, be cautious not to expose these keys.
5. **Terraform IAM Permissions**: The IAM user whose keys you’re using should have rights to create the AWS resources we intend to use (EC2, VPC, EKS, etc.). For initial testing, using an Admin policy is simplest, but for production you'd tailor a policy. Rancher’s quickstart, for example, suggests a simple policy that allows creating EC2 instances, key pairs, and security group ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=%7B%20%22Version%22%3A%20%222012,%7D%20%5D))】.

Now Terraform is ready to use. We’ll use it in the **Deployment** section to actually provision AWS infra for the CMS.

## 6. Install Docker and Docker Compose

We plan to containerize the CMS components. Docker installation steps:

1. **Install Docker Engine (Ubuntu)**:
   - Update packages: `sudo apt-get update`
   - Install pre-requisites: `sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release`
   - Add Docker’s GPG key:
     ```bash
     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
     ```
   - Add Docker apt repository:
     ```bash
     echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
     https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
     ```
   - Install Docker packages:
     ```bash
     sudo apt-get update
     sudo apt-get install -y docker-ce docker-ce-cli containerd.io
     ```
   - (Alternatively, use the convenience script: `curl -fsSL https://get.docker.com | sudo bash`).
2. **Post-install**: After installation, ensure your user is in the `docker` group to run docker without sudo:
   ```bash
   sudo usermod -aG docker $USER
   ```
   Then log out and log back in for group change to apply.
3. **Verify Docker**: Run `docker run hello-world`. This should download a test image and run it, printing a hello message, confirming Docker is functional.
4. **Install Docker Compose**: Modern Docker releases include Compose plugin. Check `docker compose version`. If it’s not present, install Docker Compose separately (if using older Docker):
   - For Linux:
     ```bash
     sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```
   - Verify with `docker-compose --version` (or `docker compose version` if using the plugin).
5. **Test Compose**: Create a simple `docker-compose.yml` to test (not mandatory now, but useful to verify). For example:
   ```yaml
   version: "3"
   services:
     web:
       image: nginx:alpine
       ports:
         - "8080:80"
   ```
   Run `docker compose up -d` in that directory and then visit http://localhost:8080 to see Nginx welcome page. Bring it down with `docker compose down`.

Docker is now set up, allowing us to containerize our app and other services. We will use Docker to create images for the Node app and maybe an OpenResty container with custom config.

## 7. (Optional) Install Rancher (for Kubernetes Management)

Rancher itself can be run as a Docker container (for a single-node install) or installed on a K8s cluster. For development or trial, a quick way is running the Rancher server in Docker on your local machine or an EC2 instance:

1. **Run Rancher Container**:
   ```bash
   docker run -d --name rancher-server --restart=unless-stopped -p 8081:80 -p 8443:443 rancher/rancher:stable
   ```
   - This runs Rancher UI on http (port 8081) and https (8443). Adjust ports if needed (especially if you have something on 443 already).
   - It might take a minute to start. Check `docker logs -f rancher-server` until you see a line about Rancher startup.
2. **Access Rancher**: Open a browser to `http://localhost:8081` (or `https://localhost:8443`). You should see the Rancher UI initialization. It will prompt to set an admin password (remember it) and then ask to set the server URL (use your machine’s IP or localhost for testing).
3. **Add a Cluster**: Rancher needs to manage a Kubernetes cluster. For testing, you can use the built-in **K3s** single-node cluster by enabling `Local Cluster` (Rancher 2.5+ manages its own local K3s). In Rancher UI, you might see a local cluster already active (the one running Rancher itself). If not, you can create a new cluster:
   - Option A: **Custom cluster** – allows you to turn any Linux host into a K8s node by running a Docker command. For instance, you can create a custom cluster in Rancher, then it will give you a `docker run ...` command to execute on nodes to join them to the cluster. If running on your local, execute that to join your machine as a node (not ideal on same machine as Rancher container, but possible in a test).
   - Option B: Use **Rancher Quick Start Terraform** – Rancher provides a Terraform module that can set up a single-node K3s cluster in AWS for Rancher and another cluster for workload ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=1,git%20clone%20https%3A%2F%2Fgithub.com%2Francher%2Fquickstart)) ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=6.%20Run%20))】. This is more complex and intended for cloud deployment (we’ll discuss in Deployment).
   - For simplicity, if just testing locally, using Rancher’s local K3s (if available) or a custom cluster on the same host can work. For production, you’d launch on AWS (which we’ll do in Deployment).
4. **Rancher Server in Production**: When we move to AWS deployment, we might deploy Rancher on an EC2 or as a workload in an EKS cluster, but often Rancher server is run separately from your apps cluster. An example from Rancher docs quickly deploying on AWS involved Terraform launching an EC2 with Rancher and a single-node cluste ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=7,output%20similar%20to%20the%20following)) ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=9,quickstart%2Francher%2Faws))】.

If you do not want to use Rancher, skip this; you can manage K8s with `kubectl` directly or use AWS EKS console. But we include Rancher for a richer ops experience. Make sure you **remember the Rancher admin password** set during initialization.

---

At this point, we have installed all necessary components:

- **Node.js & GraphQL** – environment ready, with a sample server.
- **MongoDB** – running.
- **Redis** – running.
- **AWS CLI** – configured.
- **Terraform** – installed.
- **Docker** – installed (for containerization).
- **Rancher** – optionally running (for cluster management).

In a real development workflow, you might now start coding the CMS (schema, resolvers) and spin up these services together (for example, via Docker Compose). Before jumping into integration details, ensure each piece works in isolation:

- Node app can start and serve GraphQL (tested with the hello world query).
- MongoDB can be connected to (try writing a sample from Node to Mongo).
- Redis can be pinged from Node (we’ll test integration soon).
- Terraform can at least initialize (run `terraform` in your infra directory to see help).
- Docker can build images and run containers.
- Rancher UI is accessible (if set up).

In the next section, we'll cover how to integrate these technologies, i.e., how our Node.js GraphQL server will connect to MongoDB and Redis, how OpenResty fits in front of Node, and how everything will be orchestrated via Docker/Rancher in a cohesive environment.

# Integration Guide

With all components installed, let's integrate them to build the CMS. Integration involves configuring each piece to work together: the Node.js GraphQL server will use MongoDB for data persistence and Redis for caching, OpenResty will sit in front of Node as a reverse proxy (and potentially handle some caching or routing logic), Docker will containerize services, and Rancher/Kubernetes will orchestrate them in an environment akin to production.

We’ll also outline the overall architecture of the system and how data flows through it. This is critical for understanding how the pieces communicate in a CMS scenario.

## Architecture Overview

Let's start with a high-level architecture of the CMS in a production-like environment on AWS:

```
 [Client] -- HTTP(S) --> [OpenResty (Nginx+Lua) Reverse Proxy] -- HTTP --> [Node.js GraphQL API Server] --> [MongoDB Database]
                                   |                                            |
                                   | (Cache layer: optional)                    |--> [Redis Cache]
                                   |                                            |
                       [Static files or cached responses]                   [External Services/APIs (if any)]
```

- **OpenResty (Nginx)**: Clients (browsers, apps) connect to OpenResty, which terminates SSL (for HTTPS) and handles requests on the edge. OpenResty proxies GraphQL requests to the Node.js server. It can also serve static assets (if our CMS has images or files) directly, and use its caching mechanisms to store frequent responses. For example, if many clients request the `{ latestArticles { title, summary } }` GraphQL query, OpenResty could be configured to cache the response for a short time (microcache) to offload the Node server.
- **Node.js GraphQL API**: This is the core application logic. It receives GraphQL queries and executes them. The GraphQL **resolvers** will fetch or mutate data.
- **MongoDB**: Acts as the primary **content database**. Resolvers in Node will query MongoDB (e.g., using Mongoose models) to get content. For example, a resolver for `Article.content` might run a Mongo query like `db.articles.findOne({ _id: ... })` to retrieve an article’s content from the `articles` collection.
- **Redis**: Serves as a caching layer and possibly for other ephemeral data (like sessions or rate limiting counters). Resolvers might check Redis first for cached data (e.g., the result of an expensive aggregation or a popular piece of content) before hitting MongoDB. If the data is found in Redis, it can return quickly; if not, fetch from Mongo and then store it in Redis for next time. Redis might also be used by OpenResty’s Lua scripts for caching or storing session info since OpenResty can directly query Redis in a non-blocking way.
- **Integration with External Services**: (Not explicitly in our tech list, but many CMS have external integrations). For completeness, if the CMS had to fetch data from external REST APIs or microservices, those calls would likely be made within GraphQL resolvers as well. OpenResty could also be configured to cache those external responses. But our focus is the core stack above.

- **AWS Infrastructure**: This architecture would be deployed on AWS such that OpenResty and Node run on EC2 instances or in containers on EKS, MongoDB and Redis on appropriate hosts or services, and a Load Balancer forwarding traffic to OpenResty. We will detail that in Deployment, but for integration think of them connected on a private network (e.g., within the same VPC or Kubernetes cluster). Terraform will ensure, for instance, that Node and Mongo are in the same subnet so that Node can reach Mongo on its internal address.

The general flow:

1. Client sends a GraphQL query (HTTP POST with JSON body, or GET if using persisted query) to the CMS’s public URL.
2. The request hits AWS load balancer which forwards to an OpenResty instance (or container). OpenResty decrypts SSL (if HTTPS).
3. Nginx (OpenResty) looks at the path (e.g., `/graphql`) and routes the request to the upstream Node.js service. If caching is enabled for this query and a cached response exists (and is fresh), OpenResty might return that immediately without hitting Node.
4. Node.js receives the GraphQL query. Apollo Server (or whichever GraphQL server) parses and validates it against the schema. Then it triggers resolver functions for the requested fields.
5. Resolvers execute: for data stored in MongoDB, Node will query Mongo (via Mongoose or native driver). If a Redis cache is in use, the resolver might first check Redis. For example, a `getLatestArticles` resolver could try `redis.get("latestArticles")`.
   - If cache **hit**, return the cached JSON (and skip DB).
   - If cache **miss**, query MongoDB: `Article.find().sort({publishDate:-1}).limit(5)`, get results, then store them in Redis (`SET latestArticles <data>` with an expiration).
6. MongoDB processes any queries, returning data to Node. Redis similarly returns any cached data when asked.
7. Once all resolvers complete, Node.js assembles the final GraphQL JSON response.
8. Apollo Server sends the response back to OpenResty which then returns it to the client. If OpenResty is set to cache the response, it will store it (perhaps in its shared memory or using `lua-resty-cache` module, or even in Redis via Lua if configured) so that identical requests within a short time can be served faster.
9. The client receives the data and displays the content.

Throughout this flow, there are a few integration points to configure carefully:

- **Node <-> MongoDB**: configuration of connection string, connection pool, and defining data models.
- **Node <-> Redis**: initialization of a Redis client in Node, error handling (if Redis is down, the app should still proceed to fetch from DB).
- **Node <-> OpenResty (Nginx)**: openresty needs to know how to reach Node (an upstream configuration with Node’s hostname/IP and port). Also handle timeouts: if Node is slow (e.g., DB is sluggish), OpenResty should have appropriate timeouts and maybe return a friendly error or cached content.
- **OpenResty caching**: deciding what content to cache at the proxy level. GraphQL responses vary by query and variables, so keys need to include query parameters. We might not dive deep into writing that Lua logic here, but conceptually it’s possible (for instance, using the request body as part of cache key after normalization).
- **OpenResty static content**: If the CMS serves images or uploaded files, a pattern is to use S3 or similar. If using OpenResty, it could also serve files from disk or proxy to S3. Not our main focus here, but something to note in integration (ensuring the Nginx config serves `/uploads/*` from a particular directory or upstream).
- **Rancher/Kubernetes**: When containerizing, we need to configure service discovery (e.g., in Kubernetes, Node container and OpenResty container might be in the same pod or in separate deployments with a service between). We’ll address that in the deployment/infrastructure integration sub-section.

Now, let’s break down integration specifics per component:

## Connecting Node.js to MongoDB (Database Integration)

To integrate Node (our GraphQL API) with MongoDB:

1. **Choose a MongoDB Driver/ORM**: The official MongoDB Node.js driver (`mongodb`) or an ODM/ORM like **Mongoose**. Mongoose provides a higher-level schema modeling and is popular in CMS-like apps for its ease of defining models with validation. We’ll use Mongoose in examples.
2. **Install Mongoose**:
   ```bash
   npm install mongoose
   ```
   (If you prefer the official driver, `npm install mongodb` and use MongoClient).
3. **Connect to MongoDB**: In your Node app (perhaps in an `app.js` or before starting Apollo Server), add:
   ```js
   const mongoose = require("mongoose");
   mongoose
     .connect("mongodb://localhost:27017/cmsdb", {
       useNewUrlParser: true,
       useUnifiedTopology: true,
     })
     .then(() => console.log("Connected to MongoDB"))
     .catch((err) => console.error("MongoDB connection error:", err));
   ```
   Replace the connection string as needed (e.g., if using authentication or a different host). For a local dev, `mongodb://localhost:27017/cmsdb` is fine (it will use database named "cmsdb").
   - Ensure this runs before your server starts accepting requests, so that the DB connection is established.
   - The options `{useNewUrlParser, useUnifiedTopology}` are common to avoid deprecation warnings.
   - You might also want to handle connection errors/retries if Mongo starts after Node, etc.
4. **Define Schemas and Models**: For a CMS, you likely have models like Article, User, Comment, etc. Using Mongoose, define a schema. For example, create `models/Article.js`:
   ```js
   const { Schema, model } = require("mongoose");
   const ArticleSchema = new Schema(
     {
       title: { type: String, required: true },
       content: String,
       author: { type: Schema.Types.ObjectId, ref: "User" },
       tags: [String],
       publishedAt: Date,
     },
     { timestamps: true }
   );
   module.exports = model("Article", ArticleSchema);
   ```
   This creates an `Article` model. We also might define `User` and `Comment` similarly. These schemas correspond to how GraphQL types might look, but not necessarily one-to-one.
5. **Use Models in Resolvers**: In your GraphQL resolvers, instead of dummy data, use these models. For example, suppose our GraphQL schema has:
   ```graphql
   type Article {
     id: ID!
     title: String
     content: String
     tags: [String]
     author: User
     publishedAt: String
   }
   type Query {
     articles: [Article]
     article(id: ID!): Article
   }
   ```
   Then resolvers:
   ```js
   const Article = require("./models/Article");
   const resolvers = {
     Query: {
       articles: async () => {
         return await Article.find().limit(100).exec(); // return latest 100 articles
       },
       article: async (_, { id }) => {
         return await Article.findById(id);
       },
     },
     Article: {
       author: async (article) => {
         // Assuming we have a User model and article.author contains the ObjectId
         return await User.findById(article.author);
       },
     },
   };
   ```
   The above demonstrates how resolvers interact with the database: using Mongoose queries which return promises (hence `await`). We keep them `async` to handle the asynchronous nature gracefully.
6. **Error Handling**: Ensure to handle exceptions in resolvers (Apollo will catch and send as GraphQL errors if thrown). For example, if MongoDB is down or a query fails, you may throw a user-friendly error or let the exception bubble.
7. **Testing Integration**: Restart your Node server with these changes. Use a GraphQL client (Playground or Insomnia, etc.) to run queries like `query { articles { id title } }`. If you have no data, it returns empty array. You can manually insert some documents into MongoDB to test (either via Mongo shell or writing a mutation resolver to add data).
8. **Populate Sample Data (Optional)**: You might create a temporary route or script to add sample content. For instance:
   ```js
   Article.create({
     title: "Hello World",
     content: "First post",
     publishedAt: new Date(),
   });
   ```
   Then query it through GraphQL to ensure the pipeline from GraphQL -> Node -> Mongo works.

**Data considerations**: Ensure your MongoDB instance has appropriate indexes (e.g., maybe index `publishedAt` for sorting articles, etc.). For now, with small data, it's fine. We will revisit performance considerations later.

## Using Redis in Node.js for Caching and Session (Cache Integration)

Integrating Redis into Node can serve multiple purposes: caching, session store, pub/sub. We'll focus on caching query results (and note how to also use it for things like rate limiting or user sessions if needed).

1. **Install Redis Client**: A popular Node.js Redis client is `ioredis` or the official `redis` package. We'll use the official Redis client for simplicity:
   ```bash
   npm install redis
   ```
   This is the modern Redis client (Node-redis 4.x) that uses Promises.
2. **Connect to Redis**: In your Node app initialization, after connecting to Mongo (or before, order not critical), connect to Redis:
   ```js
   const redis = require("redis");
   const redisClient = redis.createClient({ url: "redis://localhost:6379" });
   redisClient
     .connect()
     .then(() => console.log("Connected to Redis"))
     .catch((err) => console.error("Redis connection error:", err));
   ```
   This uses default no-auth. If you set a password in redis.conf, use `url: 'redis://:PASSWORD@localhost:6379'`. The client’s `connect()` returns a promise.
3. **Use Redis in Resolvers**: We can leverage Redis for caching heavy read queries. For example, a `Query.latestArticles` could try the cache first:
   ```js
   Query: {
     latestArticles: async () => {
       // Try cache
       const cacheKey = "latestArticles";
       const cached = await redisClient.get(cacheKey);
       if (cached) {
         return JSON.parse(cached);
       }
       // If not cached, query Mongo
       const data = await Article.find()
         .sort({ publishedAt: -1 })
         .limit(5)
         .lean();
       await redisClient.set(cacheKey, JSON.stringify(data), {
         EX: 60, // expire in 60 seconds
       });
       return data;
     };
   }
   ```
   Explanation:
   - We attempt to get the cached value. If present, parse it from JSON and return it (resolving quickly).
   - If not, we hit MongoDB (`find().sort().limit().lean()` - `lean()` returns plain JS objects instead of Mongoose documents, which are easier to serialize).
   - Store the result in Redis with an expiration (EX: 60 seconds). The expiry is a TTL to ensure cache invalidates and new data eventually is fetched.
   - Return the data.
     By doing this, if `latestArticles` is called frequently (say on every homepage load), after the first time, subsequent ones within the next 60 seconds will be served from the in-memory cache (Redis) in microseconds, rather than hitting the database.
4. **Cache Invalidation**: In a CMS, content changes when authors publish or update articles. We need to invalidate or update caches appropriately. If there is a mutation like `publishArticle`, after writing to MongoDB, you should also delete or update relevant Redis keys (`redisClient.del("latestArticles")` so that next query will fetch fresh data). This adds complexity, but it’s important to ensure users see up-to-date content. Simpler strategy: use short expirations (like we did, 60s) so stale data self-expires quickly.
5. **Use Redis for other things** (optional):

   - **User Session**: If using sessions (e.g., via Express-session), one can use Redis as a session store. Apollo GraphQL typically uses stateless JWT tokens for auth, but if you had session IDs, storing them in Redis is a common approach for scalability.
   - **Rate Limiting**: You can implement a simple rate limit by incrementing a counter in Redis for each request per user and setting it to expire. If it exceeds a threshold, you block further queries. This could be integrated as a middleware in Apollo (checking Redis before processing).
   - **Pub/Sub**: If the CMS had real-time notifications (like notifying all clients of a new comment), Node servers could subscribe to Redis channels. For example, on a comment create, one instance publishes to a "comments" channel and all instances (or an OpenResty Lua script) subscribed can react. This is more advanced and perhaps not needed in a basic CMS.

6. **Testing Redis Integration**: Start your Redis (if not up) and Node app. Query the `latestArticles` (or whichever query you integrated caching for) twice. The first time, see that it took the DB route (maybe add a console log "cache miss" to confirm). The second time, it should be a cache hit. You can also monitor Redis by running `redis-cli monitor` in a separate terminal to see commands in real-time. You should see the `GET` and `SET` operations.

## Reverse Proxy with OpenResty (Nginx) in front of Node.js

OpenResty (Nginx + Lua) will be configured to accept client requests and forward them to the Node.js server. We will set up a basic reverse proxy configuration and then discuss enhancements like caching and security headers.

Assuming you have OpenResty installed (from the earlier installation step), the config file is typically at `/usr/local/openresty/nginx/conf/nginx.conf` (if built from source) or `/etc/openresty/nginx.conf` (if installed via package) or `/usr/local/openresty/nginx/conf/nginx.conf`. We might use a custom config file for our application for clarity.

### Basic Nginx Reverse Proxy Setup

1. **Upstream Configuration**: Define an upstream block that points to your Node.js server(s). For example, in your nginx.conf, within the `http { ... }` block, add:
   ```nginx
   upstream cms_node {
       server 127.0.0.1:4000 fail_timeout=0;
       # If multiple Node instances, list them here (round-robin by default)
   }
   ```
   This defines a logical upstream group named "cms_node".
2. **Server Block**: Configure a server block to listen on port 80 (and 443 for SSL):

   ```nginx
   server {
       listen 80;
       server_name cms.example.com;  # your domain or IP

       location /graphql {
           proxy_pass http://cms_node;   # forward to the upstream
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_set_header Connection "";
           proxy_set_header X-Real-IP $remote_addr;
           # Other proxy_set_header for forwarded host, etc., if needed
       }

       location /playground {  # optional, if you want to expose GraphQL playground
           proxy_pass http://cms_node/playground;
       }

       # You might serve static files if any:
       location /assets/ {
           root /var/www/cms;  # example directory for static files
       }
   }
   ```

   Explanation:

   - `proxy_pass http://cms_node;` sends requests hitting `/graphql` to the Node upstream.
   - We set some headers:
     - `Host` so the Node server sees the original host requested (useful if Node logic depends on host).
     - `X-Real-IP` to forward client IP.
     - `Connection ""` to handle keep-alive properly with upstream (especially for HTTP/1.1 proxying).
   - If Apollo Server playground runs at `/` or `/playground`, proxy that too for convenience.
   - The static files example: if your CMS had an admin UI built in React for instance, you could serve it via Nginx as static files (or it might be separate).

3. **Sendfile and Buffering**: Ensure `sendfile on;` in http block for efficiency serving static files. Proxy buffers by default which is okay for typical API responses. If streaming responses (like SSE), you’d adjust it.
4. **Test Nginx**: Save this config and test syntax:
   ```bash
   sudo nginx -t -c /usr/local/openresty/nginx/conf/nginx.conf
   ```
   (Path may differ). If syntax is ok, reload Nginx:
   ```bash
   sudo nginx -s reload
   ```
   Now Nginx/OpenResty is listening on port 80.
5. **Point DNS or use hosts file**: If you have a domain (e.g., cms.example.com) and DNS pointing to your server’s IP, great. If not, for testing, you can hit `http://<server-ip>/graphql`. Or set your local `/etc/hosts` to map a test name to the server IP.
6. **Verify Proxy**: Using curl or a browser, make a request to Nginx:
   ```bash
   curl http://localhost/graphql -X POST -H "Content-Type: application/json" -d '{"query":"{ hello }"}'
   ```
   This should proxy to Node and return the GraphQL response (e.g., `{"data":{"hello":"Hello, CMS World!"}}`). If you get that, the proxy is working.

### Enabling SSL (HTTPS) - optional but recommended:

- Obtain a certificate (for dev, you can self-sign or use Let’s Encrypt for a real domain).
- In the server block, add:
  ```nginx
  listen 443 ssl;
  ssl_certificate /path/to/fullchain.pem;
  ssl_certificate_key /path/to/privkey.pem;
  ```
  And perhaps redirect port 80 to 443 in a separate server block:
  ```nginx
  server {
      listen 80;
      server_name cms.example.com;
      return 301 https://$host$request_uri;
  }
  ```
  This ensures all traffic is secure.

### Caching with OpenResty/Nginx (Microcaching):

OpenResty, by default, functions like Nginx. To enable caching of responses, we can use Nginx’s `proxy_cache`. However, caching GraphQL responses can be tricky because they are usually POST requests (which Nginx doesn’t cache by default) and their cache key might depend on the request body (query + variables). A strategy:

- If certain queries are **idempotent and cacheable**, consider allowing GET requests for them. Apollo Client and others support GET for queries if configured. Nginx can cache GET responses easily using query string as part of key.
- Alternatively, use the Lua subsystem to generate a cache key from POST body. There are OpenResty libraries for caching (e.g., lua-resty-cache or using the shared dictionary + manually storing).
- For simplicity, let's assume we will use **microcaching** for all responses to `/graphql` for a very short time (say 5 seconds). This can dramatically increase throughput for high traffic by coalescing repeated identical requests in that timefram ([The Benefits of Microcaching with NGINX](https://blog.nginx.org/blog/benefits-of-microcaching-nginx#:~:text=Microcaching%20is%20an%20effective%20method,very%20short%20periods%20of%20time))】.

Basic microcache config:

```nginx
http {
    # define keys zone for cache
    proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=microcache:10m inactive=30s max_size=100m;
    proxy_cache_key "$scheme$request_method$host$request_uri$request_body";

    server {
      ...
      location /graphql {
        proxy_pass http://cms_node;
        proxy_cache microcache;
        proxy_cache_valid 200 5s;
        proxy_cache_methods GET POST;
        proxy_cache_lock on;
        proxy_no_cache $arg_noCache;  # allow bypass with parameter
        proxy_cache_bypass $arg_noCache;
        ...
      }
    }
}
```

In the above:

- `proxy_cache_path` defines a cache store in `/tmp` with 10MB of keys (this size can be tuned) and `inactive=30s` meaning if an item isn’t accessed for 30s it’s removed.
- `proxy_cache_key` uses a combination of method, host, URI, and request body. This attempts to distinguish requests by their content. (This is not default and is a bit advanced usage; ensure `$request_body` is available - you may need `lua` to capture it or use `proxy_cache_methods` with POST which we did).
- `proxy_cache_valid 200 5s` means cache successful responses for 5 seconds. Other status codes can be listed if desired (e.g., maybe cache 404 for short time too to avoid repeated DB hits on missing content).
- `proxy_cache_methods GET POST` allows caching POST as well (which is normally not cached).
- `proxy_cache_lock on` makes sure if multiple identical requests come when item is not in cache, only one goes to backend and others wait (to avoid thundering herd).
- `proxy_no_cache` and `proxy_cache_bypass` with a parameter (like `?noCache=1`) allow clients or you to force refresh if needed.

Be careful: This is a simplified approach and storing `$request_body` as part of key could include non-hashable raw body. It might work but note Nginx normally doesn’t include body in key. For production, a safer approach is to hash the body (e.g., via Lua) and use that hash as part of key. But for demonstration, the above gives the ide ([The Benefits of Microcaching with NGINX](https://blog.nginx.org/blog/benefits-of-microcaching-nginx#:~:text=Microcaching%20is%20an%20effective%20method,very%20short%20periods%20of%20time))】.

If you enable this and reload Nginx, it will start microcaching GraphQL responses. To test:

- Make a GraphQL query with the same body twice within 5 seconds; the second time should be served from cache (you can see by enabling Nginx log `$upstream_cache_status` which would show `MISS` then `HIT`).
- Try a query with `?noCache=1` appended to URL or as a header to skip cache.

OpenResty’s Lua could implement far more sophisticated caching logic if needed (like parsing the GraphQL query to decide a cache key or TTL per operation type). But microcaching is a blunt yet effective instrument for performance, caching even personalized content for a few seconds is often fine and dramatically reduces load spike ([Microcaching with Nginx - WordOps Documentation](https://docs.wordops.net/how-to/microcaching-with-nginx/#:~:text=This%20way%20your%20server%20can,while%20still%20serving%20dynamic%20content))】.

### Additional OpenResty Lua usage:

OpenResty allows writing Lua in various phases (init, access, content, etc.). Some things you might do:

- **JWT validation**: If your GraphQL uses JWT for auth, you could have an `access_by_lua` block that verifies the token signature and maybe even set a header or variable for user ID. This offloads auth parsing from Node (though Apollo can do it too in middleware).
- **Custom routing logic**: e.g., if `Host` or some header indicates a certain site, route to a different upstream (multi-site CMS scenario).
- **WAF rules**: You could implement or use lua-resty-waf to filter out malicious payloads (like very large queries, etc., although GraphQL should handle that via max depth etc. as discussed in security).
- **Serving cached pages**: In some CMS, one might generate full HTML pages and store them in Redis or shared memory, and OpenResty could serve those directly on subsequent requests (bypassing Node). This is akin to full page caching (not typical for GraphQL API scenario, more for when using GraphQL to then render pages).

For our scope, we won’t dive deeper into Lua coding, but remember OpenResty essentially can act as another application tier (written in Lua) if needed. The integration point is that OpenResty can call out to Redis, for example, within a Lua script to get or set data, which could coordinate with what Node is doing. One could imagine advanced caching where Node on certain mutation sends a purge instruction (e.g., publishing a new article triggers Node to call a special URL or Redis pubsub that OpenResty listens to, to clear the cache of `/graphql latestArticles`).

## Containerization: Docker Compose for Development

Before deploying to AWS/Kubernetes, it's useful to tie everything together in a Docker Compose setup for local development. This ensures if someone else picks up the project, they can run a single command to start all services. Also, it mirrors what we will orchestrate in production.

Create a `docker-compose.yml` at project root:

```yaml
version: "3.8"
services:
  openresty:
    image: openresty/openresty:latest
    volumes:
      - ./deploy/openresty.conf:/etc/openresty/nginx.conf:ro
      - ./deploy/conf.d/:/etc/openresty/conf.d/:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - node
    networks:
      - cms-net

  node:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - MONGO_URL=mongodb://mongo:27017/cmsdb
      - REDIS_URL=redis://redis:6379
      # (plus any other env vars like for secrets)
    depends_on:
      - mongo
      - redis
    networks:
      - cms-net

  mongo:
    image: mongo:6.0
    volumes:
      - mongo-data:/data/db
    networks:
      - cms-net

  redis:
    image: redis:7-alpine
    networks:
      - cms-net

networks:
  cms-net:
    driver: bridge

volumes:
  mongo-data:
```

What this does:

- Defines an **openresty** service using an official image. We mount our custom config (which includes the reverse proxy settings we wrote) into the container. We expose port 80 and 443 of the container to the host (so you can hit http://localhost).
- Defines the **node** service. We assume we have a Dockerfile to build our Node app image. We'll create that next. We pass environment variables for the Mongo and Redis connection URLs. Notice we refer to `mongo` and `redis` by service name – in Docker compose, those become DNS names on the network. So `mongo:27017` will resolve to the Mongo container.
- **mongo** and **redis** services use official images. Mongo has a named volume for persistent data (so that if you `docker-compose down` without `-v`, your content stays).
- All services join the `cms-net` network so they can communicate. By default, Docker Compose sets up DNS so that each service can reach others via the service name.

Now, Dockerfile for Node (`Dockerfile` in project root):

```dockerfile
FROM node:18-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy app source
COPY . .

# Build step (if you have any transpilation or build, e.g., TypeScript, front-end)
# RUN npm run build  (if needed)

# Expose port
EXPOSE 4000

# Start the server (adjust if your start script is different)
CMD ["node", "index.js"]
```

This Dockerfile:

- Uses a lightweight Node Alpine base.
- Copies package files and installs dependencies (production-only to keep image small; you might do a multi-stage build for dev vs prod).
- Copies the rest of the code.
- Exposes port 4000 (the Node server port).
- The `CMD` runs the app.

We might need to tweak if our app requires build or uses dev dependencies. For a simple Node API, this is fine.

Build and run with Docker Compose:

```bash
docker-compose up --build
```

This will:

- Build the node image.
- Create containers for node, openresty, mongo, redis.
- The `depends_on` ensures order: mongo and redis come up before node tries to start; node comes up before openresty (though openresty will retry connecting to backend if needed).
- Once up, you should be able to hit `http://localhost/graphql` and get data. The Node container will connect to the Mongo and Redis containers using the internal network.

**Tip**: For the OpenResty config inside the container, adapt upstream to `server node:4000;` because OpenResty container should reach Node by its service name `node`. If we put our config via volumes, ensure it reflects that:

```
upstream cms_node { server node:4000; }
```

Instead of 127.0.0.1.

Now we have an integrated docker-compose environment:

- Edit code on host -> you might want to set up volumes for Node code for live reload, or use nodemon. In Compose, you could mount your code and run nodemon in the container for development convenience.
- This mirrors production architecture (except all on one machine). It's a good stepping stone to then translate to Terraform + Kubernetes.

## Orchestration with Kubernetes (via Rancher) - Production Integration

Finally, consider how this integrates when deployed on AWS with Kubernetes:

- Each service (openresty, node, mongo, redis) would be one or more containers in the cluster.
- We might choose to not run MongoDB and Redis as containers in the same cluster for production (preferring managed services or separate VMs for stateful components to avoid data loss issues on cluster churn). But it's possible to run them with PersistentVolumes.
- Using Rancher, you'd create Deployments for Node and OpenResty, a StatefulSet for Mongo (with volume claims), and maybe a Deployment or StatefulSet for Redis.
- Then use Services:
  - A ClusterIP Service for Node (so OpenResty can resolve the Node pods by service DNS).
  - Perhaps no service needed for OpenResty if it's going to be the one receiving external traffic – instead, use an **Ingress** or a Service of type LoadBalancer for OpenResty.
  - Alternatively, one could skip OpenResty in K8s and use an Ingress controller (like nginx-ingress or Traefik) to directly route to Node. But since we want OpenResty specifically (perhaps for Lua customizations), we'd run it.
- **In Kubernetes**: we might place OpenResty and Node in the same Pod (so they share localhost and can communicate easily). This is possible (sidecar pattern), but not typical to pair a reverse proxy with app unless necessary, because scaling them together means you run an Nginx for each Node instance. Another approach: deploy Node pods and a separate Deployment of Nginx pods and use a Service mesh. But let's assume we deploy them separately:
  - Node Deployment (e.g., 3 replicas).
  - OpenResty Deployment (e.g., 2 replicas), configured to proxy to the Node service (which load balances among Node pods).
  - Then use a Kubernetes Service type LoadBalancer for OpenResty pods on port 80/443. AWS will provision an ELB for that, which becomes the entry point.
- For MongoDB, in AWS we might use **Amazon DocumentDB** or host our own. If self-hosting, a **StatefulSet with 3 replicas** (a Primary and two secondaries) could be done, each with EBS volume. Or use an external Mongo cluster (less pressure on K8s).
- Redis similarly: could use **ElastiCache Redis** (managed with auto-failover) or run a small Redis in cluster with a PVC (and/or replication with Redis Sentinel).
- Rancher can help deploy this or we can create YAMLs:
  - A Deployment YAML for Node (with container image from our build, environment variables for connecting to the DB/Redis which could be internal addresses or secrets).
  - A Deployment YAML for OpenResty (with config map for its config).
  - Services for Node and OpenResty.
  - Possibly a Volume and PV/PVC for DB if self-hosted.

Given the complexity, one might actually question: do we need OpenResty if we already have Kubernetes ingress? The reason to still use OpenResty could be the Lua customizations or caching. But an alternative is using **Kong** API gateway (which is built on OpenResty) as an ingress controller – that would give similar benefits. However, since our requirement explicitly lists OpenResty, we assume we stick to that custom solution.

Anyway, the integration summary:

- All services should be configured to talk via hostnames that make sense in the cluster. E.g., in Node’s config, instead of `localhost` for Mongo, use the service name for Mongo or the DocumentDB cluster endpoint.
- Environment-specific configuration (like DB URIs, passwords) should be provided via environment variables or Kubernetes Secrets/ConfigMaps.
- Confirm that no component is still pointing to a local address that won’t work once distributed (e.g., Node shouldn’t assume Redis on localhost, etc.).
- Use health checks: Kubernetes will need liveness/readiness probes for Node and OpenResty. For Node, a simple HTTP check on `/health` (you can create a health endpoint that returns 200). For OpenResty, check that it returns 200 on `/` or something (or maybe use `nginx -t` indirectly).
- Logging: ensure Node logs to stdout (so Kubernetes can collect it), and Nginx logs as well (stdout/err in container).
- Security: in cluster, use NetworkPolicies if needed to ensure e.g. only OpenResty pods accept external traffic, etc.

We will delve more into the deployment in the next section. The integration points here are mainly to ensure the stack is logically wired together correctly. At this stage, we have a working integration in a local environment (via Compose or just running processes) that mirrors what we will deploy.

Next, we will cover how to deploy this integrated stack to AWS, step by step, using Terraform and discussing best practices for a production environment.

# Deployment

Deploying our CMS stack to AWS involves provisioning infrastructure (with Terraform), configuring our services on that infrastructure (possibly using Kubernetes via Rancher, or directly on EC2), and ensuring all components come up and communicate. We will outline a deployment strategy using **Terraform** to automate AWS resource creation, and then describe deploying our Dockerized application using **Kubernetes (EKS) with Rancher** for orchestration. We will also mention alternatives (like using ECS or directly using Docker on EC2) where appropriate, and cover best practices such as high availability, scaling, and zero-downtime deployments.

## Infrastructure Provisioning with Terraform (AWS Resources)

Using Terraform, we define the AWS infrastructure as code. Let’s consider the resources we need:

- A VPC with subnets (public for load balancer, private for application and DB).
- Internet Gateway, route tables, etc.
- Security Groups: e.g., allow HTTP/HTTPS to LB, allow LB to talk to OpenResty nodes, allow nodes to talk to DB, etc.
- EC2 instances or an EKS cluster (we will go with EKS for Kubernetes).
- If EKS: Node Groups (EC2 autoscaling group for worker nodes).
- IAM Roles: e.g., IAM role for EKS control plane (if not using Fargate), or for EC2 instances.
- Possibly RDS if using a relational DB (but we use Mongo, so not needed; if we used DocumentDB for Mongo, that is similar to RDS and could be provisioned).
- ElastiCache for Redis (if using managed Redis).
- Route53 DNS (if we want a nice domain for our service).
- ACM (AWS Certificate Manager) if we need SSL cert for LB.

**Terraform configuration**:
Let's outline key parts of a Terraform config (in HCL). Assume we have a `providers.tf` for AWS provider and perhaps Rancher or Kubernetes provider:

```hcl
# providers.tf
provider "aws" {
  region = "us-east-1"  # or your region
}

# variables for VPC etc (we can define variable blocks or use module defaults)
```

We might use Terraform modules (like official VPC module) for brevity:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.19.0"
  name = "cms-vpc"
  cidr = "10.0.0.0/16"
  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway = true
  tags = { Project = "CMS" }
}
```

This creates a VPC with two public and two private subnets, and a NAT Gateway for private subnets to reach the internet (for updates, etc). Instances in private subnets can use NAT to download packages.

**EKS Cluster**: We can use the AWS EKS Terraform module:

```hcl
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "cms-cluster"
  cluster_version = "1.27"
  subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  # Manage worker nodes
  node_groups = {
    default = {
      desired_capacity = 3
      max_capacity     = 4
      min_capacity     = 2

      instance_types = ["t3.medium"]  # instance type for each node
      subnets        = module.vpc.private_subnets
    }
  }

  tags = {
    Project = "CMS"
  }
}
```

This will create an EKS control plane and an autoscaling group of 3 worker nodes (t3.medium EC2 instances) across the private subnets. The node group will have IAM roles set up for it automatically via the module.

Terraform applying this will output (usually) the `kubeconfig` or necessary data to connect to cluster (some modules output it, otherwise you use `aws eks update-kubeconfig` after creation to set up local kubeconfig).

Alternatively, if not using Kubernetes, one might directly provision EC2 for each component:

- Launch template or module for an ASG of EC2 for Node (with userdata to pull Docker image and run).
- EC2 for Mongo (like 3 of them for replica set, or use DocumentDB cluster resource).
- But using EKS is more forward-looking for scaling and managing.

**Security Groups**:
We should ensure:

- A SG for LB (allows 80/443 from world).
- A SG for Node instances (allow 4000 from LB SG, allow 27017 to Mongo SG if applicable, etc).
- If using EKS, security handled differently (with NodeSG allowing all cluster internal traffic and LB will attach to nodes possibly).
  We might not manually manage SGs with EKS module, as it does some default but customizing might be needed:
  For simplicity: use an ELB (when we deploy OpenResty service of type LB, it will create one automatically using default SG allowing 0.0.0.0/0 on 80/443).

**MongoDB (DocumentDB)**:
If we choose AWS DocumentDB:

```hcl
resource "aws_docdb_cluster" "mongo" {
  cluster_identifier = "cms-mongo"
  master_username = "docdbmaster"
  master_password = "SuperSecurePassw0rd"
  engine = "docdb"
  vpc_security_group_ids = [module.vpc.default_security_group_id]  # just an example, ideally create specific SG
}
resource "aws_docdb_cluster_instance" "mongo_instances" {
  count               = 3
  identifier          = "cms-mongo-${count.index}"
  cluster_identifier  = aws_docdb_cluster.mongo.id
  instance_class      = "db.r5.large"
  engine              = "docdb"
  availability_zone   = element(module.vpc.azs, count.index)
}
```

This creates a DocumentDB cluster with 3 instances across AZs. The SG should allow Node instances (in same VPC) to connect on default port 27017.

**ElastiCache Redis**:

```hcl
resource "aws_elasticache_subnet_group" "redis_subnets" {
  name       = "redis-subnets"
  subnet_ids = module.vpc.private_subnets
}
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "cms-redis"
  engine               = "redis"
  node_type            = "cache.t3.small"
  num_cache_nodes      = 1
  subnet_group_name    = aws_elasticache_subnet_group.redis_subnets.name
  parameter_group_name = "default.redis7"
  port                 = 6379
  # automatic_failover_enabled would require cluster mode or replication group instead of cluster resource
}
```

This creates one cache node. For HA, one would use `aws_elasticache_replication_group` with multi-AZ support.

We skip some details, but these are the main building blocks.

Run `terraform init`, `terraform apply`. After a few minutes, we should have:

- VPC and subnets.
- EKS cluster (control plane).
- Worker nodes (EC2 instances) joined to cluster.
- Possibly DocumentDB cluster and Redis cluster (if those resources included).
- The outputs likely include cluster endpoint (for DocumentDB) and maybe a kubeconfig or EKS cluster endpoint/ARN.

At this point, infrastructure is up. Next step: deploy our application containers to the EKS cluster.

## Deploying the Application on EKS (with Rancher or kubectl)

Now we deploy OpenResty, Node, etc. If using Rancher:

- Add the EKS cluster to Rancher (either imported or created via Rancher Terraform provider).
- Use Rancher UI or Continuous Delivery (Fleet) to deploy manifests.

If doing manually with kubectl:

- Use the kubeconfig for the EKS cluster (ensure your AWS IAM can access the cluster - EKS usually lets the creator IAM user as admin by default).
- Create Kubernetes manifests (YAMLs) for deployments and services or use Helm.

Let's illustrate with `kubectl` and YAMLs:

**Namespace**: create a namespace for our app (e.g., `cms`). `kubectl create namespace cms`.

**Secret for Mongo and Redis config**: If using DocumentDB and ElastiCache, they have endpoints and credentials:

- DocumentDB endpoint (from Terraform output) and the username/password.
- If not secure to put in configmap, use Secret:
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: cms-config
    namespace: cms
  type: Opaque
  data:
    MONGO_URL: "bW9uZ29kYjovL2RvY2RibWFzdGVyOlN1cGVyU2VjdXJlUGFzc3cwcmRAY21zLW1vbmdvLmRvY2RiLmFtYXpvbmF3cy5jb206MjcwMTcvY21zZGI="
    REDIS_URL: "cmVkaXM6Ly9jbXMtcmVkaXMuY2FjaGUuYW1hem9uYXdzLmNvbTo2Mzc5"
  ```
  (The values are base64 of actual connection strings: e.g., `mongodb://docdbmaster:SuperSecurePassw0rd@cms-mongo.docdb.amazonaws.com:27017/cmsdb`, and `redis://cms-redis.xxxxxx.use1.cache.amazonaws.com:6379`).

**Deployment for Node**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cms-node
  namespace: cms
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cms-node
  template:
    metadata:
      labels:
        app: cms-node
    spec:
      containers:
        - name: node
          image: <your-docker-repo>/cms-node:latest # image built and pushed to a registry
          ports:
            - containerPort: 4000
          env:
            - name: MONGO_URL
              valueFrom:
                secretKeyRef:
                  name: cms-config
                  key: MONGO_URL
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: cms-config
                  key: REDIS_URL
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 4000
            initialDelaySeconds: 30
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /healthz
              port: 4000
            initialDelaySeconds: 15
            periodSeconds: 10
      # optionally, sidecar container for log shipping or something
```

This assumes you have built the Node image and pushed it to a repository accessible by the cluster (could be Docker Hub or AWS ECR). If ECR, ensure the node IAM role has ECR pull access or set up imagePullSecrets.

**Deployment for OpenResty**:
We have a couple ways: build a custom image including our config, or use a vanilla openresty and mount config via ConfigMap.

- Create ConfigMap for openresty config:
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: openresty-config
    namespace: cms
  data:
    nginx.conf: |
      worker_processes  1;
      events { worker_connections 1024; }
      http {
        # same content as we used in docker-compose, but upstream server name = cms-node service
        upstream cms_node { server cms-node:4000; }
        server {
          listen 80;
          server_name _;
          location / {
            proxy_pass http://cms_node;
            # ... (other proxy settings)
          }
        }
      }
  ```
- Deployment for openresty:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: cms-openresty
    namespace: cms
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: cms-openresty
    template:
      metadata:
        labels:
          app: cms-openresty
      spec:
        containers:
          - name: openresty
            image: openresty/openresty:latest
            ports:
              - containerPort: 80
            volumeMounts:
              - name: nginx-conf
                mountPath: /usr/local/openresty/nginx/conf/nginx.conf
                subPath: nginx.conf
        volumes:
          - name: nginx-conf
            configMap:
              name: openresty-config
              items:
                - key: nginx.conf
                  path: nginx.conf
  ```
  This mounts our config from the ConfigMap into the container, overriding the default nginx.conf.

**Service for Node**:
Expose Node internally so OpenResty can resolve `cms-node`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cms-node
  namespace: cms
spec:
  selector:
    app: cms-node
  ports:
    - port: 4000
      targetPort: 4000
      name: http
  clusterIP: None # optional: headless service if using upstream by DNS (though normal ClusterIP also works for proxy_pass)
```

Using `clusterIP: None` gives a headless service which might directly use DNS of endpoints. But standard cluster IP is fine since Nginx will treat it as one upstream (kube-proxy will load balance). For simplicity, can remove headless.

**Service for OpenResty**:
This will be of type LoadBalancer to get an ELB:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cms-openresty-lb
  namespace: cms
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb" # or "clb" or "alb"
spec:
  selector:
    app: cms-openresty
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

This will instruct AWS to create a network load balancer (if NLB annotation given). We could also do ALB via an Ingress resource (with ALB Ingress Controller), but using a Service of type LB is straightforward: you'll get a TCP load balancer routing to the OpenResty pods on port 80. For HTTPS, we can either:

- Add another port 443 with SSL termination on OpenResty itself (and attach an ACM cert to NLB manually).
- Or use an ALB ingress with SSL and forward to OpenResty (some complexity).
  A simple approach: use NLB and do SSL in OpenResty as we configured. That means we need the cert in OpenResty config. On AWS, you could attach an ACM certificate to a NLB using annotation `aws-load-balancer-ssl-cert` and `aws-load-balancer-ssl-ports: "443"`, and configure NLB to do TLS passthrough or termination. Alternatively, handle SSL entirely in OpenResty (then the LB is just forwarding TCP 443). Given time, we may skip detailed SSL config here.

Apply these YAMLs with `kubectl apply -f ...` for each or in one combined file. Kubernetes will spin up pods and the ELB. Use `kubectl get svc -n cms` to find the `EXTERNAL-IP` of the cms-openresty-lb service. That is the AWS NLB’s hostname.

Test by curling that external IP/hostname (or pointing a DNS record to it):

```
curl http://<elb-hostname>/graphql -d '{"query":"{ hello }"}' -H "Content-Type: application/json"
```

Should yield the GraphQL response if all is correct.

**Deploying with Rancher**:
If using Rancher, you could instead:

- Use Rancher UI to create deployments and services (you can paste YAML in GUI or use form).
- Or use Rancher's Continuous Delivery: push these YAMLs to a Git repo and have Rancher (via Fleet) apply them automatically.
- The advantage: Rancher might manage the cluster via nice UI, and you can monitor pods, etc.

## Best Practices for AWS Deployment

- **High Availability**: We deployed across multiple AZs (node group covers at least 2 AZs). The NLB will also route to instances in multiple AZs. This means even if an AZ goes down, the cluster still has nodes in another AZ running OpenResty and Node pod ([Best practices with ASG | AWS re:Post](https://repost.aws/questions/QU49gICXuKTAq7i_c3FxIE8A/best-practices-with-asg#:~:text=Best%20practices%20with%20ASG%20,across%20AZs%2C%20ensuring%20better))】. For the database: DocumentDB and ElastiCache (if used) also were configured multi-AZ (3 nodes, etc.) so they can survive AZ outage with failover.
- **Auto Scaling**: Our EKS node group can scale nodes (we set max 4). We could integrate Kubernetes **Horizontal Pod Autoscaler (HPA)** for Node deployment to increase pods if CPU or memory is high. Also cluster autoscaler can add nodes if pods can’t be scheduled. Terraform doesn't set up cluster autoscaler by default, but you can deploy the cluster-autoscaler Kubernetes deployment with proper IAM to manage ASG.
- **Immutable Infrastructure**: If updating our Node app, we'd build a new Docker image and update the Deployment (using `kubectl set image` or apply new YAML). Kubernetes will rolling update with zero downtime (it’ll spin up new pods before terminating old, thanks to readinessProbes). This achieves zero-downtime deploys.
- **Terraform State**: Use remote state backend (like an S3 bucket with locking via DynamoDB) so that state is not lost and multiple team members can work safely.
- **Monitoring and Logging**: Ensure CloudWatch is capturing EKS node logs (if you installed CloudWatch agent). We’ll cover more in Monitoring section, but for deployment ensure that e.g. the NLB is not logging by default, but we can enable if needed for access logs (to S3). Kubernetes can send logs to CloudWatch using FluentBit, or use an EFK stack.
- **DNS**: Consider setting up Route53 to map a friendly domain to the NLB or ALB. E.g., create a CNAME `cms.mydomain.com` to the LB DNS name. This can be Terraform-automated as well with `aws_route53_record`.
- **Bastion/Access**: All app is in private subnets except LB. To access pods or DB for debugging, one might set up a bastion host or use AWS SSM Session Manager on the nodes. This avoids exposing SSH directly. If using DocumentDB, to connect from local, you might need to port-forward or use a client in cluster. For operations, consider such access patterns.
- **CI/CD**: Automate the build and deployment. For instance, use GitHub Actions to:
  - Run tests on code push.
  - Build Docker image and push to ECR.
  - Update Kubernetes deployment (maybe by committing updated image tag to a manifest in Git which triggers Rancher Fleet or ArgoCD to deploy).
  - Or use `kubectl set image` in the pipeline with proper auth to cluster.
    This ensures consistent deployments. Terraform changes should also go through a pipeline (e.g., using Terraform Cloud or running plan/apply with approvals).
- **Rollbacks**: With Terraform, keep versions of state and config so you can revert infra changes. With Kubernetes, if a deploy fails, you can roll back to previous image tag easily. Consider using deployment strategies like blue-green or canary if downtime and risk must be minimized further.

Our deployment approach combined IAC (for infra) with Kubernetes manifests (for apps). Alternatively, one might deploy via ECS:

- Use Terraform to create an ECS cluster, Task Definitions for Node and OpenResty, and a Service with an Application Load Balancer. ECS would manage container placement. This is a bit simpler for smaller scale but less flexible than full K8s.
- Another approach is using AWS App Runner or Lambda for Node (but not so straightforward for our full stack with stateful DB).
  Given the advanced nature of the stack, EKS is a suitable choice and matches our Rancher usage.

We have now deployed the stack on AWS following best practices (multi-AZ, auto-scaling, infra as code, etc.). Next, we will discuss strategies for scaling this deployment to handle high traffic.

# Scaling Strategies

Scalability is crucial for an advanced CMS, especially if it must handle high traffic spikes or a growing user base. We need to ensure each layer of our architecture can scale and that we avoid bottlenecks. Scaling can be done vertically (bigger instances) or horizontally (more instances), and often a combination is used. Below we cover strategies for each component and overall considerations:

## Scaling the Node.js GraphQL Layer

**Horizontal scaling (Adding Instances)**: The stateless nature of our Node.js GraphQL server allows easy horizontal scaling. We can run multiple Node instances (as separate processes or containers) behind a load balancer. In our Kubernetes deployment, this equates to increasing the replica count of the `cms-node` Deploymen ([ Node.js: The Backbone of Modern Web Development - DEV Community](https://dev.to/vaishnavi_sonawane/nodejs-the-backbone-of-modern-web-development-49j8#:~:text=3,looking%20to%20handle%20growing%20traffic))】. With more pods, the load (queries) is spread, reducing per-instance load.

- Use Kubernetes HPA (Horizontal Pod Autoscaler) to automatically scale based on CPU or memory. For example, set HPA to maintain CPU at 50% - if average goes above, it adds pods.
- In AWS without K8s, an Auto Scaling Group for EC2 running Node (or an ECS Service’s auto-scaling) would similarly scale out tasks based on CloudWatch metrics like CPU.
- Ensure the load balancer (OpenResty or ALB) is aware of new instances. In K8s, the service will route to new pods automatically. In an ASG + LB scenario, use Elastic Load Balancer target groups with auto registration.

**Vertical scaling**: We can use more powerful EC2 instance types or allocate more CPU/RAM to pods. Node.js performance is single-threaded per process, but it can utilize more CPU if using clustering (spawning child processes per core) – though in containers we often just run one process per container and scale out containers. If using Node cluster mode (say 4 workers on a 4-core machine), that can also be considered and balanced vs. running 4 separate containers.

**Manage concurrency**: Node can handle many concurrent connections thanks to non-blocking I/O. But heavy CPU tasks in resolvers (e.g., complex calculations) can block the event loop. Offload such tasks or use worker threads if needed, or more likely, distribute the work to other services or caches to avoid blocking Node. This isn't scaling per se, but optimization to ensure Node remains scalable.

**GraphQL Query Optimization**: Use techniques to reduce load:

- Implement **DataLoader** to batch database calls and avoid N+1 query issues, thus one GraphQL query results in fewer DB roundtrip ([Performance | GraphQL](https://graphql.org/learn/performance/#:~:text=different%20kinds%20of%20objects%2C%20the,individual%20GraphQL%20operations%20from%20placing))】.
- Cache frequently requested data either at the Node level (in-memory or Redis). We did this with Redis caching in resolvers, which reduces how much load each query puts on the DB.
- Limit query complexity: as part of scaling and security, restrict how expensive queries clients can send (e.g., depth limit, or cost analysis ([Best Practices | GraphQL](https://graphql.org/faq/best-practices/#:~:text=No%20matter%20the%20concern%2C%20it%E2%80%99s,complete%20are%20all%20potential%20approaches))】. This prevents a single expensive query from hogging resources that could slow down others (which is kind of scaling within the query space).
- Use CDN for certain queries if possible: though GraphQL is dynamic, if some data can be exposed via a REST or CDN-friendly way (or if using GET queries and responses that can be cached at CloudFront), that offloads Node. This is an edge caching approach.

## Scaling the Database (MongoDB)

The database often becomes the bottleneck as traffic scales. Strategies for MongoDB:

- **Vertical Scaling**: Move to larger instance types (more RAM, faster disks). More RAM can allow Mongo to keep more of the working set in memory, speeding up reads.
- **Replica Sets for Read Scaling**: With MongoDB, you can have secondaries which can serve read-only queries. In a CMS, many operations are reads (viewing content). We can configure certain GraphQL resolvers to use a secondary for read operations (using readPreference=secondary). This distributes read load among multiple nodes while the primary handles write ([Replication - MongoDB Manual v8.0](https://www.mongodb.com/docs/manual/replication/#:~:text=Replication%20,provide%20redundancy%20and%20high%20availability))】.
- **Sharding for Write/Storage Scaling**: If data volume or write QPS grows beyond a single node’s capacity, implement shardin ([Sharding - MongoDB Manual v8.0](https://www.mongodb.com/docs/manual/sharding/#:~:text=Sharding%20,sets%20and%20high%20throughput))】. Sharding splits the data by a shard key across multiple servers. Each shard is a smaller replica set. This allows near-linear scaling of write throughput and total data size. But it adds complexity (must choose a good shard key to distribute load evenly).
- For example, if the CMS has multi-tenant data or lots of content, one might shard by tenant or content type. However, for many CMS use-cases, a single powerful node or a small replica set might suffice unless extremely high scale.
- **Optimize queries and indexes**: Ensure all frequently run queries have appropriate indexes. Use MongoDB’s profiler or explain plan to detect any full collection scans and index accordingly. Efficient queries reduce load and thus indirectly improve scalability.
- **Use Managed Services**: Using Amazon DocumentDB or MongoDB Atlas can offload some scaling tasks (they can auto-scale underlying resources or provide push-button scaling). They also manage replication and failover for you, so you can easily increase instance sizes or add replicas.

- **Caching results**: We already integrate caching (Redis, OpenResty microcache) to reduce how often the DB is hit. This is a primary scaling strategy: serve repeated content from cache rather than hitting the databas ([Performance | GraphQL](https://graphql.org/learn/performance/#:~:text=different%20kinds%20of%20objects%2C%20the,individual%20GraphQL%20operations%20from%20placing))】. A cache like Redis can handle an extremely high read throughput that would otherwise overwhelm Mongo. We should monitor cache hit rates and optimize TTLs to maximize hits for hot data.

## Scaling the Cache Layer (Redis)

Redis itself can become a bottleneck if not scaled:

- **Vertical**: Use a larger instance type or one with more memory if the dataset grows. More memory = can cache more data.
- **Horizontal (Sharding)**: Redis supports clustering, which shards keys across multiple nodes. This is useful if you need to scale beyond one node’s CPU or memory. Redis Cluster mode partitions the keyspace, so e.g. keys starting with A-M on one node, N-Z on another, etc. The client or cluster proxies manage routing. This can achieve horizontal scaling for caching.
- **Replication for Read Scalability**: If we do a lot of read from Redis (less likely, since cache reads are usually super fast anyway), we can have replicas. Typically, replication in Redis is more for HA (failover via Sentinel) than load distribution, because one node can handle huge read load. But it’s an option to have read replicas.
- **Avoid cache stampede**: This is more of an app strategy – when cache expires and many requests hit DB at once. Use techniques like cache-aside with locking or regenerate cache before expiry (or the `proxy_cache_lock on` we used in Nginx, similarly in code we could have only one process refresh an expired key).
- **Connection scaling**: Ensure Redis max clients setting is high enough. With many Node instances all connecting, check that we don't exceed default (10k). Usually fine.

Given Redis's speed, often a single instance can handle what multiple DB instances could not. But if pushing extreme load, consider clustering. Also consider alternatives like **AWS ElastiCache** which can cluster automatically and use their Global Datastore for cross-region replication if needed.

## Scaling the Web Server / Proxy (OpenResty/Nginx)

Our OpenResty layer can also scale horizontally:

- We deployed 2 replicas of OpenResty. We can increase that if needed (the load balancer will distribute traffic among them).
- Nginx (OpenResty) is very efficient with memory and can handle thousands of connections per instance (especially if properly tuned with enough worker_processes equal to CPU cores). We should monitor its CPU usage; if it's low but handling fine, we may not need many instances.
- **Microcaching** on OpenResty significantly improves how many requests it can serve because it avoids forwarding every request to Nod ([The Benefits of Microcaching with NGINX](https://blog.nginx.org/blog/benefits-of-microcaching-nginx#:~:text=Microcaching%20is%20an%20effective%20method,very%20short%20periods%20of%20time))】. This means each OpenResty instance can handle more throughput by serving repeated requests from cache in-process (very fast). This reduces the need to scale Node or Nginx as aggressively.
- If using AWS ALB instead of Nginx, ALB scales automatically by AWS (you don't manage instances). But since we are using Nginx for caching and Lua, we consider scaling it ourselves.
- If extreme load mostly on static assets, consider using a CDN (CloudFront) in front of Nginx to cache static files globally. For dynamic GraphQL, CDN isn't straightforward unless using persisted queries or specific query caching.

**Load Balancer Scaling**: For NLB, AWS can handle millions of requests per second spread across AZs as long as the instances can handle it. For ALB, AWS scales the load balancer capacity as load grows (gradually). There are AWS limits (like new connections per second) but they are high and can be increased. The main point: ensure LB isn't a bottleneck by using multi-AZ and enabling cross-zone load balancing if needed.

## Auto-Scaling Policies and Testing

- Implement auto-scaling triggers at all tiers where possible. E.g., CPU > 70% on Node pods -> add pods; Memory > 70% on Mongo instance -> maybe alert or scale up cluster size if using Atlas.
- Ensure you have scaling cooldowns to prevent flapping.
- Test scaling in staging: simulate load (using a tool like JMeter, Locust, or k6) to see at what point you need to scale out. Identify the bottleneck (maybe DB CPU saturates first, or Node event loop starts lagging which you can detect via metrics like event loop lag).
- Have a capacity plan: know how many requests per second a single Node pod can handle for typical queries, how many DB ops per second Mongo can do, etc., and plan scaling thresholds accordingly.

## Decoupling and Microservices (Advanced Scaling)

As the system grows, you might consider breaking out services:

- Perhaps separate the GraphQL gateway from microservices that handle specific parts (for example, a microservice for Search, one for Images, etc.). GraphQL can federate or stitch multiple schemas. This allows scaling each component independently.
- For instance, if image processing is heavy, have a separate service (with its own DB maybe) just for that, and GraphQL gateway calls it (via REST or through a GraphQL federation approach).
- Our current design is a monolithic Node app connecting to one DB. Monolith is simpler and scaling it horizontally often suffices for quite large scale if the code is efficient and data layer is robust. But microservices might become necessary if different parts of the system have very different scaling profiles or team ownership.

## Database Scaling Strategies (Recap and more)

- Implementing **caching at multiple layers** (Redis, Nginx) was one of our strategies.
- Additionally, implement **write-through or write-back cache** if needed: e.g., when content is updated, pre-populate cache for queries that would fetch it. This can reduce cache misses on content that was just changed (which might ironically cause high DB load after an update if everyone requests the new content at once).
- For Mongo specifically, consider using features like **compression** to reduce disk I/O, and ensure using WiredTiger which handles concurrency well.

## Content Delivery Network (CDN)

While not directly part of our stack, using a CDN for static content (images, JS/CSS for front-end) or even generated pages can offload work:

- If the CMS pages are eventually served to end-users as HTML, those could be cached on CloudFront or similar. If GraphQL is used directly by clients (like SPAs), then caching at CDN is harder (but you could cache GraphQL GET requests on CDN for anonymous data queries).
- Some headless CMS patterns involve generating static content or using SSR (server-side rendering) and caching that. If in future the CMS adds a public GraphQL endpoint for all, consider how to leverage CDN for certain heavy queries.

## Asynchronous Processing

Offload tasks from request-response cycle:

- If some operations are slow (like resizing images, sending emails on content publish, etc.), use background job queues (e.g., AWS SQS or a job framework with Redis). This doesn’t directly scale in terms of throughput for reads, but improves user-perceived performance and prevents tying up Node worker on tasks that could be done out-of-band.
- In extreme cases, one might precompute certain views or analytics periodically and cache them (so queries need not aggregate large data in real-time).

## Scale Monitoring

Scaling isn't set-and-forget. Implement monitoring (which we cover next) to watch key metrics:

- Node: CPU, memory, event loop lag, request rate, error rate.
- Mongo: op counters, replication lag, cache hit ratio (WiredTiger cache).
- Redis: memory usage, cache hit/miss count.
- Nginx: request per second, upstream response time, number of active connections.
- Based on these, adjust scaling policies or capacity.

By applying the above strategies, our CMS should be able to handle significantly higher loads:

- Horizontal scaling on stateless layers (Node, Nginx) gives near-linear capacity growth.
- Vertical/horizontal scaling on stateful layers (Mongo, Redis) ensures the data layer can keep up.
- Caching and load-shedding (limits on query complexity) reduce the load on backend components.
- Auto-scaling automates the addition/removal of resources on demand, maintaining performance during traffic spikes and saving cost when idle.

Next, we will focus on monitoring and logging, which is essential to ensure our scaled system is actually performing well and to catch issues early.

# Monitoring and Logging

Monitoring and logging are vital for maintaining a healthy production system. They provide visibility into how the CMS is performing, help detect anomalies or errors, and assist in debugging issues. We will set up monitoring for each part of the stack (Node.js, MongoDB, Redis, OpenResty, and underlying infrastructure) and configure centralized logging so we can inspect logs from all components in one place. We'll also discuss alerting and best practices for analyzing metrics.

## Infrastructure and System Monitoring

At the AWS infrastructure level:

- **AWS CloudWatch**: Provides metrics for EC2 instances (CPU, network, disk), ELB (request count, latency, HTTP 500 counts), etc. For EKS, CloudWatch Container Insights can gather CPU/mem for pods if enabled. Ensure that:

  - EC2 instances (or Kubernetes nodes) have the CloudWatch agent or at least default metrics. EKS nodes by default publish metrics via CloudWatch if you installed Container Insights.
  - Monitor node CPU/Memory to know if we are nearing limits. For example, set an alarm if any node’s CPU > 85% for 5 minutes (could indicate need to scale out).
  - Monitor network traffic to see if nearing bandwidth limits.

- **Terraform CloudWatch Alarms**: We can create alarms for critical metrics. E.g., if CPU on the database instance goes above 90%, or if freeable memory goes below a threshold, trigger an alarm (possibly integrated with an SNS topic to email/SMS the devops team).

- **Rancher Monitoring (Prometheus)**: If using Rancher, enable the Monitoring stack which deploys Prometheus and Grafan ([Monitoring and Alerting - Rancher](https://ranchermanager.docs.rancher.com/integrations-in-rancher/monitoring-and-alerting#:~:text=Prometheus%20lets%20you%20view%20metrics,and%20how%20to%20enable))】. This can automatically collect metrics from Kubernetes (via node exporter, cadvisor, etc.) and from application pods if they expose metrics. Rancher’s monitoring provides pre-built dashboards for cluster and workloads:
  - You’ll get dashboards for CPU/memory of nodes, pods, etc., which is very helpful.
  - Prometheus will scrape metrics from K8s and possibly from our app if we instrument it (more on that soon).

## Application Monitoring (APM and Metrics)

**Node.js Monitoring**:

- Use application performance monitoring (APM) tools or libraries. For Node, popular ones include New Relic APM, Datadog APM, or open-source solutions like Grafana Tempo for tracing and Prometheus for metrics.
- **Metrics collection**: We can expose custom metrics from the Node app. For example, use the **Prometheus client** for Node to track:
  - Request count, split by type (query/mutation) or even per GraphQL operation name.
  - Request durations (histogram).
  - DB query count per request.
  - Cache hit/miss counters.
  - Memory usage and event loop lag (there are packages to measure event loop delay).
  - Apollo Server also can provide some metrics by default or via plugins.
- If we integrate the Prometheus client, we can add an endpoint like `/metrics` that Prometheus (from Rancher monitoring or own deployment) can scrape. That way, we have fine-grained app metrics in Grafana.
- **Distributed tracing**: Implement OpenTelemetry in Node to trace requests through to the DB. This is advanced, but basically Node can create a trace for each GraphQL request, annotate spans for each resolver/db call, and send to a tracing backend (Jaeger, Zipkin, etc.). This helps pinpoint slow operations across services.

**MongoDB Monitoring**:

- If using DocumentDB or Atlas, they come with monitoring dashboards (Atlas has built-in monitoring UI, DocumentDB integrates with CloudWatch).
- For self-managed Mongo, enable the **MongoDB Monitoring Service (MMS)** or use tools like **Percona Monitoring and Management (PMM)** for Mongo which uses Prometheus exporters.
- Key metrics to watch:
  - Opcounters (read/write counts).
  - Current connections.
  - Cache usage (WiredTiger cache eviction rate, dirty cache).
  - Lock % (less of an issue with WiredTiger, but still check if any locks are high).
  - Replication lag (if using replicas).
- Set alerts on conditions like replication lag > X seconds, or suddenly high number of slow queries.
- Slow query log: enable profiling for slow queries (e.g., >100ms) to get logs of them. These can be logged to a file or DB collection. Use this to optimize slow queries.

**Redis Monitoring**:

- Use Redis’ INFO command regularly to gather stats. Better, use a Prometheus Redis exporter to scrap metrics (like memory_used, hits/misses, connected clients, evicted_keys).
- Look at cache hit ratio. If low, maybe our cache TTLs are too short or coverage is low. If high (over 90%), good.
- Monitor Redis CPU (usually low unless running Lua scripts) and memory. Ensure memory usage is below the maxmemory setting; if it hits maxmemory and evictions are happening (check `evicted_keys` in INFO), that means cache thrashing – might need to increase maxmemory or evaluate what can be cached less.
- If using ElastiCache, CloudWatch provides metrics like CPUUtilization, CurrConnections, Evictions, etc. Set alarms if e.g. evictions are steadily increasing (meaning cache overflow).

**Nginx/OpenResty Monitoring**:

- Nginx can output status info via the stub_status module (gives active connections, requests per second). Enable an endpoint `/nginx_status` protected by IP restriction. Prometheus has an exporter that can parse this.
- OpenResty XRay (if using OpenResty Inc’s tools) can provide deep insight, but for our purposes basic metrics suffice.
- Log metrics: we can configure Nginx to log request processing time, upstream time, response size, etc., and use a tool like GoAccess or feed logs to ELK to derive metrics. But that's post-facto analysis.
- If using Prometheus, use the **nginx-exporter** or VTS (Virtual host traffic status) module which provides more metrics via JSON for Prometheus to scrape.
- We want to know requests per second, error rate (5xx from Nginx or upstream), and upstream response times to catch if backend is slow.
- If we see upstream_response_time rising, it's a sign the Node or DB is a bottleneck. If Nginx itself has high request processing time without upstream, maybe serve stall on Nginx (rare unless disk IO for static files is an issue).
- Monitor Nginx memory and worker process CPU. Typically, Nginx is event-driven so CPU goes up with high throughput but rarely the first thing to break.

## Centralized Logging

Collecting logs from all parts of the system into one place greatly aids troubleshooting:

- **Use a Logging Stack (ELK/EFK)**: ELK = Elasticsearch, Logstash, Kibana. EFK uses Fluentd/Fluentbit instead of Logstash. On Kubernetes, an easy approach is:
  - Deploy **Fluent Bit** as a DaemonSet to collect logs from all pods (it can read container stdout from the node file system) and send them to Elasticsearch or a cloud log service.
  - Alternatively, use **CloudWatch Logs**: The CloudWatch agent on EKS can be set to push container logs. AWS also has a service called Container Insights (with Fluent Bit) that can send logs to CloudWatc ([Sending node logs to unified CloudWatch Logs (CloudWatch agent)](https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-cloudwatch-agent.html#:~:text=agent%29%20docs,those%20supplied%20by%20SSM%20Agent))】.
- For a non-K8s scenario, use the **CloudWatch Logs agent** on each instance to ship syslogs, application logs to CloudWatch. Or run a centralized syslog/Fluentd that receives logs.
- **Structure logs**: It's useful to log in JSON format so that it's easy to parse and search. For Node, use a logger like Winston or Bunyan to output JSON logs (with fields for level, message, requestId, etc.). Nginx can be configured with JSON log format (using the log_format directive). Or use key-value pairs in logs.
- Example: Node could log `{"level":"error","msg":"DB query failed","error":"...","operationName":"getArticles","requestId":"123"}`. Nginx could log `request_id=$reqid status=$status upstream_time=$upstream_response_time`.
- **Correlation**: Pass a correlation ID through the system. For instance, use an `X-Request-ID` header: OpenResty can generate a UUID for each request, add `X-Request-ID`, forward to Node. Node includes that in any log lines. Nginx logs it. Then when debugging, you can filter logs in Kibana by that ID to see the trace of a specific request across layers.
- **Retain logs**: Decide retention period (maybe 7-30 days in production). Ensure log storage (Elasticsearch or CloudWatch) has lifecycle policies to delete old logs to save space.
- **Alerting on logs**: Set up alerts for certain log patterns:
  - e.g., if "ERROR" logs in Node exceed X per minute, alert.
  - If Nginx logs frequent 502/504 errors (meaning backend issues), alert.
  - Use CloudWatch Logs Insights or Kibana watchers for this.

## Dashboarding and Alerting

- **Grafana Dashboards**: With Prometheus (via Rancher or custom), set up dashboards for:
  - Application: GraphQL QPS, latency, error rates, cache hit ratio.
  - Database: e.g., ops count, lock %, primary vs secondary traffic.
  - System: CPU/mem of nodes, number of pods running, etc.
    Rancher’s built-in Grafana likely already has cluster dashboards. Customize or add new ones for app metrics.
- **Alertmanager**: If using Prometheus, configure Alertmanager to send alerts (email/Slack/PagerDuty) based on rules. E.g., if 5xx error rate > 5% for 5 minutes => alert, if memory on Redis > 90% => alert.
- **Uptime Monitoring**: Use an external service (Pingdom, UptimeRobot, etc.) or CloudWatch Synthetics Canary to periodically hit a GraphQL endpoint (maybe a lightweight query) to ensure the system is up from outside. This catches networking or domain issues that internal monitoring might not.
- **AWS Health**: Monitor AWS Personal Health Dashboard or CloudWatch events for any issues in the region or hitting resource limits (like if hitting the max number of EC2 instances or something, AWS can emit an event).

## Security Monitoring

- **Logs for Security**: Monitor logs for unusual activity:
  - Repeated failed logins (if you have an auth system).
  - Unusual GraphQL queries (someone trying to exploit by sending deeply nested queries, etc. – your GraphQL Depth limit should mitigate but log if such attempts occur).
  - In Nginx logs, look for patterns like scanning or large payloads.
- **AWS GuardDuty**: Consider enabling GuardDuty for your AWS account to detect suspicious AWS-level events (like unusual API calls or instance traffic anomalies).
- **Kubernetes Security**: If on EKS, ensure audit logging is enabled (EKS control plane can log audit events to CloudWatch, capturing if someone execs into a pod or changes a config).
- **Prometheus alerts for security**: Could have something like alert if CPU usage spikes drastically (could indicate crypto mining if box compromised), or if an unexpected process appears on a container (harder to monitor without specialized tools, but some solutions exist).

## Error Tracking

- Use an error tracking service (like Sentry) in the Node app to capture exceptions and stack traces. This complements logging by providing a focused view on unhandled exceptions or promise rejections in the application, and can group them, notify developers, etc.
- Sentry can also track performance (similar to APM/tracing) by measuring function durations.

**Summary**: We set up a combination of:

- Metrics (Prometheus & Grafana) for quantitative monitoring (performance, resource usage).
- Logs (ELK or CloudWatch) for qualitative debugging (exact errors, messages).
- Alerts on both metrics and logs to be notified of issues proactively.
- Over time, refine thresholds (avoid alert fatigue by tuning).

By having these monitoring and logging systems:

- We can quickly detect if the system is under stress (e.g., sudden DB CPU spike or increased response times).
- We can pinpoint issues (like a specific query that always times out, by looking at logs or traces).
- We ensure reliability by catching problems before they cascade (like if Redis went down, we’d see errors and can fail over or restart quickly).
- Additionally, monitoring data helps in capacity planning – e.g., Grafana shows traffic growth over months, so we can plan to add nodes or upgrade DB ahead of time.

Next, we will look into security considerations to make sure the system is hardened against threats.

# Security Considerations

Security is critical when working with a CMS stack. We must secure each layer (GraphQL API, Node.js application, databases, caching, infrastructure) to protect data and prevent unauthorized access or attacks. Below we outline important security configurations and best practices for our tech stack:

## Network Security and Access Control

- **VPC Isolation**: We deployed components in a private VPC. Ensure that the MongoDB and Redis servers (or clusters) are in private subnets with no direct internet access. Only the application servers (Node/OpenResty) should be able to reach them. For example, configure security groups so that only the Node.js app’s instances or pods can connect to MongoDB on its port, and similarly for Redis. By default, our DocumentDB/ElastiCache were in the same VPC, which is good.
- **Security Groups**: Use least privilege rules:
  - The OpenResty load balancer SG allows inbound 80/443 from the world.
  - The OpenResty instances allow inbound from LB (or if host network, then from anywhere on port 80 if LB is not SG-limited).
  - Node instances/pods accept traffic only from OpenResty (if possible, restrict by SG or network policy).
  - MongoDB instances allow inbound on 27017 only from Node instances (SG reference or by IP range of Node subnets).
  - Redis same idea: require authentication and allow only internal access.
- **Kubernetes Network Policies**: If using Kubernetes, implement network policies to restrict pod communicatio ([15 Kubernetes Security Best Practices in 2025 - StrongDM](https://www.strongdm.com/blog/kubernetes-security-best-practices#:~:text=15%20Kubernetes%20Security%20Best%20Practices%3A,Secure))】. By default, all pods can talk to all pods in a cluster. We can lock it down:
  - Allow `openresty` pods to talk to `node` pods (on port 4000).
  - Allow `node` pods to talk to `mongo` service (if Mongo is within cluster or VPC) and `redis`.
  - Deny other cross-communication (e.g., no pod should directly talk to Mongo except node pods).
  - This acts as a micro-segmentation firewall.
- **No Public DB Access**: Confirm that MongoDB is not publicly accessible. In our case, DocumentDB by default was only in VPC (unless we set up a public endpoint, which we did not). If running your own Mongo on EC2, ensure it’s either in private subnet or firewall rules block external traffic. MongoDB without auth on the internet is a known vulnerability scenario. We will also ensure **access control (authentication) is enabled** on Mong ([Enable Access Control on Self-Managed Deployments - MongoDB](https://www.mongodb.com/docs/manual/tutorial/enable-authentication/#:~:text=MongoDB%20www,are%20required%20to%20identify%20themselves))】.
- **Bastion Host**: If you need to access the DB or servers for maintenance, set up a bastion host (jump box) in the VPC, or use AWS SSM Session Manager so that you don't open SSH to the world. If you do use SSH, lock it to specific IP addresses (your office, etc.) via security group rules.

## Authentication and Authorization

- **GraphQL API Auth**: Ensure sensitive operations require authentication. Possibly integrate JWT or OAuth:
  - E.g., to publish or edit content (mutations) require a valid JWT of an authorized user.
  - We would include an `Authorization: Bearer <token>` header; Node verifies the JWT signature (using a secret or public key). We could use a library or APOLLO's context to decode token and attach user info to context.
  - Use a strong signing algorithm (e.g., RS256 or HS256 with a long secret).
- **Role-Based Access**: Implement roles (admin, editor, viewer) in the CMS and enforce in resolvers. For example, an `updateArticle` resolver should check `context.user.role === 'editor'` or such. GraphQL doesn't have built-in auth, so we implement checks in code or use a library for directive-based auth.
- **Protecting Endpoints**: If there's an admin UI served by OpenResty, ensure it’s behind login. Possibly restrict access by IP for admin interface if feasible (like company network IP).
- **Disable GraphQL Introspection in Production**: It's recommended to turn off introspection queries in production to not expose schema details to the publi ([9 Ways To Secure your GraphQL API — GraphQL Security Checklist | Apollo GraphQL Blog](https://www.apollographql.com/blog/9-ways-to-secure-your-graphql-api-security-checklist#:~:text=While%20introspection%20is%20primarily%20helpful,to%20abuse%20a%20GraphQL%20API))】. Apollo Server allows `introspection: false` in config for production. (Keep it on in staging/dev).
- **Query Depth/Complexity Limiting**: Use a library or Apollo plugin to enforce maximum query depth or cos ([Best Practices | GraphQL](https://graphql.org/faq/best-practices/#:~:text=No%20matter%20the%20concern%2C%20it%E2%80%99s,complete%20are%20all%20potential%20approaches))】. This is both performance and security (prevents malicious queries that are extremely nested or expensive from DOS'ing the server). E.g., limit depth to, say, 5 or 6 unless client is whitelisted for more.
- **Rate Limiting**: At the API gateway level (OpenResty), consider rate limiting IP ([9 Ways To Secure your GraphQL API — GraphQL Security Checklist | Apollo GraphQL Blog](https://www.apollographql.com/blog/9-ways-to-secure-your-graphql-api-security-checklist#:~:text=Rate%20limit%20APIs))】. You can use Nginx’s `limit_req` module to throttle requests per IP (like X requests per second). GraphQL can be chatty with many small queries from one page, so tune carefully to not hamper legitimate use, but block excessive abuse.
- **CORS**: If the GraphQL API is consumed by web browsers from a different domain, configure appropriate CORS headers (Apollo can set `Access-Control-Allow-Origin`). But lock it down to known origins if possible. E.g., allow only the domains of your frontend, not `*`, to prevent potential misuse from malicious web pages.
- **Session Management**: If using sessions (like express-session with cookies), ensure cookies have `HttpOnly` and `Secure` flags, use TLS, and ideally use SameSite to prevent CSRF. But with JWT, stateless, you avoid server-side session storage. Just ensure the JWT tokens are stored securely on client (preferably in memory or httpOnly cookies).
- **Secret Management**: Do not hardcode secrets in code or images. Use Kubernetes Secrets or AWS Secrets Manager to store DB credentials, JWT signing keys, etc. We used a K8s Secret for DB connection string. Ensure IAM policies restrict who/what can access secrets (e.g., only the app).
- **Encryption in Transit**: Use HTTPS for all external traffic. Internally within VPC, also consider encrypting traffic:
  - Enable TLS for MongoDB connections if possible (DocumentDB can enforce TLS; for self Mongo, run with TLS and have Node connect with `mongodb+srv://` or certs).
  - Redis traffic can be encrypted if using ElastiCache with encryption enabled, or use stunnel if self-managed (though internal networks are less at risk).
  - At least external LB to OpenResty is HTTPS (with a proper certificate from ACM or Let's Encrypt).
- **Encryption at Rest**:
  - AWS by default can encrypt EBS volumes and DocumentDB storage. Ensure those are on (Terraform usually can set `storage_encrypted = true` for DocumentDB, EBS can be encrypted by default).
  - For Mongo on EC2, enable disk encryption at the OS level or use encrypted filesystem.
  - For Redis, snapshots or data at rest encryption if using persistent store, enable that in ElastiCache.
  - Also, any S3 buckets for media uploads should have encryption enabled and proper access policies.

## Secure Configuration of Services

- **MongoDB Access Control**: As noted, enable authentication. MongoDB should have a username/password and perhaps IP whitelist. In our config we did set a master user for DocumentD ([Replication - MongoDB Manual v8.0](https://www.mongodb.com/docs/manual/replication/#:~:text=Replication%20,provide%20redundancy%20and%20high%20availability))】. For a self-managed Mongo, you'd start without auth, create admin user, then restart with `--auth` or `security.authorization: enabled` in confi ([Enable Access Control - MongoDB Manual v7.1](https://www.mongodb.com/docs/v7.1/tutorial/enable-authentication/#:~:text=Enable%20Access%20Control%20,are%20required%20to%20identify%20themselves))】. With auth enabled, every client (Node) must provide credentials. This prevents unauthorized access if somehow the network is compromised or a port is exposed. _Never_ run MongoDB in production without access contro ([Enable Access Control on Self-Managed Deployments - MongoDB](https://www.mongodb.com/docs/manual/tutorial/enable-authentication/#:~:text=MongoDB%20www,are%20required%20to%20identify%20themselves))】.
  - Also enforce roles: the Node app user should have minimal privileges (e.g., readWrite on the application database, not cluster admin).
- **Redis Security**: Redis is by default open and no password. Set `requirepass <password>` in redis.con ([How to set password for Redis? - Stack Overflow](https://stackoverflow.com/questions/7537905/how-to-set-password-for-redis#:~:text=How%20to%20set%20password%20for,change%20foobared%20to%20your%20password))】. We did in dev optionally; in prod it's a must unless access is perfectly restricted. That way, even if someone got network access, they'd need the password to run command ([Redis security | Docs](https://redis.io/docs/latest/operate/oss_and_stack/management/security/#:~:text=When%20the%20requirepass%20setting%20is,sending%20the%20AUTH%20command))】.
  - Additionally, Redis 6 supports ACLs (so you could create a user with certain commands only). You might not need that complexity for caching, but good to know.
  - If using ElastiCache, use the Redis AUTH feature (Elasticache can generate an auth token or you can set one). And ElastiCache is in VPC so it's not reachable externally by default.
- **OpenResty/Nginx**:
  - Keep it updated (OpenResty updates include Nginx security patches). If using a Docker image, watch for new releases and rebuild.
  - Disable any modules or features not needed (from our compile, we disabled some). For instance, ensure we don't have `lua_code_cache off` in prod (should be on for performance).
  - Use TLS best practices on OpenResty: only strong ciphers, enable HTTP2, use a well-known TLS config (there are templates from Mozilla). In config: `ssl_protocols TLSv1.2 TLSv1.3; ssl_ciphers HIGH:!aNULL:!MD5;`.
  - HTTP security headers: Have OpenResty add headers like `Strict-Transport-Security` (HSTS), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN` (maybe not needed for API but for any HTML content), `Referrer-Policy`, and `Content-Security-Policy` if serving any HTML/JS. Apollo Playground should probably be disabled in prod, but if not, also secure that.
- **Node.js**:
  - Update dependencies regularly (run `npm audit`). Many security issues arise from outdated packages. Have a schedule or use dependabot.
  - Turn off detailed error messages in production (don’t leak stack traces or internal info to clients).
  - If using Express under Apollo, ensure you don’t have any other routes that could be exploited. For example, disable the default `/favicon.ico` if not needed, etc.
  - Limit payload size: GraphQL could be abused by sending huge queries or data. Use something like `graphql-depth-limit` and also perhaps an upload size limit on the Node server (Apollo has a default, but verify) to avoid out-of-memory.
  - Run Node as a non-root user in containers (our Dockerfile used node:alpine which by default runs as root, but we can switch to a node user, or better use `node:18-alpine` which often has a `node` user available). It's good we set in Dockerfile `USER node` to avoid running as root in container.
  - Set `NODE_ENV=production` in production to disable dev features and enhance performance (we did that by using `npm ci --only=production` which implies production mode).
- **Terraform and AWS**:
  - Limit IAM permissions. The IAM role used by our app (if any, say if accessing S3) should have only necessary perms.
  - The IAM user with AWS keys (for Terraform) should be kept safe. Use Terraform Cloud or a secure pipeline so keys aren't on dev machines.
  - Enable MFA on AWS console access.
  - For S3 buckets (if storing media), enforce encryption and proper bucket policies (only allow CloudFront or certain roles to fetch if needed).
  - If using ECR for images, restrict who can push/pull (though by default only your AWS account can).
- **Secrets in Terraform**: If writing secrets (like DB password) in Terraform .tfvars, secure that file (gitignore, maybe store in a secure vars store). Or use Terraform to pull from AWS Secrets Manager.

## Penetration Testing and Hardening

- Consider running a vulnerability scan or pentest against the system. Tools like OWASP ZAP can test the web endpoints. For example:
  - Test GraphQL endpoint for typical vulnerabilities like SQL injection (not applicable to Mongo exactly, but NoSQL injection, though Mongoose will handle queries as objects, still watch out for $where injection if using unsanitized input in queries).
  - Check for GraphQL introspection being disabled and not leaking info.
  - Try sending deeply nested queries or huge arrays to see if our limits hold up.
  - Check for open ports that shouldn't be open (use nmap on your public IP to ensure only 80/443).
- **Hardening OS**: Ensure base images are minimal and updated. The node:alpine is decent (small and fewer packages to exploit). If using Amazon Linux on EC2 for DB, keep it updated with security patches. Use tools like Lynis or CIS benchmarks for Linux hardening if managing servers.
- **Containers**: Use image scanning (many CI/CD or registry (ECR) have scanning for vulnerabilities in images). Address critical CVEs by updating base images or packages.
- **Kubernetes**:
  - Make sure K8s API server isn't exposed publicly (EKS by default can have a public endpoint; lock it down to specific CIDRs or use private endpoint if possible, so only via bastion or VPC one can access cluster API).
  - Use RBAC properl ([Role Based Access Control Good Practices - Kubernetes](https://kubernetes.io/docs/concepts/security/rbac-good-practices/#:~:text=Kubernetes%20RBAC%20is%20a%20key,required%20to%20execute%20their%20roles))】: ensure no overly permissive serviceaccount tokens are in use. In our case, if using default, limit access. Use separate namespace (we did "cms") to isolate. Perhaps ensure the cms namespace cannot access other namespaces' secrets by default (K8s tends to isolate, but cluster-admin roles etc. be careful with).
  - Consider implementing Pod Security Policies or Pod Security Standards to prevent risky container config (like no privileged containers, etc.). Our Node and openresty containers don't need to run privileged or with host mounts, so we should enforce that via PSP or the newer PSA (Pod Security Admission).
  - Ensure secrets in K8s are indeed treated as secret (in EKS, they are plaintext in etcd by default unless using KMS encryption - consider enabling KMS envelope encryption for secrets).

## Audit and Logging for Security

- **Audit Logs**:
  - GraphQL queries could be logged (maybe at least operation names and user who made them) to an audit log for content changes. E.g., log every mutation with user ID.
  - MongoDB can log authentication attempts or other admin actions.
  - AWS CloudTrail is enabled to record AWS API calls - use it to detect if any changes to infrastructure or unusual API calls.
  - Kubernetes audit log (if enabled in EKS) to see if someone tried to escalate privileges.
- **Log retention for security**: Keep logs relevant to security (auth logs, AWS CloudTrail, etc.) for longer (months or a year) in case needed for forensic analysis.

## Regular Updates and Maintenance (Security Perspective)

- Keep up with security updates for all components:
  - E.g., if a vulnerability in Apollo Server is announced, update that dependency promptly.
  - Watch MongoDB and Redis release notes for security fixes, apply patches (managed services handle that mostly under the hood with minor version upgrades).
  - Nginx/OpenResty - monitor their mailing lists or repos for patches and rebuild the image.
- Use automated tools where possible: e.g., Dependabot for Node packages, ECR scanning for images, AWS Inspector for EC2 (if any) to identify missing patches.

## Backup and Recovery

- Ensure backups are in place for data (though not a direct security measure, it mitigates ransomware or data loss):
  - MongoDB/DocumentDB: Take daily snapshots. Mongo Atlas does automatically if used. DocumentDB can snapshot to S3. If self-managed, run backups (mongodump or file snapshot).
  - Redis: If it's just a cache, backup not needed, but if using it as a data store (e.g., session store), consider enabling RDB snapshots to S3 or backup service.
- Test restore procedures to ensure data can be recovered in case of an incident.
- Keep backups encrypted as well (AWS snapshots can be encrypted).

By applying all these security measures:

- We reduce attack surface (only port 443 open publicly, no DB exposure).
- We enforce strong access controls at every layer (auth at API, RBAC in cluster, user roles in app, requirepass on Redis, Mongo auth (['openresty' tag wiki - Stack Overflow](https://stackoverflow.com/tags/openresty/info#:~:text=OpenResty%20aims%20to%20run%20your,MySQL%2C%20PostgreSQL%2C%20Memcached%2C%20and%20Redis)) ([Redis security | Docs](https://redis.io/docs/latest/operate/oss_and_stack/management/security/#:~:text=When%20the%20requirepass%20setting%20is,sending%20the%20AUTH%20command))】.
- We mitigate common web vulnerabilities (CORS, injection, XSS via CSP on any served content, etc.).
- We prepare for worst-case by having audit logs and backups.

Security is an ongoing process; we should perform periodic security audits and update our configurations. Also educate developers to avoid introducing vulnerabilities (like not sanitizing inputs or accidentally logging sensitive data).

Next, we'll compile common issues and troubleshooting tips if things go wrong in our stack.

# Troubleshooting Guide

Even with careful setup, issues will arise. This guide lists common problems in each part of the stack and solutions or diagnostic steps to resolve them. Organized by component, it will help quickly identify the root cause when something goes wrong.

## Node.js & GraphQL Issues

**Issue:** High response times or timeouts for GraphQL queries.  
**Symptoms:** Queries that normally are fast become slow, or the client receives 504 Gateway Timeout from OpenResty after 60s (for example).  
**Possible Causes & Solutions:**

- _Database slowness_: Check if the MongoDB query in that resolver is slow (perhaps an index is missing causing a full scan). Use MongoDB’s `explain()` on the query or check for slow query logs. Adding an index or optimizing the query can resolve this.
- _N+1 query problem_: If a resolver triggers many DB calls (e.g., in a loop without DataLoader), it can slow things drastically. Use DataLoader to batch those call ([Performance | GraphQL](https://graphql.org/learn/performance/#:~:text=different%20kinds%20of%20objects%2C%20the,individual%20GraphQL%20operations%20from%20placing))】.
- _External call latency_: If the resolver calls an external API, the delay might be outside our system. Consider adding timeouts or caching the external data.
- _Server overload_: Node’s event loop might be saturated (perhaps too much CPU work in JS). Monitor CPU – if at 100%, Node can’t keep up. Scaling out nodes or moving CPU-intensive work (like image processing) to background jobs can help.

**Issue:** GraphQL resolver throwing errors (500 errors or “Internal Server Error” in client).  
**Symptoms:** Apollo returns an error for a field or entire query; logs show exceptions.  
**Possible Causes & Solutions:**

- _Undefined property or TypeError in resolver_: A bug in our code (e.g., assuming a field exists). Add defensive checks in the code to prevent exceptions, or fix the logic. Logs/stacktrace will pinpoint where.
- _Database connection issue_: If `mongoose.connect` failed or dropped, any DB call throws. Look at Node logs on startup for a connection error (e.g., “MongoDB connection error”). Solution: ensure the DB is reachable (check network, security group) and credentials are correct. The app should attempt reconnection (Mongoose by default will retry some). If credentials were wrong, fix the secret and restart.
- _Redis connection refused_: If caching logic tries to use Redis but it’s down or URL wrong, it might throw. Check logs for Redis client errors. Ensure Redis is up (e.g., `redis-cli ping` from the Node container’s perspective). Fix network or credentials. Possibly make the code handle cache failures gracefully (e.g., catch and log but not crash).
- _GraphQL Validation errors_: If introspection is off, GraphQL Playground might show errors introspecting. That’s expected if you disabled introspection in production for securit ([9 Ways To Secure your GraphQL API — GraphQL Security Checklist | Apollo GraphQL Blog](https://www.apollographql.com/blog/9-ways-to-secure-your-graphql-api-security-checklist#:~:text=While%20introspection%20is%20primarily%20helpful,to%20abuse%20a%20GraphQL%20API))】. Re-enable in non-prod environment if needed.
- _File upload issues_: If using GraphQL for file uploads (Apollo supports multipart), misconfig could cause errors. Check that OpenResty proxy buffers are large enough if handling uploads, or use direct S3 upload to avoid this path.

**Issue:** Memory leak in Node process (memory usage growing over time, possibly hitting container limit and restarting).  
**Symptoms:** Kubernetes OOM kills the pod, or `dmesg` shows out-of-memory for the Node process; or monitoring shows memory linearly increasing.  
**Possible Causes & Solutions:**

- _Global variables accumulating_: Ensure no large data structures are being kept around unintentionally. For example, caching in memory inside Node (we prefer Redis for cache to avoid this). Use tools like Chrome DevTools inspector or `memwatch-next` to find leaks.
- _Unhandled Promises or recursive function not freeing memory_: If a promise rejection is unhandled, Node might not free contexts; add proper `.catch`. If recursive, ensure termination.
- _Too high concurrency without backpressure_: If Node is queuing many requests (because DB is slow), memory might fill with pending promises. Solution: limit concurrency (e.g., using a queue or semaphore pattern for heavy operations).
- _Excessive logging in memory_: If using something like Winston with a large buffer or not properly streaming logs, that could accumulate. Use log rotation or direct stdout (which we do in container).

**Issue:** Cannot connect to GraphQL endpoint (client gets network error, or HTTP 502/504 from Nginx).  
**Symptoms:** The service is down or inaccessible.  
**Possible Causes & Solutions:**

- _Node process crashed_: If Node crashed (maybe due to an unhandled exception that took down the process since Node by default doesn’t respawn), in K8s the pod would restart. Check `kubectl get pods` – if you see CrashLoopBackOff for Node pods, inspect logs (`kubectl logs pod -p` to get previous container log) to see crash reason. Fix underlying error in code.
- _OpenResty cannot reach Node_: OpenResty might log upstream timed out or host not found. If host not found, maybe the `upstream cms_node` DNS (service name) not resolving – check that the OpenResty container is in the same namespace or has correct DNS config (maybe missing `dnsPolicy: ClusterFirst` or service name typo). If upstream timed out, Node might be down or overloaded. Check Node pods.
- _Misconfigured LB or service_: If using AWS ALB, perhaps target health checks are failing (so LB not sending traffic). Ensure health check path is correct (we used `/healthz`). If failing, Node might not be responding with 200 – implement a simple GET /healthz that returns OK (or allow GET on GraphQL with a trivial query as health).
- _CORS blocking request_: If the front-end is in browser and GraphQL returns nothing, check console – CORS errors indicate maybe our Apollo server not sending CORS headers. Ensure Apollo `cors` options allow the origin or we configured Nginx to pass them.

**Issue:** Unusually high latency for first request after deployment or cache clear.  
**Symptom:** The first query after a while is slow, subsequent are fast.  
**Explanation:** This is likely due to cold caches: both at MongoDB (cold indexes in memory) and at Node/Redis level. Also if using `NODE_ENV=production`, the first request may trigger JIT or other initialization. This is typically normal. You can mitigate by warming up the system: run some queries after deploy (maybe a startup script or livenessProbe triggers a simple query) to populate caches. For Mongo, ensure adequate memory to keep working set to avoid disk hits on first query.

## OpenResty/Nginx Issues

**Issue:** Nginx returns 502 Bad Gateway.  
**Possible Causes:**

- Backend (Node) is not reachable or crashed (address issue as above). Check that Node is running and service discovery working.
- Proxy_pass host mismatch: If you see 502 and error log “no resolver defined to resolve cms-node”, in k8s you need a resolver (like kube-dns) or use clusterIP. We used clusterIP service name which should resolve. In container, ensure it has DNS config. If needed, add `resolver 10.0.0.10;` (kube-dns IP) in Nginx config.
- Wrong port: Maybe Node listens on 4000, but config is pointing to wrong port. Confirm Node's port and Nginx upstream.
- Security group firewall: If Nginx is on a different VM from Node and firewall blocks it, 502 results. Make sure connections allowed.

**Issue:** Nginx returns 504 Gateway Timeout.  
**Possible Causes:**

- Node took longer than Nginx’s proxy timeout (60s by default). That means something in Node or DB is extremely slow. Check Node logs for queries stuck. Perhaps a DB query hung (maybe a deadlock or waiting on a lock). Investigate DB logs. Possibly increase `proxy_read_timeout` in Nginx if needed for long operations, but better to fix the slowness.
- Or Nginx could not connect at all and timed out – similar reasons as 502 but no immediate connection refusal, just hang. Check Node connectivity.

**Issue:** SSL certificate problems (if HTTPS configured).  
**Symptoms:** Browser says certificate invalid, or Nginx fails to start with SSL errors.  
**Solutions:**

- Ensure certificate and key are correctly configured in Nginx and paths are right (permissions too). If using Let’s Encrypt, certificate might need renewal – automate using a tool (certbot or use AWS ACM with LB which is easier).
- If certificate is self-signed or from internal CA, import the CA into client trust or use a real CA.
- If using AWS ACM on NLB, ensure NLB’s listener is configured (with annotation or manually). If ACM, route 443 to Nginx as TCP, then Nginx also expects to do SSL – that double encryption might be wrong. Possibly configure NLB to do TLS pass-through (so Nginx gets the raw TLS). Or simpler: use ACM on NLB to terminate and send plain HTTP to Nginx (but then internal traffic not encrypted – maybe acceptable in VPC). Choose one TLS termination point to avoid confusion.

**Issue:** OpenResty Lua script errors.  
We didn't add complex Lua scripts in our config except caching with default keys. But if we had custom Lua and it errors, Nginx might log “lua entry thread aborted” or similar.

- Check Nginx error logs. It will show the Lua error and stack trace. Fix the Lua code accordingly.
- Common Lua issues: using a global not defined, or attempting to use cosocket in wrong phase, etc. Reference OpenResty docs for allowed operations in each context.

**Issue:** Nginx worker process high CPU usage.  
If our traffic is high, an Nginx worker might go near 100% on a core. If using multi-worker (should match core count), maybe we need more workers or to scale out Nginx. Check that it’s legitimately handling lots of requests. If CPU is high even at modest traffic:

- Possibly a tight loop in a Lua code (less likely unless we coded something).
- TLS handshake overhead if using software crypto – maybe use instances with AES-NI, or offload to ALB which might handle TLS in hardware.
- Microcaching could ironically add overhead if keys are computed in a heavy way or if a large share of requests are uncacheable (so Nginx doing more).
- Typically, solution is to scale horizontally (increase replica count or use more cores).

## MongoDB Issues

**Issue:** MongoDB connection failures (Node throws `MongoNetworkError: connection timed out`).  
**Causes:**

- Security group or network ACL blocking connection. Ensure Node can reach Mongo’s address: from Node container, try `mongosh "mongodb://user:pass@host:port/db"`. If cannot resolve host, DNS issue. If resolved but no connect, port blocked or instance down. Fix SG or ensure instance up.
- MongoDB service down: If self-hosted, check mongod process status. If DocumentDB, check AWS Console for cluster status. Perhaps it rebooted for maintenance? It should be multi-AZ to avoid downtime. If a single instance and it rebooted, Node might throw errors until it’s back. In production, use replica sets to allow failover.
- Credentials wrong: If Node logs authentication errors, maybe the secret for Mongo URI has wrong user/pass. Correct them.
- **Solution**: After addressing cause, Node should reconnect (Mongoose will keep trying unless you disabled). If not, might need to restart Node pods.

**Issue:** MongoDB high CPU or slow queries.  
**Symptoms:** CPU on DB at 100%, slow queries logged, perhaps errors like `MongoError: operation exceeded time limit` if you set a maxTimeMS.  
**Solutions:**

- Profile slow queries: use `db.currentOp()` or slow query logs to find culprit. Add indexes as needed. E.g., if filtering by `authorId` often, ensure an index on that field.
- Scale vertically: add more CPU/IO (move from general purpose to provisioned IOPS or a larger instance class). If using DocumentDB, scale the instance class up.
- Add read replicas to offload reads. You can direct some queries to secondaries in your code (Mongoose has read preference settings). But ensure eventual consistency is acceptable for those queries.
- If locks or write issues, consider sharding if write volume is beyond one primary’s capacity. That's a bigger change though.

**Issue:** MongoDB out of memory or crashes with OOM.  
**Causes:**

- Working set larger than RAM and heavy queries cause it to thrash or OOM. Monitoring will show eviction. Solution: either increase instance memory or add indexes to reduce working set needed, or shard to split data.
- Memory leak in Mongo (rare in modern versions). Upgrading might help if it's a bug.
- Not likely in DocumentDB since it's managed, but if using a small instance with not enough RAM, upgrade instance.

**Issue:** MongoDB replica set issues (if applicable).

- If secondaries lag (replication lag metric high), maybe primary is handling too many writes. Consider scaling or splitting data. Or secondary is underpowered compared to primary. Check network between them as well.
- If failover happened (primary changed), ensure the Node driver handled it (Mongoose usually does automatically by re-selecting the new primary). If Node has errors like “Not primary” then maybe it was connected to an old primary before failover. It should auto-reconnect; if not, maybe the driver version is old – update it.

**Issue:** Data inconsistency or missing data.

- This might be an application logic issue rather than DB engine. But if using eventual consistency reads (reading from secondaries), you might see data not appear immediately after a write. Ensure important reads use primary or use `await replication` logic or tune `writeConcern` and `readConcern`.
- If documents missing fields, maybe a bug in how we save (like new fields not being added because schema not updated). Check Node code.
- If truly inconsistent (like lost writes), check if any writes were not acknowledged (we typically use default writeConcern=1 so should be fine). Also if using sharding (not in our current design), could be a chunk migration delay, etc.

## Redis Issues

**Issue:** Redis connection refused or errors in Node like `RedisError: Ready check failed`.  
**Causes:**

- Redis server is down or not reachable. If down, restart it or failover to replica. If using ElastiCache, perhaps node failed – AWS will spin a new one, but endpoint might change if not using cluster mode (though with cluster mode disabled, the primary endpoint stays same across failover). Ensure using the correct endpoint (ElastiCache has a Primary Endpoint that stays constant).
- Wrong password: If `requirepass` set but Node not using it (we did supply via REDIS_URL with auth in it). Check logs for `NOAUTH Authentication required`. If present, fix the connection string to include password.
- Network block: Similar to Mongo, ensure SG allows Node to Redis. In K8s, if using ElastiCache, likely need a security group rule allowing the EKS nodes to connect (you may need to attach the cluster’s SG or node SG to ElastiCache’s allowed list).
- _Solution:_ Once connectivity is fixed, Node should reconnect automatically (the redis client will keep trying by default, or you can trigger a reconnection by restarting Node).

**Issue:** Redis performance issues or data eviction.  
**Symptoms:** Redis latency grows (should normally be <1ms). Or `INFO` shows many evictions (meaning data being removed due to maxmemory).  
**Solutions:**

- If evictions high, it means your cache is constantly full and pushing out entries. Increase Redis memory (scale up instance) or consider enabling Redis Cluster and partitioning data, or optimize what you cache (maybe you’re caching extremely large objects unnecessarily). Also evaluate eviction policy: `allkeys-lru` (default in ElastiCache for volatile caches) is usually fine.
- If latency is high, check CPU on Redis – if at 80-100%, it might be saturating a single core (Redis mostly single-threaded for commands). If so, scaling out with clustering or using a larger instance with higher clock speed can help. Also check if any commands are slow (like a large `SMEMBERS` on a huge set or something). Use `SLOWLOG` command to find slow commands. Perhaps avoid large multi-key operations or break them up.
- Check network: If Node and Redis are in different AZs, latency is slightly higher. Keep them in same AZ if possible for lower latency (but that trades off resilience, so normally multi-AZ is fine as latency still <1ms region-internal).
- If using Redis for session store, and you have extremely many sessions, consider sliding expiration or segmenting session storage.

**Issue:** Redis data not persisting (if expected to).  
We mainly use Redis as cache, so we don’t mind if it restarts and loses data. But if we used it for something critical (like user sessions not stored elsewhere), an outage could log out users.

- If needed, turn on AOF persistence or RDB snapshots. In ElastiCache, you can enable snapshot to S3 daily. If using replication, ensure automatic failover (Redis Sentinel or cluster mode).
- If you expected persistence but didn’t turn it on, that’s a config oversight – enable RDB snapshotting with a short interval.

## Kubernetes / Deployment Issues

**Issue:** Pod CrashLoopBackOff (for Node or OpenResty).  
**Causes:**

- Misconfiguration causing immediate exit. Check `kubectl logs` for the pod. For Node: maybe cannot connect to DB and code calls process.exit (not recommended) or throws at startup. For OpenResty: maybe the config map didn’t mount or had invalid config causing Nginx to exit (check `kubectl logs` OpenResty or describe pod to see if any error in events). If config is invalid, openresty might log and exit; fix the config and update the ConfigMap then restart. Use `nginx -t` within container via exec to debug.
- Insufficient resources: If liveness probes are failing repeatedly (maybe /healthz not responding because Node takes time to start), Kubernetes might kill pods thinking they’re unhealthy. Adjust readiness/liveness probe settings (initial delays, timeouts). For example, if Node needs 10s to connect to DB on startup, set readiness initialDelaySeconds to a bit more than that.
- If CrashLoopBackOff with code 137, that’s OOM kill. Means container ran out of memory. Increase limits or fix memory leak.
- If code 139 (segfault), likely OpenResty or some native module crashed - very rare, unless faulty module or OS issue.

**Issue:** Unable to pull image on Kubernetes.  
Symptoms: Pod events show `Failed to pull image ...` or `ImagePullBackOff`.  
Solutions:

- Make sure image name/tag is correct and pushed to registry.
- If using a private registry (ECR), ensure proper permissions. EKS nodes in same account can pull from ECR if the instance role has the AmazonEC2ContainerRegistryReadOnly policy (often included by default with EKS node IAM role). If not, add that policy.
- If using Docker Hub and hitting rate limits, consider using a paid plan or mirror images in your own registry.
- Use `kubectl describe pod` to see error detail, e.g., 403 from registry.

**Issue:** DNS resolution in cluster not working (OpenResty can't resolve `cms-node`).  
Add `dnsPolicy: ClusterFirst` in Deployment spec (usually default for pods) and ensure kube-dns or CoreDNS is running. If CoreDNS is crash or misconfigured, fix that (maybe it can't reach upstream due to VPC DNS issues – ensure VPC DHCP Option Set has correct DNS or use coreDNS forwarding to 8.8.8.8 etc.). You can test DNS by exec into a busybox pod and `nslookup cms-node.cms.svc.cluster.local`. If fails, investigate cluster DNS.

**Issue:** AWS Load Balancer not created or not working.

- Check service events: maybe the service of type LoadBalancer stuck in pending. Possibly because of missing AWS permissions. EKS cluster needs an IAM role for the controller to create load balancer. On EKS, if using the AWS Load Balancer Controller (for ALB Ingress), you need to deploy that separately with IAM. But for a classic ELB from service, the CCM (cloud controller manager) does it. If cluster was created with Terraform module, it should have IAM permissions. If not, ensure `controller` IAM entity has `CreateLoadBalancer` perms.
- If LB is created but health checks failing (thus no endpoint), as discussed, ensure health check path/port align. For NLB with TCP, health is just TCP connection by default (so if openresty container listening on 80, it should pass).
- If ALB used via Ingress, check Ingress status for issues (like invalid ingress annotations).

**Issue:** Terraform apply issues (like resource conflicts or permission denied).

- If Terraform tries to create something that already exists (maybe you manually created a SG), either import it into Terraform or remove the manual one.
- If apply fails due to permissions, add needed IAM to the user or role running Terraform (the quickstart policy we referenced allowed EC2\* for simplicit ([Rancher AWS Quick Start Guide | Rancher](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/aws#:~:text=%7B%20%22Version%22%3A%20%222012,%7D%20%5D))】, which covers most).
- State lock issues: if terraform says state locked, perhaps a previous run didn't unlock. Use `terraform force-unlock <lock-id>` carefully if sure no other process running.
- If changes in Terraform plan are unexpected (like it wants to destroy something critical), double-check variables. Perhaps the VPC module changed subnets causing re-create. Manage with caution and maybe adjust config to avoid destroying DB or so. Use `terraform taint` and `import` appropriately if needed.

**Issue:** Rancher related (if using Rancher UI not working).

- If Rancher UI at `//rancher_server_url` not loading, maybe the server container is down (check EC2 where it runs). Use docker logs for rancher.
- If it says "cluster not available" in Rancher, check cluster agents. Possibly the Rancher agent on EKS cannot reach the Rancher server (if server was in private net and you accessed UI via SSH tunnel etc.). Make sure rancher server is accessible to cluster (the quickstart uses `sslip.io` to give a domain).
- Rancher sometimes has to be configured with the correct server URL (did that at start). If it’s wrong, agents fail to connect. Re-run the initial to correct.

## Misc Issues

**Issue:** Outdated Dependencies or Known Vulnerabilities.  
Run `npm audit` and address them. If a vulnerability is in a sub-dependency of Apollo and no fix, consider using `resolutions` or contacting maintainers.
For OS packages (OpenResty’s openssl, etc.), update base image or patch as needed.

**Issue:** Backup/Restore testing fails.  
If you cannot restore a Mongo snapshot properly, ensure the snapshot isn't corrupt and the procedure is correct. Try smaller scale first. Possibly use `mongodump` as alternative to snapshot if snapshot failing.

**Issue:** High latency in specific region (maybe users far from deployment region).  
This is not a "bug" but network distance. Solution: consider multi-region deployment or use CDNs for static. For GraphQL, maybe set up additional read-only replicas in other regions and route read queries there (complex, requires aware).

**Issue:** Running out of file descriptors on Node or Nginx.  
Symptoms: errors about "EMFILE too many open files" in Node or "worker_connections are not enough" in Nginx.  
Solution: Increase ulimit for file descriptors. In Docker, can do via `--ulimit nofile=...` or base image might have high default. For Node, set it high, and ensure Node properly closes connections. If WebSocket or long polling, monitor that. Increase Nginx `worker_connections` in config to say 10240 if expecting lots of connections (and increase OS limit accordingly).

**Issue:** Disk space running out (for DB or logs).

- If Mongo data grows, consider scaling storage (EBS can be increased, DocumentDB auto or manual). Also prune old data if any TTL collections.
- Logs: implement log rotation. In containers, logs go to stdout, and container runtime rotates them by size by default (Docker does, but confirm configuration). Or if using Fluent bit to ingest, it can handle rotation. If logs in CloudWatch, ensure retention so you don't pay indefinite storage.
- For openresty, if not in container, set up `logrotate` for /var/log/nginx.

Each issue above can often be diagnosed by checking relevant logs and metrics:

- Always check Node logs, Nginx logs, Mongo logs in tandem around the timeframe of an incident. Often one of them will show the root cause.
- Use your monitoring dashboards to correlate events (like an increase in 5xx errors with a spike in DB CPU).
- The goal is to fail fast and loudly: configure things to give clear error messages when possible, so troubleshooting is straightforward.

This troubleshooting guide should help resolve the most common issues. In summary, methodically check each layer when a problem arises (client -> Nginx -> Node -> DB/Cache -> infrastructure) to pinpoint where it fails, then apply the specific solution. Document new issues and resolutions as you encounter them to expand the guide.

# Best Practices

To ensure the CMS and its infrastructure remain robust, performant, and maintainable over time, here is a summary of best practices gathered from each section, along with additional recommendations for production environments:

## Code and Architecture Best Practices

- **Modularize the Codebase**: Organize your Node.js project by feature (e.g., separate modules for articles, users, comments). This makes it easier to maintain and test. For GraphQL, use schema stitching or Apollo Federation if the schema becomes very large or you split into microservices.
- **Schema Design**: Design GraphQL schema with client use-cases in mind. Avoid overly deep nesting if not needed. Use connections (with pagination) for lists to prevent huge payloads. Document the schema for front-end devs.
- **Efficient Resolvers**: Always resolve data in as few queries as possible. Use batch loading (DataLoader) to avoid N+1 problems and cache at the resolver level where applicable (like caching lookups of reference data).
- **Validation and Sanitization**: Even though GraphQL type system handles basic type checking, implement additional validation for content (e.g., max length of strings, proper email format for user emails, etc.). Sanitize any content that will be rendered as HTML on the client to avoid XSS. For example, if the CMS stores HTML or Markdown, ensure that dangerous tags are stripped or escaped on output.
- **Error Handling**: Implement a consistent error handling strategy. For GraphQL, define custom error types or use extensions in errors to convey specific issues (like authentication errors vs validation errors). Make sure not to leak internal stack traces or sensitive info to clients. Log detailed errors on the server side, but send user-friendly messages to the client.
- **Testing**: Write unit tests for resolvers and any critical business logic. Also perform integration tests – you can use a tool to send GraphQL queries to a test instance and verify responses. This helps catch regressions. If possible, set up a staging environment that mirrors production for testing changes with realistic data.
- **Documentation**: Keep documentation up-to-date:
  - Inline (using GraphQL schema descriptions for fields, which GraphQL introspection can show).
  - A developer README on how to run the project, how to deploy, etc.
  - Document operational runbooks (how to recover from common issues, how to scale up, how to rotate keys, etc.), which is often invaluable for new team members or during incident response.

## Performance Optimization Best Practices

- **Use Caching Wisely**: We have multiple caches (Redis, OpenResty microcache). Monitor their effectiveness. Tune TTLs such that data is not stale for too long but you still get good hit rates. For example, if content changes infrequently, you could cache for longer (minutes) and bust on changes. If highly dynamic, shorter TTL or rely on per-request caching (DataLoader).
- **Compression**: Enable GZIP compression for responses if not already (GraphQL JSON can be highly compressible). Nginx can compress responses; Apollo Server can also support compression. This saves bandwidth and speeds up client load, at the cost of some CPU (which is usually fine).
- **HTTP/2**: If using HTTPS, ensure HTTP/2 is enabled on the load balancer or Nginx. HTTP/2 multiplexing will improve performance for multiple requests (though GraphQL often reduces need for many requests).
- **Keep-Alive connections**: Nginx by default uses keep-alive to upstream. Ensure it's enabled so that it reuses connections to Node (reduces overhead of TCP handshake frequently). Apollo (via Node http server) should also allow keep-alive. Our `proxy_set_header Connection ""` directive helps with that.
- **Batch Operations**: Consider if you need to allow batch GraphQL queries (sending multiple queries in one request). Apollo supports it, but it can also lead to misuse. If clients are making many separate small queries, maybe they should combine them into one query instead of using batching.
- **CDN for Assets**: Offload media and static content to a CDN. If the CMS allows uploading images or files, store them in S3 and serve via CloudFront. That reduces load on our system and improves global access speed. The GraphQL API could return signed URLs or CDN paths for images rather than the image bytes themselves (unless there's a reason to go through GraphQL).
- **Profiling**: Occasionally profile the Node app to find slow spots. You can use the Chrome DevTools or Node’s built-in profiler. This can identify unexpectedly heavy computations or large memory usage that can be optimized (e.g., using streaming for large data instead of buffering whole thing).

## Deployment and Automation Best Practices

- **Infrastructure as Code**: We used Terraform – continue to manage all infrastructure changes through code and version control. This ensures reproducibility. For example, if adding a new cache node or enabling a new AWS service, do it in Terraform. Use Terraform modules to avoid repetition (we used official VPC/EKS modules). Maintain the state file securely (in S3 with encryption and locking).
- **CI/CD Pipeline**: Set up a CI/CD pipeline:
  - CI: run tests and lint on each commit. Perhaps use something like ESLint for code quality, and Prettier for consistent formatting.
  - CD: automated builds and deployments. For instance, on merging to main branch, have CI build a Docker image, push to registry, then update Kubernetes (via kubectl or by updating a Helm chart or manifest repository). Use progressive delivery if possible (e.g., deploy to staging, run smoke tests, then deploy to production).
  - Implement Canary or Blue-Green deployments for low-risk deploys. Kubernetes and Rancher can handle rolling updates, but if the update is major, you might want to route a small percentage of traffic to new pods first (Kubernetes doesn't do this by default, but you can simulate by splitting service labels or using a service mesh).
- **Configuration Management**: Use consistent configurations across environments with small differences via config files or environment variables. For example, have a `.env` or configmap that sets `NODE_ENV`, database URLs, etc. Use a tool or convention to avoid config drift between dev/staging/prod. Possibly use Terraform to template Kubernetes configmaps/secrets per environment.
- **Backup and Restore Procedures**: As mentioned, have automated backups for DB. Test the restoration process in a non-prod environment regularly (maybe quarterly fire-drills). This ensures backups are valid and that the team is familiar with recovery steps.
- **Scaling Policies**: Use auto-scaling but also set safe limits to avoid runaway scaling (which could cost $$$ or overwhelm DB). For example, HPA min 2, max 10 pods, and cluster autoscaler max 5 nodes, etc., based on what your DB can handle. And have an alert if nearing those max so you can consider scaling the DB or optimizing further.
- **Multi-region DR**: If this CMS is critical, consider a disaster recovery plan. That could involve replicating data to a second region (MongoDB can have cross-region replica, or use backup to restore to another region). And having infrastructure-as-code means you could spin up in another region if the primary one has a prolonged outage. Multi-region active-active is complex but DR active-passive is achievable (with DNS switch or using CloudFront + Lambda@Edge perhaps).
- **Updating Dependencies and Systems**: Regularly update system components:
  - Plan maintenance windows to update MongoDB version (test in staging first).
  - Update Node.js runtime to latest LTS periodically to get performance improvements and security fixes.
  - Update OpenResty/Nginx to get security patches. The same for Docker base images (monitor Docker Hub or use a tool like Dependabot for Dockerfiles to alert on updates).
  - Use rolling updates to deploy these changes with minimal downtime.

## Security Maintenance Best Practices

- **Rotate Secrets**: Change DB passwords, JWT signing keys, etc., at some regular interval (maybe annually or if a developer with knowledge leaves). With minimal downtime – e.g., support multiple JWT keys during rotation, etc.
- **Least Privilege**: Continuously ensure no account or role has more permissions than needed. AWS IAM Access Analyzer can help find broad policies. Kubernetes RBAC – ensure no one has cluster-admin unless necessary, and use namespace-specific roles.
- **Penetration Testing**: Engage security experts to pentest the application periodically. They might find issues our internal testing missed, e.g., a subtle injection or a misconfigured header. Use results to improve.
- **Audit Logs**: Periodically review security logs (like CloudTrail for unusual API calls, or Auth logs for repeated failures).
- **Team Training**: Train developers on secure coding practices (like how to avoid injection even in NoSQL context, importance of not logging sensitive info, etc.). Also train ops on responding to incidents.

## Maintenance and Monitoring Best Practices

- **Instrumentation**: Over time, add more instrumentation to cover new features. If you add a new microservice or cache, integrate it into monitoring and logging from day one.
- **Run Books**: Maintain run books for common tasks (scaling up DB, clearing a cache, reprocessing data, etc.) and make sure on-call people know where to find them. For example, "if cache is corrupted, how to flush Redis safely" documented.
- **On-call and Alert Tuning**: Have a rotation for on-call if 24/7 uptime is needed. Tune alerts so that pages only for actionable items (to avoid alert fatigue). Use different levels (info, warning email vs critical page).
- **Capacity Planning**: At regular intervals (say quarterly), review usage trends and plan capacity. For instance, if traffic grew 50% in last 3 months, can current setup handle another 50%? Identify the next likely bottleneck and address proactively (maybe upgrade DB instance size or add another replica).
- **Cost Optimization**: Continuously monitor AWS costs. As architecture evolves, see if resources are underutilized (e.g., maybe we over-provisioned nodes with too much memory unused). Rightsize instances or scale down pods where possible to save cost. Use AWS Savings Plans for instances that run continuously.
- **Documentation of Architecture**: Keep an updated architecture diagram and description. New team members should be able to quickly grasp how data flows from user -> LB -> OpenResty -> Node -> DB/Cache. This helps in troubleshooting and development.

By adhering to these best practices:

- The system stays **reliable** (through monitoring, auto-healing, backups).
- It remains **secure** (through least privilege, regular updates, and audits).
- Performance stays **optimal** (through caching, profiling, and scaling).
- The development process is **efficient** (CI/CD, IaC, modular code, tests).
- The team can **respond to issues** quickly (troubleshooting guides, runbooks, alerts).

Maintaining an advanced system is an ongoing effort. Regular reviews and updates, as described, will keep the CMS running smoothly and ready to handle future demands. Always strive for automation (so processes are reproducible and not error-prone) and clarity (so anyone can understand the system behavior). With that, our step-by-step guide and best practices come to a close, providing a living reference as the project evolves.
