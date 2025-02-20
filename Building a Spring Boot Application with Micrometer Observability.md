# Building a Spring Boot Application with Micrometer Observability – A Step-by-Step Guide

## 1. Introduction to Observability

Observability is **the ability to understand the internal state of a system by examining its external outputs** ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=What%20is%20observability%3F%20In%20our,of%20Enlightning%20with%20Jonatan%20Ivanov)). In modern distributed applications, _observability_ is crucial for monitoring and debugging complex systems. Rather than “flying blind” in production, developers rely on observability data to quickly diagnose issues and ensure reliability ([Structured logging in Spring Boot 3.4](https://spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4#:~:text=Logging%20is%20a%20long%20established,readable%20format)). The concept originates from control theory, but in software it boils down to collecting and analyzing telemetry data from applications.

**Key Pillars of Observability** – often referred to as the three pillars – are **Metrics**, **Logs**, and **Traces**:

- **Metrics** – _Quantitative measures_ that provide a high-level view of system health. Metrics are aggregated numeric data points with timestamps (e.g. CPU usage, request count, average latency) ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Metrics)). They are cheap to store and easy to query, making them ideal for real-time monitoring and alerting. Metrics help identify trends or anomalies (spikes in latency, error rates, etc.) and are crucial for understanding the overall performance of services ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Due%20to%20the%20aggregated%20nature,for%20finding%20anomalies%20and%20patterns)). However, because metrics aggregate information, they lack granular context (no details about individual events) and can explode in volume if too many unique dimensions (labels/tags) are used ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=,insights%20via%20anomalies%20and%20patterns)).

- **Logs** – _Detailed event records_ that capture what the system is doing at specific moments. Logs are unstructured or semi-structured text entries (for example, error stack traces or debug messages) that developers use for deep debugging ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Logs)) ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Different%20languages%2C%20frameworks%2C%20and%20tools,Papertrail%20provide%20solutions%20for%20logging)). They are highly descriptive and can pinpoint exact issues (e.g. an exception with a specific error message) ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Different%20languages%2C%20frameworks%2C%20and%20tools,Papertrail%20provide%20solutions%20for%20logging)). Logs are the easiest telemetry to produce (even a simple `println` is a log), but they can be voluminous and hard to manage. They often require parsing or searching to find relevant information (“only extract insights if you know what to search for” ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=,to%20external%20events%20as%20well))). In a distributed environment, log aggregation tools (like ELK stack or cloud logging services) are used to collect and index logs. Structured logging (formatting logs as JSON or other consistent schemas) can greatly enhance their usefulness by making them machine-readable for analysis.

- **Traces** – _Distributed traces_ track the lifecycle of a request or transaction as it propagates through multiple services and components. A trace is composed of **spans**, each representing a unit of work (such as a single service handling part of the request) ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=Trace%20data%20is%20made%20up,be%20represented%20by%20a%20span)). By assigning a unique **trace ID** to each request and propagating it through service calls, we can reconstruct the path of that request across the system ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=A%20trace%20is%20the%20complete,is%20also%20called%20Distributed%20Tracing)). Traces provide causality and timing information – they show relationships between operations and how long each step took. This makes them invaluable for diagnosing performance bottlenecks and pinpointing where failures occur in a workflow. Implementing tracing typically involves instrumentation that propagates context (e.g. using standards like W3C Trace Context) across service boundaries. While traces are extremely powerful for debugging distributed systems, they can be more complex to implement and may introduce some overhead, so sampling is often used to collect only a representative subset of requests.

These three pillars **work together** to give a complete picture. Metrics might alert you that a problem exists (e.g. error rate spiked), logs can provide details about the error, and traces can show the path leading to the error across services ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=What%20is%20observability%3F%20In%20our,of%20Enlightning%20with%20Jonatan%20Ivanov)). In a robust observability strategy, **metrics, logs, and traces are interlinked** – for example, a trace ID in logs allows correlating log statements to a specific distributed trace, and metrics can be broken down by trace or span attributes to analyze performance per route or user. Effective observability enables faster **root cause analysis** and more confidence in managing complex, distributed applications.

Modern cloud architectures (like microservices on Kubernetes) make observability even more critical: with many moving parts, only through strong observability can DevOps teams measure system health, detect anomalies, and troubleshoot incidents in production ([A Complete Guide to Kubernetes Observability | Last9](https://last9.io/blog/a-complete-guide-to-kubernetes-observability/#:~:text=But%20what%20exactly%20is%20observability,as%20metrics%2C%20logs%2C%20and%20traces)) ([A Complete Guide to Kubernetes Observability | Last9](https://last9.io/blog/a-complete-guide-to-kubernetes-observability/#:~:text=At%20its%20core%2C%20Kubernetes%20observability,points%3A%20metrics%2C%20logs%2C%20and%20tracing)). In summary, observability is not just about gathering data, but about using that data (metrics, logs, traces) to gain insight into your system’s behavior and performance.

## 2. Spring Boot & Micrometer Overview

Spring Boot is a popular framework for building Java microservices, and it includes built-in support for observability through its **Actuator** module and integration with **Micrometer**. Micrometer, on the other hand, is a **vendor-neutral observability façade** for the JVM – think of it as the SLF4J of metrics/observability ([Micrometer Application Observability](https://micrometer.io/#:~:text=Vendor)). In this chapter, we’ll do a deep dive into how Spring Boot and Micrometer work together to implement observability (focusing on metrics and tracing), and what Micrometer Observability means in practice.

### 2.1 What is Micrometer Observability?

**Micrometer** provides a uniform API to instrument your code for metrics and other observability data **without locking into a specific monitoring system** ([Micrometer Application Observability](https://micrometer.io/#:~:text=Vendor)). With Micrometer, you write instrumentation (counters, timers, etc.) in your code, and later decide which monitoring system (Prometheus, Graphite, Datadog, etc.) to attach – Micrometer will handle publishing to those systems via _Meter Registry_ implementations. This decoupling allows you to switch or integrate multiple backends easily. Key points about Micrometer:

- It supports multiple **meter types** out-of-the-box: counters, gauges, timers, distribution summaries, long task timers, etc., using a dimensional data model (each metric can have tags for dimensions like endpoint, status, etc.) ([Micrometer Application Observability](https://micrometer.io/#:~:text=Dimensional%20Metrics)).
- It has **built-in instrumentation** for many common Java frameworks and components. Spring Boot Actuator auto-configures a lot of metrics for you (JVM memory, GC, CPU, Tomcat connection pool, Spring MVC, etc.), so you get those metrics with zero code ([Micrometer Application Observability](https://micrometer.io/#:~:text=Instrumentation%20Provided)).
- It can publish to a wide range of **monitoring systems** by configuring the appropriate registry (Prometheus, Graphite, New Relic, Datadog, CloudWatch, Elastic, etc.) ([Micrometer Application Observability](https://micrometer.io/#:~:text=Micrometer%20supports%20publishing%20metrics%20to,Google%20Stackdriver%2C%20StatsD%2C%20and%20Wavefront)). This means your metrics can be sent or exposed in the format needed by those systems.

Starting with Spring Boot 3 (and Micrometer 1.10+), Micrometer expanded beyond metrics into a broader observability role. This is often referred to as **Micrometer Observability**, which encompasses metrics, distributed tracing, and log correlation under one API. The Micrometer team introduced the **Observation API**, a new abstraction to capture an “observation” in your code that can produce metrics _and_ traces simultaneously ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=We%20have%20been%20changing%20the,new%20API%3A%20the%20Observation%20API)). The goal is to **“instrument once, benefit in multiple ways”** – you mark an operation with an Observation, and Micrometer can emit a metric for its duration, create a tracing span, and even attach contextual info to logs for that operation ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=API)) ([Micrometer Application Observability](https://micrometer.io/#:~:text=Unified%20Observability)).

**Micrometer Tracing** is the component that bridges Micrometer’s Observation API to underlying tracing systems. It acts as a façade over popular tracer libraries (like OpenTelemetry or Brave), allowing you to switch implementations similarly to how Micrometer metrics is decoupled from the backend ([Micrometer Application Observability](https://micrometer.io/#:~:text=Distributed%20Tracing)). In fact, Micrometer Tracing is the successor to the earlier Spring Cloud Sleuth project ([Micrometer Application Observability](https://micrometer.io/#:~:text=Micrometer%20Tracing%20is%20a%20facade,the%20Spring%20Cloud%20Sleuth%20project)). Spring Boot 3’s observability support builds on this: it can automatically configure Micrometer Tracing if the appropriate dependencies are on the classpath.

In summary, **Micrometer Observability** in Spring Boot means you have a unified approach to metrics and traces:

- **Metrics**: Use Micrometer’s Meter API or Spring Boot Actuator’s auto-metrics. These feed into Micrometer’s registries for various backends (like Prometheus).
- **Tracing**: Use Micrometer Observation/Tracing to generate traces. Under the hood, this can use OpenTelemetry or Brave to record spans and propagate context.
- **Log Correlation**: Spring Boot 3+ automatically ties trace context into SLF4J’s Mapped Diagnostic Context (MDC). This means log statements can include the trace and span IDs, so you can correlate logs with traces easily ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=new%20distributed%20tracing%20support%20with,helps%20to%20label%20the%20observations)).

Spring Boot provides **auto-configuration** for all of this. By including the right starters and dependencies, much of the setup is done for you. For example, adding Spring Boot Actuator pulls in Micrometer for metrics. If you then add `micrometer-registry-prometheus`, Spring Boot will expose a `/actuator/prometheus` endpoint for Prometheus to scrape ([Java: Adding custom metrics to Spring Boot Micrometer Prometheus endpoint | Fabian Lee : Software Engineer](https://fabianlee.org/2022/06/29/java-adding-custom-metrics-to-spring-boot-micrometer-prometheus-endpoint/#:~:text=,garbage%20collection%2C%20disk%2C%20and%20memory)) ([Java: Adding custom metrics to Spring Boot Micrometer Prometheus endpoint | Fabian Lee : Software Engineer](https://fabianlee.org/2022/06/29/java-adding-custom-metrics-to-spring-boot-micrometer-prometheus-endpoint/#:~:text=To%20enable%20the%20%E2%80%98%2Factuator%2Fprometheus%E2%80%99%20endpoint%2C,gradle)). If you add the Micrometer Tracing bridge and an OpenTelemetry exporter, Spring will set up tracing instrumentation and send spans to your trace backend. We’ll explore these in detail in upcoming sections.

### 2.2 Spring Boot and Observability Integration

Spring Boot has long had a focus on production readiness via Actuator. Actuator exposes endpoints for health checks, info, and metrics. Under the hood in Spring Boot 2.x, metrics were powered by Micrometer. In Spring Boot 3.x, this continues and is enhanced with tracing:

- **Spring Boot Actuator**: By including `spring-boot-starter-actuator`, you automatically get Micrometer-Core on the classpath (for metrics) and a set of auto-configured metrics. Actuator’s `/actuator/metrics` endpoint (and specific endpoints like `/metrics/jvm.memory.used`) become available. If a specific registry is present (e.g. Prometheus), it also enables an endpoint or integration for that.
- **Enabling Metrics**: Aside from the built-in metrics, you can create your own. Actuator and Micrometer expose a `MeterRegistry` bean that you can inject and use to register custom metrics. We will demonstrate how to create custom counters, gauges, and timers in **Chapter 4**.
- **Enabling Tracing**: Spring Boot 3 doesn’t include a tracer by default (to avoid forcing one on you), but it’s ready to configure one. By adding the **Micrometer Tracing bridge** along with a tracer implementation, you enable automatic tracing:

  - You choose a **tracer implementation**: For example, **OpenTelemetry** (OTel) or **Brave** (Zipkin). Micrometer provides bridge libraries for both (e.g. `micrometer-tracing-bridge-otel` or `micrometer-tracing-bridge-brave`).
  - You also add an **exporter** to send traces to a backend. For instance, to send traces in OpenTelemetry format (OTLP) to a collector or directly to Jaeger/Zipkin, you might use `opentelemetry-exporter-otlp` or a Zipkin/Jaeger specific exporter.
  - Once on the classpath, Spring Boot auto-configures instrumentation: incoming HTTP requests, RestTemplate calls, JDBC queries, etc., can all be auto-instrumented to produce spans. We’ll cover the specifics in **Chapter 5**.

- **Log Correlation**: With tracing enabled, Spring Boot will attach the trace and span IDs to the logging context. By default, it uses **W3C Trace Context** (which uses a `traceparent` header) for propagation ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=new%20distributed%20tracing%20support%20with,helps%20to%20label%20the%20observations)). The trace and span IDs are also put into SLF4J MDC under keys like `traceId` and `spanId`. You can then configure your log pattern to include these, so every log line will show the IDs. This is immensely helpful when combing through logs – you can filter by a specific traceId to see all logs for that request. We’ll see how to configure this in **Chapter 6**.

In short, Spring Boot + Micrometer gives you a **comprehensive observability toolkit**:

- **Micrometer** abstracts the metrics & tracing APIs.
- **Spring Boot Autoconfiguration** wires Micrometer into the framework (HTTP, database, etc.) and exposes data via Actuator.
- **Third-party Integrations** (Prometheus, Grafana, Jaeger, Zipkin, etc.) can be plugged in with minimal configuration to collect and visualize the data.

With this overview in mind, let’s start building our application and gradually add observability features.

## 3. Setting Up the Project

In this chapter, we’ll set up a Spring Boot project from scratch, including all necessary dependencies and basic configuration for Micrometer, metrics, and tracing. By the end of this setup, we will have a runnable Spring Boot application with Actuator, Micrometer metrics exposure, and tracing capabilities ready to be configured.

### 3.1 Project Initialization

**Step 1: Bootstrap the Spring Boot application.** You can use [Spring Initializr](https://start.spring.io) to generate a new project, or set up a Maven/Gradle project manually:

- **Spring Boot Version**: Use Spring Boot 3.x (the latest stable release) to get the newest observability features.
- **Dependencies**: Include at minimum:
  - **Spring Web** (to build a REST API we can observe).
  - **Spring Boot Actuator** (to enable metrics and health endpoints).
  - **Micrometer Registry for Prometheus** (if using Prometheus for metrics; this is `io.micrometer:micrometer-registry-prometheus`).
  - **Micrometer Tracing (Bridge)** and a tracing exporter. For example, to use OpenTelemetry and Zipkin:
    - `io.micrometer:micrometer-tracing-bridge-otel` (Micrometer Tracing bridge with OpenTelemetry).
    - `io.opentelemetry:opentelemetry-exporter-zipkin` (to send traces to Zipkin; for Jaeger, you could use `opentelemetry-exporter-jaeger`) ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=,otel)) ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=,zipkin%60%20dependency)).
  - **Logging Appender (Optional)**: If you plan to ship logs to an aggregator like Loki or Elastic, you might include a logging appender dependency (e.g. Loki’s Logback appender as shown later). This is optional for our initial setup.

If using Maven, your `pom.xml` should have entries like:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<!-- Micrometer Prometheus registry for metrics exposure -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
    <scope>runtime</scope>  <!-- use runtime scope for registry -->
</dependency>
<!-- Micrometer Tracing bridge for OpenTelemetry -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<!-- OpenTelemetry exporter to Zipkin (for traces) -->
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-zipkin</artifactId>
</dependency>
```

If using Gradle (Groovy DSL), the dependencies in `build.gradle` would look like:

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    // Prometheus registry
    runtimeOnly 'io.micrometer:micrometer-registry-prometheus'
    // Micrometer tracing (OpenTelemetry bridge)
    implementation 'io.micrometer:micrometer-tracing-bridge-otel'
    // OpenTelemetry Zipkin exporter
    implementation 'io.opentelemetry:opentelemetry-exporter-zipkin'
}
```

These include everything we need for basic observability:

- The Actuator starter brings in Micrometer core.
- The Prometheus registry adds the Prometheus endpoint.
- The tracing bridge and exporter enable distributed tracing with OpenTelemetry (we’ll configure them soon).

**Step 2: Basic application structure.** Create a simple Spring Boot application. For example, a main class annotated with `@SpringBootApplication` and a simple REST controller. This will be the code we instrument and observe.

```java
@SpringBootApplication
public class DemoObservabilityApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoObservabilityApplication.class, args);
    }
}
```

And perhaps a sample REST controller to have some activity to monitor:

```java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        // A simple endpoint we will monitor
        return "Hello, Observability!";
    }
}
```

For now, this just returns a static message. We will enhance this later with some custom metrics and simulated processing to observe latency.

### 3.2 Configuration for Observability

With dependencies on the classpath, Spring Boot Actuator and Micrometer will be auto-configured, but we need to tweak some settings in `application.properties` (or YAML) to enable full observability features:

1. **Expose necessary Actuator endpoints:** By default, in Spring Boot 3, only a few endpoints like `/health` and `/info` might be exposed. We want to expose metrics (and possibly the Prometheus scrape endpoint) and tracing if needed. Add the following to `src/main/resources/application.properties`:

   ```properties
   management.endpoints.web.exposure.include=health,info,prometheus
   management.endpoint.health.show-details=always
   ```

   This ensures the health endpoint shows details and the Prometheus endpoint (`/actuator/prometheus`) is exposed over HTTP. The Prometheus endpoint will serve all metrics in Prometheus plaintext format ([Java: Adding custom metrics to Spring Boot Micrometer Prometheus endpoint | Fabian Lee : Software Engineer](https://fabianlee.org/2022/06/29/java-adding-custom-metrics-to-spring-boot-micrometer-prometheus-endpoint/#:~:text=,garbage%20collection%2C%20disk%2C%20and%20memory)).

2. **Application Name (for tracing):** It’s useful to name your service for trace data. Many observability systems use the service name. Set your application name in properties:

   ```properties
   spring.application.name=demo-observability
   ```

   This name will be used in metrics (as a tag `application`) and in traces (as the service name for spans).

3. **Tracing configuration:** Spring Boot with Micrometer Tracing will, by default, sample 100% of requests for tracing (since we added the OpenTelemetry dependencies). In production, you might want to adjust sampling to reduce overhead. For demonstration, we’ll keep sample at 100%. (You can explicitly set `management.tracing.sampling.probability=1.0` to ensure all traces are captured, or set a value less than 1.0 to sample accordingly ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=,include%3Dprometheus)).)

   Additionally, Micrometer will propagate the trace context. By default it uses W3C Trace Context. You typically don’t need to configure this, but know that it means if your app calls another service (also instrumented), it will pass along headers like `traceparent`.

4. **Log format for correlation:** To include trace and span IDs in logs, we configure Logback (the default logging framework in Spring Boot). The easiest way:

   - If using Spring Boot 3.2+, you can set a property to update the log pattern. For example:

     ```properties
     logging.pattern.level=[%5p] [${spring.application.name:},%X{traceId:-},%X{spanId:-}]
     ```

     This will prepend each log line’s level with the app name, traceId, and spanId if present (or `-` if not) ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=,X%7BspanId)). The pattern `%X{traceId}` pulls the MDC value for traceId.

     The above is exactly what the Spring team demonstrated – resulting log lines might look like:

     ```
     2025-02-19 15:22:01.234  INFO [demo-observability,4a1f678d93bfb42a,6b3f2d4951f0f3ca] com.example.HelloController : Handling request...
     ```

     Now we can correlate that “INFO” log to a specific trace and span.

   - Alternatively, you can configure a custom `logback-spring.xml` if you need more control. In it, you would use `%X{traceId}` and `%X{spanId}` in your pattern. (We’ll discuss structured logging in **Chapter 6** more.)

5. **(Optional) Logging to external system:** If you plan to send logs to a system like Loki or Elasticsearch, you might add additional config. For Loki (Grafana’s logging system), for instance, you’d add the Loki Logback appender dependency and configure it with a URL. The Spring blog example shows adding `com.github.loki4j:loki-logback-appender` and configuring Logback to push logs to a local Loki server ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=)) ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=%3Cappender%20name%3D,NONE%7D%2Clevel%3D%25level%3C%2Fpattern%3E%20%3C%2Flabel%3E%20%3Cmessage)). This is optional and will be covered in the Logging chapter.

At this point, we have:

- The application set up with required libraries.
- Basic properties configured to expose metrics and include tracing info in logs.

**Build and Run:** Start the application (`mvn spring-boot:run` or via your IDE). You should see in the startup logs that the Actuator endpoints are enabled. If you open a browser or use curl to hit `http://localhost:8080/actuator`, you should see a list of available endpoints including **`prometheus`** and **`metrics`**. For example:

```bash
$ curl http://localhost:8080/actuator | jq .
{
  "_links": {
    "self": {"href": "http://localhost:8080/actuator", "templated": false},
    "health":{"href":"http://localhost:8080/actuator/health","templated":false},
    "info":{"href":"http://localhost:8080/actuator/info","templated":false},
    "metrics":{"href":"http://localhost:8080/actuator/metrics","templated":false},
    "prometheus":{"href":"http://localhost:8080/actuator/prometheus","templated":false}
  }
}
```

(If you don’t see `prometheus`, ensure the dependency and property are set correctly, then restart.)

Visiting `http://localhost:8080/actuator/prometheus` in a browser will show a long list of metrics in plaintext format. These include JVM and system metrics out-of-the-box (e.g. `jvm_memory_used_bytes`, `process_cpu_usage`, `http_server_requests_seconds_count`, etc.). This confirms that Micrometer is gathering metrics and exposing them for Prometheus ([Java: Adding custom metrics to Spring Boot Micrometer Prometheus endpoint | Fabian Lee : Software Engineer](https://fabianlee.org/2022/06/29/java-adding-custom-metrics-to-spring-boot-micrometer-prometheus-endpoint/#:~:text=,garbage%20collection%2C%20disk%2C%20and%20memory)). We’ll dive deeper into what these metrics are and how to add our own in the next chapter.

### 3.3 Verifying the Setup

Before we proceed, let’s verify each observability aspect is working in the baseline setup:

- **Metrics Endpoint**: Check that `http://localhost:8080/actuator/prometheus` returns metrics. You should see entries like:

  ```
  # HELP jvm_memory_used_bytes Used bytes of a given JVM memory area.
  # TYPE jvm_memory_used_bytes gauge
  jvm_memory_used_bytes{area="heap",id="PS Eden Space",} 1.2345678E7
  ...
  http_server_requests_seconds_count{exception="None",method="GET",status="200",uri="/hello",} 1.0
  ```

  The presence of `http_server_requests_seconds_count{... uri="/hello", ...} 1.0` indicates our `/hello` endpoint was called (the counter for requests is 1). These are built-in metrics from Spring MVC instrumentation.

- **Health Check**: `http://localhost:8080/actuator/health` should show an **"UP"** status (and possibly details like disk space, ping, etc., since we enabled show-details).

- **Tracing**: Since we included OpenTelemetry and Zipkin exporter, our app will try to send spans to a Zipkin server on startup. If you don’t have Zipkin running yet, you might see a warning or error in the logs about failing to connect. That’s okay for now. We will set up a tracing backend in Chapter 5. The key is that tracing is active. If you trigger the `/hello` endpoint, you should see log output including a trace ID and span ID. Also, if debugging, you could see that the Micrometer tracer is creating spans (but verifying this might require looking at internal logs or adding a test SpanHandler, which is advanced).

- **Logs with trace IDs**: Observe the console logs when hitting the endpoint:
  ```
  2025-02-19 15:25:00.123  INFO [demo-observability,TRACE_ID,SPAN_ID] o.s.web.servlet.DispatcherServlet : Completed initialization in 10 ms
  2025-02-19 15:25:05.456  INFO [demo-observability,TRACE_ID,SPAN_ID] c.e.HelloController : Handling request...
  ```
  The `TRACE_ID` and `SPAN_ID` should be actual hex values. This confirms our logging pattern is picking up the MDC values for tracing context. If you don’t see them, double-check the `logging.pattern.level` property or Logback config.

Having confirmed the setup, we’re ready to explore each aspect of observability in depth: collecting metrics, managing traces, handling logs, integrating with external tools, and eventually deploying to cloud. In the following chapters, we’ll incrementally build on this foundation.

## 4. Metrics Collection & Management

Metrics are often the starting point for observability because they provide quick insights into the system’s performance and health. In this chapter, we’ll cover how Spring Boot and Micrometer collect metrics, how to create custom metrics for your application, and best practices for managing metrics efficiently.

### 4.1 Built-in Metrics in Spring Boot

Out of the box, **Spring Boot Actuator** (with Micrometer) provides a wealth of metrics without any additional coding. These built-in metrics cover a range of components:

- **JVM Metrics**: Memory usage (`jvm.memory.*`), Garbage collection counts and timings (`jvm.gc.*`), thread counts, class loading, etc.
- **System Metrics**: CPU usage (`process.cpu.usage`), uptime, system load, disk space (as part of health).
- **Log Metrics**: If using Logback, a meter for log events (`logback.events`) by level.
- **Spring MVC / Web Metrics**: HTTP request metrics under `http.server.requests` (for each endpoint, method, status), including count, total time, max time, etc.
- **Database Metrics**: If using a DataSource, you get metrics like connection pool usage.
- **Cache Metrics**: If using a Cache manager, hits/misses.
- **Others**: There are metrics for things like Executor pools, RabbitMQ, Kafka, etc. if those are auto-configured in your app.

You can explore available metrics by hitting the Actuator `/actuator/metrics` endpoint, which will list metric names, or directly query a specific metric, e.g., `/actuator/metrics/jvm.memory.used`. However, since we have the Prometheus endpoint enabled, it’s easier to see everything there.

For example, an **HTTP request metric** as exposed by Prometheus might look like:

```
http_server_requests_seconds_count{exception="None",method="GET",status="200",uri="/hello",} 5.0
http_server_requests_seconds_sum{exception="None",method="GET",status="200",uri="/hello",} 0.123
```

This tells us 5 requests have been handled by the `/hello` endpoint, with a total accumulated time of 0.123 seconds. From this, Prometheus can compute average latency (sum/count) and we can graph rates of requests, etc.

Micrometer generally records **timers** for requests (hence the `_seconds_count` and `_seconds_sum`). It also provides a `_max` for the max observed latency. These metrics have tags such as HTTP method, status, and URI (with templated URI if available). The use of tags means metrics are **dimensional** – you can filter or break down by these tags in queries, which is very powerful.

**Inspecting a few other built-ins:**

- `jvm.memory.used` (gauge) with tags `area` (heap or non-heap) and `id` (e.g. specific memory pool) – showing current memory usage.
- `jvm.gc.memory.allocated` (counter) – how many bytes have been allocated (cumulative) since start, which grows over time (indicates GC churn).
- `logback.events` (counter) with tag `level` – number of log events at each level (INFO, WARN, etc.).
- `process.uptime` (gauge or timer) – how long the JVM has been running.

These default metrics provide a baseline for monitoring without writing any code. They cover common needs: you can track memory usage trends, GC pauses, request performance, etc. in a dashboard or trigger alerts (e.g., alert if heap usage is near max, or if error-rate of HTTP 500s goes above a threshold, since `status="500"` will be tracked).

### 4.2 Creating Custom Metrics

While built-in metrics are great, every application has its own domain-specific metrics that are important (business or application-level metrics). With Micrometer, creating custom metrics is straightforward.

Micrometer’s core interface for metrics is the `MeterRegistry`. Spring Boot will create a `MeterRegistry` bean for you (actually a composite if multiple registries). We can inject this registry into any component (using constructor injection) and use it to create our own meters.

**Common meter types:**

- **Counter** – a monotonically increasing number (e.g., count of something). Use for events you just count (increments). Example: number of orders placed, or how many times a certain event happened. In Micrometer: `Counter counter = Counter.builder("orders.placed").register(meterRegistry); counter.increment();`.
- **Gauge** – holds a value that can go up or down. Often gauges are derived from state. In Micrometer, you often supply a lambda to sample the value when requested. Example: current queue size, or current temperature reading. E.g., `Gauge.builder("queue.size", queue, q -> q.size()).register(meterRegistry);`.
- **Timer** – measures duration of events and keeps count. You record durations to it, and it tracks count, total time, max, and often percentiles/histogram (if configured). Example: time taken to process a job. Use `Timer timer = Timer.builder("job.processing.time").publishPercentileHistogram().register(meterRegistry); timer.record(() -> doJob());`.
- **Distribution Summary** – similar to Timer but for arbitrary values (not time) – e.g. sizes of payloads, or response sizes.
- **LongTaskTimer** – measures duration of long-running tasks (can have a notion of currently active tasks).

Let’s walk through adding a custom metric to our application. Suppose in our example we want to count how many times the `/hello` endpoint has greeted a user, and measure how long the greeting takes (trivially it’s fast now, but imagine it might call another service).

**Step 1: Inject MeterRegistry and define meters.** We can create a @Component bean to configure our custom metrics, or we can define them in the controller. For clarity, we’ll do it in the controller in this simple case:

```java
@RestController
public class HelloController {

    private final Counter helloCounter;
    private final Timer helloTimer;

    // Inject the MeterRegistry via constructor
    public HelloController(MeterRegistry registry) {
        // Define a Counter metric named "hello.requests"
        this.helloCounter = Counter.builder("hello.requests")
                                   .description("Number of hello requests served")
                                   .register(registry);
        // Define a Timer metric named "hello.latency"
        this.helloTimer = Timer.builder("hello.latency")
                               .description("Latency of hello requests")
                               .publishPercentileHistogram()  // enable histogram for percentiles
                               .register(registry);
    }

    @GetMapping("/hello")
    public String hello() {
        // Increment the counter
        helloCounter.increment();
        // Record the time taken by this method using the Timer
        return helloTimer.record(() -> {
            // Simulate some processing or just return the greeting
            try {
                Thread.sleep((long) (Math.random() * 100)); // simulate latency 0-100ms
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello, Observability!";
        });
    }
}
```

In the above code:

- We use `Counter.builder("hello.requests")` to create a counter. We give it a human-readable description. (Micrometer will also automatically tag this with `application=demo-observability` and any other common tags, unless you specify tags here.)
- We use `Timer.builder("hello.latency")` for a timer. We turned on `publishPercentileHistogram()`, which instructs Micrometer to calculate histogram buckets so we can get percentile metrics (e.g., 95th percentile latency) – this is optional but useful for latency metrics.
- In the `hello()` method, every time the endpoint is called, we increment the counter and record the execution time of the lambda we pass to `helloTimer.record()`. The lambda returns the string response. Timer will measure the time taken by the lambda execution.

**Step 2: Verify custom metrics appear.** After running the app and hitting `/hello` a few times, check the Prometheus endpoint output again (or /metrics). Look for `hello_requests_total` (Micrometer will convert the dot notation to `_` and add suffixes like `_total` for counters) and `hello_latency_seconds`. You should see something like:

```
# HELP hello_requests_total Number of hello requests served
# TYPE hello_requests_total counter
hello_requests_total 3.0

# HELP hello_latency_seconds
# TYPE hello_latency_seconds summary
hello_latency_seconds_count 3.0
hello_latency_seconds_sum 0.150
# Quantiles (if percentiles are published, you might also see hello_latency_seconds{quantile="0.5"} etc.)
hello_latency_seconds_max 0.08
```

The exact output format depends on how Micrometer is configured (by default, a Timer appears as a Prometheus summary which provides count, sum, and snapshot quantiles if enabled, plus a separate `_max`). In this case, after 3 calls with some random sleep, we have count=3, sum=0.150s, max ~0.08s (80ms). If the histogram was fully enabled, we’d also see lines for specific percentiles or buckets.

**Custom Tags:** We can also add tags to metrics. For example, maybe we want to tag `hello.requests` by the type of user or some parameter. We could do:

```java
Counter.builder("hello.requests")
       .tag("source", "web")
       .register(registry);
```

to tag this counter with source=web. Then in Prometheus, that metric would have a label `source="web"`. Make sure to keep tag cardinality low (don’t include user IDs or too many distinct values, more on that in Best Practices).

**Alternate way – using @Timed annotation:** Spring Boot / Micrometer also provide annotations like `@Timed` and `@Counted` to auto-create metrics around methods. For example, `@Timed(value = "hello.latency", histogram = true)` on the `hello()` method could automatically create a Timer for its execution time. This requires adding the Micrometer annotation support dependency and enabling it. We won’t detail this approach here, but it’s an option for cross-cutting metrics without manually coding the Timer logic.

### 4.3 Efficient Metrics Management (Best Practices)

Collecting metrics is powerful, but one must be mindful of **performance and manageability**. Here are some best practices and tips for managing metrics:

- **Avoid High Cardinality**: As mentioned earlier, having metrics with too many unique tag values can cause memory and storage issues ([Metrics, Events, Logs, and Traces: Observability Essentials | Last9](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/#:~:text=,insights%20via%20anomalies%20and%20patterns)). For instance, don’t tag metrics with userID or timestamp or other highly variable data. Prefer coarse labeling (e.g., status="SUCCESS"/"FAIL" rather than detailed error codes, unless the set of codes is small and known). A common anti-pattern is tagging with request URLs that include IDs (e.g., `/orders/12345` vs `/orders/{id}` template). Spring’s metrics auto-config does the right thing by using template URIs for HTTP metrics instead of raw URIs. Stick to that strategy for your custom metrics.

- **Use Timer percentiles sparingly**: Enabling percentile histograms on every Timer can be expensive (it keeps additional state for buckets). Only enable it on key metrics where you need percentiles (like request latency, maybe critical business operation durations). For others, just count and total time might suffice.

- **Metric Names and Conventions**: Use a consistent naming scheme. By convention, use `.` as separators in Micrometer metric names (they will translate to `_` in Prometheus). Include units in the name if not obvious (e.g., use `transaction.duration.seconds` or similar, though if using Timer the `_seconds` suffix will be added by Prometheus conversion). Prefix custom metrics with a domain (like `order.service.*` for metrics in the order service) to avoid naming collisions.

- **Aggregation vs Raw Data**: Metrics by nature are aggregated (especially in Prometheus). This means you typically don’t want to create a new metric for each object instance or such. For example, if you have a metric per user, that’s likely too granular. Instead, consider aggregating (like one metric that counts all users, possibly with a tag for user type if needed). Keep the metric dimensions manageable.

- **Scraping Frequency**: Prometheus by default might scrape every 15s or 30s. Very short scrap intervals (e.g., 1s) can increase overhead. Choose a scrape interval that makes sense for your needs. This is configured on Prometheus server side, but keep in mind when designing what resolution you need.

- **Use `MeterFilter` if needed**: Micrometer allows configuring MeterFilters that can, for example, disable certain metrics or rename them. If there are built-in metrics you don’t use, you could filter them out to reduce clutter. For example, you might disable metrics for an unused cache. This is done via configuration (properties or a bean). Not critical unless you identify a need.

- **Push vs Pull**: Micrometer can either expose metrics to be pulled (e.g., Prometheus pulls from the `/prometheus` endpoint) or push metrics to systems (e.g., pushing to Graphite, StatsD, etc.). The pull model with Prometheus is common in cloud native scenarios (since Prom can dynamically discover services). But if using a push system (like StatsD), Micrometer’s registry will periodically push. Ensure you configure the push interval appropriately. For Prometheus, since it’s pull, the registry just waits for scrapes, which is simpler.

- **Validate Metric Data**: In dev/test, it’s good to verify your metrics make sense. Use PromQL or the `/actuator/metrics` endpoint to query a metric and ensure it’s recording expected values (e.g., if you increment a counter on an event, trigger the event and see if it increased). This helps catch any mistakes in instrumentation early.

By collecting both built-in and custom metrics, you set up a **metrics-driven monitoring** for your app. In the next chapter, we will turn to **Distributed Tracing**, which complements metrics by providing request-level visibility across services.

## 5. Distributed Tracing

Distributed tracing is the observability pillar that allows developers to follow a transaction or request as it flows through multiple services, providing a **trace** of the path taken and timing of each component. In microservice architectures, tracing is essential to pinpoint where latency or errors occur across service boundaries. In this chapter, we’ll implement distributed tracing in our Spring Boot application using **OpenTelemetry** (OTel) via Micrometer Tracing, and integrate it with trace backends like Jaeger or Zipkin.

### 5.1 Enabling Distributed Tracing in Spring Boot

We already added the Micrometer Tracing dependency and an OpenTelemetry exporter back in the setup. To recap:

- **Micrometer Tracing Bridge (OpenTelemetry)**: `micrometer-tracing-bridge-otel` – this provides the integration to create OTel spans from Micrometer’s Observation/Tracing API.
- **OTel Exporter (Zipkin)**: `opentelemetry-exporter-zipkin` – this allows sending spans to a Zipkin-compatible endpoint (which could be a Zipkin server or even Jaeger, since Jaeger can also accept Zipkin-formatted traces on a specific port).

With these on the classpath, Spring Boot 3 will auto-configure:

- A `Tracer` bean (from OpenTelemetry).
- It will set up W3C context propagation (so it will propagate the `traceparent` and `tracestate` headers on outgoing calls).
- It instruments HTTP requests (server side) to create a span for each incoming request, named after the handler (or at least the URI template).
- It instruments RestTemplate or WebClient calls (if you use them) to create a child span for external calls.
- It can instrument other things like message listener invocations if using Spring Cloud Streams, etc., but we’ll focus on HTTP.

**Sampling**: By default, if not configured, Micrometer Tracing with OTel likely defaults to always sample (depending on version, it might use a parent-based sampler that continues a trace if incoming or samples new ones at 100%). We set `management.tracing.sampling.probability=1.0` earlier to explicitly sample all. In production, consider lowering that (e.g., 0.1 for 10% of requests) to reduce overhead.

**Running a Trace Backend**: To see traces, we need a system like Jaeger or Zipkin to collect and display them. You can choose either:

- **Zipkin**: Easiest way is to run the Zipkin server locally (e.g., using Docker: `docker run -d -p 9411:9411 openzipkin/zipkin`). Zipkin will listen on port 9411 for spans (HTTP POST in a JSON format).
- **Jaeger**: You can run Jaeger all-in-one (Docker: `docker run -d -p 16686:16686 -p 14268:14268 jaegertracing/all-in-one`). Jaeger’s collector can accept spans in multiple formats. By default, the all-in-one’s collector listens on port 14268 for “Jaeger Thrift” format HTTP. But since we have a Zipkin exporter, we could also configure Jaeger to accept Zipkin format on port 9411 or use OTel gRPC. For simplicity, we’ll proceed with Zipkin server as the target.

**Configuring Export**: Our inclusion of `opentelemetry-exporter-zipkin` should automatically configure exporting to `http://localhost:9411/api/v2/spans` (the default endpoint for Zipkin). If the Zipkin server is not running, the spans won’t be delivered and you’ll see connection errors in logs. If using Jaeger instead, you’d swap to the Jaeger exporter:

```xml
<dependency>
  <groupId>io.opentelemetry</groupId>
  <artifactId>opentelemetry-exporter-jaeger</artifactId>
</dependency>
```

And then configure the endpoint if needed (Jaeger’s default might be `http://localhost:14250` for gRPC or 14268 for HTTP Thrift; OTel auto-config might have defaults too).

Spring Boot will pick up environment variables or properties for OTel if you set them. For example, you could set:

```properties
management.otlp.tracing.endpoint=http://localhost:4318
```

if using OTLP direct to a collector. But for our case, the defaults suffice (Zipkin at localhost).

**Verification of tracing**: Start the Zipkin server, then start your Spring Boot app. Call the `/hello` endpoint a few times. In your application log, you should see messages like:

```
INFO [demo-observability,traceId=...,spanId=...] c.e.HelloController : Handling request...
```

This indicates a traceId/spanId are present. Now go to the Zipkin UI (http://localhost:9411) and use the search interface:

- Select service name = `demo-observability` (it should appear in the dropdown if spans were received).
- Hit search; you should see trace records. Each trace might have one span (if our app is just one service). If we had calls to other services, you’d see multiple spans per trace.

Click on a trace to view details. For each request to `/hello`, you should see a span (likely named something like `GET /hello`). If the instrumentation captured it, you might also see sub-spans for internal work. Since we manually timed the work with a Timer but didn’t create a manual span, likely we just have the one HTTP server span. We could manually create additional spans using the Observation API or OpenTelemetry API if needed (for example, to trace internal sections of code).

So far, our tracing is basic: each incoming request is a trace with a single span. Let’s make it a bit more interesting.

### 5.2 Manual Tracing with Micrometer Observation (OpenTelemetry)

Often, automatic instrumentation is not enough – you might have important sections of code that you want to appear as separate spans in a trace. Micrometer’s Observation API (or directly using OpenTelemetry’s API) allows you to create spans in your code.

We can demonstrate this by creating an observation inside the `/hello` method. However, note: we already have a span for the HTTP request itself. Ideally, you’d create a sub-span if you want to measure a sub-operation. For example, if `/hello` was calling an external API or doing a DB query, you might create a span around that operation.

For demonstration, let’s say our `hello()` method does two steps: step1 (maybe preparing the greeting) and step2 (logging it or sending somewhere). We can instrument those as separate spans.

Micrometer provides an `ObservationRegistry` bean. We can inject that and create observations. However, since we already have a Timer, let’s use OpenTelemetry API directly to show variety (either approach is fine):
First, add OpenTelemetry API dependency (if not already via exporter). Actually, `micrometer-tracing-bridge-otel` should bring OTel APIs. We can use the `io.opentelemetry.api.trace.Span` and `Tracer`.

Spring Boot configures an OTel Tracer for us. We can get the current span via `Span.current()` or get a Tracer bean. Simpler: use Micrometer’s `Observation` API:

```java
@Autowired
private ObservationRegistry observationRegistry;
```

Then:

```java
Observation.createNotStarted("hello.step1", observationRegistry).observe(() -> {
    // code for step1
});
```

This will create a new span (since OTel bridge is active, it creates an OTel span under the hood) with name "hello.step1", do the code, and end the span.

Let’s modify our code:

```java
@GetMapping("/hello")
public String hello() {
    helloCounter.increment();
    return helloTimer.record(() -> {
        // Start a sub-span for step 1
        Observation step1 = Observation.start("hello.step1", observationRegistry);
        try {
            // Simulate some work in step 1
            Thread.sleep(50);
            // perhaps set some metadata
            step1.event(Event.of("step1-done"));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            step1.error(e);
        } finally {
            step1.stop();
        }

        // Start a sub-span for step 2
        return Observation.createNotStarted("hello.step2", observationRegistry)
                          .observe(() -> {
            try {
                Thread.sleep(30);
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            return "Hello, Observability!";
        });
    });
}
```

What we did:

- We explicitly created and started an observation "hello.step1". We simulate 50ms of work, add an event to the span (a custom marker), and stop it. Then we used a convenient `observe` for "hello.step2" which handles start/stop around the lambda.
- These Observations nest within the current trace context (since the HTTP request span is already there and ObservationRegistry is context-aware).
- As a result, the trace for a `/hello` request should now have three spans: the HTTP server span (automatically created), and two child spans "hello.step1" and "hello.step2" (manual).
- The Timer is still measuring total time of the method; it doesn’t interfere with tracing (since Timer is just measuring time, not affecting context).

Re-run and generate a trace. In Zipkin/Jaeger UI, you should now see a trace hierarchy:

```
(trace) - GET /hello  [root span]
            \_ hello.step1 [child span, ~50ms]
            \_ hello.step2 [child span, ~30ms]
```

This demonstrates **manual instrumentation**. In a real app, step1 could be calling another service – in that case you’d use something like `RestTemplate` which is auto-instrumented (so it would generate a client span). Step2 could be a DB query – if using Spring Data/JDBC, you’d get a span for the query via auto-config (if you include the JDBC instrumentation). Spring’s Observability auto-config attempts to cover many cases without manual code, but it’s good to know you can add custom spans for important sections or to add metadata (like the `event` we added, which could be visible as a log/annotation on the span).

**Trace Propagation**: If our app calls another service (HTTP call), the tracing context will be propagated. For example, if using `RestTemplate` to call `http://otherservice:8080/api`, with `micrometer-tracing-bridge-otel` on classpath, Spring Boot auto-instruments RestTemplate. We need to use a builder to get RestTemplate instrumented:

```java
@RestController
public class HelloController {
    private final RestTemplate restTemplate;
    public HelloController(RestTemplateBuilder builder) {
        this.restTemplate = builder.build(); // Spring Boot auto-configures this RestTemplate with tracing interceptors
    }
    ...
    // inside some handler
    String response = restTemplate.getForObject("http://otherservice:8080/api", String.class);
    ...
}
```

The above would ensure that the outgoing HTTP call carries the `traceparent` header. If the other service is also instrumented, it will join the trace and you’ll see spans from both services in the same trace.

We won’t fully implement a multi-service setup here, but keep in mind that propagation is a critical part of distributed tracing – all services must agree on the context format (W3C Trace Context is standard ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=new%20distributed%20tracing%20support%20with,helps%20to%20label%20the%20observations)), which we are using). If you had an older system using B3 headers (Zipkin’s format), Micrometer can be configured to use B3 if needed, but W3C is the default.

### 5.3 Integrating with Jaeger or Zipkin

We already touched on this by using Zipkin’s exporter and UI. Let’s discuss a bit more systematically how to integrate with tracing backends and what options exist:

**Zipkin Integration**: We used OpenTelemetry’s Zipkin exporter. Spring Boot’s approach (Micrometer Tracing + OTel) means you could alternatively use OTel’s native protocol (OTLP) to send to a OpenTelemetry Collector or directly to Jaeger. Zipkin’s UI is simple and a good start for development or demos. It shows spans and timing but is somewhat limited in advanced querying.

**Jaeger Integration**: Jaeger is another popular open-source distributed tracing system (under CNCF, like OpenTelemetry). Jaeger has a UI and backend storage, and typically you would use the OpenTelemetry exporter for Jaeger or send via an OTel collector. Two ways to integrate:

- **Direct via Jaeger Exporter**: Use `opentelemetry-exporter-jaeger` dependency. By default, this might attempt to send to `localhost:14250` (gRPC). You can configure `OTEL_EXPORTER_JAEGER_ENDPOINT` or similar environment variables if needed. Jaeger’s all-in-one image can accept this without extra config.
- **Via OpenTelemetry Collector**: You could deploy an OTel Collector, have your app send OTLP to it (with `opentelemetry-exporter-otlp`), and then the collector can route to Jaeger or other backends. This adds an extra component but is very flexible (and often used in production setups).

**Configuration**: As mentioned, Spring Boot can take config via properties or environment (it recognizes standard OTel env vars like `OTEL_EXPORTER_OTLP_ENDPOINT`). For example, to send directly to Jaeger’s HTTP collector, you might set:

```properties
otel.exporter=jaeger
otel.exporter.jaeger.endpoint=http://localhost:14268/api/traces
```

(This is hypothetical syntax; in practice, Spring Boot might expect `management.otlp.tracing.endpoint` or you use OTel’s own environment variables.)

**Verification in Jaeger**: If using Jaeger UI (often at http://localhost:16686), you can search for traces by service (should list `demo-observability`). Jaeger’s UI is similar to Zipkin’s but with more features (like aggregation and searching by operation name, etc.).

**Multiple spans and Baggage**: If you pass data along with the trace (context baggage), Micrometer supports something called "remote baggage" to propagate custom fields with the trace context ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=contain%20built,helps%20to%20label%20the%20observations)). For example, you might propagate a userId or tenantId through the trace context so each service can log it or tag spans with it. This is advanced usage – you’d configure `Observation.GlobalTags` or use `Baggage` API from OpenTelemetry to add such data. We mention this as part of enterprise needs, but won’t implement it fully here.

**Summary of Tracing Setup**:

1. **Instrument code or rely on auto-instrumentation**: We did both – auto for HTTP, manual for custom spans.
2. **Exporter configuration**: We chose Zipkin. Could be Jaeger or OTLP.
3. **Verify end-to-end**: Use the chosen tracing UI to verify that a user action in the app produces a trace with spans that match expectations (names, timings, relationships).

Now that we have metrics and traces flowing, the third pillar is logging. In the next chapter, we focus on logs and how to make them more useful and correlated with the rest of our telemetry.

## 6. Logging & Correlation

Logging has been a staple of application troubleshooting for decades. In the context of observability, logs become even more powerful when correlated with metrics and traces. In this chapter, we’ll look at how to implement **structured logging**, how to aggregate logs in a centralized system, and how to correlate log entries with trace IDs (closing the loop between the observability pillars).

### 6.1 Structured Logging in Spring Boot

By default, Spring Boot logs to the console in a human-friendly format (e.g., timestamp level and message). However, unstructured logs (plain text) can be hard for machines to parse. **Structured logging** means formatting logs as structured data (often JSON), which can be easily indexed and searched by log management systems ([Structured logging in Spring Boot 3.4](https://spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4#:~:text=Structured%20logging%20is%20a%20technique,for%20structured%20logging%20is%20JSON)). A common format is JSON with fields like timestamp, level, logger name, message, etc.

Starting with Spring Boot 3.4, there is out-of-the-box support for structured logging in either **Elastic Common Schema (ECS)** JSON or Logstash JSON format ([Structured logging in Spring Boot 3.4](https://spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4#:~:text=With%20Spring%20Boot%203,it%20with%20your%20own%20formats)). If you use Boot 3.4 or above, you can simply set a property to enable JSON logging:

```properties
logging.structured.format.CONSOLE=ecs
```

This would output logs in ECS-compliant JSON (suitable for Elastic stack) ([Structured logging in Spring Boot 3.4](https://spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4#:~:text=To%20enable%20structured%20logging%20on,application.properties)). For example:

```json
{
  "@timestamp": "2025-02-19T21:30:00.123Z",
  "log.level": "INFO",
  "service.name": "demo-observability",
  "message": "Hello endpoint called",
  "trace.id": "4a1f678d93bfb42a",
  "span.id": "6b3f2d4951f0f3ca"
}
```

This JSON contains the log level, service name, message, and importantly `trace.id` and `span.id`. It’s structured, meaning a log system can index `trace.id` and allow searching all logs for a given trace easily.

If you are on an older Spring Boot version or want a custom format, you can still achieve structured logging by configuring your logger:

- **Using Logback JSON encoder**: Add `net.logstash.logback:logstash-logback-encoder` dependency. Then configure Logback to use `ch.qos.logback.classic.encoder.PatternLayoutEncoder` with a JSON pattern, or directly use logstash encoder’s `LogstashEncoder`.
- **Programmatic logging of key-value**: Some use libraries like SLF4J’s MDC to put key-value pairs, or use alternative logging frameworks that inherently log in JSON.

For our purposes, we will assume using Spring Boot’s built-in support (if available). If not, at least ensure that your log pattern includes the trace and span IDs as described earlier (`%X{traceId}` etc.). This is less about structure and more about correlation, but it’s crucial.

### 6.2 Log Correlation with Traces

Log correlation refers to the ability to connect log entries to specific requests or context – typically via trace IDs. We have already set up our logging pattern to include `traceId` and `spanId` in each log line. With structured logs, these would be fields in the JSON (e.g., `trace.id` in ECS format).

How does this work under the hood? When a trace is started (a Span is created) by Micrometer/OTel, it puts the identifiers into the SLF4J **MDC (Mapped Diagnostic Context)**. MDC is like a thread-local map of context data that the logging framework can automatically append to each log. Spring Boot’s Micrometer integration, as we saw, uses predefined keys `traceId` and `spanId` in MDC ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=,X%7BspanId)). So any log within the scope of a traced operation will have those values in MDC.

For example:

```java
LOG.info("Processing hello request for userX");
```

If called inside the trace/span, the logging framework knows to add `[traceId=abc123, spanId=def456]` (or whatever pattern we set).

**Correlating in practice**:

- In a log management system (like Kibana if using Elastic, or Grafana Loki, Splunk, etc.), you can search for a particular traceId. If your logs are structured, you’d query `trace.id: abc123`. If using plain text with pattern, you might do a text search.
- You can go from a trace in Jaeger/Zipkin and copy the trace ID, then search logs for it to see all log events during that trace. Some advanced setups push logs to the tracing system as events on the trace (OpenTelemetry allows logs to be part of trace data), but the simpler approach is external correlation via IDs.

**Log Aggregation**:
In Kubernetes or cloud environments, usually each service’s logs are aggregated to a central location (using Fluent Bit/Fluentd or a log service). Ensure that the raw logs preserve the needed info. JSON logging makes it easy because the structure is preserved. If it’s plain text, ensure it doesn’t get reformatted losing the traceId (some older log forwarders might only take a portion of line).

**Example: Using Grafana Loki**:
Loki is a log aggregation system optimized for Kubernetes. If we had a Loki agent, we could push our logs (as we saw with the Loki Logback appender config snippet in the Spring blog) ([Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3#:~:text=%3Cappender%20name%3D,NONE%7D%2Clevel%3D%25level%3C%2Fpattern%3E%20%3C%2Flabel%3E%20%3Cmessage)). In Grafana, we could then search logs for `traceID="abc123"`. Loki actually has integration where if you use Tempo (Grafana’s distributed tracing, which is OTLP based) and include traceID, Grafana can link traces to logs automatically.

**Error Tracking**:
Correlating logs and traces is extremely helpful for error analysis. For instance, if a request failed (500 error), you can go to your tracing UI, find the error span, get the trace ID. Then search logs for that trace ID to find exception stack traces or error logs that occurred on that path. This saves time compared to scanning all logs for that time period.

### 6.3 Best Practices for Logging in an Observability Context

A few tips for logging as part of observability:

- **Use appropriate log levels**: Info for general events, Debug for detailed diagnostic (often turned off in production), Warn/Error for problems. This way your log aggregator can filter noise. Do not log extensive debug data at high volume in production, as it can bloat logs.
- **Avoid sensitive data**: Be cautious not to log personal data, secrets, etc. Observability is for ops/developers, and logs can be an exposure risk.
- **Structure and Context**: We covered structure. Also include context in messages where useful (e.g., orderId in an "Order processed" log). But if it's something that goes in trace context, maybe better as part of MDC or baggage.
- **Log rotation and retention**: Even if you aggregate, keep local logs short (the aggregator should handle long-term storage). Use Spring Boot’s logging.file (or container stdout) wisely.
- **Correlation beyond trace**: Sometimes you want to correlate logs even without a trace (e.g., group logs by a certain batch job execution ID). In such cases, you can manually put custom MDC values at the start of that operation.
- **Tracking system events**: Metrics and traces often won't explicitly capture things like application startup events, background job triggers, etc. Use logs to record those (e.g., "Cache refreshed" or "Scheduled job X executed"), so you have a timeline of important events that might not be visible in metrics/traces.

Now that we have metrics, traces, and logs all being produced and correlated, we should integrate external tools to visualize and alert on this data. That’s where Prometheus, Grafana, and others come into play, which we discuss next.

## 7. Integrations with Monitoring & Visualization Tools

Our Spring Boot application now emits a lot of observability data:

- Metrics (available on `/actuator/prometheus`).
- Traces (being sent to Zipkin/Jaeger).
- Logs (with context, potentially sent to an aggregator).
  To get the most value, we integrate these with tools that allow us to **store, visualize, and alert** on this data. In this chapter, we’ll cover how to set up **Prometheus** to collect metrics, **Grafana** to visualize metrics and traces, and touch on alerts and other tools.

### 7.1 Using Prometheus for Metrics Collection

**Prometheus** is a popular open-source monitoring system optimized for time-series data (metrics). We’ve already set up our application to expose a Prometheus scrape endpoint. Now, we need to configure Prometheus server to scrape our application.

**Setting up Prometheus**:

1. **Install/Run Prometheus**: The simplest is using the official Prometheus Docker image or binary. For example, using Docker:

   ```bash
   docker run -p 9090:9090 -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
   ```

   This runs Prometheus on port 9090 and expects a configuration file.

2. **Configure `prometheus.yml`**: Prometheus configuration declares scrape targets. A minimal config (YAML) to scrape our Spring Boot app:

   ```yaml
   scrape_configs:
     - job_name: "demo-observability"
       scrape_interval: 15s
       metrics_path: "/actuator/prometheus"
       static_configs:
         - targets: ["host.docker.internal:8080"]
   ```

   If Prometheus runs in Docker and our app runs on the host at 8080, `host.docker.internal` works (for Mac/Win). Otherwise, adjust the target to where the app is accessible (if all in K8s, you'd use the service discovery there).
   This tells Prometheus to scrape our app every 15 seconds at the given path. The `job_name` will label metrics (job="demo-observability").

3. **Run Prometheus**: Ensure it starts without errors, and then navigate to `http://localhost:9090`. Use the "Status > Targets" page to confirm the target is UP. If it's down, check networking or config syntax.

4. **Query metrics**: In Prometheus’s UI, try a simple query like `hello_requests_total` (our custom metric). You should see a graph or value if data is present. You can also query built-ins like `http_server_requests_seconds_count`.

Prometheus will store these metrics in memory/disk and allow querying via PromQL. It also has a rudimentary graphing UI (mostly for ad-hoc queries). For long-term, often people use remote storage or other means if needed, but for now, local Prometheus is fine.

### 7.2 Grafana for Visualization

**Grafana** is a flexible dashboard and visualization tool that can connect to Prometheus (and many other data sources, including Jaeger for traces, Loki for logs, etc.). We will use Grafana to set up dashboards for our metrics and possibly explore traces.

**Setting up Grafana**:

1. **Run Grafana**: Similar approach, use Docker or local install. Docker example:

   ```bash
   docker run -d -p 3000:3000 grafana/grafana-oss
   ```

   This runs Grafana on port 3000. Login with default creds (admin/admin unless changed).

2. **Add Prometheus Data Source**: In Grafana UI, go to Configuration -> Data Sources -> Add data source. Choose Prometheus, set URL to `http://host.docker.internal:9090` (or appropriate address if Grafana in Docker). Save & Test, it should be successful if Prom is reachable.

3. **Create a Dashboard**:
   - For example, create a new dashboard and add a graph panel for HTTP requests. Use a PromQL query like:
     ```
     rate(http_server_requests_seconds_count{uri="/hello"}[1m])
     ```
     This shows requests per second to /hello (averaged over last 1 minute window). Alternatively, use `sum by (status) (rate(http_server_requests_seconds_count[5m]))` to see request rate by status code, etc.
   - Add another panel for latency: perhaps the 95th percentile latency. If Micrometer published percentile, you could query `http_server_requests_seconds{quantile="0.95", uri="/hello"}`. If not, you could use histogram buckets (a bit complex with PromQL). We enabled histogram for `hello.latency` with percentile, so try:
     ```
     hello_latency_seconds{quantile="0.95"}
     ```
     That might show the 95th percentile of our custom timer (if data available).
   - Add a panel for custom metric count: `hello_requests_total` (as a single stat, showing total hellos served).
   - Add CPU or memory panel: e.g., `process_cpu_usage` (you might multiply by 100 to show percent). Or `jvm_memory_used_bytes{area="heap"}` to show current heap usage (combine with total heap maybe).

Grafana panels are highly configurable (you can set titles, units, etc.). This becomes your observability dashboard where you monitor the app.

**Tracing in Grafana**: Grafana can also integrate with Jaeger or Tempo for traces. If using Jaeger:

- Add Jaeger data source (needs the Jaeger query endpoint, e.g., `http://localhost:16686`).
- You can use Grafana's "Explore" to find traces by trace ID or service name, and even link from logs to traces or vice versa if properly configured.

However, Grafana's tracing UI is not as feature-rich as Jaeger’s own UI, so it’s fine to use Jaeger UI directly. But having everything in Grafana is convenient for a single pane of glass.

**Alerts**:
Both Prometheus and Grafana support alerting:

- Prometheus has Alertmanager integration. You define alert rules in PromQL (e.g., trigger if `rate(http_server_requests_seconds_count{status="500"}[5m]) > 0.1` meaning more than 10% error rate).
- Grafana (especially with Grafana Cloud or v8+ alerting) can also create alerts from dashboard queries.

For simplicity, an example alert in Prometheus config:

```yaml
groups:
  - name: example-alert
    rules:
      - alert: HighErrorRate
        expr: rate(http_server_requests_seconds_count{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          description: "High 5xx error rate (>5% requests) for 5 minutes on {{ $labels.instance }}"
```

This would send an alert if >5% of requests are errors for 5 minutes. Alertmanager would need to be configured to email or Slack etc.

Grafana on the other hand could have a simpler approach for user-defined alerts and notification channels.

**Other Tools**:
Micrometer’s advantage is it can send metrics to other systems too. For instance, instead of Prometheus, you could use:

- **Elastic Stack (ELK)**: using Elastic APM perhaps for traces/metrics, or push metrics to Elasticsearch using Micrometer’s Elastic registry.
- **Cloud Monitoring**: e.g., send to New Relic, Datadog using respective Micrometer registries ([Micrometer Application Observability](https://micrometer.io/#:~:text=Micrometer%20supports%20publishing%20metrics%20to,Google%20Stackdriver%2C%20StatsD%2C%20and%20Wavefront)) – many companies use those SaaS platforms which provide both dashboards and traces.
- **Wavefront**: Another SaaS with strong Spring integration (Wavefront was early supported by Spring).

Our focus was open-source tools (Prom/Grafana/Jaeger) as they are accessible and common in Kubernetes setups.

### 7.3 Putting It Together in Kubernetes

Though full Kubernetes deployment is next chapter, it’s worth noting how these integrations work there:

- Prometheus in K8s usually runs inside the cluster and uses service discovery to find pods with specific annotations (like scrape annotations or specific ports). The Spring Boot Actuator Prometheus endpoint can be annotated or just known by service name for Prom to find it.
- Grafana can run in cluster too and talk to Prometheus service.
- Jaeger can be installed via Operator in K8s, and your app can send traces to the Jaeger collector service.

There are also combined solutions like **Grafana Tempo** for traces and **Loki** for logs (completing the Grafana “LGTM” stack: Loki for logs, Grafana for viz, Tempo for traces, Mimir for metrics as an alternative to Prom). But detailing those is beyond scope; just know Micrometer with OTLP can send to Tempo as well.

We have now covered how to see and use our telemetry. Next, we’ll address considerations for running this in production-like environments, especially Kubernetes, and how to maintain observability in a microservices context.

## 8. Cloud-Native Observability (Kubernetes & Microservices)

Deploying our Spring Boot application to Kubernetes (or any cloud environment) introduces new considerations for observability. In this chapter, we discuss how to ensure our metrics, logs, and traces work in a **containerized, orchestrated environment** and how to manage observability across many microservices.

### 8.1 Deploying the Application to Kubernetes

When containerizing and deploying to Kubernetes, here are important steps and checks for observability:

- **Container Image**: Build a Docker image for the app. Ensure it includes the necessary agents if any (for example, if one uses OpenTelemetry Java Agent instead of Micrometer bridging, you’d add that as a Java agent on startup. But in our approach, it’s built-in, so just normal jar).
- **Resource Requests/Limits**: Observability adds some overhead (CPU, memory). When setting Kubernetes resource requests/limits, account for a bit of overhead. For example, allow a little extra memory for metrics storage, etc. Micrometer metrics by default don’t use a lot of memory unless high cardinality, but traces buffering might use some.
- **Environment Variables/Config**: You might shift configuration to env vars in K8s:

  - e.g., `OTEL_EXPORTER_OTLP_ENDPOINT` to point to a collector service.
  - If using a different Prom endpoint path or port, configure `MANAGEMENT_SERVER_PORT` or `MANAGEMENT_ENDPOINTS_WEB_EXPOSURE_INCLUDE`.
  - Many config can remain in application.properties baked into the image or provided via ConfigMap.

- **Service Discovery for Prometheus**: Typically, you would label your pod or service so Prometheus discovers it. For example, add annotations:

  ```yaml
  prometheus.io/scrape: "true"
  prometheus.io/path: "/actuator/prometheus"
  prometheus.io/port: "8080"
  ```

  Then Prom operator or similar will find these pods and scrape them. Alternatively, use a ServiceMonitor if using the Prometheus Operator, etc.

- **Running the Trace Collector**: In K8s, you might deploy Jaeger or Zipkin as a service. For Jaeger, a common setup is installing Jaeger Operator or an AllInOne for dev. Then configure your app via env to send to `jaeger-collector.default.svc:14250` (for gRPC). Or deploy an OpenTelemetry Collector as a sidecar or daemonset – then use OTLP.

- **Log Aggregation**: Logs in Kubernetes (stdout/stderr of pods) are typically collected by Fluentd/Fluent Bit and shipped to a system (Elastic, CloudWatch, etc.). If our app logs in JSON to stdout, that JSON will be forwarded. Ensure the log agent is configured to parse JSON (so it can index fields like traceId). Many log systems auto-detect JSON. If not, consider adjusting the log agent config to treat our logs as JSON.

- **Distributed Tracing Across Services**: If you have multiple services:
  - Each should have Micrometer tracing and use the same propagation (by default W3C Trace Context, so that’s fine).
  - Ensure all services share a unique `spring.application.name` (the service name) so tracing systems differentiate them.
  - If using an OTel collector, all services send to that collector which then sends to Jaeger/Tempo.
  - When a request flows from Service A to B to C, the trace context is propagated via HTTP headers. For it to work on Kubernetes with, say, an ingress or a service mesh, ensure the mesh (if any) doesn’t break headers. Most meshes (Istio/Linkerd) will pass through or even have their own tracing integration. For example, Istio can propagate Zipkin headers and generate spans for network hops. This can complement app tracing.

### 8.2 Observability in a Microservices Architecture

Now consider an architecture with dozens of microservices, each instrumented like our app. Observability considerations:

- **Centralized Monitoring**: Use one Prometheus (or a scalable solution like Thanos for multiple) to collect all metrics. Use consistent metric naming across services for similar things (e.g., all HTTP server metrics share the `http_server_requests` name, distinguished by service through either a label or the job label).
- **Dashboards per Service and Global**: You might create a Grafana dashboard template that can be re-used for each service (just change the service name variable). Also global dashboards that aggregate (like overall error rate in the system).
- **Trace Sampling**: In a large system, sampling becomes important. Tracing every request from every service might be too much data. You can sample at edges (like only sample some percentage of incoming requests). Micrometer’s `management.tracing.sampling.probability` property can be set per service (and possibly dynamically via config) to control that. Alternatively, if using an OTel Collector, it can do head-based sampling or tail-based sampling across the entire system.
- **Log Volume**: With many services, logs can be huge. Ensure log levels are appropriately set. Use log rotation in pods (K8s will rotate by size by default). Use separate logging for debug vs error (so you can only aggregate errors centrally maybe).
- **Correlation and Context Propagation**: Besides trace IDs, you might propagate user context or other info. OpenTelemetry’s baggage or similar can be used, but be mindful: too much baggage (like user id on every trace) can increase overhead. Often, just trace id is enough to correlate across systems; you can then fetch more info by pivoting (e.g., trace id => find user from one of the span tags if needed, or correlate with an event).
- **Kubernetes-specific metrics**: If you want to monitor infrastructure (like node metrics, container CPU, etc.), those are outside the app but can be scraped by Prom (via node exporter, cAdvisor, etc.) and complement app metrics. For instance, you might see app memory usage metric vs container memory limit to see if you’re close to limits.
- **Service Mesh** (optional): If using a service mesh, consider how it affects observability:
  - Mesh typically provides its own metrics (like Envoy sidecar stats, which can include request counts, latencies at the network level) and traces (some meshes auto-trace). If you have that, you might integrate those metrics with your dashboards too.
  - But even with mesh, application-level metrics and traces (via Micrometer) are still valuable for internal logic and business events that mesh can’t see.

### 8.3 Managing and Scaling Observability Components

In cloud-native deployments, the observability infrastructure itself must be scalable and reliable:

- **Prometheus Scaling**: One Prom instance can handle a fair number of metrics, but at some point consider sharding or using Thanos/Cortex (which are beyond our scope, but just note them).
- **Storage**: Prometheus by default stores metrics on disk. For long retention (months/year), you might use remote storage or something like Thanos. Logs obviously need storage (Elasticsearch or cloud logs) – ensure indices and retention are managed (to avoid huge costs).
- **Trace Backend**: Jaeger can use Elasticsearch or Cassandra for storage of traces; ensure that’s sized properly if you trace a lot. Tempo (Grafana’s trace backend) is an alternative that is built for high-scale trace storage.
- **Overhead Monitoring**: Keep an eye on how much overhead instrumentation adds. You can even have metrics about your observability, e.g., the Micrometer Observation API might have internal metrics or use the `otel.sdk.*` metrics (OpenTelemetry SDK can expose metrics about spans exported, dropped, queue size, etc.). If CPU usage of your app is significantly impacted by tracing, consider lowering sampling or optimizing instrumentation (maybe disabling extremely hot path instrumentation).
- **Security**: When exposing Actuator endpoints in K8s, consider securing them. In production, you might not want `/actuator/prometheus` open without auth. In many setups, it's inside cluster so it's fine. But if necessary, secure with an auth token or put behind a gateway. Similarly, trace data leaving the service might contain sensitive info (like URLs, parameters); ensure your tracing system is secured (Jaeger UI should be internal or behind auth if on internet).

By addressing these points, you ensure that observability scales with your application and doesn’t become a bottleneck or single point of failure.

We’ve now covered deploying and running observability in production. Next, let’s discuss how to optimize performance and troubleshoot issues specifically related to observability instrumentation.

## 9. Performance Optimization & Troubleshooting

While observability is invaluable, it introduces additional processing in our application. In this chapter, we will discuss how to **optimize the performance** of our observability components (metrics, tracing, logging) and how to troubleshoot common issues that might arise in collecting observability data. We’ll also cover some best practices to ensure observability remains an aid, not a hindrance.

### 9.1 Minimizing Observability Overhead

Instrumentation has a cost in terms of CPU, memory, and I/O:

- **Metrics Overhead**: Updating a counter or timer is usually very fast (in-memory operations), but very high metric update rates or huge numbers of metric time series can cause CPU and memory overhead. Micrometer is designed to be efficient, but if you push it to extreme (lots of distinct tags, etc.), you could see GC pressure. A study comparing OpenTelemetry and Micrometer found differences in memory allocation: OpenTelemetry Java metrics had significantly fewer allocations in some cases vs Micrometer/Prometheus client ([OpenTelemetry Java Metrics Performance Comparison | OpenTelemetry](https://opentelemetry.io/blog/2024/java-metric-systems-compared/#:~:text=22%25,exporter%20library%2C%20but%20without%20the)). Regardless, you can follow best practices:

  - Only record metrics you need.
  - Remove unused meters (they accumulate if you create programmatically with dynamic tags).
  - Use `Histogram`/percentiles judiciously to avoid excessive tracking.
  - If using Prometheus, be mindful of scrape interval and do not scrape too frequently.

- **Tracing Overhead**: Capturing a span involves getting timestamps, possibly capturing stacktrace or exceptions, and exporting data out-of-process. The overhead is proportional to number of spans and context switches:

  - **Sampling** is the main lever. By reducing sampling rate, you drastically cut overhead (both in-app and in the backend storage) ([OpenTelemetry vs Brave - A Practical Comparison Guide - SigNoz](https://signoz.io/comparisons/opentelemetry-vs-brave/#:~:text=OpenTelemetry%20vs%20Brave%20,in%20sampling%20and%20data)). In many systems, a 100% sample of all requests is unnecessary – let’s say 10% or even 1% might be enough to spot trends, with perhaps some mechanisms to sample all for errors. Tail sampling (smartly keeping interesting traces) can be used in collectors.
  - **Batching**: OpenTelemetry SDK batches span exports. Ensure batch sizes and timeouts are tuned to not overwhelm the network (most SDKs default well, but if you see high latency in exporting, you can tweak).
  - In a high-throughput service, if latency overhead of tracing is a concern, measure it. Usually, it’s small (maybe microseconds per span), but if you have thousands of spans per second, it adds up. You could consider lighter tracers or turning off some auto-instrumentation that you don't need.
  - One optimization if needed: some people move to “observability sidecar/agent” model – using OpenTelemetry auto-instrumentation agent which offloads some work. But with Micrometer in-process, that’s not applicable, so stick to sampling.

- **Logging Overhead**: Logging can be surprisingly expensive if misused:
  - Writing to console or file is I/O. In high volume, it can slow the app. Use asynchronous appenders if possible (Logback has async appender, which decouples log writing from the request thread).
  - Avoid heavy string concatenation or object serialization in logs, especially at info level in hot paths. If debug is off, those statements won’t run (thanks to parameterized logging or guard by `LOG.isDebugEnabled()`).
  - If using JSON logging, the serialization overhead is slightly higher than plain text, but negligible compared to I/O.
  - Keep log level appropriate (don’t run debug in prod unless troubleshooting specific issues).
- **Micrometer Internal**: Under the hood, Micrometer metrics uses lock-free algorithms and caches for things like current meter values. If you ever profile and see contention in meter updates, that’s a sign you have extremely high update rates – consider aggregating at a higher level instead of every single event.

### 9.2 Troubleshooting Observability Issues

What if something in observability isn’t working? Some common issues and how to address them:

- **Metrics not visible**: If you don’t see your custom metric in Prometheus:

  - Check `/actuator/metrics` (via HTTP or JMX) if the meter is present. If not, maybe the code registering it didn’t run or conditions not met.
  - If it’s in Actuator but not in Prometheus, check that Prometheus target is up and the metric isn't filtered. Also, remember Micrometer might not show a metric until it’s updated (some meters are lazy). Our counters increment on use, so after one use it should appear.
  - Check naming: PromQL might require adjusting (e.g., Micrometer renames `.` to `_`).
  - If using a push registry, check logs for errors pushing.

- **No traces appearing in backend**:
  - Check application logs for errors from the OTel exporter. You might see connection refused if Jaeger/Zipkin is not reachable. Ensure the endpoint is correct and the service is accessible (firewall, network, etc.).
  - Confirm that traces are being generated: enable DEBUG logging for `io.opentelemetry` or `org.springframework.observability.tracing` to see if spans are being created.
  - If using sampling, perhaps your sampling is 0 (some mis-config). Ensure probability > 0.
  - If trace IDs appear in logs but nothing in UI, likely export issue. You can also run a local OpenTelemetry Collector in debugging mode to see if it receives anything.
- **Logs missing trace IDs**:

  - Check MDC configuration. If using a custom thread pool or asynchronous code, trace context might not propagate to that thread, so the MDC might not have traceId. Micrometer’s context propagation should handle many cases, but if you spawn new threads manually, you might need to wrap them (Micrometer has `ContextSnapshot` or similar to restore context).
  - Ensure your logging pattern exactly matches the keys (`traceId` vs maybe it is `trace.id` if using structured logging with a different provider).
  - If using Logback JSON encoder, ensure you include MDC fields.

- **High memory usage due to metrics**:

  - Might be due to high cardinality (each unique tag combination results in a timeseries stored). If you accidentally use something like userId as a tag, you could OOM after many users. Use Prometheus’s `/status/tsdb` or Grafana’s Prom plugin to see number of time series. Remove or reduce problematic metrics (with a MeterFilter or code change).
  - Could also be due to long histogram buckets (Timber's hist can use memory). If an endpoint has an unbounded number of routes or something, check that.

- **Inconsistent metrics after scaling**:
  - In K8s, if you have multiple instances, Prometheus will scrape each and they’ll each have their own counters. By default, queries aggregate by instance. If you scale up/down, counters reset on new instance. Use rate functions and aggregate across instance or job to handle this. This is a normal behavior but worth noting (e.g., don’t be alarmed if a counter drops; it might be a new pod).
- **Time synchronization**:

  - If logs, metrics, traces appear to have mismatched timestamps, ensure your servers/pods have correct time sync (in containers usually fine). Traces rely on system clock for span times, as do logs. If an environment has a time skew, it can confuse correlation. Docker and K8s usually handle this well via host, but on some dev machines it could be off.

- **Actuator and security**:
  - Sometimes in production, Actuator endpoints might be secured (requiring a username/password or available only on a management port). If Prometheus can’t scrape due to auth, set up either a specific auth (Prom supports basic auth headers) or expose the metrics endpoint publicly (safe if non-sensitive).
  - If you use management port (running actuator on different port), ensure Prom config uses that port.

### 9.3 Best Practices Recap

To ensure optimum performance and usefulness of observability:

- **Start with needs**: Instrument what matters (key business operations, critical performance paths). It’s easy to instrument everything, but focus on signals that will help you detect and solve problems.
- **Use standardized instrumentation**: Leverage Spring Boot’s auto-metrics/tracing as much as possible – it’s well-tested and efficient. Only add custom where needed.
- **Document your metrics and traces**: In a large team, document what each custom metric means, its units, and normal ranges. This helps others (and future you) understand dashboards.
- **Regularly revisit telemetry**: Over time, you might find some metrics aren’t useful or new ones are needed. It’s iterative – remove clutter to reduce overhead and confusion.
- **Practice failure modes**: Test what happens if observability backend is down – does the app still run fine? Typically yes, as Micrometer caches or drops data if not connected (e.g., if Zipkin is down, spans might just get dropped after some retries). Ensure that failure of an observability component doesn’t cascade into app failure. This is generally true by design (non-blocking exports), but keep an eye out for any synchronous calls in your instrumentation (shouldn’t have in our setup).
- **Stay updated**: The landscape evolves (e.g., new Spring Boot releases improved structured logging, OpenTelemetry updates improving performance ([OpenTelemetry Java Metrics Performance Comparison | OpenTelemetry](https://opentelemetry.io/blog/2024/java-metric-systems-compared/#:~:text=22%25,exporter%20library%2C%20but%20without%20the))). Upgrading can yield benefits like lower overhead and new features.

Armed with these practices, you can maintain an efficient observability setup. Finally, let’s look at some advanced scenarios and case studies to solidify our understanding.

## 10. Advanced Use Cases & Case Studies

In this final chapter, we will explore some advanced use cases of observability and real-world scenarios. These examples will illustrate how the concepts we’ve covered come together to solve practical problems, and we’ll discuss strategies used in enterprise-grade observability solutions.

### 10.1 Case Study: Debugging a Production Outage with Traces and Logs

**Scenario**: An e-commerce application composed of multiple services experienced an outage where checkout requests were timing out, causing user frustration and lost sales. The architecture involves a frontend service, an orders service, a payment service, and an inventory service.

**Observability Implementation**: All services use Spring Boot with Micrometer (similar to what we built). They export metrics to Prometheus and traces to Jaeger. Logs are aggregated in Elastic with trace IDs.

**Issue Detection**: The on-call engineer gets an alert from Prometheus: high error rate on the checkout endpoint (HTTP 5xx > 10% for 5 minutes). Grafana dashboard shows a spike in `orders_service` latency and error count. It also shows thread pool queue length increasing, indicating a bottleneck.

**Using Traces**: The engineer goes to Jaeger, filters traces for `operation="POST /checkout"` and sees many traces with very long durations (near the timeout of 30s) and some that failed. Looking at one trace timeline, they see:

- Span 1: `POST /checkout` (in frontend) – it calls `POST /orders`.
- Span 2: `POST /orders` (orders service) – inside it calls `GET /inventory` and `POST /payment`.
- Span 3: `GET /inventory` (inventory service).
- Span 4: `POST /payment` (payment service).

From the trace, Span 3 (inventory) took almost 25 seconds, which is abnormal (it usually takes <100ms). Spans 4 (payment) never happened in the failing trace because the orders service timed out waiting for inventory.

**Root Cause via Logs**: Now they suspect something is wrong in the inventory service. They copy the `traceId` from the trace and search in Kibana. They find in the inventory service logs for that traceId an ERROR: "Database connection pool exhausted, all connections in use". Further logs show slow queries as the DB was under heavy load.

**Resolution**: The team identified that a database index was missing, causing extremely slow queries under high load, which exhausted the connection pool. They added the index and also increased the pool size temporarily to mitigate.

**Learnings**: This case demonstrates:

- Metrics (error rate, latency) alerted and pointed to which service.
- Traces pinpointed the exact component (inventory DB call) causing slowdown.
- Logs gave the detailed error (connection pool exhausted).
  The combination of all three pillars allowed quick diagnosis of a problem that spans multiple services and a database. Without tracing, they might have suspected the wrong service or taken longer to find the DB issue.

### 10.2 Use Case: Custom Business Metrics and Alerting

**Scenario**: A streaming platform wants to monitor how many videos are watched concurrently and how many fail to play, to ensure a good QoS (Quality of Service).

**Implementation**: They add custom metrics:

- `video.play.start.count` (Counter) when a video play is attempted.
- `video.play.failure.count` (Counter) when a video play fails (with tag reason=... perhaps).
- `video.play.duration` (Timer) for playback duration or startup time.

Using Micrometer, these are recorded in the video service. They expose to Prometheus.

**Dashboard & Alert**: Grafana shows current concurrent plays by taking `video.play.start.count` minus `video.play.end.count` (if they track ends) or by active sessions. They set an alert: if failure rate (failures/starts) > 5% in last 5 minutes, trigger a warning. They also track the 95th percentile of `startup.time` to see if the video loading is slow (which could indicate a CDN issue).

**Outcome**: This proactive monitoring is a business-level metric (not just technical like CPU). It directly measures user experience. With Micrometer, they could easily add these counters and timers in the code where play events occur. This shows how observability is not only for technical issues but can provide insights into user-level behavior and satisfaction.

### 10.3 Enterprise-Grade Observability Solutions

Large enterprises often have more complex requirements:

- **Distributed Tracing at Scale**: They might handle millions of spans per second. Solutions involve sampling, big data storage, or switching to tools like Google’s Stackdriver, AWS X-Ray, etc., if on cloud. OpenTelemetry is becoming a standard so vendor-neutral instrumentation (like Micrometer) is future-proof – you can send data to various backends or multiple ones in parallel.
- **Metrics Federation**: Multiple clusters and regions might each have Prometheus, then a central system (Thanos/Cortex) federates data for a global view.
- **AI Ops and Anomaly Detection**: Some use machine learning on metric patterns to detect anomalies beyond static thresholds.
- **Tracing + Logging integration**: Tools like Splunk or Datadog offer UIs to click from a trace to logs automatically. We achieved similar manually; enterprises often invest in making that seamless.
- **SLO (Service Level Objectives)**: Defining SLOs (like 99th percentile latency < X) and error budgets, and using observability data to track compliance. There are tools (like Prometheus’s PromQL or Atlassian’s OpenSLO) to help with this. Our metrics (like latency percentiles, error counts) feed into those SLO calculations.
- **Governance**: When many teams produce telemetry, having conventions (naming, tagging), and guardrails (to prevent one team from accidentally sending millions of metrics and crashing the monitoring) is important. Micrometer helps by providing a consistent framework, and you might have a monitoring team reviewing instrumentation.
- **User Analytics vs Observability**: Sometimes the line blurs – metrics can also serve product analytics (e.g., number of signups per day). There might be separate pipelines for that (to e.g. Google Analytics). But one can leverage the same instrumentation for internal ops vs business analytics by exporting to different systems (Micrometer’s multi-registry feature allows publishing to two backends if needed, say Prometheus for ops, and another store for product analytics).

**Tooling Ecosystem**: In enterprise, one might use:

- **Elastic Stack** for logs and maybe metrics.
- **APM solutions** like Dynatrace, NewRelic, which auto-instrument and provide a polished experience (Micrometer has bridges for some, e.g., Dynatrace has a Micrometer registry ([Best of breed observability with Spring Micrometer and Dynatrace](https://www.dynatrace.com/news/blog/best-of-breed-observability-with-spring-micrometer-and-dynatrace/#:~:text=Dynatrace%20www,tested%20and%20optimized))).
- **Custom Dashboards**: Some build custom portals combining info from various sources.

The key is that the fundamentals remain metrics, logs, traces. As long as your application is instrumented to emit those, you can adapt the backend tooling as needed. That’s why frameworks like Micrometer and OpenTelemetry are so valuable: they provide a stable instrumentation layer decoupled from backend.

### 10.4 Final Thoughts and Best Practices

Implementing observability is an ongoing process. **Continuous improvement** is important: use incidents as learning to add new metrics or spans that would have helped detect or debug the issue faster. Also, periodically prune or adjust what you collect to balance insight vs overhead.

In summary, building a Spring Boot application with Micrometer Observability involves:

- Setting up metrics, traces, and logs from the start.
- Using Spring Boot’s auto-configuration and Micrometer’s APIs to minimize custom code.
- Verifying and visualizing the data with tools like Prometheus/ Grafana / Jaeger.
- Ensuring the solution scales in a cloud environment.
- Following best practices to avoid common pitfalls.
- Leveraging the data to actually improve reliability and performance.

By following the step-by-step approach in this guide, an advanced developer can set up a robust observability infrastructure for Spring Boot microservices, leading to easier monitoring, faster debugging, and overall more resilient applications. Observability, when done right, becomes a powerful ally in managing production systems, turning opaque “black boxes” into transparent services where issues can be seen and addressed before they become outages.
