# Spring Boot Application Logging with Filebeat, Elasticsearch, and Kibana – A Step-by-Step Guide

Building a robust log management pipeline involves **generating structured logs** from your application, **shipping them reliably**, storing and indexing them in **Elasticsearch**, and finally **visualizing and monitoring** them via Kibana. This guide walks through a comprehensive example for advanced developers, using a Spring Boot application as the log source, Filebeat as the log shipper, Elasticsearch as the log store, and Kibana for analysis. We’ll cover everything from setting up the Spring Boot app and structured logging, to configuring Filebeat and ingest pipelines, to building Kibana dashboards and deploying the stack in various environments. Each section provides step-by-step instructions, code snippets, best practices, and troubleshooting tips.

## 1. Spring Boot Setup – Project and Configuration

**Initialize the Project:** Start by creating a new Spring Boot project (using Spring Initializr or your IDE). Include the **Spring Boot Starter Web** dependency for a simple web application (this transitively includes `spring-boot-starter-logging` which brings in Logback and SLF4J). If using Maven, your `pom.xml` should declare at least:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>${spring.boot.version}</version>
</dependency>
```

This ensures Logback is on the classpath (the default logging framework in Spring Boot) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%60spring,library%20through%20the%20Slf4j%20facade)) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%3Cdependency%3E%20%3CgroupId%3Enet.logstash.logback%3C%2FgroupId%3E%20%3CartifactId%3Elogstash)). If using Gradle, add `implementation 'org.springframework.boot:spring-boot-starter-web:<version>'` to your `build.gradle`. Verify that the project builds and you can run a basic `@SpringBootApplication` main class.

**Structure:** The project should have the standard Spring Boot structure (with `src/main/java` for code and `src/main/resources` for configuration). Create an application class annotated with `@SpringBootApplication` and (optionally) a simple REST controller or a `CommandLineRunner` to generate some logs. For example:

```java
@SpringBootApplication
public class LoggingDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(LoggingDemoApplication.class, args);
    }
}
```

Optionally, add a sample REST controller or runner to produce log messages (we will configure the logging in the next section). For instance, you might use a `CommandLineRunner` bean or a `@RestController` that logs events at startup and on each request.

**Application Properties:** In `src/main/resources/application.properties` (or YAML), set the basic configs like application name and server port as needed. Also, assign a name to the application (this can be used in logs):

```properties
spring.application.name=demo-logging-app
server.port=8080
```

These will help identify the service in log entries and Kibana (the `spring.application.name` can be injected into the log configuration). With the project scaffolding in place, you’re ready to configure structured logging.

## 2. Logging Setup – Logback/SLF4J Configuration for JSON Logs

To effectively ship logs to Elasticsearch, it’s best to log in a **structured JSON format**. Structured logs are machine-readable and easier for aggregators to parse (as opposed to plain text logs which are easy for humans but hard for log aggregators to reliably parse) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=Standard)). Spring Boot’s default logging format is text; we will customize Logback to output JSON, include contextual fields, and handle file rotation.

**Add Logback JSON Dependency:** Include the Logstash Logback Encoder library, which provides Logback encoders to format logs as JSON. In Maven, add:

```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.3</version> <!-- compatible with Logback 1.2.x and Spring Boot 2.x  ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%3Cdependency%3E%20%3CgroupId%3Enet.logstash.logback%3C%2FgroupId%3E%20%3CartifactId%3Elogstash)) -->
</dependency>
```

In Gradle: `implementation 'net.logstash.logback:logstash-logback-encoder:7.3'`. This library allows us to use `LogstashEncoder` in the Logback config to produce JSON logs.

**Logback Configuration:** Create a file `src/main/resources/logback-spring.xml` (Spring Boot will automatically use this for Logback configuration). We’ll configure two profiles: one for standard console logging during development, and one for JSON logging in production. For example:

```xml
<configuration>
   <!-- Include default Spring Boot log settings for non-JSON profile -->
   <springProfile name="!json-logs">
      <include resource="org/springframework/boot/logging/logback/base.xml"/>
   </springProfile>

   <!-- JSON logging profile -->
   <springProfile name="json-logs">
      <!-- Console appender in JSON format -->
      <appender name="jsonConsole" class="ch.qos.logback.core.ConsoleAppender">
         <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
      </appender>
      <!-- File appender in JSON format with rolling policy -->
      <appender name="jsonFile" class="ch.qos.logback.core.rolling.RollingFileAppender">
         <file>logs/app.log</file>  <!-- log file location -->
         <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/app-%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>7</maxHistory> <!-- keep 7 days of logs -->
         </rollingPolicy>
         <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
      </appender>
      <!-- Root logger uses both appenders -->
      <root level="INFO">
         <appender-ref ref="jsonConsole"/>
         <appender-ref ref="jsonFile"/>
      </root>
   </springProfile>
</configuration>
```

In this configuration:

- When the Spring profile `json-logs` is **active**, Logback will output logs in JSON to both console and a rolling file (one file per day, keeping 7 days) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=)) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=)). When the profile is not active (e.g. during local dev), it falls back to default text logging for readability ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=,logs%20is%20active)).
- The JSON encoder outputs each log event as a single line JSON object containing fields like `@timestamp`, `level`, `logger_name`, `thread_name`, and the log `message` ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%7B%22%40timestamp%22%3A%222023)). (If an exception is logged, the stack trace will be included in a `stack_trace` field as part of the JSON output, with newline characters embedded ([logstash-logback-encoder/README.md at master · liangyanfeng/logstash-logback-encoder · GitHub](https://github.com/liangyanfeng/logstash-logback-encoder/blob/master/README.md#:~:text=)).)
- We used a TimeBasedRollingPolicy to rotate log files daily. You could also use a size-based policy or a combination for log rotation, ensuring old logs are archived or deleted to avoid unlimited file growth.

**Activate JSON Logging:** In production, you’ll run the app with the `json-logs` profile active to enable JSON output. For example, add `--spring.profiles.active=json-logs` to the JVM arguments or set `SPRING_PROFILES_ACTIVE=json-logs` as an environment variable. In development, you can omit this profile to see the familiar text logs (since JSON is hard to read manually) ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=,logs%20is%20active)).

**Structured Log Fields:** The default JSON from `LogstashEncoder` includes useful fields:

- `@timestamp` (log event time),
- `level` (INFO, DEBUG, etc.),
- `logger_name` (the class or logger that logged the message),
- `thread_name`,
- `message`, and others.

You can further customize the JSON output. For example, you could add an **application name** or environment field. In the above snippet, we could inject the Spring app name using a `springProperty` and include it as a field in the JSON (the Spring Framework Guru example shows adding `appName` and even a trace ID) ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=%3Cformat%3E%20%3Clabel%3E%20%3Cpattern%3Eapp%3D%24%7BappName%7D%2Chost%3D%24%7BHOSTNAME%7D%2CtraceID%3D%25X%7BtraceId%3A,sortByTime)) ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=%3Cappender,configuration)). For brevity, we stick with the defaults, which are sufficient for basic log analysis. Make sure that any unique fields you add (like `traceId` for distributed tracing correlation) are included in the JSON format.

**SLF4J Usage:** In your application code, use SLF4J (`LoggerFactory.getLogger(...)` and `logger.info("message")`) as usual. The Logback config ensures all such logs (from your code and Spring internals) will be captured and formatted. For example, a log statement `logger.warn("User {} failed login from IP {}", userId, ip)` would produce a JSON log entry like:

```json
{
  "@timestamp": "2025-03-15T10:00:23.456Z",
  "level": "WARN",
  "logger_name": "com.example.LoginService",
  "thread_name": "http-nio-8080-exec-3",
  "message": "User 42 failed login from IP 10.1.1.123"
}
```

with any exception stack traces, if logged, included as a `stack_trace` field (multi-line stack traces are kept in one JSON field). These JSON logs will be much easier to index and search in Elasticsearch than plain text logs.

**Troubleshooting Log Configuration:** If your application fails to start due to Logback config errors, check the console for configuration parse errors. Common issues include using an incompatible version of `logstash-logback-encoder` (ensure it’s compatible with your Logback version; e.g., version 7.4+ of the encoder requires Logback 1.3+, which Spring Boot 3 uses, but Spring Boot 2.x uses Logback 1.2 so stick to encoder 7.3) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%3Cdependency%3E%20%3CgroupId%3Enet.logstash.logback%3C%2FgroupId%3E%20%3CartifactId%3Elogstash)). Also verify the file path (`logs/app.log`) exists or can be created by the app; Spring Boot by default writes to `./spring.log` if `logging.file.name` is set, but here we explicitly set our file appender path. Once the app runs with JSON logging, we can proceed to ship those logs.

## 3. Filebeat Configuration – Shipping Logs to Elasticsearch

**What is Filebeat?** Filebeat is a lightweight log shipper (Beat) that **tails log files and forwards log lines** to destinations like Elasticsearch or Logstash. We use Filebeat to read our Spring Boot log file and send each JSON log entry to Elasticsearch in real-time. Filebeat is preferred for simplicity and reliability; it’s resource-efficient and can handle backpressure (it will slow down reading if Elasticsearch is overwhelmed, preventing data loss) ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%20won%E2%80%99t%20let%20you%20overload,your%20pipeline)).

**Install Filebeat:** Download and install Filebeat from Elastic’s website (choose the version matching your Elasticsearch version). You can run it on the same host as the Spring Boot app (e.g., as a service or Docker container). For example, on Linux you might use `deb`/`rpm` packages or simply download the tar, or use Docker image `docker.elastic.co/beats/filebeat:8.x`. Ensure Filebeat can access the directory where your Spring Boot app writes logs.

**Filebeat Configuration File (`filebeat.yml`):** Open the Filebeat config (usually `/etc/filebeat/filebeat.yml` or a custom path if using Docker). We will configure: an **input** (to read the log file), some **parsing settings** (to handle JSON and multiline), and an **output** (to Elasticsearch). Minimal configuration for our scenario:

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /path/to/your/app/logs/app.log* # path to log file(s); wildcard for rotated files
    multiline.pattern: "^[[:space:]]"
    multiline.negate: false
    multiline.match: after
    json.keys_under_root: true
    json.add_error_key: true
    # (Filebeat 7.x and 8.x automatically detect JSON per line; these settings ensure JSON is parsed)

output.elasticsearch:
  hosts: ["localhost:9200"]
  protocol: "http"
  username: "elastic"
  password: "YourElasticPassword"
  index: "demo-logging-app-%{+yyyy.MM.dd}"
  pipeline: "springboot-logs-pipeline" # optional ingest pipeline for additional parsing
```

Let’s break down what this configuration does:

- **Input Path:** The `paths` setting should point to the Spring Boot log file. Use the absolute path to `app.log` as configured in Logback (and include `*` to catch rotated files like `app-2025-03-15.log`). This way Filebeat will read new log lines as they are appended.

- **Multiline Handling:** The multiline settings combine stack trace lines into a single event. The regex pattern `^[[:space:]]` matches lines beginning with whitespace ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=multiline.pattern%3A%20%27,after)), which is a common trait of continuation lines in Java stack traces (each line after the first in a stack trace starts with a tab or space). By setting `negate: false` and `match: after`, Filebeat will **append any line that starts with whitespace to the previous line** ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=,does%20not%20match%20the%20pattern)). This means if an exception is logged and printed across multiple lines, Filebeat will treat it as one log message event, preserving the full stack trace in one JSON (preventing the stack trace lines from appearing as separate log entries in Elasticsearch) ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=So%2C%20the%20stack%20trace%20above,file)) ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=multiline.pattern%3A%20%27,after)). This is important for accurate log context.

- **JSON Parsing:** The `json.keys_under_root: true` tells Filebeat to parse each line as JSON and place the decoded fields at the root of the event ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=,dot%20keys%20in%20the)) ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=,removed%20from%20the%20original%20json)). Since our log lines are already JSON, this setting will decode them so that fields like `message`, `level`, `logger_name`, etc., become first-class fields in the event (rather than one big string). We also set `json.add_error_key: true` to add an `error.message` field if JSON parsing fails (useful for troubleshooting) ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=should%20be%20enabled%20when%20the,or%20multiline%20aggregation%20will%20occur)). **Note:** We did not specify `json.message_key` here because our JSON log is not nested inside another field — each line is a pure JSON object. Filebeat will by default put the raw text in the `message` field, but since we decode JSON, the `message` field from our JSON (the log message) will overwrite the original. By also specifying an explicit `index` in the output (see below), we avoid using Filebeat’s default indexing which might include its own keys. If needed, `json.overwrite_keys: true` can ensure Filebeat’s own default fields (like its `message`) are overwritten by our JSON fields ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=,produced%20by%20an%20ECS%20logger)).

- **Output to Elasticsearch:** Under `output.elasticsearch`, specify the host URL of Elasticsearch (in this case, localhost on default port 9200). If security is enabled on ES (which it is by default in Elastic 8.x), provide the credentials (e.g., the built-in `elastic` superuser and its password, or a dedicated ingest user). You can also use API keys or SSL certificates if configured — ensure Filebeat is set up with the appropriate TLS settings if your ES uses HTTPS.

- **Custom Index Name:** We set `index: "demo-logging-app-%{+yyyy.MM.dd}"` to have Filebeat write to a daily index for our app (named by date). This is a best practice for time-series log data, as it allows easy index rotation and deletion. Without this, Filebeat default would use an index like `filebeat-8.x-YYYY.MM.dd` (or an ILM policy) ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Similar%20to%20what%20you%20have,from%20the%20Elasticsearch%20indices%20list)). A custom index name lets us manage mappings and lifecycle for just our app’s logs. **Important:** When you set a custom index in Filebeat, the default index template may not automatically apply, so we will create a mapping template in Elasticsearch (covered in the next section).

- **Ingest Pipeline (Optional):** We referenced a pipeline named `"springboot-logs-pipeline"`. This is optional – if you want Elasticsearch to perform additional parsing or enrichment (like processing fields further or adding geoIP info), you can create an ingest pipeline in Elasticsearch and tell Filebeat to use it for each event. We’ll discuss pipeline setup in the next section. If you do not need any extra processing on the Elasticsearch side (because the logs are already structured), you can omit the `pipeline` setting.

**Enable and Run Filebeat:** Once configured, start Filebeat. For example, on Linux: `sudo systemctl start filebeat` (if installed as service) or run `filebeat -c filebeat.yml -e` to run it foreground and output logs to console for debugging. On Docker, run the container with volume mounts for your config and log file. When Filebeat starts, it should log that it opened the file (harvester started) and soon publish events to Elasticsearch. Use `filebeat test output` to test connectivity to ES (it should say "connection OK").

**Troubleshooting Filebeat:** If you don’t see logs in Elasticsearch, check Filebeat’s own logs. Common issues:

- Filebeat not harvesting the file: Ensure `enabled: true` and the file path is correct. Filebeat may ignore a file if it was previously ingested (to avoid re-reading old logs). Delete the Filebeat registry (often in `/var/lib/filebeat/registry` or set a clean registry) to force re-read, or use `start_position: beginning` for first run.
- JSON parse errors: If the logs aren’t strict JSON (e.g., extra trailing commas or unescaped characters), Filebeat will add an `error.message` field. Use Kibana to check if `error.message: json` appears ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=should%20be%20enabled%20when%20the,or%20multiline%20aggregation%20will%20occur)). In our case, using a proven encoder means this is unlikely.
- Elasticsearch errors: Filebeat logs will show if ES rejected events (e.g., mapping conflicts or authentication issues). Ensure the credentials are correct and have privileges to create indices and write. If using a cloud service (AWS OpenSearch or Elastic Cloud), ensure the endpoint and any required cloud ID/auth are configured.

Once Filebeat is successfully pushing data, you should see the index in Elasticsearch. Let’s set up Elasticsearch and Kibana to receive and visualize these logs.

## 4. Elasticsearch & Kibana Setup – Index Management and Configuration

**Install Elasticsearch and Kibana:** If you haven’t already, install Elasticsearch and Kibana (preferably the same version). For local testing, you can use Docker images or download the archives:

- **Elasticsearch:** Configure it for single-node development mode by setting `discovery.type=single-node` (if using Docker, this is done by default in recent versions). Ensure it’s running and accessible on `localhost:9200`. Also, if security is enabled (Elastic 8+), use the generated password for the `elastic` user or create a new user for Filebeat ingest.
- **Kibana:** Run Kibana and point it to your Elasticsearch (e.g., in `kibana.yml` or via environment, set `ELASTICSEARCH_HOSTS: ["http://localhost:9200"]`). Kibana typically runs on `localhost:5601`.

**Verify Logs in Elasticsearch:** Once Elasticsearch is up and Filebeat is running, verify that logs are indexing:

- Use the Kibana Dev Tools console or `curl` to check for indices: for example, `GET _cat/indices?v` should show an index like `demo-logging-app-2025.03.15` (if Filebeat created it). You can also search for a document: `GET demo-logging-app-*/_search?q=level:INFO` to see if documents are present.
- If the index is not there, check Filebeat logs again or Elasticsearch logs for errors. If the index is there but no documents, possibly Filebeat started but hasn’t sent events (check that your application actually logged something after Filebeat start; generate a few log lines by accessing the app or triggering the logger).

**Index Mapping and Templates:** We want Elasticsearch to properly map fields (e.g., `@timestamp` as a date, `level` as keyword, etc.) and not use defaults that might be suboptimal. By default, ES will infer field types: the `@timestamp` from our JSON will likely be parsed as a date (because Filebeat might recognize it as timestamp), and string fields will become text + keyword multifields. However, it’s good practice to define an index template for consistency. We can define a template so that any index matching `demo-logging-app-*` gets our custom mappings and settings. In Kibana Dev Tools, execute:

```json
PUT _index_template/demo-logging-app-template
{
  "index_patterns": ["demo-logging-app-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "refresh_interval": "5s"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "logger_name": { "type": "keyword" },
        "thread_name": { "type": "keyword" },
        "message": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above":256 } } },
        "stack_trace": { "type": "text" }
      }
    }
  }
}
```

This template ensures specific types:

- `@timestamp` as date,
- `level`, `logger_name`, `thread_name` as keywords (exact match, aggregatable fields),
- `message` as text (full-text search) with a keyword subfield for exact matching,
- `stack_trace` as text (not analyzed in detail, but stored for searching error text).

Apply this _before_ a new index is created (if an index already exists, you may need to reindex or adjust mapping via the compose index API, which is advanced). If you already have an index, you can delete it (if it’s test data) so that it gets recreated with the template on the next write. Another approach is to use Elasticsearch’s dynamic templates or the default Filebeat template, but for clarity we explicitly set a template.

**Ingest Pipeline (Optional):** If you want to do additional processing on the logs as they come into Elasticsearch, set up an ingest pipeline. For instance, you might want to:

- Copy the `level` field to `log.level` (to conform with Elastic Common Schema),
- Parse an IP address field to geo-location (not applicable in our simple log example),
- Or extract an exception type from the `stack_trace`.

As an example, we create a simple pipeline that just copies our `level` field to `log.level` and sets the event `@timestamp` from the log (in case Filebeat’s event time is different):

```json
PUT _ingest/pipeline/springboot-logs-pipeline
{
  "description": "Process Spring Boot app logs",
  "processors": [
    {
      "set": {
        "field": "log.level",
        "value": "{{level}}"
      }
    },
    {
      "date": {
        "field": "@timestamp",
        "target_field": "@timestamp",
        "formats": ["ISO8601"]
      }
    }
  ]
}
```

We referenced this pipeline in Filebeat config (`pipeline: "springboot-logs-pipeline"`). The above pipeline uses a date processor to parse the `@timestamp` field (which is already an ISO8601 string from our JSON) and overwrite the document’s `@timestamp`. In practice, Filebeat might have already done that if it recognized the JSON field as the timestamp; but this ensures the final indexed timestamp is correct and uses the log’s time, not the ingestion time. We also copy `level` to `log.level` to match ECS naming. You could add more processors, such as remove the original `level` if not needed or add any tags. If no extra processing is needed, you can skip the pipeline entirely.

**Kibana Index Pattern (Data View):** Now that logs are flowing into an index with known pattern, configure Kibana to recognize it:

1. In Kibana, go to **Stack Management > Index Patterns (Data Views)** ([Create an index pattern | Kibana Guide [7.17] | Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=1,Click%20Create%20index%20pattern)).
2. Click “Create index pattern”. Enter the index pattern as `demo-logging-app-*` (or `filebeat-*` if you used default). Kibana will auto-detect indices matching this pattern ([Create an index pattern | Kibana Guide [7.17] | Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=3,aliases%20that%20match%20your%20input)).
3. Select `@timestamp` as the time filter field (Kibana will suggest it since our mapping has a date field) ([Create an index pattern | Kibana Guide [7.17] | Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=4,filtering%20your%20data%20by%20time)).
4. Create the index pattern. Now Kibana knows about fields like `level`, `message`, etc., for our logs ([Create an index pattern | Kibana Guide [7.17] | Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=5)).

**Discover Logs:** Navigate to **Analytics > Discover** in Kibana and select the new index pattern (if it’s not already the default) ([Create a dashboard to visualize application logs in Kibana - DEV Community](https://dev.to/moesmp/create-a-dashboard-to-visualize-application-logs-in-kibana-2h5h#:~:text=Image%3A%20Alt%20Text)). You should see log documents streaming in. You can use the search bar to filter logs (for example, `level: "ERROR"` to see only error logs). Verify that fields are parsed: for instance, you can add “level”, “logger_name”, etc. as columns in Discover to confirm they are properly ingested as separate fields (not just part of the message). Each log event should be a structured JSON document in Elasticsearch, thanks to our Filebeat JSON parsing and ingest pipeline.

**Troubleshooting Data Ingestion:** If you do not see data in Discover:

- Check that the time range in Kibana is correct (e.g., “Last 15 minutes”). If your logs are older, adjust the time picker.
- Ensure the correct index pattern is selected and that it shows a document count > 0. If not, use Dev Tools `GET demo-logging-app-*/_count` to ensure data exists.
- If the index exists but has 0 documents, Filebeat may not be sending. Recheck Filebeat logs and config (as in previous section).
- If documents exist but fields look wrong (e.g., all data under a single `message` field), the JSON parsing might have failed. Verify Filebeat’s JSON config and that your log lines are strictly JSON (our logback config should produce well-formed JSON lines).
- If you get mapping errors in Elasticsearch (e.g., a field mapping conflict), your template might not have been applied or a field was ingested before template. Check the index’s mapping in Dev Tools to see types. You may need to adjust field types or recreate the index with the correct template.

With data confirmed in Elasticsearch and visible in Kibana, we can move on to creating visualizations and dashboards.

## 5. Log Ingestion and Processing – Pipelines, Filters, and Enrichment

We have set up basic ingestion where Filebeat forwards logs to Elasticsearch, and an optional ingest pipeline to tweak fields. In more complex scenarios, you might need additional processing:

- **Field Extraction (Parsing):** If you were not logging in JSON, you’d rely on parsing raw log lines. For example, using a Logstash pipeline or an Elasticsearch ingest pipeline with a Grok processor to extract fields (timestamp, level, etc.) from a log message. Since we chose to log JSON at the source, we avoided this step – which is a key **design decision**: structuring logs at the application level simplifies downstream processing ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20is%20considered%20one%20of,the%20part%20performed%20by%20Logstash)). If structured logging wasn’t possible, Filebeat alone “cannot transform the logs into easy-to-analyze structured data” ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20is%20considered%20one%20of,the%20part%20performed%20by%20Logstash)); you’d then ship to Logstash for grok or use ingest pipelines heavily.

- **Metadata Enrichment:** Filebeat can add useful metadata. For example, you can add cloud instance info by enabling the `add_cloud_metadata` processor (which automatically detects if running on AWS, GCP, Azure and adds fields like instance ID, region). Similarly, `add_host_metadata` can record the host name, and `add_docker_metadata` or `kubernetes` autodiscover can tag container or pod info if running in such environments ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%E2%80%99s%20container)). To use these, in `filebeat.yml` under `processors:` section, add for example:

  ```yaml
  processors:
    - add_cloud_metadata: ~
    - add_host_metadata: ~
    - add_fields:
        target: ""
        fields:
          environment: "production"
  ```

  This would enrich every event with cloud and host fields (if applicable) and a custom `environment: production` field. Enriched data allows more granular Kibana filtering (e.g., filter logs by `cloud.instance.id` or environment).

- **Ingest Node Processing:** We already demonstrated a simple ingest pipeline. You can get very sophisticated here. For instance, you could use a **Grok** processor in the ingest pipeline to parse the `message` field if it contains structured content (ours doesn’t need it). Or use a **Script** processor to compute custom values. If your logs contain an error code or user ID, you could do a lookup (with the Enrich processor, which references a lookup index) to add descriptions or user details. These are advanced and outside the scope of this tutorial, but know that ingest pipelines (or Logstash pipelines) offer flexibility to **clean and augment logs** as they flow in ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=supports%20SSL%20%26%20TLS%20encryption%2C,the%20part%20performed%20by%20Logstash)).

- **Pipeline vs. Filebeat Processing:** A note on where to do processing: Filebeat has some processing capability (via the `processors` in filebeat.yml and its decoding options), but complex transformations (regex parsing, external lookups) are typically done in Elasticsearch ingest or Logstash. Using ingest pipelines keeps the shipping lightweight (Filebeat just ships) and offloads work to Elasticsearch nodes. This is fine for moderate volumes, but for very high volume or complex parsing, a dedicated Logstash or stream processor might be preferred so as not to burden Elasticsearch. Our scenario is straightforward, so Filebeat + ingest node is sufficient.

**Handling High Volume and Large Events:** If your Spring Boot app produces a high volume of logs or very large log entries, consider tuning Filebeat and Elasticsearch:

- Increase Filebeat’s `bulk_max_size` (batch of events sent) and Elasticsearch output workers to increase throughput (but monitor ES performance).
- For extremely large single log events (e.g., huge stack traces), note that Filebeat has a default `max_bytes` (10MB) for a log line ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=The%20default%20is%2016384)) – events larger than that will be truncated. You can raise this in filebeat config if needed, or consider breaking such logs.
- Use compression on the Filebeat output (enabled by default) to reduce bandwidth usage.

**Error Handling:** If Elasticsearch is down or unreachable, Filebeat will retry (with backoff). Thanks to its at-least-once delivery and tracking of file offsets, it will catch up once Elasticsearch is available, without duplicating logs ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%20won%E2%80%99t%20let%20you%20overload,your%20pipeline)). Ensure you have adequate disk space on the source in case of prolonged outages (logs will accumulate). You can also configure a disk spool for Filebeat in newer versions as a buffer.

At this point, our logs are being ingested properly and enriched as needed. We can focus on using Kibana to analyze this data.

## 6. Kibana Dashboards – Visualization, Analytics, and Alerts

With logs indexed in Elasticsearch, Kibana becomes a powerful interface to query and visualize them. We’ll create a basic logging dashboard and set up an alert to illustrate capabilities.

**Exploring Logs in Discover:** We already used Kibana’s **Discover** to verify logs. Discover allows ad-hoc queries and quick analysis (you can filter by fields, test search queries, and view individual log events in JSON detail). For example, try filtering for a specific logger or message text to ensure those fields are searchable. This is great for troubleshooting specific incidents (like searching all ERROR logs in the last 1 hour, or all logs for `userId:123`).

**Creating Visualizations:** For more continuous monitoring, build visualizations:

1. **Log Level Distribution:** Create a pie chart or bar chart to show the proportion of log levels (INFO, WARN, ERROR, etc.) over a time range. In Kibana:

   - Go to **Visualize Library** (or **Dashboard > Create Visualization** in newer Kibana).
   - Choose a **Pie Chart** (or **Donut**). Select the index pattern “demo-logging-app-\*”.
   - For the metric, use a **Count** of records. For the slice, choose a **Terms** aggregation on the `level` field (or `log.level` if you mapped it) ([Create a dashboard to visualize application logs in Kibana - DEV Community](https://dev.to/moesmp/create-a-dashboard-to-visualize-application-logs-in-kibana-2h5h#:~:text=match%20at%20L216%20,and%20then)). You might need to use the keyword field of level, depending on mapping (in our template, `level` is keyword already).
   - You’ll get a pie chart of log counts by level (e.g., 80% INFO, 15% WARN, 5% ERROR). Save this visualization as "Log Level Distribution".

2. **Log Volume Over Time:** Create a line chart to show log count over time (to spot traffic spikes or error spikes):

   - Choose **Line Chart** (or the newer **Lens** visualization for a quick approach).
   - X-axis: date histogram on `@timestamp`. Y-axis: count of logs.
   - (Optional) Split lines by level: add a series or use Lens to break down by `level` field, so each log level is a line on the chart.
   - This shows how many logs per minute/hour are coming in, and you can observe patterns or anomalies (e.g., a sudden surge in ERROR logs). Save as "Logs Over Time".

3. **Top Loggers or Services:** If your application has multiple modules (identified by `logger_name` or maybe you use `spring.application.name` if multiple apps in one index), you can visualize top log sources. For example:

   - Create a **Data Table** viz. Bucket: Terms on `logger_name` (top 10). Metric: Count.
   - This might show which classes or components are logging the most (could indicate noisy components or where most of the activity is).
   - Save as "Top Loggers".

4. **Saved Search for Errors:** In Discover, you can search for `level: "ERROR"` and then save that search (e.g., call it "Error Logs Last 24h"). You can embed this saved search in a dashboard to always have the latest error log list visible.

**Building the Dashboard:** Go to **Dashboard** and create a new dashboard. Add the visualizations we saved: the pie (log level distribution), line chart (log volume), table (top loggers), and perhaps the saved search of error logs. Arrange them as desired. This dashboard provides an at-a-glance view of the logging activity:

- You can immediately see if error logs are occurring (and their proportion).
- Spot trends over time (spikes might correlate with incidents or load).
- Identify which part of the app is most active or problematic.

**Adding Kibana Alerts:** Kibana Alerting (if enabled; basic license allows some alerting features via the Kibana alerting framework) can create rules based on index data. For example, set up an alert: “If more than 5 ERROR logs occur within 1 minute, trigger an alert”. To do this:

- Go to **Alerts and Inspections** (or **Stack Management > Alerts**).
- Create a rule of type **Index Query** (or **Log Threshold** if using Observability features). Point it to the index pattern and set a condition like `level: "ERROR"` and frequency.
- Actions: you can hook up email, Slack, or other connectors to notify when the condition is met.

Alternatively, use Watcher (in Elastic Stack) if you have a license, or a custom script to query periodically. But Kibana’s alerting UI is straightforward for basic needs.

**Testing the Setup:** Induce some logs to see things in action. For instance, call an endpoint of your app to generate a few INFO logs, then trigger an error (perhaps a specific request that throws an exception). Watch the Filebeat logs (it should pick up the new lines immediately) and then see them appear in Kibana (Discover). The visualizations on the dashboard should update on refresh, showing the new error count.

**Troubleshooting Kibana & Visualization:**

- If Kibana doesn’t show fields in the index pattern, click the refresh fields button in the index pattern management (sometimes needed when new fields appear).
- If visualizations show no data, check the time filter in the dashboard (upper right). Set it to a range that covers your data (e.g., "Last 15 minutes" or a specific range).
- If an index pattern wasn’t created, Kibana’s Discover might say “no data view”. Ensure you did the index pattern step after data was indexed.
- Performance: For very large data sets, using Kibana lens or aggregations on text fields can be slow. Ensure fields used in aggregations are keywords (in our mapping, they are). If you have tons of logs, consider enabling [Kibana data compression or sampling] or focusing visualizations on shorter time slices by default.

By now, we have a functional dashboard and alert. Team members can use this to monitor the application’s logs in real time. Next, we’ll discuss how to deploy this stack and monitor it in different environments.

## 7. Deployment and Monitoring – From Local to Production

Deploying the Spring Boot + Filebeat + ELK stack in production requires planning for scalability, security, and reliability. Here are strategies for various environments:

**Local/Development Environment:** Locally, as we did, you might run everything on one machine or docker-compose. This is fine for dev/testing. In a real deployment:

- **Production Spring Boot App:** Package your Spring Boot app as a jar or container. In either case, ensure the logging profile `json-logs` is active in the prod environment (via `SPRING_PROFILES_ACTIVE`). If using containers (Docker/Kubernetes), you might choose to log to STDOUT instead of a file – in which case Filebeat (or another collector) would harvest the container logs. Our tutorial assumes file logging; adjust accordingly if using console logging (Filebeat can tail Docker JSON log files or you could use Elastic’s Filebeat Autodiscover for Kubernetes).
- **Filebeat Deployment:** Filebeat should run wherever the logs are. On VMs, you install it on each VM where the app runs (as an agent). On Kubernetes, the common approach is to run Filebeat as a **DaemonSet** – one per node, tailing logs of all pods. Elastic provides Kubernetes manifests for Filebeat that use autodiscover to track container logs and add Kubernetes metadata (pod name, labels) to each log event ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%E2%80%99s%20container)). This is highly useful in microservices environments, as you can filter logs by service or pod in Kibana easily. In our case of a single app, a DaemonSet with filters for that namespace might be used.
- **Elasticsearch and Kibana:** For production, deploy Elasticsearch in a resilient configuration. This could be:
  - Managed service: **Elastic Cloud** (or Elasticsearch Service on AWS/Azure) which provides Elasticsearch and Kibana as a service. You’d just point Filebeat to the cloud endpoint (using `cloud.id` and `cloud.auth` settings, which simplify connecting Beats to Elastic Cloud).
  - Self-hosted: A cluster of Elasticsearch nodes (at least 2-3 for HA). Ensure to tune JVM heap, set up monitoring, and snapshots for backup. Kibana can be run as a deployment (only one instance needed typically).
  - AWS OpenSearch: AWS’s managed Elasticsearch (OpenSearch) can be used; Filebeat config would point to the domain endpoint. Be aware of differences in version or certain features like alerting if you use OpenSearch Dashboards instead of Kibana.
  - On Kubernetes: You can use the Elastic Cloud on Kubernetes (ECK) operator to deploy Elasticsearch and Kibana inside the cluster, or use Helm charts. Ensure persistent storage for Elasticsearch data and adequate resource requests.

**Security Considerations:** In production, secure the stack:

- Use TLS encryption for shipping logs (Filebeat to Elasticsearch). Elasticsearch can be configured with HTTPS; then set Filebeat `output.elasticsearch.ssl.certificate_authorities` etc. to trust the cert. If using Elastic Cloud, this is handled for you (just use the cloud ID and auth).
- Enable authentication – use a specific Elasticsearch user for Filebeat (with roles `ingest_admin` and `index_write` privileges on the target index). Do not use the superuser in production.
- Lock down access to Kibana with proper user roles. For example, a “dev” role that can read the log indices and create dashboards, but not modify ingest pipelines.

**Monitoring the Pipeline:** Monitor each component:

- **Filebeat Monitoring:** Filebeat can be configured to output its own metrics and logs. Elastic’s Stack Monitoring (X-Pack Monitoring) can collect Beats metrics. You could also track Filebeat’s log for harvester issues. Ensuring Filebeat is running on all instances (perhaps via a configuration management or as part of the container spec) is important. In Kubernetes, the DaemonSet approach helps ensure it runs everywhere and respawns if crashed.
- **Elasticsearch Monitoring:** Use Kibana’s **Stack Monitoring** to watch ES cluster health, index indexing rate, search rate, JVM usage, etc. Set up alerts for node down or high heap usage if possible. Also monitor index sizes – logs can grow quickly, so implement Index Lifecycle Management (ILM) to delete or archive old indices. For example, you might delete logs older than 30 days or rollover to lower-cost storage.
- **Kibana/Uptime:** Ensure Kibana is up and reachable for the team. In critical setups, multiple Kibana instances behind a load balancer can be run (Kibana itself is stateless for reads).

**Optimizing Performance:**

- Tune index refresh interval for log indices to balance real-time search vs throughput. If you don’t need second-by-second visibility, increasing `refresh_interval` to 30s or 60s can improve bulk indexing performance.
- Use ILM to rollover indices daily or when they reach a certain size (like 50GB). This prevents any single index from becoming too large to search efficiently. Our daily index approach is a simple form of this.
- If log volume is extremely high (many gigabytes per day), consider a message queue (like Kafka) and Logstash to buffer spikes. Filebeat can send to Kafka, and Logstash pulls from Kafka to ES. This decouples ingestion from indexing so that bursts don’t overwhelm Elasticsearch.
- Scale Elasticsearch horizontally (more nodes, or using hot-warm architecture: hot nodes for recent data, warm nodes for older read-heavy data). Use index lifecycle to move indices to warm nodes after a period.
- Consider using data streams (if using Elasticsearch 7.9+ and ILM) which simplifies rollover. Beats can be configured to use data streams and ILM.

**Cloud-Specific Notes:**

- **AWS:** If deploying on EC2, you might use CloudFormation or Terraform to set up EC2 for the app and Filebeat, and an Amazon OpenSearch cluster. Ensure the network allows Filebeat to send data (security groups, VPC endpoints if needed). Amazon’s service might use IAM for access; Filebeat doesn’t natively sign AWS IAM requests, so typically you use OpenSearch’s basic auth or an intermediate Logstash. Alternatively, you can use Amazon Kinesis Firehose to ship logs to OpenSearch, but that requires a different agent or integration.
- **Azure:** Azure has an offering via Azure Marketplace for Elastic (which essentially is Elastic Cloud under the hood). You could also self-manage on Azure VMs or AKS. Azure Monitor is another route (sending logs to Log Analytics workspace), but if sticking to ELK, treat it similarly to AWS – deploy VMs or containers, ensure networking and perhaps use Azure Files or Disks for storage in k8s.
- **Kubernetes (EFK):** In containerized deployments, one advantage of Filebeat (or Fluentd) is you can aggregate logs from all app pods easily. Label your pods with app identifiers so the log shipper can tag logs accordingly. For Spring Boot on k8s, often one might use **Fluentd** as shown in many EFK setups, but Filebeat is equally capable and often more efficient. Elastic provides an official Filebeat chart/manifest for k8s which you can adapt (it uses autodiscover providers to get pod labels, etc.).

Finally, **test your logging pipeline under load**. Generate a high volume of logs (maybe use a script to call an endpoint in a loop) to see how the system holds up. Check for any lag (Filebeat should keep up; if not, it will log warnings). Check Elasticsearch indexing rate and ensure no errors.

**Maintenance:** Rotate encryption certificates, update Filebeat and Elastic Stack versions periodically (keeping them in sync). Have a process for updating index templates when your log structure changes (for example, if you add new fields via logging). Keep an eye on the disk usage of logs in Elasticsearch; set up Curator or ILM to delete old ones to prevent running out of disk.

---

By following this guide, you have a full end-to-end logging solution: a Spring Boot application emitting **structured JSON logs**, shipped by **Filebeat** to **Elasticsearch**, and visualized in **Kibana**. This setup will greatly aid in monitoring applications, debugging issues through centralized logs, and alerting on error conditions in real time. With the fundamentals in place, you can extend it with features like tracing correlation, metrics (using Metricbeat or Prometheus), and even APM for a comprehensive observability stack. Happy logging!

**Sources:**

1. Orlando L. Otero – _Configuring JSON-Formatted Logs in Spring Boot_ ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=This%20blog%20post%20helps%20you,be%20fed%20to%20Log%20Aggregators)) ([Configuring JSON-Formatted Logs in Spring Boot applications with Slf4j, Logback and Logstash](https://tech.asimio.net/2023/08/01/Formatting-JSON-Logs-in-Spring-Boot-2-applications-with-Slf4j-Logback-and-Logstash.html#:~:text=%3Cdependency%3E%20%3CgroupId%3Enet.logstash.logback%3C%2FgroupId%3E%20%3CartifactId%3Elogstash))
2. John Thompson – _JSON Logging with Spring Boot (SpringFramework.guru)_ ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=%3Cformat%3E%20%3Clabel%3E%20%3Cpattern%3Eapp%3D%24%7BappName%7D%2Chost%3D%24%7BHOSTNAME%7D%2CtraceID%3D%25X%7BtraceId%3A,sortByTime)) ([JSON Logging with Spring Boot Made Easy - Spring Framework Guru](https://springframework.guru/json-logging-with-spring-boot/#:~:text=%3Cappender,configuration))
3. Logz.io – _Shipping Multiline Logs with Filebeat_ ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=multiline.pattern%3A%20%27,after)) ([Shipping Multiline Logs with Filebeat | Logz.io](https://logz.io/blog/shipping-multiline-logs-with-filebeat/#:~:text=,does%20not%20match%20the%20pattern))
4. Elastic Filebeat Reference – _JSON and Multiline settings_ ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=,dot%20keys%20in%20the)) ([Log input | Filebeat Reference [8.17] | Elastic](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html#:~:text=,removed%20from%20the%20original%20json))
5. Auth0 Engineering – _Spring Boot Logs Aggregation with ELK_ ([Spring Boot Logs Aggregation and Monitoring Using ELK Stack](https://auth0.com/blog/spring-boot-logs-aggregation-and-monitoring-using-elk-stack/#:~:text=Filebeat%20is%20considered%20one%20of,the%20part%20performed%20by%20Logstash))
6. Elastic Filebeat Official Docs – _Filebeat and Backpressure_ ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%20won%E2%80%99t%20let%20you%20overload,your%20pipeline)), _Cloud and Container Monitoring_ ([Filebeat: Lightweight Log Analysis & Elasticsearch | Elastic](https://www.elastic.co/beats/filebeat#:~:text=It%E2%80%99s%20container))
7. Kibana User Guide – _Creating Index Patterns_ ([Create an index pattern | Kibana Guide [7.17] | Elastic](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html#:~:text=1,Click%20Create%20index%20pattern))
