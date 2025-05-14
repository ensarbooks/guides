# Troubleshooting Java Spring Boot Microservices and Tomcat: A Comprehensive Guide for Software Architects

## Table of Contents

1. **Introduction**
2. **Observability and Monitoring Fundamentals**
3. **Profiling and Diagnostic Tools for Java Systems**
4. **Common Performance Bottlenecks and Tuning**
5. **Memory Management Issues and GC Tuning**
6. **Concurrency and Threading Challenges**
7. **Dependency and Configuration Pitfalls**
8. **Integration Failures in Distributed Systems**
9. **Resilience Patterns for Fault Tolerance**
10. **Apache Tomcat: Configuration and Tuning**
11. **Infrastructure and Deployment Considerations**
12. **Summary of Best Practices and Error Resolution**

## 1. Introduction

Software architects responsible for Java applications built with Spring Boot and running on Apache Tomcat need a strategic approach to troubleshooting. Unlike low-level debugging focused on code, an architect’s perspective emphasizes **system-wide insights, architectural patterns, and proactive measures**. Modern enterprise systems often consist of **distributed microservices**, where issues can arise from inter-service interactions, resource constraints, or environment misconfigurations. This documentation provides a structured, in-depth guide to diagnosing and resolving common problems in such systems, including performance degradations, memory leaks, deadlocks, misconfigurations, and integration failures.

**Scope and Audience:** This guide is written for software architects and senior engineers. It covers **architectural and runtime issues** in Java-based microservices using Spring Boot and Tomcat (whether Tomcat is embedded within Spring Boot or used as an external servlet container). We focus on **strategic troubleshooting insights** – how to identify root causes and implement lasting solutions – rather than step-by-step code debugging. The content spans performance tuning, memory and concurrency management, distributed system concerns, and deployment considerations. We also highlight tools and best practices (e.g. monitoring with Prometheus/Grafana, logging with ELK stack, profiling with JDK Flight Recorder or JProfiler) that enable effective troubleshooting and **observability** at scale.

**How to Use This Guide:** Each chapter addresses a category of issues:

- We begin with **observability fundamentals** (logging, monitoring, and tracing) because robust insights are prerequisite to troubleshooting.
- We then discuss specific problem domains: performance, memory, threading, configuration, and integration issues. Each of these chapters describes typical symptoms, underlying causes, and approaches to diagnose and resolve the problems. Key points are summarized in tables (error types, root causes, resolution strategies) for quick reference.
- Later chapters cover **resilience patterns** (to design systems that handle failures gracefully) and **Tomcat-specific tuning**, as well as **infrastructure aspects** like containerization, Kubernetes orchestration, CI/CD pipelines, and cloud-native considerations.
- Finally, a summary consolidates best practices and provides a quick lookup for common issues and their solutions.

Throughout the document, we cite **authoritative sources** – official documentation, expert books and blogs, and industry whitepapers – to reinforce best practices. These references appear as inline citations in the format 【source†lines】. We encourage readers to consult these sources for deeper exploration. By the end of this guide, an architect should be equipped with a **holistic troubleshooting strategy** for Java Spring Boot microservices on Tomcat: one that not only fixes current problems but also **prevents future issues by informed design and configuration**.

## 2. Observability and Monitoring Fundamentals

In a distributed Spring Boot architecture, **observability** is key – one cannot fix what one cannot see. This chapter covers the three pillars of observability (logging, metrics, and tracing) and how architects can establish a monitoring ecosystem to quickly detect and diagnose issues. We discuss best practices like centralized logging, unique request correlation IDs, and instrumentation for metrics, along with popular tools (ELK stack, Prometheus, Grafana, etc.). By implementing robust observability, architects ensure that when problems occur, the symptoms and contributing factors are transparent.

### 2.1 Logging Strategies and Best Practices

**Centralized and Structured Logging:** Every microservice should emit logs that can be aggregated and searched centrally (for example, using the ELK stack – Elasticsearch, Logstash, Kibana – or cloud logging services). Rather than storing log files locally, a **12-factor app** approach is recommended: treat logs as event streams, outputting to stdout/stderr and letting the execution environment collect and route them. This ensures logs from all services can be collated and analyzed together. Logs should be in a **structured format** (JSON or similar) to facilitate querying (e.g. by timestamp, severity, user ID, etc.).

**Log Levels and Content:** Architects should define conventions for log levels (INFO, DEBUG, ERROR, etc.) and ensure sensitive data is not logged. At INFO level, logs might include high-level lifecycle events (service start/stop, configuration loaded). DEBUG logs can be enabled temporarily for detailed traces. ERROR logs should include stack traces and key context for failures. It’s crucial to log **contextual information** – such as request IDs, user IDs, session IDs – so that events can be correlated across components.

**Correlation IDs for Distributed Tracing:** In microservices, a single user request often flows through multiple services. Implementing a **unique request ID** that is passed along call chains greatly aids troubleshooting. Each service, upon receiving a request (HTTP or messaging), should generate or propagate a correlation ID and include it in all log entries for that request. Spring Cloud Sleuth (in Spring Boot 2) or Micrometer Tracing (in Spring Boot 3+) can automate this, attaching trace IDs and span IDs to logs. By querying the central log store for a specific ID, architects can reconstruct end-to-end execution paths across services.

**Log Retention and Analysis:** Store logs in a centralized system where they can be kept for an appropriate retention period and easily searched. This enables post-incident forensics (e.g., finding when a particular error started and what changed in the system at that time). Use log analysis tools to set up **alerts** for certain error patterns or rate spikes (for example, trigger an alert if ERROR logs exceed a threshold per minute). Logs can also be used for trend analysis (as the 12-factor principles note, logs can be graphed to observe trends like requests per minute or error rates).

### 2.2 Metrics and Monitoring Systems

**Application Metrics:** Beyond logs, metrics provide numeric observability of system health. Spring Boot offers integration with **Micrometer**, a metrics collection library that can expose key metrics out-of-the-box (JVM memory usage, GC pauses, CPU, thread pool stats, HTTP request rates and durations, etc.). Using Spring Boot Actuator, one can easily expose a `/actuator/metrics` endpoint and even a `/actuator/prometheus` scrape endpoint. This allows a Prometheus server to periodically gather metrics from each service instance.

**Prometheus and Grafana:** **Prometheus** is a widely used monitoring system that scrapes metrics and provides a powerful query language (PromQL) for aggregating and alerting on metrics. **Grafana** can visualize these metrics in dashboards. Architects should define key **Service Level Indicators (SLIs)** like request throughput, average latency, error rate, memory usage, etc., and track them via Grafana dashboards. For example, a dashboard might show each microservice’s request rate vs. error rate, and JVM memory utilization over time. Prometheus can be configured to send alerts (via Alertmanager) when certain metrics breach thresholds (e.g., high error rate or low available memory).

Spring Boot’s Micrometer integration with Prometheus makes this straightforward – the app exposes metrics in Prometheus format, including custom metrics developers add. By hitting the `/actuator/prometheus` endpoint, one can retrieve all metrics in a text format. These include generic metrics (like `jvm_memory_used_bytes`) and any custom counters or timers defined in the code. **Distributed microservices monitoring** means deploying Prometheus to scrape each instance (potentially via Kubernetes service discovery), and aggregating the data for a global view.

**System and Infrastructure Metrics:** In addition to application-level metrics, monitor infrastructure metrics: CPU utilization, system load, container resource usage, network I/O, etc. Tools like **cAdvisor** and **Node Exporter** (for Kubernetes nodes) can feed Prometheus with container and host metrics. This helps differentiate whether a performance issue is due to the application code or an overwhelmed host (e.g., if CPU is at 100% or if container memory is hitting its limit). Ensure that **Tomcat metrics** (like active threads, request counts) are also exposed – Spring Boot Actuator can expose a thread dump or Tomcat stats via JMX, which can be scraped or logged if needed.

**Alerting and SLOs:** The monitoring system should support **alerting**. Define meaningful alerts to catch issues early: e.g., alert if a service’s error rate > 5% for 5 minutes, or if average latency > defined SLA, or if memory usage is close to Xmx limit. Tie these into on-call processes. From an SRE (Site Reliability Engineering) perspective, define **Service Level Objectives (SLOs)** for your services (such as 99th percentile latency) and use metrics to monitor compliance. This ensures the architecture meets its performance and reliability targets, and alarms when it drifts.

### 2.3 Distributed Tracing

**Need for Tracing:** In complex microservice architectures, even with logs and metrics, it can be challenging to pinpoint where a particular request is slowing down or failing. **Distributed tracing** complements the picture by recording causal relationships and timing information for each segment of a request’s journey through multiple services.

**Implementations:** Spring Boot (especially Spring Cloud) historically offered **Spring Cloud Sleuth** which integrates with tracing systems like Zipkin. In Spring Boot 3+, there’s built-in support via Micrometer Tracing and Brave or OpenTelemetry for trace data. Using **OpenTelemetry** is an emerging standard: one can instrument the services to export trace spans to a backend like Jaeger or Zipkin. Many APM (Application Performance Monitoring) solutions (e.g., Dynatrace, New Relic) also provide distributed tracing that works out-of-the-box.

**How it Works:** When a request enters Service A, a trace ID is created (or retrieved from incoming headers if it’s already in progress). A span (with a span ID) is started for Service A’s handling. When Service A calls Service B (e.g., via REST over HTTP), it passes the trace context (trace ID, current span ID as parent) to Service B (often via HTTP headers like `X-B3-TraceId`, `X-B3-SpanId` if using Zipkin/B3 propagation, or the W3C Trace Context headers). Service B then continues the trace with a child span, and so on. The result is a **trace** that connects all spans, showing the flow across services and how much time was spent in each. This is invaluable to locate which service or operation caused a latency spike or error.

**Using Traces in Troubleshooting:** When performance issues or errors arise that involve multiple components, consult trace data to see the end-to-end timeline. For example, you might find that a user request spends 50ms in Service A, then 2000ms in Service B – indicating a bottleneck in B. Or a trace may show that a call to an external API times out after 5 seconds, causing a chain reaction. Traces often visualize critical paths and can highlight where **cascading failures** occur (like many requests piling up on a single slow dependency).

Spring’s observability updates in Spring Boot 3 have made this easier: with Micrometer’s Observation API, you instrument once and get both metrics and traces. The architect should ensure that all microservices are configured to propagate trace context (Spring Cloud Sleuth does this automatically for supported clients like RestTemplate or WebClient). If using open standards, ensure consistency (e.g., if using OpenTelemetry, deploy a collector and use the same trace ID format across languages/services).

**Log Correlation:** A practical tip: integrate tracing with logging by outputting the trace ID in logs (as mentioned earlier). Spring Sleuth can add trace and span IDs to every log line. This way, even if you’re searching logs, you can group log entries by trace. As the Spring team emphasizes, correlating logs with traces greatly enhances debuggability.

### 2.4 Tooling: ELK, Prometheus, and Grafana Setup

**ELK Stack for Logs:** An effective setup for a Spring Boot microservices system is to have each container send its stdout (application logs) to a central log aggregator. Using **Filebeat/Logstash** to ship logs into **Elasticsearch** allows indexing of logs from all services. Kibana then provides a UI to search and create dashboards of log data. For example, you might create a Kibana dashboard showing the rate of ERROR logs per service, or to filter logs for a specific user session across services (using the correlation ID). Ensure the log fields (timestamp, level, service name, trace ID, etc.) are well-defined for easy filtering.

**Prometheus & Grafana for Metrics:** Each Spring Boot service with Actuator and Micrometer can be scraped by Prometheus. In Kubernetes, one might label each pod and use service discovery so Prometheus automatically finds new service instances. Grafana can then be connected to Prometheus as a data source. Create dashboards per service and aggregate ones:

- **Service dashboard:** CPU, memory, threads, GC activity, request rate, error rate, latency percentiles for that service.
- **System overview:** compare metrics across services (e.g., latencies or error rates, to spot if one service is the outlier causing a slowdown).
- **Database/dashboard:** if using a database, monitor DB-specific metrics (via Prometheus exporters or Actuator DB metrics).

**Alerting Setup:** Use Prometheus Alertmanager or an APM’s alerting feature to set up notifications (email/Slack/PagerDuty, etc.) when thresholds are crossed. For example, if the **thread pool** of Tomcat is saturated (Tomcat’s metric for active threads equals its maxThreads), or if **heap usage after GC** exceeds some limit consistently, alert the on-call team. Monitoring tools can also watch for anomalies (sudden changes) rather than static thresholds.

**Example – Monitoring a Spring Boot Microservice:** Suppose we have an order-processing microservice. We instrument it to record:

- Business metric: number of orders processed per minute.
- Performance metric: average time to process an order (perhaps using a Micrometer Timer around the service method).
- Resource metrics: JVM memory and Tomcat threads, via Actuator.
  All of these are exposed at `/actuator/prometheus`. Prometheus scrapes them and Grafana shows a panel for orders/minute, a panel for processing latency, and one for JVM memory. During a traffic surge, these dashboards might show orders per minute spiking, and perhaps latency increasing if the service is struggling. If an alert fires that latency is too high, architects can quickly check these dashboards: maybe it shows that CPU is maxed out or DB query time went up concurrently. This narrows down the cause (e.g., a specific dependency like the database is slow).

In summary, **investing in observability** is the foundation of strategic troubleshooting. With comprehensive logging, metrics, and tracing in place, architects and operators can efficiently pinpoint issues in complex Java/Spring Boot systems. The following chapters assume that these observability practices are in effect, as we delve into diagnosing specific types of problems such as performance bottlenecks or memory leaks.

## 3. Profiling and Diagnostic Tools for Java Systems

Even with good observability, certain problems require deeper inspection of the Java Virtual Machine (JVM) and the application internals. This chapter covers the **diagnostic and profiling tools** that architects should be familiar with. These tools range from those built into the JDK (like Java Flight Recorder, JDK Mission Control, jstack, jmap) to third-party profilers (like JProfiler, YourKit) and APM tools. We also discuss best practices for using these tools in production environments in a safe manner.

### 3.1 JVM Built-in Diagnostics

The JDK comes with a suite of troubleshooting utilities that can be used for monitoring and post-mortem analysis:

- **Java Flight Recorder (JFR)** and **JDK Mission Control (JMC)**: JFR is a low-overhead profiler built into the JVM that can record events related to CPU usage, memory allocation, garbage collection, thread states, I/O, locks, etc. It is designed to be always-on in production with minimal impact (usually <2% overhead for default profiling). JMC is a GUI tool to analyze JFR recordings. To use these, one can start a flight recording on a running application (for example, with `jcmd <pid> JFR.start` and later `JFR.dump`) or even configure the JVM to dump a recording on events like an **OutOfMemoryError**. The data from JFR is extremely rich; as Oracle’s docs note, no other tool gives as much profiling data with so little overhead. JFR data can be used to troubleshoot performance issues (see section 4) and memory leaks (section 5).

- **jstack (Thread Dump Utility)**: The `jstack` tool can capture a snapshot of all thread stack traces in a running JVM. This is critical for diagnosing **thread deadlocks, stuck threads, or thread pool exhaustion**. For example, if a service is unresponsive, an architect can run `jstack <pid>` (or send a kill -3 signal on Unix) to get a thread dump. The JDK’s built-in deadlock detector will analyze the dump and if any threads are in a circular deadlock, it will print a section like _“Found one Java-level deadlock:”_ with the threads involved and the locks they are waiting on. This immediate feedback pinpoints deadlocks. Even if no deadlock, inspecting thread dumps can reveal if threads are stuck waiting on external calls or locks. The `jstack -l` option includes lock information (showing which locks each thread owns or waits for). Architects should be comfortable reading thread dumps to spot patterns: e.g., many threads blocked on a certain class/method might indicate a bottleneck or synchronization issue.

- **jmap (Memory Map) and Heap Dumps**: `jmap` can be used to capture a heap dump of the JVM’s memory. If memory leak is suspected, taking a heap dump and analyzing it with tools like Eclipse MAT (Memory Analyzer) can reveal which objects are consuming memory and what is holding references to them. Additionally, `jmap -histo` can show a histogram of object counts by class in the heap (useful for a quick check if some class is growing unexpectedly). Generating heap dumps in production should be done carefully (it can freeze the application briefly and the dump file can be very large), but it is invaluable for **memory leak analysis** (discussed in Chapter 5).

- **jcmd Utility**: `jcmd` is a versatile command that can do operations like triggering a GC, dumping heap or threads, starting/stopping JFR recordings, etc., all in one tool. For example, `jcmd <pid> GC.heap_info` will print heap usage info, and `jcmd <pid> Thread.print` is analogous to jstack.

- **Java Mission Control (JMC)**: This GUI can attach to a running JVM (with JMX enabled) and provide live monitoring. It can display CPU, memory, and even live thread information, and it’s tightly integrated with Flight Recorder for analyzing recordings. JMC is an advanced tool that architects can use to do both real-time diagnostics and offline analysis of recordings.

- **VisualVM and JConsole**: VisualVM (which in some JDK distributions is packaged, or can be downloaded separately) provides a user-friendly UI to monitor a JVM’s threads, memory, and CPU in real time, and can trigger thread dumps or heap dumps. JConsole is a simpler JMX viewer that can show JMX MBeans – Spring Boot Actuator, for instance, exposes metrics via JMX which can be viewed in JConsole under the `metrics` domain.

Oracle’s Troubleshooting Guide documentation gives an overview of these tools and categorizes them by use case (monitoring vs post-mortem, etc.). For example, thread dump tools are under “Hung processes” investigation, and JFR under performance analysis.

**Using these in Production:** Many of these tools (JFR, JMX-based monitors) can be used while the application is running with minimal impact. However, thread dumps and heap dumps can be large; ensure the system has enough disk space and watch out for pauses. It’s often best to capture data during an incident and then analyze offline. Always test these tools in staging to understand their impact.

### 3.2 Third-Party Profilers and APMs

**Java Profilers (JProfiler, YourKit, etc.):** Third-party profilers attach to a JVM (often via the Java Debug Interface) and can collect detailed information about CPU usage per method, memory allocation hotspots, and more. Tools like **JProfiler** or **YourKit** have both live monitoring and offline analysis capabilities. They provide features like:

- CPU sampling or instrumentation to find which methods are consuming the most CPU time.
- Memory analysis to find allocation rates and potential leaks.
- Monitoring of JDBC calls, HTTP calls, etc., if integrated with frameworks.

These profilers are excellent for deep dives (for example, to optimize a specific piece of code or to trace a complex memory leak). However, they typically incur more overhead than JFR, so they are used in controlled environments (or in production during off-peak hours with caution). An architect might use these in a staging environment with production-like data to reproduce a performance issue and identify the slow method or inefficient algorithm.

**Application Performance Monitoring (APM) tools:** Products like New Relic, AppDynamics, Dynatrace, or Elastic APM provide agent-based monitoring. A Java agent is attached to the JVM which instruments common frameworks (Servlet calls, Spring beans, database calls, etc.) to automatically collect performance metrics and traces. APMs give a high-level view: transaction response times, slowest operations, error rates, and often can pinpoint slow database queries or external calls. They often have nice dashboards and can be easier to use for continuous monitoring than running manual profilers. Major tech companies often build custom APM solutions to meet their scale; open-source options (Pinpoint, Apache SkyWalking, etc.) also exist.

From an architect’s viewpoint, an APM can be a great help: for example, seeing that 40% of response time is spent in database queries vs 60% in application logic guides where to optimize. APMs also often detect errors and provide the stack trace where they occurred, which helps with quick root cause identification.

**JVM Monitoring Tools:** In addition to full APMs, there are lighter tools like **GC Easy** (for analyzing GC logs) or **Glowroot** (an open source APM-lite). There’s also **Netflix’s Vector** tool for visualizing system and JVM counters over time. Tools that analyze **GC logs** can transform verbose GC output into understandable metrics like GC frequency and pause time percentiles.

### 3.3 Best Practices for Profiling and Monitoring

**Profile in Pre-production:** It’s advisable to run load tests in a staging environment and profile the application to discover hot spots before they become production issues. Use JFR or profilers during these tests to capture how the system behaves under load (CPU hotspots, memory churn, etc.). This can uncover, say, an inefficient sorting algorithm that only becomes noticeable at high volumes.

**Continuous Monitoring vs On-Demand Profiling:** Some tools (APMs, JFR in continuous mode) are running all the time. Others (thread dumps, heap dumps, JProfiler) you use when needed. A good strategy:

- Keep JFR running in continuous recording with a rolling buffer in production (since its overhead is minimal). This way, if something goes wrong, you can dump the recording to see what was happening before and during the incident. In fact, when an OOM error happens, the JVM can dump a JFR recording automatically (with `-XX:StartFlightRecording` and appropriate settings).
- When alerted of a problem, use jstack (or better, automated thread dump collectors) to quickly check thread states. If the problem is a hang or deadlock, thread dumps will reveal it (the deadlock detection in thread dumps is very handy). Some monitoring setups take thread dumps periodically and even analyze them for common issues (e.g., some APMs can show if a thread is stuck for too long).
- If memory issues are suspected (e.g., memory usage climbs over time), enable additional monitoring like `-Xlog:gc*` to log GC details or use jmap to get histograms over time. You might schedule a heap dump when certain conditions met (though be mindful of performance).
- Use remote JMX connections for non-intrusive monitoring. For instance, via JMX you can observe memory usage and even invoke operations like triggering a garbage collection or retrieving specific metrics. Ensure secure JMX (since opening JMX in production can be a security risk if not protected).

**Combining Data Sources:** Often, solving an incident requires correlating multiple data sources: logs, metrics, thread dumps, etc. For example, suppose a service is experiencing slow responses. Metrics show high latency and thread pool saturation; logs show many timeouts calling another service; a thread dump shows many threads stuck waiting on an HTTP client. Putting this together, you deduce that calls to Service X are hanging and exhausting threads – perhaps Service X is down or slow (an integration issue). This illustrates how the observability (Chapter 2) and diagnostics (Chapter 3) tools work in tandem for effective troubleshooting.

Finally, document the insights gained from using these tools. If a particular profiling session uncovered an inefficiency, capture that knowledge (and ideally, add automated tests or checks to catch regression). The goal is not just to fix one incident, but to feed that back into architectural decisions (e.g., “We need better caching here” or “We should break this lock into smaller locks to avoid contention”).

With observability (Chapter 2) and diagnostics (Chapter 3) in place, we now move into specific categories of issues, starting with performance bottlenecks.

## 4. Common Performance Bottlenecks and Tuning

Performance issues can manifest as **slow response times, high CPU usage, poor throughput, or unresponsive services under load**. This chapter examines common causes of performance bottlenecks in Java Spring Boot applications and how to troubleshoot them. We consider CPU-bound and IO-bound bottlenecks, database performance, thread pool sizing, and caching. We also discuss how to tune the system (and JVM) to alleviate these issues, and how to verify improvements.

### 4.1 Identifying Bottlenecks: CPU, I/O, or Other?

The first step is to identify what kind of bottleneck you are facing. According to Oracle’s performance troubleshooting guide, different applications have different bottlenecks – some are limited by **I/O or network latency**, others by **thread synchronization**, others are purely **CPU-bound**, and some by **garbage collection pauses**. It is also possible to have multiple bottlenecks at once.

Key symptoms and indicators:

- **High CPU Utilization**: If your service’s CPU is maxed out (one core at 100% or all cores near saturation), and response times are slow, you likely have a CPU-bound bottleneck. This could be due to inefficient code (e.g. algorithms that are O(n^2) on large inputs), or simply heavy load that exceeds capacity. Tools: JFR or a profiler can show which methods are consuming CPU. Perhaps an expensive operation (like JSON serialization, encryption, image processing, etc.) is a hotspot.
- **High Latency with Low CPU (Possible I/O Bottleneck)**: If threads are mostly waiting (CPU is moderately used or low, but the service is slow), the bottleneck could be external – waiting on database queries, waiting on network calls, or waiting on file I/O. In thread dumps, many threads might be in a WAITING or BLOCKED state on socket reads. Metrics might show that calls to a particular dependency (DB, another microservice) are slow.
- **Thread Contention / Synchronization**: If CPU isn’t fully utilized and you suspect threads are contending (maybe many threads trying to access a synchronized block or a common resource), you might see thread dumps where threads are BLOCKED on a lock held by another thread. JFR’s **synchronization events** or the JDK’s `jfr print` can highlight if a lot of time is spent contending on locks. Alternatively, a code hotspot may not be CPU but rather waiting for monitors – a sign to consider reducing lock scope or using more granular locks or lock-free structures.
- **Garbage Collection Overhead**: If the application is pausing frequently for GC, it can degrade throughput and latency. Symptoms include increasing GC frequency and pause times visible in GC logs, and perhaps high CPU usage in GC threads (but not in your code). If GC is the bottleneck, one might see that a lot of time is in GC and not in actual work. This can happen if the heap is under-provisioned or if there’s a lot of allocation churn. The Oracle guide mentions GC time as a potential bottleneck equal in importance to CPU or IO waits.

To systematically find bottlenecks, JFR is helpful. Oracle suggests looking at events such as I/O, method profiling, lock profiling in the flight recording. For example, events like `jdk.SocketRead` or `jdk.DBQuery` could show where time is spent.

### 4.2 CPU-Bound Issues and Optimization

When the CPU is the bottleneck, the approach is:

- **Locate the Hot Code Path:** Use a profiler or JFR method sampling to find which methods or code paths are using the most CPU time. Often a small number of methods consume the majority of CPU. For instance, you might find a particular loop or a stream processing operation that’s expensive.
- **Assess Algorithmic Complexity:** Ensure that any CPU-intensive logic has acceptable complexity. A common surprise in enterprise apps is an inadvertent **N+1 query problem** (which is partly CPU and partly DB) – where an ORM like Hibernate loads data in a suboptimal way (multiple queries when one could do) – leading to a flurry of CPU activity in both the app and DB. Such an issue can often be fixed by changing fetch strategies or query methods (e.g., using a join fetch to avoid N+1 selects). The JRebel blog notes N+1 problems can sometimes be resolved by a simple configuration change.
- **Caching Results:** If profiling reveals repeated computations, consider caching. Spring Boot apps can use Spring Cache to memoize the results of expensive operations (e.g., an expensive calculation or a remote call result that doesn’t change often). But use caching judiciously – ensure the cache has eviction policies to avoid memory issues.
- **Increase Parallelism (if possible):** If the code can be parallelized and the CPU bottleneck is due to single-threaded processing, using more threads or asynchronous processing might help (assuming CPU cores are available). For CPU-bound tasks, the maximum useful threads roughly equals number of CPU cores (since more threads than cores can lead to context switching overhead). With the introduction of virtual threads in Java (Project Loom, JDK 19+), some CPU-bound workflows might be structured differently, but as of 2025, traditional threading is still widely used.
- **Native or GPU Offloading:** In extreme cases of CPU-heavy tasks (like image/video processing), consider native libraries or offloading to specialized systems. This is more of a design consideration.

**Example:** A Spring Boot service was spending 70% of its CPU time in JSON serialization of a large response object. The architect could address this by either simplifying the object graph (thus reducing serialization work), enabling compression (to trade CPU for network – but that would actually increase CPU), or using an alternative JSON library that’s faster. Another example: using parallel streams or completable futures to make use of multiple cores for independent tasks in a request.

After changes, always re-run tests to see if the CPU usage and response times improved.

### 4.3 I/O and Database Bottlenecks

I/O (network or disk) often dominates microservice performance:

- **Database Bottlenecks:** The most common case: queries are slow or the database is overloaded. Symptoms include high response times that largely consist of waiting for DB results. If using an ORM like Spring Data JPA/Hibernate, enable SQL logging to see what queries are being run. You might discover missing indexes (causing full table scans), or queries that return far more data than needed. The solution may be to add indexes, optimize the query, or use caching for read-heavy scenarios. Also consider the **N+1 queries** mentioned: use JOINs or batch fetch to reduce repetitive queries. If the DB is a shared resource across microservices, it may itself be overloaded – scaling the database or introducing read replicas could be needed.
- **External Service Calls:** If a microservice depends on third-party APIs or other internal services, those calls can become a bottleneck if they are slow or unreliable. One slow downstream can slow the entire user request (we will discuss timeouts and circuit breakers in the Resilience chapter). To troubleshoot, measure the latency of each external call (use metrics or APM breakdowns). If Service A calls Service B and is slow, look at Service B’s performance or network latency between them.
- **Disk I/O:** Less common in microservices (since typically you don’t do heavy disk ops in a stateless service), but things like writing logs (synchronous disk I/O) or loading large files can cause delays. Ensure any file access isn’t on a hot path (and consider asynchronous logging to not block the main thread).
- **Thread Pool Exhaustion due to I/O**: In a classic Spring MVC app with Tomcat, each HTTP request is handled by a thread from the Tomcat thread pool. If those threads spend a long time waiting on I/O, you could run out of threads to handle new requests. This is effectively a performance bottleneck – throughput stalls because all threads are tied up. A thread dump would show many threads in states like WAITING on a socket read. One solution is to use an asynchronous/non-blocking approach (Spring WebFlux or reactive programming) so that waiting doesn’t block threads. But absent a full reactive rewrite, the immediate mitigations are: tune thread pool size and enforce timeouts so threads don’t get stuck indefinitely (more on timeouts later). **Note:** Simply increasing thread pool size can help if the external latency is not too high and the server has enough resources, but it’s a band-aid if the external call is extremely slow or hangs.

**Performance and Capacity Planning:** Use load testing to understand at what point your service saturates. For example, you might find that at 200 requests per second, CPU is fine but DB CPU goes to 90%. That tells you the database is your bottleneck at that load. You could then plan to scale the database or refactor the service (maybe use caching or CQRS to reduce DB load).

One should also be aware of the **“fallacies of distributed computing”** – one of which is that latency is zero and bandwidth is infinite. In reality, network calls add latency. In microservices, doing things that were once in-process method calls may now be REST calls across the network, potentially adding tens of milliseconds each. If you chain many microservices, those latencies add up. As an architect, consider the depth of call chains – overly chatty communication can kill performance. It might be better to combine some services or use async messaging to reduce synchronous wait time.

A pattern to watch out for is **over-chattiness** between microservices (similar to N+1 but at service scale). E.g., Service A needs data for 100 items and calls Service B 100 times (synchronously) – this will be slow and heavy. A better design is to allow a batch request. If you spot such a pattern in traces or logs, consider redesigning the interface.

### 4.4 Thread Pool Tuning (Tomcat and Async Executors)

**Tomcat Thread Pool:** By default, Spring Boot’s embedded Tomcat uses a fixed thread pool (the **maxThreads** setting, default \~200). If your service is I/O heavy (e.g., waits on DB or network), you might benefit from having more threads to handle concurrent requests up to a point. However, more threads mean more memory and context switching overhead. If your threads often block on I/O, having too few threads will underutilize CPU but throttle throughput. Having too many threads can overwhelm the CPU scheduler and even the DB (if they all make DB calls simultaneously).

Monitor the Tomcat threads: Spring Boot Actuator has a `/actuator/threaddump` and metrics for Tomcat threads. If you frequently see all threads busy and requests queuing, that’s a sign to possibly increase maxThreads (and/or investigate why each request is slow). Conversely, if threads are mostly idle, increasing them won’t help.

One advanced Tomcat feature: using an **Executor** (a shared thread pool) instead of separate thread pools per connector. When using a thread pool per connector, Tomcat does not shrink the pool once it grows; a sudden spike can cause the pool to expand and those threads remain for the life of the JVM. Using a shared executor, threads can be reused across connectors and potentially reduced when idle. For most Spring Boot apps with one HTTP connector, this isn’t critical, but if you have multiple connectors/protocols it’s worth considering. The key point is to **monitor and right-size the thread pools** – ensure enough threads to handle the expected concurrency, but not so many as to waste resources. Tomcat’s internal performance can degrade if you have far too many threads (because of contention on internal structures).

**Async and Worker Thread Pools:** Spring Boot apps often use additional thread pools, e.g., via `@Async` methods or scheduling tasks. These should also be tuned. A common issue is creating an Executor with not enough threads or an unbounded queue which can lead to tasks queuing up. If using such async tasks for background work, monitor their execution time and completion.

**Project Loom (Virtual Threads):** It’s worth mentioning that Java’s new virtual threads (available in Java 19+ as preview, and potentially production-ready in Java 21/22) allow a different model where each request could use a lightweight thread without worrying about the cost of blocking. This can simplify tuning because you don’t have to manage small thread pools – you can spawn many virtual threads. However, at the time of writing (2025), many frameworks (including Spring) are adapting to Loom; it’s an emerging option to watch for to handle I/O-bound concurrency more gracefully (some resources compare traditional thread pools vs virtual threads). For now, though, tuning traditional pools is still relevant.

### 4.5 Caching and Content Delivery

**Caching Layers:** A high percentage of performance issues can be alleviated by introducing caching at various levels:

- In-memory caches in the application for frequently accessed data that is expensive to compute or fetch. Spring’s `@Cacheable` abstraction (with providers like Caffeine, Ehcache, etc.) makes this easy. Just be cautious with memory (Chapter 5 covers memory leak potential if caches grow without bounds).
- Distributed caches or databases like Redis or Memcached to offload frequent read requests from the primary database.
- HTTP response caching or use of a CDN (Content Delivery Network) for static content, if applicable.

An architect should identify data that is read often but changes rarely – ideal for caching. For example, configuration data or reference data (like a list of countries) could be cached instead of querying DB every time. In microservices, caching can also happen at the client side – e.g., if Service A calls Service B for some info that doesn’t change often, Service A might cache those results for a short time.

**Pooling Resources:** Similar to caching, make sure to use **connection pools** for external resources. For databases, using a JDBC connection pool (HikariCP is default in Spring Boot) is essential for performance – establishing a DB connection is expensive. Ensure the pool is sized correctly (too small -> wait time for a connection; too large -> DB overloaded). Tomcat’s JDBC connection pool or Hikari’s settings like `maximumPoolSize` should be tuned according to expected concurrent DB usage. Monitor if the pool is exhausted frequently (Actuator can expose metrics for active vs idle connections).

For HTTP calls to other services, similarly, use connection pooling (HTTP client libraries often have pooling by default or configurable). Creating new TCP connections for each request adds latency.

**Compression and Transfer Optimization:** In web services, enabling GZIP compression for responses can trade CPU to reduce network time. Tomcat allows setting `compression="on"` for connectors. This helps if responses are large (like JSON payloads). The eG Innovations guide notes that text-based content can often be compressed up to 90%, greatly reducing network latency for clients. However, compression uses CPU – ensure CPU headroom or do it selectively for large payloads.

**HTTP/2 and Asynchronous Responses:** If using Tomcat 9+/Spring Boot with HTTP/2 enabled (often via SSL), it can improve throughput by multiplexing requests over fewer connections. Also consider if some endpoints can be made asynchronous (Spring WebFlux or Servlet 3 async) to allow one thread to handle other work while a response is being prepared (useful when combining data from multiple sources).

### 4.6 Garbage Collection and Memory Tuning for Performance

Though memory is discussed in Chapter 5, it intersects with performance. A poorly tuned garbage collector can cause high pause times (thus latency spikes). The choice of GC algorithm matters:

- The current default in recent JDKs is **G1GC** (Garbage-First Garbage Collector), which balances throughput and pause time. For most, G1 is a good default. If ultra-low pause times are needed, **ZGC** or **Shenandoah** are new collectors offering very low pause but at the cost of more CPU usage in the background. The eG guide suggests using modern GCs like G1 or ZGC for best performance.
- **GC pause tuning:** G1 allows a target max pause time (`-XX:MaxGCPauseMillis`). Setting this to, say, 200ms or 100ms can guide the GC to try to stay under that pause length. Shorter target means more frequent GCs (lower pause each time, but possibly more CPU overall). A value between 500–2000ms is recommended in one guide if you want to balance throughput and latency. If low latency is priority (e.g., for UI or interactive services), aim for lower pause (e.g., 100-200ms). Always measure – if GC is using >5% of CPU time, that’s considered a lot and might hurt performance.
- **Heap sizing:** Ensure the JVM has enough heap (`-Xmx`). If the heap is too small for the working set of the application, the JVM will spend a lot of time garbage collecting (trying to free memory) and possibly throw OutOfMemoryErrors. On the other hand, too large a heap can cause long GC pauses for some collectors (though G1 and ZGC scale better to large heaps).
- **Monitoring GC:** Enable GC logging (e.g., `-Xlog:gc*:file=gc.log:time`) to capture GC events. You can post-analyze these logs with tools to see how often major GCs occur and how long they pause. If you see repeated long pauses, it might be necessary to adjust GC algorithm or parameters.

**Example:** Suppose under heavy load, you notice latency spikes every few seconds. GC logs reveal full GCs of 1.5 seconds happening often. This indicates a problem – maybe old generation is too full. Solution might be to increase heap or tune G1 (or switch to a no-pause collector like ZGC if using JDK17+). After tuning (increasing Xmx and setting a pause target), you observe full GCs are rare or <0.2s, smoothing out latency.

### 4.7 Case Study Summary (Performance)

Let’s summarize common performance issues, their causes, and fixes in a table for clarity:

| **Performance Issue**             | **Symptoms**                                                                             | **Common Root Causes**                                                                                                                                    | **Resolution Strategies**                                                                                                                                                                                                                                                     |
| --------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High CPU, slow responses          | 100% CPU utilization, threads active                                                     | Inefficient algorithms or code (e.g., N^2 loops), lack of caching, heavy JSON processing, small thread pool with CPU-bound tasks causing context switches | Profile to find hot methods; optimize code or algorithms (e.g., use better data structures); add caching for repetitive computations; increase threads only up to core count for CPU tasks; consider native optimization if needed.                                           |
| High latency, low CPU (IO-bound)  | Threads waiting, request timeouts                                                        | External calls slow (DB, API); network latency; N+1 service calls; single-threaded waiting on IO                                                          | Tune database (add indexes, optimize queries); batch calls to downstream instead of many small calls; increase thread pool for handling more concurrent IO; use asynchronous IO or reactive to avoid blocking threads; set timeouts so stuck IO doesn’t hold threads forever. |
| Thread pool starvation (blocking) | Many requests queued, thread count at max, throughput plateaus                           | Too many threads waiting on slow IO or locks; no timeouts on external calls causing threads to hang                                                       | Increase maxThreads (if CPU/memory allows) to handle more concurrent waits; use timeouts on external calls to free threads; consider breaking work into smaller async tasks. In long term, consider reactive programming to reduce thread usage for waits.                    |
| Database throughput issues        | High DB CPU, slow queries, or frequent DB timeouts                                       | Missing indexes; N+1 query pattern from ORM; insufficient caching; DB connection pool exhausted                                                           | Analyze slow queries (use APM or logs); add indexes or rewrite queries; use second-level cache or app-level caches for frequent reads; tune connection pool size to match DB capability and app needs.                                                                        |
| Frequent GC pauses                | Periodic latency spikes, “Stop-the-world” logs in GC log, GC taking significant CPU time | Heap too small for workload causing continuous GC; use of old GC algorithm with long pauses; excessive object churn (allocations)                         | Increase heap memory if usage justifies it; switch to G1GC (or ZGC for low-pause); tune GC pause target (MaxGCPauseMillis) to acceptable value; optimize code to allocate less garbage (reuse objects, etc.) if allocation rate is extreme.                                   |
| Network bandwidth saturation      | High network I/O, throughput drops when data size large                                  | Transferring large payloads (images, large JSON) frequently; lack of compression or paging                                                                | Enable GZIP compression for text responses; use streaming or pagination for large datasets; consider CDN or moving large data transfer out of synchronous request path.                                                                                                       |

_Table 4.1: Common Performance Problems, Causes, and Solutions_

Performance tuning is often iterative: identify the bottleneck, fix or mitigate it, then find the next one. Importantly, always verify that your changes don’t negatively impact other aspects (e.g., caching improves speed but watch out for memory growth). Also maintain a holistic view – sometimes the issue isn’t in the microservice at all but in how clients use it (e.g., sending too many requests, or not handling responses efficiently). An architect’s role is to ensure the system as a whole meets performance requirements, which might involve coordinating changes across multiple services or components.

Now that we’ve covered performance, we move on to memory-related issues, which often intertwine with performance but have their own distinct troubleshooting approaches.

## 5. Memory Management Issues and GC Tuning

Memory problems in Java can be tricky – they often develop over time and can lead to severe outages (OutOfMemoryError crashes) or performance degradation (excessive garbage collection). In this chapter, we cover **memory leaks**, **garbage collection tuning**, **OutOfMemoryError troubleshooting**, and related aspects like object pooling. We also consider Spring/Tomcat specific memory considerations (like classloader leaks on redeploys).

### 5.1 Understanding Memory Leaks and OutOfMemoryErrors

A **memory leak** in Java is typically when the application unintentionally retains references to objects that are no longer needed, preventing the garbage collector from reclaiming that memory. Over time, such leaks cause the heap usage to grow until it fills up, resulting in an `java.lang.OutOfMemoryError: Java heap space`. It’s important to note, however, that not every OutOfMemoryError (OOM) is caused by a leak; it could simply be that the application really needed more memory than was configured.

As the Oracle documentation explains, an OOM is thrown when the GC can’t allocate a new object and the heap can’t be expanded further. This can happen either because:

- **True Memory Leak**: Objects that are no longer needed are still referenced (due to a bug), so the heap fills up over time.
- **Insufficient Heap**: The application legitimately needs more memory (maybe due to large data or caches) than what’s been allocated by `-Xmx`. In this case, the OOM does not imply a leak; the solution may be to increase heap or reduce usage.
- **Native Memory Issues**: Sometimes OOM is thrown for off-heap reasons (native allocations, or Metaspace in Java 8+ if class loading is excessive). The error message in the exception usually indicates the area (“Java heap space” vs “Metaspace” vs others).
- **Garbage Collector Overhead Limit**: In rare cases, if the JVM spends too much time in GC with little result (e.g., >98% time in GC freeing <2% heap), it can throw an OOM to signal it’s overwhelmed.

**Memory Leak Impact:** A leak often shows as gradual performance degradation: as memory fills, garbage collections become more frequent (to free up space) and response times may suffer, until eventually an OOM crash or severe slowdown occurs. Memory leaks can also cause out-of-memory failures in containers if memory usage exceeds container limits.

**Common Causes of Memory Leaks:**

- **Unbounded Object Storage**: For example, using a `static` `List` or `Map` to accumulate data and never removing entries. Static collections live for the life of the JVM, so if they grow, that memory is never freed unless explicitly cleared.
- **Unreleased Resources**: Not closing JDBC connections, file handles, etc. If these accumulate, not only do you risk running out of those resources, but also associated memory may not be freed. For instance, each open connection might have buffers.
- **ThreadLocal Misuse**: Using `ThreadLocal` variables and not removing them properly can cause leaks, especially in app servers. If a ThreadLocal references a heavy object, and the thread is from a pool that lives forever, that object stays in memory even if logically not needed. (In web apps, ThreadLocal leaks are notorious when using thread pools across deployments).
- **Long-lived Threads**: Spawning threads that never stop can hold onto references. E.g., a background thread that has a reference to the Spring ApplicationContext or some big object will prevent those from being GCed. In a Spring Boot app, if you start threads manually, ensure they either end or don’t hold large references.
- **Caching without bounds**: Caches that grow indefinitely can exhaust memory. Always use size limits or TTL (time-to-live) on caches. E.g., an in-memory cache of user sessions that never evicts old sessions will leak memory.
- **Library bugs or improper use**: Sometimes third-party libraries can cause leaks if not used properly (e.g., failing to deregister drivers or MBeans on shutdown).
- **ClassLoader leaks (in redeploy scenarios)**: In environments where you deploy multiple apps or reload apps (like an external Tomcat or JEE server), classes from old deployments might stay in memory if the app doesn’t clean up static references or if threads aren’t stopped. For example, each web app has a classloader; if a class in the app registers a JDBC driver or starts a Thread that isn’t stopped, that classloader can’t be garbage collected, leading to a **permgen/metaspace leak**. Mark Thomas (Tomcat developer) points out that webapps must deregister JDBC drivers on shutdown; if not, Tomcat will try to do it. Also, threads started by the webapp carry the webapp’s classloader as context, so if not stopped, they pin the classloader in memory. (In Spring Boot’s self-contained model, you typically restart the whole JVM on redeploy, so classloader leaks are less of an issue there, but it’s relevant if using external containers or an OSGi environment).

IBM’s documentation categorizes memory leaks in Java EE apps as thread/ThreadLocal leaks, classloader leaks, system resource leaks, connection leaks, etc.. This captures that leaks can happen in various areas – not just heap objects, but also threads or native resources.

### 5.2 Detecting Memory Leaks

**Monitoring and Metrics:** Keep an eye on memory usage metrics over time. If heap usage after full GCs steadily rises release over release or day over day in a long-running service, that’s a red flag. Tools like Prometheus can track the JVM’s used heap. Also, monitor GC frequency: increasing GC activity could indicate growing live set. Java’s **Objects Pending Finalization** metric (and the `Finalizer` queue) should be near zero; if it grows, it means objects with finalizers aren’t being collected (could hint at certain leaks like unclosed streams).

**Heap Dumps:** As mentioned earlier, a heap dump is the most direct way to find leaks. Generate a heap dump when memory usage is high (but before OOM if possible). Then use a memory analyzer:

- Look at the largest objects (by retained size). For example, you might find a `ArrayList` with millions of entries of some DTO class – then you trace who holds that list. Maybe it’s a static field.
- Look at the dominator tree: find which objects are preventing a lot of other objects from being freed.
- Many profilers can also do heap analysis. Some APMs will automatically capture heap dumps on OOM.

**JDK Flight Recorder (JFR):** JFR can help with leaks by capturing object allocation information and even identifying objects that survived multiple GCs (old objects). It has an event for “Old Object Sample” which can show objects that have been in the heap for a long time. In JMC, you can use the Leak Suspects analysis which leverages this to pinpoint likely leaks. For instance, as Oracle’s guide shows, you can identify the class of objects that keep growing and see their allocation stack trace. JFR can be run continuously and doesn’t cause much overhead, which is great for capturing data leading up to a leak.

**Step-by-Step Leak Diagnosis:**

1. Notice signs of a leak (memory not being freed, OOM errors).
2. Trigger a full GC (using `jcmd <pid> GC.run` for example) and see if memory comes down significantly. If not, likely those objects are referenced.
3. Take a heap dump.
4. Analyze with MAT or JVisualVM:

   - Use “Leak Suspects Report” (MAT has this) – it often identifies big collections or large retained sets.
   - Look at the path to GC roots for suspect objects. That tells you what is holding them. For example, you find `HashMap` X is held by static field Y of class Z. Then you know where in code the leak is.

5. If heap dumps are huge or production can’t pause, consider doing a smaller scale test that simulates the leak (if you have an idea of what triggers it) and dump heap there.

**Common findings:**

- Static collections not cleared.
- Listeners not removed (e.g., adding listeners to some static manager and never removing).
- Misuse of caches (e.g., using `ConcurrentHashMap` as cache without eviction).
- ThreadLocal holding heavy objects and threads staying alive in pool.

A concrete example from the field: A Spring Boot app had an ever-growing memory footprint. Heap dump revealed millions of `org.springframework.security.core.context.SecurityContextImpl` objects. The cause was that the security context was being stored in a ThreadLocal but never cleaned up properly after requests when using a custom thread pool. The fix was to clear the ThreadLocal at end of request or use the framework’s mechanisms correctly. This illustrates how thread-associated data can leak if not managed, especially in asynchronous setups.

### 5.3 Garbage Collection Tuning

We touched on GC in performance, but here specifically in the context of preventing memory issues:

- **Choose the Right GC for the Job:** For most web services, the default G1 GC is fine. If you require low latency and have a large heap, consider ZGC (JDK 15+) which can handle very large heaps with minimal pause (often sub-10ms pauses). G1 works well up to several gigabytes heap with manageable pauses.
- **Metaspace and Classloader**: If you see OOM for Metaspace, increase metaspace size or (if in a redeploy scenario) look for classloader leaks. Metaspace OOM in Spring Boot standalone is rare unless you’re dynamically loading lots of classes.
- **Tune Heap Regions** (advanced): G1 has parameters like region size, initiating heap occupancy percent, etc. These typically don’t need tweaking unless you have special allocation patterns. Monitor GC logs first to identify problems.
- **Promotion and Allocation Failure:** Look at GC logs for terms like “to-space exhausted” or “promotion failed” which indicate issues in collector.
- **Explicit GC and System.gc():** Avoid calling System.gc() in production – it forces full GCs and usually hurts performance more than helps. If an external process calls it (like via JMX), consider disabling explicit GC calls via `-XX:+DisableExplicitGC`.

**Memory vs. Performance Trade-off:** Sometimes to fix memory issues, you reduce caches or limit data, which could impact performance because you have to recompute more often or fetch from DB more. It’s a balance. For instance, a huge cache might eliminate DB calls (good for performance) but may eventually crash the app (bad for availability). The architect’s job is to find the right size – often using production data to decide (like if only top 1000 items are hot, you cache those, not everything).

### 5.4 Tomcat and Spring-specific Memory Concerns

**Tomcat Memory Leak Prevention:** Tomcat (when used as an external server with webapps) has features to detect common leaks on redeploy. It will log warnings like “The web application \[XYZ] created a ThreadLocal with key of type \[abc] (value \[def]) but failed to remove it when the web application was stopped. This is likely to create a memory leak.” These logs are valuable if you ever see them – they literally point out leak suspects. In embedded mode (Spring Boot), these issues manifest as general leaks since the app doesn’t reload, it just dies on exit.

**Large HTTP Sessions:** If you use HTTP sessions (less common in stateless microservices, but possible), they can accumulate lots of data. A user with a very large session or many active sessions can be a memory hog. Solution: distribute sessions (if in cluster) or use external session store (Redis) or simply keep session data minimal.

**Spring Bean Lifecycle:** Typically Spring doesn’t leak memory – beans live as long as the context (usually the whole app uptime). But if you’re creating new ApplicationContexts at runtime (rare in microservices), be careful to close them to avoid classloader leaks.

**Data Volume and Batching:** A pattern that can cause memory spikes is reading a huge data set into memory for processing (e.g., reading 100k database rows into a list). This can OOM if not sized right. It’s better to stream or batch such processing. Spring Batch or streaming APIs (like Java 8 Streams backed by database cursors, or using JDBC fetch size) can help.

### 5.5 Handling OutOfMemoryError in Production

If an OutOfMemoryError occurs in production:

- The JVM might not kill itself immediately if it’s just a heap OOM within a thread (though often certain parts of Spring or Tomcat will catch it and may shut down). But usually, after OOM, the process is in a bad state (some tasks could not allocate memory). The best course is typically to **restart the service**. Ensure your orchestration (Kubernetes, etc.) treats OOM as a reason to restart the container.
- Configure the JVM to generate a heap dump on OOM (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/path/to/dumps`). This way, you get a snapshot at the moment of failure for analysis.
- Also use the JVM option `-XX:OnOutOfMemoryError="<command>"` if you want to perform some action (like sending an alert or copying logs) on OOM.
- After a restart (short term fix), analyze the heap dump offline to find the leak and deploy a fix.

**Memory and Containers:** When running in Docker/Kubernetes, ensure the JVM is aware of container memory limits. Modern JVMs (Java 10+) do this by default (they read cgroup memory limits). On older Java 8, you had to set `-XX:+UseContainerSupport` (in later 8u releases) or manually size Xmx. If not, the JVM might think it has the whole host memory and hit the cgroup limit leading to container OOMKill (which is different from a Java OOM exception). Always set Xmx a bit below the container’s memory limit to give room for GC and native overhead. Use also `-XX:MaxDirectMemorySize` if your app heavily uses NIO direct buffers so that doesn’t grow unbounded.

### 5.6 Summary of Memory Issue Mitigation

In summary, memory issues require careful monitoring and sometimes deep analysis:

- Use tools like heap dump analyzers and JFR to find leaks.
- Follow best coding practices: close resources, avoid unnecessary static mutable state, limit cache sizes, use ThreadLocals carefully.
- Choose appropriate garbage collector and tune if necessary to balance throughput and pauses.
- Test under load and long-duration tests to catch slow leaks.

Let's compile some of these into a quick reference table:

| **Memory Issue**                    | **Symptom**                                                                           | **Root Cause**                                                                                                                    | **Resolution**                                                                                                                                                                                                                                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Gradual heap growth (memory leak)   | Heap usage climbs over time, OOM eventually, frequent GCs with little freed memory    | Unintentional references preventing GC (static collections, ThreadLocal, etc.), or unbounded caches                               | Identify leaking objects via heap dump (find large retained objects and GC root paths). Fix code: remove or clear static references, use weak references if appropriate, add cache eviction, remove ThreadLocals on thread end.                                                                        |
| OutOfMemoryError – Java heap        | Crash or error “Java heap space”                                                      | Could be leak, or simply too much data load for heap, or very slow memory leak in long run                                        | If not a leak, increase Xmx or reduce usage (e.g., process data in streams). If leak, see above. Use `HeapDumpOnOutOfMemoryError` to capture dump for analysis.                                                                                                                                        |
| OutOfMemoryError – Metaspace        | OOM with metaspace, often after redeploys                                             | Classloader leaks (classes from old deployments not unloaded)                                                                     | Fix: ensure proper resource cleanup on undeploy (stop threads, deregister drivers). Increase MaxMetaspaceSize as a stop-gap. In Spring Boot (fat jar), metaspace OOM likely indicates excessive dynamic class generation (could be frameworks like ByteBuddy, etc. – analyze what classes are loaded). |
| High GC time (not enough memory)    | Application slow, GC running constantly (e.g., GC logs show back-to-back collections) | Working set nearly as large as heap (no leak, just under-provisioned memory), or very allocation-heavy workload causing GC thrash | Increase heap memory so GC has breathing room; tune GC (e.g., use a concurrent collector if pause time is an issue); optimize application to allocate less if possible (object reuse, etc.). Monitor that GC time is <5% of runtime ideally.                                                           |
| Memory fragmentation (rare with G1) | Full GC doesn’t free expected space, weird allocation failures                        | Sometimes native memory fragmentation or large objects not fitting contiguous space (less an issue with modern collectors)        | If using older collector like CMS, fragmentation could OOM even with free heap – switching to G1/ZGC helps. Otherwise, periodic full GC or restart may be needed. Native memory issues require looking at off-heap usage (DirectByteBuffers, etc.) and limiting them.                                  |
| Large objects in memory (not leak)  | High heap usage but stable, long GC pauses                                            | Loading very large data sets into memory (e.g., reading a huge file into RAM, or loading entire DB table)                         | Use streaming to handle data in chunks. If need in memory, maybe split into smaller pieces or upgrade hardware. For long pause, consider G1’s region sizing or use ZGC which handles large heaps better.                                                                                               |

_Table 5.1: Memory Issues, Causes, and Solutions_

Memory management in Java is automatic, but that doesn’t mean we can ignore it. As architects, we must ensure that our system design doesn’t inadvertently hog memory. This includes setting guidelines for developers (e.g., “don’t cache unbounded data,” “be cautious with static state”). Also consider load/performance testing not just for throughput but for endurance (run tests that simulate weeks of operation to see if memory footprint stabilizes or grows).

With memory covered, we move to another tricky area: concurrency and threading issues.

## 6. Concurrency and Threading Challenges

Concurrency bugs can be some of the most elusive. They may not appear until the system is under certain conditions or may cause intermittent failures/hangs. In Java, common concurrency issues include **thread deadlocks, livelocks, thread starvation, race conditions**, and issues specific to thread pools. In the context of Spring Boot and Tomcat, we often deal with **thread pool management** and ensuring that multi-threaded components (like @Async methods, schedulers, etc.) run smoothly. This chapter focuses on identifying and resolving deadlocks and thread contention, as well as best practices to avoid these problems.

### 6.1 Thread Deadlocks

A **deadlock** occurs when two or more threads are waiting on each other in a circular way, such that none can proceed. For example, Thread A holds Lock 1 and waits for Lock 2, while Thread B holds Lock 2 and waits for Lock 1 – they’ll wait forever.

**Detection:** As discussed, the easiest way is via a thread dump. The JVM can detect deadlocks involving monitor locks (synchronized blocks) and high-level locks (like `java.util.concurrent.Lock`) and will flag it in the thread dump output. The dump will list the threads and locks in the cycle. For instance:

```
Found one Java-level deadlock:
"Thread-1":
  waiting to lock Monitor@0x123 (Object X)
  which is held by "Thread-2"
"Thread-2":
  waiting to lock Monitor@0x456 (Object Y)
  which is held by "Thread-1"
```

This tells you exactly which locks and threads are involved.

If the application appears hung (no progress), definitely take a thread dump. Deadlocks often cause total freeze if they occur in core threads (e.g., if Tomcat’s request threads deadlock on some shared resource, all new requests may hang too). If only a subset of threads deadlock, the system might limp along but with reduced functionality.

**Common Causes in Enterprise Apps:**

- Nested synchronized blocks in inconsistent order (Lock ordering problem).
- Two threads calling each other’s synchronized methods (each has a lock, calling into the other who has the other lock).
- Using multiple locks without a defined global ordering. A best practice is to always acquire multiple locks in a consistent order in all threads to avoid cycles.
- Database deadlocks are a different beast (two transactions waiting on each other’s row locks). Those are detected by the DB which usually aborts one. But they manifest as errors, not hung threads, so here we focus on in-JVM deadlocks.

**Resolution:** Once a deadlock has occurred, the only way to recover is usually to restart or externally intervene (there is no safe way to forcefully unlock locks in Java). So prevention is key. If you identify the code causing it, refactor to avoid locking or to use try-lock with timeouts if possible (though that can degrade into livelock if not careful).

In some cases, using higher-level concurrency utilities can help avoid manual locking. For example, using `ConcurrentHashMap` or `java.util.concurrent.Atomic` classes can eliminate the need for explicit locks. Or using immutable data structures that avoid needing locks.

**Case Example:** Suppose two Spring @Scheduled tasks deadlock. Task1 synchronizes on A then B; Task2 synchronizes on B then A. This is a classic deadlock if they run concurrently. Solution could be to avoid locking both at once, or merge into one task if possible, or enforce ordering (always lock A then B in both tasks). Logging and analysis of thread dumps would reveal this scenario.

### 6.2 Thread Pool Starvation and Exhaustion

Even if no deadlock, a thread pool can become **starved** (exhausted) if threads are tied up and no free threads are available for other tasks. We saw one example under performance: all Tomcat threads waiting on slow I/O causing requests to queue.

Another subtle scenario is **thread pool self-deadlock**:

- For example, using `AsyncRestTemplate` or making a call to another service on the same thread pool. If not configured properly, one might end up in a situation where a Tomcat request thread calls out to an external service that is actually served by the same application (or same pool) – effectively waiting on itself. If all threads do this, it deadlocks. This often happens in thread pools if a task submits another task to the same pool and waits for it (a form of deadlock).
- More concretely: In a microservice A, suppose a request needs to fetch data from microservice B, but due to configuration error, it actually calls itself (A) or a service that calls back into A. If A’s thread pool is small and all threads are waiting on responses from B (which are actually queued in A because calls came back to itself), you have a deadly embrace.

**Async and CompletableFutures:** Be careful when using `CompletableFuture.supplyAsync` without specifying an executor – by default it uses ForkJoinPool.commonPool. If that common pool is starved or if you do something like `.get()` on the future in a thread, you could block waiting for a completion that needs a thread.

**Detection:** Thread dumps help here too. You may see many threads in WAITING state on a `java.util.concurrent.Future` or similar. Also, metrics like active vs queued tasks for a pool (if exposed) will show you if the pool is at max with tasks pending.

**Solution:**

- Increase pool size (short term relief).
- Ensure tasks on a pool don’t indefinitely wait for other tasks on the same pool. If they must wait, consider using a separate pool for that work, or redesign so it’s asynchronous all the way (don’t block waiting for completion).
- Use tools: There are also utilities in JDK (like ThreadMXBean) to detect deadlocks not just with locks but with wait/notify or future waiting, but they are not automatic. APMs might show if a lot of threads are waiting on futures.

### 6.3 Lock Contention and Synchronization Issues

Not all concurrency issues are deadlocks; some are **live locks** or heavy contention:

- **High contention**: Many threads frequently trying to lock the same resource can lead to wasted time context switching. This will show up as CPU time but no throughput gain. E.g., multiple threads appending to a shared list with a lock – they might spend time waiting. If profiling or JFR shows a lot of time in `ObjectMonitor` or `Lock` events, that’s a sign.
- If using `synchronized` collections (like Vector, Hashtable, or Collections.synchronizedList), these can become a bottleneck under concurrency. It might be better to switch to modern concurrent collections (like ConcurrentHashMap, CopyOnWriteArrayList depending on use-case).

**Atomicity/Race Conditions:** These are logic bugs where, for example, two threads update a non-thread-safe structure concurrently causing inconsistent state. In a Spring Boot app, much of the framework is thread-safe or uses thread confinement (each request in separate thread). But if you have any shared mutable state (e.g., a static counter that isn’t atomic), you can get races. Those might manifest as incorrect results rather than hangs (like a counter missing increments under load). The fix is to use `AtomicInteger` or proper synchronization around that variable.

**Double-Checked Locking & volatile:** If implementing patterns like singletons or caches with double-checked locking, ensure the use of `volatile` for the instance reference. Otherwise, you risk subtle memory model issues. This is more of a correctness concern than immediate troubleshooting, but can cause weird behavior.

### 6.4 Best Practices to Avoid Concurrency Pitfalls

**Immutability:** Favor immutable objects and pure functions that don’t require locking. For example, instead of having a method that accumulates data in a shared list, have it return a new list or use stream processing.

**Thread-safe Libraries:** Use thread-safe variants of utilities. For instance, if you need a queue accessed by multiple threads, use `ConcurrentLinkedQueue` or `LinkedBlockingQueue` instead of a manually synchronized list.

**Minimize Lock Scope:** If you must lock, keep the critical section as small as possible (e.g., compute data outside the lock, then quickly lock to update a shared structure). This reduces contention time.

**Avoid Nested Locks:** As much as possible, avoid locking multiple mutexes at once. If needed, document an ordering and stick to it to prevent deadlock.

**Thread Pool Config in Spring Boot:**

- The Tomcat thread pool (for incoming requests) is configured via properties (e.g., `server.tomcat.max-threads`). Set this based on expected concurrency and resource constraints.
- If using `@Async` with Spring’s `TaskExecutor`, define the pool size and queue capacity. A bounded queue with CallerRuns policy can avoid out-of-memory if flooded, but if too small can degrade throughput.
- If using scheduling (`@Scheduled`), by default it’s single-threaded. If you have multiple scheduled tasks that might overlap, consider configuring a `TaskScheduler` bean with a thread pool.

**Monitoring Concurrency:** Include thread states in monitoring. For instance, using Prometheus’s JMX exporter or Micrometer to track threads in state RUNNABLE vs BLOCKED. A sudden rise in BLOCKED threads could indicate a new contention issue in a release.

**Testing:** Write multi-threaded tests where possible. Use tools like ConcurrencyTestHarness or the jcstress tool for low-level concurrency testing for critical concurrent structures.

**Resilience to Hangs:** Implement timeouts for operations that might hang and fallback logic (to be discussed in Resilience chapter). For example, if a thread is waiting on an external call, don’t let it wait forever – apply a timeout so it will wake up, log an error, and not permanently tie up the thread.

In multi-service architectures, a “hung” thread might not be due to a coding deadlock but waiting on another service that is slow or dead (which we handle via timeouts and circuit breakers). Those are not strictly deadlocks but can cause similar symptoms (lots of waiting threads).

### 6.5 Analysis Tools for Concurrency

We’ve talked about thread dumps and JFR. There are some additional aids:

- **Java VisualVM Sampler**: It can sample thread states over time, showing what percentage of time threads are blocked or waiting.
- **IBM Concurrency Diagnostic**: IBM had some tools for WebSphere (not directly relevant to Spring Boot, but general ideas).
- **eG Innovations APM**: The earlier reference suggests using APM to monitor thread states over time. If an APM is in place, check if it has a thread contention or deadlock detection feature.
- **Custom Thread Deadlock Detector**: As one StackExchange answer suggests, one can programmatically use `ThreadMXBean.findDeadlockedThreads()` on a schedule to detect deadlocks in a running app and potentially alert. This could be integrated as a last resort – e.g., an admin endpoint that checks for deadlocks.

In critical systems, sometimes an automated action is taken: if a deadlock is detected, the process might restart (since it’s stuck anyway). But identifying false positives vs real is tricky, so usually just alerting humans is preferred.

### 6.6 Summarizing Concurrency Troubleshooting

To summarize:

- **Deadlocks**: Use thread dumps, then fix code to avoid circular waits.
- **Thread starvation**: Increase threads or break dependencies that cause threads to wait on each other.
- **Contention**: Use better concurrency constructs to reduce waiting.
- **Care in design**: Prefer stateless and independent request handling, avoid shared state unless necessary.

We can incorporate some of this in a short table:

| **Concurrency Issue**               | **Symptom**                                                                                                                                           | **Cause**                                                                                                                          | **Solution**                                                                                                                                                                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Thread deadlock                     | One or more threads stuck forever waiting (application hang). Thread dump shows “Found one deadlock”.                                                 | Cyclic locking order (Thread A holds X waits Y, Thread B holds Y waits X)                                                          | Refactor to avoid circular locks. Establish lock ordering or use atomic/concurrent structures to remove explicit locks. Possibly use a single lock instead of two if appropriate.                                                                |
| Thread pool exhaustion              | All threads in a pool are busy and new tasks cannot execute (requests time out or queue up). Dump shows threads waiting on external calls or futures. | Long blocking operations on each thread (e.g., waiting on network or another task). Possibly tasks mutually waiting on each other. | Add timeouts to blocking calls to release threads. Increase pool size if resources allow. Separate dependent tasks onto different pools to avoid self-waiting. Use asynchronous frameworks to avoid tying up threads during waits.               |
| High lock contention                | CPU high but progress low, many threads BLOCKED on same lock, low throughput.                                                                         | Many threads synchronized on a shared resource or data structure.                                                                  | Reduce lock scope or frequency. Use finer-grained locks or lock-free data structures (e.g., ConcurrentHashMap). Re-examine need for the lock (maybe maintain thread-confined copies of data and merge later).                                    |
| Race condition (data inconsistency) | Inconsistent data, e.g., counters wrong, missing updates under load, but no obvious error/exception.                                                  | Shared mutable state without proper synchronization (e.g., non-volatile flags, unsynchronized updates).                            | Use thread-safe constructs: declare shared flags as `volatile` if needed, or use synchronized/atomic operations for shared variables. Prefer immutable data exchange. Write tests to simulate concurrent access and verify correctness.          |
| ThreadLocal leak (special case)     | Memory leak across threads (especially in container reuse). Not directly a concurrency bug, but concurrency-related resource handling.                | ThreadLocal not removed, holding large object, in a thread pool that lives long.                                                   | Ensure ThreadLocal variables are removed (`remove()`) after use, e.g., in a `finally` block or using frameworks that do it (Spring’s RequestContext, etc., usually cleans up). Use try-with-resources or other guards for thread-bound contexts. |

_Table 6.1: Concurrency Issues and Solutions_

In a Spring Boot microservice, heavy manual concurrency control is less common for request handling (since each request is already parallel by default via Tomcat threads). But if you implement background processing or in-memory work queues, be mindful of these principles.

Now we have tackled performance, memory, and concurrency. The next chapter will address _dependency and configuration pitfalls_, which often cause issues not in the form of performance or crashes, but in misbehavior, startup failures, or integration mismatches.

## 7. Dependency and Configuration Pitfalls

In a complex Java project, especially one using Spring Boot with many starters and libraries, **dependency management** and proper configuration are crucial. Issues in this category include version conflicts (JAR hell), misconfigured Spring Boot properties leading to disabled features or security holes, and environment mismatches. Architects need to enforce good dependency hygiene (often via a BOM – Bill of Materials) and have strategies for configuration across environments (dev, test, prod) that avoid surprises. This chapter discusses common pitfalls and troubleshooting methods for dependency and configuration issues.

### 7.1 Dependency Version Conflicts (JAR Hell)

**The problem:** Java’s classpath can only have one version of a given class at runtime (assuming no classloader isolation beyond that). If your app brings two different versions of the same library (e.g., due to transitive dependencies), you can get NoSuchMethodError, LinkageError, ClassCastException, or inconsistent behavior. Spring Boot uses a curated dependency BOM to align versions, but if you override or add different versions, you might hit conflicts.

**Symptoms:**

- Application fails to start with `NoClassDefFoundError` or `NoSuchMethodError`. For example, if you have two different versions of a library and Spring Boot pulled in one but compile was against another, at runtime a method might not exist.
- Strange behavior at runtime – e.g., logging not working because multiple SLF4J bindings present.
- Incompatible library versions causing subtle bugs (like different default settings).

**Troubleshooting:**

- Use Maven/Gradle’s dependency tree to see if you have conflicting versions. (`mvn dependency:tree` or Gradle’s `dependencies` task output).
- Look for duplicate JARs or classes. Sometimes shading (bundling dependencies) can cause internal conflicts.
- If using Spring Boot, leverage the **Spring Boot BOM** (spring-boot-dependencies) which ensures a consistent set of dependency versions that are known to work together. Try to not override versions unless necessary.
- If you need a specific version of a library that conflicts with Boot’s, ensure others that depend on it don’t bring a different version. You might use dependency exclusions or force a specific version.
- Test the application startup thoroughly after adding new dependencies.

**Example:** Suppose you add a library that brings an older version of Jackson JSON library, while Spring Boot uses a newer version. You might get an error because Spring Boot’s autoconfiguration expects a class in Jackson that isn’t in the older version. The fix is to align the Jackson version – either exclude the older one or upgrade everything to the newer. Using the Spring Boot BOM or the `spring-boot-starter-json` (which pulls the right Jackson) can avoid this.

Another classic example is having both log4j and log4j2 or multiple logging bridges on classpath, leading to warnings like “Class path contains multiple SLF4J bindings.” While not fatal, it can cause confusion in logging output. The solution is to only include one logging framework and its binder.

**Jakarta vs Javax (Spring 5 vs Spring 6):** A recent dependency pitfall arises from the **Javax to Jakarta EE namespace change**. Spring Framework 6 / Spring Boot 3 moved to Jakarta EE 9+ (so uses `jakarta.servlet` etc.). If you accidentally mix a Spring Boot 3 application with an older Servlet container (Tomcat 9 or Jetty that expects `javax.servlet`), it will not work. For instance, deploying a Spring Boot 3 WAR to Tomcat 9 yields nothing or errors – because Tomcat 9 expects Servlets in `javax.*`. As the Stack Overflow answer explains, Spring Boot 2.x (Spring 5) is Java EE 8 (javax) and is incompatible with Tomcat 10 (Jakarta), and conversely Spring Boot 3 (Jakarta) is incompatible with Tomcat 9. **Compatibility matrix:** If using Boot 3, ensure the servlet container is Tomcat 10+ (which supports Jakarta Servlet 5.0). If using Boot 2, stick to Tomcat 9 or earlier. This is a configuration/dependency issue that can cause the app to not respond at all (as in the question, it started then shut down immediately with no obvious error, because no matching servlet environment).

So, pay attention to such breaking changes. The Spring Boot 3 release notes and migration guide emphasize upgrading Tomcat when moving to Spring 6/Jakarta.

### 7.2 Spring Boot Auto-Configuration and Configuration Mistakes

Spring Boot’s auto-configuration is a boon for productivity but if assumptions are wrong, you can get misconfigurations:

- **Disabling/enabling auto-config:** Sometimes you might accidentally exclude an auto-configuration class and then a feature (like security or Actuator) doesn’t work fully. If something is not behaving (say, metrics not exposing), check if any configuration property or annotation is disabling relevant auto-config classes. The Spring Boot `--debug` flag can show conditional auto-configuration report to see what got applied or not.
- **Profiles and property sources:** A common issue is thinking a property is set when it’s not, due to profile ordering. For example, having an application.yml and an application-prod.yml, but maybe not activating the profile when you think. Always verify the active profiles (Spring will log them on startup) and which sources it’s using. Misplaced or misspelled properties cause them to fall back to defaults.
- **Case-sensitivity and format:** Spring Boot external config keys are relaxed binding (not case sensitive, and can use hyphen or camel). But a typo still means the property is ignored. If a config isn’t taking effect, check for typos.
- **Environment-specific differences:** Maybe in dev you run with H2 database (auto-configured) but in prod you set a JDBC URL. If you forget to set the prod profile correctly or include the required driver on classpath, the app might fail to start (e.g., no driver for the DB). These issues are usually caught in testing, but surprises happen if environments drift.

**Dependency Misconfig (starter misuse):** Spring Boot starters pull dependencies. If someone accidentally excludes something crucial (like spring-web in a web app), things might not start. Or if you override a version to one that’s incompatible with Boot’s expectation (like an older Spring Framework version), it may break.

**Troubleshooting Approach:**

- Look at startup logs. Spring Boot logs a banner of configs and also errors if beans can’t be created. Often configuration issues show up as exceptions at startup (BeanCreationException, etc.), indicating something is missing.
- Use the Actuator `env` endpoint (if available) to see what config properties are in effect at runtime – you might catch that a property wasn’t loaded.
- Use the Actuator `conditions` (or in newer Spring Boot, `configprops` or the debug condition report) to see which auto-config classes were not applied and why.
- Check that your configuration files are being picked up (correct file name, in the classpath, etc.). Spring Boot by default loads application.properties or .yml from classpath and external locations – but if you package differently, ensure it’s there.

**Case example:** A microservice was supposed to connect to a message broker. The developer set properties for the broker’s URL in a `application-prod.yaml`, but forgot to activate the profile “prod” when deploying. The service came up using default config (which pointed to localhost broker, which it couldn’t reach, and thus messaging didn’t work). The solution was to activate the profile via an environment variable or use `SPRING_PROFILES_ACTIVE=prod`, or merge config appropriately. This highlights the importance of knowing what profile is active and making sure the intended config is loaded.

### 7.3 Infrastructure and Environment Configuration

Sometimes the app is fine, but environment config is off:

- **JDK version differences:** Ensure you run on a supported Java version. Spring Boot 3 requires Java 17+. Running it on Java 11 would fail to start (unsupported class version).
- **File encoding or locale:** If dealing with internationalization or file paths, differences in OS (Windows vs Linux path separators, etc.) can cause issues.
- **Time zones:** If not handled, running in a different timezone could alter behavior (maybe tests pass in one zone but not another due to date parsing).
- **Case sensitivity**: Windows file system vs Linux can catch you (e.g., referring to a file in resources with wrong case works on Windows, fails on Linux).
- **Container config:** In Docker, if you forget to pass certain env variables or mount files (like a keystore for SSL), the app might start with defaults or fail.

### 7.4 Misconfiguration of Frameworks/Components

Some pitfalls related to specific configurations:

- **Hibernate/JPA lazy initialization:** If an entity is fetched lazily outside of a transaction, you get LazyInitializationException. This is a mis-use issue – solution could be to adjust fetch type or ensure the code accesses needed fields within the transaction, or use OpenSessionInView (not always recommended in microservices).
- **Spring Security config errors:** e.g., not restricting actuator in production because management security is off or a property is wrong – leading to unintended open endpoints.
- **Actuator exposure:** If you want actuators like /health to be accessible without auth, you must configure it. If not, you might find those endpoints returning 401 unauthorized unexpectedly.
- **Micrometer metrics registry:** If you intend to push metrics to a system (like pushing to Graphite or use Prometheus), you must include the appropriate dependency and config. Missing that, metrics might not be exposed as you think. Always verify metrics output.

### 7.5 Tools for Managing Config and Dependencies

**Bill of Materials (BOM):** As mentioned, using BOMs (Spring Boot BOM, or others like Spring Cloud BOM) ensures compatibility. For example, Spring Cloud releases align with certain Spring Boot versions. Mixing versions can cause issues (e.g., using Spring Cloud Netflix versions not meant for your Boot version). Always consult the compatibility docs.

**Dependency Management Tools:** Maven’s Enforcer plugin can be configured to fail the build on dependency convergence issues (multiple versions). This can catch conflicts early.

**Configuration Management:** In large deployments, using a **Configuration Server** (Spring Cloud Config) or Kubernetes ConfigMaps helps manage config centrally. But ensure that the config server itself is consistent and that you don’t accidentally deploy services pointing to the wrong config repo or branch.

**Secret Management:** If, for example, credentials are missing, the app might start but fail on connecting to DB or API. You need a strategy (Vault, etc.) to supply those without hardcoding. When a service cannot connect to a resource due to bad credentials, it’s often traced to either not setting the config or mis-typing it.

### 7.6 Summarizing Config/Dependency Issues

We compile a quick table for some config pitfalls:

| **Config/Dependency Issue**                   | **Symptom**                                                                                                   | **Cause**                                                                                                       | **Solution/Check**                                                                                                                                                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Classpath version conflict                    | NoSuchMethodError, ClassDefNotFound, or weird runtime errors when calling certain APIs                        | Two versions of a library present (e.g., older transitive dep overriding newer)                                 | Check `dependency:tree`. Align versions via BOM or exclusion. Remove duplicate jars. Ensure using compatible versions (Spring Boot BOM ensures Spring, Tomcat versions align, e.g., Boot 3 with Tomcat 10).                    |
| App fails to start after upgrade              | Application shuts down or errors on startup with missing classes (e.g., javax.\* not found)                   | Incompatibility between frameworks (e.g., moved from javax to jakarta namespace)                                | Use correct server/library versions (Jakarta EE 10 APIs for Spring 6). See migration guides. For example, upgrade Tomcat when moving to Spring Boot 3.                                                                         |
| Property not taking effect                    | Behavior remains default, or wrong endpoint used, etc. Possibly log says “Using default X because Y not set.” | Misnamed or misplaced configuration property; wrong profile active; property overridden later by another source | Verify active profiles and config files. Use `/actuator/env` to see if property is present. Correct the spelling/case of keys. Ensure profile activation (SPRING_PROFILES_ACTIVE).                                             |
| Wrong environment config applied              | App uses dev settings in prod (e.g., connects to dev DB) or vice versa                                        | Profile not activated or config server pointing to wrong env, or environment variable not set                   | Clearly separate configs. Use spring.profiles.active or profile-specific YAML. Double-check deployment scripts passing correct env variables.                                                                                  |
| Missing dependency leading to runtime failure | A feature doesn’t work (e.g., metrics endpoint 404, or JSON parsing fails)                                    | Did not include necessary library or starter (for metrics, need micrometer-registry-prometheus, etc.)           | Add the appropriate Spring Boot starter or dependency. Spring Boot docs list what starters include what. If intentionally excluding something, ensure alternative is in place.                                                 |
| Logging doesn’t work as expected              | No logs or multiple log formats printed                                                                       | Logging binder conflict (e.g., multiple SLF4J bindings), or using JUL without bridge                            | Remove extra log bindings (for SLF4J, only have one, typically Logback in Spring Boot). If using a different framework, exclude Boot’s default logger. Test logging on startup (Spring Boot usually logs the binder it found). |

_Table 7.1: Configuration and Dependency Issues_

In general, adhere to the principle of **convention over configuration** (use Spring Boot’s defaults and structures) unless you have a reason to deviate, and when you do deviate, document and ensure thorough testing in environment parity.

Now that internal issues are covered, the next chapter will address **integration failures in distributed systems**, which often span beyond a single application’s boundaries.

## 8. Integration Failures in Distributed Systems

Microservices introduce another class of problems: those arising from communication between services or with external systems. Even if each service is individually sound (no leaks, no deadlocks), the interactions can fail due to network issues, misconfigured endpoints, or partial failures. This chapter looks at troubleshooting **inter-service integration issues**: timeouts, connection failures, inconsistent data across services, and so on. We also consider the broader **distributed system concerns** such as latency, throughput matching, and data consistency.

### 8.1 Timeout and Connection Issues

One of the most common integration problems is a service calling another and getting no response or a very slow response. This can cause cascading delays. As we discussed earlier, _timeouts_ are crucial:

- **No Timeout = Danger**: If Service A calls Service B with no timeout, and B hangs (maybe due to its own issue), then threads in A will hang indefinitely, possibly causing thread pool starvation. Many HTTP client libraries default to no timeout (Java’s HttpURLConnection in the past, Apache HttpClient default used to be high or infinite). For example, the Zalando engineering blog emphasizes that infinite timeouts are unacceptable in production; if a downstream gets stuck and threads wait infinitely, it can exhaust resources and cascade failures. The fix is to always set reasonable timeouts on connections and requests.
- **Connection vs Read Timeout**: Set both: a connection timeout (to establish TCP) and a read timeout (for waiting on data). A typical practice is connection timeout a bit lower than overall timeout, but both should be tuned to network conditions. For microservices in same data center, connection should be very fast (ms), so a low connection timeout (e.g., 100ms) is fine. The read timeout depends on expected response times of the service; maybe a few seconds for normal operations, longer for batch endpoints, etc.
- **Symptoms of missing timeouts**: Threads stuck (see thread dump with stack trace showing a socket read or Future.get without timeout). Also the calling service might not log a timeout error, because from its perspective nothing “errored” (it’s just waiting). You will see only that requests to A pile up. Eventually maybe an upstream (like a load balancer or API gateway) times out the call.
- **Ensure Retries with Backoff**: Even with timeouts, if calls fail or timeout, consider a retry policy, but with caution: blind retries can amplify load (thundering herd). Use exponential backoff and a limit on retries. If a service B is down, dozens of callers from A all retrying immediately could flood B when it recovers or overwhelm the network.

**Troubleshooting**:

- Check the configuration of HTTP clients (RestTemplate, WebClient, OkHttp, etc.). Are timeouts set? If not, that’s likely a bug.
- If using Spring’s `RestTemplate`, you set timeouts on the underlying RequestFactory. For WebClient (reactive), you can use `.timeout(Duration)` or handle via reactor Netty options.
- Look at logs on both sides: does Service B receive the request? If not, maybe network issue or service discovery issue.
- Ping the endpoint manually (using curl or similar) from the environment to ensure connectivity (especially if networking policies are involved).
- In Kubernetes, check if service DNS is correct and the service is up. Sometimes failing calls are due to DNS misconfiguration or missing service registration.

### 8.2 Service Unavailable or Errors

Integration failure can also be explicit errors:

- HTTP 500/400 from a service due to bad request or server error.
- Authentication/authorization failures (e.g., one service not authorized to call another – maybe missing OAuth token or wrong certificate).
- Protocol mismatch (one side expecting JSON, other sending XML, etc.). In microservices with clear contracts (like REST with JSON), this is less common but can happen if one service updates an API and others not updated (leading to JSON parse errors, for instance).

**Troubleshooting:**

- Use **API contract tests** or at least verify request/response formats. If Service A started failing calling B after B was updated, suspect a contract change or bug in B.
- Check error logs: Service B might log why it returned 500. If you have distributed tracing, trace IDs help link the failing call from A to B’s logs.
- For auth issues: verify that service A is including the proper auth token or certificate expected by B. If using mutual TLS, check that certificates are correctly configured (common integration failure in cloud deployments if certificate secrets aren’t loaded properly).
- Ensure that any **circuit breaker** or gateway isn’t blocking the call. For example, if you have an API gateway, a misconfigured route or a rate limiter might be preventing calls from succeeding.

### 8.3 Data Mismatch and Schema Evolution

Microservices often communicate via JSON or Avro, etc. If one side changes the schema (adds a field, etc.), ideally it’s backwards compatible. But if not, the consumer might break. For instance:

- Service A expects a JSON field “status” but Service B’s new version changed it to “state” – calls break or A misbehaves because it gets null for status.
- Or types changed (an integer became string, etc.).

**Mitigation**: Strongly version your APIs or use techniques like consumer-driven contracts testing to catch these. Use a schema registry if using Avro/Protobuf to manage versioning.

**Troubleshooting**: If an integration used to work and now doesn’t after a deployment, suspect an API change. Compare the payloads. Perhaps run both old and new versions of service B (if possible) to see differences. The solution might be to update service A to the new contract or roll back the change on B and plan a compatible deployment.

### 8.4 Message Queue and Async Integration

Not all integration is sync HTTP. If using messaging (JMS, RabbitMQ, Kafka):

- **Messages not delivered**: Could be broker down, or wrong topic/queue name configuration.
- **Consumers failing**: If the message format changed, consumers may throw exceptions upon receiving. This might not be immediately visible unless you monitor dead letter queues or error logs.
- **Duplicate messages**: If acknowledgements aren’t handled properly, you might reprocess messages. Idempotency and deduplication become issues.
- **Transaction issues**: A common pattern is using distributed transactions or outbox pattern for consistency. If misconfigured, could result in partial updates (data in one service updated, but message not sent to other, etc.).

**Troubleshooting**:

- For messaging, use monitoring tools (e.g., RabbitMQ management UI or Kafka consumer group lags). See if messages are piling up because consumers can’t process.
- Check configuration: correct broker address, credentials, queue/topic names. It’s easy to have a property pointing to a wrong exchange or misspelling.
- If using Spring Cloud Stream or Spring Kafka, ensure the binder is set up right. Mismatched group IDs in Kafka could lead to no consumers for a partition if mis-set.
- Look at any dead-letter queue for clues if messages are being routed there due to errors.

### 8.5 Distributed Transactions and Consistency

In distributed systems, maintaining data consistency is tricky. If an integration fails halfway:

- Example: Service A and B are supposed to both update their databases upon an event. If A updated its DB and then calling B failed, you have an inconsistent state. Ideally, you’d use a saga or compensation mechanism.
- While this is more design than troubleshooting, as an architect you need to foresee and design for eventual consistency or compensations.

From a troubleshooting perspective:

- If data between services is out of sync, trace through the event or request flows. Perhaps a particular event didn’t reach a service. Use audit logs if available. Many systems create audit trails for critical operations.
- Introduce tools like **distributed tracing not just for latency but for causality** – you could trace that a request that created an order in service A should have triggered a message to service B to create a corresponding shipment; if B never got it, trace message logs or broker logs. Possibly the message was lost or never sent due to a bug.

### 8.6 The Fallacies of Distributed Computing

Sun’s classic fallacies (the network is reliable, etc.) remind us: networks can fail, latency is not zero, throughput is not infinite, topology can change, etc. Thus:

- Always suspect network issues if integration fails: e.g., DNS misconfigured, firewall rules blocking traffic. Especially across data centers or to third parties.
- Use tools like `ping`, `traceroute`, or cloud-specific network diagnostic tools when a service cannot talk to another.
- Cloud considerations: if using cloud services (e.g., AWS RDS, S3, etc.), ensure VPC endpoints or internet gateways are configured. Many times a service fails to reach S3 because no internet egress is set up from a private subnet.

**Cascading failure**: If one service goes down, ensure it doesn’t bring down others. This leads into **resilience patterns** (next chapter). But from troubleshooting view, if multiple services fail simultaneously, investigate if one’s failure caused an overload or chain reaction.

**Observability in Integration**: We emphasized tracing. Additionally, **metrics like error rate per dependency** are useful. E.g., expose a metric in service A: “calls_failed_service_B_count”. If that spikes, you know calls to B are failing – which might be quicker to alert on than waiting for overall request failures.

### 8.7 Service Discovery & Config

If using a service registry (Eureka, Consul, Kubernetes DNS):

- Services might not register or discover properly. E.g., a service registers under a name slightly different than what the caller looks up.
- TTL expiration or stale info leading to trying to call an instance that’s gone (though robust clients handle that).
- In Kubernetes, a common issue is forgetting to add a service entry or misnaming it. That leads to DNS resolution failures (`Unknown host` exceptions in the caller).
- If using load balancers (like Spring Cloud LoadBalancer or Ribbon), ensure they’re picking up the instances.

**Troubleshoot**:

- For discovery-based, check the registry’s admin UI or API: is the target service listed and healthy?
- If one instance is misbehaving, maybe it’s unhealthy but not deregistered – calls go to it and fail. Implement health checks so discovery removes bad instances.
- Check config: Spring Cloud has properties for service IDs, make sure they match across services.

### 8.8 Summarizing Integration Failures

A summary table for integration issues:

| **Integration Issue**               | **Symptom**                                                                      | **Likely Cause**                                                                                                                                          | **Solution**                                                                                                                                                                                                                                                                                                      |
| ----------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Downstream timeout/hang             | Service A calls B and waits indefinitely, apparent hang or very slow response.   | Missing or too high timeout; downstream service hung; network partition causing calls to never complete.                                                  | Implement timeouts on calls. Use circuit breaker to fail fast if B is unresponsive. Investigate B’s health or network connectivity (e.g., is B down or slow).                                                                                                                                                     |
| Immediate “connection refused”      | Call fails quickly with connection error.                                        | Target service not running or wrong host/port; firewall blocking; service discovery returned wrong address.                                               | Verify service B is up at expected address/port. Check configuration of endpoint (URL correctness). If using service discovery, ensure registry info is correct and client config (e.g., correct VIP name). Open firewall/ports as needed.                                                                        |
| HTTP 500 or error response          | Received error response from downstream (or a fault code).                       | Bug or exception in service B; contract mismatch (A sent bad data unknowingly).                                                                           | Check logs of service B for the error at that timestamp. Fix bug or adjust input. If contract mismatch, align request format between services (deploy compatible version).                                                                                                                                        |
| Authentication failure (401/403)    | Service A gets unauthorized from B.                                              | Missing or invalid credentials/token in the request. Possibly misconfigured security (A not set to include token, or token expired).                      | Ensure service A is including auth header (e.g., JWT or OAuth token). Configure token refresh if expired. Check that A’s identity has permission in B (maybe an OAuth scope issue).                                                                                                                               |
| Messages not consumed               | Messages piling in queue/topic, or actions supposed to happen aren’t happening.  | Consumer service down or misconfigured (wrong queue name or group); message format changed and consumer throwing errors; authentication to broker failed. | Verify consumer service is running and connected to broker. Check logs for consumer exceptions. Ensure config (queue/topic names, group IDs) match exactly between producer and consumer. If format changed, update consumer accordingly or handle both formats.                                                  |
| Data inconsistency between services | e.g., Order status in Service A is "shipped" but Shipping service has no record. | An integration event or call failed silently; no compensating action was taken. Possibly transaction across services broke.                               | Trace the workflow: find if the event to create shipment was sent and maybe lost. Check event logs or outbox. If found bug (e.g., not retrying message), fix and possibly run a reconciliation to sync data (an out-of-band script). Implement saga compensation if needed to handle partial failures gracefully. |
| Service discovery failure           | “Unknown host” or no instances found when calling by service name.               | Service not registered or client not configured for discovery; network DNS issues in container orchestration.                                             | If using Eureka/Consul, ensure client config (service name, registry URL) is correct and that service is registered (check registry UI). In K8s, ensure Service object exists and DNS is resolving (test with `nslookup` inside pod). Possibly add retries on lookup or fallback IPs if suitable.                 |
| Cascade failure / overload          | When B is down, A also becomes slow or crashes due to backlog.                   | Lack of bulkheads: A’s resources exhausted waiting on B (thread pool or connection pool filled). Cascading failure due to no isolation.                   | Implement bulkhead pattern (separate thread pool for calls to B, so A doesn’t tie up all threads). Use circuit breaker to cut off calls to B quickly after some failures, allowing A to fail fast or degrade gracefully. Scale out or shed load if one component overloads others.                                |

_Table 8.1: Integration Failure Scenarios_

An architect should consider these integration risks early and design the system to handle them (which leads us to the next chapter on resilience patterns). For troubleshooting existing issues, the strategies above (monitoring, tracing, config checking) will help pinpoint the cause.

## 9. Resilience Patterns for Fault Tolerance

Building on the integration issues, this chapter focuses on the **architectural patterns and best practices** to make distributed systems robust. While previous chapters addressed troubleshooting specific problems, here we consider how to **prevent problems or mitigate them** so that failures in one part do not cascade. We will discuss patterns like **circuit breakers, retries, bulkheads, fallback, and chaos engineering**, citing how they help and how to implement/monitor them.

### 9.1 Circuit Breakers and Fail-Fast

As introduced by Michael Nygard in _Release It!_ and summarized by Martin Fowler, the **Circuit Breaker pattern** is fundamental to avoid cascading failures. A circuit breaker watches calls to a remote service (or any risky operation) and if a certain failure threshold is reached, it “trips” and short-circuits further calls, immediately returning an error (or fallback) instead of trying the remote operation. This prevents continuously tying up resources with calls likely to fail.

**Benefits:**

- Protects a struggling service from traffic by cutting off calls from the client side after it’s clear they’ll likely fail.
- Protects the calling service from waiting on long timeouts repeatedly.
- Gives time for the downstream service to recover, after which the breaker can allow some test calls (half-open state) to check if it’s back.

**Implementation:** Libraries like Netflix Hystrix (now in maintenance, but popular historically), Resilience4j (a more recent lightweight library), or Spring Cloud Circuit Breaker abstraction (which can use Resilience4j under the hood) are common. With minimal config, you wrap remote calls in a circuit breaker. E.g., using Resilience4j’s annotations or programmatic API you can define a circuit breaker with thresholds (e.g., trip if >50% of last 20 calls failed).

**Monitoring**: Expose metrics for circuit breaker state (open/closed, number of trips). You want to know if a circuit is frequently tripping – that indicates persistent issues with that downstream dependency.

**Integration with timeouts & retries**: Circuit breaker often works hand-in-hand with timeouts (it counts a timeout as a failure) and with retries (breaker prevents retried calls from constantly hitting a down service). Fowler pointed out how cascading failures happen when many callers pile on an unresponsive supplier, exhausting resources – circuit breakers turn those partial failures into fast failures to avoid resource exhaustion.

**Example**: Service A calls Service B. If B goes down, A’s breaker for B opens after, say, 5 failures. For the next period, A’s calls to B instantly return a fallback (maybe cached data or an error message like “Service unavailable, please try later”) instead of hanging. After some time, the breaker half-closes and tries a call – if B is up, it resumes normal operation, if not, it stays open. This way, A remains responsive (perhaps with degraded functionality), and B is not overwhelmed with useless attempts when it’s clearly down.

### 9.2 Retry Patterns and Backoff

**Retries**: Automatically retrying a failed operation can transiently recover from glitches (like a momentary network blip or a temporarily busy service). However, as mentioned, retries must be used carefully:

- Too aggressive can cause **retry storms**. For instance, if 100 calls all time out and all retry immediately, that doubles the traffic on the struggling service.
- Use **exponential backoff**: after first failure, wait a bit, second retry wait longer, etc., to avoid synchronized retries. Possibly add jitter (randomness) to avoid patterns where many clients retry at once.
- Limit retries: maybe 3 attempts max. Beyond that, likely a bigger issue.
- Mark idempotent operations: Only safe to retry if the operation is idempotent or the client can handle duplicates. For GETs it’s fine, for POSTs causing side effects, be careful (the operation might have succeeded but response lost – then a retry could double-execute. In such cases incorporate idempotency keys or use at-least-once logic with de-duplication).

**In Spring Boot**: Resilience4j also provides a retry module. Spring Retry (spring-retry) can be used to annotate methods with @Retryable and define backoff policy.

**When troubleshooting**, look at logs to see if an operation was attempted multiple times (could indicate retries kicking in). Also ensure that the combination of retries and timeouts doesn’t lead to very long waits. For example, 3 retries with a 5s timeout each could make a user wait 15+ seconds – which might be unacceptable unless handled asynchronously.

### 9.3 Bulkheads and Resource Isolation

The **Bulkhead pattern** (named after compartments in a ship) involves isolating portions of the system so that a failure in one does not sink the whole ship. In practice, this means:

- Use separate thread pools or semaphores for different categories of tasks. E.g., isolate calls to External Service X in its own pool, separate from the main request handling pool. So if Service X is slow and threads pile up, it only exhausts that dedicated pool, not the entire server’s threads.
- Similarly, one might separate user-facing requests vs background jobs onto different thread pools or even separate service instances, so a backlog in one doesn’t block the other.
- Limit concurrency to certain operations. For instance, if writing to a slow disk or doing a big file parse, allow only N such tasks at a time to avoid exhausting CPU/memory.

**In Tomcat context**: Bulkheads aren’t directly a Tomcat feature, but you could run separate Tomcat connectors or separate microservices. More often, at the application level, we use bulkhead via separate thread pools in code or via Hystrix/Resilience4j which allows an isolation strategy (thread pool per command).

**Real example**: Netflix when open-sourcing Hystrix explained how they isolate dependencies – each external dependency wrapped in a circuit breaker, running in its own small thread pool. If a dependency becomes latent and threads fill up, only that small pool is affected (requests to that dependency get queued/rejected in that pool), while the main logic threads remain free to serve other functionality (maybe delivering partial results or graceful errors). This prevents one bad component from bringing down everything.

For architects, designing microservices themselves is a form of bulkhead: separate services for separate concerns, so one service’s crash doesn’t directly crash others (though without patterns above, it can still have indirect effects).

### 9.4 Fallbacks and Graceful Degradation

**Fallback logic** complements circuit breakers and retries. When an operation fails or circuit is open, what do we do? Options:

- Return cached data from a previous successful call.
- Return a default value or an apology message.
- Switch to a secondary service if available (redundancy).
- Degrade functionality: e.g., if the recommendation service is down, serve the page without recommendations rather than failing the whole page.

Designing good fallbacks is application-specific. But they should be in place for non-critical features. Identify which parts of the system can be temporarily sacrificed to keep core functionality alive.

**Example**: An e-commerce site might still show product pages even if the “Similar Products” section fails to load due to a service issue – just show the page minus that section, and maybe log or show a placeholder.

From a code perspective, fallback could be implemented in the catch block of a try or via circuit breaker libraries (Hystrix allowed defining a fallback method). Or simply checking if a dependent service is available (maybe via a health check call or via circuit breaker status) and skipping that step if not.

### 9.5 Chaos Engineering and Testing Resilience

**Chaos Engineering** is the practice of inducing failures in a controlled way to test the system’s resilience. Netflix’s Chaos Monkey is famous for randomly terminating instances in production to ensure the system is robust to that. In more advanced forms, they simulate network latency, outage of a dependency, etc.

For an architect, encouraging chaos testing (in staging or even production with guardrails) is a proactive way to find weaknesses. For instance:

- Run a scenario where Service B is shut down – does Service A’s circuit breaker kick in properly and does the overall user experience degrade gracefully or does it collapse?
- Introduce network latency to see if timeouts are tuned properly. If a random 2s delay in Service C causes others to break, maybe timeouts are too low or logic not handling it.
- Use tools (there are chaos engineering platforms and also manual approaches like tweaking iptables to drop packets).

**GameDays**: Many organizations do “game day” exercises where they simulate a data center outage or a major component failure and walk through how the system and team responds. This often reveals both technical and process issues to fix.

By doing this proactively, many issues in integration and resilience can be addressed before they occur unexpectedly.

### 9.6 Patterns for Load Management

On a related note:

- **Rate Limiting**: Prevent any one client or service from overloading another by enforcing limits (e.g., an API gateway might limit a client to X requests per second). If a service is being thrashed by too many requests, it might start returning 429 Too Many Requests to throttle.
- **Load Shedding**: At some point of high load, it might be better for a service to reject some requests quickly (shed load) rather than accept and time out on all. This could be a simple approach like if a queue length is too long, start dropping new requests (maybe with a graceful message). This ensures the system doesn’t enter complete thrash mode. As an analogy, better to serve 80% of users normally and drop 20% than to slow to a crawl and effectively serve 0% properly.
- **Auto-scaling**: Ensure your Kubernetes or VM auto-scaling policies are aggressive enough to handle spikes and recover from failures by adding capacity. However, note that auto-scaling takes time (order of tens of seconds or minutes), so it’s not a substitute for in-the-moment resilience mechanisms like circuit breakers or bulkheads.

### 9.7 Summary of Resilience Measures

It’s useful to compile which patterns address which problems:

- **Circuit Breaker**: Handles unreliable downstream by preventing resource exhaustion and providing quick failure when downstream is bad.
- **Retry with Backoff**: Handles transient failures (network hiccup, transient server error) without human intervention, while minimizing additional load when failing.
- **Bulkhead (Isolated Pool)**: Prevents one failing component from exhausting critical resources of the system.
- **Rate Limiting/Throttling**: Protects a service from excessive load, whether malicious or accidental.
- **Fail-fast vs Fail-slow**: Prefer to detect a likely failure fast and handle it (like circuit break) rather than waiting until threads pile up (fail-slow).
- **Graceful Degradation**: Ensures partial functionality continues in an outage.
- **Chaos Testing & Observability**: Validates these measures and ensures you're aware (via dashboards/alerts) when they are happening (e.g., how many times the fallback is being used, etc., which might indicate an issue to fix).

When troubleshooting in a resilient system, you often then check:

- Are circuit breakers opening? (If yes, investigate the underlying cause of failures, but also be glad the system didn’t crash).
- Are retries happening often? (If yes, maybe the reliability is poor).
- Did auto-scaling occur as expected during a traffic spike or did it lag?

Finally, ensure the team knows how to monitor these. Possibly integrate circuit breaker events into a centralized alerting (e.g., if breaker X is open > 1 minute, alert ops to check service B).

In the next chapter, we will consider Apache Tomcat specifics, some of which we've touched on (connectors, thread pools, etc.), but we’ll cover any remaining Tomcat-focused issues.

## 10. Apache Tomcat: Configuration and Tuning

Apache Tomcat is the servlet container underpinning many Spring Boot applications (embedded) or running standalone for deployed WARs. Properly configuring Tomcat is essential for both performance and stability. In this chapter, we concentrate on Tomcat-specific considerations: connector configuration (HTTP threads, connection pool, timeouts), memory settings unique to Tomcat, and troubleshooting typical Tomcat errors.

### 10.1 Embedded vs External Tomcat

**Embedded Tomcat (Spring Boot)**: Spring Boot by default uses an embedded Tomcat (or optionally Jetty/Undertow). Embedded Tomcat configurations are usually done via `application.properties` (for example, `server.tomcat.max-threads`, `server.tomcat.accept-count` for queue length, `server.tomcat.max-connections`, etc.). The Boot team selects safe defaults suitable for many applications (e.g., maxThreads=200). One must adjust these based on expected load:

- If you have an I/O heavy service, you might increase `max-threads` so it can handle more concurrent requests without queueing (given enough CPU to handle them when they’re not blocked).
- `accept-count` is the queue length for incoming connections when all threads busy. If you set it too low, clients may get connection refused faster; too high and you might queue too many (maybe better to let clients see a quick rejection than wait forever).

**External Tomcat**: Some organizations deploy Spring applications as WARs to a Tomcat instance. In that case, configuration is done in `server.xml` or setenv scripts. Many of the tuning principles are the same, but there are additional considerations:

- Align Tomcat version with Java and Spring (as mentioned, Spring 6 needs Tomcat 10). If you deploy on the wrong Tomcat version, you could get class incompatibility.
- Tomcat’s own memory usage: Tomcat doesn’t consume a lot outside the webapps, but each webapp classloader and any JNDI resources, etc., contribute to metaspace and native threads usage.
- If multiple webapps in one Tomcat, one app can impact others (one reason Spring Boot favors one app per container). For troubleshooting in external Tomcat, one might look at Tomcat manager status to see thread usage per webapp, etc.

**AJP Connector**: If using AJP (with an httpd front), ensure secure configurations (there was the Ghostcat vulnerability on default AJP open to internet). Usually, microservices won’t use AJP unless integrating with older infrastructure.

### 10.2 Connector and Thread Pool Settings

We already covered thread pool tuning in section 4 and 6. To recap and extend specifically:

- **maxThreads**: The maximum number of request processing threads per connector (HTTP). It's crucial for throughput. Set it according to expected concurrent requests. If too low, throughput will be limited and clients queued (Tomcat will queue up to acceptCount). If too high and the workload is CPU-bound, threads beyond CPU count won't help much (and each thread uses memory \~ a few hundred KB stack plus overhead).
- **minSpareThreads**: Tomcat will keep at least this many idle threads ready. If you expect bursts, you can set a decent minSpare to avoid cost of creating new threads during burst.
- **maxConnections**: In Tomcat NIO (default), this is max simultaneous connections (keep-alive connections count too). If you expect many keep-alive clients, bump this above maxThreads (because connections can be idle waiting).
- **connectionTimeout**: (socket timeout for waiting for request data). Default 20s. If clients sometimes hang or send slowly, Tomcat will close after this. You might reduce it to free threads sooner if you don't want to wait that long for slow clients.
- **keepAliveTimeout**: By default same as connectionTimeout. If you want to fine-tune how long to keep connections alive, you can reduce it. Long keep-alive saves the cost of re-handshake for frequent callers, but tying up a connection slot for too long for infrequent callers can be wasteful.
- **maxKeepAliveRequests**: By default, Tomcat allows 100 requests per keep-alive connection before closing. If you have HTTP/1.1 clients making many requests, you could increase it. For HTTP/2, it's different (multiplexing).

**Tomcat Executor**: As cited earlier, you can define a shared executor (thread pool) and have connectors use it. This is useful if you have multiple connectors (say HTTP and AJP) and want to share threads. It also allows Tomcat to **reduce threads** when idle (the executor can shrink pool threads, whereas a connector’s own pool does not shrink by default, only grows up to max and stays). If memory is a concern, an executor might be helpful to not have hundreds of threads hanging around idle.

**Tomcat and Virtual Threads (Project Loom)**: Not as of Tomcat 10, but looking forward, Tomcat might support virtual threads for request processing, which could drastically change tuning (not needing 200 physical threads, etc.). But that's experimental.

### 10.3 Tomcat Memory and Resource Settings

Memory settings largely come from the JVM (heap, etc.), but Tomcat has specific things:

- **Java Heap**: Set via CATALINA_OPTS if external Tomcat, or via the JVM args in Spring Boot. Ensure it's sized well, as discussed. If multiple apps, consider each app's need.
- **Thread Stack Size**: Rarely needed to tune on modern systems, but if you have deep recursion you might need to increase thread stack (`-Xss`). However, more threads means more aggregate stack memory usage (maxThreads \* Xss).
- **Connection Buffer Sizes**: Tomcat NIO connector has `socket.rxBufSize` and `socket.txBufSize`. Tuning these can affect throughput for sending large responses or reading large requests. eG suggested possibly increasing to 64KB or higher for better throughput on high-latency networks. But the defaults are usually fine (most OS default buffers are fine on LAN). Only consider if dealing with high-bandwidth scenarios (like file download service).
- **Protocol selection**: Tomcat supports NIO (Java non-blocking IO, default), and possibly APR/native (if native libs are installed) which can use OS sendfile etc. For most cases, Java NIO is good enough. APR might give some benefits in specific scenarios or allow use of OpenSSL directly for SSL.
- **Compression**: In Tomcat, `compression="on"` and setting `compressibleMimeType` (by default text/\* and some others). If CPU is plenty and network is a bottleneck, ensure compression is on. We saw how it can reduce traffic massively for text responses. Conversely, if CPU is tight and responses are small, turning compression off could save CPU (tiny responses don't benefit much from compression).
- **SSL configuration**: If using SSL directly on Tomcat, ensure to use modern protocols (TLS1.2+), HTTP/2 if needed (set `protocol="org.apache.coyote.http11.Http11AprProtocol"` with OpenSSL or use the NIO2 with ALPN for HTTP/2). Also consider setting `maxHttpHeaderSize` if you have large headers (JWT tokens etc.), default 8k might be insufficient and cause 400 errors if exceeded. Increase to 16k or 32k if needed (be mindful of memory if you expect huge headers rarely).
- **Error handling**: Custom error pages vs default. Not performance but user experience.

**Common Tomcat-specific errors**:

- **“Too many open files”**: If under high load, you might hit OS limits for file descriptors (each socket counts). This is not Tomcat config but OS config (ulimit). Ensure to set ulimit nofile high (e.g., 10k or more) if expecting many connections. Tomcat will log if it can’t accept because of this.
- **OutOfMemory: PermGen/Metaspace**: If deploying/redeploying on external Tomcat, memory leaks can lead to PermGen (on Java 7) or Metaspace (Java 8+) OOM as discussed. Tomcat has listeners that try to clean known offenders (JDBC driver dereg, ThreadLocal clean). Still, ideally fix the app leak. In short run, increasing Metaspace can postpone the issue, but better to eliminate the leak source (see Chapter 5).
- **Session persistence issues**: Tomcat can persist sessions to disk on shutdown by default (manager serialization). In microservices, often stateless or using external session stores, so it's often disabled or irrelevant. But if you see warnings about session serialization failing, you might disable that (set `saveOnRestart="false"` in Context).
- **Incorrect URI encoding**: Sometimes if not configured, Tomcat might treat %2F in URLs as literal '/' or reject; config like `allowEncodedSlash` can be toggled if needed.
- **Proxy misconfiguration**: If Tomcat is behind a proxy, ensure the proxy passes correct `X-Forwarded-*` headers and configure `RemoteIpValve` so that Spring Boot knows the correct client IP and scheme. Otherwise, you might have issues with redirect URLs (HTTP vs HTTPS) or logging wrong client IP.

### 10.4 Monitoring Tomcat in Production

Apart from general app metrics, some Tomcat-specific things:

- Tomcat MBeans (if JMX enabled) provide info like current thread count, current threads busy, request count, processing time, etc. Spring Boot’s metrics incorporate some of these. For example, Micrometer can pull `tomcat.sessions.active` etc. If using an external Tomcat, consider enabling JMX and using tools to collect those (e.g., JConsole or Jolokia agent with Prometheus JMX exporter).
- **Access Logs**: Ensure access logging is on in Tomcat (embedded Boot defaults to off to not create files, but you can enable a Valve for access log or use an alternative like logging the requests in Spring). Access logs are key for troubleshooting slow or failed requests from the perspective of Tomcat.
- **Thread dumps**: On external Tomcat, you might not have Spring Actuator to get dumps easily; use `jstack` on Tomcat process.
- **Tomcat Manager**: If running external Tomcat, the Manager webapp can show status of threads, memory, sessions per app, etc. It’s a quick way to check if one webapp has excessive sessions or threads in use.

### 10.5 Hardening and Security

While not exactly troubleshooting, misconfiguration can lead to security issues:

- Disable or secure the Tomcat manager and host-manager in production (if you even have them deployed).
- Change the default shutdown port (8005) or better, disable the shutdown listener (someone could send shutdown command if port is open).
- Use TLS for all traffic, obviously.
- Keep Tomcat updated; new versions contain not just features but important security fixes.

### 10.6 Summary of Tomcat Tuning Tips

Let's summarize key Tomcat tuning items:

- **Thread Pools**: Ensure `maxThreads` is sufficient for your concurrency, but not excessive. Monitor threads in use and adjust. Use an executor if needing to reclaim threads on idle.
- **Connection Backlog**: `acceptCount` should be set to how many connections can wait if all threads busy. If too low, clients get connection refused quickly under load. If set high, those clients will wait (they might time out on their side).
- **TimeOuts**: `connectionTimeout` – usually fine default (20s). Could lower if you want to free threads faster from slow clients. `keepAliveTimeout` – might set lower than connectionTimeout if you want to aggressively close idle keep-alives.
- **Max Connections**: If expecting thousands of keep-alive connections, raise `maxConnections`. Otherwise, default (typically 10k) is fine.
- **Memory**: Use appropriate heap (Xmx) and ensure `MaxMetaspaceSize` is set to avoid unbounded metaspace growth if leaks.
- **GC**: If using large heaps, consider G1 GC as recommended for server applications.
- **OS**: High file descriptor limit, adequate user processes limit (if you spawn processes).
- **Tomcat clustering**: If using Tomcat session replication (likely not in microservices but in older setups), tune the cluster sender threads, etc., or consider modern stateless approaches instead.
- **Logging**: Tomcat internal logs (catalina.out) and application logs should be separated if possible (Spring Boot does log to console which ends up in catalina.out if external). Use a logging framework that rotates files, etc. Ensure you don’t fill disk with logs.

By properly tuning Tomcat and understanding these settings, many performance issues can be avoided (like not hitting thread starvation or out-of-file descriptors at peak).

Finally, we have covered from the code internals to the server config. The next chapter will discuss infrastructure and deployment, bridging into DevOps territory, which ensures that the software architecture plays well with containerization, CI/CD, and cloud environment.

## 11. Infrastructure and Deployment Considerations

Software doesn't run in a vacuum; how we deploy and operate Spring Boot applications (especially in containers and on Kubernetes or cloud VMs) significantly affects troubleshooting and stability. This chapter addresses the _operational architecture_: Docker configuration, Kubernetes orchestration settings, CI/CD pipelines, and cloud-native patterns that an architect should consider.

### 11.1 Containerization (Docker) Best Practices

Most Spring Boot microservices are packaged as Docker images for easy deployment. Some points to consider:

- **JVM Memory in Containers**: As discussed, ensure the JVM respects container limits. For Java 11+, it's automatic; for Java 8, use `-XX:+UseContainerSupport` (from 8u191 onwards; older versions need manual `-Xmx` tuning). Set Xmx a bit below the container limit (e.g., if container memory limit is 512M, maybe Xmx=460M to leave room for code cache, threads, etc.). Also set `-XX:MaxMetaspaceSize` to avoid metaspace growing unbounded if there's a leak.
- **CPU limits**: The JVM also can respect cgroups for CPU. If you set CPU limits, the JVM will see a lower number of processors. This affects ForkJoinPool and other internal sizing. For instance, if you limit to 0.5 CPU in K8s, the JVM might see 1 CPU (or sometimes fraction not handled, depends on version). It's often better to set requests/limits in whole CPUs to avoid confusion (or use the `-XX:ActiveProcessorCount` flag to explicitly set CPU count if needed).
- **Image Build**: Use lean base images (e.g., adoptopenjdk:17-jre-slim or eclipse-temurin, or even distroless Java for minimal attack surface). A smaller image is easier to distribute and has fewer security vulnerabilities.
- **Layering**: Leverage Docker layering to cache dependencies: Spring Boot's layered jar (since 2.3) can create separate layers for dependencies vs application classes. Use that in your Dockerfile so that if you change your app code, you don't re-download all dependencies (which speeds up builds).
- **Healthcheck in Docker**: Define a Docker HEALTHCHECK that calls the `/actuator/health` or a lightweight endpoint. This allows Docker to mark the container unhealthy which K8s can use (though in K8s usually liveness/readiness probes are used directly).
- **File system**: If the app writes files (logs, temp files), ensure volumes if needed. Generally prefer logging to stdout (12-factor) so that the platform (Docker/K8s) collects logs. If using an embedded database (H2) for some reason, data might need a volume to persist (though in microservices likely external DB is used).
- **Timezones/Locales**: If your app expects a certain locale, make sure the base image has it or configure the JVM with `user.timezone` property.
- **JDK vs JRE in container**: If using a JDK base image, you're carrying extra weight (tools like javac, etc.). Use a JRE or runtime image for production containers to reduce size unless you specifically need tooling inside the container (which is rare). Newer distributions (like Temurin) have jre variants or use jlink to create custom slim runtime images.
- **Security**: Run as non-root in the container. Spring Boot doesn’t need root. Either use a base image that defines a non-root user or specify `USER` in Dockerfile after adding app jar. Also limit capabilities (though using a high-level base image typically handles this). Ensure any secrets (DB passwords, etc.) are not baked into image but provided via env vars or mounted files.

### 11.2 Kubernetes Orchestration and Cloud-Native Ops

Deploying on Kubernetes (or similar orchestrators) introduces a lot of config:

- **Liveness and Readiness Probes**: These are critical. A readiness probe (often hitting `/actuator/health`) makes sure the service only gets traffic when it’s ready (like after warming up caches or after establishing connections). If misconfigured, a pod might receive traffic too early and fail. A liveness probe can auto-restart a stuck container (for example, if deadlocked or OOMed and not fully crashed). Ensure the probes are not too sensitive (so they don’t cause flapping restarts due to minor hiccups) but also not too lax. Use Spring Boot's health groups to perhaps have a readiness health that checks downstream dependencies, etc.
- **Resource Requests/Limits**: Set appropriate CPU and memory requests/limits for each service to ensure stable scheduling and to avoid noisy neighbor issues. Tune these based on profiling under load.
- **Horizontal Pod Autoscaler (HPA)**: If enabled, make sure it scales on relevant metrics (CPU is common, but consider custom metrics like request latency or queue length). The HPA should respond before the service is completely overwhelmed. E.g., if CPU > 80% for 5 minutes, scale out.
- **Service Mesh / Networking**: If using Istio/Linkerd, etc., they add another layer that could affect things. For example, mTLS might cause initial slight delays, or misconfig could block traffic. When troubleshooting connectivity, verify if the mesh sidecar is healthy (sometimes the sidecar itself might crash or consume memory).
- **ConfigMaps and Secrets**: Externalize configuration via ConfigMaps/Secrets. Watch out for config changes: Spring Boot Actuator has /refresh endpoint (with Spring Cloud) to reload config, or you might restart pods on config changes. If a configMap is updated but pods not restarted (and you’re not using dynamic refresh), pods may still use old config – be mindful and have a strategy (like rolling restart on config changes).
- **Logging and Monitoring**: Use sidecar pattern or DaemonSets for log aggregation (e.g., Fluentd to Elastic, or a dedicated log agent container). Ensure logs from each pod are tagged with pod name, etc., for traceability. Use Kubernetes labels to group logs/metrics per service.
- **Ingress and Load Balancing**: If issues at the edge (like user can't reach service), check ingress controller logs and config. Sometimes path rules or host rules misrouted traffic. Also, consider client-side load balancing vs service-side. In Spring Cloud (Netflix OSS), you might have Ribbon in the app doing load balancing; in K8s one typically relies on Service (which load-balances across pods) plus an Ingress or API Gateway. If using gateway, ensure its timeouts are configured to slightly larger than service timeouts, so it doesn’t cut off responses prematurely.
- **DNS**: In K8s, DNS resolution issues can occur if CoreDNS is under pressure. If you see intermittent resolution failures, maybe scale CoreDNS or use caching in clients.

### 11.3 CI/CD Pipeline Integration

A robust CI/CD pipeline helps catch issues early:

- **Automated Testing**: Beyond unit and integration tests, incorporate performance tests or at least some stress tests in a staging environment as part of pipeline (maybe nightly or triggered on demand). This can catch performance regressions (e.g., memory leaks introduced by a change) before production.
- **Static Analysis and Scanning**: Tools like SonarQube can catch potential concurrency issues (like dubious synchronized usage) or memory issues (like huge objects) by code inspection. Security scanners can find dependencies with known vulnerabilities so you can update before issues occur.
- **Container Scanning**: Scan Docker images for vulnerabilities (so you can update base images).
- **Infrastructure as Code**: Use Terraform, Helm, etc., and version control them. This ensures the config deployed is repeatable. If a problem happens, you can trace it to changes in code or infra config clearly.
- **Blue-Green / Canary Deploys**: These strategies can reduce downtime and allow quick rollback. For instance, deploy v2 while v1 is still running, test it (maybe with a small portion of traffic = canary), then switch. If issues, easy to switch back. This minimizes time spent troubleshooting in a crisis because you can just revert to stable version and then diagnose v2 offline.
- **Distributed Tracing in CI**: Some advanced pipelines run synthetic transactions or integration tests in an environment and capture traces which they can analyze for regressions (like an integration call that suddenly takes longer).

### 11.4 Cloud Services and Managed Infrastructure

If using managed services (DBaaS, cache as a service, etc.):

- **Connectivity**: Ensure network (VPC, security groups) allows your app pods to reach the service endpoints. Many a time, a misconfigured security group or network ACL is the reason a service cannot talk to a database.
- **Credentials**: Use cloud secret managers (AWS Secrets Manager, etc.) to supply credentials. Ensure rotation policies do not break your app (if credentials rotate, the app should pick up new ones ideally without restart).
- **Scaling**: If your app auto-scales, ensure your database or other dependencies can handle that scaling (may need to scale those too or use serverless variants that auto-scale).
- **Cloud Logging/Monitoring**: Integrate with cloud monitoring (like CloudWatch, Azure Monitor). Send custom metrics or at least ensure the basics (CPU, memory, restart count) are captured and alerted.

### 11.5 Patterns like 12-Factor for Deployments

The Twelve-Factor App methodology is practically a guideline for CI/CD and cloud-native:

- **Config as environment variables**: We already ensure that (no hard-coded configs).
- **Logs as event streams**: we direct logs to stdout/err for collection.
- **Disposability**: Fast startup and graceful shutdown. For K8s, graceful shutdown is vital: Spring Boot should handle SIGTERM by gracefully shutting down (it does via Spring context close). You can configure a `preStop` hook in K8s to call `/actuator/shutdown` (for example) or just rely on Spring Boot’s shutdown handling. Also set `terminationGracePeriodSeconds` such that the app has time to finish processing ongoing requests when shutdown signal comes (e.g., 30 seconds).
- **Dev/prod parity**: Use similar environments. If you containerize, run the container locally for testing (maybe with Docker Compose or kind for K8s). This avoids “it works on my machine but not in prod” issues because of environment differences.
- **Release management**: Use proper versioning for artifacts and have the ability to roll back easily.

### 11.6 Example: Troubleshooting in a CI/CD Context

Imagine a scenario: You deploy a new version and your Kubernetes liveness probe starts failing, causing the pod to restart repeatedly (“CrashLoopBackOff”). How to troubleshoot:

1. Describe the pod to see events: maybe it says liveness probe failed, or OOMKilled.
2. If OOMKilled, then likely the memory limit was too low or a memory leak triggers quickly. Check logs (if any before kill) or run the container locally with same settings to reproduce. Solution: raise limit or fix leak.
3. If liveness failed, check what the liveness probe does. If it hits `/health` and that now returns down (perhaps because a new health check was added that fails due to missing config?), then the app is considering itself unhealthy and K8s kills it. Possibly a misconfiguration (e.g., a new dependency not available, so health check fails). Solution: fix config or adjust the health check to not fail on that (or mark it readiness only).
4. Or maybe the app isn’t even starting (probe fails because app never up). Then use `kubectl logs` to see startup logs. Might find a Spring Boot exception (e.g., couldn’t connect to DB -> maybe secret wrong). Then correct the secret or config map via pipeline and redeploy.

CI/CD pipelines should ideally catch some of these (like a config mistake might be caught if you have integration tests that validate connectivity using test configs). But production is the real test; having good observability at infrastructure level (K8s events, etc.) plus application logs is key.

### 11.7 Summing Up Infrastructure Strategies

Architects should work closely with DevOps/SRE teams or adopt a DevOps mindset to ensure:

- The system is observable at both app and infrastructure levels.
- Deployments are smooth and issues can be rolled back.
- The architecture can adapt to infra failures (if a node goes down, pods reschedule, etc., ensure state is not lost - stateless or external state).
- The cost is optimized (over-provisioning resources can be wasteful; under-provisioning causes performance issues - find the right balance via load testing and monitoring).

This also touches on reliability engineering: define SLOs for services (e.g., 99.9% uptime, response in 200ms 95th percentile). Then design infra (redundancy, failover) to meet those. If using cloud multi-region deployments for high availability, ensure your app supports that (e.g., can handle active-active with a distributed database or active-passive with quick failover).

Now we proceed to the final chapter, summarizing all these practices and providing quick lookup tables for error types, root causes, and solutions.

## 12. Summary of Best Practices and Error Resolution

In this concluding chapter, we consolidate the insights from throughout the document. We provide a high-level checklist of best practices for software architects in charge of Spring Boot microservices on Tomcat, and we include summary tables of common issues, their root causes, detection techniques, and resolution strategies as a quick reference.

### 12.1 Comprehensive Checklist for Architects

**Design & Code Level:**

- _Use proven frameworks correctly:_ Rely on Spring Boot auto-configuration and conventions to avoid common mistakes. Only override defaults with good reason, and document such changes.
- _Write idempotent and fault-tolerant integration code:_ Ensure external calls have proper timeouts and retries (with backoff). Use circuit breakers to prevent cascade failures.
- _Avoid shared mutable state:_ Design services to be stateless wherever possible (store state in databases, not in-memory across requests), which simplifies concurrency and scaling.
- _Implement proper error handling:_ Catch exceptions at service boundaries and return meaningful errors or fallbacks. Ensure resources (DB connections, streams) are closed in finally blocks or use try-with-resources.
- _Include context in exceptions:_ E.g., when throwing a custom exception, include which service or operation failed, to speed up pinpointing issues when reading logs or traces.

**Observability & Monitoring:**

- _Centralize logging and ensure they are informative:_ Log key events, but avoid overly verbose logs at INFO level in production. Use structured logging for easier querying.
- _Metrics dashboards:_ Have dashboards for each service and overall system, showing metrics like request rate, error rate, latency percentiles, CPU, memory, GC time, etc. Also include business metrics (transactions per minute, etc.).
- _Alerting:_ Set up alerts on symptoms (high error rate, high latency, memory nearing limit, etc.) and also on cause indicators (e.g., thread pool exhausted, circuit breaker open for >N minutes).
- _Distributed tracing:_ Ensure each request can be traced across services with an ID. Use tools to visualize traces to quickly identify where slowdowns or errors occur.

**Performance & Capacity:**

- _Load testing:_ Do regular performance tests to know the capacity of each service and the system. Determine the breaking points (max RPS, max concurrent users) and plan capacity accordingly (with some headroom).
- _GC tuning and monitoring:_ Pick a garbage collector suitable for your needs (G1GC is usually a safe default). Monitor GC logs in staging under load to ensure no long pauses. Tune heap size and pause goals if needed.
- _Thread pool sizing:_ Right-size Tomcat thread pools and any async executors. Monitor actual usage to adjust. Use bulkheads (separate pools) for isolation of slow tasks.

**Resilience & Recovery:**

- _Circuit breakers & Bulkheads:_ Implement them on all network calls to external systems or between services. Monitor their activity.
- _Graceful degradation:_ Decide what the system should do if a component is down (serve cached data? show partial UI?). Implement those fallbacks.
- _Time-out strategy:_ A hierarchy of timeouts (client – gateway – service – internal calls) should be set such that each layer times out slightly sooner than the layer above, to avoid one layer waiting long after the other has given up.
- _Chaos testing:_ Periodically simulate failures (shutdown instances, inject latency) in a test environment (or production with minimal impact) to verify the system’s resilience mechanisms actually work.

**Configuration & Deployment:**

- _Externalize all config:_ No secrets or env-specific config in code. Use environment vars or config server. This prevents mistakes like using dev DB in prod or vice versa.
- _Consistent environments:_ Keep dev/staging as close to prod as possible (similar Tomcat/JDK, similar scaling topology) to catch issues early.
- _CI pipeline tests:_ Include tests for config correctness (maybe a startup test that loads all contexts with prod-like config), security scans, and maybe automated chaos tests or memory leak detection runs (like run a soak test and analyze heap).
- _Rolling deployment strategy:_ Use blue-green or canary deployments to minimize impact of new bugs. Ensure ability to roll back quickly (immutable infrastructure helps: you can just route traffic back to old version).
- _Documentation and runbooks:_ Document common failure scenarios and known solutions. E.g., “If service X is slow, check if database index Y exists” or “If out of memory, see if some config was changed to allow unlimited cache”. This helps on-call engineers troubleshoot faster.

**Tomcat & Server:**

- _Tune Tomcat as needed:_ e.g., for high loads, increase `maxThreads`; for many idle connections, increase `maxConnections`. For large requests or responses, consider raising `maxHttpHeaderSize` or buffer sizes.
- _Keep Tomcat and Java updated:_ Use latest stable releases to benefit from performance improvements (JDK updates can give 5-20% perf gains) and security fixes.
- _Use HTTPS and secure configs:_ Ensure connectors are configured for TLS (and HTTP/2 if beneficial). Disable weak ciphers.
- _Monitor Tomcat specifics:_ Keep an eye on thread pools (via JMX) and connector stats. For external Tomcat, the Manager app or JMX can show if threads are maxed out or if request processing time is spiking.

### 12.2 Quick Reference Tables

Finally, we present summary tables that categorize common issues (drawn from previous chapters) with causes and resolutions. These serve as a quick lookup.

**Table 12.1: Runtime Errors and Failures**

| **Issue**                     | **Symptoms**                                                                                                             | **Root Cause**                                                                                                                                                        | **Resolution**                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **High CPU usage, slow**      | 100% CPU, requests slow, high latency                                                                                    | Hot loop or inefficient algorithm; too many threads context-switching; GC thrash if CPU spent in GC                                                                   | Profile to find hot code and optimize (improve algorithm, add caching). Reduce unnecessary concurrency. Tune GC or increase heap if GC overhead is high.                                                                                                                                                                                                                                    |
| **Memory leak (OutOfMemory)** | Gradual memory growth, eventually OOM error; frequent full GCs freeing little memory                                     | Unreleased references (static collections, ThreadLocals, etc.); excessive cache with no eviction; classloader leaks on redeploy                                       | Analyze heap dump to identify leaked objects and references. Fix code to remove or weak-reference them. Add cache eviction or size limit. For classloader leaks, ensure threads and drivers are cleaned up on undeploy.                                                                                                                                                                     |
| **Thread deadlock**           | Application hung, certain requests never complete; thread dump shows deadlock cycle                                      | Two or more threads waiting on locks held by each other (improper lock ordering)                                                                                      | Use thread dump info to locate code causing deadlock. Refactor to avoid nested locks or enforce consistent lock ordering. Possibly replace explicit locks with concurrent utilities or redesign to not need locking.                                                                                                                                                                        |
| **Thread pool exhaustion**    | Requests queue up (Tomcat acceptCount overflow), throughput plummets; thread dump: many threads waiting on I/O or locks  | Too many threads tied up (e.g., waiting on slow DB or external calls with no timeout) causing no free threads; or tasks submitted to a limited pool outnumber threads | Increase `maxThreads` if CPU can handle it. More importantly, fix root cause: add timeouts to external calls so threads don’t wait forever; use asynchronous processing if appropriate to free threads during waits. For internal pools, increase pool size or use separate pools (bulkhead) to isolate blocking tasks.                                                                     |
| **Frequent GC pauses**        | App pauses periodically (e.g., 1s pause every 30s); GC log shows many collections; CPU usage might be high in GC threads | Heap too small for workload (constant allocation pressure or large live set); using unsuitable GC algorithm for pause-sensitive environment                           | Increase heap (`-Xmx`) so that GC is less frequent. If pauses still long, tune GC: for example, G1GC with a target pause time, or consider Shenandoah/ZGC for low-pause needs. Also check for large object churn – if possible, optimize code to allocate less (reuse objects or use pools for short-lived high-cost objects).                                                              |
| **Slow database queries**     | High response times, threads waiting on DB; DB CPU high, maybe timeouts or deadlocks at DB                               | Missing indexes, poorly written SQL (N+1 queries causing many calls), or DB connection pool exhausted causing wait                                                    | Identify slow queries (enable SQL logging or APM database trace). Add indexes or optimize query logic (batch operations, avoid N+1 by proper join fetch). Increase connection pool if threads often wait for a connection, but also ensure DB can handle more connections. If DB itself is bottleneck, consider caching frequently read data or scaling the database (read replicas, etc.). |
| **Service call timeouts**     | Calls to another service fail with timeout, error logs show `ReadTimeout` or similar; possibly circuit breaker opens     | Downstream service is down or slow; or network issues dropping packets; no timely response                                                                            | Verify health of downstream service. Implement a retry with backoff for transient issues. If persistent, circuit breaker will prevent repeated hangs. Investigate network (DNS resolution, load balancer) if service should be up. Adjust timeout if needed (if too strict for normal response).                                                                                            |
| **Authentication failure**    | API calls returning 401/403 errors unexpectedly                                                                          | Misconfigured auth (token not sent, or wrong audience/scope); clock skew causing token expiry; cert or key rotation issues                                            | Ensure client includes correct auth token and it’s refreshed properly. Check configuration of auth server and resource server – scopes match, time sync (NTP) is correct. Update any rotated credentials (e.g., if using certificates, ensure new cert is mounted).                                                                                                                         |
| **Client-side errors (400)**  | One service receives HTTP 400 from another (bad request)                                                                 | Contract mismatch – request format incorrect (missing required field, wrong content type); or version incompatibility in API                                          | Compare request against API specification. If a field was renamed or validation tightened in the new version, update the client to send correct data. Implement backward-compatible changes or versioned endpoints to avoid such issues.                                                                                                                                                    |

**Table 12.2: Deployment and Environmental Issues**

| **Deployment Issue**                  | **Symptoms**                                                                                                                               | **Root Cause**                                                                                                                                                              | **Resolution**                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Container OOMKill**                 | Container killed by Kubernetes (OOMKill in events) – app log abruptly ends; pod restarting                                                 | Process exceeded container memory limit (cgroups) – either memory leak or just too low limit for workload                                                                   | Increase container memory limit if usage was expected to grow that high. If leak, fix leak (see memory leak above). Add monitoring on memory to catch nearing limits. Also ensure JVM is configured to stay within limit (Xmx).                                                                                                                                                                    |
| **CrashLoopBackOff**                  | Pod starts, then crashes repeatedly (K8s)                                                                                                  | Could be uncaught exception on startup causing immediate exit; or failing liveness probe causing K8s to restart pod; or misconfiguration (e.g., wrong command causing exit) | Check pod logs to see if Spring Boot application threw an exception on startup (common: config missing leading to BeanCreationException). Fix config or code accordingly. If liveness probe is the issue (app isn't ready in time), consider lengthening initial delay or fixing the app to start faster (e.g., defer heavy initialization or increase resources).                                 |
| **Service not reachable**             | Requests to service URL time out or give host unknown; in K8s, Service IP not responding                                                   | DNS or service registry not resolving to any instance; or network policy blocking traffic; or all pods of that service are down                                             | Verify that service is registered (in K8s, `kubectl get endpoints` for the service to see if pods listed). If none, then pods aren’t ready or label selector mismatch – fix deployment labels or wait for pods. If DNS issue, check CoreDNS logs or configuration. If using service mesh, check sidecar is functioning.                                                                            |
| **Config not applied**                | After deployment, app using default config (e.g., connecting to wrong endpoint or missing a feature)                                       | Forgot to set environment variable or ConfigMap in deployment; or wrong profile active; possibly secret not mounted due to naming error                                     | Double-check the deployment manifest/Helm values for config. Ensure the env var names match what the app expects (Spring Boot expects e.g. `MY_PROP` to map to `my.prop`). Verify profile via logs (Spring logs active profiles on startup). Mount and reference secrets correctly (check volume mount path or env var reference).                                                                 |
| **TLS/Cert issues**                   | Service fails to connect over SSL (e.g., to database or another service) – SSLHandshakeException; or browser fails to trust service’s cert | Certificate trust issue: perhaps missing root CA in truststore, or wrong cert presented (like using a dev self-signed cert in prod), or hostname mismatch                   | Import necessary CA certificates into truststore (or use container’s CA certs if available). If using Spring’s SSL config, ensure keystore/truststore paths and passwords are correct. For outbound calls, if self-signed, either add to truststore or enable skipping verification (not recommended for prod). Ensure certificates are valid (not expired) and CN/SAN matches the hostnames used. |
| **Slow startup**                      | Application takes an unusually long time to start (delaying readiness)                                                                     | Could be trying to connect to something that’s down (e.g., waiting on DB connection timeout), doing large data load at boot, or insufficient CPU causing slow processing    | Identify startup bottleneck: logs can show which step hangs. If waiting on external resource, consider making that config lazy or optional on startup (or ensure the resource is available). Increase the CPU request for the pod so it gets enough CPU to start. Use Spring Boot's startup actuator or Java Flight Recorder events to profile startup if needed.                                  |
| **Inconsistent env between dev/prod** | Bugs appear in production that were not visible in dev/test (e.g., case sensitivity, locale issues, etc.)                                  | Environmental differences: OS (Linux vs Windows), case-sensitive file system, different default locale or timezone, different JVM args, etc.                                | Align environments: run tests in a Linux container similar to prod. Explicitly set locale/timezone if assumption in code. Use containerization in dev to match prod environment as much as possible. Add tests for environment-specific aspects if known (for example, file path case tests).                                                                                                      |

**Table 12.3: Tools and Techniques Quick Guide**

| **Need**                      | **Recommended Tools/Techniques**                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Thread dump analysis**      | Use `jstack` for on-demand dump; or Spring Actuator `/dump` (if enabled). Tools like FastThread or Samurai can format dumps. Look for “deadlock” keyword or common stack traces showing waits.                                                                                                                                                                                                           |
| **Heap dump/memory analysis** | Generate heap dump (`jmap -dump` or OnOutOfMemoryError option). Analyze with Eclipse MAT. Look at Leak Suspects, Dominator tree for large retained memory. Use JFR’s heap statistics for leak sampling.                                                                                                                                                                                                  |
| **GC analysis**               | Enable GC logs (`-Xlog:gc*` for Java 11+). Use GC Easy online analyzer or gceasy.io blog for common patterns. Key metrics: GC frequency, pause times, GC cause (if many “Promotion failed” consider larger heap or tuning). Check GC overhead percent – if >5-10%, consider action.                                                                                                                      |
| **Performance profiling**     | Java Flight Recorder (low overhead, good for production snapshot). JProfiler/YourKit for deep dive in test environment. For CPU, sample profiling is safer (less overhead) – highlight hotspots. For synchronous web apps, also measure endpoint-specific times (Spring Boot metrics or APM).                                                                                                            |
| **Database analysis**         | Enable slow query log on DB (if possible). Use APM with a DB probe to see which queries slow. Profiling in app might show time in JDBC calls. Tools like pgBadger (for Postgres) or OEM (Oracle Enterprise Manager) can help for DB-side. Ensure connection pool metrics are exposed – if active connections = max, then pool is a bottleneck.                                                           |
| **Distributed tracing**       | Implement OpenTelemetry or Zipkin. Use a trace UI to follow a request’s path, see timing at each service. Great for pinpointing which service in a chain is slow or throwing error. It also helps correlate logs by trace ID across services.                                                                                                                                                            |
| **Monitoring Dashboards**     | Grafana with Prometheus (common stack). Use Micrometer to feed Prometheus. Have dashboards by service and one global. Key panels: RPS, latency (avg, 95th, 99th percentile), error rate, instance count, CPU/mem of pods, GC time, DB connection usage, thread pool usage. Update these as you learn new failure modes (e.g., add a panel for circuit breaker open count if using Resilience4j metrics). |
| **Incident response**         | Maintain runbooks as living documents. For example, “If latency spike: check Grafana -> if external calls slow, possibly issue with dependency. If CPU high, see APM profile or thread dump…”. This guides on-call engineers. Also, use synthetic checks (ping services periodically) to detect issues before users do.                                                                                  |
| **Capacity planning**         | Use load test results and production usage to forecast usage. Employ auto-scaling but also know the limits. If expecting traffic surge (marketing event), test at that scale in advance. Monitor resource usage trend – e.g., memory creeping up might indicate a leak – schedule proactive fix rather than react to OOM.                                                                                |

### 12.3 Final Thoughts

Troubleshooting complex systems is as much about **process** as tools: collect data, form a hypothesis, test it, and iterate. Always communicate with your team and possibly users about issues and mitigation steps. As an architect, promote a culture of _proactive detection_ (through monitoring and testing) so that many issues are resolved before they become incidents in production.

By following the guidelines in this document – from strategic design principles to tactical debugging tips – software architects can significantly reduce downtime and ensure that when problems arise, they are quickly diagnosed and resolved. Building a resilient, observable, and well-understood system is the best way to keep a Java Spring Boot microservices architecture running smoothly on Apache Tomcat in production.
