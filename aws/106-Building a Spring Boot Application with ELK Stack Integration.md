# Building a Spring Boot Application with ELK Stack Integration (Step-by-Step Guide)

This guide will walk you through creating an advanced Spring Boot application and integrating it with the ELK stack (Elasticsearch, Logstash, Kibana) and Filebeat for centralized logging. We will use Docker Compose to orchestrate these services. The guide is organized into clear sections with step-by-step instructions, code snippets, and explanations.

## 1. Introduction to Spring Boot and ELK Stack

**Spring Boot and Microservices:** Spring Boot is a Java framework that simplifies building production-ready applications. It favors convention over configuration, allowing developers to create standalone applications with embedded servers and minimal XML. In a **microservices architecture**, an application is divided into multiple small services. Each service runs independently, which offers benefits in agility and scalability. However, debugging can become challenging when an operation spans several services – logs are scattered across different services and machines ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Having%20a%20good%20log%20monitoring,in%20case%20an%20error%20comes)). Having a strategy for centralized logging is crucial in such distributed systems ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=But%20it%20becomes%20very%20complex,centralized%20log%20aggregation%20and%20analysis)).

**The ELK Stack:** ELK is an acronym for **Elasticsearch, Logstash, and Kibana** – a trio of open-source tools used for log aggregation, search, and visualization:

- **Elasticsearch (E):** A distributed, highly scalable search and analytics engine. It stores and indexes log data, making it searchable in near real-time ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=,insights%20from%20your%20application%20data)).
- **Logstash (L):** A flexible server-side data processing pipeline. It can collect logs from various sources (e.g., our Spring Boot services), filter or transform them (e.g., parse timestamps), and send the results to a destination like Elasticsearch ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=It%20acts%20as%20the%20central,insights%20from%20your%20application%20data)).
- **Kibana (K):** A visualization and analytics UI that works on top of Elasticsearch. It allows you to explore the indexed logs, create charts, dashboards, and alerts for monitoring your applications ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=logs%20from%20various%20sources%20,insights%20from%20your%20application%20data)).

In addition to ELK, we will use **Filebeat**, which is part of the Elastic Beats family. **Filebeat** is a lightweight log shipper that monitors log files and forwards the log events to Logstash or Elasticsearch for processing ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=Elasticsearch%3A%20https%3A%2F%2Fwww)). In our setup, Spring Boot will write log messages to a file, Filebeat will tail that file and send the logs to Logstash, and Logstash will parse and forward them to Elasticsearch. Kibana will then visualize those logs.

**Why use ELK with Spring Boot?** Combining Spring Boot with the ELK stack provides a powerful centralized logging solution for microservices. Key advantages include:

- **Centralized Logging:** All logs from different services are aggregated in one place (Elasticsearch), avoiding the need to SSH into individual servers to read log files ([ELK In Spring Boot - Integrate ELK stack into Spring Boot application 2024 - LearnerBits](https://learnerbits.com/elk-in-spring-boot-2024/#:~:text=1,Easy%20integration%20with%20microservices%20architecture)).
- **Powerful Search & Analytics:** Elasticsearch’s querying allows you to quickly find specific log entries and analyze patterns or errors across services ([ELK In Spring Boot - Integrate ELK stack into Spring Boot application 2024 - LearnerBits](https://learnerbits.com/elk-in-spring-boot-2024/#:~:text=1,Easy%20integration%20with%20microservices%20architecture)). You can query logs by fields (timestamp, level, service, etc.) to pinpoint issues.
- **Real-Time Monitoring:** Kibana dashboards enable real-time viewing of system status, error rates, and other metrics derived from logs ([ELK In Spring Boot - Integrate ELK stack into Spring Boot application 2024 - LearnerBits](https://learnerbits.com/elk-in-spring-boot-2024/#:~:text=1,Easy%20integration%20with%20microservices%20architecture)). This helps in identifying problems as they occur.
- **Seamless Microservices Integration:** The ELK stack is designed to work in distributed environments and integrates easily with microservice architectures ([ELK In Spring Boot - Integrate ELK stack into Spring Boot application 2024 - LearnerBits](https://learnerbits.com/elk-in-spring-boot-2024/#:~:text=1,Easy%20integration%20with%20microservices%20architecture)). It provides a unified view of logs across many Spring Boot instances.
- **Improved Troubleshooting:** With centralized and structured logs, you can trace a request across multiple microservices by correlating log entries, significantly reducing debugging time ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Microservices%20architectures%2C%20while%20offering%20agility%2C,Let%E2%80%99s%20briefly%20introduce%20these%20components)) ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=modularity%2C%20can%20introduce%20challenges%20when,Let%E2%80%99s%20briefly%20introduce%20these%20components)).

By the end of this guide, you will have a Spring Boot application emitting logs that are shipped to an ELK stack. You will be able to search and analyze those logs in Kibana, which greatly aids debugging and monitoring in a microservice system.

## 2. Setting Up the Development Environment

Before we start coding, we need to prepare our development environment with all necessary tools:

### 2.1 Install Java and Maven

- **Java Development Kit (JDK):** Ensure you have JDK 11 or above installed (Spring Boot 3.x requires Java 17 or later). You can download an OpenJDK distribution or the official Oracle JDK. Verify the installation by running `java -version` in your terminal, which should display the Java version.
- **Maven:** We will use Maven to manage dependencies and build the Spring Boot application. Install Maven (3.6+). Verify by running `mvn -v`, which should display Maven's version and Java info. If you prefer Gradle, you can use it as well, but this guide will assume Maven for commands.

### 2.2 Set Up an IDE

Choose an IDE or editor that supports Spring Boot:

- **IntelliJ IDEA** (recommended for Spring Boot for its excellent Spring support),
- **Eclipse/STS (Spring Tool Suite)**,
- **Visual Studio Code** with the Java Extension Pack.

Install your preferred IDE and open it. You may also install any Spring Boot plugins if available (for example, Spring Boot Dashboard in VS Code or Spring Assistant in IntelliJ) to simplify running the application.

### 2.3 Install Docker and Docker Compose

We will use Docker to containerize Elasticsearch, Logstash, Kibana, and Filebeat. Install **Docker Desktop** if you're on Windows or Mac, or **Docker Engine** if on Linux. Docker Compose is usually included with Docker Desktop. If not, install it separately following the official docs ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=1,Docker%20Compose%20for%20your%20environment)) ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=If%20you%E2%80%99re%20using%20Docker%20Desktop%2C,Resources)). Ensure Docker is running and test it:

```bash
docker --version
docker-compose --version
```

These commands should output version information. If Docker Compose is not a separate command (Docker Desktop integrates it), you can test by running `docker compose version` (note: newer Docker use `docker compose` without hyphen).

**Allocate adequate resources:** If using Docker Desktop, allocate at least 4GB of RAM in Docker settings for the ELK stack (Elasticsearch can be memory intensive) ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=If%20you%E2%80%99re%20using%20Docker%20Desktop%2C,Resources)).

### 2.4 Database (PostgreSQL/MySQL)

For the database integration part, ensure you have a database server ready:

- **PostgreSQL or MySQL:** Install one of these or use an existing instance. For example, install PostgreSQL and verify that you can connect to it. Alternatively, you can run a database in Docker for testing (e.g., `docker run -p 5432:5432 -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=user -e POSTGRES_DB=mydb -d postgres` to quickly start a Postgres container).
- Note the connection details (hostname, port, database name, username, password) as we will configure Spring Boot to use the database.

### 2.5 Verify Setup

- **Java:** `java -version` (should show e.g. `openjdk version "17.x"`).
- **Maven:** `mvn -v` (should show Maven and Java info).
- **Docker:** `docker run hello-world` (should run a test container successfully).
- **Database:** Connect using a client or CLI (e.g., `psql` for Postgres or `mysql` for MySQL) to confirm it's running.

With the environment ready, we can proceed to create the Spring Boot project.

## 3. Creating a Spring Boot Application

In this section, we'll initialize a new Spring Boot project, implement some basic functionality, connect it to a database, and configure logging. We assume an **advanced developer** audience, so certain basics of Spring Boot will be mentioned briefly. Our example will be a simple **Employee management** service with a REST API and a database.

### 3.1 Setting Up a New Spring Boot Project

**Using Spring Initializr:** The easiest way to start is by using [Spring Initializr](https://start.spring.io/). Spring Initializr allows you to generate a Spring Boot project skeleton with the desired dependencies. Open the Initializr web interface (start.spring.io) in your browser. Enter the project metadata and dependencies:

- **Project:** Maven (or Gradle) Project.
- **Language:** Java.
- **Spring Boot:** (Select the latest stable version).
- **Project Metadata:** Group (e.g., `com.example`), Artifact (e.g., `spring-elk-demo`), Name (`spring-elk-demo`).
- **Packaging:** Jar (default), Java version 17 (or appropriate).
- **Dependencies:** Select **Spring Web** (for REST endpoints), **Spring Data JPA** (for database integration), and the JDBC driver for your database (e.g., **PostgreSQL Driver** or **MySQL Driver**). You can also include **Lombok** for reducing boilerplate, though it's optional.

Click "Generate" to download the project zip. The Spring team suggests using Initializr to bootstrap new projects ([Getting Started | Building an Application with Spring Boot](https://spring.io/guides/gs/spring-boot#:~:text=you%20a%20quick%20taste%20of,project%20as%20a%20zip%20file)). Unzip the project and open it in your IDE. Alternatively, you can create the project directly from your IDE (both IntelliJ and Eclipse have Spring Initializr integration: e.g., **File -> New -> Spring Starter Project**).

**Project Structure:** After generation, you should see a typical Spring Boot structure:

```
spring-elk-demo/
 └── src/main/java/com/example/springelkdemo/
       └── SpringElkDemoApplication.java   (the main class)
 └── src/main/resources/
       ├── application.properties         (configuration file)
       └── ... (other resources)
 └── pom.xml (Maven build file)
```

Ensure the project builds by running Maven compile (`mvn compile`). The `SpringElkDemoApplication` class contains the `main` method with `@SpringBootApplication` annotation – this is the entry point of the Spring Boot app.

### 3.2 Configuring Application Properties

Spring Boot uses `src/main/resources/application.properties` (or `.yml`) for configuration. We will set up properties for database connectivity and logging:

**Database Configuration:** Open `application.properties` and add the following (adapt for MySQL if using that):

```properties
# Database configurations
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=myuser
spring.datasource.password=mypassword
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

Replace the URL, username, and password with your database credentials. In this example, it's pointing to a PostgreSQL database `mydb` on the local machine. The `ddl-auto=update` is convenient for development – it will auto-create database tables based on entities (not recommended for production). `show-sql=true` will log SQL statements (useful to verify queries, can be turned off later).

If using MySQL, your URL would be `jdbc:mysql://localhost:3306/mydb` and you should include the MySQL driver dependency instead of PostgreSQL.

**Logging Configuration (Basic):** By default, Spring Boot logs only to the console with Logback. To integrate with ELK, we want logs to be written to a file (so Filebeat can pick them up) and ideally in a format that’s easy to parse. Spring Boot allows simple logging to a file via properties:

```properties
# Logging to a file (in addition to console)
logging.file.name=logs/springboot/app.log
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss} %-5level [%thread] %logger{36} - %msg%n
```

Here, `logging.file.name` specifies the log file path. We chose `logs/springboot/app.log` (relative to the project directory) – it will create a folder `logs/springboot` and write `app.log` there. The `logging.pattern.file` sets a custom log format pattern for that file: timestamp, log level, thread, logger name, and message. This pattern will produce log lines like:

```
2025-02-19 03:00:00 INFO  [http-nio-8080-exec-1] c.e.springelkdemo.EmployeeService - Employee created successfully
```

The above configuration is a quick way to enable file logging. Under the hood, Spring Boot will configure a rolling file appender with 10MB size by default ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=You%20can%20also%20set%20the,logging.file)).

For advanced logging control, you can use a Logback configuration file. For example, create `src/main/resources/logback-spring.xml` if you need to customize appenders more finely:

```xml
<configuration>
    <!-- File appender with rolling policy -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/springboot/app.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/springboot/app-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory> <!-- keep logs for 30 days -->
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} %-5level [%thread] %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    <root level="INFO">
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

This explicit Logback config ensures logs are written to `app.log` and rotated daily or when they exceed 10MB, with up to 30 days of history. We set root logging level to INFO (so DEBUG logs will not be written by default). You can also keep the console appender if you want logs in both places, but it's optional once file logging is in place.

**(Optional) Switching to Log4j2:** Spring Boot uses Logback by default (through `spring-boot-starter-logging`). If you prefer Log4j2, you would add the dependency `spring-boot-starter-log4j2` and exclude Logback. That is not necessary for this guide, but be aware you have this option. The logging configuration concepts are similar (you'd use a `log4j2.xml` file instead).

### 3.3 Implementing REST Endpoints and Services

Let's create a simple REST API to demonstrate our application. We will model an `Employee` entity and expose endpoints to create and retrieve employees.

**Entity and Repository:** Create a new package `com.example.springelkdemo.model`. In it, create `Employee.java`:

```java
package com.example.springelkdemo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "employees")
public class Employee {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String role;

    // Constructors, getters, setters (or use Lombok @Data for brevity)
    public Employee() {}
    public Employee(String name, String role) {
        this.name = name; this.role = role;
    }
    // ... getters and setters ...
}
```

This is a JPA entity mapped to a table `employees` with fields `id`, `name`, `role`. Next, create a repository interface to perform database operations, in package `com.example.springelkdemo.repository`:

```java
package com.example.springelkdemo.repository;

import com.example.springelkdemo.model.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    // JpaRepository provides basic CRUD operations
}
```

Spring Data JPA will provide the implementation at runtime.

**Service Layer (Optional):** For a simple demo, we might not need a separate service layer, but let's include one to show where to add logging inside business logic. Create `EmployeeService` in `com.example.springelkdemo.service`:

```java
package com.example.springelkdemo.service;

import com.example.springelkdemo.model.Employee;
import com.example.springelkdemo.repository.EmployeeRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EmployeeService {
    private static final Logger logger = LoggerFactory.getLogger(EmployeeService.class);
    private final EmployeeRepository repo;
    public EmployeeService(EmployeeRepository repo) { this.repo = repo; }

    public Employee addEmployee(Employee emp) {
        Employee saved = repo.save(emp);
        logger.info("Added employee with id {}", saved.getId());
        return saved;
    }
    public List<Employee> listEmployees() {
        logger.debug("Fetching all employees from DB");
        return repo.findAll();
    }
}
```

This service uses an SLF4J `Logger` to log important events: we log at INFO level when a new employee is added (including the generated ID) and at DEBUG level when listing all employees. The log messages will go to our configured appenders (console/file). Since the root level is INFO, debug logs won't show unless we raise the logging level for this class/package (we can configure `logging.level.com.example.springelkdemo.service=DEBUG` in properties if needed). Logging inside service methods like this ensures we have traceable events in the logs.

**Controller:** Now create a REST controller in `com.example.springelkdemo.controller` to expose HTTP endpoints:

```java
package com.example.springelkdemo.controller;

import com.example.springelkdemo.model.Employee;
import com.example.springelkdemo.service.EmployeeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employees")
public class EmployeeController {
    private static final Logger logger = LoggerFactory.getLogger(EmployeeController.class);
    private final EmployeeService service;
    public EmployeeController(EmployeeService service) { this.service = service; }

    @PostMapping
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {
        Employee saved = service.addEmployee(employee);
        logger.info("HTTP POST /api/employees - Created Employee {}", saved.getId());
        return ResponseEntity.ok(saved);
    }

    @GetMapping
    public List<Employee> getAllEmployees() {
        logger.info("HTTP GET /api/employees - Fetching all employees");
        return service.listEmployees();
    }
}
```

We have two endpoints:

- `POST /api/employees` to create a new employee (expects JSON body with name and role, and returns the saved employee with ID).
- `GET /api/employees` to list all employees.

We also added logging in the controller: each endpoint logs an INFO message when invoked, including the HTTP method and the resource. This is useful to trace incoming requests in the logs.

**Test the Application:** At this point, run the Spring Boot app (e.g., use your IDE's run or `mvn spring-boot:run`). Ensure your database is running so the application can connect. If everything is set up, the application should start with an INFO log similar to:

```
2025-02-19 03:01:23 INFO  [main] o.s.b.w.embedded.tomcat.TomcatWebServer : Tomcat started on port(s): 8080
2025-02-19 03:01:23 INFO  [main] c.e.springelkdemo.SpringElkDemoApplication : Started SpringElkDemoApplication in X seconds
```

Try calling the endpoints:

- Use a tool like **cURL** or Postman to send a request:
  - `POST http://localhost:8080/api/employees` with JSON body `{"name":"Alice","role":"Developer"}`.
  - `GET http://localhost:8080/api/employees` to fetch the list (should include Alice).
- Check the console or `logs/springboot/app.log`. You should see the log messages from our `EmployeeService` and `EmployeeController`. For example:
  ```
  2025-02-19 03:02:10 INFO  [http-nio-8080-exec-1] c.e.s.controller.EmployeeController - HTTP POST /api/employees - Created Employee 1
  2025-02-19 03:02:10 INFO  [http-nio-8080-exec-1] c.e.s.service.EmployeeService - Added employee with id 1
  ```
  The log file confirms that our logging configuration is working and capturing events.

So far, we've built a Spring Boot service with logging and database integration. Next, we'll set up the ELK stack using Docker Compose and forward these logs for centralized analysis.

## 4. Setting Up the ELK Stack with Docker Compose

Now we will deploy Elasticsearch, Logstash, and Kibana using Docker Compose. We’ll also prepare a configuration for Logstash to handle incoming logs. By the end of this section, you’ll have an ELK stack running locally, though it won’t receive logs until we configure Filebeat in the next section.

### 4.1 Writing the Docker Compose Configuration

Create a new file in your project directory called **`docker-compose.yml`**. This file will define services for **Elasticsearch**, **Logstash**, and **Kibana**. We will add Filebeat later (in section 5).

Start by defining the version and a shared volume for persistent data:

```yaml
version: "3.8" # Compose file format version
volumes:
  esdata: {} # Named volume for Elasticsearch data
```

Now, add the services one by one:

**1. Elasticsearch Service:**

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.10
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - cluster.name=spring-elk-cluster
      - bootstrap.memory_lock=true
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - esdata:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk-net
```

Let’s break down the configuration:

- We use the official Elasticsearch image version 7.17.10. (You can use a newer 8.x version, but 7.x is simpler for now as it doesn’t force security by default.)
- `discovery.type=single-node` configures ES to form a single-node cluster (no need for minimum master nodes).
- `cluster.name` is set to a custom name (optional).
- `bootstrap.memory_lock=true` and `memlock` ulimits disable swapping for ES memory (improves performance).
- `ES_JAVA_OPTS` limits ES JVM heap to 512MB in this example (adjust if you have more memory; by default ES might use 2g which could be heavy on small dev machines).
- We mount a volume `esdata` at `/usr/share/elasticsearch/data` (the path where ES stores indices) so data persists between container restarts.
- Port **9200** is exposed so we can access Elasticsearch’s REST API from our host (e.g., for queries or for Kibana). We map it to the same port on localhost.
- The service is on a custom network `elk-net` (we'll define that network at the end of the file). Using a network ensures all services can communicate by name (e.g., Kibana can reach “elasticsearch” host).

**2. Logstash Service:**

```yaml
logstash:
  image: docker.elastic.co/logstash/logstash:7.17.10
  container_name: logstash
  depends_on:
    - elasticsearch
  volumes:
    - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
  ports:
    - "5044:5044"
    - "9600:9600"
  networks:
    - elk-net
```

Explanation:

- Using official Logstash image (7.17.10 to match Elasticsearch version).
- We set `depends_on: elasticsearch` to start ES first (Logstash might try to connect to ES output on startup depending on config).
- We mount a file `logstash.conf` (which we will create in a moment) into Logstash’s pipeline directory. This config will tell Logstash how to receive logs and where to send them.
- Ports:
  - `5044:5044` is the port where Logstash will listen for Beats (Filebeat) input. We expose it to host as well (though not strictly necessary if Filebeat runs in the same network; but exposing can help if Filebeat was running externally or for debugging). Logstash uses the Beats input plugin on this port.
  - `9600:9600` is an optional port for Logstash’s API (used for monitoring). Not critical, but we expose it in case we want to check Logstash stats.
- Network: on `elk-net` so it can communicate with Elasticsearch (we'll reference ES by hostname in config).

**3. Kibana Service:**

```yaml
kibana:
  image: docker.elastic.co/kibana/kibana:7.17.10
  container_name: kibana
  depends_on:
    - elasticsearch
  environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
  ports:
    - "5601:5601"
  networks:
    - elk-net
```

Details:

- Official Kibana image (same version).
- It depends on Elasticsearch as well.
- We provide an environment variable to point Kibana at Elasticsearch. By default, Kibana tries to reach `http://localhost:9200`, which isn't correct when running in Docker. Setting `ELASTICSEARCH_HOSTS=http://elasticsearch:9200` tells Kibana to connect to the Elasticsearch service we named (Docker’s DNS will resolve "elasticsearch" to the ES container’s IP).
- Port **5601** is exposed so we can access the Kibana web UI from our host browser.
- Network: `elk-net` for internal communication.

Add the network definition at the bottom of the compose file:

```yaml
networks:
  elk-net:
    driver: bridge
```

This defines a custom bridge network `elk-net` which our services join, isolating them from other containers and allowing them to address each other by container name.

Now, **create the Logstash configuration file** referenced in the compose (`./logstash.conf`). This file instructs Logstash how to handle incoming log data from Filebeat:

```conf
input {
    beats {
        port => 5044
    }
}
filter {
    # Grok parse Spring Boot log if needed
    grok {
        match => { "message" => "%{TIMESTAMP_ISO8601:log-timestamp}%{SPACE}%{LOGLEVEL:log-level} %{NUMBER:pid} --- \\[%{DATA:thread}\\] %{DATA:logger} {1,} : %{GREEDYDATA:log-message}" }
        overwrite => [ "message" ]
    }
    # (Optional) Convert timestamp string to actual timestamp
    date {
        match => [ "log-timestamp", "YYYY-MM-dd HH:mm:ss.SSS" ]
        target => "@timestamp"
        remove_field => [ "log-timestamp" ]
    }
}
output {
    elasticsearch {
        hosts => ["http://elasticsearch:9200"]
        index => "myapp-logs-%{+YYYY.MM.dd}"
        # No auth for now since Elasticsearch 7.x by default has no security
    }
    stdout { codec => rubydebug }  # for debugging (prints events to Logstash console)
}
```

Let’s explain this Logstash pipeline:

- **Input:** We use the Beats input plugin on port 5044. This will receive log events from Filebeat (which we'll configure later). We don't need to specify host because it listens on all interfaces by default. Once Filebeat is sending data, Logstash will get those events on this port ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=input%20,)).
- **Filter:** We have a Grok filter that attempts to parse the incoming log line (the `message` field) into structured fields. The grok pattern looks complex – it corresponds to the log pattern we set in Logback:
  - `%{TIMESTAMP_ISO8601:log-timestamp}` extracts the timestamp string.
  - `%{LOGLEVEL:log-level}` extracts the log level (INFO, DEBUG, etc.).
  - `%{NUMBER:pid}` extracts the process ID.
  - The pattern then matches the `---` separator and the thread in square brackets into `thread`, the logger name into `logger`, and finally the actual log message into `log-message`. This Grok pattern is designed for Spring Boot’s default log format ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=grok%20%7B%20match%20%3D,message%7D%22%20%7D%20%7D)).
  - We use `overwrite => [ "message" ]` to replace the original message with the parsed version (not strictly necessary; it's optional).
  - The filter might add tags like `_grokparsefailure` if a log line doesn’t match (e.g., startup logs from Spring Boot that don’t follow the pattern). We can refine the pattern or conditionally apply it, but for now, this should parse our application logs.
- We also included a **date filter**. This takes the `log-timestamp` string (parsed by grok) and tries to convert it to a Logstash `@timestamp`. We specified the format `YYYY-MM-dd HH:mm:ss.SSS` which matches our log pattern. If successful, it sets the event’s `@timestamp` field to the log time (instead of Logstash reception time) and removes the original `log-timestamp` field. This ensures that in Elasticsearch/Kibana the log appears at the correct time. If this fails or is not present, the event’s `@timestamp` will default to when Logstash processed it.
- **Output:** We send events to Elasticsearch running at `elasticsearch:9200` (using the internal network address). We specify an index name pattern `myapp-logs-%{+YYYY.MM.dd}`. This will create a daily index (e.g., "myapp-logs-2025.02.19") for our application logs. This separation by date is a common practice for logging – it makes it easier to manage retention and search by time. In Kibana, we will later use a wildcard index pattern `myapp-logs-*` to catch all daily indices.
  - We are not enabling authentication here (it’s not needed for ES 7.x by default). If you use ES 8.x with security, you’d have to add `user` and `password` in this config.
- We also add a `stdout { codec => rubydebug }` output. This will print processed events to the Logstash container’s console in a Ruby debug format (pretty-printed JSON). This is useful to verify that parsing is working. We can remove or disable it later. To see these logs, you can run `docker-compose logs -f logstash` when everything is up.

Save `logstash.conf`. We now have all parts of the compose and config in place. The directory should have:

- `docker-compose.yml`
- `logstash.conf`
- (Our Spring Boot project files, including the `logs/` directory which will be created when the app runs and writes logs)

Before running, a quick note on **resource limits**: Elasticsearch is memory intensive. If your machine has low memory, consider increasing `ES_JAVA_OPTS=-Xms256m -Xmx256m` (or giving Docker more memory). Also, on Linux, ensure the system’s virtual memory map count is high enough (`vm.max_map_count` kernel setting). Elasticsearch requires `vm.max_map_count` to be at least 262144 ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=The%20,for%20production%20use)). On Linux, you can set this by running:

```bash
sudo sysctl -w vm.max_map_count=262144
```

(This setting persists until reboot, for a permanent change add it to `/etc/sysctl.conf`). On Windows/Mac, Docker usually handles this via the Docker VM. If Elasticsearch fails to start with an error about `vm.max_map_count`, use the above command on your host or Docker's VM.

### 4.2 Running and Troubleshooting the ELK Stack

Now we are ready to start the ELK stack containers:

1. **Start Docker Compose:** In the directory with `docker-compose.yml`, run:

   ```bash
   docker-compose up -d
   ```

   This will pull the Elasticsearch, Logstash, and Kibana images (if not already downloaded) and start the containers in the background (`-d` for detached mode).

2. **Verify Containers are Running:** Execute:

   ```bash
   docker-compose ps
   ```

   You should see `elasticsearch`, `logstash`, and `kibana` listed with their status (`Up`). If any service is not up (e.g., exits with an error), use `docker-compose logs <service>` to inspect its output:

   - `docker-compose logs elasticsearch` – look for any obvious errors. The first startup of Elasticsearch can be slow as it initializes. You should eventually see log lines indicating it started (e.g., "started", "cluster health status").
   - `docker-compose logs kibana` – Kibana also takes a while to start (it will continuously try to connect to Elasticsearch until ES is ready). Wait a minute and check again; look for "Kibana is now available (ready)" message.
   - `docker-compose logs logstash` – Logstash may print some warnings if Elasticsearch isn't up yet (since it tries to connect to output). Eventually, it should say "Successfully started Logstash API endpoint" and wait for input on 5044.

3. **Test Elasticsearch:** You can test if Elasticsearch is responding by running:

   ```bash
   curl http://localhost:9200/
   ```

   This should return a JSON with cluster name and status. For example:

   ```json
   {
     "name" : "elasticsearch",
     "cluster_name" : "spring-elk-cluster",
     "cluster_uuid" : "...",
     "version" : { ... },
     "tagline" : "You Know, for Search"
   }
   ```

   This confirms ES is up (and using our cluster name).

4. **Access Kibana:** Open a web browser and navigate to **[http://localhost:5601](http://localhost:5601)**. This is the Kibana UI. The first load might show a "Kibana is loading" page while it initializes plugins. Once ready, you should see the Kibana interface. Since we are using Elastic 7.x without security, you won't be prompted to log in. (If you used 8.x, the default `elastic` user password or enrollment token would be needed; for simplicity we used 7.x to avoid that in dev mode.)

At this point, the ELK stack is running. However, it isn't receiving any data yet. If you go to Kibana's **Discover** tab now, it will ask you to configure an index pattern – we will do that after we send logs in.

**Troubleshooting startup issues:**

- If Elasticsearch keeps restarting or is unhealthy:
  - Check memory. If it logs `OutOfMemoryError`, allocate more memory or reduce ES heap (`ES_JAVA_OPTS`). Ensure your Docker engine has enough memory.
  - Check `vm.max_map_count` as mentioned earlier if you see related errors. The ES container log would explicitly mention if it's too low.
- If Kibana does not connect:
  - It might be waiting for Elasticsearch. Ensure ES is fully up. The compose `depends_on` ensures start order but not health – sometimes Kibana comes up before ES is completely ready.
  - You can also look at Kibana logs: `docker-compose logs kibana`. If you see messages like "Unable to retrieve version information from Elasticsearch", it's still trying. Give it time. Once ES is up, Kibana should succeed.
- Logstash might output some errors until Filebeat connects (like it may complain about no pipeline data, or show the stdout of events once filebeat is on). For now, it's okay if Logstash appears idle – we haven't fed it logs yet.

We have our Spring Boot app (running on host or IDE) generating logs to `logs/springboot/app.log`, and an ELK stack running in Docker, ready to ingest logs. Next, we will configure Filebeat to bridge the two: reading the log file and sending entries to Logstash.

## 5. Configuring Filebeat for Log Forwarding

**Filebeat** will tail the Spring Boot log file and forward the log lines to our Logstash pipeline. We will run Filebeat as a Docker container (to keep things consistent, though you could run it directly on the host too). In this section, we set up Filebeat with Docker Compose and verify that logs flow from the Spring Boot app to Elasticsearch.

### 5.1 Installing and Setting Up Filebeat in Docker

We will add a Filebeat service to our existing Docker Compose setup. This allows us to manage it along with the other services.

First, create a **Filebeat configuration file** in the project directory named **`filebeat.yml`**. This will instruct Filebeat what to monitor and where to send data:

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/springboot/app.log
    # Optional: combine multi-line stack traces into a single event
    multiline.pattern: '^\s'
    multiline.negate: false
    multiline.match: after

output.logstash:
  hosts: ["logstash:5044"]
```

Let’s break it down:

- We define one input of type "log". This input will read log file lines.
- `paths` specifies which log files to monitor. We use `/var/log/springboot/app.log` as a path inside the Filebeat container. We will ensure this path maps to our host’s log file via a volume.
- We set `enabled: true` (Filebeat by default only runs inputs that are enabled).
- The **multiline** section is optional but recommended for Java stack traces. It says: if a line starts with whitespace (`pattern: '^\s'` meaning a line beginning with a space), it should be appended to the previous line's log event. This way, multi-line exceptions will be sent as one log entry instead of separate lines. We use `match: after` to indicate it's a continuation. This helps because our grok pattern or JSON parsing should treat the entire stack trace as part of the message field.
- The **output** is set to Logstash on host "logstash" port 5044. Since Filebeat will run in the same Docker network (`elk-net`), it can resolve `logstash` to the Logstash container. This configuration means Filebeat will ship all log events to Logstash (which in turn outputs to Elasticsearch) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=filebeat.inputs%3A%20,%2FUsers%2FSmit%2FDownloads%2Fdemo%2Fmyapp.log)).

Now, update **`docker-compose.yml`** to add the Filebeat service. We can place it under the other services:

```yaml
filebeat:
  image: docker.elastic.co/beats/filebeat:7.17.10
  container_name: filebeat
  depends_on:
    - logstash
  volumes:
    - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
    - ./logs/springboot/:/var/log/springboot/
  networks:
    - elk-net
```

Explanation:

- We use the official Filebeat image (version 7.17.10).
- `depends_on: logstash` ensures Filebeat starts after Logstash (so Logstash is ready to receive data).
- We mount our `filebeat.yml` into the container’s Filebeat config path. The official container looks for `/usr/share/filebeat/filebeat.yml` by default.
- We also mount the host directory containing our log file into the container. Our Spring Boot app writes to `./logs/springboot/app.log` on the host (relative to project directory). We mount `./logs/springboot/` to `/var/log/springboot/` inside the container. This way, Filebeat inside the container will find the log at `/var/log/springboot/app.log`, matching the path in its config.
  - **Important:** Ensure the Spring Boot application is writing to the log file before starting Filebeat. If the file or directory doesn’t exist, Filebeat may not find anything. You might want to start the app (if not already running) so that `logs/springboot/app.log` is created. Alternatively, create the folder manually so the mount point exists.
- Filebeat doesn’t need any ports exposed; it will initiate connections to Logstash. It just needs to be on the same network as Logstash (which we set with `elk-net`).

Go ahead and **start Filebeat** by re-running Docker Compose:

```bash
docker-compose up -d filebeat
```

This will start the Filebeat container (our other services are already up). If you use `docker-compose up -d` without specifying, it will ensure any new services (filebeat) are started as well.

### 5.2 Defining Filebeat Input and Output & Testing Log Forwarding

We already defined the Filebeat input (the log file) and output (Logstash) in `filebeat.yml`. Let’s verify that everything is connected:

**Check Filebeat logs:** Run:

```bash
docker-compose logs -f filebeat
```

You should see Filebeat’s startup logs. It will log which files it is monitoring. Look for lines like:

```
filebeat    | INFO  log/input.go:157  Configured paths: [/var/log/springboot/app.log]
filebeat    | INFO  [monitoring]...
filebeat    | INFO  Harvester started for file: /var/log/springboot/app.log
```

This indicates Filebeat found our log file and started a harvester on it. If the Spring Boot app is running and writing to the file, Filebeat should almost immediately pick up any new lines.

If the log file already had content, Filebeat will attempt to send it. By default, Filebeat might start at the end of the file (to only send new logs) unless configured otherwise. It keeps track of the file offset in a registry.

**Generate some logs:** If your Spring Boot application wasn’t running, start it now. Trigger a couple of actions:

- Hit the `GET /api/employees` endpoint (which will log a fetch).
- Perhaps create a new employee with the POST endpoint (logs creation).

Each action generates log lines in `app.log`. Filebeat should detect these new lines and forward them.

**Observe Logstash and Elasticsearch:** While filebeat is running:

- Run `docker-compose logs -f logstash` in another terminal. You should see Logstash outputting the events (because we included the stdout output in Logstash config). For example, Logstash might print a Rubydebug dump for each event:
  ```json
  {
      "@timestamp" => "2025-02-19T09:10:12.345Z",
      "log-level" => "INFO",
      "logger" => "c.e.s.controller.EmployeeController",
      "log-message" => "HTTP GET /api/employees - Fetching all employees",
      "thread" => "http-nio-8080-exec-1",
      "pid" => "12345",
      ...
      "tags" => []
  }
  ```
  This indicates Logstash received the log line and parsed it: we see separate fields for level, logger, thread, etc. The `@timestamp` has been set (if the date filter worked, it uses the original timestamp).
  If you see `_grokparsefailure` in tags or unparsed messages, it means the pattern didn't match perfectly (maybe due to a slight format difference). Adjust the pattern if needed. But if your pattern aligns with your log format, you should see named fields as above.
- Check **Elasticsearch indices:** Run:
  ```bash
  curl -X GET "http://localhost:9200/_cat/indices?v"
  ```
  This will list all indices in ES. Look for an index named **`myapp-logs-*`** (with today’s date). If you see one and a document count, that means logs are indexed. For example:
  ```
  health index             pri rep docs.count ...
  green  myapp-logs-2025.02.19 1   0         2 ...
  ```
  This shows two documents (which likely correspond to two log events we generated).

If you prefer, you can also query Elasticsearch directly for log entries:

```bash
curl -XGET "http://localhost:9200/myapp-logs-*/_search?q=log-level:INFO&pretty"
```

This will search for logs with level INFO. The response will include the documents with all fields.

At this point, the pipeline is functional:

- Spring Boot writes log to file.
- Filebeat tails the file and ships logs to Logstash ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=Lets%20configure%20the%20filebeat%20to,read%20the%20logs%20file)) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=output.logstash%3A%20hosts%3A%20%5B)).
- Logstash parses and indexes into Elasticsearch ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=output%20,YYYY.MM.dd%7D%22)).
- Elasticsearch stores the log events in an index.
- We are ready to use Kibana to visualize these logs.

**Troubleshooting Filebeat & Log Forwarding:**

- If Filebeat logs show errors connecting to Logstash (e.g., connection refused):
  - Ensure the network is correct. The Filebeat container should resolve `logstash` to the Logstash container’s IP. All services were put on `elk-net`. If you accidentally ran Filebeat outside compose or on host, it wouldn't know the name. Running via compose as configured should be fine.
  - Also confirm Logstash container is indeed listening on 5044. Logstash logs should show it started the beats input on 5044.
- If Filebeat cannot open the log file:
  - Make sure the path is correct and the file exists. The `volumes` mapping must be correct. On Unix-like OS, file permissions might matter (Filebeat runs as `root` in the container by default, so it should have access).
  - If the Spring Boot app runs as a non-root user and created the file, that’s okay; the container’s root should still read it unless file permissions are restrictive. Typically, open permissions or same user mapping could be needed, but usually reading is not an issue.
- If logs are not appearing in ES:
  - Check Filebeat logs for any parsing errors.
  - Check Logstash logs for errors. Sometimes if the grok fails, Logstash might still send the event with tags `_grokparsefailure`. Those events still get indexed (unless we drop them explicitly).
  - Ensure Elasticsearch is not rejecting requests. For instance, if the index template is not configured and you have data type issues (unlikely in our basic scenario).
- If you suspect Filebeat->Logstash pipeline, you can test by sending a dummy log line. For example, stop Filebeat and try manually:
  ```bash
  echo "Test log line" | nc localhost 5044
  ```
  This might not be straightforward due to the Lumberjack protocol Beats uses (so this netcat trick might not show up properly, since it's not plain TCP text). A better approach is to add a temporary input to Logstash to listen on TCP or to output Filebeat directly to Elasticsearch for narrowing down. But if all components are up, usually the pipeline works.

We now have confirmed that logs from our Spring Boot app make it to Elasticsearch. The next step is to use Kibana to search and visualize these logs.

## 6. Integrating Spring Boot Logging with ELK

In the previous sections, we set up the flow of logs. Now, we will discuss refining the integration: structured logging formats and log levels.

### 6.1 Structured Logging (JSON Logs)

To make logs more easily parseable, it's a common best practice to log in a **structured** format like JSON. Currently, we used a custom pattern and Grok in Logstash to parse. While this works, it requires maintaining the grok pattern. Alternatively, we could have the application output JSON logs directly, so Logstash (or even Filebeat/Elasticsearch ingest) can parse them without complex grok.

**Why JSON logs?** Standard text logs are human-readable but hard for log aggregators to parse consistently, especially if formats change ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=Standard)). JSON is machine-readable – each log field can be a JSON field. Logging in JSON ensures that metadata (timestamp, level, etc.) are already structured. This can simplify our pipeline because Filebeat or Elasticsearch can directly understand the log structure.

Spring Boot (Logback) can be configured to log in JSON with the help of the **Logstash Logback Encoder** library. This third-party library provides encoders to output Logback events as JSON. To use it:

- Add the dependency to Maven:

  ```xml
  <dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.3</version>  <!-- ensure compatibility with Logback version -->
  </dependency>
  ```

  (The version 7.3 works with Logback 1.2; if using Spring Boot 3.x/Logback 1.3, version 7.4+ might be needed – see library docs ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%3Cdependency%3E%20%3CgroupId%3Enet.logstash.logback%3C%2FgroupId%3E%20%3CartifactId%3Elogstash)).)

- Update `logback-spring.xml` to use a JSON encoder. For example:

  ```xml
  <configuration>
    <appender name="FILE_JSON" class="ch.qos.logback.core.rolling.RollingFileAppender">
      <file>logs/springboot/app.json</file>
      <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
          <fileNamePattern>logs/springboot/app-%d{yyyy-MM-dd}.%i.json</fileNamePattern>
          <maxFileSize>10MB</maxFileSize>
          <maxHistory>30</maxHistory>
      </rollingPolicy>
      <encoder class="net.logstash.logback.encoder.LogstashEncoder">
          <!-- Optionally, you can configure the encoder for including MDC or custom fields -->
      </encoder>
    </appender>
    <root level="INFO">
      <appender-ref ref="FILE_JSON"/>
    </root>
  </configuration>
  ```

  Here we changed the appender to use `LogstashEncoder`, which by default will output each log event as a JSON object (one per line). A log entry might look like:

  ```json
  {
    "@timestamp": "2025-02-19T09:15:00.123Z",
    "@version": 1,
    "message": "HTTP GET /api/employees - Fetching all employees",
    "logger_name": "com.example.springelkdemo.controller.EmployeeController",
    "thread_name": "http-nio-8080-exec-1",
    "level": "INFO",
    "level_value": 20000
  }
  ```

  Each field is clearly delineated (timestamp, message, logger_name, etc.). You can add more context (for instance, include MDC data like request IDs, which we’ll discuss in best practices).

- With JSON logging in place, we would adjust Filebeat/Logstash:
  - We could remove the grok filter in Logstash entirely. Instead, use a **JSON filter** or have Filebeat decode JSON. For example, Filebeat has `decode_json_fields` processor or you can set `output.elasticsearch` with ingest pipeline. If we stick to Logstash, we can do:
    ```conf
    input { beats { port => 5044 codec => json } }
    ```
    This tells Logstash to treat incoming data as JSON (so it will automatically parse the JSON string into fields). Or use a filter:
    ```conf
    filter {
      json { source => "message" }
    }
    ```
    which will parse the JSON in the "message" field to structured fields.
  - The advantage is that all those fields (level, logger_name, etc.) appear in Elasticsearch without writing a custom grok. We just need to ensure the JSON format from Logback matches what Logstash expects (LogstashEncoder is designed to be compatible).
  - The index mapping would accommodate these fields automatically (Elasticsearch will infer types on first index). Optionally, we might adjust our index or use an index template to define data types (like `@timestamp` as date, etc.). Since the JSON has `@timestamp` and `level` as text, etc., it should be fine.

**Note:** If you have structured logging, you might directly send logs from Filebeat to Elasticsearch (bypassing Logstash) because you no longer need heavy parsing. You can use Elasticsearch Ingest Node pipelines to do minor processing if needed. We included Logstash in this guide to demonstrate parsing and as it’s commonly used for more complex transformations.

### 6.2 Customizing Logging Levels and Formats

Regardless of format (plain or JSON), it’s important to manage **log levels**:

- During development or troubleshooting, you might set more verbose logging (DEBUG) for certain packages. In production, you typically use INFO or WARN as the default to avoid overhead.
- You can configure log levels in Spring Boot via properties. For example, to enable debug for our service layer, add:
  ```properties
  logging.level.com.example.springelkdemo.service=DEBUG
  ```
  This will make EmployeeService log debug messages (as we coded one in `listEmployees`). Spring Boot supports fine-grained control using `logging.level.<package>=LEVEL` ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=If%20the%20only%20change%20you,shown%20in%20the%20following%20example)).
- You can also change logging levels at runtime if you include the Spring Boot Actuator and use the `/actuator/loggers` endpoint, but that’s beyond our scope.

**Log Format Customization:** If not using JSON, ensure your pattern includes all the information you need (timestamps, thread, etc.). We did that. If you want to include things like an application ID or environment, you might hardcode or use logging context.

- You could use MDC (Mapped Diagnostic Context) to add contextual info (e.g., a request ID or user ID). For example, in a filter or aspect, you populate `MDC.put("requestId", someId)` at the start of a request. Then in your log pattern or JSON encoder, include `%X{requestId}` to append the MDC value. This is useful for tracing logs per request.
- In JSON logging, the logstash encoder can automatically include MDC entries as fields if configured.

**Summary:** At this point, we have an operational logging pipeline. We have highlighted that structured logging (JSON) can simplify the integration by eliminating the need for Logstash filters. Many advanced Spring Boot projects adopt JSON logging from the start for this reason ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=are%20easy%20to%20read%20by,the%20log%20format%20keeps%20changing)). Even without JSON, our current text pattern and grok accomplish the goal.

Our Spring Boot application’s logs are now flowing to ELK. We can adjust the verbosity via configuration as needed and ensure that critical information is logged. Next, we will use Kibana to visualize and analyze these logs.

## 7. Visualizing Logs in Kibana

Kibana is the UI for querying and visualizing our logs. In this section, we'll configure Kibana to recognize the logs index, and then demonstrate basic visualization creation and log analysis.

### 7.1 Setting Up Index Patterns in Kibana

When you first access Kibana (http://localhost:5601), you need to define an **Index Pattern** (in Kibana 7.x, sometimes called "Data View" in newer versions) to tell Kibana which Elasticsearch indices to explore.

**Create an Index Pattern:**

1. In Kibana’s left sidebar, go to **Stack Management** (the gear icon).
2. Under “Kibana”, click **Index Patterns** (or "Data Views"). Then click the **Create index pattern** button ([Create an index pattern | Kibana Guide [7.17] - Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=Open%20the%20main%20menu%2C%20then,and%20Kibana%20looks%20for)).
3. For the index pattern name, enter `myapp-logs-*`. This pattern will match all indices that start with `myapp-logs-` (like `myapp-logs-2025.02.19` and future ones). You should see it recognize the index we created (it might show a preview or count of matches).
4. Choose the Time Field: select `@timestamp` from the dropdown. This field will be used for time-based filtering (most log indices have a `@timestamp` field which we populated via Logstash). If `@timestamp` is not present, you could use the log-timestamp string or ingestion time, but since we configured Logstash to set `@timestamp`, use that.
5. Click **Create index pattern** to save.

Now Kibana knows about our log index. We can start exploring the data.

### 7.2 Discovering Logs

Navigate to **Discover** in Kibana (menu on left, compass icon). On the top left, ensure your new index pattern (`myapp-logs-*`) is selected as the data source.

You should see logs appearing in the table view (if the time range is correct). By default, Kibana shows the last 15 minutes. Ensure that the log entries you generated fall within the time filter (adjust the time picker in the top right, e.g., to "Last 1 hour" or a custom range including the current date/time). If all is set, you should see entries listed, with columns like **@timestamp** and **message**, etc.

Each log event will show its message and a few fields. You can expand an entry to see all fields:

- For example, our log from `EmployeeController` might show fields: `log-level: INFO`, `logger: com.example...EmployeeController`, `log-message: HTTP GET /api/employees - Fetching all employees`, `thread: http-nio-8080-exec-1`, etc., as well as `@timestamp` and possibly `pid`, `tags` (if any) and so on. If you used JSON logging, you'd see those JSON fields accordingly (level, logger_name, etc.).

**Filtering and Searching Logs:**

- Kibana’s search bar allows Lucene or KQL (Kibana Query Language) queries. For example, to filter only ERROR logs, you can type `log-level: "ERROR"` (assuming our grok field is `log-level`). If using JSON logging, the field might be `level` or similar.
- You can also add filters using the UI: click **Add filter**, choose field (e.g., log-level), operator (is), value (ERROR). This filters the view to just error logs.
- Try searching for text: e.g., type `Alice` in the search bar to find logs containing the word "Alice" (if one of our log messages or fields had that).
- You can also filter by time by adjusting the time picker.

### 7.3 Creating Dashboards and Visualizations

One of Kibana’s strengths is creating visualizations from log data. We can build charts to monitor our application. Let’s create a couple of examples:

**Example 1: Log Level Distribution Pie Chart** – A pie chart showing the proportion of INFO, WARN, ERROR logs.

1. Go to **Visualize Library** (or **Create Visualization**).
2. Choose a Pie Chart (in older Kibana, you might pick Aggregation-based Pie).
3. Select the `myapp-logs-*` index pattern for the data source.
4. For the aggregation:
   - **Bucket**: select a Terms aggregation on the field `log-level` (or `level` depending on how it's stored).
   - Set the size to, say, 5 (to show top 5 terms, basically INFO, DEBUG, WARN, ERROR etc., though we only expect a few).
5. The chart preview will show slices for each log level present in the data and their counts.
6. You can customize labels (e.g., show counts or percentages).
7. Save the visualization as "Log Level Distribution".

**Example 2: Logs Over Time Line Chart** – A line chart to see how many log events occur over time (could be useful to spot spikes).

1. Create a new visualization (Line chart).
2. Data source: `myapp-logs-*`.
3. X-Axis: Date Histogram on `@timestamp` (interval can be auto or set a fixed interval depending on time range).
4. Y-Axis: Count (the count of log events per time bucket).
5. This will show a time series of log counts. If you only have a handful of logs, it might look sparse. But imagine in a real system, you’d see peaks during high usage or error spikes.
6. Save as "Log Volume Over Time".

**Example 3: Top Endpoints or Top Users** – If we logged info about endpoints or user IDs in logs, we could do a terms aggregation on those. In our simple app, we might not have rich data to do that. But as an idea: if each log had a field `endpoint` or `userId`, we could visualize which endpoints are called most or which users see errors, etc.

**Dashboards:** Kibana allows you to combine visualizations into a dashboard:

- Go to **Dashboard**, create a new dashboard.
- Click **Add Panels** and select the visualizations you created (the pie chart and line chart, etc.).
- Arrange them on the grid.
- Save the dashboard as "Spring Boot Logs Dashboard".

You now have a live dashboard. You can set auto-refresh (e.g., refresh every 10 seconds) for real-time monitoring. If you generate more logs (e.g., hit the API endpoints more), you’ll see the charts update (after refresh).

### 7.4 Analyzing Logs

Beyond visualizations, Kibana’s **Discover** tab is your friend for ad-hoc analysis:

- For instance, if an error occurred, you can search for `"ERROR"` and perhaps a keyword in the error message. Kibana will show you matching log entries. Because we centralized logs, you might have multiple services; in such a case, you could also filter by service name if you include that in logs or index naming.
- You can click on field values to filter. E.g., in Discover, if you see `log-level: ERROR` in a log entry, clicking it gives option to filter for only ERROR or exclude ERROR. This interactive filtering helps drill down.
- Use Kibana’s **Dev Tools -> Console** if you want to run more complex ES queries or aggregations directly. For example, you could run a query to find how many errors occurred in the last 24 hours by a certain component.

By leveraging Kibana, you have transformed raw logs into insights. Developers and DevOps teams can quickly pinpoint issues (e.g., see an unusual spike of ERROR logs on the timeline, click it to zoom in, filter by error type, and then find the cause).

**Tip:** You can also set up Kibana **Alerts** (under Observability/Alerts) to send notifications (email, Slack, etc.) when certain log conditions occur (like if ERROR logs increase beyond a threshold). This is an advanced use-case but extremely useful in production monitoring.

We have now covered how to explore and visualize logs. The next section discusses advanced configurations, including securing our ELK stack and scaling it for production use.

## 8. Advanced Configurations and Performance Tuning

As you move from a development setup to production, there are several considerations for hardening and scaling the ELK stack, as well as optimizing performance.

### 8.1 Security for Elasticsearch and Kibana

In our dev setup, we left Elasticsearch and Kibana with default (no authentication, no TLS). In production, **security is essential**:

- **Enable Authentication:** Elastic Stack 8.x has security (basic auth) on by default. For 7.x (which we used), you should enable X-Pack security. This involves setting up passwords for the built-in users. Typically:
  - Set `xpack.security.enabled=true` in Elasticsearch config (or env var) and configure accounts. You can bootstrap an `elastic` superuser password either via CLI or env (`ELASTIC_PASSWORD`) ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=4.%20In%20the%20,variables)).
  - In Docker Compose, for ES 8+, you might do:
    ```yaml
    environment:
      - xpack.security.enabled=true
      - xpack.security.authc.api_key.enabled=true
      - ELASTIC_PASSWORD=StrongPassword123
    ```
    This sets the password for the `elastic` user on startup.
  - For Kibana, you then set:
    ```yaml
    environment:
      - ELASTICSEARCH_HOSTS=["http://elasticsearch:9200"]
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=StrongPassword123
    ```
    So Kibana can authenticate to ES.
  - After this, you access Kibana via http://localhost:5601 and log in with username `elastic` and the password you set.
- **TLS/Encryption:** Consider enabling TLS encryption especially if data travels over untrusted networks. Elasticsearch can be configured with SSL certificates for HTTP and transport layer, and Kibana with its own cert or connecting via HTTPS to ES. Elastic provides documentation on enabling TLS. For development, you might skip it, but for production it's recommended to encrypt traffic and not send logs in plain text (especially if logs contain sensitive info).
- **Firewall and Access Control:** If running on servers, ensure that Elasticsearch (9200) is not open to the world. It should be accessible only by authorized services (Kibana, your applications if they query it, etc.). Kibana (5601) might be user-facing for your team; secure it behind authentication and perhaps IP whitelisting or VPN.
- **Logstash Security:** If using Logstash, you can enable TLS on the beats input and have Filebeat send securely. Also, if ES requires auth, you put credentials in Logstash’s elasticsearch output config (or use API keys).

In short, lock down the stack before exposing it. Default credentials or open access can lead to breaches (Elasticsearch databases have been targets when left open).

### 8.2 Scaling the ELK Stack (Clustering and High Availability)

Our Compose setup runs single instances of each component. In production, depending on volume and availability requirements:

- **Elasticsearch Cluster:** Run multiple Elasticsearch nodes (to handle more data and provide high availability). Typically, you’d run at least a 3-node cluster for production (so that if one node goes down, the cluster can still function). Each node can be on separate servers. You might have dedicated master nodes, data nodes, etc., but for moderate logging needs, 3 nodes doing both roles could suffice. Docker Compose can spin up multiple ES instances (with different names/ports) or more commonly you’d deploy ES on VMs or Kubernetes. Elastic provides Orchestration (ECK – Elastic Cloud on Kubernetes) to manage clusters easily ([Elastic Stack Monitoring with Elastic Cloud on Kubernetes](https://www.elastic.co/pt/blog/elastic-stack-monitoring-with-elastic-cloud-on-kubernetes#:~:text=Elastic%20Stack%20Monitoring%20with%20Elastic,manage%20Elastic%20Stack%20Monitoring)).
- **Kibana:** Usually one instance is fine (it doesn’t store data, it’s stateless). But you can run multiple Kibana instances behind a load balancer if needed for concurrent users or HA. Each Kibana connects to the same ES cluster. They all share the state stored in ES (saved dashboards, etc.).
- **Logstash and Beats:** To handle high log volumes, you can scale horizontally:

  - **Logstash:** You can run multiple Logstash instances in parallel, but you need to distribute the load. One way is to use a message queue like **Kafka** or RabbitMQ: have Filebeat send to a Kafka topic, and have multiple Logstash consumers read from that topic. This decouples ingestion rate and processing. Our example in section 4 had a note about Kafka (though we didn’t implement it) ([

    Setting Up Elastic-based logging stack with Docker Compose · All things
    ](https://dzlab.github.io/monitoring/2024/05/21/elk-docker-compose/#:~:text=The%20filebeat%20service%20will%20consume,be%20then%20queried%20with%20Kibana)). Kafka can buffer billions of messages, acting as a safety net if ES is slow.

  - Alternatively, Filebeat can directly load-balance to multiple Logstash instances if you list multiple hosts in `output.logstash`.
  - **Filebeat:** If you have many servers producing logs, you typically run one Filebeat per server (as an agent). In containerized environments (like Kubernetes), you might run Filebeat as a DaemonSet on each node to collect container logs. Each Filebeat would send to Logstash or ES.

- **Docker Swarm/Kubernetes:** For deploying a scaled ELK stack, using an orchestrator is ideal:
  - In Docker Swarm, you could define services in a stack file and scale them (e.g., `docker service scale logstash=3`). Ensure to handle coordination (like use a queue for logstash as mentioned).
  - In Kubernetes, you might deploy Elasticsearch using the official Elastic Cloud on K8s (ECK) operator, which can manage cluster nodes, upgrades, etc., or use Helm charts. Similarly, deploy Kibana and Logstash pods. Kubernetes logging often uses the EFK stack (Elasticsearch, Fluentd, Kibana) as fluentd can be used instead of Logstash. However, Logstash can also run on K8s.
  - Also consider using **Elastic Cloud** (hosted service) to avoid managing the cluster yourself. You can ship logs from Filebeat to Elastic Cloud (which runs ES and Kibana for you).

**Scaling considerations:**

- As log volume grows, monitor Elasticsearch performance. You may need to increase resources (CPU, RAM, SSDs). Also consider using **Index Lifecycle Management (ILM)** to rollover and delete old indices automatically to manage disk usage.
- Logstash can be memory heavy if not tuned. For high volumes, sometimes using Beats + Elasticsearch ingest pipelines is more lightweight (you cut out Logstash). For example, Filebeat can send JSON logs directly to an Elasticsearch ingest pipeline that applies grok or other processors.

### 8.3 Performance Optimization Techniques

Here are some tips to optimize performance of the logging pipeline:

- **Optimize Log Generation:** In your Spring Boot app, avoid excessively verbose logging in hot paths. For instance, don’t log inside a tight loop or for every array element in a batch. Use appropriate log levels (DEBUG for diagnostic info that can be turned off in production). Also consider asynchronous logging so that the log writing doesn’t slow down your application threads. Logback can be made asynchronous by using `AsyncAppender`, which buffers logs and processes them in a separate thread.
- **Batching and Buffering:** Elasticsearch and Logstash both work more efficiently when ingesting logs in bulk. Filebeat already batches events and Logstash outputs in bulk to ES. Ensure those batch sizes are tuned if needed (Filebeat `bulk_max_size`, Logstash `flush_size`, etc., typically the defaults are fine).
- **Index Management:** Each day (or each index) consider how many shards you really need. By default, an index might have 1 shard, 1 replica (replica provides redundancy). If you have a single node, replicas are unused (can't be assigned). If you have a cluster, set replicas to at least 1 for fault tolerance. Too many shards can hurt performance. For logging, one shard per index is often okay if daily indices, unless volume is huge.
- **Mapping and Templates:** If you know the structure of your logs (especially with JSON logging), define an index template so that fields are mapped to proper types (date, keyword, text). This avoids mapping explosions or inefficient text analysis on fields that don't need it. For example, log level could be a keyword (exact value match), logger name maybe a keyword, message could be text (full-text searchable). Kibana's Index Pattern will show which fields are searchable and aggregatable based on mapping.
- **Resource Allocation:** Give Elasticsearch enough memory (heap ~ half of system RAM, but do not exceed ~32GB heap due to JVM pointer compression). Monitor ES’s JVM garbage collection (via Kibana monitoring or logs). For Logstash, if it’s a bottleneck, increase pipeline workers or batch size. Filebeat is lightweight but if reading many files, adjust its `spool_size` (batch of lines to send) and perhaps memory queue.
- **Avoiding Disk Bottlenecks:** Logs can be heavy on I/O. Use fast disks (NVMe SSDs) for Elasticsearch data. If running in Docker, ensure the volume for ES data is on a fast drive (and not the default slower storage). Also, if using the default JSON logging for Docker (we aren’t, but if you were capturing container stdout), the docker daemon writes logs to json files which could also become a bottleneck. Our approach avoids that by writing directly to a file and Filebeat reading it.
- **Retention and Archiving:** Don’t keep unlimited logs in Elasticsearch. This will grow your cluster endlessly. Implement a strategy to delete or archive old logs (ILM can move indices to cheaper storage and then delete after X days). This ensures ES remains performant with a manageable amount of data.

### 8.4 Debugging and Troubleshooting Common Issues

Even with tuning, issues can arise. Here are some common problems and how to address them:

- **Elasticsearch fails to start (Exit Code 78)**: This often is the `vm.max_map_count` issue. Solution: set the kernel setting as described earlier ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=The%20,for%20production%20use)) and restart ES.
- **Elasticsearch cluster red/orange status**: Could be due to missing replicas (if you only have one node and have replica=1, the replica can’t be assigned, status yellow – which is okay for one node). Red means a primary shard is unassigned (maybe ES crashed mid-write). Check Kibana Stack Management -> Index Management for details. Possibly force allocate or reindex if needed. Ensuring a stable cluster with at least one replica avoids data loss.
- **Logstash memory leak or high CPU**: If Logstash is overwhelmed, you might see it lag behind (Filebeat may show backpressure, slowing down reading). Check Logstash logs for backpressure signals. Solutions: increase JVM heap for Logstash, or scale out Logstash instances and load balance inputs.
- **Filebeat not harvesting files**: If new files aren’t picked up, check that the path patterns in filebeat.yml match exactly. Filebeat uses a registry to remember the last read position. If you delete a log file and recreate it, Filebeat might treat it as same file by inode and not re-read unless the inode changed. You can clear the registry (usually at `/usr/share/filebeat/data/registry` in the container) when testing, or set `logging.file.rotateOnStartup=true` in dev to create new files.
- **Logs not appearing in Kibana**: If you know logs should be there (Filebeat logs show sent X events), check:
  - Index pattern is correct and time range is correct.
  - Perhaps the logs went to a different index name than expected. Maybe your Logstash index pattern or date format had an error. Use the `_cat/indices` check to see if a new index got created with a slightly different name (like `myapp-logs-2025.19.02` if date format was wrong).
  - If using security, ensure Kibana user has access to that index (the `elastic` superuser will, but if using a restricted user, set roles properly).
- **Grok parse failures**: If in Kibana you see the raw message or a tag `_grokparsefailure` on events, then some logs didn't match. Possibly our pattern doesn't cover a certain log format (like a stack trace line or a startup log line). You can refine the Logstash pipeline:
  - Use conditional logic, e.g., `if "Started SpringElkDemoApplication" in [message] { drop { } }` to drop the irrelevant startup log or parse it differently.
  - Adjust the grok pattern to be more lenient or add patterns for multiline. Alternatively, since we have multiline handled in Filebeat for exceptions, ensure that is working (if not, exceptions might come as separate lines that grok can't parse).
- **Time zone issues**: If you notice logs times are off by a few hours in Kibana, it could be time zone. Our date filter didn't specify a timezone, so it assumed the timestamp was local or UTC? `TIMESTAMP_ISO8601` without TZ might parse as local time. Kibana by default shows times in your browser's local timezone.
  - Check if the `@timestamp` in JSON (when expanded) matches your actual event time. If it’s off, you might need to adjust the date filter to specify timezone or ensure your application logs in UTC. A quick fix: you can configure Logback to output timestamps in UTC by using `%d{yyyy-MM-dd'T'HH:mm:ss.SSSZZ}` or similar, which includes timezone.
- **Kibana performance**: If you have millions of logs, the Discover view might be slow or heavy. Use filters and time range to limit data. Also consider using Kibana's Logs app (if enabled, under Observability -> Logs) which is tailored for streaming logs.

By anticipating these issues and following best practices, you can maintain a robust logging system.

## 9. Deploying to Production

Finally, let's discuss how to deploy this setup (Spring Boot application and ELK stack) to a production environment, and how to integrate it into a CI/CD pipeline. We'll also touch on best practices specifically for logging in microservices in a production context.

### 9.1 CI/CD Pipeline for Spring Boot with Docker

A typical production deployment will involve building Docker images for your Spring Boot app and deploying them, along with the ELK stack (or connecting to an existing ELK deployment). A CI/CD pipeline might look like:

1. **Continuous Integration (CI):** On each code push or merge:

   - Run tests (unit/integration tests).
   - Build the Spring Boot application (e.g., `mvn clean package` to get a fat jar).
   - Build a Docker image for the app. For example, create a `Dockerfile` for the Spring Boot app:
     ```dockerfile
     FROM eclipse-temurin:17-jdk-alpine  # small JDK base image
     COPY target/spring-elk-demo.jar /app/app.jar
     WORKDIR /app
     EXPOSE 8080
     ENTRYPOINT ["java","-jar","app.jar"]
     ```
     This minimal Dockerfile copies the jar and sets the entrypoint. (In a real scenario, you might have a multi-stage build to compile and then build the final image).
   - Tag and push the Docker image to a registry (DockerHub, ECR, etc.) e.g., `mycompany/spring-elk-demo:latest`.
   - (Optional) Also package or version your `docker-compose.yml` or Kubernetes manifests.

2. **Continuous Deployment (CD):** Deploy the new image to your environment:
   - If using Docker Compose on a server: pull the new image and do `docker-compose down && docker-compose up -d` (downtime can be mitigated by more advanced strategies, but Compose is basic).
   - In a more advanced setup, use Kubernetes: you'd update a Deployment with the new image tag, and K8s would do a rolling update (creating new pods with the new version, then terminating old ones).
   - Use a CI/CD tool (Jenkins, GitLab CI, GitHub Actions, etc.) to automate this. For example, a Jenkins pipeline could build the image and then use SSH or an agent on the server to run the deployment commands.
   - Ensure environment-specific configurations are handled. You might not commit passwords; instead use environment variables or external config (Spring Boot can externalize config in production, maybe via Kubernetes ConfigMaps or environment variables for database creds, etc.).
   - The ELK stack could be deployed separately from the application. Often, logging infrastructure is always running and apps just send data to it. You might not bring up ELK for each app deploy (except maybe the Filebeat sidecar or agent). Instead, you'd have a logging cluster and your app containers (or hosts) run Filebeat pointed at that cluster.

**CI/CD for Log components:** If you manage your own ELK, you might also automate its deployment:

- Use infrastructure as code (Docker Compose, Terraform, Ansible, Helm charts for K8s) to provision Elastic, Kibana, etc. Given the complexity, many choose hosted solutions for Elasticsearch to reduce ops burden.
- If self-managing, treat the config files (logstash.conf, filebeat.yml) as code too. For example, version control them. If a change is needed (like new grok pattern for a new service's logs), update the config and roll out a new Logstash container or config map.

**Automated Testing of Logging:** It’s a good idea to include some integration tests or staging tests where the app runs and you verify logs make it to Elasticsearch. This can be done by spinning up an ES container in a test and using a Testcontainers-based approach or a local environment test.

### 9.2 Deploying the ELK Stack in Production

When deploying ELK to production:

- **Resource Planning:** Determine expected log volume (events per second, data per day). Size your Elasticsearch cluster accordingly (number of nodes, RAM, CPU, disk). As a ballpark, if you log, say, 1GB per day, over 30 days that's 30GB of data plus index overhead (maybe indexing can add ~20-30% overhead). A single medium ES node could handle that. But if you're logging tens of GB or more per day, you'll need a cluster, and possibly indexing pipelines to filter out unnecessary data.
- **High Availability:** As mentioned, use multiple ES nodes (and ideally on different servers or AZs if cloud) with replicas, so that if one goes down, data is still accessible. Kibana can be single (if it goes down, no data loss, just UI downtime). Filebeat on each service host should buffer a bit if ES/Logstash is unreachable, but if the outage is long, some logs might be lost or Filebeat might stop if backpressure is too high. Consider using message queue (Kafka) for durability if that’s a concern.
- **Persistent Storage:** In Compose we used a named volume for ES data. In production, ensure those map to actual disk mounts with sufficient space. Also, have a backup strategy for ES indexes if the logs are critical (you can take snapshots of indices to S3 or other storage using ES snapshot API).
- **Monitoring the Monitors:** Use monitoring tools to keep an eye on your ELK stack itself. Elastic's X-Pack monitoring (or open-source alternatives like Prometheus exporters) can track ES node health, indexing rate, queue lengths, etc. This way you get alerted if, say, Logstash event queue is constantly full (meaning it's not keeping up), or if ES CPU is pegged at 100% for long periods (maybe need to scale up/out).
- **Separation of Environments:** Have separate logging environment for dev/test vs production, or use separate indices with prefixes (like `dev-myapp-logs-*` vs `prod-myapp-logs-*`) if sending to one cluster. This prevents test logs from mixing with prod logs.

**Alternate Approaches:** In Kubernetes environments, the typical stack is **EFK** (Elasticsearch, Fluentd, Kibana) or **ELK** with Filebeat/Metricbeat, etc. Fluentd/Fluent Bit can be used similarly to collect logs. The principles remain the same: aggregate logs and centralize them.

### 9.3 Best Practices for Logging in Microservices

To conclude, let's summarize some **best practices** for logging in a microservices context:

1. **Use Structured, Consistent Log Format:** Ensure all services log in a similar format (preferably JSON). This consistency makes it easier to parse and query logs. As we discussed, structured logging (like JSON) is highly recommended for microservices environments ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=are%20easy%20to%20read%20by,the%20log%20format%20keeps%20changing)).
2. **Include Context (Correlation ID):** Implement **Correlation IDs** for requests that span multiple services. For example, generate a unique ID (GUID) for each incoming request at the API gateway or first service, then pass it along downstream (e.g., via an HTTP header like `X-Correlation-ID`). Each service picks it up and includes it in its logs (MDC can automatically attach it to all logs for that request thread). This allows you to trace a single user request across numerous microservices by searching for that ID ([Mastering Microservices Logging - Best Practices Guide - SigNoz](https://signoz.io/blog/microservices-logging/#:~:text=Mastering%20Microservices%20Logging%20,to%20aggregate%20and%20analyze)). This practice is crucial in microservice debugging.
3. **Log Appropriate Information at Appropriate Levels:**
   - Use INFO for high-level application events (start/stop, major business actions), DEBUG for detailed debugging info (which can be disabled in prod), WARN for abnormal situations that are handled, ERROR for exceptions or issues that need attention.
   - Avoid logging sensitive data (PII, passwords, secrets) in logs ([Logging in Microservices: 5 Best Practices | Better Stack Community](https://betterstack.com/community/guides/logging/logging-microservices/#:~:text=Another%20thing%20you%20can%20do,while%20still%20maintaining%20log%20utility)). Mask or omit such information to comply with security and privacy.
   - If you must log something sensitive for debugging, scrub it out before writing (some logging frameworks support templates to omit or hash certain fields).
4. **Don’t Log too Verbosely in Prod:** Large volume of logs not only impacts performance but also costs more to store and analyze. Stick to needed information. If something is too verbose, consider raising its level to DEBUG so it's off by default.
5. **Centralize and Separate Log Streams:** Send logs to a central system (like ELK). Ensure each service’s logs can be distinguished. This can be via an explicit field (like "service":"user-service" in each log entry) or by indexing to separate indices per service (Filebeat can route logs to different index based on file path or config). Our example mostly dealt with one service; in a multi-service setup, you might use Filebeat with multiple inputs and add fields like `fields.service: employee-service` for logs from that service.
6. **Implement Log Retention Policies:** Do not keep logs forever. Decide how long logs are useful (for compliance or debugging). Many organizations keep 2-4 weeks of online logs and archive older ones. Use ILM to delete or move indices older than X days. This controls disk usage.
7. **Use Alerts and Analytics:** Treat logs not just as debug data but as operational data. Set up alerts for certain patterns (e.g., an error log with "OutOfMemory" should page someone). Use analytics to spot trends (e.g., a slow increase in WARN logs might indicate a brewing issue like resource exhaustion or a bug).
8. **Test your Logging Setup:** Just as you test features, test that your logging integration works whenever you add a new service or change a format. A broken logging pipeline (e.g., logs not being collected) can leave you blind to issues.
9. **Correlation with Traces/Metrics:** Logging is one pillar of observability. The others are metrics and tracing. For a holistic view, use distributed tracing (e.g., OpenTelemetry, Spring Cloud Sleuth as shown in some references) to capture request flows and tie them with logs (often the correlation ID bridges logs and traces). Also monitor metrics (e.g., request rates, error rates) from your services. These together will make diagnosing issues easier.
10. **Keep Logging Overhead Low in Services:** Offload heavy processing to the log system. The service should just emit logs quickly (non-blocking if possible) and let Filebeat/Logstash handle them. We used async appender suggestion and minimal formatting logic in the app for this reason.

By following these practices, you ensure that your microservices are observable, and issues can be identified and resolved faster. For example, when an error occurs, you'll quickly trace it across services by an ID, see all related logs, and possibly correlate with metrics like CPU spikes or memory usage from the same time.

## 10. Appendices

### 10.1 Useful Commands Reference

Here is a quick reference of commands and snippets useful during setup and maintenance:

**Spring Boot & Maven:**

- Run application: `mvn spring-boot:run` (or use your IDE's run).
- Package jar: `mvn package` (result in `target/*.jar`).
- Run the jar: `java -jar spring-elk-demo.jar` (you can pass `--spring.profiles.active=prod` or other props if needed).
- Set logging level via CLI: `java -Dlogging.level.com.example=DEBUG -jar app.jar`.

**Docker & Docker Compose:**

- Build Docker image for app: `docker build -t myapp:1.0 .` (ensure Dockerfile in current dir).
- Run a container: `docker run -d -p 8080:8080 myapp:1.0`.
- Start services with Compose: `docker-compose up -d` (in directory of yaml).
- Stop services: `docker-compose down` (add `-v` to remove volumes).
- View combined logs: `docker-compose logs -f` (shows logs of all containers; or specify a service).
- List running containers: `docker ps` (or `docker-compose ps` in context of compose).
- Enter a container shell: `docker exec -it <container_name> /bin/bash` (useful for debugging, e.g., check if filebeat container can see the log file, etc.).
- Prune unused containers/volumes: `docker system prune` (careful – removes stopped containers and dangling images).

**Elasticsearch (via API using curl or Kibana Console):**

- Check cluster health: `curl http://localhost:9200/_cluster/health?pretty`.
- List indices: `curl http://localhost:9200/_cat/indices?v`.
- Get mapping of index: `curl http://localhost:9200/myapp-logs-*/_mapping?pretty`.
- Search logs (simple): `curl http://localhost:9200/myapp-logs-*/_search?q=logger:EmployeeService`.
- Search logs (complex JSON query):
  ```bash
  curl -H "Content-Type: application/json" -XGET localhost:9200/myapp-logs-*/_search?pretty -d '{
    "query": {
      "bool": {
        "must": [
           {"match": {"log-message": "error"}}
        ],
        "filter": [
           {"term": {"log-level": "ERROR"}}
        ]
      }
    }
  }'
  ```
  (This finds documents where log-message contains "error" and log-level is exactly ERROR.)
- Delete an index (to clear data): `curl -XDELETE http://localhost:9200/myapp-logs-2025.02.19` (use with caution!).
- Index a test document (for troubleshooting):
  ```bash
  curl -XPOST "http://localhost:9200/myapp-logs-test/_doc" -H 'Content-Type: application/json' -d'
  { "@timestamp":"2025-02-19T00:00:00Z", "log-level":"INFO", "message":"Test log"}'
  ```

**Kibana:**

- Access Kibana: [http://localhost:5601](http://localhost:5601).
- In Kibana Dev Tools Console, you can use the same ES queries without curl.

**Logstash:**

- Test Logstash config (if you have logstash installed locally): `logstash -f logstash.conf --config.test_and_exit` (checks config syntax).
- Send a test message via TCP:
  ```
  echo '{"@timestamp":"2025-02-19T12:00:00.000Z","message":"hello","level":"INFO"}' | nc localhost 5044
  ```
  (If Logstash input codec is plain, this might not parse as JSON automatically; if codec is json, this would create a doc.)
- Logstash API (if open on 9600): `curl http://localhost:9600/_node/stats/pipeline?pretty` (shows pipeline metrics like events received, filtered, etc.).

**Filebeat:**

- Check Filebeat registry (in container at `/usr/share/filebeat/data/registry/filebeat` usually, you can exec into container and look).
- Filebeat test output (not easily done in container without running command manually, but if installed locally: `filebeat test output` to test connection to ES/LS, and `filebeat test config` to verify config file syntax).

**System:**

- Set `vm.max_map_count` on Linux: `sudo sysctl -w vm.max_map_count=262144` ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=To%20view%20the%20current%20value,setting%2C%20run)). To make permanent, add `vm.max_map_count=262144` to `/etc/sysctl.conf`.
- Monitor Docker resource usage: `docker stats` (shows live CPU/mem usage of containers).
- Monitor Elasticsearch logs: They appear via `docker-compose logs elasticsearch`. Or inside container in `/usr/share/elasticsearch/logs/`.

### 10.2 Troubleshooting Guide

Here’s a quick troubleshooting table for common issues:

- **Problem:** Elasticsearch container exits with error "`max virtual memory areas vm.max_map_count [65530] is too low`".  
  **Cause:** Host setting for virtual memory too low for ES.  
  **Solution:** Increase `vm.max_map_count` to at least 262144 on the host and restart the container ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=The%20,for%20production%20use)).
- **Problem:** Kibana shows "Could not fetch index pattern" or no data.  
  **Cause:** Index pattern not created or no indices match.  
  **Solution:** Create the correct index pattern in Kibana (e.g., `myapp-logs-*`). Ensure logs are indexed (use `_cat/indices` to verify index names).
- **Problem:** Filebeat container running but Logstash not receiving data (no logs).  
  **Cause:** Misconfiguration of Filebeat output or network issue.  
  **Solution:** Check Filebeat logs for connection errors. Verify that Filebeat’s `output.logstash.hosts` is set to `logstash:5044` and that the Filebeat service is on same network as Logstash. Ensure Logstash is listening (check `docker-compose logs logstash` for "Beats input opened"). If needed, expose 5044 and try connecting via host to test.
- **Problem:** Logstash is receiving data (as seen in stdout) but nothing in Elasticsearch.  
  **Cause:** Issue in output stage. Could be authentication failure (if ES secure), or index naming issue.  
  **Solution:** Check Logstash logs for errors on output. If using security, ensure credentials are correct. If index name has illegal characters, ES might reject (though our pattern is fine). Also check ES logs for any indexing errors.
- **Problem:** A specific type of log (e.g., multiline stack trace) is not indexed or is split incorrectly.  
  **Cause:** Multiline not configured or pattern mismatch.  
  **Solution:** Enable multiline in Filebeat config (as we did) to join stack traces. If already done, verify the regex (in our config, we used `'^\s'` to capture lines starting with whitespace as continuation). Adjust if needed (some logs might not have leading space). Alternatively, handle multiline in Logstash using multiline codec.
- **Problem:** After restarting the Spring Boot app, no new logs appear in Kibana.  
  **Cause:** Possibly Filebeat thinks it already read those logs (if the file was recreated with same name and inode).  
  **Solution:** Restart Filebeat so it re-harvests. Or delete the registry entry for that file (not trivial manually). Ensuring file rotation uses new file names helps (so Filebeat sees a new file). For dev, easiest is bounce Filebeat container whenever you restart the app if logs not updating.
- **Problem:** Data volume grows too large.  
  **Cause:** Old indices not removed.  
  **Solution:** Implement ILM or manually delete indices older than a threshold. You can use Curator (an Elastic tool) or ILM (with policies like delete after X days). For example, to delete >30d: use ILM policy with delete phase at 30d, or periodically run a script to DELETE indices with date < today-30.
- **Problem:** Logstash pipeline slows down significantly, causing Filebeat to backpressure (Filebeat logs might say "delay because of backpressure").  
  **Cause:** Logstash can't process as fast as logs incoming. Possibly heavy grok or too much volume for one instance.  
  **Solution:** Optimize grok (use more specific patterns to avoid catastrophic backtracking, or parse differently). Increase Logstash JVM heap if it's GC thrashing. Scale out: run multiple Logstash instances and have Filebeat distribute load. Or consider switching to a lighter pipeline (e.g., use Elasticsearch ingest nodes for parsing).
- **Problem:** One microservice's logs are too noisy and clutter Kibana for others.  
  **Solution:** Use separate indices per service. For example, Filebeat can add a field `service: X` and Logstash can use it in the index name (`index => "%{[service]}-logs-%{+YYYY.MM.dd}"`). Then in Kibana, you can have separate index patterns or filters for each service. Alternatively, use tags or fields in queries to isolate logs by service.

### 10.3 Additional Resources and References

For further reading and reference, here are some useful resources:

- **Spring Boot Reference - Logging:** Official Spring Boot documentation on logging configuration and how to customize Logback or Log4j2 ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=Spring%20Boot%20has%20a%20,it%20is%20the%20first%20choice)) ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=You%20can%20also%20set%20the,logging.file)).
- **Elastic Stack (Elasticsearch, Kibana, Beats) Documentation:** Official Elastic docs, including [Install Elasticsearch with Docker][ElasticDocker] (covers important host settings) and [Filebeat Reference - Log Input][FilebeatLog] for configuring Filebeat inputs ([Log input | Filebeat Reference [8.17] - Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=Use%20the%20log%20input%20to,and%20fetch%20the%20log)).
- **Auth0 Blog – _Spring Boot Logs Aggregation and Monitoring using ELK_:** A step-by-step tutorial similar to this guide, which also demonstrates separating logs by service using Filebeat and includes example code ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=This%20article%20will%20demonstrate%20how,available%20in%20this%20GitHub%20repository)) ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=developing%20any%20software,in%20case%20an%20error%20comes)).
- **Centralized Logging for Microservices (Mindbowser Blog):** Article explaining benefits of ELK in microservices and some setup guidance ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Microservices%20architectures%2C%20while%20offering%20agility%2C,Let%E2%80%99s%20briefly%20introduce%20these%20components)) ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Benefits%20of%20Centralized%20Logging%20with,ELK)).
- **Better Stack Community – _Logging in Microservices: 5 Best Practices_:** Discusses best practices like standardization, centralization, correlation IDs, etc., which we summarized ([Logging in Microservices: 5 Best Practices | Better Stack Community](https://betterstack.com/community/guides/logging/logging-microservices/#:~:text=1)) ([Logging in Microservices: 5 Best Practices | Better Stack Community](https://betterstack.com/community/guides/logging/logging-microservices/#:~:text=3)).
- **Smit Shah’s Blog – _Filebeat Integration with Spring Boot_:** Provides a concise example of Filebeat + Logstash config for Spring Boot logs (which inspired our config) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=Lets%20configure%20the%20filebeat%20to,read%20the%20logs%20file)) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=filter%20,message%7D%22%20%7D%20%7D)).
- **Dev.to – _Building a Robust ELK Integration with Spring Boot Microservices_:** A blog covering advanced topics like distributed tracing (Sleuth) and APM integration in addition to ELK, for those looking to go beyond just logging ([Building a Robust ELK Integration with Spring Boot Microservices - DEV Community](https://dev.to/devaaai/building-a-robust-elk-integration-with-spring-boot-microservices-1gc1#:~:text=Integrating%20ELK%20with%20Spring%20Boot,maintainable%2C%20and%20highly%20observable%20system)) ([Building a Robust ELK Integration with Spring Boot Microservices - DEV Community](https://dev.to/devaaai/building-a-robust-elk-integration-with-spring-boot-microservices-1gc1#:~:text=,friendly%20dashboards%20for%20actionable%20insights)).
- **Docker Official Documentation:** For installation and usage of Docker and Docker Compose [Docker Desktop Guide][DockerDesktop] ([How to install in windows? : r/immich - Reddit](https://www.reddit.com/r/immich/comments/1b5u6p2/how_to_install_in_windows/#:~:text=https%3A%2F%2Fdocs.docker.com%2Fdesktop%2Finstall%2Fwindows,reboot)).
- **Elastic Forums and Stack Overflow:** Many troubleshooting Q&As exist for specific errors (e.g., searching the exact error message often leads to solutions, like the vm.max_map_count issue or filebeat common problems).

By leveraging these resources and the steps in this guide, you should be well-equipped to implement a robust logging system for Spring Boot microservices with the ELK stack and Docker. Logging, when done right, becomes an asset rather than overhead – it provides eyes into the behavior of a complex system, which is invaluable for maintaining and scaling applications.

---

**Footnotes / References:**

([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=This%20article%20will%20demonstrate%20how,available%20in%20this%20GitHub%20repository)) Tyagi, Apoorv. _Spring Boot Logs Aggregation and Monitoring Using ELK Stack_. Auth0 Blog (2021). – Discusses challenges of debugging microservices and introduces ELK as a solution ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Having%20a%20good%20log%20monitoring,in%20case%20an%20error%20comes)), demonstrating integration steps.

([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Microservices%20architectures%2C%20while%20offering%20agility%2C,Let%E2%80%99s%20briefly%20introduce%20these%20components)) ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Benefits%20of%20Centralized%20Logging%20with,ELK)) Mindbowser. _Explore Streamlined Development: ELK Stack for Spring Boot Microservices_. – Highlights how ELK centralizes logs and benefits like unified storage and real-time monitoring in microservices ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Microservices%20architectures%2C%20while%20offering%20agility%2C,Let%E2%80%99s%20briefly%20introduce%20these%20components)) ([Centralized Logging for Spring Boot Microservices: ELK Guide](https://www.mindbowser.com/explore-spring-boot-microservices/#:~:text=Benefits%20of%20Centralized%20Logging%20with,ELK)).

([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=Lets%20configure%20the%20filebeat%20to,read%20the%20logs%20file)) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=filter%20,message%7D%22%20%7D%20%7D)) Shah, Smit. _Filebeat Integration with Spring Boot Application_. (2024). – Provides Filebeat config to monitor a Spring Boot log file and Logstash grok patterns for parsing Spring Boot logs (INFO level, timestamp, etc.) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=filebeat.inputs%3A%20,%2FUsers%2FSmit%2FDownloads%2Fdemo%2Fmyapp.log)) ([Filebeat Integration with Spring Boot Application](https://shahsmit.hashnode.dev/filebeat-integration-with-spring-boot-application#:~:text=filter%20,message%7D%22%20%7D%20%7D)).

([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=Spring%20Boot%20has%20a%20,it%20is%20the%20first%20choice)) ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=You%20can%20also%20set%20the,logging.file)) Spring Boot Documentation – Section on logging configuration. Explains how to use starters for logging and ways to configure logging levels and file output via properties ([83. Logging](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html#:~:text=If%20the%20only%20change%20you,shown%20in%20the%20following%20example)).

([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=The%20,for%20production%20use)) Elastic Documentation – _Install Elasticsearch with Docker_. – States the requirement for vm.max_map_count=262144 for production use of Elasticsearch and how to set it ([Install Elasticsearch with Docker | Elasticsearch Guide [8.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=The%20,for%20production%20use)).

([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=are%20easy%20to%20read%20by,the%20log%20format%20keeps%20changing)) Otero, Orlando. _Configuring JSON-Formatted Logs in Spring Boot_. – Emphasizes formatting logs as JSON for easy ingestion by log aggregators ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=are%20easy%20to%20read%20by,the%20log%20format%20keeps%20changing)).

([Mastering Microservices Logging - Best Practices Guide - SigNoz](https://signoz.io/blog/microservices-logging/#:~:text=Mastering%20Microservices%20Logging%20,to%20aggregate%20and%20analyze)) SigNoz Blog – _Mastering Microservices Logging - Best Practices_. – Recommends including correlation IDs in all log entries for traceability across microservices ([Mastering Microservices Logging - Best Practices Guide - SigNoz](https://signoz.io/blog/microservices-logging/#:~:text=Mastering%20Microservices%20Logging%20,to%20aggregate%20and%20analyze)).

([Logging in Microservices: 5 Best Practices | Better Stack Community](https://betterstack.com/community/guides/logging/logging-microservices/#:~:text=Another%20thing%20you%20can%20do,while%20still%20maintaining%20log%20utility)) Better Stack Community – _Logging in Microservices: 5 Best Practices_. – Advises against logging sensitive information and suggests using log shippers to redact if needed ([Logging in Microservices: 5 Best Practices | Better Stack Community](https://betterstack.com/community/guides/logging/logging-microservices/#:~:text=Another%20thing%20you%20can%20do,while%20still%20maintaining%20log%20utility)).

([Create an index pattern | Kibana Guide [7.17] - Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=Open%20the%20main%20menu%2C%20then,and%20Kibana%20looks%20for)) Elastic Kibana Guide – _Create an index pattern_. – How to create an index pattern in Kibana via Stack Management ([Create an index pattern | Kibana Guide [7.17] - Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=Open%20the%20main%20menu%2C%20then,and%20Kibana%20looks%20for)).

[ElasticDocker]: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
[FilebeatLog]: https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html
[DockerDesktop]: https://docs.docker.com/desktop/install/windows-install/
