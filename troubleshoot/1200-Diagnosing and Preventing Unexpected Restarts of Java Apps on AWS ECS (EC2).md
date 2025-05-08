# Diagnosing and Preventing Unexpected Restarts of Java Apps on AWS ECS (EC2)

**Authors:** \[Your Name], \[Team or Company if applicable]
**Date:** May 2025

## Introduction

Running Java applications on Amazon Elastic Container Service (ECS) with the EC2 launch type provides flexibility and control over the infrastructure. However, unexpected container restarts can occur due to various issues in the application or environment. This technical guide is a comprehensive resource for backend engineers and DevOps professionals to **diagnose and prevent** these restarts. We will explore the architecture of Java apps on ECS, common causes of restarts (memory leaks, thread exhaustion, SQS misconfiguration, etc.), and best practices to ensure high availability. The guide covers ECS task lifecycle and health checks, integration with CloudWatch for logging and monitoring, pitfalls specific to **Spring Framework** and **OSGi** in containers, thread management, SQS handling (including DLQs), error isolation strategies, container configuration tuning, and real-world case studies with solutions.

Throughout this guide, we include code examples, configuration snippets, diagrams, and tables to illustrate key concepts. Short paragraphs and bullet points are used to enhance readability. By the end, you should be equipped to identify why your Java service might be restarting on ECS and implement robust measures to **prevent unplanned downtime**.

## 1. Architecture of Java Applications on ECS (EC2 Launch Type)

To effectively troubleshoot restarts, it's important to understand how Java applications run on ECS (EC2 launch type) and how ECS manages the container lifecycle. This section provides an overview of the architecture, including ECS cluster setup on EC2, tasks and services, and how a typical Java application (using Spring, OSGi, SQS, etc.) fits into this environment.

### 1.1 Amazon ECS on EC2: Clusters, Tasks, and Services

Amazon ECS (Elastic Container Service) is a container orchestration platform. With the **EC2 launch type**, you deploy containers to a cluster of your own EC2 instances (each running the ECS agent). Key ECS components include:

- **Cluster:** A logical grouping of EC2 instances (container hosts) on which your tasks run. For EC2-backed clusters, you typically manage an Auto Scaling Group of instances that register with the cluster.
- **Task Definition:** A JSON blueprint that defines your container(s) configuration (Docker image, CPU/memory, ports, environment variables, etc.). It can include one or multiple containers (e.g., an application container and a sidecar).
- **Task:** An instantiation of a task definition. It’s the running unit of deployment (analogous to a container pod). Each task gets scheduled on an EC2 instance with sufficient resources.
- **Service:** An ECS Service ensures that a desired number of task copies are running. If a task stops or becomes unhealthy, the service will launch a replacement to maintain the count (ensuring high availability).

**EC2 vs. Fargate:** In EC2 mode, you manage EC2 servers (giving more control and potentially lower cost for steady workloads), whereas Fargate is serverless (AWS manages the compute). EC2 tasks can leverage host features like instance storage and custom agent settings. (Note: ECS on EC2 requires capacity management via Auto Scaling groups, whereas Fargate tasks simply run as long as they’re needed.) This guide focuses on EC2 launch type specifics.

### 1.2 Java Application Stack in an ECS Container

Our Java application uses a stack including the Spring Framework, OSGi modular components, AWS SQS messaging, and multithreading (thread pools, background jobs, subscriber listeners). Within a container:

- **Spring Framework:** Often provides the core runtime (e.g., a Spring Boot application). Spring may manage web endpoints (if any) and background tasks. Spring Boot applications embed a servlet container (Tomcat/Jetty) by default, which could be relevant if the app exposes HTTP health endpoints.
- **OSGi Container:** The application is packaged into OSGi bundles, possibly running on an OSGi framework (like Apache Karaf or Equinox). OSGi provides modularity – the app is composed of bundles that can be loaded/unloaded. In a containerized environment, dynamic loading is usually limited in production (the container image includes all needed bundles upfront), but OSGi still influences class loading and lifecycle.
- **AWS SQS (Simple Queue Service):** The app likely has components consuming messages from SQS queues (e.g., using AWS SDK or Spring Cloud AWS). SQS decouples producers and consumers – our app acts as a consumer, fetching messages and processing them. This asynchronous architecture improves resilience and scaling (front-end producers won’t overwhelm the back-end; messages queue up until processed).
- **Multithreading:** To handle concurrent work, the app employs thread pools or background threads (for SQS message processing, scheduled tasks, etc.). For example, an SQS listener might use a pool of worker threads to process messages in parallel. Efficient thread management is crucial – mismanaging threads can cause memory issues or stalls.

**Typical Deployment Architecture:** The Java application is built into a Docker image. The image is deployed as a container in an ECS task. The ECS service might attach to a load balancer (if the app exposes an HTTP API or health check endpoint), and the app likely communicates with SQS (for incoming jobs) and perhaps other AWS services (DynamoDB, RDS, etc., not directly in scope).

For instance, consider an **event-driven processing service**: user actions generate messages put onto SQS; our ECS task pulls messages, processes each (possibly interacting with a database or another service), and upon completion, deletes the message. This decoupled flow is illustrated in the diagram below, where SQS holds tasks and the ECS service processes them:

&#x20;_Example of an ECS service processing messages from an SQS queue (decoupled, event-driven architecture)._

Each ECS task runs an instance of the Java app which continuously polls the SQS queue (using long polling). The benefit is scalability and isolation – multiple tasks can share the workload, and the front-end and back-end are decoupled for reliability.

### 1.3 ECS Task Lifecycle on EC2

Understanding the ECS task lifecycle helps diagnose why a task might stop or restart. ECS tasks transition through a series of states:

- **PROVISIONING:** ECS is preparing resources before launching the task (e.g., attaching ENI if using awsvpc networking).
- **PENDING:** The task is waiting for an available EC2 instance with enough capacity. The ECS scheduler has placed the task but it’s not running yet.
- **ACTIVATING:** ECS is setting up the container (pulling the Docker image, creating container, connecting network).
- **RUNNING:** The task’s container is up and running; the application process is presumably running inside.
- **DEACTIVATING:** The task is being shut down (for example, ECS received a stop request or the task finished on its own). For tasks in a service, this might mean the task is being replaced or scaled down.
- **STOPPING:** ECS is finalizing shutdown on the container. In EC2, the ECS agent sends a `SIGTERM` to the container’s main process and, after a grace period, a `SIGKILL` if it hasn’t exited. (By default, the grace period is 30 seconds, configurable via the task’s `stopTimeout`).
- **DEPROVISIONING:** ECS is releasing resources post-stop (e.g., detaching network interfaces in awsvpc mode).
- **STOPPED:** The task is fully stopped. ECS will report an exit code and a reason for the stop. If part of a service, ECS will launch a new task to replace it (unless scaling down).

&#x20;_States in the Amazon ECS Task Lifecycle (from provisioning to stopped)._

When a task stops unexpectedly, checking the **“Stopped” reason** is the first diagnostic step. ECS provides a reason message for stopped tasks (visible in the ECS console or via CLI `describe-tasks`) indicating why the task exited – for example, “OutOfMemoryError: Container killed due to memory usage” or "Essential container in task exited". We will explore how to retrieve and interpret these in Section 3.

**ECS Service behavior:** If your Java app is running under an ECS Service with a desired count (say N tasks), the service will automatically attempt to keep N tasks running. That means if one task goes STOPPED due to a failure, ECS will schedule a new one (creating a _restart-like_ behavior). From the application's perspective, it appears as an unexpected restart. Our goal is to minimize these by addressing root causes.

**EC2 Instance considerations:** With EC2 launch type, tasks share underlying EC2 resources. A single EC2 instance might run multiple tasks (depending on CPU/Memory allocated). If the EC2 host encounters resource pressure (CPU steal, memory exhaustion) it can indirectly affect tasks. It’s important to monitor not just container-level metrics but also the EC2 host health. (For instance, if the host is starved and your container cannot get CPU, it might miss health check pings and be killed by ECS as “unhealthy”.) Ensuring the ECS cluster’s EC2 instances have the ECS agent updated and enough capacity is part of the architecture best practices.

**Integration with other AWS Services:** Java apps on ECS often use IAM Roles for Tasks (a taskRole) to access SQS, S3, etc., without embedding AWS credentials. Ensure the task’s IAM role has proper permissions (e.g., to read from the SQS queue, to send CloudWatch metrics, etc.). Misconfigured IAM won’t directly restart a container, but could lead to the app throwing exceptions which might cascade into failure if not handled.

Now that we have an architectural baseline, we can delve into the common causes of unexpected restarts of the Java application, and how to diagnose those issues.

## 2. Common Causes of Unexpected Restarts

Unexpected restarts usually indicate the container (and thus the Java process inside) has stopped due to an error or was terminated by ECS for some reason. We will cover common causes in detail:

- **Memory Issues:** OutOfMemoryError in the JVM or container memory limits being exceeded.
- **Thread Leaks or Exhaustion:** Running out of threads or causing deadlocks, leading to an unresponsive app.
- **SQS Misconfigurations:** Issues like message backlogs, improper long polling, or unhandled exceptions in message processing.
- **Container Health Check Failures:** The app failing ECS health checks (could be due to crashes or temporary hangs).
- **OSGi Bundle Faults:** Problems specific to the OSGi modules (e.g., bundle startup failures causing the app to terminate).

Each cause will be described along with how it triggers restarts and how to confirm if it’s the culprit.

### 2.1 Memory Issues (Java Heap, Off-Heap, and Container Memory Limits)

One of the most frequent causes of container restarts is the application exceeding memory limits. This can manifest in two ways:

- **JVM OutOfMemoryError (OOM) inside the container:** The Java process runs out of heap or other memory and throws an OOM exception. By default, this might not immediately stop the JVM (unless `-XX:+ExitOnOutOfMemoryError` is used), but often an OOM in a critical area will crash the app or leave it non-functional.
- **Container Memory Limit Reached:** If the process uses more memory than the ECS task’s memory allocation, the container runtime or OS will kill the process (typically with a SIGKILL), which ECS reports as a stopped task due to OOM.

**Symptoms:** In CloudWatch Logs or ECS task events, you may see errors like “OutOfMemoryError: Container killed due to memory usage” or exit code 137 signals. For example, an ECS agent log snippet for an OOM event looks like: _“Process within container ... died due to OOM ... Error: Container killed due to memory usage”_. ECS marks the task stopped with reason OutOfMemoryError.

When investigating memory issues, consider both **heap usage and off-heap memory**. Java memory consumption includes: heap, metaspace, thread stacks, direct byte buffers, etc. The sum of these can exceed the Java heap size. As an illustration, _threads_ alone can consume significant memory: each thread has a stack (by default \~1MB, though actual resident usage is typically lower \~100-200KB due to lazy allocation). If an application creates hundreds or thousands of threads (e.g., through unbounded thread pool growth), that can add up to many hundreds of MB of memory outside the heap.

**Common memory-related causes:**

- _Memory Leak:_ The application might be retaining objects (on heap) without releasing, so heap usage grows until an OOM occurs. This could be due to caches that never evict, or listeners that accumulate, etc.
- _Metaspace Leak:_ Especially relevant in OSGi environments – if bundles are restarted frequently or lots of classes are loaded, Metaspace (which holds class metadata) can grow unbounded if not configured. By default metaspace is unlimited (unless `-XX:MaxMetaspaceSize` is set). A leak in metaspace (for instance, continually loading new classes via OSGi without unloading) can eventually trigger an OOM in metaspace.
- _Direct ByteBuffer / Off-Heap usage:_ If using NIO buffers or certain frameworks (Netty, etc.), off-heap memory might be used. The default max direct memory equals the heap size, but it can be changed with `-XX:MaxDirectMemorySize`. Exhausting off-heap memory also throws an OOM error (though often as a Direct buffer OOM).
- _Native Memory:_ Some libraries or the JVM itself allocate native memory. For example, large thread pools (each thread stack is native memory), large code caches for JIT, or usage of `String.intern()` (which can bloat the JVM’s string table off-heap).
- _Container Limit too Low:_ The ECS task’s memory limit might simply be set too low for the workload. If the Java process tries to use more than available, the kernel OOM killer steps in.

**Diagnosing Memory Problems:**

1. **Check ECS Task Stop Reason and Exit Code:** If it’s an OOM kill, ECS will mark the task as stopped with reason containing _OutOfMemoryError_. The exit code is often 137 (128 + 9 for SIGKILL) which is typical for OS-terminated processes due to OOM. Exit code 137 can also happen if the container didn’t shut down within the stop timeout, but ECS will explicitly say if it was due to memory. In contrast, a graceful exit or a System.exit in the app might show a different code (0 or 1, etc.).
2. **Examine CloudWatch Logs (Application logs):** Often the Java logs will contain an `java.lang.OutOfMemoryError` stack trace if the JVM threw one (e.g., “Java heap space” or “Metaspace”). If the container was killed by the OS, you might not see a Java stack trace (because it wasn’t a handled exception), but you might see a lack of logs prior to restart or a sudden stop.
3. **Check Memory Metrics:** If CloudWatch Container Insights or Docker stats are available, see if memory usage was climbing steadily. A pattern of rising memory until \~100% then a drop to zero corresponds to an OOM kill.
4. **Heap Dump or Memory Profiler:** In a non-production or controlled environment, replicate the scenario and obtain a heap dump (`-XX:+HeapDumpOnOutOfMemoryError` can automatically dump on OOM). Analyze the heap dump for leaks (using tools like Eclipse MAT). For off-heap, use **Native Memory Tracking (NMT)** or profilers to see where native memory is going.
5. **Code Review for Unbounded Structures:** Look at code for caches, static collections, or thread creation that could indicate growth.

**Solutions/Prevention for Memory Issues:**

- _Fix Leaks:_ The ultimate fix is to resolve the memory leak in code (e.g., remove references in caches, stop accumulating interned strings, properly close resources that retain memory). Real-world example: a messaging consumer failed to acknowledge messages, causing an internal list to retain all unacked messages until OOM – the fix was to always ACK or drop messages appropriately.
- _Tune JVM and Container Memory:_ Ensure the JVM’s heap settings align with container limits. A common practice is to set `-Xmx` to somewhat below the ECS memory limit (e.g., if container memory is 1GB, set `-Xmx750m` or use `-XX:MaxRAMPercentage` to let JVM auto-size to \~75-80%). This leaves room for non-heap usage. **Do not rely on default heap settings** – modern JVMs will see the cgroup limit and often use a fraction of it for heap by default, but it’s safer to be explicit for predictability.
- _Enable GC Logging:_ GC logs can show if frequent Full GCs happen (which might indicate memory pressure). Though in containers, ensure logs either go to stdout or a file that is shipped out, otherwise they might be lost.
- _Use Alerts:_ Set up CloudWatch alarms on high memory utilization (e.g., >85% for a sustained period) to act before an OOM kill occurs.
- _Leverage OOM Help:_ Consider `-XX:+ExitOnOutOfMemoryError` in Java 8+ to force the JVM to terminate on OOM, which will let ECS catch it immediately (rather than a hung process). Also use `-XX:+HeapDumpOnOutOfMemoryError` and specify a path in a writable volume to get a dump for analysis when it happens.

**Memory Case Study:** An ECS task with 1GB limit was restarting daily. ECS events showed _“OutOfMemoryError: Container killed due to memory usage”_. Analysis revealed a cache in the app was growing indefinitely. The short-term fix was to increase the task memory to 2GB, giving headroom (this reduced immediate restarts) while a code fix was implemented to evict cache entries. In parallel, AWS CodeGuru Profiler was suggested to profile live memory usage. After the fix, memory stabilized well below the limit.

Remember that beyond Java’s own memory, the OS inside the container might need a small amount (tiniest if using minimal base images). But usually the bulk of memory use is the JVM. So manage your Java memory wisely to avoid container OOMs.

### 2.2 Thread Leaks and Exhaustion

Threads are a finite resource, and thread-related issues can lead to restarts indirectly by making the app unresponsive or by consuming excessive memory (as discussed above). Key thread problems include:

- **Thread Leaks:** The application creates threads (e.g., via `new Thread()` or ThreadPool executors) but does not properly shut them down. Over time, the number of live threads grows. Each thread uses stack memory and some CPU scheduling overhead. Eventually, this can lead to **OutOfMemoryError (unable to create new native thread)** if the process hits OS thread limits or memory limits. It could also degrade performance (too many threads context-switching).
- **Thread Pool Exhaustion (Starvation):** If using a bounded thread pool (e.g., a fixed size pool) and all threads become blocked (waiting on I/O, locks, etc.), new tasks cannot be executed and the application may appear hung. For instance, if all consumer threads waiting on a slow database, new messages from SQS queue might queue up internally and health checks might fail because the app isn’t processing requests.
- **Deadlocks:** Two or more threads waiting on each other’s locks can cause a complete stall in part of the application. If the deadlock affects a critical component (like the thread that responds to health check or a main processing loop), ECS might mark the container unhealthy (due to no response) and restart it.

**Symptoms of Thread Issues:**

- The application becomes unresponsive or slow before a restart. You might see timeouts in logs.
- No obvious exception (like no OOM, etc.), making cause less visible in ECS events (ECS might just say “Essential container stopped without report” or health check failed).
- A **“java.lang.OutOfMemoryError: unable to create new native thread”** in logs indicates the process hit the thread limit (which is often due to too many threads).
- If thread starvation occurs, you might see warning messages like **“Thread starvation or clock leap detected”** (this is a message from some executors when they can’t schedule tasks on time).
- CloudWatch metrics: if you push custom metrics, a rising thread count is a red flag. Otherwise, high CPU could be a sign if many threads are active, or conversely CPU near 0 if threads are deadlocked.

**Diagnosing Threads:**

- **Thread Dump:** The most powerful tool is capturing a thread dump (stack trace of all threads) from the JVM when the issue is occurring. On ECS (Linux), you can exec into the container or use `ecs exec` feature, then run `jstack <pid>` or send `kill -3 <pid>` which causes the JVM to print a thread dump to stdout. The thread dump reveals how many threads exist and what they are doing. Look for repeated patterns (e.g., hundreds of threads in a similar stack trace – that could be a leak where each iteration creates a thread).
- **Metrics:** If using Spring Boot Actuator or Micrometer, the JVM metrics include _jvm.threads.live_, _jvm.threads.daemon_, etc. These can be exposed to CloudWatch or Prometheus. A steadily increasing thread count signals a leak.
- **OS Metrics:** On the EC2 host, the process’s thread count can be seen (`top -H` or other tools) if you have access.
- **Code audit:** Identify places threads are created. Common culprits: creating an `ExecutorService` and never shutting it down, using timers or schedulers that spawn threads periodically, or libraries that spawn threads on each request (which would be a bug). OSGi bundles might spawn background threads on activation – ensure they stop on deactivation.

**Thread Management Best Practices:**

- Use bounded thread pools (e.g., fixed size or with queue limits) for executors to avoid unlimited thread creation. For example, when consuming SQS, use a fixed thread pool for processing messages.
- Always shut down executors on application shutdown (Spring Boot can manage this if beans are properly defined, or use Runtime shutdown hooks).
- Monitor thread count. If you see it rising unexpectedly, investigate before it crashes.
- Set `-Xss` (thread stack size) to a smaller value if you need to allow more threads within the same memory footprint (default 1MB can be reduced if each thread only needs small stack, but be cautious and test if going lower than 512k).
- Consider using **virtual threads** (Project Loom, if using Java 19+ in the future) for handling massive concurrency without many OS threads – though that’s cutting edge and beyond scope, it’s a Java evolution to be aware of.

**Real Example – Thread Leak:** Suppose an OSGi bundle starts a new thread for a scheduler each time it’s updated, without stopping the old one. After a few deployments, dozens of threads accumulate. Eventually the JVM hit the OS threads limit, causing an OOM “unable to create new native thread” and the container restarted. Diagnosis via thread dump showed many threads named “SchedulerThread-#”. Solution: modify the bundle to track and stop the old thread on update (or use a ScheduledExecutor that can be reused). After the fix, thread count stabilized and no further restarts occurred.

**Real Example – Thread Starvation:** A Java app using a fixed thread pool of size 10 for message processing got stuck when all 10 threads were waiting on an external API call that hung. The SQS messages piled up (visible in CloudWatch as queue length increasing) and the app didn’t respond to the health check (which tried to poke the app via HTTP) leading ECS to mark it unhealthy. ECS replaced the task. The root cause was external API slowness. Solution: increased the thread pool to handle bursts, but more importantly implemented timeouts on the external calls and used fallback logic so threads wouldn’t block indefinitely. Also integrated a circuit breaker – if external API is down, fail fast and free the thread rather than hang. This prevented recurrence of the starvation-induced restarts.

In summary, **thread leaks** manifest similarly to memory leaks, while **thread starvation/deadlock** manifests as hung containers. Both can trigger ECS to restart the task (either via OOM kill or health failure). Proper thread management and monitoring are key to preventing these issues.

### 2.3 AWS SQS Misconfigurations and Backlog Overload

Amazon SQS is a durable queue service, and our application likely relies on it to receive work. Misconfigurations or improper handling of SQS can indirectly cause our app to crash or restart. Some scenarios include:

- **Unbounded Backlogs:** If message production outpaces consumption, the queue backlog grows. While SQS itself will handle large backlogs (up to the limit of queue storage), our application needs to handle a surge gracefully. If not, a huge backlog might tempt developers to scale up consumers drastically, which if done improperly (spawning too many processing threads or tasks) could lead to resource exhaustion as discussed above. Alternatively, messages might pile up and their processing may hit timeouts.
- **Long Processing Times:** If each message takes a long time to process and the app doesn’t use concurrency, the messages back up. ECS might not restart because of this alone, but it might violate SLAs or lead operators to manually restart thinking it’s stuck. Also, long processing increases the chance a deployment or scale-in terminates the task mid-process (if not handled, see graceful shutdown later).
- **Visibility Timeout Misconfig:** If the visibility timeout on the queue is too short relative to processing time, messages might become visible again while still being processed, leading to duplicate processing and possibly confusing application state or increased load. Conversely, if it’s too long and a task crashes, messages stay hidden longer than necessary.
- **No Dead-Letter Queue (DLQ):** Without a DLQ, a “poison message” (one that consistently causes processing to fail) will be retried endlessly, possibly causing the app to repeatedly throw exceptions or even crash if the exception is severe. This can create a loop of restarts if not addressed.
- **Unhandled Exceptions in Listeners:** If using a high-level framework (like Spring’s `@SqsListener` or a library), an exception during message processing might be caught internally, but if not, could bubble up and potentially crash the thread or the whole consumer loop. Even if caught, if not sent to a DLQ after max attempts, the app might get stuck reprocessing the same failing message. This could monopolize threads or cause repeated errors that might be misinterpreted as the app being faulty (leading to restarts).
- **Improper scaling policy:** If the system auto-scales ECS tasks based on queue length (a common pattern), a misconfigured policy could scale down too aggressively, terminating tasks while they still had work (some messages might get requeued and processed again by new tasks), or not scale up quickly enough (leading to long backlogs that operators might try to “fix” by restarting services). Using the **“backlog per task”** scaling approach is recommended to smoothly adjust tasks based on queue length.

**Diagnosing SQS-related issues:**

- **Check Logs for Messaging Errors:** Look for exceptions when processing messages. For example, deserialization errors, timeouts calling downstream services per message, etc. These might not directly restart the app but can fill logs and indicate why throughput is low or failing.
- **Monitor Queue Metrics:** CloudWatch provides `ApproximateNumberOfMessagesVisible` (backlog size) and `ApproximateNumberOfMessagesNotVisible` (in-flight messages). If backlog continually grows and in-flight is high, it means consumers are not keeping up. Also watch `NumberOfMessagesSent` vs `NumberOfMessagesDeleted` rates – if sent >> deleted, backlog grows.
- **DLQ metrics:** If a DLQ is configured, monitor if messages are appearing there (CloudWatch can alarm on `NumberOfMessagesSent` to DLQ > 0). Messages in DLQ mean they failed processing multiple times.
- **ECS Task count changes:** If using auto-scaling on SQS, check if tasks were scaled in/out rapidly. ECS Service events or CloudWatch Alarms may show if scaling was triggered by queue metrics.

**Best Practices for SQS to Avoid Restarts:**

- **Use Dead-Letter Queues:** Always configure a DLQ for your SQS queue with an appropriate `maxReceiveCount`. This ensures that any message that consistently fails (e.g., bad data causing an exception) will be moved out of the main queue after a few attempts, preventing it from poisoning your consumer repeatedly. DLQs isolate problematic messages for later analysis, so your app can continue with other messages. Also set up an alert when messages appear in the DLQ, so you’re aware of failures.
- **Gracefully Handle Message Failures:** Catch exceptions in message processing logic. For example, if using Spring’s `SimpleMessageListenerContainer` or `@SqsListener`, implement error handlers or use try-catch around your processing. Ensure that a failing message doesn’t crash the entire consumer thread. Instead, log the error, maybe increment a retry counter (if you manage retries in-app), and let the message go back to queue or to DLQ after exceeding attempts. The goal is **fail fast and isolate** – one bad message should not take down the whole app.
- **Tune Visibility Timeout:** Set it slightly above your worst-case processing time. If a task often takes \~30 seconds, maybe set visibility timeout to 60 seconds to allow some headroom. Too high and messages stuck with a dead consumer take longer to retry; too low and you risk duplicate processing.
- **Use Batch Retrieval if Possible:** The AWS SQS SDK allows receiving up to 10 messages at a time. Batching can improve throughput and reduce API calls. Just ensure your processing can handle a batch (e.g., loop through them, possibly in parallel if needed). This helps drain backlog faster without needing too many threads.
- **Auto-Scaling Consumers:** Employ ECS Service Auto Scaling based on queue length per task. For example, target a certain backlog per consumer (AWS suggests a formula known as **backlog per task** where you scale out if `messages_per_task` > threshold). This way, if backlog grows, ECS adds tasks; if backlog shrinks, tasks scale down (after finishing current messages). This dynamic scaling prevents scenarios of massive unhandled backlog or idle over-provisioning. Just be careful to allow tasks to finish processing messages on scale-in (we’ll cover graceful termination).
- **Throttling and Back-pressure:** If an external dependency (DB, third-party API) is slow, consuming messages at an unlimited rate can overwhelm it and cause failures. Implement back-pressure: e.g., limit number of concurrently processed messages when such dependencies are under strain. You can also temporarily pause SQS polling if needed (some frameworks allow a pause of the consumer thread, or you can adjust by scaling down tasks manually).

**Example Scenario:** The service experiences a sudden spike in SQS messages. The backlog jumps to 10,000. If the service is one task with a single-threaded consumer, obviously it’ll lag far behind. If someone decided to quickly scale up by increasing desired tasks to 5, but each container still had default memory for maybe only a few threads, those tasks might each spawn dozens of threads if not configured, possibly causing memory issues. A better approach: configure each task to use a reasonable number of threads (say 10) and scale out tasks gradually via auto-scaling (maybe one task per 1000 messages backlog). This way, you handle load by both vertical and horizontal scaling without hitting a single container’s limits.

**SQS and Restarts:** Generally, SQS issues cause processing failures or slowness, but not directly container crashes. However, they contribute to conditions that _lead_ to restarts: e.g., a poison message causing repeated exceptions might not kill the JVM, but an operator might mistakenly redeploy or ECS might replace a task if it fails health checks due to those exceptions affecting responsiveness. Ensuring robust SQS handling means the app remains healthy and doesn’t require a restart as a “fix.” Use DLQ as a safety net so the app doesn’t get stuck on the same bad message continuously.

### 2.4 Container Health Check Failures and Mishealth

ECS can be configured with container health checks – commands run inside the container to verify the app’s health. Additionally, if the service is fronted by an Elastic Load Balancer (like an ALB), the load balancer’s health check can influence ECS (unhealthy tasks are stopped/replaced). Unexpected restarts can occur if the health checks are too stringent or the application becomes temporarily unresponsive.

**Health Check Mechanism:** In the ECS task definition, you can specify a health check for the container (e.g., an HTTP call to a health endpoint or a shell command). ECS will run this check at intervals. If the container fails the check a certain number of times consecutively, ECS marks it **UNHEALTHY**. For an essential container, if it’s unhealthy, the task health is unhealthy and ECS will stop the task and start a new one. This is meant to self-heal applications.

Common causes of health check failures:

- **Application Hang or Crash:** If the app is not responding on the health endpoint (maybe due to a deadlock or GC pause or it crashed), the health check (say an HTTP GET) will fail.
- **Slow Startup:** If the health check is enabled too soon, the container might not have finished starting the app. ECS health checks have a configurable grace period (startPeriod). If not set, the app could be killed during a slow startup because it wasn’t healthy in the first minute. Always set a `startPeriod` sufficiently long for your app initialization.
- **Network Glitch or Timeouts:** A transient network issue or an overloaded container might cause one or two failed health checks (e.g., a timeout on the HTTP health request). If the `retries` threshold is small, the task could be killed even though the app would have recovered if given a bit more time.
- **Wrong Health Check Command:** If misconfigured, the health check might be checking the wrong endpoint or port. For instance, checking `/:health` on port 8080 but the app runs on 9090 will always fail. This is a configuration bug that causes perpetual restarts.
- **Dependency Health Impact:** If the health check is sophisticated (e.g., it checks database connectivity), a failure in a dependency (DB down) could cause your app to report unhealthy. ECS would then restart the task, which likely doesn’t fix the DB issue and just causes unnecessary churn (and potentially cascading failures as all tasks restart and perhaps overload the DB when they reconnect). You might want health checks to be simpler (check the app’s own liveness, not all dependencies).

**Diagnosing Health Check Triggers:**

- Check ECS Service Events: it will log messages like “service my-service (port 8080) is unhealthy in target-group due to health check failures” or “Task was stopped because container health check failed X consecutive times”.
- If using AWS CLI/SDK, `describe-tasks` will show `healthStatus` of containers (HEALTHY/UNHEALTHY) and stopped reason might indicate health check failure.
- Look at the application logs around the times of suspected health failure – was the app actually doing work or was it hung?
- Check CloudWatch metrics: If an ALB is in play, the ALB TargetGroup healthy host count metric dropping to 0 indicates health check issues. ALB also provides a log (if access logs enabled) of health check pings.
- Validate configuration: Ensure the health check command in task definition is correct (e.g., `CMD-SHELL curl -f http://localhost:8080/actuator/health || exit 1` would be a typical HTTP check for a Spring Boot actuator health endpoint).

**Preventing Unnecessary Restarts from Health Checks:**

- **Set Reasonable Thresholds:** If your app occasionally has longer GC pauses or spikes, set the health check interval and timeout to accommodate that. For example, interval 30s, timeout 5s, retries 3 (so \~1.5 minutes of failures to trigger replace). This avoids flapping on minor hiccups.
- **Use `startPeriod`:** During app startup, skip health checks. E.g., `startPeriod: 60` seconds if your app needs a minute to boot. ECS won’t count failures in that initial window.
- **Graceful Degradation vs. Hard Fail:** Decide what your health check should indicate. A distinction: _Liveness_ check (is app running) vs _Readiness_ check (is app ready to serve traffic). On ECS, there is one health check per container. If you have an ALB, you might tie it to readiness (so it only sends traffic when ready), whereas ECS health could just be liveness. You might implement a health endpoint that returns success if app is up (even if dependencies are down, maybe include status info but return HTTP 200 to indicate “don’t kill me, I’m alive”). This way, if DB is down, the container stays running (perhaps retrying DB connection) instead of restarting and still failing. This is nuanced: sometimes you _do_ want to restart on dependency failure, but often the better approach is to let the app handle it (perhaps with its own retry/backoff).
- **Avoid Overlapping Deploy restarts and Health timeout:** If you deploy a new version (rolling update), ECS will start new tasks and stop old. If health check is too strict, new tasks might not pass in time and ECS might roll back or cause a bounce. Ensure your health check settings align with deployment strategy (but that’s more deployment stability than runtime restart – still worth noting).

**Example:** An ECS service had a health check hitting `/health`. The app was healthy, but one day an AWS SDK call in the health endpoint (to verify an S3 connection) started hanging due to S3 issue. The health endpoint timed out, ECS killed the task as unhealthy. All tasks went down one by one (each hung on health check due to S3) – causing downtime. The solution was to simplify the health endpoint to not call external services (just return OK if the app’s main thread is running). External dependencies were moved to a separate **readiness** indicator that wasn’t tied to ECS’s kill decision. This prevented ECS from killing tasks for a transient S3 outage, and instead allowed the app to log warnings and wait for S3 to recover.

In summary, misconfigured or aggressive health checks can cause the cure to be worse than the disease – tasks restart when they might have been fine if left alone. Tuning these ensures ECS restarts tasks only when truly necessary (app is completely hung or crashed).

### 2.5 OSGi Bundle Faults and Modular System Issues

OSGi brings modularity and dynamic loading to Java. In an OSGi-based application, the overall JVM might stay running while individual bundles (modules) can start, stop, or restart. However, certain OSGi-related issues can lead to the entire JVM crashing or becoming unstable, leading to container restarts:

- **Bundle Start Failure:** If a critical bundle fails to start (for example, it throws an exception in its `Activator` or during Spring context initialization), the OSGi container might not have a complete application to run. Some OSGi containers (like Apache Karaf) might handle this gracefully (leaving the bundle in “Failed” state), but if the application logic can’t proceed, it might be as good as a crash. In some setups, a severe failure in a bundle could call `System.exit` (not typical, but possible if not handled).
- **Class Loader Leaks:** Each bundle has its own class loader. If bundles are dynamically updated or reloaded at runtime (perhaps not common in immutable container deployments, but possible in an update scenario), old class loaders might not get GC’d if references persist, leading to metaspace memory leaks. Over time this can OOM the JVM (metaspace OutOfMemoryError), causing a restart.
- **Native Libraries in Bundles:** If a bundle loads a native library (via JNI), and if that library is loaded multiple times or not unloaded properly on bundle stop, it can cause issues or crashes.
- **Fragmentation of Logging/Monitoring:** OSGi uses a Service Registry; if the monitoring or logging service (or any critical service) is provided by a bundle that fails, you might lose insight or the app might decide it cannot continue.
- **Concurrency Issues in Modular Interactions:** Perhaps one bundle spawns a thread and doesn’t stop it when the bundle stops, similar to thread leaks. If an admin triggers a dynamic update (perhaps via JMX or OSGi console) of a bundle, and the old threads keep running and new ones start, you can get weird states or double-processing that might lead someone to restart the whole container to clean up.

In a containerized world, teams often choose not to do dynamic updates in production containers (preferring to build a new image for changes). So the OSGi system might be mostly static between deployments. In that case, OSGi issues would mostly surface at startup (bundle wiring issues, etc.) or not at all. But it’s worth considering:

**Diagnosing OSGi-related problems:**

- **OSGi Logs (Karaf logs, etc.):** Check for bundle exception traces. For example, “Bundle X failed to start” with an exception. This might appear in stdout or a log file depending on how logging is configured.
- **OSGi Console (if accessible):** In dev environments, using the OSGi console (`felix:lb` or Karaf console commands) can show if all bundles are Active or if some are stuck in “Resolved” or “Failed” state.
- If the application just exits during startup, maybe a bundle’s Activator called a System.exit erroneously on error. That would directly terminate the JVM. The ECS task would stop with exit code 1 or some non-137 code, possibly. The logs would cut off around that bundle’s start.
- **Heap/Metaspace analysis:** If suspecting classloader leaks, use a heap dump and look at ClassLoader instances retaining classes.

**OSGi Pitfalls in Containers & Solutions:**

- **Avoid Dynamic Changes in Production:** As mentioned, treat the whole OSGi application as immutable while running in a container. That means no installing new bundles at runtime (except perhaps via a controlled rollout). This avoids a whole class of issues with half-applied changes. As one article noted, containerizing OSGi means you lose some dynamic pluggability but gain consistency.
- **Ensure Clean Bundle Shutdown:** If you do stop bundles (during a shutdown of the container, all bundles get stopped by the framework), make sure each bundle’s stop routine cleans up threads, closes files, etc. This is more of a development guideline but crucial to avoid leaks on repeated runs (not usually an issue if container is destroyed on stop, but relevant if you reuse OSGi container for multiple deployments which is rare here).
- **Watch Out for Fragment and Package Wiring Issues:** Sometimes a bundle may appear started but some required dependency (OSGi service or package import) is unsatisfied, causing hidden errors. This can lead to functionality not working, which might cascade into errors that could crash something. It’s more of a functional bug than a direct restart cause, but could indirectly cause a critical thread to die.
- **Monitoring inside OSGi:** Use the OSGi JMX or a monitoring bundle to keep tabs on memory and threads within the OSGi framework. E.g., Apache Karaf provides MBeans for bundle states. If a specific bundle is repeatedly causing issues, you can pinpoint it via monitoring.

**Real-World OSGi Issue:** An OSGi-based microservice had an embedded database driver as a bundle. The driver bundle tried to create a temporary file but lacked permissions in the container’s read-only filesystem, causing a runtime exception that was not caught. This bubbled up and caused the Spring context (also OSGi-managed) to fail, effectively terminating the app initialization. The container exited soon after launch. ECS kept trying to restart the task, and it kept failing. The solution was to adjust the container filesystem or configure the driver to not use a temp file, and ensure such exceptions are handled gracefully during startup.

Another example: Using an old version of Log4j inside OSGi, where each bundle classloader loaded the logging classes, caused memory bloat. The fix was to use OSGi’s _boot delegation_ or a shared logging service so that only one copy of the logger classes loaded.

In summary, OSGi issues can be tricky because they may not always obviously point to why the _whole container_ is affected. Focus on startup logs and ensure all bundles report started. The advantage of OSGi (modularity) in containers is somewhat reduced (since you deploy all at once), but the complexity remains. Therefore, rigorous testing of the OSGi assembly before deploying to ECS is essential to avoid runtime surprises that could cause restarts.

---

These common causes often intermix (for instance, an SQS backlog might cause thread and memory issues, or an OSGi bundle leak causes memory issues). The next section will discuss how to use ECS and AWS tools to diagnose these problems when they happen in the cloud environment.

## 3. Diagnostics with ECS: Health Checks, Logs, and CloudWatch

Having identified potential causes, effective **diagnosis** is key to pinpointing the exact reason for a restart. AWS ECS provides multiple tools and integration points for monitoring and debugging:

- ECS Health Checks and Events
- CloudWatch Logs (for application logs) and ECS Agent logs
- CloudWatch Metrics and Container Insights
- Retrieving diagnostic information (like task stopped reason, exit codes)
- ECS Exec and other debugging methods

This section focuses on how to leverage these for troubleshooting.

### 3.1 ECS Task Health Status and Events

When a task stops or is killed, ECS generates an event. In the ECS **service events** (visible in ECS Console under the service, or via CloudWatch Events/EventBridge), you might see messages like:

- “Task <ID> stopped due to: **OutOfMemoryError: Container killed due to memory usage**” – indicating an OOM killed it.
- “Task <ID> is unhealthy, stopping.” – indicating the ECS health check failed.
- “Essential container in task exited (exit code X).” – if the main container’s process exited on its own (code X helps hint at cause).

To get these details:

- **ECS Console:** Go to the cluster, then the service, then “Events” tab. Also, under “Tasks”, for stopped tasks, you can click and see a “Stopped Reason”.
- **AWS CLI:** `aws ecs describe-tasks --cluster yourCluster --tasks yourTaskId` will show `lastStatus`, `stopCode` (e.g., EssentialContainerExited, TaskFailedToStart, etc.), and `stoppedReason`. For example, `stoppedReason: OutOfMemoryError: Container killed due to memory usage` or `stoppedReason: Essential container exited with code 1`.

There is also a set of documented common stopped task error messages in AWS docs – these can guide you (e.g., they note that exit code 137 typically means not stopped gracefully within 30s or OOM kill).

**Container Exit Codes:**

- `0`: Clean exit (normally you wouldn't expect your service to exit on its own if it's long-running).
- `137`: As discussed, means SIGKILL (128+9) – often OOM or forced kill.
- `143`: SIGTERM (128+15) – likely the task was told to stop (scaling down or deployment) and it exited gracefully in response. If you see 143 unexpectedly, it might mean ECS or someone issued a stop (maybe as part of scale in or an update).
- Non-zero like `1` or any other: The Java process itself exited with an error code. By default, uncaught exceptions won't cause a specific code, but some frameworks or launch scripts might call System.exit(1) on failure. Examine logs for any fatal error.

**ECS Health vs. ALB Health:** If you use a load balancer, ECS will also stop tasks that the ALB reports as unhealthy (unless you disabled that in service settings). ALB health check failure will reflect in ECS events (“target group health check failed”). So ensure to check both ECS and ALB if applicable.

Knowing why a task stopped guides your next steps – e.g., OOM vs health check are very different causes.

### 3.2 CloudWatch Logs for Application and Container Logs

**CloudWatch Logs** is typically used to collect container logs from ECS. If your task definition’s log configuration uses `awslogs` driver, your Java app’s stdout/stderr (or any configured log file output via sidecar/agent) will end up in a CloudWatch Log Group. Make sure you have this set up, as it’s invaluable:

- In task definition, e.g.:

  ```json
  "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
          "awslogs-group": "/ecs/my-service",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
      }
  }
  ```

  This will stream logs. You can then go to CloudWatch Logs console, find the group, and filter by the task or container ID.

Using CloudWatch Logs:

- Search for exceptions or keywords (“Exception”, “ERROR”, “OutOfMemoryError”, etc.).
- If the app crashed, look at the last log entries before the container restart time.
- Ensure log timestamps align with the event – sometimes logs might stop abruptly.

**ECS Agent Logs (on EC2):** On the EC2 host, the ECS agent also logs to `/var/log/ecs/ecs-agent.log`. This can have low-level info like in the earlier StackOverflow example showing “DockerGoClient: Process ... died due to OOM”. Accessing these requires either SSH into the instance or using SSM if configured. In many cases, the CloudWatch stopped reason is enough, but agent logs can confirm (especially if you suspect an ECS issue or a Docker daemon issue).

**Enabling Container Insights:** CloudWatch Container Insights for ECS can also capture logs and metrics. It can collect stdout logs and metrics like CPU, mem, networking for tasks. If enabled, you get better overview in CloudWatch console (ECS/EKS Monitoring dashboard). It might also collect the number of container restarts if using the new restart policy feature.

**Structured Logging and Tracing:** If your app uses structured logging (JSON) or tracing (AWS X-Ray, etc.), these can provide additional clues. For example, X-Ray might show if calls were timing out often before a crash. This is advanced and requires instrumentation in the app, but mentioning that distributed tracing can help if multiple services are involved in the failure chain.

**Summary of Logs Use:** Logs are your primary evidence of what happened _inside_ the app leading up to a restart. Always cross-reference timeline: If a task stopped at 12:00:30, what do logs show around 12:00:25? Was there a stack trace? Or did logs just cease (pointing to a hard kill)? That differentiation tells you if it was graceful vs kill.

### 3.3 CloudWatch Metrics and Alarms (CPU, Memory, etc.)

While logs tell you what happened, **metrics** can often tell you _when_ and _how_ it happened across time:

- **ECS Service Metrics:** ECS automatically provides some metrics like CPU and Memory utilization for tasks. For EC2 launch type, these come from the ECS agent which fetches Docker stats. If you go to CloudWatch Metrics, under ECS/ContainerInstances or ECS/Services you might find these. CPU is in percentage of task’s allocated CPU, Memory in bytes of the task usage vs allocated.
- **EC2 Metrics:** The EC2 instances have their own metrics (CPU, network, maybe memory if CW agent is installed). If all tasks on an instance slow down, check if the instance CPU was at 100% or if it was swapping (if memory on host exhausted).
- **Custom Application Metrics:** If you’ve instrumented the app (e.g., using Micrometer to CloudWatch, or Prometheus, etc.), you could have things like request rates, error counts, garbage collection pause times, etc. These can be critical: e.g., a spike in GC pause time might correlate with a health check timeout and restart.

**Prometheus/Grafana in ECS:** If you use Prometheus, you might run a Prom server either on the cluster or external scraping an endpoint on the app (if app exposes metrics at /metrics). In ECS, service discovery for Prom can be done via AWS Service Discovery or using ECS Task metadata endpoints. AWS also offers Managed Prometheus. Grafana can visualize all these metrics for easier correlation.

**CloudWatch Alarms:** It is highly recommended to set up alarms that notify you (or even take action) on:

- High memory utilization of a task (e.g., >90% for 5 minutes) – could warn before OOM happens.
- High CPU for prolonged time (could indicate a CPU leak or stuck loop).
- Task count changes – e.g., if desired count is 4 but running count keeps fluctuating or going below, something’s wrong (tasks keep dying). You can create an alarm on ECS service metric “RunningTaskCount” if it drops unexpectedly.
- DLQ messages – an alarm on DLQ having >0 messages as mentioned. This catches failing SQS processing.
- No logs output – a trickier one, but if your app normally logs regularly, silence could mean a hang. You could use a Logs Insights query alarm or external tooling to detect if no log entry in last X minutes.

**Using Container Insights dashboards:** If enabled, you get a nice dashboard per cluster showing CPU/mem of each service, etc. It also can show the number of task restarts (if using ECS restart policy, CloudWatch collects `ContainerRestarts` metric). Even without that, it shows task creation/destruction.

**Example Metric Diagnosis:** Suppose you see a task restarted at time T. Checking CloudWatch metrics, you find memory usage of that task climbed steadily to the limit right before T, and CPU spiked possibly as GC thrashed, then dropped to zero at T as the task died. This clearly points to memory exhaustion. Another scenario: memory was fine, but CPU flatlined at 0% for a minute before restart – perhaps the app was stuck (not doing work), which could align with a deadlock. Or CPU went 100% (maybe a runaway thread) and health failed. Each pattern hints at different root causes.

### 3.4 ECS Exec and On-the-Fly Diagnostics

AWS ECS Exec is a feature that allows you to open a shell (or run a command) inside a running container over AWS’s secure channel (no direct network needed to container). This is extremely useful if you catch a container in the problematic state but before it’s killed.

**Use cases:**

- Run `jstack` to capture thread dump.
- Run `jmap` to inspect memory usage (though dumping a heap in a running prod container is heavy).
- Look at the filesystem, check if some unexpected files or logs (maybe heapdump got written).
- Interactively poke the application (maybe use curl inside the container to hit internal endpoints).

To use ECS Exec, you need to enable it on the task (set `"enableExecuteCommand": true` in the task definition or service). Then use AWS CLI: `aws ecs execute-command --cluster myCluster --task myTaskId --container myContainer --interactive --command "/bin/sh"`. This will drop you into a shell if everything is set up (role permissions, SSM agent, etc., are needed).

**Safety:** Do this in non-prod or prod with caution, as poking around a live system can have side effects. However, for stuck containers it might be the only way to see what’s going on internally if logs are insufficient.

### 3.5 Putting It Together: A Diagnostics Workflow

When facing an unexpected restart issue in ECS:

1. **Observe Frequency and Pattern:** Is it happening to all tasks or just one? Does it happen under load, or at a certain time each day (could hint at a cron job or a memory cycle)?
2. **Check ECS Events & Reasons:** Gather the stopped reason from ECS for at least a few instances. This narrows down cause (e.g., if always OOM vs always unhealthy).
3. **Examine Application Logs (before death):** Look at each failure instance’s logs. Note any common error or last log line.
4. **Correlate with Metrics:** Check CloudWatch metrics around the failure times for anomalies (memory, CPU, SQS queue, etc.).
5. **Deep Dive (if needed):** If cause still unclear, reproduce in a test environment with debug tools (enable more logging, use profilers). Or deploy the app with ECS Exec enabled and wait to catch it in the act to gather dumps.
6. **Identify Root Cause:** Based on evidence, determine if it’s memory, thread, external system, etc. Then apply specific fixes (which following sections and previous cause sections address).

ECS, CloudWatch, and associated tools give a robust toolbox for diagnosing. It’s critical to have these observability pieces in place **before** problems occur. Set up logging and monitoring as part of deployment, so that when a restart happens you aren’t blind.

Next, we will discuss pitfalls and considerations specific to our tech stack (Spring and OSGi) in the ECS context, and then move on to strategies to make the application more resilient (so that even if issues occur, they don’t always require a full restart).

## 4. Spring and OSGi Pitfalls in Container Environments

Our application uses Spring (likely Spring Boot or Spring Framework) and OSGi. These technologies bring their own lifecycle and configuration behaviors which, if not aligned with container operation, can lead to problems. Here we discuss some common pitfalls and how to mitigate them:

### 4.1 Spring Framework (Boot) Considerations

**Graceful Shutdown:** Spring Boot (since 2.3) has graceful shutdown support. When the JVM gets a SIGTERM (which ECS sends on task stop), Spring Boot will by default try to shut down gracefully: it stops accepting new requests and waits for in-flight requests to finish (configurable via `spring.lifecycle.timeout-per-shutdown-phase`). Ensure this is enabled (`server.shutdown=graceful` in application.properties for web apps). For non-web background tasks, you may need to handle shutdown hooks yourself (e.g., listen for context closed event to stop processing new messages from SQS).

**Shutdown of Thread Pools:** If you use Spring’s `@Async` or scheduling, or define Executor beans, mark them with `@PreDestroy` or configure as beans that Spring will close on context shutdown. Spring will call `shutdown()` on `ThreadPoolTaskExecutor` beans if they are lifecycle beans. But if you create threads outside of Spring’s knowledge, Spring won’t manage them.

**Configuration via Environment:** In container environments, using environment variables for config is common (12-factor app principles). Spring Boot easily maps env vars (e.g., `MY_APP_FOO` to `my.app.foo` property). Ensure your ECS task definition passes needed configs as env vars or uses AWS Systems Manager Parameter Store/Secrets Manager (Spring Cloud AWS can load those). A pitfall is forgetting to externalize something – e.g., memory settings. If your Docker image has a fixed `-Xmx`, you might want to make that adjustable per deployment. Consider using the `JAVA_OPTS` environment variable pattern and reference it in the startup script.

**Spring Cloud AWS SQS:** If using Spring’s SQS listener (`@SqsListener`), note that it manages polling threads internally. By default it might spawn a thread per queue listener. You can configure concurrency (`SpringCloudAWSMessagingAutoConfiguration` properties like `sqs.executor.core-size`). If not configured, it could either under-utilize or over-utilize threads. Make sure it aligns with what the container resources can handle.

**Actuator and Health:** Spring Boot Actuator provides health checks and metrics. If you have actuator’s health endpoint exposed and perhaps used for ECS health check, ensure the health indicator doesn’t cause the issues as mentioned earlier. You can also customize the health endpoint to exclude certain checks via properties (e.g., `management.health.db.enabled=false` if you want to not fail health when DB is down).

**Fat JAR vs Thin JAR:** Most likely a fat JAR is used in the Docker image. If using OSGi, perhaps not (OSGi likely uses bundle jars). But if it were just Spring Boot, one caution: building a fat JAR and running with `java -jar` can have an effect on startup time and memory (because it loads everything at once). But this is usually fine.

**Memory Settings and Spring:** Spring itself doesn’t have special memory needs aside from what your app does. But using Spring + Hibernate + other libraries can add to metaspace usage (lots of classes). So ensure if you see metaspace OOM, you might increase MaxMetaspaceSize or upgrade Spring (as newer versions tend to have better defaults or fewer permgen issues since permgen is gone in Java8+).

**Developer vs Prod profile:** Sometimes, a mis-configured Spring profile can cause trouble in containers (like using an H2 database in memory accidentally in prod profile, which could bloat memory). Double-check that the correct profiles are active in ECS (via `SPRING_PROFILES_ACTIVE`). Remove any dev/test specific beans that shouldn’t run in prod.

### 4.2 OSGi Pitfalls and Best Practices

**Logging in OSGi:** Ensure the logging framework works in OSGi. If using something like Pax Logging (common in Karaf) or Log4j as an OSGi bundle, configuration issues can result in no logs or excessive logs. For instance, duplicate log configuration in multiple bundles might cause large log output or conflicts.

**Class Loader Issues:** OSGi can have subtle class loader issues where one bundle doesn’t see classes of another. This can cause `ClassNotFoundException` or `NoClassDefFoundError` which might crash a bundle during start. Those errors should appear in logs. To avoid this, carefully manage Import-Package/Export-Package in bundle manifests. If a crucial class isn’t visible, either adjust the bundle manifest or use something like Karaf features to ensure proper wiring. This is more build-time concern, but runtime symptom is a bundle failing to start (which, as discussed, can cripple the app).

**Bundle Dependencies on Config/Admin:** Some OSGi apps use Configuration Admin or similar to load configs. If these configs aren’t provided, bundles might not start. Make sure any required config is packaged or provided via environment. For instance, a bundle might expect a system property for some directory path. In container, such paths may not exist or be writable. Solution: configure the bundle to use a path that exists (like `/tmp` which is often writable in containers) or mount a volume if needed.

**Handling OSGi Lifecycle:** In an ECS context, you likely start the OSGi container (which then starts all bundles) and you never purposely stop bundles until the container is killed. So, you might not need dynamic lifecycle management. But still:

- If a bundle does crash or get accidentally stopped, you might consider having an OSGi watchdog that attempts to restart it (some OSGi frameworks have options to auto-restart failed bundles).
- If you allow remote OSGi management (e.g., JMX or SSH into Karaf console), be careful. While useful for debugging, making changes could void the immutability of your container and make it hard to reconcile state. Usually, treat the container as read-only at runtime, and fix issues via new deployment rather than hot patching OSGi in production.

**Combining Spring and OSGi:** There was “Spring Dynamic Modules” (Spring DM) in the past for using Spring in OSGi. If your app uses that, ensure the Spring application context inside each bundle is properly configured. One classic issue: component scanning in an OSGi bundle might not see components in other bundles. Or you might inadvertently start multiple Spring contexts. Ensure that if multiple bundles use Spring, they either each handle their part or you have one master Spring context.

### 4.3 Combined Spring-OSGi Scenarios

One important scenario is the **shutdown sequence** in an OSGi + Spring app. When ECS sends SIGTERM, ideally: Spring’s context closes (stopping its beans/tasks) and the OSGi framework shuts down bundles. Make sure these two are coordinated. For example, if Spring is embedded in OSGi, the OSGi container might need to be told to stop. If using Apache Karaf, it will handle SIGTERM by shutting down the container (stopping bundles). Verify in testing that a SIGTERM (simulated by `docker stop` which gives the default 30s) actually brings down the app cleanly. If not, you may need a custom shutdown hook.

**In summary for Spring/OSGi:** Leverage Spring Boot’s features for graceful shutdown and health checks, use OSGi mostly as a modular class-loading system but avoid runtime bundle changes in production, and be mindful of how OSGi components behave in a container (especially in terms of logging, threads, and config). With these practices, Spring and OSGi can coexist without causing unexpected restarts beyond the issues discussed earlier.

## 5. Thread Lifecycle and Monitoring Techniques in Java/ECS

Threads have a lifecycle: they are born, do work, and either terminate or wait (blocked) for more work. In a Java app on ECS, thread lifecycle management is crucial:

- **Creation:** Threads are created by the JVM (for internal tasks like GC), by frameworks (e.g., Tomcat thread pools), or by application code (executors, etc.). Each thread consumes resources (CPU, memory for stack).
- **Running/Blocked:** Threads may be running (using CPU) or blocked (waiting for I/O, sleep, lock). A blocked thread still occupies memory and a slot in the thread scheduler.
- **Termination:** When a thread’s `run()` method exits normally or by uncaught exception, the thread terminates. If it’s a pooled thread, the pool might recreate it or reuse threads.

In Java, non-daemon threads prevent the JVM from shutting down. Spring Boot and most frameworks use non-daemon threads for their main work, which is why the JVM stays alive until you explicitly stop it. Daemon threads are killed when the JVM exits. Knowing this, if your app were to accidentally mark threads as daemon or non-daemon incorrectly, it could either prevent proper shutdown or cause the JVM to exit prematurely. Typically not an issue unless custom thread management is involved.

**Monitoring thread lifecycle in ECS:**

- As discussed, using **thread dumps** is the primary method to inspect thread states. It’s useful to automate thread dump capturing on certain conditions. For instance, you can set up a signal handler: in Linux, `kill -3` sends a SIGQUIT which by default the JVM converts into a thread dump to stdout. So, you could use ECS Exec or even an automated script to send SIGQUIT to the JVM process (pid 1 in container) to get a dump in CloudWatch Logs.
- **JMX Monitoring:** Java Management Extensions expose `ThreadMXBean` which can give you the current thread count, peak thread count, and even thread CPU times and contention stats. You can use tools like JConsole, VisualVM, or Mission Control to attach (though in ECS on EC2, you’d need to open JMX ports which is not trivial, or use SSH tunnel through the host). Instead, a simpler way is to use a JMX -> CloudWatch exporter or Prometheus JMX Exporter. For example, the **Prometheus JMX Exporter** can run as a Java agent in your app and expose metrics, including `jvm_threads_live`, etc., which you can scrape and visualize.
- **OS Level Monitoring:** On the EC2 host, if you have access, `ps -L -p <pid>` will list all lightweight processes (threads) of the Java process, and `/proc/<pid>/task` will contain subdirectories for each thread. This is more low-level but can confirm how many threads exist from the OS perspective.
- **Set Resource Limits:** Besides CPU/memory, you can set ulimit for max user processes (which includes threads) via ECS task definition (using `ulimits` parameter). For example, setting a limit of say 1000 threads can ensure a runaway thread creation doesn’t exceed that. If hit, the app will throw unable to create thread error rather than bringing down the whole node. It’s a safety net but ideally, your app never hits it.
- **Thread Naming:** A practical tip – give your threads meaningful names (many frameworks do this). This makes thread dumps readable (e.g., "SqsListener-worker-3" vs "Thread-63"). When you create executors, you can supply a ThreadFactory that names threads. This way, when monitoring, you immediately know which component a thread belongs to. It simplifies debugging thread leaks (you see hundreds of "DownloaderThread" and know which pool is misconfigured).

**Life after a restart:** When a container restarts, all threads are of course gone and will be recreated fresh in the new JVM. That can clear out a problem temporarily (e.g., if you had 1000 leaked threads and it restarts to 50 normal threads). But without fixing the root cause, the leak will build up again. Thus monitoring thread metrics over time can indicate a slow leak well before it reaches failure.

In summary, treat threads as a vital resource. Monitor their count and states, use dumps to inspect issues like deadlock, and impose limits if necessary. Properly tune thread pools for expected concurrency and ensure they terminate on shutdown. This avoids scenarios where threads lead to container instability.

## 6. SQS Backlogs, Dead Letter Queues (DLQs), and Subscriber Error Handling

We’ve touched on SQS best practices earlier; here we’ll provide concrete techniques and examples for managing message processing to avoid restarts:

### 6.1 Handling Backlogs Gracefully

When an SQS backlog grows, you have a few options:

- **Scale Out:** As discussed, add more consumer instances (ECS tasks). Use CloudWatch alarms on queue length to trigger ECS Service auto-scaling. For example, target 100 messages per task. If 1000 messages, scale to 10 tasks. This keeps per-container load reasonable.
- **Throttle Intake:** If scaling out is not instant or there’s a sudden spike, ensure your application doesn’t try to grab too many messages at once. Use the max messages per poll (10) judiciously. If processing is heavy, maybe poll 5 at a time to avoid one container loading 10 huge tasks into memory at once.
- **Time-Based Batching:** If backlog can be processed a bit slower without harm, implement a small delay or sleep in the consumer loop when messages are continuous. This avoids maxing CPU if not necessary. But if real-time processing is needed, better to scale out.

A simple pseudo-code for an SQS polling loop without Spring:

```java
AmazonSQS sqs = AmazonSQSClientBuilder.defaultClient();
String queueUrl = sqs.getQueueUrl("MyQueue").getQueueUrl();
int batchSize = 5;
while (running) {
    ReceiveMessageRequest req = new ReceiveMessageRequest(queueUrl)
                                    .withMaxNumberOfMessages(batchSize)
                                    .withWaitTimeSeconds(20);
    List<Message> msgs = sqs.receiveMessage(req).getMessages();
    for (Message m : msgs) {
        try {
            processMessage(m.getBody());
            sqs.deleteMessage(queueUrl, m.getReceiptHandle());
        } catch (Exception e) {
            log.error("Processing failed for message " + m.getMessageId(), e);
            // Optionally send to a custom DLQ or mark for retry
            // (Usually, if not deleted, it will go back to queue and eventually to DLQ after maxReceiveCount)
        }
    }
}
```

In this snippet, the `processMessage` is wrapped in try-catch. On exception, we log the error. We did not delete the message in that case, so it will become visible again after the visibility timeout. If this message keeps failing, after `maxReceiveCount` (set in queue redrive policy) it will move to DLQ automatically.

**Key point:** Ensure that any exception does **not escape** the loop to the outer while, otherwise it might terminate the polling thread. In frameworks like Spring, this is handled for you, but always double-check: for example, Spring Cloud AWS will catch exceptions and not kill the listener, but you should configure the error handler to send the message to DLQ or at least log properly.

### 6.2 Dead-Letter Queue (DLQ) Management

An SQS DLQ is simply another SQS queue that stores messages that fail processing too many times. To set it up:

- Create an SQS queue (e.g., “MyQueue-dlq”).
- In the main queue’s Redrive Policy, set the DLQ ARN and `maxReceiveCount` (e.g., 5). This can be done via AWS Console or CloudFormation/Terraform.
- Now, if a message is received 5 times without being deleted, SQS will move it to the DLQ.

Once messages are in DLQ, what next?

- Set up a CloudWatch alarm on the DLQ’s `ApproximateNumberOfMessagesVisible` > 0 to alert your team. This means something is consistently failing.
- You can build a tool or script to review DLQ messages. For example, periodically (maybe a small Lambda) that reads DLQ and logs the messages (or sends to developers).
- Determine root cause of those messages: it could be bad data. You might need to fix code to handle that data, or clean the data.
- After fixing, you might retry those DLQ messages by moving them back to main queue (SQS console has a “Redrive” option, or use the `StartMessageMoveTask` API). Or, if the messages are not needed, you can discard them.

DLQs help avoid the scenario where one bad message causes infinite processing loop and potential memory buildup or log spam, which could destabilize the container.

### 6.3 Subscriber Error Handling

Whether you poll SQS manually or use a listener container, robust error handling in message processing is vital:

- **Use Try-Catch:** As shown, wrap processing in try-catch. Handle specific exceptions if some are expected (e.g., JSON parsing error vs business validation error).
- **Log Wisely:** Log the exception with context (message ID, perhaps a snippet of payload if not sensitive). But avoid logging the entire message repeatedly if it’s large or if many fail – that could flood logs and ironically cause disk or memory pressure.
- **Avoid System.exit:** It should go without saying, but never call `System.exit` on a processing error. We want the app to recover or at least isolate the error to that message, not terminate the JVM.
- **Retries in App:** Sometimes you may want to retry immediately a few times before giving up (like a transient DB issue). Use exponential backoff if you do (e.g., wait 1s, then 2s, etc.). However, be careful not to hold the message too long beyond visibility timeout, or else two consumers might end up processing it. If you need long retries, better to release the message and let it reappear and be picked up again (which naturally spaces out attempts by visibility timeout).
- **Idempotency and Deduplication:** Ensure your processing is idempotent or can handle duplicates, because if a container crashes mid-message, that message will be retried by another container later. If your processing causes side effects (like writing to DB), design it such that reprocessing the same message doesn’t break things (e.g., use message IDs to detect duplicates, or make the operation safe to repeat).
- **Poison Pill handling:** If a particular message content always crashes a certain library (maybe a known bug), you might do a content filter: detect that pattern, and skip or send to DLQ immediately without retrying 5 times. This is an advanced scenario, but it can save resources.
- **Parallelism**: If using manual threads to process messages in parallel, ensure thread exceptions are handled. In Java, if a Runnable throws, the thread just terminates; the rest of the pool continues but that particular task is lost. Implement an `UncaughtExceptionHandler` on threads to log such cases. Or use an ExecutorService that returns Future and catch exceptions from `future.get()`.

**Example with Spring @SqsListener (pseudo):**

```java
@Component
public class OrderListener {

    @SqsListener(value = "OrdersQueue")
    public void handleOrder(String orderJson, @Header("SenderId") String sender) {
       try {
           Order order = objectMapper.readValue(orderJson, Order.class);
           orderService.process(order);
       } catch(Exception e) {
           log.error("Failed to process order from " + sender, e);
           // Spring will not delete the message if exception is thrown
           // It will go back to queue and possibly DLQ after retries
           throw e;
       }
    }
}
```

In this example, by throwing the exception, the message is not deleted. Spring AWS will release it. After `maxReceiveCount`, it lands in DLQ. Alternatively, one could catch and swallow exception to prevent immediate requeue, but that would mean message is considered successfully processed (which you likely don’t want). So usually, letting it throw is fine as framework handles the requeue. The main takeaway is that the exception is confined to this method; it doesn’t crash the whole application context.

By following these practices, the messaging part of the app becomes robust – capable of handling spikes and bad messages without requiring human intervention or container restarts. The system will effectively **self-heal** in the sense that it offloads troublesome tasks to DLQ and keeps chugging on new messages.

## 7. Error Isolation and Recovery Without Full Restarts

A hallmark of resilient systems is that they can recover from certain errors internally, without needing a complete restart (which in our case means avoiding the ECS task cycling). Here are strategies to achieve that:

### 7.1 Bulkhead Pattern (Isolate Components)

The **Bulkhead** pattern means partitioning your system so that a failure in one part doesn’t sink the whole ship (like compartments in a boat). In practice:

- Use separate thread pools for distinct tasks. For example, if your application does SQS processing and also serves an HTTP API (just hypothetical), give them separate pools so one doesn’t starve the other.
- Even within SQS processing, if you have different categories of messages, you could assign different pools or even separate ECS services for them. That way, if one type of message processing runs into trouble (e.g., external dependency down causing threads to hang), the others can continue.
- Limit resource usage per component. For instance, if a certain operation is known to be CPU heavy, you might want to run it at a controlled rate (like with a semaphore limit) so it doesn’t consume all CPU and freeze the health check.

Bulkheads in ECS context could also mean separate the work into multiple services or tasks. But assuming it’s one app, within the app we apply this by careful design of concurrency limits.

### 7.2 Circuit Breaker Pattern

A **Circuit Breaker** is typically used for calls to external services. If the external service is failing or slow, the circuit “opens” and the application skips or fails fast those calls for a while instead of hanging on them each time. How this helps:

- It prevents threads from piling up waiting on a service that is down (thus avoiding thread starvation).
- It avoids continuing to send traffic to a service that will error, giving it time to recover.

Libraries like Netflix Hystrix (now legacy, but Resilience4j is a popular alternative) implement circuit breakers. For example, wrapping a call to a payment API: if 10 calls in a row failed, then for the next minute, immediately fail (or return a fallback response) instead of attempting the API. After a cooldown, try again; if it succeeds, close the circuit.

In our scenario, if an external dependency is causing restarts (say a database that occasionally times out causing our app to throw exceptions widely), a circuit breaker could reduce the impact: the app could detect DB is down and stop trying for a bit, perhaps serve limited functionality or queue requests internally. The app remains alive (health check might even still pass if we report “DB down” but HTTP 200 for health since app is still running). When DB comes back, the circuit breaker closes and operations resume. This way, we avoided a death spiral of failing health checks and restarts for what was a transient issue.

### 7.3 Graceful Degradation

This ties to circuit breakers but more generally: design the app to **degrade** instead of crash when something goes wrong. For example:

- If cache service is unavailable, maybe serve data from database (slower but works) rather than throwing null pointer exceptions.
- If one module of the app (say optional analytics logging) fails, catch its exceptions and log it, but don’t let it take down the transaction path.
- In OSGi terms, perhaps if one bundle fails, the system could detect it and continue other operations that are not dependent on it. This requires your components to be decoupled enough. Perhaps provide a stub implementation when a bundle is not present (OSGi Service dynamics can allow a service to not be there; your code should handle that gracefully by, say, disabling related features).

### 7.4 Self-Monitoring and Restarting Components

Within a long-running app, you can sometimes program it to self-heal certain things:

- If a background thread encounters an irrecoverable error and dies, you could have a supervisor thread notice that and spawn a new thread to replace it. This is akin to how actor systems (like Akka) work: actors are supervised and can be restarted in the same JVM if they crash. Implementing this from scratch is complex, but for specific cases you might. For instance, a scheduler thread that polls SQS: if it ever stops (no log output for X seconds), you could detect that and start a new polling thread.
- If memory usage is creeping up, the app could proactively flush caches or call `System.gc()` (not usually effective for real leaks, but could help if it’s fragmentation).
- The app could detect if it's in an unhealthy state (e.g., an internal critical check fails) and take action. One drastic action could be to deliberately exit (triggering ECS to restart it). That sounds counter to “without restarting,” but sometimes a controlled suicide is better than a hung process. For example, using `ExitOnOutOfMemoryError` flag is essentially telling the JVM to die and restart rather than stay alive but useless. Some apps implement a “watchdog” that if certain conditions met (like can't connect to message queue for 10 minutes), they exit – allowing a fresh start. Use with caution: only as last resort after attempts to self-recover fail.

### 7.5 Sidecar for Specialized Tasks

Another form of isolation is moving certain functionality to a **sidecar container** in the same ECS task:

- If a particular library has a history of crashing the JVM (maybe a native library with a segfault risk), one strategy is to isolate that functionality in a separate process. For instance, instead of the Java app processing images (which might use native code), you run a separate image-processing microservice (even in the same task, or as a different service) and call it via HTTP/RPC. That way if it crashes, it doesn’t kill the main app.
- ECS tasks support multiple containers. If you have something that tends to fail often but can be quickly restarted, you could mark it as non-essential with a restart policy. ECS can then restart just that sidecar on failure without affecting the main app. (For example, a sidecar tailing a file and shipping logs might crash on a corner case log line; you can restart it in-place).

### 7.6 Example: Database Connection Failure

Let’s illustrate a full sequence: the app connects to a database and processes requests. If DB goes down:

- Without isolation: threads might hang on DB queries, the web endpoints time out, health check (if checking DB) fails, ECS restarts the container.
- With resilience: use a connection pool with timeout settings (so calls fail fast), and wrap calls with a circuit breaker. When DB is down, fail quickly and perhaps return a friendly error to the user (“Service temporarily unavailable, please try later”). The health check of the container might still return 200 OK because the app itself is running (perhaps we mark a health subcomponent as down but overall liveness as up). Meanwhile, a background thread keeps trying to get a connection occasionally. When DB comes back, everything resumes normally. **No container restart needed.**

The user experience degraded (couldn’t get data during downtime) but the system recovered by itself. This is preferable to thrashing containers which might drop state, cold start, etc.

In summary, not every error should translate to a process exit. Design your app to compartmentalize failures and recover internally when possible. ECS will handle the infrastructure restart if the app truly goes down, but we aim to handle as much as possible within the app to minimize those scenarios. This leads to higher uptime and less operational intervention.

## 8. Container Configuration Best Practices

Beyond code-level strategies, how you configure the container and the ECS task can greatly influence stability. Here are best practices for JVM settings, ECS resource limits, and container setup:

**8.1 JVM Flags and Settings:**

- **Heap Sizing:** As noted, set an explicit max heap (`-Xmx`). In container environments, starting Java 10+, the JVM will size the heap based on container memory by default. Still, many set `-Xmx` to be safe. Aim for \~70-80% of container memory for the heap to leave room for other memory (thread stacks, metaspace, direct buffers). For example, in a 2GB container, `-Xmx1536m` (1.5GB) is reasonable.
- **Garbage Collector:** Use a GC suitable for your workload. The default G1 GC is usually fine. If you have very large heaps and pause-sensitive, consider Shenandoah or ZGC (Java 11+ options). In most cases, tuning GC is not needed unless you see GC as a bottleneck (long pauses causing health timeouts). If you do tune, some flags: `-XX:MaxGCPauseMillis=<ms>` for G1 (as a hint), or enabling `-XX:+UseContainerSupport` (which is on by default in recent JDKs to respect cgroup limits).
- **Metaspace:** If you have tons of classes (e.g., OSGi with many bundles), monitor metaspace. You can set `-XX:MaxMetaspaceSize` to a prudent limit (though if you hit it, you get OOM). It might be better to let it grow but ensure container has headroom.
- **Dump on OOM:** Always add `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof`. If an OOM occurs, you get a heap dump in `/tmp` (or another path). Ensure your task definition has access to persistent storage (EFS volume, etc.) or at least that `/tmp` has space. The dump can be large, but if you have EFS or host volume, it can be retained after container death for analysis.
- **Exit on OOM:** Consider `-XX:+ExitOnOutOfMemoryError` (Java 8u92+). This flag forces the JVM to terminate on OOM rather than sometimes struggling along. This plays well with ECS: ECS will then immediately restart the container (if in a service). It’s better than a hung process that might require manual intervention.
- **CPU Settings:** The JVM will detect available CPUs (by default the CPU shares given to the container). If you give 1 vCPU, Java sees 1 available processor. If using CPU shares (not an integer CPU), Java might see a fraction. There was an issue historically where Java would see fewer CPUs than available in containers, but with modern Java and proper CPU quota settings it should accurately reflect. If needed, you can override CPU count seen by Java with `-XX:ActiveProcessorCount=<N>`.
- **Thread Stack Size:** As discussed, default is 1MB per thread. If you expect thousands of threads (which is unusual, but say you use virtual threads or highly concurrent design), you could lower `-Xss256k` or `512k`. Test thoroughly; too low can cause StackOverflow errors in deep call stacks.

Let’s summarize some JVM options in a table:

| **Setting**           | **Recommendation**                                                                                  | **Reason**                                                |
| --------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Heap Size (`-Xmx`)    | \~75-80% of container memory or use `MaxRAMPercentage`.                                             | Leave headroom for off-heap memory, avoid OOM.            |
| GC Algorithm          | Use default (G1) unless specific issues, then consider ZGC/Shenandoah.                              | G1 is balanced for most; low-pause GCs for special cases. |
| OOM Handling          | Enable heap dump and consider `ExitOnOutOfMemoryError`.                                             | Aids diagnostics and ensures quick recovery on OOM.       |
| Metaspace             | Monitor; set `MaxMetaspaceSize` if needed (e.g., limit to 256m).                                    | Prevent runaway metaspace in case of classloader leaks.   |
| Thread Stack (`-Xss`) | Default 1m (consider 512k if many threads and shallow stacks).                                      | More threads within same memory; trade-off depth.         |
| JIT/Code Cache        | Usually no change needed. (If CPU constrained, you could limit JIT threads with `CICompilerCount`). | Only tune if profiling shows JIT causing issues.          |

It’s often best to keep JVM settings as default as possible and change one thing at a time when tuning.

**8.2 ECS Task Resource Limits:**

- **Memory vs MemoryReservation:** In your task def, `memory` is the hard limit (container is killed if exceeded) and `memoryReservation` is a soft limit (reservation). For example, you might set `memoryReservation=512` and `memory=1024` (MB). The container can use up to 1024MB, but ECS will try to pack containers on an instance such that at least 512MB is accounted for this container. If you omit reservation, it’s the same as setting it equal to memory (hard limit). Soft limits are useful when you want to over-provision a bit on a host for bursts. Hard limit is critical to avoid host OOM. Generally: **always set a hard memory limit** to catch leaks and protect the host.
- **CPU:** With EC2 launch type, if you don’t specify CPU units, your container can use up to the whole host CPU (contention decided by shares). It’s good to specify CPU units (e.g., 512 units = 0.5 vCPU) so that ECS can schedule and account for CPU. It also enables CPU isolation if needed (if you use CPU limits). For a Java app, giving it some headroom beyond expected is wise – CPU starvation can cause slow responses and trigger health fail.
- **ulimits:** As mentioned, you can set `nofile` (max open files) and `nproc` (max processes/threads). For Java, `nofile` might need increase if it opens many files or network connections. `nproc` can prevent fork bombs or thread explosion. For example, you might set `nproc=1024` for safety (this counts threads + processes).
- **Disk (Ephemeral Storage):** By default, Fargate tasks have limited ephemeral storage (like 20GB), and EC2 tasks use host storage. If your app writes a lot (temporary files, logs if not shipped), ensure the host or volume has capacity. In EC2 launch type, you can mount EBS or use instance store. Consider using persistent storage (EFS) for any large or important data the app generates, instead of container’s ephemeral filesystem.
- **Networking:** If using awsvpc mode (each task gets an ENI), ensure the EC2 instance has enough network capacity (ENI limits, bandwidth). If high network traffic, monitor ECS metrics for bytes in/out.

**8.3 Container Launch and Lifecycle:**

- **Entry Point and Shutdown:** Use a proper entry point script if needed to capture TERM signal. For instance, with `exec java ...` so that the Java process gets the signal. If using stock OpenJDK image, it handles signals correctly. If you wrap java in a shell script, double-check you use `exec`.
- **Health Check in Task Def:** Configure as discussed: a reasonable command like `CMD-SHELL curl -f http://localhost:8080/health || exit 1`, with interval, timeout, retries, startPeriod tuned to your app. This ensures ECS can replace hung tasks but not kill healthy ones mistakenly.
- **Sidecar Containers:** If you include sidecars (for logging, monitoring, etc.), mark non-critical ones as "essential=false" so that if they die, the task isn’t killed (unless you want that). Also add appropriate `dependsOn` in task def so they start before/with the main app if needed. E.g., a sidecar that fetches configs should start before app.
- **Logging Configuration:** Use JSON or structured logging if possible to ease analysis. Also make sure logs go to stdout/stderr or to a mounted volume that a sidecar can read. In ECS, simplest is stdout -> awslogs. Avoid writing huge logs to the container filesystem as it can fill up ephemeral disk.

**8.4 Retry Strategies (Outside App):**

- **ECS Service Retries:** If a task fails to start (maybe hits an error on bootstrap), ECS will retry. When deploying a new version, you can enable **ECS Deployment Circuit Breaker** which can auto-roll back a bad deployment if tasks keep failing to become healthy.
- **ECS Container Restart Policy:** A new feature allows a container to be auto-restarted X times before giving up. For example, if you have a non-critical failure that is transient, ECS can restart the container without dropping the task. In our single-container scenario, that’s similar to restarting the task, but it avoids going through the full task stop/start cycle (network reattachment, etc., might be slightly faster).
- **Exponential Backoff in Clients:** Ensure any AWS SDK clients (like SQS, DynamoDB) use retries with backoff. The AWS SDK v2 does so by default. This prevents hammering a service that is throttling errors and gives time for recovery. It also reduces likelihood of an error propagating up as an exception that could cause a crash.

**8.5 Use of Sidecars:**

Let's detail common sidecar uses relevant to Java ECS apps:

- _Monitoring Sidecar:_ e.g., Prometheus JMX Exporter – run it as a Java agent or as a sidecar that connects via JMX to the main app to pull metrics, and expose on an endpoint for scraping. This decouples metrics collection from the app process.
- _Logging Sidecar:_ Instead of writing to CloudWatch directly, some use a Fluent Bit/Fluentd sidecar to collect and forward logs (especially if needing to send to multiple destinations or do transformation). The main app just writes to stdout or a file, and the sidecar ships it.
- _Proxy/Service Mesh:_ In advanced setups, you might have an Envoy proxy sidecar for service mesh. This can add resilience (like Envoy can do some automatic retries, circuit breaking on the network level). But with ECS EC2, service mesh is less common than in Kubernetes, though AWS App Mesh does support ECS.
- _Debugging Sidecar:_ You could have a SSH or SSM Agent container in the task to allow debug access if exec wasn’t available. Or even a secondary shell container that shares the process namespace (not typical in ECS).
- _Database or Cache as sidecar:_ Rare in ECS to run a DB as sidecar (usually use AWS services instead), but sometimes a lightweight cache or an agent (like a local X-Ray daemon for tracing) might run alongside.

When using sidecars, allocate resources to them too. For example, if Fluent Bit uses \~50 MB, account that in memory (either include in the same task’s memory or define its own limit). It’s easy to forget that and then the main app OOMs because the sidecar also used memory under the hood.

In summary, treat the container like a mini VM: allocate CPU, memory wisely, set limits to prevent one container from affecting others on the host, and leverage ECS features (health checks, restart policies) to automatically recover from failures when they do occur. A well-configured container will be resilient and performant, and many potential restart causes will be preempted (for instance, simply having the correct memory limit and Xmx can prevent OOM restarts).

## 9. Monitoring and Alerting (CloudWatch, Prometheus, Grafana, Custom Metrics)

Proactive monitoring is essential to catch issues before they lead to restarts and to diagnose them quickly if they do. We have partially discussed this, but here we structure the monitoring and alerting setup:

### 9.1 Amazon CloudWatch Monitoring

**CloudWatch Metrics to Enable:**

- **ECS Cluster Metrics:** CPUReservation, MemoryReservation (how much of your cluster is used) – helps to know if you’re nearing capacity.
- **ECS Service Metrics:** Available in CloudWatch as custom metrics (e.g., `ServiceName/CPUUtilization`). Ensure **Container Insights** are enabled for ECS. This gives per-task metrics as well.
- **Infrastructure Metrics:** EC2 instance metrics (CPU, network, disk). If memory usage on EC2 is desired, you can install the CloudWatch Agent on the instances to report mem and disk.
- **SQS Metrics:** Monitor `ApproximateNumberOfMessagesVisible` (backlog length) and `ApproximateAgeOfOldestMessage`. If age of oldest message is growing, your processing is lagging behind.
- **SQS DLQ Metrics:** As mentioned, any `NumberOfMessagesSent` to DLQ or visible messages in DLQ > 0 should trigger an alarm.

**CloudWatch Alarms & Actions:**

- Set thresholds for above metrics. E.g., Alarm if CPU > 80% for 5 minutes (could indicate runaway thread or insufficient capacity – consider scaling or investigating). Alarm if Memory > 90%. Alarm if messages in DLQ >= 1.
- You can configure EventBridge rules to detect ECS task failures. For instance, there's an event pattern for ECS Task State Change to STOPPED with desired reasons. You could catch a pattern where `stoppedReason` contains "OutOfMemoryError" and trigger an SNS notification to immediately alert that a task died of OOM.
- Use CloudWatch **Anomaly Detection** on metrics like memory or CPU if baseline is known, to catch unusual patterns automatically.
- If using AWS CloudWatch Synthetics (canaries), you can create heartbeat canaries that periodically hit your app’s endpoint from outside to ensure it's reachable (though this overlaps with ALB health checks).

**CloudWatch Logs Insights:** This is a feature to run queries on logs. You could set up queries to find occurrences of certain exceptions. For example, a query for all `ERROR` logs in last 5 minutes. While not exactly real-time alert (though you can create CloudWatch Logs alerts based on number of occurrences of a pattern), it’s great for rapid analysis after the fact. You can also create a dashboard widget showing log error counts.

### 9.2 Prometheus and Grafana

**Prometheus Setup on ECS:** You have a few options:

- Run Prometheus on one of the EC2 instances or a separate instance, and configure ECS tasks to **publish metrics** to it. Because ECS tasks may come and go and have dynamic IPs, you can use service discovery: AWS ECS can be integrated via **AWS SD** in Prometheus (it can call AWS APIs to find tasks by service). Alternatively, run a sidecar in each task that pushes metrics to a gateway.
- The simplest might be using CloudWatch as the data source with managed Grafana, but if Prom/Graf is preferred: AWS offers **Amazon Managed Prometheus** (AMP) and **Amazon Managed Grafana**. With AMP, you can use AWS DIscovery to automatically scrape ECS tasks. This is a bit advanced to set up but very powerful (no need to maintain your own Prom server).
- Expose metrics from the app: e.g., if using Spring Boot Actuator, `/actuator/prometheus` endpoint can produce Prom metrics. Ensure network access (if Prom is external, the tasks need to be in a security group that Prom can reach).

**Grafana Dashboards:** Grafana can combine CloudWatch and Prometheus data. For ECS, you might have a dashboard showing:

- Task count over time.
- CPU/Memory for each task or average.
- SQS queue length.
- Garbage collection metrics (if using Prometheus via Micrometer, you can get jvm_gc_pause and count).
- Custom app metrics (e.g., number of messages processed per minute, error count per minute).

**Custom Metrics in CloudWatch:** If not using Prometheus, you can push your own metrics to CloudWatch using the AWS SDK (`PutMetricData`). For example, publish a metric "ActiveThreads" or "QueueProcessingTime". However, doing this for many metrics can be tedious. Often, it’s easier to either rely on Prometheus or use a library like Dropwizard Metrics + CloudWatch reporter, or Micrometer with CloudWatch registry. Micrometer (used in Spring Boot) can send a batch of metrics to CloudWatch periodically. Be mindful of CloudWatch costs (it charges per metric). Prometheus might be more cost-effective if you have many metrics and high churn.

**Example Custom Metric Push (pseudo-code):**

```java
AmazonCloudWatch cw = AmazonCloudWatchClientBuilder.defaultClient();
Dimension svcDim = new Dimension().withName("ServiceName").withValue("OrderService");
MetricDatum datum = new MetricDatum()
    .withMetricName("OrdersProcessed")
    .withUnit(StandardUnit.Count)
    .withValue((double) ordersProcessedInLastInterval)
    .withDimensions(svcDim)
    .withTimestamp(new Date());
PutMetricDataRequest req = new PutMetricDataRequest()
    .withNamespace("MyApplication")
    .withMetricData(datum);
cw.putMetricData(req);
```

You’d run something like that periodically (maybe from a scheduled task). CloudWatch then stores it, and you can alarm on it or graph it. In this example, a sudden drop in OrdersProcessed metric could alert you something’s wrong (consumers stuck).

**Alerting**: Connect alerts to on-call or notification channels (email, Slack, etc.). Use AWS SNS or PagerDuty integrations for critical alarms (like app down or task restarted too many times). It's also useful to set up a dashboard big screen where the team can see system health at a glance.

### 9.3 End-to-End Tracing (Bonus)

While not explicitly asked, a note on distributed tracing: If your app calls other microservices or databases, implementing tracing (AWS X-Ray or OpenTelemetry) is very helpful. X-Ray, for instance, can time each segment (SQS receive, processing, DB calls) and if a segment is erroring or slow, you spot it. It can even show that a particular message caused a fault.

X-Ray can be used by running the X-Ray daemon as a sidecar or using AWS Distro for OpenTelemetry (ADOT) collector. The app then sends trace data to that, which relays to X-Ray service. In X-Ray console, you’d see a service map and can detect anomalies like increased error rates or latency, which might be precursors to container issues.

### 9.4 Continuous Improvement

Set up **regular reviews of metrics and alerts**. After each incident (or false alarm), refine thresholds. Maybe you got alerted for high CPU at 80% but that’s normal during daily batch processing – bump threshold to 90% or use anomaly detection. Or maybe a restart happened with no alarm – see what metric could be tied to it and add one. Over time, you’ll build a robust monitoring system that gives you high confidence.

Remember, monitoring not only helps in diagnosing restarts, it helps in preventing them by catching warning signs. For example, memory usage creeping up over days (memory leak) could be alerted when crossing a threshold, allowing a fix or proactive restart before a crash occurs.

## 10. Real-World Case Studies and Solutions

Finally, let’s look at some concrete case studies that encapsulate the themes discussed, and how they were resolved:

### Case Study 1: Memory Leak Causing OOM Restarts

**Scenario:** A Spring Boot application on ECS (EC2 launch type) began restarting roughly every 2 days. ECS stopped reasons showed “OutOfMemoryError: Container killed due to memory usage”. CloudWatch metrics indicated a slow but steady increase in memory usage over 48 hours until hitting the container’s 512MB limit, then a restart (exit 137). Logs did not show explicit OOM exceptions, indicating the OS killed the process.

**Diagnosis:** A heap dump was taken by enabling `HeapDumpOnOutOfMemoryError` and found a large number of objects of a certain class were never released. It turned out to be a cache (guava cache) that had no eviction policy – it kept growing as new entries were added. Each restart cleared the cache, making the problem cyclic.

**Solution:** Developers implemented an eviction policy (LRU with maximum size) on the cache. They also added a custom metric for cache size and an alert if it exceeds a threshold. After deploying the fix, memory usage stabilized. As additional safety, they increased container memory to 768MB and set an alarm on memory > 700MB to catch any future leaks early. The application no longer restarts unexpectedly; any memory growth would trigger an alert for investigation, preventing a crash.

### Case Study 2: Thread Pool Exhaustion from SQS Surge

**Scenario:** An order processing service using SQS experienced a surge of messages (10x normal volume) during a sale event. The single ECS task (2 vCPU, 4 GB) tried to handle all messages. It used an unbounded cached thread pool for processing. As thousands of messages arrived, it spawned \~2000 threads. The JVM eventually threw “unable to create new native thread” and some threads got stuck in DB calls. The health check timed out (app couldn’t respond while GC thrashing and context switching among thousands of threads), and ECS replaced the task.

**Diagnosis:** Logs and thread dump from before restart (obtained via CloudWatch Logs) revealed an enormous number of active threads all initiated from the SQS listener. Many were blocked on database inserts (the DB was overwhelmed too). The restart cleared the threads but when the new task came up, it attempted the same surge and would have likely repeated the failure if the surge hadn't subsided by then.

**Solution:** Multiple actions were taken:

- The thread pool was changed to a fixed size (e.g., 50 threads) to cap concurrency and avoid runaway creation.
- ECS service auto-scaling was enabled based on queue length. Now if queue > 500 messages, scale out another task (and similarly scale in when low). In a subsequent event, they had 5 tasks consuming, each with 50 threads max, instead of 1 task with 2000 threads.
- Implemented backpressure: if DB is slow, the app now uses a RateLimiter to slow down retrieval from SQS (so it doesn’t fetch thousands more messages when it can’t even process current ones).
- The combination of these prevented thread exhaustion. In later high-volume events, the system processed gradually with no crashes. The queue backlog went up but was steadily worked off as tasks scaled out, and no health check failures occurred.

### Case Study 3: Misconfigured Health Check Causing Restart Loop

**Scenario:** A microservice was deployed behind an Application Load Balancer. The ECS task had a health check command that curled an internal `/health` endpoint. The `/health` endpoint, unfortunately, was doing an extensive check including querying the database and an external API. During periods when the DB or API was slow, the `/health` call exceeded its 2-second timeout, causing the health check to fail. ECS marked the task unhealthy and killed it. At one point, a minor network blip to the external API caused _all_ tasks to cycle out as unhealthy within a few minutes, even though the API issue was transient.

**Diagnosis:** CloudWatch showed Target Group health fluctuating and ECS events indicated tasks stopped for health check failures. Logs showed the health endpoint hanging at the external API call. Essentially, the app was _too strict_ in declaring itself unhealthy due to a dependency issue.

**Solution:** They redefined the health check strategy:

- The `/health` endpoint was split into `/health/liveness` and `/health/readiness`. The liveness check only returns OK if the app’s internal state is good (e.g., main thread up, not in an error loop), and it ignores external dependencies. Readiness check still checks DB/API and returns more detailed info.
- The ECS/ALB health check was pointed to the liveness endpoint (which is very lightweight and unlikely to ever time out unless the app is truly hung).
- Thus, if the DB is down, the app stays running (liveness OK, readiness FAIL). The team can get alerted via a separate readiness monitor or the app’s logs, but ECS won’t kill the container. This allowed the app to ride through transient outages. If the DB outage was prolonged, they could decide to recycle tasks manually, but importantly it was under their control, not an automated loop.
- Additionally, they increased the health check timeout to 5s and retries to 5, giving more leeway.

After this change, no more restart loops occurred. In one instance later, the external API went down for 5 minutes – the app threads handling those calls logged errors, the readiness reported FAIL (seen on a dashboard), but the ECS tasks stayed running and reconnect logic eventually recovered when the API came back.

### Case Study 4: OSGi Bundle Failure on Startup

**Scenario:** An OSGi-based service packaged via Apache Karaf was containerized. On a new deployment, the container would repeatedly start and then stop after \~30 seconds. ECS logs showed `Essential container exited with code 1`. The Karaf logs (in CloudWatch) showed an exception: one bundle failed to start due to a missing configuration file, causing a `RuntimeException` in its Activator. Karaf’s behavior (in this setup) was to call System.exit when startup failed (since it was running in server mode). This meant the Java process exited whenever that bundle misfired.

**Diagnosis:** They identified the missing configuration (the bundle expected a config in Karaf’s etc directory which wasn’t provided in the container image). The System.exit call was part of Karaf’s handling of certain fatal errors (could be configured, but by default it shut down the container if boot features fail).

**Solution:** They provided the required configuration file via the container image (and also made it possible to override via environment if needed). They also adjusted the Karaf start script to not exit on boot feature failure, allowing the process to stay up even if a bundle failed (so that they could manually fix or at least get a shell). After adding the config, the bundle started successfully and the service stayed up. This case underscored the importance of testing container images in an environment identical to production: the missing config was caught quickly in staging.

Additionally, they implemented a **startup probe** script outside ECS: basically a script that tried to start the app container locally and verify all bundles Active. This caught such issues before pushing to ECS.

---

These case studies highlight how different issues manifest and how a combination of approaches – code fixes, configuration tweaks, and AWS features – resolve them. A common theme is **visibility**: in each case, having logs, metrics, and error messages was crucial to root cause analysis. Then, applying the principles discussed (memory management, proper concurrency control, health check tuning, robust OSGi config) led to the solutions.

## Conclusion

In this guide, we covered the architecture of Java applications on ECS with EC2, common causes of unexpected restarts, and a wide array of strategies to diagnose and prevent them. To recap a few key takeaways:

- **Know Your Lifecycle:** Understanding ECS task lifecycle and how ECS interacts (health checks, signals) with your app helps you design your app (and its Docker image) to shut down and start up cleanly, avoiding unnecessary restarts.
- **Resource Management:** Memory and threads are common culprits. Use the tools at your disposal (JVM options, ECS limits, monitoring) to prevent leaks and catch issues early. Configure CPU/memory in ECS so that your app has enough room but is contained if something goes wrong.
- **Robust Coding Practices:** In your Spring/OSGi app, handle exceptions, use timeouts, and don’t assume everything will always be available. That way a hiccup doesn’t turn into a crash. Utilize Spring Boot features for graceful shutdown and health checks wisely.
- **AWS Integration:** Leverage CloudWatch for logs and metrics; set up DLQs for SQS; use auto-scaling to handle load rather than brute-forcing one container to do everything. AWS provides many mechanisms (like DLQ, scaling policies, Circuit Breaker for deployments) to improve resiliency – use them.
- **Observability:** It cannot be overstated – invest in good monitoring (CloudWatch, Prometheus, etc.). It will pay off when diagnosing that 3 AM incident or, even better, alert you to a problem during business hours before it becomes an outage.
- **Test and Tune:** The first deployment of an app to ECS might expose new behavior (different from running on a VM). Do load testing and chaos testing if possible. Induce failures (stop DB, overflow queue) in a controlled environment to see how your app and ECS react, then adjust accordingly (maybe increase a timeout, add a catch, etc.).

With the above practices, you can significantly reduce the frequency of unexpected restarts. And when a restart does happen, you’ll have the information needed to quickly pinpoint why and address it. The result is a more resilient, self-healing Java application that can run reliably on AWS ECS, delivering the uptime and performance your users expect.
